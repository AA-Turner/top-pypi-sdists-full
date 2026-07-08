"""Shared utility functions for the cyclopts CLI."""

import json
import time
import typing as t
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import urlencode

if t.TYPE_CHECKING:
    from dreadnode.app.cli.args import PlatformArgs
    from dreadnode.app.main import Dreadnode

from dreadnode.core.log import console

# Label-column width for detail views (2-space indent + label text + padding).
# Shared so every domain renders key/value blocks with consistent alignment.
_LABEL_W = 14

T = t.TypeVar("T")

# ---------------------------------------------------------------------------
# CLI-VOCAB-001: synonym alias map
# ---------------------------------------------------------------------------
#
# A flag's canonical name matches the underlying API parameter name. When the
# same conceptual filter appears under different names across commands, each
# command accepts the synonyms as cyclopts aliases.
#
# Pass these tuples as ``name=`` on ``cyclopts.Parameter``. The first entry is
# canonical (matches the API parameter); the rest are aliases preserved for
# cross-command muscle memory.
_FLAG_STATE: tuple[str, ...] = ("--state", "--status")
_FLAG_STATUS: tuple[str, ...] = ("--status", "--state")
_FLAG_SEARCH: tuple[str, ...] = ("--search", "--query")
_FLAG_QUERY: tuple[str, ...] = ("--query", "--search")


# ---------------------------------------------------------------------------
# Standardized output helpers
# ---------------------------------------------------------------------------


def print_success(message: str, *, indent: int = 0) -> None:
    console.print(f"{' ' * indent}[green]✓[/] {message}")


def print_error(message: str, *, indent: int = 0) -> None:
    console.print(f"{' ' * indent}[red]✗[/] {message}")


def print_warning(message: str, *, indent: int = 0) -> None:
    console.print(f"{' ' * indent}[yellow]![/] {message}")


def print_info(message: str, *, indent: int = 0) -> None:
    console.print(f"{' ' * indent}[blue]i[/] {message}")


def print_markdown(content: str) -> None:
    """Render a markdown blob to the shared console.

    Used by ``dreadnode capability info --readme`` and
    ``dreadnode task info --readme`` to render bundle READMEs inline.
    """
    from rich.markdown import Markdown

    console.print(Markdown(content))


def print_skip(message: str, *, indent: int = 0) -> None:
    console.print(f"{' ' * indent}[dim]-[/] {message}")


def print_link(profile_url: str, path: str, **query: str) -> None:
    """Print a clickable platform web URL.

    Builds the URL from the server base URL (stripping any ``/api/v1`` suffix),
    the given path, and optional query parameters.
    """
    root = profile_url.rstrip("/")
    for suffix in ("/api/v1", "/api"):
        if root.endswith(suffix):
            root = root[: -len(suffix)]
            break
    qs = f"?{urlencode(query)}" if query else ""
    url = f"{root}/{path.lstrip('/')}{qs}"
    console.print()
    console.print(f"  [dim]→[/dim] View on web: [u][link={url}]{url}[/link][/u]")


# ---------------------------------------------------------------------------
# CLI-CONF-001/002/003: confirmation prompts for destructive actions
# ---------------------------------------------------------------------------


def confirm_destructive(prompt: str, *, yes: bool) -> bool:
    """Confirm an irreversible action, honoring ``--yes`` and TTY state.

    Returns ``True`` when the action should proceed, ``False`` when the user
    declines at the prompt. Raises ``RuntimeError`` when stdin is not a TTY
    and ``--yes`` was not supplied — the error names ``--yes`` so non-interactive
    callers know the recovery path.

    Pair with a ``--yes`` flag declared as::

        yes: t.Annotated[
            bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())
        ] = False
    """
    if yes:
        return True

    import sys

    from rich.prompt import Confirm

    if not sys.stdin.isatty():
        raise RuntimeError(
            "Confirmation required but stdin is not interactive. "
            "Re-run with --yes to skip the prompt."
        )
    return Confirm.ask(prompt, default=False)


