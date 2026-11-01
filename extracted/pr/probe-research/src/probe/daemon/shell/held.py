"""what a held command would run as code (scripts its words do not show) and its strict credential/private reading."""

from __future__ import annotations
import os
import re
import shlex
from dataclasses import dataclass, field
from pathlib import Path
from probe.daemon.shell.parse import _ASSIGNMENT
from probe.daemon.shell.safe_lists import _WRAPPERS
from probe.daemon.shell.words import _norm


# --- what a held command runs ----------------------------------------------
#
# A command that is NOT safe is shown to the researcher and runs on their yes.
# The question shows its words; a script it runs is a file whose text the words
# do not show. So the daemon never asks to run a file in the folders it writes
# without a question (`names_writable`), and a script anywhere else is hashed
# into the question and re-hashed before the yes runs (`held_scripts`). Both
# read the command leniently (it need not pass `classify`), best effort.

_SHELL_RUNNERS = frozenset({"bash", "sh", "zsh", "dash", "ksh", "fish"})
_RUNNER_FAMILY = (
    (re.compile(r"(python|pypy)[0-9.]*"), "python"),
    (re.compile(r"perl[0-9.]*"), "perl"),
    (re.compile(r"node(js)?"), "node"),
    (re.compile(r"ruby[0-9.]*"), "ruby"),
)
#: Per family: options whose next word is a value (never the script), and options
#: after which no script file follows (the code is on the command line).
_RUNNER_OPTIONS: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    "shell": (frozenset({"-o", "-O", "+o", "+O", "--rcfile", "--init-file"}), frozenset({"-c"})),
    "python": (frozenset({"-W", "-X", "--check-hash-based-pycs"}), frozenset({"-c", "-m"})),
    "perl": (frozenset({"-I", "-M", "-m", "-x"}), frozenset({"-e", "-E"})),
    "node": (frozenset({"-r", "--require", "--import", "--loader", "--experimental-loader", "-C", "--conditions",
                        "--input-type"}), frozenset({"-e", "--eval", "-p", "--print"})),
    "ruby": (frozenset({"-I", "-r", "-C", "-E", "-F"}), frozenset({"-e"})),
}  # fmt: skip
#: A wrapper's options whose next word is a value (`sudo -u root`, `timeout -s KILL`).
_WRAPPER_VALUES = frozenset({"-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-U", "-S", "-s", "-k", "-n", "-i",
                             "-o", "-e", "-w"})  # fmt: skip
_PUNCT = frozenset("();<>|&")
#: What splits a word into the pieces a path may hide in (`open('.env')`,
#: `--key=id_rsa`, `a.pem,b.pem`): the characters a file name in practice never holds.
_PATH_PIECES = re.compile(r"[^\w.~/+@%-]+")


@dataclass
class _Held:
    words: list[str]
    stdin: list[str]  # the targets of its `<` redirects
    piped: bool  # after a `|`: its input is the previous command's output
    #: The targets of its other redirects (`> f`, `>> ~/.zshrc`): files it writes,
    #: which a scan of what a command names must see too.
    targets: list[str] = field(default_factory=list)


def _tree_read(words: list[str]) -> bool:
    """Does this simple command read a whole tree's contents? Any `rg` (it
    searches a tree unless every name is a file); `grep`/`egrep`/`fgrep`/`diff`
    with anything that can mean recursive, read wider than the programs do, so
    a false yes only asks: a short cluster holding `r` or `R` anywhere (a `--`
    may be an option's value: `grep -e -- -r .`), a long option any prefix of
    `--recursive` or `--dereference-recursive` from `--rec` / `--der` on, and
    any word holding `recurse` (`-d recurse`, `--directories=recurse`)."""
    while words and "=" in words[0] and not words[0].startswith("-"):  # `X=1 grep -rn ...`
        words = words[1:]
    if not words:
        return False
    name = os.path.basename(words[0])
    if name == "rg":
        return True
    if name not in ("grep", "egrep", "fgrep", "diff"):
        return False
    for word in words[1:]:
        if "recurse" in word or (len(word) >= 3 and "recurse".startswith(word.split("=")[-1].lstrip("-"))):
            return True  # `-d recurse`, `--directories=recurse`, and GNU's prefixes of it (`-d rec`)
        if name != "diff" and (word in ("-d", "-D") or word.startswith(("-d", "--d"))):
            return True  # grep's `-d ACTION` / `--directories=ACTION` / `--devices`: read wide, it only asks
        if word.startswith("--"):
            opt = word.split("=", 1)[0]
            if (len(opt) >= 5 and "--recursive".startswith(opt)) or (
                    len(opt) >= 5 and "--dereference-recursive".startswith(opt)):
                return True
        elif word.startswith("-") and ("r" in word[1:] or "R" in word[1:]):
            return True
    return False


def _held_commands(command: str) -> list[_Held] | None:
    """The simple commands of `command`, read the way `shlex` reads them (quotes
    removed, `$` and globs left as text, every newline a separator); None when
    it cannot be read (an unclosed quote)."""
    lex = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        tokens = list(lex)
    except ValueError:
        return None
    out = [_Held([], [], False)]
    k = 0
    while k < len(tokens):
        tok = tokens[k]
        if tok and set(tok) <= _PUNCT:
            if "<" in tok or ">" in tok:  # a redirect: the next word is its target
                target = tokens[k + 1] if k + 1 < len(tokens) else ""
                if tok == "<" and target:
                    out[-1].stdin.append(target)
                elif target:
                    out[-1].targets.append(target)
                k += 2
                continue
            out.append(_Held([], [], tok in ("|", "|&")))
        else:
            out[-1].words.append(tok)
        k += 1
    return [c for c in out if c.words]


