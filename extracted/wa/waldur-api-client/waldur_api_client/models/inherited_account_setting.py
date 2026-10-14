from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_setting_source import AccountSettingSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="InheritedAccountSetting")


@_attrs_define
class InheritedAccountSetting:
    """
    Attributes:
        value (Union[Unset, str]): The value the setting resolves to.
        source (Union[Unset, AccountSettingSource]):
    """

    value: Union[Unset, str] = UNSET
    source: Union[Unset, AccountSettingSource] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, AccountSettingSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = AccountSettingSource(_source)

        inherited_account_setting = cls(
            value=value,
            source=source,
        )

        inherited_account_setting.additional_properties = d
        return inherited_account_setting

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
