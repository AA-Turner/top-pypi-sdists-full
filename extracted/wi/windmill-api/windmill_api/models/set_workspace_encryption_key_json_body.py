from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetWorkspaceEncryptionKeyJsonBody")


@_attrs_define
class SetWorkspaceEncryptionKeyJsonBody:
    """
    Attributes:
        new_key (str):
        skip_reencrypt (Union[Unset, bool]):
    """

    new_key: str
    skip_reencrypt: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_key = self.new_key
        skip_reencrypt = self.skip_reencrypt

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_key": new_key,
            }
        )
        if skip_reencrypt is not UNSET:
            field_dict["skip_reencrypt"] = skip_reencrypt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_key = d.pop("new_key")

        skip_reencrypt = d.pop("skip_reencrypt", UNSET)

        set_workspace_encryption_key_json_body = cls(
            new_key=new_key,
            skip_reencrypt=skip_reencrypt,
        )

        set_workspace_encryption_key_json_body.additional_properties = d
        return set_workspace_encryption_key_json_body

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
