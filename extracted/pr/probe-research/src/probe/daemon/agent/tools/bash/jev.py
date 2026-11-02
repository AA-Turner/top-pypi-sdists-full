"""ask Jev about a held shell command and bind its yes to the programs the command runs."""

from __future__ import annotations
import os
import re
from pathlib import Path
from typing import Any

from probe.shared.mailbox import approvals as appr


#: WHAT JEV MAY JUDGE: `python -c CODE`, alone or after plain `cd DIR`s, and
#: nothing else. Four review rounds of a list of "read-only" programs each found
#: a new way a listed program writes, runs a helper through PATH or reads names
#: its words don't show (`file -z` runs a decompressor, `diff -l` runs `pr`,
#: `gzip -Sc` deletes, `unzip --p` cancels `-p`, `xxd a b` writes, `pip show
#: --log` writes, `sha256sum -c` reads a list, `printf %n` sets PATH, `ps e`
#: prints other environments): the safe list's own per-program rules are where
#: those belong, and reads now run there anywhere. Inline Python is the gray
#: zone left: its whole code is in the command's text, which is what Jev reads.

#: The only Python options a judged `python -c` may carry: none turns the
#: daemon shell's PYTHONSAFEPATH or PYTHONDONTWRITEBYTECODE off (`-E`, `-I`
#: and `-X` would; `-m` and a file run code its words don't show).
_PYTHON_FLAGS = frozenset({"-P", "-B", "-s", "-S", "-u", "-q", "-O", "-OO", "-b", "-bb"})
_PYTHON_NAME = re.compile(r"python(3(\.\d+)?)?")
_PYTHON_REAL = re.compile(r"python(\d+)\.(\d+)")


def _parts(command: str) -> list[list[str]] | None:
    """The simple commands of `command` as the checker's own strict reading
    splits them (`shell._split`), their words unquoted; None when that reading
    refuses it: `$`, backticks, globs and braces expand to what the text
    doesn't show (`X=curl; $X`, `head -c 20 *`). Not the lenient reading the
    scans use: it takes a quoted `'>'` for a redirect and merges the command
    after it (`echo '>'; uv run x.py`) into echo's words."""
    from probe.daemon import shell as sh

    try:
        parts = sh._split(sh._tokenize(command))
    except sh._Refuse:
        return None
    if any(part.redirects for part in parts):
        return None  # a redirect writes or reads what the words don't name; a heredoc runs bash on its body
    return [[w.value for w in part.words] for part in parts]


def _never_judged(deps: Deps, command: str, cwd: Path) -> bool:
    """A command Jev is never asked about: anything but `python -c CODE` on a
    Python 3.11+ (`_python_judgeable`: its options from `_PYTHON_FLAGS`, named
    bare, found on the shell's PATH outside the working folders, no `X=1`
    before it), alone or after plain `cd DIR`s, read by the checker's strict
    reading (`_parts`: no `$`, backticks, globs or braces). And never while the
    shell's PATH holds a folder of the session (a repo's `.venv/bin`)."""
    parts = _parts(command)
    if not parts or _path_reaches_the_session(deps, cwd):
        return True
    is_judged = False
    for words in parts:
        if not words:
            continue
        name = words[0]
        if name == "cd" and len(words) == 2 and not words[1].startswith("-"):
            continue
        if not _PYTHON_NAME.fullmatch(name) or _program(deps, name, cwd) is None:
            return True
        if not _python_judgeable(deps, name, words[1:], cwd):
            return True
        is_judged = True
    return not is_judged


def _roots(deps: Deps, cwd: Path) -> list[str]:
    return [os.path.realpath(r) for r in (*deps.workdirs, cwd)]


def _inside_roots(real: str, roots: list[str]) -> bool:
    return any(real == r or real.startswith(r.rstrip(os.sep) + os.sep) for r in roots)


def _path_reaches_the_session(deps: Deps, cwd: Path) -> bool:
    """Does the daemon shell's PATH hold a folder inside a working folder or
    the session's folder (a repo's `.venv/bin`, `node_modules/.bin`)?"""
    from probe.daemon import shell as sh

    roots = _roots(deps, cwd)
    return any(entry and _inside_roots(os.path.realpath(entry), roots)
               for entry in sh.minimal_env()["PATH"].split(os.pathsep))


def _program(deps: Deps, name: str, cwd: Path) -> str | None:
    """The real file `name` runs, found on the daemon shell's PATH; None when
    there is none, or it lies inside a working folder or the session's folder
    (a repo's own `cut`). Nothing is run to find it."""
    import shutil

    from probe.daemon import shell as sh

    found = shutil.which(name, path=sh.minimal_env()["PATH"])
    if not found:
        return None
    real = os.path.realpath(found)
    return None if _inside_roots(real, _roots(deps, cwd)) else real


