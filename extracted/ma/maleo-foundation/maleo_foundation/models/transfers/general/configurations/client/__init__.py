from pydantic import BaseModel, ConfigDict, Field
from .maleo import MaleoClientsConfigurations

class ClientConfigurations(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    maleo: MaleoClientsConfigurations = Field(default_factory=MaleoClientsConfigurations, description="Maleo client's configurations")