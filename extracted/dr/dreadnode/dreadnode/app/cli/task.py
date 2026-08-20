"""Task subcommands for the cyclopts CLI."""

import json
import re
import shutil
import string
import subprocess
import sys
import tempfile
import typing as t
from importlib.resources import files
from pathlib import Path

import cyclopts

from dreadnode.app.cli.args import PlatformArgs
from dreadnode.app.cli.shared import (
    _FLAG_SEARCH,
    ArtifactRef,
    VersionedRef,
    _collect_pages,
    _hint,
    _print_json,
    _render_list,
    _sync_progress,
    _visibility_markup,
    classify_sync_operands,
    configured_dreadnode,
    confirm_destructive,
    connect_for_sync,
    console,
    copy_tree_replacing,
    ensure_name_only_refs,
    ensure_version,
    print_error,
    print_info,
    print_markdown,
    print_success,
    print_warning,
    pull_environment_to_dir,
    resolve_publish_flag,
)
from dreadnode.core.util import valid_version
from dreadnode.packaging.task_validation import NAME_PATTERN, ValidationIssue

cli = cyclopts.App(
    name="task",
    help="Environments with success conditions that agents operate in — for evaluations, training, and optimization.",
)


# ---------------------------------------------------------------------------
# Local helpers
# ---------------------------------------------------------------------------


def _summarize_task(p: dict[str, t.Any]) -> str:
    name = p.get("name", "unknown")
    visibility = "public" if p.get("is_public") else "private"
    difficulty = p.get("difficulty")
    source = p.get("source")
    description = p.get("description")
    parts = [f"[cyan]{name}[/cyan] {_visibility_markup(visibility)}"]
    meta = [m for m in (source, difficulty) if m]
    if meta:
        parts.append(f"[dim]{' · '.join(meta)}[/dim]")
    if description:
        parts.append(f"[dim]-[/dim] {description}")
    return "  ".join(parts)


_TASK_LIST_ROW_FIELDS: tuple[str, ...] = (
    "description",
    "is_public",
    "difficulty",
    "source",
    "tags",
    "author",
    "license",
    "sandbox_provider",
    "created_at",
)


def _write_file(path: Path, content: str) -> None:
    """Write a file, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _prepare_target_dir(task_dir: Path, *, force: bool) -> None:
    """Ensure ``task_dir`` can be freshly populated.

    If ``task_dir`` doesn't exist, returns immediately. Otherwise, ``force``
    determines whether and how to clear the existing target:

    - Without ``--force``: raise FileExistsError.
    - With ``--force`` on a regular file: unlink it.
    - With ``--force`` on a symlink (even to a directory): unlink the link only,
      never follow it — dereferencing could blow away state far outside the
      intended target.
    - With ``--force`` on a directory: rmtree it, after guarding against
      clobbering the current working directory or any ancestor of it.
    """
    if not task_dir.exists() and not task_dir.is_symlink():
        return

    if not force:
        raise FileExistsError(f"{task_dir} already exists — use --force to overwrite")

    if task_dir.is_symlink():
        task_dir.unlink()
        return

    if task_dir.is_file():
        task_dir.unlink()
        return

    if task_dir.is_dir():
        resolved = task_dir.resolve()
        cwd = Path.cwd().resolve()
        if resolved == cwd or resolved in cwd.parents:
            raise ValueError(
                f"refusing to --force overwrite {resolved}: would clobber the current working "
                "directory or an ancestor"
            )
        shutil.rmtree(task_dir)
        return

    raise ValueError(f"{task_dir} exists but is neither a file, directory, nor symlink")


# ---------------------------------------------------------------------------
# Starter templates for `init`
# ---------------------------------------------------------------------------
#
# Templates live in dreadnode/app/cli/templates/init/ and are loaded at runtime
# via importlib.resources. The two .yaml.tmpl files contain sentinel-marked
# blocks that the renderer activates/deactivates based on CLI flags. The
# supplemental scripts (verify.sh, provision.sh, teardown.sh, solution.sh) are
# static and copied verbatim.

_TEMPLATE_PKG = "dreadnode.app.cli.templates.init"

_FLAG_PATH_DEFAULT = "/tmp/result.txt"  # noqa: S108 — documented default path for security-task flag output
_FLAG_VALUE_DEFAULT = "FLAG{replace_me}"

_BLOCK_BEGIN_RE = re.compile(r"^# ===> begin (\S+)\s*$")
_BLOCK_END_RE = re.compile(r"^# ===> end (\S+)\s*$")


def _load_template(relative_path: str) -> str:
    """Read a template file from the bundled templates package."""
    return files(_TEMPLATE_PKG).joinpath(relative_path).read_text()


def _yaml_scalar(value: t.Any) -> str:
    """Format a Python value as a safely-quoted single-line YAML expression.

    Uses JSON encoding, which is a strict subset of YAML flow style. This
    handles quoting, escaping, and nested structures correctly for strings,
    integers, booleans, and lists, so any author-provided metadata value can
    be substituted into a task.yaml mapping without injection risk.
    """
    return json.dumps(value, ensure_ascii=False)


def _render_task_yaml(
    template_text: str,
    *,
    activate: set[str],
    deactivate: set[str],
    substitutions: dict[str, str],
) -> str:
    """Process a sentinel-block template into a final task.yaml.

    Each sentinel-marked block in the template is either left as-is, fully
    uncommented (activated), or fully commented (deactivated) based on the
    activate/deactivate sets. After block transforms, ``${var}`` placeholders
    are substituted using ``string.Template.safe_substitute`` so unknown vars
    survive intact.
    """
    overlap = activate & deactivate
    if overlap:
        raise ValueError(f"blocks both activated and deactivated: {sorted(overlap)}")

    out: list[str] = []
    current_key: str | None = None
    current_buffer: list[str] = []

    for line in template_text.splitlines():
        m_begin = _BLOCK_BEGIN_RE.match(line)
        m_end = _BLOCK_END_RE.match(line)

        if m_begin is not None:
            if current_key is not None:
                raise ValueError(
                    f"nested block: {m_begin.group(1)!r} opened inside {current_key!r}"
                )
            current_key = m_begin.group(1)
            current_buffer = []
            continue

        if m_end is not None:
            if current_key is None:
                raise ValueError(f"end sentinel without matching begin: {m_end.group(1)!r}")
            if m_end.group(1) != current_key:
                raise ValueError(
                    f"sentinel mismatch: end {m_end.group(1)!r} != begin {current_key!r}"
                )
            out.extend(_apply_block_state(current_buffer, current_key, activate, deactivate))
            current_key = None
            current_buffer = []
            continue

        if current_key is not None:
            current_buffer.append(line)
        else:
            out.append(line)

    if current_key is not None:
        raise ValueError(f"unclosed block: {current_key!r}")

    rendered = "\n".join(out)
    if not rendered.endswith("\n"):
        rendered += "\n"
    return string.Template(rendered).safe_substitute(substitutions)


def _apply_block_state(
    lines: list[str], key: str, activate: set[str], deactivate: set[str]
) -> list[str]:
    if key in activate:
        return [_uncomment_line(ln) for ln in lines]
    if key in deactivate:
        return [_comment_line(ln) for ln in lines]
    return lines


def _uncomment_line(line: str) -> str:
    """Strip a single leading comment marker from an inactive-form line."""
    if line.startswith("# "):
        return line[2:]
    if line.startswith("#"):
        return line[1:]
    return line


def _comment_line(line: str) -> str:
    """Prepend a comment marker to an active-form line."""
    if not line.strip():
        return line
    if line.lstrip().startswith("#"):
        return line  # already commented
    return "# " + line


# ---------------------------------------------------------------------------
# init — cyclopts groups + command
# ---------------------------------------------------------------------------

Difficulty = t.Literal["easy", "medium", "hard"]


def _init_verify_group_validator(argument_collection: t.Any) -> None:
    """Enforce: ``--with-verify`` is mutually exclusive with any ``--flag-*`` arg.

    ``--flag-value`` and ``--flag-path`` both describe the flag verification
    method and are compatible with each other. ``--with-verify`` switches to
    the script verification method and cannot coexist with either.
    """
    populated = argument_collection.filter_by(value_set=True)
    names = {a.name for a in populated}
    flag_names = names & {"--flag-value", "--flag-path"}
    if "--with-verify" in names and flag_names:
        labels = ", ".join(sorted(flag_names))
        raise ValueError(f"--with-verify is mutually exclusive with {labels}")


_INIT_SHAPE_GROUP = cyclopts.Group("Shape")
_INIT_FEATURES_GROUP = cyclopts.Group("Optional supplemental scripts")
_INIT_META_GROUP = cyclopts.Group("Catalog metadata")
_INIT_VERIFY_GROUP = cyclopts.Group(
    "Verification",
    validator=_init_verify_group_validator,
)


@cli.command(alias="new")
def init(
    name: str,
    *,
    # --- Shape -------------------------------------------------------------
    remote: t.Annotated[
        bool,
        cyclopts.Parameter(
            group=_INIT_SHAPE_GROUP,
            negative=(),
            help="Scaffold a remote/external task — no docker-compose, no Dockerfile.",
        ),
    ] = False,
    force: t.Annotated[
        bool,
        cyclopts.Parameter(
            group=_INIT_SHAPE_GROUP,
            negative=(),
            help="Overwrite an existing directory at the target path.",
        ),
    ] = False,
    path: t.Annotated[
        Path,
        cyclopts.Parameter(
            group=_INIT_SHAPE_GROUP,
            help="Parent directory to create the task folder in.",
        ),
    ] = Path(),
    # --- Optional supplemental scripts ------------------------------------
    with_verify: t.Annotated[
        bool,
        cyclopts.Parameter(
            group=(_INIT_FEATURES_GROUP, _INIT_VERIFY_GROUP),
            negative=(),
            help="Drop a verify.sh stub and switch verification.method to script.",
        ),
    ] = False,
    with_solution: t.Annotated[
        bool,
        cyclopts.Parameter(
            group=_INIT_FEATURES_GROUP,
            negative=(),
            help="Drop a solution.sh stub and uncomment the solution: block.",
        ),
    ] = False,
    # --- Catalog metadata pre-fills ---------------------------------------
    version: t.Annotated[
        str,
        cyclopts.Parameter(
            name="--initial-version",
            group=_INIT_META_GROUP,
            help="Initial semver version for the task.",
        ),
    ] = "0.1.0",
    description: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=_INIT_META_GROUP,
            help="One-line catalog summary.",
        ),
    ] = None,
    difficulty: t.Annotated[
        Difficulty | None,
        cyclopts.Parameter(
            group=_INIT_META_GROUP,
            help="Difficulty level (easy, medium, or hard).",
        ),
    ] = None,
    tag: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            group=_INIT_META_GROUP,
            negative_iterable=(),
            help="Discovery tag (repeatable).",
        ),
    ] = None,
    source: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=_INIT_META_GROUP,
            help="Suite or group the task belongs to (e.g. apex, portswigger).",
        ),
    ] = None,
    author: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=_INIT_META_GROUP,
            help="Task author (free-form string).",
        ),
    ] = None,
    license: t.Annotated[
        str | None,
        cyclopts.Parameter(
            name="--license",
            group=_INIT_META_GROUP,
            help="SPDX license identifier (e.g. MIT, Apache-2.0).",
        ),
    ] = None,
    repository: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=_INIT_META_GROUP,
            help="Source repository URL.",
        ),
    ] = None,
    max_agent_timeout_sec: t.Annotated[
        int | None,
        cyclopts.Parameter(
            group=_INIT_META_GROUP,
            validator=cyclopts.validators.Number(gt=0),
            help="Evaluation timeout hint in seconds (advisory).",
        ),
    ] = None,
    # --- Verification pre-fills -------------------------------------------
    flag_value: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=_INIT_VERIFY_GROUP,
            help="Plaintext value for verification.value (default flag method only).",
        ),
    ] = None,
    flag_path: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=_INIT_VERIFY_GROUP,
            help="Path the agent writes for the flag (default /tmp/result.txt).",
        ),
    ] = None,
) -> None:
    """Scaffold a new task directory ready for development.

    The scaffolded ``task.yaml`` doubles as an entrypoint to the task contract:
    every spec feature appears as a commented opt-in block with a one-line
    hint. Pass ``--with-verify`` / ``--with-solution`` to scaffold the matching
    script stub *and* uncomment the matching block. Pass any catalog metadata
    flag (``--description``, ``--difficulty``, ``--tag``, etc.) to pre-fill
    that field.

    The result passes structural validation immediately. ``dn task validate``
    may still emit best-practice warnings until you fill in catalog metadata
    and add a reference solution.

    Examples:

        # Default scaffold (compose + flag verification)
        dn task init my-task

        # Remote task with script-based verification
        dn task init my-task --remote --with-verify --with-solution

        # Fully-stamped one-shot for an automation pipeline
        dn task init my-task \
          --description "SQLi against a vintage forum" --difficulty medium \
          --tag web --tag sqli --source apex --author "Alice <alice@dn>" \
          --license MIT --initial-version 0.2.0 \
          --flag-value "FLAG{tiger_alt_pwn3d}" --with-solution
    """
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError(
            f'Invalid task name "{name}" — must be kebab-case [a-z0-9][a-z0-9-]* '
            "(lowercase letters, digits, and hyphens; must start with alphanumeric)"
        )
    if not valid_version(version):
        raise ValueError(
            f'Invalid --initial-version "{version}" — must be semver (e.g. 0.1.0, 1.0.0-beta.1)'
        )

    effective_flag_path = flag_path or _FLAG_PATH_DEFAULT
    effective_flag_value = flag_value or _FLAG_VALUE_DEFAULT
    # flag_path appears verbatim in the instruction literal block, so reject
    # control characters that would break YAML block scalar indentation.
    if any(ch in effective_flag_path for ch in "\r\n\t"):
        raise ValueError("--flag-path must not contain newlines or tabs")

    task_dir = path.resolve() / name
    _prepare_target_dir(task_dir, force=force)

    # --- Build activation set + substitution map -------------------------
    activate: set[str] = set()
    deactivate: set[str] = set()

    if with_verify:
        activate.add("verification.script")
        deactivate.add("verification.flag")
    if with_solution:
        activate.add("solution")

    if description is not None:
        activate.add("metadata.description")
    if difficulty is not None:
        activate.add("metadata.difficulty")
    if tag:
        activate.add("metadata.tags")
    if source is not None:
        activate.add("metadata.source")
    if author is not None:
        activate.add("metadata.author")
    if license is not None:
        activate.add("metadata.license")
    if repository is not None:
        activate.add("metadata.repository")
    if max_agent_timeout_sec is not None:
        activate.add("metadata.max_agent_timeout_sec")

    # Regex/type-safe fields are emitted as raw YAML scalars; free-text fields
    # go through _yaml_scalar (JSON encoding) to guarantee they produce valid
    # YAML regardless of what metacharacters the author passes.
    substitutions: dict[str, str] = {
        "name": name,
        "version": version,
        "difficulty": difficulty if difficulty is not None else "easy",
        "max_agent_timeout_sec": (
            str(max_agent_timeout_sec) if max_agent_timeout_sec is not None else "600"
        ),
        # flag_path has two forms: the mapping form is JSON-escaped for YAML
        # safety, the display form is the raw path for the instruction literal
        # block where the user actually wants to see it unquoted.
        "flag_path": _yaml_scalar(effective_flag_path),
        "flag_path_display": effective_flag_path,
        "flag_value": _yaml_scalar(effective_flag_value),
        # Catalog metadata: real value when provided, realistic example otherwise.
        "description": _yaml_scalar(
            description if description is not None else "Short summary for the catalog"
        ),
        "tags": _yaml_scalar(tag or ["crypto", "web"]),
        "source": _yaml_scalar(source if source is not None else "my-suite"),
        "author": _yaml_scalar(author if author is not None else "Your Name <you@example.com>"),
        "license": _yaml_scalar(license if license is not None else "MIT"),
        "repository": _yaml_scalar(
            repository if repository is not None else "https://github.com/..."
        ),
    }

    # --- Render task.yaml -------------------------------------------------
    template_name = "task-remote.yaml.tmpl" if remote else "task.yaml.tmpl"
    task_yaml_text = _render_task_yaml(
        _load_template(template_name),
        activate=activate,
        deactivate=deactivate,
        substitutions=substitutions,
    )
    _write_file(task_dir / "task.yaml", task_yaml_text)
    print_success(f"{name}/task.yaml")

    # --- Compose + Dockerfile (default shape only) -----------------------
    if not remote:
        _write_file(task_dir / "docker-compose.yaml", _load_template("docker-compose.yaml"))
        print_success(f"{name}/docker-compose.yaml")

        _write_file(
            task_dir / "challenge" / "Dockerfile",
            _load_template("challenge/Dockerfile"),
        )
        print_success(f"{name}/challenge/Dockerfile")

    # --- Optional supplemental scripts -----------------------------------
    if with_verify:
        _write_file(task_dir / "verify.sh", _load_template("verify.sh"))
        print_success(f"{name}/verify.sh")
    if with_solution:
        _write_file(task_dir / "solution.sh", _load_template("solution.sh"))
        print_success(f"{name}/solution.sh")

    # --- Next steps -------------------------------------------------------
    next_steps = [
        f"Edit {name}/task.yaml — set the instruction and verification details.",
        f"Run `dn task validate {name}` to check your work.",
    ]
    if with_verify and with_solution:
        next_steps.append(f"Run `dn task validate --smoke {name}` once verify.sh is implemented.")

    console.print()
    console.print("[bold]Next steps[/bold]")
    for i, step in enumerate(next_steps, start=1):
        console.print(f"  {i}. {step}")


# ---------------------------------------------------------------------------
# push
# ---------------------------------------------------------------------------


@cli.command(alias="upload")
def push(
    path: Path,
    *,
    name: str | None = None,
    skip_upload: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    publish: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    skip_validate: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    public_compat: t.Annotated[
        bool,
        cyclopts.Parameter(name="--public", negative=(), show=False),
    ] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Publish a task to your organization's registry.

    Builds an OCI image from the task directory and pushes it.
    Skips the upload if the remote content already matches (idempotent).
    Pass --publish to make the task discoverable by other organizations.

    Args:
        path: Task directory containing task.yaml and docker-compose.yaml.
        name: Override the registry name.
        skip_upload: Build and validate locally without publishing.
        force: Push even if the remote content already matches.
        publish: Ensure the task is publicly discoverable after publishing.
        skip_validate: Skip local validation (push even if the platform would
            reject it at ingest). Not recommended.
    """
    publish = resolve_publish_flag(publish, public_compat)
    dn = configured_dreadnode(platform)
    result = dn.push_environment(
        path,
        name=name,
        skip_upload=skip_upload,
        force=force,
        publish=publish,
        validate=not skip_validate,
    )
    if not result.success:
        raise RuntimeError("; ".join(result.errors) or "Task push failed")

    if result.package_name is None or result.package_version is None:
        raise RuntimeError("Task push returned incomplete metadata")

    ref = f"[cyan]{result.package_name}[/cyan]@[dim]{result.package_version or '1.0.0'}[/dim]"
    if skip_upload or not dn.can_sync:
        console.print(f"Built {ref}")
        return
    if result.blobs_uploaded == 0 and result.blobs_skipped > 0:
        console.print(f"{ref} already up to date")
        return
    digest = result.manifest_digest or "unknown"
    console.print(f"Pushed {ref} [dim]({digest})[/dim]")


