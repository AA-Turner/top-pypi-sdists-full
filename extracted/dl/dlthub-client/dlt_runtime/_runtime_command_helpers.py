"""Helper functions for runtime CLI commands.

Pure helpers (no service deps) and service-dependent loaders (no display).
"""

# Python internals
import json
import tarfile
from datetime import datetime
from io import BytesIO
from pathlib import Path
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    Literal,
    NoReturn,
    Optional,
    Union,
)
from uuid import UUID

# Other libraries
import httpx
import yaml
from dlt._workspace._workspace_context import active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.exceptions import CliCommandInnerException
from dlt._workspace.exceptions import WorkspaceRunContextNotAvailable
from dlt._workspace.deployment import (
    DEFAULT_DEPLOYMENT_MODULE,
    MANIFEST_ENGINE_VERSION,
    default_dashboard_manifest,
    generate_manifest_hash,
    match_triggers_with_selectors,
    resolve_job_ref,
)
from dlt._workspace.deployment._run_helpers import load_manifest_with_warnings
from dlt._workspace.deployment._trigger_helpers import is_selector
from dlt._workspace.deployment.exceptions import (
    AmbiguousJobRef,
    InvalidJobRef,
    JobRefNotFound,
)
from dlt._workspace.deployment.typing import (
    TJobRef,
    TJobsDeploymentManifest,
    TTrigger,
)
from dlt._workspace.deployment.file_selector import (
    ConfigurationFileSelector,
    WorkspaceFileSelector,
)
from dlt._workspace.deployment.package_builder import PackageBuilder
from dlt._workspace.deployment.requirements import (
    WorkspaceRequirementsError,
    export_workspace_requirements,
    save_requirements,
)
from dlt_runtime.exceptions import (
    AmbiguousWorkspaceName,
    NoRunsFound,
    RuntimeNotAuthenticated,
    RuntimeOperationNotAuthorized,
    WorkspaceNotFound,
    exception_from_response,
    handle_client_exceptions,
)
from dlt_runtime import runtime as _runtime_module
from dlt_runtime import urls
from dlt_runtime.runtime import (
    RuntimeAuthService,
    _tls_verify,
)
from dlt_runtime.runtime_clients.api.api.configurations import (
    create_configuration,
    get_configuration,
    get_latest_configuration,
    list_configurations,
)
from dlt_runtime.runtime_clients.api.api.deployments import (
    create_deployment,
    get_deployment,
    get_latest_deployment,
    list_deployments,
)
from dlt_runtime.runtime_clients.api.api.dataplanes import list_dataplanes
from dlt_runtime.runtime_clients.api.api.runs import (
    get_run,
    list_runs,
)
from dlt_runtime.runtime_clients.api.api.scripts import (
    get_script,
    list_scripts,
)
from dlt_runtime.runtime_clients.api.api.workspaces import (
    deploy as deploy_manifest,
    get_workspace as get_workspace_api,
    get_workspace_dataplane_access_token,
)
from dlt_runtime.runtime_clients.api.models.deploy_manifest_request import (
    DeployManifestRequest,
)
from dlt_runtime.runtime_clients.api.client import Client as ApiClient
from dlt_runtime.runtime_clients.api.models.dataplane_access_token_response import (
    DataplaneAccessTokenResponse,
)
from dlt_runtime.runtime_clients.api.models.dataplane_info import DataplaneInfo
from dlt_runtime.runtime_clients.api.models.detailed_run_response import (
    DetailedRunResponse,
)
from dlt_runtime.runtime_clients.api.models.list_scripts_archived import (
    ListScriptsArchived,
)
from dlt_runtime.runtime_clients.api.models.run_status import RunStatus
from dlt_runtime.runtime_clients.api.models.t_job_definition import (
    TJobDefinition as ApiTJobDefinition,
)
from dlt_runtime.runtime_clients.api.models.upload_initiated_response import (
    UploadInitiatedResponse,
)
from dlt_runtime.runtime_clients.api.models.workspace_response import WorkspaceResponse
from dlt_runtime.runtime_clients.api.types import Unset
from dlt_runtime.runtime_clients.logs.models.log_line import LogLine
from dlt_runtime.strings import (
    JOB_SELECTOR_NOT_FOUND,
    ORG_ID_CONFLICTS_WITH_PIN,
    ORG_ID_NOT_ACTIVE,
    PINNED_ORG_NOT_ACCESSIBLE,
    UNPIN_ORG_REMEDIATION,
    WORKSPACE_BELONGS_TO_OTHER_ORG,
)
from dlt_runtime.typing import (
    OrganizationGroup,
    OrganizationInfo,
    RuntimeInfo,
    SyncResult,
    UserInfo,
    WorkspaceChoice,
    WorkspaceInfo,
)
from dlt_runtime.version import __version__

if TYPE_CHECKING:
    from dlt_runtime.runtime_clients.api.models.deploy_manifest_response import (
        DeployManifestResponse,
    )

# Re-export view constants needed by loaders
from dlt_runtime._runtime_command_views import (  # noqa: F401
    DEPLOYMENT_HEADERS,
    CONFIGURATION_HEADERS,
    _extract_keys,
    _format_log_line,
    _preprocess_run_output,
)
from dlt_runtime._runtime_command_views import format_job_selector


NON_TERMINAL_RUN_STATUSES = frozenset(
    {RunStatus.PENDING, RunStatus.STARTING, RunStatus.RUNNING, RunStatus.CANCELLING}
)


def _to_uuid(value: Union[str, UUID]) -> UUID:
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except ValueError:
        raise CliCommandInnerException(
            cmd="dlthub",
            msg=f"Invalid UUID: {value}",
        )


