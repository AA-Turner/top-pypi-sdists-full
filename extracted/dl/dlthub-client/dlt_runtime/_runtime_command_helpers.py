"""Helper functions for runtime CLI commands.

Pure helpers (no service deps) and service-dependent loaders (no display).
"""

# Python internals
import json
from datetime import datetime, timedelta, timezone
from functools import wraps
from inspect import signature
from io import BytesIO
from pathlib import Path
from typing import (
    Any,
    Callable,
    Literal,
    Mapping,
    NoReturn,
    Optional,
    Sequence,
    Union,
    cast,
)
from uuid import UUID

# Other libraries
from dlt._workspace._workspace_context import active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.cli.exceptions import CliCommandInnerException
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
from dlt._workspace.deployment.typing import TJobRef, TJobsDeploymentManifest, TTrigger
from dlt._workspace.exceptions import WorkspaceRunContextNotAvailable
from dlt.common.json import json as json_dlt

# Current package
from dlt_runtime import runtime as _runtime_module, urls

# Re-export view constants needed by loaders
from dlt_runtime._runtime_command_views import (  # noqa: F401
    CONFIGURATION_HEADERS,
    DEPLOYMENT_HEADERS,
    _extract_keys,
    _preprocess_run_output,
    format_job_selector,
)
from dlt_runtime.exceptions import (
    AmbiguousWorkspaceName,
    NoRunsFound,
    RuntimeClientException,
    RuntimeNotAuthenticated,
    RuntimeOperationNotAuthorized,
    WorkspaceNotFound,
    handle_client_exceptions,
)
from dlt_runtime.runtime import AuthenticationMethod, CliSession, PrincipalKind
from dlt_runtime.strings import (
    JOB_SELECTOR_NOT_FOUND,
    NOT_CONNECTED_TO_WORKSPACE,
    ORG_ID_CONFLICTS_WITH_PIN,
    ORG_ID_NOT_ACTIVE,
    PINNED_ORG_NOT_ACCESSIBLE,
    UNPIN_ORG_REMEDIATION,
    WORKSPACE_API_KEY_NO_WORKSPACE,
    WORKSPACE_BELONGS_TO_OTHER_ORG,
)
from dlt_runtime.typing import (
    CallerInfo,
    OrganizationGroup,
    OrganizationInfo,
    RuntimeInfo,
    SyncResult,
    WorkspaceChoice,
    WorkspaceInfo,
)
from dlthub_sdk import (
    KEEP,
    WORKSPACE_PROFILE,
    Configuration,
    Dataplane,
    Deployment,
    DeployReport,
    Job,
    JobRun,
    Keep,
    LogLine,
    Runtime,
    Sync,
    VariableChange,
    VariableScope,
    Workspace,
)
from dlthub_sdk.errors import NotFound as SdkNotFound


def _run_id_from_ref(ref: str, run_number: Optional[int] = None) -> Optional[UUID]:
    """Extracts job run UUID from `ref` and returns it, mixing with `run_number` is not allowed"""
    try:
        run_id = UUID(ref)
    except (AttributeError, TypeError, ValueError):
        return None
    if run_number is not None:
        raise CliCommandInnerException(
            cmd="job",
            msg=(
                f"Run number {run_number} cannot be combined with run id {ref}."
                " Pass a run id on its own, or a job reference with a run number."
            ),
        )
    return run_id


