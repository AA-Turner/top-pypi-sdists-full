from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..models.forge_error_kind import ForgeErrorKind
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.provider_status import ProviderStatus
  from ..models.rate_limit import RateLimit





T = TypeVar("T", bound="ForgeHealth")



@_attrs_define
class ForgeHealth:
    """ 
        Attributes:
            forge (Forge):
            reachable (bool): Whether the last refresh attempt against this forge succeeded.
            repo_count (int): Repositories with write access this forge reported.
            starting (bool | Unset): True while the rows shown for this forge are the ones the last run
                saved and no refresh has asked the forge since the app started.
                The forge is then neither reachable nor in error (errorKind is
                absent); it has not been checked yet. The first refresh that
                reaches it replaces this entry. A client says "starting up,
                showing data from 3 minutes ago", and never "unreachable".
            stale_since (datetime.datetime | Unset): Present when the last refresh against this forge failed, or the
                forge has not been asked yet since the app started (see
                starting), and the pull requests, issues and repos in the
                response are the last good ones, fetched at this time, instead of
                none. Absent when the data
                is current, and for a forge that has never fetched successfully,
                which has nothing to show. A forge that has not answered counts
                as failed, so a hung forge does not hold back the others: after
                three minutes in a scheduled refresh, after one minute in a
                refresh a person asked for. A forge still answering the last
                refresh is not asked again, and counts as failed too. A client
                can say "unreachable, showing
                data from 3 minutes ago".
            error (str | Unset): A human-readable explanation of the last failure, if reachable is false. Mapped from
                errorKind, not the raw underlying error text. Omitted when reachable.
            error_kind (ForgeErrorKind | Unset): Why a forge is unreachable, or why a write to it was rejected, as
                coarse as every forge this service talks to can agree on.
                "unreachable" is a request that got no response; "upstream_error" is
                the forge answering with a 5xx (a gateway timeout, say), and the
                status is in ForgeHealth.upstreamStatus. "unauthorized" covers both a
                bad token and a forbidden request; "not_found" usually means a wrong
                instance URL. "conflict" is only ever returned from a pull-request
                write — the forge reports the PR itself isn't currently mergeable. "unknown" covers a signal this
                service doesn't recognize, rather than a guessed-at specific cause.
            upstream_status (int | Unset): The 5xx status the forge answered with, set only when errorKind is
                upstream_error. The forge is not shown as down until three fetches in a row have failed, whatever the cause,
                with the latest a 5xx; one failure among healthy ones changes nothing.
            rate_limit_graph_ql (RateLimit | Unset): One of a forge API's own request budgets for the credential the last
                refresh used — see ForgeHealth.rateLimitGraphQL/rateLimitREST for which budget this is and when each is (or
                isn't) reported.
            rate_limit_rest (RateLimit | Unset): One of a forge API's own request budgets for the credential the last
                refresh used — see ForgeHealth.rateLimitGraphQL/rateLimitREST for which budget this is and when each is (or
                isn't) reported.
            dependabot_commands_blocked (str | Unset): Why a "@dependabot" comment sent through this forge's credential
                would be refused. Dependabot only honours commands from a user with push access and ignores GitHub App accounts
                whatever permissions the App holds. Set only for GitHub when the connected credential is an App with no personal
                access token saved to send commands as. The Dependabot buttons lock with this text, auto-update-branch skips
                Dependabot pull requests, and the dependabot-action endpoint answers 409 with it. Omitted when commands work.
            rerun_checks_blocked (str | Unset): Why this forge can't rerun checks. Set only for a Forgejo whose version is 7
                to 16, which has no API route for it. A version below 7 is left to the forge, because a Gitea numbers itself
                that way. The version is read in the background, read again after an hour while it blocks, and retried after a
                failed read or one that gives no number. A block that has gone stale is dropped when the read fails. Rerun
                failed checks is not offered for the forge, and the page shows this text where the button would be. Omitted when
                rerunning works or the version could not be read.
            provider_status (ProviderStatus | Unset):
     """

    forge: Forge
    reachable: bool
    repo_count: int
    starting: bool | Unset = UNSET
    stale_since: datetime.datetime | Unset = UNSET
    error: str | Unset = UNSET
    error_kind: ForgeErrorKind | Unset = UNSET
    upstream_status: int | Unset = UNSET
    rate_limit_graph_ql: RateLimit | Unset = UNSET
    rate_limit_rest: RateLimit | Unset = UNSET
    dependabot_commands_blocked: str | Unset = UNSET
    rerun_checks_blocked: str | Unset = UNSET
    provider_status: ProviderStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.provider_status import ProviderStatus # noqa: PLC0415
        from ..models.rate_limit import RateLimit # noqa: PLC0415
        forge = self.forge.value

        reachable = self.reachable

        repo_count = self.repo_count

        starting = self.starting

        stale_since: str | Unset = UNSET
        if not isinstance(self.stale_since, Unset):
            stale_since = self.stale_since.isoformat()

        error = self.error

        error_kind: str | Unset = UNSET
        if not isinstance(self.error_kind, Unset):
            error_kind = self.error_kind.value


        upstream_status = self.upstream_status

        rate_limit_graph_ql: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rate_limit_graph_ql, Unset):
            rate_limit_graph_ql = self.rate_limit_graph_ql.to_dict()

        rate_limit_rest: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rate_limit_rest, Unset):
            rate_limit_rest = self.rate_limit_rest.to_dict()

        dependabot_commands_blocked = self.dependabot_commands_blocked

        rerun_checks_blocked = self.rerun_checks_blocked

        provider_status: dict[str, Any] | Unset = UNSET
        if not isinstance(self.provider_status, Unset):
            provider_status = self.provider_status.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "reachable": reachable,
            "repoCount": repo_count,
        })
        if starting is not UNSET:
            field_dict["starting"] = starting
        if stale_since is not UNSET:
            field_dict["staleSince"] = stale_since
        if error is not UNSET:
            field_dict["error"] = error
        if error_kind is not UNSET:
            field_dict["errorKind"] = error_kind
        if upstream_status is not UNSET:
            field_dict["upstreamStatus"] = upstream_status
        if rate_limit_graph_ql is not UNSET:
            field_dict["rateLimitGraphQL"] = rate_limit_graph_ql
        if rate_limit_rest is not UNSET:
            field_dict["rateLimitREST"] = rate_limit_rest
        if dependabot_commands_blocked is not UNSET:
            field_dict["dependabotCommandsBlocked"] = dependabot_commands_blocked
        if rerun_checks_blocked is not UNSET:
            field_dict["rerunChecksBlocked"] = rerun_checks_blocked
        if provider_status is not UNSET:
            field_dict["providerStatus"] = provider_status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_status import ProviderStatus # noqa: PLC0415
        from ..models.rate_limit import RateLimit # noqa: PLC0415
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        reachable = d.pop("reachable")

        repo_count = d.pop("repoCount")

        starting = d.pop("starting", UNSET)

        _stale_since = d.pop("staleSince", UNSET)
        stale_since: datetime.datetime | Unset
        if isinstance(_stale_since,  Unset):
            stale_since = UNSET
        else:
            stale_since = datetime.datetime.fromisoformat(_stale_since)




        error = d.pop("error", UNSET)

        _error_kind = d.pop("errorKind", UNSET)
        error_kind: ForgeErrorKind | Unset
        if isinstance(_error_kind,  Unset):
            error_kind = UNSET
        else:
            error_kind = ForgeErrorKind(_error_kind)




        upstream_status = d.pop("upstreamStatus", UNSET)

        _rate_limit_graph_ql = d.pop("rateLimitGraphQL", UNSET)
        rate_limit_graph_ql: RateLimit | Unset
        if isinstance(_rate_limit_graph_ql,  Unset):
            rate_limit_graph_ql = UNSET
        else:
            rate_limit_graph_ql = RateLimit.from_dict(_rate_limit_graph_ql)




        _rate_limit_rest = d.pop("rateLimitREST", UNSET)
        rate_limit_rest: RateLimit | Unset
        if isinstance(_rate_limit_rest,  Unset):
            rate_limit_rest = UNSET
        else:
            rate_limit_rest = RateLimit.from_dict(_rate_limit_rest)




        dependabot_commands_blocked = d.pop("dependabotCommandsBlocked", UNSET)

        rerun_checks_blocked = d.pop("rerunChecksBlocked", UNSET)

        _provider_status = d.pop("providerStatus", UNSET)
        provider_status: ProviderStatus | Unset
        if isinstance(_provider_status,  Unset):
            provider_status = UNSET
        else:
            provider_status = ProviderStatus.from_dict(_provider_status)




        forge_health = cls(
            forge=forge,
            reachable=reachable,
            repo_count=repo_count,
            starting=starting,
            stale_since=stale_since,
            error=error,
            error_kind=error_kind,
            upstream_status=upstream_status,
            rate_limit_graph_ql=rate_limit_graph_ql,
            rate_limit_rest=rate_limit_rest,
            dependabot_commands_blocked=dependabot_commands_blocked,
            rerun_checks_blocked=rerun_checks_blocked,
            provider_status=provider_status,
        )


        forge_health.additional_properties = d
        return forge_health

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
