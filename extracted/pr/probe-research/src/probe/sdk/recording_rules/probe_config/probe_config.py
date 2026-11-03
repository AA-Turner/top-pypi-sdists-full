"""`.probe.config`: how much of a path Probe may touch, in gitignore syntax.

A `.probe.config` in any folder sets a LEVEL for paths under that folder:

- `off`: Probe never reads them and records nothing about them -- no run
  opened there, no artifact or note about them, no daemon event;
- `read`: the Probe daemon may see the agent's work on them, as context; Probe
  records nothing about them (to the SDK, the CLI and the agent this is `off`);
- `hash`: the SDK records each file's IDENTITY and nothing else -- its path,
  sha256 (or the >1 GiB fingerprint), size and row count -- so a step over the
  data still opens a run (metrics, config, these identities) and its arrows
  appear; never bytes, previews, uploads, output capture or text from the
  file. Below 64 bytes not even the hash. To the daemon this is `off`;
- `on`: recorded as usual (what `!pattern` means).

`read` and `hash` do not combine: one path has one winning level, and where
two verdicts meet (a symlink and its target) one at `read` and one at `hash`
make `off`. The guarantee is about what Probe RECORDS: text an agent prints
into its own session transcript still uploads with the transcript, as under
`off`. A client from before `hash` existed reads it as `off`.

A plain line is `off`. `@probe <level>` on a line of its own sets the level of
the lines after it (written first, it is the file's default), and
`<pattern> @probe <level>` sets one line's. A level only narrows what the
session's on / read / off switch allows; it never blocks the agent's own
Probe lookups. The rules are git's (`gitignore(5)`), applied the way git
applies them:

- a file covers its own folder and everything below it; patterns are relative
  to that folder; a folder with no file inherits its parents' rules;
- a later line beats an earlier one, a deeper file beats a shallower one;
- a folder at `off` is closed, as git closes an ignored folder: nothing inside
  it is looked at (its own `.probe.config` included) and no line turns
  anything inside it back on. `secret/*` closes nothing, so
  `secret/important.txt @probe on` after it works;
- a folder at `read`, `hash` or `on` stays open: what is inside it takes the
  folder's level unless a line matches it directly; a deeper `.probe.config`
  inside a `read` or `hash` folder may narrow it to `off`, never loosen it;
- `/` anchors, a trailing `/` matches folders only, `**` spans folders.

One deliberate difference from git: files ABOVE a repository root count too,
so `~/.probe.config` is the machine-wide list and `~/code/.probe.config` with
`/*` then `!/repo-a/` tracks only repo-a.

A file ABOVE the folder an agent session started in is the researcher's to set
aside for that session (`probe session parent ignore`); until they answer it is
followed. Files at or below the launch folder always apply.

THIS MODULE IS STDLIB-ONLY AND IMPORTS NOTHING FROM `probe`. It is copied
verbatim beside both plugins' hooks (`_probe_config.py`), which run under the
system python with no package on their path (`make sync-probe-config`; `tests/test_probe_config_sync.py` fails
when a copy drifts). Matching never uses a backtracking regex: a segment glob
is a dynamic-programming match, so no pattern can make a check slow.

FAILS CLOSED. A `.probe.config` that exists but cannot be read (permissions, a
FIFO, a directory, over `MAX_BYTES`, undecodable) excludes everything under its
folder, with a warning: a privacy list that silently stops applying is worse
than one that over-applies. A pattern git would never match is skipped, as git
skips it.
"""

from __future__ import annotations

import errno
import functools
import hashlib
import json
import os
import stat
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

CONFIG_NAME = ".probe.config"
#: The retired folder default (`<folder>/.probe/config.json`, #1252). An old one
#: set to `off` or `read` still counts as `*` here until `probe doctor --fix`
#: converts it, so retiring the feature never starts recording anywhere.
LEGACY_DIRNAME = ".probe"
LEGACY_FILENAME = "config.json"
#: Over this, a `.probe.config` is unreadable (fails closed).
MAX_BYTES = 1024 * 1024
#: The parent-config answer beside a session's state file.
PARENT_SUFFIX = ".parent-config"
#: Where a session started, beside its state file (written once, at seed).
LAUNCH_SUFFIX = ".launch-dir"

