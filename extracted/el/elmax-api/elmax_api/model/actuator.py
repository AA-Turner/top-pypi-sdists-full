from typing import Dict

from elmax_api.model.endpoint import DeviceEndpoint


class Actuator(DeviceEndpoint):
    """Representation of an actuator"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 opened: bool):
        super().__init__(endpoint_id=endpoint_id, visible=visible, index=index, name=name)
        self._opened = opened

    @property
    def opened(self) -> bool:
        return self._opened

    def __eq__(self, other):
        super_equals = super().__eq__(other)
        if not super_equals:
            return False
        return self.opened == other.opened

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Actuator':
        """Create a new actuator object from the API json response"""
        actuator = Actuator(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            opened=response_entry.get('aperta')
        )
        return actuator
