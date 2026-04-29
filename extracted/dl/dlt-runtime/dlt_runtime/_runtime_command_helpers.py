"""Helper functions for runtime CLI commands.

Pure helpers (no service deps) and service-dependent loaders (no display).
"""

# Python internals
import json
import os
import tarfile
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generator, Literal, Optional, Union, cast
from uuid import UUID

# Other libraries
import httpx
import yaml
from dlt._workspace._workspace_context import active
from dlt._workspace.cli import echo as fmt
from dlt._workspace.exceptions import WorkspaceRunContextNotAvailable
from dlt._workspace.deployment import (
    DEFAULT_DEPLOYMENT_MODULE,
    MANIFEST_ENGINE_VERSION,
    default_dashboard_manifest,
    generate_manifest_hash,
    manifest_from_module,
    match_triggers_with_selectors,
    pick_trigger,
    resolve_job_ref,
)
from dlt._workspace.deployment.trigger import manual
from dlt._workspace.deployment._trigger_helpers import is_selector
from dlt._workspace.deployment.exceptions import (
    AmbiguousJobRef,
    InvalidJobRef,
    JobRefNotFound,
)
from dlt._workspace.deployment.manifest import compute_default_trigger, expand_triggers
from dlt._workspace.deployment.typing import (
    TFilesManifest,
    TJobDefinition,
    TJobRef,
    TJobsDeploymentManifest,
    TTrigger,
)
from dlt._workspace.deployment.file_selector import (
    ConfigurationFileSelector,
    WorkspaceFileSelector,
)
from dlt._workspace.deployment.package_builder import (
    DEFAULT_MANIFEST_FILE_NAME,
    PackageBuilder,
)
from dlt._workspace.deployment.requirements import (
    WorkspaceRequirementsError,
    export_workspace_requirements,
    save_requirements,
)
from urllib.parse import urlparse

from dlt_runtime.exceptions import (
    AmbiguousJobSelector,
    AmbiguousWorkspaceName,
    NoRunsFound,
    RuntimeClientException,
    RuntimeOperationNotAuthorized,
    WorkspaceNotFound,
    exception_from_response,
    handle_client_exceptions,
)
from dlt_runtime.runtime import (
    RuntimeAuthService,
    UserInfo,
    WorkspaceInfo,
)
from dlt_runtime.runtime_clients.api.api.configurations import (
    create_configuration,
    get_configuration,
    get_configuration_files_manifest,
    get_latest_configuration,
    get_latest_configuration_files_manifest,
    list_configurations,
)
from dlt_runtime.runtime_clients.api.api.deployments import (
    create_deployment,
    get_deployment,
    get_deployment_files_manifest,
    get_latest_deployment,
    get_latest_deployment_files_manifest,
    list_deployments,
)
from dlt_runtime.runtime_clients.api.api.runs import (
    get_run,
    list_runs,
)
from dlt_runtime.runtime_clients.api.api.scripts import (
    get_script,
    list_scripts,
)
from dlt_runtime.runtime_clients.api.client import Client as ApiClient
from dlt_runtime.runtime_clients.api.types import Unset
from dlt_runtime.runtime_clients.api.models.create_deployment_body import (
    CreateDeploymentBody,
)
from dlt_runtime.runtime_clients.api.models.detailed_run_response import (
    DetailedRunResponse,
)
from dlt_runtime.runtime_clients.api.models.list_scripts_archived import (
    ListScriptsArchived,
)
from dlt_runtime.runtime_clients.api.models.log_line import LogLine
from dlt_runtime.runtime_clients.api.models.t_files_manifest import (
    TFilesManifest as ApiTFilesManifest,
)
from dlt_runtime.runtime_clients.api.types import File
from dlt_runtime.typing import ConnectInfo, FileDelta, RuntimeInfo, SyncResult
from dlt_runtime.version import __version__

if TYPE_CHECKING:
    from dlt_runtime.runtime_clients.api.models.deploy_manifest_response import (
        DeployManifestResponse,
    )
    from dlt_runtime.runtime_clients.api.models.t_job_definition import (
        TJobDefinition as ApiTJobDefinition,
    )

