from typing import List, Optional
from fastapi import HTTPException
from app.repositories.users import UserRepository
from app.schemas.users import UserUpdate, UserResponse

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self, page: int, limit: int, sort: str, order: str) -> List[UserResponse]:
        users = self.user_repository.get_all()
        if sort in users[0]:
            reverse = True if order == "desc" else False
            users = sorted(users, key=lambda x: x.get(sort, ""), reverse=reverse)
        else:
            raise ValueError(f"Invalid sort field: {sort}") 

        total_items = len(users)
        total_pages = (total_items + limit - 1) // limit
        offset = (page - 1) * limit
        paginated_users = users[offset : offset + limit]
        return {
            "results": paginated_users,
            "total_items": total_items,
            "total_pages": total_pages,
        }

    def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.user_repository.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, user_id: str, user: UserUpdate) -> Optional[UserResponse]:
        updated_user = self.user_repository.update(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found or update failed")
        return UserResponse(**updated_user)

    def delete_user(self, user_id: str) -> bool:
        deleted = self.user_repository.delete(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found or deletion failed")
        return True