def _resolve_workspace_id(user_info: UserInfo, workspace: str) -> str:
    """Resolve a workspace name or ID to an owned workspace ID."""

    workspace = workspace.strip()

    # Exact ID match is always unambiguous — return immediately.
    for ws in user_info["workspaces"]:
        if ws.get("role") == "owner" and workspace == ws["id"]:
            return ws["id"]

    matches = [
        ws
        for ws in user_info["workspaces"]
        if ws.get("role") == "owner" and ws["name"] == workspace
    ]

    if len(matches) == 1:
        return matches[0]["id"]

    if len(matches) > 1:
        raise AmbiguousWorkspaceName(workspace, matches)

    is_uuid = True
    try:
        UUID(workspace)
    except ValueError:
        is_uuid = False
    raise WorkspaceNotFound(workspace, is_uuid=is_uuid)


def _active_orgs(user_info: UserInfo) -> list[OrganizationInfo]:
    """All organizations the user is an active member of."""
    return [org for org in user_info["organizations"] if org.get("active", True)]


def _active_org_count(user_info: UserInfo) -> int:
    return len(_active_orgs(user_info))


def _sole_active_org_id(user_info: UserInfo) -> Optional[str]:
    """Return the single active org's id, or None if zero or multiple."""
    actives = _active_orgs(user_info)
    return actives[0]["id"] if len(actives) == 1 else None


def _org_label(user_info: UserInfo, organization_id: str) -> str:
    """Render an org as `name (id)` if the name is known, else just the id."""
    for org in user_info["organizations"]:
        if org["id"] == organization_id:
            return f"{org['name']} ({organization_id})"
    return organization_id


def _scope_user_info_to_org(user_info: UserInfo, organization_id: str) -> UserInfo:
    """Return a UserInfo whose `workspaces` and `organizations` are filtered to one org."""
    scoped: UserInfo = {
        "email": user_info["email"],
        "user_id": user_info["user_id"],
        "identity_id": user_info["identity_id"],
        "default_organization_id": user_info["default_organization_id"],
        "workspaces": [
            ws
            for ws in user_info["workspaces"]
            if ws.get("organization_id") == organization_id
        ],
        "organizations": [
            org for org in user_info["organizations"] if org["id"] == organization_id
        ],
    }
    if "default_workspace" in user_info:
        scoped["default_workspace"] = user_info["default_workspace"]
    return scoped


def _validate_org_id(user_info: UserInfo, org_id: str) -> None:
    """Raise if `org_id` (from `--org-id`) is not in the user's active organizations."""
    actives = _active_orgs(user_info)
    if any(org["id"] == org_id for org in actives):
        return
    valid = ", ".join(f"{org['name']} ({org['id']})" for org in actives) or "<none>"
    raise CliCommandInnerException(
        cmd="workspace",
        msg=ORG_ID_NOT_ACTIVE.format(org_id=org_id, valid=valid),
    )


def _validate_pinned_org_id(user_info: UserInfo, pinned_org_id: str) -> None:
    """Raise if the org pinned in `.dlt/config.toml` is not in the user's active orgs."""
    # Distinct message from `_validate_org_id`: the user must remove the line
    # from config.toml manually (CLI never overwrites it).
    if any(org["id"] == pinned_org_id for org in _active_orgs(user_info)):
        return
    raise CliCommandInnerException(
        cmd="workspace",
        msg=PINNED_ORG_NOT_ACCESSIBLE.format(
            pinned_org_id=pinned_org_id, remediation=UNPIN_ORG_REMEDIATION
        ),
    )


def _check_org_arg_matches_pin(
    user_info: UserInfo, pinned_org_id: Optional[str], org_id: str
) -> None:
    """Raise if `--org-id` disagrees with the org pinned in config.toml."""
    if not pinned_org_id or pinned_org_id == org_id:
        return
    raise CliCommandInnerException(
        cmd="workspace",
        msg=ORG_ID_CONFLICTS_WITH_PIN.format(
            org_id=org_id,
            pinned_label=_org_label(user_info, pinned_org_id),
            remediation=UNPIN_ORG_REMEDIATION,
        ),
    )


def _resolve_effective_org_id(
    user_info: UserInfo,
    pinned_org_id: Optional[str],
    org_id: Optional[str],
) -> Optional[str]:
    """Settle the org scope for a `connect` call (validation + precedence).

    Precedence: pinned org in config.toml > `--org-id` flag > None.
    Raises if `--org-id` is unknown or disagrees with the pin, or if the
    pinned org is no longer accessible.
    """
    if org_id is not None:
        _validate_org_id(user_info, org_id)
        _check_org_arg_matches_pin(user_info, pinned_org_id, org_id)
    elif pinned_org_id:
        # Stale pin (org deleted / membership removed) — surface before
        # scoping yields an empty group list.
        _validate_pinned_org_id(user_info, pinned_org_id)
    return pinned_org_id or org_id


def _raise_cross_org(
    user_info: UserInfo, ws: WorkspaceInfo, effective_org_id: str
) -> NoReturn:
    """Raise the standard "workspace lives in a different org" error."""
    raise CliCommandInnerException(
        cmd="workspace",
        msg=WORKSPACE_BELONGS_TO_OTHER_ORG.format(
            ws_name=ws["name"],
            ws_org=ws.get("organization_name") or ws.get("organization_id"),
            effective_label=_org_label(user_info, effective_org_id),
            remediation=UNPIN_ORG_REMEDIATION,
        ),
    )


def _org_id_to_persist(
    user_info: UserInfo,
    resolved_ws: Optional[WorkspaceInfo],
    effective_org_id: Optional[str],
) -> str:
    """Pick the org_id to write_connection persists (write-once)."""
    # Prefer the resolved workspace's own org → effective scope → default.
    if resolved_ws is not None and resolved_ws.get("organization_id"):
        return resolved_ws["organization_id"]
    if effective_org_id:
        return effective_org_id
    return user_info["default_organization_id"]


