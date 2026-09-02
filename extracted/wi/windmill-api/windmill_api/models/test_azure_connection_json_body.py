from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TestAzureConnectionJsonBody")


@_attrs_define
class TestAzureConnectionJsonBody:
    """
    Attributes:
        azure_resource_path (str):
    """

    azure_resource_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        azure_resource_path = self.azure_resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "azure_resource_path": azure_resource_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        azure_resource_path = d.pop("azure_resource_path")

        test_azure_connection_json_body = cls(
            azure_resource_path=azure_resource_path,
        )

        test_azure_connection_json_body.additional_properties = d
        return test_azure_connection_json_body

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
