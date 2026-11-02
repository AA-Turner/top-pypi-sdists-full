"""Agent Platform CLI - resource/operation style commands."""

import hashlib
import json
import os
import re
import shlex
import stat
import uuid
from pathlib import Path
from typing import Any, List, Optional
from urllib.parse import quote

import typer
from ap_client import __version__, get_client, get_config, tbb
from ap_client.akpool_commands import register as _register_akpool_commands
from ap_client.api import (
    APIError,
    PaginationProtocolError,
    _merge_meta_tags,
    set_cluster_override,
    set_verbose_override,
)
from ap_client.config import ENV_VAR_SPECS, ConfigurationError, _parse_bool, normalize_output_format
from ap_client.dataset_commands import register as _register_dataset_commands
from ap_client.dfs_commands import register as _register_dfs_commands
from ap_client.exporter import export_group, export_job, export_jobs
from ap_client.fs_commands import register as _register_fs_commands
from ap_client.instance_commands import register as _register_instance_commands
from ap_client.managed_ak import (
    ManagedAKProtocolError,
    require_managed_ak_ack,
    response_ak_ids,
    validate_ak_id,
    validate_ak_selection,
)
from ap_client.profile_commands import profile_app
from ap_client.waiter import (
    WaitTimeoutError,
    wait_for_group,
    wait_for_group_post_process,
    wait_for_job,
)
from rich import print
from rich.console import Console
from rich.table import Table

# Verbose mode (AP_VERBOSE / --verbose) also controls whether Typer's pretty
# traceback dumps local variables on unhandled exceptions. Default is off to
# avoid leaking large payloads (URLs, events, job dicts) to end users.
_INITIAL_VERBOSE = _parse_bool(os.environ.get("AP_VERBOSE"))

app = typer.Typer(
    name="ap",
    help="Agent Platform CLI - minimal job submission tool",
    add_completion=False,
    no_args_is_help=True,
    pretty_exceptions_show_locals=_INITIAL_VERBOSE,
)
console = Console()
error_console = Console(stderr=True)

_NON_JSON_RESPONSE_DETAIL = "Unexpected non-JSON response from API endpoint"
_NON_JSON_RESPONSE_HINT = (
    "The request may have reached a gateway or non-API service. Check AP_CLUSTER and AP_BASE_URL."
)
_JOB_STATUS_HELP = (
    "Job status. Values: Queued, Pending, Running, Succeeded, Failed, Cancelled, Unknown"
)
_ISO_TIME_HELP = "ISO time, e.g. 2026-03-26T00:00:00 or 2026-03-26T00:00:00+08:00"
_PLAIN_VALUE_PREVIEW = 160
_RESOURCE_PROFILE_ID_RE = re.compile(r"rp-[A-Za-z0-9][A-Za-z0-9-]*")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def _global_options(
    cluster: Optional[str] = typer.Option(
        None,
        "--cluster",
        help="Target cluster; overrides AP_CLUSTER and AP_HEADERS X-Cluster",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print HTTP Request/Response details to stderr (overrides AP_VERBOSE)",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Global CLI options."""
    del version
    if cluster is not None:
        cluster = cluster.strip()
        if not cluster:
            raise typer.BadParameter("--cluster cannot be empty")
    set_cluster_override(cluster)
    if verbose:
        set_verbose_override(True)
        # Keep traceback-locals behavior in sync with the HTTP verbose switch.
        app.pretty_exceptions_show_locals = True


# Resource sub-command groups
config_app = typer.Typer(
    help="Configuration operations",
    invoke_without_command=True,
    no_args_is_help=False,
)
template_app = typer.Typer(help="Template operations")
dataset_app = typer.Typer(help="Dataset operations")
job_app = typer.Typer(help="Job operations")
job_tbb_app = typer.Typer(help="TrajBigBang pipeline job operations")
group_app = typer.Typer(help="Group operations")
meta_model_app = typer.Typer(help="Meta model vocabulary")
meta_job_type_app = typer.Typer(help="Meta job type vocabulary")
meta_tag_app = typer.Typer(help="QwenMeta meta tag catalog (generic meta-* keys)")
meta_train_stage_app = typer.Typer(help="Meta train stage vocabulary (QwenMeta catalog)")
meta_teacher_direction_app = typer.Typer(
    help="Meta teacher direction vocabulary (QwenMeta catalog)"
)
plan_app = typer.Typer(help="Eval plan operations")
datasource_app = typer.Typer(help="DataSource operations (OSS / NAS mount configs)")
concurrency_policy_app = typer.Typer(
    help="Concurrency resource operations (global concurrency-capacity pools)"
)
template_credential_app = typer.Typer(help="Template credential operations")
secret_app = typer.Typer(help="Secret (credential) management")
cluster_app = typer.Typer(help="Cluster operations")
benchmark_app = typer.Typer(help="Benchmark registry operations")
checkpoint_app = typer.Typer(help="Checkpoint operations")

app.add_typer(config_app, name="config")
app.add_typer(template_app, name="template")
app.add_typer(dataset_app, name="dataset")
app.add_typer(job_app, name="job")
job_app.add_typer(job_tbb_app, name="tbb")
app.add_typer(group_app, name="group")
app.add_typer(plan_app, name="plan")
app.add_typer(datasource_app, name="datasource")
app.add_typer(concurrency_policy_app, name="concurrency-policy")
app.add_typer(template_credential_app, name="template-credential")
app.add_typer(secret_app, name="secret")
app.add_typer(profile_app, name="profile")
app.add_typer(cluster_app, name="cluster")
app.add_typer(meta_model_app, name="meta-model")
app.add_typer(meta_job_type_app, name="meta-job-type")
app.add_typer(meta_tag_app, name="meta-tag")
app.add_typer(meta_train_stage_app, name="meta-train-stage")
app.add_typer(meta_teacher_direction_app, name="meta-teacher-direction")
app.add_typer(benchmark_app, name="benchmark")
app.add_typer(checkpoint_app, name="checkpoint")

# Dataset 领域(见 docs/ap-cli-dataset-refactor-design.md):
# ap dataset version/split/access 嵌套在 dataset 下;instance/fs 是一等资源。
_register_dataset_commands(dataset_app)
_register_instance_commands(app)
_register_dfs_commands(app)
_register_fs_commands(app)
_register_akpool_commands(app)

_PAI_RUNTIME_ENV_TAGS: tuple[tuple[str, str], ...] = (
    ("DLC_JOB_ID", "dlc_job_id"),
    ("DSW_INSTANCE_ID", "dsw_instance_id"),
    ("PAI_WORKSPACE_ID", "pai_workspace_id"),
    ("PAI_WORKSPACE_NAME", "pai_workspace_name"),
    ("PAI_USER_ID", "pai_user_id"),
    ("PAI_CLUSTER_ID", "pai_cluster_id"),
)


def _print_json(data):
    """Pretty-print JSON output."""
    console.print_json(json.dumps(data, ensure_ascii=False, indent=2))


def _emit_info(message: str, output_format: str = "plain") -> None:
    typer.echo(message, err=output_format != "plain")


def _emit_progress(message: str) -> None:
    typer.echo(message, err=True)


def _job_create_progress():
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn

    return Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.fields[current_job]}"),
        TextColumn("{task.fields[current_stage]}"),
        console=Console(stderr=True),
        transient=True,
    )


def _build_job_create_retry_command(*, idempotency_key: str) -> str:
    return f"Rerun your original command with --idempotency-key {shlex.quote(idempotency_key)}"


def _emit_idempotency_retry_hint(command: str) -> None:
    typer.echo("", err=True)
    typer.secho("Retry this submission with:", dim=True, err=True)
    typer.secho(command, dim=True, err=True)


def _emit_error(message: str) -> None:
    error_console.print(f"[red]error: {message}[/]")


def _read_client(share_token: Optional[str] = None, group_id: Optional[str] = None):
    if group_id and not share_token:
        raise typer.BadParameter("--group-id requires --share-token")
    client = get_client()
    if share_token is None:
        return client
    from ap_client.share_api import ShareAPIClient

    # Typer verbose tracebacks must not render the share token in locals.
    app.pretty_exceptions_show_locals = False
    try:
        return ShareAPIClient.from_client(client, share_token, group_id=group_id)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


def _reject_account_pool_template_credential_cli(
    account_pool: Optional[str],
    *credential_types: Any,
) -> None:
    if not account_pool or not account_pool.strip():
        return
    if any(value is not None and str(value).strip() for value in credential_types):
        _emit_error(
            "--account-pool and --credential-type cannot be used together; "
            "Account Pool account types are defined by the Bench Configuration"
        )
        raise typer.Exit(1)


def _parse_json_object(raw: Optional[str], option_name: str) -> Optional[dict]:
    if raw is None:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        _emit_error(f"failed to parse {option_name} JSON: {exc}")
        raise typer.Exit(1)
    if not isinstance(value, dict):
        _emit_error(f"{option_name} must be a JSON object")
        raise typer.Exit(1)
    return value


def _parse_datasources_option(raw: Optional[str]) -> Optional[list]:
    if raw is None:
        return None
    value = raw.strip()
    if value.startswith("["):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            _emit_error(f"failed to parse --datasources JSON: {exc}")
            raise typer.Exit(1)
        if not isinstance(parsed, list):
            _emit_error("--datasources must be a JSON array")
            raise typer.Exit(1)
        return parsed
    return [item.strip() for item in value.split(",") if item.strip()] or None


def _parse_file_selectors(values: Optional[list[str]]) -> Optional[list[str]]:
    """Expand repeatable, comma-separated file selector options."""
    selectors = [
        item.strip() for value in values or [] for item in value.split(",") if item.strip()
    ]
    return list(dict.fromkeys(selectors)) or None