def _group_workspaces_by_org(user_info: UserInfo) -> list[OrganizationGroup]:
    """Build picker groups: one section per active org, owned workspaces only."""
    # Ids stamped here drive both the view (`[N]` labels) and the picker
    # resolver — single source of truth for the numbering.
    groups: list[OrganizationGroup] = []
    next_id = 0
    # Server order keeps the picker layout stable across invocations.
    for org in _active_orgs(user_info):
        org_id = org["id"]
        owned = [
            ws
            for ws in user_info["workspaces"]
            if ws.get("role") == "owner" and ws.get("organization_id") == org_id
        ]
        # Create row owns the first [N] in this group; workspaces follow.
        create_id = next_id
        next_id += 1
        ws_choices: list[WorkspaceChoice] = []
        for ws in owned:
            ws_choices.append(WorkspaceChoice(id=next_id, workspace=ws))
            next_id += 1
        groups.append(
            OrganizationGroup(
                organization_id=org_id,
                organization_name=org["name"],
                create_id=create_id,
                workspaces=ws_choices,
            )
        )
    return groups


def _flatten_owned(groups: list[OrganizationGroup]) -> list[WorkspaceInfo]:
    """Concat all owned workspaces across groups (for auto-select-single check)."""
    out: list[WorkspaceInfo] = []
    for g in groups:
        out.extend(c["workspace"] for c in g["workspaces"])
    return out


def _get_workspace_name(
    user_info: Optional[UserInfo], workspace_id: str
) -> Optional[str]:
    """Look up the workspace name for the currently connected workspace."""
    if user_info is None:
        return None
    for ws in user_info["workspaces"]:
        if ws["id"] == workspace_id:
            return ws["name"]
    return None


def _get_workspace_org_name(
    user_info: Optional[UserInfo], workspace_id: str
) -> Optional[str]:
    """Look up the organization name for the given workspace."""
    if user_info is None:
        return None
    for ws in user_info["workspaces"]:
        if ws["id"] == workspace_id:
            return ws.get("organization_name")
    return None


def _ensure_profile_warning(required_profile: str) -> bool:
    """Warn if recommended profile is not set up."""
    try:
        ctx = active()
        available = set(ctx.available_profiles())
        if required_profile not in available:
            if required_profile == "access":
                fmt.warning(
                    "No 'access' profile detected. Only default config/secrets will be used. "
                    "Dashboard/notebook sharing may be limited."
                )
            elif required_profile == "prod":
                fmt.warning(
                    "No 'prod' profile detected. Only default config/secrets will be used."
                )
            return False
        return True
    except Exception:
        # Fallback silent; lack of profiles is non-fatal
        return False


def _generate_local_manifest(
    name_or_path: str, use_all: bool = True
) -> tuple[TJobsDeploymentManifest, str, list["ApiTJobDefinition"], list[str]]:
    """Generate a deployment manifest locally from a module or file."""

    manifest, manifest_hash, warnings = load_manifest_with_warnings(
        name_or_path, use_all=use_all
    )
    api_jobs = [ApiTJobDefinition.from_dict(job) for job in manifest["jobs"]]
    return manifest, manifest_hash, api_jobs, warnings


def _default_dashboard_manifest_bundle() -> tuple[
    TJobsDeploymentManifest, str, list["ApiTJobDefinition"], list[str]
]:
    """Build the ad-hoc dashboard-only manifest bundle."""

    manifest = default_dashboard_manifest()
    manifest_hash = generate_manifest_hash(manifest)
    api_jobs = [ApiTJobDefinition.from_dict(job) for job in manifest["jobs"]]
    return manifest, manifest_hash, api_jobs, []


# ---------------------------------------------------------------------------
# Service-dependent loaders (no display)
# ---------------------------------------------------------------------------


def _resolve_workspace_name(auth_service: RuntimeAuthService) -> Optional[str]:
    """Look up the human-readable name for the currently connected workspace."""
    try:
        user_info = auth_service.fetch_user_info()
    except Exception:
        return None
    return _get_workspace_name(user_info, auth_service.workspace_id)


def _resolve_job_ref_from_server(
    name_or_ref: str,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
    include_archived: bool = True,
) -> str:
    """Resolve a name / partial ref / UUID to a canonical job_ref. Raises if unresolved."""
    # UUID — pass through; the API resolves on `id`.
    try:
        UUID(name_or_ref)
        return name_or_ref
    except ValueError:
        pass

    # Qualified `section.name` / `jobs.section.name` — resolve locally (no server scope needed).
    if "." in name_or_ref:
        try:
            return str(resolve_job_ref(name_or_ref))
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            raise CliCommandInnerException(
                cmd="job",
                msg=JOB_SELECTOR_NOT_FOUND.format(selector=name_or_ref),
            )

    # Bare name — try local manifest first to avoid a server round-trip.
    try:
        manifest, _, _, _ = _generate_local_manifest(DEFAULT_DEPLOYMENT_MODULE)
        local_refs = [TJobRef(j["job_ref"]) for j in manifest.get("jobs", [])]
        try:
            return str(resolve_job_ref(name_or_ref, local_refs))
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            pass
    except Exception:
        # No local manifest — fall back to the server.
        pass

    # Bare name — fetch the workspace job list as the resolution scope.
    archived = (
        ListScriptsArchived.ALL if include_archived else ListScriptsArchived.FALSE
    )
    with handle_client_exceptions():
        res = list_scripts.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            archived=archived,
        )
    if isinstance(res.parsed, list_scripts.ListScriptsResponse200) and res.parsed.items:
        job_refs = [TJobRef(s.job_ref) for s in res.parsed.items]
        try:
            return str(resolve_job_ref(name_or_ref, job_refs))
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            pass

    raise CliCommandInnerException(
        cmd="job",
        msg=JOB_SELECTOR_NOT_FOUND.format(selector=name_or_ref),
    )


