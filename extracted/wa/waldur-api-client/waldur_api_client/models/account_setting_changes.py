from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_setting_change import AccountSettingChange


T = TypeVar("T", bound="AccountSettingChanges")


@_attrs_define
class AccountSettingChanges:
    """
    Attributes:
        account_scope (AccountSettingChange):
        username_generation_policy (AccountSettingChange):
        username_anonymized_prefix (AccountSettingChange):
        homedir_prefix (AccountSettingChange):
        login_shell (AccountSettingChange):
    """

    account_scope: "AccountSettingChange"
    username_generation_policy: "AccountSettingChange"
    username_anonymized_prefix: "AccountSettingChange"
    homedir_prefix: "AccountSettingChange"
    login_shell: "AccountSettingChange"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_scope = self.account_scope.to_dict()

        username_generation_policy = self.username_generation_policy.to_dict()

        username_anonymized_prefix = self.username_anonymized_prefix.to_dict()

        homedir_prefix = self.homedir_prefix.to_dict()

        login_shell = self.login_shell.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_scope": account_scope,
                "username_generation_policy": username_generation_policy,
                "username_anonymized_prefix": username_anonymized_prefix,
                "homedir_prefix": homedir_prefix,
                "login_shell": login_shell,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_setting_change import AccountSettingChange

        d = dict(src_dict)
        account_scope = AccountSettingChange.from_dict(d.pop("account_scope"))

        username_generation_policy = AccountSettingChange.from_dict(d.pop("username_generation_policy"))

        username_anonymized_prefix = AccountSettingChange.from_dict(d.pop("username_anonymized_prefix"))

        homedir_prefix = AccountSettingChange.from_dict(d.pop("homedir_prefix"))

        login_shell = AccountSettingChange.from_dict(d.pop("login_shell"))

        account_setting_changes = cls(
            account_scope=account_scope,
            username_generation_policy=username_generation_policy,
            username_anonymized_prefix=username_anonymized_prefix,
            homedir_prefix=homedir_prefix,
            login_shell=login_shell,
        )

        account_setting_changes.additional_properties = d
        return account_setting_changes

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