# Re-export view constants needed by loaders
from dlt_runtime._runtime_command_views import (  # noqa: F401
    DEPLOYMENT_HEADERS,
    CONFIGURATION_HEADERS,
    _extract_keys,
    _format_log_line,
    _preprocess_run_output,
    format_job_label,
)


# ---------------------------------------------------------------------------
# Pure helpers (no service dependencies)
# ---------------------------------------------------------------------------


def _to_uuid(value: Union[str, UUID]) -> UUID:
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except ValueError as e:
        raise ValueError(f"Invalid UUID: {value}") from e


def _get_web_ui_url() -> str:
    api_base_url = active().runtime_config.api_base_url or ""
    parsed = urlparse(api_base_url)
    hostname = parsed.hostname or ""
    return f"{parsed.scheme}://{hostname.replace('api.', '')}"


def _resolve_workspace(user_info: UserInfo, workspace: str) -> str:
    """Resolve a workspace name or ID to an owned workspace ID."""
    # Raises WorkspaceNotFound on miss; AmbiguousWorkspaceName on duplicate names.
    workspace = workspace.strip()

    # Exact ID match is always unambiguous — return immediately.
    for ws in user_info.workspaces:
        if ws.role == "owner" and workspace == ws.id:
            return ws.id

    matches = [
        ws for ws in user_info.workspaces if ws.role == "owner" and ws.name == workspace
    ]

    if len(matches) == 1:
        return matches[0].id

    if len(matches) > 1:
        raise AmbiguousWorkspaceName(workspace, matches)

    is_uuid = True
    try:
        UUID(workspace)
    except ValueError:
        is_uuid = False
    raise WorkspaceNotFound(workspace, is_uuid=is_uuid)


def _resolve_or_create_workspace(
    user_info: UserInfo,
    workspace: str,
    *,
    auth_service: "RuntimeAuthService",
) -> tuple[str, bool]:
    """Resolve a workspace name/ID; create by name if not found."""
    # Return (workspace_id, was_created)
    # UUID inputs that don't match never auto-create.
    try:
        return _resolve_workspace(user_info, workspace), False
    except WorkspaceNotFound as e:
        if e.is_uuid:
            raise LookupError(
                f"Workspace '{workspace}' not found among your owned workspaces."
            ) from e
        new_id = auth_service.create_new_workspace(
            user_info, workspace, description=None
        )
        # Keep user_info in sync with the just-created workspace so downstream
        # _get_workspace_name() resolves the name without an extra round-trip.
        user_info.workspaces.append(
            WorkspaceInfo(id=new_id, name=workspace, description="", role="owner")
        )
        return new_id, True


def _get_workspace_name(user_info: UserInfo, workspace_id: str) -> Optional[str]:
    """Look up the workspace name for the currently connected workspace."""
    for ws in user_info.workspaces:
        if ws.id == workspace_id:
            return ws.name
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


def _warn_missing_profiles() -> None:
    """Warn if recommended profiles (prod, access) are not available locally.

    Advisory only — never modifies require.profile values in job definitions.
    """
    try:
        available = set(active().available_profiles())
        if "prod" not in available:
            fmt.warning(
                "No 'prod' profile detected. Batch jobs will use default config/secrets only."
            )
        if "access" not in available:
            fmt.warning(
                "No 'access' profile detected. Interactive jobs may have limited sharing."
            )
    except Exception:
        pass