def _held_dirs(commands: list[_Held], cwd: str, home: str) -> list[str]:
    """Every folder the command may run in: its own, and every `cd` / `pushd` target
    (read against all the folders seen so far: an over-approximation). A `cd` in a
    pipeline moves nothing in bash, and is counted all the same: that only adds a
    folder to look in (its own is never dropped), the safe side for what this
    feeds (`names_writable`, `held_scripts`)."""
    dirs = [cwd]
    for c in commands:
        if c.words[0] in ("cd", "pushd") and len(c.words) > 1:
            for real in _held_resolve(c.words[-1], dirs, home):
                if real not in dirs:
                    dirs.append(real)
    return dirs


def _held_resolve(word: str, dirs: list[str], home: str) -> list[str]:
    if word == "~" or word.startswith("~/"):
        word = home + word[1:]
    out: list[str] = []
    for d in dirs:
        joined = os.path.join(d, word)
        for path in (_norm(joined), os.path.realpath(joined)):
            if path not in out:
                out.append(path)
    return out


def _runner(name: str) -> str | None:
    if name in _SHELL_RUNNERS:
        return "shell"
    return next((family for pattern, family in _RUNNER_FAMILY if pattern.fullmatch(name)), None)


def held_scripts(command: str, *, cwd: Path, home: Path) -> list[str] | None:
    """The files `command` runs as code, whose text its words do not show: a
    program named by its path (`./run.sh`), `source FILE` / `. FILE`, the script
    of bash / sh / zsh / python / perl / node / ruby (behind env, sudo, nohup,
    timeout...), and what such an interpreter reads on stdin when it has no
    script (`bash < f`, `cat f | python`). Realpaths, whether or not they exist
    yet, in every folder a `cd` may reach. None when the command cannot be read."""
    commands = _held_commands(command)
    if commands is None:
        return None
    home_s = _norm(os.path.abspath(str(home)))
    dirs = _held_dirs(commands, os.path.realpath(str(cwd)), home_s)
    found: list[str] = []

    def add(word: str) -> None:
        for real in _held_resolve(word, dirs, home_s):
            if real not in found:
                found.append(real)

    def scan(words: list[str], c: _Held, previous: list[_Held], depth: int) -> None:
        k = 0
        while k < len(words) and _ASSIGNMENT.match(words[k]):
            k += 1
        # Wrappers run the rest: env, sudo, nohup, timeout 10, nice -n 5, xargs...
        while k < len(words) and os.path.basename(words[k]) in _WRAPPERS - _SHELL_RUNNERS - {".", "source"}:
            if words[k] == "eval" and depth < 3:  # its words are one command line
                for n in _held_commands(" ".join(words[k + 1 :])) or []:
                    scan(n.words, n, [], depth + 1)
                return
            k += 1
            while k < len(words) and (words[k].startswith(("-", "+")) or _ASSIGNMENT.match(words[k])
                                      or re.fullmatch(r"[0-9.]+[smhd]?", words[k])):
                if words[k] == "-c" and k + 1 < len(words) and depth < 3:
                    nested = _held_commands(words[k + 1]) or []
                    for n in nested:
                        scan(n.words, n, [], depth + 1)
                    return
                k += 2 if words[k] in _WRAPPER_VALUES else 1
        if k >= len(words):
            return
        program = words[k]
        if "/" in program:
            add(program)
        name = os.path.basename(program)
        rest = words[k + 1 :]
        if name in (".", "source"):
            if rest:
                add(rest[0])
            return
        family = _runner(name)
        if family is None:
            return
        values, code = _RUNNER_OPTIONS[family]
        j = 0
        while j < len(rest):
            word = rest[j]
            # `-c`, or a cluster ending in it (`bash -lc`, `perl -ne`, `python -Bc`).
            if word in code or (word[:1] == "-" and word[1:2] not in ("-", "") and f"-{word[-1]}" in code):
                if family == "shell" and j + 1 < len(rest) and depth < 3:
                    for n in _held_commands(rest[j + 1]) or []:
                        scan(n.words, n, [], depth + 1)
                return
            if word in values:
                j += 2
                continue
            if word in ("-", "-s") or word == "--":
                j += 1
                if word == "--" and j < len(rest):
                    add(rest[j])
                    return
                continue
            if word.startswith(("-", "+")):
                j += 1
                continue
            add(word)
            return
        # No script on the command line: it reads its code from stdin.
        for target in c.stdin:
            add(target)
        if c.piped:
            for p in previous:
                for word in [*p.words[1:], *p.stdin]:
                    if not word.startswith("-") and any(os.path.isfile(r) for r in _held_resolve(word, dirs, home_s)):
                        add(word)

    pipeline: list[_Held] = []
    for c in commands:
        pipeline = [*pipeline, c] if c.piped else [c]
        scan(c.words, c, pipeline[:-1], 0)
    return found
