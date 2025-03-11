import bcrypt
import base64
from fastapi import HTTPException
from app.core import security 
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterSchema, LoginSchema
from app.core.exceptions import DuplicatedError, InternalServerError

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def sign_up(self, user: RegisterSchema) -> dict:
        existing_user = self.user_repository.get_by_email(user.email)
        if existing_user is not None:
            raise DuplicatedError("User with this email already exists")

        hashed_password = self.hash_password(user.password)
        
        user_create = RegisterSchema(
            name=user.name,
            email=user.email,
            password=hashed_password
        )
        created_user = self.user_repository.create(user_create)
        if created_user is None:
            raise InternalServerError("Failed to create user. Please try again later")

        return {
            "message": "User Registered Successfully"
        }

    def sign_in(self, credentials: LoginSchema) -> dict:
        user = self.user_repository.get_by_email(credentials.email)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not self.verify_password(credentials.password, user.get("password", "")):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = security.create_access_token(
            data={"sub": user["id"]}
        )

        refresh_token = security.create_refresh_token(
            data={"sub": user["id"]}
        )

        return {
            "message": "User Logged In Successfully",
            "token": {
                "token_type": "bearer",
                "access_token": access_token,
                "refresh_token": refresh_token
            },
        }

    def sign_out(self) -> dict:
        return {"message": "Successfully signed out"}

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return base64.b64encode(hashed).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            hashed_bytes = base64.b64decode(hashed_password)
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_bytes)
        except Exception:
            return False