@cli.command()
def publish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more task families visible to other organizations."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_task_visibility(ref.org, ref.name, is_public=True)
        print_success(f"Published {ref.qualified_name}")


@cli.command()
def unpublish(
    refs: t.Annotated[list[str], cyclopts.Parameter(negative_iterable=())],
    *,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Make one or more task families private."""
    dn = configured_dreadnode(platform)
    parsed_refs = ensure_name_only_refs(refs, dn.profile.org_key)
    for ref in parsed_refs:
        dn.set_task_visibility(ref.org, ref.name, is_public=False)
        print_success(f"Unpublished {ref.qualified_name}")


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    search: t.Annotated[str | None, cyclopts.Parameter(name=_FLAG_SEARCH)] = None,
    limit: int = 50,
    include_public: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show tasks in your organization.

    Args:
        search: Search by name or description.
        limit: Maximum results to show.
        include_public: Include public tasks from other organizations.
        as_json: Output raw JSON instead of a summary.
    """
    api, profile = platform.connect()
    items = _collect_pages(
        lambda page, page_size: api.list_tasks(
            profile.org_key,
            search=search,
            page=page,
            limit=page_size,
            include_public=include_public,
        ),
        limit=limit,
        page_size=100,
        items_key="tasks",
    )
    _render_list(
        items,
        as_json=as_json,
        summary=_summarize_task,
        empty_msg="No tasks found",
        fields=_TASK_LIST_ROW_FIELDS,
    )
    if not as_json and items:
        example = items[0].get("name", "<name>")
        _hint(f"dn task info {example}")


# ---------------------------------------------------------------------------
# info
# ---------------------------------------------------------------------------


@cli.command()
def info(
    ref: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    readme: t.Annotated[bool, cyclopts.Parameter(name="--readme", alias="-R", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Show details and instructions for a task.

    Displays metadata, visibility, difficulty, tags, and the full
    task instruction. Version is optional — defaults to the latest.

    Args:
        ref: Task to inspect (e.g. my-task, my-task@1.0.0).
        as_json: Output raw JSON instead of formatted summary.
        readme: Render the bundled README (markdown) instead of
            the summary metadata.
    """
    api, profile = platform.connect()
    vref = ensure_version(api, "task", ArtifactRef.parse(ref, profile.org_key))

    if readme:
        from dreadnode.app.api.client import NotFoundError

        try:
            payload = api.get_task_readme(vref.org, vref.name)
        except NotFoundError:
            print_warning(f"No README found in {vref.qualified_name}")
            return
        content = str(payload.get("content") or "")
        if not content.strip():
            print_warning(f"README in {vref.qualified_name} is empty")
            return
        print_markdown(content)
        return

    task = api.get_task(vref.org, vref.name, vref.version)

    if as_json:
        _print_json(task)
        return

    console.print(_summarize_task(task))

    tags = task.get("tags")
    if tags and isinstance(tags, list):
        console.print(f"  [dim]tags:[/dim] {', '.join(str(tag) for tag in tags)}")

    instruction = task.get("instruction")
    if instruction:
        console.print()
        console.print("[bold]Instruction[/bold]")
        console.print(f"[dim]{'─' * 40}[/dim]")
        console.print(instruction.strip())
    _hint(f"dn task pull {vref.qualified_name}")
    _hint(f"dn task info {vref.qualified_name} --readme")


# ---------------------------------------------------------------------------
# pull
# ---------------------------------------------------------------------------


@cli.command(alias="download")
def pull(
    ref: str,
    *,
    output: t.Annotated[Path | None, cyclopts.Parameter(name="--output", alias="-o")] = None,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    upgrade: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Download a task for local development or inspection.

    Pulls the task from the registry into the local package cache. Use
    this to inspect how a task is built, fork it, or test it locally
    with docker compose. Pass ``--output`` to also materialize it to a
    directory you choose — useful for carrying an environment onto an
    air-gapped instance and pushing it there.

    Args:
        ref: Task to pull (e.g. my-task or acme/my-task).
        output: Also copy the task to this directory. Defaults to the
            package cache only. Implies --upgrade, so the copy you carry
            out is always a complete fresh extraction rather than whatever
            the cache happens to hold.
        force: Overwrite the output directory if it already exists.
        upgrade: Re-download even if already cached locally.
    """
    dn = configured_dreadnode(platform)
    _api, profile = platform.connect()
    parsed = ArtifactRef.parse(ref, profile.org_key)

    package_ref = f"environment://{parsed.qualified_name}"

    # Fail on an existing destination before downloading anything (CLI-SYNC-033),
    # not after a full pull.
    dest = output.resolve() if output is not None else None
    if dest is not None and (dest.exists() or dest.is_symlink()) and not force:
        raise FileExistsError(f"{dest} already exists — use --force to overwrite")

    # When materializing to a chosen directory we need a fresh extraction: the
    # cache-skip path doesn't report a dest, and a carried-out copy should be
    # complete regardless of what's already cached.
    result = dn.pull_package([package_ref], upgrade=upgrade or output is not None)

    if not result.success:
        raise RuntimeError("; ".join(result.errors) or "Pull failed")

    display = parsed.with_version(result.version).format() if result.version else parsed.format()

    if dest is not None:
        if result.dest is None:
            raise RuntimeError("Pull succeeded but no cached files were found to copy")
        copy_tree_replacing(result.dest, dest)
        print_success(f"Pulled {display} to {dest}")
        return

    if result.dest:
        console.print(f"Pulled {display} to {result.dest}")
    else:
        console.print(f"Pulled {display}")


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


@cli.command(alias="rm")
def delete(
    ref: str,
    *,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Remove a published task version from the registry.

    Args:
        ref: Task to delete (e.g. my-task@1.0.0). Version is required.
        yes: Skip the confirmation prompt.
    """
    api, profile = platform.connect()
    vref = ArtifactRef.parse_versioned(ref, profile.org_key)

    # Verify it exists before prompting
    api.get_task(vref.org, vref.name, vref.version)

    if not confirm_destructive(f"Delete {vref.format()}?", yes=yes):
        console.print("[dim]Cancelled[/dim]")
        return

    api.delete_task(vref.org, vref.name, vref.version)
    print_success(f"Deleted {vref.format()}")


# ---------------------------------------------------------------------------
# sync
# ---------------------------------------------------------------------------


def _pull_environments_to_dir(
    dn: t.Any,
    api: t.Any,
    org: str,
    directory: Path,
    *,
    force: bool,
    on_progress: t.Callable[[str, str, str | None], None],
) -> tuple[list[str], list[str], list[tuple[str, str]]]:
    """Pull every task environment in *org* to ``directory/<name>``.

    Returns (pulled, skipped, failed). Additive copy semantics: a name whose
    destination already exists is skipped unless *force*.
    """
    directory.mkdir(parents=True, exist_ok=True)

    items = _collect_pages(
        lambda page, page_size: api.list_tasks(org, page=page, limit=page_size),
        limit=10_000,
        page_size=100,
        items_key="tasks",
    )

    pulled: list[str] = []
    skipped: list[str] = []
    failed: list[tuple[str, str]] = []

    for item in items:
        name = item.get("name")
        if not name:
            continue
        dest = (directory / name).resolve()
        # Skip already-present environments from the path alone — no
        # version-resolution API call for a name we won't pull (CLI-SYNC-035).
        if (dest.exists() or dest.is_symlink()) and not force:
            skipped.append(name)
            on_progress(name, "skipped", None)
            continue
        try:
            vref = ensure_version(api, "task", ArtifactRef.parse(name, org))
        except ValueError as e:
            # No published version — nothing to pull; not a failure (CLI-SYNC-036).
            skipped.append(name)
            on_progress(name, "skipped", str(e))
            continue
        try:
            # Address the resolved version, not the registry `latest` tag, so the
            # bytes on disk match the version we report (CLI-SYNC-034).
            pull_environment_to_dir(
                dn, f"environment://{vref.qualified_name}:{vref.version}", dest, force=force
            )
            pulled.append(name)
            on_progress(name, "pulled", vref.version)
        except Exception as e:
            failed.append((name, str(e)))
            on_progress(name, "failed", str(e))

    return pulled, skipped, failed


_DEFAULT_SYNC_WORKERS = 8


@cli.command()
def sync(
    src: str,
    dst: str | None = None,
    *,
    force: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    publish: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    public_compat: t.Annotated[
        bool,
        cyclopts.Parameter(name="--public", negative=(), show=False),
    ] = False,
    workers: int = _DEFAULT_SYNC_WORKERS,
    skip_validate: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Bulk-copy task environments between a local directory and a platform.

    One operand is a platform URL, the other a local directory; the direction
    follows from which is which:

    - ``sync <dir> <url>`` — publish every task under the directory, pushing
      only those whose content changed (ideal for CI). ``sync <dir>`` alone
      pushes to the platform your connection flags point at.
    - ``sync <url> <dir>`` — pull every task in your organization down into the
      directory (one subfolder per task), for carrying onto an air-gapped
      instance.

    The platform URL resolves to a profile you have logged in to; if none
    matches, the command tells you to ``dn login --server <url>`` first.

    Args:
        src: A platform URL to pull from, or a directory to push from.
        dst: A directory to pull into, or a platform URL to push to. Omit to
            push ``src`` to the connection-flag platform (back-compat form).
        force: Copy every task even if unchanged / already present.
        publish: Ensure published tasks are publicly discoverable (push only).
        workers: Number of parallel upload workers (push only).
        skip_validate: Skip local validation on push (upload even tasks the
            platform would reject at ingest). Not recommended.
    """
    publish = resolve_publish_flag(publish, public_compat)
    plan = classify_sync_operands(src, dst)
    api, dn, profile = connect_for_sync(plan, platform)

    if plan.direction == "pull":
        if publish:
            print_warning("--publish is ignored when pulling")
        if skip_validate or workers != _DEFAULT_SYNC_WORKERS:
            print_warning("--workers and --skip-validate only apply to push; ignoring")
        pulled, skipped, failed = _pull_environments_to_dir(
            dn,
            api,
            profile.org_key,
            plan.directory,
            force=force,
            on_progress=_sync_progress,
        )
        total = len(pulled) + len(skipped) + len(failed)
        console.print(
            f"\nPulled {total}: "
            f"[green]{len(pulled)} pulled[/green], "
            f"[dim]{len(skipped)} skipped[/dim], "
            f"[red]{len(failed)} failed[/red]"
        )
        if failed:
            raise SystemExit(1)
        return

    result = dn.sync_environments(
        plan.directory,
        force=force,
        publish=publish,
        max_workers=workers,
        validate=not skip_validate,
        on_progress=_sync_progress,
        on_status=lambda msg: console.print(msg),
    )

    total = len(result.uploaded) + len(result.skipped) + len(result.failed)
    console.print(
        f"\nSynced {total}: "
        f"[green]{len(result.uploaded)} uploaded[/green], "
        f"[dim]{len(result.skipped)} skipped[/dim], "
        f"[red]{len(result.failed)} failed[/red]"
    )
    if not result.ok:
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


@cli.command(alias="check")
def validate(
    path: str,
    *,
    strict: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    build: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    smoke: t.Annotated[bool, cyclopts.Parameter(negative=())] = False,
    pull: t.Annotated[bool, cyclopts.Parameter(name="--pull", negative=())] = False,
    yes: t.Annotated[bool, cyclopts.Parameter(name="--yes", alias="-y", negative=())] = False,
    env: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--env",
            alias="-e",
            help=(
                "Inject env into the challenge service at smoke time only "
                "(KEY=VALUE for a literal, or bare KEY to forward the value from "
                "your shell so secrets stay out of argv; repeatable). Scoped to "
                "the challenge/task service -- does not reach solution.sh or verify."
            ),
            negative_iterable=(),
        ),
    ] = None,
    timeout: int | None = None,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Check that task definitions are well-formed before publishing.

    Validates task.yaml, docker-compose.yaml, port mappings, and
    script references. Discovers and validates all tasks when given a
    parent directory. When a path does not exist locally but resolves to
    a published task, validation can pull the remote task into a temporary
    local directory and run the same validation flow.

    Args:
        path: Task directory, parent directory containing multiple tasks,
            or published task ref when using remote validation.
        strict: Treat warnings as failures (exit code 1).
        build: Also run docker compose build for each task.
        smoke: Full lifecycle test -- boot containers, verify that verify.sh
            rejects unsolved state, and (if solution.sh exists) verify it
            accepts the reference solution. Implies --build. Judge-backed
            methods (``script_and_judge``, ``flag_and_judge``) run their
            mechanical half here; the judge is not invoked offline.
            ``outcome_judge`` has no mechanical half and is skipped.
        pull: Treat path as a published task ref and pull it for local validation.
        yes: Accept remote validation without prompting when path is not local.
        env: Env to inject into the challenge service for the smoke run only
            (``-e``/``--env``, repeatable). ``KEY=VALUE`` sets a literal; a bare
            ``KEY`` forwards the value from ``os.environ`` so secrets never touch
            argv. Merged into the ephemeral compose -- the on-disk compose is
            untouched -- and overrides any same-named key the compose declares.
            Targets the challenge/task service(s) only: it does NOT reach
            solution.sh or verify, which run in a separate sandbox. Only
            meaningful with ``--smoke``; ignored (with a warning) otherwise.
        timeout: Per-task wall-clock budget in seconds for smoke testing.
            When unset, falls back to the task's ``max_agent_timeout_sec`` or
            120 seconds if neither is declared.
    """
    if smoke:
        build = True

    if env and not smoke:
        print_warning("--env / -e only applies to --smoke; ignoring", indent=2)
        env = None

    resolved = Path(path).resolve()
    if resolved.exists():
        _validate_local_task_path(
            resolved,
            strict=strict,
            build=build,
            smoke=smoke,
            timeout=timeout,
            service_env=env,
        )
        return

    explicit_remote = pull or yes
    ref = _resolve_remote_task_ref(path, platform, required=explicit_remote)
    if ref is None:
        raise FileNotFoundError(f"Path not found: {resolved}")

    if not explicit_remote and not _confirm_remote_task_validation(ref, smoke=smoke):
        console.print("[dim]Cancelled[/dim]")
        return

    _validate_remote_task_ref(
        ref,
        platform=platform,
        strict=strict,
        build=build,
        smoke=smoke,
        timeout=timeout,
        service_env=env,
    )


def _validate_local_task_path(
    resolved: Path,
    *,
    strict: bool,
    build: bool,
    smoke: bool,
    timeout: int | None,
    service_env: list[str] | None = None,
) -> None:
    """Run validation against a local task directory or task tree."""
    from dreadnode.packaging.task_validation import (
        ValidationIssue,
        discover_task_directories,
        validate_task_directory,
    )

    if (resolved / "task.yaml").is_file():
        dirs = [resolved]
        conflicts: list[tuple[Path, Path]] = []
    else:
        dirs, conflicts = discover_task_directories(resolved)
        if not dirs:
            raise FileNotFoundError(f"No task.yaml found in {resolved} or its subdirectories")

    errors: list[tuple[str, str]] = []
    warnings: list[str] = []

    for parent, nested in conflicts:
        rel_parent = parent.relative_to(resolved) if parent != resolved else Path(parent.name)
        rel_nested = nested.relative_to(resolved) if nested != resolved else Path(nested.name)
        errors.append((str(rel_nested), f"task nested inside another task ({rel_parent})"))
        print_error(f"{rel_nested}", indent=2)
        console.print(f"       layout: task nested inside another task ({rel_parent})")

    for task_dir in dirs:
        dir_name = task_dir.name
        try:
            issues = validate_task_directory(task_dir, root_dir=resolved)
            errs = [i for i in issues if i.level == "error"]
            warns = [i for i in issues if i.level == "warning"]
            infos = [i for i in issues if i.level == "info"]

            if build and not errs and _find_compose_file(task_dir) is not None:
                result = subprocess.run(
                    ["docker", "compose", "build"],  # noqa: S607
                    cwd=task_dir,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    stderr_lines = [ln for ln in result.stderr.strip().splitlines() if ln.strip()]
                    summary = stderr_lines[-1] if stderr_lines else "build failed"
                    errs.append(ValidationIssue("error", "docker-build", summary))

            if smoke and not errs:
                smoke_issues = _run_smoke_test(task_dir, timeout=timeout, service_env=service_env)
                for issue in smoke_issues:
                    if issue.level == "error":
                        errs.append(issue)
                    else:
                        warns.append(issue)

            tally = _format_tally(len(errs), len(warns), len(infos))
            header = f"{dir_name}{tally}"
            if errs:
                errors.append((dir_name, "; ".join(i.message for i in errs)))
                print_error(header, indent=2)
            elif warns:
                warnings.append(dir_name)
                print_warning(header, indent=2)
            else:
                print_success(header, indent=2)

            # Group by severity so the reader sees blockers first, then things
            # to improve, then trivia. Each section has its own visual tier.
            _render_issue_section("error", list(errs))
            _render_issue_section("warning", list(warns))
            _render_issue_section("info", list(infos))
            if errs or warns or infos:
                console.print()

            if errs and smoke:
                break
        except Exception as exc:
            errors.append((dir_name, str(exc)))
            print_error(f"{dir_name}: {exc}", indent=2)
            if smoke:
                break

    total = len(dirs)
    failed = len(errors)
    warned = len(warnings)
    ok_count = total - failed - warned
    console.print(
        f"\nValidated {total}: "
        f"[green]{ok_count} ok[/green], [yellow]{warned} warn[/yellow], [red]{failed} failed[/red]"
    )
    if errors or (strict and warnings):
        raise SystemExit(1)


def _resolve_remote_task_ref(
    raw_ref: str,
    platform: PlatformArgs,
    *,
    required: bool,
) -> VersionedRef | None:
    try:
        api, profile = platform.connect()
        return ensure_version(api, "task", ArtifactRef.parse(raw_ref, profile.org_key))
    except Exception:
        if required:
            raise
        return None


def _confirm_remote_task_validation(ref: VersionedRef, *, smoke: bool) -> bool:
    from rich.prompt import Confirm

    if not sys.stdin.isatty():
        raise RuntimeError(
            f"Remote task {ref.qualified_name}@{ref.version} exists, but stdin is not "
            "interactive. Re-run with --pull to validate the pulled task, or --yes to accept "
            "the remote validation prompt."
        )

    warning = ""
    if smoke:
        warning = (
            " Smoke validation may build containers and run scripts from the remote task package."
        )
    return Confirm.ask(
        f"Remote task {ref.format()} exists. Pull it to be validated locally?{warning}",
        default=False,
    )


def _validate_remote_task_ref(
    ref: VersionedRef,
    *,
    platform: PlatformArgs,
    strict: bool,
    build: bool,
    smoke: bool,
    timeout: int | None = None,
    service_env: list[str] | None = None,
) -> None:
    dn = configured_dreadnode(platform)
    print_info(f"Pulling {ref.qualified_name}@{ref.version} for local validation")

    package_ref = f"environment://{ref.qualified_name}:{ref.version}"
    pull_result = dn.pull_package([package_ref], upgrade=False)
    if not pull_result.success or pull_result.dest is None:
        joined = "; ".join(pull_result.errors) or "pull failed"
        raise RuntimeError(f"{ref.qualified_name}@{ref.version}: {joined}")

    with tempfile.TemporaryDirectory(prefix=f"dreadnode-task-validate-{ref.name}-") as tmp:
        validation_dir = Path(tmp) / ref.name
        shutil.copytree(pull_result.dest, validation_dir)
        _validate_local_task_path(
            validation_dir,
            strict=strict,
            build=build,
            smoke=smoke,
            timeout=timeout,
            service_env=service_env,
        )


# ---------------------------------------------------------------------------
# smoke test helpers
# ---------------------------------------------------------------------------
#
# v1 smoke test contract:
#
# - Verification scripts use exit codes (TSK-VER-011), not the legacy
#   /logs/verifier/reward.txt file.
# - Tasks do NOT include a `client` container (TSK-ENV-004). Instead, the
#   smoke runner stands up a single long-lived "agent sandbox" container per
#   run to stand in for production's agent sandbox:
#     * solution.sh always runs inside the sandbox container (it's the
#       agent's proxy — the agent is always sandboxed in production).
#     * verify.sh runs per `verification.where`:
#         - `where: environment` (default) — on the host, with the task
#           directory as cwd. Used to check server-side state (curl/docker
#           against compose services via published localhost ports).
#         - `where: agent` — exec'd into the sandbox container so it shares
#           the agent's filesystem (and the result file it wrote).
# - Compose, when present, comes up alongside; the sandbox attaches to its
#   network and sees compose DNS names. Composeless tasks skip the compose
#   phase but still run solution in the sandbox — the agent runtime is a
#   real constraint regardless.
# - provision.sh and teardown.sh always run on the host (they represent the
#   platform-side verifier infra, not the agent).
# - Only `verification.method` of `script` or `flag` is smoke-tested. Other
#   methods (`outcome_judge`, `trajectory`) emit a "skipping" warning.


_ISSUE_INDENT = " " * 5  # aligns under the ✗/✓/! task-row glyph


def _format_tally(errs: int, warns: int, infos: int) -> str:
    """Return a dim suffix like ``  2 errors, 4 warnings, 6 info`` — empty if all zero.

    Only non-zero buckets show up so clean tasks stay quiet.
    """
    parts: list[str] = []
    if errs:
        parts.append(f"[red]{errs} error{'s' if errs != 1 else ''}[/red]")
    if warns:
        parts.append(f"[yellow]{warns} warning{'s' if warns != 1 else ''}[/yellow]")
    if infos:
        parts.append(f"[dim]{infos} info[/dim]")
    if not parts:
        return ""
    return "  [dim]·[/dim] " + " [dim]·[/dim] ".join(parts)


_LEVEL_STYLE: dict[str, tuple[str, str]] = {
    # level -> (rich style, line glyph)
    "error": ("red", "✗"),
    "warning": ("yellow", "!"),
    "info": ("dim", "·"),
}
_SECTION_LABEL: dict[str, str] = {
    "error": "errors",
    "warning": "warnings",
    "info": "info",
}


def _render_issue_section(level: str, items: list["ValidationIssue | str"]) -> None:
    """Render a severity-grouped block of issues with column-aligned components.

    Layout per line:

        <indent> <glyph> <component padded to col_width>  <message>

    Long messages are soft-wrapped with a hanging indent that lines up under
    the message column, so the reader never loses the visual gutter. Multi-
    line messages (e.g. schema errors with embedded YAML examples) keep their
    own indentation past the first line.
    """
    import textwrap as _tw

    if not items:
        return
    style, glyph = _LEVEL_STYLE[level]
    label = _SECTION_LABEL[level]

    # Build (component, message) pairs up front so we can compute column width.
    rows: list[tuple[str, str]] = []
    for item in items:
        if isinstance(item, str):
            rows.append(("", item))
        else:
            rows.append((item.component or "", item.message))

    col_width = max((len(comp) for comp, _ in rows), default=0)
    # "indent(5) + glyph(1) + space(1) + comp + 2-space gutter + message"
    prefix_width = len(_ISSUE_INDENT) + 2 + col_width + 2
    avail = max(20, console.width - prefix_width)
    cont_indent = " " * prefix_width

    console.print(f"{_ISSUE_INDENT}[dim]{label}[/dim]")
    for comp, message in rows:
        raw_lines = message.splitlines() or [""]
        first = raw_lines[0]
        wrapped = _tw.wrap(first, width=avail) or [""]
        comp_col = f"{comp:<{col_width}}" if col_width else ""
        console.print(f"{_ISSUE_INDENT}[{style}]{glyph}[/] [{style}]{comp_col}[/]  {wrapped[0]}")
        for extra in wrapped[1:]:
            console.print(f"{cont_indent}{extra}")
        for raw in raw_lines[1:]:
            console.print(f"{cont_indent}{raw}")


def _find_compose_file(task_dir: Path) -> Path | None:
    """Return the compose file in ``task_dir``, or None if no compose is declared.

    Docker compose accepts both ``.yaml`` and ``.yml``; accepting both here keeps
    the validate gate, build gate, and smoke helper in lockstep.
    """
    for name in ("docker-compose.yaml", "docker-compose.yml"):
        candidate = task_dir / name
        if candidate.is_file():
            return candidate
    return None


def _compose_run(
    args: list[str],
    *,
    cwd: Path,
    timeout_sec: float | None = None,
    compose_file: Path | None = None,
    project_name: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a docker compose command, returning the completed process.

    ``compose_file`` and ``project_name`` let smoke drive a rewritten
    compose file under a unique project name so parallel smoke runs can't
    collide on host ports or compose state. When ``compose_file`` is set,
    ``--project-directory`` is pinned to ``cwd`` so relative build contexts
    in the rewritten file still resolve against the task directory rather
    than wherever the rewritten copy lives.
    """
    prefix: list[str] = ["docker", "compose"]
    if compose_file is not None:
        prefix += ["-f", str(compose_file), "--project-directory", str(cwd)]
    if project_name is not None:
        prefix += ["-p", project_name]
    return subprocess.run(  # noqa: S603
        [*prefix, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout_sec,
    )


def _script_env(extra: dict[str, str] | None) -> dict[str, str] | None:
    """Merge *extra* into ``os.environ`` for subprocess execution, or None if empty."""
    import os

    if not extra:
        return None
    merged = dict(os.environ)
    merged.update(extra)
    return merged


def _stream_subprocess(
    cmd: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None,
    timeout_sec: float,
    label: str,
) -> subprocess.CompletedProcess[str]:
    """Run a subprocess and forward output to the console line by line.

    Each line is prefixed with a dim ``│ <label> │`` gutter so it's visually
    distinct from the smoke runner's own messages. stderr is merged into
    stdout so ordering matches what the script itself produces. A
    ``CompletedProcess`` with the full captured text is still returned so
    error-reporting can include a tail of the output.
    """
    import select
    import time

    proc = subprocess.Popen(  # noqa: S603
        cmd,
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    lines: list[str] = []
    deadline = time.monotonic() + max(timeout_sec, 1)

    def _emit(raw: str) -> None:
        # markup=False so stray [ in script output don't get parsed; style
        # applies to the whole line without needing markup.
        console.print(
            f"       │ {label} │ {raw.rstrip()}",
            markup=False,
            highlight=False,
            style="dim",
        )
        lines.append(raw if raw.endswith("\n") else raw + "\n")

    import contextlib

    try:
        while True:
            if time.monotonic() > deadline:
                proc.kill()
                with contextlib.suppress(subprocess.TimeoutExpired):
                    proc.wait(timeout=5)
                raise subprocess.TimeoutExpired(cmd, timeout_sec)
            ready, _, _ = select.select([proc.stdout], [], [], 0.25)
            if ready:
                line = proc.stdout.readline()
                if line:
                    _emit(line)
                    continue
                # Empty read = EOF
                break
            if proc.poll() is not None:
                # Drain anything left buffered after process exit.
                for remainder in proc.stdout:
                    _emit(remainder)
                break
    finally:
        if proc.poll() is None:
            proc.kill()
            with contextlib.suppress(subprocess.TimeoutExpired):
                proc.wait(timeout=5)

    return subprocess.CompletedProcess(
        args=cmd,
        returncode=proc.returncode if proc.returncode is not None else -1,
        stdout="".join(lines),
        stderr="",
    )


def _run_task_script(
    task_dir: Path,
    script: str,
    *,
    timeout_sec: float,
    env: dict[str, str] | None = None,
    label: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a task-relative script on the host with the task directory as cwd.

    ``env`` is merged into the current environment (not replacing it), so the
    script still gets ``PATH``, ``HOME``, etc. alongside the injected values.
    When ``label`` is provided, the script's stdout/stderr is streamed live
    with a dim prefix so smoke output is self-describing by default.
    """
    if label is not None:
        return _stream_subprocess(
            ["bash", script],
            cwd=task_dir,
            env=_script_env(env),
            timeout_sec=timeout_sec,
            label=label,
        )
    return subprocess.run(  # noqa: S603
        ["bash", script],  # noqa: S607
        cwd=task_dir,
        capture_output=True,
        text=True,
        check=False,
        timeout=max(timeout_sec, 1),
        env=_script_env(env),
    )


# Default image for the containerized smoke sandbox. The reference
# ``solution.sh`` and any ``where: agent`` ``verify.sh`` both exec into this
# container, so its toolset must match what a real agent gets in production.
# The image mirrors the production agent sandbox toolchain
# (``platform/e2b/template_base.py``): python 3.13 + jq/git/curl/wget + uv,
# node, bun, gh, and friends, minus the SDK and S3-mount infra. Built from
# ``platform/docker/Dockerfile.task-smoke-solution`` and published by
# ``.github/workflows/publish-task-smoke-solution.yml``.
#
# Pinned by digest (immutable) so smoke runs are byte-for-byte reproducible.
# The digest is the multi-arch manifest-list index for tag ``2026.06.09``;
# bump both together when the image is rebuilt (the publish workflow prints
# the new digest in its run summary).
_DEFAULT_AGENT_SMOKE_IMAGE = (
    "docker.io/dreadnode/task-smoke-solution@sha256:"
    "11464ba1cedae10a9f31e58cb386b1382225d323f60b85e63bc826668a3bfdc8"
)


# ---------------------------------------------------------------------------
# Agent sandbox container
# ---------------------------------------------------------------------------
#
# Solution always runs in this container; verify runs in it too when
# ``verification.where: agent``. Single long-lived container per smoke run so
# files solution writes (e.g. /tmp/result.txt) survive the handoff to verify
# — mirroring production, where the agent and ``where: agent`` verifier
# share the same sandbox filesystem.


def _start_agent_container(
    *,
    image: str,
    network: str | None,
    env: dict[str, str] | None = None,
    pull_timeout_sec: float = 120.0,
) -> str:
    """Start a long-lived agent sandbox container and return its ID.

    The container runs ``sleep infinity`` so the smoke runner can ``docker
    exec`` solution/verify scripts into it. Attached to *network* when given
    (the compose project network), otherwise the default bridge so the agent
    still has outbound connectivity for composeless tasks.
    """
    cmd: list[str] = ["docker", "run", "-d", "--rm"]
    if network:
        cmd += ["--network", network]
    for key, value in (env or {}).items():
        cmd += ["-e", f"{key}={value}"]
    cmd += [image, "sleep", "infinity"]
    result = subprocess.run(  # noqa: S603
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=max(pull_timeout_sec, 5),
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown docker error"
        raise RuntimeError(f"failed to start agent container ({image}): {stderr}")
    container_id = result.stdout.strip()
    if not container_id:
        raise RuntimeError(f"docker did not return a container id for {image}")
    return container_id


def _stop_agent_container(container_id: str) -> None:
    """Best-effort ``docker rm -f`` for the agent container."""
    import contextlib

    with contextlib.suppress(subprocess.SubprocessError, OSError):
        subprocess.run(  # noqa: S603
            ["docker", "rm", "-f", container_id],  # noqa: S607
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )


# Where the task directory is staged inside the agent sandbox. Mirrors the
# environment sandbox's ``/home/user/task`` (TSK-EXEC-011) in spirit: scripts
# run from the task directory with all sibling files present.
_AGENT_TASK_DIR = "/task"


def _stage_task_dir_in_agent_container(container_id: str, task_dir: Path) -> None:
    """Copy the task directory into the agent container at ``_AGENT_TASK_DIR``.

    Multi-file solutions are contract-compliant (TSK-DIR-002 only requires
    self-containment *within* the task directory), so ``solution.sh`` must be
    able to reach siblings like ``solution.py`` or ``challenges/``. Staging
    the whole directory once, right after the container starts, gives every
    in-container script the same view.
    """
    # `docker cp <dir> <cid>:/task` creates /task and copies the *contents*
    # of <dir> into it when /task doesn't exist yet (docker cp semantics for
    # a non-existent directory destination).
    result = subprocess.run(  # noqa: S603
        ["docker", "cp", str(task_dir), f"{container_id}:{_AGENT_TASK_DIR}"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown docker error"
        raise RuntimeError(f"failed to stage task directory into agent container: {stderr}")


def _exec_in_agent_container(
    container_id: str,
    script: str,
    *,
    timeout_sec: float,
    label: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a task script inside the running agent container via ``docker exec``.

    ``script`` is the task-relative script path (e.g. ``solution.sh``),
    executed from the staged task directory (``_AGENT_TASK_DIR``) so sibling
    files the script references — ``solution.py``, ``challenges/``, helper
    scripts — resolve exactly as they do on disk (ENG-7113).

    Env vars travel with the container (set at ``docker run`` time), not per
    exec — keeps the contract simple: anything in the smoke context is
    visible to every script that runs in the sandbox.
    """
    cmd = ["docker", "exec", "-w", _AGENT_TASK_DIR, container_id, "bash", script]
    if label is not None:
        return _stream_subprocess(
            cmd,
            cwd=Path.cwd(),
            env=None,
            timeout_sec=timeout_sec,
            label=label,
        )
    return subprocess.run(  # noqa: S603
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=max(timeout_sec, 1),
    )


def _read_file_from_agent_container(container_id: str, path: str) -> tuple[bool, str, str]:
    """Read a file from inside the agent container.

    Returns ``(exists, content, error_reason)``. Missing files return
    ``(False, "", reason)`` so callers can distinguish "not written yet"
    from "container itself is broken."
    """
    result = subprocess.run(  # noqa: S603
        ["docker", "exec", container_id, "cat", path],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "No such file or directory" in stderr:
            return False, "", f"file '{path}' does not exist in agent container"
        return False, "", stderr or f"could not read '{path}' from agent container"
    return True, result.stdout, ""


def _remove_file_in_agent_container(container_id: str, path: str) -> None:
    """Best-effort ``rm -f`` inside the agent container.

    Used to clear any pre-existing flag file before the negative-verify
    phase so the unsolved check is meaningful.
    """
    import contextlib

    with contextlib.suppress(subprocess.SubprocessError, OSError):
        subprocess.run(  # noqa: S603
            ["docker", "exec", container_id, "rm", "-f", path],  # noqa: S607
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )


def _discover_compose_network(
    task_dir: Path,
    *,
    compose_file: Path,
    project_name: str,
) -> str | None:
    """Return the compose project's primary network name, or None.

    Queries ``docker compose ps -q`` for the first container id, then inspects
    it for network attachments. Robust to custom networks in the compose file
    since we read the actual attachment from Docker rather than guessing
    ``<project>_default``.
    """
    import json

    ps = _compose_run(
        ["ps", "-q"],
        cwd=task_dir,
        timeout_sec=10,
        compose_file=compose_file,
        project_name=project_name,
    )
    if ps.returncode != 0:
        return None
    container_ids = [line.strip() for line in ps.stdout.strip().splitlines() if line.strip()]
    if not container_ids:
        return None
    inspect = subprocess.run(  # noqa: S603
        ["docker", "inspect", container_ids[0], "--format", "{{json .NetworkSettings.Networks}}"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    if inspect.returncode != 0:
        return None
    try:
        networks = json.loads(inspect.stdout)
    except json.JSONDecodeError:
        return None
    if not isinstance(networks, dict) or not networks:
        return None
    for key in networks:
        if isinstance(key, str):
            return key
    return None


def _wait_for_infrastructure(
    task_dir: Path,
    deadline: float,
    *,
    compose_file: Path | None = None,
    project_name: str | None = None,
) -> ValidationIssue | None:
    """Poll until all compose services are healthy or have exited cleanly.

    A service is considered ready if:
    - It is ``running`` and either has no healthcheck or healthcheck is ``healthy``.
    - It has ``exited`` with code 0 (one-shot initializer pattern).

    Because the smoke test exists to run verify/solution against a live
    environment, at least one service must be in the ``running`` state — a
    stack where every service has exited is an error even if every exit code
    was zero, since there is nothing left for verify.sh to talk to.

    A service that exits non-zero, or fails to reach a ready state before the
    deadline, returns a ``ValidationIssue``.
    """
    import json
    import time

    while time.monotonic() < deadline:
        result = _compose_run(
            ["ps", "--format", "json"],
            cwd=task_dir,
            timeout_sec=10,
            compose_file=compose_file,
            project_name=project_name,
        )
        if result.returncode != 0:
            time.sleep(2)
            continue

        services: list[dict[str, t.Any]] = []
        for raw_line in result.stdout.strip().splitlines():
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                services.append(json.loads(stripped))
            except json.JSONDecodeError:
                continue

        if not services:
            time.sleep(2)
            continue

        all_ready = True
        any_running = False
        for svc in services:
            name = svc.get("Service", svc.get("Name", "?"))
            state = svc.get("State", "")
            health = svc.get("Health", "")

            if state == "exited":
                exit_code = svc.get("ExitCode", 0)
                if exit_code != 0:
                    return ValidationIssue(
                        "error",
                        "smoke-infra",
                        f"service '{name}' exited with code {exit_code}",
                    )
                # Cleanly exited (init/seeder pattern) — count as ready.
                continue

            if state != "running":
                all_ready = False
                break

            if health and health != "healthy":
                all_ready = False
                break

            any_running = True

        if all_ready:
            if not any_running:
                return ValidationIssue(
                    "error",
                    "smoke-infra",
                    "all compose services exited; nothing running for verify.sh to reach",
                )
            return None

        time.sleep(2)

    return ValidationIssue("error", "smoke-infra", "services not ready before timeout")


def _smoke_project_name(task_dir: Path) -> str:
    """Return a docker compose project name unique to this smoke run.

    ``smoke-<task_dir_slug>-<pid>-<short_uuid>``. Keeping the task slug in the
    name makes ``docker compose ls`` output legible while the pid + uuid guard
    against collisions between parallel runs of the same task.
    """
    import os
    import re
    import uuid

    slug = re.sub(r"[^a-z0-9]+", "-", task_dir.name.lower()).strip("-")[:32]
    return f"smoke-{slug}-{os.getpid()}-{uuid.uuid4().hex[:6]}"


def _extract_bind_source(entry: t.Any) -> str | None:
    """Return the host source of a compose volume entry iff it's a bind mount.

    Compose accepts short-form (``"host:container[:mode]"``) and long-form
    (``{type: bind, source: ..., target: ...}``). Named volumes
    (``{type: volume, ...}`` or bare ``myvol:/data``) return None — they're
    not host paths, so smoke can let ``docker compose down -v`` reap them.
    """
    if isinstance(entry, str):
        host = entry.split(":", 1)[0]
        # Short form: a host source is a path (absolute or task-relative).
        # Anything else is a named-volume reference.
        if host.startswith(("/", "./", "../")):
            return host
        return None
    if isinstance(entry, dict):
        if entry.get("type") not in (None, "bind"):
            return None
        source = entry.get("source")
        if isinstance(source, str) and source.startswith(("/", "./", "../")):
            return source
        return None
    return None


def _ephemeral_bind_mount_dirs(compose_doc: dict[str, t.Any], task_dir: Path) -> list[Path]:
    """Return absolute host paths that smoke owns as ephemeral state.

    Convention: any compose bind-mount source under the task directory whose
    first path component starts with ``.`` is treated as smoke-owned
    ephemeral state — e.g. the spec's ``./.submission/`` submission service
    convention (TSK-SUB-003), which accumulates agent uploads on the host
    filesystem. Wiping these before/after the compose lifecycle keeps each
    smoke run hermetic so a prior run's flag file can't poison the next
    run's negative verification.

    Author-owned task content (``./challenge/``, ``./fixtures/``) is left
    alone — only top-level hidden directories qualify.
    """
    services = compose_doc.get("services")
    if not isinstance(services, dict):
        return []
    task_dir_abs = task_dir.resolve()
    seen: set[Path] = set()
    out: list[Path] = []
    for svc_config in services.values():
        if not isinstance(svc_config, dict):
            continue
        volumes = svc_config.get("volumes")
        if not isinstance(volumes, list):
            continue
        for entry in volumes:
            source = _extract_bind_source(entry)
            if source is None:
                continue
            abs_path = (task_dir_abs / source).resolve()
            try:
                rel = abs_path.relative_to(task_dir_abs)
            except ValueError:
                continue  # escapes task dir — not ours to touch
            parts = rel.parts
            if not parts or not parts[0].startswith("."):
                continue
            if abs_path in seen:
                continue
            seen.add(abs_path)
            out.append(abs_path)
    return out


def _wipe_ephemeral_bind_mount_dirs(paths: list[Path]) -> None:
    """Best-effort: recreate each path empty.

    Run before ``compose up`` (clears state from prior runs or manual
    invocations) and in ``finally`` after ``compose down`` (leaves no
    debris). ``rmtree`` swallows errors because the wipe is defensive —
    a permission glitch on one path shouldn't fail the smoke run.
    """
    import contextlib
    import shutil

    for path in paths:
        with contextlib.suppress(OSError):
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)
            path.mkdir(parents=True, exist_ok=True)


def _parse_service_env(values: list[str] | None) -> dict[str, str]:
    """Parse repeatable smoke ``-e``/``--env`` flags into a ``{KEY: VALUE}`` map.

    ``KEY=VALUE`` sets a literal value (split on the first ``=``). A bare ``KEY``
    forwards the value from ``os.environ`` so secrets stay out of argv, shell
    history, and ``ps``. A bare key whose variable is unset is an error -- you
    asked to forward it, but there is nothing to forward, so fail loud rather
    than silently inject an empty string.
    """
    if not values:
        return {}
    import os

    out: dict[str, str] = {}
    for raw in values:
        key, sep, value = raw.partition("=")
        key = key.strip()
        if not key:
            raise ValueError(f"--env expects KEY or KEY=VALUE, got: {raw!r}")
        if sep:
            out[key] = value
        elif key in os.environ:
            out[key] = os.environ[key]
        else:
            raise ValueError(
                f"--env {key}: no value supplied and {key} is not set in the environment"
            )
    return out


def _normalize_compose_env(raw: t.Any) -> dict[str, t.Any]:
    """Normalize a compose ``environment`` block to map form.

    Compose accepts either a list (``["K=v", "BARE"]``) or a map
    (``{K: v}``). List entries are split on the first ``=``; a bare list entry
    (host pass-through) becomes ``{KEY: None}``. Anything else yields an empty
    map so callers can merge unconditionally.
    """
    if isinstance(raw, dict):
        return dict(raw)
    if isinstance(raw, list):
        out: dict[str, t.Any] = {}
        for entry in raw:
            if not isinstance(entry, str):
                continue
            key, sep, value = entry.partition("=")
            out[key] = value if sep else None
        return out
    return {}


def _write_ephemeral_compose_file(
    original: Path,
    destination: Path,
    *,
    inject_env: dict[str, str] | None = None,
) -> dict[str, list[int]]:
    """Rewrite ``original`` so every service's ports use random host ports.

    Docker compose short-form ``"3000"`` (container port only) assigns a
    random host port at ``up`` time, which we discover afterwards via
    ``docker compose port``. Returns ``{service: [container_port, ...]}`` so
    the caller knows which ports to query.

    When ``inject_env`` is given, those entries are merged into every service's
    ``environment`` block (normalized to map form first), overriding any
    same-named key the compose declares. This is the smoke-time challenge-env
    injection (``dn task validate --smoke -e KEY=VALUE``): non-destructive, the
    on-disk compose is never touched -- the same seam where ports are mutated.
    """
    import yaml

    doc = yaml.safe_load(original.read_text())
    if not isinstance(doc, dict):
        destination.write_text(original.read_text())
        return {}
    services = doc.get("services")
    if not isinstance(services, dict):
        destination.write_text(original.read_text())
        return {}

    per_service: dict[str, list[int]] = {}
    for svc_name, svc_config in services.items():
        if not isinstance(svc_config, dict):
            continue
        if inject_env:
            merged = _normalize_compose_env(svc_config.get("environment"))
            merged.update(inject_env)
            svc_config["environment"] = merged
        raw_ports = svc_config.get("ports")
        if not isinstance(raw_ports, list) or not raw_ports:
            continue
        container_ports: list[int] = []
        rewritten: list[t.Any] = []
        for entry in raw_ports:
            parsed = _parse_compose_port_entry(entry)
            if parsed is None:
                rewritten.append(entry)
                continue
            container, _ = parsed
            container_ports.append(container)
            rewritten.append(str(container))  # container-only form → random host
        svc_config["ports"] = rewritten
        if container_ports:
            per_service[svc_name] = container_ports

    destination.write_text(yaml.safe_dump(doc, sort_keys=False))
    return per_service


def _discover_host_ports(
    *,
    task_dir: Path,
    compose_file: Path,
    project_name: str,
    declared: dict[str, list[int]],
) -> dict[str, dict[int, int]]:
    """Query ``docker compose port`` to map each declared container port to its
    actual assigned host port after ``up``.
    """
    out: dict[str, dict[int, int]] = {}
    for service, ports in declared.items():
        svc_mapping: dict[int, int] = {}
        for container_port in ports:
            result = _compose_run(
                ["port", service, str(container_port)],
                cwd=task_dir,
                timeout_sec=10,
                compose_file=compose_file,
                project_name=project_name,
            )
            if result.returncode != 0:
                continue
            text = result.stdout.strip()
            if not text or ":" not in text:
                continue
            # Output is e.g. "0.0.0.0:53421" or "[::]:53421" on some hosts.
            host_port_str = text.rsplit(":", 1)[-1].strip()
            try:
                svc_mapping[container_port] = int(host_port_str)
            except ValueError:
                continue
        if svc_mapping:
            out[service] = svc_mapping
    return out


def _parse_compose_port_entry(entry: t.Any) -> tuple[int, int] | None:
    """Parse one compose port entry. Returns ``(container_port, host_port)`` or None.

    Accepts ints (``3000``), short-form strings (``"3000"``, ``"3001:3000"``,
    ``"127.0.0.1:3001:3000"``, ``"3001:3000/tcp"``), and the long form
    ``{target: 3000, published: 3001}``.
    """
    if isinstance(entry, int):
        return entry, entry
    if isinstance(entry, dict):
        target = entry.get("target")
        published = entry.get("published", target)
        if isinstance(target, int):
            try:
                return target, int(published) if published is not None else target
            except (TypeError, ValueError):
                return None
        return None
    if not isinstance(entry, str):
        return None
    # Strip protocol suffix, then split on colons. The container port is always
    # the last numeric segment; host port is the second-to-last (if present).
    base = entry.split("/", 1)[0]
    parts = base.split(":")
    try:
        if len(parts) == 1:
            p = int(parts[0])
            return p, p
        if len(parts) == 2:
            return int(parts[1]), int(parts[0])
        if len(parts) == 3:
            return int(parts[2]), int(parts[1])
    except ValueError:
        return None
    return None


def _parse_compose_host_ports(compose_path: Path) -> dict[str, dict[int, int]]:
    """Return ``{service: {container_port: host_port}}`` from a compose file.

    Only services with ``ports`` are included — ``expose`` is intentionally
    omitted since those services aren't reachable from the host.
    """
    import yaml

    out: dict[str, dict[int, int]] = {}
    try:
        doc = yaml.safe_load(compose_path.read_text())
    except (OSError, yaml.YAMLError):
        return out
    if not isinstance(doc, dict):
        return out
    services = doc.get("services") or {}
    if not isinstance(services, dict):
        return out

    for svc_name, svc_config in services.items():
        if not isinstance(svc_config, dict):
            continue
        raw_ports = svc_config.get("ports")
        if not isinstance(raw_ports, list):
            continue
        mapping: dict[int, int] = {}
        for entry in raw_ports:
            parsed = _parse_compose_port_entry(entry)
            if parsed is not None:
                container, host = parsed
                mapping[container] = host
        if mapping:
            out[svc_name] = mapping
    return out


def _build_smoke_context(
    raw: dict[str, t.Any],
    host_ports: dict[str, dict[int, int]],
) -> tuple[dict[str, str], dict[str, str]]:
    """Build ``(env_vars, template_vars)`` for **host-side** script execution.

    ``host_ports`` maps ``service → {container_port: host_port}`` as discovered
    from ``docker compose port`` after the stack is up. URLs use
    ``http://localhost:<host_port>`` since scripts in this mode run on the host.
    Used for flag-method solution/verify, environment-side script verify,
    provision, and teardown.
    """
    template_vars: dict[str, str] = {}
    declared_ports = raw.get("ports") if isinstance(raw.get("ports"), dict) else {}

    for service, port_list in (declared_ports or {}).items():
        if not isinstance(port_list, list) or not port_list:
            continue
        svc_mapping = host_ports.get(service, {})
        if not svc_mapping:
            continue
        primary_container: int | None = next(
            (p for p in port_list if isinstance(p, int) and p in svc_mapping),
            None,
        )
        if primary_container is None:
            continue
        primary_host = svc_mapping[primary_container]
        template_vars[f"{service}_host"] = "localhost"
        template_vars[f"{service}_port"] = str(primary_host)
        template_vars[f"{service}_url"] = f"http://localhost:{primary_host}"
        for port in port_list:
            if isinstance(port, int) and port in svc_mapping:
                template_vars[f"{service}_url_{port}"] = f"http://localhost:{svc_mapping[port]}"

    env_vars = {_template_key_to_env(k): v for k, v in template_vars.items()}
    return env_vars, template_vars


def _build_agent_network_context(
    raw: dict[str, t.Any],
) -> tuple[dict[str, str], dict[str, str]]:
    """Build ``(env_vars, template_vars)`` for **container-side** execution.

    URLs use the compose **service DNS name** + **container port**, matching
    what a container attached to the compose network sees (and approximating
    what a real agent sandbox attached to the task network would see). Used
    for ``where: agent`` verify/solution scripts that run inside a sandbox,
    and for the rendered instruction preview — because the instruction is
    what the real agent will read, and the real agent is always sandboxed.
    """
    template_vars: dict[str, str] = {}
    declared_ports = raw.get("ports") if isinstance(raw.get("ports"), dict) else {}

    for service, port_list in (declared_ports or {}).items():
        if not isinstance(port_list, list) or not port_list:
            continue
        container_ports = [p for p in port_list if isinstance(p, int)]
        if not container_ports:
            continue
        primary = container_ports[0]
        template_vars[f"{service}_host"] = service
        template_vars[f"{service}_port"] = str(primary)
        template_vars[f"{service}_url"] = f"http://{service}:{primary}"
        for port in container_ports:
            template_vars[f"{service}_url_{port}"] = f"http://{service}:{port}"

    env_vars = {_template_key_to_env(k): v for k, v in template_vars.items()}
    return env_vars, template_vars


def _template_key_to_env(key: str) -> str:
    """Convert a template variable key (``app_url``) to an env var name (``APP_URL``)."""
    return key.upper().replace("-", "_").replace(".", "_")


def _render_template(text: str, context: dict[str, str]) -> tuple[str, list[str]]:
    """Render ``{{var}}`` placeholders. Returns ``(rendered, unresolved_keys)``.

    Unresolved placeholders are left intact so authors see exactly which variable
    didn't resolve, rather than getting a silent empty string.
    """
    import re

    unresolved: list[str] = []

    def _sub(match: "re.Match[str]") -> str:
        key = match.group(1)
        if key in context:
            return context[key]
        unresolved.append(key)
        return match.group(0)

    rendered = re.sub(r"\{\{\s*(\w+)\s*\}\}", _sub, text)
    return rendered, unresolved


def _check_flag_content(
    content: str, *, value: str | None, hash_str: str | None
) -> tuple[bool, str]:
    """Return ``(passed, reason)`` for a flag-method verification check.

    Compares already-read flag *content* (whitespace stripped) against either
    the plaintext ``value`` or the ``hash_str`` (``alg:hex`` or bare hex).
    Sourcing the content from disk or from an agent container is the
    caller's responsibility — this helper is the comparison-only core so it
    can be reused across execution contexts.
    """
    import hashlib

    from dreadnode.packaging.task_validation import parse_flag_hash

    stripped = content.strip()
    if value is not None:
        return stripped == value.strip(), "content did not match expected value"
    if hash_str:
        try:
            alg, expected_hex = parse_flag_hash(hash_str)
        except ValueError as exc:
            return False, f"invalid hash format: {exc}"
        actual_hex = hashlib.new(alg, stripped.encode()).hexdigest()
        return actual_hex == expected_hex, "content hash did not match expected"
    return False, "no expected value or hash declared"


_DEFAULT_SMOKE_TIMEOUT = 120


def _resolve_smoke_timeout(raw: dict[str, t.Any], explicit: int | None) -> int:
    """Pick a smoke wall-clock budget.

    Precedence: explicit CLI ``--timeout`` → task.yaml ``max_agent_timeout_sec``
    → :data:`_DEFAULT_SMOKE_TIMEOUT`. The CLI override always wins so users can
    debug slow tasks without editing the manifest.
    """
    if explicit is not None:
        return explicit
    declared = raw.get("max_agent_timeout_sec")
    if isinstance(declared, int) and declared > 0:
        return declared
    return _DEFAULT_SMOKE_TIMEOUT


def _run_smoke_test(
    task_dir: Path,
    *,
    timeout: int | None = None,
    service_env: list[str] | None = None,
) -> list[ValidationIssue]:
    """Run the v1 smoke lifecycle for a single task directory.

    Lifecycle:

    1. (Compose tasks only) ``docker compose up -d --build`` and wait until
       all services are healthy or have exited cleanly.
    2. ``provision.sh`` on host (optional). Stdout JSON merges into both
       host and agent template/env contexts.
    3. Start a long-lived agent sandbox container, attached to the compose
       network if present, default bridge otherwise.
    4. **Negative verification** — with no solution run yet, verification must
       report failure. For ``method: flag`` any pre-existing flag file is
       removed from the sandbox first so the unsolved check is meaningful.
    5. **Positive verification** — run solution.sh in the sandbox, then
       re-verify. Skipped if no solution script is declared.
    6. ``teardown.sh`` on host (optional).
    7. Stop the agent container. (Compose tasks only) ``docker compose down``.

    Execution model:

    - The task directory is staged into the agent sandbox at ``/task`` right
      after the container starts; every in-container script runs from there,
      so sibling files (``solution.py``, ``challenges/``, helpers) resolve
      exactly as on disk.
    - **solution.sh** always runs inside the agent sandbox container — it
      stands in for the agent, which is always sandboxed in production.
    - **verify.sh** dispatches on ``verification.where``:
        - ``where: agent`` — exec'd into the same sandbox container, so
          files solution wrote (e.g. ``/tmp/result.txt``) are visible.
          Note: smoke gives this script the staged task dir, but production
          delivers only the script itself (TSK-EXEC-008/TSK-VER-015) — a
          sibling-reading agent verify still fails in production.
        - ``where: environment`` (default) — runs on host with
          ``cwd=task_dir`` and ``host_env`` (localhost:host_port URLs),
          for checking server-side state via compose services.
    - **method: flag** — solution writes the flag inside the sandbox;
      the runner reads it back via ``docker exec cat``.

    Requires docker. Returns a list of ValidationIssue for any problems found.
    """
    import tempfile
    import time

    import yaml

    issues: list[ValidationIssue] = []

    # Challenge-service env to merge into the ephemeral compose (smoke only).
    # Parse up front so a bad/unset bare key fails loud before any docker work.
    try:
        injected_service_env = _parse_service_env(service_env)
    except ValueError as exc:
        issues.append(ValidationIssue("error", "smoke", str(exc)))
        return issues

    raw = yaml.safe_load((task_dir / "task.yaml").read_text())
    timeout = _resolve_smoke_timeout(raw, timeout)
    verification = raw.get("verification") or {}
    solution = raw.get("solution") or {}
    provision_cfg = raw.get("provision") or {}
    teardown_cfg = raw.get("teardown") or {}

    method = verification.get("method") if isinstance(verification, dict) else None
    # Compound judge-backed methods share a mechanical half with their bare
    # counterparts (see ``_verify_script_only`` in service_execution.py, used by
    # both ``script`` and ``script_and_judge``). Smoke can't run the judge
    # offline — it has no agent trajectory — but it can and should run that
    # mechanical half: provision → negative verify → solution.sh → positive
    # verify → teardown. So normalize to the base method here; the judge is
    # simply never invoked in the smoke runner. ``outcome_judge`` has no
    # mechanical half, so it stays skipped below.
    if method == "script_and_judge":
        method = "script"
    elif method == "flag_and_judge":
        method = "flag"
    verify_script = verification.get("script") if isinstance(verification, dict) else None
    where = verification.get("where") if isinstance(verification, dict) else None
    solution_script = solution.get("script") if isinstance(solution, dict) else None
    provision_script = provision_cfg.get("script") if isinstance(provision_cfg, dict) else None
    provision_timeout = (
        provision_cfg.get("timeout", 120) if isinstance(provision_cfg, dict) else 120
    )
    teardown_script = teardown_cfg.get("script") if isinstance(teardown_cfg, dict) else None
    teardown_timeout = teardown_cfg.get("timeout", 120) if isinstance(teardown_cfg, dict) else 120

    if method not in ("script", "flag"):
        issues.append(
            ValidationIssue(
                "warning",
                "smoke",
                f"smoke test does not support verification.method: {method!r} — skipping",
            )
        )
        return issues

    if method == "script":
        if not verify_script:
            issues.append(
                ValidationIssue(
                    "warning",
                    "smoke",
                    "method: script declared without verify script — skipping",
                )
            )
            return issues
        if not (task_dir / verify_script).is_file():
            issues.append(
                ValidationIssue(
                    "error",
                    "smoke",
                    f"verification script '{verify_script}' not found on disk",
                )
            )
            return issues

    # Flag path is a container-side path under the new model — solution.sh
    # always runs in the agent sandbox, so the file lives inside it. The
    # smoke runner reads it back via ``docker exec cat`` rather than from
    # the host filesystem.
    flag_path: str | None = None
    flag_value: str | None = None
    flag_hash: str | None = None
    if method == "flag":
        raw_path = verification.get("path")
        flag_value = verification.get("value")
        flag_hash = verification.get("hash")
        if not raw_path:
            issues.append(
                ValidationIssue("error", "smoke", "verification.path is required for method: flag"),
            )
            return issues
        if not (flag_value or flag_hash):
            issues.append(
                ValidationIssue(
                    "error",
                    "smoke",
                    "verification needs 'value' or 'hash' for method: flag",
                ),
            )
            return issues
        flag_path = str(raw_path)

    compose_path = _find_compose_file(task_dir)
    has_compose = compose_path is not None

    if injected_service_env and not has_compose:
        issues.append(
            ValidationIssue(
                "warning",
                "smoke",
                "-e/--env was given but this task has no compose service to inject into",
            )
        )

    # Two smoke contexts are built after compose is up:
    #   - host_env / host_template_vars: service URLs using the randomly
    #     assigned host ports. Used for scripts that run on the host.
    #   - agent_env / agent_template_vars: service URLs using compose DNS
    #     names (http://<service>:<container_port>). Used for scripts that
    #     run inside a container on the compose network (where: agent), and
    #     for the rendered instruction preview (which shows what the real
    #     agent will read).
    host_env: dict[str, str] = {}
    host_template_vars: dict[str, str] = {}
    agent_env: dict[str, str] = {}
    agent_template_vars: dict[str, str] = {}

    # Per-run ephemeral compose file + project name so parallel smoke runs
    # don't collide on fixed host ports or shared compose state.
    smoke_compose_file: Path | None = None
    smoke_project: str | None = None
    smoke_compose_workspace: tempfile.TemporaryDirectory[str] | None = None
    declared_host_ports: dict[str, list[int]] = {}
    compose_network: str | None = None

    deadline = time.monotonic() + timeout

    def remaining() -> float:
        return max(0.0, deadline - time.monotonic())

    compose_started = False
    agent_container_id: str | None = None
    ephemeral_bind_mounts: list[Path] = []

    def run_solution_script() -> subprocess.CompletedProcess[str]:
        """Run solution.sh in the agent sandbox container, cwd = staged task dir."""
        assert agent_container_id is not None  # guarded — container starts before this
        assert solution_script is not None  # guarded above
        return _exec_in_agent_container(
            agent_container_id,
            solution_script,
            timeout_sec=remaining(),
            label="solution",
        )

    def run_verify_script(*, label: str) -> subprocess.CompletedProcess[str]:
        """Run verify.sh — in the agent container or on the host per `where`."""
        assert verify_script is not None  # guarded above
        if where == "agent":
            assert agent_container_id is not None  # guarded
            return _exec_in_agent_container(
                agent_container_id,
                verify_script,
                timeout_sec=remaining(),
                label=label,
            )
        # where: environment (default) — runs on host with task dir as cwd
        # and host_env (localhost:port URLs) for compose service access.
        return _run_task_script(
            task_dir,
            verify_script,
            timeout_sec=remaining(),
            env=host_env,
            label=label,
        )

    def verify_passes(*, label: str) -> tuple[bool, str]:
        """Return ``(passed, detail)`` for the current verification method."""
        if method == "script":
            result = run_verify_script(label=label)
            if result.returncode == 0:
                return True, ""
            tail = result.stdout.strip().splitlines()[-3:] if result.stdout.strip() else []
            return False, "; ".join(tail)
        # method == "flag" — solution writes inside the agent container, so
        # read the file back via docker exec.
        assert flag_path is not None  # guarded above
        assert agent_container_id is not None  # guarded
        exists, content, _ = _read_file_from_agent_container(agent_container_id, flag_path)
        if not exists:
            return False, f"flag file '{flag_path}' not produced by solution"
        return _check_flag_content(content, value=flag_value, hash_str=flag_hash)

    try:
        # --- Phase 1: Infrastructure (compose only) ----------------------
        if has_compose:
            assert compose_path is not None
            smoke_project = _smoke_project_name(task_dir)
            smoke_compose_workspace = tempfile.TemporaryDirectory(
                prefix=f"{task_dir.name}-smoke-compose-"
            )
            smoke_compose_file = Path(smoke_compose_workspace.name) / compose_path.name
            declared_host_ports = _write_ephemeral_compose_file(
                compose_path,
                smoke_compose_file,
                inject_env=injected_service_env or None,
            )

            # Clear smoke-owned ephemeral bind-mount dirs (e.g. ./.submission)
            # before compose up so a prior run's leftover state can't poison
            # this run's negative-verify phase.
            import yaml as _yaml

            try:
                compose_doc = _yaml.safe_load(smoke_compose_file.read_text())
            except _yaml.YAMLError:
                compose_doc = None
            if isinstance(compose_doc, dict):
                ephemeral_bind_mounts = _ephemeral_bind_mount_dirs(compose_doc, task_dir)
                if ephemeral_bind_mounts:
                    _wipe_ephemeral_bind_mount_dirs(ephemeral_bind_mounts)

            console.print("       [dim]smoke: starting containers (ephemeral ports)...[/]")
            result = _compose_run(
                ["up", "-d", "--build"],
                cwd=task_dir,
                timeout_sec=remaining(),
                compose_file=smoke_compose_file,
                project_name=smoke_project,
            )
            if result.returncode != 0:
                stderr_lines = [ln for ln in result.stderr.strip().splitlines() if ln.strip()]
                summary = stderr_lines[-1] if stderr_lines else "compose up failed"
                issues.append(ValidationIssue("error", "smoke-infra", summary))
                return issues
            compose_started = True

            infra_issue = _wait_for_infrastructure(
                task_dir,
                deadline,
                compose_file=smoke_compose_file,
                project_name=smoke_project,
            )
            if infra_issue:
                issues.append(infra_issue)
                return issues

            # Discover the actual host ports assigned by docker, then build
            # the smoke contexts so solution/verify see concrete URLs.
            host_ports = _discover_host_ports(
                task_dir=task_dir,
                compose_file=smoke_compose_file,
                project_name=smoke_project,
                declared=declared_host_ports,
            )
            host_env, host_template_vars = _build_smoke_context(raw, host_ports)
            agent_env, agent_template_vars = _build_agent_network_context(raw)
            compose_network = _discover_compose_network(
                task_dir,
                compose_file=smoke_compose_file,
                project_name=smoke_project,
            )

            elapsed = timeout - remaining()
            console.print(f"       [dim]smoke: infrastructure up ({elapsed:.0f}s)[/]")
            if host_template_vars:
                port_summary = ", ".join(
                    f"{svc}={url}"
                    for svc, url in sorted(
                        (k.removesuffix("_url"), v)
                        for k, v in host_template_vars.items()
                        if k.endswith("_url") and "_url_" not in k
                    )
                )
                if port_summary:
                    console.print(f"       [dim]smoke: {port_summary}[/]")
        else:
            console.print("       [dim]smoke: composeless task — skipping infrastructure[/]")

        # --- Phase 1b: Provision (optional) ------------------------------
        # README §Provisioning: provision runs before the agent, outputs JSON
        # to stdout, and the JSON keys are merged into the template/env context
        # for downstream phases.
        if provision_script:
            if not (task_dir / provision_script).is_file():
                issues.append(
                    ValidationIssue(
                        "error",
                        "smoke-provision",
                        f"provision script '{provision_script}' not found on disk",
                    )
                )
                return issues
            console.print("       [dim]smoke: running provision.sh...[/]")
            provision_deadline = min(float(provision_timeout), remaining())
            # Provision parses stdout as JSON, so we intentionally do NOT
            # stream it — a well-behaved provision script emits progress on
            # stderr and only the JSON object on stdout. Streaming would mix
            # the two and break parsing.
            result = _run_task_script(
                task_dir,
                provision_script,
                timeout_sec=provision_deadline,
                env=host_env,
            )
            if result.returncode != 0:
                stderr_tail = (
                    result.stderr.strip().splitlines()[-3:] if result.stderr.strip() else []
                )
                detail = "; ".join(stderr_tail) if stderr_tail else ""
                msg = f"provision.sh failed (exit {result.returncode})"
                if detail:
                    msg += f" — {detail}"
                issues.append(ValidationIssue("error", "smoke-provision", msg))
                return issues

            import json as _json

            provision_data: dict[str, t.Any] = {}
            stdout = result.stdout.strip()
            if stdout:
                try:
                    parsed = _json.loads(stdout)
                except _json.JSONDecodeError as exc:
                    issues.append(
                        ValidationIssue(
                            "error",
                            "smoke-provision",
                            f"provision.sh stdout is not valid JSON: {exc}",
                        )
                    )
                    return issues
                if not isinstance(parsed, dict):
                    issues.append(
                        ValidationIssue(
                            "error",
                            "smoke-provision",
                            f"provision.sh must emit a JSON object (got {type(parsed).__name__})",
                        )
                    )
                    return issues
                provision_data = parsed

            for key, value in provision_data.items():
                str_value = str(value)
                env_name = _template_key_to_env(str(key))
                # Merge into both contexts — provision output is provider-
                # agnostic (e.g. a lab URL) and applies equally to host-side
                # and container-side execution.
                host_template_vars[str(key)] = str_value
                agent_template_vars[str(key)] = str_value
                host_env[env_name] = str_value
                agent_env[env_name] = str_value
            console.print(
                f"       [dim]smoke: provision added {len(provision_data)} template var(s)[/]"
            )

        # --- Phase 1c: Render instruction and surface unresolved vars ----
        # Instruction is rendered with the agent-network context so the preview
        # matches what the real agent sandbox will read: compose DNS URLs, not
        # host-mapped localhost ports that only exist for the smoke harness.
        instruction = raw.get("instruction")
        if isinstance(instruction, str) and agent_template_vars:
            rendered, unresolved = _render_template(instruction, agent_template_vars)
            if unresolved:
                # Surface as an error — an instruction that references an
                # undeclared template variable would render as literal
                # "{{var}}" for the agent, which is broken at runtime.
                missing = ", ".join(sorted(set(unresolved)))
                issues.append(
                    ValidationIssue(
                        "error",
                        "smoke-instruction",
                        f"instruction references unresolved template var(s): {missing}",
                    )
                )
                return issues
            if rendered != instruction:
                console.print("       [dim]smoke: rendered instruction preview:[/]")
                for line in rendered.splitlines():
                    console.print(f"       [dim]│ {line}[/]")

        # --- Phase 1d: Start agent sandbox container ----------------------
        # Solution always runs in this container; `where: agent` verify runs
        # in it too. One long-lived container per smoke run so files solution
        # writes (e.g. /tmp/result.txt) survive into verify — mirroring
        # production, where the agent and ``where: agent`` verifier share
        # the same sandbox filesystem.
        console.print("       [dim]smoke: starting agent sandbox container...[/]")
        try:
            agent_container_id = _start_agent_container(
                image=_DEFAULT_AGENT_SMOKE_IMAGE,
                network=compose_network,
                env=agent_env,
            )
            # Stage the task directory at /task so in-container scripts can
            # reach sibling files (solution.py, challenges/, helpers) — the
            # original smoke design (2026-04-02 spec), restored by ENG-7113.
            _stage_task_dir_in_agent_container(agent_container_id, task_dir)
        except (RuntimeError, subprocess.SubprocessError, OSError) as exc:
            issues.append(ValidationIssue("error", "smoke-infra", str(exc)))
            return issues

        # --- Phase 2: Negative verification ------------------------------
        # For flag-method, clear any stale state so the unsolved check is
        # meaningful. The flag file lives inside the agent container under
        # the new model, so cleanup is a docker exec rm. For script-method,
        # the verify script is responsible for observing the unsolved state
        # itself.
        if method == "flag" and flag_path is not None:
            _remove_file_in_agent_container(agent_container_id, flag_path)

        passed, _ = verify_passes(label="verify·neg")
        if passed:
            issues.append(
                ValidationIssue(
                    "error",
                    "smoke-verify",
                    "verification passes without solution (always-pass bug)",
                )
            )
            return issues
        console.print("       [dim]smoke: verification correctly rejects unsolved state[/]")

        # --- Phase 3: Positive verification (optional) -------------------
        if not solution_script:
            issues.append(
                ValidationIssue(
                    "warning",
                    "smoke",
                    "no solution script declared — skipping positive verification",
                )
            )
            return issues

        if not (task_dir / solution_script).is_file():
            issues.append(
                ValidationIssue(
                    "warning",
                    "smoke",
                    f"solution script '{solution_script}' not found — skipping positive "
                    "verification",
                )
            )
            return issues

        result = run_solution_script()
        if result.returncode != 0:
            stderr_tail = result.stdout.strip().splitlines()[-3:] if result.stdout.strip() else []
            detail = "; ".join(stderr_tail) if stderr_tail else ""
            msg = f"solution.sh failed (exit {result.returncode})"
            if detail:
                msg += f" — {detail}"
            issues.append(ValidationIssue("error", "smoke-solve", msg))
            return issues
        console.print("       [dim]smoke: solution.sh completed[/]")

        passed, detail = verify_passes(label="verify·pos")
        if not passed:
            msg = "verification fails after running solution"
            if detail:
                msg += f" — {detail}"
            issues.append(ValidationIssue("error", "smoke-verify", msg))
            return issues
        console.print("       [dim]smoke: verification correctly accepts reference solution[/]")

    except subprocess.TimeoutExpired:
        issues.append(ValidationIssue("error", "smoke-infra", f"timed out after {timeout}s"))
    finally:
        # Teardown runs first — the README contract is that teardown releases
        # external resources created by provision, which is important to do
        # even when the run fails before verification completes. Failures here
        # are logged but don't change the outcome (matches README §Provisioning).
        if teardown_script and (task_dir / teardown_script).is_file():
            console.print("       [dim]smoke: running teardown.sh...[/]")
            try:
                td_result = _run_task_script(
                    task_dir,
                    teardown_script,
                    timeout_sec=min(float(teardown_timeout), max(remaining(), 5.0)),
                    env=host_env,
                    label="teardown",
                )
                if td_result.returncode != 0:
                    issues.append(
                        ValidationIssue(
                            "warning",
                            "smoke-teardown",
                            f"teardown.sh exited {td_result.returncode} — "
                            "external resources may be leaked",
                        )
                    )
            except subprocess.TimeoutExpired:
                issues.append(
                    ValidationIssue(
                        "warning",
                        "smoke-teardown",
                        "teardown.sh timed out — external resources may be leaked",
                    )
                )
        if agent_container_id is not None:
            _stop_agent_container(agent_container_id)
        if compose_started:
            _compose_run(
                ["down", "-v", "--remove-orphans"],
                cwd=task_dir,
                timeout_sec=30,
                compose_file=smoke_compose_file,
                project_name=smoke_project,
            )
        if smoke_compose_workspace is not None:
            smoke_compose_workspace.cleanup()
        # Re-wipe the ephemeral bind-mount dirs after compose down so smoke
        # never leaves debris on the host that a later run (or a manual
        # docker compose) could see as solved state.
        if ephemeral_bind_mounts:
            _wipe_ephemeral_bind_mount_dirs(ephemeral_bind_mounts)

    return issues
