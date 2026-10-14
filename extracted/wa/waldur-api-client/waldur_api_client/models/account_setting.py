from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_setting_source import AccountSettingSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inherited_account_setting import InheritedAccountSetting


T = TypeVar("T", bound="AccountSetting")


@_attrs_define
class AccountSetting:
    """
    Attributes:
        value (Union[Unset, str]): The value the setting resolves to.
        source (Union[Unset, AccountSettingSource]):
        inherited (Union[Unset, InheritedAccountSetting]):
    """

    value: Union[Unset, str] = UNSET
    source: Union[Unset, AccountSettingSource] = UNSET
    inherited: Union[Unset, "InheritedAccountSetting"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        inherited: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.inherited, Unset):
            inherited = self.inherited.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if source is not UNSET:
            field_dict["source"] = source
        if inherited is not UNSET:
            field_dict["inherited"] = inherited

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inherited_account_setting import InheritedAccountSetting

        d = dict(src_dict)
        value = d.pop("value", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, AccountSettingSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = AccountSettingSource(_source)

        _inherited = d.pop("inherited", UNSET)
        inherited: Union[Unset, InheritedAccountSetting]
        if isinstance(_inherited, Unset):
            inherited = UNSET
        else:
            inherited = InheritedAccountSetting.from_dict(_inherited)

        account_setting = cls(
            value=value,
            source=source,
            inherited=inherited,
        )

        account_setting.additional_properties = d
        return account_setting

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
