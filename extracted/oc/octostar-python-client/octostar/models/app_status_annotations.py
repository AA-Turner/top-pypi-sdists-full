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


T = TypeVar("T", bound="AppStatusAnnotations")


@attr.s(auto_attribs=True)
class AppStatusAnnotations:
    """Annotations for the app

    ### Example:
    `{'deployment.kubernetes.io/revision': '1', 'os-app-name': 'MyAPP', 'os-app-title': 'MyAPP is awesome', 'os-
            manifest': '...', 'os-ontology': 'os_ontology_v1', 'os-username': 'admin'}

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
        app_status_annotations = cls()

        app_status_annotations.additional_properties = d
        return app_status_annotations

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
