"""`.probeignore`: paths the researcher does not want Probe to capture.

Gitignore syntax (via ``pathspec``), read from three places and combined:

- ``.probeignore`` at the git toplevel of the run's working directory, or the
  working directory itself outside a repo (or the file ``PROBE_IGNORE_FILE``
  names). Only that one file: a ``.probeignore`` in a subfolder is NOT read, as
  a nested ``.gitignore`` would be. Outside a git repo the root is the working
  directory, so a script started from a subfolder reads the subfolder's file.
  ``probe exec`` exports ``PROBE_IGNORE_FILE`` (and its ``ignore=`` patterns in
  ``PROBE_IGNORE_EXPORTED``) to its child, so the child -- and anything the
  child starts, which inherits its environment -- uses the parent's rules even
  after a ``cd``;
- ``PROBE_IGNORE``: extra patterns, one per line or comma-separated (a pattern
  holding a comma belongs in the file);
- ``probe.init(ignore=[...])``.

UNDER ``probe exec``, the launcher on this host captures for its child: it
collects the child's reads and sweeps its folder after the child exits, and it
took the code snapshot BEFORE the child started. A child's own
``probe.init(ignore=[...])`` therefore reaches the launcher through the channels
those captures already read -- a line in the child's read spool
(``inputs.hand_to_launcher``) and the launcher's output-window record
(``outputs.share_ignore``) -- so its reads and outputs are filtered too. The
code snapshot is already taken, so ``ignore=`` cannot change it: the child
warns, and patterns meant for code capture belong in ``.probeignore`` or
``PROBE_IGNORE`` where the command is launched.

WHERE A PATTERN APPLIES. Inside the root (the directory holding the file: the
git toplevel, or the working directory outside a repo) every pattern is matched
the way git reads a ``.gitignore``. A path OUTSIDE it -- an ``outputs=`` folder
in ``$SCRATCH``, a dataset read from ``/mnt/data`` -- is matched:

- relative to the capture's own root when it has one (the output folder for
  the output sweep): every ``PROBE_IGNORE`` / ``ignore=`` pattern, and the
  file's UNANCHORED patterns (``*.jsonl``, ``ckpt/``, ``**/tmp``). An anchored
  file pattern (``/data``, ``runs/*/dump``) names a place under the root and
  cannot apply there; output capture says so once;
- with no capture root (a read): the unanchored patterns only, against the
  whole path, so ``*.ckpt`` and ``ckpt/`` apply wherever the file is.

A READ is matched both as opened and as resolved, because ``open()`` follows
symlinks: with ``data/`` excluded, ``datalink/rows.csv`` (``datalink -> data``)
is out too, and so is a file an excluded link leads to outside the root
(``bigdata/`` excluded, ``bigdata -> /mnt/big``: a loader opening
``/mnt/big/x`` by its resolved path). Only links at the root's top level, or
named by a glob-free pattern, are followed that way: finding every link would
mean walking the tree. Code and output capture never follow a link, so they
match a link by its own name, as git does.

A file under an excluded folder stays excluded whatever a later ``!`` line
says, as in git (``data/`` then ``!data/keep.csv`` keeps ``keep.csv`` out; write
``data/*`` to re-include it). Matching is case-sensitive on every OS, like git
with ``core.ignorecase=false``.

**It only excludes.** A match removes a path from code capture, output capture
and read capture; nothing here can put a path back. A ``!pattern`` re-includes
only against the lines above it, so it can undo an earlier ``.probeignore``
line, never a safety stop (a credential folder, a credential-shaped name, a
file whose content holds a credential), which is decided separately and first.
What the caller names explicitly still wins: ``log_artifact`` and
``include=`` are not filtered.

**Bounded.** Matching runs in ``probe.init()`` and on every ``open()`` the read
hook sees, and a gitignore wildcard compiles to a backtracking regex
(``*a*a*a*a*a*a*a*a*b`` took 51 s on one 60-character name). A pattern with
more than ``MAX_STARS`` single ``*`` or ``MAX_DOUBLE_STARS`` ``**``, or longer
than ``MAX_PATTERN_CHARS``, is skipped with a warning, as are lines past
``MAX_PATTERNS`` and bytes past ``MAX_FILE_BYTES``. Only a regular file is
read (a FIFO named ``.probeignore`` would block ``probe.init()`` forever); an
unreadable one is named in a warning, and a UTF-16 one (PowerShell's ``>``) is
decoded as such.

**Opt-in, no default patterns (D22).** No file, no variable and no argument
means :func:`load` returns ``None`` and capture pays nothing: ``pathspec`` is
imported only when there is a pattern to compile.
"""

