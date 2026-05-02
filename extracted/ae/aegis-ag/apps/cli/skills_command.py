"""Top-level skill management surface for the Aegis launcher."""

from __future__ import annotations

from argparse import SUPPRESS, ArgumentParser, Namespace
from pathlib import Path

from packages.skills import SkillDefinition, skill_provenance_fields

from .cli_main_support import CliCardSection, _print_cli_card
from .runtime import CliRuntime


def _build_parser(
    *,
    default_state_dir: Path | None = None,
    default_profile_dir: Path | None = None,
) -> ArgumentParser:
    parser = ArgumentParser(
        prog="aegis skills",
        description="Inspect, search, install, and toggle skill packages without entering wake.",
    )
    parser.add_argument("--state-dir", default=default_state_dir, type=Path, help=SUPPRESS)
    parser.add_argument("--profile-dir", default=default_profile_dir, type=Path, help=SUPPRESS)
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser(
        "list",
        help="List built-in, installed, authored, and discovered local skill entries.",
    )
    list_parser.add_argument("--limit", type=int, default=24)

    active = subparsers.add_parser(
        "active",
        help="Show the currently enabled installed skills for the active profile.",
    )
    active.add_argument("--limit", type=int, default=24)

    search = subparsers.add_parser(
        "search",
        help="Search local shelves first, then configured external skill sources.",
    )
    search.add_argument("query", nargs="+")
    search.add_argument("--source", default=None)
    search.add_argument("--limit", type=int, default=12)

    view = subparsers.add_parser(
        "view",
        help="Inspect one local or external skill package by id or reference.",
    )
    view.add_argument("reference")

    enable = subparsers.add_parser(
        "enable",
        help="Enable one installed skill for the active profile.",
    )
    enable.add_argument("skill_id")

    disable = subparsers.add_parser(
        "disable",
        help="Disable one installed skill for the active profile.",
    )
    disable.add_argument("skill_id")

    install = subparsers.add_parser(
        "install",
        help="Install one skill package from a hub id, public reference, local path, or manifest path.",
    )
    install.add_argument("reference")

    return parser


def _runtime_from_args(args: Namespace) -> CliRuntime:
    return CliRuntime.create(
        state_dir=Path(args.state_dir).expanduser(),
        profile_dir=Path(args.profile_dir).expanduser(),
    )


def _skill_summary_lines(skill: SkillDefinition) -> tuple[str, ...]:
    lines = [
        f"skill_id · {skill.skill_id}",
        f"display_name · {skill.display_name}",
        f"enabled · {skill.enabled}",
        f"version · {skill.version}",
        f"summary · {skill.summary}",
        f"provenance · {skill.provenance or 'built-in'}",
    ]
    slash_command = str(skill.metadata.get("slash_command") or "").strip()
    if slash_command:
        lines.append(f"slash_command · /{slash_command}")
    for label, value in skill_provenance_fields(skill.metadata):
        lines.append(f"{label} · {value}")
    return tuple(lines)


def _instruction_lines(skill: SkillDefinition) -> tuple[str, ...]:
    text = skill.instruction_text.strip()
    if not text:
        return ("<empty>",)
    return tuple(line.rstrip() for line in text.splitlines())


def _print_skill_list(runtime: CliRuntime, *, limit: int) -> None:
    entries = runtime.list_skill_hub(limit=limit)
    lines = tuple(
        f"{_display_skill_reference(entry)} | {entry.display_name} | source={entry.source_id} | {entry.summary}"
        for entry in entries
    ) or ("<empty>",)
    _print_cli_card(
        "Aegis skills",
        "Local skill shelves and bundled entries visible to the current operator profile.",
        sections=(
            CliCardSection("Visible catalog", lines),
            CliCardSection(
                "Next steps",
                (
                    "aegis skills active",
                    "aegis skills search <query>",
                    "aegis skills view <skill-id|reference>",
                    "aegis skills install <skill-id|reference|/path/to/skill>",
                ),
            ),
        ),
        next_commands=("aegis wake",),
    )


def _print_active_skills(runtime: CliRuntime, *, limit: int) -> None:
    skills = tuple(skill for skill in runtime.skill_catalog() if skill.enabled)
    lines = tuple(
        f"{skill.skill_id} | enabled={skill.enabled} | {skill.display_name} | {skill.summary}"
        for skill in skills[:limit]
    ) or ("<empty>",)
    _print_cli_card(
        "Aegis skills",
        "Enabled installed skill packages for the active profile.",
        sections=(CliCardSection("Active skills", lines),),
        next_commands=("aegis skills list", "aegis wake"),
    )


