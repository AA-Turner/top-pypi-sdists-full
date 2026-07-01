"""
cvc.agent.auto_skill — Automatic skill-draft creation from completed agent turns.

This is CVC's runtime-independent implementation of the pattern that
upstream ships only as a text instruction ("After 5+ tool calls, offer
to save as a skill"). Upstream leaves the entire decision to the LLM
during the turn; CVC runs an *additional* heuristic reflection
**after** the turn finishes, before the SSE `done` event leaves the
gateway. The result is a draft SKILL.md that the user can review and
approve — not a silently-promoted new skill.

Why drafts (not direct promotion):
    Bad skills are liabilities. If the heuristic misclassifies a turn,
    we'd pollute the active skill set with false positives. Drafts give
    the user a one-click approval path. The CLI / dashboard surface
    them as "X drafts awaiting review".

What gets captured per turn:
    - Tool sequence (ordered list of tool names)
    - File extensions touched (.py, .tsx, .toml, etc.)
    - Error→fix patterns (tool A failed, tool B succeeded)
    - Skills loaded during the turn
    - Total tool calls and total wall-clock tool time

Heuristic gate (don't even try to draft if):
    - Tool calls < 5              (trivial turn)
    - Turn errored                (no usable pattern)
    - Tool sequence is a single   (no workflow to capture)
      repeated tool

Dedupe gate (skip if an existing skill's name appears in the
turn's loaded-skill list AND its tool sequence matches):
    Walk the active skills list and check whether any skill's name
    appears in the loaded-skills set. If yes, the user already had
    coverage — skip drafting.

Confidence score (0..1):
    base 0.5
    +0.2 if 8+ tool calls (real work)
    +0.2 if any error was hit and recovered (problem-solving)
    +0.1 if multiple file domains touched (.py + .tsx, etc.)
    +0.1 if no existing skill was loaded for this pattern
    capped at 0.95 (never 1.0 — the human must still approve)

Draft storage:
    ~/.cvc/skills/.drafts/<generated-name>/SKILL.md

Draft frontmatter carries audit metadata (state, confidence,
source_turn, tool_sequence) so the dashboard can sort/filter
without re-parsing the body.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

logger = logging.getLogger("cvc.agent.auto_skill")

# ── Tunables ──────────────────────────────────────────────────────────

MIN_TOOL_CALLS = 5                  # below this, don't bother drafting
CONFIDENCE_THRESHOLD = 0.6          # below this, save but flag low-confidence
MAX_DRAFTS_PER_SESSION = 5          # hard ceiling per session_id

# Tool name → file-extension pattern (for "what files did we touch")
_FILE_TOOLS = {
    "read_file": ".generic",
    "write_file": ".generic",
    "patch": ".generic",
    "edit_file": ".generic",
    "search_files": ".generic",
    "browser_navigate": ".html",
    "web_extract": ".html",
    "vision_analyze": ".image",
    "image_generate": ".image",
    "image_to_ascii": ".image",
    "terminal": ".shell",
}

# Path-extension extractor (best-effort)
_PATH_EXT_RE = re.compile(r"\.[a-zA-Z0-9]{1,8}(?=[/\"'\s)\]}>,]|$)")


# ── Per-turn signal ───────────────────────────────────────────────────


@dataclass
class TurnSignal:
    """Structured view of one completed turn, used for skill drafting."""

    session_id: str
    turn_id: str
    user_message: str
    tool_sequence: list[str] = field(default_factory=list)
    file_extensions: set[str] = field(default_factory=set)
    skills_loaded: set[str] = field(default_factory=set)
    error_recovery_count: int = 0
    success_after_failure: int = 0
    total_tool_calls: int = 0
    total_tool_ms: int = 0
    final_response: str = ""
    workspace_path: str | None = None

    @property
    def distinct_tool_count(self) -> int:
        return len(set(self.tool_sequence))

    @property
    def signature_hash(self) -> str:
        """Stable hash of the tool-sequence + extensions + skills.

        Used to suppress duplicate drafts when the same pattern fires
        across multiple turns.
        """
        h = hashlib.sha256()
        h.update(",".join(self.tool_sequence).encode())
        h.update(b"|")
        h.update(",".join(sorted(self.file_extensions)).encode())
        h.update(b"|")
        h.update(",".join(sorted(self.skills_loaded)).encode())
        return h.hexdigest()[:16]

    @property
    def is_eligible(self) -> bool:
        """Heuristic gate: is this turn worth a draft?"""
        if self.total_tool_calls < MIN_TOOL_CALLS:
            return False
        if not self.final_response:
            return False
        if self.distinct_tool_count < 2:
            # A single tool used repeatedly isn't a workflow.
            return False
        return True


def signal_from_outbox(
    *,
    session_id: str,
    turn_id: str,
    user_message: str,
    outbox_events: list[dict],
    final_response: str = "",
    workspace_path: str | None = None,
) -> TurnSignal:
    """Build a TurnSignal by replaying the outbox events.

    Outbox events are the dashboard-shaped ChatEvent dicts already
    flowing through chat.py. We just need to project them into the
    structured view this module uses.
    """
    sig = TurnSignal(
        session_id=session_id,
        turn_id=turn_id,
        user_message=user_message,
        final_response=final_response,
        workspace_path=workspace_path,
    )
    last_result_ok: dict[str, bool] = {}
    for evt in outbox_events:
        et = evt.get("type")
        if et == "tool_start":
            name = evt.get("name", "")
            if not name or name.startswith("_"):
                continue
            sig.tool_sequence.append(name)
            sig.total_tool_calls += 1
            # Extract file extensions from args if present
            args = evt.get("args") or {}
            for v in args.values():
                if isinstance(v, str):
                    for ext in _PATH_EXT_RE.findall(v):
                        if ext and ext != ".":
                            sig.file_extensions.add(ext.lower())
            # Skill loads
            if name == "skill_view":
                target = args.get("name") or args.get("skill_name") or ""
                if isinstance(target, str) and target:
                    sig.skills_loaded.add(target)
        elif et == "tool_result":
            call_id = evt.get("call_id", "")
            ok = _result_is_ok(evt.get("output", ""))
            last_result_ok[call_id] = ok
        elif et == "tool_progress" and evt.get("error"):
            sig.error_recovery_count += 1
    # Pair tool starts with results for success-after-failure detection.
    # Walk in order: when we see a failed tool_result followed by a
    # later success of the same tool name, that counts.
    # (Approximate — exact pairing requires call_id correlation.)
    failed_tools: set[str] = set()
    for evt in outbox_events:
        if evt.get("type") == "tool_result":
            name = evt.get("name", "")
            ok = _result_is_ok(evt.get("output", ""))
            if not ok and name:
                failed_tools.add(name)
            elif ok and name in failed_tools:
                sig.success_after_failure += 1
                failed_tools.discard(name)
        if evt.get("type") == "tool_start":
            name = evt.get("name", "")
            started = evt.get("started_at_ms")
            ended = evt.get("ended_at_ms")
            if isinstance(started, int) and isinstance(ended, int):
                sig.total_tool_ms += max(0, ended - started)
    return sig


def _result_is_ok(output: Any) -> bool:
    """Heuristic: did this tool succeed?

    Tries common success markers ({"success": True}, "OK", "0", etc.)
    and falls back to "no error keyword" — never perfect, but enough
    to drive a draft-confidence signal.
    """
    if output is None:
        return True  # empty = nothing to flag
    if isinstance(output, dict):
        if "success" in output:
            return bool(output["success"])
        if "error" in output:
            return not bool(output["error"])
        if "failed" in output:
            return not bool(output["failed"])
        return True
    s = str(output)
    if not s:
        return True
    sl = s.lower()
    # Strong failure markers
    for marker in ("traceback", "exception:", "error:", "failed:", "permission denied", "not found"):
        if marker in sl:
            return False
    return True


# ── Confidence scoring ────────────────────────────────────────────────


def compute_confidence(sig: TurnSignal) -> float:
    """Heuristic confidence score (0..1) that this turn produced a
    reusable pattern worth capturing."""
    if not sig.is_eligible:
        return 0.0
    score = 0.5
    if sig.total_tool_calls >= 8:
        score += 0.2
    if sig.error_recovery_count > 0 or sig.success_after_failure > 0:
        score += 0.2
    if len(sig.file_extensions) >= 2:
        score += 0.1
    if not sig.skills_loaded:
        score += 0.1
    return min(score, 0.95)


# ── Skill name generation ────────────────────────────────────────────


_GENERIC_NAME_RE = re.compile(r"[^a-z0-9-]+")


def _slugify(s: str, max_len: int = 48) -> str:
    s = s.lower().strip()
    s = _GENERIC_NAME_RE.sub("-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:max_len] or "auto"


def generate_skill_name(sig: TurnSignal) -> str:
    """Generate a draft skill name from the dominant tool + file ext.

    Format: ``auto-<top-tool>-<top-ext>-<short-hash>``. The hash makes
    two drafts from similar-but-distinct patterns non-colliding.
    """
    # Top tool = most frequent in the sequence
    tool_counts: dict[str, int] = {}
    for t in sig.tool_sequence:
        tool_counts[t] = tool_counts.get(t, 0) + 1
    top_tool = sorted(tool_counts.items(), key=lambda kv: -kv[1])[0][0] if tool_counts else "misc"
    top_tool = _slugify(top_tool, 16)
    top_ext = sorted(sig.file_extensions)[0].lstrip(".") if sig.file_extensions else "work"
    top_ext = _slugify(top_ext, 12)
    short_hash = sig.signature_hash[:6]
    return f"auto-{top_tool}-{top_ext}-{short_hash}"


# ── Draft content generation ─────────────────────────────────────────


def render_draft_skill_md(sig: TurnSignal) -> str:
    """Produce a starter SKILL.md from the turn signal.

    The body is a TEMPLATE — sections are pre-populated with the
    observed signal (tools used, files touched, errors hit) so the
    user can edit instead of starting from scratch. The description
    is generic on purpose; the user fills it in before approving.
    """
    name = generate_skill_name(sig)
    confidence = compute_confidence(sig)
    tools_str = ", ".join(f"`{t}`" for t in sorted(set(sig.tool_sequence)))
    exts_str = ", ".join(sorted(sig.file_extensions)) or "(none observed)"
    skills_str = ", ".join(sorted(sig.skills_loaded)) or "(none)"
    user_msg = (sig.user_message or "").strip().splitlines()[0][:240]

    body = f"""---