#: The levels, least restrictive first. `on` is recorded; `read`, `hash` and
#: `off` are not recorded as usual (`Verdict.excluded`): `hash` records only a
#: file's identity (`Verdict.identity_only`), and `off` is not even read
#: (`Verdict.hidden`). `read` and `hash` are not ordered against each other
#: (`read` lets the daemon see, `hash` lets the SDK record identity): where both
#: meet, the answer is `off` (`stricter`). The rank orders the rest, and makes
#: `read` the looser of the two where only a loosest is asked (`check_cwd`).
ON = "on"
READ = "read"
HASH = "hash"
OFF = "off"
LEVELS = (ON, READ, HASH, OFF)
_RANK = {ON: 0, READ: 1, HASH: 2, OFF: 3}
#: The levels inside which a deeper `.probe.config` may narrow (to `off`) but
#: never loosen (`_ceiling`).
_CEILINGS = (READ, HASH)
#: The word that sets a level: `@probe <level>` alone on a line sets the lines
#: after it, `<pattern> @probe <level>` one line.
LEVEL_WORD = "@probe"

FOLLOW = "follow"
IGNORE = "ignore"
#: A parent file reaches this session and nobody has asked yet.
UNASKED = "unasked"
#: Asked, not answered: followed.
PENDING = "pending"

#: Case-insensitive file systems by default (macOS, Windows): match without case,
#: which excludes more, never less.
_FOLD_CASE = sys.platform in ("darwin", "win32")

#: Skipped by the session-start scan below the launch folder (never by a check).
SCAN_SKIP_DIRS = frozenset(
    {".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache", ".pytest_cache",
     ".ruff_cache", ".tox", ".cache", "site-packages", "wandb", ".hg", ".svn"}
)


# What the SDK and CLI print (agent-facing refusals live in session_marker).
INIT_EXCLUDED = "probe: `{path}` is excluded by `{source}`, so no run was opened. The script runs as usual."
INIT_HASH_ONLY = (
    "probe: `{path}` is at `hash` by `{source}`: the run records metrics, config and the identity "
    "(path, hash, size, rows) of the files it reads and writes there, never their contents or its console log."
)
ARTIFACT_EXCLUDED = "probe: `{path}` is excluded by `{source}`, so it was not uploaded."
FOLDER_DEFAULT_RETIRED = (
    "Folder defaults are retired. List paths Probe should never record in a `.probe.config` "
    "(gitignore syntax); `probe ignore check PATH` tests it."
)
DOCTOR_OLD_DEFAULT = (
    "`{path}` is a retired folder default (`{state}`); it still blocks recording, as `*`. "
    "`probe doctor --fix` turns it into `{dir}/.probe.config`."
)
DOCTOR_OLD_DEFAULT_ON = (
    "`{path}` is a retired folder default (`on`) and does nothing now; `probe doctor --fix` "
    "deletes it. To track only some folders: machine default `on`, and `/*` then `!/<folder>/` "
    "in a parent's `.probe.config`."
)


def local_path_of(uri: str | None) -> str | None:
    """The local path a `file://` uri names (`file:///a%20b`, `file://localhost/x`),
    else None."""
    if not isinstance(uri, str) or not uri.lower().startswith("file:"):
        return None
    from urllib.parse import unquote, urlparse

    parsed = urlparse(uri)
    if parsed.netloc not in ("", "localhost"):
        return None
    return unquote(parsed.path) or None


def shown(path: str | os.PathLike) -> str:
    """A path as a message names it (`~` for home)."""
    return _display(os.fspath(path))


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

