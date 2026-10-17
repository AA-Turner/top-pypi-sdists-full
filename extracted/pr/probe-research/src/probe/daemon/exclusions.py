"""`.probe.config` for the Probe daemon: an event about a path at `off` never
enters the session store; one about a path at `read` enters it tagged. A path
at `hash` is `off` here (`probe_config.daemon_view`): the SDK may record its
identity, the daemon never sees it.

Every transcript line the worker reads goes through `Worker._parse` and then
the store, and everything the daemon does -- its bites, its reader, its tools
over the store -- reads the store. So the filter sits in one place, between the
adapter and the store (`Filter.keep`), and the folder check skips excluded
files before it reads them (`Filter.path_excluded`).

An event is dropped when (`off`, as git closes an ignored folder):

- the folder it ran in is `off`: the transcript line's own `cwd`, a shell
  call's `workdir` (Codex), else where the session started;
- it is a tool call naming an `off` path (`file_path` / `path` / ..., a
  command token containing `/`, or a file a glob token like `a/*` expands to);
- it is the output of a call that was dropped -- in the same line, a later
  line, or after a restart (the dropped ids live in the store, `DROPPED_FACT`).

A tool's output that LISTS `off` files (`grep -rn`, `rg`, a search tool:
`path:line:text`, or a bare path per line) keeps its other lines; those lines
go. A bare file name in a command (`--out model.ckpt`) is not a place and does
not drop the call: dropping it would hide the run itself, and the CLI refuses
recording the excluded file.

A `read` path stays in the store, so the daemon understands the work: the call
naming it (or run in a `read` folder), its output, and an output listing it
carry `READ_NOTE` (`Event.note`), which the model sees with them. Nothing about
them is recorded: `precheck` refuses a write that names one.

Files above the session's launch folder are set aside only when the researcher
answered `ignore` for exactly them (`probe session parent`). The session's
transcript still uploads whole; this decides only what the daemon sees.
"""

from __future__ import annotations

import fnmatch
import logging
import os
import re
import shlex
import time
from pathlib import Path

from probe.daemon.events import Event, Kind
from probe.sdk import probe_config as pc

#: The store fact holding the ids of dropped calls whose output has not been
#: seen yet (`{call_id: offset}`), so the output is dropped too, across chunks
#: and restarts. The newest `MAX_DROPPED` are kept.
DROPPED_FACT = "probe_config_dropped_calls"
#: The `read`-tagged calls whose output has not been seen yet (`{call_id: [offset, note]}`).
READ_FACT = "probe_config_read_calls"
#: What the model sees with an event about a `read` path.
READ_NOTE = "`.probe.config` sets {paths} to read: Probe may look, records nothing about it."
#: A glob token in a command is expanded to at most this many files to check,
#: for at most this long (a `**` over a huge tree must not stall the worker).
MAX_GLOB_MATCHES = 20_000
GLOB_BUDGET_S = 0.5
#: Per stream: the last event read was a dropped call with no id (pi / Kimi
#: shell), whose output is the next output event on that stream.
BARE_FACT = "probe_config_bare:{stream}"
MAX_DROPPED = 2000
VIEW_TTL_S = 2.0
_PATH_KEYS = ("file_path", "path", "notebook_path", "filepath", "file", "target_file", "dir_path")
_TOKEN_RE = re.compile(r"""[^\s'"();|&<>`]+""")
_GLOB_CHARS = frozenset("*?[")
#: Characters a path in tool output is made of (no quotes, braces or spaces):
#: a JSON blob or a sentence is never taken for one.
_PATH_CHARS = r"[\w./~@+=,%-]"
#: `path:12:text`, `path-12-text`, `path:text` (grep / rg / a search tool).
_LISTED_RE = re.compile(rf"^(?P<path>(?:\.{{0,2}}/|~/)?{_PATH_CHARS}*/{_PATH_CHARS}*|{_PATH_CHARS}+\.\w+)(?::\d+[:\-]|-\d+-|:)")
#: A line that is nothing but a path (`rg -l`, `find`, `ls -d */x`).
_BARE_RE = re.compile(rf"^(?:\.{{0,2}}/|~/)?{_PATH_CHARS}*/{_PATH_CHARS}*$")
#: Over this, an output is scrubbed only when nothing below where it ran is
#: `off` (`pc.off_inside`); otherwise its text is replaced by a notice.
_MAX_OUTPUT_LINES = 50_000
#: A listing line's path prefix is looked for in this many characters (a long
#: line of data is not a path; the regex stays linear).
_LINE_HEAD = 1024
#: A tool call naming more places than this, where an `off` path is near, is
#: dropped: unchecked names fail closed.
MAX_NAMES = 5000
#: How long `pc.off_inside` answers are reused.
INSIDE_TTL_S = 5.0
#: Option names whose value is a file the program WRITES (`--out model.ckpt`): a
#: bare `off` name there is not a read, and dropping the call would hide the run.
_OUTPUT_OPTIONS = frozenset({"-o", "--out", "--output", "--output-dir", "--output_dir", "--save", "--save-to",
                             "--save_path", "--checkpoint", "--ckpt", "--log", "--logdir", "--log-dir",
                             "--dest", "--target"})
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
#: `==> path <==` (head / tail of several files).
_HEAD_RE = re.compile(r"^==> (?P<path>.+) <==$")
#: `--- path` / `+++ path` of a unified diff (`diff -u`, `git diff`).
_UNIFIED_RE = re.compile(r"^(?:---|\+\+\+) (?P<path>\S.*?)(?:\t.*)?$")
#: Prefixes git puts on a diff's paths (`a/`, `b/`; `i/`, `w/`, `c/`, `o/` with
#: `diff.mnemonicPrefix`).
_DIFF_PREFIXES = ("a/", "b/", "i/", "w/", "c/", "o/", "1/", "2/")

