"""apply .probe.config to tool calls: classify in this session's folders, refuse or scrub `off` paths."""

from __future__ import annotations
import time
from pathlib import Path
from typing import Any
from probe.shared.command_rules import command_rules as precheck


def _classify(deps: Deps, command: str, cwd: Path, *, piped_input: bool = False) -> Any:
    """`shell.classify` with this session's folders, in `cwd`. With the `bash`
    tool set the Probe skills folder is read-only open to the read programs (the
    writer's and the audit's; it was the `read` tool's), and the reader reads
    nothing outside the working folders (as its `read` tool never did)."""
    from probe.daemon import shell as sh
    from probe.daemon.agent import toolset

    read_dirs: list[Path] = []
    if toolset.bash_only() and not deps.reader:
        from probe.daemon.worker.bite.bite import skills_root

        root = skills_root()
        read_dirs = [root] if root is not None else []
    return sh.classify(command, workdirs=deps.workdirs, home=deps.home, cwd=cwd, protected=deps.protected,
                       write_dirs=deps.write_dirs, piped_input=piped_input, hidden=_off_check(deps, cwd),
                       off_inside=_off_inside_check(deps), read_dirs=read_dirs, inside_only=deps.reader)


def _config_checker(deps: Deps, cwd: Path) -> Any:
    """A `probe_config.Checker` as this session sees the `.probe.config` files
    (the ones above its launch folder the researcher set aside do not count)."""
    from probe.sdk import probe_config as pc
    from probe.sdk import session_marker

    _start, skip = pc.session_view(session_marker.sessions_dir(), deps.session_id)
    # `hash` is `off` to the daemon (C9).
    return pc.Checker(cwd=str(cwd), skip=skip, legacy=True, daemon=True)


def _off_check(deps: Deps, cwd: Path) -> Any:
    """For the shell's checks: is a path `off` (Probe never reads it)? When the
    check cannot be built, every path counts as `off` (fail closed)."""
    try:
        checker = _config_checker(deps, cwd)
    except Exception:  # noqa: BLE001
        return lambda path: True
    return lambda path: checker.check(path).hidden


#: `probe_config.off_inside` answers, per (session, folder): (when, answer).
_OFF_INSIDE: dict[tuple[str, str], tuple[float, bool]] = {}
_OFF_INSIDE_TTL_S = 5.0


def _off_inside_check(deps: Deps) -> Any:
    """For the shell's checks: does a folder hold an `off` path somewhere below?
    (A command reading the whole tree is then refused.) Reused for 30 s."""
    from probe.sdk import probe_config as pc
    from probe.sdk import session_marker

    def check(folder: str) -> bool:
        key = (deps.session_id, folder)
        now = time.monotonic()
        hit = _OFF_INSIDE.get(key)
        if hit is not None and now - hit[0] < _OFF_INSIDE_TTL_S:
            return hit[1]
        try:
            _start, skip = pc.session_view(session_marker.sessions_dir(), deps.session_id)
            answer = pc.off_inside(folder, skip=skip, legacy=True)
        except Exception:  # noqa: BLE001
            answer = True
        if len(_OFF_INSIDE) > 4096:
            _OFF_INSIDE.clear()
        _OFF_INSIDE[key] = (now, answer)
        return answer

    return check


def _off_scrubbed(deps: Deps, text: str, cwd: Path) -> str:
    """A shell output minus the lines that show an `off` file (a backstop: a
    command reading a tree that holds one is refused before it runs)."""
    try:
        from probe.shared.harness import session_filter as ex

        return ex.scrub_listing(text, _config_checker(deps, cwd))[0]
    except Exception:  # noqa: BLE001 - fail closed
        return "[output removed: it could not be checked against .probe.config]"


def _config_block(deps: Deps, parsed: precheck.Parsed, here: Path) -> precheck.Block | None:
    """A command naming a path a `.probe.config` keeps out of the record, as this
    session sees the files (`precheck.check_config`). A check that fails refuses
    the command (fail closed)."""
    try:
        from probe.sdk import probe_config as pc
        from probe.sdk import session_marker

        _start, skip = pc.session_view(session_marker.sessions_dir(), deps.session_id)
        checker = pc.Checker(cwd=str(here), skip=skip, legacy=True, daemon=True)
        return precheck.check_config(parsed, cwd=here, checker=checker, document=_document_path(deps, parsed))
    except Exception as exc:  # noqa: BLE001
        return precheck.Block(precheck.new_block_id(),
                              f"the .probe.config check failed ({type(exc).__name__}), so it was not run",
                              "probe_config", argv=parsed.argv, overridable=False)
from probe.daemon.agent.tools.probe_cli.probe_cli import _document_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
