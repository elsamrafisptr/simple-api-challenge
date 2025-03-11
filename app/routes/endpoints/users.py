from fastapi import APIRouter, Depends, HTTPException, Query, status
from dependency_injector.wiring import Provide
from app.core.container import Container
from app.middlewares.middleware import inject
from app.core.dependencies import get_current_user
from app.schemas.users import UserUpdate
from app.services.users import UserService

router = APIRouter(prefix="/users", tags=["user"])

@router.get("/")
@inject
def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
    sort: str = Query("created_at"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: dict = Depends(get_current_user)
):
    users = service.get_all_users(page=page, limit=limit, sort=sort, order=order)
    return {
        "message": "Users retrieved successfully",
        "data": users["results"],
        "pagination": {
            "current_page": page,
            "total_pages": users["total_pages"],
            "total_items": users["total_items"],
        },
    }

@router.get("/email/{email}")
@inject
def get_user_by_email(
    email: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: dict = Depends(get_current_user)
):
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user:
        user["password"] = None

    return {"message": "User retrieved successfully", "data": user}

@router.get("/id/{user_id}")
@inject
def get_user_by_id(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: dict = Depends(get_current_user)
):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user:
        user["password"] = None

    return {"message": "User retrieved successfully", "data": user}


@router.get("/me", response_model_exclude_none=True)
@inject
def get_current_user_info(
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: dict = Depends(get_current_user)
):
    user = service.get_user_by_id(current_user["id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "User retrieved successfully", "data": user}

@router.put("/{user_id}")
@inject
def update_user(
    user_id: str,
    user_data: UserUpdate,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: dict = Depends(get_current_user)
):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    updated_user = service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Updated User not found")

    return {"message": "User retrieved successfully", "data": updated_user}

@router.delete("/{user_id}")
@inject
def delete_user(
    user_id: str,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: dict = Depends(get_current_user)
):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    deleted_user = service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not deleted")

    return {"message": "User Deleted Successfully"}