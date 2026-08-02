from typing import Dict

from elmax_api.model.endpoint import DeviceEndpoint


class Zone(DeviceEndpoint):
    """Representation of a zone configuration"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 opened: bool,
                 excluded: bool):
        super().__init__(endpoint_id=endpoint_id, visible=visible, index=index, name=name)
        self._opened = opened
        self._excluded = excluded

    @property
    def opened(self) -> bool:
        return self._opened

    @property
    def excluded(self) -> bool:
        return self._excluded

    def __eq__(self, other):
        super_equals = super().__eq__(other)
        if not super_equals:
            return False
        return self.opened==other.opened and self.excluded==other.excluded

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Zone':
        """Create a new zone configuration object from the API json response"""
        zone = Zone(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            opened=response_entry.get('aperta'),
            excluded=response_entry.get('esclusa')
        )
        return zone