log = logging.getLogger("probe.daemon.exclusions")


class Filter:
    def __init__(self, store, session_id: str, cwd: Path | str | None) -> None:
        self.store = store
        self.session_id = session_id
        self.fallback = str(cwd) if cwd else None
        self._view_at = -1.0e9
        self._start: str | None = None
        self._skip: frozenset = frozenset()
        self._cache: dict[tuple, pc.Verdict] = {}
        self._dropped: dict | None = None  # DROPPED_FACT, loaded once, written on change
        self._read: dict | None = None  # READ_FACT, loaded once, written on change
        self._globs: dict[tuple, tuple[list[str], bool]] = {}  # expansions, cleared with the view
        self._bare: dict[str, bool] = {}
        self._bare_note: dict[str, str] = {}  # a `read` note for the next id-less output
        self._inside: dict[str, tuple[float, bool]] = {}  # pc.off_inside answers

    # -- the session's view ---------------------------------------------------

    def _view(self) -> tuple[str | None, frozenset]:
        now = time.monotonic()
        if now - self._view_at >= VIEW_TTL_S:
            try:
                from probe.sdk import session_marker

                start, skip = pc.session_view(session_marker.sessions_dir(), self.session_id)
            except Exception:  # noqa: BLE001 - a check never breaks the worker
                start, skip = None, frozenset()
            self._start, self._skip = start or self.fallback, skip
            self._view_at = now
            self._cache.clear()
            self._globs.clear()
        return self._start, self._skip

    def _verdict(self, path: str, *, where: str | None, as_cwd: bool = False) -> pc.Verdict:
        start, skip = self._view()
        key = (path, where, as_cwd)
        hit = self._cache.get(key)
        if hit is None:
            kw = {"skip": skip, "legacy": True, "ttl": VIEW_TTL_S}
            try:
                if as_cwd:
                    hit = pc.check_cwd(path, cwd=where or start, **kw)
                else:
                    hit = pc.check(path, cwd=where or start, **kw)
                # `hash` is `off` to the daemon: it never sees the path (C9).
                hit = pc.daemon_view(hit)
            except Exception:  # noqa: BLE001
                hit = pc.NOT_EXCLUDED
            if len(self._cache) > 20_000:
                self._cache.clear()
            self._cache[key] = hit
        return hit

    def _excluded(self, path: str, *, where: str | None, as_cwd: bool = False) -> bool:
        """Is `path` `off`: never even read?"""
        return self._verdict(path, where=where, as_cwd=as_cwd).hidden

    def checker(self, where: str | None) -> pc.Checker:
        """One batch of checks (an output's lines, a glob's matches)."""
        start, skip = self._view()
        return pc.Checker(cwd=where or start, skip=skip, legacy=True, ttl=VIEW_TTL_S, daemon=True)

    def path_excluded(self, path: str) -> bool:
        """For the folder check: is this file kept out of the record (`read` or
        `off`)? The check only finds files to record, so it skips both."""
        return self._verdict(path, where=None).excluded

    # -- events ---------------------------------------------------------------

    def _where(self, event: Event, line_cwd: str | None) -> str | None:
        workdir = event.tool_input.get("workdir") if event.tool_input else None
        start, _skip = self._view()
        if isinstance(workdir, str) and workdir:
            base = event.cwd or line_cwd or start
            return workdir if os.path.isabs(workdir) or not base else os.path.join(base, workdir)
        return event.cwd or line_cwd or start

    def _names(self, event: Event) -> list[str]:
        names: list[str] = []
        for key in _PATH_KEYS:
            value = event.tool_input.get(key)
            if isinstance(value, str) and value:
                names.append(value)
        command = event.command()
        if command:
            for token in _TOKEN_RE.findall(command):
                value = token.split("=", 1)[1] if token.startswith("-") and "=" in token else token
                if "/" in value and "://" not in value:
                    names.append(value)
        return names

    def off_inside(self, folder: str) -> bool:
        """`pc.off_inside` as this session sees the files, reused for INSIDE_TTL_S."""
        now = time.monotonic()
        hit = self._inside.get(folder)
        if hit is not None and now - hit[0] < INSIDE_TTL_S:
            return hit[1]
        _start, skip = self._view()
        answer = pc.off_inside(folder, skip=skip, legacy=True, ttl=VIEW_TTL_S)
        if len(self._inside) > 4096:
            self._inside.clear()
        self._inside[folder] = (now, answer)
        return answer

    def _reads_off(self, event: Event, where: str | None) -> bool:
        """Does the command read an `off` path its words never name as one: a
        file named bare (`cat secret.txt`), or a whole tree holding one (`rg x .`,
        `grep -r`, `find`, `git diff`)? Its output cannot be trusted to say."""
        command = event.command()
        if not command:
            return False
        start, _skip = self._view()
        files, trees = command_reads(command, where or start)
        checker = self.checker(where)
        if any(checker.check(path).hidden for path in files):
            return True
        if any(self.off_inside(tree) for tree in trees):
            return True
        return named_off(command, command_bases(command, where or start), checker, self._expanded)

    def _expanded(self, name: str, where: str | None) -> list[str]:
        """A glob token (`a/*`, `data/**/*.csv`) as the files it names now, at most
        MAX_GLOB_MATCHES; any other token as itself."""
        if _GLOB_CHARS.isdisjoint(name):
            return [name]
        start, _skip = self._view()
        base = where or start
        pattern = os.path.expanduser(name)
        if base and not os.path.isabs(pattern):
            pattern = os.path.join(base, pattern)
        key = (name, base)
        hit = self._globs.get(key)
        if hit is None:
            found, complete = _bounded_glob(pattern, time.monotonic() + GLOB_BUDGET_S, MAX_GLOB_MATCHES)
            hit = ([name, *found], complete)
            if len(self._globs) > 512:
                self._globs.clear()
            self._globs[key] = hit
        return hit[0]

    def _glob_cut_short(self, name: str, where: str | None) -> bool:
        """A glob that could not be expanded in full: what it skipped is unknown."""
        if _GLOB_CHARS.isdisjoint(name):
            return False
        self._expanded(name, where)
        start, _skip = self._view()
        base = where or start
        pattern = os.path.expanduser(name)
        if base and not os.path.isabs(pattern):
            pattern = os.path.join(base, pattern)
        hit = self._globs.get((name, base))
        return hit is not None and not hit[1]

    def _call_excluded(self, event: Event, where: str | None) -> bool:
        names = self._names(event)
        if len(names) > MAX_NAMES:
            return bool(where) and self.off_inside(where)  # too many to check: closed near an off path
        checker = self.checker(where)
        for name in names:
            if any(checker.check(path).hidden for path in self._expanded(name, where)):
                return True
            if self._glob_cut_short(name, where) and self.off_inside(_glob_base(name, where)):
                return True
        return self._reads_off(event, where)

    def _read_names(self, event: Event, where: str | None) -> list[str]:
        """The places a kept call names that are `read` (its folder included)."""
        out: list[str] = []
        if where and self._verdict(where, where=None, as_cwd=True).level == pc.READ:
            out.append(f"the folder it ran in ({pc.shown(where)})")
        checker = self.checker(where)
        for name in self._names(event):
            if any(checker.check(path).level == pc.READ for path in self._expanded(name, where)):
                out.append(f"`{name}`")
        command = event.command()
        if command:
            start, _skip = self._view()
            files, _trees = command_reads(command, where or start)
            for path in files:
                if checker.check(path).level == pc.READ and f"`{os.path.basename(path)}`" not in out:
                    out.append(f"`{os.path.basename(path)}`")
        return out

    def _scrub_output(self, event: Event, where: str | None) -> list[str]:
        """Drop the lines of an output that list an `off` file; the `read` files
        it lists, for the note."""
        text = event.text or ""
        if text.count("\n") >= _MAX_OUTPUT_LINES and where and self.off_inside(where):
            event.text = "[output removed: too long to check against .probe.config]"
            return []
        text, read = scrub_listing(text, self.checker(where))
        event.text = text
        return read

    def keep(self, events: list[Event], *, stream: str, line_cwd: str | None = None) -> list[Event]:
        """`events` minus what a `.probe.config` keeps from the daemon. Ids are
        assigned BEFORE this (`Worker._parse`), so a kept event's id never moves.
        Never raises."""
        try:
            return self._keep(events, stream=stream, line_cwd=line_cwd)
        except Exception as exc:  # noqa: BLE001 - fail closed: the tool events go, the rest stays
            log.warning("probe.config filter failed (%s); tool events of this line were dropped", type(exc).__name__)
            try:
                if self._dropped is not None:
                    for e in events:
                        if e.kind == Kind.TOOL_CALL and e.call_id:
                            self._dropped[e.call_id] = e.offset
                    self.store.set_fact(DROPPED_FACT, self._dropped)
            except Exception:  # noqa: BLE001
                pass
            return [e for e in events if e.kind not in (Kind.TOOL_CALL, Kind.TOOL_OUTPUT, Kind.FILE_CHANGE)]

    def _keep(self, events: list[Event], *, stream: str, line_cwd: str | None) -> list[Event]:
        if not events:
            return events
        if self._dropped is None:
            self._dropped = dict(self.store.fact(DROPPED_FACT, {}) or {})
        if self._read is None:
            self._read = dict(self.store.fact(READ_FACT, {}) or {})
        dropped_calls = self._dropped
        read_calls = self._read
        read_changed = False
        bare_key = BARE_FACT.format(stream=stream)
        if stream not in self._bare:
            self._bare[stream] = bool(self.store.fact(bare_key, False))
        bare = was_bare = self._bare[stream]
        changed = False
        kept: list[Event] = []
        for event in events:
            where = self._where(event, line_cwd)
            if event.kind == Kind.TOOL_OUTPUT:
                if event.call_id and event.call_id in dropped_calls:
                    dropped_calls.pop(event.call_id, None)
                    changed = True
                    continue
                if not event.call_id and bare:
                    bare = False
                    continue
                if not event.call_id and stream in self._bare_note:
                    event.note = self._bare_note.pop(stream)
            if event.kind == Kind.SUBAGENT and event.parent and event.parent in dropped_calls:
                continue
            excluded = bool(where) and self._excluded(where, where=None, as_cwd=True)
            if not excluded and event.kind == Kind.TOOL_CALL:
                excluded = self._call_excluded(event, where)
            if excluded:
                if event.kind == Kind.TOOL_CALL:
                    if event.call_id:
                        dropped_calls[event.call_id] = event.offset
                        changed = True
                    else:
                        bare = True
                continue
            if event.kind == Kind.TOOL_CALL:
                bare = False
                self._bare_note.pop(stream, None)
                names = self._read_names(event, where)
                if names:
                    event.note = _read_note(names)
                    if event.call_id:
                        read_calls[event.call_id] = [event.offset, event.note]
                        read_changed = True
                    else:
                        self._bare_note[stream] = event.note
            if event.kind == Kind.TOOL_OUTPUT:
                listed = self._scrub_output(event, where)
                tagged = read_calls.pop(event.call_id, None) if event.call_id else None
                if tagged is not None:
                    read_changed = True
                if listed:
                    event.note = _read_note(listed)
                elif tagged is not None:
                    event.note = tagged[1]
                if event.note is None and event.text and where and \
                        self._verdict(where, where=None, as_cwd=True).level == pc.READ:
                    event.note = _read_note([f"the folder it ran in ({pc.shown(where)})"])
            kept.append(event)
        if changed:
            if len(dropped_calls) > MAX_DROPPED:
                newest = sorted(dropped_calls.items(), key=lambda kv: kv[1])[-MAX_DROPPED:]
                dropped_calls.clear()
                dropped_calls.update(newest)
            self.store.set_fact(DROPPED_FACT, dropped_calls)
        if read_changed:
            if len(read_calls) > MAX_DROPPED:
                newest = sorted(read_calls.items(), key=lambda kv: kv[1][0])[-MAX_DROPPED:]
                read_calls.clear()
                read_calls.update(newest)
            self.store.set_fact(READ_FACT, read_calls)
        if bare != was_bare:
            self._bare[stream] = bare
            self.store.set_fact(bare_key, bare)
        return kept