# ---------------------------------------------------------------------------
# Dreadnode factory
# ---------------------------------------------------------------------------


def configured_dreadnode(args: "PlatformArgs") -> "Dreadnode":
    """Build a configured Dreadnode instance from CLI args."""
    from dreadnode.app.main import Dreadnode

    profile = args.resolve()
    return Dreadnode().configure(
        server=profile.url,
        api_key=profile.api_key,
        organization=profile.organization,
        workspace=profile.workspace,
        project=profile.project,
    )


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------


def _jsonable(value: t.Any) -> t.Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if hasattr(value, "__dict__"):
        return {
            key: _jsonable(item) for key, item in vars(value).items() if not key.startswith("_")
        }
    return value


def _print_json(value: t.Any) -> None:
    print(json.dumps(_jsonable(value), indent=2, sort_keys=True))


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ArtifactRef:
    """Resolved artifact reference with org always set and name always bare.

    Examples (with default_org='myorg'):
        my-cap            → org=myorg, name=my-cap, version=None
        my-cap@1.0.0      → org=myorg, name=my-cap, version=1.0.0
        acme/my-cap       → org=acme,  name=my-cap, version=None
        acme/my-cap@1.0.0 → org=acme,  name=my-cap, version=1.0.0
    """

    org: str
    name: str
    version: str | None = None

    @classmethod
    def parse(cls, value: str, default_org: str) -> "ArtifactRef":
        """Parse [org/]name[@version] with org fallback."""
        org, name, version = _parse_ref(value)
        return cls(org=org or default_org, name=name, version=version)

    @classmethod
    def parse_versioned(cls, value: str, default_org: str) -> "VersionedRef":
        """Parse a reference that requires a version (e.g. my-cap@1.0.0)."""
        org, name, version = _parse_ref(value)
        if not version:
            raise ValueError(f"version required (e.g. {name}@1.0.0)")
        return VersionedRef(org=org or default_org, name=name, version=version)

    @property
    def qualified_name(self) -> str:
        """Org-qualified name: 'org/name'."""
        return f"{self.org}/{self.name}"

    def with_version(self, version: str) -> "VersionedRef":
        """Return a VersionedRef with the given version."""
        return VersionedRef(org=self.org, name=self.name, version=version)

    def format(self) -> str:
        """Rich-formatted display string: org/name@version."""
        v = self.version or "latest"
        return f"[dim]{self.org}/[/dim][cyan]{self.name}[/cyan]@[dim]{v}[/dim]"


@dataclass(frozen=True, kw_only=True)
class VersionedRef(ArtifactRef):
    """ArtifactRef with version guaranteed non-None.

    Created only through ArtifactRef.parse_versioned(),
    ArtifactRef.with_version(), or ensure_version().
    """

    version: str


def parse_env_model_overrides(
    values: list[str] | None,
    *,
    resolve: t.Callable[[str], str] | None = None,
) -> dict[str, str] | None:
    """Parse repeatable ``--env-model ROLE=MODEL_ID`` flags into a role->id map.

    Targets the task ENVIRONMENT (defender) models — distinct from ``--model``
    (the solver/agent model) and ``--judge-model``. Later repeats override earlier
    ones for the same role (per-role merge). ``resolve`` (e.g. ``resolve_model``)
    normalizes each id. Returns ``None`` when no overrides are given.
    """
    if not values:
        return None
    out: dict[str, str] = {}
    for raw in values:
        if "=" not in raw:
            raise ValueError(f"--env-model expects ROLE=MODEL_ID, got: {raw!r}")
        role, _, model_id = raw.partition("=")
        role = role.strip()
        model_id = model_id.strip()
        if not role:
            raise ValueError(f"--env-model role must not be empty: {raw!r}")
        if not model_id:
            raise ValueError(f"--env-model model id must not be empty: {raw!r}")
        out[role] = resolve(model_id) if resolve else model_id
    return out or None


