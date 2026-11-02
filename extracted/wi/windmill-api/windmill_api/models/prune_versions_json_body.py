from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.prune_versions_json_body_resource_type import PruneVersionsJsonBodyResourceType

T = TypeVar("T", bound="PruneVersionsJsonBody")


@_attrs_define
class PruneVersionsJsonBody:
    """
    Attributes:
        resource_type (PruneVersionsJsonBodyResourceType):
    """

    resource_type: PruneVersionsJsonBodyResourceType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resource_type = self.resource_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_type": resource_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        resource_type = PruneVersionsJsonBodyResourceType(d.pop("resource_type"))

        prune_versions_json_body = cls(
            resource_type=resource_type,
        )

        prune_versions_json_body.additional_properties = d
        return prune_versions_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