def scrub_listing(text: str, checker: pc.Checker) -> tuple[str, list[str]]:
    """`text` minus what it shows of `off` files, and the `read` files it names.
    Used on the agent's outputs and on the daemon's own shell's.

    A line naming an `off` file goes (`path:line:text`, a bare path, an
    `rg --json` line, a NUL-separated list); so does every line of a section
    headed by one: a diff's file (`diff --git`, `---` / `+++`, any prefix,
    colours stripped), `==> path <==`, or a bare path line (`rg --heading`)
    until a blank line or the next path. A BACKSTOP: an output that never names
    the file it shows (`rg -I`, a script) gets past it, which is why a command
    reading a tree holding an `off` path is dropped whole (`command_reads`)."""
    if not text:
        return text, []
    lines = text.split("\n")
    kept: list[str] = []
    read: list[str] = []
    dropped = 0
    section: str | None = None  # "diff" | "head" | "heading": a hidden section's kind

    def level(candidate: str) -> str:
        candidate = candidate.strip().strip('"')
        if not candidate:
            return pc.ON
        verdict = checker.check(candidate)
        if verdict.level == pc.READ and f"`{candidate}`" not in read:
            read.append(f"`{candidate}`")
        return verdict.level

    def diff_off(names: list[str]) -> bool:
        out = []
        for name in names:
            out.append(name)
            for prefix in _DIFF_PREFIXES:
                if name.startswith(prefix):
                    out.append(name[len(prefix):])
        return any(level(p) == pc.OFF for p in _diff_paths(out, checker))

    for k, raw in enumerate(lines):
        line = _ANSI_RE.sub("", raw) if "\x1b" in raw else raw
        head = line[:_LINE_HEAD]
        if head.startswith("diff "):
            rest = head.split(None, 1)[1] if " " in head else ""
            words = [w for w in shlex_split(rest) if not w.startswith("-")]
            section = "diff" if diff_off(words[-2:]) else None
            if section:
                dropped += 1
                continue
            kept.append(raw)
            continue
        unified = _UNIFIED_RE.match(head)
        if unified and unified.group("path") != "/dev/null":
            if diff_off([unified.group("path")]):
                section = "diff"
        named = _HEAD_RE.match(head)
        if named:
            section = "head" if level(named.group("path")) == pc.OFF else None
            if section:
                dropped += 1
                continue
        if section == "heading" and (not line.strip() or _BARE_RE.match(line.strip()) or _LISTED_RE.match(head)):
            section = None
        if section:
            dropped += 1
            continue
        if "\0" in line:  # `find -print0`, `rg -0`: `path\0rest`
            first = line.split("\0", 1)[0]
            if first.strip() and level(first) == pc.OFF:
                dropped += 1
                continue
            parts = line.split("\0")
            shown = [p for p in parts if not (p.strip() and _is_path(p.strip()) and level(p) == pc.OFF)]
            if len(shown) != len(parts):
                dropped += len(parts) - len(shown)
                raw = "\0".join(shown)
        candidate = None
        match = _LISTED_RE.match(head)
        if match:
            candidate = match.group("path")
        elif _BARE_RE.match(line.strip()) or _NAME_RE.match(line.strip()):
            candidate = line.strip()
            if level(candidate) == pc.OFF:
                # `rg --heading -n`: the numbered lines under it are that file's. A
                # bare path followed by anything else (a `cat .probe.config`, an
                # `ls`) is one line: only it goes, or the rest of the output would.
                following = lines[k + 1] if k + 1 < len(lines) else ""
                if _NUMBERED_RE.match(_ANSI_RE.sub("", following)):
                    section = "heading"
                dropped += 1
                continue
            candidate = None
        else:
            spaced = _SPACED_RE.match(head)  # `secret/my file.txt:1:text`
            json_path = _JSON_PATH_RE.search(head)  # `rg --json`
            if spaced:
                candidate = spaced.group("path")
            elif json_path:
                candidate = json_path.group(1).replace('\\"', '"').replace("\\\\", "\\")
        if candidate and level(candidate) == pc.OFF:
            dropped += 1
            continue
        kept.append(raw)
    if dropped:
        kept.append(f"[{dropped} line(s) about paths a .probe.config excludes were removed]")
        return "\n".join(kept), read
    return text, read


