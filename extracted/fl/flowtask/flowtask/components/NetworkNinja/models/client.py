from datamodel import BaseModel, Field
from .abstract import AbstractPayload
from .organization import Organization


class Client(AbstractPayload):
    client_id: int = Field(required=False)
    client_name: str
    status: bool = Field(required=True, default=True)
    orgid: int = Field(required=False)
    program_id: int = Field(required=False)
    program_name: str
    program_slug: str

    class Meta:
        name: str = 'clients'
        schema: str = 'networkninja'
        strict: bool = True
        as_objects: bool = True