from __future__ import annotations

import codecs
import functools
import os
import stat
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

#: The file's name, at the git toplevel (or the working directory).
IGNORE_FILE = ".probeignore"
#: Extra patterns, one per line or comma-separated.
ENV_PATTERNS = "PROBE_IGNORE"
#: Absolute path of the file to read instead of looking for one; `probe exec`
#: exports it for its child.
ENV_FILE = "PROBE_IGNORE_FILE"
#: The launcher's ``ignore=`` patterns, which `probe exec` exports for its child
#: one per line (`join_lines`), exactly: a comma in a pattern survives, where
#: ``PROBE_IGNORE`` would split it. Not for hand use; ``PROBE_IGNORE`` is.
ENV_EXPORTED = "PROBE_IGNORE_EXPORTED"
#: The reason recorded for a path a pattern excluded.
REASON = "probeignore"

#: Bounds (see the module docstring, "Bounded").
MAX_FILE_BYTES = 64 * 1024
MAX_PATTERNS = 1_000
MAX_PATTERN_CHARS = 1_024
MAX_STARS = 3
MAX_DOUBLE_STARS = 2
#: Verdicts cached per folder (the read hook asks per open); cleared when full.
_CACHE_MAX = 8_192
#: Entries of the root's top level looked at for excluded symlinks, and how
#: many link targets are kept (see `IgnoreRules._link_targets`).
MAX_LINK_SCAN = 10_000
MAX_LINK_TARGETS = 64