#: Segment tokens: ("lit", ch) | ("one",) | ("star",) | ("class", negated, items)
#: where items are (lo, hi) code-point ranges or ("cls", name).
_POSIX_CLASSES = {
    "alnum": str.isalnum,
    "alpha": str.isalpha,
    "blank": lambda c: c in " \t",
    "cntrl": lambda c: ord(c) < 32 or ord(c) == 127,
    "digit": lambda c: "0" <= c <= "9",
    "graph": lambda c: c.isprintable() and not c.isspace(),
    "lower": str.islower,
    "print": str.isprintable,
    "punct": lambda c: c.isprintable() and not c.isalnum() and not c.isspace(),
    "space": str.isspace,
    "upper": str.isupper,
    "xdigit": lambda c: c in "0123456789abcdefABCDEF",
}


class _BadPattern(ValueError):
    pass


def _tokenize_segment(seg: str) -> tuple:
    """One `/`-free pattern segment as tokens. Raises `_BadPattern` for what git's
    wildmatch can never match (an unterminated `[`, a trailing lone `\\`)."""
    out: list = []
    i, n = 0, len(seg)
    while i < n:
        c = seg[i]
        if c == "\\":
            if i + 1 >= n:
                raise _BadPattern("trailing backslash")
            out.append(("lit", seg[i + 1]))
            i += 2
        elif c == "*":
            if not out or out[-1] != ("star",):
                out.append(("star",))
            i += 1
        elif c == "?":
            out.append(("one",))
            i += 1
        elif c == "[":
            token, i = _bracket(seg, i)
            out.append(token)
        else:
            out.append(("lit", c))
            i += 1
    return tuple(out)


def _bracket(seg: str, i: int) -> tuple[tuple, int]:
    """Parse `[...]` starting at seg[i] == '['. Returns (token, next index)."""
    j = i + 1
    n = len(seg)
    negated = False
    if j < n and seg[j] in "!^":
        negated = True
        j += 1
    items: list = []
    first = True
    while True:
        if j >= n:
            raise _BadPattern("unterminated [")
        c = seg[j]
        if c == "]" and not first:
            return ("class", negated, tuple(items)), j + 1
        first = False
        if c == "[" and j + 1 < n and seg[j + 1] == ":":
            end = seg.find(":]", j + 2)
            if end < 0:
                raise _BadPattern("unterminated [:")
            name = seg[j + 2 : end]
            if name not in _POSIX_CLASSES:
                raise _BadPattern(f"unknown class [:{name}:]")
            items.append(("cls", name))
            j = end + 2
            continue
        if c == "\\":
            j += 1
            if j >= n:
                raise _BadPattern("unterminated [")
            c = seg[j]
        lo = c
        j += 1
        if j + 1 < n and seg[j] == "-" and seg[j + 1] != "]":
            hi = seg[j + 1]
            if hi == "\\":
                if j + 2 >= n:
                    raise _BadPattern("unterminated [")
                hi = seg[j + 2]
                j += 1
            j += 2
            items.append((lo, hi))
        else:
            items.append((lo, lo))


def _class_has(items: tuple, ch: str) -> bool:
    for item in items:
        if item[0] == "cls":
            if _POSIX_CLASSES[item[1]](ch):
                return True
        elif item[0] <= ch <= item[1]:
            return True
    return False


def _token_eq(token: tuple, ch: str) -> bool:
    kind = token[0]
    if kind == "lit":
        if _FOLD_CASE:
            return token[1].lower() == ch.lower()
        return token[1] == ch
    if kind == "one":
        return ch != "/"
    # class
    if ch == "/":
        return False
    hit = _class_has(token[2], ch) or (_FOLD_CASE and (_class_has(token[2], ch.lower()) or _class_has(token[2], ch.upper())))
    return hit != token[1]


def _match_segment(tokens: tuple, name: str) -> bool:
    """Glob-match one path segment. O(len(tokens) * len(name)), no backtracking."""
    n = len(name)
    # prev[j]: tokens[:i] match name[:j]
    prev = [False] * (n + 1)
    prev[0] = True
    for token in tokens:
        cur = [False] * (n + 1)
        if token == ("star",):
            seen = False
            for j in range(n + 1):
                seen = seen or prev[j]
                cur[j] = seen
        else:
            for j in range(1, n + 1):
                cur[j] = prev[j - 1] and _token_eq(token, name[j - 1])
        prev = cur
        if not any(prev):
            return False
    return prev[n]


