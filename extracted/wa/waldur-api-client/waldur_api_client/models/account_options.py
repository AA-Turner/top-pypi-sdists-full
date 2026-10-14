from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_scope import AccountScope
from ..models.blank_enum import BlankEnum
from ..models.username_generation_policy_enum import UsernameGenerationPolicyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountOptions")


@_attrs_define
class AccountOptions:
    """
    Attributes:
        account_scope (Union[AccountScope, BlankEnum, Unset]): Where accounts are held: 'offering' keeps one account per
            offering (the historical behaviour); 'provider' shares one account per user across the provider's offerings.
        username_generation_policy (Union[BlankEnum, Unset, UsernameGenerationPolicyEnum]): How the usernames of
            offering users are generated.
        username_anonymized_prefix (Union[Unset, str]): Prefix for anonymized usernames; the name is the prefix followed
            by the account's POSIX UID.
        homedir_prefix (Union[Unset, str]): Prefix of each account's home directory; the username follows.
        login_shell (Union[Unset, str]): Login shell assigned to GLAuth/LDAP accounts.
    """

    account_scope: Union[AccountScope, BlankEnum, Unset] = UNSET
    username_generation_policy: Union[BlankEnum, Unset, UsernameGenerationPolicyEnum] = UNSET
    username_anonymized_prefix: Union[Unset, str] = UNSET
    homedir_prefix: Union[Unset, str] = UNSET
    login_shell: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_scope: Union[Unset, str]
        if isinstance(self.account_scope, Unset):
            account_scope = UNSET
        elif isinstance(self.account_scope, AccountScope):
            account_scope = self.account_scope.value
        else:
            account_scope = self.account_scope.value

        username_generation_policy: Union[Unset, str]
        if isinstance(self.username_generation_policy, Unset):
            username_generation_policy = UNSET
        elif isinstance(self.username_generation_policy, UsernameGenerationPolicyEnum):
            username_generation_policy = self.username_generation_policy.value
        else:
            username_generation_policy = self.username_generation_policy.value

        username_anonymized_prefix = self.username_anonymized_prefix

        homedir_prefix = self.homedir_prefix

        login_shell = self.login_shell

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
        d = dict(src_dict)

        def _parse_account_scope(data: object) -> Union[AccountScope, BlankEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                account_scope_type_0 = AccountScope(data)

                return account_scope_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            account_scope_type_1 = BlankEnum(data)

            return account_scope_type_1

        account_scope = _parse_account_scope(d.pop("account_scope", UNSET))

        def _parse_username_generation_policy(data: object) -> Union[BlankEnum, Unset, UsernameGenerationPolicyEnum]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                username_generation_policy_type_0 = UsernameGenerationPolicyEnum(data)

                return username_generation_policy_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            username_generation_policy_type_1 = BlankEnum(data)

            return username_generation_policy_type_1

        username_generation_policy = _parse_username_generation_policy(d.pop("username_generation_policy", UNSET))

        username_anonymized_prefix = d.pop("username_anonymized_prefix", UNSET)

        homedir_prefix = d.pop("homedir_prefix", UNSET)

        login_shell = d.pop("login_shell", UNSET)

        account_options = cls(
            account_scope=account_scope,
            username_generation_policy=username_generation_policy,
            username_anonymized_prefix=username_anonymized_prefix,
            homedir_prefix=homedir_prefix,
            login_shell=login_shell,
        )

        account_options.additional_properties = d
        return account_options

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