def shlex_split(text: str) -> list[str]:
    try:
        return shlex.split(text)
    except ValueError:
        return text.split()


def _command_tokens(command: str) -> list[str]:
    """The words of a shell command with its operators split out as words of their
    own, stuck or not (`cd /o;rg` is `cd`, `/o`, `;`, `rg`), newlines as `;`."""
    try:
        lexer = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        return list(lexer)
    except ValueError:
        return command.split()


def _operator(token: str) -> bool:
    return token in _SEPARATORS or bool(token) and set(token) <= set("&|;()")


#: Programs that read the files they are given (a bare name included: `cat secret.txt`).
_FILE_READERS = frozenset({
    "cat", "head", "tail", "less", "more", "bat", "batcat", "nl", "wc", "sort", "uniq", "cut", "awk",
    "gawk", "sed", "xxd", "od", "hexdump", "strings", "jq", "yq", "cmp", "diff", "file", "md5sum",
    "sha1sum", "sha224sum", "sha256sum", "sha384sum", "sha512sum", "b2sum", "cksum", "shasum", "base64",
    "tac", "grep", "egrep", "fgrep", "rg", "ag", "ack",
    "cp", "mv", "tar", "zip", "gzip", "gunzip", "zcat", "column", "fold", "paste", "iconv", "openssl", "pdftotext",
})
#: Programs that read a whole tree when given a folder (or the current one).
_TREE_READERS = frozenset({"rg", "ag", "ack", "find", "fd", "fdfind", "tree", "du"})
#: Wrappers whose arguments are the real command.
_WRAPPERS = frozenset({"sudo", "time", "nice", "nohup", "command", "builtin", "exec", "stdbuf", "timeout"})
_SEPARATORS = frozenset({"&&", "||", "|", ";", "&", "(", ")", "|&", "\n"})

