from typing import Dict

from elmax_api.model.cover_status import CoverStatus
from elmax_api.model.endpoint import DeviceEndpoint


class Cover(DeviceEndpoint):
    """Representation of a cover"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 position: int,
                 status: CoverStatus):
        super().__init__(endpoint_id=endpoint_id, visible=visible, index=index, name=name)
        self._position = position
        self._status = status

    @property
    def position(self) -> int:
        return self._position

    @property
    def status(self) -> CoverStatus:
        return self._status

    def __eq__(self, other):
        super_equals = super().__eq__(other)
        if not super_equals:
            return False
        return self.position == other.position and self.status == other.status

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Cover':
        """Create a new cover object from the API json response"""
        cover = Cover(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            position=response_entry.get('posizione'),
            status=CoverStatus(response_entry['stato'])
        )
        return cover
