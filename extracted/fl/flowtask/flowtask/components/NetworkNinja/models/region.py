from typing import Any
from datamodel import BaseModel, Field

class Region(BaseModel):
    region_id: str = Field(required=False, alias='id')
    region_name: str = Field(required=False, alias='name')
    is_active: bool = Field(required=False, alias='active')
    client_id: int
    orgid: int

    class Meta:
        name: str = 'regions'
        schema: str = 'networkninja'
        strict: bool = True

# def create_region(
#     name: str,
#     value: Any,
#     target_type: Any,
#     parent_data: BaseModel
# ) -> Region:
#     client_id = parent_data.get('client_id', None) if parent_data else None
#     print('Parent Data: ', name, value, target_type, client_id)
#     # return target_type(**args)
#     return Region(region_id='1', region_name='Test Region')

# # TODO: To be implemented in Datamodel.
# BaseModel.register_parser(Region, create_region, 'region_name')
