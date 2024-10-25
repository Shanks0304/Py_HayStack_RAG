from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    PROJECT_NAME: str
    UPLOAD_DIR: str
    class Config:
        env_file = ".env"

