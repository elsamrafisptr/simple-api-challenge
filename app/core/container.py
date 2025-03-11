from dependency_injector import containers, providers
from app.core.database import db
from app.repositories.users import UserRepository
from app.services.auth import AuthService
from app.services.users import UserService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.routes.endpoints.users",
            "app.routes.endpoints.auth",
            "app.core.dependencies",
        ]
    )

    firebase_db = providers.Singleton(lambda: db)

    user_repository = providers.Factory(UserRepository, db=firebase_db)

    user_service = providers.Factory(UserService, user_repository=user_repository)
    auth_service = providers.Factory(AuthService, user_repository=user_repository)
