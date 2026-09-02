"""
Native Python scaffold command for syncing SpecKit agent context files.

Replaces the legacy ``.specify/scripts/bash/update-agent-context.sh`` script
with a simpler design: the active feature's ``plan.md`` Technical Context is
summarized and inserted into the target agent's context file (e.g.
``.github/copilot-instructions.md``, ``.cursorrules``) between
``<!-- SPECKIT START -->`` / ``<!-- SPECKIT END -->`` markers, without
touching any other content in the file.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.state import is_dry_run
from agentic_devtools.task_state import print_task_tracking_info

from .scaffold_common import FeatureResolutionError, resolve_active_feature

#: Markers delimiting the SpecKit-managed block within an agent context file.
SPECKIT_START_MARKER = "<!-- SPECKIT START -->"
SPECKIT_END_MARKER = "<!-- SPECKIT END -->"

#: YAML frontmatter required for Cursor ``.mdc`` rule files to auto-load.
MDC_FRONTMATTER = "---\nalwaysApply: true\n---\n"
#: Regex matching an existing YAML frontmatter block at the very start of a file.
#: Accepts both LF and CRLF line endings so that Windows-edited ``.mdc`` files are
#: detected correctly instead of receiving a spurious second frontmatter block.
_MDC_FRONTMATTER_RE = re.compile(r"\A---\r?\n(?:.*?\r?\n)?---\r?\n", re.DOTALL)

#: Supported agent types mapped to their context file, relative to repo root.
AGENT_FILE_MAP: dict[str, str] = {
    "agy": "AGENTS.md",
    "alquimia": "ALQUIMIA.md",
    "amp": "AGENTS.md",
    "auggie": ".augment/rules/specify-rules.md",
    "bob": "AGENTS.md",
    "copilot": ".github/copilot-instructions.md",
    "claude": "CLAUDE.md",
    "cline": ".clinerules/specify-rules.md",
    "codebuddy": "CODEBUDDY.md",
    "codex": "AGENTS.md",
    "devin": "AGENTS.md",
    "firebender": ".firebender/rules/specify-rules.mdc",
    "forge": "AGENTS.md",
    "gemini": "GEMINI.md",
    "cursor-agent": ".cursor/rules/specify-rules.mdc",
    "generic": "AGENTS.md",
    "goose": "AGENTS.md",
    "grok": "AGENTS.md",
    "hermes": "AGENTS.md",
    "junie": ".junie/AGENTS.md",
    "opencode": "AGENTS.md",
    "kiro-cli": "AGENTS.md",
    "kimi": "AGENTS.md",
    "kilocode": ".kilocode/rules/specify-rules.md",
    "lingma": ".lingma/rules/specify-rules.md",
    "omp": "AGENTS.md",
    "pi": "AGENTS.md",
    "qodercli": "QODER.md",
    "qwen": "QWEN.md",
    "rovodev": "AGENTS.md",
    "shai": "SHAI.md",
    "tabnine": "TABNINE.md",
    "trae": ".trae/rules/project_rules.md",
    "vibe": "AGENTS.md",
    "windsurf": ".windsurf/rules/specify-rules.md",
    "zcode": "ZCODE.md",
    "zed": "AGENTS.md",
    # Additional compatibility aliases supported by earlier AGDT workflows and
    # generic __AGENT__ passthrough values.
    "cursor": ".cursorrules",
    "q": "AGENTS.md",  # Legacy integration key (Amazon Q Developer CLI).
    "qoder": "QODER.md",
    "roo": ".roo/rules/specify-rules.md",
}

#: Technical Context fields extracted from plan.md, in display order.
_TECHNICAL_CONTEXT_FIELDS = (
    "Language/Version",
    "Primary Dependencies",
    "Storage",
    "Testing",
    "Target Platform",
    "Project Type",
)

_FIELD_RE = re.compile(r"^\*\*([^*]+)\*\*:\s*(.*?)\s*$")
_SECTION_HEADING_RE = re.compile(r"^#{2,6}\s+")
_UNRESOLVED_VALUE_SENTINEL = "NEEDS CLARIFICATION"

__all__ = [
    "AGENT_FILE_MAP",
    "SPECKIT_END_MARKER",
    "SPECKIT_START_MARKER",
    "apply_marker_block",
    "build_plan_context_block",
    "escape_marker_tokens",
    "extract_technical_context",
    "scaffold_update_agent_context_async",
    "scaffold_update_agent_context_command",
    "update_agent_context",
]


def escape_marker_tokens(value: str) -> str:
    """HTML-escape managed marker tokens in interpolated plan values.

    Replaces literal ``<!-- SPECKIT START -->`` and ``<!-- SPECKIT END -->``
    with their ``&lt;!-- ... --&gt;`` forms so user-controlled branch/path/context
    values cannot inject additional marker lines that would break idempotent
    replacement in ``apply_marker_block``.
    """
    return value.replace(SPECKIT_START_MARKER, html.escape(SPECKIT_START_MARKER)).replace(
        SPECKIT_END_MARKER, html.escape(SPECKIT_END_MARKER)
    )


def extract_technical_context(plan_text: str) -> dict[str, str]:
    """
    Extract filled-in Technical Context fields from a ``plan.md`` document.

    Args:
        plan_text: Full text content of ``plan.md``.

    Returns:
        Mapping of field name (e.g. ``"Language/Version"``) to its value, for
        fields whose value has been filled in. Fields still holding an
        unresolved template placeholder (values starting with ``[``), the
        ``NEEDS CLARIFICATION`` sentinel, or an empty value are omitted.
        Multi-line field values are flattened into a single line; bullet-style
        continuation lines are joined with ``; `` so list items remain distinct.
    """
    fields: dict[str, str] = {}
    lines = plan_text.splitlines()
    index = 0
    while index < len(lines):
        match = _FIELD_RE.match(lines[index].strip())
        if not match:
            index += 1
            continue
        name = match.group(1).strip()
        value_parts: list[str] = []
        first_value = match.group(2).strip()
        if first_value:
            value_parts.append(first_value)

        index += 1
        while index < len(lines):
            stripped = lines[index].strip()
            if _FIELD_RE.match(stripped) or _SECTION_HEADING_RE.match(stripped):
                break
            if stripped:
                value_parts.append(stripped)
            index += 1

        normalized_parts = [part[2:].strip() if part.startswith("- ") else part for part in value_parts]
        bullet_flags = [part.startswith("- ") for part in value_parts]
        first_bullet_index = next(
            (bullet_index for bullet_index, is_bullet in enumerate(bullet_flags) if is_bullet),
            None,
        )
        if first_bullet_index is None:
            value = " ".join(normalized_parts).strip()
        else:
            prefix = " ".join(normalized_parts[:first_bullet_index]).strip()
            bullet_items: list[str] = []
            bullet_parts = normalized_parts[first_bullet_index:]
            bullet_part_flags = bullet_flags[first_bullet_index:]
            current_bullet = bullet_parts[0]
            for part, is_bullet in zip(bullet_parts[1:], bullet_part_flags[1:]):
                if is_bullet:
                    bullet_items.append(current_bullet)
                    current_bullet = part
                else:
                    current_bullet = f"{current_bullet} {part}".strip()
            bullet_items.append(current_bullet)
            bullet_text = "; ".join(bullet_items)
            value = f"{prefix} {bullet_text}".strip() if prefix else bullet_text
        if (
            name not in _TECHNICAL_CONTEXT_FIELDS
            or not value
            or value.startswith("[")
            or _UNRESOLVED_VALUE_SENTINEL in value.upper()
        ):
            continue
        fields[name] = value
    return fields


def build_plan_context_block(branch: str, feature_dir_display: str, fields: dict[str, str]) -> str:
    """
    Build the Markdown block inserted between the SpecKit markers.

    Args:
        branch: Active feature/branch name.
        feature_dir_display: Feature directory path to display (repo-relative
            when possible).
        fields: Technical Context fields as returned by
            ``extract_technical_context``.

    Returns:
        The full block text, including both start and end markers.
    """
    escaped_branch = escape_marker_tokens(branch)
    escaped_feature_dir_display = escape_marker_tokens(feature_dir_display)
    lines = [
        SPECKIT_START_MARKER,
        "",
        f"### Active SpecKit Feature: {escaped_branch}",
        "",
        f"- **Plan**: `{escaped_feature_dir_display}/plan.md`",
    ]
    for name in _TECHNICAL_CONTEXT_FIELDS:
        if name in fields:
            lines.append(f"- **{name}**: {escape_marker_tokens(fields[name])}")
    lines.extend(["", SPECKIT_END_MARKER])
    return "\n".join(lines)


def ensure_mdc_frontmatter(text: str) -> str:
    """
    Ensure a Cursor ``.mdc`` rule file has ``alwaysApply: true`` YAML frontmatter.

    Cursor auto-loads rule files only when their frontmatter includes
    ``alwaysApply: true``. If *text* starts with a YAML frontmatter block
    (``---\\n…\\n---\\n`` with either LF or CRLF line endings), that block is
    updated in place to ensure ``alwaysApply: true`` is present and the original
    newline style is preserved; otherwise the standard LF frontmatter is prepended.

    Args:
        text: Current file content (may be empty for a new file).

    Returns:
        *text* with the frontmatter present at the top.
    """
    match = _MDC_FRONTMATTER_RE.match(text)
    if not match:
        return MDC_FRONTMATTER + text

    frontmatter = match.group(0)
    body = text[match.end() :]
    # Detect newline style from the matched block and build the delimiter string.
    nl = "\r\n" if "\r\n" in frontmatter else "\n"
    delim = f"---{nl}"
    # Strip the opening and closing delimiter lines to get the inner content.
    inner = frontmatter[len(delim) : len(frontmatter) - len(delim)]
    inner_lines = inner.splitlines()  # splitlines handles both LF and CRLF
    updated_lines: list[str] = []
    always_apply_found = False
    for line in inner_lines:
        if re.match(r"^alwaysApply:\s*[\"']?(?:true|false)[\"']?\s*(?:#.*)?$", line, flags=re.IGNORECASE):
            updated_lines.append("alwaysApply: true")
            always_apply_found = True
        else:
            updated_lines.append(line)
    if not always_apply_found:
        updated_lines.append("alwaysApply: true")
    updated_frontmatter = delim + nl.join(updated_lines) + nl + delim
    return updated_frontmatter + body


def apply_marker_block(existing_text: str, block: str) -> str:
    """
    Insert or replace the SpecKit-managed block within *existing_text*.

    Args:
        existing_text: Current content of the agent context file (may be
            empty for a file that does not yet exist).
        block: The replacement block, as returned by
            ``build_plan_context_block``.

    Returns:
        The updated file content. If both markers are already present, the
        content between them (inclusive) is replaced in place. Otherwise the
        block is appended to the end of the file.

    Raises:
        ValueError: If marker text appears in a malformed layout instead of as
            exactly one ordered pair of standalone marker lines.
    """
    if existing_text:
        start_lines: list[int] = []
        end_lines: list[int] = []
        lines = existing_text.splitlines(keepends=True)
        for index, line in enumerate(lines):
            stripped = line.strip()
            contains_start = SPECKIT_START_MARKER in line
            contains_end = SPECKIT_END_MARKER in line
            if contains_start and stripped != SPECKIT_START_MARKER:
                raise ValueError("Malformed SpecKit marker block: start marker must appear on its own line.")
            if contains_end and stripped != SPECKIT_END_MARKER:
                raise ValueError("Malformed SpecKit marker block: end marker must appear on its own line.")
            if stripped == SPECKIT_START_MARKER:
                start_lines.append(index)
            if stripped == SPECKIT_END_MARKER:
                end_lines.append(index)

        if start_lines or end_lines:
            if len(start_lines) != 1 or len(end_lines) != 1 or start_lines[0] >= end_lines[0]:
                raise ValueError("Malformed SpecKit marker block: expected exactly one ordered marker pair.")
            trailing_newline = "\n" if lines[end_lines[0]].endswith("\n") else ""
            replacement_lines = [block + trailing_newline]
            updated_lines = lines[: start_lines[0]] + replacement_lines + lines[end_lines[0] + 1 :]
            return "".join(updated_lines)
    if not existing_text:
        return block + "\n"
    separator = "" if existing_text.endswith("\n") else "\n"
    return existing_text + separator + "\n" + block + "\n"


def update_agent_context(
    agent_type: str, repo_root: Path, feature_dir: Path, branch: str, *, dry_run: bool = False
) -> Path | None:
    """
    Update the agent context file for *agent_type* with the active plan context.

    Args:
        agent_type: Key into ``AGENT_FILE_MAP``, e.g. ``"copilot"``.  If the key
            is not present in ``AGENT_FILE_MAP`` the function prints a warning and
            returns ``None`` (no-op), matching upstream specify-cli's behaviour for
            integrations that do not have a default context file.
        repo_root: Repository root.
        feature_dir: Active feature directory (must contain ``plan.md``).
        branch: Active branch/feature name to display.
        dry_run: When ``True``, skip all filesystem mutations (``mkdir``,
            ``write_text``) and return the predicted agent file path without
            writing it.  All validation (path-escape, plan.md checks, marker
            validation) still runs so that dry-run output is accurate.

    Returns:
        Path to the (updated or predicted) agent context file, or ``None`` when
        *agent_type* is not recognised (no-op skip with a printed warning).

    Raises:
        ValueError: If the agent file resolves to a path outside *repo_root*
            (e.g. via a symlink).
        FileNotFoundError: If ``plan.md`` does not exist in *feature_dir*.
    """
    if agent_type not in AGENT_FILE_MAP:
        print(
            f"WARNING: agent type '{agent_type}' is not mapped to a context file — skipping update.",
            file=sys.stderr,
        )
        return None

    plan_path = feature_dir / "plan.md"
    if plan_path.is_symlink():
        raise ValueError(f"Refusing to read symlinked plan.md: {plan_path}")
    if not plan_path.is_file():
        raise FileNotFoundError(f"plan.md not found in {feature_dir}. Run agdt-speckit-plan first.")
    fields = extract_technical_context(plan_path.read_text(encoding="utf-8"))
    try:
        feature_dir_display = feature_dir.relative_to(repo_root).as_posix()
    except ValueError:
        feature_dir_display = feature_dir.as_posix()
    block = build_plan_context_block(branch, feature_dir_display, fields)

    agent_file = repo_root / AGENT_FILE_MAP[agent_type]
    resolved_agent_file = agent_file.resolve(strict=False)
    resolved_repo_root = repo_root.resolve()
    try:
        resolved_agent_file.relative_to(resolved_repo_root)
    except ValueError:
        raise ValueError(
            f"Agent file {agent_file} resolves to {resolved_agent_file}, which is outside the repository root "
            f"{resolved_repo_root}. Refusing to write to a path outside the repository."
        )
    existing_text = agent_file.read_text(encoding="utf-8") if agent_file.is_file() else ""
    updated_text = apply_marker_block(existing_text, block)
    if agent_file.suffix == ".mdc":
        updated_text = ensure_mdc_frontmatter(updated_text)
    if not dry_run:
        agent_file.parent.mkdir(parents=True, exist_ok=True)
        agent_file.write_text(updated_text, encoding="utf-8")
    return agent_file


def scaffold_update_agent_context_async(_argv: list[str] | None = None) -> None:
    """Background wrapper for ``agdt-speckit-scaffold-update-agent-context``."""
    argv = list(sys.argv[1:] if _argv is None else _argv)
    task = run_function_in_background(
        module_path="agentic_devtools.cli.speckit.scaffold_update_agent_context",
        function_name="scaffold_update_agent_context_command",
        command_display_name="agdt-speckit-scaffold-update-agent-context",
        func_kwargs={"argv": argv},
    )
    print_task_tracking_info(task)


def scaffold_update_agent_context_command(argv: list[str] | None = None) -> None:
    """CLI entry point for ``agdt-speckit-scaffold-update-agent-context``."""
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-scaffold-update-agent-context",
        description="Sync the active SpecKit plan context into an AI agent's context file.",
    )
    parser.add_argument(
        "agent_type",
        help=(
            "Target agent to update (e.g. 'copilot', 'claude', 'cursor'). "
            "If the agent type is not in the built-in map the command exits 0 with a warning."
        ),
    )
    args = parser.parse_args(argv)

    try:
        active = resolve_active_feature()
        dry_run = is_dry_run()
        agent_file = update_agent_context(
            args.agent_type, active.repo_root, active.feature_dir, active.branch, dry_run=dry_run
        )
    except (FeatureResolutionError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if agent_file is None:
        return
    if dry_run:
        print(f"[DRY RUN] Would update {agent_file}")
    else:
        print(f"Updated {agent_file}")
