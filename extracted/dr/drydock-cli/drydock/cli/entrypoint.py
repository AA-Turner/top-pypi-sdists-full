from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

from rich import print as rprint

from drydock import __version__
from drydock.core.agents.models import BuiltinAgentName
from drydock.core.config.harness_files import init_harness_files_manager
from drydock.core.trusted_folders import has_trustable_content, trusted_folders_manager
from drydock.setup.trusted_folders.trust_folder_dialog import (
    TrustDialogQuitException,
    ask_trust_folder,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Drydock interactive CLI")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "initial_prompt",
        nargs="?",
        metavar="PROMPT",
        help="Initial prompt to start the interactive session with.",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        nargs="?",
        const="",
        metavar="TEXT",
        help="Run in programmatic mode: send prompt, auto-approve all tools, "
        "output response, and exit.",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        metavar="N",
        help="Maximum number of assistant turns "
        "(only applies in programmatic mode with -p).",
    )
    parser.add_argument(
        "--max-price",
        type=float,
        metavar="DOLLARS",
        help="Maximum cost in dollars (only applies in programmatic mode with -p). "
        "Session will be interrupted if cost exceeds this limit.",
    )
    parser.add_argument(
        "--enabled-tools",
        action="append",
        metavar="TOOL",
        help="Enable specific tools. In programmatic mode (-p), this disables "
        "all other tools. "
        "Can use exact names, glob patterns (e.g., 'bash*'), or "
        "regex with 're:' prefix. Can be specified multiple times.",
    )
    parser.add_argument(
        "--output",
        type=str,
        choices=["text", "json", "streaming"],
        default="text",
        help="Output format for programmatic mode (-p): 'text' "
        "for human-readable (default), 'json' for all messages at end, "
        "'streaming' for newline-delimited JSON per message.",
    )
    parser.add_argument(
        "--json-schema",
        metavar="FILE",
        help="Path to JSON Schema file. Constrains the final output to match the schema.",
    )
    parser.add_argument(
        "--agent",
        metavar="NAME",
        default=BuiltinAgentName.DEFAULT,
        help="Agent to use (builtin: default, plan, accept-edits, auto-approve, "
        "or custom from ~/.drydock/agents/NAME.toml)",
    )
    parser.add_argument("--setup", action="store_true", help="Setup API key and exit")
    parser.add_argument(
        "--fix-windows-path",
        action="store_true",
        help="Add the per-user Python Scripts directory to user PATH on Windows "
        "(no-op on Linux/macOS). Useful when `pip install --user drydock-cli` "
        "warned that drydock.exe is not on PATH.",
    )
    parser.add_argument(
        "--doctor",
        action="store_true",
        help="Check ~/.drydock/config.toml for drift vs. package defaults and exit",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="With --doctor: rewrite ~/.drydock/config.toml to union missing "
        "defaults (writes .bak backup first). No effect without --doctor.",
    )
    parser.add_argument(
        "--workdir",
        type=Path,
        metavar="DIR",
        help="Change to this directory before running",
    )

    parser.add_argument(
        "--dangerously-skip-permissions",
        action="store_true",
        help="Skip all tool permission checks. Equivalent to --agent auto-approve. "
        "Use with caution — tools will execute without confirmation.",
    )
    parser.add_argument(
        "-k", "--insecure",
        action="store_true",
        help="Disable SSL certificate verification for web searches and API calls. "
        "Useful behind corporate proxies with self-signed certificates.",
    )
    parser.add_argument(
        "--consultant",
        metavar="MODEL",
        help="Enable consultant mode: when the agent is uncertain or stuck in a loop, "
        "it can call a more capable model (e.g., 'gemini-2.5-pro') for single-turn advice. "
        "The consultant is NOT used for tool calls, only reasoning.",
    )

    parser.add_argument(
        "--local",
        metavar="URL",
        nargs="?",
        const="http://localhost:8000/v1",
        help="Use a local LLM server (default: http://localhost:8000/v1). "
        "Sets up a 'local' provider and model automatically. "
        "Example: drydock --local http://localhost:11434/v1",
    )

    # Feature flag for teleport, not exposed to the user yet
    parser.add_argument("--teleport", action="store_true", help=argparse.SUPPRESS)

    continuation_group = parser.add_mutually_exclusive_group()
    continuation_group.add_argument(
        "-c",
        "--continue",
        action="store_true",
        dest="continue_session",
        help="Continue from the most recent saved session",
    )
    continuation_group.add_argument(
        "--resume",
        metavar="SESSION_ID",
        help="Resume a specific session by its ID (supports partial matching)",
    )
    return parser.parse_args()


