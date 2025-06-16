from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_db_name: str = Field(..., env="MONGO_DB_NAME")
    mongo_collection_name: str = Field(..., env="MONGO_COLLECTION_NAME")
    mongo_tool_collection: str = Field(..., env="MONGO_TOOL_COLLECTION")
    secret_key: str = Field(..., env="SECRET_KEY")
    credential_db: str = "credential_db"
    credential_collection: str = "credentials"

    class Config:
        env_file = ".env"

settings = Settings()