def _print_search_results(runtime: CliRuntime, query: str, *, source: str | None, limit: int) -> None:
    local_entries = runtime.search_skill_hub(query, limit=limit)
    external_entries = runtime.search_skill_sources(query, source=source, limit=limit)
    sections = [
        CliCardSection(
            "Local shelves",
            tuple(
                f"{_display_skill_reference(entry)} | {entry.display_name} | source={entry.source_id} | {entry.summary}"
                for entry in local_entries
            )
            or ("<empty>",),
        ),
        CliCardSection(
            "External sources",
            tuple(
                f"{entry.reference} | {entry.display_name} | source={entry.source_id} | trust={entry.trust_level or '<unknown>'} | {entry.summary}"
                for entry in external_entries
            )
            or ("<empty>",),
        ),
    ]
    _print_cli_card(
        "Aegis skills",
        f'Search results for "{query}".',
        sections=tuple(sections),
        next_commands=(
            "aegis skills view <skill-id|reference>",
            "aegis skills install <skill-id|reference>",
        ),
    )


def _print_skill_detail(runtime: CliRuntime, reference: str) -> None:
    skill = runtime.inspect_skill_source(reference)
    _print_cli_card(
        "Aegis skills",
        f"Detail for {skill.display_name}.",
        sections=(
            CliCardSection("Metadata", _skill_summary_lines(skill)),
            CliCardSection("Instructions", _instruction_lines(skill)),
        ),
        next_commands=("aegis skills install <skill-id|reference>", "aegis wake"),
    )


def _print_skill_toggle(runtime: CliRuntime, *, skill_id: str, enabled: bool) -> None:
    updated = runtime.set_skill_enabled(skill_id, enabled)
    detail = "enabled" if enabled else "disabled"
    _print_cli_card(
        "Aegis skills",
        f"{updated.display_name} is now {detail}.",
        sections=(CliCardSection("Updated skill", _skill_summary_lines(updated)),),
        next_commands=("aegis skills active", "aegis wake"),
    )


def _print_skill_install(runtime: CliRuntime, reference: str) -> None:
    record = runtime.install_skill_source(reference)
    skill_ids = ", ".join(record.skill_ids) if record.skill_ids else "<empty>"
    _print_cli_card(
        "Aegis skills",
        "Installed one skill source into the active operator profile.",
        sections=(
            CliCardSection(
                "Install record",
                (
                    f"status · {record.status}",
                    f"source_path · {record.source_path}",
                    f"skill_ids · {skill_ids}",
                    f"detail · {record.detail}",
                ),
            ),
        ),
        next_commands=("aegis skills active", "aegis wake"),
    )


def _display_skill_reference(entry) -> str:
    if getattr(entry, "source_id", "") == "builtin":
        return str(getattr(entry, "skill_id", "")).strip() or str(getattr(entry, "reference", ""))
    return str(getattr(entry, "reference", "")).strip()


def command_main(
    argv: list[str] | None = None,
    *,
    default_state_dir: Path | None = None,
    default_profile_dir: Path | None = None,
) -> int:
    parser = _build_parser(
        default_state_dir=default_state_dir,
        default_profile_dir=default_profile_dir,
    )
    args = parser.parse_args(argv)
    runtime = _runtime_from_args(args)
    command = args.command or "list"

    if command == "list":
        _print_skill_list(runtime, limit=getattr(args, "limit", 24))
        return 0
    if command == "active":
        _print_active_skills(runtime, limit=getattr(args, "limit", 24))
        return 0
    if command == "search":
        _print_search_results(
            runtime,
            " ".join(args.query).strip(),
            source=args.source,
            limit=args.limit,
        )
        return 0
    if command == "view":
        _print_skill_detail(runtime, args.reference)
        return 0
    if command == "enable":
        _print_skill_toggle(runtime, skill_id=args.skill_id, enabled=True)
        return 0
    if command == "disable":
        _print_skill_toggle(runtime, skill_id=args.skill_id, enabled=False)
        return 0
    if command == "install":
        _print_skill_install(runtime, args.reference)
        return 0
    parser.error(f"unknown skills command: {command}")
    return 2


__all__ = ["command_main"]