def _resolve_trigger_selectors(
    selectors: list[str],
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> tuple[list[str], list[str]]:
    """Split CLI args into (selectors, job_refs); bare names resolve to canonical job_refs."""
    out_selectors: list[str] = []
    out_job_refs: list[str] = []
    scripts: list[Any] | None = None

    for s in selectors:
        if is_selector(s):
            out_selectors.append(s)
            continue

        if scripts is None:
            try:
                scripts = _fetch_jobs(api_client, auth_service)
            except Exception:
                scripts = []

        job_refs = [sc.job_ref for sc in scripts]
        try:
            ref = str(resolve_job_ref(s, job_refs))
            out_job_refs.append(ref)
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            # Couldn't resolve — pass through as a selector; API will surface no-match.
            out_selectors.append(s)

    return out_selectors, out_job_refs


def requires_login(
    _func: Optional[Callable[..., Any]] = None, *, auto_login: bool = True
) -> Callable[..., Any]:
    """Inject authenticated `auth_service` kwarg; auto-runs login flow on missing token."""

    # `auto_login=True` (default): device flow starts when login required,
    # `--resume` is printed in non-interactive mode, controller body skipped via
    # `return None`. `auto_login=False` raises a clean error instead.
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            auth: Optional[RuntimeAuthService] = kwargs.pop("auth_service", None)
            if auth is None:
                auth = RuntimeAuthService(run_context=active())
            # api-key mode: no JWT to validate; bad keys raise at request time.
            if auth.has_api_key():
                kwargs["auth_service"] = auth
                return func(*args, **kwargs)
            try:
                auth.authenticate()
            except RuntimeNotAuthenticated as e:
                if not auto_login:
                    raise CliCommandInnerException(
                        cmd="dlthub",
                        msg="Not logged in. Run 'dlthub login' first.",
                        inner_exc=e,
                    ) from e
                # Late import: helpers → _runtime_command would otherwise cycle.
                from dlt_runtime._runtime_command import login as login_cmd

                result = login_cmd(minimal_logging=True, not_logged_in_hint=True)
                if result is None:
                    return None
                auth = result
            kwargs["auth_service"] = auth
            return func(*args, **kwargs)

        return wrapper

    return decorator if _func is None else decorator(_func)


def requires_workspace(
    _func: Optional[Callable[..., Any]] = None, *, auto_connect: bool = True
) -> Callable[..., Any]:
    """Require connected workspace_id; inject `api_client`. Stack under @requires_login."""

    # Reads `auth_service` already placed by @requires_login.
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            auth: Optional[RuntimeAuthService] = kwargs.get("auth_service")
            assert auth is not None, (
                "@requires_workspace must be stacked under @requires_login"
            )
            if not auth.has_workspace():
                if not auto_connect or auth.has_api_key():
                    raise CliCommandInnerException(
                        cmd="dlthub",
                        msg=(
                            "Not connected to workspace. "
                            "Run 'dlthub workspace connect <name>' first."
                        ),
                    )
                from dlt_runtime._runtime_command import _connect_workspace_with_picker

                _connect_workspace_with_picker(auth)
            api_client = kwargs.pop("api_client", None)
            if api_client is None:
                # Module-attribute lookup keeps `patch.object(runtime, ...)` effective.
                api_client = _runtime_module.get_api_client(auth)
            kwargs["api_client"] = api_client
            return func(*args, **kwargs)

        return wrapper

    return decorator if _func is None else decorator(_func)


def _get_latest_run(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    script_id_or_name: Optional[str] = None,
) -> DetailedRunResponse:
    """Get the latest run for a script or workspace if script is not provided."""
    if script_id_or_name:
        with handle_client_exceptions():
            script = get_script.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                script_id_or_ref=script_id_or_name,
            )
        if isinstance(script.parsed, get_script.DetailedScriptResponse):
            with handle_client_exceptions():
                runs = list_runs.sync_detailed(
                    client=api_client,
                    workspace_id=_to_uuid(auth_service.workspace_id),
                    script_id=script.parsed.id,
                    limit=1,
                )
            if isinstance(runs.parsed, list_runs.ListRunsResponse200):
                if not runs.parsed.items:
                    raise NoRunsFound("No runs executed for this job")
                else:
                    return runs.parsed.items[0]
            raise exception_from_response(
                f"Failed to get runs for script with name or id {script_id_or_name}",
                runs,
            )
        else:
            raise exception_from_response(
                f"Failed to get script with name or id {script_id_or_name}", script
            )

    else:
        with handle_client_exceptions():
            runs = list_runs.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                limit=1,
            )
        if isinstance(runs.parsed, list_runs.ListRunsResponse200):
            if not runs.parsed.items:
                raise NoRunsFound("No runs executed in this workspace")
            else:
                return runs.parsed.items[0]
        raise exception_from_response("Failed to get runs for workspace", runs)


def _fetch_run_detail(
    run_id: UUID,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> DetailedRunResponse:
    """Fetch a single run's current detail (status, timings, duration) by ID."""
    with handle_client_exceptions():
        result = get_run.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            run_id=run_id,
        )
    if not isinstance(result.parsed, DetailedRunResponse):
        raise exception_from_response("Failed to get run info", result)
    return result.parsed


def _fetch_available_regions(*, api_client: ApiClient) -> list[DataplaneInfo]:
    """Fetch available regions."""
    with handle_client_exceptions("Failed to fetch available regions"):
        result = list_dataplanes.sync_detailed(client=api_client)
    if not isinstance(result.parsed, list):
        raise exception_from_response("Failed to fetch available regions", result)
    return result.parsed