name: {name}
description: "Use when {user_msg or '<describe the trigger pattern>'}."
version: 0.1.0-draft
author: CVC (auto-generated)
license: MIT
state: draft
confidence: {confidence:.2f}
source:
  session_id: {sig.session_id}
  turn_id: {sig.turn_id}
  generated_at_turn: true
metadata:
  cvc:
    tags: [auto-generated, review-required]
    related_skills: [{", ".join(sorted(sig.skills_loaded)) or ""}]
    tool_sequence_hash: {sig.signature_hash}
---

# {name.replace("-", " ").title()} (DRAFT — review before approving)

> Auto-generated by CVC's post-turn reflection. The body is a starter
> template populated from observed signals in the source turn. Edit
> the description and Overview before approving — auto-generated
> descriptions are intentionally generic and may not capture the
> real trigger class.

## Overview

This draft was generated from a turn that produced:

- **Total tool calls:** {sig.total_tool_calls}
- **Distinct tools:** {sig.distinct_tool_count}
- **File extensions touched:** {exts_str}
- **Skills loaded during the turn:** {skills_str}
- **Error → recovery events:** {sig.error_recovery_count} error(s), {sig.success_after_failure} successful retry(ies)
- **Total tool time:** {sig.total_tool_ms / 1000:.1f}s

