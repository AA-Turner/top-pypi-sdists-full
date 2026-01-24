from pydantic import UUID4, BaseModel


class IntegrationResponse(BaseModel):
    name: str
    id: UUID4


class CreateIntegrationRequest(BaseModel):
    name: str
    data: dict
