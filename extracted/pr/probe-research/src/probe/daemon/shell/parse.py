"""read a command the way bash would: tokens, commands joined by operators, the folders each runs in."""

from __future__ import annotations
import os
import re
from dataclasses import dataclass
from typing import Iterator
from probe.daemon.shell.classifier.refusals import _Never, _R_HEREDOC, _Refuse


#: The probe commands a quoted heredoc may feed (`_Checker._probe_heredoc`), and
#: what a probe heredoc in another shape answers (NEW wording,
#: tests/fixtures/daemon_prompts/tools/bash-replies.NEW.md).
PROBE_STDIN_COMMANDS = (("draft", "edit"), ("daemon", "task"))
#: The whole-command shape of each, as the refusals name it.
PROBE_HEREDOC_SHAPES = {("draft", "edit"): "probe draft edit PATH <<'EOF'", ("daemon", "task"): "probe daemon task <<'EOF'"}
R_PROBE_HEREDOC = "A probe heredoc must be the whole command: `{shape}`, the text, then a line reading EOF."
R_PROBE_HEREDOC_TAIL = "Something follows the heredoc - `probe {command}` with its text must be the whole command."
R_PROBE_HEREDOC_CHAINED = "`probe {command}` with its heredoc must be the whole command: run the rest in another call."
_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\+?=")
_HEREDOC_TAG = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_CONTROL = frozenset({"|", "&&", "||", ";", "\n"})

_R_DOLLAR = "`$` is allowed only inside single quotes."
#: The one shape a file write takes (the tools name it when a note write is refused).
R_HEREDOC = _R_HEREDOC
_R_BRACE = "An unquoted `{` or `}` can expand to other paths or group commands."


# --- reading the command ---------------------------------------------------


@dataclass(frozen=True)
class _Word:
    value: str  # after quote removal
    raw: str  # as written
    tilde: bool = False  # starts with an unquoted ~ that bash expands to $HOME
    #: The empty VALUE `_dashdash_as_value` puts where a `--` was: never a name or a path.
    synthetic: bool = False


@dataclass(frozen=True)
class _Op:
    op: str  # a control operator (_CONTROL) or a redirect ("<", ">", ">>", ">&", "<<", ...)
    fd: str | None = None  # the digits written before a redirect ("2" in 2>&1)


@dataclass
class _Part:
    words: list[_Word]
    redirects: list[tuple[_Op, _Word]]
    before: str  # the control operator in front of it ("" for the first)