#: git verbs that print files' contents or names from the whole repository.
_GIT_TREE_VERBS = frozenset({"diff", "show", "grep", "ls-files", "status", "whatchanged", "archive", "ls-tree"})
_GIT_LOG_PATCH = ("-p", "--patch", "-u", "--stat", "--numstat", "--shortstat", "--name-only",
                  "--name-status", "--raw", "--summary", "--full-diff", "--cc", "-c")


#: The long options of a tree reader that take the next word as their value, so the
#: tree it walks may be the current folder's (GNU's, which reads any unambiguous start
#: of a long option: `--ig` is `--ignore`).
_VALUE_LONGS = {
    "ls": ("--ignore", "--hide", "--time-style", "--format", "--sort", "--width", "--tabsize", "--quoting-style",
           "--indicator-style", "--block-size", "--time"),
    "du": ("--block-size", "--max-depth", "--threshold", "--exclude", "--time-style"),
}
#: Their short options that take a value, GNU's and BSD's (BSD ls `-D FORMAT`, BSD du
#: `-I MASK`): in a cluster the rest of it, or the next word, is the value.
_VALUE_LETTERS = {"ls": "DITw", "du": "BIXdt"}
#: A word of find's leading options (as `shell._FIND_LEADING`): GNU's -H -L -P, BSD's
#: -E -X -d -s -x, in a cluster, ending in BSD's -f whose value is a start folder.
_FIND_LEADING = re.compile(r"-([EHLPXdsx]*)(?:f(.*))?")


def _spells(word: str, name: str) -> bool:
    """Whether `word` is the long option `name`, or a start of it GNU reads as it."""
    given = word.split("=", 1)[0]
    return word.startswith("--") and len(given) > 2 and name.startswith(given)