def _toplevel(cwd: str) -> str | None:
    """The git toplevel of ``cwd``, or None (no repo, no git, any failure).
    Read-only: ``rev-parse`` writes nothing, and optional locks are off."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    top = proc.stdout.strip()
    return top if proc.returncode == 0 and top else None


@functools.lru_cache(maxsize=4096)
def _real_dir(directory: str) -> str:
    """``realpath`` of a directory, cached: the read hook asks per open, and a
    loader reading a million files reads them from a few directories."""
    return os.path.realpath(directory)


def _under(full: str, root: str) -> str | None:
    try:
        rel = os.path.relpath(full, root)
    except ValueError:  # Windows: a path on another drive than the root
        return None
    if rel == os.curdir or rel == os.pardir or rel.startswith(os.pardir + os.sep):
        return None
    return rel.replace(os.sep, "/")


def _within(full: str, root: str) -> str | None:
    """``full`` relative to ``root`` in posix form, or None outside it.

    Tried as written, then with symlinks resolved on both sides: git reports
    its toplevel resolved, while a working directory, an ``outputs=`` folder or
    an opened path may reach the same tree through a link (a symlinked
    checkout, macOS's ``/var`` -> ``/private/var``). Only the DIRECTORY is
    resolved: a pattern matches a link by its own name, as in git.
    """
    rel = _under(full, root)
    if rel is None:
        head, tail = os.path.split(full)
        rel = _under(os.path.join(_real_dir(head), tail), _real_dir(root))
    return rel


def _resolved(full: str) -> str:
    """``full`` with its symlinks resolved, cheaply: the directory from the
    per-directory cache, then one ``lstat`` for the last component."""
    head, tail = os.path.split(full)
    real = os.path.join(_real_dir(head), tail)
    if os.path.islink(real):
        real = os.path.realpath(real)
    return real


def _trim_trailing_spaces(pattern: str) -> str:
    """A pattern without its trailing spaces, as git reads a line: they are
    dropped unless a backslash escapes them (``a\\ `` keeps one)."""
    end = None  # where the current run of unescaped trailing spaces starts
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == " ":
            if end is None:
                end = i
        else:
            end = None
            if char == "\\":
                i += 1  # the next character is escaped, a space included
        i += 1
    return pattern if end is None else pattern[:end]


def _anchored(pattern: str) -> bool:
    """Whether a gitignore pattern names a place under its root (a `/` other
    than a trailing one: `/data`, `runs/*/dump`) rather than a name that may
    sit at any depth (`*.jsonl`, `ckpt/`, `**/tmp/x`). Trailing spaces are
    trimmed first, as git trims them: `ckpt/ ` is `ckpt/`."""
    pattern = _trim_trailing_spaces(pattern)
    body = pattern[1:] if pattern.startswith("!") else pattern
    body = body.rstrip("/")
    if body.startswith("**/"):
        return False
    return "/" in body


def _too_costly(pattern: str) -> bool:
    """A pattern whose regex could backtrack for seconds on one name."""
    if len(pattern) > MAX_PATTERN_CHARS:
        return True
    plain = pattern.replace("\\*", "")
    doubles = plain.count("**")
    return doubles > MAX_DOUBLE_STARS or plain.replace("**", "").count("*") > MAX_STARS


def split_patterns(raw: str | None) -> list[str]:
    """``PROBE_IGNORE``'s patterns: one per line or comma-separated, each
    stripped of surrounding spaces. (A comma cannot be inside a pattern here;
    put such a pattern in the file.)"""
    if not raw:
        return []
    return [p.strip() for line in raw.splitlines() for p in line.split(",") if p.strip()]


def join_lines(patterns: Iterable[str]) -> str:
    """``ENV_EXPORTED``'s value: one pattern per line. A newline cannot be in a
    pattern (a `.probeignore` line is one), a comma can."""
    return "\n".join(patterns)


def split_lines(raw: str | None) -> list[str]:
    """The inverse of :func:`join_lines`: patterns exactly as given."""
    return [line for line in (raw or "").split("\n") if line.strip()]


def normalize(patterns: Any) -> tuple[str, ...]:
    """``ignore=`` as a tuple of patterns: a string is one pattern. Raises
    ``ValueError`` for anything that is not strings, before a run is opened."""
    if patterns is None:
        return ()
    if isinstance(patterns, str):
        return (patterns,)
    try:
        items = tuple(patterns)
    except TypeError:
        raise ValueError("ignore= takes gitignore-style patterns as strings") from None
    if not all(isinstance(p, str) for p in items):
        raise ValueError("ignore= takes gitignore-style patterns as strings")
    return items


def _file_lines(path: str) -> list[str]:
    """The file's lines, at most ``MAX_FILE_BYTES`` of it. Never blocks and
    never raises:

    - only a regular file is read: it is opened non-blocking and checked
      before reading, so a FIFO named ``.probeignore`` (which would block
      ``probe.init()`` forever) or a directory is skipped with a warning;
    - a file that exists but cannot be read (``chmod 000``) is named in a
      warning rather than silently applying nothing;
    - BOM-tolerant: a UTF-8 BOM (a Windows editor) would otherwise glue itself
      to the first pattern, and a UTF-16 file (PowerShell's ``>``) is decoded
      as UTF-16 instead of as garbage. A file still holding NUL bytes is some
      other encoding: its patterns would be garbage, so it is warned about.
    """
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0))
    except FileNotFoundError:
        return []
    except OSError as exc:
        _warn(f"probe: {path} could not be read ({exc.strerror or exc}); its patterns do not apply")
        return []
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            _warn(f"probe: {path} is not a regular file; its patterns do not apply")
            return []
        with os.fdopen(fd, "rb") as fh:
            fd = -1  # the file object owns it now
            raw = fh.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        _warn(f"probe: {path} could not be read ({exc.strerror or exc}); its patterns do not apply")
        return []
    finally:
        if fd >= 0:
            os.close(fd)
    truncated = len(raw) > MAX_FILE_BYTES
    raw = raw[:MAX_FILE_BYTES]
    if raw.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        text = raw[: len(raw) - len(raw) % 2].decode("utf-16", errors="replace")
    else:
        text = raw.decode("utf-8-sig", errors="replace")
    if "\x00" in text:
        _warn(f"probe: {path} is not UTF-8 or UTF-16 text (it holds NUL bytes); its patterns "
              "do not apply. Save it as UTF-8.")
        return []
    lines = text.splitlines()
    if truncated:
        if lines and not text.endswith(("\n", "\r")):
            lines.pop()  # cut mid-line: never apply half a pattern
        _warn(f"probe: {path} is over {MAX_FILE_BYTES // 1024} KB; only its first "
              f"{MAX_FILE_BYTES // 1024} KB of patterns are used")
    return lines


def _meaningful(lines: Iterable[str]) -> list[str]:
    """Patterns only: not blank, not a `#` comment (a `#` at the line's start,
    as in git)."""
    return [line for line in lines if line.strip() and not line.startswith("#")]


def _warn(message: str) -> None:
    from . import safe_warn

    safe_warn.warn(message, stacklevel=3)


@dataclass(frozen=True)
class IgnoreRules:
    """Compiled patterns. ``root`` is what relative paths are matched against
    (see the module docstring for paths outside it)."""

    root: str
    #: Every pattern kept, the file's first.
    patterns: tuple[str, ...]
    #: The file the patterns came from, if any (exported by `probe exec`).
    source_file: str | None = None
    #: How many of ``patterns`` came from the file.
    n_file: int = 0
    _spec: Any = field(default=None, repr=False, compare=False)
    _elsewhere: Any = field(default=None, repr=False, compare=False)
    _anywhere: Any = field(default=None, repr=False, compare=False)
    _cache: dict = field(default_factory=dict, repr=False, compare=False)
    #: Computed once, when first needed (`_link_targets`).
    _memo: dict = field(default_factory=dict, repr=False, compare=False)

    def ignored(
        self,
        path: str,
        *,
        base: str | None = None,
        is_dir: bool = False,
        capture_root: str | None = None,
        follow: bool = False,
    ) -> bool:
        """True when a pattern excludes ``path``.

        ``path`` is absolute, or relative to ``base`` (default: ``root``).
        ``is_dir`` lets a directory walk prune a whole directory (``data/``
        matches the directory itself). ``capture_root`` is the root of the
        capture asking (the output folder), for a path outside ``root``.
        ``follow`` is for a READ, which follows symlinks: the path is matched
        as opened, then resolved, then against where the root's excluded links
        lead (see the module docstring).
        """
        full = os.path.abspath(os.path.join(base or self.root, path))
        if capture_root is not None:
            capture_root = os.path.abspath(capture_root)
        if self._verdict(full, is_dir, capture_root):
            return True
        if not follow:
            return False
        real = _resolved(full)
        if real != full and self._verdict(real, is_dir, capture_root):
            return True
        targets = self._link_targets()
        return bool(targets) and any(real == t or real.startswith(t + os.sep) for t in targets)

    def _verdict(self, full: str, is_dir: bool, capture_root: str | None) -> bool:
        """The patterns against one absolute path (see the module docstring
        for where each applies)."""
        rel = _within(full, self.root)
        if rel is not None:
            return self._match(self._spec, ("root",), rel, is_dir)
        if capture_root is not None:
            rel = _within(full, capture_root)
            if rel is not None:
                return self._match(self._elsewhere, ("capture", capture_root), rel, is_dir)
        rel = os.path.splitdrive(full)[1].replace(os.sep, "/").lstrip("/")
        return bool(rel) and self._match(self._anywhere, ("anywhere",), rel, is_dir)

    def _link_targets(self) -> tuple[str, ...]:
        """Where the root's EXCLUDED symlinks lead, when that is outside the
        root: with ``bigdata/`` excluded and ``bigdata -> /mnt/big``, a loader
        that resolves the path first opens ``/mnt/big/x``, which no pattern
        names. Computed on first use and kept: one ``scandir`` of the root's
        top level (at most ``MAX_LINK_SCAN`` entries) plus one ``lstat`` per
        glob-free pattern, never a walk of the tree. A target holding the root
        itself (``up -> ..``) is never kept: it would exclude every read."""
        found = self._memo.get("links")
        if found is not None:
            return found
        root = self.root
        candidates: list[str] = []
        try:
            with os.scandir(root) as entries:
                for count, entry in enumerate(entries):
                    if count >= MAX_LINK_SCAN:
                        break
                    try:
                        if entry.is_symlink():
                            candidates.append(entry.path)
                    except OSError:
                        continue
        except OSError:
            pass
        for pattern in self.patterns:
            if pattern.startswith("!") or any(c in pattern for c in "*?[\\"):
                continue
            rel = pattern.strip("/")
            if rel:
                candidates.append(os.path.join(root, rel))
        real_root = _real_dir(root)
        targets: list[str] = []
        for candidate in dict.fromkeys(candidates):
            try:
                if not os.path.lexists(candidate):
                    continue
                real = os.path.realpath(candidate)
                if real == real_root or _under(real, real_root) is not None or _under(real_root, real) is not None:
                    continue  # inside the root (matched as resolved), or holding it
                if self._verdict(candidate, os.path.isdir(candidate), None):
                    targets.append(real.rstrip(os.sep) or real)
            except (OSError, ValueError):
                continue
            if len(targets) >= MAX_LINK_TARGETS:
                break
        found = self._memo["links"] = tuple(targets)
        return found

    def _match(self, spec: Any, key: tuple, rel: str, is_dir: bool) -> bool:
        """``spec`` against ``rel``, a parent folder first: a file under an
        excluded folder stays out whatever a later ``!`` says, as in git."""
        if spec is None:
            return False
        cache = self._cache
        if len(cache) > _CACHE_MAX:
            cache.clear()
        parts = rel.split("/")
        for depth in range(1, len(parts)):
            folder = "/".join(parts[:depth]) + "/"
            hit = cache.get((key, folder))
            if hit is None:
                hit = cache[(key, folder)] = bool(spec.match_file(folder))
            if hit:
                return True
        return bool(spec.match_file(rel + "/" if is_dir else rel))

    def unreachable(self, capture_root: str) -> tuple[str, ...]:
        """The file's anchored patterns, when ``capture_root`` lies outside
        ``root`` (they name places under ``root`` and cannot apply there)."""
        if _within(os.path.join(os.path.abspath(capture_root), "x"), self.root) is not None:
            return ()
        return tuple(p for p in self.patterns[: self.n_file] if _anchored(p))


def load(
    cwd: str | None = None,
    extra: Iterable[str] | None = None,
    *,
    environ: dict[str, str] | None = None,
) -> IgnoreRules | None:
    """The rules for a capture rooted at ``cwd``, or None when there are none.

    Never raises (nor blocks): an unreadable file, or one that is not a
    regular file, is no patterns and a warning, and a pattern ``pathspec``
    cannot compile (or `_too_costly` to match) is dropped with a warning rather
    than costing the capture.
    """
    env = os.environ if environ is None else environ
    here = os.path.abspath(cwd or os.getcwd())
    named = env.get(ENV_FILE)
    if named:
        source: str | None = os.path.abspath(named)
        root = os.path.dirname(source)
    else:
        root = _toplevel(here) or here
        source = os.path.join(root, IGNORE_FILE)
    from_file = _meaningful(_file_lines(source)) if source else []
    if not from_file:
        source = None
    others = _meaningful(
        [*split_patterns(env.get(ENV_PATTERNS)), *split_lines(env.get(ENV_EXPORTED)), *(extra or [])]
    )
    return _build(root, from_file, others, source, warn=True)


def _build(
    root: str, from_file: list[str], others: list[str], source: str | None, *, warn: bool
) -> IgnoreRules | None:
    """Compile the patterns into the three specs `IgnoreRules` matches with.
    Each pattern loses its trailing spaces first, as git reads it, so a stray
    space never changes where a pattern applies (`ckpt/ ` is `ckpt/`)."""
    from_file = [p for p in map(_trim_trailing_spaces, from_file) if p]
    others = [p for p in map(_trim_trailing_spaces, others) if p]
    patterns = [*from_file, *others]
    if not patterns:
        return None
    skipped: list[str] = []
    if len(patterns) > MAX_PATTERNS:
        skipped.extend(patterns[MAX_PATTERNS:])
    kept_file, kept_other = [], []
    for index, pattern in enumerate(patterns[:MAX_PATTERNS]):
        if _too_costly(pattern) or _compile((pattern,))[0] is None:
            skipped.append(pattern)
        else:
            (kept_file if index < len(from_file) else kept_other).append(pattern)
    if skipped and warn:
        _warn(
            f"probe: {len(skipped)} {IGNORE_FILE} pattern(s) are ignored (unreadable, too "
            f"costly to match, or past the first {MAX_PATTERNS}): "
            f"{', '.join(repr(p[:80]) for p in skipped[:5])}"
        )
    kept = (*kept_file, *kept_other)
    if not kept:
        return None
    elsewhere = [p for p in kept_file if not _anchored(p)] + kept_other
    anywhere = [p for p in kept if not _anchored(p)]
    return IgnoreRules(
        root=root,
        patterns=kept,
        source_file=source,
        n_file=len(kept_file),
        _spec=_compile(kept)[0],
        _elsewhere=_compile(tuple(elsewhere))[0] if elsewhere else None,
        _anywhere=_compile(tuple(anywhere))[0] if anywhere else None,
    )


def _compile(patterns: tuple[str, ...]) -> tuple[Any, list[str]]:
    """``(spec or None, patterns that would not compile)``. Never raises."""
    try:
        import pathspec
    except ImportError:
        return None, list(patterns)
    try:
        return pathspec.GitIgnoreSpec.from_lines(patterns), []
    except Exception:  # noqa: BLE001 -- one bad line may not cost the others
        pass
    good: list[str] = []
    bad: list[str] = []
    for pattern in patterns:
        try:
            pathspec.GitIgnoreSpec.from_lines([pattern])
            good.append(pattern)
        except Exception:  # noqa: BLE001
            bad.append(pattern)
    return (pathspec.GitIgnoreSpec.from_lines(good) if good else None), bad


def unseen_by_launcher(
    patterns: Iterable[str], rules: IgnoreRules | None, environ: dict[str, str] | None = None
) -> list[str]:
    """Those of a child's ``ignore=`` ``patterns`` its launcher never loaded:
    in neither the file it exported (``PROBE_IGNORE_FILE``), ``PROBE_IGNORE``
    nor its own exported ``ignore=``. The launcher's code snapshot, taken
    before the child started, could not have applied them."""
    env = os.environ if environ is None else environ
    known = {*split_patterns(env.get(ENV_PATTERNS)), *split_lines(env.get(ENV_EXPORTED))}
    if rules is not None and env.get(ENV_FILE):
        known.update(rules.patterns[: rules.n_file])
    known = {_trim_trailing_spaces(p) for p in known}
    return [p for p in patterns if _trim_trailing_spaces(p) and _trim_trailing_spaces(p) not in known]


@dataclass(frozen=True)
class AnyOf:
    """Several rule sets as one: a path any of them excludes is excluded. How
    a capture applies the rules another process of the run handed it (a
    ``probe exec`` child's ``ignore=``) beside its own."""

    rules: tuple[IgnoreRules, ...]

    def ignored(self, path: str, **kw: Any) -> bool:
        return any(rules.ignored(path, **kw) for rules in self.rules)


def combine(*rules: IgnoreRules | None) -> IgnoreRules | AnyOf | None:
    """``rules`` as one matcher (None dropped, duplicates once), or None."""
    kept = tuple(dict.fromkeys(r for r in rules if r is not None))
    if not kept:
        return None
    return kept[0] if len(kept) == 1 else AnyOf(kept)


def to_record(rules: IgnoreRules | None) -> dict[str, Any] | None:
    """What a recovery record stores, so a capture rebuilt in a fresh
    interpreter (a hard-death recovery) excludes exactly what the run did."""
    if rules is None:
        return None
    return {
        "root": rules.root,
        "patterns": list(rules.patterns),
        "source_file": rules.source_file,
        "n_file": rules.n_file,
    }


def from_record(record: Any) -> IgnoreRules | None:
    """The rules :func:`to_record` stored, or None. Never raises."""
    if not isinstance(record, dict):
        return None
    root = record.get("root")
    patterns = record.get("patterns")
    if not isinstance(root, str) or not isinstance(patterns, list):
        return None
    patterns_l = [p for p in patterns if isinstance(p, str)]
    source = record.get("source_file")
    source = source if isinstance(source, str) else None
    n_file = record.get("n_file")
    if not isinstance(n_file, int) or isinstance(n_file, bool) or not 0 <= n_file <= len(patterns_l):
        n_file = len(patterns_l) if source else 0
    try:
        return _build(root, patterns_l[:n_file], patterns_l[n_file:], source, warn=False)
    except Exception:  # noqa: BLE001 -- a record may never cost the recovery
        return None
