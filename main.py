from fastapi import FastAPI, HTTPException
from auth import users_info, hash_password, verify_password
from pydantic import BaseModel

app = FastAPI()

tasks = []


class RegisterRequest(BaseModel):
    email: str
    password: str
    

class LoginRequest(BaseModel):
    email: str
    password: str
    
    
    

@app.get("/home")
def home():
    return "It's a homepage"



@app.post("/register", status_code=201)
def register(user : RegisterRequest):
    
    if user.email in users_info:
        raise HTTPException(
            status_code = 409,
            detail="user already exist"
        )
        
    hashed = hash_password(user.password)
    users_info[user.email] = hashed

    return {
        "message": "User registered successfully",
        "email": user.email
    }
    
     
     
@app.post("login",status_code=200)
def login(user: LoginRequest):
    
    if user.email not in users_info:
        raise HTTPException(
            status_code=401,
            detail="user not found"
        )

    
    if verify_password(user.password, users_info[user.email]):
        return {"message": "login successful"}
    else:
        raise HTTPException(
            status_code=401,
            detail="incorrect password"
        )



@app.post("/create_task", status_code=201)
def create_task(task: str):
    
    if not task.strip():
        raise HTTPException(
            status_code=400,
            detail="Task cannot be empty"
        )
    
    tasks.append(task)
    return {
        "message": "task created successfully",
        "task": task
    }
    
    
    
@app.get("/view_all_tasks")
def view_task():
    print("Here are your all tasks")
    return tasks



@app.delete("/delete_task/{index}")
def delete_task(index: int):
    if index < 0 or index >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = tasks.pop(index)
    
    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }
    
    
    
@app.get("/get_single_task/{index}")
def get_single_task(index : int):
    if index < 0 or index >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "index": index, "task:": tasks[index]
    }
    
    
    
@app.put("/update_task/{index}/{new_task}")
def update_task(index : int, new_task: str):
    if index < 0 or index >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found");

    tasks[index] = new_task
    
    return {
        f"task updated at index: {index}" : tasks[index]
    }