def _generate_local_manifest(
    name_or_path: str, use_all: bool = True
) -> tuple[TJobsDeploymentManifest, str, list["ApiTJobDefinition"], list[str]]:
    """Generate a deployment manifest locally from a module or file.

    Returns (manifest, hash, api_jobs, warnings).
    Raises ImportError / FileNotFoundError with helpful message if module not found
    or fails to import.
    """
    from dlt_runtime.runtime_clients.api.models.t_job_definition import (
        TJobDefinition as ApiTJobDefinition,
    )

    try:
        manifest, warnings = manifest_from_module(name_or_path, use_all=use_all)
    except (ModuleNotFoundError, ImportError) as e:
        # Distinguish "the deployment file itself is missing" from
        # "the file exists but failed to import (downstream import error)".
        # The catch is broad because import_module() raises both for the
        # target module not existing AND for any import inside it failing.
        if (
            name_or_path.endswith(".py")
            or "/" in name_or_path
            or os.sep in name_or_path
        ):
            file_path = Path(name_or_path).resolve()
        else:
            file_path = Path.cwd() / f"{name_or_path}.py"

        if file_path.exists():
            # File is there — surface the real import error so the user can
            # fix it instead of being told the file is missing.
            raise ImportError(
                f"Failed to import '{file_path.name}': {type(e).__name__}: {e}"
            ) from e

        if name_or_path == DEFAULT_DEPLOYMENT_MODULE:
            raise FileNotFoundError(
                f"No '{DEFAULT_DEPLOYMENT_MODULE}.py' file found in the workspace. "
                "Create one and import your job declarations and notebook modules into it. "
                "See https://dlthub.com/docs/runtime/deployment for details."
            ) from e
        raise ImportError(
            f"Could not import module '{name_or_path}'. "
            "Check that the file exists and is a valid Python module."
        ) from e

    manifest_hash = generate_manifest_hash(manifest)
    api_jobs = [ApiTJobDefinition.from_dict(job) for job in manifest["jobs"]]
    return manifest, manifest_hash, api_jobs, warnings


def _default_dashboard_manifest_bundle() -> tuple[
    TJobsDeploymentManifest, str, list["ApiTJobDefinition"], list[str]
]:
    """Build the ad-hoc dashboard-only manifest bundle.

    Used when no `__deployment__.py` exists but the user still wants a dashboard.
    Returns (manifest, hash, api_jobs, warnings) matching `_generate_local_manifest`.
    """
    from dlt_runtime.runtime_clients.api.models.t_job_definition import (
        TJobDefinition as ApiTJobDefinition,
    )

    manifest = default_dashboard_manifest()
    manifest_hash = generate_manifest_hash(manifest)
    api_jobs = [ApiTJobDefinition.from_dict(job) for job in manifest["jobs"]]
    return manifest, manifest_hash, api_jobs, []


def _select_single_job(
    manifest: TJobsDeploymentManifest,
    selectors: list[str],
    *,
    forbidden_job_type: str | None = None,
) -> tuple[TJobDefinition, str]:
    """Select a single job from manifest using selectors.

    Expands triggers locally, matches selectors, picks a trigger for each job.
    Returns (job_def, trigger_str) for the single matched job.

    Raises LookupError if zero match, AmbiguousJobSelector if multiple match,
    RuntimeClientException for forbidden-type / no-manual-jobs cases.
    """
    matched: list[tuple[TJobDefinition, str]] = []

    for job_def in manifest["jobs"]:
        job_type = job_def["entry_point"]["job_type"]
        expanded = expand_triggers(job_def)
        hits = match_triggers_with_selectors(job_type, expanded, selectors)
        trigger = pick_trigger(hits, job_def.get("default_trigger"))
        if trigger is not None:
            # manual: confirmed the job allows manual launch, but the actual
            # trigger string should be the job's natural default when available.
            if str(trigger).startswith("manual:"):
                default = compute_default_trigger(job_def)
                if default is not None:
                    trigger = default
            matched.append((job_def, str(trigger)))

    # Filter out forbidden job types
    if forbidden_job_type:
        forbidden = [
            (jd, t)
            for jd, t in matched
            if jd["entry_point"]["job_type"] == forbidden_job_type
        ]
        allowed = [
            (jd, t)
            for jd, t in matched
            if jd["entry_point"]["job_type"] != forbidden_job_type
        ]
        if forbidden and not allowed:
            job_type_label = (
                "interactive" if forbidden_job_type == "interactive" else "batch"
            )
            refs = ", ".join(jd["job_ref"] for jd, _ in forbidden)
            raise RuntimeClientException(
                f"Matched jobs are {job_type_label} (not allowed here): {refs}"
            )
        matched = allowed

    if not matched:
        selector_str = ", ".join(selectors)
        # A manual: selector that didn't match means no job has expose.manual=True.
        # Distinguish the explicit-ref form from the glob form for a useful message.
        specific_manual_refs = [
            s[len("manual:") :]
            for s in selectors
            if s.startswith("manual:") and s not in ("manual:", "manual:*")
        ]
        glob_manual = any(s in ("manual:", "manual:*") for s in selectors)
        if specific_manual_refs:
            raise RuntimeClientException(
                f"Job '{specific_manual_refs[0]}' does not allow manual runs. "
                "Set expose(manual=True) in the job definition or use a different trigger."
            )
        if glob_manual:
            raise RuntimeClientException(
                "No jobs in this manifest allow manual runs. "
                "Set expose(manual=True) on at least one job, or use "
                "'dlt runtime trigger <selector>' to fire jobs by their own triggers."
            )
        raise LookupError(
            f"No jobs matched selector(s): {selector_str}. "
            "Check available jobs with 'dlt runtime info' or 'dlt runtime job list'."
        )

    if len(matched) == 1:
        return matched[0]

    raise AmbiguousJobSelector(matched)