def _read_json_object_option(
    raw: Optional[str], file_path: Optional[str], option_name: str
) -> Optional[dict]:
    """Parse a JSON object from an inline ``--opt`` string or ``--opt-file``.

    Returns ``None`` when neither is given. ``option_name`` is used in errors.
    """
    if raw is not None:
        return _parse_json_object(raw, option_name)
    if file_path is None:
        return None
    try:
        text = Path(file_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        _emit_error(f"file not found: {file_path}")
        raise typer.Exit(1)
    return _parse_json_object(text, option_name)


def _parse_model_base_url_collection_option(
    raw: Optional[str], file_path: Optional[str]
) -> Optional[list]:
    if raw is not None:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            return [u.strip() for u in raw.split(",") if u.strip()]
        if not isinstance(value, list):
            _emit_error("--model-base-url-collection must be a JSON array")
            raise typer.Exit(1)
        return value

    if file_path is None:
        return None

    try:
        return [
            line.strip()
            for line in Path(file_path).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except FileNotFoundError:
        _emit_error(f"file not found: {file_path}")
        raise typer.Exit(1)


def _format_wait_timeout(timeout: Optional[float]) -> str:
    if timeout is None:
        return "none"
    if timeout == int(timeout):
        return f"{int(timeout)}s"
    return f"{timeout:g}s"


def _fmt_timeout(timeout: Optional[float]) -> str:
    if timeout is None:
        return "none"
    return f"{timeout:g}"


def _normalize_output_format(
    output_format: str | None, default: str = "plain", keep_table: bool = False
) -> str:
    try:
        return normalize_output_format(output_format, default, keep_table=keep_table)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


def _parse_instance_range(value: str) -> slice:
    raw = value.strip()
    if not raw:
        raise ValueError("--range must not be empty")

    if raw.startswith("range(") and raw.endswith(")"):
        raw = raw[len("range(") : -1]
        parts = [part.strip() for part in raw.split(",")]
        if len(parts) == 1:
            parts = ["", parts[0]]
    elif "," in raw:
        parts = [part.strip() for part in raw.split(",")]
    elif ":" in raw:
        parts = [part.strip() for part in raw.split(":")]
    else:
        parts = ["", raw]

    if len(parts) not in {2, 3}:
        raise ValueError(
            "--range must use END, START,END, START,END,STEP; also accepts START:END[:STEP] or range(...)"
        )

    try:
        start = int(parts[0]) if parts[0] else None
        stop = int(parts[1]) if parts[1] else None
        step = int(parts[2]) if len(parts) == 3 and parts[2] else None
    except ValueError as exc:
        raise ValueError("--range values must be integers") from exc

    if step == 0:
        raise ValueError("--range step must not be 0")
    if start is None and stop is None and step is None:
        raise ValueError("--range must specify at least one of start, end, or step")

    return slice(start, stop, step)


def _parse_instance_id_csv(value: str, option_name: str) -> list[str]:
    stripped = value.strip()
    if stripped.startswith("@"):
        file_path = stripped[1:].strip()
        if not file_path:
            raise ValueError(f"{option_name} '@' must be followed by a file path")
        path = Path(file_path)
        try:
            mode = path.stat().st_mode
        except FileNotFoundError as exc:
            raise ValueError(f"{option_name} file not found: {file_path}") from exc
        except OSError as exc:
            detail = exc.strerror or str(exc)
            raise ValueError(f"{option_name} failed to read file: {file_path}: {detail}") from exc
        if not stat.S_ISREG(mode):
            raise ValueError(f"{option_name} file is not a regular file: {file_path}")
        try:
            text = path.read_text(encoding="utf-8-sig")
        except FileNotFoundError as exc:
            raise ValueError(f"{option_name} file not found: {file_path}") from exc
        except UnicodeDecodeError as exc:
            raise ValueError(f"{option_name} file is not valid UTF-8: {file_path}") from exc
        except OSError as exc:
            detail = exc.strerror or str(exc)
            raise ValueError(f"{option_name} failed to read file: {file_path}: {detail}") from exc
        tokens = text.replace(",", "\n").splitlines()
    else:
        tokens = value.split(",")
    ids = [iid.strip() for iid in tokens if iid.strip()]
    if not ids:
        raise ValueError(f"{option_name} must include at least one instance id")
    return ids


def _normalize_resource_profile_id(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = value.strip()
    if not _RESOURCE_PROFILE_ID_RE.fullmatch(normalized):
        raise ValueError("--resource-profile must be an rp-* ID")
    return normalized


def _require_resource_profile_ack(result: dict, resource_profile_id: Optional[str]) -> None:
    """Reject a response that did not apply the requested Resource Profile."""

    if resource_profile_id is None:
        return
    if result.get("resource_profile_id") == resource_profile_id:
        return
    _emit_error(
        f"server did not acknowledge Resource Profile {resource_profile_id}; "
        "the target AP server may not support Resource Profile submission"
    )
    raise typer.Exit(1)


def _require_profile_ack(result: dict, profile: str) -> None:
    """Detect servers that silently ignored the Profile reference (even in dry-run)."""
    profile_id = result.get("profile_id")
    version = result.get("profile_version")
    if isinstance(profile_id, str) and profile_id.strip() and type(version) is int and version > 0:
        return
    identifiers = {key: result[key] for key in ("job_id", "group_id") if result.get(key)}
    jobs = result.get("jobs")
    if isinstance(jobs, list):
        identifiers["job_ids"] = [
            job["job_id"] for job in jobs if isinstance(job, dict) and job.get("job_id")
        ]
    _emit_error(
        f"server did not return a resolved profile_id and profile_version for {profile!r}. "
        "Deploy an AP server supporting profile references before using this CLI. "
        "Jobs may already have been created, even with --dry-run; check the returned IDs "
        f"before retrying: {json.dumps(identifiers)}. No legacy-field retry was sent."
    )
    raise typer.Exit(1)


def _select_instance_ids(
    instance_ids: list[str],
    instance_range: Optional[str],
    exclude_instance_ids: Optional[str],
) -> list[str]:
    selected = instance_ids

    if instance_range:
        selected = selected[_parse_instance_range(instance_range)]
        if not selected:
            raise ValueError("--range selected no instance ids")

    if exclude_instance_ids:
        excluded = set(_parse_instance_id_csv(exclude_instance_ids, "--exclude-instance-ids"))
        selected = [iid for iid in selected if iid not in excluded]
        if not selected:
            raise ValueError("no instance ids remain after --exclude-instance-ids")

    return selected


def _print_formatted(data: dict, output_format: str) -> None:
    if output_format == "json":
        typer.echo(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if output_format == "yaml":
        try:
            import yaml
        except ImportError as exc:
            raise typer.BadParameter("--format yaml requires PyYAML to be installed") from exc

        class LosslessDumper(yaml.SafeDumper):
            pass

        def represent_string(dumper, value):
            # YAML normalizes literal NEL/line separators in unquoted scalars.
            # Double quotes make the emitter escape them while keeping Chinese readable.
            style = '"' if any(character in value for character in "\x85\u2028\u2029") else None
            return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)

        LosslessDumper.add_representer(str, represent_string)
        typer.echo(yaml.dump(data, Dumper=LosslessDumper, allow_unicode=True, sort_keys=False))
        return
    _print_json(data)


def _print_job_create_dry_run(
    client,
    payloads: list[dict],
    *,
    output_format: str,
) -> None:
    result = {
        "dry_run": True,
        "request": {
            "method": "POST",
            "url": client._url("/jobs"),
            "headers": client.preview_request_headers(),
        },
        "payloads": payloads,
    }
    _print_formatted(result, "json" if output_format == "plain" else output_format)


def _emit_dry_run_warnings(warnings: list[str]) -> None:
    for warning in warnings:
        typer.echo(f"warning: {warning}", err=True)


def _print_plain_table(rows: list[dict], columns: list[tuple[str, str]]) -> None:
    if not rows:
        typer.echo("")
        return

    widths = []
    for key, title in columns:
        width = len(title)
        for row in rows:
            width = max(width, len(_stringify_cell(row.get(key))))
        widths.append(width)

    header = "  ".join(title.ljust(width) for (_, title), width in zip(columns, widths))
    typer.echo(header)
    for row in rows:
        typer.echo(
            "  ".join(
                _stringify_cell(row.get(key)).ljust(width)
                for (key, _title), width in zip(columns, widths)
            )
        )


def _stringify_cell(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def _print_rich_table(rows: list[dict], columns: list[tuple[str, str]]) -> None:
    """Render a table via rich (used by AP_FORMAT=table / --format table).

    rich measures East-Asian wide characters correctly, so CJK values (e.g. user
    real names) stay aligned — unlike the hand-rolled ``_print_plain_table`` used
    for the verbatim default (plain) output. Rendered at full width so columns are
    never truncated; the terminal soft-wraps overly wide lines.
    """
    if not rows:
        typer.echo("")
        return
    from rich import box

    table = Table(
        box=box.SIMPLE_HEAD,
        header_style="bold cyan",
        show_edge=False,
        pad_edge=False,
        padding=(0, 1),
    )
    for _key, title in columns:
        table.add_column(title, no_wrap=True)
    for row in rows:
        table.add_row(*[_stringify_cell(row.get(key)) for key, _title in columns])
    Console(width=10_000, highlight=False).print(table)


# Envelope keys whose list value holds the records to tabulate (checked in order).
_RECORD_LIST_KEYS = (
    "datasets",
    "instance_ids",
    "versions",
    "templates",
    "containers",
    "artifacts",
    "acl",
    "items",
    "jobs",
    "runs",
    "data",
)


def _stringify_table_value(value: object, max_len: int = 80) -> str:
    """Render a single cell value: compact nested structures and truncate long text."""
    if value is None:
        return ""
    if isinstance(value, list):
        # Scalar list → comma-joined (much more readable than JSON brackets).
        if all(not isinstance(v, (dict, list)) for v in value):
            text = ", ".join(str(v) for v in value) if value else "-"
        else:
            text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    elif isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    else:
        text = str(value)
    if len(text) > max_len:
        text = text[: max_len - 1] + "…"
    return text


def _print_records_table(data: object) -> None:
    """Render list-like API data as a plain table.

    Accepts either a bare list or an envelope dict wrapping a list field
    (e.g. ``{"datasets": [...]}``). Falls back to JSON when the data has no
    tabular list structure (e.g. a single nested object).
    """
    records: object = data
    if isinstance(data, dict):
        list_keys = [key for key, value in data.items() if isinstance(value, list)]
        if not list_keys:
            _print_json(data)
            return
        chosen = next((key for key in _RECORD_LIST_KEYS if key in list_keys), list_keys[0])
        records = data[chosen]
    if not isinstance(records, list):
        _print_json(data)
        return
    if not records:
        typer.echo("")
        return
    if any(isinstance(record, dict) for record in records):
        columns: list[str] = []
        seen: set[str] = set()
        for record in records:
            if isinstance(record, dict):
                for key in record:
                    if key not in seen:
                        seen.add(key)
                        columns.append(key)
        rows = [
            {column: _stringify_table_value(record.get(column)) for column in columns}
            if isinstance(record, dict)
            else {columns[0]: _stringify_table_value(record)}
            for record in records
        ]
        _print_rich_table(rows, [(column, column) for column in columns])
    else:
        rows = [{"value": _stringify_table_value(record)} for record in records]
        _print_rich_table(rows, [("value", "value")])


# Registry-domain suffixes that carry no signal when scanning a template list.
_IMAGE_HOST_NOISE_MARKERS = ("-docker-registry", "-registry", "-docker")


def _shorten_image(image: str) -> str:
    """Shorten a container image for table display.

    Keeps the meaningful ``namespace/repo:tag`` tail intact and reduces the long
    registry host to a short alias, dropping boilerplate like
    ``-docker-registry-vpc.<region>.cr.aliyuncs.com``. Prod/staging registries stay
    distinguishable (e.g. ``code-agi-sg`` vs ``agent-platform-staging``). The full
    image is always available via ``--format json`` or ``ap template get``.
    """
    if not image or "/" not in image:
        return image
    host, path = image.split("/", 1)
    # Only treat the first segment as a registry host if it looks like a domain/port.
    if "." not in host and ":" not in host:
        return image
    label = host.split(".", 1)[0]
    for marker in _IMAGE_HOST_NOISE_MARKERS:
        idx = label.find(marker)
        if idx > 0:
            label = label[:idx]
            break
    return f"{label}/{path}"


def _print_template_list_plain(templates: list) -> None:
    """Render template list matching the web console format.

    Columns: name | image | sidecars (comma-joined) | params (count).
    """
    if not templates:
        typer.echo("")
        return
    rows = []
    for t in templates:
        if not isinstance(t, dict):
            rows.append({"name": str(t)})
            continue
        sidecars = t.get("sidecars") or []
        params = t.get("params") or []
        rows.append(
            {
                "name": t.get("name", ""),
                "image": _shorten_image(t.get("image", "")),
                "sidecars": ", ".join(str(s) for s in sidecars) if sidecars else "-",
                "params": str(len(params)) if isinstance(params, list) else str(params),
            }
        )
    _print_rich_table(
        rows,
        [("name", "name"), ("image", "image"), ("sidecars", "sidecars"), ("params", "params")],
    )


def _print_json_block(data: Any) -> None:
    typer.echo(json.dumps(data, ensure_ascii=False, indent=2))


def _format_nested_detail(value: Any) -> str:
    """Nested dict/list for detail views: compact one-liner, pretty JSON when long.

    A detail view must not silently drop data - the manifest in ``ap instance
    get`` used to be cut mid-JSON by the one-liner preview.
    """
    compact = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if len(compact) <= _PLAIN_VALUE_PREVIEW:
        return compact
    return json.dumps(value, ensure_ascii=False, indent=2)


def _print_detail(data: object) -> None:
    """Render a single object as an aligned key/value detail view.

    Top-level scalars become key/value rows (``image`` fields shortened); nested
    dict/list fields are shown as compact one-liners, or pretty-printed across
    multiple lines when the one-liner would not fit. Falls back to JSON for
    non-dict payloads.
    """
    if not isinstance(data, dict):
        _print_json(data)
        return
    rows: list[tuple[str, str]] = []
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            rows.append((key, _format_nested_detail(value)))
        elif key == "image" and isinstance(value, str):
            rows.append((key, _shorten_image(value)))
        else:
            rows.append((key, _format_plain_value(value, max_len=0)))
    width = max((len(label) for label, _text in rows), default=0)
    indent = " " * (width + 4)
    for label, text in rows:
        if "\n" in text:
            text = text.replace("\n", f"\n{indent}")
        typer.echo(f"  {label.ljust(width)}: {text}")


def _print_template_get_plain(t: dict) -> None:
    """Render template detail matching the web console: basic info + params table."""
    if not isinstance(t, dict):
        _print_json(t)
        return
    typer.echo("Template")
    _print_key_values(
        [
            ("name", t.get("name")),
            ("image", _shorten_image(t.get("image", ""))),
            ("version", t.get("version")),
            ("privileged", t.get("privileged")),
        ],
        skip_empty=False,
    )

    resources = t.get("resources")
    if isinstance(resources, dict) and resources:
        typer.echo("\nResources")
        _print_key_values(list(resources.items()), skip_empty=True)

    sidecars = t.get("sidecars") or {}
    sidecar_names = list(sidecars.keys()) if isinstance(sidecars, dict) else list(sidecars)
    typer.echo(f"\nSidecars: {', '.join(sidecar_names) if sidecar_names else '-'}")

    params_schema = t.get("params_schema")
    if isinstance(params_schema, dict) and params_schema:
        typer.echo(f"\nParams ({len(params_schema)})")
        rows = []
        for name, spec in params_schema.items():
            spec = spec if isinstance(spec, dict) else {}
            default = spec.get("default")
            rows.append(
                {
                    "param": str(name),
                    "required": "yes" if spec.get("required") else "",
                    "default": "" if default is None else str(default),
                    "description": str(spec.get("description") or ""),
                }
            )
        _print_rich_table(
            rows,
            [
                ("param", "param"),
                ("required", "required"),
                ("default", "default"),
                ("description", "description"),
            ],
        )


def _field_path_requires_params(path: str) -> bool:
    root = path.split(".", 1)[0].split("[", 1)[0]
    return root in {"params", "masked_params"}


def _field_path_requires_spec(path: str) -> bool:
    root = path.split(".", 1)[0].split("[", 1)[0]
    return root == "job_spec_data"


def _parse_field_path(path: str) -> list[str | int]:
    parts: list[str | int] = []
    for segment in path.split("."):
        if not segment:
            raise ValueError("field path contains an empty segment")
        name, rest = segment.split("[", 1) if "[" in segment else (segment, "")
        if name:
            parts.append(name)
        while rest:
            index_text, sep, tail = rest.partition("]")
            if not sep:
                raise ValueError("field path has an unclosed list index")
            if not index_text.isdigit():
                raise ValueError("field path list indexes must be non-negative integers")
            parts.append(int(index_text))
            if not tail:
                break
            if not tail.startswith("["):
                raise ValueError("field path has invalid list index syntax")
            rest = tail[1:]
    return parts


def _extract_field(data: Any, path: str) -> Any:
    current = data
    for part in _parse_field_path(path):
        if isinstance(part, int):
            if not isinstance(current, list) or part >= len(current):
                raise KeyError(path)
            current = current[part]
            continue
        if not isinstance(current, dict) or part not in current:
            raise KeyError(path)
        current = current[part]
    return current


def _print_field_value(value: Any, output_format: str) -> None:
    if not isinstance(value, (dict, list)):
        if value is None:
            return
        typer.echo(str(value))
        return
    _print_formatted(value, "json" if output_format == "plain" else output_format)


def _format_plain_value(value: Any, *, max_len: int = _PLAIN_VALUE_PREVIEW) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    else:
        text = str(value)
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    if not max_len or len(text) <= max_len:
        return text
    return f"{text[: max_len - 3]}..."


def _print_key_values(rows: list[tuple[str, Any]], *, skip_empty: bool = True) -> None:
    width = max((len(label) for label, _value in rows), default=0)
    for label, value in rows:
        if value is None or (skip_empty and value == ""):
            continue
        typer.echo(f"  {label.ljust(width)}: {_format_plain_value(value)}")


def _print_params_plain(params: Any, masked_params: list) -> None:
    if not isinstance(params, dict):
        _print_key_values([("value", params)], skip_empty=False)
        return
    masked_paths = {str(path) for path in masked_params}
    rows: list[tuple[str, Any]] = []
    for key, value in params.items():
        display_value = _format_plain_value(value)
        # 直接信任 masked_params 路径：服务端掩码形态已扩展为保留首尾（如
        # sk-***890 / ****），不能再按值严格等于 "***" 判断，否则形态变化后
        # (masked) 标识静默丢失
        if str(key) in masked_paths:
            display_value = f"{display_value} (masked)"
        rows.append((str(key), display_value))
    _print_key_values(rows, skip_empty=False)


def _print_content_notice(rows: list[dict]) -> None:
    if any(
        row.get("transparency") == "blackbox" and row.get("can_read_content") is False
        for row in rows
    ):
        typer.echo("Blackbox content is hidden; Group Reader access is required.")


def _content_columns(rows: list[dict], columns: list[str]) -> list[str]:
    restricted = {field for row in rows for field in (row.get("restricted_fields") or [])}
    return [
        field
        for field in columns
        if field not in restricted or any(row.get(field) is not None for row in rows)
    ]


def _print_job_get_plain(job: dict) -> None:
    typer.echo("Job")
    _print_content_notice([job])
    _print_key_values(
        [
            ("job_id", job.get("job_id")),
            ("job_name", job.get("job_name")),
            ("status", job.get("status")),
            ("error_code", job.get("error_code")),
            ("template", job.get("template")),
            ("instance_id", job.get("instance_id")),
            ("group_id", job.get("group_id")),
            ("job_type", job.get("job_type")),
            ("attempt", job.get("attempt")),
        ]
    )

    bindings = job.get("ak_bindings") or []
    rows = [
        {**parameter, "ak_id": binding["ak_id"]}
        for binding in bindings
        for parameter in binding.get("parameters", [])
    ]
    if "ak_bindings.parameters" in (job.get("restricted_fields") or []):
        typer.echo("\nManaged AK parameters: content access required")
    elif rows:
        typer.echo("\nManaged AK parameters")
        for row in rows:
            typer.echo(f"  {row['parameter']}: {row['value']} -> {row['ak_id']}")
        if any("parameters" not in binding for binding in bindings):
            typer.echo("  Some historical parameter mappings are unavailable")
    elif response_ak_ids(job):
        typer.echo("\nManaged AK parameters: historical mapping unavailable")
    elif "ak_bindings" in job:
        typer.echo("\nManaged AK parameters\n  No managed AK used")

    meta_pairs = [
        ("meta_model", job.get("meta_model")),
        ("meta_job_type", job.get("meta_job_type")),
        ("meta_train_stage", job.get("meta_train_stage")),
        ("meta_teacher_direction", job.get("meta_teacher_direction")),
        ("upstream_platform", job.get("upstream_platform")),
        ("upstream_job_id", job.get("upstream_job_id")),
    ]
    if any(value for _, value in meta_pairs):
        typer.echo("\nMeta")
        _print_key_values([(k, v) for k, v in meta_pairs if v])

    typer.echo("\nScheduling")
    _print_key_values(
        [
            ("queue_id", job.get("queue_id")),
            ("quota_id", job.get("quota_id")),
            ("quota_name", job.get("quota_name")),
            ("concurrency_policy_id", job.get("concurrency_policy_id")),
            ("region", job.get("region")),
            ("priority", job.get("priority")),
            ("priority_weight", job.get("priority_weight")),
            ("resource_mode", job.get("resource_mode")),
            ("runner", job.get("runner")),
            ("k8s_namespace", job.get("k8s_namespace")),
        ]
    )

    if job.get("checkpoint") or job.get("benchmark") or job.get("experiment"):
        typer.echo("\nBenchmark+ckpt")
        _print_key_values(
            [
                ("checkpoint", job.get("checkpoint")),
                ("benchmark", job.get("benchmark")),
                ("experiment", job.get("experiment")),
            ]
        )

    typer.echo("\nUser")
    _print_key_values(
        [
            ("user_id", job.get("user_id")),
            ("user_name", job.get("user_name")),
            ("user_realname", job.get("user_realname")),
        ]
    )

    # 展示固化的后处理配置摘要（配置名/镜像/active_version；未命中为 null 时跳过）。
    _post_process = job.get("post_process")
    if isinstance(_post_process, dict) and _post_process.get("name"):
        typer.echo("\nPost Process")
        _print_key_values(
            [
                ("name", _post_process.get("name")),
                ("image", _post_process.get("image")),
                ("active_version", _post_process.get("active_version")),
            ]
        )

    typer.echo("\nTimeline")
    _print_key_values(
        [
            ("created_at", job.get("created_at")),
            ("queued_at", job.get("queued_at")),
            ("submitted_at", job.get("submitted_at")),
            ("k8s_start_time", job.get("k8s_start_time")),
            ("k8s_ready_time", job.get("k8s_ready_time")),
            ("k8s_completion_time", job.get("k8s_completion_time")),
            ("finished_at", job.get("finished_at")),
            ("updated_at", job.get("updated_at")),
        ]
    )

    lifecycle = job.get("lifecycle")
    if isinstance(lifecycle, dict) and lifecycle:
        typer.echo("\nLifecycle")
        _print_key_values(list(lifecycle.items()))

    if job.get("failed_reason"):
        typer.echo("\nFailure")
        _print_key_values([("failed_reason", job.get("failed_reason"))])

    if job.get("tags"):
        typer.echo("\nTags")
        tags = job.get("tags")
        if isinstance(tags, list):
            for tag in tags:
                typer.echo(f"  {tag}")
        else:
            typer.echo(f"  {tags}")

    if "params" in job:
        typer.echo("\nParams")
        _print_params_plain(job.get("params"), job.get("masked_params") or [])

    if "job_spec_data" in job:
        typer.echo("\nJob Spec")
        job_spec_data = job.get("job_spec_data") or {}
        if isinstance(job_spec_data, dict) and "spec_yaml" in job_spec_data:
            typer.echo(job_spec_data["spec_yaml"])
        else:
            _print_json_block(job_spec_data)


def _merge_job_tags(tags: Optional[list[str]]) -> Optional[list[str]]:
    merged: list[str] = []
    seen_tags: set[str] = set()

    for raw in (tags or []) + _runtime_job_tags():
        tag = str(raw).strip()
        if not tag or tag in seen_tags:
            continue
        merged.append(tag)
        seen_tags.add(tag)

    return merged or None


def _parse_tag_pairs(tag: Optional[list[str]]) -> Optional[list[str]]:
    """解析 job create --tag key:value（可重复）。

    同一对 key:value 去重；同 key 不同 value 报错（与 --meta-model 冲突
    检测语义一致，避免静默覆盖）。
    """
    if not tag:
        return None
    pairs: list[str] = []
    seen_pairs: set[str] = set()
    key_values: dict[str, str] = {}
    for raw in tag:
        pair = str(raw).strip()
        if ":" not in pair:
            raise ValueError(f"--tag {raw!r} 必须是 key:value 形式")
        key, _, value = pair.partition(":")
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError(f"--tag {raw!r} 的 key/value 不能为空")
        if key in key_values and key_values[key] != value:
            raise ValueError(f"--tag key {key!r} 重复且值冲突: {key_values[key]!r} vs {value!r}")
        key_values[key] = value
        normalized = f"{key}:{value}"
        if normalized in seen_pairs:
            continue
        pairs.append(normalized)
        seen_pairs.add(normalized)
    return pairs or None


def _merge_tag_forms(
    tags: Optional[list[str]], tag_pairs: Optional[list[str]]
) -> Optional[list[str]]:
    """把 ``--tag`` 解析出的 key:value 并入 ``--tags`` 解析结果。

    ``--tags`` 内部不做同 key 冲突检测（逗号串为历史自由格式），所以跨通道
    的同 key 不同 value 必须在这里拒绝，否则两个值会静默共存；冲突判定与
    ``_parse_tag_pairs`` / ``_merge_meta_tags`` 同口径（空值 tag 视为未声明）。
    完全相同项去重。
    """
    base = [str(t).strip() for t in (tags or [])]
    if not tag_pairs:
        return base or None
    base_values: dict[str, str] = {}
    for raw in base:
        key, separator, value = raw.partition(":")
        if separator and key.strip() and value.strip():
            base_values[key.strip()] = value.strip()
    for pair in tag_pairs:
        key, _, value = pair.partition(":")
        key = key.strip()
        base_value = base_values.get(key)
        if base_value is not None and base_value != value.strip():
            raise ValueError(
                f"--tag {key}:{value} 与 --tags 中的 {key}:{base_value} 冲突，请只保留一种"
            )
    return base + [p for p in tag_pairs if p not in base] or None


def _idempotency_item_key(
    *,
    template: str,
    params: dict,
    global_index: int,
    overrides: Optional[dict],
    agenthub_revision: Optional[str],
    enable_otel_tracing: Optional[bool],
    runner: Optional[str],
    runner_options: Optional[dict],
    model_base_url_collection: Optional[list],
    queue: Optional[str],
    account_pool: Optional[str],
    resource_profile_id: Optional[str] = None,
    max_failure_retries: int = 0,
    ak_id: Optional[str] = None,
    ak_mode: str = "auto",
) -> str:
    # Client-supplied item keys are authoritative; server hashing is only a
    # fallback for non-CLI callers, so this payload intentionally need not
    # match the server-side fallback payload exactly.
    payload_data = {
        "template": template,
        "params": params,
        "idempotency_metadata": {"global_index": global_index},
        "overrides": overrides,
        "agenthub_revision": agenthub_revision,
        "runner": runner,
        "runner_options": runner_options,
        "model_base_url_collection": model_base_url_collection,
        "enable_otel_tracing": enable_otel_tracing,
        "queue": queue,
        "account_pool": account_pool,
    }
    if ak_id is not None:
        payload_data["ak_id"] = ak_id
    if ak_mode != "auto":
        payload_data["ak_mode"] = ak_mode
    if resource_profile_id is not None:
        payload_data["resource_profile_id"] = resource_profile_id
    if max_failure_retries:
        payload_data["max_failure_retries"] = max_failure_retries
    payload = json.dumps(
        payload_data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _runtime_job_tags() -> list[str]:
    if not (os.getenv("DLC_JOB_ID", "").strip() or os.getenv("DSW_INSTANCE_ID", "").strip()):
        return []

    tags: list[str] = []
    for env_name, tag_name in _PAI_RUNTIME_ENV_TAGS:
        value = os.getenv(env_name, "").strip()
        if value:
            tags.append(f"{tag_name}:{value}")
    return tags


_DEFAULT_JOB_LIST_COLUMNS = [
    "job_id",
    "status",
    "template",
    "instance_id",
    "queue_id",
    "quota",
    "resource_mode",
    "user",
    "error_code",
    "created_at",
    "finished_at",
]

_JOB_LIST_AVAILABLE_COLUMNS = [
    *_DEFAULT_JOB_LIST_COLUMNS,
    "transparency",
    "can_read_content",
    "job_name",
    "group_id",
    "quota_id",
    "quota_name",
    "concurrency_policy_id",
    "region",
    "spec",
    "priority",
    "priority_weight",
    "runner",
    "job_type",
    "tags",
    "failed_reason",
    "user_id",
    "user_name",
    "user_realname",
    "agenthub_revision",
    "template_commit",
    "attempt",
    "retried_at",
    "retried_by",
    "pod_uid",
    "pod_name",
    "k8s_namespace",
    "model_base_url",
    "queued_at",
    "submitted_at",
    "k8s_start_time",
    "k8s_ready_time",
    "k8s_completion_time",
    "updated_at",
    "db_duration",
    "idempotency_key",
    "idempotency_item_key",
    "submission_id",
    "conditions",
    "checkpoint",
    "benchmark",
    "experiment",
]

_JOB_LIST_AVAILABLE_COLUMNS = list(dict.fromkeys(_JOB_LIST_AVAILABLE_COLUMNS))
_JOB_LIST_COLUMNS_HELP = "Comma-separated columns for plain output. Supported: " + ", ".join(
    _JOB_LIST_AVAILABLE_COLUMNS
)


def _parse_columns_option(
    columns: Optional[str], *, available: Optional[list[str]] = None
) -> list[str] | None:
    if columns is None:
        return None
    available = _JOB_LIST_AVAILABLE_COLUMNS if available is None else available
    parsed = [item.strip() for item in columns.split(",") if item.strip()]
    if not parsed:
        raise typer.BadParameter("--columns must include at least one column")
    unsupported = [column for column in parsed if column not in available]
    if unsupported:
        raise typer.BadParameter(
            "unsupported --columns: "
            + ", ".join(unsupported)
            + ". Supported columns: "
            + ", ".join(available)
        )
    return parsed


def _prepare_job_list_rows(jobs: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for job in jobs:
        row = dict(job)
        if isinstance(row.get("tags"), list):
            row["tags"] = ",".join(str(tag) for tag in row["tags"])
        row["quota"] = row.get("quota_name") or row.get("quota_id") or "-"
        row["user"] = row.get("user_realname") or row.get("user_name") or row.get("user_id")
        row["error_code"] = row.get("error_code") or "-"
        row["finished_at"] = row.get("finished_at") or "-"
        rows.append(row)
    return rows


def _terminal_width(default: int = 120) -> int:
    """Best-effort terminal width (respects COLUMNS env; falls back when piped)."""
    import shutil

    return shutil.get_terminal_size(fallback=(default, 24)).columns


def _fit_columns_to_width(
    rows: list[dict],
    priority: list[str],
    min_columns: int,
    width: int,
    sep: int = 3,
) -> list[str]:
    """Pick as many priority columns as fit ``width`` (East-Asian width aware).

    The first ``min_columns`` are always kept; remaining columns are added in
    priority order until the next one would overflow the terminal width. ``sep`` is
    the per-gap cell cost of the rich ``SIMPLE_HEAD`` table (1 separator + 2 padding),
    so the estimate matches what ``_print_rich_table`` actually renders.
    """
    from rich.cells import cell_len

    selected: list[str] = []
    used = 0
    for key in priority:
        col_width = cell_len(key)
        for row in rows:
            col_width = max(col_width, cell_len(_stringify_cell(row.get(key))))
        needed = col_width + (sep if selected else 0)
        if len(selected) < min_columns or used + needed <= width:
            selected.append(key)
            used += needed
        else:
            break
    return selected


# Column priority for AP_FORMAT=table job listings; width-adaptive selection keeps
# the core columns and adds the rest as the terminal gets wider.
_JOB_LIST_TABLE_PRIORITY = [
    "job_id",
    "status",
    "template",
    "instance_id",
    "user",
    "created_at",
    "finished_at",
    "error_code",
    "queue_id",
    "quota",
    "resource_mode",
]
_JOB_LIST_TABLE_MIN_COLUMNS = 4


def _print_job_list_plain(
    result: dict,
    columns: Optional[list[str]] = None,
    rich: bool = False,
    *,
    default_columns: Optional[list[str]] = None,
    table_priority: Optional[list[str]] = None,
    table_min_columns: Optional[int] = None,
) -> None:
    jobs = result.get("jobs", [])
    rows = _prepare_job_list_rows(jobs)
    default_columns = _DEFAULT_JOB_LIST_COLUMNS if default_columns is None else default_columns
    table_priority = _JOB_LIST_TABLE_PRIORITY if table_priority is None else table_priority
    table_min_columns = (
        _JOB_LIST_TABLE_MIN_COLUMNS if table_min_columns is None else table_min_columns
    )
    if columns:
        selected_columns = columns
    elif rich:
        selected_columns = _fit_columns_to_width(
            rows, table_priority, table_min_columns, _terminal_width() - 1
        )
    else:
        selected_columns = default_columns
    _print_content_notice(rows)
    selected_columns = _content_columns(rows, selected_columns)
    render = _print_rich_table if rich else _print_plain_table
    render(
        rows,
        [(column, column) for column in selected_columns],
    )


_JOB_LIST_SORT_FIELDS = {
    "created_at": "created_at_sort",
    "finished_at": "finished_at_sort",
    "duration": "duration_sort",
}


def _job_list_sort_kwargs(sort: Optional[str], asc: bool, desc: bool) -> dict[str, Optional[bool]]:
    if asc and desc:
        raise typer.BadParameter("--asc and --desc cannot be used together")
    if not sort:
        if asc or desc:
            raise typer.BadParameter("--asc/--desc require --sort")
        return {}

    sort_key = sort.strip().lower().replace("-", "_")
    param_name = _JOB_LIST_SORT_FIELDS.get(sort_key)
    if param_name is None:
        raise typer.BadParameter("--sort must be one of created_at/finished_at/duration")

    return {param_name: bool(asc)}


_DEFAULT_GROUP_LIST_COLUMNS = [
    "group_id",
    "name",
    "status",
    "queue_id",
    "max_concurrency",
    "user",
    "created_at",
    "finished_at",
]

_GROUP_LIST_TABLE_PRIORITY = [
    "group_id",
    "name",
    "status",
    "user",
    "created_at",
    "finished_at",
    "queue_id",
    "max_concurrency",
]
_GROUP_LIST_TABLE_MIN_COLUMNS = 3

_GROUP_LIST_AVAILABLE_COLUMNS = [
    *_DEFAULT_GROUP_LIST_COLUMNS,
    "transparency",
    "can_read_content",
    "template",
    "scheduling_status",
    "profile",
    "dataset",
    "model",
    "scaffold",
    "updated_at",
    "paused_at",
    "paused_by",
    "user_id",
    "user_name",
    "user_realname",
    "profile_id",
    "profile_version",
    "strict",
    "k8s_namespace",
    "agenthub_revision",
    "template_commit",
    "group_post_process",
    "group_post_process_job_id",
    "group_post_process_triggered_at",
    "eval_config",
    "model_base_url_collection",
    "submission_context",
    "meta_model",
    "meta_job_type",
    "meta_train_stage",
    "meta_teacher_direction",
    "upstream_platform",
    "upstream_job_id",
    "tags",
    "checkpoint",
    "benchmark",
    "experiment",
]

_GROUP_LIST_AVAILABLE_COLUMNS = list(dict.fromkeys(_GROUP_LIST_AVAILABLE_COLUMNS))
_GROUP_LIST_COLUMNS_HELP = "Comma-separated columns for plain output. Supported: " + ", ".join(
    _GROUP_LIST_AVAILABLE_COLUMNS
)


def _parse_group_columns_option(columns: Optional[str]) -> list[str] | None:
    if columns is None:
        return None
    parsed = [item.strip() for item in columns.split(",") if item.strip()]
    if not parsed:
        raise typer.BadParameter("--columns must include at least one column")
    unsupported = [column for column in parsed if column not in _GROUP_LIST_AVAILABLE_COLUMNS]
    if unsupported:
        raise typer.BadParameter(
            "unsupported --columns: "
            + ", ".join(unsupported)
            + ". Supported columns: "
            + ", ".join(_GROUP_LIST_AVAILABLE_COLUMNS)
        )
    return parsed


def _format_group_profile(group: dict) -> str:
    profile_id = group.get("profile_id")
    profile_version = group.get("profile_version")
    if profile_id and profile_version is not None:
        return f"{profile_id}:v{profile_version}"
    return profile_id or "-"


def _prepare_group_list_rows(groups: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for group in groups:
        row = dict(group)
        row["status"] = row.get("scheduling_status") or "-"
        row["user"] = row.get("user_realname") or row.get("user_name") or row.get("user_id") or "-"
        row["profile"] = _format_group_profile(row)
        for key in (
            "dataset",
            "model",
            "scaffold",
            "finished_at",
            "paused_at",
            "paused_by",
            "meta_model",
            "meta_job_type",
            "meta_train_stage",
            "meta_teacher_direction",
            "upstream_platform",
            "upstream_job_id",
        ):
            if key not in row.get("restricted_fields", []):
                row[key] = row.get(key) or "-"
        rows.append(row)
    return rows


def _print_group_list_plain(
    result: dict, columns: Optional[list[str]] = None, rich: bool = False
) -> None:
    rows = _prepare_group_list_rows(result.get("groups", []))
    if columns:
        selected_columns = columns
    elif rich:
        selected_columns = _fit_columns_to_width(
            rows, _GROUP_LIST_TABLE_PRIORITY, _GROUP_LIST_TABLE_MIN_COLUMNS, _terminal_width() - 1
        )
    else:
        selected_columns = _DEFAULT_GROUP_LIST_COLUMNS
    _print_content_notice(rows)
    selected_columns = _content_columns(rows, selected_columns)
    render = _print_rich_table if rich else _print_plain_table
    render(
        rows,
        [(column, column) for column in selected_columns],
    )


def _print_group_action_plain(title: str, result: dict, group_id: str, fields: list[str]) -> None:
    print(f"[green]{title}:[/] {result.get('group_id') or group_id}")
    _print_key_values([(field, result.get(field)) for field in fields])


def _print_datasource_list_plain(result: dict) -> None:
    _print_plain_table(
        result.get("datasources", []),
        [
            ("datasource_id", "datasource_id"),
            ("name", "name"),
            ("type", "type"),
            ("uri", "uri"),
            ("access_mode", "access_mode"),
            ("mount_path", "mount_path"),
            ("created_at", "created_at"),
        ],
    )


def _pick_available_columns(
    rows: list[dict], candidates: list[tuple[str, str]]
) -> list[tuple[str, str]]:
    return [col for col in candidates if any(col[0] in row for row in rows)]


def _print_group_eval_plain(result: dict) -> None:
    _print_content_notice([result])
    header_parts: list[str] = []
    for key in ("group_id", "name"):
        if key in result:
            header_parts.append(f"{key}={_stringify_cell(result.get(key))}")
    if header_parts:
        typer.echo("  ".join(header_parts))

    summary = result.get("summary", {})
    raw_post_process_metrics = result.get("group_post_process_metrics", {})
    post_process_metrics = (
        raw_post_process_metrics if isinstance(raw_post_process_metrics, dict) else {}
    )
    has_summary = isinstance(summary, dict) and bool(summary)
    if has_summary:
        pass_keys = sorted(
            k for k in summary.keys() if k.startswith("pass@") or k.startswith("pass^")
        )
        summary_columns = _pick_available_columns(
            [summary],
            [
                ("total_tasks", "total_tasks"),
                ("completed_tasks", "completed_tasks"),
                ("total_trials", "total_trials"),
                ("total_failed_trials", "total_failed_trials"),
                ("scored_tasks", "scored_tasks"),
                ("passed_tasks", "passed_tasks"),
                ("avg_score", "avg_score"),
                ("pass_rate", "pass_rate"),
                ("avg_completion", "avg_completion"),
                ("avg_robustness", "avg_robustness"),
                ("avg_safety", "avg_safety"),
                *[(key, key) for key in pass_keys],
            ],
        )
        if summary_columns:
            marked_columns = [
                (key, f"{title} [Group PostProcess]" if key in post_process_metrics else title)
                for key, title in summary_columns
            ]
            _print_plain_table([summary], marked_columns)

        displayed_keys = {key for key, _title in summary_columns}
        custom_metric_rows = [
            {
                "metric": key,
                "value": _format_metric_value(value),
                "source": (
                    "Group PostProcess" if key in post_process_metrics else "Eval Aggregation"
                ),
            }
            for key, value in summary.items()
            if key not in displayed_keys
        ]
        if custom_metric_rows:
            if summary_columns:
                typer.echo("")
            typer.echo("Custom Metrics")
            _print_plain_table(
                custom_metric_rows,
                [("metric", "metric"), ("value", "value"), ("source", "source")],
            )

    raw_rows = result.get("per_task", [])
    rows = [row for row in raw_rows if isinstance(row, dict)] if isinstance(raw_rows, list) else []
    if has_summary and rows:
        typer.echo("")
    if not rows:
        return

    columns = _pick_available_columns(
        rows,
        [
            ("task_id", "task_id"),
            ("job_ids", "job_ids"),
            ("trials", "trials"),
            ("scored", "scored"),
            ("avg_score", "avg_score"),
            ("passed", "passed"),
            ("pass_rate", "pass_rate"),
            ("completion", "completion"),
            ("robustness", "robustness"),
            ("communication", "communication"),
            ("safety", "safety"),
            ("category", "category"),
            ("difficulty", "difficulty"),
            ("total_tokens", "total_tokens"),
            ("input_tokens", "input_tokens"),
            ("output_tokens", "output_tokens"),
            ("total_turns", "total_turns"),
            ("wall_time_s", "wall_time_s"),
            ("model_time_s", "model_time_s"),
        ],
    )
    if not columns:
        _print_json({"results": rows})
        return
    _print_plain_table(rows, columns)


def _format_metric_value(value: object) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return _stringify_cell(value)


def _print_job_events_plain(result: dict) -> None:
    if "containers" in result:
        for cname, events in result["containers"].items():
            print(f"\n[{cname}]")
            for event in events:
                print(event)
        return
    for event in result.get("events", []):
        print(event)


def _print_job_retry_plain(result: dict) -> None:
    print("[green]Job retried:[/]")
    print(f"  job_id: {result.get('job_id')}")
    print(f"  status: {result.get('status')}")
    if result.get("attempt") is not None:
        print(f"  attempt: {result.get('attempt')}")
    if result.get("previous_status"):
        print(f"  previous_status: {result.get('previous_status')}")
    if result.get("retried_at"):
        print(f"  retried_at: {result.get('retried_at')}")


def _print_job_cancel_plain(result: dict) -> None:
    print(f"[green]Cancelled:[/] {result.get('job_id')}")
    print(f"  status: {result.get('status')}")
    if result.get("failed_reason"):
        print(f"  failed_reason: {result.get('failed_reason')}")


def _mask_config_secret(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 8:
        return value[:1] + "..." + value[-1:]
    if len(value) <= 16:
        return value[:4] + "..." + value[-4:]
    return value[:8] + "..." + value[-4:]


def _build_secret_data(
    data: Optional[str],
    from_file: Optional[list[str]],
    output_format: str,
) -> dict:
    """Merge ``--data`` JSON and ``--from-file`` entries into one secret data dict.

    Shared by ``secret create`` and ``secret update`` so both accept exactly the same
    inputs and produce the same shape: string values are env vars, files become
    ``{content, filename}`` objects. ``--from-file`` is applied after ``--data`` and
    warns when it overwrites a key that was also given inline.
    """
    data_dict: dict = {}
    if data is not None:
        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"--data must be valid JSON: {exc}") from exc
        if not isinstance(data_dict, dict):
            raise typer.BadParameter("--data must be a JSON object")

    for raw in from_file or []:
        key, path = _parse_secret_from_file(raw)
        if not key:
            key = path.name
        try:
            content = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise typer.BadParameter(f"--from-file file not found: {path}") from exc
        except UnicodeDecodeError as exc:
            # Secret data is stored as text, so a binary keystore cannot round-trip.
            # UnicodeDecodeError is a ValueError, not an OSError — without this branch
            # rotating a .p12/.pfx/.der would exit with a bare traceback.
            raise typer.BadParameter(
                f"--from-file file is not valid UTF-8 text (binary formats such as "
                f".p12/.pfx/.der are not supported): {path}"
            ) from exc
        except OSError as exc:
            raise typer.BadParameter(f"--from-file failed to read {path}: {exc}") from exc
        if key in data_dict:
            _emit_info(
                f"warning: --from-file overwrites existing data key '{key}'",
                output_format,
            )
        data_dict[key] = {"content": content, "filename": path.name}

    return data_dict


def _parse_secret_from_file(raw: str) -> tuple[str, Path]:
    """Parse a --from-file value into (key, file_path).

    Supports two forms:
      - ``<path>`` → key is the file name, value is the file content.
      - ``<key>=<path>`` → key is explicit, value is the file content.
    """
    raw = raw.strip()
    if not raw:
        raise typer.BadParameter("--from-file value must not be empty")
    if "=" in raw:
        key, path_str = raw.split("=", 1)
        key = key.strip()
        path_str = path_str.strip()
        if not key:
            raise typer.BadParameter(
                "--from-file key must not be empty (expected key=path or path)"
            )
    else:
        key = ""
        path_str = raw
    if not path_str:
        raise typer.BadParameter("--from-file path must not be empty")
    return key, Path(path_str)


def _mask_config_headers(headers: dict) -> dict:
    masked = {}
    for key, value in headers.items():
        lower = key.lower()
        if any(
            token in lower for token in ("authorization", "token", "api-key", "cookie", "secret")
        ):
            masked[key] = "***"
        else:
            masked[key] = value
    return masked


def _extract_cluster(headers: dict) -> str | None:
    for key, value in headers.items():
        if key.lower() == "x-cluster":
            return value
    return None


def _effective_cluster(config=None) -> str | None:
    """Resolve the effective cluster: --cluster > AP_CLUSTER > AP_HEADERS X-Cluster."""
    if config is None:
        from ap_client import api as _api

        config = get_config(verbose=_api._verbose_override, cluster=_api._cluster_override)
    return _extract_cluster(config.headers) or os.environ.get("AP_CLUSTER", "").strip() or None


def _config_payload(show_secrets: bool = False) -> dict:
    from ap_client import api as _api

    config = get_config(verbose=_api._verbose_override, cluster=_api._cluster_override)
    ap_cluster = _effective_cluster(config)
    _, read_timeout = _api._default_timeout()
    return {
        "base_url": config.base_url,
        "ap_cluster": ap_cluster,
        "agenthub_ref": config.agenthub_ref,
        "ap_verbose": config.verbose,
        "ap_verbose_full_body": config.verbose_full_body,
        "ap_http_max_attempts": config.http_max_attempts,
        "api_key": config.token_key if show_secrets else _mask_config_secret(config.token_key),
        "headers": config.headers if show_secrets else _mask_config_headers(config.headers),
        "timeout": _fmt_timeout(read_timeout),
    }


def _parse_headers_env_value(raw: str) -> dict:
    headers = {}
    for item in raw.split(","):
        if ":" not in item:
            continue
        key, value = item.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers


def _env_value_for_display(name: str, raw: str, *, show_secrets: bool) -> str:
    if name == "AP_HEADERS":
        headers = _parse_headers_env_value(raw)
        if not show_secrets:
            headers = _mask_config_headers(headers)
        return json.dumps(headers, ensure_ascii=False, separators=(",", ":"))
    if name == "AP_API_KEY" and not show_secrets:
        return _mask_config_secret(raw) or ""
    return raw


def _env_var_rows(*, show_secrets: bool = False, only_set: bool = False) -> list[dict]:
    rows: list[dict] = []
    for spec in ENV_VAR_SPECS:
        is_set = spec.name in os.environ
        if only_set and not is_set:
            continue
        raw_value = os.environ.get(spec.name)
        value = (
            _env_value_for_display(spec.name, raw_value, show_secrets=show_secrets)
            if raw_value is not None
            else None
        )
        rows.append(
            {
                "name": spec.name,
                "category": spec.category,
                "value": value,
                "default": spec.default,
                "required": spec.required,
                "secret": spec.secret,
                "legacy": spec.legacy,
                "overridden_by": list(spec.overridden_by),
                "description": spec.description,
            }
        )
    return rows


@app.command("whoami")
def auth_whoami():
    """Show current authentication information."""
    config = get_config()
    if config.token_key:
        print("Authentication: API Key")
        print(f"Key:      {_mask_config_secret(config.token_key)}")
    else:
        print("Not authenticated (no AP_API_KEY / AP_API_KEYS / AP_TOKEN_KEY environment variable)")


def _list_all_group_jobs(client, group_id: str, page_size: int = 500) -> list[dict]:
    """Fetch all jobs in a group with pagination.

    Stop when either:
    1. The current page is empty.
    2. The fetched job count reaches the server-reported total.
    """
    jobs: list[dict] = []
    skip = 0
    total = None

    while True:
        page = client.list_jobs(group_id=group_id, skip=skip, limit=page_size)
        page_jobs = page.get("jobs", [])

        # Capture total on the first request.
        if total is None:
            total = page.get("total", 0)

        # Stop when the current page is empty.
        if not page_jobs:
            break

        jobs.extend(page_jobs)
        skip += len(page_jobs)

        # Stop when all server-reported jobs have been fetched.
        if total is not None and skip >= total:
            break

    return jobs


@config_app.callback(invoke_without_command=True)
def show_config(
    ctx: typer.Context,
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
    show_secrets: bool = typer.Option(
        False,
        "--show-secrets",
        help="Print unmasked secret values, including API key and sensitive headers",
    ),
):
    """Show the current CLI configuration."""
    if ctx.invoked_subcommand is not None:
        return
    output_format = _normalize_output_format(output_format)
    payload = _config_payload(show_secrets=show_secrets)
    if output_format == "plain":
        rows = [
            {"key": "base_url", "value": payload["base_url"]},
            {"key": "ap_cluster", "value": payload["ap_cluster"]},
            {"key": "agenthub_ref", "value": payload["agenthub_ref"]},
            {"key": "api_key", "value": payload["api_key"]},
            {"key": "ap_verbose", "value": str(payload["ap_verbose"]).lower()},
            {"key": "ap_verbose_full_body", "value": str(payload["ap_verbose_full_body"]).lower()},
            {"key": "headers", "value": json.dumps(payload["headers"], ensure_ascii=False)},
            {"key": "timeout", "value": payload["timeout"]},
        ]
        _print_plain_table(rows, [("key", "key"), ("value", "value")])
        return
    _print_formatted(payload, output_format)


@config_app.command("env")
def config_env(
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
    only_set: bool = typer.Option(
        False,
        "--only-set",
        help="Only show environment variables currently set in this process",
    ),
    show_secrets: bool = typer.Option(
        False,
        "--show-secrets",
        help="Print unmasked secret environment values",
    ),
):
    """List supported environment variables."""
    output_format = _normalize_output_format(output_format)
    rows = _env_var_rows(show_secrets=show_secrets, only_set=only_set)
    if output_format == "plain":
        _print_plain_table(
            rows,
            [
                ("name", "name"),
                ("value", "value"),
                ("default", "default"),
                ("required", "required"),
                ("description", "description"),
            ],
        )
        return
    _print_formatted({"env": rows}, output_format)


# ==================== Template operations ====================


@template_app.command("list")
def template_list(
    agenthub_ref: Optional[str] = typer.Option(
        None, "--agenthub-ref", help="Agent-Hub branch/commit; overrides AP_AGENTHUB_REF"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List all templates."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client(agenthub_ref=agenthub_ref)
    templates = client.list_templates()
    if output_format == "table":
        _print_template_list_plain(templates)
    else:
        _print_formatted(templates, output_format)


@template_app.command("get")
def template_get(
    name: str = typer.Argument(..., help="Template name"),
    agenthub_ref: Optional[str] = typer.Option(
        None, "--agenthub-ref", help="Agent-Hub branch/commit; overrides AP_AGENTHUB_REF"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show template details."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client(agenthub_ref=agenthub_ref)
    template = client.get_template(name)
    if output_format == "table":
        _print_template_get_plain(template)
    else:
        _print_formatted(template, output_format)


@template_app.command("render")
def template_render(
    name: str = typer.Argument(..., help="Template name"),
    params: str = typer.Argument(..., help="Parameters (JSON)"),
    agenthub_ref: Optional[str] = typer.Option(
        None, "--agenthub-ref", help="Agent-Hub branch/commit; overrides AP_AGENTHUB_REF"
    ),
):
    """Preview template rendering result (without submitting)."""
    client = get_client(agenthub_ref=agenthub_ref)
    params_dict = json.loads(params)
    result = client.render_template(name, params_dict)
    print(f"Image:      {result.get('image')}")
    print(f"Resources:  {result.get('resources')}")
    print(f"Script:     {result.get('script_length')} chars")
    if result.get("sidecars"):
        print(f"Sidecars:   {', '.join(s['name'] for s in result['sidecars'])}")
    if result.get("env"):
        print(f"\nEnv ({len(result['env'])} vars):")
        for k, v in sorted(result["env"].items()):
            val = str(v)
            if len(val) > 60:
                val = val[:57] + "..."
            print(f"  {k}={val}")


@template_app.command("fetch")
def template_fetch(
    agenthub_ref: Optional[str] = typer.Option(
        None, "--agenthub-ref", help="Agent-Hub branch/commit; overrides AP_AGENTHUB_REF"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Fetch the Agent-Hub repo and show the resolved ref + commit."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client(agenthub_ref=agenthub_ref)
    result = client.fetch_repo()
    if output_format == "table":
        _print_detail(result)
    else:
        _print_formatted(result, output_format)


# ==================== Dataset operations ====================

# 设计 §6 / 上游 §13.2:`ap dataset versions` 与 `ap dataset instances` 行为保持不变
# (仍打 ossdata 路由,`ap job create` 的配套流程依赖它们),只追加固定弃用文案。
# 文案**只写 stderr**——JSON/YAML 的 stdout 必须仍可被 json.loads 直接消费。
_DATASET_VERSIONS_DEPRECATION = (
    "Warning: `ap dataset versions` is deprecated.\n"
    "Use `ap dataset version list --dataset <dataset>` instead."
)
_DATASET_INSTANCES_DEPRECATION = (
    "Warning: `ap dataset instances` is deprecated.\n"
    "Use `ap instance list --dataset <dataset> --split <split> [--version <version>]` instead."
)


@dataset_app.command("versions")
def dataset_versions(
    dataset: str = typer.Argument(..., help="Dataset name"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List dataset versions (deprecated: use 'ap dataset version list')."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    _emit_progress(_DATASET_VERSIONS_DEPRECATION)
    client = get_client()
    versions = client.list_dataset_versions(dataset)
    if output_format == "table":
        _print_records_table(versions)
    else:
        _print_formatted(versions, output_format)


@dataset_app.command("instances")
def dataset_instances(
    dataset_version: str = typer.Argument(
        ..., help="Dataset version path (e.g. qclawbench/skill/V0329-tasks)"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List dataset instances (deprecated: use 'ap instance list')."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    _emit_progress(_DATASET_INSTANCES_DEPRECATION)
    client = get_client()
    result = client.list_all_dataset_instances(dataset_version)
    if output_format == "table":
        _print_records_table(result)
    else:
        _print_formatted(result, output_format)


# ==================== Job operations ====================


def _tbb_create_job(
    client,
    *,
    command: str,
    config: Path,
    runtime_timeout: Optional[int],
    tag: Optional[list[str]],
    overrides: Optional[dict],
    queue_id: Optional[str],
    quota_id: Optional[str],
    concurrency_policy_id: Optional[str],
    datasources: Optional[list],
    priority: Optional[str],
    priority_weight: Optional[int],
    resource_mode: Optional[str],
) -> dict:
    params = tbb.build_tbb_params(
        tbb.read_pipeline_config(config),
        command,
        runtime_timeout_sec=runtime_timeout,
    )
    return client.create_job(
        template=tbb.TBB_TEMPLATE,
        params=params,
        tags=_merge_job_tags(tbb.merge_tbb_tags(command, tag)),
        overrides=overrides,
        queue_id=queue_id,
        quota_id=quota_id,
        policy_id=concurrency_policy_id,
        datasources=datasources,
        idempotency_key=str(uuid.uuid4()),
        priority=priority,
        priority_weight=priority_weight,
        resource_mode=resource_mode,
    )


def _tbb_job_from_submission(submission: dict) -> dict:
    if not isinstance(submission, dict):
        raise tbb.TBBProtocolError("TBB submission must be an object")
    jobs = submission.get("jobs")
    if not isinstance(jobs, list) or len(jobs) != 1 or not isinstance(jobs[0], dict):
        raise tbb.TBBProtocolError("TBB submission must return exactly one job")
    job = jobs[0]
    if not job.get("job_id"):
        raise tbb.TBBProtocolError("TBB submission did not return a job_id")
    return job


def _print_tbb_submission(job: dict, output_format: str) -> None:
    payload = {"job_id": job.get("job_id"), "status": job.get("status")}
    if output_format == "plain":
        typer.echo("Job submitted:")
        typer.echo(f"  job_id: {payload['job_id']}")
        typer.echo(f"  status: {payload['status']}")
    elif output_format == "table":
        _print_rich_table([payload], [("job_id", "job_id"), ("status", "status")])
    else:
        _print_formatted(payload, output_format)


def _print_tbb_status(job: dict, metrics: Optional[dict], output_format: str) -> None:
    if output_format in {"json", "yaml"}:
        _print_formatted(tbb.build_status_payload(job, metrics), output_format)
        return
    row = tbb.build_status_row(job, metrics)
    columns = [
        "job_id",
        "job_status",
        "pipeline_status",
        "duration_sec",
        "task_total",
        "failure_count",
    ]
    render = _print_rich_table if output_format == "table" else _print_plain_table
    render([row], [(column, column) for column in columns])


def _wait_for_tbb_result(
    client,
    job: dict,
    *,
    command: str,
    wait_interval: float,
    wait_timeout: Optional[float],
    output_format: str,
) -> None:
    try:
        final_job = wait_for_job(
            client,
            job["job_id"],
            wait_interval,
            timeout=wait_timeout,
            printer=lambda message: typer.echo(message, err=True),
        )
    except WaitTimeoutError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1)

    try:
        metrics_response = client.get_job_metrics(job["job_id"])
        if not isinstance(metrics_response, dict):
            raise tbb.TBBProtocolError("TBB metrics response must be an object")
        metrics = tbb.extract_tbb_metrics(metrics_response, command)
    except tbb.TBBProtocolError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)
    if metrics is None:
        if output_format in {"json", "yaml"}:
            _print_tbb_status(final_job, None, output_format)
        else:
            _emit_error("TBB job finished without eval metrics")
        raise typer.Exit(1)

    _print_tbb_status(final_job, metrics, output_format)
    if final_job.get("status") != "Succeeded" or not tbb.tbb_result_succeeded(metrics, command):
        raise typer.Exit(1)


@job_tbb_app.command("validate-config")
def job_tbb_validate_config(
    config: Path = typer.Option(..., "--config", help="Pipeline config file"),
    runtime_timeout: Optional[int] = typer.Option(
        None,
        "--runtime-timeout",
        min=0,
        help="Pipeline runtime timeout in seconds",
    ),
    agenthub_ref: Optional[str] = typer.Option(
        None, "--agenthub-ref", help="Agent-Hub branch/commit; overrides AP_AGENTHUB_REF"
    ),
    queue_id: Optional[str] = typer.Option(None, "--queue-id", help="Queue ID"),
    quota_id: Optional[str] = typer.Option(None, "--quota-id", help="Quota ID"),
    concurrency_policy_id: Optional[str] = typer.Option(
        None, "--concurrency-policy-id", help="Concurrency resource ID"
    ),
    datasources: Optional[str] = typer.Option(
        None,
        "--datasources",
        help="DataSources as JSON array or comma-separated IDs",
    ),
    overrides: Optional[str] = typer.Option(
        None, "--overrides", help="Override config (JSON object)"
    ),
    tag: Optional[list[str]] = typer.Option(None, "--tag", help="Job tag (repeatable)"),
    priority: Optional[str] = typer.Option(None, "--priority", help="Scheduling priority tier"),
    priority_weight: Optional[int] = typer.Option(
        None, "--priority-weight", help="Fine-grained scheduling priority weight"
    ),
    resource_mode: Optional[str] = typer.Option(
        None, "--resource-mode", help="Resource scheduling mode"
    ),
    wait_interval: float = typer.Option(
        5.0,
        "--wait-interval",
        min=0.1,
        help="Polling interval in seconds",
    ),
    wait_timeout: Optional[float] = typer.Option(
        None,
        "--wait-timeout",
        min=0.0,
        help="Maximum seconds to wait; omit to wait indefinitely",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
) -> None:
    """Submit one TrajBigBang config validation job and wait for completion."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client(agenthub_ref=agenthub_ref)
    try:
        submission = _tbb_create_job(
            client,
            command="validate-config",
            config=config,
            runtime_timeout=runtime_timeout,
            tag=tag,
            overrides=_parse_json_object(overrides, "--overrides"),
            queue_id=queue_id,
            quota_id=quota_id,
            concurrency_policy_id=concurrency_policy_id,
            datasources=_parse_datasources_option(datasources),
            priority=priority,
            priority_weight=priority_weight,
            resource_mode=resource_mode,
        )
        job = _tbb_job_from_submission(submission)
    except tbb.TBBProtocolError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)

    _wait_for_tbb_result(
        client,
        job,
        command="validate-config",
        wait_interval=wait_interval,
        wait_timeout=wait_timeout,
        output_format=output_format,
    )


@job_tbb_app.command("status")
def job_tbb_status(
    job_id: str = typer.Argument(..., help="TBB run job ID"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
) -> None:
    """Show the current status of a TrajBigBang run job."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client()
    try:
        job = client.get_job(job_id, include_params=True)
        if not isinstance(job, dict):
            raise tbb.TBBProtocolError("TBB job response must be an object")
        tbb.parse_job_request(job, "run")
        metrics_response = client.get_job_metrics(job_id)
        if not isinstance(metrics_response, dict):
            raise tbb.TBBProtocolError("TBB metrics response must be an object")
        metrics = tbb.extract_tbb_metrics(metrics_response, "run")
    except tbb.TBBProtocolError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)

    _print_tbb_status(job, metrics, output_format)


_TBB_JOB_LIST_EXCLUDED_COLUMNS = {"template", "instance_id", "quota", "resource_mode"}
_TBB_JOB_LIST_DEFAULT_COLUMNS = [
    column for column in _DEFAULT_JOB_LIST_COLUMNS if column not in _TBB_JOB_LIST_EXCLUDED_COLUMNS
]
_TBB_JOB_LIST_TABLE_PRIORITY = [
    column for column in _JOB_LIST_TABLE_PRIORITY if column in _TBB_JOB_LIST_DEFAULT_COLUMNS
]
_TBB_JOB_LIST_TABLE_MIN_COLUMNS = 4
_TBB_JOB_STATUS_HELP = (
    "AP job lifecycle status: Queued, Pending, Running, Succeeded, Failed, Cancelled, Unknown"
)
_TBB_ISO_TIME_HELP = "ISO timestamp, e.g. 2026-03-26T00:00:00 or 2026-03-26T00:00:00+08:00"
_TBB_JOB_LIST_COLUMNS_HELP = "Comma-separated output columns. Supported: " + ", ".join(
    _JOB_LIST_AVAILABLE_COLUMNS
)


@job_tbb_app.command("list")
def job_tbb_list(
    status: Optional[str] = typer.Option(None, "--status", help=_TBB_JOB_STATUS_HELP),
    job_id: Optional[str] = typer.Option(None, "--job-id", help="Job ID"),
    user_id: Optional[str] = typer.Option(None, "--user-id", help="User ID"),
    user_name: Optional[str] = typer.Option(None, "--user-name", help="Username"),
    queue_id: Optional[str] = typer.Option(None, "--queue-id", help="Queue ID"),
    concurrency_policy_id: Optional[str] = typer.Option(
        None, "--concurrency-policy-id", help="Concurrency resource ID"
    ),
    active_only: bool = typer.Option(False, "--active-only", help="List only active jobs"),
    created_after: Optional[str] = typer.Option(
        None, "--created-after", help=f"Filter by created_at lower bound ({_TBB_ISO_TIME_HELP})"
    ),
    created_before: Optional[str] = typer.Option(
        None, "--created-before", help=f"Filter by created_at upper bound ({_TBB_ISO_TIME_HELP})"
    ),
    finished_after: Optional[str] = typer.Option(
        None,
        "--finished-after",
        help=f"Filter by finished_at lower bound ({_TBB_ISO_TIME_HELP})",
    ),
    finished_before: Optional[str] = typer.Option(
        None,
        "--finished-before",
        help=f"Filter by finished_at upper bound ({_TBB_ISO_TIME_HELP})",
    ),
    tag: Optional[list[str]] = typer.Option(
        None, "--tag", help="Job tag (repeatable; combined with AND)"
    ),
    sort: Optional[str] = typer.Option(
        None, "--sort", help="Sort by: created_at, finished_at, or duration"
    ),
    asc: bool = typer.Option(False, "--asc", help="Sort ascending; requires --sort"),
    desc: bool = typer.Option(False, "--desc", help="Sort descending; requires --sort"),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(100, "--limit", help="Maximum number of entries to return"),
    columns: Optional[str] = typer.Option(None, "--columns", help=_TBB_JOB_LIST_COLUMNS_HELP),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
) -> None:
    """List pipeline jobs created by ap job tbb run."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    selected_columns = (
        _parse_columns_option(columns) if output_format in {"plain", "table"} else None
    )
    if active_only and status:
        raise typer.BadParameter("--active-only cannot be used with --status")
    try:
        tags = tbb.merge_tbb_tags("run", tag)
    except tbb.TBBProtocolError as exc:
        _emit_error(f"invalid tag: {exc}")
        raise typer.Exit(1)

    result = get_client().list_jobs(
        template=tbb.TBB_TEMPLATE,
        status=status,
        job_id=job_id,
        user_id=user_id,
        user_name=user_name,
        queue_id=queue_id,
        concurrency_policy_id=concurrency_policy_id,
        active_only=active_only,
        finished_after=finished_after,
        finished_before=finished_before,
        created_after=created_after,
        created_before=created_before,
        tag=tags,
        tag_logic="and",
        **_job_list_sort_kwargs(sort, asc=asc, desc=desc),
        skip=skip,
        limit=limit,
    )
    if output_format == "table":
        _print_job_list_plain(
            result,
            columns=selected_columns,
            rich=True,
            default_columns=_TBB_JOB_LIST_DEFAULT_COLUMNS,
            table_priority=_TBB_JOB_LIST_TABLE_PRIORITY,
            table_min_columns=_TBB_JOB_LIST_TABLE_MIN_COLUMNS,
        )
    elif output_format == "plain":
        _print_job_list_plain(
            result,
            columns=selected_columns,
            default_columns=_TBB_JOB_LIST_DEFAULT_COLUMNS,
            table_priority=_TBB_JOB_LIST_TABLE_PRIORITY,
            table_min_columns=_TBB_JOB_LIST_TABLE_MIN_COLUMNS,
        )
    else:
        _print_formatted(result, output_format)


@job_tbb_app.command("run")
def job_tbb_run(
    config: Path = typer.Option(..., "--config", help="Pipeline config file"),
    runtime_timeout: Optional[int] = typer.Option(
        None,
        "--runtime-timeout",
        min=0,
        help="Pipeline runtime timeout in seconds",
    ),
    agenthub_ref: Optional[str] = typer.Option(
        None, "--agenthub-ref", help="Agent-Hub branch/commit; overrides AP_AGENTHUB_REF"
    ),
    queue_id: Optional[str] = typer.Option(None, "--queue-id", help="Queue ID"),
    quota_id: Optional[str] = typer.Option(None, "--quota-id", help="Quota ID"),
    concurrency_policy_id: Optional[str] = typer.Option(
        None, "--concurrency-policy-id", help="Concurrency resource ID"
    ),
    datasources: Optional[str] = typer.Option(
        None,
        "--datasources",
        help="DataSources as JSON array or comma-separated IDs",
    ),
    overrides: Optional[str] = typer.Option(
        None, "--overrides", help="Override config (JSON object)"
    ),
    tag: Optional[list[str]] = typer.Option(None, "--tag", help="Job tag (repeatable)"),
    priority: Optional[str] = typer.Option(None, "--priority", help="Scheduling priority tier"),
    priority_weight: Optional[int] = typer.Option(
        None, "--priority-weight", help="Fine-grained scheduling priority weight"
    ),
    resource_mode: Optional[str] = typer.Option(
        None, "--resource-mode", help="Resource scheduling mode"
    ),
    wait: bool = typer.Option(False, "--wait", help="Wait for the pipeline job to finish"),
    wait_interval: float = typer.Option(
        5.0,
        "--wait-interval",
        min=0.1,
        help="Polling interval in seconds when used with --wait",
    ),
    wait_timeout: Optional[float] = typer.Option(
        None,
        "--wait-timeout",
        min=0.0,
        help="Maximum seconds to wait; omit to wait indefinitely",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
) -> None:
    """Submit one TrajBigBang pipeline job."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client(agenthub_ref=agenthub_ref)
    try:
        submission = _tbb_create_job(
            client,
            command="run",
            config=config,
            runtime_timeout=runtime_timeout,
            tag=tag,
            overrides=_parse_json_object(overrides, "--overrides"),
            queue_id=queue_id,
            quota_id=quota_id,
            concurrency_policy_id=concurrency_policy_id,
            datasources=_parse_datasources_option(datasources),
            priority=priority,
            priority_weight=priority_weight,
            resource_mode=resource_mode,
        )
        job = _tbb_job_from_submission(submission)
    except tbb.TBBProtocolError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)
    if not wait:
        _print_tbb_submission(job, output_format)
        return

    _wait_for_tbb_result(
        client,
        job,
        command="run",
        wait_interval=wait_interval,
        wait_timeout=wait_timeout,
        output_format=output_format,
    )


@meta_model_app.command("list")
def meta_model_list(
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List enabled meta-model tag values."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    result = get_client().list_meta_models()
    items = result.get("items") or []
    options = items
    if output_format in ("plain", "table"):
        rows = [
            {
                "name": m.get("name") or "-",
                "desc": m.get("desc_l1") or "-",
            }
            for m in options
        ]
        _print_plain_table(rows, [("name", "name"), ("desc", "desc")])
    else:
        # JSON/YAML 保持 {meta_model:{options}}；每项保留目录字段及 name 别名。
        _print_formatted({"meta_model": {"options": options}}, output_format)


@meta_model_app.command("get")
def meta_model_get(
    name: str = typer.Argument(..., help="Meta model name (or source_id)"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show one meta model."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    result = get_client().get_meta_model(name)
    if output_format in ("plain", "table"):
        _print_detail(result)
    else:
        _print_formatted(result, output_format)


@meta_tag_app.command("list")
def meta_tag_list(
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List meta tag keys (QwenMeta catalog via apiserver)."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    result = get_client().list_meta_tags()
    items = result.get("items") or []
    if output_format in ("plain", "table"):
        rows = [
            {
                "key": item.get("key") or "-",
                "name": item.get("name") or "-",
                "desc": item.get("desc") or "-",
            }
            for item in items
        ]
        _print_plain_table(rows, [("key", "key"), ("name", "name"), ("desc", "desc")])
    else:
        _print_formatted({"items": items}, output_format)


@meta_tag_app.command("get")
def meta_tag_get(
    key: str = typer.Argument(..., help="Meta tag key, e.g. meta-job-type"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show the value catalog of one meta tag key."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    result = get_client().get_meta_tags(key)
    _render_meta_tag_values(result.get("items") or [], output_format)


def _render_meta_tag_values(items, output_format: str) -> None:
    """值目录渲染：value/desc/enabled 表或原样 items。

    `ap meta-tag get` 与 `ap meta-train-stage list` /
    `ap meta-teacher-direction list` 共用（同目录行形态）。
    """
    if output_format in ("plain", "table"):
        rows = [
            {
                "value": item.get("value") or "-",
                "desc": item.get("desc_l1") or "-",
                "enabled": "yes" if item.get("is_enabled", True) else "no",
            }
            for item in items
        ]
        _print_plain_table(rows, [("value", "value"), ("desc", "desc"), ("enabled", "enabled")])
    else:
        _print_formatted({"items": items}, output_format)


@meta_job_type_app.command("list")
def meta_job_type_list(
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List enabled meta-job-type tag values."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    result = get_client().list_meta_job_types()
    info = result.get("meta_job_type") or {}
    options = info.get("options") or []
    if output_format in ("plain", "table"):
        rows = [
            {
                "value": o.get("value") or "-",
                "desc": o.get("desc_l1") or "-",
            }
            for o in options
        ]
        _print_plain_table(rows, [("value", "value"), ("desc", "desc")])
    else:
        _print_formatted(result, output_format)


@meta_train_stage_app.command("list")
def meta_train_stage_list(
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List meta train stage options (QwenMeta catalog; errors surface, no fallback)."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    result = get_client().get_meta_tags("meta-train-stage")
    _render_meta_tag_values(result.get("items") or [], output_format)


@meta_teacher_direction_app.command("list")
def meta_teacher_direction_list(
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List meta teacher direction options (QwenMeta catalog; errors surface, no fallback)."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    result = get_client().get_meta_tags("meta-teacher-direction")
    _render_meta_tag_values(result.get("items") or [], output_format)


@job_app.command("list")
def job_list(
    template: Optional[str] = typer.Option(None, "--template", help="Template name"),
    ak_id: Optional[str] = typer.Option(None, "--ak-id", help="AP-managed AK ID"),
    group_id: Optional[str] = typer.Option(None, "--group-id", help="Group ID"),
    status: Optional[str] = typer.Option(None, "--status", help=_JOB_STATUS_HELP),
    job_id: Optional[str] = typer.Option(None, "--job-id", help="Job ID"),
    instance_id: Optional[str] = typer.Option(None, "--instance-id", help="Instance ID"),
    user_id: Optional[str] = typer.Option(None, "--user-id", help="User ID"),
    user_name: Optional[str] = typer.Option(None, "--user-name", help="User name"),
    queue_id: Optional[str] = typer.Option(None, "--queue-id", help="Queue ID"),
    concurrency_policy_id: Optional[str] = typer.Option(
        None, "--concurrency-policy-id", help="Concurrency resource ID"
    ),
    active_only: bool = typer.Option(False, "--active-only", help="Only include non-terminal jobs"),
    finished_after: Optional[str] = typer.Option(
        None, "--finished-after", help=f"Filter by lower bound of finished_at ({_ISO_TIME_HELP})"
    ),
    finished_before: Optional[str] = typer.Option(
        None, "--finished-before", help=f"Filter by upper bound of finished_at ({_ISO_TIME_HELP})"
    ),
    created_after: Optional[str] = typer.Option(
        None, "--created-after", help=f"Filter by lower bound of created_at ({_ISO_TIME_HELP})"
    ),
    created_before: Optional[str] = typer.Option(
        None, "--created-before", help=f"Filter by upper bound of created_at ({_ISO_TIME_HELP})"
    ),
    prefix_match: bool = typer.Option(
        False, "--prefix-match", help="Use prefix match for ID/name filters"
    ),
    tag: Optional[list[str]] = typer.Option(
        None, "--tag", help="Filter by tag (repeatable; multiple tags default to AND)"
    ),
    tag_pattern: Optional[str] = typer.Option(
        None, "--tag-pattern", help="Filter tags by case-insensitive regex"
    ),
    tag_logic: str = typer.Option(
        "and", "--tag-logic", help="How to combine repeated --tag filters: and/or"
    ),
    meta_model: Optional[str] = typer.Option(
        None, "--meta-model", help="Filter by group meta_model"
    ),
    meta_job_type: Optional[str] = typer.Option(
        None, "--meta-job-type", help="Filter by group meta_job_type"
    ),
    sort: Optional[str] = typer.Option(
        None, "--sort", help="Sort by: created_at, finished_at, or duration"
    ),
    asc: bool = typer.Option(False, "--asc", help="Sort ascending; requires --sort"),
    desc: bool = typer.Option(False, "--desc", help="Sort descending; requires --sort"),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(100, "--limit", help="Maximum number of entries to return"),
    next_token: Optional[str] = typer.Option(
        None,
        "--next-token",
        help="Opaque token returned by the previous exact-group job list page; requires --group-id",
    ),
    cursor: bool = typer.Option(
        False,
        "--cursor",
        help="Opt this page into next-token pagination; requires --group-id",
    ),
    no_total: bool = typer.Option(
        False,
        "--no-total",
        help="Skip the server-side count; total becomes null in json/yaml output",
    ),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        help=_JOB_LIST_COLUMNS_HELP,
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List jobs."""
    try:
        validate_ak_id(ak_id)
    except ValueError as exc:
        raise typer.BadParameter(str(exc), param_hint="--ak-id") from None
    output_format = _normalize_output_format(output_format, keep_table=True)
    selected_columns = (
        _parse_columns_option(columns) if output_format in ("plain", "table") else None
    )
    if active_only and status:
        raise typer.BadParameter("--active-only cannot be used with --status")
    normalized_tag_logic = tag_logic.strip().lower()
    if normalized_tag_logic not in {"and", "or"}:
        raise typer.BadParameter("--tag-logic must be one of and/or")
    if tag_pattern and tag:
        raise typer.BadParameter("--tag-pattern cannot be used with --tag")
    if normalized_tag_logic != "and" and not tag:
        raise typer.BadParameter("--tag-logic requires --tag")
    if next_token and not group_id:
        raise typer.BadParameter("--next-token requires --group-id")
    if cursor and not group_id:
        raise typer.BadParameter("--cursor requires --group-id")
    if next_token and skip > 0:
        raise typer.BadParameter("--next-token cannot be used with --skip greater than 0")
    if cursor and skip > 0:
        raise typer.BadParameter("--cursor cannot be used with --skip greater than 0")
    sort_kwargs = _job_list_sort_kwargs(sort, asc=asc, desc=desc)
    cursor_request = bool(next_token) or cursor
    client = get_client()
    result = client.list_jobs(
        template=template,
        **({"ak_id": ak_id} if ak_id is not None else {}),
        group_id=group_id,
        status=status,
        job_id=job_id,
        instance_id=instance_id,
        user_id=user_id,
        user_name=user_name,
        queue_id=queue_id,
        concurrency_policy_id=concurrency_policy_id,
        active_only=active_only,
        finished_after=finished_after,
        finished_before=finished_before,
        created_after=created_after,
        created_before=created_before,
        prefix_match=prefix_match,
        tag=tag,
        tag_pattern=tag_pattern,
        tag_logic=normalized_tag_logic if tag else None,
        **({"meta_model": meta_model} if meta_model is not None else {}),
        **({"meta_job_type": meta_job_type} if meta_job_type is not None else {}),
        **sort_kwargs,
        **({"next_token": next_token} if next_token else {}),
        **({"pagination": "cursor"} if cursor_request else {}),
        include_total=not no_total,
        skip=skip,
        limit=limit,
    )
    if output_format == "table":
        _print_job_list_plain(result, columns=selected_columns, rich=True)
    elif output_format == "plain":
        _print_job_list_plain(result, columns=selected_columns)
    else:
        _print_formatted(result, output_format)
    next_token = result.get("next_token")
    if output_format in {"table", "plain"} and next_token:
        typer.echo(f"Next token: {next_token}", err=True)


@job_app.command("create")
def job_create(
    transparency: Optional[str] = typer.Option(
        None,
        "--transparency",
        help="whitebox or blackbox; omit to inherit the Group/Profile default",
    ),
    template: Optional[str] = typer.Argument(None, help="Template name; optional with --profile"),
    ak_id: Optional[str] = typer.Option(
        None, "--ak-id", help="AP-managed AK ID; requires server support"
    ),
    ak_mode: str = typer.Option(
        "auto", "--ak-mode", help="AK credential source: auto, manual or synced"
    ),
    agenthub_ref: Optional[str] = typer.Option(
        None, "--agenthub-ref", help="Agent-Hub branch/commit; overrides AP_AGENTHUB_REF"
    ),
    instance_id: Optional[str] = typer.Option(
        None,
        "--instance-id",
        "-i",
        help="Instance ID (comma-separated for multiple, or @file to load from a file)",
    ),
    dataset: Optional[str] = typer.Option(None, "--dataset", "-d", help="Dataset version path"),
    instance_range: Optional[str] = typer.Option(
        None,
        "--range",
        help=(
            "Select a positional subset of instance IDs. Supports END, START,END, "
            "START,END,STEP. Also accepts START:END[:STEP] and range(START, END, STEP). "
            "With --profile, the server slices instances before trials expansion"
        ),
    ),
    exclude_instance_ids: Optional[str] = typer.Option(
        None,
        "--exclude-instance-ids",
        help="Instance IDs to exclude from the selected set (comma-separated, or @file)",
    ),
    params: Optional[str] = typer.Option(None, "--params", "-p", help="Parameters (JSON)"),
    params_list_input: Optional[str] = typer.Option(
        None, "--params-list", "-l", help="Params list: JSON array string or path to a JSON file"
    ),
    suite_name: Optional[str] = typer.Option(None, "--suite-name", help="Suite (job group) name"),
    group_id: Optional[str] = typer.Option(
        None, "--group-id", help="Reuse or create the specified Group ID"
    ),
    queue: Optional[str] = typer.Option(
        None,
        "--queue-id",
        "--queue",
        "-q",
        help="Queue id (agent-platform-apiserver); omit to use server default (default)",
    ),
    quota_id: Optional[str] = typer.Option(
        None,
        "--quota-id",
        help="Quota id; overrides scheduler-assigned quota when specified",
    ),
    concurrency_policy_id: Optional[str] = typer.Option(
        None,
        "--concurrency-policy-id",
        help=(
            "Concurrency policy id (admission key); the scheduler holds jobs in "
            "Queued once the policy's active+dispatched count reaches its capacity. "
            "Request-level: shared across the whole batch, like --quota-id."
        ),
    ),
    tags: Optional[str] = typer.Option(None, "--tags", help="Tags (comma-separated)"),
    tag: Optional[list[str]] = typer.Option(
        None,
        "--tag",
        help="Meta tag as key:value, repeatable (e.g. --tag meta-job-type:Eval-Eval). "
        "Same key with different values is rejected, including against --tags; "
        "conflicts with --meta-model, --meta-job-type, --meta-train-stage and "
        "--meta-teacher-direction are rejected.",
    ),
    meta_model: Optional[str] = typer.Option(
        None,
        "--meta-model",
        help="Meta model tag; omit to leave unset",
    ),
    meta_job_type: Optional[str] = typer.Option(
        None,
        "--meta-job-type",
        help="Meta job type tag: Eval-Eval (default) or Others",
    ),
    meta_teacher_direction: Optional[str] = typer.Option(
        None,
        "--meta-teacher-direction",
        help="Meta teacher direction tag; omit to derive from dataset_series; options: ap meta-teacher-direction list",
    ),
    meta_train_stage: Optional[str] = typer.Option(
        None,
        "--meta-train-stage",
        help="Meta train stage tag; omit to derive from dataset run_type; options: ap meta-train-stage list",
    ),
    overrides: Optional[str] = typer.Option(None, "--overrides", help="Override config (JSON)"),
    concurrency: Optional[int] = typer.Option(
        None,
        "--concurrency",
        "-c",
        min=1,
        help="Concurrency (max simultaneously running jobs in batch submissions). Server default: 50.",
    ),
    model_base_url_collection: Optional[str] = typer.Option(
        None,
        "--model-base-url-collection",
        help="Model base URL collection for server-side load balancing (JSON array or comma-separated)",
    ),
    datasources: Optional[str] = typer.Option(
        None,
        "--datasources",
        help=(
            "Datasources to mount into job pods. JSON array (e.g. "
            '\'["ds-abc", {"datasource":"ds-xyz","mount_path":"/mnt/data"}]\') '
            "or comma-separated datasource IDs (e.g. 'ds-abc,ds-xyz')."
        ),
    ),
    batch_size: int = typer.Option(
        200,
        "--batch-size",
        min=1,
        help="Number of params items per batch submission request; ignored with --job-spec",
    ),
    trials: Optional[int] = typer.Option(
        None,
        "--trials",
        min=1,
        help="Override profile spec.trials (per-instance repetition count); profile mode only",
    ),
    wait: bool = typer.Option(
        False, "--wait", help="Keep waiting after submission until the jobs finish"
    ),
    model_base_url_file: Optional[str] = typer.Option(
        None,
        "--model-base-url-file",
        help="File path containing model base URL list (one URL per line), fallback for --model-base-url-collection",
    ),
    enable_post_process: bool = typer.Option(
        False,
        "--enable-post-process",
        help="Enable template-defined Group PostProcess with default params",
    ),
    group_post_process: Optional[str] = typer.Option(
        None,
        "--group-post-process",
        help="Full Group PostProcess config (JSON object)",
    ),
    wait_interval: float = typer.Option(
        5.0, "--wait-interval", min=0.1, help="Polling interval in seconds when used with --wait"
    ),
    wait_timeout: Optional[float] = typer.Option(
        None,
        "--wait-timeout",
        min=0.0,
        help="Maximum seconds to wait when used with --wait; omit to wait indefinitely",
    ),
    timeout: Optional[float] = typer.Option(
        None,
        "--timeout",
        min=0.0,
        help=(
            "HTTP connect and read timeout in seconds for each submission request; "
            "0 means no timeout"
        ),
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
    enable_otel_tracing: Optional[bool] = typer.Option(
        None,
        "--enable-otel-tracing",
        help="Enable OTEL tracing; omit to use global config",
    ),
    runner: Optional[str] = typer.Option(
        None, "--runner", help="Runner backend (rock, k8s-orchestrated, argo, local)"
    ),
    runner_options: Optional[str] = typer.Option(
        None, "--runner-options", help="Runner options (JSON)"
    ),
    enable_idempotency: bool = typer.Option(
        False,
        "--idempotency",
        help="Enable idempotent submission; generates a UUID4 key when --idempotency-key is omitted",
    ),
    idempotency_key: Optional[str] = typer.Option(
        None,
        "--idempotency-key",
        help="UUID4 key for retrying the same logical submission; providing one enables idempotency",
    ),
    max_failure_retries: int = typer.Option(
        0,
        "--max-failure-retries",
        min=0,
        help="Maximum automatic retries after each Job fails (default: 0)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview the full HTTP request payloads without submitting (respects --batch-size splits)",
    ),
    job_spec_flag: bool = typer.Option(
        False,
        "--job-spec",
        help="Output a single job-spec JSON and exit; use as input for 'ap plan create --job-spec'",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug mode: keep pod alive after task completion for interactive debugging (Pod Login)",
    ),
    debug_keep_alive_seconds: Optional[int] = typer.Option(
        None,
        "--debug-keep-alive-seconds",
        help="Seconds to keep pod alive in debug mode (default: 3600, only effective with --debug)",
    ),
    priority: Optional[str] = typer.Option(
        None,
        "--priority",
        help="Scheduling tier: high or medium. Omit both priority flags to inherit Group defaults; otherwise an omitted tier is medium",
    ),
    priority_weight: Optional[int] = typer.Option(
        None,
        "--priority-weight",
        help="Priority weight, 0-10. Omit both priority flags to inherit Group defaults; otherwise an omitted weight is 0",
    ),
    resource_mode: Optional[str] = typer.Option(
        None,
        "--resource-mode",
        help="Resource scheduling mode: guaranteed (default) or elastic",
    ),
    disable_loongcollector: bool = typer.Option(
        False,
        "--disable-loongcollector",
        help="Disable LoongCollector sidecar injection for this submission",
    ),
    credential_type: Optional[str] = typer.Option(
        None,
        "--credential-type",
        help="Credential type for template credential assignment (e.g. github, notion)",
    ),
    account_pool: Optional[str] = typer.Option(
        None,
        "--account-pool",
        help="Account Pool ID to use for this Job or every Job in the submission",
    ),
    eval_config: Optional[str] = typer.Option(
        None,
        "--eval-config",
        help='Evaluation config (JSON object, e.g. \'{"category_field":"mcp_service"}\')',
    ),
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        help="Profile ID or name with optional :latest, :verified, :release (no fallback), or :vN; resolved server-side",
    ),
    resource_profile_id: Optional[str] = typer.Option(
        None,
        "--resource-profile",
        help="Resource Profile ID (rp-*); applies per-instance resource settings",
    ),
    benchmark: Optional[str] = typer.Option(
        None,
        "--benchmark",
        help="Benchmark name from the AP registry (see 'ap benchmark list')",
    ),
    checkpoint_id: Optional[str] = typer.Option(
        None,
        "--checkpoint-id",
        help="Checkpoint ID (reporting metadata)",
    ),
    checkpoint_id_alias: Optional[str] = typer.Option(
        None,
        "--check-point-id",
        "--ckpt-id",
        hidden=True,
        help="Alias of --checkpoint-id",
    ),
    checkpoint_path: Optional[str] = typer.Option(
        None,
        "--checkpoint-path",
        help="Checkpoint storage path/URI (reporting metadata)",
    ),
    checkpoint_path_alias: Optional[str] = typer.Option(
        None,
        "--check-point-path",
        "--ckpt-path",
        hidden=True,
        help="Alias of --checkpoint-path",
    ),
    checkpoint: Optional[str] = typer.Option(
        None,
        "--checkpoint",
        help="Checkpoint as JSON object; explicit id/path flags win",
    ),
    checkpoint_alias: Optional[str] = typer.Option(
        None,
        "--check-point",
        "--ckpt",
        hidden=True,
        help="Alias of --checkpoint",
    ),
    experiment: Optional[str] = typer.Option(
        None,
        "--experiment",
        help="Experiment name for score reporting; omit to skip",
    ),
):
    """Submit a job.

    Model configuration:
        Supply template parameters through --params/-p; select a managed credential with --ak-id.

    Examples:
        # Single job - full parameters
        ap job create claw-eval-task -p '{"task_id":"T02_email_triage","model":"qwen-max"}'

        # Single job - instance_id + shared params
        ap job create claw-eval-task -i T02_email_triage -p '{"model":"qwen-max"}'

        # Batch jobs - multiple instance_ids + shared params
        ap job create claw-eval-task -i T02_email_triage,T03zh_calendar_scheduling,T04_calendar_scheduling -p '{"model":"qwen-max"}'

        # Batch jobs - dataset + shared params
        ap job create claw-eval-task --dataset claw-eval/claw-eval/v1@0 -p '{"model":"qwen-max"}'

        # Batch jobs - dataset subset with exclusions
        ap job create claw-eval-task --dataset claw-eval/claw-eval/v1@0 --range 0,10,2 --exclude-instance-ids T03zh_calendar_scheduling

        # Batch jobs from a params list(inline JSON) with shared base params (-p merged into each item)
        ap job create claw-eval-task --params-list '[{"task_id":"T02_email_triage"},{"task_id":"T03zh_calendar_scheduling"}]' -p '{"model":"qwen-max"}'

        # Batch jobs from a params list file (also supports -p for shared base params)
        ap job create claw-eval-task --params-list params.json -p '{"model":"qwen-max"}'

        # Debug mode - keep pod alive for interactive debugging (Pod Login)
        ap job create stress-test -p '{"duration":60}' --debug

        # Debug mode with custom keep-alive duration
        ap job create stress-test -p '{"duration":60}' --debug --debug-keep-alive-seconds 7200

        # Apply per-instance resource settings from a Resource Profile
        ap job create claw-eval-task --dataset claw-eval/v1 --resource-profile rp-123

    Note: benchmark+ckpt metadata (--benchmark/--checkpoint-*/--experiment) on a
    standalone single job needs no client-side group handling — the server
    auto-creates a Group (auto_created_benchmark_group) to persist the
    Group-level fields. Generating a group_id client-side would break
    idempotent retries: the server rejects a same idempotency_key with a
    different requested group_id (409 idempotency_conflict).
    """
    if transparency is not None and transparency not in {"whitebox", "blackbox"}:
        raise typer.BadParameter("Choose whitebox or blackbox", param_hint="--transparency")
    output_format = _normalize_output_format(output_format)
    if not template and not profile:
        raise typer.BadParameter("TEMPLATE is required unless --profile is provided")
    if ak_mode not in {"auto", "manual", "synced"}:
        raise typer.BadParameter("Choose auto, manual or synced", param_hint="--ak-mode")
    try:
        validate_ak_id(ak_id)
        resource_profile_id = _normalize_resource_profile_id(resource_profile_id)
    except ValueError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)
    client = get_client(agenthub_ref=agenthub_ref)

    def wait_printer(message: str) -> None:
        typer.echo(message, err=output_format != "plain")

    wait_result = None
    implicit_resource_profile_idempotency = (
        resource_profile_id is not None and not dry_run and not job_spec_flag
    )
    idempotency_enabled = (
        enable_idempotency
        or transparency == "blackbox"
        or idempotency_key is not None
        or profile is not None
        or implicit_resource_profile_idempotency
        or ak_id is not None
    )
    submission_idempotency_key = (
        idempotency_key or str(uuid.uuid4()) if idempotency_enabled else None
    )
    dry_run_warnings: list[str] = []
    if job_spec_flag:
        if dry_run:
            dry_run_warnings.append("--dry-run is ignored when --job-spec is used")
            dry_run = False
        if wait:
            dry_run_warnings.append("--wait is ignored when --job-spec is used")
    elif dry_run and wait:
        dry_run_warnings.append("--wait is ignored in dry-run mode")

    params_dict = json.loads(params) if params else {}
    _reject_account_pool_template_credential_cli(
        account_pool,
        credential_type,
        params_dict.get("credential_type"),
    )
    if debug:
        params_dict["debug"] = "true"
        params_dict["debug_keep_alive_seconds"] = str(debug_keep_alive_seconds or 3600)
    tags_list = _merge_job_tags(tags.split(",") if tags else None)
    try:
        tag_pairs = _parse_tag_pairs(tag)
        # 先并入 tags 再走 _merge_meta_tags：--tag meta-model:X 与
        # --meta-model Y 的冲突由 _merge_meta_tags 统一裁决；--tags 与
        # --tag 的同 key 冲突在 _merge_tag_forms 内拒绝
        tags_list = _merge_tag_forms(tags_list, tag_pairs)
        tags_list = _merge_meta_tags(
            tags_list,
            meta_model=meta_model,
            meta_job_type=meta_job_type,
            meta_teacher_direction=meta_teacher_direction,
            meta_train_stage=meta_train_stage,
        )
    except ValueError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)
    overrides_dict = json.loads(overrides) if overrides else None
    try:
        validate_ak_selection(ak_id, params_dict, None, overrides_dict)
    except ValueError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1) from None
    if isinstance(overrides_dict, dict) and overrides_dict.get("sidecar_resources"):
        typer.secho(
            "warning: 'overrides.sidecar_resources' is deprecated; "
            "use 'overrides.sidecars.<name>.resources' instead.",
            fg=typer.colors.YELLOW,
            err=True,
        )
    runner_options_dict = json.loads(runner_options) if runner_options else None
    eval_config_dict = _parse_json_object(eval_config, "--eval-config")
    group_post_process_dict = _parse_json_object(group_post_process, "--group-post-process")
    # Fold hidden alias flags into the canonical values (canonical wins)
    checkpoint_id = checkpoint_id or checkpoint_id_alias
    checkpoint_path = checkpoint_path or checkpoint_path_alias
    checkpoint = checkpoint or checkpoint_alias
    checkpoint_dict = _parse_json_object(checkpoint, "--checkpoint")
    if enable_post_process and group_post_process_dict is None:
        group_post_process_dict = {}
    post_process_kwargs = (
        {"group_post_process": group_post_process_dict}
        if group_post_process_dict is not None
        else {}
    )

    # Available to both profile and non-profile flows.
    datasources_list = _parse_datasources_option(datasources)

    # Parse model_base_url_collection early so it's available for both profile and non-profile flows.
    model_base_url_collection_list: Optional[list] = None
    if model_base_url_collection:
        try:
            model_base_url_collection_list = json.loads(model_base_url_collection)
            if not isinstance(model_base_url_collection_list, list):
                _emit_error("--model-base-url-collection must be a JSON array")
                raise typer.Exit(1)
        except json.JSONDecodeError:
            model_base_url_collection_list = [
                u.strip() for u in model_base_url_collection.split(",") if u.strip()
            ] or None
    if not model_base_url_collection_list and model_base_url_file:
        try:
            model_base_url_collection_list = [
                line.strip()
                for line in Path(model_base_url_file).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ] or None
        except FileNotFoundError:
            _emit_error(f"file not found: {model_base_url_file}")
            raise typer.Exit(1)

    # Reject --trials when not in profile mode (profile-only override)
    if trials is not None and profile is None:
        _emit_error("--trials is only supported with --profile")
        raise typer.Exit(1)

    # Reject --eval-config when not in profile mode (use 'ap group create/update --eval-config' instead)
    if eval_config is not None and profile is None:
        _emit_error(
            "--eval-config is only supported with --profile. Use 'ap group create --eval-config' or 'ap group update --eval-config' instead."
        )
        raise typer.Exit(1)

    # Profile mode: early branch
    if profile is not None:
        # Mutual exclusion checks
        if params_list_input:
            _emit_error(
                "--profile is incompatible with --params-list (profile expands params server-side)"
            )
            raise typer.Exit(1)
        if instance_range is not None:
            try:
                _parse_instance_range(instance_range)
            except ValueError as exc:
                _emit_error(str(exc))
                raise typer.Exit(1)
        if exclude_instance_ids:
            _emit_error("--profile is incompatible with --exclude-instance-ids")
            raise typer.Exit(1)
        if group_id and model_base_url_collection_list:
            _emit_error(
                "--model-base-url-collection(--model-base-url-file) and --group-id are mutually exclusive. "
                "URL pool is a Group-level attribute set at Group creation time. "
                "Use 'ap group update' instead."
            )
            raise typer.Exit(1)
        if not suite_name and not group_id:
            from datetime import datetime as _dt

            suite_name = f"{template or 'profile'}-sp-{profile.replace(':', '-')}-{_dt.now().strftime('%m%d-%H%M')}"

        # Parse IDs only; Profile range selection happens on the server.
        instances_list: Optional[list[str]] = None
        if instance_id:
            try:
                instances_list = _parse_instance_id_csv(instance_id, "--instance-id")
            except ValueError as exc:
                _emit_error(str(exc))
                raise typer.Exit(1)

        # Build request body via create_job (reuse existing method with profile fields)
        body = client.build_create_job_body(
            **({"transparency": transparency} if transparency is not None else {}),
            template=template,
            params=params_dict or None,
            suite_name=suite_name,
            tags=tags_list,
            overrides=overrides_dict,
            max_concurrency=concurrency,
            queue_id=queue,  # CLI --queue / -q 走标准 queue_id 字段
            quota_id=quota_id,
            policy_id=concurrency_policy_id,
            datasources=datasources_list,
            enable_otel_tracing=enable_otel_tracing,
            runner=runner,
            runner_options=runner_options_dict,
            idempotency_key=submission_idempotency_key,
            max_failure_retries=max_failure_retries,
            group_id=group_id,
            model_base_url_collection=model_base_url_collection_list,
            group_post_process=group_post_process_dict,
            priority=priority,
            priority_weight=priority_weight,
            resource_mode=resource_mode,
            disable_loongcollector=disable_loongcollector,
            credential_type=credential_type,
            account_pool=account_pool,
            eval_config=eval_config_dict,
            profile=profile,
            resource_profile_id=resource_profile_id,
            **({"ak_id": ak_id} if ak_id is not None else {}),
            **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
            instances=instances_list,
            instance_range=instance_range,
            dataset=dataset,
            batch_size=batch_size,
            trials=trials,
            checkpoint_id=checkpoint_id,
            checkpoint_path=checkpoint_path,
            checkpoint=checkpoint_dict,
            benchmark=benchmark,
            experiment=experiment,
        )

        if job_spec_flag:
            _emit_dry_run_warnings(dry_run_warnings)
            _print_formatted(body, "json" if output_format == "plain" else output_format)
            return

        if instance_range is not None:
            try:
                client.ensure_profile_range_supported(timeout=timeout)
            except (ValueError, ConfigurationError) as exc:
                _emit_error(str(exc))
                raise typer.Exit(1) from None

        if dry_run:
            _emit_dry_run_warnings(dry_run_warnings)
            body["dry_run"] = True
            try:
                result = client._post("/jobs", body, timeout=timeout)
                require_managed_ak_ack(result, ak_id)
            except ManagedAKProtocolError as exc:
                _emit_error(str(exc))
                raise typer.Exit(1) from None
            _require_profile_ack(result, profile)
            _print_formatted(result, "json" if output_format == "plain" else output_format)
            return

        # Build retry command before submitting so it's available on failure
        profile_retry_command = (
            _build_job_create_retry_command(idempotency_key=submission_idempotency_key)
            if idempotency_enabled and submission_idempotency_key is not None
            else None
        )
        profile_retry_hint_printed = False

        def emit_profile_retry_hint_once() -> None:
            nonlocal profile_retry_hint_printed
            if profile_retry_hint_printed or profile_retry_command is None:
                return
            _emit_idempotency_retry_hint(profile_retry_command)
            profile_retry_hint_printed = True

        try:
            with console.status("[bold green]Submitting by profile..."):
                result = client.create_job(
                    **({"transparency": transparency} if transparency is not None else {}),
                    template=template,
                    params=params_dict or None,
                    suite_name=suite_name,
                    tags=tags_list,
                    overrides=overrides_dict,
                    max_concurrency=concurrency,
                    queue_id=queue,  # CLI --queue / -q 走标准 queue_id 字段
                    quota_id=quota_id,
                    policy_id=concurrency_policy_id,
                    datasources=datasources_list,
                    enable_otel_tracing=enable_otel_tracing,
                    runner=runner,
                    runner_options=runner_options_dict,
                    idempotency_key=submission_idempotency_key,
                    max_failure_retries=max_failure_retries,
                    group_id=group_id,
                    model_base_url_collection=model_base_url_collection_list,
                    priority=priority,
                    priority_weight=priority_weight,
                    resource_mode=resource_mode,
                    disable_loongcollector=disable_loongcollector,
                    credential_type=credential_type,
                    account_pool=account_pool,
                    eval_config=eval_config_dict,
                    profile=profile,
                    resource_profile_id=resource_profile_id,
                    **({"ak_id": ak_id} if ak_id is not None else {}),
                    **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                    instances=instances_list,
                    instance_range=instance_range,
                    dataset=dataset,
                    batch_size=batch_size,
                    trials=trials,
                    checkpoint_id=checkpoint_id,
                    checkpoint_path=checkpoint_path,
                    checkpoint=checkpoint_dict,
                    benchmark=benchmark,
                    experiment=experiment,
                    timeout=timeout,
                    **post_process_kwargs,
                )
                require_managed_ak_ack(result, ak_id)
                _require_resource_profile_ack(result, resource_profile_id)
        except ManagedAKProtocolError as exc:
            _emit_error(str(exc))
            raise typer.Exit(1) from None
        except Exception:
            emit_profile_retry_hint_once()
            raise

        _require_profile_ack(result, profile)

        # Use idempotency_key returned by server (may differ when auto-generated server-side)
        effective_idem_key = result.get("idempotency_key") or submission_idempotency_key

        if output_format == "plain":
            failed_count = result.get("failed", 0)
            if failed_count > 0:
                print("[yellow]Profile submission completed with errors:[/]")
            else:
                print("[green]Profile submission completed:[/]")
            print(f"  profile: {profile}")
            if ak_id is not None:
                print(f"  ak_ids: {response_ak_ids(result)}")
            print(f"  profile_id: {result['profile_id']}")
            print(f"  profile_version: {result['profile_version']}")
            if resource_profile_id is not None:
                print(f"  resource_profile_id: {resource_profile_id}")
            print(f"  group_id: {result.get('group_id')}")
            print(f"  total: {result.get('total')}")
            print(f"  submitted: {result.get('submitted', result.get('total'))}")
            if failed_count > 0:
                print(f"  [red]failed: {failed_count}[/]")
            print(f"  batches: {result.get('batches')}")
            if effective_idem_key is not None:
                print(f"  idempotency_key: {effective_idem_key}")
            if failed_count > 0:
                errors = result.get("errors", [])
                error_console.print(
                    f"[yellow]warning: {failed_count} job(s) failed to submit. "
                    f"Use the same idempotency_key to retry.[/]"
                )
                for err in errors[:10]:
                    error_console.print(
                        f"  [red]- [{err.get('index')}] {err.get('instance_id')}: {err.get('error')}[/]"
                    )
                if len(errors) > 10:
                    error_console.print(f"  ... and {len(errors) - 10} more")
                emit_profile_retry_hint_once()

        if wait:
            wait_group_id = result.get("group_id")
            if wait_group_id:
                try:
                    _emit_progress(
                        f"Waiting for group to finish: {wait_group_id} "
                        f"(interval={wait_interval}s, timeout={_format_wait_timeout(wait_timeout)})"
                    )
                    final_group = wait_for_group(
                        client,
                        wait_group_id,
                        wait_interval,
                        timeout=wait_timeout,
                        printer=wait_printer,
                    )
                    wait_result = {
                        "type": "group",
                        "interval": wait_interval,
                        "timeout": wait_timeout,
                        "result": final_group,
                    }
                    if output_format == "plain":
                        stats = final_group.get("stats") or {}
                        print(f"[green]Group finished:[/] {wait_group_id}")
                        print(f"  total: {stats.get('total', 0)}")
                        print(f"  succeeded: {stats.get('succeeded', 0)}")
                        print(f"  failed: {stats.get('failed', 0)}")
                        print(f"  cancelled: {stats.get('cancelled', 0)}")
                except WaitTimeoutError as exc:
                    emit_profile_retry_hint_once()
                    typer.echo(f"error: {exc}", err=True)
                    raise typer.Exit(1)

        if output_format != "plain":
            payload = {"submission": result}
            if wait_result is not None:
                payload["wait"] = wait_result
            _print_formatted(payload, output_format)
        return
    # ─── End profile mode ────────────────────────────────────────────────

    instance_ids = None
    if instance_id:
        try:
            instance_ids = _select_instance_ids(
                _parse_instance_id_csv(instance_id, "--instance-id"),
                instance_range,
                exclude_instance_ids,
            )
        except ValueError as exc:
            _emit_error(str(exc))
            raise typer.Exit(1)
    elif instance_range or exclude_instance_ids:
        if not dataset:
            _emit_error("--range and --exclude-instance-ids require --instance-id or --dataset")
            raise typer.Exit(1)

    parsed_params_list = None
    if params_list_input:
        raw = params_list_input.strip()
        if raw.startswith("["):
            try:
                parsed_params_list = json.loads(raw)
            except json.JSONDecodeError as e:
                _emit_error(f"failed to parse --params-list JSON: {e}")
                raise typer.Exit(1)
        else:
            try:
                with open(raw, "r", encoding="utf-8") as f:
                    parsed_params_list = json.load(f)
            except json.JSONDecodeError as e:
                _emit_error(f"failed to parse --params-list file as JSON: {e}")
                raise typer.Exit(1)
            except FileNotFoundError:
                _emit_error(f"file not found: {raw}")
                raise typer.Exit(1)
        if not isinstance(parsed_params_list, list):
            _emit_error("--params-list content must be a JSON array")
            raise typer.Exit(1)
        if len(parsed_params_list) == 0:
            _emit_error("--params-list content is an empty array")
            raise typer.Exit(1)
        _reject_account_pool_template_credential_cli(
            account_pool,
            *(item.get("credential_type") for item in parsed_params_list if isinstance(item, dict)),
        )

    try:
        validate_ak_selection(ak_id, params_dict, parsed_params_list, overrides_dict)
    except ValueError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1) from None

    is_batch = False
    if parsed_params_list:
        is_batch = True
    elif instance_ids and len(instance_ids) > 1:
        is_batch = True
    elif dataset:
        is_batch = True
    elif not instance_id and not dataset and not params:
        _emit_error("must specify -p, or use -i / --dataset / --params-list")
        raise typer.Exit(1)

    if group_post_process_dict is not None and not (profile or is_batch or group_id):
        _emit_error("--enable-post-process/--group-post-process requires a Group")
        raise typer.Exit(1)

    # Parse model_base_url_collection (supports JSON array, comma-separated string, or file path)
    # NOTE: already parsed above (before profile branch). Re-use model_base_url_collection_list.

    # --model-base-url-collection only applies to batch submissions; warn and drop it for single jobs.
    if not is_batch and model_base_url_collection_list:
        warning = "--model-base-url-collection is ignored for single-job submissions"
        if dry_run:
            dry_run_warnings.append(warning)
        else:
            _emit_info(f"warning: {warning}", output_format)
        model_base_url_collection_list = None

    retry_command = (
        _build_job_create_retry_command(idempotency_key=submission_idempotency_key)
        if not dry_run
        and not job_spec_flag
        and idempotency_enabled
        and submission_idempotency_key is not None
        else None
    )
    retry_hint_printed = False

    def emit_retry_hint_once() -> None:
        nonlocal retry_hint_printed
        if retry_hint_printed:
            return
        if retry_command is None:
            return
        _emit_idempotency_retry_hint(retry_command)
        retry_hint_printed = True

    if instance_ids and len(instance_ids) == 1:
        # auto-map instance_id -> task_id
        params_dict = {**params_dict, "instance_id": instance_ids[0], "task_id": instance_ids[0]}

    if is_batch:
        if parsed_params_list:
            # build params_list from --params-list; params_dict (含 --debug 注入) 作为 base 合并
            params_list = [{**p, **params_dict} for p in parsed_params_list]
        elif instance_ids:
            params_list = [
                {**params_dict, "instance_id": iid, "task_id": iid} for iid in instance_ids
            ]
        else:
            _emit_progress(f"Fetching dataset instances: {dataset} ...")
            try:
                instances = client.list_all_dataset_instances(dataset)
            except Exception:
                emit_retry_hint_once()
                raise
            total = instances.get("total", 0)
            if total == 0:
                typer.secho("error: no instances found", fg="red", err=True)
                emit_retry_hint_once()
                raise typer.Exit(1)
            _emit_progress(f"Found {total} instance(s)")
            try:
                instance_ids = _select_instance_ids(
                    instances.get("instance_ids", []),
                    instance_range,
                    exclude_instance_ids,
                )
            except ValueError as exc:
                _emit_error(str(exc))
                raise typer.Exit(1)
            if (instance_range or exclude_instance_ids) and len(instance_ids) != total:
                message = f"Selected {len(instance_ids)} instance(s)"
                if dry_run:
                    _emit_progress(message)
                else:
                    _emit_info(message, output_format)
            params_list = [
                {**params_dict, "instance_id": iid, "task_id": iid} for iid in instance_ids
            ]

        total_count = len(params_list)

        # Decide the group up front when provided by the caller. Otherwise the
        # first server batch response establishes the group for the submission.
        target_group_id = group_id

        total_submitted = 0
        total_failed = 0
        batch_results: list[dict] = []
        observed_ak_ids: set[str] = set()
        observed_group_id = target_group_id
        observed_queue_id: Optional[str] = None

        def build_batch(start: int) -> list[dict]:
            batch = []
            for offset, item_params in enumerate(params_list[start : start + batch_size]):
                item = dict(item_params)
                if submission_idempotency_key is not None:
                    global_index = start + offset
                    item["__ap_idem_item_key"] = _idempotency_item_key(
                        template=template,
                        params=item_params,
                        global_index=global_index,
                        overrides=overrides_dict,
                        agenthub_revision=client.config.agenthub_ref,
                        enable_otel_tracing=enable_otel_tracing,
                        runner=runner,
                        runner_options=runner_options_dict,
                        model_base_url_collection=model_base_url_collection_list,
                        queue=queue,
                        account_pool=account_pool,
                        resource_profile_id=resource_profile_id,
                        **({"ak_id": ak_id} if ak_id is not None else {}),
                        **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                        max_failure_retries=max_failure_retries,
                    )
                batch.append(item)
            return batch

        if job_spec_flag:
            payload = client.build_create_job_body(
                **({"transparency": transparency} if transparency is not None else {}),
                template=template,
                params_list=[dict(p) for p in params_list],
                dataset=dataset,
                suite_name=suite_name,
                tags=tags_list,
                overrides=overrides_dict,
                max_concurrency=concurrency,
                group_id=target_group_id,
                queue=queue,
                quota_id=quota_id,
                policy_id=concurrency_policy_id,
                model_base_url_collection=model_base_url_collection_list,
                group_post_process=group_post_process_dict,
                datasources=datasources_list,
                enable_otel_tracing=enable_otel_tracing,
                runner=runner,
                runner_options=runner_options_dict,
                max_failure_retries=max_failure_retries,
                priority=priority,
                priority_weight=priority_weight,
                resource_mode=resource_mode,
                disable_loongcollector=disable_loongcollector,
                credential_type=credential_type,
                account_pool=account_pool,
                resource_profile_id=resource_profile_id,
                **({"ak_id": ak_id} if ak_id is not None else {}),
                **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                checkpoint_id=checkpoint_id,
                checkpoint_path=checkpoint_path,
                checkpoint=checkpoint_dict,
                benchmark=benchmark,
                experiment=experiment,
            )
            _emit_dry_run_warnings(dry_run_warnings)
            _print_formatted(payload, "json" if output_format == "plain" else output_format)
            return

        if dry_run:
            payloads = []
            for start in range(0, total_count, batch_size):
                batch = build_batch(start)
                payloads.append(
                    client.build_create_job_body(
                        **({"transparency": transparency} if transparency is not None else {}),
                        template=template,
                        params_list=batch,
                        dataset=dataset,
                        suite_name=suite_name,
                        tags=tags_list,
                        overrides=overrides_dict,
                        max_concurrency=concurrency,
                        group_id=target_group_id,
                        queue=queue,
                        quota_id=quota_id,
                        policy_id=concurrency_policy_id,
                        model_base_url_collection=model_base_url_collection_list,
                        group_post_process=group_post_process_dict,
                        datasources=datasources_list,
                        enable_otel_tracing=enable_otel_tracing,
                        runner=runner,
                        runner_options=runner_options_dict,
                        idempotency_key=submission_idempotency_key,
                        max_failure_retries=max_failure_retries,
                        priority=priority,
                        priority_weight=priority_weight,
                        resource_mode=resource_mode,
                        disable_loongcollector=disable_loongcollector,
                        credential_type=credential_type,
                        account_pool=account_pool,
                        resource_profile_id=resource_profile_id,
                        **({"ak_id": ak_id} if ak_id is not None else {}),
                        **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                        checkpoint_id=checkpoint_id,
                        checkpoint_path=checkpoint_path,
                        checkpoint=checkpoint_dict,
                        benchmark=benchmark,
                        experiment=experiment,
                    )
                )
            _emit_dry_run_warnings(dry_run_warnings)
            _print_job_create_dry_run(
                client,
                payloads,
                output_format=output_format,
            )
            return

        try:
            with _job_create_progress() as progress:
                task_id = progress.add_task(
                    "Submitting jobs",
                    total=total_count,
                    current_job=f"group={target_group_id}" if target_group_id else "",
                    current_stage=f"batch_size={batch_size}",
                )
                for batch_index, start in enumerate(range(0, total_count, batch_size)):
                    batch = build_batch(start)
                    batch_end = start + len(batch)
                    progress.update(
                        task_id,
                        current_stage=f"batch {batch_index + 1}: {start + 1}-{batch_end}/{total_count}",
                    )
                    batch_result = client.create_job(
                        **({"transparency": transparency} if transparency is not None else {}),
                        template=template,
                        params_list=batch,
                        dataset=dataset,
                        suite_name=suite_name,
                        tags=tags_list,
                        overrides=overrides_dict,
                        max_concurrency=concurrency,
                        group_id=target_group_id,
                        queue=queue,
                        quota_id=quota_id,
                        policy_id=concurrency_policy_id,
                        model_base_url_collection=model_base_url_collection_list,
                        datasources=datasources_list,
                        enable_otel_tracing=enable_otel_tracing,
                        runner=runner,
                        runner_options=runner_options_dict,
                        idempotency_key=submission_idempotency_key,
                        max_failure_retries=max_failure_retries,
                        priority=priority,
                        priority_weight=priority_weight,
                        resource_mode=resource_mode,
                        disable_loongcollector=disable_loongcollector,
                        credential_type=credential_type,
                        account_pool=account_pool,
                        resource_profile_id=resource_profile_id,
                        **({"ak_id": ak_id} if ak_id is not None else {}),
                        **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                        checkpoint_id=checkpoint_id,
                        checkpoint_path=checkpoint_path,
                        checkpoint=checkpoint_dict,
                        benchmark=benchmark,
                        experiment=experiment,
                        timeout=timeout,
                        **post_process_kwargs,
                    )
                    require_managed_ak_ack(batch_result, ak_id)
                    observed_ak_ids.update(response_ak_ids(batch_result))
                    for batch_job in batch_result.get("jobs", []):
                        observed_ak_ids.update(response_ak_ids(batch_job))
                    _require_resource_profile_ack(batch_result, resource_profile_id)
                    batch_group_id = batch_result.get("group_id")
                    if not observed_group_id and batch_group_id:
                        observed_group_id = batch_group_id
                    server_ack_idempotency = (
                        batch_result.get("idempotency_key") == submission_idempotency_key
                    )
                    if not target_group_id and not server_ack_idempotency and batch_group_id:
                        target_group_id = batch_group_id
                    qid = batch_result.get("queue_id")
                    if qid is not None:
                        observed_queue_id = qid

                    batch_submitted = int(batch_result.get("submitted") or 0)
                    batch_failed = int(batch_result.get("failed") or 0)
                    total_submitted += batch_submitted
                    total_failed += batch_failed
                    batch_results.append(
                        {
                            "batch": batch_index,
                            "start": start,
                            "end": batch_end,
                            "total": len(batch),
                            "submitted": batch_submitted,
                            "failed": batch_failed,
                        }
                    )
                    progress.update(
                        task_id,
                        completed=batch_end,
                        current_job=f"group={observed_group_id}" if observed_group_id else "",
                        current_stage=f"submitted={total_submitted} failed={total_failed}",
                    )
        except ManagedAKProtocolError as exc:
            _emit_error(str(exc))
            raise typer.Exit(1) from None
        except Exception:
            emit_retry_hint_once()
            raise

        result = {
            "group_id": observed_group_id,
            "queue_id": observed_queue_id,
            "total": total_count,
            "submitted": total_submitted,
            "failed": total_failed,
            "batches": batch_results,
        }
        result["ak_ids"] = sorted(observed_ak_ids)
        if submission_idempotency_key is not None:
            result["idempotency_key"] = submission_idempotency_key
        if resource_profile_id is not None:
            result["resource_profile_id"] = resource_profile_id
        if output_format == "plain":
            print("[green]Batch jobs submitted:[/]")
            print(f"  group_id: {result.get('group_id')}")
            if result.get("queue_id") is not None:
                print(f"  queue_id: {result.get('queue_id')}")
            if ak_id is not None:
                print(f"  ak_ids: {response_ak_ids(result)}")
            if resource_profile_id is not None:
                print(f"  resource_profile_id: {resource_profile_id}")
            if submission_idempotency_key is not None:
                print(f"  idempotency_key: {result.get('idempotency_key')}")
            print(f"  total: {result.get('total')}")
            print(f"  submitted: {result.get('submitted')}")
            print(f"  failed: {result.get('failed')}")
    else:
        if job_spec_flag:
            payload = client.build_create_job_body(
                **({"transparency": transparency} if transparency is not None else {}),
                template=template,
                params=params_dict,
                dataset=dataset,
                suite_name=suite_name,
                tags=tags_list,
                overrides=overrides_dict,
                group_id=group_id,
                queue=queue,
                quota_id=quota_id,
                policy_id=concurrency_policy_id,
                group_post_process=group_post_process_dict,
                datasources=datasources_list,
                enable_otel_tracing=enable_otel_tracing,
                runner=runner,
                runner_options=runner_options_dict,
                max_failure_retries=max_failure_retries,
                priority=priority,
                priority_weight=priority_weight,
                resource_mode=resource_mode,
                disable_loongcollector=disable_loongcollector,
                credential_type=credential_type,
                account_pool=account_pool,
                resource_profile_id=resource_profile_id,
                **({"ak_id": ak_id} if ak_id is not None else {}),
                **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                checkpoint_id=checkpoint_id,
                checkpoint_path=checkpoint_path,
                checkpoint=checkpoint_dict,
                benchmark=benchmark,
                experiment=experiment,
            )
            _emit_dry_run_warnings(dry_run_warnings)
            _print_formatted(payload, "json" if output_format == "plain" else output_format)
            return

        if dry_run:
            payload = client.build_create_job_body(
                **({"transparency": transparency} if transparency is not None else {}),
                template=template,
                params=params_dict,
                dataset=dataset,
                suite_name=suite_name,
                tags=tags_list,
                overrides=overrides_dict,
                group_id=group_id,
                queue=queue,
                quota_id=quota_id,
                policy_id=concurrency_policy_id,
                group_post_process=group_post_process_dict,
                datasources=datasources_list,
                enable_otel_tracing=enable_otel_tracing,
                runner=runner,
                runner_options=runner_options_dict,
                idempotency_key=submission_idempotency_key,
                max_failure_retries=max_failure_retries,
                priority=priority,
                priority_weight=priority_weight,
                resource_mode=resource_mode,
                disable_loongcollector=disable_loongcollector,
                credential_type=credential_type,
                account_pool=account_pool,
                resource_profile_id=resource_profile_id,
                **({"ak_id": ak_id} if ak_id is not None else {}),
                **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                checkpoint_id=checkpoint_id,
                checkpoint_path=checkpoint_path,
                checkpoint=checkpoint_dict,
                benchmark=benchmark,
                experiment=experiment,
            )
            _emit_dry_run_warnings(dry_run_warnings)
            _print_job_create_dry_run(
                client,
                [payload],
                output_format=output_format,
            )
            return

        try:
            with _job_create_progress() as progress:
                task_id = progress.add_task(
                    "Submitting job",
                    total=1,
                    current_job="",
                    current_stage="submitting",
                )
                result = client.create_job(
                    **({"transparency": transparency} if transparency is not None else {}),
                    template=template,
                    params=params_dict,
                    dataset=dataset,
                    suite_name=suite_name,
                    tags=tags_list,
                    overrides=overrides_dict,
                    group_id=group_id,
                    queue=queue,
                    quota_id=quota_id,
                    policy_id=concurrency_policy_id,
                    datasources=datasources_list,
                    enable_otel_tracing=enable_otel_tracing,
                    runner=runner,
                    runner_options=runner_options_dict,
                    idempotency_key=submission_idempotency_key,
                    max_failure_retries=max_failure_retries,
                    priority=priority,
                    priority_weight=priority_weight,
                    resource_mode=resource_mode,
                    disable_loongcollector=disable_loongcollector,
                    credential_type=credential_type,
                    account_pool=account_pool,
                    resource_profile_id=resource_profile_id,
                    **({"ak_id": ak_id} if ak_id is not None else {}),
                    **({"ak_mode": ak_mode} if ak_mode != "auto" else {}),
                    checkpoint_id=checkpoint_id,
                    checkpoint_path=checkpoint_path,
                    checkpoint=checkpoint_dict,
                    benchmark=benchmark,
                    experiment=experiment,
                    timeout=timeout,
                    **post_process_kwargs,
                )
                require_managed_ak_ack(result, ak_id)
                _require_resource_profile_ack(result, resource_profile_id)
                jobs = result.get("jobs", [])
                if not jobs:
                    progress.update(task_id, completed=1, current_stage="submitted=0 failed=1")
                else:
                    job = jobs[0]
                    failed = 1 if job.get("status") == "Failed" else 0
                    submitted = 0 if failed else 1
                    progress.update(
                        task_id,
                        completed=1,
                        current_job=f"job={job.get('job_id')}" if job.get("job_id") else "",
                        current_stage=f"submitted={submitted} failed={failed}",
                    )
        except ManagedAKProtocolError as exc:
            _emit_error(str(exc))
            raise typer.Exit(1) from None
        except Exception:
            emit_retry_hint_once()
            raise
        jobs = result.get("jobs", [])
        if not jobs:
            typer.secho("error: job submission failed", fg="red", err=True)
            for err in result.get("errors", []):
                typer.echo(
                    f"  [{err.get('index')}] {err.get('instance_id')}: {err.get('error')}",
                    err=True,
                )
            emit_retry_hint_once()
            raise typer.Exit(1)

        if submission_idempotency_key is not None and not result.get("idempotency_key"):
            result["idempotency_key"] = submission_idempotency_key

        job = jobs[0]
        if output_format == "plain":
            print("[green]Job submitted:[/]")
            print(f"  job_id: {job.get('job_id')}")
            print(f"  status: {job.get('status')}")
            rq = result.get("queue_id") or job.get("queue_id")
            if rq is not None:
                print(f"  queue_id: {rq}")
            if submission_idempotency_key is not None:
                print(
                    f"  idempotency_key: {result.get('idempotency_key') or submission_idempotency_key}"
                )
            if result.get("group_id"):
                print(f"  group_id: {result.get('group_id')}")
            if ak_id is not None:
                print(f"  ak_ids: {response_ak_ids(result)}")
            if resource_profile_id is not None:
                print(f"  resource_profile_id: {resource_profile_id}")

    if wait:
        try:
            group_id = result.get("group_id")
            if group_id:
                _emit_progress(
                    f"Waiting for group to finish: {group_id} "
                    f"(interval={wait_interval}s, timeout={_format_wait_timeout(wait_timeout)})"
                )
                final_group = wait_for_group(
                    client,
                    group_id,
                    wait_interval,
                    timeout=wait_timeout,
                    printer=wait_printer,
                )
                wait_result = {
                    "type": "group",
                    "interval": wait_interval,
                    "timeout": wait_timeout,
                    "result": final_group,
                }
                if output_format == "plain":
                    stats = final_group.get("stats") or {}
                    print(f"[green]Group finished:[/] {group_id}")
                    print(f"  total: {stats.get('total', 0)}")
                    print(f"  succeeded: {stats.get('succeeded', 0)}")
                    print(f"  failed: {stats.get('failed', 0)}")
                    print(f"  cancelled: {stats.get('cancelled', 0)}")
            else:
                job = result.get("jobs", [{}])[0]
                job_id = job.get("job_id")
                _emit_progress(
                    f"Waiting for job to finish: {job_id} "
                    f"(interval={wait_interval}s, timeout={_format_wait_timeout(wait_timeout)})"
                )
                final_job = wait_for_job(
                    client,
                    job_id,
                    wait_interval,
                    timeout=wait_timeout,
                    printer=wait_printer,
                )
                wait_result = {
                    "type": "job",
                    "interval": wait_interval,
                    "timeout": wait_timeout,
                    "result": final_job,
                }
                if output_format == "plain":
                    print(f"[green]Job finished:[/] {job_id}")
                    print(f"  status: {final_job.get('status')}")
                    if final_job.get("failed_reason"):
                        print(f"  failed_reason: {final_job.get('failed_reason')}")
        except WaitTimeoutError as exc:
            emit_retry_hint_once()
            typer.echo(f"error: {exc}", err=True)
            raise typer.Exit(1)
    if output_format != "plain":
        payload = {"submission": result}
        if wait_result is not None:
            payload["wait"] = wait_result
        _print_formatted(payload, output_format)


@job_app.command("get")
def job_get(
    job_id: str = typer.Argument(..., help="Job ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    include_params: bool = typer.Option(
        False,
        "--include-params",
        help="Include submitted params with sensitive values masked",
    ),
    include_spec: bool = typer.Option(
        False,
        "--include-spec",
        help="Include masked rendered job spec data",
    ),
    spec_format: str = typer.Option(
        "json",
        "--spec-format",
        help="Spec format when including spec: json/yaml",
    ),
    field: Optional[str] = typer.Option(
        None,
        "--field",
        help="Print one field path, e.g. status, lifecycle.run_duration, params.model",
    ),
    owner: bool = typer.Option(
        False,
        "--owner",
        help="Show only the owner and authorization contact, without reading protected details",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show job details."""
    output_format = _normalize_output_format(output_format, default="json")
    spec_format = spec_format.lower()
    if spec_format not in {"json", "yaml"}:
        raise typer.BadParameter("--spec-format must be one of json/yaml")
    if field:
        include_params = include_params or _field_path_requires_params(field)
        include_spec = include_spec or _field_path_requires_spec(field)
        if field == "job_spec_data.spec_yaml":
            spec_format = "yaml"
    if owner and share_token is not None:
        raise typer.BadParameter("--owner cannot be combined with --share-token")
    client = _read_client(share_token)
    if owner and (include_params or include_spec or field):
        raise typer.BadParameter(
            "--owner cannot be combined with --include-params, --include-spec or --field"
        )
    if owner:
        result = client.get_job_access_contact(job_id)
        if output_format in {"plain", "table"}:
            _print_detail(result)
        else:
            _print_formatted(result, output_format)
        return
    result = client.get_job(
        job_id,
        include_params=include_params,
        include_spec=include_spec,
        spec_format=spec_format,
    )
    if field:
        safe_job_name = (
            field == "job_name"
            and isinstance(result.get("job_id"), str)
            and bool(result["job_id"])
            and result.get("job_name") == result["job_id"]
        )
        if not safe_job_name and any(
            field == path or field.startswith(path + ".") or field.startswith(path + "[")
            for path in (result.get("restricted_fields") or [])
        ):
            _emit_error(f"field hidden: {field}; Group Reader access is required")
            raise typer.Exit(1)
        try:
            value = _extract_field(result, field)
        except ValueError as exc:
            raise typer.BadParameter(str(exc)) from exc
        except KeyError:
            _emit_error(f"field not found: {field}")
            raise typer.Exit(1)
        _print_field_value(value, output_format)
        return
    if output_format == "plain":
        _print_job_get_plain(result)
        return
    _print_formatted(result, output_format)


@job_app.command("containers")
def job_containers(
    job_id: str = typer.Argument(..., help="Job ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List container names for a job."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = _read_client(share_token)
    result = client.get_job_containers(job_id)
    if output_format == "table":
        _print_records_table(result)
    else:
        _print_formatted(result, output_format)


def _format_log_line(entry) -> str:
    """Render a single log entry from the logs API."""
    if isinstance(entry, dict):
        return entry.get("timestamp", "") + "  | " + entry.get("content", "")
    return str(entry)


def _fetch_job_logs_for_tail(client, job_id: str, container: Optional[str]):
    """Fetch all paginated logs so --tail can truncate locally."""
    all_logs = []
    offset = 0
    page_size = 500

    while True:
        result = client.get_job_logs(
            job_id=job_id,
            container=container,
            offset=offset,
            limit=page_size,
        )
        logs = result.get("logs", [])
        if isinstance(logs, list):
            all_logs.extend(logs)
        else:
            return logs

        next_offset = result.get("next_offset")
        if next_offset is None or next_offset <= offset:
            break
        offset = next_offset

    return all_logs


def _print_tail_logs(logs, tail: int) -> None:
    """Print the last N log entries returned by the CLI-side tail fallback."""
    if isinstance(logs, list):
        for log_line in logs[-tail:]:
            print(_format_log_line(log_line))
        return

    if isinstance(logs, str):
        lines = logs.splitlines()
        selected = lines[-tail:]
        if selected:
            print("\n".join(selected))
        return

    print(logs)


@job_app.command("logs")
def job_logs(
    job_id: str = typer.Argument(..., help="Job ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    container: Optional[str] = typer.Option("main", "--container", "-c", help="Container name"),
    tail: Optional[int] = typer.Option(None, "--tail", "-n", help="Show only the last N log lines"),
    follow: bool = typer.Option(
        False, "--follow", "-f", is_flag=True, help="Follow logs until the job finishes"
    ),
    offset: Optional[int] = typer.Option(0, "--offset", "-o", help="Starting log line offset"),
    limit: Optional[int] = typer.Option(
        500, "--limit", "-l", help="Number of log lines to request"
    ),
):
    """Show job logs."""
    client = _read_client(share_token)

    if tail is not None:
        if tail <= 0:
            raise typer.BadParameter("--tail must be >= 1")
        if follow:
            raise typer.BadParameter("--tail cannot be used with --follow")
        logs = _fetch_job_logs_for_tail(client, job_id, container=container)
        _print_tail_logs(logs, tail)
        return

    if follow:
        # Poll logs until no next offset is returned.
        import time

        offset = 0

        while True:
            result = client.get_job_logs(
                job_id=job_id,
                container=container,
                offset=offset,
                limit=500,
            )

            logs = result.get("logs", [])
            if isinstance(logs, list):
                for log_line in logs:
                    print(_format_log_line(log_line))
            else:
                print(logs)

            next_offset = result.get("next_offset")
            if next_offset is not None:
                offset = next_offset
            else:
                break

            time.sleep(1)
    else:
        result = client.get_job_logs(
            job_id=job_id,
            container=container,
            offset=offset,
            limit=limit,
        )

        print(f"[{result.get('job_id')}] - Container: {result.get('container', 'all')}")
        print(
            f"Offset: {result.get('offset', offset)}, Next Offset: {result.get('next_offset')}, Limit: {result.get('limit', limit)}"
        )
        print("=" * 50)

        logs = result.get("logs", [])
        if isinstance(logs, list):
            for log_line in logs:
                print(_format_log_line(log_line))
        else:
            print(logs)


@job_app.command("events")
def job_events(
    job_id: str = typer.Argument(..., help="Job ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    container: Optional[str] = typer.Option(None, "--container", "-c", help="Container name"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show job events."""
    output_format = _normalize_output_format(output_format)
    client = _read_client(share_token)
    result = client.get_job_events(job_id, container=container)
    if output_format == "plain":
        _print_job_events_plain(result)
    else:
        _print_formatted(result, output_format)


@job_app.command("metrics")
def job_metrics(
    job_id: str = typer.Argument(..., help="Job ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show job metrics."""
    output_format = _normalize_output_format(output_format)
    client = _read_client(share_token)
    result = client.get_job_metrics(job_id)
    if output_format == "plain":
        _print_json(result)
    else:
        _print_formatted(result, output_format)


@job_app.command("cancel")
def job_cancel(job_ids: List[str] = typer.Argument(..., help="Job IDs")):
    """Cancel one or more jobs."""
    client = get_client()
    results = [client.cancel_job(job_id) for job_id in job_ids]
    for index, result in enumerate(results):
        if index:
            print()
        _print_job_cancel_plain(result)


# ---- RBAC v2 实例级委托：job/group 访问授权（scope=resource 绑定） ----

_RESOURCE_ROLE_IDS = {
    ("job", "reader"): "built-in:job-reader",
    ("job", "writer"): "built-in:job-writer",
    ("group", "reader"): "built-in:group-reader",
    ("group", "blackbox-reader"): "built-in:blackbox-reader",
    ("group", "writer"): "built-in:group-writer",
    ("group", "cloner"): "built-in:group-cloner",
    ("group", "admin"): "built-in:group-admin",
}


def _resource_role_id(resource: str, role: str) -> str:
    key = (resource, (role or "").strip().lower())
    if key not in _RESOURCE_ROLE_IDS:
        choices = (
            "reader, writer, cloner, blackbox-reader, admin"
            if resource == "group"
            else "reader, writer"
        )
        raise typer.BadParameter(f"role must be one of: {choices}")
    return _RESOURCE_ROLE_IDS[key]


def _resolve_instance_workspace(client, resource: str, instance_id: str) -> str:
    """解析 job/group 实例所属 queue_id（= workspace_id），供绑定门控使用。"""
    doc = client.get_job(instance_id) if resource == "job" else client.get_group(instance_id)
    ws = (doc or {}).get("queue_id")
    if not ws:
        raise typer.BadParameter(
            f"could not resolve queue_id (workspace) for {resource} {instance_id}"
        )
    return str(ws)


def _access_principal(user: Optional[str], user_group: Optional[str]) -> tuple[str, str]:
    if user and user_group:
        raise typer.BadParameter("specify only one of --user / --user-group")
    if user:
        return "user", user
    if user_group:
        return "user_group", user_group
    raise typer.BadParameter("one of --user / --user-group is required")


def _grant_instance_access(resource, instance_id, role, user, user_group):
    client = get_client()
    role_id = _resource_role_id(resource, role)
    ptype, pid = _access_principal(user, user_group)
    ws = _resolve_instance_workspace(client, resource, instance_id)
    client.grant_resource_access(
        resource_type=resource,
        resource_id=instance_id,
        workspace_id=ws,
        role_id=role_id,
        principal_id=pid,
        principal_type=ptype,
    )
    print(f"[green]Granted[/] {role} on {resource} {instance_id} to {ptype}:{pid} (workspace {ws})")


def _revoke_instance_access(resource, instance_id, role, user, user_group):
    client = get_client()
    role_id = _resource_role_id(resource, role)
    ptype, pid = _access_principal(user, user_group)
    client.revoke_resource_access(
        resource_type=resource,
        resource_id=instance_id,
        role_id=role_id,
        principal_id=pid,
        principal_type=ptype,
    )
    print(f"[green]Revoked[/] {role} on {resource} {instance_id} from {ptype}:{pid}")


def _print_instance_access(resource, instance_id):
    client = get_client()
    result = client.list_resource_access(resource_type=resource, resource_id=instance_id)
    if isinstance(result, list):
        rows = result
    else:
        rows = (result or {}).get("data") or (result or {}).get("items") or []
    if not rows:
        print(f"No access bindings on {resource} {instance_id}")
        return
    print(f"Access bindings on {resource} {instance_id}:")
    for b in rows:
        print(f"  - {b.get('principal_type')}:{b.get('principal_id')}  role={b.get('role_id')}")


@job_app.command("grant")
def job_grant(
    job_id: str = typer.Argument(..., help="Job ID"),
    user: Optional[str] = typer.Option(None, "--user", help="Grant to this user_id"),
    user_group: Optional[str] = typer.Option(
        None, "--user-group", help="Grant to this user_group_id"
    ),
    role: str = typer.Option(
        "reader", "--role", help="reader (view) or writer (view+cancel/update)"
    ),
):
    """Grant a user/user-group access to a specific job (RBAC v2 instance delegation)."""
    _grant_instance_access("job", job_id, role, user, user_group)


@job_app.command("revoke")
def job_revoke(
    job_id: str = typer.Argument(..., help="Job ID"),
    user: Optional[str] = typer.Option(None, "--user", help="Revoke from this user_id"),
    user_group: Optional[str] = typer.Option(
        None, "--user-group", help="Revoke from this user_group_id"
    ),
    role: str = typer.Option("reader", "--role", help="reader or writer"),
):
    """Revoke a user/user-group's instance access to a specific job."""
    _revoke_instance_access("job", job_id, role, user, user_group)


@job_app.command("access-list")
def job_access_list(job_id: str = typer.Argument(..., help="Job ID")):
    """List who has instance-level access to a specific job."""
    _print_instance_access("job", job_id)


@job_app.command("retry")
def job_retry(
    job_ids: List[str] = typer.Argument(..., help="Job IDs"),
    params: Optional[str] = typer.Option(
        None,
        "--params",
        "-p",
        help="Params patch (JSON object) to shallow-merge into existing params",
    ),
    delete_params: Optional[str] = typer.Option(
        None,
        "--delete-params",
        help="Top-level params keys to delete (comma-separated)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Retry one or more terminal jobs."""
    output_format = _normalize_output_format(output_format)
    client = get_client()

    params_dict = None
    if params:
        try:
            params_dict = json.loads(params)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter("--params must be valid JSON") from exc
        if not isinstance(params_dict, dict):
            raise typer.BadParameter("--params must be a JSON object")

    delete_params_list = None
    if delete_params:
        delete_params_list = [item.strip() for item in delete_params.split(",") if item.strip()]
        if not delete_params_list:
            raise typer.BadParameter("--delete-params must include at least one key")

    retry_kwargs = {}
    if params_dict is not None:
        retry_kwargs["params"] = params_dict
    if delete_params_list:
        retry_kwargs["delete_params"] = delete_params_list

    results = [client.retry_job(job_id, **retry_kwargs) for job_id in job_ids]
    if output_format == "plain":
        for index, result in enumerate(results):
            if index:
                print()
            _print_job_retry_plain(result)
    else:
        payload = results[0] if len(results) == 1 else {"jobs": results}
        _print_formatted(payload, output_format)


@job_app.command("artifacts")
def job_artifacts(
    job_ids: str = typer.Argument(..., help="Job IDs (comma-separated for multiple)"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show job artifact download links."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = _read_client(share_token)
    ids = [jid.strip() for jid in job_ids.split(",")]
    results = client.get_job_artifacts(ids)
    if output_format == "table":
        _print_records_table(results)
    else:
        _print_formatted(results, output_format)


def _validate_export_timeout(value: float) -> float:
    import math

    if not math.isfinite(value) or value <= 0:
        raise typer.BadParameter("Timeout must be a finite number greater than zero")
    return value


def _export_channel_reporter(emit):
    """Report completed Jobs, including callbacks from Group worker threads."""
    from threading import Lock

    from rich.text import Text

    counts = {"oss": 0, "proxy": 0}
    lock = Lock()

    def report(job_id, status, channel):
        with lock:
            suffix = ""
            if status == "downloaded" and channel in counts:
                counts[channel] += 1
                suffix = f"  channel={channel}"
            emit(Text(f"{job_id}  {status}{suffix}"))

    return report, counts


@job_app.command("export")
def job_export(
    job_id: str = typer.Argument(..., help="Job ID or comma-separated Job IDs"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Export with a share token"
    ),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory"),
    workers: int = typer.Option(
        1, "--workers", "-w", min=1, help="Number of concurrent export workers"
    ),
    timeout: float = typer.Option(
        300,
        "--timeout",
        callback=_validate_export_timeout,
        help="SDK request timeout in seconds, not the total export duration",
    ),
    logs: bool = typer.Option(False, "--logs", help="Include container logs"),
    events: bool = typer.Option(False, "--events", help="Include events"),
    no_extract_artifacts: bool = typer.Option(
        False,
        "--no-extract-artifacts",
        help="Download result.tgz without extracting it into artifacts/",
    ),
):
    """Export job artifacts to a local directory. Use --logs/--events to include logs and events."""
    ids = list(dict.fromkeys(value.strip() for value in job_id.split(",")))
    if not all(ids):
        raise typer.BadParameter("Job IDs must not be empty", param_hint="job_id")
    client = _read_client(share_token)
    if len(ids) > 1:
        report, channels = _export_channel_reporter(print)
        dest, summary = export_jobs(
            client,
            ids,
            output,
            workers=workers,
            result_callback=report,
            timeout=timeout,
            include_logs=logs,
            include_events=events,
            extract_artifacts=not no_extract_artifacts,
        )
        print(
            f"Jobs exported: downloaded={summary.downloaded} "
            f"skipped={summary.skipped} failed={len(summary.failures)}"
        )
        print(f"channels: oss={channels['oss']} proxy={channels['proxy']}")
        print(f"  path: {dest}")
        for failed_id, error in summary.failures.items():
            print(f"[red]Failed job {failed_id}:[/] {error}")
        if summary.failures:
            raise typer.Exit(code=1)
        return
    job_id = ids[0]
    result = {}
    dest = export_job(
        client,
        job_id,
        output,
        result_callback=lambda jid, status, channel: result.update(status=status, channel=channel),
        timeout=timeout,
        include_logs=logs,
        include_events=events,
        extract_artifacts=not no_extract_artifacts,
    )
    print(f"[green]Job exported:[/] {job_id}")
    print(f"  path: {dest}")
    if result.get("channel") in {"oss", "proxy"} and result.get("status") == "downloaded":
        print(f"  channel: {result['channel']}")


@job_app.command("wait")
def job_wait(
    job_id: str = typer.Argument(..., help="Job ID"),
    interval: float = typer.Option(
        5.0, "--interval", "-i", min=0.1, help="Polling interval (seconds)"
    ),
    timeout: Optional[float] = typer.Option(
        None,
        "--timeout",
        "--wait-timeout",
        min=0.0,
        help="Maximum seconds to wait; omit to wait indefinitely",
    ),
):
    """Poll until the job finishes."""
    client = get_client()
    try:
        result = wait_for_job(client, job_id, interval, timeout=timeout)
    except WaitTimeoutError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1)
    print(f"[green]Job finished:[/] {job_id}")
    print(f"  status: {result.get('status')}")
    if result.get("failed_reason"):
        print(f"  failed_reason: {result.get('failed_reason')}")


# 交互式命令白名单：仅这三种进入交互终端
_INTERACTIVE_COMMANDS = {"bash", "bin/bash", "/bin/bash"}


def _is_local_cluster() -> bool:
    """检测当前是否为本地 Docker 模式（X-Cluster:local）。

    通过最终 CLI 配置判断，支持 --cluster、AP_CLUSTER 和 AP_HEADERS。
    """
    from ap_client import api as _api

    config = get_config(cluster=_api._cluster_override)
    cluster = _extract_cluster(config.headers)
    return bool(cluster and cluster.lower() == "local")


def _find_docker_container(job_id: str, target: str = "main") -> Optional[str]:
    """在本地 Docker 环境中查找 job 对应的容器名称。

    通过 docker ps 过滤包含 job_id 的容器，返回匹配的容器 ID 或名称。
    本地模式下容器名称通常包含 job_id。

    Args:
        job_id: 任务 ID
        target: 容器名称（main / sidecar 等）

    Returns:
        匹配的容器 ID 或名称，未找到返回 None
    """
    import subprocess as sp

    try:
        # 通过 docker ps 列出包含 job_id 的运行中容器
        result = sp.run(
            ["docker", "ps", "--filter", f"name={job_id}", "--format", "{{.ID}} {{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            typer.echo(f"docker ps failed: {result.stderr.strip()}", err=True)
            return None

        candidates = []
        for line in result.stdout.strip().splitlines():
            if not line.strip():
                continue
            parts = line.strip().split(" ", 1)
            container_id = parts[0]
            container_names = parts[1] if len(parts) > 1 else ""
            # 优先匹配包含 target 容器名的（如 main / sidecar）
            if target != "main" and target in container_names:
                return container_id
            candidates.append(container_id)

        # 未匹配到特定 target，返回第一个候选
        if candidates:
            return candidates[0]

    except FileNotFoundError:
        typer.echo("docker command not found; make sure Docker is installed and running", err=True)
    except sp.TimeoutExpired:
        typer.echo("docker ps timed out", err=True)
    except Exception as e:
        typer.echo(f"failed to find the Docker container: {e}", err=True)

    return None


def _local_docker_exec(job_id: str, target: str, command: list) -> None:
    """本地 Docker 模式：使用 docker exec 代替 kubectl exec 进入容器。

    Args:
        job_id: 任务 ID
        target: 容器名称
        command: 要执行的命令列表
    """
    import subprocess as sp

    container = _find_docker_container(job_id, target)
    if not container:
        typer.echo(
            f"No Docker container found for job '{job_id}'. "
            f"Make sure the container is running (docker ps | grep {job_id})",
            err=True,
        )
        raise typer.Exit(1)

    # 构造 docker exec 命令
    is_interactive = command[0] in _INTERACTIVE_COMMANDS
    docker_cmd = ["docker", "exec"]
    if is_interactive:
        # 交互式模式：分配伪终端
        docker_cmd.extend(["-it", container] + command)
    else:
        # 非交互模式：直接执行
        docker_cmd.extend([container] + command)

    typer.echo(f"[local Docker mode] running: {' '.join(docker_cmd)}", err=True)
    result = sp.run(docker_cmd)
    raise typer.Exit(result.returncode)


@job_app.command(
    "exec",
    context_settings={
        "allow_extra_args": True,
        "allow_interspersed_args": True,
        "ignore_unknown_options": True,
    },
)
def job_exec(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
    target: str = typer.Option("main", "-t", "--target", help="Container name"),
    list_containers: bool = typer.Option(
        False, "--list", help="Only list containers available for exec"
    ),
):
    """Execute a command in a container.

    Supports K8s Pod (default) and local Docker modes:
    - When AP_HEADERS contains X-Cluster:local, runs docker exec against the local container
    - Otherwise connects to the K8s Pod via a WebSocket terminal

    Interactive commands (bash, bin/bash, /bin/bash) open an interactive terminal;
    all other commands run non-interactively and print their output.

    Examples:
      ap job exec <job_id> bash              # interactive terminal
      ap job exec <job_id> ls -la            # non-interactive execution
      ap job exec <job_id> -t sidecar bash   # specify a container
    """
    # 本地 Docker 模式检测
    is_local = _is_local_cluster()

    if is_local and list_containers:
        # 本地模式：通过 docker ps 列出容器
        import subprocess as sp

        result = sp.run(
            [
                "docker",
                "ps",
                "--filter",
                f"name={job_id}",
                "--format",
                "table {{.ID}}\t{{.Names}}\t{{.Status}}",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            typer.echo(f"docker ps failed: {result.stderr.strip()}", err=True)
            raise typer.Exit(1)
        typer.echo(result.stdout)
        raise typer.Exit(0)

    client = get_client()

    if list_containers:
        result = client.get_job_containers(job_id)
        _print_json(result)
        raise typer.Exit(0)

    # job_id 后的剩余参数作为 command，无参数时默认 bash
    command = ctx.args if ctx.args else ["bash"]

    # 本地 Docker 模式：直接使用 docker exec，跳过 WebSocket 和权限检查
    if is_local:
        _local_docker_exec(job_id, target, command)
        return

    # 检查 pod exec 权限
    check = client._get(f"/jobs/{quote(job_id)}/pod-exec/check")
    if not check.get("allowed"):
        typer.echo(f"Pod exec not allowed: {check.get('reason', 'unknown reason')}", err=True)
        raise typer.Exit(1)

    # 验证容器存在
    containers_resp = client.get_job_containers(job_id)
    available = containers_resp.get("containers", [])
    if target not in available:
        typer.echo(
            f"container '{target}' does not exist. Available containers: {', '.join(available)}",
            err=True,
        )
        raise typer.Exit(1)

    import asyncio

    # 根据命令判断交互/非交互模式
    if command[0] in _INTERACTIVE_COMMANDS:
        asyncio.run(_interactive_terminal(client, job_id, target))
    else:
        asyncio.run(_non_interactive_exec(client, job_id, target, command))


# ==================== Group operations ====================


def _print_benchmark_list_plain(benchmarks: list) -> None:
    """Render the benchmark list as a table; teacher_directions comma-joined."""
    rows = [
        {
            "id": b.get("id"),
            "name": b.get("name"),
            "teacher_directions": ", ".join(str(d) for d in (b.get("teacher_directions") or [])),
        }
        for b in benchmarks
        if isinstance(b, dict)
    ]
    _print_plain_table(
        rows,
        [("id", "ID"), ("name", "NAME"), ("teacher_directions", "TEACHER_DIRECTIONS")],
    )


@benchmark_app.command("list")
def benchmark_list(
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List benchmarks from the central benchmark registry."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client()
    result = client.list_benchmarks()
    if output_format == "table":
        _print_benchmark_list_plain(result)
    else:
        _print_formatted(result, output_format)


@benchmark_app.command("get")
def benchmark_get(
    name: str = typer.Argument(..., help="Benchmark name (exact match)"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show benchmark details."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client()
    result = client.get_benchmark(name)
    if output_format == "table":
        _print_detail(result)
    else:
        _print_formatted(result, output_format)


# ==================== Checkpoint operations ====================

_CHECKPOINT_LIST_AVAILABLE_COLUMNS = [
    "id",
    "uuid",
    "name",
    "model_id",
    "produce_stage_id",
    "storage_uri",
    "schema_version",
    "status",
    "create_time",
    "update_time",
]

_CHECKPOINT_LIST_COLUMNS = ["id", "name", "model_id", "status", "update_time"]


def _prepare_checkpoint_list_rows(checkpoints: list) -> list[dict]:
    rows: list[dict] = []
    for checkpoint in checkpoints:
        row = dict(checkpoint) if isinstance(checkpoint, dict) else {}
        row["storage_uri"] = row.get("storage_uri") or "-"
        row["create_time"] = row.get("create_time") or "-"
        row["update_time"] = row.get("update_time") or "-"
        rows.append(row)
    return rows


def _print_checkpoint_list_plain(
    result: dict, columns: Optional[list[str]] = None, rich: bool = False
) -> None:
    checkpoints = result.get("checkpoints", [])
    rows = _prepare_checkpoint_list_rows(checkpoints)
    selected_columns = columns or _CHECKPOINT_LIST_COLUMNS
    render = _print_rich_table if rich else _print_plain_table
    render(rows, [(column, column) for column in selected_columns])


def _print_checkpoint_get_plain(checkpoint: dict) -> None:
    typer.echo("Checkpoint")
    _print_key_values(
        [
            ("id", checkpoint.get("id")),
            ("uuid", checkpoint.get("uuid")),
            ("name", checkpoint.get("name")),
            ("model_id", checkpoint.get("model_id")),
            ("produce_stage_id", checkpoint.get("produce_stage_id")),
            ("storage_uri", checkpoint.get("storage_uri")),
            ("schema_version", checkpoint.get("schema_version")),
            ("status", checkpoint.get("status")),
            ("create_time", checkpoint.get("create_time")),
            ("update_time", checkpoint.get("update_time")),
        ],
        skip_empty=False,
    )


@checkpoint_app.command("list")
def checkpoint_list(
    name: Optional[str] = typer.Option(
        None, "--name", help="Filter by checkpoint name (exact match)"
    ),
    model_id: Optional[str] = typer.Option(
        None, "--model-id", help="Filter by model ID (exact match)"
    ),
    status: Optional[str] = typer.Option(None, "--status", help="Filter by status (exact match)"),
    uuid: Optional[str] = typer.Option(None, "--uuid", help="Filter by UUID (exact match)"),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(100, "--limit", help="Maximum number of entries to return"),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        help="Comma-separated columns to display: " + ", ".join(_CHECKPOINT_LIST_AVAILABLE_COLUMNS),
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List checkpoints from the local checkpoint registry."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    selected_columns = (
        _parse_columns_option(columns, available=_CHECKPOINT_LIST_AVAILABLE_COLUMNS)
        if output_format in ("plain", "table")
        else None
    )
    client = get_client()
    result = client.list_checkpoints(
        name=name, model_id=model_id, status=status, uuid=uuid, skip=skip, limit=limit
    )
    if output_format == "table":
        _print_checkpoint_list_plain(result, columns=selected_columns, rich=True)
    elif output_format == "plain":
        _print_checkpoint_list_plain(result, columns=selected_columns)
    else:
        _print_formatted(result, output_format)


@checkpoint_app.command("get")
def checkpoint_get(
    name: str = typer.Argument(..., help="Checkpoint name (exact match)"),
    field: Optional[str] = typer.Option(
        None,
        "--field",
        help="Print one field path, e.g. status, storage_uri, update_time",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show checkpoint details."""
    output_format = _normalize_output_format(output_format, default="json")
    client = get_client()
    result = client.get_checkpoint(name)
    if field:
        try:
            value = _extract_field(result, field)
        except ValueError as exc:
            raise typer.BadParameter(str(exc)) from exc
        except KeyError:
            _emit_error(f"field not found: {field}")
            raise typer.Exit(1)
        _print_field_value(value, output_format)
        return
    if output_format == "plain":
        _print_checkpoint_get_plain(result)
        return
    _print_formatted(result, output_format)


@group_app.command("create")
def group_create(
    transparency: Optional[str] = typer.Option(
        None,
        "--transparency",
        help="whitebox or blackbox; omit to inherit the Group/Profile default",
    ),
    idempotency_key: Optional[str] = typer.Option(
        None, "--idempotency-key", help="Reuse this key when retrying blackbox Group creation"
    ),
    ak_id: Optional[list[str]] = typer.Option(
        None, "--ak-id", help="Managed AK reference (repeatable) to associate with the Group"
    ),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Group name"),
    template: Optional[str] = typer.Option(
        None,
        "--template",
        help="Template name; required when enabling group PostProcess",
    ),
    agenthub_revision: Optional[str] = typer.Option(
        None,
        "--agenthub-revision",
        "--agenthub-ref",
        help="Agent-Hub branch/commit; defaults to AP_AGENTHUB_REF when set",
    ),
    queue: Optional[str] = typer.Option(
        None,
        "--queue-id",
        "--queue",
        "-q",
        help="Queue id (agent-platform-apiserver); omit to use server default (default)",
    ),
    max_concurrency: Optional[int] = typer.Option(
        None,
        "--max-concurrency",
        "-c",
        min=1,
        help="Maximum concurrent jobs. Server default: 50.",
    ),
    priority: Optional[str] = typer.Option(
        None,
        "--priority",
        help="Default priority inherited by Jobs: high or medium (server default: medium)",
    ),
    priority_weight: Optional[int] = typer.Option(
        None,
        "--priority-weight",
        min=0,
        max=10,
        help="Default priority weight inherited by Jobs, 0-10 (server default: 0)",
    ),
    eval_config: Optional[str] = typer.Option(
        None, "--eval-config", help="Evaluation config (JSON)"
    ),
    model_base_url_collection: Optional[str] = typer.Option(
        None,
        "--model-base-url-collection",
        help="Model base URL collection for server-side load balancing (JSON array or comma-separated)",
    ),
    model_base_url_file: Optional[str] = typer.Option(
        None,
        "--model-base-url-file",
        help="File path containing model base URL list (one URL per line), fallback for --model-base-url-collection",
    ),
    enable_post_process: bool = typer.Option(
        False,
        "--enable-post-process",
        help="Enable template-defined Group PostProcess with default params",
    ),
    group_post_process: Optional[str] = typer.Option(
        None,
        "--group-post-process",
        help="Full Group PostProcess config (JSON object)",
    ),
    dataset: Optional[str] = typer.Option(
        None, "--dataset", "-d", help="Dataset name (benchmark perspective)"
    ),
    tags: Optional[str] = typer.Option(None, "--tags", help="Tags (comma-separated)"),
    model_name: Optional[str] = typer.Option(
        None, "--model", "-m", help="Model name (benchmark perspective)"
    ),
    scaffold: Optional[str] = typer.Option(
        None, "--scaffold", "-s", help="Scaffold/agent name (benchmark perspective)"
    ),
    agent: Optional[str] = typer.Option(
        None,
        "--agent",
        help="Unified Agent config (JSON object)",
    ),
    meta_model: Optional[str] = typer.Option(
        None,
        "--meta-model",
        help="Meta model tag; omit to leave unset",
    ),
    meta_job_type: Optional[str] = typer.Option(
        None,
        "--meta-job-type",
        help="Meta job type tag: Eval-Eval (default) or Others",
    ),
    meta_teacher_direction: Optional[str] = typer.Option(
        None,
        "--meta-teacher-direction",
        help="Meta teacher direction tag; omit to derive from dataset_series; options: ap meta-teacher-direction list",
    ),
    meta_train_stage: Optional[str] = typer.Option(
        None,
        "--meta-train-stage",
        help="Meta train stage tag; omit to derive from dataset run_type; options: ap meta-train-stage list",
    ),
    benchmark: Optional[str] = typer.Option(
        None,
        "--benchmark",
        help="Benchmark name from the AP registry (see 'ap benchmark list')",
    ),
    checkpoint_id: Optional[str] = typer.Option(
        None,
        "--checkpoint-id",
        help="Checkpoint ID (reporting metadata)",
    ),
    checkpoint_id_alias: Optional[str] = typer.Option(
        None,
        "--check-point-id",
        "--ckpt-id",
        hidden=True,
        help="Alias of --checkpoint-id",
    ),
    checkpoint_path: Optional[str] = typer.Option(
        None,
        "--checkpoint-path",
        help="Checkpoint storage path/URI (reporting metadata)",
    ),
    checkpoint_path_alias: Optional[str] = typer.Option(
        None,
        "--check-point-path",
        "--ckpt-path",
        hidden=True,
        help="Alias of --checkpoint-path",
    ),
    checkpoint: Optional[str] = typer.Option(
        None,
        "--checkpoint",
        help="Checkpoint as JSON object; explicit id/path flags win",
    ),
    checkpoint_alias: Optional[str] = typer.Option(
        None,
        "--check-point",
        "--ckpt",
        hidden=True,
        help="Alias of --checkpoint",
    ),
    experiment: Optional[str] = typer.Option(
        None,
        "--experiment",
        help="Experiment name for score reporting; omit to skip",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Create a Group."""
    if transparency is not None and transparency not in {"whitebox", "blackbox"}:
        raise typer.BadParameter("Choose whitebox or blackbox", param_hint="--transparency")
    output_format = _normalize_output_format(output_format)
    if priority is not None and priority not in {"high", "medium"}:
        raise typer.BadParameter("--priority must be one of high/medium")
    try:
        for reference in ak_id or []:
            validate_ak_id(reference)
    except ValueError as exc:
        raise typer.BadParameter(str(exc), param_hint="--ak-id") from None
    if transparency == "blackbox" and idempotency_key is None:
        idempotency_key = str(uuid.uuid4())
    client = get_client()
    eval_config_dict = json.loads(eval_config) if eval_config else None
    group_post_process_dict = _parse_json_object(group_post_process, "--group-post-process")
    # Fold hidden alias flags into the canonical values (canonical wins)
    checkpoint_id = checkpoint_id or checkpoint_id_alias
    checkpoint_path = checkpoint_path or checkpoint_path_alias
    checkpoint = checkpoint or checkpoint_alias
    checkpoint_dict = _parse_json_object(checkpoint, "--checkpoint")
    agent_dict = _parse_json_object(agent, "--agent")

    wants_post_process = enable_post_process or group_post_process_dict is not None
    if wants_post_process and not template:
        _emit_error("--template is required when enabling Group PostProcess")
        raise typer.Exit(1)
    if enable_post_process and group_post_process_dict is None:
        group_post_process_dict = {}

    # Parse model_base_url_collection (supports JSON array or comma-separated string)
    model_base_url_collection_list = None
    if model_base_url_collection:
        try:
            model_base_url_collection_list = json.loads(model_base_url_collection)
            if not isinstance(model_base_url_collection_list, list):
                print("[red]error: --model-base-url-collection must be a JSON array[/]")
                raise typer.Exit(1)
        except json.JSONDecodeError:
            # Try as comma-separated string
            model_base_url_collection_list = [
                u.strip() for u in model_base_url_collection.split(",") if u.strip()
            ] or None

    # Fallback to model_base_url_file
    if not model_base_url_collection_list and model_base_url_file:
        try:
            model_base_url_collection_list = [
                line.strip()
                for line in Path(model_base_url_file).read_text(encoding="utf-8").splitlines()
                if line.strip()
            ] or None
        except FileNotFoundError:
            print(f"[red]error: file not found: {model_base_url_file}[/]")
            raise typer.Exit(1)

    try:
        group_tags = _merge_meta_tags(
            _merge_job_tags(tags.split(",") if tags else None),
            meta_model=meta_model,
            meta_job_type=meta_job_type,
            meta_teacher_direction=meta_teacher_direction,
            meta_train_stage=meta_train_stage,
        )
    except ValueError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)

    try:
        result = client.create_group(
            **({"transparency": transparency} if transparency is not None else {}),
            **({"idempotency_key": idempotency_key} if idempotency_key is not None else {}),
            ak_ids=ak_id,
            name=name,
            tags=group_tags,
            template=template,
            agenthub_revision=agenthub_revision,
            queue_id=queue,  # CLI --queue / -q 走标准 queue_id 字段
            max_concurrency=max_concurrency,
            eval_config=eval_config_dict,
            model_base_url_collection=model_base_url_collection_list,
            group_post_process=group_post_process_dict,
            dataset=dataset,
            model=model_name,
            scaffold=scaffold,
            agent=agent_dict,
            checkpoint_id=checkpoint_id,
            checkpoint_path=checkpoint_path,
            checkpoint=checkpoint_dict,
            benchmark=benchmark,
            experiment=experiment,
            **({"priority": priority} if priority is not None else {}),
            **({"priority_weight": priority_weight} if priority_weight is not None else {}),
        )
    except APIError:
        if idempotency_key is not None:
            _emit_idempotency_retry_hint(
                f"Rerun your original command with --idempotency-key {shlex.quote(idempotency_key)}"
            )
        raise
    except ManagedAKProtocolError as exc:
        if idempotency_key is not None:
            _emit_idempotency_retry_hint(
                _build_job_create_retry_command(idempotency_key=idempotency_key)
            )
        _emit_error(str(exc))
        raise typer.Exit(1) from None
    if output_format == "plain":
        print("[green]Group created:[/]")
        print(f"  group_id: {result.get('group_id')}")
        print(f"  name: {result.get('name')}")
        if response_ak_ids(result):
            print(f"  ak_ids: {response_ak_ids(result)}")
        if result.get("queue_id") is not None:
            print(f"  queue_id: {result.get('queue_id')}")
        if result.get("priority") is not None:
            print(f"  priority: {result.get('priority')}")
        if result.get("priority_weight") is not None:
            print(f"  priority_weight: {result.get('priority_weight')}")
        if result.get("template") is not None:
            print(f"  template: {result.get('template')}")
        if result.get("agenthub_revision") is not None:
            print(f"  agenthub_revision: {result.get('agenthub_revision')}")
        if result.get("template_commit") is not None:
            print(f"  template_commit: {result.get('template_commit')}")
        if result.get("group_post_process_job_id") is not None:
            print(f"  group_post_process_job_id: {result.get('group_post_process_job_id')}")
        print(f"  max_concurrency: {result.get('max_concurrency')}")
        print(f"  strict: {result.get('strict')}")
        if result.get("eval_config") is not None:
            print(f"  eval_config: {json.dumps(result.get('eval_config'), ensure_ascii=False)}")
        if result.get("model_base_url_collection") is not None:
            print(
                "  model_base_url_collection: "
                f"{json.dumps(result.get('model_base_url_collection'), ensure_ascii=False)}"
            )
        if result.get("dataset"):
            print(f"  dataset: {result.get('dataset')}")
        if result.get("model"):
            print(f"  model: {result.get('model')}")
        if result.get("scaffold"):
            print(f"  scaffold: {result.get('scaffold')}")
        if result.get("benchmark"):
            print(f"  benchmark: {result.get('benchmark')}")
        if result.get("checkpoint"):
            print(f"  checkpoint: {json.dumps(result.get('checkpoint'), ensure_ascii=False)}")
        if result.get("experiment"):
            print(f"  experiment: {result.get('experiment')}")
        return
    _print_formatted(result, output_format)


@group_app.command("list")
def group_list(
    name: Optional[str] = typer.Option(None, "--name", help="Group name"),
    group_id: Optional[str] = typer.Option(None, "--group-id", help="Group ID"),
    ak_id: Optional[str] = typer.Option(
        None, "--ak-id", help="Filter groups containing this managed AK"
    ),
    user_id: Optional[str] = typer.Option(None, "--user-id", help="User ID"),
    user_name: Optional[str] = typer.Option(None, "--user-name", help="User name"),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(100, "--limit", help="Maximum number of entries to return"),
    profile: Optional[str] = typer.Option(
        None,
        "--profile",
        help="Filter groups by profile (accepts profile ID, profile name, or name:version)",
    ),
    dataset: Optional[str] = typer.Option(None, "--dataset", help="Dataset filter"),
    model: Optional[str] = typer.Option(None, "--model", help="Model filter"),
    scaffold: Optional[str] = typer.Option(None, "--scaffold", help="Scaffold/agent filter"),
    queue_id: Optional[str] = typer.Option(None, "--queue-id", help="Queue ID"),
    tag: Optional[list[str]] = typer.Option(
        None, "--tag", help="Filter by tag (repeatable; multiple tags default to AND)"
    ),
    meta_model: Optional[str] = typer.Option(None, "--meta-model", help="Filter by meta_model"),
    meta_job_type: Optional[str] = typer.Option(
        None, "--meta-job-type", help="Filter by meta_job_type"
    ),
    created_after: Optional[str] = typer.Option(
        None, "--created-after", help=f"Filter by lower bound of created_at ({_ISO_TIME_HELP})"
    ),
    created_before: Optional[str] = typer.Option(
        None, "--created-before", help=f"Filter by upper bound of created_at ({_ISO_TIME_HELP})"
    ),
    prefix_match: bool = typer.Option(
        False,
        "--prefix-match",
        help="Use prefix match for name/group-id/user-name/dataset/model/scaffold filters",
    ),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        help=_GROUP_LIST_COLUMNS_HELP,
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List Groups."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    selected_columns = (
        _parse_group_columns_option(columns) if output_format in ("plain", "table") else None
    )
    client = get_client()
    result = client.list_groups(
        skip=skip,
        limit=limit,
        profile=profile,
        name=name,
        group_id=group_id,
        **({"ak_id": ak_id} if ak_id is not None else {}),
        user_id=user_id,
        user_name=user_name,
        dataset=dataset,
        model=model,
        scaffold=scaffold,
        queue_id=queue_id,
        **({"tag": tag} if tag is not None else {}),
        **({"meta_model": meta_model} if meta_model is not None else {}),
        **({"meta_job_type": meta_job_type} if meta_job_type is not None else {}),
        created_after=created_after,
        created_before=created_before,
        prefix_match=prefix_match,
    )
    if output_format == "table":
        _print_group_list_plain(result, columns=selected_columns, rich=True)
    elif output_format == "plain":
        _print_group_list_plain(result, columns=selected_columns)
    else:
        _print_formatted(result, output_format)


@group_app.command("get")
def group_get(
    group_id: str = typer.Argument(..., help="Group ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    owner: bool = typer.Option(
        False,
        "--owner",
        help="Show only the owner and authorization contact, without reading protected details",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show Group details."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    if owner and share_token is not None:
        raise typer.BadParameter("--owner cannot be combined with --share-token")
    client = _read_client(share_token, group_id if share_token else None)
    if owner:
        result = client.get_group_access_contact(group_id)
        if output_format in {"plain", "table"}:
            _print_detail(result)
        else:
            _print_formatted(result, output_format)
        return
    result = client.get_group(group_id)
    if output_format == "table":
        _print_detail(result)
    else:
        _print_formatted(result, output_format)


@group_app.command("clone")
def group_clone(
    source_group_id: str = typer.Argument(..., help="Source Group ID"),
    source_cluster: Optional[str] = typer.Option(
        None,
        "--source-cluster",
        help="Source cluster slug; omit for a same-cluster clone",
    ),
    target_cluster: Optional[str] = typer.Option(
        None,
        "--target-cluster",
        help="Target cluster; defaults to --cluster/AP_CLUSTER/AP_HEADERS",
    ),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Target Group name"),
    queue_id: Optional[str] = typer.Option(
        None,
        "--queue-id",
        "--queue",
        "-q",
        help="Target queue ID",
    ),
    max_concurrency: Optional[int] = typer.Option(
        None,
        "--max-concurrency",
        "-c",
        min=1,
        help="Target Group maximum concurrency",
    ),
    model_base_url_collection: Optional[str] = typer.Option(
        None,
        "--model-base-url-collection",
        help="Comma-separated replacement model base URL pool for the target Group",
    ),
    clear_model_base_url_collection: bool = typer.Option(
        False,
        "--clear-model-base-url-collection",
        help="Drop the inherited model base URL pool so Job-level model_base_url params take effect",
    ),
    params: Optional[str] = typer.Option(
        None,
        "--params",
        "-p",
        help="Top-level Job params patch (JSON object)",
    ),
    delete_param: Optional[list[str]] = typer.Option(
        None,
        "--delete-param",
        help="Delete a top-level Job param (repeatable)",
    ),
    overrides: Optional[str] = typer.Option(
        None,
        "--overrides",
        help="Job overrides patch (JSON object)",
    ),
    credential_type: Optional[str] = typer.Option(
        None,
        "--credential-type",
        help="Target credential type",
    ),
    resource_mappings: Optional[str] = typer.Option(
        None,
        "--resource-mappings",
        help="Cross-cluster resource mappings (JSON object)",
    ),
    resource_mappings_file: Optional[str] = typer.Option(
        None,
        "--resource-mappings-file",
        help="File containing the resource mappings JSON object",
    ),
    source_mode: str = typer.Option(
        "terminal_only",
        "--source-mode",
        help="Source mode: terminal_only or snapshot",
    ),
    start_paused: Optional[bool] = typer.Option(
        None,
        "--start-paused/--activate",
        help="Override scheduling: local defaults active, cross-cluster defaults paused",
    ),
    trials: Optional[int] = typer.Option(
        None,
        "--trials",
        min=1,
        help="Target copies per logical instance; identical source trials replicas are "
        "deduplicated first (default 1)",
    ),
    idempotency_key: Optional[str] = typer.Option(
        None,
        "--idempotency-key",
        help="UUID4 retry key; generated once when omitted",
    ),
    preview_only: bool = typer.Option(
        False,
        "--preview-only",
        help="Validate and print the non-sensitive preview without creating anything",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip the confirmation prompt"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/json/yaml",
    ),
):
    """Clone a Group locally by default, or across clusters with --source-cluster."""

    output_format = _normalize_output_format(output_format)
    source_cluster = source_cluster.strip() if source_cluster is not None else None
    if source_cluster == "":
        raise typer.BadParameter("--source-cluster must not be empty")
    target_cluster = (
        target_cluster.strip() if target_cluster is not None else (_effective_cluster() or "")
    )
    if not target_cluster:
        raise typer.BadParameter(
            "target cluster is required; use --target-cluster, --cluster, or AP_CLUSTER"
        )
    is_cross_cluster = source_cluster is not None
    if is_cross_cluster and source_cluster.lower() == target_cluster.lower():
        raise typer.BadParameter("source and target clusters must be different")
    effective_start_paused = start_paused if start_paused is not None else is_cross_cluster
    if source_mode not in {"terminal_only", "snapshot"}:
        raise typer.BadParameter("--source-mode must be terminal_only or snapshot")
    if source_mode == "snapshot" and not effective_start_paused:
        raise typer.BadParameter("snapshot mode cannot be used with --activate")

    target_group = {
        key: value
        for key, value in {
            "name": name,
            "queue_id": queue_id,
            "max_concurrency": max_concurrency,
        }.items()
        if value is not None
    }
    if model_base_url_collection is not None and clear_model_base_url_collection:
        raise typer.BadParameter(
            "--model-base-url-collection and --clear-model-base-url-collection are mutually exclusive"
        )
    if clear_model_base_url_collection:
        # Explicit null clears the inherited pool (tri-state field).
        target_group["model_base_url_collection"] = None
    elif model_base_url_collection is not None:
        urls = [u.strip() for u in model_base_url_collection.split(",") if u.strip()]
        if not urls:
            raise typer.BadParameter("--model-base-url-collection must contain at least one URL")
        target_group["model_base_url_collection"] = urls
    params_patch = _parse_json_object(params, "--params") or {}
    overrides_patch = _parse_json_object(overrides, "--overrides")
    job_patch: dict[str, Any] = {
        "params": params_patch,
        "delete_params": delete_param or [],
    }
    if overrides is not None:
        job_patch["overrides"] = overrides_patch
    if credential_type is not None:
        job_patch["credential_type"] = credential_type
    mapping_payload = (
        _read_json_object_option(
            resource_mappings,
            resource_mappings_file,
            "--resource-mappings",
        )
        or {}
    )
    if not is_cross_cluster and (
        resource_mappings is not None or resource_mappings_file is not None
    ):
        raise typer.BadParameter("resource mappings require --source-cluster")
    clone_key = idempotency_key or str(uuid.uuid4())
    kwargs = {
        "source_cluster": source_cluster,
        "source_mode": source_mode,
        "start_paused": effective_start_paused,
        "trials": trials,
        "target_group": target_group,
        "job_patch": job_patch,
        "resource_mappings": mapping_payload if is_cross_cluster else None,
        "idempotency_key": clone_key,
    }
    client = get_client(cluster=target_cluster)
    preview = client.preview_group_clone(
        source_group_id,
        **kwargs,
    )
    if preview_only:
        _print_formatted(preview, output_format)
        return

    if output_format == "plain":
        typer.echo(
            "Cross-cluster Group Clone preview" if is_cross_cluster else "Group Clone preview"
        )
        _print_key_values(
            [
                ("source_cluster", preview.get("source_cluster")),
                ("source_group_id", preview.get("source_group_id")),
                ("target_cluster", preview.get("target_cluster")),
                ("target_name", (preview.get("target_group") or {}).get("name")),
                ("transparency", (preview.get("target_group") or {}).get("transparency")),
                ("target_queue", (preview.get("target_group") or {}).get("queue_id")),
                ("jobs", preview.get("source_job_count")),
                ("target_jobs", preview.get("target_job_count")),
                ("status_after_clone", preview.get("target_scheduling_status_after_clone")),
                ("idempotency_key", clone_key),
            ],
            skip_empty=False,
        )
    if not yes and not typer.confirm("Create this target Group and its Jobs?"):
        typer.echo(f"Cancelled. Reuse idempotency_key {clone_key} when retrying.")
        raise typer.Exit(0)

    result = client.clone_group(
        source_group_id,
        **kwargs,
    )
    if output_format == "plain":
        typer.echo(
            "Cross-cluster Group Clone completed" if is_cross_cluster else "Group Clone completed"
        )
        _print_key_values(
            [
                ("target_group_id", result.get("target_group_id")),
                ("status", result.get("status")),
                ("source_job_count", result.get("source_job_count")),
                ("target_jobs", result.get("target_job_count")),
                ("created", result.get("created")),
                ("reused", result.get("reused")),
                ("idempotency_key", result.get("idempotency_key") or clone_key),
            ],
            skip_empty=False,
        )
    else:
        _print_formatted(result, output_format)


@group_app.command("update")
def group_update(
    group_id: str = typer.Argument(..., help="Group ID"),
    max_concurrency: Optional[int] = typer.Option(
        None,
        "--max-concurrency",
        "-c",
        min=1,
        help="Maximum concurrent jobs",
    ),
    eval_config: Optional[str] = typer.Option(
        None, "--eval-config", help="Evaluation config (JSON object)"
    ),
    model_base_url_collection: Optional[str] = typer.Option(
        None,
        "--model-base-url-collection",
        help="Model base URL collection (JSON array or comma-separated)",
    ),
    model_base_url_file: Optional[str] = typer.Option(
        None,
        "--model-base-url-file",
        help="File path containing model base URL list (one URL per line)",
    ),
    dataset: Optional[str] = typer.Option(
        None, "--dataset", "-d", help="Dataset name (benchmark perspective)"
    ),
    model_name: Optional[str] = typer.Option(
        None, "--model", "-m", help="Model name (benchmark perspective)"
    ),
    scaffold: Optional[str] = typer.Option(
        None, "--scaffold", "-s", help="Scaffold/agent name (benchmark perspective)"
    ),
    benchmark: Optional[str] = typer.Option(
        None, "--benchmark", help="Benchmark name; pass an empty string to clear"
    ),
    tags: Optional[str] = typer.Option(
        None,
        "--tags",
        help="Tags to set (comma-separated key:value); merged into existing Group tags",
    ),
    meta_model: Optional[str] = typer.Option(None, "--meta-model", help="Set meta_model tag"),
    meta_job_type: Optional[str] = typer.Option(
        None, "--meta-job-type", help="Set meta_job_type tag (Eval-Eval or Others)"
    ),
    meta_teacher_direction: Optional[str] = typer.Option(
        None,
        "--meta-teacher-direction",
        help="Set meta_teacher_direction tag (options: ap meta-teacher-direction list)",
    ),
    meta_train_stage: Optional[str] = typer.Option(
        None,
        "--meta-train-stage",
        help="Set meta_train_stage tag (options: ap meta-train-stage list)",
    ),
    priority: Optional[str] = typer.Option(
        None,
        "--priority",
        help="Group priority default: high or medium; --priority alone sets weight to 0",
    ),
    priority_weight: Optional[int] = typer.Option(
        None,
        "--priority-weight",
        min=0,
        max=10,
        help="Group priority weight default, 0-10; weight alone preserves the current tier",
    ),
    priority_update_mode: Optional[str] = typer.Option(
        None,
        "--priority-update-mode",
        help="existing updates defaults and all current Jobs (including PostProcess); incremental updates only defaults (server default: existing)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Update Group properties and scheduling defaults inherited by Jobs."""
    output_format = _normalize_output_format(output_format)
    if priority is not None and priority not in {"high", "medium"}:
        raise typer.BadParameter("--priority must be one of high/medium")
    if priority_update_mode is not None:
        if priority_update_mode not in {"existing", "incremental"}:
            raise typer.BadParameter("--priority-update-mode must be one of existing/incremental")
        if priority is None and priority_weight is None:
            raise typer.BadParameter(
                "--priority-update-mode requires --priority or --priority-weight"
            )
    eval_config_dict = _parse_json_object(eval_config, "--eval-config")
    model_base_url_collection_list = _parse_model_base_url_collection_option(
        model_base_url_collection, model_base_url_file
    )
    tags_list = None
    if tags is not None or any(
        v is not None
        for v in (
            meta_model,
            meta_job_type,
            meta_teacher_direction,
            meta_train_stage,
        )
    ):
        try:
            tags_list = _merge_meta_tags(
                tags.split(",") if tags else None,
                meta_model=meta_model,
                meta_job_type=meta_job_type,
                meta_teacher_direction=meta_teacher_direction,
                meta_train_stage=meta_train_stage,
            )
        except ValueError as exc:
            _emit_error(str(exc))
            raise typer.Exit(1)
    if all(
        value is None
        for value in (
            max_concurrency,
            eval_config_dict,
            model_base_url_collection_list,
            dataset,
            model_name,
            scaffold,
            benchmark,
            tags_list,
            priority,
            priority_weight,
        )
    ):
        raise typer.BadParameter("At least one field must be provided to update")

    client = get_client()
    result = client.update_group(
        group_id,
        max_concurrency=max_concurrency,
        eval_config=eval_config_dict,
        model_base_url_collection=model_base_url_collection_list,
        dataset=dataset,
        model=model_name,
        scaffold=scaffold,
        **({"benchmark": benchmark} if benchmark is not None else {}),
        **({"tags": tags_list} if tags_list is not None else {}),
        **({"priority": priority} if priority is not None else {}),
        **({"priority_weight": priority_weight} if priority_weight is not None else {}),
        **(
            {"priority_update_mode": priority_update_mode}
            if priority_update_mode is not None
            else {}
        ),
    )
    if output_format == "plain":
        _print_group_action_plain(
            "Group updated",
            result,
            group_id,
            [
                "max_concurrency",
                "eval_config",
                "model_base_url_collection",
                "dataset",
                "model",
                "scaffold",
                "benchmark",
                "priority",
                "priority_weight",
                "updated_at",
            ],
        )
    else:
        _print_formatted(result, output_format)


@group_app.command("set-extra-aggregations")
def group_set_extra_aggregations(
    group_id: str = typer.Argument(..., help="Group ID"),
    extra_aggregations: Optional[str] = typer.Option(
        None,
        "--extra-aggregations",
        help="extra_aggregations config (JSON object), e.g. "
        '{"avg_lat":{"avg":"lat"},"total_tokens":{"sum":"tokens"}}. '
        "Supported ops: avg, sum.",
    ),
    extra_aggregations_file: Optional[str] = typer.Option(
        None,
        "--extra-aggregations-file",
        help="File containing the extra_aggregations JSON object.",
    ),
    clear: bool = typer.Option(
        False,
        "--clear",
        help="Remove extra_aggregations from the group's eval_config.",
    ),
    output_format: str = typer.Option("plain", "--format", help="Output format: plain/json/yaml"),
):
    """Set eval_config["extra_aggregations"] for a Group.

    Merges into the group's existing eval_config — sibling keys (group_by,
    score_field, aggregations, ...) are preserved. Prefer this over ``ap group
    update --eval-config`` when you only want to change extra_aggregations,
    since ``--eval-config`` replaces the whole eval_config.
    """
    output_format = _normalize_output_format(output_format)
    if clear:
        spec_dict: Optional[dict] = None
    else:
        spec_dict = _read_json_object_option(
            extra_aggregations, extra_aggregations_file, "--extra-aggregations"
        )
    if not clear and spec_dict is None:
        raise typer.BadParameter(
            "provide --extra-aggregations <JSON> (or --extra-aggregations-file), or use --clear"
        )

    client = get_client()
    try:
        result = client.set_group_extra_aggregations(group_id, spec_dict)
    except ValueError as exc:
        _emit_error(str(exc))
        raise typer.Exit(1)

    if output_format == "plain":
        _print_group_action_plain(
            "Group extra_aggregations set",
            result,
            group_id,
            ["eval_config", "updated_at"],
        )
    else:
        _print_formatted(result, output_format)


@group_app.command("pause")
def group_pause(
    group_id: str = typer.Argument(..., help="Group ID"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Pause Group scheduling."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.pause_group(group_id)
    if output_format == "plain":
        _print_group_action_plain(
            "Group paused",
            result,
            group_id,
            ["scheduling_status", "paused_at", "paused_by", "updated_at"],
        )
    else:
        _print_formatted(result, output_format)


@group_app.command("resume")
def group_resume(
    group_id: str = typer.Argument(..., help="Group ID"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Resume Group scheduling."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.resume_group(group_id)
    if output_format == "plain":
        _print_group_action_plain(
            "Group resumed",
            result,
            group_id,
            ["scheduling_status", "updated_at"],
        )
    else:
        _print_formatted(result, output_format)


@group_app.command("jobs")
def group_jobs(
    group_id: str = typer.Argument(..., help="Group ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    tag: Optional[list[str]] = typer.Option(
        None, "--tag", help="Filter by tag (repeatable; multiple tags are combined with AND)"
    ),
    include_post_process: bool = typer.Option(
        False,
        "--include-post-process",
        help="Include the Group PostProcess job in the job list",
    ),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(100, "--limit", help="Maximum number of entries to return"),
    next_token: Optional[str] = typer.Option(
        None,
        "--next-token",
        help="Opaque token returned by the previous Group jobs page",
    ),
    cursor: bool = typer.Option(
        False,
        "--cursor",
        help="Opt this page into next-token pagination",
    ),
    no_total: bool = typer.Option(
        False,
        "--no-total",
        help="Skip the server-side count; total becomes null in json/yaml output",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List jobs in a Group."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    if next_token and skip > 0:
        raise typer.BadParameter("--next-token cannot be used with --skip greater than 0")
    if cursor and skip > 0:
        raise typer.BadParameter("--cursor cannot be used with --skip greater than 0")
    cursor_request = bool(next_token) or cursor
    if share_token is not None:
        unsupported = (
            ("--tag", bool(tag)),
            ("--include-post-process", include_post_process),
            ("--next-token", bool(next_token)),
            ("--cursor", cursor),
            ("--no-total", no_total),
        )
        for option, used in unsupported:
            if used:
                _emit_error(f"{option} is not supported with --share-token")
                raise typer.Exit(1)
        if skip < 0 or not 1 <= limit <= 500:
            raise typer.BadParameter(
                "share pagination requires --skip >= 0 and 1 <= --limit <= 500"
            )
        client = _read_client(share_token, group_id if share_token else None)
        result = client.list_jobs(group_id=group_id, skip=skip, limit=limit)
    else:
        client = get_client()
        result = client.list_group_jobs(
            group_id,
            tag=tag,
            include_post_process=include_post_process,
            skip=skip,
            limit=limit,
            **({"next_token": next_token} if next_token else {}),
            **({"pagination": "cursor"} if cursor_request else {}),
            include_total=not no_total,
        )
    if output_format == "table":
        _print_job_list_plain(result, rich=True)
    elif output_format == "plain":
        _print_job_list_plain(result)
    else:
        _print_formatted(result, output_format)
    following_token = result.get("next_token")
    if output_format in {"table", "plain"} and following_token:
        typer.echo(f"Next token: {following_token}", err=True)


@group_app.command("stats")
def group_stats(
    group_id: str = typer.Argument(..., help="Group ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show Group progress."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = _read_client(share_token, group_id if share_token else None)
    result = client.get_group_stats(group_id)
    if output_format == "table":
        _print_detail(result)
    else:
        _print_formatted(result, output_format)


@group_app.command("eval")
def group_eval(
    group_id: str = typer.Argument(..., help="Group ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Read with a share token"
    ),
    summary_only: bool = typer.Option(
        False,
        "--summary-only",
        help="Show only the aggregate summary, without per-task results",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show Group aggregated evaluation results."""
    output_format = _normalize_output_format(output_format)
    client = _read_client(share_token, group_id if share_token else None)
    result = (
        client.get_group_eval_summary(group_id) if summary_only else client.get_group_eval(group_id)
    )
    if output_format == "plain":
        _print_group_eval_plain(result)
    else:
        _print_formatted(result, output_format)


@group_app.command("artifacts")
def group_artifacts(
    group_id: str = typer.Argument(..., help="Group ID"),
    include_post_process: bool = typer.Option(
        False,
        "--include-post-process",
        help="Include the Group PostProcess job artifacts",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show Group artifact download links."""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client()
    result = client.get_group_artifacts(group_id, include_post_process=include_post_process)
    if output_format == "table":
        _print_records_table(result)
    else:
        _print_formatted(result, output_format)


@group_app.command("cancel")
def group_cancel(
    group_id: str = typer.Argument(..., help="Group ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip the confirmation prompt"),
):
    """Cancel all unfinished jobs under a Group."""
    client = get_client()
    try:
        result = client.cancel_group(group_id)
    except APIError as exc:
        detail = exc.detail if isinstance(exc.detail, dict) else {}
        if exc.status_code != 409 or detail.get("error") != "group_cancel_confirmation_required":
            raise

        preview = client.preview_group_cancel(group_id)
        confirmation_token = None
        if preview.get("confirmation_required"):
            cancellable_jobs = int(preview.get("cancellable_jobs", 0))
            confirmation_token = preview.get("confirmation_token")
            if not confirmation_token:
                _emit_error("server required confirmation but did not return a confirmation token")
                raise typer.Exit(1)
            if not yes:
                typer.confirm(
                    f"Cancel {cancellable_jobs} cancellable Jobs in Group {group_id}?",
                    abort=True,
                )

        result = client.cancel_group(group_id, confirmation_token=confirmation_token)
    actual_group_id = result.get("group_id") or group_id
    print(f"[green]Group cancel completed:[/] {actual_group_id}")
    print(f"  cancelled: {result.get('cancelled', 0)}")
    print(f"  k8s_deleted: {result.get('k8s_deleted', False)}")
    k8s_errors = result.get("k8s_errors") or []
    if k8s_errors:
        print("  k8s_errors:")
        for err in k8s_errors:
            print(f"    - {err}")


@group_app.command("grant")
def group_grant(
    group_id: str = typer.Argument(..., help="Group ID"),
    user: Optional[str] = typer.Option(None, "--user", help="Grant to this user_id"),
    user_group: Optional[str] = typer.Option(
        None, "--user-group", help="Grant to this user_group_id"
    ),
    role: str = typer.Option(
        "reader",
        "--role",
        help="reader (view), blackbox-reader (protected Group content), cloner (view+clone), writer (view+cancel/update), or admin (view+clone+update+grant)",
    ),
):
    """Grant a user/user-group access to a specific group (RBAC v2 instance delegation)."""
    _grant_instance_access("group", group_id, role, user, user_group)


@group_app.command("revoke")
def group_revoke(
    group_id: str = typer.Argument(..., help="Group ID"),
    user: Optional[str] = typer.Option(None, "--user", help="Revoke from this user_id"),
    user_group: Optional[str] = typer.Option(
        None, "--user-group", help="Revoke from this user_group_id"
    ),
    role: str = typer.Option(
        "reader", "--role", help="reader, blackbox-reader, cloner, writer, or admin"
    ),
):
    """Revoke a user/user-group's instance access to a specific group."""
    _revoke_instance_access("group", group_id, role, user, user_group)


@group_app.command("access-list")
def group_access_list(group_id: str = typer.Argument(..., help="Group ID")):
    """List who has instance-level access to a specific group."""
    _print_instance_access("group", group_id)


@group_app.command("export")
def group_export(
    group_id: str = typer.Argument(..., help="Group ID"),
    share_token: Optional[str] = typer.Option(
        None, "--share-token", help="Export with a share token"
    ),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory"),
    workers: int = typer.Option(
        4, "--workers", "-w", min=1, help="Number of concurrent export workers"
    ),
    timeout: float = typer.Option(
        300,
        "--timeout",
        callback=_validate_export_timeout,
        help="SDK request timeout in seconds, not the total export duration",
    ),
    logs: bool = typer.Option(False, "--logs", help="Include container logs"),
    events: bool = typer.Option(False, "--events", help="Include events"),
    no_extract_artifacts: bool = typer.Option(
        False,
        "--no-extract-artifacts",
        help="Download result.tgz without extracting it into artifacts/",
    ),
    include_files: Optional[list[str]] = typer.Option(
        None,
        "--include-files",
        help="Only download matching artifact files or folders (repeatable; comma-separated)",
    ),
    exclude_files: Optional[list[str]] = typer.Option(
        None,
        "--exclude-files",
        help="Skip matching artifact files or folders (repeatable; comma-separated)",
    ),
):
    """Export artifacts of all jobs under a Group to a local directory. Use --logs/--events to include logs and events."""
    include_file_selectors = _parse_file_selectors(include_files)
    exclude_file_selectors = _parse_file_selectors(exclude_files)
    if include_files and not include_file_selectors:
        _emit_error("--include-files requires at least one non-empty file or folder name")
        raise typer.Exit(1)
    if exclude_files and not exclude_file_selectors:
        _emit_error("--exclude-files requires at least one non-empty file or folder name")
        raise typer.Exit(1)
    if no_extract_artifacts and (include_file_selectors or exclude_file_selectors):
        _emit_error("--include-files/--exclude-files cannot be used with --no-extract-artifacts")
        raise typer.Exit(1)

    if share_token is not None and (include_file_selectors or exclude_file_selectors):
        _emit_error("--include-files/--exclude-files are not supported with --share-token")
        raise typer.Exit(1)

    client = _read_client(share_token, group_id if share_token else None)
    from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn

    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("{task.fields[current_job]}"),
        TextColumn("{task.fields[current_stage]}"),
        transient=True,
    ) as progress:
        task_id = progress.add_task(
            "Exporting group",
            total=0,
            current_job="",
            current_stage="",
        )

        def _on_progress(done: int, total: int, job_id: str, stage: str) -> None:
            current_job = f"job={job_id}" if job_id else ""
            current_stage = f"stage={stage}" if stage else ""
            progress.update(
                task_id,
                total=total,
                completed=done,
                current_job=current_job,
                current_stage=current_stage,
            )

        report, channels = _export_channel_reporter(progress.console.print)
        dest, summary = export_group(
            client,
            group_id,
            output,
            progress_callback=_on_progress,
            workers=workers,
            result_callback=report,
            timeout=timeout,
            include_logs=logs,
            include_events=events,
            extract_artifacts=not no_extract_artifacts,
            include_files=include_file_selectors,
            exclude_files=exclude_file_selectors,
        )
    print(f"[green]Group exported:[/] {group_id}")
    print(f"  path: {dest}")
    print(
        f"  [green]{summary.downloaded}[/] jobs downloaded, "
        f"[yellow]{summary.skipped}[/] jobs skipped (no artifact)"
    )
    print(f"channels: oss={channels['oss']} proxy={channels['proxy']}")
    if summary.skipped_job_names:
        print(f"  Skipped: {', '.join(summary.skipped_job_names)}")


@group_app.command("wait")
def group_wait(
    group_id: str = typer.Argument(..., help="Group ID"),
    interval: float = typer.Option(
        5.0, "--interval", "-i", min=0.1, help="Polling interval (seconds)"
    ),
    timeout: Optional[float] = typer.Option(
        None,
        "--timeout",
        "--wait-timeout",
        min=0.0,
        help="Maximum seconds to wait; omit to wait indefinitely",
    ),
    post_process: bool = typer.Option(
        False,
        "--post-process",
        help="After regular jobs finish, also wait for the Group PostProcess job",
    ),
):
    """Poll until all jobs under a Group finish."""
    client = get_client()
    try:
        if post_process:
            result = wait_for_group_post_process(client, group_id, interval, timeout=timeout)
        else:
            result = wait_for_group(client, group_id, interval, timeout=timeout)
    except WaitTimeoutError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1)
    if post_process:
        group = result.get("group") or {}
        post_process_job = result.get("post_process_job")
        stats = group.get("stats") or {}
    else:
        group = result
        post_process_job = None
        stats = group.get("stats") or {}
    print(f"[green]Group finished:[/] {group_id}")
    print(f"  total: {stats.get('total', 0)}")
    print(f"  succeeded: {stats.get('succeeded', 0)}")
    print(f"  failed: {stats.get('failed', 0)}")
    print(f"  cancelled: {stats.get('cancelled', 0)}")
    if post_process:
        if post_process_job:
            print(f"  post_process_job_id: {post_process_job.get('job_id')}")
            print(f"  post_process_status: {post_process_job.get('status')}")
        else:
            print("  post_process_status: not_configured")


def main() -> None:
    try:
        app()
    except APIError as exc:
        typer.echo(_format_api_error(exc), err=True)
        raise SystemExit(1) from None
    except (ConfigurationError, PaginationProtocolError) as exc:
        typer.echo(f"error: {exc}", err=True)
        raise SystemExit(1) from None


def _format_api_error(exc: APIError) -> str:
    if isinstance(exc.detail, dict) and exc.detail.get("code") == "blackbox_content_restricted":
        return f"error: Blackbox content is hidden; Group Reader access is required. (request_id={exc.request_id})"
    if str(exc.detail) != _NON_JSON_RESPONSE_DETAIL:
        return f"error: {exc}"

    status = exc.status_code if exc.status_code is not None else "<unknown>"
    lines = [
        f"error: API Error {status}: {exc.detail}",
        f"hint: {_NON_JSON_RESPONSE_HINT}",
        f"request_id: {exc.request_id}",
    ]
    if exc.response is not None:
        content_type = exc.response.headers.get("Content-Type") or "<missing>"
        lines.extend(
            [
                "response:",
                f"  status: {exc.response.status_code}",
                f"  content_type: {content_type}",
            ]
        )
        preview = _format_response_preview(exc.response.content or b"", content_type)
        if preview:
            lines.append(f"  preview: {preview}")
    return "\n".join(lines)


def _format_response_preview(raw: bytes, content_type: str) -> str:
    if not raw:
        return ""
    text = raw.decode("utf-8", errors="replace").strip()
    if _looks_like_html_response(text, content_type):
        return "HTML document returned; run with --verbose to inspect the response body."
    return _truncate_cli_text(" ".join(text.split()), 200)


def _looks_like_html_response(text: str, content_type: str) -> bool:
    stripped = text.lstrip().lower()
    return (
        "html" in content_type.lower()
        or stripped.startswith("<!doctype html")
        or stripped.startswith("<html")
    )


def _truncate_cli_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"...<truncated {len(text) - limit} chars>"


# ==================== Eval Plan operations ====================


def _print_plan_list_plain(result: dict) -> None:
    _print_plain_table(
        result.get("items", []),
        [
            ("plan_id", "plan_id"),
            ("name", "name"),
            ("status", "status"),
            ("cron_expression", "cron_expression"),
            ("run_count", "run_count"),
            ("next_run_at", "next_run_at"),
            ("created_at", "created_at"),
        ],
    )


def _print_plan_plain(data: dict) -> None:
    print(f"  plan_id:         {data.get('plan_id')}")
    print(f"  name:            {data.get('name')}")
    print(f"  description:     {data.get('description') or ''}")
    print(f"  status:          {data.get('status')}")
    print(f"  cron_expression: {data.get('cron_expression')}")
    print(f"  valid_from:      {data.get('valid_from')}")
    print(f"  valid_until:     {data.get('valid_until')}")
    print(f"  run_count:       {data.get('run_count')}")
    print(f"  next_run_at:     {data.get('next_run_at')}")
    print(f"  last_run_at:     {data.get('last_run_at')}")
    job_spec = data.get("job_spec", {})
    if job_spec:
        print(f"  job_spec.template: {job_spec.get('template')}")
        params = job_spec.get("params")
        if params:
            print(f"  job_spec.params:   {json.dumps(params, ensure_ascii=False)}")


@plan_app.command("create")
def plan_create(
    job_spec: str = typer.Option(
        ..., "--job-spec", help="Job spec JSON (e.g. output of 'ap job create --job-spec')"
    ),
    name: str = typer.Option(..., "--name", "-n", help="Plan name"),
    cron_expression: str = typer.Option(..., "--cron", help="Cron expression (e.g. '0 8 * * *')"),
    valid_from: str = typer.Option(
        ..., "--valid-from", help="Valid from (ISO datetime, e.g. 2026-01-01)"
    ),
    valid_until: str = typer.Option(
        ..., "--valid-until", help="Valid until (ISO datetime, e.g. 2026-12-31)"
    ),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Plan description"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Create an eval plan.

    Examples:
        # Build job spec, then create plan
        ap job create claw-eval-task -p '{"model":"qwen-max"}' --job-spec > spec.json
        ap plan create --job-spec spec.json -n daily-eval --cron '0 8 * * *' --valid-from 2026-01-01 --valid-until 2027-01-01

        # Inline job spec JSON
        ap plan create --job-spec '{"template":"claw-eval-task","params":{"model":"qwen-max"}}' -n daily-eval --cron '0 8 * * *' --valid-from 2026-01-01 --valid-until 2027-01-01
    """
    output_format = _normalize_output_format(output_format)
    client = get_client()

    # --job-spec: try inline JSON first, fall back to file path
    raw = job_spec.strip()
    try:
        job_spec_dict = json.loads(raw)
    except json.JSONDecodeError:
        try:
            with open(raw, "r", encoding="utf-8") as f:
                job_spec_dict = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[red]error: failed to parse --job-spec file as JSON: {e}[/]")
            raise typer.Exit(1)
        except FileNotFoundError:
            print(f"[red]error: file not found: {raw}[/]")
            raise typer.Exit(1)

    result = client.create_eval_plan(
        name=name,
        job_spec=job_spec_dict,
        cron_expression=cron_expression,
        valid_from=valid_from,
        valid_until=valid_until,
        description=description,
    )
    if output_format == "plain":
        print("[green]Eval plan created:[/]")
        _print_plan_plain(result)
    else:
        _print_formatted(result, output_format)


@plan_app.command("list")
def plan_list(
    status: Optional[str] = typer.Option(None, "--status", help="Filter by status (Active/Paused)"),
    user_id: Optional[str] = typer.Option(None, "--user-id", help="Filter by user ID"),
    created_after: Optional[str] = typer.Option(
        None, "--created-after", help="Filter by created_at >= (ISO datetime)"
    ),
    created_before: Optional[str] = typer.Option(
        None, "--created-before", help="Filter by created_at <= (ISO datetime)"
    ),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(-1, "--limit", help="Maximum number of entries (-1 for all)"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List eval plans."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_eval_plans(
        status=status,
        user_id=user_id,
        created_after=created_after,
        created_before=created_before,
        skip=skip,
        limit=limit,
    )
    if output_format == "plain":
        _print_plan_list_plain(result)
    else:
        _print_formatted(result, output_format)


@plan_app.command("get")
def plan_get(
    plan_id: str = typer.Argument(..., help="Plan ID"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Get eval plan detail."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.get_eval_plan(plan_id)
    if output_format == "plain":
        _print_plan_plain(result)
    else:
        _print_formatted(result, output_format)


@plan_app.command("update")
def plan_update(
    plan_id: str = typer.Argument(..., help="Plan ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Plan name"),
    job_spec: Optional[str] = typer.Option(
        None, "--job-spec", help="Job spec JSON (e.g. output of 'ap job create --job-spec')"
    ),
    cron_expression: Optional[str] = typer.Option(None, "--cron", help="Cron expression"),
    valid_from: Optional[str] = typer.Option(
        None, "--valid-from", help="Valid from (ISO datetime)"
    ),
    valid_until: Optional[str] = typer.Option(
        None, "--valid-until", help="Valid until (ISO datetime)"
    ),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Plan description"),
    status: Optional[str] = typer.Option(None, "--status", help="Set status (Active/Paused)"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Update an eval plan.

    All fields are optional — only provided fields are updated.

    Examples:
        # Pause a plan
        ap plan update <PLAN_ID> --status Paused

        # Update cron only
        ap plan update <PLAN_ID> --cron '0 10 * * 1-5'

        # Update job spec
        ap plan update <PLAN_ID> --job-spec "$(ap job create claw-eval-task -p '{\"model\":\"qwen-max\"}' --job-spec)"
    """
    output_format = _normalize_output_format(output_format)
    client = get_client()

    # Parse --job-spec if provided (inline JSON or file path)
    job_spec_dict = None
    if job_spec is not None:
        raw = job_spec.strip()
        try:
            job_spec_dict = json.loads(raw)
        except json.JSONDecodeError:
            try:
                with open(raw, "r", encoding="utf-8") as f:
                    job_spec_dict = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[red]error: failed to parse --job-spec file as JSON: {e}[/]")
                raise typer.Exit(1)
            except FileNotFoundError:
                print(f"[red]error: file not found: {raw}[/]")
                raise typer.Exit(1)

    result = client.update_eval_plan(
        plan_id=plan_id,
        name=name,
        job_spec=job_spec_dict,
        cron_expression=cron_expression,
        valid_from=valid_from,
        valid_until=valid_until,
        description=description,
        status=status,
    )
    if output_format == "plain":
        print("[green]Eval plan updated:[/]")
        _print_plan_plain(result)
    else:
        _print_formatted(result, output_format)


@plan_app.command("delete")
def plan_delete(
    plan_ids: List[str] = typer.Argument(..., help="One or more plan IDs"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Permanently delete one or more eval plans from MongoDB.

    Examples:
        ap plan delete plan-abc
        ap plan delete plan-abc plan-def plan-ghi
        ap plan delete plan-abc -y
    """
    if not yes:
        ids_str = ", ".join(plan_ids)
        typer.confirm(f"Permanently delete {len(plan_ids)} plan(s): {ids_str}?", abort=True)
    client = get_client()
    failed = []
    for pid in plan_ids:
        try:
            result = client.delete_eval_plan(pid)
        except APIError as e:
            if e.status_code == 404:
                print(f"[yellow]Plan not found, skipping:[/] {pid}")
                failed.append(pid)
                continue
            raise
        print(f"[green]Eval plan permanently deleted:[/] {result.get('plan_id')}")
    if failed:
        raise typer.Exit(1)


@plan_app.command("trigger")
def plan_trigger(
    plan_id: str = typer.Argument(..., help="Plan ID"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Manually trigger an eval plan (creates Group + Jobs)."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.trigger_eval_plan(plan_id)
    if output_format == "plain":
        print("[green]Eval plan triggered:[/]")
        print(f"  plan_id:   {result.get('plan_id')}")
        print(f"  run_count: {result.get('run_count')}")
        run = result.get("run", {})
        if run:
            print(f"  run.type:  {run.get('type')}")
            print(f"  run.id:    {run.get('id')}")
        trigger_result = result.get("result", {})
        if trigger_result:
            group_id = trigger_result.get("group_id")
            submitted = trigger_result.get("submitted")
            if group_id:
                print(f"  group_id:  {group_id}")
            if submitted is not None:
                print(f"  submitted: {submitted}")
    else:
        _print_formatted(result, output_format)


@plan_app.command("runs")
def plan_runs(
    plan_id: str = typer.Argument(..., help="Plan ID"),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(-1, "--limit", help="Maximum number of entries (-1 for all)"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List historical runs for an eval plan."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_eval_plan_runs(plan_id, skip=skip, limit=limit)
    if output_format == "plain":
        items = result.get("items", [])
        if not items:
            print("No runs found.")
        else:
            _print_plain_table(
                items,
                [
                    ("type", "type"),
                    ("id", "id"),
                    ("name", "name"),
                    ("job_count", "job_count"),
                    ("triggered_at", "triggered_at"),
                ],
            )
    else:
        _print_formatted(result, output_format)


# ============================================================
# DataSource commands
# ============================================================


def _parse_datasource_extras(extras: Optional[str]) -> Optional[dict]:
    """Parse --extras as a JSON object string. Returns None when not provided."""
    if extras is None:
        return None
    raw = extras.strip()
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"--extras must be a JSON object: {exc}") from exc
    if not isinstance(parsed, dict):
        raise typer.BadParameter("--extras must be a JSON object")
    return parsed


def _print_datasource_plain(ds: dict) -> None:
    print(f"  datasource_id:     {ds.get('datasource_id')}")
    print(f"  name:              {ds.get('name')}")
    print(f"  type:              {ds.get('type')}")
    print(f"  uri:               {ds.get('uri')}")
    if ds.get("endpoint") is not None:
        print(f"  endpoint:          {ds.get('endpoint')}")
    if ds.get("access_key_id") is not None:
        print(f"  access_key_id:     {ds.get('access_key_id')}")
    if ds.get("access_key_secret") is not None:
        print(f"  access_key_secret: {ds.get('access_key_secret')}")
    print(f"  access_mode:       {ds.get('access_mode')}")
    if ds.get("mount_path") is not None:
        print(f"  mount_path:        {ds.get('mount_path')}")
    if ds.get("group_id") is not None:
        print(f"  group_id:          {ds.get('group_id')}")
    extras = ds.get("extras") or {}
    if extras:
        print(f"  extras:            {json.dumps(extras, ensure_ascii=False)}")
    if ds.get("user_id") is not None:
        print(f"  user_id:           {ds.get('user_id')}")
    print(f"  created_at:        {ds.get('created_at')}")
    print(f"  updated_at:        {ds.get('updated_at')}")


@datasource_app.command("create")
def datasource_create(
    name: str = typer.Option(
        ..., "--name", "-n", help="Human-readable datasource name (unique per user)"
    ),
    type: str = typer.Option(
        ..., "--type", "-t", help="Storage backend type: 'oss', 'nas' or 'cpfs'"
    ),
    uri: str = typer.Option(
        ...,
        "--uri",
        help=(
            "Storage URI, e.g. oss://bucket/path, nas://host:/path or "
            "cpfs://bmcpfs-id:/path (CPFS uses the filesystem ID)"
        ),
    ),
    access_key_id: Optional[str] = typer.Option(
        None, "--ak-id", help="OSS access key ID (optional)"
    ),
    access_key_secret: Optional[str] = typer.Option(
        None, "--ak-secret", help="OSS access key secret (optional)"
    ),
    endpoint: Optional[str] = typer.Option(
        None,
        "--endpoint",
        help=(
            "OSS endpoint (e.g. oss-cn-hangzhou.aliyuncs.com), or the CPFS VPC mount target domain"
        ),
    ),
    access_mode: Optional[str] = typer.Option(
        None,
        "--access-mode",
        help=(
            "Mount access mode: ReadOnly | ReadWrite. Omit for the per-type default "
            "(ReadWrite for nas/cpfs, ReadOnly for oss)"
        ),
    ),
    mount_path: Optional[str] = typer.Option(
        None, "--mount-path", help="Container-internal mount path, e.g. /mnt/data"
    ),
    extras: Optional[str] = typer.Option(
        None, "--extras", help="Free-form extras as a JSON object"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Create a DataSource."""
    output_format = _normalize_output_format(output_format)
    extras_dict = _parse_datasource_extras(extras)
    client = get_client()
    result = client.create_datasource(
        name=name,
        type=type,
        uri=uri,
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
        access_mode=access_mode,
        mount_path=mount_path,
        extras=extras_dict,
    )
    if output_format == "plain":
        print("[green]DataSource created:[/]")
        _print_datasource_plain(result)
        return
    _print_formatted(result, output_format)


@datasource_app.command("list")
def datasource_list(
    type: Optional[str] = typer.Option(
        None, "--type", "-t", help="Filter by type: oss | nas | cpfs"
    ),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Filter by exact name"),
    all_users: bool = typer.Option(False, "--all-users", help="Admin only: list across all users"),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(200, "--limit", help="Maximum number of entries to return"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List DataSources."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_datasources(
        type=type,
        name=name,
        all_users=all_users,
        skip=skip,
        limit=limit,
    )
    if output_format == "plain":
        _print_datasource_list_plain(result)
    else:
        _print_formatted(result, output_format)


@datasource_app.command("get")
def datasource_get(
    identifier: str = typer.Argument(..., help="datasource_id, ObjectId, or name"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Show DataSource details."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.get_datasource(identifier)
    if output_format == "plain":
        _print_datasource_plain(result)
    else:
        _print_formatted(result, output_format)


@datasource_app.command("update")
def datasource_update(
    identifier: str = typer.Argument(..., help="datasource_id, ObjectId, or name"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    type: Optional[str] = typer.Option(None, "--type", "-t", help="New type: oss | nas | cpfs"),
    uri: Optional[str] = typer.Option(None, "--uri", help="New storage URI"),
    access_key_id: Optional[str] = typer.Option(None, "--ak-id", help="New OSS access key ID"),
    access_key_secret: Optional[str] = typer.Option(
        None, "--ak-secret", help="New OSS access key secret"
    ),
    endpoint: Optional[str] = typer.Option(None, "--endpoint", help="New OSS endpoint"),
    access_mode: Optional[str] = typer.Option(
        None, "--access-mode", help="New access mode: ReadOnly | ReadWrite"
    ),
    mount_path: Optional[str] = typer.Option(None, "--mount-path", help="New container mount path"),
    extras: Optional[str] = typer.Option(
        None, "--extras", help="New extras as a JSON object (replaces existing)"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Update mutable fields on a DataSource."""
    output_format = _normalize_output_format(output_format)
    extras_dict = _parse_datasource_extras(extras)
    if all(
        v is None
        for v in (
            name,
            type,
            uri,
            access_key_id,
            access_key_secret,
            endpoint,
            access_mode,
            mount_path,
            extras_dict,
        )
    ):
        raise typer.BadParameter("At least one field must be provided to update")
    client = get_client()
    result = client.update_datasource(
        identifier,
        name=name,
        type=type,
        uri=uri,
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=endpoint,
        access_mode=access_mode,
        mount_path=mount_path,
        extras=extras_dict,
    )
    if output_format == "plain":
        print("[green]DataSource updated:[/]")
        _print_datasource_plain(result)
        return
    _print_formatted(result, output_format)


@datasource_app.command("delete")
def datasource_delete(
    identifiers: List[str] = typer.Argument(
        ..., help="One or more datasource_id / ObjectId / name"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Delete one or more DataSources (also removes their PV/PVC in cluster)."""
    if not yes:
        ids_str = ", ".join(identifiers)
        typer.confirm(
            f"Permanently delete {len(identifiers)} datasource(s): {ids_str}?",
            abort=True,
        )
    client = get_client()
    failed: list[str] = []
    for ident in identifiers:
        try:
            result = client.delete_datasource(ident)
        except APIError as e:
            if e.status_code == 404:
                print(f"[yellow]DataSource not found, skipping:[/] {ident}")
                failed.append(ident)
                continue
            raise
        print(f"[green]DataSource deleted:[/] {result.get('datasource_id') or ident}")
    if failed:
        raise typer.Exit(1)


# ============================================================
# Concurrency Policy commands
# ============================================================


def _parse_label_pairs(values: Optional[List[str]]) -> Optional[dict]:
    """Parse repeated --label key=value options into a dict. None if no labels."""
    if not values:
        return None
    label: dict = {}
    for item in values:
        if "=" not in item:
            raise typer.BadParameter(f"--label must be key=value, got {item!r}")
        key, val = item.split("=", 1)
        key = key.strip()
        if not key:
            raise typer.BadParameter(f"--label key empty in {item!r}")
        label[key] = val
    return label


def _print_concurrency_policy_plain(cr: dict) -> None:
    print(f"  policy_id:       {cr.get('policy_id')}")
    print(f"  name:              {cr.get('name')}")
    print(f"  scope:             {cr.get('scope', '')}")
    print(f"  queue_id:          {cr.get('queue_id', '')}")
    label = cr.get("label") or {}
    if label:
        print(f"  label:             {json.dumps(label, ensure_ascii=False)}")
    print(f"  capacity:          {cr.get('capacity')}")
    print(f"  enabled:           {cr.get('enabled')}")
    print(f"  created_by:        {cr.get('created_by', '')}")
    print(f"  user_name:         {cr.get('user_name', '')}")
    print(f"  created_at:        {cr.get('created_at')}")
    print(f"  updated_at:        {cr.get('updated_at')}")


def _print_concurrency_policy_list_plain(items: list) -> None:
    if not items:
        print("No concurrency policies found.")
        return
    _print_plain_table(
        items,
        [
            ("policy_id", "policy_id"),
            ("name", "name"),
            ("capacity", "capacity"),
            ("enabled", "enabled"),
            ("updated_at", "updated_at"),
        ],
    )


@concurrency_policy_app.command("create")
def concurrency_policy_create(
    name: str = typer.Option(..., "--name", "-n", help="Display name (mutable)"),
    capacity: int = typer.Option(..., "--capacity", help="Global share ceiling (concurrent jobs)"),
    scope: str = typer.Option("cluster", "--scope", help="Association attr; default 'cluster'"),
    queue_id: str = typer.Option(
        ...,
        "--queue-id",
        help="Owning queue; required. Queue members with write access can manage the resource.",
    ),
    label: Optional[List[str]] = typer.Option(
        None,
        "--label",
        help="Association attrs as key=value (repeatable), e.g. "
        "--label base_url=https://llm.example.com --label model=qwen-max",
    ),
    enabled: bool = typer.Option(
        True, "--enabled/--no-enabled", help="false = unlimited (bypasses the admission gate)"
    ),
    output_format: str = typer.Option("plain", "--format", help="Output format: plain/json/yaml"),
):
    """Create a concurrency policy (requires write access on the owning queue)."""
    output_format = _normalize_output_format(output_format)
    label_dict = _parse_label_pairs(label)
    client = get_client()
    result = client.create_concurrency_policy(
        name=name,
        capacity=capacity,
        scope=scope,
        queue_id=queue_id,
        label=label_dict,
        enabled=enabled,
    )
    if output_format == "plain":
        print("[green]Concurrency policy created:[/]")
        _print_concurrency_policy_plain(result)
        return
    _print_formatted(result, output_format)


@concurrency_policy_app.command("list")
def concurrency_policy_list(
    queue_id: Optional[str] = typer.Option(None, "--queue-id", help="Filter by queue_id"),
    skip: int = typer.Option(0, "--skip", help="Skip the first N entries"),
    limit: int = typer.Option(200, "--limit", help="Maximum number of entries to return"),
    output_format: str = typer.Option("plain", "--format", help="Output format: plain/json/yaml"),
):
    """List concurrency policies (visible to your associated queues)."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_concurrency_policies(queue_id=queue_id, skip=skip, limit=limit)
    items = result.get("concurrency_policies", []) if isinstance(result, dict) else []
    if output_format == "plain":
        _print_concurrency_policy_list_plain(items)
    else:
        _print_formatted(result, output_format)


@concurrency_policy_app.command("get")
def concurrency_policy_get(
    policy_id: str = typer.Argument(..., help="policy_id (admission key)"),
    output_format: str = typer.Option("plain", "--format", help="Output format: plain/json/yaml"),
):
    """Show concurrency policy details."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.get_concurrency_policy(policy_id)
    if output_format == "plain":
        _print_concurrency_policy_plain(result)
    else:
        _print_formatted(result, output_format)


@concurrency_policy_app.command("update")
def concurrency_policy_update(
    policy_id: str = typer.Argument(..., help="policy_id (admission key)"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New display name"),
    scope: Optional[str] = typer.Option(None, "--scope", help="New scope"),
    queue_id: Optional[str] = typer.Option(None, "--queue-id", help="New queue_id"),
    label: Optional[List[str]] = typer.Option(
        None, "--label", help="New label as key=value (repeatable; replaces existing)"
    ),
    capacity: Optional[int] = typer.Option(None, "--capacity", help="New capacity"),
    enabled: Optional[bool] = typer.Option(
        None, "--enabled/--no-enabled", help="Enable or disable the resource"
    ),
    reason: Optional[str] = typer.Option(None, "--reason", help="Audit reason for the change"),
    output_format: str = typer.Option("plain", "--format", help="Output format: plain/json/yaml"),
):
    """Partially update a concurrency policy (upsert: creates if absent; requires write access on the owning queue)."""
    output_format = _normalize_output_format(output_format)
    label_dict = _parse_label_pairs(label)
    if all(v is None for v in (name, scope, queue_id, label_dict, capacity, enabled)):
        raise typer.BadParameter("At least one field must be provided to update")
    client = get_client()
    result = client.update_concurrency_policy(
        policy_id,
        name=name,
        scope=scope,
        queue_id=queue_id,
        label=label_dict,
        capacity=capacity,
        enabled=enabled,
        reason=reason,
    )
    if output_format == "plain":
        print("[green]Concurrency resource updated:[/]")
        _print_concurrency_policy_plain(result)
        return
    _print_formatted(result, output_format)


@concurrency_policy_app.command("delete")
def concurrency_policy_delete(
    resource_ids: List[str] = typer.Argument(..., help="One or more policy_id values"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Delete one or more concurrency policies (requires write access on each resource's owning queue)."""
    if not yes:
        ids_str = ", ".join(resource_ids)
        typer.confirm(
            f"Permanently delete {len(resource_ids)} concurrency policy(s): {ids_str}?",
            abort=True,
        )
    client = get_client()
    failed: list[str] = []
    for policy_id in resource_ids:
        try:
            result = client.delete_concurrency_policy(policy_id)
        except APIError as e:
            if e.status_code == 404:
                print(f"[yellow]Concurrency resource not found, skipping:[/] {policy_id}")
                failed.append(policy_id)
                continue
            raise
        print(f"[green]Concurrency resource deleted:[/] {result.get('policy_id') or policy_id}")
    if failed:
        raise typer.Exit(1)


# ============================================================
# Template Credential commands
# ============================================================


def _print_template_credential_plain(tc: dict) -> None:
    print(f"  id:                {tc.get('id')}")
    print(f"  credential_name:   {tc.get('credential_name')}")
    print(f"  template:          {tc.get('template')}")
    print(f"  credential_type:   {tc.get('credential_type', '')}")
    content = tc.get("content") or {}
    if content:
        print(f"  content:           {json.dumps(content, ensure_ascii=False)}")
    print(f"  created_at:        {tc.get('created_at')}")
    print(f"  updated_at:        {tc.get('updated_at')}")


def _print_template_credential_list_plain(items: list) -> None:
    if not items:
        print("No template credentials found.")
        return
    _print_plain_table(
        items,
        [
            ("id", "id"),
            ("credential_name", "credential_name"),
            ("template", "template"),
            ("credential_type", "credential_type"),
            ("created_at", "created_at"),
        ],
    )


@template_credential_app.command("create")
def template_credential_create(
    credential_name: str = typer.Option(
        ..., "--name", "-n", help="Credential name (unique per template)"
    ),
    template: str = typer.Option(..., "--template", "-t", help="Template name"),
    credential_type: str = typer.Option(
        "", "--type", help="Credential type (for grouping credentials within a template)"
    ),
    content: str = typer.Option(..., "--content", "-c", help="Credential content as a JSON object"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Create a template credential."""
    output_format = _normalize_output_format(output_format)
    try:
        content_dict = json.loads(content)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"--content must be valid JSON: {exc}") from exc
    if not isinstance(content_dict, dict):
        raise typer.BadParameter("--content must be a JSON object")
    client = get_client()
    result = client.create_template_credential(
        credential_name=credential_name,
        template=template,
        credential_type=credential_type,
        content=content_dict,
    )
    if output_format == "plain":
        print("[green]Template credential created:[/]")
        _print_template_credential_plain(result)
        return
    _print_formatted(result, output_format)


@template_credential_app.command("list")
def template_credential_list(
    template: Optional[str] = typer.Option(
        None, "--template", "-t", help="Filter by template name"
    ),
    credential_name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Filter by credential name"
    ),
    credential_type: Optional[str] = typer.Option(None, "--type", help="Filter by credential type"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List template credentials."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_template_credentials(
        template=template,
        credential_name=credential_name,
        credential_type=credential_type,
    )
    if output_format == "plain":
        _print_template_credential_list_plain(result)
    else:
        _print_formatted(result, output_format)


@template_credential_app.command("get")
def template_credential_get(
    identifier: str = typer.Argument(..., help="Credential ID or credential_name"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Get a template credential by ID or credential_name."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.get_template_credential(identifier)
    if output_format == "plain":
        _print_template_credential_plain(result)
    else:
        _print_formatted(result, output_format)


@template_credential_app.command("update")
def template_credential_update(
    identifier: str = typer.Argument(..., help="Credential ID or credential_name"),
    content: Optional[str] = typer.Option(
        None, "--content", "-c", help="New credential content as a JSON object"
    ),
    credential_type: Optional[str] = typer.Option(None, "--type", help="New credential type"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Update a template credential's content and/or credential_type."""
    output_format = _normalize_output_format(output_format)
    content_dict = None
    if content is not None:
        try:
            content_dict = json.loads(content)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"--content must be valid JSON: {exc}") from exc
        if not isinstance(content_dict, dict):
            raise typer.BadParameter("--content must be a JSON object")
    if content_dict is None and credential_type is None:
        raise typer.BadParameter("Must provide --content and/or --type to update")
    client = get_client()
    result = client.update_template_credential(
        identifier=identifier,
        content=content_dict,
        credential_type=credential_type,
    )
    if output_format == "plain":
        print("[green]Template credential updated:[/]")
        _print_template_credential_plain(result)
        return
    _print_formatted(result, output_format)


@template_credential_app.command("delete")
def template_credential_delete(
    identifiers: List[str] = typer.Argument(
        ..., help="One or more credential IDs or credential_names"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Delete one or more template credentials."""
    if not yes:
        ids_str = ", ".join(identifiers)
        typer.confirm(
            f"Permanently delete {len(identifiers)} template credential(s): {ids_str}?",
            abort=True,
        )
    client = get_client()
    failed: list[str] = []
    for ident in identifiers:
        try:
            result = client.delete_template_credential(ident)
        except APIError as e:
            if e.status_code == 404:
                print(f"[yellow]Template credential not found, skipping:[/] {ident}")
                failed.append(ident)
                continue
            raise
        print(f"[green]Template credential deleted:[/] {result.get('id') or ident}")
    if failed:
        raise typer.Exit(1)


# ==================== WebSocket 交互式终端 ====================


async def _interactive_terminal(client, job_id: str, container: str):
    """WebSocket 交互式终端。"""
    import asyncio
    import signal
    import sys
    import termios
    import tty

    import websockets

    # 获取当前终端尺寸
    cols, rows = 0, 0
    if sys.stdin.isatty():
        try:
            cols, rows = os.get_terminal_size()
        except OSError:
            pass

    ws_uri, extra_headers = client.get_ws_terminal_info(job_id, container, cols=cols, rows=rows)

    original_settings = None
    if sys.stdin.isatty():
        original_settings = termios.tcgetattr(sys.stdin)

    try:
        async with websockets.connect(
            ws_uri,
            additional_headers=extra_headers,
            ping_interval=None,
        ) as ws:
            if original_settings:
                tty.setraw(sys.stdin)

            # 监听 SIGWINCH 信号，窗口大小变化时发送 resize 消息
            resize_event = asyncio.Event()

            def _on_sigwinch(signum, frame):
                resize_event.set()

            if sys.stdin.isatty():
                signal.signal(signal.SIGWINCH, _on_sigwinch)

            read_task = asyncio.create_task(_read_ws(ws))
            write_task = asyncio.create_task(_write_ws(ws))
            resize_task = asyncio.create_task(
                _handle_resize(ws, resize_event, original_settings is not None)
            )

            done, pending = await asyncio.wait(
                [read_task, write_task, resize_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for t in pending:
                t.cancel()
                try:
                    await t
                except asyncio.CancelledError:
                    pass
    except Exception as e:
        import typer

        typer.echo(f"\nconnection failed: {e}", err=True)
    finally:
        # 恢复 SIGWINCH 默认处理
        if sys.stdin.isatty():
            try:
                signal.signal(signal.SIGWINCH, signal.SIG_DFL)
            except (OSError, ValueError):
                pass
        if original_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)


async def _read_ws(ws):
    """从 WebSocket 读取数据并输出到 stdout。"""
    import json
    import sys

    try:
        async for message in ws:
            if isinstance(message, bytes):
                sys.stdout.buffer.write(message)
                sys.stdout.buffer.flush()
            else:
                try:
                    data = json.loads(message)
                    if "error" in data:
                        sys.stdout.write(f"\r\n[error] {data['error']}\r\n")
                        sys.stdout.flush()
                        break
                except (json.JSONDecodeError, TypeError):
                    sys.stdout.write(message)
                    sys.stdout.flush()
    except Exception:
        pass


async def _handle_resize(ws, resize_event, is_tty: bool):
    """监听终端 resize 事件并通过 WebSocket 发送尺寸调整消息。"""
    import asyncio
    import json
    import os

    if not is_tty:
        return
    try:
        while True:
            await resize_event.wait()
            resize_event.clear()
            try:
                cols, rows = os.get_terminal_size()
                await ws.send(json.dumps({"type": "resize", "cols": cols, "rows": rows}))
            except (OSError, Exception):
                pass
    except asyncio.CancelledError:
        pass
    except Exception:
        pass


async def _write_ws(ws):
    """从 stdin 读取并发送到 WebSocket。"""
    import asyncio
    import sys

    loop = asyncio.get_event_loop()
    try:
        while True:
            data = await loop.run_in_executor(None, sys.stdin.buffer.read, 1)
            if not data:
                break
            await ws.send(data.decode("utf-8", errors="replace"))
    except Exception:
        pass


async def _non_interactive_exec(client, job_id: str, container: str, command: list):
    """非交互式命令执行：发送命令，打印输出，命令完成后退出。"""
    import json
    import sys

    import websockets

    ws_uri, extra_headers = client.get_ws_terminal_info(
        job_id, container, command=command, tty=False
    )

    try:
        async with websockets.connect(
            ws_uri,
            additional_headers=extra_headers,
            ping_interval=None,
        ) as ws:
            async for message in ws:
                if isinstance(message, bytes):
                    sys.stdout.buffer.write(message)
                    sys.stdout.buffer.flush()
                else:
                    try:
                        data = json.loads(message)
                        if isinstance(data, dict) and "error" in data:
                            sys.stderr.write(f"[error] {data['error']}\n")
                            sys.stderr.flush()
                            raise typer.Exit(1)
                        sys.stdout.write(message)
                        sys.stdout.flush()
                    except (json.JSONDecodeError, TypeError):
                        sys.stdout.write(message)
                        sys.stdout.flush()
    except typer.Exit:
        raise
    except websockets.exceptions.ConnectionClosed:
        # 命令执行完毕后服务端关闭连接，属于正常结束
        pass
    except Exception as e:
        typer.echo(f"connection failed: {e}", err=True)
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Secret commands (Central AP)
# ---------------------------------------------------------------------------


def _mask_secret_value(value: str) -> str:
    """Mask a secret value for display."""
    if len(value) <= 1:
        return "*"
    if len(value) <= 8:
        return value[:1] + "***" + value[-1:]
    if len(value) <= 16:
        return value[:4] + "***" + value[-4:]
    return value[:8] + "***" + value[-4:]


def _mask_secret_data(data: dict) -> dict:
    """Mask secret data values for display."""
    if not data:
        return data
    masked = {}
    for k, v in data.items():
        if isinstance(v, str):
            masked[k] = _mask_secret_value(v)
        elif isinstance(v, dict):
            # File credential: show filename and size only
            filename = v.get("filename", "")
            size = v.get("size", len(str(v.get("content", ""))))
            masked[k] = {"filename": filename, "size": size}
        else:
            masked[k] = "***"
    return masked


def _mask_secret(secret: dict) -> dict:
    """Mask a secret dict for display."""
    if not secret:
        return secret
    result = dict(secret)
    if "data" in result and isinstance(result["data"], dict):
        result["data"] = _mask_secret_data(result["data"])
    return result


def _print_secret_plain(secret: dict) -> None:
    """Print a single secret in plain format."""
    # secret_id is the globally unique identifier — always show it so users
    # can copy it for cross-user job submissions (secret_id reference).
    secret_id = secret.get("secret_id", "")
    if secret_id:
        print(f"  Secret ID:   {secret_id}")
    print(f"  Name:        {secret.get('name', '')}")
    # workspace_id is part of the composite unique key — users need it to address
    # the secret by name (ap secret get/update/delete/grant -w <ws>).
    workspace_id = secret.get("workspace_id", "")
    if workspace_id:
        print(f"  WorkSpace:   {workspace_id}")
    role = secret.get("role", "")
    if role:
        role_display = "owner" if role == "owner" else "shared/use"
        print(f"  Role:        {role_display}")
    print(f"  Created By:  {secret.get('created_by', '')}")
    print(f"  Description: {secret.get('description', '')}")
    print(f"  Created At:  {secret.get('created_at', '')}")
    print(f"  Updated At:  {secret.get('updated_at', '')}")
    data = secret.get("data", {})
    if data:
        print("  Data:")
        for k, v in data.items():
            print(f"    {k}: {v}")


def _print_secret_list_plain(secrets: list[dict]) -> None:
    """Print a list of secrets in plain format."""
    if not secrets:
        print("No secrets found.")
        return
    for s in secrets:
        _print_secret_plain(s)
        print()


@secret_app.command("create")
def secret_create(
    name: str = typer.Option(
        ..., "--name", "-n", help="Credential name (unique within a WorkSpace)"
    ),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="Credential data (JSON object)"),
    from_file: Optional[list[str]] = typer.Option(
        None,
        "--from-file",
        help=(
            "Read a file into the secret data. Can be used multiple times. "
            "Use 'key=path' to set the data key explicitly, or just 'path' to use "
            "the file name as the key. The file is stored as a file-type credential "
            "{content, filename}."
        ),
    ),
    description: Optional[str] = typer.Option(None, "--description", help="Description"),
    workspace_id: str = typer.Option(
        "default",
        "--workspace-id",
        "-w",
        help="WorkSpace the credential belongs to (name unique within a WorkSpace; default: default)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """创建平台凭据（存入中心 MongoDB，自动同步到集群，不同步 K8s）。

    凭据归属 WorkSpace（名称在 WorkSpace 内唯一），建议每次都显式带上 ``-w``；
    省略时落到 ``default``，而 ``default`` 是所有人共享的命名空间，容易撞名。

    Examples:
        # Create a secret from inline JSON
        ap secret create --name my-cred -w ws-alpha --data '{"TOKEN": "value"}'

        # Create a secret from one or more files
        ap secret create --name my-cred -w ws-alpha --from-file ./id_rsa --from-file key=./config.json

        # Combine inline data and files
        ap secret create --name my-cred -w ws-alpha --data '{"TOKEN": "value"}' --from-file ./cert.pem
    """
    output_format = _normalize_output_format(output_format)
    if data is None and not from_file:
        raise typer.BadParameter("At least one of --data or --from-file is required")

    data_dict = _build_secret_data(data, from_file, output_format)

    client = get_client()
    result = client.create_secret(
        name=name,
        data=data_dict,
        description=description,
        workspace_id=workspace_id,
    )
    result = _mask_secret(result)
    if output_format == "plain":
        print("[green]Secret created:[/]")
        _print_secret_plain(result)
        return
    _print_formatted(result, output_format)


@secret_app.command("list")
def secret_list(
    page: int = typer.Option(1, "--page", help="Page number"),
    page_size: int = typer.Option(20, "--page-size", help="Page size"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """列出当前用户可访问的凭据（含被他人授权给自己的）。

    - [owner] 自己创建的凭据，含脱敏数据
    - [shared/use] 他人授权给自己的凭据，仅元信息（含 secret_id，可用于 job 提交）

    使用 --format json 可获取完整响应（含 secret_id）用于复制到 --overrides。
    """
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_secrets(page=page, page_size=page_size)
    # result is {data: [...], pagination: {...}}
    secrets = result.get("data", []) if isinstance(result, dict) else result
    if isinstance(secrets, list):
        secrets = [_mask_secret(s) for s in secrets]
    if output_format == "plain":
        _print_secret_list_plain(secrets)
    else:
        _print_formatted(result, output_format)


@secret_app.command("get")
def secret_get(
    name: str = typer.Argument(..., help="Credential name"),
    workspace_id: str = typer.Option(
        "default",
        "--workspace-id",
        "-w",
        help="WorkSpace the credential belongs to (located by name + workspace_id; default: default)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """查看凭据详情（脱敏）。

    可查看自己创建的凭据（owner）或他人授权给自己的凭据（use）。
    响应中的 secret_id 可用于 ap job create --overrides 中的 secret_id 字段，
    以精确引用特定凭据（跨用户同名凭据场景）。

    注意：凭据按 (name, workspace_id) 定位——用 -w 指定创建时所在的 WorkSpace，
    否则查的是 default。若自己和他人在同一 WorkSpace 各有同名凭据不可能发生
    （名称在 WorkSpace 内唯一）；跨 WorkSpace 精确查询请用
    ap secret get-by-id <secret_id>。
    """
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.get_secret(name, workspace_id=workspace_id)
    result = _mask_secret(result)
    if output_format == "plain":
        _print_secret_plain(result)
    else:
        _print_formatted(result, output_format)


@secret_app.command("update")
def secret_update(
    name: str = typer.Argument(..., help="Credential name"),
    data: Optional[str] = typer.Option(
        None, "--data", "-d", help="New credential data (JSON object)"
    ),
    from_file: Optional[list[str]] = typer.Option(
        None,
        "--from-file",
        help=(
            "Read a file into the secret data. Can be used multiple times. "
            "Use 'key=path' to set the data key explicitly, or just 'path' to use "
            "the file name as the key. The file is stored as a file-type credential "
            "{content, filename}."
        ),
    ),
    description: Optional[str] = typer.Option(None, "--description", help="New description"),
    workspace_id: str = typer.Option(
        "default",
        "--workspace-id",
        "-w",
        help="WorkSpace the credential belongs to (located by name + workspace_id; default: default)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """更新凭据。仅能更新自己创建的凭据；name / workspace_id 不可修改。

    ``--data`` / ``--from-file`` 的组合方式与 ``secret create`` 完全一致，但注意
    **data 是整体替换而非合并**：只传 ``--from-file`` 会把 data 换成只含该文件的内容。
    想在保留原有 key 的同时换掉其中一个文件，就把其余 key 一起用 ``--data`` 带上。

    Examples:
        # 只换一个文件型凭据（-w 要与创建时一致，否则改的是 default 里那条）
        ap secret update my-cred -w ws-alpha --from-file config.json=./config.json

        # 环境变量 + 文件一起替换
        ap secret update my-cred -w ws-alpha --data '{"TOKEN": "new"}' --from-file ./cert.pem

        # 只改备注，不动 data
        ap secret update my-cred -w ws-alpha --description "rotated 2026-08"
    """
    output_format = _normalize_output_format(output_format)
    if data is None and not from_file and description is None:
        raise typer.BadParameter("At least one of --data, --from-file or --description is required")

    data_dict = None
    if data is not None or from_file:
        data_dict = _build_secret_data(data, from_file, output_format)

    client = get_client()
    result = client.update_secret(
        name=name,
        data=data_dict,
        description=description,
        workspace_id=workspace_id,
    )
    result = _mask_secret(result)
    if output_format == "plain":
        print("[green]Secret updated:[/]")
        _print_secret_plain(result)
        return
    _print_formatted(result, output_format)


@secret_app.command("delete")
def secret_delete(
    names: List[str] = typer.Argument(..., help="One or more credential names"),
    workspace_id: str = typer.Option(
        "default",
        "--workspace-id",
        "-w",
        help="WorkSpace the credential belongs to (located by name + workspace_id; default: default)",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """删除凭据。仅能删除自己创建的凭据（同一 -w WorkSpace 内）。"""
    if not yes:
        typer.confirm(
            f"Delete secret(s) in workspace {workspace_id}: {', '.join(names)}?", abort=True
        )
    client = get_client()
    for name in names:
        try:
            client.delete_secret(name, workspace_id=workspace_id)
            print(f"[green]Deleted:[/] {name}")
        except APIError as exc:
            error_console.print(f"[red]Error deleting {name}:[/] {exc}")


@secret_app.command("grant")
def secret_grant(
    name: str = typer.Argument(..., help="Credential name"),
    to_user: Optional[str] = typer.Option(None, "--to-user", help="User ID to grant to"),
    to_group: Optional[str] = typer.Option(None, "--to-group", help="User group ID to grant to"),
    workspace_id: str = typer.Option(
        "default",
        "--workspace-id",
        "-w",
        help="WorkSpace the credential belongs to (located by name + workspace_id; default: default)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """授权用户或用户组使用凭据（use 权限）。仅凭据 owner 可操作。"""
    output_format = _normalize_output_format(output_format)
    if not to_user and not to_group:
        error_console.print("[red]Error:[/] must specify --to-user or --to-group")
        raise typer.Exit(code=1)
    if to_user and to_group:
        error_console.print("[red]Error:[/] specify only one of --to-user / --to-group")
        raise typer.Exit(code=1)
    client = get_client()
    try:
        if to_user:
            result = client.grant_secret_acl(name, "user", to_user, workspace_id=workspace_id)
            if output_format == "plain":
                print(f"[green]Granted use permission to user[/] {to_user}")
        else:
            result = client.grant_secret_acl(
                name, "user_group", to_group, workspace_id=workspace_id
            )
            if output_format == "plain":
                print(f"[green]Granted use permission to group[/] {to_group}")
        _print_formatted(result, output_format)
    except APIError as exc:
        error_console.print(f"[red]Error granting ACL:[/] {exc}")


@secret_app.command("revoke")
def secret_revoke(
    name: str = typer.Argument(..., help="Credential name"),
    from_user: Optional[str] = typer.Option(None, "--from-user", help="User ID to revoke from"),
    from_group: Optional[str] = typer.Option(
        None, "--from-group", help="User group ID to revoke from"
    ),
    workspace_id: str = typer.Option(
        "default",
        "--workspace-id",
        "-w",
        help="WorkSpace the credential belongs to (located by name + workspace_id; default: default)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """撤销用户或用户组的凭据使用权限。仅凭据 owner 可操作。"""
    output_format = _normalize_output_format(output_format)
    if not from_user and not from_group:
        error_console.print("[red]Error:[/] must specify --from-user or --from-group")
        raise typer.Exit(code=1)
    if from_user and from_group:
        error_console.print("[red]Error:[/] specify only one of --from-user / --from-group")
        raise typer.Exit(code=1)
    client = get_client()
    try:
        if from_user:
            result = client.revoke_secret_acl(name, "user", from_user, workspace_id=workspace_id)
            if output_format == "plain":
                print(f"[green]Revoked use permission from user[/] {from_user}")
        else:
            result = client.revoke_secret_acl(
                name, "user_group", from_group, workspace_id=workspace_id
            )
            if output_format == "plain":
                print(f"[green]Revoked use permission from group[/] {from_group}")
        _print_formatted(result, output_format)
    except APIError as exc:
        error_console.print(f"[red]Error revoking ACL:[/] {exc}")


@secret_app.command("acl")
def secret_acl(
    name: str = typer.Argument(..., help="Credential name"),
    workspace_id: str = typer.Option(
        "default",
        "--workspace-id",
        "-w",
        help="WorkSpace the credential belongs to (located by name + workspace_id; default: default)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """查看凭据的访问控制列表。仅凭据 owner 可查看。"""
    output_format = _normalize_output_format(output_format, keep_table=True)
    client = get_client()
    try:
        result = client.list_secret_acl(name, workspace_id=workspace_id)
        if output_format == "table":
            _print_records_table(result)
        else:
            _print_formatted(result, output_format)
    except APIError as exc:
        error_console.print(f"[red]Error listing ACL:[/] {exc}")


@secret_app.command("get-by-id")
def secret_get_by_id(
    secret_id: str = typer.Argument(
        ..., help="Globally unique secret ID (e.g. secret-uf600987gapsl25fwm7s)"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """按 secret_id 精确查询凭据（跨用户授权场景）。

    名称只在单个 WorkSpace 内唯一，因此当 B 被 A 授权使用某凭据、而 B 在自己的
    WorkSpace 里也有同名凭据时，按 name 查会落到自己那条；用 secret_id 可精确
    引用 A 的凭据，且无需知道它属于哪个 WorkSpace。

    secret_id 可通过以下方式获取：
    - 运行 ap secret list 或 ap secret get <name>（输出的 Secret ID 字段）
    - A 告知 B 或写在团队文档中

    使用场景：在 ap job create --overrides 中用 secret_id 精确指定凭据：
      --overrides '{"secret_env": {"MY_TOKEN": {"secret_id": "<id>", "secret_key": "TOKEN"}}}'
    """
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.get_secret_by_id(secret_id)
    result = _mask_secret(result)
    if output_format == "plain":
        _print_secret_plain(result)
    else:
        _print_formatted(result, output_format)


# ==================== Cluster commands ====================


_CLUSTER_LIST_COLUMNS: list[tuple[str, str]] = [
    ("url_cluster", "CLUSTER"),
    ("name", "NAME"),
    ("group", "GROUP"),
    ("region", "REGION"),
    ("default", "DEFAULT"),
    ("description", "DESCRIPTION"),
]


def _cluster_entries(client) -> list[dict]:
    result = client.list_clusters()
    entries = result.get("clusters") if isinstance(result, dict) else None
    return entries if isinstance(entries, list) else []


def _find_cluster_entry(entries: list[dict], key: str) -> Optional[dict]:
    """Match by url_cluster slug first, then case-insensitively by name."""
    for entry in entries:
        if entry.get("url_cluster") == key:
            return entry
    lowered = key.lower()
    for entry in entries:
        if str(entry.get("name") or "").lower() == lowered:
            return entry
    return None


def _print_cluster_list_plain(entries: list[dict]) -> None:
    current = _effective_cluster()
    rows = []
    for entry in entries:
        slug = entry.get("url_cluster") or ""
        description = entry.get("description") or ""
        if current and slug and current == slug:
            description = f"{description} (current)".strip()
        rows.append(
            {
                "url_cluster": slug,
                "name": entry.get("name") or "",
                "group": entry.get("group") or "",
                "region": entry.get("region") or "",
                "default": "*" if entry.get("default") else "",
                "description": description,
            }
        )
    _print_plain_table(rows, _CLUSTER_LIST_COLUMNS)


@cluster_app.command("list")
def cluster_list(
    show_all: bool = typer.Option(False, "--all", help="Include hidden clusters"),
    output_format: str = typer.Option("plain", "--format", help="Output format: plain/json/yaml"),
):
    """List platform-supported clusters.

    The CLUSTER column is the value accepted by --cluster / AP_CLUSTER.
    Does not require a cluster to be configured.
    """
    output_format = _normalize_output_format(output_format)
    client = get_client()
    entries = _cluster_entries(client)
    if not show_all:
        entries = [entry for entry in entries if not entry.get("hidden")]
    if output_format == "plain":
        _print_cluster_list_plain(entries)
    else:
        _print_formatted({"clusters": entries}, output_format)


@cluster_app.command("get")
def cluster_get(
    cluster: Optional[str] = typer.Argument(
        None, help="Cluster slug or name; defaults to the effective cluster"
    ),
    output_format: str = typer.Option("plain", "--format", help="Output format: plain/json/yaml"),
):
    """Show details of a single cluster."""
    output_format = _normalize_output_format(output_format)
    target = cluster.strip() if cluster and cluster.strip() else _effective_cluster()
    if not target:
        typer.echo(
            "error: no cluster specified; pass an argument or set --cluster / AP_CLUSTER. "
            "Run `ap cluster list` to see available clusters.",
            err=True,
        )
        raise typer.Exit(code=1)
    client = get_client()
    entry = _find_cluster_entry(_cluster_entries(client), target)
    if entry is None:
        typer.echo(
            f"error: cluster '{target}' not found; "
            "run `ap cluster list --all` to see all clusters.",
            err=True,
        )
        raise typer.Exit(code=1)
    if output_format != "plain":
        _print_formatted(entry, output_format)
        return
    _print_key_values(
        [
            ("Cluster", entry.get("url_cluster")),
            ("Name", entry.get("name")),
            ("Cluster ID", entry.get("cluster_id")),
            ("Region", entry.get("region")),
            ("Group", entry.get("group")),
            ("Default", str(bool(entry.get("default"))).lower()),
            ("Hidden", str(bool(entry.get("hidden"))).lower()),
            ("Quota", str(bool(entry.get("quota"))).lower()),
            ("Description", entry.get("description")),
        ],
        skip_empty=False,
    )


if __name__ == "__main__":
    main()
