"""before a writer run, check out the summary of every entity the session's writes touched."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.agent.tools.drafts import (
    SUMMARY_DRAFTS,
    SUMMARY_DRAFTS_KEPT,
    _bound_drafts,
    _draft_dirty,
    _drafts,
    _remember_note,
    _remember_refused,
)


# ---------------------------------------------------------------------------
# Loading the writer's summaries (ARTIFACT-PAGES P3): checked out by the worker
# before a run, shown as outlines, edited in place.
# ---------------------------------------------------------------------------

#: The most the worker spends loading summaries before a run, version reads
#: and checkouts together (review of #3034, finding 5): past it the run goes
#: on with what is on disk.
AUTOLOAD_TIMEOUT_S = 20.0
#: Logbook rows looked at for what the session wrote (newest first).
_TOUCH_ROWS = 400


def _probe_words(argv_json: str) -> list[str] | None:
    try:
        argv = json.loads(argv_json)
    except ValueError:
        return None
    if not isinstance(argv, list) or not argv or argv[0] != "probe":
        return None
    return [str(a) for a in argv[1:]]


def touched_entities(store, *, limit: int = SUMMARY_DRAFTS_KEPT) -> list[tuple[str, str, float]]:
    """`(kind, ref, at)` of each project and experiment this session's writes
    landed on or created, newest first, at most `limit`. From the LOGBOOK --
    the writes the daemon ran, each read by the CLI's own parse of its
    arguments (`summary_cli.landing`; an experiment created under a project
    touches both) -- never from the status line's resolver, which collapses an
    experiment to its project."""
    from probe.shared.notes import summary as summary_cli

    seen: dict[tuple[str, str], float] = {}
    rows = store.db.execute("SELECT argv, at FROM writes WHERE status = 'ran' ORDER BY id DESC LIMIT ?",
                            (_TOUCH_ROWS,))
    for row in rows:
        words = _probe_words(row["argv"])
        if not words:
            continue
        found = summary_cli.landing(words)
        hits = [found] if found else []
        if found and found[0] == summary_cli.EXPERIMENT:
            try:
                parsed = precheck.parse(words)
            except precheck.ParseError:
                parsed = None
            if parsed is not None and parsed.path == "experiment create":
                parent = next((v for v in precheck._strings(parsed.params.get("project")) if v.strip()), None)
                if parent:
                    hits.append((summary_cli.PROJECT, parent))
        for hit in hits:
            if hit not in seen:
                seen[hit] = float(row["at"])
        if len(seen) >= limit:
            break
    return [(k, r, at) for (k, r), at in list(seen.items())[:limit]]


async def _summary_head(deps: Deps, kind: str, ref: str) -> dict | None:
    """The summary's version and mode (`probe_api.summary_head`), or None when
    it cannot be read; a replay answers it when it can, else nothing is asked."""
    from probe.daemon.session import probe_api

    if deps.replay is not None:
        ask = getattr(deps.replay, "summary_head", None)
        return await ask(kind, ref) if ask is not None else None
    try:
        return await asyncio.wait_for(probe_api.summary_head(deps.probe_env, kind, ref), probe_api.SCOPE_TIMEOUT_S)
    except probe_api.KeyRefused:
        _mark_key_refused(deps)
        return None
    except Exception:  # noqa: BLE001 -- unknown: the draft on disk stands
        return None


async def autoload_summaries(deps: Deps) -> list[str]:
    """Before a writer run (no model round): bring the summaries of every
    project and experiment the session touched (`touched_entities`, at most
    `SUMMARY_DRAFTS_KEPT`) onto disk as drafts, through the CLI as the
    writer's own checkout would (`_remember_note` records it). Only what needs
    it (review of #3034, finding 5): an entity with no draft yet, or whose
    clean draft's version is no longer the server's (`_summary_head`, one
    plain read; nothing when that read fails). A draft holding unpushed edits
    is never replaced -- the worker leaves it, and so does the CLI if asked
    (`summary_cli.DraftDirty`) -- and its outline says so. Checkouts skip the
    Metrics-center question (`--no-visuals`); everything together is bounded by
    `AUTOLOAD_TIMEOUT_S`. Nothing while the team's summaries are the lane's,
    or Probe refuses the key. Returns the anchors checked out. Never raises."""
    try:
        _tally(deps)
        if deps.reader or deps.audit or deps.summaries_off or _mode_seen(deps) == "lane" or deps.key_refused:
            return []
        touched = touched_entities(deps.store)
        drafts = _drafts(deps.store)
        for kind, ref, at in touched:
            anchor = f"{kind}={ref}"
            if anchor in drafts:
                drafts[anchor] = {**drafts[anchor], "at": max(float(drafts[anchor].get("at") or 0), at)}
        deps.store.set_fact(SUMMARY_DRAFTS, _bound_drafts(drafts))

        async def wanted(kind: str, ref: str) -> bool:
            entry = drafts.get(f"{kind}={ref}")
            path = str((entry or {}).get("path") or "")
            if entry is None or not path or not Path(path).exists():
                return True
            if _draft_dirty(path):
                return False
            head = await _summary_head(deps, kind, ref)
            return head is not None and int(head.get("version") or 0) != int(entry.get("version") or 0)

        async def one(kind: str, ref: str) -> str | None:
            anchor = f"{kind}={ref}"
            if not await wanted(kind, ref):
                return None
            argv = ["summary", "checkout", f"--{kind}", ref, "--no-visuals"]
            result = await run_probe_process(deps, argv, f"autoload:{anchor}:{int(deps.store.clock())}")
            if result.code != 0:
                _remember_refused(deps, anchor, result.stdout)
                log.info("summary autoload of %s did not check out (exit %s)", anchor, result.code)
                return None
            parsed = precheck.parse(argv)
            _remember_note(deps, parsed, result.stdout)
            note_summary_marks(deps, parsed, argv, result.stdout, result.stderr)
            return anchor

        done = await asyncio.wait_for(asyncio.gather(*(one(k, r) for k, r, _ in touched)), AUTOLOAD_TIMEOUT_S)
        drafts = _drafts(deps.store)
        for kind, ref, at in touched:  # the checkout stamped `at` now: the touch time orders them
            entry = drafts.get(f"{kind}={ref}")
            if entry is not None:
                drafts[f"{kind}={ref}"] = {**entry, "at": at}
        deps.store.set_fact(SUMMARY_DRAFTS, _bound_drafts(drafts))
        return [a for a in done if a]
    except Exception as exc:  # noqa: BLE001 -- loading is a help, never a failed run
        log.warning("summary autoload failed: %s: %s", type(exc).__name__, exc)
        return []
from probe.daemon.agent.tools.probe_cli.owed import _mode_seen, _tally, note_summary_marks  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.process import _mark_key_refused, log, run_probe_process  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
