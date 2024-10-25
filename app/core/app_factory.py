from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings
settings = Settings()

class FastAPIApp:
    def __init__(self):
        self.app = FastAPI()
        self.add_middleware()
        self.include_routers()
        self.add_root_router()

    def add_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def include_routers(self):
        from ..apis.routers import router as api_router
        self.app.include_router(api_router, tags=['apis'])

    def add_root_router(self):
        @self.app.get("/", tags=['root'])
        async def root():
            return {'message': 'Hello World'}
        
    def get_app(self):
        self.app.title = settings.PROJECT_NAME
        return self.app