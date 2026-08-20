"""Task set subcommands for the cyclopts CLI.

A task set is a named, org-scoped, optionally-public list of task *references*
(`<org>/<name>[@version]`). It is a bookmark, not a bundle — see
``specs/task-sets/`` for the canonical contract.
"""

import typing as t
from pathlib import Path

import cyclopts
import yaml
from rich.table import Table

from dreadnode.app.api.client import ConflictError, NotFoundError
from dreadnode.app.cli.args import PlatformArgs
from dreadnode.app.cli.shared import (
    _FLAG_SEARCH,
    ArtifactRef,
    _collect_pages,
    _hint,
    _print_json,
    _render_list,
    _sync_progress,
    _visibility_markup,
    configured_dreadnode,
    confirm_destructive,
    console,
    print_error,
    print_success,
    print_warning,
    pull_environment_to_dir,
)

cli = cyclopts.App(
    name="task-set",
    help="Named, org-scoped lists of task references — curate suites and run them as one evaluation.",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _summarize_task_set(p: dict[str, t.Any]) -> str:
    """One-line task set summary for list output."""
    org = p.get("org_key")
    name = p.get("name", "unknown")
    qualified = f"{org}/{name}" if org else name
    visibility = "public" if p.get("is_public") else "private"
    count = p.get("member_count")
    members = f"[dim]{count} members[/dim]" if count is not None else ""
    source = p.get("source")
    suffix = f" [dim]-[/dim] {source}" if source else ""
    tags = p.get("tags")
    tag_suffix = f" [dim]{' '.join(f'#{tag}' for tag in tags)}[/dim]" if tags else ""
    return (
        f"[cyan]{qualified}[/cyan] {_visibility_markup(visibility)} {members}{suffix}{tag_suffix}"
    )


_TASK_SET_LIST_ROW_FIELDS: tuple[str, ...] = (
    "name",
    "org_key",
    "is_public",
    "member_count",
    "source",
    "tags",
    "created_at",
    "updated_at",
)


def _load_task_set_manifest(path: Path) -> dict[str, t.Any]:
    """Load a ``task-set.yaml`` manifest into a request body.

    Accepts a file or a directory containing ``task-set.yaml``. Members may be
    bare strings (``<org>/<name>`` or ``<org>/<name>@<version>``) or objects
    (``{task_name, task_version?, notes?}``); both forms are passed through
    verbatim and validated server-side against the manifest contract
    (TSS-MANI-*).
    """
    resolved = path.expanduser()
    if resolved.is_dir():
        resolved = resolved / "task-set.yaml"
    if not resolved.exists():
        raise FileNotFoundError(f"No task-set.yaml found at {resolved}")

    parsed = yaml.safe_load(resolved.read_text())
    if parsed is None:
        raise ValueError("task-set.yaml is empty")
    if not isinstance(parsed, dict):
        raise TypeError("task-set.yaml must contain a YAML mapping")
    if "members" not in parsed:
        raise ValueError("task-set.yaml must include a 'members' list")
    return dict(parsed)


def _print_warnings(warnings: object) -> None:
    """Surface the TSS-VIS-003 publish warnings loudly on a public write."""
    if not isinstance(warnings, list) or not warnings:
        return
    print_warning(f"This set is public but {len(warnings)} member(s) are not publicly runnable:")
    for warning in warnings:
        console.print(f"  [dim]-[/dim] {warning}")


def _member_status(member: dict[str, t.Any]) -> str:
    """Color-coded resolution status for a member row."""
    reason = member.get("unresolvable_reason")
    if reason:
        return f"[red]{reason}[/red]"
    resolved = member.get("task_version_resolved")
    return (
        f"[green]resolved[/green] [dim]{resolved}[/dim]" if resolved else "[green]resolved[/green]"
    )


def _run_hint(ref: str) -> str:
    """The next-step command that turns a set into an evaluation."""
    return f"dn evaluation create --task-set {ref} --model <model>"


def _parse_member_ref(raw: str) -> tuple[str, str | None]:
    """Split a member reference into ``(task_name, version)``.

    Members are org-qualified — ``<org>/<name>`` (bare) or
    ``<org>/<name>@<version>`` (pinned). The bare-vs-pinned distinction is
    preserved verbatim; the API owns grammar validation (TSS-MANI-004/005).
    """
    name, sep, version = raw.partition("@")
    name = name.strip().strip("/")
    if "/" not in name:
        raise ValueError(
            f"member '{raw}' must be org-qualified as '<org>/<name>' (a bare task name is rejected)"
        )
    pinned = version.strip() or None if sep else None
    return name, pinned


def _member_key(task_name: str, version: str | None) -> tuple[str, str | None]:
    """Identity of a member for de-duplication and matching (TSS-MANI-006)."""
    return (task_name, version)


def _resolved_to_manifest_member(member: dict[str, t.Any]) -> str | dict[str, t.Any]:
    """Convert a server *detail* member back into a *manifest* member.

    Uses ``task_version_pinned`` — the author's bare/pinned intent — never the
    read-time ``task_version_resolved``, so a round-trip doesn't silently pin a
    bare reference. Members with notes keep the object form; the rest collapse
    to the compact ``<org>/<name>[@<version>]`` string.
    """
    task_name = member.get("task_name", "")
    pinned = member.get("task_version_pinned")
    notes = member.get("notes")
    if notes:
        out: dict[str, t.Any] = {"task_name": task_name}
        if pinned:
            out["task_version"] = pinned
        out["notes"] = notes
        return out
    return f"{task_name}@{pinned}" if pinned else task_name


def _manifest_members_from_detail(detail: dict[str, t.Any]) -> list[str | dict[str, t.Any]]:
    """The full member list of a set in manifest form, order preserved."""
    return [_resolved_to_manifest_member(m) for m in (detail.get("members") or [])]


def _update_body_from_detail(detail: dict[str, t.Any], members: list[t.Any]) -> dict[str, t.Any]:
    """Build a full-replace PUT body that carries metadata forward (TSS-MUT-001).

    A PUT replaces description/tags/source/members, so they must be echoed back
    or they reset to defaults. Visibility is not part of a PUT — it is owned by
    the visibility endpoint and left untouched here — so ``is_public`` is omitted.
    Only ``members`` changes on an add/remove.
    """
    body: dict[str, t.Any] = {"members": members}
    for key in ("description", "tags", "source"):
        value = detail.get(key)
        if value is not None:
            body[key] = value
    return body


def _dump_manifest(manifest: dict[str, t.Any]) -> str:
    """Serialize a manifest dict to YAML with a stable, human-friendly key order."""
    ordered = {
        key: manifest[key]
        for key in ("name", "description", "source", "tags", "is_public", "members")
        if key in manifest
    }
    return yaml.safe_dump(ordered, sort_keys=False, default_flow_style=False)


def _manifest_from_detail(detail: dict[str, t.Any], *, name: str) -> dict[str, t.Any]:
    """Project a set detail into an authorable manifest (for pull/clone)."""
    manifest: dict[str, t.Any] = {"name": name}
    if detail.get("description"):
        manifest["description"] = detail["description"]
    if detail.get("source"):
        manifest["source"] = detail["source"]
    if detail.get("tags"):
        manifest["tags"] = list(detail["tags"])
    if detail.get("is_public"):
        manifest["is_public"] = True
    manifest["members"] = _manifest_members_from_detail(detail)
    return manifest


_INIT_TEMPLATE = """\
# Task set — a named, org-scoped list of task references you can run as one
# evaluation. Upload with `dn task-set push`; inspect with `dn task-set info`.
name: {name}

# Optional catalog metadata (uncomment to use).
# description: One-line summary of what this suite covers.
# source: Suite or group this set belongs to (e.g. apex, portswigger).
# tags:
#   - web
#   - sqli

# When true, the set *listing* becomes visible to other organizations. Member
# task visibility is unchanged. Defaults to false (org-only).
# is_public: false

# Members are task references: '<org>/<name>' (latest visible version) or
# '<org>/<name>@<version>' (pinned). Use the object form to attach notes.
members:
  - your-org/example-task
  # - your-org/example-task@1.2.0
  # - task_name: your-org/another-task
  #   notes: why this one is in the suite
"""


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------


@cli.command(alias="new")
def init(
    name: str,
    *,
    path: Path | None = None,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
) -> None:
    """Scaffold a ``task-set.yaml`` manifest ready to edit and push.

    Writes a commented starter manifest — every field appears with a one-line
    hint, so the file doubles as an entry point to the manifest contract. Edit
    the members, then run ``dn task-set push`` to upload.

    Args:
        name: Name for the new set (kebab-case, e.g. apex-web).
        path: Manifest file or a directory to write task-set.yaml into
            (default: ./task-set.yaml).
        force: Overwrite an existing manifest at the target path.
    """
    target = (path or Path("task-set.yaml")).expanduser()
    if target.is_dir():
        target = target / "task-set.yaml"
    if target.exists() and not force:
        raise FileExistsError(f"{target} already exists — use --force to overwrite")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_INIT_TEMPLATE.format(name=name))
    print_success(f"Wrote {target}")

    console.print()
    console.print("[bold]Next steps[/bold]")
    console.print(f"  1. Edit {target} — replace the example members with real task refs.")
    console.print(f"  2. Run `dn task-set push {target}` to upload.")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    search: t.Annotated[str | None, cyclopts.Parameter(name=_FLAG_SEARCH)] = None,
    tag: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(name="--tag", negative_iterable=()),
    ] = None,
    source: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(name="--source", negative_iterable=()),
    ] = None,
    contains: t.Annotated[str | None, cyclopts.Parameter(name="--contains")] = None,
    limit: int = 50,
    include_public: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show task sets in your organization.

    Args:
        search: Full-text search across name, description, source, and tags.
        tag: Filter to sets carrying this tag. Repeatable (any-of).
        source: Filter by source. Repeatable (any-of).
        contains: Filter to sets referencing a task — '<org>/<name>' (any
            version) or '<org>/<name>@<version>' (exact pinned version).
        limit: Maximum results to show.
        include_public: Include public sets from other organizations.
        as_json: Output raw JSON instead of a summary.
    """
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_task_sets(
            profile.org_key,
            search=search,
            tags=tag,
            source=source,
            contains=contains,
            page=page,
            limit=page_size,
            include_public=include_public,
        ),
        limit=limit,
        page_size=100,
        items_key="task_sets",
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_task_set,
        empty_msg="No task sets found",
        fields=_TASK_SET_LIST_ROW_FIELDS,
    )
    if not as_json and items:
        first = items[0]
        org = first.get("org_key", profile.org_key)
        _hint(f"dn task-set info {org}/{first.get('name', '<name>')}")


# ---------------------------------------------------------------------------
# info
# ---------------------------------------------------------------------------


@cli.command()
def info(
    ref: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show a task set with each member's per-caller resolution status.

    Members are resolved under your visibility at read time. Cross-org members
    you cannot see collapse to 'not_found' — the platform never discloses
    whether a task in another org exists (TSS-RES-004).

    Args:
        ref: Task set to inspect (e.g. apex-web or acme/apex-web).
        as_json: Output raw JSON instead of a table.
    """
    api, profile = platform.connect()
    set_ref = ArtifactRef.parse(ref, profile.org_key)
    if set_ref.version is not None:
        raise ValueError("task sets are not versioned — drop the '@version' suffix")

    detail = api.get_task_set(set_ref.org, set_ref.name)

    if as_json:
        _print_json(detail)
        return

    console.print(_summarize_task_set(detail))
    if detail.get("description"):
        console.print(f"  [dim]{detail['description']}[/dim]")
    set_id = detail.get("id")
    if set_id:
        console.print(f"  [dim]id:[/dim] [dim]{set_id}[/dim]")
    byline = detail.get("created_by_user") or {}
    author = byline.get("name") or byline.get("email") if isinstance(byline, dict) else None
    if author:
        console.print(f"  [dim]created by:[/dim] {author}")

    _print_warnings(detail.get("warnings"))

    members = detail.get("members") or []
    unresolvable = detail.get("unresolvable_count") or 0
    if unresolvable:
        console.print(
            f"  [dim]{unresolvable} of {len(members)} members unresolvable under you[/dim]"
        )

    if members:
        owns = (
            detail.get("organization_id") is not None and detail.get("org_key") == profile.org_key
        )
        has_notes = any(m.get("notes") for m in members)
        table = Table(show_header=True, title_style="bold")
        table.add_column("Member", style="cyan")
        table.add_column("Pinned", style="dim")
        table.add_column("Status")
        if owns:
            table.add_column("Publicly runnable")
        if has_notes:
            table.add_column("Notes", style="dim")
        for member in members:
            row = [
                member.get("task_name", "unknown"),
                member.get("task_version_pinned") or "-",
                _member_status(member),
            ]
            if owns:
                runnable = member.get("publicly_runnable")
                row.append("[green]yes[/green]" if runnable else "[yellow]no[/yellow]")
            if has_notes:
                row.append(member.get("notes") or "")
            table.add_row(*row)
        console.print(table)

    _hint(_run_hint(set_ref.qualified_name))


