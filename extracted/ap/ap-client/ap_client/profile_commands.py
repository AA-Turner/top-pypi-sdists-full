"""CLI sub-commands for Submission Profile management (ap profile ...)."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from ap_client import get_client
from ap_client.api import APIError  # noqa: F401
from ap_client.config import normalize_output_format
from rich import print
from rich.table import Table
from rich.text import Text


def _import_yaml():
    """Lazy-import PyYAML; raise BadParameter if not installed."""
    try:
        import yaml

        return yaml
    except ImportError as exc:
        raise typer.BadParameter("PyYAML is required for YAML support but not installed") from exc


profile_app = typer.Typer(help="Submission profile operations")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_output_format(output_format: str | None, default: str = "plain") -> str:
    try:
        return normalize_output_format(output_format, default)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc


def _print_formatted(data, output_format: str) -> None:
    if output_format == "json":
        typer.echo(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if output_format == "yaml":
        yaml = _import_yaml()
        typer.echo(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        return
    raise ValueError(f"Unexpected output format: {output_format!r}")


def _load_spec(
    file: Optional[Path],
    spec_inline: Optional[str],
) -> dict:
    """Load and validate spec from --file or --spec.

    Exactly one of the two must be provided. Returns parsed dict.
    """
    if file and spec_inline:
        print("[red]Error:[/] --file and --spec are mutually exclusive", file=sys.stderr)
        raise typer.Exit(1)
    if not file and not spec_inline:
        print("[red]Error:[/] Either --file or --spec is required", file=sys.stderr)
        raise typer.Exit(1)

    if file:
        if not file.exists():
            print(f"[red]Error:[/] File not found: {file}", file=sys.stderr)
            raise typer.Exit(1)
        content = file.read_text(encoding="utf-8")
        suffix = file.suffix.lower()
        if suffix in (".yaml", ".yml"):
            yaml = _import_yaml()
            try:
                data = yaml.safe_load(content)
            except yaml.YAMLError as exc:
                print(f"[red]Error:[/] Invalid YAML: {exc}", file=sys.stderr)
                raise typer.Exit(1) from exc
        else:
            # Default: treat as JSON
            try:
                data = json.loads(content)
            except json.JSONDecodeError as exc:
                print(f"[red]Error:[/] Invalid JSON: {exc}", file=sys.stderr)
                raise typer.Exit(1) from exc
    else:
        # Inline spec (JSON only)
        try:
            data = json.loads(spec_inline)  # type: ignore[arg-type]
        except json.JSONDecodeError as exc:
            print(f"[red]Error:[/] Invalid JSON in --spec: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc

    if not isinstance(data, dict):
        print(
            "[red]Error:[/] Spec must be a JSON object (dict), not a list or scalar",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    return data


def _load_metadata(metadata_inline: Optional[str]) -> Optional[dict]:
    """Parse the currently supported explicit profile metadata override."""
    if metadata_inline is None:
        return None
    try:
        data = json.loads(metadata_inline)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"Invalid JSON in --metadata: {exc}") from exc
    if not isinstance(data, dict):
        raise typer.BadParameter("Metadata must be a JSON object")
    unsupported_keys = set(data) - {"scaffold"}
    if unsupported_keys:
        raise typer.BadParameter(
            "--metadata only supports the scaffold key; "
            "dataset and split are derived from the profile spec"
        )
    return data


# Name constraint — single source of truth shared by help text, CLI
# validation, and error messages.  Server-side ValidateProfileName
# enforces the same rule; keep in sync when changing.
_NAME_CONSTRAINT = "3-128 chars, only [a-zA-Z0-9_-]"
_NAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,128}$")


def _fmt_dt(value: Optional[str]) -> str:
    """Parse ISO 8601 string and format as 'YYYY-MM-DD HH:MM:SS' for compact display.

    Date-only strings (e.g. '2026-05-25') are returned as-is without time.
    """
    if not value:
        return "-"
    raw = str(value)
    # Python < 3.11 fromisoformat doesn't accept "Z"
    s = raw.replace("Z", "+00:00")
    # Python < 3.11 fromisoformat only accepts 3 or 6 fractional digits; strip them
    s = re.sub(r"\.\d+", "", s)
    try:
        dt = datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return "-"
    # If original had no time component, return date only
    if "T" not in raw and " " not in raw.strip():
        return dt.strftime("%Y-%m-%d")
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _print_job_meta_plain(job_meta: dict) -> None:
    benchmark = job_meta.get("benchmark") or "(inherit from spec)"
    tags = ", ".join(job_meta.get("tags") or []) or "(none)"
    typer.echo(f"  Job benchmark default: {benchmark}")
    typer.echo(f"  Job tag defaults:      {tags}")


def _print_job_meta_result(result: dict, output_format: str) -> None:
    if output_format != "plain":
        _print_formatted(result, output_format)
        return
    typer.echo("Profile Job defaults saved. Profile version is unchanged.")
    payload = result.get("data", result)
    if isinstance(payload, dict) and isinstance(payload.get("job_meta"), dict):
        _print_job_meta_plain(payload["job_meta"])


def _print_profile_plain(profile: dict) -> None:
    """Pretty-print a single profile in plain format."""
    pid = profile.get("profile_id") or profile.get("id", "-")
    owner_id = profile.get("owner", "")
    owner_name = profile.get("owner_name") or owner_id or "-"
    owner_disp = f"{owner_name} ({owner_id})" if owner_id and owner_name != owner_id else owner_name
    verification = profile.get("verification")

    print(f"  [bold]ID:[/]           {pid}")
    print(f"  [bold]Name:[/]         {profile.get('name', '-')}")
    print(f"  [bold]Description:[/]  {profile.get('description') or '-'}")
    print(f"  [bold]Template:[/]     {profile.get('template', '-')}")
    print(f"  [bold]Account Pool:[/] {profile.get('account_pool') or '-'}")
    print(f"  [bold]Version:[/]      {profile.get('version', '-')}")
    print(f"  [bold]Owner:[/]        {owner_disp}")
    print(f"  [bold]Active:[/]       {profile.get('is_active', '-')}")
    if verification:
        print(
            f"  [bold]Verified:[/]     v{verification.get('version', '?')}"
            f" by {verification.get('verified_by', '-')}"
            f" (group={verification.get('group_id', '-')},"
            f" at {_fmt_dt(verification.get('verified_at'))})"
        )
    release = profile.get("release")
    if release:
        print(
            f"  [bold]Released:[/]     v{profile.get('version', '?')}"
            f" by {release.get('released_by', '-')}"
            f" (at {_fmt_dt(release.get('released_at'))})"
        )
    print(f"  [bold]Created:[/]      {_fmt_dt(profile.get('created_at'))}")
    print(f"  [bold]Updated:[/]      {_fmt_dt(profile.get('updated_at'))}")
    if profile.get("update_reason"):
        typer.echo(f"  Update reason: {profile['update_reason']}")
    if isinstance(profile.get("job_meta"), dict):
        _print_job_meta_plain(profile["job_meta"])

    spec = profile.get("spec")
    if not isinstance(spec, dict):
        return

    # Submission control fields (underscore-prefixed and well-known spec fields)
    submission_keys = (
        ("_submit_mode", "Submit Mode"),
        ("_dataset_key", "Dataset Key"),
        ("concurrency", "Concurrency"),
        ("batch_size", "Batch Size"),
        ("trials", "Trials"),
        ("trials_mode", "Trials Mode"),
        ("job_tags", "Job Tags"),
        ("agenthub_revision", "Agenthub Revision"),
    )
    submission_rows = [
        (label, spec.get(key)) for key, label in submission_keys if spec.get(key) is not None
    ]
    if submission_rows:
        print("\n  [bold]Submission:[/]")
        for label, value in submission_rows:
            print(f"    {label + ':':<20} {value}")

    params = spec.get("params")
    if isinstance(params, dict) and params:
        print(f"\n  [bold]Params[/] ({len(params)}):")
        width = max(len(k) for k in params.keys()) + 1
        for key in sorted(params.keys()):
            val = params[key]
            # Compact rendering for nested structures
            if isinstance(val, (dict, list)):
                val = json.dumps(val, ensure_ascii=False)
            print(f"    {key + ':':<{width}} {val}")

    group_post_process = spec.get("group_post_process")
    if isinstance(group_post_process, dict):
        print("\n  [bold]Group PostProcess:[/]")
        print(f"    {json.dumps(group_post_process, ensure_ascii=False)}")


def _print_profile_list_plain(data: dict) -> None:
    """Pretty-print a list of profiles using rich.Table."""
    # Handle apiserver PagedSuccess envelope: {code, message, data, pagination}
    items = data.get("data") or data.get("items") or data.get("profiles") or []
    pagination = data.get("pagination") or {}
    total = pagination.get("total", data.get("total", len(items)))
    page = pagination.get("page", data.get("page", 1))
    print(f"[bold]Profiles[/] (page {page}, showing {len(items)} of {total}):\n")
    if not items:
        print("  (none)")
        return

    table = Table(box=None, header_style="bold", show_edge=False, padding=(0, 1))
    table.add_column("ID", no_wrap=True)
    table.add_column("VER", no_wrap=True)
    table.add_column("TEMPLATE")
    table.add_column("NAME")
    table.add_column("OWNER")

    for p in items:
        pid = p.get("profile_id") or p.get("id", "-")
        owner = p.get("owner_name") or p.get("owner", "") or "-"
        table.add_row(
            pid,
            f"v{p.get('version', '?')}",
            p.get("template") or "-",
            p.get("name") or "-",
            owner,
        )
    print(table)


def _print_versions_plain(data: dict, profile_id: str) -> None:
    """Pretty-print version history using rich.Table."""
    # Handle apiserver PagedSuccess envelope: {code, message, data, pagination}
    items = data.get("data") or data.get("items") or data.get("versions") or []
    pagination = data.get("pagination") or {}
    total = pagination.get("total", data.get("total", len(items)))
    print(f"[bold]Versions for {profile_id}[/] ({total} total):\n")
    if not items:
        print("  (none)")
        return

    table = Table(box=None, header_style="bold", show_edge=False, padding=(0, 1))
    table.add_column("VER", no_wrap=True)
    table.add_column("NAME")
    table.add_column("TEMPLATE")
    table.add_column("UPDATED", no_wrap=True)
    table.add_column("VERIFIED")
    table.add_column("RELEASED")
    table.add_column("GROUP")
    table.add_column("REASON")

    for v in items:
        ver = v.get("verification") or {}
        table.add_row(
            f"v{v.get('version', '?')}",
            v.get("name") or "-",
            v.get("template") or "-",
            _fmt_dt(v.get("updated_at")),
            "true" if ver else "-",
            "true" if v.get("release") else "-",
            ver.get("group_id") or "-",
            Text(v.get("update_reason") or "-"),
        )
    print(table)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@profile_app.command("create")
def profile_create(
    name: str = typer.Option(..., "--name", "-n", help=f"Profile name ({_NAME_CONSTRAINT})"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Spec file (JSON or YAML)"),
    spec_inline: Optional[str] = typer.Option(
        None, "--spec", "-s", help="Inline spec as JSON string"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Profile description"
    ),
    account_pool: Optional[str] = typer.Option(
        None,
        "--account-pool",
        help="Default Account Pool ID used when a submission does not override it",
    ),
    metadata_inline: Optional[str] = typer.Option(
        None,
        "--metadata",
        help="Profile metadata override as JSON (currently only scaffold; dataset/split are derived)",
    ),
    tags: Optional[list[str]] = typer.Option(
        None, "--tag", help="Initial profile tag (repeatable)"
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Create a new submission profile."""
    if not _NAME_RE.match(name):
        print(
            f"[red]Error:[/] Invalid name: {_NAME_CONSTRAINT}",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    output_format = _normalize_output_format(output_format)
    spec = _load_spec(file, spec_inline)
    metadata = _load_metadata(metadata_inline)
    client = get_client()
    result = client.create_profile(
        name=name,
        spec=spec,
        description=description,
        account_pool=account_pool,
        metadata=metadata,
        tags=tags,
    )
    if output_format == "plain":
        print("[green]Profile created:[/]")
        _print_profile_plain(result)
    else:
        _print_formatted(result, output_format)


@profile_app.command("set-tags")
def profile_set_tags(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    tags: Optional[list[str]] = typer.Option(
        None, "--tag", help="Replacement profile tag (repeatable)"
    ),
    clear: bool = typer.Option(False, "--clear", help="Clear all profile tags"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Replace all tags on a submission profile."""
    if bool(tags) == clear:
        raise typer.BadParameter("exactly one of --tag or --clear is required")
    output_format = _normalize_output_format(output_format)
    client = get_client()
    replacement = [] if clear else tags or []
    result = client.replace_profile_tags(identifier, replacement)
    if output_format == "plain":
        payload = result.get("data", result) if isinstance(result, dict) else {}
        effective_tags = (
            payload.get("tags", replacement) if isinstance(payload, dict) else replacement
        )
        shown = ", ".join(effective_tags) if effective_tags else "(cleared)"
        print(f"[green]Profile tags updated:[/] {identifier} -> {shown}")
    else:
        _print_formatted(result, output_format)


@profile_app.command("patch-job-meta")
def profile_patch_job_meta(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    benchmark: Optional[str] = typer.Option(
        None, "--benchmark", help="Set the Job benchmark default; an empty value clears it"
    ),
    clear_benchmark: bool = typer.Option(
        False, "--clear-benchmark", help="Clear the live benchmark default and inherit from spec"
    ),
    append_tags: Optional[list[str]] = typer.Option(
        None, "--append-tag", help="Append a Job default tag (repeatable)"
    ),
    remove_tags: Optional[list[str]] = typer.Option(
        None, "--remove-tag", help="Remove an exact Job default tag (repeatable)"
    ),
    output_format: str = typer.Option(
        None, "--format", help="Output format: plain/table/json/yaml (default: AP_FORMAT or plain)"
    ),
):
    """Patch Job defaults without changing the Profile version.

    Omitted fields stay unchanged. Remove and append tags in one request to
    replace a keyed tag. Profile tags and spec are not changed.
    """
    output_format = _normalize_output_format(output_format)
    if benchmark is not None and clear_benchmark:
        raise typer.BadParameter("--benchmark and --clear-benchmark are mutually exclusive")
    patch: dict = {}
    if clear_benchmark or benchmark is not None:
        patch["benchmark"] = None if clear_benchmark else benchmark
    delta: dict = {}
    if append_tags:
        delta["append"] = append_tags
    if remove_tags:
        delta["remove"] = remove_tags
    if delta:
        patch["tags"] = delta
    if not patch:
        raise typer.BadParameter(
            "provide --benchmark, --clear-benchmark, --append-tag or --remove-tag"
        )
    result = get_client().update_profile_job_meta(identifier, patch)
    _print_job_meta_result(result, output_format)


@profile_app.command("update-job-meta")
def profile_update_job_meta(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    job_meta_json: str = typer.Option(
        ..., "--json", help="Complete job_meta JSON object; '{}' clears all live defaults"
    ),
    output_format: str = typer.Option(
        None, "--format", help="Output format: plain/table/json/yaml (default: AP_FORMAT or plain)"
    ),
):
    """Replace all Job defaults without changing the Profile version.

    Supply the full job_meta object using --json. Omitted fields are cleared;
    '{}' clears all live defaults. Use patch-job-meta to change selected fields.
    Profile tags and spec are not changed, and --reason is not required.
    """
    output_format = _normalize_output_format(output_format)
    try:
        job_meta = json.loads(job_meta_json)
        # Reject non-JSON constants such as NaN before constructing a request.
        json.dumps(job_meta, allow_nan=False)
    except ValueError as exc:
        raise typer.BadParameter(f"Invalid JSON: {exc}", param_hint="--json") from exc
    if not isinstance(job_meta, dict):
        raise typer.BadParameter("must be a JSON object", param_hint="--json")
    result = get_client().replace_profile_job_meta(identifier, job_meta)
    _print_job_meta_result(result, output_format)


@profile_app.command("list")
def profile_list(
    keyword: Optional[str] = typer.Option(None, "--keyword", "-k", help="Filter by name keyword"),
    template: Optional[str] = typer.Option(None, "--template", "-t", help="Filter by template"),
    dataset: Optional[str] = typer.Option(
        None, "--dataset", help="Filter by metadata dataset (case-insensitive substring)"
    ),
    scaffold: Optional[str] = typer.Option(
        None, "--scaffold", help="Filter by metadata scaffold (case-insensitive substring)"
    ),
    owner: Optional[str] = typer.Option(None, "--owner", help="Filter by owner ID"),
    profile_ids: Optional[list[str]] = typer.Option(
        None, "--profile-id", help="Filter by profile ID (repeatable; max 100)"
    ),
    tags: Optional[list[str]] = typer.Option(
        None, "--tag", help="Filter by tag (repeatable; max 10; combined with AND)"
    ),
    all_profiles: bool = typer.Option(
        False, "--all", "-a", help="Show all profiles (not just own)"
    ),
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    page_size: int = typer.Option(20, "--page-size", help="Items per page"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List submission profiles (default: own profiles only)."""
    if keyword and profile_ids:
        raise typer.BadParameter("--profile-id and --keyword are mutually exclusive")
    if owner and all_profiles:
        raise typer.BadParameter("--owner and --all are mutually exclusive")
    if profile_ids and len(profile_ids) > 100:
        raise typer.BadParameter("--profile-id accepts at most 100 values")
    if tags and len(tags) > 10:
        raise typer.BadParameter("--tag accepts at most 10 values")
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_profiles(
        keyword=keyword,
        template=template,
        dataset=dataset,
        scaffold=scaffold,
        owner=owner,
        profile_ids=profile_ids,
        tags=tags,
        show_all=all_profiles,
        page=page,
        page_size=page_size,
    )
    if output_format == "plain":
        _print_profile_list_plain(result)
    else:
        _print_formatted(result, output_format)


@profile_app.command("get")
def profile_get(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    version: Optional[int] = typer.Option(None, "--version", "-v", help="Get a specific version"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Get submission profile details (optionally a specific version)."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.get_profile(identifier, version=version)
    if output_format == "plain":
        _print_profile_plain(result)
    else:
        _print_formatted(result, output_format)


@profile_app.command("update")
def profile_update(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="New spec file (JSON or YAML)"),
    spec_inline: Optional[str] = typer.Option(
        None, "--spec", "-s", help="New inline spec as JSON string"
    ),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description"),
    reason: str = typer.Option(
        ..., "--reason", help="Required reason for this update (1-500 characters after trimming)"
    ),
    account_pool: Optional[str] = typer.Option(
        None,
        "--account-pool",
        help="Set the default Account Pool ID; pass an empty value to clear it",
    ),
    metadata_inline: Optional[str] = typer.Option(
        None,
        "--metadata",
        help="Profile metadata override as JSON (currently only scaffold; dataset/split are derived)",
    ),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Update a submission profile (full spec replacement).

    Renaming a profile is intentionally not supported via the CLI — the
    profile name is treated as a stable handle. Provide either --file or
    --spec to replace the spec. --reason is required and must contain 1-500
    characters after trimming. A previous version's reason is never reused.
    """
    output_format = _normalize_output_format(output_format)
    reason = reason.strip()
    if not reason:
        raise typer.BadParameter("must not be empty or whitespace", param_hint="--reason")
    if len(reason) > 500:
        raise typer.BadParameter("must be at most 500 characters", param_hint="--reason")
    spec = _load_spec(file, spec_inline)
    metadata = _load_metadata(metadata_inline)

    # Get current profile to fill in unchanged fields (name is preserved
    # verbatim so that the server's `name` required-field validation
    # passes without exposing rename as a CLI capability).
    client = get_client()
    current = client.get_profile(identifier)

    final_description = description if description is not None else current.get("description", "")
    final_account_pool = account_pool if account_pool is not None else current.get("account_pool")
    final_metadata = metadata if metadata is not None else current.get("metadata")

    result = client.update_profile(
        profile_id=current.get("profile_id") or current.get("id") or identifier,
        name=current.get("name", ""),
        spec=spec,
        description=final_description,
        account_pool=final_account_pool,
        metadata=final_metadata,
        reason=reason,
    )
    if output_format == "plain":
        print("[green]Profile updated:[/]")
        _print_profile_plain(result)
    else:
        _print_formatted(result, output_format)


@profile_app.command("delete")
def profile_delete(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Delete a submission profile."""
    if not yes:
        typer.confirm(f"Delete profile '{identifier}'?", abort=True)
    client = get_client()
    try:
        client.delete_profile(identifier)
    except APIError as e:
        if e.status_code == 404:
            print(f"[yellow]Profile not found:[/] {identifier}", file=sys.stderr)
            raise typer.Exit(1) from e
        raise
    print(f"[green]Profile deleted:[/] {identifier}")


@profile_app.command("versions")
def profile_versions(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    page_size: int = typer.Option(20, "--page-size", help="Items per page"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """List all versions of a submission profile."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.list_profile_versions(identifier, page=page, page_size=page_size)

    # The versions API only returns archived versions. On page 1 we prepend
    # the current (latest) version from get_profile so users see the full
    # version history — same strategy as the console frontend.
    if page == 1:
        current = client.get_profile(identifier)
        items_key = "data" if "data" in result else "items" if "items" in result else "versions"
        items = result.get(items_key) or []
        # Match the version-summary API instead of inferring fields from an
        # archived row: optional fields may exist only on the current version.
        # Keep spec and live job_meta out of the version-list response.
        fields = (
            "version",
            "name",
            "description",
            "template",
            "account_pool",
            "owner_name",
            "owner_realname",
            "author_name",
            "author_realname",
            "tags",
            "verification",
            "release",
            "update_reason",
            "updated_at",
        )
        current_item = {k: current[k] for k in fields if k in current}
        result[items_key] = [current_item] + items
        # Adjust total count (+1 for current version)
        if "pagination" in result:
            result["pagination"]["total"] = result["pagination"].get("total", len(items)) + 1
        elif "total" in result:
            result["total"] = result.get("total", len(items)) + 1

    if output_format == "plain":
        _print_versions_plain(result, identifier)
    else:
        _print_formatted(result, output_format)


@profile_app.command("verify")
def profile_verify(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    version: int = typer.Option(..., "--version", "-v", help="Version number to verify"),
    group_id: str = typer.Option(..., "--group-id", "-g", help="Group ID for verification"),
    output_format: str = typer.Option(
        None,
        "--format",
        help="Output format: plain/table/json/yaml (default: AP_FORMAT or command default)",
    ),
):
    """Verify a specific version of a submission profile."""
    output_format = _normalize_output_format(output_format)
    client = get_client()
    result = client.verify_profile_version(identifier, version=version, group_id=group_id)
    if output_format == "plain":
        print(f"[green]Profile version verified:[/] {identifier} v{version}")
        if isinstance(result, dict):
            verification = result.get("verification") or {}
            verified_by = verification.get("verified_by", "-")
            vgroup = verification.get("group_id", "-")
            verified_at = _fmt_dt(verification.get("verified_at"))
            print(f"  Verified by: {verified_by} (group={vgroup}, at {verified_at})")
    else:
        _print_formatted(result, output_format)


@profile_app.command("revoke-verify")
def profile_revoke_verify(
    identifier: str = typer.Argument(..., help="Profile ID or name"),
    version: int = typer.Option(
        ..., "--version", "-v", help="Version number to revoke verification"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Revoke verification for a specific version of a submission profile."""
    if not yes:
        typer.confirm(f"Revoke verification for '{identifier}' v{version}?", abort=True)
    client = get_client()
    client.revoke_profile_verification(identifier, version=version)
    print(f"[green]Verification revoked:[/] {identifier} v{version}")
