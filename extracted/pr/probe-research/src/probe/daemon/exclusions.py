"""`.probe.config` for the Probe daemon: an event about a path Probe never
records never enters the session store.

Every transcript line the worker reads goes through `Worker._parse` and then
the store, and everything the daemon does -- its bites, its reader, its tools
over the store -- reads the store. So the filter sits in one place, between the
adapter and the store (`Filter.keep`), and the folder check skips excluded
files before it reads them (`Filter.path_excluded`).

An event is dropped when:

- the folder it ran in is excluded: the transcript line's own `cwd`, a shell
  call's `workdir` (Codex), else where the session started;
- it is a tool call naming an excluded path (`file_path` / `path` / ...,
  or a command token containing `/`);
- it is the output of a call that was dropped -- in the same line, a later
  line, or after a restart (the dropped ids live in the store, `DROPPED_FACT`).

A tool's output that LISTS excluded files (`grep -rn`, `rg`, a search tool:
`path:line:text`, or a bare path per line) keeps its other lines; those lines
go. A bare file name in a command (`--out model.ckpt`) is not a place and does
not drop the call: dropping it would hide the run itself, and the CLI refuses
recording the excluded file.

Files above the session's launch folder are set aside only when the researcher
answered `ignore` for exactly them (`probe session parent`). The session's
transcript still uploads whole; this decides only what the daemon sees.
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

from probe.daemon.events import Event, Kind
from probe.sdk import probe_config as pc

#: The store fact holding the ids of dropped calls whose output has not been
#: seen yet (`{call_id: offset}`), so the output is dropped too, across chunks
#: and restarts. The newest `MAX_DROPPED` are kept.
DROPPED_FACT = "probe_config_dropped_calls"
#: Per stream: the last event read was a dropped call with no id (pi / Kimi
#: shell), whose output is the next output event on that stream.
BARE_FACT = "probe_config_bare:{stream}"
MAX_DROPPED = 2000
VIEW_TTL_S = 2.0
_PATH_KEYS = ("file_path", "path", "notebook_path", "filepath", "file", "target_file", "dir_path")
_TOKEN_RE = re.compile(r"""[^\s'"();|&<>`]+""")
#: Characters a path in tool output is made of (no quotes, braces or spaces):
#: a JSON blob or a sentence is never taken for one.
_PATH_CHARS = r"[\w./~@+=,%-]"
#: `path:12:text`, `path-12-text`, `path:text` (grep / rg / a search tool).
_LISTED_RE = re.compile(rf"^(?P<path>(?:\.{{0,2}}/|~/)?{_PATH_CHARS}*/{_PATH_CHARS}*|{_PATH_CHARS}+\.\w+)(?::\d+[:\-]|-\d+-|:)")
#: A line that is nothing but a path (`rg -l`, `find`, `ls -d */x`).
_BARE_RE = re.compile(rf"^(?:\.{{0,2}}/|~/)?{_PATH_CHARS}*/{_PATH_CHARS}*$")
_MAX_OUTPUT_LINES = 5000


class Filter:
    def __init__(self, store, session_id: str, cwd: Path | str | None) -> None:
        self.store = store
        self.session_id = session_id
        self.fallback = str(cwd) if cwd else None
        self._view_at = -1.0e9
        self._start: str | None = None
        self._skip: frozenset = frozenset()
        self._cache: dict[tuple, bool] = {}
        self._dropped: dict | None = None  # DROPPED_FACT, loaded once, written on change
        self._bare: dict[str, bool] = {}

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
        return self._start, self._skip

    def _excluded(self, path: str, *, where: str | None, as_cwd: bool = False) -> bool:
        start, skip = self._view()
        key = (path, where, as_cwd)
        hit = self._cache.get(key)
        if hit is None:
            kw = {"skip": skip, "legacy": True, "ttl": VIEW_TTL_S}
            try:
                if as_cwd:
                    hit = pc.check_cwd(path, cwd=where or start, **kw).excluded
                else:
                    hit = pc.check(path, cwd=where or start, **kw).excluded
            except Exception:  # noqa: BLE001
                hit = False
            if len(self._cache) > 20_000:
                self._cache.clear()
            self._cache[key] = hit
        return hit

    def path_excluded(self, path: str) -> bool:
        """For the folder check: is this file excluded?"""
        return self._excluded(path, where=None)

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
        return names[:64]

    def _call_excluded(self, event: Event, where: str | None) -> bool:
        return any(self._excluded(name, where=where) for name in self._names(event))

    def _scrub_output(self, event: Event, where: str | None) -> None:
        """Drop the lines of an output that list an excluded file."""
        text = event.text
        if not text or "/" not in text and ":" not in text:
            return
        lines = text.split("\n")
        if len(lines) > _MAX_OUTPUT_LINES:
            return
        kept: list[str] = []
        dropped = 0
        for line in lines:
            candidate = None
            match = _LISTED_RE.match(line)
            if match:
                candidate = match.group("path")
            elif _BARE_RE.match(line.strip()):
                candidate = line.strip()
            if candidate and self._excluded(candidate, where=where):
                dropped += 1
                continue
            kept.append(line)
        if dropped:
            kept.append(f"[{dropped} line(s) about paths a .probe.config excludes were removed]")
            event.text = "\n".join(kept)

    def keep(self, events: list[Event], *, stream: str, line_cwd: str | None = None) -> list[Event]:
        """`events` minus what a `.probe.config` keeps from the daemon. Ids are
        assigned BEFORE this (`Worker._parse`), so a kept event's id never moves.
        Never raises."""
        try:
            return self._keep(events, stream=stream, line_cwd=line_cwd)
        except Exception:  # noqa: BLE001 - a broken check never hides the session
            return events

    def _keep(self, events: list[Event], *, stream: str, line_cwd: str | None) -> list[Event]:
        if not events:
            return events
        if self._dropped is None:
            self._dropped = dict(self.store.fact(DROPPED_FACT, {}) or {})
        dropped_calls = self._dropped
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
            if event.kind == Kind.TOOL_OUTPUT:
                self._scrub_output(event, where)
            kept.append(event)
        if changed:
            if len(dropped_calls) > MAX_DROPPED:
                newest = sorted(dropped_calls.items(), key=lambda kv: kv[1])[-MAX_DROPPED:]
                dropped_calls.clear()
                dropped_calls.update(newest)
            self.store.set_fact(DROPPED_FACT, dropped_calls)
        if bare != was_bare:
            self._bare[stream] = bare
            self.store.set_fact(bare_key, bare)
        return kept
