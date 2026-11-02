from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset


T = TypeVar("T", bound="AppStatusLabels")


@attr.s(auto_attribs=True)
class AppStatusLabels:
    """Labels assigned to the App

    ### Example:
    `{'app.kubernetes.io/instance': 'local', 'app.kubernetes.io/name': 'my-service', 'os-alias': 'my-service', 'os-
            ancestor': 'od-c2-d2-e61', 'os-app-id': 'od-c2-d2-e61', 'os-deployment-id': 'od-c2-d2-e61', 'os-entity-id':
            'e61b7226-b3ac-4974-b9f7-66f4eda5b51d', 'os-instance-type': 'normal', 'os-needs-ingress': 'true', 'os-ontology':
            'os_ontology_v1', 'os-username': 'admin', 'os-workload-type': 'frontend', 'os-workspace':
            'd2cc4d61-3f0a-499f-a867-75bfd29a1d08'}

    """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        app_status_labels = cls()

        app_status_labels.additional_properties = d
        return app_status_labels

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
