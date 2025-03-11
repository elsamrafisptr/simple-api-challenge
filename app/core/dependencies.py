import jwt
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.config import configs
from app.core.container import Container
from app.services.users import UserService

@inject
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service: UserService = Depends(Provide[Container.user_service])
):
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            configs.JWT_SECRET_KEY,
            algorithms=["HS256"],
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing 'sub' field",
            )

        print(f"User ID from token: {user_id}")

        current_user = service.get_user_by_id(user_id)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or token invalid",
            )

        return current_user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

