from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.settings_summary_theme import SettingsSummaryTheme
from typing import cast






T = TypeVar("T", bound="SettingsSummary")



@_attrs_define
class SettingsSummary:
    """ The signed-in user's settings as `GET /api/v1/settings/summary` and the
    `get_settings` MCP tool return them: every field of
    SettingsResponse except `webhookToken` and `webhookSecret`, which are
    never part of it, plus `webhookConfigured`. No forge token appears,
    only whether one is set. Field meanings are those of the same-named
    SettingsResponse properties.

        Attributes:
            github_username (str):
            github_token_set (bool):
            github_app_installation_id (int):
            github_app_configured (bool):
            forgejo_url (str):
            forgejo_username (str):
            forgejo_token_set (bool):
            webhook_configured (bool): Whether this user's webhook token and secret exist. They are
                created the first time the Settings page reads
                `GET /api/v1/settings`, never by this read, so this is false for a
                user who has not opened Settings yet.
            renovate_rebase_label (str):
            renovate_authors (list[str]):
            hide_dependency_dashboard (bool):
            ignored_titles (list[str]):
            ignored_title_counts (list[int | None]):
            theme (SettingsSummaryTheme):
            timezone (str):
     """

    github_username: str
    github_token_set: bool
    github_app_installation_id: int
    github_app_configured: bool
    forgejo_url: str
    forgejo_username: str
    forgejo_token_set: bool
    webhook_configured: bool
    renovate_rebase_label: str
    renovate_authors: list[str]
    hide_dependency_dashboard: bool
    ignored_titles: list[str]
    ignored_title_counts: list[int | None]
    theme: SettingsSummaryTheme
    timezone: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        github_username = self.github_username

        github_token_set = self.github_token_set

        github_app_installation_id = self.github_app_installation_id

        github_app_configured = self.github_app_configured

        forgejo_url = self.forgejo_url

        forgejo_username = self.forgejo_username

        forgejo_token_set = self.forgejo_token_set

        webhook_configured = self.webhook_configured

        renovate_rebase_label = self.renovate_rebase_label

        renovate_authors = self.renovate_authors



        hide_dependency_dashboard = self.hide_dependency_dashboard

        ignored_titles = self.ignored_titles



        ignored_title_counts = []
        for ignored_title_counts_item_data in self.ignored_title_counts:
            ignored_title_counts_item: int | None
            ignored_title_counts_item = ignored_title_counts_item_data
            ignored_title_counts.append(ignored_title_counts_item)



        theme = self.theme.value

        timezone = self.timezone


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "githubUsername": github_username,
            "githubTokenSet": github_token_set,
            "githubAppInstallationId": github_app_installation_id,
            "githubAppConfigured": github_app_configured,
            "forgejoUrl": forgejo_url,
            "forgejoUsername": forgejo_username,
            "forgejoTokenSet": forgejo_token_set,
            "webhookConfigured": webhook_configured,
            "renovateRebaseLabel": renovate_rebase_label,
            "renovateAuthors": renovate_authors,
            "hideDependencyDashboard": hide_dependency_dashboard,
            "ignoredTitles": ignored_titles,
            "ignoredTitleCounts": ignored_title_counts,
            "theme": theme,
            "timezone": timezone,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        github_username = d.pop("githubUsername")

        github_token_set = d.pop("githubTokenSet")

        github_app_installation_id = d.pop("githubAppInstallationId")

        github_app_configured = d.pop("githubAppConfigured")

        forgejo_url = d.pop("forgejoUrl")

        forgejo_username = d.pop("forgejoUsername")

        forgejo_token_set = d.pop("forgejoTokenSet")

        webhook_configured = d.pop("webhookConfigured")

        renovate_rebase_label = d.pop("renovateRebaseLabel")

        renovate_authors = cast(list[str], d.pop("renovateAuthors"))


        hide_dependency_dashboard = d.pop("hideDependencyDashboard")

        ignored_titles = cast(list[str], d.pop("ignoredTitles"))


        ignored_title_counts = []
        _ignored_title_counts = d.pop("ignoredTitleCounts")
        for ignored_title_counts_item_data in (_ignored_title_counts):
            def _parse_ignored_title_counts_item(data: object) -> int | None:
                if data is None:
                    return data
                return cast(int | None, data)

            ignored_title_counts_item = _parse_ignored_title_counts_item(ignored_title_counts_item_data)

            ignored_title_counts.append(ignored_title_counts_item)


        theme = SettingsSummaryTheme(d.pop("theme"))




        timezone = d.pop("timezone")

        settings_summary = cls(
            github_username=github_username,
            github_token_set=github_token_set,
            github_app_installation_id=github_app_installation_id,
            github_app_configured=github_app_configured,
            forgejo_url=forgejo_url,
            forgejo_username=forgejo_username,
            forgejo_token_set=forgejo_token_set,
            webhook_configured=webhook_configured,
            renovate_rebase_label=renovate_rebase_label,
            renovate_authors=renovate_authors,
            hide_dependency_dashboard=hide_dependency_dashboard,
            ignored_titles=ignored_titles,
            ignored_title_counts=ignored_title_counts,
            theme=theme,
            timezone=timezone,
        )


        settings_summary.additional_properties = d
        return settings_summary

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
