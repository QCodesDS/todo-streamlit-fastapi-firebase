from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials
from google.cloud import firestore
import os

# Init Firebase Admin với emulator
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "127.0.0.1:9099"
os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {"projectId": "todo-streamlit-fastapi"})
db = firestore.Client(project="todo-streamlit-fastapi")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: xác thực token
async def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        decoded = auth.verify_id_token(token)
        return decoded["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# Auth routes
from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/register")
async def register(body: AuthRequest):
    try:
        user = auth.create_user(email=body.email, password=body.password)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
async def login(body: AuthRequest):
    import requests as req
    url = "http://127.0.0.1:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=fake-api-key"
    res = req.post(url, json={
        "email": body.email,
        "password": body.password,
        "returnSecureToken": True
    })
    data = res.json()
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"]["message"])
    return {"idToken": data["idToken"], "uid": data["localId"]}

# Todo routes
class TodoRequest(BaseModel):
    title: str
    done: bool = False

@app.get("/todos")
async def get_todos(uid: str = Depends(get_current_user)):
    todos_ref = db.collection("todos").where("uid", "==", uid).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in todos_ref]

@app.post("/todos")
async def create_todo(body: TodoRequest, uid: str = Depends(get_current_user)):
    doc_ref = db.collection("todos").document()
    doc_ref.set({"title": body.title, "done": body.done, "uid": uid})
    return {"id": doc_ref.id, "title": body.title, "done": body.done}

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, body: TodoRequest, uid: str = Depends(get_current_user)):
    doc_ref = db.collection("todos").document(todo_id)
    doc_ref.update({"title": body.title, "done": body.done})
    return {"id": todo_id, "title": body.title, "done": body.done}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, uid: str = Depends(get_current_user)):
    db.collection("todos").document(todo_id).delete()
    return {"message": "Deleted"}