from typing import Dict


class DeviceEndpoint:
    def __init__(self, endpoint_id: str, visible: bool, index: int, name: str):
        self._endpoint_id = endpoint_id
        self._visible = visible
        self._index = index
        self._name = name

    @property
    def endpoint_id(self) -> str:
        return self._endpoint_id

    @property
    def visible(self) -> bool:
        return self._visible

    @property
    def index(self) -> int:
        return self._index

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other):
        return self.endpoint_id == other.endpoint_id and \
               self.visible==other.visible and \
                self.index==other.index and \
                self.name==other.name

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'DeviceEndpoint':
        """Create a new area configuration object from the API json response"""
        endpoint = DeviceEndpoint(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
        )
        return endpoint