**Original user request:** {user_msg or "(empty)"}

## When to Use

> ⚠️ Edit this section to describe the trigger class. The current text
> is a copy of the user's original message, not a generalizable trigger.

- TODO: replace with the real trigger ("Use when ...")

Don't use for:

- TODO: list counter-triggers

## Tool Sequence Observed

{tools_str}

(ordered as fired — see `metadata.cvc.tool_sequence_hash` for the
deterministic signature used for dedupe)

## Common Pitfalls

- TODO: capture pitfalls observed in the source turn (errors hit,
  retries needed, files that needed cleanup after the run)

## Verification Checklist

- [ ] Description captures the trigger class, not just one task
- [ ] Body has actionable commands, not just narrative
- [ ] Related skills cross-referenced correctly
- [ ] No PII or workspace-specific paths in the body
- [ ] Confidence score above 0.7 — if lower, more review needed

## Approval Path

```bash
# Preview before approving
cvc skills drafts show {name}

# Promote to active set (writes to ~/.cvc/skills/<category>/)
cvc skills drafts approve {name}

# Or discard
cvc skills drafts reject {name}
```
"""
    return body


# ── Dedupe against existing skills ────────────────────────────────────


def find_existing_skill_coverage(sig: TurnSignal) -> str | None:
    """Return the name of an existing skill that already covers this
    pattern, or None.

    Walks the active skill list (bundled + user + drafts) and checks
    whether any skill's name appears in the loaded-skills set of the
    turn, OR matches the tool-sequence signature.
    """
    try:
        from cvc.agent.skills import discover_skills  # noqa: WPS433
        skills = discover_skills(workspace=sig.workspace_path or ".")
    except Exception as e:
        logger.debug("discover_skills failed during dedupe: %s", e)
        return None
    loaded_lc = {s.lower() for s in sig.skills_loaded}
    for s in skills:
        if s.name.lower() in loaded_lc:
            return s.name
    return None


# ── Draft write ──────────────────────────────────────────────────────


def save_draft(sig: TurnSignal) -> Path | None:
    """Write a draft SKILL.md to ``~/.cvc/skills/.drafts/<name>/SKILL.md``.

    Returns the path on success, or None if:
    - The turn isn't eligible
    - An existing skill already covers the pattern
    - The per-session draft ceiling is hit
    - A draft with the same signature already exists

    Audit log lives at ``~/.cvc/skills/.drafts/.audit.json`` (append-only).
    """
    if not sig.is_eligible:
        logger.debug("auto_skill: turn %s not eligible (tool_calls=%d)",
                     sig.turn_id, sig.total_tool_calls)
        return None

    coverage = find_existing_skill_coverage(sig)
    if coverage:
        logger.debug("auto_skill: turn %s already covered by skill %s",
                     sig.turn_id, coverage)
        return None

    from cvc.skills.drafts import (  # noqa: WPS433 — late import to avoid cycle
        DRAFTS_DIR,
        append_audit,
        load_audit,
    )
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    audit = load_audit()
    # Per-session ceiling
    session_drafts = [a for a in audit
                      if a.get("session_id") == sig.session_id
                      and a.get("state") == "draft"]
    if len(session_drafts) >= MAX_DRAFTS_PER_SESSION:
        logger.debug("auto_skill: session %s hit draft ceiling (%d)",
                     sig.session_id, MAX_DRAFTS_PER_SESSION)
        return None

    # Dedupe against existing drafts by signature hash
    name = generate_skill_name(sig)
    for a in audit:
        if a.get("state") == "draft" and a.get("signature_hash") == sig.signature_hash:
            logger.debug("auto_skill: signature %s already drafted as %s",
                         sig.signature_hash, a.get("name"))
            return None

    target_dir = DRAFTS_DIR / name
    target_md = target_dir / "SKILL.md"
    if target_md.exists():
        # Don't overwrite a draft the user may be editing
        logger.debug("auto_skill: draft %s already exists at %s", name, target_md)
        return None

    target_dir.mkdir(parents=True, exist_ok=True)
    target_md.write_text(render_draft_skill_md(sig), encoding="utf-8")
    append_audit({
        "name": name,
        "session_id": sig.session_id,
        "turn_id": sig.turn_id,
        "signature_hash": sig.signature_hash,
        "confidence": compute_confidence(sig),
        "tool_sequence": sig.tool_sequence,
        "file_extensions": sorted(sig.file_extensions),
        "skills_loaded": sorted(sig.skills_loaded),
        "state": "draft",
        "created_at": _now_iso(),
        "path": str(target_md),
    })
    logger.info("auto_skill: created draft %s (confidence=%.2f) at %s",
                name, compute_confidence(sig), target_md)
    return target_md


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


# ── Hook entry point used by gateway ─────────────────────────────────


def maybe_create_draft(
    *,
    session_id: str,
    turn_id: str,
    user_message: str,
    outbox_events: Iterable[dict],
    final_response: str = "",
    workspace_path: str | None = None,
) -> dict | None:
    """Single public entry point. Returns a small dict with the result
    so the gateway can log/emit it; None when no draft was created."""
    try:
        sig = signal_from_outbox(
            session_id=session_id,
            turn_id=turn_id,
            user_message=user_message,
            outbox_events=list(outbox_events),
            final_response=final_response,
            workspace_path=workspace_path,
        )
        confidence = compute_confidence(sig)
        if not sig.is_eligible:
            return {"eligible": False, "reason": "below threshold",
                    "total_tool_calls": sig.total_tool_calls}
        coverage = find_existing_skill_coverage(sig)
        if coverage:
            return {"eligible": True, "drafted": False,
                    "covered_by": coverage,
                    "confidence": confidence}
        path = save_draft(sig)
        if path is None:
            return {"eligible": True, "drafted": False,
                    "reason": "deduped or session-cap hit",
                    "confidence": confidence}
        return {
            "eligible": True,
            "drafted": True,
            "path": str(path),
            "name": path.parent.name,
            "confidence": confidence,
            "tool_sequence": sig.tool_sequence,
        }
    except Exception as e:  # pragma: no cover — reflection is best-effort
        logger.exception("auto_skill reflection failed for turn %s: %s", turn_id, e)
        return None