# ---------------------------------------------------------------------------
# push
# ---------------------------------------------------------------------------


def _rehome_manifest_member(
    member: str | dict[str, t.Any], target_org: str, leaf: str | None = None
) -> str | dict[str, t.Any]:
    """Rewrite a manifest member's org to *target_org*, preserving name/version/notes.

    ``push --with-members`` republishes every member environment under the pushing
    profile's org, so the manifest must reference members there or it would dangle
    (CLI-SYNC-041). Only the org segment of the task name changes; the pinned
    version and notes are preserved.

    *leaf* overrides the leaf name taken from the manifest. Callers that know the
    identity a member was actually published under should pass it, because the
    manifest leaf and the published name can differ (see the caller in ``push``).
    """
    if isinstance(member, str):
        ref, sep, version = member.partition("@")
        resolved_leaf = leaf or ref.split("/")[-1]
        rehomed = f"{target_org}/{resolved_leaf}"
        return f"{rehomed}@{version}" if sep else rehomed
    if isinstance(member, dict):
        out = dict(member)
        resolved_leaf = leaf or str(out.get("task_name", "")).split("/")[-1]
        out["task_name"] = f"{target_org}/{resolved_leaf}"
        return out
    return member


def _member_task_name(member: str | dict[str, t.Any]) -> str:
    """The org-qualified task name of a manifest member, ignoring any version."""
    if isinstance(member, dict):
        return str(member.get("task_name", ""))
    if isinstance(member, str):
        return member.partition("@")[0].strip().strip("/")
    return ""