#: A segment that is exactly `**`.
_GLOBSTAR = ("globstar",)


@dataclass(frozen=True)
class Rule:
    """One pattern line of one `.probe.config`."""

    base: str  # the folder holding the file
    source: str  # the file (or a synthetic description)
    line: int
    pattern: str  # the line as written (trimmed)
    negated: bool
    dir_only: bool
    anchored: bool
    segments: tuple  # tuple of token-tuples or _GLOBSTAR
    #: From a retired folder default (`.probe/config.json` off/read): it counts
    #: only inside an agent session (`legacy=True`), the only place it ever did.
    legacy: bool = False
    #: What a match sets: `on`, `read` or `off`.
    level: str = OFF
    #: The pattern alone (no `!`, no `@probe` suffix), for describing the place.
    text: str = ""

    def matches(self, rel: tuple[str, ...], is_dir: bool) -> bool:
        """Does this rule match the path `rel` (segments relative to `base`)?"""
        if self.dir_only and not is_dir:
            return False
        if not rel:
            return False
        if not self.anchored:
            return _match_segment(self.segments[0], rel[-1])
        return _match_segments(self.segments, rel)

    def could_reach(self, rel: tuple[str, ...]) -> bool:
        """Could this rule match `rel` (as a folder), one of its ancestors below
        `base`, or anything inside it? From the pattern alone, no disk. A rule
        that sets `on` restricts nothing, so it reaches nothing."""
        if self.level == ON:
            return False
        if not self.anchored:
            return True
        for k in range(1, len(rel) + 1):
            if _match_segments(self.segments, rel[:k]):
                return True
        return _extends(self.segments, rel)

    @property
    def where(self) -> str:
        return f"{self.source}:{self.line} ({self.pattern})" if self.line else f"{self.source} ({self.pattern})"


def _match_segments(pat: tuple, path: tuple[str, ...]) -> bool:
    """Match pattern segments against path segments; `**` spans folders.

    A trailing `**` needs at least one segment (`abc/**` is what is INSIDE abc);
    a leading or middle `**` may span none."""
    m, n = len(pat), len(path)
    # dp[i][j]: pat[i:] matches path[j:]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[m][n] = True
    for i in range(m - 1, -1, -1):
        seg = pat[i]
        last = i == m - 1
        for j in range(n, -1, -1):
            if seg is _GLOBSTAR or seg == _GLOBSTAR:
                if last:
                    dp[i][j] = j < n  # one or more remaining segments
                else:
                    # zero segments, or eat one and stay
                    dp[i][j] = dp[i + 1][j] or (j < n and dp[i][j + 1])
            else:
                dp[i][j] = j < n and _match_segment(seg, path[j]) and dp[i + 1][j + 1]
    return dp[0][0]


def _extends(pat: tuple, path: tuple[str, ...]) -> bool:
    """Can `pat` match some path that STARTS with all of `path` plus at least one
    more segment? (The rule reaches inside the folder `path`.)"""
    m, n = len(pat), len(path)
    # reach[i][j]: pat[:i] consumed path[:j]
    reach = [[False] * (n + 1) for _ in range(m + 1)]
    reach[0][0] = True
    for i in range(m):
        seg = pat[i]
        for j in range(n + 1):
            if not reach[i][j]:
                continue
            if seg is _GLOBSTAR or seg == _GLOBSTAR:
                # A globstar can swallow the rest of `path` and still match more.
                return True
            if j < n and _match_segment(seg, path[j]):
                reach[i + 1][j + 1] = True
    # All of `path` consumed with pattern left over: the rest can match below.
    return any(reach[i][n] for i in range(m))


def level_of(word: str) -> str | None:
    """`on` / `read` / `hash` / `off` from a level word (any case), else None."""
    low = word.lower()
    return low if low in _RANK else None


def setting_line(raw: str) -> str | None:
    """The level word of an `@probe <level>` line, else None (a pattern line)."""
    parts = raw.strip(" \t\r\n").split()
    if len(parts) == 2 and parts[0].lower() == LEVEL_WORD:
        return parts[1]
    return None