def _resolve_run_id_by_number(
    *,
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    script_path_or_job_name: str,
    run_number: int,
) -> UUID:
    with handle_client_exceptions():
        script = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_ref=script_path_or_job_name,
        )
    if not isinstance(script.parsed, get_script.DetailedScriptResponse):
        raise exception_from_response(
            f"Failed to get script with name or id {script_path_or_job_name}", script
        )
    with handle_client_exceptions():
        runs = list_runs.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id=script.parsed.id,
        )
    if (
        not isinstance(runs.parsed, list_runs.ListRunsResponse200)
        or not runs.parsed.items
    ):
        raise exception_from_response("Failed to get runs for script", runs)
    for r in runs.parsed.items:
        if r.number == run_number:
            return r.id
    raise CliCommandInnerException(
        cmd="job",
        msg=f"Run number {run_number} not found for script/job {script_path_or_job_name}",
    )


def _read_files_manifest_from_tar(stream: BytesIO) -> tuple[list[str], int]:
    """Read ``manifest.yaml`` from a deployment tarball and return its file list."""

    stream.seek(0)
    with tarfile.open(fileobj=stream, mode="r:*") as tar:
        member = tar.getmember("manifest.yaml")
        f = tar.extractfile(member)
        assert f is not None, "manifest.yaml in tarball is not a regular file"
        manifest = yaml.safe_load(f)
    files = manifest.get("files", [])
    file_names = [item["relative_path"] for item in files]
    return file_names, len(file_names)


def _post_upload_returning(
    upload_url: str,
    upload_token: str,
    files: dict[str, tuple[str, bytes, str]],
) -> dict[str, Any]:
    """POST tarball bytes to the DP API upload route and return the JSON body."""

    response = httpx.post(
        upload_url,
        files=files,
        headers={
            "Authorization": f"Bearer {upload_token}",
            "User-Agent": f"dlt-runtime-cli/{__version__}",
        },
        timeout=httpx.Timeout(60.0),
        verify=_tls_verify(),
    )
    if response.status_code not in (200, 201):
        raise CliCommandInnerException(
            "sync",
            f"Upload failed (HTTP {response.status_code}): {response.text[:500]}",
        )
    body: dict[str, Any] = response.json()
    return body


def _do_sync_deployment(
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
    dry_run: bool = False,
    compute_diff: bool = False,
) -> SyncResult:
    """Three-step sync: empty-body POST mints upload token; multipart upload
    to the DP API stores bytes in vault and writes the row back to the CP;
    the upload response carries the full ``DeploymentResponse``.
    """
    workspace_id = _to_uuid(auth_service.workspace_id)

    # Build the tarball locally (gives us the ``content_hash``) so we can
    # short-circuit when the latest deployment already matches.
    content_stream = BytesIO()
    package_builder = PackageBuilder(context=active())
    package_hash = package_builder.write_package_to_stream(
        file_selector=WorkspaceFileSelector(active()), output_stream=content_stream
    )
    with handle_client_exceptions():
        latest_deployment = get_latest_deployment.sync_detailed(
            workspace_id=workspace_id,
            client=api_client,
        )
    if isinstance(latest_deployment.parsed, get_latest_deployment.DeploymentResponse):
        if latest_deployment.parsed.content_hash == package_hash:
            content_stream.close()
            return SyncResult(status="no_changes")
    elif isinstance(latest_deployment.parsed, get_latest_deployment.ErrorResponse404):
        pass  # will create below
    else:
        content_stream.close()
        raise exception_from_response(
            "Failed to get latest deployment", latest_deployment
        )

    if dry_run:
        content_stream.close()
        return SyncResult(status="would_create", data={"package_hash": package_hash})

    # Export the workspace requirements manifest alongside the code tarball.
    try:
        manifest = export_workspace_requirements(Path(active().run_dir))
    except WorkspaceRequirementsError as ex:
        content_stream.close()
        raise CliCommandInnerException(
            "sync", f"Failed to export workspace requirements: {ex}"
        ) from ex
    requirements_stream = BytesIO()
    save_requirements(manifest, requirements_stream)
    requirements_bytes = requirements_stream.getvalue()

    code_bytes = content_stream.getvalue()

    # Step 1: empty-body POST — mints the DataplaneUserJwt + returns upload URL.
    with handle_client_exceptions():
        create_deployment_result = create_deployment.sync_detailed(
            workspace_id=workspace_id,
            client=api_client,
        )
    if not isinstance(create_deployment_result.parsed, UploadInitiatedResponse):
        raise exception_from_response(
            "Failed to create deployment", create_deployment_result
        )
    initiated = create_deployment_result.parsed

    # Step 2: multipart upload to the DP API. Response is the full row.
    deployment_dict = _post_upload_returning(
        upload_url=initiated.upload_url,
        upload_token=initiated.upload_token,
        files={
            "files": ("workspace.tar.gz", code_bytes, "application/x-tar"),
            "requirements": (
                "requirements.json",
                requirements_bytes,
                "application/json",
            ),
        },
    )
    return SyncResult(
        status="created",
        data=_extract_keys(deployment_dict, DEPLOYMENT_HEADERS),
    )