def _resolve_job_ref_in_manifest(
    name_or_ref: str, manifest: TJobsDeploymentManifest
) -> Optional[str]:
    """Resolve a name/partial ref to canonical job_ref via manifest jobs."""
    try:
        return str(
            resolve_job_ref(name_or_ref, [j["job_ref"] for j in manifest["jobs"]])
        )
    except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
        return None


def _resolve_selector(
    selector_or_job_ref: str | None,
    manifest: TJobsDeploymentManifest,
    *,
    default_selector: str = "manual:",
) -> list[str]:
    """Resolve a user-provided selector/job_ref into a list of selectors.

    If it looks like a job_ref, resolves it and creates a manual: selector.
    Otherwise uses it as-is. Returns [default_selector] if None.

    The default selector is ``"manual:"`` (which `_normalize_selector` expands
    to the glob ``manual:*``) — meaning "any job that allows manual launch".
    This matches the contract of `launch`/`serve`/`run-pipeline`: pick a single
    job that the user can manually start, and ignore jobs whose triggers are
    only schedules / events / `expose.manual=False`.
    """
    if selector_or_job_ref is None:
        return [default_selector]

    resolved = _resolve_job_ref_in_manifest(selector_or_job_ref, manifest)
    if resolved is not None:
        return [manual(resolved)]

    # Use as-is (selector pattern)
    return [selector_or_job_ref]


def _resolve_job_ref_locally(name_or_ref: str) -> Optional[str]:
    """Resolve a short name against the local deployment manifest, or None."""
    # Broad catch: a missing/broken local manifest must not break commands
    # like `logs` — they should fall back to server-side resolution.
    try:
        manifest, _, _, _ = _generate_local_manifest(DEFAULT_DEPLOYMENT_MODULE)
    except Exception:
        return None
    return _resolve_job_ref_in_manifest(name_or_ref, manifest)


# ---------------------------------------------------------------------------
# Service-dependent loaders (no display)
# ---------------------------------------------------------------------------


def _resolve_job_ref_from_server(
    name_or_ref: str,
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
    include_archived: bool = True,
) -> str:
    """Resolve a name or partial ref to a canonical job_ref.

    Tries the local manifest first (same path as `launch`), then qualified-ref
    local resolution, then the server job list for bare names. Returns the
    input unchanged if every path fails.
    """
    try:
        UUID(name_or_ref)
        return name_or_ref
    except ValueError:
        pass

    local_ref = _resolve_job_ref_locally(name_or_ref)
    if local_ref is not None:
        return local_ref

    if "." in name_or_ref:
        # Qualified ref — resolve locally
        try:
            return str(resolve_job_ref(name_or_ref))
        except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
            return name_or_ref

    # Bare name — fetch job list from server.
    # Outer broad catch is intentional: this helper is a best-effort resolver
    # used by CLI args; on any server/network failure we return the raw name
    # so the downstream API call surfaces the real error.
    try:
        archived = (
            ListScriptsArchived.ALL if include_archived else ListScriptsArchived.FALSE
        )
        with handle_client_exceptions():
            res = list_scripts.sync_detailed(
                client=api_client,
                workspace_id=_to_uuid(auth_service.workspace_id),
                archived=archived,
            )
        if (
            isinstance(res.parsed, list_scripts.ListScriptsResponse200)
            and res.parsed.items
        ):
            job_refs = [TJobRef(s.job_ref) for s in res.parsed.items]
            try:
                return str(resolve_job_ref(name_or_ref, job_refs))
            except (InvalidJobRef, JobRefNotFound, AmbiguousJobRef):
                pass
    except Exception:
        pass

    return name_or_ref


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


