"""Command-line interface for csrd-utils."""

import argparse
import json
import sys
from importlib.metadata import version
from pathlib import Path

from .audit import run_audit
from .compose import apply as compose_apply
from .compose import validate as compose_validate
from .doctor import run_doctor
from .generate import run_generate_menu

# ---------------------------------------------------------------------------
# Bash completion
# ---------------------------------------------------------------------------


def _parser_shape(
    parser: argparse.ArgumentParser,
    chain: tuple[str, ...] = (),
) -> tuple[dict[tuple[str, ...], list[str]], dict[tuple[str, ...], list[str]]]:
    commands: dict[tuple[str, ...], list[str]] = {}
    options: dict[tuple[str, ...], list[str]] = {}

    subcommands: list[str] = []
    flags: list[str] = []
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            subcommands.extend(sorted(action.choices.keys()))
            for name, subparser in action.choices.items():
                child_chain = (*chain, name)
                child_commands, child_options = _parser_shape(subparser, child_chain)
                commands.update(child_commands)
                options.update(child_options)
        else:
            flags.extend([item for item in action.option_strings if item.startswith("-")])

    commands[chain] = sorted(dict.fromkeys(subcommands))
    options[chain] = sorted(dict.fromkeys(flags))
    return commands, options


def _render_bash_completion() -> str:
    """Render a dynamic bash completion script.

    Instead of baking a static word list, the script calls
    ``csrd --_complete`` at tab-time so it always reflects the
    currently installed version's commands and flags.
    """
    return (
        "# bash completion for csrd — dynamic (calls csrd --_complete)\n"
        "_csrd_completion() {\n"
        "  local cur words\n"
        '  cur="${COMP_WORDS[COMP_CWORD]}"\n'
        '  words=$(csrd --_complete "${COMP_WORDS[@]:1:COMP_CWORD-1}" 2>/dev/null)\n'
        '  COMPREPLY=( $(compgen -W "$words" -- "$cur") )\n'
        "}\n"
        "complete -F _csrd_completion csrd csrd-utils csrt\n"
    )


def _handle_complete(parser: argparse.ArgumentParser, words: list[str]) -> int:
    """Print completion candidates for the given partial command line.

    Called by the bash completion script via ``csrd --_complete <words>``.
    """
    commands, options = _parser_shape(parser)

    # Walk the word chain to find the deepest matching subcommand
    chain: tuple[str, ...] = ()
    for word in words:
        if word.startswith("-"):
            continue
        candidate = (*chain, word)
        if candidate in commands:
            chain = candidate

    command_candidates = commands.get(chain, [])
    option_candidates = options.get(chain, [])
    print(" ".join(command_candidates + option_candidates))
    return 0


# ---------------------------------------------------------------------------
# Completion install/uninstall
# ---------------------------------------------------------------------------

_COMPLETION_DIR = Path.home() / ".local" / "share" / "bash-completion" / "completions"
_COMPLETION_FILE = _COMPLETION_DIR / "csrd"


def _install_completion() -> int:
    """Write the bash completion script to the user completions directory.

    bash-completion auto-loads files from ``~/.local/share/bash-completion/completions/``
    so no ``.bashrc`` edit is needed.  The script is a thin shim that calls
    ``csrd --_complete`` at tab-time, so it never goes stale after upgrades.
    """

    _COMPLETION_DIR.mkdir(parents=True, exist_ok=True)
    already = _COMPLETION_FILE.is_file()
    _COMPLETION_FILE.write_text(_render_bash_completion(), encoding="utf-8")
    if already:
        print(f"Updated bash completion at {_COMPLETION_FILE}")
    else:
        print(f"Installed bash completion to {_COMPLETION_FILE}")
        print("Open a new shell to activate.")
    return 0


