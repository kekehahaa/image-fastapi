import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_HOST: str
    PROJECT_PORT: int
    DB_PATH: str
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", '..', '.env')
    )

settings = Settings()

if __name__ == "__main__":
    print(settings.DB_PATH)