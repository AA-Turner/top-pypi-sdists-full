"""a shell line that certainly starts a Probe run (`probe exec` opening one, `probe run start`)."""

from __future__ import annotations
import os
import re
import shlex
from probe.service.hints.triggers.window import MAX_TEXT_CHARS
#: What a shell runs in front of a command it starts.
_WRAPPERS = frozenset({"env", "nohup", "time", "command", "exec", "nice", "stdbuf", "caffeinate"})
#: `probe exec`'s options that take a value, and those that open a run here.
_EXEC_VALUES = frozenset({"--cwd", "--project", "--experiment", "--slug", "--name", "--description", "--tag",
                          "--external-id", "--config", "--parent", "--relation", "--intent", "--authored-by",
                          "--launcher", "--outputs", "--input", "--output"})
_EXEC_OPENS = frozenset({"--project", "--experiment", "--slug", "--name", "--description", "--tag",
                         "--external-id", "--config", "--intent"})
_HELP = frozenset({"--help", "-h"})
_SHELL_OPERATORS = frozenset({"&&", "||", ";", "|", "&", "(", ")", ";;", "|&"})
#: A shell line longer than this is never read as a launch: `shell_part` is
#: quadratic in heredoc markers (32 kB of them take seconds), and the tail
#: thread reads every session.
MAX_COMMAND_CHARS = MAX_TEXT_CHARS
#: A heredoc's body (kept: the rest of its first line, which is still shell), and
#: a quoted string: text a command only writes (`shell_part`).
_HEREDOC = re.compile(r"<<-?[ \t]*(['\"]?)(\w+)\1([^\n]*)\n(?:.*?\n)??[ \t]*\2[ \t]*(?:\n|$)", re.DOTALL)
_QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")


# -- triggers ---------------------------------------------------------------------


def shell_part(command: str) -> str:
    """What the shell itself runs: heredoc bodies and quoted strings blanked, so
    text a command only writes (a CHANGELOG line, a doc) never reads as run."""
    return _QUOTED.sub("''", _HEREDOC.sub(lambda m: f"<<{m.group(2)}{m.group(3)}\n", command))


def _segments(text: str) -> list[list[str]]:
    """A shell line's simple commands, as words; [] when any line of it cannot
    be split. `text` is `shell_part`'s (quoted strings and heredoc bodies
    blanked), so a newline left in it ends a command, as `;` does."""
    segments: list[list[str]] = [[]]
    for line in text.replace("\\\n", " ").split("\n"):
        lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        lexer.commenters = ""
        segments.append([])
        try:
            for token in lexer:
                if token in _SHELL_OPERATORS or (token and set(token) <= set("&|;()")):
                    segments.append([])
                else:
                    segments[-1].append(token)
        except ValueError:
            return []  # an unbalanced quote: nothing in it is certain
    return [s for s in segments if s]


def _probe_args(words: list[str]) -> list[str] | None:
    """The arguments of `probe` when it is the command these words run
    (after variable assignments and plain wrappers: `env`, `nohup`, `uv run`)."""
    i = 0
    while i < len(words):
        word = words[i]
        name = os.path.basename(word)
        if "=" in word and not word.startswith("-") and re.match(r"[A-Za-z_][A-Za-z0-9_]*=", word):
            i += 1
        elif name in _WRAPPERS:
            i += 1
            while i < len(words) and (words[i].startswith("-") or (name == "env" and "=" in words[i])):
                i += 1
        elif name == "uv" and i + 1 < len(words) and words[i + 1] == "run":
            i += 2
            while i < len(words) and words[i].startswith("-"):
                i += 1
        elif name == "probe":
            return words[i + 1:]
        else:
            return None
    return None


def _opens_with_exec(args: list[str]) -> bool:
    """`probe exec <args>`: does it open a NEW run? `probe exec RUN -- cmd`
    takes one that exists (as the CLI reads it: a word before `--` is the run,
    unless an option that opens one here is given; then it starts the command)."""
    if "--" in args:
        own, command = args[: args.index("--")], args[args.index("--") + 1:]
    else:
        own, command = args, []
    if any(a in _HELP for a in own):
        return False
    words: list[str] = []
    opens = False
    i = 0
    while i < len(own):
        arg = own[i]
        name = arg.split("=", 1)[0]
        if arg.startswith("-"):
            opens = opens or name in _EXEC_OPENS
            i += 2 if name in _EXEC_VALUES and "=" not in arg else 1
            continue
        words.append(arg)
        i += 1
    if "--" in args:
        return bool(command) and (not words or opens)
    return opens and bool(words)


def launches_run(command: str) -> bool:
    """Does this shell line certainly start a Probe run: `probe exec` opening
    a new one, or `probe run start` (never with `--help`)? Text a command only
    writes (heredoc bodies, quoted strings) is not read as run."""
    if not command or len(command) > MAX_COMMAND_CHARS or "probe" not in command:
        return False
    try:
        text = shell_part(command)
    except Exception:  # noqa: BLE001 -- unparsable: nothing is certain
        return False
    for words in _segments(text):
        args = _probe_args(words)
        if not args:
            continue
        if args[0] == "exec" and _opens_with_exec(args[1:]):
            return True
        if args[:2] == ["run", "start"] and not any(a in _HELP for a in args[2:]):
            return True
    return False
