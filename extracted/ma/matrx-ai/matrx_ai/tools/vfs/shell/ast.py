from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True, slots=True)
class LiteralPart:
    text: str
    quoted: bool = False  # True if part of a single- or double-quoted segment


@dataclass(frozen=True, slots=True)
class VarPart:
    name: str
    default: str | None = None
    mode: str = "plain"
    # plain    -> $VAR / ${VAR}
    # default  -> ${VAR:-word}      (use word if unset/empty)
    # use_default -> ${VAR-word}    (use word if unset)
    # assign   -> ${VAR:=word}      (assign word if unset/empty)
    # error    -> ${VAR:?msg}       (error if unset/empty)
    # alt      -> ${VAR:+word}      (use word if set/nonempty)
    # length   -> ${#VAR}
    # prefix   -> ${VAR#pat}, ${VAR##pat}
    # suffix   -> ${VAR%pat}, ${VAR%%pat}
    # replace  -> ${VAR/pat/repl}, ${VAR//pat/repl}


@dataclass(frozen=True, slots=True)
class CmdSubPart:
    command: CommandList


@dataclass(frozen=True, slots=True)
class ArithPart:
    expression: str


@dataclass(frozen=True, slots=True)
class GlobPart:
    pattern: str


@dataclass(frozen=True, slots=True)
class TildePart:
    user: str | None = None


WordPart = LiteralPart | VarPart | CmdSubPart | ArithPart | GlobPart | TildePart


@dataclass(frozen=True, slots=True)
class Word:
    parts: list[WordPart]
    # When True, the word originates from inside double-quotes (no splitting/glob).
    # Mixed words (e.g. abc"def") are tracked at the part level via LiteralPart.quoted.
    fully_quoted: bool = False


RedirOp = Literal[">", ">>", "<", "2>", "2>>", "&>", "&>>", "<<<", "<<", "<<-"]


@dataclass(frozen=True, slots=True)
class Redirect:
    op: RedirOp
    fd: int | None
    target: Word | None
    heredoc_body: str | None = None
    heredoc_quoted: bool = False
    heredoc_strip_tabs: bool = False  # for <<-
    heredoc_expand: bool = True  # False if quoted terminator (<<'EOF')


@dataclass(frozen=True, slots=True)
class SimpleCommand:
    assignments: list[tuple[str, Word]]
    argv: list[Word]
    redirects: list[Redirect] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Subshell:
    body: CommandList
    redirects: list[Redirect] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Pipeline:
    commands: list[SimpleCommand | Subshell]
    negated: bool = False


@dataclass(frozen=True, slots=True)
class AndOrList:
    pipelines: list[Pipeline]
    operators: list[Literal["&&", "||"]]


Separator = Literal[";", "&", "\n"]


@dataclass(frozen=True, slots=True)
class CommandList:
    items: list[AndOrList]
    separators: list[Separator]


Node = SimpleCommand | Pipeline | AndOrList | CommandList | Subshell