def _resolve_workspace_id(caller_info: CallerInfo, workspace: str) -> str:
    """Resolve a workspace name or ID to an owned workspace ID."""

    workspace = workspace.strip()

    # Exact ID match is always unambiguous — return immediately.
    for ws in caller_info["workspaces"]:
        if ws.get("role") == "owner" and workspace == ws["id"]:
            return ws["id"]

    matches = [
        ws
        for ws in caller_info["workspaces"]
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


def _active_orgs(caller_info: CallerInfo) -> list[OrganizationInfo]:
    """All organizations the caller is an active member of."""
    return [org for org in caller_info["organizations"] if org.get("active", True)]


def _sole_active_org_id(caller_info: CallerInfo) -> Optional[str]:
    """Return the single active org's id, or None if zero or multiple."""
    actives = _active_orgs(caller_info)
    return actives[0]["id"] if len(actives) == 1 else None


def _org_label(caller_info: CallerInfo, organization_id: str) -> str:
    """Render an org as `name (id)` if the name is known, else just the id."""
    for org in caller_info["organizations"]:
        if org["id"] == organization_id:
            return f"{org['name']} ({organization_id})"
    return organization_id


def _scope_caller_info_to_org(
    caller_info: CallerInfo, organization_id: str
) -> CallerInfo:
    """Return a CallerInfo whose `workspaces` and `organizations` are filtered to one org."""
    scoped: CallerInfo = {
        "workspaces": [
            ws
            for ws in caller_info["workspaces"]
            if ws.get("organization_id") == organization_id
        ],
        "organizations": [
            org for org in caller_info["organizations"] if org["id"] == organization_id
        ],
    }
    if "identity" in caller_info:
        scoped["identity"] = caller_info["identity"]
    return scoped


def _validate_org_id(caller_info: CallerInfo, org_id: str) -> None:
    """Raise if `org_id` (from `--org-id`) is not in the caller's active organizations."""
    actives = _active_orgs(caller_info)
    if any(org["id"] == org_id for org in actives):
        return
    valid = ", ".join(f"{org['name']} ({org['id']})" for org in actives) or "<none>"
    raise CliCommandInnerException(
        cmd="workspace",
        msg=ORG_ID_NOT_ACTIVE.format(org_id=org_id, valid=valid),
    )


def _validate_pinned_org_id(caller_info: CallerInfo, pinned_org_id: str) -> None:
    """Raise if the org pinned in `.dlt/config.toml` is not in the caller's active orgs."""
    # Distinct message from `_validate_org_id`: the user must remove the line
    # from config.toml manually (CLI never overwrites it).
    if any(org["id"] == pinned_org_id for org in _active_orgs(caller_info)):
        return
    raise CliCommandInnerException(
        cmd="workspace",
        msg=PINNED_ORG_NOT_ACCESSIBLE.format(
            pinned_org_id=pinned_org_id, remediation=UNPIN_ORG_REMEDIATION
        ),
    )


def _check_org_arg_matches_pin(
    caller_info: CallerInfo, pinned_org_id: Optional[str], org_id: str
) -> None:
    """Raise if `--org-id` disagrees with the org pinned in config.toml."""
    if not pinned_org_id or pinned_org_id == org_id:
        return
    raise CliCommandInnerException(
        cmd="workspace",
        msg=ORG_ID_CONFLICTS_WITH_PIN.format(
            org_id=org_id,
            pinned_label=_org_label(caller_info, pinned_org_id),
            remediation=UNPIN_ORG_REMEDIATION,
        ),
    )


def _resolve_effective_org_id(
    caller_info: CallerInfo,
    pinned_org_id: Optional[str],
    org_id: Optional[str],
) -> Optional[str]:
    """Settle the org scope for a `connect` call (validation + precedence).

    Precedence: pinned org in config.toml > `--org-id` flag > None.
    Raises if `--org-id` is unknown or disagrees with the pin, or if the
    pinned org is no longer accessible.
    """
    if org_id is not None:
        _validate_org_id(caller_info, org_id)
        _check_org_arg_matches_pin(caller_info, pinned_org_id, org_id)
    elif pinned_org_id:
        # Stale pin (org deleted / membership removed) — surface before
        # scoping yields an empty group list.
        _validate_pinned_org_id(caller_info, pinned_org_id)
    return pinned_org_id or org_id


def _raise_cross_org(
    caller_info: CallerInfo, ws: WorkspaceInfo, effective_org_id: str
) -> NoReturn:
    """Raise the standard "workspace lives in a different org" error."""
    raise CliCommandInnerException(
        cmd="workspace",
        msg=WORKSPACE_BELONGS_TO_OTHER_ORG.format(
            ws_name=ws["name"],
            ws_org=ws.get("organization_name") or ws.get("organization_id"),
            effective_label=_org_label(caller_info, effective_org_id),
            remediation=UNPIN_ORG_REMEDIATION,
        ),
    )


def _org_id_to_persist(
    caller_info: CallerInfo,
    resolved_ws: Optional[WorkspaceInfo],
    effective_org_id: Optional[str],
) -> str:
    """Pick the org_id to write_connection persists (write-once)."""
    # Prefer the resolved workspace's own org → effective scope → first active org.
    if resolved_ws is not None and resolved_ws.get("organization_id"):
        return resolved_ws["organization_id"]
    if effective_org_id:
        return effective_org_id
    return _active_orgs(caller_info)[0]["id"]


def _group_workspaces_by_org(caller_info: CallerInfo) -> list[OrganizationGroup]:
    """Build picker groups: one section per active org, owned workspaces only."""
    # Ids stamped here drive both the view (`[N]` labels) and the picker
    # resolver — single source of truth for the numbering.
    groups: list[OrganizationGroup] = []
    next_id = 0
    # Server order keeps the picker layout stable across invocations.
    for org in _active_orgs(caller_info):
        org_id = org["id"]
        owned = [
            ws
            for ws in caller_info["workspaces"]
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


def _get_workspace_name(
    workspaces: list[WorkspaceInfo], workspace_id: str
) -> Optional[str]:
    """Look up the workspace name for the currently connected workspace."""
    for ws in workspaces:
        if ws["id"] == workspace_id:
            return ws["name"]
    return None


def _get_workspace_org_name(
    workspaces: list[WorkspaceInfo], workspace_id: str
) -> Optional[str]:
    """Look up the organization name for the given workspace."""
    for ws in workspaces:
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


def _job_to_api_item(job: Any) -> Mapping[str, Any]:
    # manifests keep datetime interval bounds; the SDK wraps each definition
    # free-form, so render JSON-native (isoformat) before handing it over.
    return cast(Mapping[str, Any], json.loads(json_dlt.dumps(job)))


def _generate_local_manifest(
    name_or_path: str, use_all: bool = True
) -> tuple[TJobsDeploymentManifest, str, list[Mapping[str, Any]], list[str]]:
    """Generate a deployment manifest locally from a module or file."""

    manifest, manifest_hash, warnings = load_manifest_with_warnings(
        name_or_path, use_all=use_all
    )
    api_jobs = [_job_to_api_item(job) for job in manifest["jobs"]]
    return manifest, manifest_hash, api_jobs, warnings


def _default_dashboard_manifest_bundle() -> tuple[
    TJobsDeploymentManifest, str, list[Mapping[str, Any]], list[str]
]:
    """Build the ad-hoc dashboard-only manifest bundle."""

    manifest = default_dashboard_manifest()
    manifest_hash = generate_manifest_hash(manifest)
    api_jobs = [_job_to_api_item(job) for job in manifest["jobs"]]
    return manifest, manifest_hash, api_jobs, []


# ---------------------------------------------------------------------------
# Service-dependent loaders (no display)
# ---------------------------------------------------------------------------


def _resolve_job_ref_from_server(
    name_or_ref: str,
    *,
    workspace: Workspace[Sync],
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
    jobs = _fetch_jobs(workspace, include_archived=include_archived)
    if jobs:
        try:
            return str(resolve_job_ref(name_or_ref, [TJobRef(j.job_ref) for j in jobs]))
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            pass

    raise CliCommandInnerException(
        cmd="job",
        msg=JOB_SELECTOR_NOT_FOUND.format(selector=name_or_ref),
    )


def _resolve_trigger_selectors(
    selectors: list[str],
    *,
    workspace: Workspace[Sync],
) -> tuple[list[str], list[str]]:
    """Split CLI args into (selectors, job_refs); bare names resolve to canonical job_refs."""
    out_selectors: list[str] = []
    out_job_refs: list[str] = []
    scripts: list[Job[Sync]] | None = None

    for s in selectors:
        if is_selector(s):
            out_selectors.append(s)
            continue

        if scripts is None:
            try:
                scripts = _fetch_jobs(workspace)
            except Exception:
                scripts = []

        job_refs = [TJobRef(sc.job_ref) for sc in scripts]
        try:
            ref = str(resolve_job_ref(s, job_refs))
            out_job_refs.append(ref)
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            # Couldn't resolve — pass through as a selector; API will surface no-match.
            out_selectors.append(s)

    return out_selectors, out_job_refs


def requires_auth(
    _func: Optional[Callable[..., Any]] = None, *, auto_login: bool = True
) -> Callable[..., Any]:
    """Inject authenticated `session` kwarg; auto-runs login flow on missing
    token, unless an API key is configured."""

    # `auto_login=True` (default): device flow starts when login required,
    # `--resume` is printed in non-interactive mode, controller body skipped via
    # `return None`. `auto_login=False` raises a clean error instead.
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            session: Optional[CliSession] = kwargs.pop("session", None)
            if session is None:
                session = CliSession(run_context=active())
            # api-key mode: no JWT to validate; principal_kind() rejects unknown prefixes early
            if session.authentication_method() is AuthenticationMethod.API_KEY:
                session.principal_kind()
                kwargs["session"] = session
                return func(*args, **kwargs)
            try:
                session.authenticate()
            except RuntimeNotAuthenticated as e:
                if not auto_login:
                    raise CliCommandInnerException(
                        cmd="dlthub",
                        msg="Not logged in. Run 'dlthub login' first.",
                        inner_exc=e,
                    ) from e
                # Late import: helpers → _runtime_command would otherwise cycle.
                # Current package
                from dlt_runtime._runtime_command import (  # noqa: PLC0415
                    login as login_cmd,
                )

                result = login_cmd(minimal_logging=True, not_logged_in_hint=True)
                if result is None:
                    return None
                session = result
            kwargs["session"] = session
            return func(*args, **kwargs)

        return wrapper

    return decorator if _func is None else decorator(_func)


def requires_workspace(
    _func: Optional[Callable[..., Any]] = None,
    *,
    auto_connect: bool = True,
) -> Callable[..., Any]:
    """Require connected workspace_id; inject `runtime`. Stack under @requires_auth."""

    # Reads `session` already placed by @requires_auth.
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        wanted = set(signature(func).parameters)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            session: Optional[CliSession] = kwargs.get("session")
            assert session is not None, (
                "@requires_workspace must be stacked under @requires_auth"
            )
            if not session.has_workspace():
                if session.principal_kind() is PrincipalKind.SERVICE_ACCOUNT:
                    raise CliCommandInnerException(
                        cmd="dlthub", msg=WORKSPACE_API_KEY_NO_WORKSPACE
                    )
                if (
                    not auto_connect
                    or session.authentication_method() is AuthenticationMethod.API_KEY
                ):
                    raise CliCommandInnerException(
                        cmd="dlthub", msg=NOT_CONNECTED_TO_WORKSPACE
                    )
                # Current package
                from dlt_runtime._runtime_command import (  # noqa: PLC0415
                    _connect_workspace_with_picker,
                )

                _connect_workspace_with_picker(session)
            # Each command declares what it needs; the workspace is read once
            # here rather than re-derived by every loader it calls.
            # Module-attribute lookup keeps `patch.object(runtime, ...)` effective.
            client = kwargs.get("runtime")
            if client is None and {"runtime", "workspace"} & wanted:
                client = _runtime_module.get_sdk_runtime(session)
            if "runtime" in wanted:
                kwargs["runtime"] = client
            if "workspace" in wanted and kwargs.get("workspace") is None:
                assert client is not None
                with handle_client_exceptions():
                    kwargs["workspace"] = client.workspaces.get(id=session.workspace_id)
            if "session" not in wanted:
                kwargs.pop("session", None)
            return func(*args, **kwargs)

        return wrapper

    return decorator if _func is None else decorator(_func)


def _get_latest_run(
    workspace: Workspace[Sync],
    script_id_or_name: Optional[str] = None,
) -> JobRun[Sync]:
    """Get the latest run for a script or workspace if script is not provided."""
    with handle_client_exceptions():
        runs = (
            workspace.jobs.get(ref=script_id_or_name).runs
            if script_id_or_name
            else workspace.job_runs
        )
    # Translated outside the shim: it wraps everything raised inside it, so a
    # NoRunsFound raised in there would reach `workspace info` as a RuntimeError.
    try:
        with handle_client_exceptions():
            return runs.latest()
    except RuntimeClientException as e:
        # The platform reports "nothing has run yet" the same way it reports a
        # missing job; the job above already proved it exists.
        if not isinstance(e.__cause__, SdkNotFound):
            raise
        raise NoRunsFound(
            "No runs executed for this job"
            if script_id_or_name
            else "No runs executed in this workspace"
        ) from e


def _fetch_run_detail(
    run_id: UUID,
    *,
    workspace: Workspace[Sync],
) -> JobRun[Sync]:
    """Fetch a single run's current detail (status, timings, duration) by ID."""
    with handle_client_exceptions():
        return workspace.job_runs.get(id=str(run_id))


def _fetch_available_regions(*, runtime: Runtime[Sync]) -> Sequence[Dataplane[Sync]]:
    """Fetch available regions."""
    with handle_client_exceptions("Failed to fetch available regions"):
        return runtime.dataplanes.list()


def _resolve_run_id_by_number(
    *,
    workspace: Workspace[Sync],
    script_path_or_job_name: str,
    run_number: int,
) -> UUID:
    # Client-side: the platform cannot address a run by its number.
    with handle_client_exceptions():
        job = workspace.jobs.get(ref=script_path_or_job_name)
        for run in job.runs.list():
            if run.number == run_number:
                return UUID(run.id)
    raise CliCommandInnerException(
        cmd="job",
        msg=f"Run number {run_number} not found for script/job {script_path_or_job_name}",
    )


def _do_sync_deployment(
    *,
    workspace: Workspace[Sync],
    dry_run: bool = False,
) -> SyncResult:
    """Three-step sync: empty-body POST mints upload token; multipart upload
    to the DP API stores bytes in vault and writes the row back to the CP;
    the upload response carries the full ``DeploymentResponse``.
    """
    deployments = workspace.deployments

    # Build the tarball locally (gives us the ``content_hash``) so we can
    # short-circuit when the latest deployment already matches.
    content_stream = BytesIO()
    package_builder = PackageBuilder(context=active())
    package_hash = package_builder.write_package_to_stream(
        file_selector=WorkspaceFileSelector(active()), output_stream=content_stream
    )
    # A workspace with nothing deployed yet has no latest, which is not an error.
    with handle_client_exceptions():
        try:
            if deployments.latest().content_hash == package_hash:
                content_stream.close()
                return SyncResult(status="no_changes")
        except SdkNotFound:
            pass

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

    # The SDK owns both phases: the create call mints an id, a URL and a token
    # scoped to this one upload, so nothing else can supply them.
    with handle_client_exceptions():
        stored = deployments.upload(
            code=content_stream.getvalue(), requirements=requirements_bytes
        )
    return SyncResult(
        status="created",
        data=_extract_keys(stored.to_dict(), DEPLOYMENT_HEADERS),
    )


def _do_sync_configuration(
    *,
    workspace: Workspace[Sync],
    dry_run: bool = False,
) -> SyncResult:
    """Three-step sync (configuration variant). See ``_do_sync_deployment``."""
    configurations = workspace.configurations
    content_stream = BytesIO()
    package_builder = PackageBuilder(context=active())
    package_hash = package_builder.write_package_to_stream(
        file_selector=ConfigurationFileSelector(active()), output_stream=content_stream
    )

    # A workspace with nothing configured yet has no latest, which is not an error.
    with handle_client_exceptions():
        try:
            if configurations.latest().content_hash == package_hash:
                content_stream.close()
                return SyncResult(status="no_changes")
        except SdkNotFound:
            pass

    if dry_run:
        content_stream.close()
        return SyncResult(status="would_create", data={"package_hash": package_hash})

    with handle_client_exceptions():
        stored = configurations.upload(data=content_stream.getvalue())
    return SyncResult(
        status="created",
        data=_extract_keys(stored.to_dict(), CONFIGURATION_HEADERS),
    )


def _fetch_runtime_info(
    *, session: CliSession, workspace: Workspace[Sync]
) -> RuntimeInfo:
    """Fetch workspace overview data — returns RuntimeInfo model.

    Email is shown for humans only; a workspace key's service-account email stays hidden.
    """
    caller_info = session.fetch_caller_info()
    workspaces = caller_info["workspaces"]
    identity = caller_info.get("identity")
    email = (
        identity["email"]
        if identity and session.principal_kind() is PrincipalKind.HUMAN
        else None
    )
    ws_id = workspace.id

    info = RuntimeInfo(
        workspace_id=ws_id,
        workspace_name=_get_workspace_name(workspaces, ws_id),
        organization_name=_get_workspace_org_name(workspaces, ws_id),
        workspace_url=urls.workspace_url(ws_id),
        local_dir=str(active().run_dir),
        job_count=0,
    )
    if email:
        info["email"] = email

    # jobs
    with handle_client_exceptions():
        job_count = workspace.jobs.count()
    if job_count:
        info["job_count"] = job_count

    # latest run
    try:
        latest_run = _get_latest_run(workspace)
    except NoRunsFound:
        latest_run = None
    if latest_run is not None:
        # No manifest in this code path — `section.name` is the safe shortest form.
        info["latest_run_name"] = format_job_selector(latest_run.job_ref)
        info["latest_run_status"] = str(latest_run.status)
        if latest_run.started_at is not None:
            info["latest_run_started"] = latest_run.started_at
        if latest_run.ended_at is not None:
            info["latest_run_ended"] = latest_run.ended_at

    # deployment and configuration — a workspace may have neither yet
    with handle_client_exceptions():
        try:
            latest_deployment = workspace.deployments.latest()
        except SdkNotFound:
            latest_deployment = None
        try:
            latest_configuration = workspace.configurations.latest()
        except SdkNotFound:
            latest_configuration = None
    if latest_deployment is not None:
        info["deployment_version"] = latest_deployment.version
        info["deployment_date"] = latest_deployment.created_at
    if latest_configuration is not None:
        info["configuration_version"] = latest_configuration.version
        info["configuration_date"] = latest_configuration.created_at

    # Predefined profiles from the current workspace (server-side)
    for ws in workspaces:
        if ws["id"] == ws_id and ws.get("predefined_profiles"):
            info["predefined_profiles"] = dict(ws["predefined_profiles"])
            break

    return info


LogStreamEvent = tuple[Literal["log", "warning", "error"], str]

# Window after completion in which persisted logs may still be flushing to blob storage.
RECENTLY_FINISHED_LOG_WINDOW = timedelta(minutes=3)


def _is_recently_finished_terminal(time_ended: datetime | None) -> bool:
    """Return True when a terminal run ended within RECENTLY_FINISHED_LOG_WINDOW."""
    if time_ended is None:
        return False
    ended = (
        time_ended.replace(tzinfo=timezone.utc)
        if time_ended.tzinfo is None
        else time_ended.astimezone(timezone.utc)
    )
    return datetime.now(timezone.utc) - ended < RECENTLY_FINISHED_LOG_WINDOW


def _fetch_workspace_variables(
    workspace: Workspace[Sync],
    *,
    profile: Optional[str] = None,
    workspace_only: bool = False,
) -> tuple[VariableScope, ...]:
    """Every scope unless a selector narrows it to one."""
    # The SDK takes one selector: KEEP for every scope, None for the
    # workspace-level one, a name for that profile.
    wanted: Union[str, None, Keep] = KEEP
    if workspace_only:
        wanted = WORKSPACE_PROFILE
    elif profile is not None:
        wanted = profile
    with handle_client_exceptions("Failed to list variables"):
        return workspace.variables.list(profile=wanted)


def _change_workspace_variables(
    workspace: Workspace[Sync],
    *,
    profile: Optional[str],
    plain: Optional[dict[str, str]] = None,
    secrets: Optional[dict[str, str]] = None,
    deletes: Optional[list[str]] = None,
) -> tuple[VariableChange, ...]:
    """One atomic batch against a single scope; ``profile=None`` is workspace-wide."""
    with handle_client_exceptions("Failed to change variables"):
        return workspace.variables.apply(
            profile=profile,
            upserts=plain,
            secrets=secrets,
            deletes=deletes,
        )


def _should_hide_log_line(log: LogLine) -> bool:
    """Drop runner-internal diagnostics and provider lifecycle noise from user output."""
    return log.phase in ("runner", "provider")


def _fetch_workspaces(
    session: CliSession,
) -> tuple[list[Any], Optional[str]]:
    """Return (workspaces, current_workspace_id) for display."""
    try:
        current_ws_id: Optional[str] = session.workspace_id
    except (RuntimeOperationNotAuthorized, WorkspaceRunContextNotAvailable):
        current_ws_id = None
    return session.fetch_caller_info()["workspaces"], current_ws_id


def _fetch_job_run_info(
    workspace: Workspace[Sync],
    *,
    script_path_or_job_name: str,
    run_number: Optional[int] = None,
) -> JobRun[Sync]:
    """Resolve and fetch a single run."""
    run_id = _run_id_from_ref(script_path_or_job_name, run_number)
    if run_id is not None:
        return _fetch_run_detail(run_id, workspace=workspace)
    if run_number is None:
        # `latest` already returns the full run, so there is nothing to re-read.
        return _get_latest_run(workspace, script_path_or_job_name)
    run_id = _resolve_run_id_by_number(
        workspace=workspace,
        script_path_or_job_name=script_path_or_job_name,
        run_number=run_number,
    )
    return _fetch_run_detail(run_id, workspace=workspace)


def _fetch_runs(
    workspace: Workspace[Sync],
    script_path_or_job_name: Optional[str] = None,
    *,
    running_only: bool = False,
) -> list[JobRun[Sync]]:
    """Fetch runs, optionally filtered by script. Returns runs sorted desc by number."""
    # `running_only` filters out terminal-state runs client-side; the server
    # endpoint has no equivalent flag yet (issue: TODO follow-up).
    with handle_client_exceptions():
        runs = (
            workspace.jobs.get(ref=script_path_or_job_name).runs
            if script_path_or_job_name
            else workspace.job_runs
        )
        items = list(runs.list(limit=100))
    if running_only:
        items = [r for r in items if not r.finished]
    # Server orders by date_added DESC; trust that — no client-side resort.
    return items


def _fetch_deployments(
    workspace: Workspace[Sync],
) -> list[Deployment[Sync]]:
    """Fetch the newest 100 deployments."""
    with handle_client_exceptions():
        return list(workspace.deployments.list(limit=100))


def _fetch_deployment_info(
    workspace: Workspace[Sync],
    deployment_version_no: Optional[int] = None,
) -> Deployment[Sync]:
    """Fetch a single deployment (latest or by version). Returns deployment model."""
    with handle_client_exceptions():
        held = workspace.deployments
        if deployment_version_no is None:
            return held.latest()
        return held.get(version=deployment_version_no)


def _fetch_configurations(
    workspace: Workspace[Sync],
) -> list[Configuration[Sync]]:
    """Fetch the newest 100 configurations."""
    with handle_client_exceptions():
        return list(workspace.configurations.list(limit=100))


def _fetch_configuration_info(
    workspace: Workspace[Sync],
    configuration_version_no: Optional[int] = None,
) -> Configuration[Sync]:
    """Fetch a single configuration (latest or by version). Returns configuration model."""
    with handle_client_exceptions():
        held = workspace.configurations
        if configuration_version_no is None:
            return held.latest()
        return held.get(version=configuration_version_no)


def _fetch_jobs(
    workspace: Workspace[Sync],
    *,
    include_archived: bool = False,
) -> list[Job[Sync]]:
    """Fetch all jobs (scripts). Returns list of job models."""
    # Including archived jobs means dropping the filter, not naming both values.
    with handle_client_exceptions():
        jobs = workspace.jobs
        return list(jobs.list(archived=KEEP if include_archived else False))


def _filter_scripts_by_selectors(
    scripts: list[Job[Sync]],
    selectors: list[str],
) -> list[Job[Sync]]:
    """Filter jobs by trigger selectors (client-side).

    Empty selectors → empty match (nothing was asked for).
    """
    if not selectors:
        return []

    return [
        job
        for job in scripts
        if match_triggers_with_selectors(
            str(job.job_type), [TTrigger(t) for t in job.triggers], selectors
        )
    ]


def _resolve_selectors_to_scripts(
    args: list[str],
    *,
    workspace: Workspace[Sync],
    include_archived: bool = False,
) -> list[Job[Sync]]:
    """Resolve CLI selector/job-ref args to matched jobs.

    Splits *args* into selectors and bare job refs, fetches all jobs,
    applies selector matching and ref resolution, returns the union.
    Returns all jobs when *args* is empty.
    """
    scripts = _fetch_jobs(workspace, include_archived=include_archived)
    if not args:
        return scripts

    selectors: list[str] = []
    ref_set: set[str] = set()
    job_refs = [TJobRef(sc.job_ref) for sc in scripts]

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
    result: list[Job[Sync]] = []
    for sc in [*selector_matched, *ref_matched]:
        if sc.job_ref not in seen:
            seen.add(sc.job_ref)
            result.append(sc)
    return result


def _fetch_job_info(
    workspace: Workspace[Sync],
    script_path_or_job_name: str,
) -> Job[Sync]:
    """Fetch a single job (script). Returns job model."""
    with handle_client_exceptions():
        return workspace.jobs.get(ref=script_path_or_job_name)


def _do_deploy_manifest(
    *,
    manifest_hash: str,
    api_jobs: Sequence[Mapping[str, Any]],
    deployment_module: str | None,
    description: str | None,
    dry_run: bool,
    workspace: Workspace[Sync],
) -> DeployReport[Sync]:
    """Reconcile the workspace's jobs against the manifest."""
    with handle_client_exceptions("Failed to deploy manifest"):
        return workspace.jobs.deploy_manifest(
            {"engine_version": MANIFEST_ENGINE_VERSION, "jobs": api_jobs},
            manifest_hash=manifest_hash,
            module=deployment_module,
            description=description,
            dry_run=dry_run,
        )