def check_and_resolve_trusted_folder() -> None:
    try:
        cwd = Path.cwd()
    except FileNotFoundError:
        rprint(
            "[red]Error: Current working directory no longer exists.[/]\n"
            "[yellow]The directory you started drydock from has been deleted. "
            "Please change to an existing directory and try again, "
            "or use --workdir to specify a working directory.[/]"
        )
        sys.exit(1)

    if not has_trustable_content(cwd) or cwd.resolve() == Path.home().resolve():
        return

    is_folder_trusted = trusted_folders_manager.is_trusted(cwd)

    if is_folder_trusted is not None:
        return

    try:
        is_folder_trusted = ask_trust_folder(cwd)
    except (KeyboardInterrupt, EOFError, TrustDialogQuitException):
        sys.exit(0)
    except Exception as e:
        rprint(f"[yellow]Error showing trust dialog: {e}[/]")
        return

    if is_folder_trusted is True:
        trusted_folders_manager.add_trusted(cwd)
    elif is_folder_trusted is False:
        trusted_folders_manager.add_untrusted(cwd)


def _warn_on_path_shadow() -> None:
    """If a different drydock install — either on PATH or in a
    well-known install dir — is newer than the one we're running,
    print a one-line warning.

    Operator observed 2026-06-08: ~/.local/bin/drydock was 2.9.46
    (months old) while the auto-released install in
    ~/miniforge3/envs/drydock/bin was 2.10.4. The fresh install
    wasn't even on PATH (the conda env wasn't activated), so a
    strict $PATH walk wouldn't catch this. We also scan a few
    conventional install locations.

    Opt-out: DRYDOCK_NO_SHADOW_WARN=1.
    """
    if os.environ.get("DRYDOCK_NO_SHADOW_WARN", "").strip().lower() in (
        "1", "true", "yes",
    ):
        return
    if __version__ == "dev":
        # Running from source — every install would be "newer" by version
        # number but the dev tree IS what's intended. Skip.
        return
    try:
        import glob
        import shutil
        from packaging.version import Version
        running_bin = shutil.which("drydock")
        if not running_bin:
            return
        running_real = os.path.realpath(running_bin)

        # 1) Anything on $PATH named drydock.
        candidates: list[str] = []
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            if path_dir and os.path.isdir(path_dir):
                p = os.path.join(path_dir, "drydock")
                if os.path.isfile(p) and os.access(p, os.X_OK):
                    candidates.append(p)
        # 2) Conventional install dirs (uv tool, conda envs) — these
        # often contain drydock but aren't on PATH unless activated.
        home = os.path.expanduser("~")
        for pattern in (
            os.path.join(home, ".local", "bin", "drydock"),
            os.path.join(home, "miniforge3", "envs", "*", "bin", "drydock"),
            os.path.join(home, "miniconda3", "envs", "*", "bin", "drydock"),
            os.path.join(home, "anaconda3", "envs", "*", "bin", "drydock"),
            os.path.join(home, ".local", "share", "uv", "tools",
                         "drydock-cli", "bin", "drydock"),
            "/usr/local/bin/drydock",
        ):
            for p in glob.glob(pattern):
                if os.path.isfile(p) and os.access(p, os.X_OK):
                    candidates.append(p)

        seen: set[str] = {running_real}
        for cand in candidates:
            cand_real = os.path.realpath(cand)
            if cand_real in seen:
                continue
            seen.add(cand_real)
            try:
                other_ver = _read_drydock_version_for(cand_real)
            except Exception:
                continue
            if not other_ver:
                continue
            if Version(other_ver) > Version(__version__):
                rprint(
                    f"[yellow]Note: drydock {other_ver} is installed at "
                    f"{cand}, but this session is running {__version__} "
                    f"from {running_real}. To use the newer one, run "
                    f"{cand} directly or put its bin dir first on PATH. "
                    f"Silence: DRYDOCK_NO_SHADOW_WARN=1.[/]"
                )
                return  # one warning is enough
    except Exception:
        # Never block startup on a diagnostic.
        return