def drops_file_names(command: str) -> bool:
    """Whether an rg or grep in `command` prints matches without the names of the
    files they came from (`rg -I` / `--no-filename`, `grep -h` / `--no-filename`),
    which the output filter goes by. Read broadly: any word of such a part."""
    letter = {"rg": "I", "grep": "h", "egrep": "h", "fgrep": "h"}
    program = None
    for word in _command_tokens(command):
        if _operator(word):
            program = None
        elif program is None:
            if not (word in _WRAPPERS or word == "env" or ("=" in word and not word.startswith("-"))):
                program = os.path.basename(word)  # past `sudo`, `env X=1`, as `command_reads` reads it
        elif program in letter and word.startswith("-") and word != "-":
            if word.startswith("--") and _spells(word, "--no-filename"):
                return True
            if not word.startswith("--") and letter[program] in word[1:]:
                return True
    return False


def _no_name_left(program: str, args: list[str]) -> bool:
    """ls / du: whether, with every word an option may take as its value taken (after
    a long one, `--ig /tmp`; after a short cluster ending in a value letter,
    `-RaI /tmp`), no name is left, so the tree it walks is the current folder."""
    skip = names_only = False
    for a in args:
        if skip:
            skip = False
        elif names_only or a == "-" or not a.startswith("-"):
            return False
        elif a == "--":
            names_only = True
        elif a.startswith("--"):
            skip = "=" not in a and any(_spells(a, name) for name in _VALUE_LONGS[program])
        else:
            skip = a[-1] in _VALUE_LETTERS[program]
    return True


def _find_starts(args: list[str]) -> tuple[list[str], bool]:
    """find's start folders, past its leading options (-H -L -P -D X -Olevel, BSD's
    flags and `-f PATH`) and a `--`; and whether it may walk `.` as well (`-fstype`
    is GNU's test, BSD's `-f stype`)."""
    starts: list[str] = []
    walks_here = False
    k = 0
    while k < len(args):
        a = args[k]
        if a == "--":
            k += 1
            break
        if a == "-D":
            k += 2
            continue
        if a.startswith("-O"):
            k += 1
            continue
        flags = _FIND_LEADING.fullmatch(a)
        if not flags or not (flags.group(1) or flags.group(2) is not None):
            break
        k += 1
        if flags.group(2):
            starts.append(flags.group(2))
            walks_here = True
        elif flags.group(2) is not None and k < len(args):
            starts.append(args[k])
            k += 1
    while k < len(args) and not args[k].startswith(("-", "(", "!", ")", ",")):
        starts.append(args[k])
        k += 1
    return starts, walks_here


def _grep_recurses(args: list[str]) -> bool:
    """grep -r / -R in any spelling, or `-d` / `--directories` with anything but
    `read` or `skip` (GNU takes any start of `recurse`, BSD any case)."""
    for k, a in enumerate(args):
        if a == "--":
            break
        if not a.startswith("-") or a == "-":
            continue
        following = args[k + 1] if k + 1 < len(args) else ""
        if a.startswith("--"):
            if _spells(a, "--recursive") or _spells(a, "--dereference-recursive"):
                return True
            if _spells(a, "--directories") and (a.split("=", 1)[1] if "=" in a else following) not in ("read", "skip"):
                return True
            continue
        if "r" in a[1:] or "R" in a[1:]:
            return True
        for i, letter in enumerate(a[1:]):
            if letter == "d":
                if (a[i + 2 :] or following) not in ("read", "skip"):
                    return True
                break
            if letter in "efmABCD":  # the rest of the word is this option's value
                break
    return False


def command_reads(command: str, cwd: str | None) -> tuple[list[str], list[str]]:
    """`(files, trees)` a shell command reads, as far as its words say: files a
    reader is given (`cat secret.txt`, a bare name included), and folders a tree
    reader walks (`rg x .`, `grep -r`, `find`, `ls -R`, `diff -r`, a repo-wide
    `git diff` / `git show` / `git status` / `git log -p`), in every folder a `cd`
    may have left it in, as bash runs it: after `&&` the folder the `cd` reached;
    after `;`, `||` or a newline any folder reached so far (the `cd` may have
    failed); and a `cd` in a pipeline moves nothing (each side is a subshell:
    `cd /x | rg -I KEY .` searches here), but as the pipeline's last part under
    `shopt -s lastpipe` it runs in this shell, so what follows may run in its
    folder too (`true | cd /x; rg .`). Paths that do not exist are left out (a
    bare word is a word). Never raises."""
    files: list[str] = []
    trees: list[str] = []
    start = cwd or os.getcwd()
    segments: list[tuple[str, list[str]]] = [("", [])]  # (the operator before it, its words)
    for token in _command_tokens(command):
        if _operator(token):
            segments.append((token, []))
        else:
            segments[-1][1].append(token)
    seen, success, previous = [start], [start], [start]
    for k, (before, words) in enumerate(segments):
        if before == "&&":
            heres = success
        elif before in ("|", "|&"):
            heres = previous
        else:
            heres = list(seen)
        piped = before in ("|", "|&") or (k + 1 < len(segments) and segments[k + 1][0] in ("|", "|&"))
        previous = heres
        success = heres
        while words and ("=" in words[0] and not words[0].startswith("-") or words[0] in _WRAPPERS
                         or words[0] == "env"):
            words = words[1:]
        if not words:
            continue
        program = os.path.basename(words[0])
        args = words[1:]
        if program in ("cd", "pushd", "popd"):
            target = next((a for a in args if not a.startswith("-")), None)
            if program == "popd" or args[:1] == ["-"]:
                moved = list(seen)  # back to a folder seen before
            else:
                target = os.path.expanduser(target if target is not None else "~")  # a bare `cd` goes home
                moved = [os.path.normpath(os.path.join(here, target)) for here in heres]
            # In a pipeline the `cd` runs in a subshell and moves nothing -- unless it is
            # the last part under `shopt -s lastpipe`, which runs it in this shell: there
            # its folder is one more the later parts may run in, never the only one.
            success = [*heres, *(f for f in moved if f not in heres)] if piped else moved
            seen += [folder for folder in moved if folder not in seen]
            continue
        for here in heres:
            _part_reads(program, args, here, files, trees)
    return files, trees


