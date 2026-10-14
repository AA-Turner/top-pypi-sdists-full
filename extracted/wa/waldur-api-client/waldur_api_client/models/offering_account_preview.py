from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_example import AccountExample
    from ..models.account_rename import AccountRename
    from ..models.account_setting_changes import AccountSettingChanges


T = TypeVar("T", bound="OfferingAccountPreview")


@_attrs_define
class OfferingAccountPreview:
    """
    Attributes:
        uuid (str):
        name (str):
        settings (AccountSettingChanges):
        changed (list[str]):
        example (AccountExample):
        renames (list['AccountRename']):
        provider_accounts_kept (int): Provider accounts that keep their username and POSIX values.
        accounts_keeping_home_or_shell (int): Existing accounts that keep their home directory and login shell; the
            change applies to accounts created afterwards.
    """

    uuid: str
    name: str
    settings: "AccountSettingChanges"
    changed: list[str]
    example: "AccountExample"
    renames: list["AccountRename"]
    provider_accounts_kept: int
    accounts_keeping_home_or_shell: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        settings = self.settings.to_dict()

        changed = self.changed

        example = self.example.to_dict()

        renames = []
        for renames_item_data in self.renames:
            renames_item = renames_item_data.to_dict()
            renames.append(renames_item)

        provider_accounts_kept = self.provider_accounts_kept

        accounts_keeping_home_or_shell = self.accounts_keeping_home_or_shell

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "settings": settings,
                "changed": changed,
                "example": example,
                "renames": renames,
                "provider_accounts_kept": provider_accounts_kept,
                "accounts_keeping_home_or_shell": accounts_keeping_home_or_shell,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_example import AccountExample
        from ..models.account_rename import AccountRename
        from ..models.account_setting_changes import AccountSettingChanges

        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        settings = AccountSettingChanges.from_dict(d.pop("settings"))

        changed = cast(list[str], d.pop("changed"))

        example = AccountExample.from_dict(d.pop("example"))

        renames = []
        _renames = d.pop("renames")
        for renames_item_data in _renames:
            renames_item = AccountRename.from_dict(renames_item_data)

            renames.append(renames_item)

        provider_accounts_kept = d.pop("provider_accounts_kept")

        accounts_keeping_home_or_shell = d.pop("accounts_keeping_home_or_shell")

        offering_account_preview = cls(
            uuid=uuid,
            name=name,
            settings=settings,
            changed=changed,
            example=example,
            renames=renames,
            provider_accounts_kept=provider_accounts_kept,
            accounts_keeping_home_or_shell=accounts_keeping_home_or_shell,
        )

        offering_account_preview.additional_properties = d
        return offering_account_preview

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
