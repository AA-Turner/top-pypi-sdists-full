from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListWorkspaceMacrosResponse200Item")


@_attrs_define
class ListWorkspaceMacrosResponse200Item:
    """
    Attributes:
        name (str):
        params (str): verbatim parameter list
        body (str): verbatim body after AS [TABLE]
        is_table (bool):
        provider_path (str): path of the `// macros` library script
    """

    name: str
    params: str
    body: str
    is_table: bool
    provider_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        params = self.params
        body = self.body
        is_table = self.is_table
        provider_path = self.provider_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "params": params,
                "body": body,
                "is_table": is_table,
                "provider_path": provider_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        params = d.pop("params")

        body = d.pop("body")

        is_table = d.pop("is_table")

        provider_path = d.pop("provider_path")

        list_workspace_macros_response_200_item = cls(
            name=name,
            params=params,
            body=body,
            is_table=is_table,
            provider_path=provider_path,
        )

        list_workspace_macros_response_200_item.additional_properties = d
        return list_workspace_macros_response_200_item

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
