from fastapi import APIRouter , Query , Request, Depends
from services.user import get_users, create_user


router = APIRouter(
    prefix="/users",
    tags=["USERS"],
)

@router.get("")
def get_users_list(request:Request):
    return get_users(request)

@router.post("")
async def create_new_user(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        payload = {}
    return create_user(request,payload)