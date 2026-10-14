from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account_setting import AccountSetting


T = TypeVar("T", bound="OfferingAccountSettings")


@_attrs_define
class OfferingAccountSettings:
    """
    Attributes:
        account_scope (Union[Unset, AccountSetting]):
        username_generation_policy (Union[Unset, AccountSetting]):
        username_anonymized_prefix (Union[Unset, AccountSetting]):
        homedir_prefix (Union[Unset, AccountSetting]):
        login_shell (Union[Unset, AccountSetting]):
    """

    account_scope: Union[Unset, "AccountSetting"] = UNSET
    username_generation_policy: Union[Unset, "AccountSetting"] = UNSET
    username_anonymized_prefix: Union[Unset, "AccountSetting"] = UNSET
    homedir_prefix: Union[Unset, "AccountSetting"] = UNSET
    login_shell: Union[Unset, "AccountSetting"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_scope: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.account_scope, Unset):
            account_scope = self.account_scope.to_dict()

        username_generation_policy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.username_generation_policy, Unset):
            username_generation_policy = self.username_generation_policy.to_dict()

        username_anonymized_prefix: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.username_anonymized_prefix, Unset):
            username_anonymized_prefix = self.username_anonymized_prefix.to_dict()

        homedir_prefix: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.homedir_prefix, Unset):
            homedir_prefix = self.homedir_prefix.to_dict()

        login_shell: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.login_shell, Unset):
            login_shell = self.login_shell.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_scope is not UNSET:
            field_dict["account_scope"] = account_scope
        if username_generation_policy is not UNSET:
            field_dict["username_generation_policy"] = username_generation_policy
        if username_anonymized_prefix is not UNSET:
            field_dict["username_anonymized_prefix"] = username_anonymized_prefix
        if homedir_prefix is not UNSET:
            field_dict["homedir_prefix"] = homedir_prefix
        if login_shell is not UNSET:
            field_dict["login_shell"] = login_shell

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_setting import AccountSetting

        d = dict(src_dict)
        _account_scope = d.pop("account_scope", UNSET)
        account_scope: Union[Unset, AccountSetting]
        if isinstance(_account_scope, Unset):
            account_scope = UNSET
        else:
            account_scope = AccountSetting.from_dict(_account_scope)

        _username_generation_policy = d.pop("username_generation_policy", UNSET)
        username_generation_policy: Union[Unset, AccountSetting]
        if isinstance(_username_generation_policy, Unset):
            username_generation_policy = UNSET
        else:
            username_generation_policy = AccountSetting.from_dict(_username_generation_policy)

        _username_anonymized_prefix = d.pop("username_anonymized_prefix", UNSET)
        username_anonymized_prefix: Union[Unset, AccountSetting]
        if isinstance(_username_anonymized_prefix, Unset):
            username_anonymized_prefix = UNSET
        else:
            username_anonymized_prefix = AccountSetting.from_dict(_username_anonymized_prefix)

        _homedir_prefix = d.pop("homedir_prefix", UNSET)
        homedir_prefix: Union[Unset, AccountSetting]
        if isinstance(_homedir_prefix, Unset):
            homedir_prefix = UNSET
        else:
            homedir_prefix = AccountSetting.from_dict(_homedir_prefix)

        _login_shell = d.pop("login_shell", UNSET)
        login_shell: Union[Unset, AccountSetting]
        if isinstance(_login_shell, Unset):
            login_shell = UNSET
        else:
            login_shell = AccountSetting.from_dict(_login_shell)

        offering_account_settings = cls(
            account_scope=account_scope,
            username_generation_policy=username_generation_policy,
            username_anonymized_prefix=username_anonymized_prefix,
            homedir_prefix=homedir_prefix,
            login_shell=login_shell,
        )

        offering_account_settings.additional_properties = d
        return offering_account_settings

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
