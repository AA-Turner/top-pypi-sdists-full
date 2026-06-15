"""CLI entry point — command dispatch and output routing."""
from __future__ import annotations

import importlib
import json
import sys
import time

from kanban_framework.cli.main_renderers import (  # noqa: F401
    _format_table,
    _render_create,
    _render_dashboard,
    _render_help,
    _render_init,
    _render_json_fallback,
    _render_knowledge,
    _render_nlp,
    _render_score,
    _render_show,
    _render_status,
    _render_summary,
    _render_time,
    _render_update,
)
from kanban_framework.cli.main_commands import (  # noqa: F401
    _cmd_check_env,
    _cmd_stats,
    _cmd_sync_agents,
    _cmd_update,
    _is_pre_release,
)
from kanban_framework.cli.main_version import get_version as _get_version  # noqa: F401

_CMD_MAP: dict[str, tuple[str, str]] = {
    "check-env":  ("kanban_framework.cli.main", "_cmd_check_env"),
    "benchmark":  ("kanban_framework.cli.benchmark", "dispatch"),
    "init":       ("kanban_framework.cli.task", "cmd_init"),
    "scan":       ("kanban_framework.cli.task", "cmd_scan"),
    "create":     ("kanban_framework.cli.task", "cmd_create"),
    "task":       ("kanban_framework.cli.task", "cmd_task"),
    "status":     ("kanban_framework.cli.task", "cmd_status"),
    "show":       ("kanban_framework.cli.task", "cmd_show"),
    "clean":      ("kanban_framework.cli.task", "cmd_clean"),
    "promote":    ("kanban_framework.cli.task", "cmd_promote"),
    "run":        ("kanban_framework.cli.run", "cmd_run"),
    "decide":     ("kanban_framework.cli.run", "cmd_decide"),
    "guard":      ("kanban_framework.cli.guard_cmd", "cmd_guard"),
    "workflow":   ("kanban_framework.cli.workflow_cmd", "cmd_workflow"),
    "worktree":   ("kanban_framework.cli.run", "cmd_worktree"),
    "nlp":        ("kanban_framework.cli.run", "cmd_nlp"),
    "recover":    ("kanban_framework.cli.run", "cmd_recover"),
    "rollback":   ("kanban_framework.cli.run", "cmd_rollback"),
    "resume":     ("kanban_framework.cli.run", "cmd_resume"),
    "subtask":    ("kanban_framework.cli.subtask", "dispatch"),
    "score":      ("kanban_framework.cli.query", "cmd_score"),
    "summary":    ("kanban_framework.cli.query", "cmd_summary"),
    "progress":   ("kanban_framework.cli.query", "cmd_progress"),
    "time":       ("kanban_framework.cli.query", "cmd_time"),
    "dashboard":  ("kanban_framework.cli.query", "cmd_dashboard"),
    "inbox":      ("kanban_framework.cli.inbox", "dispatch"),
    "knowledge":  ("kanban_framework.cli.knowledge", "dispatch"),
    "feedback":   ("kanban_framework.cli.inbox", "cmd_feedback"),
    "version":    ("kanban_framework.cli.version", "dispatch"),
    "plan":           ("kanban_framework.cli.plan", "dispatch"),
    "evolve-skills":  ("kanban_framework.cli.skills", "dispatch"),
    "framework":      ("kanban_framework.cli.framework", "dispatch"),
    "evaluator":      ("kanban_framework.cli.evaluator", "dispatch"),
    "help":           ("kanban_framework.cli.main", "_cmd_help"),
    "sync-agents":    ("kanban_framework.cli.main", "_cmd_sync_agents"),
    "update":         ("kanban_framework.cli.main", "_cmd_update"),
    "codebase":       ("kanban_framework.cli.codebase", "dispatch"),
    "stats":          ("kanban_framework.cli.main", "_cmd_stats"),
    "hook":           ("kanban_framework.cli.hook", "cmd_hook"),
    "install-codeburn": ("kanban_framework.cli.task", "cmd_install_codeburn"),
}

_USE_JSON = True
_start_time = time.time()

# Commands that prefer human-readable text output by default.
# These are primarily interactive / visual / setup commands where JSON
# provides no value to either human or agent.
_TEXT_DEFAULT_COMMANDS: set[str] = {"dashboard", "init", "help", "hook"}


def _ensure_utf8_stdout() -> None:
    """Force UTF-8 on stdout/stderr — Windows default is cp936/gbk.

    Without this, Chinese characters in JSON output show as ??? on
    Windows cmd/Git Bash (#657). The reconfigure API is available
    on Python 3.7+ TextIOWrapper.
    """
    import os
    # Also set PYTHONIOENCODING for subprocesses (e.g. pip, sync_skill.py)
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
            elif hasattr(stream, "buffer"):
                # Fallback for non-TextIOWrapper streams
                import io
                setattr(sys, "stdout" if stream is sys.stdout else "stderr",
                        io.TextIOWrapper(stream.buffer, encoding="utf-8",
                                         errors="replace", line_buffering=True))
        except Exception:
            pass


_ensure_utf8_stdout()


