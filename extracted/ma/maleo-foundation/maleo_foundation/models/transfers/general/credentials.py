from pydantic import BaseModel, Field
from uuid import UUID

class MaleoCredentials(BaseModel):
    id: int = Field(..., description="ID")
    uuid: UUID = Field(..., description="UUID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")