def _python_judgeable(deps: Deps, name: str, args: list[str], cwd: Path) -> bool:
    """`python -c CODE` only: every option before `-c` from `_PYTHON_FLAGS`, and
    the real interpreter a Python 3.11+ (one that honours PYTHONSAFEPATH, which
    `shell.minimal_env` sets), read from its real file's name
    (`/usr/bin/python3` -> `python3.12`). Nothing is run to find out: a probe
    that ran it would run whatever PATH names. A name without a version (a
    pyenv shim) is no.

    RESIDUAL, not closed: Python runs `site`'s startup hooks (a `.pth` file or
    `sitecustomize`/`usercustomize` in a site-packages folder) before the code.
    Planting one is a write, and the daemon makes none unasked; whoever could
    plant one (the coding agent, the researcher) can run code directly."""
    k = 0
    while k < len(args) and args[k] in _PYTHON_FLAGS:
        k += 1
    if k >= len(args) - 1 or args[k] != "-c":
        return False
    real = _program(deps, name, cwd)
    m = _PYTHON_REAL.fullmatch(os.path.basename(real or ""))
    return bool(m) and (int(m.group(1)), int(m.group(2))) >= (3, 11)


def _programs(deps: Deps, command: str, cwd: Path) -> list[tuple] | None:  # None: not bindable
    """What Jev's yes is bound to (G3): each program the command's parts run,
    as its real file and that file's identity (device, inode, size, change
    time). A link pointed elsewhere, a file replaced by rename, or one written
    in place (its change time moves, which no one can set back) while Jev
    answers is a different command."""
    out: list[tuple] = []
    for words in _parts(command) or []:
        if not words or words[0] == "cd":
            continue
        real = _program(deps, words[0], cwd)
        try:
            st = os.stat(real) if real else None
        except OSError:
            st = None
        if st is None:
            return None  # no identity to bind a yes to: never judged
        out.append((real, (st.st_dev, st.st_ino, st.st_size, st.st_ctime_ns)))
    return out


def _judgeable(deps: Deps, command: str, verdict: Any, cwd: Path) -> bool:
    """May Jev be asked about this held command at all? Not when it names a
    credential-shaped file (`Verdict.credential`), a hidden file or folder or a
    whole tree's contents (`Verdict.private`), a policy path, or runs what
    `_never_judged` names."""
    from probe.daemon import shell as sh

    parts = _parts(command)
    names = sh.strict_names(command, workdirs=deps.workdirs, home=deps.home, cwd=cwd, protected=deps.protected,
                            write_dirs=deps.write_dirs)  # the strict reading too: `x '>'; cd ~ && ... .bashrc`
    return not (parts is None or names is None or any(names) or getattr(verdict, "credential", True)
                or getattr(verdict, "private", True) or any(sh._tree_read(words) for words in parts)
                or _names_policy_path(deps, command, cwd) is not None or _never_judged(deps, command, cwd))


async def _jev_approval(deps: Deps, command: str, verdict: Any, cwd: Path, facts: dict, held: dict) -> str | None:
    """Jev's yes to a held shell command (`command_check`), as the logbook's
    reason (`auto-approved: Jev p=0.97`, the lowest answer); None: ask the
    researcher. Never asked about what `_judgeable` keeps from Jev, a command
    that runs a script file (its text is the file's, which never goes to
    TypeSafe), or one the researcher was already asked about (a question waits,
    or they said no). A yes is checked again before it stands (G3): Jev took up
    to 3 s, and a link can be pointed at a key, or a program at another file, in
    that time: so the same real programs, the same verdict, no credential,
    private or policy path, and still no script."""
    from probe.daemon.shell import command_check

    if facts.get("scripts") or not _judgeable(deps, command, verdict, cwd):
        return None
    pol = appr.POLICIES["shell.unsafe_command"]
    if deps.board.find_same(deps.session_id, pol.name, pol.fingerprint(facts), appr.action_digest(held)):
        return None
    programs = _programs(deps, command, cwd)
    if programs is None:
        return None
    answer = await command_check.ask_probe(command=command, cwd=str(cwd), reason=str(verdict.reason or ""),
                                           working_folders=_working_roots(deps))
    if answer is None or not answer.approve:
        return None
    again_programs = _programs(deps, command, cwd)
    if again_programs is None or again_programs != programs:
        return None
    again = _classify(deps, command, cwd)
    if not again.safe and (again.refused or again.reason != verdict.reason or not _judgeable(deps, command, again, cwd)):
        return None
    if _script_facts(deps, command, cwd):
        return None
    return command_check.jev_reason(answer.lowest)
from probe.daemon.agent.tools.bash.bash import _names_policy_path  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.bash.steps import _working_roots  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.config import _classify  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.refusals import _script_facts  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