def _do_sync_configuration(
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
    dry_run: bool = False,
    compute_diff: bool = False,
) -> SyncResult:
    """Three-step sync (configuration variant). See ``_do_sync_deployment``."""
    workspace_id = _to_uuid(auth_service.workspace_id)
    content_stream = BytesIO()
    package_builder = PackageBuilder(context=active())
    package_hash = package_builder.write_package_to_stream(
        file_selector=ConfigurationFileSelector(active()), output_stream=content_stream
    )

    with handle_client_exceptions():
        latest_configuration = get_latest_configuration.sync_detailed(
            workspace_id=workspace_id,
            client=api_client,
        )
    if isinstance(
        latest_configuration.parsed, get_latest_configuration.ConfigurationResponse
    ):
        if latest_configuration.parsed.content_hash == package_hash:
            content_stream.close()
            return SyncResult(status="no_changes")
    elif isinstance(
        latest_configuration.parsed,
        get_latest_configuration.ErrorResponse404,
    ):
        pass  # will create below
    else:
        content_stream.close()
        raise exception_from_response(
            "Failed to get latest configuration", latest_configuration
        )

    if dry_run:
        content_stream.close()
        return SyncResult(status="would_create", data={"package_hash": package_hash})

    config_bytes = content_stream.getvalue()

    with handle_client_exceptions():
        create_configuration_result = create_configuration.sync_detailed(
            workspace_id=workspace_id,
            client=api_client,
        )
    if not isinstance(create_configuration_result.parsed, UploadInitiatedResponse):
        raise exception_from_response(
            "Failed to create configuration", create_configuration_result
        )
    initiated = create_configuration_result.parsed

    config_dict = _post_upload_returning(
        upload_url=initiated.upload_url,
        upload_token=initiated.upload_token,
        files={
            "data": (
                "configurations.tar.gz",
                config_bytes,
                "application/x-tar",
            ),
        },
    )
    return SyncResult(
        status="created",
        data=_extract_keys(config_dict, CONFIGURATION_HEADERS),
    )


def _fetch_runtime_info(
    *, auth_service: RuntimeAuthService, api_client: ApiClient
) -> RuntimeInfo:
    """Fetch workspace overview data — returns RuntimeInfo model."""
    user_info = auth_service.fetch_user_info()
    ws_id = auth_service.workspace_id

    info = RuntimeInfo(
        workspace_id=ws_id,
        workspace_name=_get_workspace_name(user_info, ws_id),
        organization_name=_get_workspace_org_name(user_info, ws_id),
        workspace_url=urls.workspace_url(ws_id),
        local_dir=str(active().run_dir),
        job_count=0,
    )
    if user_info is not None:
        info["email"] = user_info["email"]

    # jobs
    with handle_client_exceptions():
        scr = list_scripts.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(ws_id),
        )
    if isinstance(scr.parsed, list_scripts.ListScriptsResponse200) and scr.parsed.items:
        info["job_count"] = len(scr.parsed.items)

    # latest run
    try:
        latest_run = _get_latest_run(api_client, auth_service)
    except NoRunsFound:
        latest_run = None
    if isinstance(latest_run, DetailedRunResponse):
        # No manifest in this code path — `section.name` is the safe shortest form.
        info["latest_run_name"] = format_job_selector(
            latest_run.script.job_definition.job_ref
        )
        info["latest_run_status"] = str(latest_run.status)
        if isinstance(latest_run.time_started, datetime):
            info["latest_run_started"] = latest_run.time_started
        if isinstance(latest_run.time_ended, datetime):
            info["latest_run_ended"] = latest_run.time_ended
    elif latest_run is not None:
        raise exception_from_response("Failed to get latest run", latest_run)

    # deployment
    with handle_client_exceptions():
        latest_deployment = get_latest_deployment.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(ws_id),
        )
    if isinstance(latest_deployment.parsed, get_latest_deployment.DeploymentResponse):
        info["deployment_version"] = latest_deployment.parsed.version
        info["deployment_date"] = latest_deployment.parsed.date_added
    elif not isinstance(
        latest_deployment.parsed, get_latest_deployment.ErrorResponse404
    ):
        raise exception_from_response(
            "Failed to get latest deployment", latest_deployment
        )

    # configuration
    with handle_client_exceptions():
        latest_configuration = get_latest_configuration.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(ws_id),
        )
    if isinstance(
        latest_configuration.parsed, get_latest_configuration.ConfigurationResponse
    ):
        info["configuration_version"] = latest_configuration.parsed.version
        info["configuration_date"] = latest_configuration.parsed.date_added
    elif not isinstance(
        latest_configuration.parsed, get_latest_configuration.ErrorResponse404
    ):
        raise exception_from_response(
            "Failed to get latest configuration", latest_configuration
        )

    # Predefined profiles from the current workspace (server-side)
    if user_info is not None:
        for ws in user_info["workspaces"]:
            if ws["id"] == ws_id and ws.get("predefined_profiles"):
                info["predefined_profiles"] = dict(ws["predefined_profiles"])
                break

    return info


LogStreamEvent = tuple[Literal["log", "warning", "error"], str]


def _resolve_dataplane_logs_endpoint(
    api_client: ApiClient,
    workspace_id: UUID,
) -> tuple[str, str]:
    """Return ``(dataplane_base_url, dataplane_user_jwt)`` for the workspace.

    Reads the workspace to get its ``dataplane_url`` and mints a fresh
    DataplaneUserJwt — used by the logs service for both the static fetch and
    the SSE stream.
    """
    with handle_client_exceptions("Failed to read workspace"):
        ws_resp = get_workspace_api.sync_detailed(
            client=api_client, workspace_id=workspace_id
        )
    if not isinstance(ws_resp.parsed, WorkspaceResponse):
        raise exception_from_response("Failed to read workspace", ws_resp)

    with handle_client_exceptions("Failed to mint dataplane access token"):
        token_resp = get_workspace_dataplane_access_token.sync_detailed(
            client=api_client, workspace_id=workspace_id
        )
    if not isinstance(token_resp.parsed, DataplaneAccessTokenResponse):
        raise exception_from_response(
            "Failed to mint dataplane access token", token_resp
        )

    return ws_resp.parsed.dataplane_url.rstrip("/"), token_resp.parsed.token


