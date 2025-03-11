from fastapi import APIRouter
from app.routes.endpoints.auth import router as auth_router
from app.routes.endpoints.users import router as user_router

routers = APIRouter()
router_list = [auth_router, user_router]

for router in router_list:
    routers.include_router(router)