def _setup_logging() -> None:
    """Configure kanban logger to write to .kanban/log/kanban.log."""
    try:
        from kanban_framework.infra.filesystem import Filesystem
        root = Filesystem.find_project_root()
        log_dir = root / ".kanban" / "log"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "kanban.log"

        import logging
        logger = logging.getLogger("kanban")
        logger.setLevel(logging.DEBUG)

        # Avoid duplicate handlers on repeated calls
        if not logger.handlers:
            fh = logging.FileHandler(str(log_file), encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            fmt = logging.Formatter("%(asctime)s %(levelname)-5s %(name)s %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")
            fh.setFormatter(fmt)
            logger.addHandler(fh)
    except Exception:
        pass


def main() -> None:
    global _USE_JSON, _start_time
    import warnings
    warnings.filterwarnings("ignore", message=".*urllib3.*")
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="requests")
    _start_time = time.time()
    args = sys.argv[1:]

    explicit_json = "--json" in args or "-o" in args
    explicit_text = "--text" in args

    if explicit_text:
        _USE_JSON = False
        args = [a for a in args if a != "--text"]
    # --json flag: force JSON mode (overrides text-default commands)
    args = [a for a in args if a not in ("--json", "-o")]

    # Commands that prefer human-readable output default to text mode
    # unless --json is explicitly passed.
    cmd = args[0] if args else ""
    if not explicit_json and not explicit_text and cmd in _TEXT_DEFAULT_COMMANDS:
        _USE_JSON = False

    _setup_logging()

    if not args or args[0] in ("--help", "-h", "help"):
        if not explicit_json:
            _render_help()
        else:
            _output({"success": True, "data": _cmd_help(args[1:] if len(args) > 1 else [])})
        return

    if args[0] in ("--version", "-V"):
        _output_version()
        return

    cmd = args[0]

    # Intercept --help/-h in subcommand args to prevent dirty data (#594).
    # Without this, `kanban knowledge add --help` would create a blank entry
    # because the handler treats "--help" as a positional content argument.
    #
    # BUT: commands with their own dispatch() (benchmark, knowledge, etc.)
    # handle --help per-subcommand and should NOT be intercepted here (#636).
    _DISPATCH_COMMANDS = frozenset({
        "benchmark", "knowledge", "version", "plan", "evolve-skills",
        "framework", "evaluator", "inbox", "subtask", "codebase",
    })
    if ("--help" in args or "-h" in args) and cmd not in _DISPATCH_COMMANDS:
        _output({"success": True, "data": {
            "help": True,
            "command": cmd,
            "message": (
                f"Use '/kanban help' for the full command list, or read the reference docs.\n"
                f"Common {cmd} subcommands: kanban {cmd} --help"
            ),
        }})
        return

    entry = _CMD_MAP.get(cmd)
    if entry is None:
        _output({"success": False, "error": f"unknown command: {cmd}", "code": "UNKNOWN_COMMAND"})
        sys.exit(1)

    import logging
    _log = logging.getLogger("kanban")
    _log.info("command: %s %s", cmd, " ".join(args[1:]))

    mod_name, fn_name = entry
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, fn_name)
    try:
        result = fn(args[1:])
        # Convention: handlers return `{"error": "..."}` for expected failures
        # (bad input, missing files, validation errors). These must surface as
        # `success: False` in the JSON envelope — not be wrapped as success.
        # Without this, `kanban create --mode bogus` returned success=True
        # even though the handler explicitly rejected the mode (#644).
        is_error = isinstance(result, dict) and bool(result.get("error"))
        _log.info("command %s completed: success=%s", cmd, not is_error)
        if _USE_JSON:
            if is_error:
                _output({
                    "success": False,
                    "error": result["error"],
                    "code": result.get("code", "HandlerError"),
                    "data": result,  # preserve extra fields like available_modes
                })
            else:
                _output({"success": True, "data": result})
        else:
            _render(cmd, result)
    except Exception as e:
        import traceback
        tb_text = traceback.format_exc()
        _log.exception("command %s failed: %s", cmd, e)
        # Always echo full traceback to stderr so terminal users can debug —
        # JSON users get it under the "traceback" field below.
        sys.stderr.write(tb_text)
        log_file_path = ""
        try:
            from kanban_framework.infra.filesystem import Filesystem as _Fs
            log_file_path = str(_Fs.find_project_root() / ".kanban" / "log" / "kanban.log")
        except Exception:
            pass
        _output({
            "success": False,
            "error": str(e),
            "code": type(e).__name__,
            "traceback": tb_text,
            "command": f"{cmd} {' '.join(args[1:])}".strip(),
            "log_file": log_file_path,
        })


def _render(cmd: str, data: dict) -> None:
    global _start_time
    renderers = {
        "status": _render_status,
        "show": _render_show,
        "create": _render_create,
        "init": _render_init,
        "score": _render_score,
        "summary": _render_summary,
        "time": _render_time,
        "nlp": _render_nlp,
        "dashboard": _render_dashboard,
        "update": _render_update,
        "knowledge": _render_knowledge,
    }
    renderer = renderers.get(cmd)
    if renderer:
        renderer(data)
    else:
        _render_json_fallback(cmd, data)
    elapsed = (time.time() - _start_time) * 1000
    print(f"\n  [{elapsed:.0f}ms]")


def _output(data: dict) -> None:
    global _start_time
    elapsed = (time.time() - _start_time) * 1000
    data["elapsed_ms"] = round(elapsed, 1)
    print(json.dumps(data, ensure_ascii=False))


def _cmd_help(args: list[str]) -> dict:
    from kanban_framework.cli.main_commands import _cmd_help as _help
    return _help(args, _CMD_MAP)


def _output_version() -> None:
    ver = _get_version()
    if _USE_JSON:
        _output({"success": True, "data": {"version": ver}})
    else:
        print(f"kanban {ver}")


if __name__ == "__main__":
    main()