def _require_auth() -> tuple[RuntimeAuthService, UserInfo]:
    """Authenticate and return (auth_service, user_info)."""
    # Propagates RuntimeNotAuthenticated; the boundary handler in
    # commands.py:execute() routes that to Phase 1 device-flow recovery.
    auth_service = RuntimeAuthService(run_context=active())
    auth_service.authenticate()
    return auth_service, auth_service.fetch_user_info()


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
    raise LookupError(
        f"Run number {run_number} not found for script/job {script_path_or_job_name}"
    )


def _resolve_connection(
    auth_service: RuntimeAuthService,
    user_info: UserInfo,
    workspace_id: Optional[str] = None,
) -> ConnectInfo:
    """Resolve workspace connection — no display.

    Returns ConnectInfo describing the resolved state. If interactive selection
    is needed, ConnectInfo.needs_selection is set and workspace_id is not yet final.
    """
    local_dir = str(active().run_dir)

    if workspace_id is not None:
        ws_name = _get_workspace_name(user_info, workspace_id)
        return ConnectInfo(
            workspace_id=workspace_id, workspace_name=ws_name, local_dir=local_dir
        )

    remote_ids = [ws.id for ws in user_info.workspaces]
    local_ws_id = auth_service.workspace_run_context.runtime_config.workspace_id

    if not local_ws_id:
        return ConnectInfo(
            workspace_id="",
            workspace_name=None,
            local_dir=local_dir,
            needs_selection="no_local",
        )

    if remote_ids and local_ws_id not in remote_ids:
        return ConnectInfo(
            workspace_id=local_ws_id,
            workspace_name=None,
            local_dir=local_dir,
            needs_selection="mismatch",
        )

    ws_name = _get_workspace_name(user_info, local_ws_id)
    return ConnectInfo(
        workspace_id=local_ws_id, workspace_name=ws_name, local_dir=local_dir
    )


def _local_files_manifest_from_tarball(stream: BytesIO) -> TFilesManifest:
    """Extract manifest.yaml from a just-written tarball (rewinds first)."""
    # TODO: dlt's PackageBuilder.write_package_to_stream returns only the hash;
    # the per-file manifest is computed but only emitted as a tarball member.
    # Upstream a `build_manifest(file_selector)` (or a `(hash, manifest)`-returning
    # variant) so we don't have to re-open the tarball just to read it back.
    stream.seek(0)
    with tarfile.open(fileobj=stream, mode="r:*") as tar:
        f = tar.extractfile(tar.getmember(DEFAULT_MANIFEST_FILE_NAME))
        assert f is not None
        manifest = cast(TFilesManifest, yaml.safe_load(f))
    return manifest


def _diff_file_manifests(local: TFilesManifest, remote: TFilesManifest) -> FileDelta:
    """Per-file diff: paths added/deleted; entries differing on hash/linkname → updated."""
    # Both manifests carry per-file sha3_256 (regular files) or linkname
    # (symlinks) in the entry dict, so dict equality is sufficient — no
    # re-hashing needed on either side.
    local_map = {item["relative_path"]: item for item in local["files"]}
    remote_map = {item["relative_path"]: item for item in remote["files"]}

    added = sorted(set(local_map) - set(remote_map))
    deleted = sorted(set(remote_map) - set(local_map))
    common = set(local_map) & set(remote_map)
    updated = sorted(p for p in common if local_map[p] != remote_map[p])
    unchanged_count = len(common) - len(updated)
    return FileDelta(
        added=added, updated=updated, deleted=deleted, unchanged_count=unchanged_count
    )


