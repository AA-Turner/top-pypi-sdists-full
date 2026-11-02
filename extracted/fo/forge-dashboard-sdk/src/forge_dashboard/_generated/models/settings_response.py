from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.settings_response_theme import SettingsResponseTheme
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="SettingsResponse")



@_attrs_define
class SettingsResponse:
    """ The signed-in user's own GitHub/Forgejo configuration. Never
    includes a forge token's value — only whether one is currently
    saved, so the UI can show a "Configured" badge without the secret
    ever reaching the browser. webhookToken/webhookSecret are the
    exception: they're ours to hand back in the clear, since the user
    has to paste them into the forge's own webhook setup.

        Attributes:
            github_username (str): Used as a token-free public-repos fallback when no GitHub token is set.
            github_token_set (bool): Whether a GitHub token is currently saved.
            github_app_installation_id (int): The installation ID of the alrayyes-automation GitHub App
                this user has connected, or 0 if none. Not a
                secret — it's an opaque integer GitHub already shows the
                user on its own installation settings page — so, unlike
                githubTokenSet, this round-trips as a plain value. Takes
                precedence over a saved githubToken whenever both are set
                and the server has an App configured (see
                githubAppConfigured).
            github_app_configured (bool): Whether this server has a GitHub App configured at all
                (server-wide GITHUB_APP_ID/GITHUB_APP_PRIVATE_KEY_BASE64 —
                not a saved setting). The Settings page uses this to
                explain why githubAppInstallationId can't be saved when
                it's false.
            forgejo_url (str): Always without a username, password, query string or fragment,
                even if the stored value predates those being refused.
            forgejo_username (str): Used as a token-free public-repos fallback when no Forgejo token is set.
            forgejo_token_set (bool): Whether a Forgejo token is currently saved.
            webhook_token (str): Identifies this user in a webhook URL
                (`/api/webhooks/{provider}/{webhookToken}`). Generated on
                first visit to Settings and stable after that.
            webhook_secret (str): Pasted into the forge's own webhook "Secret" field, used to
                verify the signature header on incoming webhook deliveries
                (`X-Hub-Signature-256` on GitHub, `X-Forgejo-Signature` on
                Forgejo). Never appears in the webhook URL itself.
            renovate_rebase_label (str): The label Renovate's own rebase/retry trigger listens for on
                a repo (Renovate's own `rebaseLabel` config option — genuinely
                per-repo configurable, so this is a user-set override rather
                than a hardcoded constant). Empty means Renovate's own
                documented default, `rebase`.
            renovate_authors (list[str]): The logins that are Renovate on the user's forges. On GitHub the
                App's own `renovate` and `renovate[bot]` are always recognised.
                A Forgejo or GitLab instance has no App: Renovate runs there as
                an ordinary account with whatever name the instance gave it, so
                the user lists it here. A pull request by one of these gets
                Renovate's own rebase, not Update branch, and is a `dependency`.
                Matched case-insensitively. Empty means only the GitHub slugs.
            theme (SettingsResponseTheme): The signed-in user's own theme preference. Empty
                means "system" — follow the browser's prefers-color-scheme
                rather than a saved choice. Set only from Settings; every
                other page reads it via the lightweight
                GET /api/v1/settings/theme instead of this endpoint.
            ignored_title_counts (list[int | None]): Per pattern in `ignoredTitles`, same order and same length: how
                many of the viewer's currently open issues that pattern matches
                on its own. An issue two patterns match counts for both, so the
                entries can sum to more than `settingsHiddenIssueCount`. Every
                entry is null while the count is unknown (the viewer's first
                refresh has not finished, see `firstRefreshDone` on the
                dashboard snapshot, or there is no snapshot), never a made-up 0.
                Only this viewer's issues are counted. On GET and on the PUT
                response alike: a PUT returns the counts for the list it just
                saved, worked out from the issues the viewer had before the save.
            timezone (str | Unset): The signed-in user's own time zone as an IANA name such as
                `Europe/Amsterdam`. Empty means the browser's own zone. Set only
                from Settings (PUT /api/v1/settings/timezone); every other page reads
                it via GET /api/v1/settings/timezone.
            hide_dependency_dashboard (bool | Unset): Whether the user hides the bot-kept "Dependency Dashboard" issue
                everywhere: the server leaves a `housekeeping` issue out of the
                `issues` of GET /api/v1/dashboard and its stream, and out of every
                count and total built from them (`navCounts`, Insights). Always
                present once the server applies it.
            ignored_titles (list[str] | Unset): Patterns for issue titles to leave out, in the server's own
                regular expression syntax (Go RE2: no lookahead and no
                backreferences). A pattern matches anywhere in the title and
                ignores case; an issue matching any one is left out of `issues`
                and of every count and total built from them, the same as
                `hideDependencyDashboard`. Always present once the server
                applies it. Empty means none.
     """

    github_username: str
    github_token_set: bool
    github_app_installation_id: int
    github_app_configured: bool
    forgejo_url: str
    forgejo_username: str
    forgejo_token_set: bool
    webhook_token: str
    webhook_secret: str
    renovate_rebase_label: str
    renovate_authors: list[str]
    theme: SettingsResponseTheme
    ignored_title_counts: list[int | None]
    timezone: str | Unset = UNSET
    hide_dependency_dashboard: bool | Unset = UNSET
    ignored_titles: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        github_username = self.github_username

        github_token_set = self.github_token_set

        github_app_installation_id = self.github_app_installation_id

        github_app_configured = self.github_app_configured

        forgejo_url = self.forgejo_url

        forgejo_username = self.forgejo_username

        forgejo_token_set = self.forgejo_token_set

        webhook_token = self.webhook_token

        webhook_secret = self.webhook_secret

        renovate_rebase_label = self.renovate_rebase_label

        renovate_authors = self.renovate_authors



        theme = self.theme.value

        ignored_title_counts = []
        for ignored_title_counts_item_data in self.ignored_title_counts:
            ignored_title_counts_item: int | None
            ignored_title_counts_item = ignored_title_counts_item_data
            ignored_title_counts.append(ignored_title_counts_item)



        timezone = self.timezone

        hide_dependency_dashboard = self.hide_dependency_dashboard

        ignored_titles: list[str] | Unset = UNSET
        if not isinstance(self.ignored_titles, Unset):
            ignored_titles = self.ignored_titles




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
            "webhookToken": webhook_token,
            "webhookSecret": webhook_secret,
            "renovateRebaseLabel": renovate_rebase_label,
            "renovateAuthors": renovate_authors,
            "theme": theme,
            "ignoredTitleCounts": ignored_title_counts,
        })
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if hide_dependency_dashboard is not UNSET:
            field_dict["hideDependencyDashboard"] = hide_dependency_dashboard
        if ignored_titles is not UNSET:
            field_dict["ignoredTitles"] = ignored_titles

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

        webhook_token = d.pop("webhookToken")

        webhook_secret = d.pop("webhookSecret")

        renovate_rebase_label = d.pop("renovateRebaseLabel")

        renovate_authors = cast(list[str], d.pop("renovateAuthors"))


        theme = SettingsResponseTheme(d.pop("theme"))




        ignored_title_counts = []
        _ignored_title_counts = d.pop("ignoredTitleCounts")
        for ignored_title_counts_item_data in (_ignored_title_counts):
            def _parse_ignored_title_counts_item(data: object) -> int | None:
                if data is None:
                    return data
                return cast(int | None, data)

            ignored_title_counts_item = _parse_ignored_title_counts_item(ignored_title_counts_item_data)

            ignored_title_counts.append(ignored_title_counts_item)


        timezone = d.pop("timezone", UNSET)

        hide_dependency_dashboard = d.pop("hideDependencyDashboard", UNSET)

        ignored_titles = cast(list[str], d.pop("ignoredTitles", UNSET))


        settings_response = cls(
            github_username=github_username,
            github_token_set=github_token_set,
            github_app_installation_id=github_app_installation_id,
            github_app_configured=github_app_configured,
            forgejo_url=forgejo_url,
            forgejo_username=forgejo_username,
            forgejo_token_set=forgejo_token_set,
            webhook_token=webhook_token,
            webhook_secret=webhook_secret,
            renovate_rebase_label=renovate_rebase_label,
            renovate_authors=renovate_authors,
            theme=theme,
            ignored_title_counts=ignored_title_counts,
            timezone=timezone,
            hide_dependency_dashboard=hide_dependency_dashboard,
            ignored_titles=ignored_titles,
        )


        settings_response.additional_properties = d
        return settings_response

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
