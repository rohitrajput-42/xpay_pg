from fastapi import APIRouter
from endpoints.user import router as users

routers = APIRouter()
router_list = [users]

for router in router_list:
    routers.include_router(router)