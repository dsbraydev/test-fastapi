from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# DUMMY DATA
todo_list = [
    {"id": 1, "title": "Gym", "description": "Go to the Gym", "completed": False},
    {"id": 2, "title": "Reading", "description": "Read a min of 10 pages a day", "completed": False},
    {"id": 3, "title": "Diet", "description": "Did you eat healthy today", "completed": True},
]

class Task(BaseModel):
    title: str
    description: str
    completed: bool

class TaskWithID(Task):
    id: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do List API!"}

# ALL TASKS
@app.get("/tasks", response_model=List[TaskWithID])
def get_tasks():
    return todo_list

# GET TASK
@app.get("/tasks/{task_id}", response_model=TaskWithID)
def get_task(task_id: int):
    for task in todo_list:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# CREATE TASK
@app.post("/tasks", response_model=TaskWithID)
def create_task(task: Task):
    new_id = max([task["id"] for task in todo_list], default=0) + 1
    new_task = task.dict()
    new_task["id"] = new_id
    todo_list.append(new_task)
    return new_task

# UPDATE TASK
@app.put("/tasks/{task_id}", response_model=TaskWithID)
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(todo_list):
        if task["id"] == task_id:
            todo_list[index].update(updated_task.dict())
            todo_list[index]["id"] = task_id  # Ensure ID remains unchanged
            return todo_list[index]
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE TASK
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(todo_list):
        if task["id"] == task_id:
            deleted_task = todo_list.pop(index)
            return {"message": "Task deleted", "task": deleted_task}
    raise HTTPException(status_code=404, detail="Task not found")
