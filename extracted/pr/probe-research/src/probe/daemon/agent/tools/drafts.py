"""remember the draft file each checkout made and whether it holds unpushed edits."""

from __future__ import annotations
import json
import os
import time
from pathlib import Path
from probe.shared.command_rules import command_rules as precheck


#: The flags that name a note's or a summary's document. Sweep groups and files
#: no longer carry notes, so `--group` / `--artifact` name none.
_ANCHORS = ("project", "experiment", "run", "note")


def _anchor_key(parsed: precheck.Parsed) -> str:
    return "|".join(f"{k}={parsed.params.get(k)}" for k in _ANCHORS if parsed.params.get(k))


def _checkout_key(checkout: str, parsed: precheck.Parsed) -> str:
    """Where a checkout's path is kept: a note's under its flags alone (as
    before), a summary's or a visuals draft's under its command too."""
    anchors = _anchor_key(parsed)
    return anchors if checkout == "notes checkout" else f"{checkout}|{anchors}"


#: The summaries the writer keeps (ARTIFACT-PAGES P3): what each checkout of
#: one said, by its anchor flags (`_anchor_key`, as a push must repeat them):
#: {anchor: {"kind", "label", "path", "version", "edited_by", "edited_at",
#: "you", "format", "at"}}, `at` the last time the session touched it. The
#: worker shows them as OUTLINES (`summary_outline`), never their text: a full
#: page is large, and a writer that edits the draft in place (`edit`) needs
#: only where things are. Bounded: the `SUMMARY_DRAFTS_KEPT` most recently
#: touched entities (`_bound_drafts`).
SUMMARY_DRAFTS = "summary_drafts"
#: At most this many entities are kept checked out and outlined for the
#: writer: the most recently touched. A session that touches a seventh drops
#: the one it touched longest ago (its draft stays on disk; a checkout brings
#: it back).
SUMMARY_DRAFTS_KEPT = 6


def _drafts(store) -> dict[str, dict]:
    saved = store.fact(SUMMARY_DRAFTS)
    return {k: v for k, v in saved.items() if isinstance(v, dict)} if isinstance(saved, dict) else {}


def _bound_drafts(drafts: dict[str, dict]) -> dict[str, dict]:
    """The `SUMMARY_DRAFTS_KEPT` most recently touched, one per draft file."""
    by_path: dict[str, tuple[str, dict]] = {}
    for anchor, entry in sorted(drafts.items(), key=lambda kv: float(kv[1].get("at") or 0)):
        by_path[str(entry.get("path") or anchor)] = (anchor, entry)
    newest = sorted(by_path.values(), key=lambda kv: float(kv[1].get("at") or 0), reverse=True)
    return dict(newest[:SUMMARY_DRAFTS_KEPT])


def _remember_note(deps: Deps, parsed: precheck.Parsed, stdout: str) -> None:
    """The file a `notes checkout`, `summary checkout` or `visuals options`
    wrote (the `path` of the JSON it prints on stdout), for the push or `visuals
    set` with the same flags (`_document_path`); and what a summary checkout
    said about the page, for its outline (`SUMMARY_DRAFTS`)."""
    if parsed.path not in _DOCUMENT_FROM.values():
        if parsed.path == "summary push":
            _draft_after_push(deps, parsed, stdout)
        return
    try:
        payload = json.loads(stdout or "")
    except ValueError:
        return
    path = payload.get("path") if isinstance(payload, dict) else None
    if isinstance(path, str) and os.path.isabs(path):
        checkouts = deps.store.fact("checkouts", {}) or {}
        checkouts[_checkout_key(parsed.path, parsed)] = path
        deps.store.set_fact("checkouts", checkouts)
        if parsed.path == "summary checkout":
            drafts = _drafts(deps.store)
            drafts[_anchor_key(parsed)] = {
                "kind": str(payload.get("target") or ""), "label": str(payload.get("label") or ""),
                "path": path, "version": int(payload.get("version") or 0),
                "edited_by": payload.get("edited_by"), "edited_at": payload.get("edited_at"),
                "you": payload.get("you"), "format": payload.get("format") or "markdown",
                "at": deps.store.clock()}
            deps.store.set_fact(SUMMARY_DRAFTS, _bound_drafts(drafts))


def _draft_after_push(deps: Deps, parsed: precheck.Parsed, stdout: str) -> None:
    """A push that landed: its draft is the page now, at the new version, last
    edited by this writer."""
    drafts = _drafts(deps.store)
    entry = drafts.get(_anchor_key(parsed))
    if entry is None:
        return
    payload = _json(stdout)
    if not (payload and payload.get("pushed")):
        return
    drafts[_anchor_key(parsed)] = {
        **entry, "version": int(payload.get("version") or 0), "edited_by": entry.get("you") or entry.get("edited_by"),
        "edited_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(deps.store.clock())), "at": deps.store.clock()}
    deps.store.set_fact(SUMMARY_DRAFTS, _bound_drafts(drafts))


def _draft_dirty(path: str) -> bool:
    """Does the draft hold edits its base copy (the server's text at checkout)
    lacks? An unreadable one counts as dirty: never replaced."""
    draft = Path(path)
    if not draft.exists():
        return False
    try:
        return draft.read_text(encoding="utf-8") != draft.with_suffix(".base").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True


def _remember_refused(deps: Deps, anchor: str, stdout: str) -> None:
    """A checkout the CLI refused because the draft holds unpushed edits
    (`refused` in its JSON): the draft is still the session's to outline."""
    from probe.shared.notes import summary as summary_cli

    payload = _json(stdout)
    if not payload or payload.get("refused") != summary_cli.REFUSED_UNPUSHED or not payload.get("path"):
        return
    drafts = _drafts(deps.store)
    entry = drafts.get(anchor) or {}
    drafts[anchor] = {**entry, "kind": str(payload.get("target") or ""), "label": str(payload.get("label") or ""),
                      "path": str(payload["path"]), "version": int(payload.get("version") or 0),
                      "format": payload.get("format") or "markdown", "at": deps.store.clock()}
    deps.store.set_fact(SUMMARY_DRAFTS, _bound_drafts(drafts))
from probe.daemon.agent.tools.probe_cli.owed import _json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.probe_cli import _DOCUMENT_FROM  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
