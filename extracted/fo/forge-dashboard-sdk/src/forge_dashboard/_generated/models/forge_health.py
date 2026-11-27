from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..models.forge_error_kind import ForgeErrorKind
from ..models.forge_health_cause import ForgeHealthCause
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.failed_installation import FailedInstallation
  from ..models.forge_capabilities import ForgeCapabilities
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
            capabilities (ForgeCapabilities): What one forge can do, as facts a client reads instead of testing the forge's
                name. A forge this service learns to talk to is one more set of values here, so a client that reads these needs
                no change for it.
            starting (bool | Unset): True while the rows shown for this forge are the ones the last run
                saved and no fetch from the forge has answered in time since the
                app started. `reachable` is then false and errorKind is absent: it
                is not in error, it has not been heard from. A first fetch that
                passes the scheduled deadline of three minutes, and a pass skipped
                behind it, leave this entry as it is, and the late answer is
                dropped. A refresh a person asked for stops waiting after one
                minute, but the fetch runs on and this entry stays until it
                answers. The first fetch that answers within the scheduled deadline
                replaces it. When three passes in a row have
                gone unanswered, counting deadline and skipped passes together,
                the flag and the "starting" cause go, and errorKind is
                "unreachable", with the saved rows and staleSince kept. While it is
                true a client says "starting up, showing data from 3 minutes ago",
                and never "unreachable".
            cause (ForgeHealthCause | Unset): Why the rows shown for this forge are not from the latest read,
                while the forge is not down. "starting" is the same fact as
                the `starting` flag, and goes when that flag does: the rows are the
                ones the last run saved and no fetch from the forge has answered in
                time since the app started.
                "slow" means the forge has not answered yet and is not counted as
                down. Either a refresh a person asked for stopped waiting after one
                minute and the fetch is still running, which counts as no miss, or
                a fetch hit the scheduled deadline of three minutes and the forge
                is held until three passes in a row have missed. The last good rows
                are held and the forge is still reachable. A forge never read
                before can be "slow" with no rows while its first fetch runs on.
                It then has no `rowsReadAt`, and a client must not read the
                missing rows as closed or gone, or offer actions for it.
                A fetch that runs on is applied as soon as it answers. Otherwise
                any later pass that does not miss clears the cause, including one
                that holds a 5xx or does not ask
                because the rate limit is spent or at its reserve. Absent when the
                rows are current, and when the forge is shown as down (see
                errorKind). A client words it, "slow to answer" or "starting up",
                and does not call the rows live.
            rows_read_at (datetime.datetime | Unset): Present only while `cause` is "slow": about when the held rows
                were read. It is normally the time of the last full read that
                answered, including one that could not read some repositories,
                whose rows are older. When webhook refreshes have made every
                repository current after a failed full refresh or a restart, it is
                the time of the last of those, and rows refreshed before it are
                older. A webhook may also have refreshed single repositories since,
                so some rows can be newer. `staleSince` is worked out the same way,
                with the same limits. `rowsReadAt` stays the same through further
                missed and skipped passes, and goes when `cause` does. `rowsReadAt`
                is not `staleSince`: the forge is still reachable, and nothing is
                locked. A client can say "slow to answer, showing data from 3
                minutes ago".
            stale_since (datetime.datetime | Unset): Present when the last refresh against this forge failed, or the
                forge has not been asked yet since the app started (see
                starting), and the pull requests, issues and repos in the
                response are the last good ones, fetched at this time, instead of
                none. Cleared, with the forge reading as reachable again, once a
                webhook refresh has made every repo of the forge current, even
                while full refreshes keep failing. Absent when the data
                is current, and for a forge that has never fetched successfully,
                which has nothing to show. A hung forge does not hold back the
                others: a scheduled refresh waits three minutes for it and a
                refresh a person asked for waits one. Only the three minutes count
                against the forge. A fetch the person's refresh stopped waiting for
                runs on up to that limit, and the forge is not asked again
                meanwhile. A client can say "unreachable, showing
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
            failed_installations (list[FailedInstallation] | Unset): The GitHub App installations that did not answer this
                refresh while the forge itself did (reachable is true). Each one's pull requests and issues keep the last rows
                read, and the other installations load as usual. Set only for GitHub, and only when more than one installation
                is read. Omitted when every installation answered.
     """

    forge: Forge
    reachable: bool
    repo_count: int
    capabilities: ForgeCapabilities
    starting: bool | Unset = UNSET
    cause: ForgeHealthCause | Unset = UNSET
    rows_read_at: datetime.datetime | Unset = UNSET
    stale_since: datetime.datetime | Unset = UNSET
    error: str | Unset = UNSET
    error_kind: ForgeErrorKind | Unset = UNSET
    upstream_status: int | Unset = UNSET
    rate_limit_graph_ql: RateLimit | Unset = UNSET
    rate_limit_rest: RateLimit | Unset = UNSET
    dependabot_commands_blocked: str | Unset = UNSET
    rerun_checks_blocked: str | Unset = UNSET
    provider_status: ProviderStatus | Unset = UNSET
    failed_installations: list[FailedInstallation] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.failed_installation import FailedInstallation # noqa: PLC0415
        from ..models.forge_capabilities import ForgeCapabilities # noqa: PLC0415
        from ..models.provider_status import ProviderStatus # noqa: PLC0415
        from ..models.rate_limit import RateLimit # noqa: PLC0415
        forge = self.forge.value

        reachable = self.reachable

        repo_count = self.repo_count

        capabilities = self.capabilities.to_dict()

        starting = self.starting

        cause: str | Unset = UNSET
        if not isinstance(self.cause, Unset):
            cause = self.cause.value


        rows_read_at: str | Unset = UNSET
        if not isinstance(self.rows_read_at, Unset):
            rows_read_at = self.rows_read_at.isoformat()

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

        failed_installations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.failed_installations, Unset):
            failed_installations = []
            for failed_installations_item_data in self.failed_installations:
                failed_installations_item = failed_installations_item_data.to_dict()
                failed_installations.append(failed_installations_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "reachable": reachable,
            "repoCount": repo_count,
            "capabilities": capabilities,
        })
        if starting is not UNSET:
            field_dict["starting"] = starting
        if cause is not UNSET:
            field_dict["cause"] = cause
        if rows_read_at is not UNSET:
            field_dict["rowsReadAt"] = rows_read_at
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
        if failed_installations is not UNSET:
            field_dict["failedInstallations"] = failed_installations

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.failed_installation import FailedInstallation # noqa: PLC0415
        from ..models.forge_capabilities import ForgeCapabilities # noqa: PLC0415
        from ..models.provider_status import ProviderStatus # noqa: PLC0415
        from ..models.rate_limit import RateLimit # noqa: PLC0415
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        reachable = d.pop("reachable")

        repo_count = d.pop("repoCount")

        capabilities = ForgeCapabilities.from_dict(d.pop("capabilities"))




        starting = d.pop("starting", UNSET)

        _cause = d.pop("cause", UNSET)
        cause: ForgeHealthCause | Unset
        if isinstance(_cause,  Unset):
            cause = UNSET
        else:
            cause = ForgeHealthCause(_cause)




        _rows_read_at = d.pop("rowsReadAt", UNSET)
        rows_read_at: datetime.datetime | Unset
        if isinstance(_rows_read_at,  Unset):
            rows_read_at = UNSET
        else:
            rows_read_at = datetime.datetime.fromisoformat(_rows_read_at)




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




        _failed_installations = d.pop("failedInstallations", UNSET)
        failed_installations: list[FailedInstallation] | Unset = UNSET
        if _failed_installations is not UNSET:
            failed_installations = []
            for failed_installations_item_data in _failed_installations:
                failed_installations_item = FailedInstallation.from_dict(failed_installations_item_data)



                failed_installations.append(failed_installations_item)


        forge_health = cls(
            forge=forge,
            reachable=reachable,
            repo_count=repo_count,
            capabilities=capabilities,
            starting=starting,
            cause=cause,
            rows_read_at=rows_read_at,
            stale_since=stale_since,
            error=error,
            error_kind=error_kind,
            upstream_status=upstream_status,
            rate_limit_graph_ql=rate_limit_graph_ql,
            rate_limit_rest=rate_limit_rest,
            dependabot_commands_blocked=dependabot_commands_blocked,
            rerun_checks_blocked=rerun_checks_blocked,
            provider_status=provider_status,
            failed_installations=failed_installations,
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