def merge_env_model_overrides(
    existing: t.Any, parsed: dict[str, str] | None
) -> dict[str, str] | None:
    """Per-role merge of CLI overrides onto any manifest ``model_overrides``.

    A ``--env-model`` flag overrides only its own role, leaving the rest of a
    ``model_overrides`` block loaded from ``--file`` intact (unlike whole-value
    flag replacement). Returns ``None`` when neither source has entries.
    """
    merged: dict[str, str] = {}
    if isinstance(existing, dict):
        merged.update({str(k): str(v) for k, v in existing.items()})
    if parsed:
        merged.update(parsed)
    return merged or None


def _parse_ref(value: str) -> tuple[str | None, str, str | None]:
    """Shared parsing logic for artifact references."""
    version: str | None = None
    if "@" in value:
        value, version = value.rsplit("@", 1)
        version = version.strip().strip("/") or None
        if version and version.lower() == "latest":
            version = None

    org: str | None = None
    if "/" in value:
        org, value = value.split("/", 1)
        org = org.strip().strip("/") or None

    name = value.strip().strip("/")
    if not name:
        raise ValueError("artifact name cannot be empty")

    return org, name, version


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------


def _status_color(status: str) -> str:
    """Return Rich markup color for a job/resource status."""
    status_lower = status.lower()
    if status_lower in {"running", "pending", "queued", "starting", "uploading"}:
        return "yellow"
    if status_lower in {"completed", "success", "succeeded", "ready", "active"}:
        return "green"
    if status_lower in {"failed", "cancelled", "error", "stopped"}:
        return "red"
    if status_lower in {"critical", "high"}:
        return "red"
    if status_lower in {"medium", "warning"}:
        return "yellow"
    if status_lower in {"low", "info"}:
        return "default"
    return "default"


def _status_dot(status: str, *, color: str | None = None) -> str:
    """Colored Unicode dot prefix for a status value.

    *color* may override the result of ``_status_color`` when callers carry a
    domain-specific color map (e.g. evaluation's expanded status set).
    """
    resolved = color or _status_color(status)
    return f"[{resolved}]●[/{resolved}]"


def _visibility_markup(visibility: str) -> str:
    """Return Rich-formatted visibility label."""
    if visibility == "public":
        return "[green]public[/green]"
    return "[bright_blue]private[/bright_blue]"


# ---------------------------------------------------------------------------
# Identifier + label helpers (shared by evaluation, airt, worlds, …)
# ---------------------------------------------------------------------------


def _short_id(full_id: str) -> str:
    """First 8 chars of an ID — used for compact display only.

    Commands that look up resources by ID accept the full identifier; the
    short form is for terminal-friendly rendering.
    """
    return str(full_id)[:8]


def _fmt_id(full_id: str) -> str:
    """Render an ID with the copyable short prefix prominent, full UUID dim."""
    short = _short_id(full_id)
    rest = str(full_id)[8:]
    return f"{short}[dim]{rest}[/dim]"


def _label(text: str) -> str:
    """Left-aligned label padded to ``_LABEL_W`` visible characters.

    Always emits at least one space after the label text so a long label
    can't collide with the value that follows.
    """
    pad = max(1, _LABEL_W - 2 - len(text))
    return f"  [dim]{text}[/dim]{' ' * pad}"


def _continuation() -> str:
    """Blank prefix matching ``_label`` width for continuation lines."""
    return " " * _LABEL_W


def _hint(text: str) -> None:
    """Print a dim next-step hint below command output (CLI-FLOW-002)."""
    console.print(f"\n  [dim]→[/dim] {text}")


# ---------------------------------------------------------------------------
# Timestamp formatting
# ---------------------------------------------------------------------------


def _parse_dt(ts: str | datetime | None) -> datetime | None:
    """Parse an ISO timestamp string or pass through a datetime."""
    if ts is None:
        return None
    if isinstance(ts, datetime):
        dt = ts
    else:
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


