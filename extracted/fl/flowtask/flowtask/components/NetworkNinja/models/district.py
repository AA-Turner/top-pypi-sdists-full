from datamodel import BaseModel, Field


class District(BaseModel):
    district_id: str = Field(required=False, alias='id')
    district_name: str = Field(required=False, alias='name')
    is_active: bool = Field(required=False, alias='active')
    client_id: int
    orgid: int

    class Meta:
        name: str = 'districts'
        schema: str = 'networkninja'
        strict: bool = True
