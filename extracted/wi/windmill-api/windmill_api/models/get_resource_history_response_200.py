from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_resource_history_response_200_versions_item import GetResourceHistoryResponse200VersionsItem


T = TypeVar("T", bound="GetResourceHistoryResponse200")


@_attrs_define
class GetResourceHistoryResponse200:
    """
    Attributes:
        versions (List['GetResourceHistoryResponse200VersionsItem']):
        versioned (bool):
    """

    versions: List["GetResourceHistoryResponse200VersionsItem"]
    versioned: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        versions = []
        for versions_item_data in self.versions:
            versions_item = versions_item_data.to_dict()

            versions.append(versions_item)

        versioned = self.versioned

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "versions": versions,
                "versioned": versioned,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_resource_history_response_200_versions_item import GetResourceHistoryResponse200VersionsItem

        d = src_dict.copy()
        versions = []
        _versions = d.pop("versions")
        for versions_item_data in _versions:
            versions_item = GetResourceHistoryResponse200VersionsItem.from_dict(versions_item_data)

            versions.append(versions_item)

        versioned = d.pop("versioned")

        get_resource_history_response_200 = cls(
            versions=versions,
            versioned=versioned,
        )

        get_resource_history_response_200.additional_properties = d
        return get_resource_history_response_200

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