@cli.command(alias="upload")
def push(
    path: Path | None = None,
    *,
    name: str | None = None,
    public: t.Annotated[bool | None, cyclopts.Parameter(name="--public")] = None,
    with_members: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Create or replace a task set from a ``task-set.yaml`` manifest.

    Upserts into your organization: a set with the manifest's name is replaced
    in full (TSS-MUT-001), otherwise it is created. Publishing is ungated — if
    the result is public, any member that is not publicly runnable is surfaced
    as a warning but never blocks the write (TSS-VIS-002/003).

    Pass ``--with-members`` to push a bundle produced by ``pull --with-members``:
    every member task environment under the directory is published first (so the
    manifest never references tasks that don't yet exist on the target), then the
    manifest is upserted. If any member fails to publish, the manifest is not
    written.

    Args:
        path: Manifest file or a directory containing task-set.yaml
            (default: ./task-set.yaml). With ``--with-members`` this must be the
            bundle directory.
        name: Override the manifest's set name.
        public: Force is_public on (--public) or off (--no-public),
            overriding the manifest.
        with_members: First publish member task environments found under the
            directory, then upsert the manifest.
        as_json: Output the resulting set as JSON.
    """
    manifest_source = path or Path("task-set.yaml")
    request = _load_task_set_manifest(manifest_source)
    if name:
        request["name"] = name
    if public is not None:
        request["is_public"] = public

    set_name = request.get("name")
    if not set_name or not isinstance(set_name, str):
        raise ValueError("task-set.yaml must include a 'name' (or pass --name)")

    api, profile = platform.connect()

    if with_members:
        # Local import: dreadnode.app.main imports the CLI modules.
        from dreadnode.app.main import _load_environment_metadata

        bundle_dir = Path(manifest_source).expanduser()
        if not bundle_dir.is_dir():
            bundle_dir = bundle_dir.parent
        dn = configured_dreadnode(platform)
        env_result = dn.sync_environments(
            bundle_dir,
            on_progress=_sync_progress,
            on_status=lambda msg: console.print(msg),
        )
        console.print(
            f"Members: [green]{len(env_result.uploaded)} pushed[/green], "
            f"[dim]{len(env_result.skipped)} skipped[/dim], "
            f"[red]{len(env_result.failed)} failed[/red]"
        )
        if not env_result.ok:
            raise RuntimeError("Member environments failed to publish — manifest not written")

        # Members were republished under this profile's org; rewrite the manifest
        # refs to match so the pushed set never dangles (CLI-SYNC-041).
        #
        # The published identity is each bundle directory's `task.yaml` name, which
        # is what sync_environments reports — NOT the manifest leaf. `push --name`
        # overrides the registry name without rewriting task.yaml, so a member
        # published as <org>/newname can still declare `name: oldname` inside. Keying
        # off the manifest leaf would reject that bundle even though every member
        # published fine, so rehome to what actually landed.
        published = set(env_result.uploaded) | set(env_result.skipped)
        original_members = request.get("members", [])
        rehomed_members: list[str | dict[str, t.Any]] = []
        leaf_source: dict[str, str] = {}

        for original in original_members:
            source_name = _member_task_name(original)
            member_dir = bundle_dir / source_name
            if not (member_dir / "task.yaml").is_file():
                raise FileNotFoundError(
                    f"member '{source_name}' has no task environment in the bundle — "
                    "re-pull with --with-members or drop it from task-set.yaml"
                )
            leaf, _version = _load_environment_metadata(member_dir)
            if leaf not in published:
                raise RuntimeError(
                    f"member '{source_name}' declares '{leaf}' in its task.yaml but was "
                    "not published under that name — refusing to write a manifest that "
                    "would reference a missing member"
                )
            # Two members sharing a published name across source orgs (acme/foo +
            # beta/foo) both land on <org>/foo, silently merging into one task.
            prior = leaf_source.get(leaf)
            if prior is not None and prior != source_name:
                raise ValueError(
                    f"members '{prior}' and '{source_name}' both rehome to "
                    f"'{profile.org_key}/{leaf}' — cross-org members sharing a leaf "
                    "name can't be pushed into a single org"
                )
            leaf_source[leaf] = source_name
            rehomed_members.append(_rehome_manifest_member(original, profile.org_key, leaf))

        request["members"] = rehomed_members

    try:
        api.get_task_set(profile.org_key, set_name)
    except NotFoundError:
        exists = False
    else:
        exists = True

    if exists:
        # A PUT replaces the editable record but never changes visibility
        # (TSS-MUT-001) — strip is_public from the body and apply an explicit
        # --public/--no-public through the dedicated visibility endpoint.
        update_body = {k: v for k, v in request.items() if k not in ("name", "is_public")}
        result = api.update_task_set(profile.org_key, set_name, update_body)
        verb = "Replaced"
        if public is not None and bool(result.get("is_public")) != public:
            visibility = api.update_task_set_visibility(profile.org_key, set_name, is_public=public)
            result["is_public"] = visibility.get("is_public", public)
            if visibility.get("warnings") is not None:
                result["warnings"] = visibility["warnings"]
    else:
        result = api.create_task_set(profile.org_key, request)
        verb = "Created"

    if as_json:
        _print_json(result)
        return

    _print_warnings(result.get("warnings"))
    member_count = result.get("member_count", len(request.get("members", [])))
    print_success(
        f"{verb} [cyan]{profile.org_key}/{set_name}[/cyan] [dim]({member_count} members)[/dim]"
    )
    _hint(f"dn task-set info {profile.org_key}/{set_name}")
    _hint(_run_hint(f"{profile.org_key}/{set_name}"))


# ---------------------------------------------------------------------------
# add / remove
# ---------------------------------------------------------------------------


@cli.command()
def add(
    ref: str,
    members: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Add one or more task references to an existing set.

    A convenience over editing the manifest: the current set is read, the new
    members are appended, and the full set is written back (TSS-MUT-001 — the
    API has no member-level patch). Members already present are left untouched.

    Args:
        ref: Task set to edit (e.g. apex-web or acme/apex-web).
        members: Task references to add, '<org>/<name>' or
            '<org>/<name>@<version>'. Repeatable.
    """
    api, profile = platform.connect()
    set_ref = ArtifactRef.parse(ref, profile.org_key)
    if set_ref.version is not None:
        raise ValueError("task sets are not versioned — drop the '@version' suffix")

    detail = api.get_task_set(set_ref.org, set_ref.name)
    manifest_members = _manifest_members_from_detail(detail)
    existing = {
        _member_key(m.get("task_name", ""), m.get("task_version_pinned"))
        for m in (detail.get("members") or [])
    }

    added: list[str] = []
    for raw in members:
        task_name, version = _parse_member_ref(raw)
        key = _member_key(task_name, version)
        display = f"{task_name}@{version}" if version else task_name
        if key in existing:
            console.print(f"  [dim]-[/dim] {display} [dim]already a member[/dim]")
            continue
        existing.add(key)
        manifest_members.append(f"{task_name}@{version}" if version else task_name)
        added.append(display)

    if not added:
        console.print("[dim]Nothing to add[/dim]")
        return

    result = api.update_task_set(
        set_ref.org, set_ref.name, _update_body_from_detail(detail, manifest_members)
    )
    _print_warnings(result.get("warnings"))
    print_success(
        f"Added {len(added)} member(s) to [cyan]{set_ref.qualified_name}[/cyan] "
        f"[dim]({result.get('member_count', len(manifest_members))} total)[/dim]"
    )
    _hint(f"dn task-set info {set_ref.qualified_name}")


@cli.command()
def remove(
    ref: str,
    members: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Remove one or more task references from a set.

    Matches members exactly: a bare ref ('<org>/<name>') removes the bare
    member, a pinned ref ('<org>/<name>@<version>') removes that pinned member.
    The set is read and rewritten in full (TSS-MUT-001).

    Args:
        ref: Task set to edit (e.g. apex-web or acme/apex-web).
        members: Task references to remove. Repeatable.
    """
    api, profile = platform.connect()
    set_ref = ArtifactRef.parse(ref, profile.org_key)
    if set_ref.version is not None:
        raise ValueError("task sets are not versioned — drop the '@version' suffix")

    detail = api.get_task_set(set_ref.org, set_ref.name)
    current = detail.get("members") or []

    drop: set[tuple[str, str | None]] = set()
    for raw in members:
        task_name, version = _parse_member_ref(raw)
        drop.add(_member_key(task_name, version))

    kept: list[str | dict[str, t.Any]] = []
    removed = 0
    for member in current:
        key = _member_key(member.get("task_name", ""), member.get("task_version_pinned"))
        if key in drop:
            removed += 1
            continue
        kept.append(_resolved_to_manifest_member(member))

    if not removed:
        console.print("[dim]No matching members to remove[/dim]")
        return
    if not kept:
        raise ValueError(
            "a set must keep at least one member — to delete the set entirely run "
            f"`dn task-set delete {set_ref.qualified_name}`"
        )

    result = api.update_task_set(set_ref.org, set_ref.name, _update_body_from_detail(detail, kept))
    _print_warnings(result.get("warnings"))
    print_success(
        f"Removed {removed} member(s) from [cyan]{set_ref.qualified_name}[/cyan] "
        f"[dim]({result.get('member_count', len(kept))} remaining)[/dim]"
    )


# ---------------------------------------------------------------------------
# pull / clone
# ---------------------------------------------------------------------------


def _pull_set_members(
    dn: t.Any,
    detail: dict[str, t.Any],
    directory: Path,
    *,
    force: bool,
) -> tuple[list[str], list[str], list[tuple[str, str]]]:
    """Pull each member environment of a set into ``directory/<org>/<name>``.

    Members carry their org-qualified ``task_name`` and the author's pinned
    version (if any); a bare member pulls the latest. The destination is keyed by
    the **org-qualified** name so members that share a leaf name across orgs don't
    collide (CLI-SYNC-040). Returns (pulled, skipped, failed) by short task name.
    """
    pulled: list[str] = []
    skipped: list[str] = []
    failed: list[tuple[str, str]] = []

    for member in detail.get("members") or []:
        task_name = member.get("task_name")
        if not task_name:
            continue
        pinned = member.get("task_version_pinned")
        short = task_name.split("/")[-1]
        ref_uri = f"environment://{task_name}" + (f":{pinned}" if pinned else "")
        dest = (directory / task_name).resolve()
        try:
            if pull_environment_to_dir(dn, ref_uri, dest, force=force):
                pulled.append(short)
            else:
                skipped.append(short)
        except Exception as e:
            failed.append((short, str(e)))

    return pulled, skipped, failed


@cli.command(alias="export")
def pull(
    ref: str,
    path: Path | None = None,
    *,
    with_members: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Export a set to a local ``task-set.yaml`` you can edit and re-push.

    The reverse of ``push``: members come down in the author's bare/pinned form
    (never the read-time resolved version), so a pull/edit/push round-trip
    doesn't silently pin bare references.

    A set is a bookmark, not a bundle — by default only the manifest is written.
    Pass ``--with-members`` to also pull each member's task environment into the
    target directory (one subfolder per task), producing a self-contained bundle
    you can carry onto an air-gapped instance and push there.

    Args:
        ref: Task set to export (e.g. apex-web or acme/apex-web).
        path: File or directory to write task-set.yaml into
            (default: ./task-set.yaml). With ``--with-members`` this is always
            treated as a directory.
        with_members: Also pull each member's task environment alongside the manifest.
        force: Overwrite an existing manifest / member directories at the target.
    """
    api, profile = platform.connect()
    set_ref = ArtifactRef.parse(ref, profile.org_key)
    if set_ref.version is not None:
        raise ValueError("task sets are not versioned — drop the '@version' suffix")

    if with_members:
        base_dir = (path or Path()).expanduser()
        if base_dir.exists() and not base_dir.is_dir():
            raise NotADirectoryError(
                f"{base_dir} is not a directory — --with-members writes a bundle directory"
            )
        base_dir.mkdir(parents=True, exist_ok=True)
        target = base_dir / "task-set.yaml"
    else:
        base_dir = None
        target = (path or Path("task-set.yaml")).expanduser()
        if target.is_dir():
            target = target / "task-set.yaml"
    if target.exists() and not force:
        raise FileExistsError(f"{target} already exists — use --force to overwrite")

    detail = api.get_task_set(set_ref.org, set_ref.name)
    manifest = _manifest_from_detail(detail, name=set_ref.name)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_dump_manifest(manifest))
    member_count = detail.get("member_count", len(manifest["members"]))
    print_success(
        f"Exported [cyan]{set_ref.qualified_name}[/cyan] to {target} ({member_count} members)"
    )

    if with_members and base_dir is not None:
        dn = configured_dreadnode(platform)
        pulled, skipped, failed = _pull_set_members(dn, detail, base_dir, force=force)
        for name in pulled:
            print_success(name, indent=2)
        for name, err in failed:
            print_error(f"{name}: {err}", indent=2)
        console.print(
            f"Members: [green]{len(pulled)} pulled[/green], "
            f"[dim]{len(skipped)} skipped[/dim], [red]{len(failed)} failed[/red]"
        )
        if failed:
            raise SystemExit(1)

    _hint(f"dn task-set push {target}")


@cli.command()
def clone(
    ref: str,
    name: str | None = None,
    *,
    public: t.Annotated[bool, cyclopts.Parameter(name="--public", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Copy a set into your organization under a new name.

    Reads the source set (your org, or any public set from another org) and
    re-creates it in your org. Members carry over in their bare/pinned form;
    the copy starts private unless ``--public`` is passed.

    Args:
        ref: Source set to copy (e.g. apex-web or acme/apex-web).
        name: Name for the copy (default: the source name).
        public: Make the copy public immediately.
    """
    api, profile = platform.connect()
    src_ref = ArtifactRef.parse(ref, profile.org_key)
    if src_ref.version is not None:
        raise ValueError("task sets are not versioned — drop the '@version' suffix")

    detail = api.get_task_set(src_ref.org, src_ref.name)
    new_name = name or src_ref.name
    request = _manifest_from_detail(detail, name=new_name)
    request["is_public"] = public

    try:
        result = api.create_task_set(profile.org_key, request)
    except ConflictError as exc:
        raise ValueError(
            f"a task set named '{new_name}' already exists in {profile.org_key} — "
            "pass a different name (e.g. `dn task-set clone "
            f"{src_ref.qualified_name} my-copy`)"
        ) from exc

    _print_warnings(result.get("warnings"))
    member_count = result.get("member_count", len(request["members"]))
    print_success(
        f"Cloned [cyan]{src_ref.qualified_name}[/cyan] to "
        f"[cyan]{profile.org_key}/{new_name}[/cyan] [dim]({member_count} members)[/dim]"
    )
    _hint(f"dn task-set info {profile.org_key}/{new_name}")


# ---------------------------------------------------------------------------
# publish / unpublish
# ---------------------------------------------------------------------------


@cli.command()
def publish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more task sets visible to other organizations.

    The set *listing* becomes public; member-task visibility is unchanged.
    Members that are not publicly runnable are surfaced as warnings (TSS-VIS-003).
    """
    api, profile = platform.connect()
    for raw in refs:
        set_ref = ArtifactRef.parse(raw, profile.org_key)
        result = api.update_task_set_visibility(set_ref.org, set_ref.name, is_public=True)
        _print_warnings(result.get("warnings"))
        print_success(f"Published {set_ref.org}/{set_ref.name}")


@cli.command()
def unpublish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more task sets private (org-only)."""
    api, profile = platform.connect()
    for raw in refs:
        set_ref = ArtifactRef.parse(raw, profile.org_key)
        api.update_task_set_visibility(set_ref.org, set_ref.name, is_public=False)
        print_success(f"Unpublished {set_ref.org}/{set_ref.name}")


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


@cli.command(alias="rm")
def delete(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Delete one or more task sets.

    Each set is hard-deleted (TSS-MUT-006). Past evaluations that referenced it
    keep running off their snapshots; a new evaluation against the deleted set
    fails with task_set_not_found.

    Args:
        refs: Task sets to delete (e.g. apex-web or acme/apex-web). Repeatable.
        yes: Skip the confirmation prompt.
    """
    api, profile = platform.connect()
    set_refs = [ArtifactRef.parse(raw, profile.org_key) for raw in refs]
    for set_ref in set_refs:
        if set_ref.version is not None:
            raise ValueError("task sets are not versioned — drop the '@version' suffix")
        # Confirm each exists before prompting.
        api.get_task_set(set_ref.org, set_ref.name)

    if len(set_refs) == 1:
        prompt = f"Delete {set_refs[0].qualified_name}?"
    else:
        listed = ", ".join(r.qualified_name for r in set_refs)
        prompt = f"Delete {len(set_refs)} task sets ({listed})?"
    if not confirm_destructive(prompt, yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    for set_ref in set_refs:
        api.delete_task_set(set_ref.org, set_ref.name)
        print_success(f"Deleted {set_ref.qualified_name}")
