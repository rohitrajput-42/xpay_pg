from fastapi import FastAPI, Request
import uvicorn
from routes import users
from services.user import get_users, create_user

app = FastAPI()


@app.get("/get_user/{user_id}")
def get_users_list(request:Request, user_id: str):
    return get_users(request, user_id)

@app.post("/registration")
async def create_new_user(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        payload = {}
    return create_user(request,payload)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="debug" , host = "0.0.0.0" , reload= True)