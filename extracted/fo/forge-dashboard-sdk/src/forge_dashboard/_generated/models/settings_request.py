from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SettingsRequest")



@_attrs_define
class SettingsRequest:
    """ Replaces the signed-in user's saved GitHub/Forgejo configuration.
    A blank `githubToken` or `forgejoToken` keeps whatever token is
    already saved for that forge rather than clearing it — this is
    the only way to update the username fields without having to
    resubmit a token you don't want to re-paste. githubAppInstallationId
    is different: a plain replace like githubUsername, not coalesced —
    0 or omitted really does disconnect the App. Rejected (400) if
    the server has no GitHub App configured (see
    SettingsResponse.githubAppConfigured). Theme isn't settable
    here at all — see PUT /api/v1/settings/theme.

        Attributes:
            github_token (str | Unset):
            github_username (str | Unset):
            github_app_installation_id (int | Unset): 0 means none. A negative or non-integer value is a 400 naming
                this field, as is any value on a server with no GitHub App
                configured.
            forgejo_url (str | Unset): Required, once the save is merged with what is already stored,
                whenever a Forgejo token or username is set. That depends on
                stored state, so a schema alone can't express it: a save that
                breaks it is a 400 naming `forgejoUrl`.

                Must be a plain `http://` or `https://` base URL with a host,
                optionally with a path prefix. One that carries a username,
                password, query string or fragment, or has another scheme, is a
                400 naming `forgejoUrl`, and nothing is saved. The error never
                repeats the URL.
            forgejo_token (str | Unset):
            forgejo_username (str | Unset):
            renovate_rebase_label (str | Unset):
            renovate_authors (list[str] | Unset): Replaces the saved list. Entries are trimmed; blanks and
                repeats (ignoring case) are dropped. Omitted or empty clears it.
            hide_dependency_dashboard (bool | Unset): Replaces the saved choice; omitted means false, like
                `renovateAuthors`, so a form sends it on every save. See
                SettingsResponse.hideDependencyDashboard.
            ignored_titles (list[str] | Unset): Replaces the saved list; omitted or empty clears it. Entries are
                trimmed; blanks and repeats (ignoring case) are dropped. Each
                must compile as a Go RE2 regular expression: one that does not
                is a 400 naming `ignoredTitles` and the entry, with the reason in
                plain words ("ignoredTitles entry 2, "(": missing closing )"),
                and nothing is saved. More than 20 entries, or an entry over 200
                characters, is a 400 too. See SettingsResponse.ignoredTitles.
     """

    github_token: str | Unset = UNSET
    github_username: str | Unset = UNSET
    github_app_installation_id: int | Unset = UNSET
    forgejo_url: str | Unset = UNSET
    forgejo_token: str | Unset = UNSET
    forgejo_username: str | Unset = UNSET
    renovate_rebase_label: str | Unset = UNSET
    renovate_authors: list[str] | Unset = UNSET
    hide_dependency_dashboard: bool | Unset = UNSET
    ignored_titles: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        github_token = self.github_token

        github_username = self.github_username

        github_app_installation_id = self.github_app_installation_id

        forgejo_url = self.forgejo_url

        forgejo_token = self.forgejo_token

        forgejo_username = self.forgejo_username

        renovate_rebase_label = self.renovate_rebase_label

        renovate_authors: list[str] | Unset = UNSET
        if not isinstance(self.renovate_authors, Unset):
            renovate_authors = self.renovate_authors



        hide_dependency_dashboard = self.hide_dependency_dashboard

        ignored_titles: list[str] | Unset = UNSET
        if not isinstance(self.ignored_titles, Unset):
            ignored_titles = self.ignored_titles




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if github_token is not UNSET:
            field_dict["githubToken"] = github_token
        if github_username is not UNSET:
            field_dict["githubUsername"] = github_username
        if github_app_installation_id is not UNSET:
            field_dict["githubAppInstallationId"] = github_app_installation_id
        if forgejo_url is not UNSET:
            field_dict["forgejoUrl"] = forgejo_url
        if forgejo_token is not UNSET:
            field_dict["forgejoToken"] = forgejo_token
        if forgejo_username is not UNSET:
            field_dict["forgejoUsername"] = forgejo_username
        if renovate_rebase_label is not UNSET:
            field_dict["renovateRebaseLabel"] = renovate_rebase_label
        if renovate_authors is not UNSET:
            field_dict["renovateAuthors"] = renovate_authors
        if hide_dependency_dashboard is not UNSET:
            field_dict["hideDependencyDashboard"] = hide_dependency_dashboard
        if ignored_titles is not UNSET:
            field_dict["ignoredTitles"] = ignored_titles

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        github_token = d.pop("githubToken", UNSET)

        github_username = d.pop("githubUsername", UNSET)

        github_app_installation_id = d.pop("githubAppInstallationId", UNSET)

        forgejo_url = d.pop("forgejoUrl", UNSET)

        forgejo_token = d.pop("forgejoToken", UNSET)

        forgejo_username = d.pop("forgejoUsername", UNSET)

        renovate_rebase_label = d.pop("renovateRebaseLabel", UNSET)

        renovate_authors = cast(list[str], d.pop("renovateAuthors", UNSET))


        hide_dependency_dashboard = d.pop("hideDependencyDashboard", UNSET)

        ignored_titles = cast(list[str], d.pop("ignoredTitles", UNSET))


        settings_request = cls(
            github_token=github_token,
            github_username=github_username,
            github_app_installation_id=github_app_installation_id,
            forgejo_url=forgejo_url,
            forgejo_token=forgejo_token,
            forgejo_username=forgejo_username,
            renovate_rebase_label=renovate_rebase_label,
            renovate_authors=renovate_authors,
            hide_dependency_dashboard=hide_dependency_dashboard,
            ignored_titles=ignored_titles,
        )


        settings_request.additional_properties = d
        return settings_request

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
