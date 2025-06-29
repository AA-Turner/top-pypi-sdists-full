from pydantic import BaseModel, Field

class ServiceConfigurations(BaseModel):
    key: str = Field(..., description="Service's key")
    name: str = Field(..., description="Service's name")
    host: str = Field(..., description="Service's host")
    port: int = Field(..., description="Service's port")