def _fetch_remote_files_manifest(
    api_client: ApiClient,
    auth_service: RuntimeAuthService,
    kind: Literal["deployment", "configuration"],
    ref: str = "latest",
) -> TFilesManifest:
    """Call GET /workspaces/{ws}/{deployments|configurations}/{ref}/files."""
    workspace_id = _to_uuid(auth_service.workspace_id)
    is_latest = ref == "latest"
    # Coerce non-`latest` refs to UUID/int (the parameterized client signature).
    parsed_ref: UUID | int | None = None
    if not is_latest:
        try:
            parsed_ref = UUID(ref)
        except ValueError:
            parsed_ref = int(ref)
    with handle_client_exceptions():
        if kind == "deployment":
            if is_latest:
                result = get_latest_deployment_files_manifest.sync_detailed(
                    workspace_id=workspace_id, client=api_client
                )
            else:
                assert parsed_ref is not None
                result = get_deployment_files_manifest.sync_detailed(
                    workspace_id=workspace_id,
                    deployment_id_or_version=parsed_ref,
                    client=api_client,
                )
        else:
            if is_latest:
                result = get_latest_configuration_files_manifest.sync_detailed(
                    workspace_id=workspace_id, client=api_client
                )
            else:
                assert parsed_ref is not None
                result = get_configuration_files_manifest.sync_detailed(
                    workspace_id=workspace_id,
                    configuration_id_or_version=parsed_ref,
                    client=api_client,
                )

    # Only TFilesManifest carries the {"engine_version", "files"} shape we need;
    if not isinstance(result.parsed, ApiTFilesManifest):
        raise exception_from_response(f"Failed to get {kind} files manifest", result)
    return cast(TFilesManifest, result.parsed.to_dict())


def _do_sync_deployment(
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
    dry_run: bool = False,
    compute_diff: bool = False,
) -> SyncResult:
    package_builder = PackageBuilder(context=active())
    # `with BytesIO()` ensures the content stream is closed on every exit path
    # (early returns + raises) without scattered .close() calls.
    with BytesIO() as content_stream:
        package_hash = package_builder.write_package_to_stream(
            file_selector=WorkspaceFileSelector(active()),
            output_stream=content_stream,
        )
        with handle_client_exceptions():
            latest_deployment = get_latest_deployment.sync_detailed(
                workspace_id=_to_uuid(auth_service.workspace_id),
                client=api_client,
            )
        # remote_version: latest version on the server (None if the workspace
        # has never been deployed). Used for the dry-run "would create vN+1
        # (was vN)" message; not consumed on the real-upload path.
        remote_version: int | None = None
        if isinstance(
            latest_deployment.parsed, get_latest_deployment.DeploymentResponse
        ):
            if latest_deployment.parsed.content_hash == package_hash:
                return SyncResult(status="no_changes")
            remote_version = latest_deployment.parsed.version
        elif isinstance(
            latest_deployment.parsed, get_latest_deployment.ErrorResponse404
        ):
            pass  # will create below
        else:
            raise exception_from_response(
                "Failed to get latest deployment", latest_deployment
            )

        # Compute file delta when the caller will display it; for SILENT level
        # we skip the second roundtrip entirely.
        file_delta: FileDelta | None = None
        if compute_diff:
            local_manifest = _local_files_manifest_from_tarball(content_stream)
            if remote_version is not None:
                remote_manifest = _fetch_remote_files_manifest(
                    api_client, auth_service, "deployment"
                )
            else:
                remote_manifest = TFilesManifest(engine_version=1, files=[])
            file_delta = _diff_file_manifests(local_manifest, remote_manifest)

        if dry_run:
            # Skip requirements export + upload entirely; the local hash already
            # told us the upload would create a new version.
            data: dict[str, Any] = {"package_hash": package_hash}
            if remote_version is not None:
                data["current_version"] = remote_version
            if file_delta is not None:
                data["file_delta"] = file_delta
            return SyncResult(status="would_create", data=data)

        # export the workspace requirements manifest alongside the code tarball
        try:
            manifest = export_workspace_requirements(Path(active().run_dir))
        except WorkspaceRequirementsError as ex:
            raise RuntimeClientException(
                f"Failed to export workspace requirements: {ex}"
            ) from ex
        requirements_stream = BytesIO()
        save_requirements(manifest, requirements_stream)
        requirements_stream.seek(0)

        with handle_client_exceptions():
            create_deployment_result = create_deployment.sync_detailed(
                workspace_id=_to_uuid(auth_service.workspace_id),
                client=api_client,
                body=CreateDeploymentBody(
                    files=File(
                        payload=content_stream,
                        file_name="workspace.tar.gz",
                        mime_type="application/x-tar",
                    ),
                    requirements=File(
                        payload=requirements_stream,
                        file_name="requirements.json",
                        mime_type="application/json",
                    ),
                ),
            )
        if isinstance(
            create_deployment_result.parsed, create_deployment.DeploymentResponse
        ):
            data = _extract_keys(
                create_deployment_result.parsed.to_dict(), DEPLOYMENT_HEADERS
            )
            if file_delta is not None:
                data["file_delta"] = file_delta
            return SyncResult(status="created", data=data)
        raise exception_from_response(
            "Failed to create deployment", create_deployment_result
        )


