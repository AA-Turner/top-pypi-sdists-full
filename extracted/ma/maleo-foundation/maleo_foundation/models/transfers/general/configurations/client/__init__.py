from pydantic import BaseModel, Field
from .maleo import MaleoClientsConfigurations

class ClientConfigurations(BaseModel):
    maleo: MaleoClientsConfigurations = Field(..., description="Maleo client's configurations")

    class Config:
        arbitrary_types_allowed=True