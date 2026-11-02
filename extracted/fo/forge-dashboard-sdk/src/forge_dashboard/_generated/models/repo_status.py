from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="RepoStatus")



@_attrs_define
class RepoStatus:
    """ One tracked repository, whether or not it currently has anything
    open — repoCount alone can't name it, and it wouldn't otherwise
    appear anywhere pullRequests/issues don't already mention it.

        Attributes:
            forge (Forge):
            full_name (str):
            url (str): The repo's own page on its forge, for linking out.
            ignored (bool): Whether the signed-in user has ignored this repo in either
                scope below — true whenever ignoredPRs or
                ignoredIssues is true. The repo itself still appears here
                with accurate hasWebhook/canManageWebhooks regardless.
            ignored_p_rs (bool): Whether the signed-in user has ignored this repo's pull
                requests specifically — its pullRequests entries are
                excluded from this same response and from Insights.
            ignored_issues (bool): Whether the signed-in user has ignored this repo's issues
                specifically — its issues entries are excluded from
                this same response and from Insights.
            has_webhook (bool): Whether this app has ever recorded a signature-verified
                webhook delivery for this repo. Passive: it reflects a real
                delivery having arrived, not whether a webhook object exists
                on the forge — a correctly configured webhook that just
                hasn't fired yet still reads false here, the same as a
                misconfigured one would.
            can_manage_webhooks (bool): Whether the signed-in user's own permission on this repo is
                enough to list/create its webhooks — GitHub requires admin
                specifically (write/maintain can push but still 404 on the
                hooks endpoint, by GitHub's own design); Forgejo's equivalent
                is its own admin permission flag. Always false for a repo
                reached through an unauthenticated, username-only listing.
                A point-in-time snapshot: a permission change since the last
                refresh can still make a following ensure-webhook call fail
                despite this having said true. For a GitHub App connection
                there is no user role to read, so this is true when listing
                the repo's webhooks worked on the last refresh.
            rebase_bots (bool): Whether the signed-in user has turned on rebasing bot pull
                requests for this repo. A behind Dependabot or Renovate pull
                request gets the bot's own rebase, whatever the repo's
                automatic branch update setting says. Human, draft and
                release-please pull requests are not covered.
            auto_update_branch (bool): Whether the signed-in user has turned on automatic branch
                updates for this repo — any of its pull requests the
                background refresh finds behind its base branch gets updated
                the same way a manual "Update branch" click would. A
                Dependabot pull request gets its own rebase comment instead,
                and a Renovate one its own rebase label, mirroring their
                manual action buttons. A release-please pull request is
                always skipped by this background pass, so no unattended write
                lands on a release branch. The dashboard's manual "Update
                branch" button is still offered on it, since release-please
                has no rebase action of its own.
            logo_url (str | Unset): The repository's own logo, only when it has one: a GitHub
                repository's custom social preview image, or a Forgejo
                repository's own avatar. Absent otherwise, and never the
                generated social card GitHub shows for a repository with none,
                nor the owner's avatar. Always an https URL, passed through
                unchanged and never proxied: on GitHub exactly
                repository-images.githubusercontent.com, on Forgejo the
                instance's own host. A GitHub custom image is a wide banner,
                not a square logo.
                Absent for a repository reached through an unauthenticated,
                username-only listing, since that listing carries no image.
            webhook_locked_by_connection (bool | Unset): Present and true when canManageWebhooks is false because the
                connection itself can't manage webhooks on this repo (GitHub
                refused the hooks listing: a GitHub App without the Webhooks
                permission, or a repo outside its installation; Forgejo sent no
                permissions object for the repo), rather than the signed-in
                user's role. A failed or rate-limited listing doesn't
                set it. Absent otherwise.
            webhook_needs_token (bool | Unset): Present and true when canManageWebhooks is false because no
                token is saved for the forge. The repos then came from a
                username-only listing, which the forge answers as an anonymous
                caller, so the permissions it reports say nothing about the
                signed-in user's role. Saving a token with the webhook scope in
                Settings is the fix. Absent when a token is saved, whatever
                role it holds. Set today for Forgejo only.
            failing_since (datetime.datetime | Unset): Present when the last fetch of this repository failed, and the
                time of the first failure in the run it is still part of. Its
                pull requests and issues are then the last good ones. Absent
                when the repository is fetching fine. It is not saved, so it
                restarts from the first failure after a restart.
            failing_for_good (bool | Unset): Present and true when failingSince is older than the cutoff the
                refresh schedule uses for a repository that keeps failing, a
                fixed multiple of the refresh interval. Retrying has not helped
                by then. The server works this out when it builds the response,
                so a client shows it without doing the arithmetic, and a
                repository crosses the cutoff in what the client sees at the
                next refresh. Absent otherwise.
     """

    forge: Forge
    full_name: str
    url: str
    ignored: bool
    ignored_p_rs: bool
    ignored_issues: bool
    has_webhook: bool
    can_manage_webhooks: bool
    rebase_bots: bool
    auto_update_branch: bool
    logo_url: str | Unset = UNSET
    webhook_locked_by_connection: bool | Unset = UNSET
    webhook_needs_token: bool | Unset = UNSET
    failing_since: datetime.datetime | Unset = UNSET
    failing_for_good: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        full_name = self.full_name

        url = self.url

        ignored = self.ignored

        ignored_p_rs = self.ignored_p_rs

        ignored_issues = self.ignored_issues

        has_webhook = self.has_webhook

        can_manage_webhooks = self.can_manage_webhooks

        rebase_bots = self.rebase_bots

        auto_update_branch = self.auto_update_branch

        logo_url = self.logo_url

        webhook_locked_by_connection = self.webhook_locked_by_connection

        webhook_needs_token = self.webhook_needs_token

        failing_since: str | Unset = UNSET
        if not isinstance(self.failing_since, Unset):
            failing_since = self.failing_since.isoformat()

        failing_for_good = self.failing_for_good


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "url": url,
            "ignored": ignored,
            "ignoredPRs": ignored_p_rs,
            "ignoredIssues": ignored_issues,
            "hasWebhook": has_webhook,
            "canManageWebhooks": can_manage_webhooks,
            "rebaseBots": rebase_bots,
            "autoUpdateBranch": auto_update_branch,
        })
        if logo_url is not UNSET:
            field_dict["logoUrl"] = logo_url
        if webhook_locked_by_connection is not UNSET:
            field_dict["webhookLockedByConnection"] = webhook_locked_by_connection
        if webhook_needs_token is not UNSET:
            field_dict["webhookNeedsToken"] = webhook_needs_token
        if failing_since is not UNSET:
            field_dict["failingSince"] = failing_since
        if failing_for_good is not UNSET:
            field_dict["failingForGood"] = failing_for_good

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        url = d.pop("url")

        ignored = d.pop("ignored")

        ignored_p_rs = d.pop("ignoredPRs")

        ignored_issues = d.pop("ignoredIssues")

        has_webhook = d.pop("hasWebhook")

        can_manage_webhooks = d.pop("canManageWebhooks")

        rebase_bots = d.pop("rebaseBots")

        auto_update_branch = d.pop("autoUpdateBranch")

        logo_url = d.pop("logoUrl", UNSET)

        webhook_locked_by_connection = d.pop("webhookLockedByConnection", UNSET)

        webhook_needs_token = d.pop("webhookNeedsToken", UNSET)

        _failing_since = d.pop("failingSince", UNSET)
        failing_since: datetime.datetime | Unset
        if isinstance(_failing_since,  Unset):
            failing_since = UNSET
        else:
            failing_since = datetime.datetime.fromisoformat(_failing_since)




        failing_for_good = d.pop("failingForGood", UNSET)

        repo_status = cls(
            forge=forge,
            full_name=full_name,
            url=url,
            ignored=ignored,
            ignored_p_rs=ignored_p_rs,
            ignored_issues=ignored_issues,
            has_webhook=has_webhook,
            can_manage_webhooks=can_manage_webhooks,
            rebase_bots=rebase_bots,
            auto_update_branch=auto_update_branch,
            logo_url=logo_url,
            webhook_locked_by_connection=webhook_locked_by_connection,
            webhook_needs_token=webhook_needs_token,
            failing_since=failing_since,
            failing_for_good=failing_for_good,
        )


        repo_status.additional_properties = d
        return repo_status

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
