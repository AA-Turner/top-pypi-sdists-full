from typing import Dict, List

from elmax_api.model.alarm_status import AlarmStatus, AlarmArmStatus
from elmax_api.model.endpoint import DeviceEndpoint


class Area(DeviceEndpoint):
    """Representation of an Area configuration"""

    def __init__(self,
                 endpoint_id: str,
                 visible: bool,
                 index: int,
                 name: str,
                 status: AlarmStatus,
                 armed_status: AlarmArmStatus,
                 available_statuses: List[AlarmStatus],
                 available_arm_statuses: List[AlarmArmStatus]):
        super().__init__(endpoint_id=endpoint_id, visible=visible, index=index, name=name)
        self._status = status
        self._armed_status = armed_status
        self._available_arm_statuses = available_arm_statuses
        self._available_statuses = available_statuses

    @property
    def available_arm_statuses(self) -> List[AlarmArmStatus]:
        """
        Supported list of available alarm arm-statutes
        Returns:

        """
        return self._available_arm_statuses

    @property
    def available_statuses(self) -> List[AlarmStatus]:
        """
        Supported list of available alarm statuses
        Returns:

        """
        return self._available_statuses

    @property
    def status(self) -> AlarmStatus:
        """
        Current alarm status.

        Returns: `AlarmStatus`

        """
        return self._status

    @property
    def armed_status(self) -> AlarmArmStatus:
        """
        Current alarm arm status

        Returns: `AlarmArmStatus`

        """
        return self._armed_status

    def __eq__(self, other):
        super_equals = super().__eq__(other)
        if not super_equals:
            return False
        return self.status == other.status and self.armed_status == other.armed_status and self.available_arm_statuses == other.available_arm_statuses and self.available_statuses == other.available_statuses

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'Area':
        """Create a new area configuration object from the API json response"""
        area = Area(
            endpoint_id=response_entry.get('endpointId'),
            visible=response_entry.get('visibile'),
            index=response_entry.get('indice'),
            name=response_entry.get('nome'),
            status=AlarmStatus(response_entry['statoSessione']),
            armed_status=AlarmArmStatus(response_entry['stato']),
            available_statuses=[ AlarmStatus(a) for a in response_entry['statiSessioneDisponibili'] ],
            available_arm_statuses=[AlarmArmStatus(a) for a in response_entry['statiDisponibili']]
        )
        return area