def _relative_time(ts: str | datetime | None) -> str:
    """Human-friendly relative time like ``3m ago`` or ``just now``."""
    dt = _parse_dt(ts)
    if dt is None:
        return "-"
    delta = int((datetime.now(tz=UTC) - dt).total_seconds())
    if delta < 0:
        return "just now"
    if delta < 60:
        return f"{delta}s ago"
    if delta < 3600:
        return f"{delta // 60}m ago"
    if delta < 86400:
        h = delta // 3600
        m = (delta % 3600) // 60
        return f"{h}h{m:02d}m ago" if m else f"{h}h ago"
    return f"{delta // 86400}d ago"


def _fmt_timestamp(ts: str | datetime | None) -> str:
    """Relative time as primary, short clock time as context.

    Returns e.g. ``3m ago (08:46:00)`` or ``2d ago (Apr 01 14:30)``.
    """
    dt = _parse_dt(ts)
    if dt is None:
        return "-"
    rel = _relative_time(ts)
    delta = int((datetime.now(tz=UTC) - dt).total_seconds())
    if delta < 86400:
        clock = dt.strftime("%H:%M:%S")
    else:
        clock = dt.strftime("%b %d %H:%M")
    return f"{rel}  [dim]({clock})[/dim]"


def _fmt_duration(start: str | datetime | None, end: str | datetime | None) -> str:
    """Format the elapsed time between two timestamps."""
    if start is None:
        return "-"

    dt_start = _parse_dt(start)
    if dt_start is None:
        return "-"
    dt_end = _parse_dt(end) if end is not None else datetime.now(tz=UTC)
    if dt_end is None:
        return "-"

    delta_secs = int((dt_end - dt_start).total_seconds())
    if delta_secs < 0:
        return "-"
    if delta_secs < 60:
        return f"{delta_secs}s"
    mins = delta_secs // 60
    secs = delta_secs % 60
    if mins < 60:
        return f"{mins}m{secs:02d}s"
    hours = mins // 60
    remaining_mins = mins % 60
    return f"{hours}h{remaining_mins:02d}m"


def _fmt_score(value: float | None, *, precision: int = 3) -> str:
    """Format a numeric score, returning a dim placeholder when ``None``."""
    if value is None:
        return "[dim]-[/dim]"
    return f"{float(value):.{precision}f}"


def _fmt_count(value: int | None) -> str:
    """Format an integer count, returning a dim placeholder when ``None``."""
    if value is None:
        return "[dim]-[/dim]"
    return f"{int(value):,}"


ArtifactType = t.Literal["capability", "dataset", "model", "task"]

_VERSION_LIST_METHODS: dict[str, str] = {
    "capability": "list_capability_versions",
    "dataset": "list_dataset_versions",
    "model": "list_model_versions",
    "task": "list_task_versions",
}


def ensure_version(api: t.Any, artifact_type: ArtifactType, ref: ArtifactRef) -> VersionedRef:
    """Return a VersionedRef, resolving latest from the API if needed."""
    if ref.version:
        return ref.with_version(ref.version)
    method = getattr(api, _VERSION_LIST_METHODS[artifact_type])
    payload = method(ref.org, ref.name)
    versions = payload.get("versions", [])
    if not versions:
        raise ValueError(f"No versions found for {ref.name}")
    return ref.with_version(str(versions[0]))


def ensure_name_only_refs(raw_refs: list[str], default_org: str) -> list[ArtifactRef]:
    """Parse refs for name-level operations and reject version-qualified inputs."""
    refs = [ArtifactRef.parse(value, default_org) for value in raw_refs]
    invalid = [ref for ref in refs if ref.version is not None]
    if invalid:
        joined = ", ".join(f"{ref.qualified_name}@{ref.version}" for ref in invalid)
        raise ValueError(f"visibility is name-level; omit @version for: {joined}")
    return refs


def resolve_publish_flag(publish: bool, public_compat: bool) -> bool:
    """Resolve publish intent, warning when the deprecated compatibility flag is used."""
    if public_compat:
        print_warning("--public is deprecated; use --publish")
    return publish or public_compat