def _do_sync_configuration(
    *,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
    dry_run: bool = False,
    compute_diff: bool = False,
) -> SyncResult:
    package_builder = PackageBuilder(context=active())
    with BytesIO() as content_stream:
        package_hash = package_builder.write_package_to_stream(
            file_selector=ConfigurationFileSelector(active()),
            output_stream=content_stream,
        )
        with handle_client_exceptions():
            latest_configuration = get_latest_configuration.sync_detailed(
                workspace_id=_to_uuid(auth_service.workspace_id),
                client=api_client,
            )
        remote_version: int | None = None
        if isinstance(
            latest_configuration.parsed,
            get_latest_configuration.ConfigurationResponse,
        ):
            if latest_configuration.parsed.content_hash == package_hash:
                return SyncResult(status="no_changes")
            remote_version = latest_configuration.parsed.version
        elif isinstance(
            latest_configuration.parsed,
            get_latest_configuration.ErrorResponse404,
        ):
            pass  # will create below
        else:
            raise exception_from_response(
                "Failed to get latest configuration", latest_configuration
            )

        file_delta: FileDelta | None = None
        if compute_diff:
            local_manifest = _local_files_manifest_from_tarball(content_stream)
            if remote_version is not None:
                remote_manifest = _fetch_remote_files_manifest(
                    api_client, auth_service, "configuration"
                )
            else:
                remote_manifest = TFilesManifest(engine_version=1, files=[])
            file_delta = _diff_file_manifests(local_manifest, remote_manifest)

        if dry_run:
            data: dict[str, Any] = {"package_hash": package_hash}
            if remote_version is not None:
                data["current_version"] = remote_version
            if file_delta is not None:
                data["file_delta"] = file_delta
            return SyncResult(status="would_create", data=data)

        with handle_client_exceptions():
            create_configuration_result = create_configuration.sync_detailed(
                workspace_id=_to_uuid(auth_service.workspace_id),
                client=api_client,
                body=create_configuration.CreateConfigurationBody(
                    file=File(
                        payload=content_stream,
                        file_name="configurations.tar.gz",
                        mime_type="application/x-tar",
                    )
                ),
            )
        if isinstance(
            create_configuration_result.parsed,
            create_configuration.ConfigurationResponse,
        ):
            data = _extract_keys(
                create_configuration_result.parsed.to_dict(),
                CONFIGURATION_HEADERS,
            )
            if file_delta is not None:
                data["file_delta"] = file_delta
            return SyncResult(status="created", data=data)
        raise exception_from_response(
            "Failed to create configuration", create_configuration_result
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
        workspace_url=f"{_get_web_ui_url()}/w/{ws_id}",
        local_dir=str(active().run_dir),
        job_count=0,
    )
    if user_info is not None:
        info["email"] = user_info.email

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
        jd = latest_run.script.job_definition.to_dict()
        info["latest_run_name"] = format_job_label(
            jd["job_ref"], jd.get("expose"), jd.get("deliver")
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
        for ws in user_info.workspaces:
            if ws.id == ws_id and ws.predefined_profiles:
                info["predefined_profiles"] = dict(ws.predefined_profiles)
                break

    return info


LogStreamEvent = tuple[Literal["log", "warning", "error"], str]


def _iter_run_log_stream(
    run_id: UUID,
    *,
    follow: bool = True,
    auth_service: RuntimeAuthService,
    api_client: ApiClient,
) -> Generator[LogStreamEvent, None, None]:
    """
    Stream logs from the run stream endpoint using SSE.

    Yields (level, message) tuples for each event. Callers decide how to display.

    When *follow* is False the generator replays existing logs and stops.
    A 1-second read timeout detects the end of the replay.
    """
    workspace_id = _to_uuid(auth_service.workspace_id)

    # Get the base URL and auth headers from the API client
    base_url = api_client._base_url.rstrip("/")
    stream_url = f"{base_url}/v1/workspaces/{workspace_id}/runs/{run_id}/logs/stream"

    headers = {
        "Accept": "text/event-stream",
        "User-Agent": f"dlt-runtime-cli/{__version__}",
    }

    if auth_service.auth_info:
        headers["Authorization"] = f"Bearer {auth_service.auth_info.jwt_token}"

    # In non-follow mode a 1 s read timeout acts as end-of-replay detection.
    stream_timeout = None if follow else httpx.Timeout(None, read=1.0)

    try:
        with httpx.stream(
            "GET", stream_url, headers=headers, timeout=stream_timeout, verify=False
        ) as response:
            if response.status_code != 200:
                yield (
                    "error",
                    f"Failed to connect to log stream: {response.status_code}",
                )
                return

            try:
                buffer = ""
                for chunk in response.iter_text():
                    buffer += chunk
                    lines = buffer.split("\n")
                    buffer = lines.pop()  # Keep incomplete line in buffer

                    for line in lines:
                        if line.startswith("data: "):
                            data = line[6:]  # Remove "data: " prefix
                            try:
                                log_data = json.loads(data)
                                # Create LogLine from the streamed data
                                log = LogLine(
                                    phase=log_data["channel"],
                                    line_num=log_data["line_num"],
                                    reported_at=log_data["reported_at"],
                                    content=log_data["content"],
                                )
                                yield ("log", _format_log_line(log))
                            except (json.JSONDecodeError, KeyError) as e:
                                yield ("warning", f"Failed to parse log line: {e}")
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
    return user_info.workspaces, current_ws_id


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
) -> list[Any]:
    """Fetch runs, optionally filtered by script. Returns list of run models."""
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
    if isinstance(list_runs_result.parsed, list_runs.ListRunsResponse200):
        return (
            list(list_runs_result.parsed.items) if list_runs_result.parsed.items else []
        )
    raise exception_from_response("Failed to list workspace runs", list_runs_result)


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
) -> list[Any]:
    """Fetch all jobs (scripts). Returns list of script models."""
    with handle_client_exceptions():
        res = list_scripts.sync_detailed(
            client=api_client,
            workspace_id=_to_uuid(auth_service.workspace_id),
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
) -> list[Any]:
    """Resolve CLI selector/job-ref args to matched ScriptResponse objects.

    Splits *args* into selectors and bare job refs, fetches all jobs,
    applies selector matching and ref resolution, returns the union.
    Returns all scripts when *args* is empty.
    """
    scripts = _fetch_jobs(api_client, auth_service)
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
    from dlt_runtime.runtime_clients.api.api.workspaces import deploy as deploy_manifest
    from dlt_runtime.runtime_clients.api.models.deploy_manifest_request import (
        DeployManifestRequest,
    )

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