def _part_reads(program: str, args: list[str], here: str, files: list[str], trees: list[str]) -> None:
    """`command_reads` for one command, run in `here`."""
    options = [a for a in args if a.startswith("-") and a != "-"]
    positional = [a for a in args if not a.startswith("-")]
    if program == "git":
        git_reads(args, here, files, trees)
        return
    recursive = program in _TREE_READERS or (
        program in ("grep", "egrep", "fgrep") and _grep_recurses(args)
    ) or (program == "ls" and any(_spells(o, "--recursive") or (not o.startswith("--") and "R" in o[1:])
                                  for o in options)) \
        or (program == "diff" and any(o == "-r" or _spells(o, "--recursive")
                                      or (not o.startswith("--") and "r" in o[1:]) for o in options))
    walks_here = recursive and program in _VALUE_LONGS and _no_name_left(program, args)
    if program == "find":  # start folders come before the expression
        positional, walks_find = _find_starts(args)
        walks_here = walks_here or walks_find
    # Option values and patterns are positional words too; which word is a
    # path is not knowable without each program's option table, so: the
    # words that exist are what is read, and with none, the folder it runs in.
    paths = [os.path.join(here, os.path.expanduser(a)) for a in positional]
    existing = [p for p in paths if os.path.lexists(p)]
    if recursive:
        folders = [p for p in existing if os.path.isdir(p)]
        if folders:
            trees.extend(folders)
        elif program != "diff" and not [p for p in existing if not os.path.isdir(p)]:
            trees.append(here)
        if walks_here and here not in trees:
            trees.append(here)
    if program in _FILE_READERS or recursive:
        files.extend(p for p in existing if not os.path.isdir(p))


def command_bases(command: str, cwd: str | None) -> list[str]:
    """Every folder a word of `command` could be relative to: where it ran, and
    each `cd` / `pushd` / `git -C` target in it (a subshell's `cd` included, as
    a `(cd x); cat y` reads `y` where it ran, but a `cd x && cat y` in x)."""
    here = cwd or os.getcwd()
    bases = [here]
    words = _command_tokens(command)  # `cd /o;rg`: the folder is `/o`, not `/o;`
    for k, word in enumerate(words):
        if word in ("cd", "pushd", "-C"):
            target = words[k + 1] if k + 1 < len(words) else ""
            if not target or _operator(target):
                if word == "-C":
                    continue
                target = "~"  # a bare `cd` goes home
            for base in list(bases):
                folder = os.path.normpath(os.path.join(base, os.path.expanduser(target)))
                if folder not in bases:
                    bases.append(folder)
    return bases


def named_off(command: str, bases: list[str], checker: pc.Checker, expand) -> bool:
    """Does any word of `command` (unquoted, wherever it sits: after `|`, in
    backticks, in a here-string) name or glob an existing `off` file, relative to
    any of `bases`? A file a program is told to WRITE (`--out model.ckpt`, after
    `>`) is not a read. A word that names nothing that exists is a word."""
    words = shlex_split(command.replace("\n", " ; "))
    seen: set[str] = set()
    for k, word in enumerate(words):
        prev = words[k - 1] if k else ""
        if prev in _OUTPUT_OPTIONS or prev in (">", ">>", "&>", "2>", "1>") or prev.endswith(">"):
            continue
        if word.startswith("-") and "=" in word:
            name, word = word.split("=", 1)
            if name in _OUTPUT_OPTIONS:
                continue
        for piece in [word, *[p for p in re.split(r"[`$()<>|;&]", word) if p and p != word]]:
            piece = piece.strip("'\"")
            if not piece or piece in seen or "://" in piece:
                continue
            seen.add(piece)
            for base in bases:
                candidates = expand(piece, base) if not _GLOB_CHARS.isdisjoint(piece) else [piece]
                for cand in candidates:
                    full = cand if os.path.isabs(os.path.expanduser(cand)) else os.path.join(base, cand)
                    full = os.path.expanduser(full)
                    if os.path.lexists(full) and checker.check(full).hidden:
                        return True
    return False


