from typing import Dict

from elmax_api.model.endpoint import DeviceEndpoint


class Group(DeviceEndpoint):
    """Representation of a Group configuration"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str):
        super().__init__(endpoint_id=endpoint_id, visible=visible, index=index, name=name)

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Group':
        """Create a new group configuration object from the API json response"""
        group = Group(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
        )
        return group