def _uninstall_completion() -> int:
    """Remove the installed bash completion file."""

    if _COMPLETION_FILE.is_file():
        _COMPLETION_FILE.unlink()
        print(f"Removed {_COMPLETION_FILE}")
    else:
        print("No completion file installed.")
    return 0


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="csrd", description="csrd utilities")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"csrd-utils {version('csrd-utils')}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # ── generate ──────────────────────────────────────────────────────
    gen = sub.add_parser("generate", help="Interactive generator menu")
    gen.add_argument(
        "target",
        nargs="?",
        choices=[
            "workspace",
            "preset",
            "add-service",
            "add-infra",
            "remove-infra",
            "add-augment",
            "add-version",
            "add-frontend",
            "remove-service",
            "rename-service",
            "list-augments",
            "empty",
        ],
        help="Direct generator target",
    )
    gen.add_argument("--name", dest="generate_name", help="Workspace or service name")
    gen.add_argument(
        "--git-init",
        action="store_true",
        default=False,
        help="Initialize a git repository in the generated workspace",
    )
    gen.add_argument(
        "--features",
        nargs="*",
        choices=["database", "caching", "messaging"],
        default=None,
        help="Service capabilities to wire (for add-service)",
    )
    gen.add_argument("--port", type=int, default=None, help="Service port (for add-service)")
    gen.add_argument(
        "--infra-type",
        dest="infra_type",
        choices=["postgres", "mariadb", "sqlite", "redis", "rabbitmq"],
        default=None,
        help="Infrastructure type (for add-infra / remove-infra)",
    )
    gen.add_argument(
        "--service-name",
        dest="service_name",
        default=None,
        help="Service name (for remove-service / rename-service)",
    )
    gen.add_argument(
        "--new-name",
        dest="new_name",
        default=None,
        help="New service name (for rename-service)",
    )
    gen.add_argument(
        "--version-date",
        dest="version_date",
        default=None,
        help="Version date in YYYY-MM-DD format (for add-version)",
    )

    # ── compose ───────────────────────────────────────────────────────
    compose = sub.add_parser("compose", help="Compose operations")
    compose_sub = compose.add_subparsers(dest="compose_command")

    val = compose_sub.add_parser("validate", help="Validate csrd-compose.yaml")
    val.add_argument("--output", type=Path, default=Path.cwd(), help="Workspace root")
    val.add_argument("--json", action="store_true", help="Print validated spec as JSON")

    plan = compose_sub.add_parser("plan", help="Preview resolved compose baseline")
    plan.add_argument("--output", type=Path, default=Path.cwd(), help="Workspace root")
    plan.add_argument("--json", action="store_true", help="Print plan payload as JSON")

    apply_cmd = compose_sub.add_parser("apply", help="Render baseline workspace artifacts")
    apply_cmd.add_argument("--output", type=Path, default=Path.cwd(), help="Workspace root")
    apply_cmd.add_argument(
        "--git-init",
        action="store_true",
        default=False,
        help="Initialize a git repository in the workspace",
    )

    # ── doctor ────────────────────────────────────────────────────────
    doctor = sub.add_parser("doctor", help="Validate service compatibility")
    doctor.add_argument("--service", type=Path, default=Path.cwd(), help="Service root path")
    doctor.add_argument("--json", action="store_true", help="Print doctor report as JSON")

    # ── audit ─────────────────────────────────────────────────────────
    audit = sub.add_parser("audit", help="Audit weak or insecure service defaults")
    audit.add_argument(
        "--service",
        type=Path,
        default=None,
        help="Service path (default: workspace root or cwd)",
    )
    audit.add_argument("--json", action="store_true", help="Print audit report as JSON")

    # ── completion ────────────────────────────────────────────────────
    completion = sub.add_parser("completion", help="Shell completion helpers")
    completion_sub = completion.add_subparsers(dest="completion_shell", required=True)
    completion_sub.add_parser("bash", help="Print bash completion script")
    completion_sub.add_parser("install", help="Install bash completion to ~/.local/share")
    completion_sub.add_parser("uninstall", help="Remove installed bash completion")

    return parser


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def main() -> int:
    # Shorthand: `csrd compose <path>` => `csrd compose apply --output <path>`
    raw_argv = sys.argv[1:]
    if len(raw_argv) >= 2 and raw_argv[0] == "compose":
        second = raw_argv[1]
        if second not in {"validate", "plan", "apply", "-h", "--help"} and not second.startswith(
            "-"
        ):
            shorthand_dir = Path(second).resolve()
            has_spec = (shorthand_dir / "csrd-compose.yaml").is_file() or (
                shorthand_dir / "csrd-compose.yml"
            ).is_file()
            if not has_spec:
                print(f"ERROR: Compose shorthand requires csrd-compose.yaml in: {shorthand_dir}")
                print(
                    "Hint: create a spec first (csrd generate workspace --name <name>) "
                    "or use explicit apply: csrd compose apply --output <path>"
                )
                return 1
            sys.argv = [sys.argv[0], "compose", "apply", "--output", second, *raw_argv[2:]]

    parser = _build_parser()

    # Hidden --_complete for dynamic tab completion (called by the bash shim)
    if raw_argv and raw_argv[0] == "--_complete":
        return _handle_complete(parser, raw_argv[1:])

    args = parser.parse_args()

    # ── generate ──────────────────────────────────────────────────────
    if args.command == "generate":
        return run_generate_menu(
            target=getattr(args, "target", None),
            name=getattr(args, "generate_name", None),
            git_init=getattr(args, "git_init", False),
            features=getattr(args, "features", None),
            port=getattr(args, "port", None),
            infra_type=getattr(args, "infra_type", None),
            service_name=getattr(args, "service_name", None),
            new_name=getattr(args, "new_name", None),
            version_date=getattr(args, "version_date", None),
        )

    # ── compose ───────────────────────────────────────────────────────
    if args.command == "compose":
        compose_cmd = getattr(args, "compose_command", None)
        if compose_cmd is None:
            parser.print_help()
            return 0

        output_dir = Path(args.output).resolve()
        try:
            if compose_cmd == "apply":
                generated = compose_apply(output_dir, git_init=getattr(args, "git_init", False))
                print(f"Rendered compose workspace at: {generated}")
                return 0

            if compose_cmd == "validate":
                spec = compose_validate(output_dir)
                if args.json:
                    print(json.dumps(spec.model_dump(mode="python"), indent=2, sort_keys=True))
                else:
                    print(f"Compose spec valid: {output_dir / 'csrd-compose.yaml'}")
                return 0

            if compose_cmd == "plan":
                spec = compose_validate(output_dir)
                payload = {
                    "workspace": spec.workspace.name,
                    "version": spec.version,
                    "services": len(spec.services),
                    "infra": len(spec.infra),
                    "presets": [p.name for p in spec.presets],
                    "overrides_keys": sorted(spec.overrides.keys()),
                }
                if args.json:
                    print(json.dumps(payload, indent=2, sort_keys=True))
                else:
                    print("Compose plan")
                    print(f"- workspace: {payload['workspace']}")
                    print(f"- version: {payload['version']}")
                    print(f"- services: {payload['services']}")
                    print(f"- infra: {payload['infra']}")
                    presets = payload["presets"]
                    overrides_keys = payload["overrides_keys"]
                    assert isinstance(presets, list)
                    assert isinstance(overrides_keys, list)
                    print(f"- presets: {', '.join(presets) if presets else '<none>'}")
                    print(
                        f"- overrides: {', '.join(overrides_keys) if overrides_keys else '<none>'}"
                    )
                return 0
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1

    # ── completion ────────────────────────────────────────────────────
    # ── doctor ────────────────────────────────────────────────────────
    if args.command == "doctor":
        service_path = Path(getattr(args, "service", Path.cwd())).resolve()
        report = run_doctor(service_path)
        if getattr(args, "json", False):
            from dataclasses import asdict

            print(json.dumps(asdict(report), indent=2, sort_keys=True))
        else:
            if report.ok:
                print("Doctor check passed.")
            else:
                print("Doctor check failed.")
            for err in report.errors:
                print(f"ERROR: {err}")
            for warning in report.warnings:
                print(f"WARN: {warning}")
        return 0 if report.ok else 1

    # ── audit ─────────────────────────────────────────────────────────
    if args.command == "audit":
        audit_path = getattr(args, "service", None)
        target = audit_path.resolve() if audit_path is not None else Path.cwd().resolve()
        audit_report = run_audit(target)
        payload = audit_report.to_payload()
        if getattr(args, "json", False):
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            if audit_report.ok:
                print("Audit passed (no high-severity findings).")
            else:
                print("Audit failed (high-severity findings detected).")
            for finding in audit_report.findings:
                print(
                    f"{finding.severity.upper()}: [{finding.rule}] "
                    f"{finding.file} :: {finding.message}"
                )
                print(f"  evidence: {finding.evidence}")
                print(f"  fix: {finding.remediation}")
        return 0 if audit_report.ok else 1

    if args.command == "completion":
        shell = getattr(args, "completion_shell", None)
        if shell == "bash":
            print(_render_bash_completion(), end="")
            return 0
        if shell == "install":
            return _install_completion()
        if shell == "uninstall":
            return _uninstall_completion()

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