def _glob_base(name: str, where: str | None) -> str:
    """The folder a glob starts in: its words before the first wildcard."""
    head = []
    for part in os.path.expanduser(name).split(os.sep):
        if not _GLOB_CHARS.isdisjoint(part):
            break
        head.append(part)
    base = os.sep.join(head) or "."
    return base if os.path.isabs(base) else os.path.join(where or os.getcwd(), base)


def git_reads(args: list[str], here: str, files: list[str], trees: list[str]) -> None:
    """What a git command reads, for `command_reads`."""
    k = 0
    while k < len(args) and args[k].startswith("-"):
        if args[k] == "-C" and k + 1 < len(args):
            here = os.path.normpath(os.path.join(here, os.path.expanduser(args[k + 1])))
            k += 2
            continue
        k += 2 if args[k] in ("-c", "--git-dir", "--work-tree") else 1
    if k >= len(args):
        return
    verb, rest = args[k], args[k + 1:]
    root = _repo_root(here) or here
    for word in rest:  # `REV:path`: root-relative (`./path`: here-relative)
        if ":" in word and not word.startswith("-") and not word.startswith(":"):
            name = word.split(":", 1)[1]
            if name:
                base = here if name.startswith("./") else root
                files.append(os.path.normpath(os.path.join(base, name)))
    if verb == "log" and not any(o in _GIT_LOG_PATCH or o.startswith(("--stat", "-p")) for o in rest):
        return
    if verb not in _GIT_TREE_VERBS and verb not in ("log", "blame", "cat-file"):
        return
    spec = rest[rest.index("--") + 1:] if "--" in rest else [w for w in rest if not w.startswith("-")]
    named = [os.path.join(here, os.path.expanduser(w)) for w in spec if ":" not in w]
    named = [p for p in named if os.path.lexists(p)]
    if named:
        trees.extend(p for p in named if os.path.isdir(p))
        files.extend(p for p in named if not os.path.isdir(p))
    elif verb in _GIT_TREE_VERBS or verb == "log":
        trees.append(root)


#: A numbered match line under an `rg --heading -n` / `grep` heading.
_NUMBERED_RE = re.compile(r"^\d+[:\-]")
#: A line that is one file name and nothing else (`rg --heading` in the folder itself).
_NAME_RE = re.compile(rf"^{_PATH_CHARS}+\.\w+$")
#: `path with spaces/x.txt:12:text` (a listing line whose path has a space).
_SPACED_RE = re.compile(r"^(?P<path>[^\0:]*/[^\0:]*?)(?::\d+[:\-]|-\d+-)")


#: `"path":{"text":"..."}` in an `rg --json` line.
_JSON_PATH_RE = re.compile(r'"path":\{"text":"((?:[^"\\]|\\.)*)"')


def _is_path(text: str) -> bool:
    return bool(_BARE_RE.match(text) or "/" in text)


def _diff_paths(names: list[str], checker: pc.Checker) -> list[str]:
    """A diff section's file, as places to check: relative to the folder the
    command ran in and to the repository it is in (git prints root-relative)."""
    base = checker.cwd or os.getcwd()
    roots = [base]
    root = _repo_root(base)
    if root and root != base:
        roots.append(root)
    return [name if os.path.isabs(name) else os.path.join(r, name) for name in names for r in roots]


def _repo_root(folder: str) -> str | None:
    current = folder
    while True:
        if os.path.exists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _bounded_glob(pattern: str, deadline: float, cap: int) -> tuple[list[str], bool]:
    """`(files, finished)`: the files `pattern` names (`*`, `?`, `[..]` per
    folder, `**` across folders), visiting entries one at a time only until
    `deadline` and `cap`. `finished` False: what it did not visit is unknown, and
    the caller fails closed."""
    parts = [p for p in pattern.split(os.sep) if p]
    root = os.sep if pattern.startswith(os.sep) else ""
    out: list[str] = []
    state = {"finished": True}

    def over() -> bool:
        if len(out) >= cap or time.monotonic() > deadline:
            state["finished"] = False
            return True
        return False

    def entries(folder: str):
        try:
            with os.scandir(folder or ".") as it:
                for entry in it:
                    if over():
                        return
                    yield entry
        except OSError:
            return

    def walk(folder: str, i: int) -> None:
        if over():
            return
        if i == len(parts):
            if os.path.lexists(folder):
                out.append(folder)
            return
        part = parts[i]
        if part == "**":
            walk(folder, i + 1)
            for entry in entries(folder):
                try:
                    if entry.is_dir(follow_symlinks=False) and not entry.name.startswith("."):
                        walk(os.path.join(folder, entry.name), i)
                except OSError:
                    continue
            return
        if not any(c in part for c in "*?["):
            walk(os.path.join(folder, part), i + 1)
            return
        for entry in entries(folder):
            name = entry.name
            if fnmatch.fnmatchcase(name, part) and (part.startswith(".") or not name.startswith(".")):
                walk(os.path.join(folder, name), i + 1)

    try:
        walk(root, 0)
    except (RecursionError, ValueError, OSError):
        return out, False
    return out, state["finished"]



def _read_note(names: list[str]) -> str:
    shown = ", ".join(names[:3]) + (f" and {len(names) - 3} more" if len(names) > 3 else "")
    return READ_NOTE.format(paths=shown)
