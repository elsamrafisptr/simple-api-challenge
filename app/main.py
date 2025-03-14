from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import configs
from app.routes.routes import routers as v1_routers
from app.utils.pattern import singleton
from app.core.container import Container

app = FastAPI()

@singleton
class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title=configs.PROJECT_NAME,
            version="0.1.0",
        )

        self.container = Container()
        self.db = self.container.firebase_db()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        @self.app.get("/")
        def root():
            return {"message": f"Welcome to {configs.PROJECT_NAME}"}
        
        self.app.include_router(v1_routers, prefix="/api/v1")
        
app_instance = App()
app = app_instance.app