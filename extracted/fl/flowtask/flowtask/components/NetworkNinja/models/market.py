from datamodel import BaseModel, Field
from .abstract import AbstractPayload

class Market(AbstractPayload):
    market_id: str = Field(required=False, alias='id')
    market_name: str = Field(required=False, alias='name')
    district_id: int
    region_id: int
    client_id: int
    orgid: int
    is_active: bool = Field(required=False, alias='active', default=True)

    class Meta:
        name: str = 'markets'
        schema: str = 'networkninja'
        strict: bool = True
