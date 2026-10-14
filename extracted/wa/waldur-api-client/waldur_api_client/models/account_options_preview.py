from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_options_versions import AccountOptionsVersions
    from ..models.offering_account_preview import OfferingAccountPreview


T = TypeVar("T", bound="AccountOptionsPreview")


@_attrs_define
class AccountOptionsPreview:
    """
    Attributes:
        account_options (AccountOptionsVersions):
        warnings (list[str]): Things to settle before saving, e.g. a missing group range.
        offerings (list['OfferingAccountPreview']):
        renamed (int):
        provider_accounts_kept (int):
        accounts_keeping_home_or_shell (int):
        username_conflicts (int): People whose usernames disagree across offerings. Non-zero blocks switching to per
            service provider accounts.
    """

    account_options: "AccountOptionsVersions"
    warnings: list[str]
    offerings: list["OfferingAccountPreview"]
    renamed: int
    provider_accounts_kept: int
    accounts_keeping_home_or_shell: int
    username_conflicts: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_options = self.account_options.to_dict()

        warnings = self.warnings

        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        renamed = self.renamed

        provider_accounts_kept = self.provider_accounts_kept

        accounts_keeping_home_or_shell = self.accounts_keeping_home_or_shell

        username_conflicts = self.username_conflicts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_options": account_options,
                "warnings": warnings,
                "offerings": offerings,
                "renamed": renamed,
                "provider_accounts_kept": provider_accounts_kept,
                "accounts_keeping_home_or_shell": accounts_keeping_home_or_shell,
                "username_conflicts": username_conflicts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_options_versions import AccountOptionsVersions
        from ..models.offering_account_preview import OfferingAccountPreview

        d = dict(src_dict)
        account_options = AccountOptionsVersions.from_dict(d.pop("account_options"))

        warnings = cast(list[str], d.pop("warnings"))

        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = OfferingAccountPreview.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        renamed = d.pop("renamed")

        provider_accounts_kept = d.pop("provider_accounts_kept")

        accounts_keeping_home_or_shell = d.pop("accounts_keeping_home_or_shell")

        username_conflicts = d.pop("username_conflicts")

        account_options_preview = cls(
            account_options=account_options,
            warnings=warnings,
            offerings=offerings,
            renamed=renamed,
            provider_accounts_kept=provider_accounts_kept,
            accounts_keeping_home_or_shell=accounts_keeping_home_or_shell,
            username_conflicts=username_conflicts,
        )

        account_options_preview.additional_properties = d
        return account_options_preview

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