# ---------------------------------------------------------------------------
# Render helpers
# ---------------------------------------------------------------------------

SummaryFn = t.Callable[[dict[str, t.Any]], str]
"""Takes a JSON-serializable dict, returns a one-line human summary."""

PageFetcher = t.Callable[[int, int], t.Any]
"""(page, page_size) -> raw API client response (dict or list)."""


# ---------------------------------------------------------------------------
# List-row projection (CLI-OUT-002 / CLI-OUT-004)
# ---------------------------------------------------------------------------

_LIST_ROW_BASE_KEYS: tuple[str, ...] = ("id", "name", "version", "org_key")


def _project_row(item: dict[str, t.Any], fields: t.Iterable[str]) -> dict[str, t.Any]:
    """Project a list-row dict to base identifiers plus *fields* for ``--json`` output.

    Returns the base keys (``id``, ``name``, ``version``, ``org_key``) — when the
    resource carries them — plus any of *fields* present on the row. Keys absent
    on the row are dropped silently. Nested structures and detail-only fields
    (component listings, full manifests, build status) are excluded by virtue of
    not being named in *fields*.
    """
    keys = dict.fromkeys((*_LIST_ROW_BASE_KEYS, *fields))
    return {key: item[key] for key in keys if key in item}


def _collect_pages(
    fetch: PageFetcher,
    *,
    limit: int,
    page_size: int = 100,
    items_key: str = "items",
) -> list[dict[str, t.Any]]:
    """Fetch successive pages until *limit* items are collected or results are exhausted.

    Works with API methods that return either a paginated dict (with *items_key*)
    or a plain list.  Page size is kept constant across requests so that
    server-side offset calculations stay aligned.
    """
    collected: list[dict[str, t.Any]] = []
    page = 1
    while len(collected) < limit:
        result = fetch(page, page_size)
        if isinstance(result, dict):
            items = result.get(items_key, [])
        else:
            items = _to_payload(result)
        collected.extend(
            _to_payload(item) if not isinstance(item, dict) else item for item in items
        )
        if len(items) < page_size:
            break
        page += 1
    return collected[:limit]