def _tokenize(s: str) -> list[_Word | _Op]:
    """Split a command the way bash would, refusing every construct it can't vouch for."""
    out: list[_Word | _Op] = []
    buf: list[str] = []
    start = -1  # where the current word began (-1: no word yet)
    quoted = False  # the current word has a quoted part
    tilde = False
    i, n = 0, len(s)

    def end_word(at: int) -> None:
        nonlocal buf, start, quoted, tilde
        if start >= 0:
            out.append(_Word("".join(buf), s[start:at], tilde))
        buf, start, quoted, tilde = [], -1, False, False

    while i < n:
        c = s[i]
        if c in " \t":
            end_word(i)
            i += 1
        elif c == "\n":
            end_word(i)
            # A newline right after |, && or || continues the command.
            if not (out and isinstance(out[-1], _Op) and out[-1].op in ("|", "&&", "||")):
                out.append(_Op("\n"))
            i += 1
        elif c == "\\":
            if i + 1 >= n:
                raise _Refuse("The command ends with a stray backslash.")
            if s[i + 1] == "\n":  # line continuation
                i += 2
                continue
            if start < 0:
                start = i
            buf.append(s[i + 1])
            quoted = True
            i += 2
        elif c == "'":
            if start < 0:
                start = i
            j = s.find("'", i + 1)
            if j < 0:
                raise _Refuse("A single quote is never closed.")
            buf.append(s[i + 1 : j])
            quoted = True
            i = j + 1
        elif c == '"':
            if start < 0:
                start = i
            quoted = True
            j = i + 1
            while True:
                if j >= n:
                    raise _Refuse("A double quote is never closed.")
                d = s[j]
                if d == '"':
                    break
                if d == "$":
                    raise _Refuse(_R_DOLLAR)
                if d == "`":
                    raise _Refuse("Backticks run a command inside the command.")
                if d == "\\" and j + 1 < n and s[j + 1] in '$`"\\\n':
                    if s[j + 1] != "\n":
                        buf.append(s[j + 1])
                    j += 2
                    continue
                buf.append(d)
                j += 1
            i = j + 1
        elif c == "$":
            raise _Refuse(_R_DOLLAR)
        elif c == "`":
            raise _Refuse("Backticks run a command inside the command.")
        elif c in "*?[":
            raise _Refuse(
                f"An unquoted `{c}` is a glob - it could match paths the check never saw."
            )
        elif c == "{" and start < 0 and s.startswith("{}", i) and (i + 2 == n or s[i + 2] in " \t\n;|&<>"):
            # The whole word `{}` (find's placeholder) never expands. Anywhere else a
            # brace may: `a{b,c}`, `{x..y}`, a `{` left open for a later word.
            start = i
            buf.append("{}")
            i += 2
        elif c in "{}":
            raise _Refuse(_R_BRACE)
        elif c in "()":
            raise _Refuse("Parentheses start a subshell, a group or a process substitution.")
        elif c == "#" and start < 0:
            raise _Refuse("Comments (#) aren't allowed.")
        elif c == "~" and start < 0:
            nxt = s[i + 1] if i + 1 < n else ""
            if nxt and nxt not in "/ \t\n;|&<>":
                raise _Refuse("`~name`, `~+` and `~-` expand to other folders.")
            start, tilde = i, True
            buf.append("~")
            i += 1
        elif c == "~" and s[i - 1] in "=:":
            raise _Refuse("A `~` after `=` or `:` can expand to $HOME.")
        elif c == ";":
            end_word(i)
            if s.startswith((";;", ";&"), i):
                raise _Refuse("`;;` and `;&` belong to case statements, which aren't allowed.")
            out.append(_Op(";"))
            i += 1
        elif c == "&":
            end_word(i)
            for op in ("&&", "&>>", "&>"):
                if s.startswith(op, i):
                    out.append(_Op(op))
                    i += len(op)
                    break
            else:
                raise _Refuse("A single `&` runs a command in the background.")
        elif c == "|":
            end_word(i)
            if s.startswith("||", i):
                out.append(_Op("||"))
                i += 2
            else:  # `|&` pipes stderr too: still a pipe
                out.append(_Op("|"))
                i += 2 if s.startswith("|&", i) else 1
        elif c in "<>":
            word = "".join(buf)
            fd = None
            if start >= 0 and not quoted and re.fullmatch(r"[0-9]+", word):
                fd = word  # `2>`: the digits belong to the redirect
                buf, start, quoted, tilde = [], -1, False, False
            else:
                end_word(i)
            ops = (">>", ">&", ">|", ">") if c == ">" else ("<<<", "<<-", "<<", "<&", "<>", "<")
            op = next(o for o in ops if s.startswith(o, i))
            out.append(_Op(op, fd))
            i += len(op)
        else:
            if start < 0:
                start = i
            buf.append(c)
            i += 1
    end_word(n)
    return out


def _split(tokens: list[_Word | _Op]) -> list[_Part]:
    """Group tokens into commands joined by control operators."""
    parts: list[_Part] = []
    words: list[_Word] = []
    redirects: list[tuple[_Op, _Word]] = []
    before = ""
    pending: _Op | None = None
    for tok in tokens:
        if isinstance(tok, _Word):
            if pending is not None:
                redirects.append((pending, tok))
                pending = None
            else:
                words.append(tok)
            continue
        if pending is not None:
            raise _Refuse(f"The redirect `{pending.op}` has no target.")
        if tok.op not in _CONTROL:
            pending = tok
            continue
        parts.append(_Part(words, redirects, before))
        words, redirects, before = [], [], tok.op
    if pending is not None:
        raise _Refuse(f"The redirect `{pending.op}` has no target.")
    parts.append(_Part(words, redirects, before))

    # Bash accepts empty commands around `;` and newlines (`ls;`); anything else is broken.
    kept: list[_Part] = []
    for k, part in enumerate(parts):
        if part.words or part.redirects:
            kept.append(part)
            continue
        after = parts[k + 1].before if k + 1 < len(parts) else ""
        if part.before not in ("", ";", "\n") or after not in ("", ";", "\n"):
            raise _Refuse("An operator (|, &&, ||) has no command on one side.")
    if not kept:
        raise _Refuse("The command is empty.")
    return kept


