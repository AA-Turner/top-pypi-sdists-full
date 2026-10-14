from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.inherited_account_setting import InheritedAccountSetting


T = TypeVar("T", bound="AccountSettingChange")


@_attrs_define
class AccountSettingChange:
    """
    Attributes:
        before (InheritedAccountSetting):
        after (InheritedAccountSetting):
    """

    before: "InheritedAccountSetting"
    after: "InheritedAccountSetting"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        before = self.before.to_dict()

        after = self.after.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "before": before,
                "after": after,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inherited_account_setting import InheritedAccountSetting

        d = dict(src_dict)
        before = InheritedAccountSetting.from_dict(d.pop("before"))

        after = InheritedAccountSetting.from_dict(d.pop("after"))

        account_setting_change = cls(
            before=before,
            after=after,
        )

        account_setting_change.additional_properties = d
        return account_setting_change

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