def _build_logs_request(
    suffix: str,
    accept: str,
    *,
    run_id: UUID,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> tuple[str, dict[str, str]]:
    """Resolve the dataplane logs endpoint and build the request URL + auth headers."""
    workspace_id = _to_uuid(auth_service.workspace_id)
    dataplane_url, dataplane_token = _resolve_dataplane_logs_endpoint(
        api_client, workspace_id
    )
    url = f"{dataplane_url}/logs/v1/workspaces/{workspace_id}/runs/{run_id}{suffix}"
    headers = {
        "Accept": accept,
        "User-Agent": f"dlt-runtime-cli/{__version__}",
        "Authorization": f"Bearer {dataplane_token}",
    }
    return url, headers


def _should_hide_log_line(log: LogLine) -> bool:
    """Drop runner-internal diagnostics and provider lifecycle noise from user output."""
    return log.phase in ("runner", "provider")


def _parse_log_line_event(json_str: str) -> Optional[LogStreamEvent]:
    """Parse a JSON-encoded LogLine into a ``('log', formatted)`` event."""

    try:
        log = LogLine.from_dict(json.loads(json_str))
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
        return ("warning", f"Failed to parse log line: {e}")
    if _should_hide_log_line(log):
        return None
    return ("log", _format_log_line(log))


def _iter_run_logs_historical(
    run_id: UUID,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> Generator[LogStreamEvent, None, None]:
    """Yield ``(level, message)`` for each NDJSON log line of a terminal run."""
    url, headers = _build_logs_request(
        "/logs",
        "application/x-ndjson",
        run_id=run_id,
        auth_service=auth_service,
        api_client=api_client,
    )
    try:
        with httpx.stream(
            "GET", url, headers=headers, verify=_tls_verify()
        ) as response:
            if response.status_code == 404:
                yield ("error", "Run logs not found.")
                return
            if response.status_code != 200:
                yield ("error", f"Failed to fetch run logs: {response.status_code}")
                return
            for line in response.iter_lines():
                if not line:
                    continue
                event = _parse_log_line_event(line)
                if event is not None:
                    yield event
    except httpx.HTTPError as e:
        yield ("error", f"HTTP error while fetching logs: {e}")


def _iter_run_log_stream(
    run_id: UUID,
    *,
    follow: bool = True,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> Generator[LogStreamEvent, None, None]:
    """Yield ``(level, message)`` events from the live SSE log stream.

    When *follow* is False the generator replays existing logs and stops;
    a 1-second read timeout detects the end of the replay.
    """
    url, headers = _build_logs_request(
        "/logs/stream",
        "text/event-stream",
        run_id=run_id,
        auth_service=auth_service,
        api_client=api_client,
    )
    # In non-follow mode a 1 s read timeout acts as end-of-replay detection.
    stream_timeout = None if follow else httpx.Timeout(None, read=1.0)

    try:
        with httpx.stream(
            "GET",
            url,
            headers=headers,
            timeout=stream_timeout,
            verify=_tls_verify(),
        ) as response:
            if response.status_code != 200:
                yield (
                    "error",
                    f"Failed to connect to log stream: {response.status_code}",
                )
                return
            try:
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        event = _parse_log_line_event(line[6:])
                        if event is not None:
                            yield event
                    elif line.startswith("event: error"):
                        yield ("error", "Stream error event received")
                        return
            except httpx.ReadTimeout:
                return
    except httpx.HTTPError as e:
        yield ("error", f"HTTP error while streaming logs: {e}")
    except Exception as e:
        yield ("error", f"Error streaming logs: {e}")


# ---------------------------------------------------------------------------
# Entity loaders (fetch API data, return models — no display)
# ---------------------------------------------------------------------------


def _fetch_workspaces(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
) -> tuple[list[Any], Optional[str]]:
    """Return (workspaces, current_workspace_id) for display."""
    try:
        current_ws_id: Optional[str] = auth_service.workspace_id
    except (RuntimeOperationNotAuthorized, WorkspaceRunContextNotAvailable):
        current_ws_id = None
    return user_info["workspaces"], current_ws_id


def _fetch_job_run_info(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    *,
    script_path_or_job_name: str,
    run_number: Optional[int] = None,
) -> "get_run.DetailedRunResponse":
    """Resolve and fetch a single run, return DetailedRunResponse."""
    if run_number is None:
        run = _get_latest_run(api_client, auth_service, script_path_or_job_name)
        run_id = run.id
    else:
        run_id = _resolve_run_id_by_number(
            api_client=api_client,
            auth_service=auth_service,
            script_path_or_job_name=script_path_or_job_name,
            run_number=run_number,
        )

    with handle_client_exceptions():
        get_run_result = get_run.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            run_id=_to_uuid(run_id),
        )
    if isinstance(get_run_result.parsed, get_run.DetailedRunResponse):
        return get_run_result.parsed
    raise exception_from_response("Failed to get run status", get_run_result)


def _fetch_runs(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    script_path_or_job_name: Optional[str] = None,
    *,
    running_only: bool = False,
) -> list[Any]:
    """Fetch runs, optionally filtered by script. Returns runs sorted desc by number."""
    # `running_only` filters out terminal-state runs client-side; the server
    # endpoint has no equivalent flag yet (issue: TODO follow-up).
    script_id: Optional[UUID] = None
    if script_path_or_job_name:
        with handle_client_exceptions():
            script = get_script.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                script_id_or_ref=script_path_or_job_name,
            )
        if isinstance(script.parsed, get_script.DetailedScriptResponse):
            script_id = script.parsed.id
        else:
            raise exception_from_response(
                f"Failed to get script with name {script_path_or_job_name} from runtime."
                " Did you create one?",
                script,
            )

    with handle_client_exceptions():
        list_runs_result = list_runs.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id=script_id,
        )
    if not isinstance(list_runs_result.parsed, list_runs.ListRunsResponse200):
        raise exception_from_response("Failed to list workspace runs", list_runs_result)

    items = list(list_runs_result.parsed.items) if list_runs_result.parsed.items else []
    if running_only:
        items = [r for r in items if r.status in NON_TERMINAL_RUN_STATUSES]
    # Server orders by date_added DESC; trust that — no client-side resort.
    return items


