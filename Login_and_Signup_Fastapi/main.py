from fastapi import FastAPI
from routers import user
from fastapi import Depends
from dependencies import get_current_user 


app = FastAPI()

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Login System"}



@app.get("/dashboard")
def dashboard(current_user: str = Depends(get_current_user)):
    return {"message": f"Welcome {current_user}!"}