def _split_level(text: str) -> tuple[str, str | None]:
    """`(pattern, level word)` for `<pattern> @probe <word>`, else `(text, None)`.
    Plain scans, no regex: the suffix is the last two words, `@probe` and the
    level, after whitespace. A pattern that really ends in ` @probe x` escapes
    it (`\\@probe`)."""
    end = len(text)
    while end and text[end - 1] in " \t":
        end -= 1
    j = end
    while j and text[j - 1] not in " \t":
        j -= 1
    word = text[j:end]
    k = j
    while k and text[k - 1] in " \t":
        k -= 1
    m = k
    while m and text[m - 1] not in " \t":
        m -= 1
    if not word or k == j or text[m:k].lower() != LEVEL_WORD:
        return text, None
    n = m
    while n and text[n - 1] in " \t":
        n -= 1
    if n == m or n == 0:
        return text, None
    body = text[:n]
    if body.endswith("\\") and not body.endswith("\\\\"):
        body += text[n]  # an escaped space just before the suffix stays
    return body, word


def parse_line(raw: str, base: str, source: str, line: int, default: str = OFF) -> Rule | None:
    """One `.probe.config` line as a Rule, None for a blank, comment or `@probe`
    setting line. `default` is the level a plain line sets (the last `@probe
    <level>` line above it). Raises `_BadPattern` for a line git would never match."""
    return _parse(raw, base, source, line, default)[0]


def _parse(raw: str, base: str, source: str, line: int, default: str = OFF) -> tuple[Rule | None, str | None]:
    """`parse_line`, plus a warning about the line (an unknown level counts as `off`)."""
    text = raw.rstrip("\r\n")
    if not text or text.startswith("#"):
        return None, None
    if setting_line(text) is not None:
        return None, None
    text, word = _split_level(text)
    note = None
    level = default
    if word is not None:
        level = level_of(word) or OFF
        if level_of(word) is None:
            note = f"`{word}` is not a level (on, read, hash, off), so the line counts as `off`."
    text = _trim_trailing_spaces(text)
    if not text:
        return None, None
    negated = False
    if text.startswith("!"):
        negated = True
        text = text[1:]
        if word is None:
            level = ON
    elif text.startswith("\\!") or text.startswith("\\#"):
        text = text[1:]
    if not text:
        return None, None
    shown_text = text
    dir_only = text.endswith("/") and not text.endswith("\\/")
    body = text[:-1] if dir_only else text
    if not body:
        return None, None
    anchored = "/" in body
    if body.startswith("/"):
        body = body[1:]
    if not body:
        return None, None
    parts = body.split("/")
    segments: list = []
    for part in parts:
        if part == "**":
            if segments and segments[-1] == _GLOBSTAR:
                continue
            segments.append(_GLOBSTAR)
        elif part == "":
            # `a//b`: git collapses nothing here; an empty segment never matches.
            raise _BadPattern("empty path segment")
        else:
            segments.append(_tokenize_segment(part))
    if not anchored and segments == [_GLOBSTAR]:
        # A lone `**` with no slash is a basename `*`.
        segments = [(("star",),)]
    return Rule(
        base=base,
        source=source,
        line=line,
        pattern=raw.rstrip("\r\n").strip(),
        negated=negated,
        dir_only=dir_only,
        anchored=anchored,
        segments=tuple(segments),
        level=level,
        text=shown_text,
    ), note


def _trim_trailing_spaces(text: str) -> str:
    """Trailing spaces go unless escaped with a backslash (`gitignore(5)`)."""
    end = len(text)
    while end > 0 and text[end - 1] == " ":
        backslashes = 0
        k = end - 2
        while k >= 0 and text[k] == "\\":
            backslashes += 1
            k -= 1
        if backslashes % 2 == 1:
            break
        end -= 1
    return text[:end]


def _everything(base: str, source: str, why: str, *, legacy: bool = False) -> Rule:
    """A synthetic rule excluding everything under `base` (fail closed)."""
    return Rule(
        base=base, source=source, line=0, pattern=why, negated=False, dir_only=False,
        anchored=False, segments=((("star",),),), legacy=legacy, level=OFF, text="*",
    )