def _read_drydock_version_for(executable_path: str) -> str | None:
    """Given a drydock executable path, return the installed version
    by reading dist-info metadata. Tries two env layouts: the binary's
    sibling (env/bin/drydock + env/lib/.../site-packages — conda/venv
    style) and the binary's shebang-pointed python (uv tool installs
    that put the script in ~/.local/bin but the env at
    ~/.local/share/uv/tools/...). No subprocess fork."""
    candidate_envs: list[str] = []
    # Layout A: <env>/bin/drydock — env root is one level up.
    bin_dir = os.path.dirname(executable_path)
    candidate_envs.append(os.path.dirname(bin_dir))
    # Layout B: read the shebang from the executable and resolve the
    # python interpreter path to its env root.
    try:
        with open(executable_path, "rb") as f:
            first = f.readline()
        if first.startswith(b"#!"):
            shebang = first[2:].strip().decode("utf-8", errors="replace")
            # shebang format is usually "/path/to/env/bin/python" possibly
            # followed by args; take the executable token.
            py = shebang.split()[0] if shebang.split() else ""
            if py:
                # Use the literal shebang path, NOT realpath — many tool
                # installers (uv) ship a venv where bin/python is a
                # symlink to system python. realpath would jump us out
                # of the venv to /usr, losing the dist-info location.
                py_bin_dir = os.path.dirname(py)
                candidate_envs.append(os.path.dirname(py_bin_dir))
    except OSError:
        pass

    for env_root in candidate_envs:
        lib_dir = os.path.join(env_root, "lib")
        if not os.path.isdir(lib_dir):
            continue
        for py_dir in sorted(os.listdir(lib_dir), reverse=True):
            candidate_sp = os.path.join(lib_dir, py_dir, "site-packages")
            if not os.path.isdir(candidate_sp):
                continue
            try:
                for entry in os.listdir(candidate_sp):
                    if entry.startswith("drydock_cli-") and entry.endswith(".dist-info"):
                        meta = os.path.join(candidate_sp, entry, "METADATA")
                        if not os.path.isfile(meta):
                            continue
                        with open(meta, encoding="utf-8") as f:
                            for line in f:
                                if line.startswith("Version:"):
                                    return line.split(":", 1)[1].strip()
            except OSError:
                continue
    return None


def main() -> None:
    args = parse_arguments()

    if getattr(args, "fix_windows_path", False):
        from drydock.cli.fix_windows_path import fix_windows_path
        sys.exit(fix_windows_path())

    if getattr(args, "doctor", False):
        from drydock.core.config.doctor import run_doctor
        init_harness_files_manager("user", "project")
        sys.exit(run_doctor(apply=bool(getattr(args, "fix", False))))

    # PATH-shadow check (after early-exit args, before interactive setup).
    _warn_on_path_shadow()

    if args.workdir:
        workdir = args.workdir.expanduser().resolve()
        if not workdir.is_dir():
            rprint(
                f"[red]Error: --workdir does not exist or is not a directory: {workdir}[/]"
            )
            sys.exit(1)
        os.chdir(workdir)

    # --dangerously-skip-permissions → force auto-approve agent
    if args.dangerously_skip_permissions:
        args.agent = BuiltinAgentName.AUTO_APPROVE

    # --insecure → disable SSL verification globally
    if args.insecure:
        os.environ["DRYDOCK_INSECURE"] = "1"
        os.environ["CURL_CA_BUNDLE"] = ""
        os.environ["REQUESTS_CA_BUNDLE"] = ""
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    # --consultant → store for agent loop to use
    if args.consultant:
        os.environ["DRYDOCK_CONSULTANT_MODEL"] = args.consultant

    # --local → set up local LLM provider without editing config
    if getattr(args, "local", None):
        os.environ["DRYDOCK_LOCAL_URL"] = args.local
        # Respect an explicit env-var override (used by harness/CI).
        # Otherwise probe /v1/models — retry once with a longer timeout
        # because containerized tbench trials saw the 5s window expire on
        # cold-start, falling back to model="local" which loses ALL
        # Gemma 4 optimizations (slim prompt, tool disables, non-streaming).
        if os.environ.get("DRYDOCK_LOCAL_MODEL", "").strip():
            rprint(
                f"[green]Using local model: "
                f"{os.environ['DRYDOCK_LOCAL_MODEL']} at {args.local} "
                f"(via DRYDOCK_LOCAL_MODEL env)[/]"
            )
        else:
            model_name = None
            try:
                import httpx
                for attempt in (1, 2):
                    try:
                        resp = httpx.get(f"{args.local}/models", timeout=15)
                        if resp.status_code == 200:
                            models = resp.json().get("data", [])
                            if models and models[0].get("id"):
                                model_name = models[0]["id"]
                                break
                    except Exception:
                        if attempt == 2:
                            raise
            except Exception:
                pass
            if model_name:
                os.environ["DRYDOCK_LOCAL_MODEL"] = model_name
                rprint(f"[green]Using local model: {model_name} at {args.local}[/]")
            else:
                # Detection failed. Default to "gemma4" — drydock is
                # optimized for Gemma 4 + llama.cpp per README, so this
                # is the right fallback in the overwhelming common case.
                # Loud warning lets the user override if they're running
                # something else.
                os.environ["DRYDOCK_LOCAL_MODEL"] = "gemma4"
                rprint(
                    f"[yellow]Couldn't detect model name at {args.local}; "
                    f"defaulting to model=gemma4. Override with "
                    f"DRYDOCK_LOCAL_MODEL=<name> if the server runs a "
                    f"different model.[/]"
                )

    is_interactive = args.prompt is None
    if is_interactive:
        check_and_resolve_trusted_folder()
    init_harness_files_manager("user", "project")

    from drydock.cli.cli import run_cli

    run_cli(args)


if __name__ == "__main__":
    main()