def _to_payload(obj: t.Any) -> t.Any:
    """Normalize a response object (Pydantic model or raw dict/list) to JSON-serializable form."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")
    if isinstance(obj, list):
        return [_to_payload(item) for item in obj]
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "__dict__"):
        return _jsonable(obj)
    return obj


def _render(obj: t.Any, *, as_json: bool, summary: SummaryFn) -> None:
    """Render a single item as JSON or a one-line summary."""
    payload = _to_payload(obj)
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        console.print(summary(payload))


def _render_list(
    obj: t.Any,
    *,
    as_json: bool,
    summary: SummaryFn,
    empty_msg: str,
    items_key: str = "items",
    fields: t.Iterable[str] | None = None,
) -> None:
    """Render a paginated list as JSON or per-item summaries.

    When *fields* is provided, ``--json`` emits a list-row projection per
    CLI-OUT-002: each item is reduced to base identifiers plus *fields*. When
    *fields* is None, the raw payload is emitted unchanged (used by detail and
    pure-machine commands).
    """
    payload = _to_payload(obj)
    items = payload.get(items_key, []) if isinstance(payload, dict) else payload
    if as_json:
        if fields is None:
            print(json.dumps(payload, indent=2, sort_keys=True))
            return
        rows = [
            _project_row(item if isinstance(item, dict) else _jsonable(item), fields)
            for item in items
        ]
        print(json.dumps(rows, indent=2, sort_keys=True))
        return
    if not items:
        console.print(f"[dim]{empty_msg}[/dim]")
        return
    for item in items:
        console.print(summary(_jsonable(item) if not isinstance(item, dict) else item))


def _render_logs(obj: t.Any, *, as_json: bool) -> None:
    """Render a log response (training or optimization)."""
    payload = _to_payload(obj)
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    for entry in payload.get("items", []):
        level = entry["level"]
        level_color = (
            "red" if level in {"ERROR", "CRITICAL"} else "yellow" if level == "WARNING" else "dim"
        )
        console.print(
            f"[dim]{entry['timestamp']}[/dim] [{level_color}]{level}[/{level_color}] {entry['message']}"
        )


def _render_artifacts(obj: t.Any, *, as_json: bool) -> None:
    """Render an artifacts response (training or optimization)."""
    payload = _to_payload(obj)
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    print(json.dumps(payload.get("artifacts", {}), indent=2, sort_keys=True))


# --- Shared summary functions (used by multiple domain modules) ---


def _summarize_package(p: dict[str, t.Any]) -> str:
    name = p.get("full_name") or p.get("name", "unknown")
    version = p.get("latest_version") or p.get("version", "unknown")
    visibility = p.get("visibility", "private")
    return f"[cyan]{name}[/cyan]@[dim]{version}[/dim] {_visibility_markup(visibility)}"


_PACKAGE_LIST_ROW_FIELDS: tuple[str, ...] = (
    "full_name",
    "summary",
    "visibility",
    "type",
    "package_type",
    "latest_version",
    "created_at",
    "updated_at",
)


def _summarize_sandbox(payload: dict[str, t.Any]) -> str:
    sandbox_id = payload.get("id", "unknown")
    provider_sandbox_id = payload.get("provider_sandbox_id", "unknown")
    state = payload.get("state", "unknown")
    sandbox_kind = payload.get("sandbox_kind", "unknown")
    project_key = payload.get("project_key")
    color = _status_color(state)
    project_suffix = f" [dim]project={project_key}[/dim]" if project_key else ""
    return (
        f"[dim]{sandbox_id}[/dim] [{color}]{state}[/{color}] "
        f"[cyan]{sandbox_kind}[/cyan] [dim]{provider_sandbox_id}[/dim]{project_suffix}"
    )


_SANDBOX_LIST_ROW_FIELDS: tuple[str, ...] = (
    "provider_sandbox_id",
    "state",
    "sandbox_kind",
    "project_id",
    "project_key",
    "created_at",
    "updated_at",
)


def _render_package_list(packages: t.Any, *, as_json: bool) -> None:
    _render_list(
        packages,
        as_json=as_json,
        summary=_summarize_package,
        empty_msg="No packages found",
        fields=_PACKAGE_LIST_ROW_FIELDS,
    )


# ---------------------------------------------------------------------------
# Wait / poll helpers
# ---------------------------------------------------------------------------

_TERMINAL_STATUSES = {"completed", "partial", "failed", "cancelled"}


def _get_status(obj: t.Any) -> str | None:
    """Extract status from a Pydantic model (.status) or raw dict (.get('status'))."""
    if hasattr(obj, "status"):
        return obj.status
    if isinstance(obj, dict):
        return obj.get("status")
    return None


def _wait_for_job(
    poll_fn: t.Callable[[], T],
    *,
    job_id: str,
    label: str,
    poll_interval_sec: float,
    timeout_sec: float | None,
) -> T:
    """Generic poll-until-terminal loop. ``poll_fn`` takes no args and returns the job."""
    deadline = None if timeout_sec is None else time.monotonic() + timeout_sec
    while True:
        job = poll_fn()
        if _get_status(job) in _TERMINAL_STATUSES:
            return job
        if deadline is not None and time.monotonic() >= deadline:
            raise TimeoutError(f"Timed out waiting for {label} job {job_id}")
        time.sleep(poll_interval_sec)


# ---------------------------------------------------------------------------
# Sync progress callback
# ---------------------------------------------------------------------------


def _sync_progress(name: str, status: str, error: str | None) -> None:
    if status == "uploaded":
        print_success(name, indent=2)
    elif status == "skipped":
        print_skip(name, indent=2)
    elif status == "failed":
        print_error(f"{name}: {error}", indent=2)
