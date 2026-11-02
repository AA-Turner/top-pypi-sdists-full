from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDevWorkspaceResponse200")


@_attrs_define
class GetDevWorkspaceResponse200:
    """
    Attributes:
        id (str):
        name (str):
        dev_workspace_label (Union[Unset, None, str]): Environment label, e.g. 'dev' or 'staging'; null defaults to
            'dev'
    """

    id: str
    name: str
    dev_workspace_label: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        dev_workspace_label = self.dev_workspace_label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if dev_workspace_label is not UNSET:
            field_dict["dev_workspace_label"] = dev_workspace_label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        dev_workspace_label = d.pop("dev_workspace_label", UNSET)

        get_dev_workspace_response_200 = cls(
            id=id,
            name=name,
            dev_workspace_label=dev_workspace_label,
        )

        get_dev_workspace_response_200.additional_properties = d
        return get_dev_workspace_response_200

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