def _cd_word(part: _Part) -> _Word | None:
    """The folder of a plain `cd FOLDER` (None for anything else)."""
    words = part.words
    if not words or words[0].value != "cd":
        return None
    args = words[1:]
    if args and args[0].value == "--":
        args = args[1:]
    if len(args) != 1 or not args[0].value or args[0].value.startswith("-"):
        return None
    return args[0]


def _expand(word: _Word, home: str) -> str:
    return home + word.value[1:] if word.tilde else word.value


#: A process's own folders (`/proc/self/cwd/..`, `/proc/1234/root`, `/dev/fd/3`): the
#: check resolves them in ITS process, bash in the command's.
_PROC_SELF = re.compile(r"/proc/(self|thread-self|[0-9]+)(/|$)|/dev/fd/")
#: A probe command line inside one word (`awk 'BEGIN{system("probe run list")}'`,
#: `git -c core.pager='probe ...'`): `probe` then a lowercase subcommand.
_EMBEDDED_PROBE = re.compile(r"(?<![\w./-])probe\s+[a-z]")
#: Programs that run text in their arguments as commands (`awk system()`, `git -c
#: core.pager=`, `su -c`, `ssh host CMD`...). Only theirs are read for a probe
#: command line: "linear probe accuracy" is an ordinary phrase in ML work.
_CODE_ARGS = frozenset({"awk", "gawk", "mawk", "nawk", "busybox", "doas", "flock", "git", "make", "parallel",
                        "screen", "script", "ssh", "su", "sudo", "tmux", "watch"})


def _never_setting(name: str) -> None:
    """A Probe setting (`PROBE_*`) set, unset or exported by the shell: never run."""
    if name.startswith("PROBE_"):
        raise _Never(f"It sets or unsets {name}, Probe's own setting. The shell has no Probe key - Probe writes go "
                     "through `probe`.")


def _stderr_only(op: _Op, target: _Word) -> bool:
    """`2>&1` or `2>/dev/null`: the redirects a probe step may carry."""
    return op.fd == "2" and ((op.op == ">&" and target.value == "1")
                             or (op.op == ">" and target.value == "/dev/null" and not target.tilde))


def _is_probe(part: _Part) -> bool:
    return bool(part.words) and part.words[0].value == "probe"


def _text(part: _Part) -> str:
    """One command as bash reads it, from the words as written (quotes kept)."""
    redirects = [f"{op.fd or ''}{op.op}{target.raw}" for op, target in part.redirects]
    return " ".join([w.raw for w in part.words] + redirects)


def _walk(parts: list[_Part], start: str, home: str) -> Iterator[tuple[_Part, list[str]]]:
    """Yield each command with the folders it may run in, following `cd`.

    A folder is kept as bash would see it (a `cd` goes to the logical path, or to
    the physical one if that fails); every check resolves it with realpath. After
    `&&` only the folder a successful `cd` reached counts; after `;`, `||` or a
    newline, every folder reached so far does (the `cd` may have failed); the
    sides of a pipeline run in subshells, so a `cd` there moves nothing.
    """
    seen = [start]
    success = [start]
    previous = [start]
    for k, part in enumerate(parts):
        if part.before == "&&":
            cands = success
        elif part.before == "|":
            cands = previous
        else:
            cands = list(seen)
        yield part, cands
        piped = part.before == "|" or (k + 1 < len(parts) and parts[k + 1].before == "|")
        target = None if piped else _cd_word(part)
        if target is None:
            success = cands
        else:
            path = _expand(target, home)
            success = []
            for cand in cands:
                joined = os.path.join(cand, path)
                for folder in (os.path.normpath(joined), os.path.realpath(joined)):
                    if folder not in success:
                        success.append(folder)
            seen += [f for f in success if f not in seen]
        previous = cands
