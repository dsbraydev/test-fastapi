from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the To-Do List API!"}

def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["title"] == "Gym"

def test_get_single_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Gym"

    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_create_task():
    new_task = {
        "title": "Learn FastAPI",
        "description": "Build a CRUD app",
        "completed": False
    }
    response = client.post("/tasks", json=new_task)
    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["title"] == new_task["title"]

def test_update_task():
    updated_task = {
        "title": "Gym 2",
        "description": "Go to the gym!!!",
        "completed": True
    }
    response = client.put("/tasks/1", json=updated_task)
    assert response.status_code == 200
    assert response.json()["title"] == "Gym 2"

    response = client.put("/tasks/999", json=updated_task)
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"

    response = client.delete("/tasks/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_post_and_delete_task():
    new_task = {
        "title": "DELETE",
        "description": "delete task",
        "completed": False
    }
    response = client.post("/tasks", json=new_task)
    assert response.status_code == 200
    created_task = response.json()

    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json()["task"]["id"] == created_task["id"]