def _fetch_deployments(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
) -> list[Any]:
    """Fetch all deployments. Returns list of deployment models."""
    with handle_client_exceptions():
        list_deployments_result = list_deployments.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(
        list_deployments_result.parsed, list_deployments.ListDeploymentsResponse200
    ):
        return (
            list(list_deployments_result.parsed.items)
            if list_deployments_result.parsed.items
            else []
        )
    raise exception_from_response("Failed to list deployments", list_deployments_result)


def _fetch_deployment_info(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    deployment_version_no: Optional[int] = None,
) -> Any:
    """Fetch a single deployment (latest or by version). Returns deployment model."""
    if deployment_version_no is None:
        with handle_client_exceptions():
            result = get_latest_deployment.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
            )
    else:
        with handle_client_exceptions():
            result = get_deployment.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                deployment_id_or_version=deployment_version_no,
            )
    if isinstance(result.parsed, get_deployment.DeploymentResponse):
        return result.parsed
    raise exception_from_response("Failed to get deployment info", result)


def _fetch_configurations(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
) -> list[Any]:
    """Fetch all configurations. Returns list of configuration models."""
    with handle_client_exceptions():
        list_configurations_result = list_configurations.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
        )
    if isinstance(
        list_configurations_result.parsed,
        list_configurations.ListConfigurationsResponse200,
    ) and isinstance(list_configurations_result.parsed.items, list):
        return (
            list(list_configurations_result.parsed.items)
            if list_configurations_result.parsed.items
            else []
        )
    raise exception_from_response(
        "Failed to list configurations", list_configurations_result
    )


def _fetch_configuration_info(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    configuration_version_no: Optional[int] = None,
) -> Any:
    """Fetch a single configuration (latest or by version). Returns configuration model."""
    if configuration_version_no is None:
        with handle_client_exceptions():
            result = get_latest_configuration.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
            )
    else:
        with handle_client_exceptions():
            result = get_configuration.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                configuration_id_or_version=configuration_version_no,
            )
    if isinstance(result.parsed, get_configuration.ConfigurationResponse):
        return result.parsed
    raise exception_from_response("Failed to get configuration info", result)


def _fetch_jobs(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    *,
    include_archived: bool = False,
) -> list[Any]:
    """Fetch all jobs (scripts). Returns list of script models."""
    archived = (
        ListScriptsArchived.ALL if include_archived else ListScriptsArchived.FALSE
    )
    with handle_client_exceptions():
        res = list_scripts.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            archived=archived,
        )
    if isinstance(res.parsed, list_scripts.ListScriptsResponse200) and isinstance(
        res.parsed.items, list
    ):
        return list(res.parsed.items) if res.parsed.items else []
    raise exception_from_response("Failed to list jobs", res)


def _filter_scripts_by_selectors(
    scripts: list[Any],
    selectors: list[str],
) -> list[Any]:
    """Filter ScriptResponse objects by trigger selectors (client-side).

    Empty selectors → empty match (nothing was asked for).
    """
    if not selectors:
        return []

    matched = []
    for script in scripts:
        raw_triggers = getattr(script, "triggers", None)
        if raw_triggers is None or isinstance(raw_triggers, Unset):
            triggers: list[TTrigger] = []
        else:
            triggers = [TTrigger(t) for t in raw_triggers]
        job_type = (
            script.script_type.value
            if hasattr(script.script_type, "value")
            else str(script.script_type)
        )
        if match_triggers_with_selectors(job_type, triggers, selectors):
            matched.append(script)
    return matched


def _resolve_selectors_to_scripts(
    args: list[str],
    *,
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    include_archived: bool = False,
) -> list[Any]:
    """Resolve CLI selector/job-ref args to matched ScriptResponse objects.

    Splits *args* into selectors and bare job refs, fetches all jobs,
    applies selector matching and ref resolution, returns the union.
    Returns all scripts when *args* is empty.
    """
    scripts = _fetch_jobs(api_client, auth_service, include_archived=include_archived)
    if not args:
        return scripts

    selectors: list[str] = []
    ref_set: set[str] = set()
    job_refs = [sc.job_ref for sc in scripts]

    for s in args:
        if is_selector(s):
            selectors.append(s)
        else:
            try:
                ref_set.add(str(resolve_job_ref(s, job_refs)))
            except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
                selectors.append(s)

    selector_matched = _filter_scripts_by_selectors(scripts, selectors)
    ref_matched = [sc for sc in scripts if sc.job_ref in ref_set]

    seen: set[str] = set()
    result: list[Any] = []
    for sc in [*selector_matched, *ref_matched]:
        if sc.job_ref not in seen:
            seen.add(sc.job_ref)
            result.append(sc)
    return result


def _fetch_job_info(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    script_path_or_job_name: str,
) -> Any:
    """Fetch a single job (script). Returns script model."""
    with handle_client_exceptions():
        res = get_script.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            script_id_or_ref=script_path_or_job_name,
        )
    if isinstance(res.parsed, get_script.DetailedScriptResponse):
        return res.parsed
    raise exception_from_response("Failed to get job info", res)


def _do_deploy_manifest(
    *,
    manifest_hash: str,
    api_jobs: list["ApiTJobDefinition"],
    deployment_module: str | None,
    description: str | None,
    dry_run: bool,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> "DeployManifestResponse":
    """Call deploy_manifest API and return the response."""
    with handle_client_exceptions():
        result = deploy_manifest.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
            body=DeployManifestRequest(
                job_definition_engine_version=MANIFEST_ENGINE_VERSION,
                job_definition_hash=manifest_hash,
                jobs=api_jobs,
                deployment_module=deployment_module,
                description=description,
                dry_run=dry_run,
            ),
        )
    if isinstance(result.parsed, deploy_manifest.DeployManifestResponse):
        return result.parsed
    raise exception_from_response("Failed to deploy manifest", result)
