"""
Per-turn soul auto-encoding — fired after EVERY chat turn.

This is the H2 wiring that was missing from the dashboard chat path.

Background: the legacy CLI session loop fires `cognitive_hooks.on_session_stop`
after the whole chat ends. But dashboard chats are persistent — they
NEVER end. The user can keep the same thread open for weeks. If the
soul only learns at session-stop, it NEVER learns.

This module provides `update_soul_after_turn(user_message, assistant_text,
workspace_path)` which is called from the dashboard chat stream after
every turn completes. It:

  1. Runs the H2 mood classifier on the user's message
  2. Runs the H2 entity extractor on user message + assistant text
     (the assistant often mentions names/projects the user cares
     about even when the user doesn't — we should remember those too)
  3. Writes to the user model immediately (snapshot-on-save auto-runs)
  4. All best-effort — never crashes the chat stream

Workspace-aware: each workspace has its own `.cvc/` so the soul that
learns about HydroMain lives in HydroMain's .cvc/, not the user's
~/.cvc/. Resolution order: env override > CWD/.cvc > HOME/.cvc.

The function is sync (not async) — it's called from the SSE stream's
async context but does no I/O beyond a small file write. We expose
`async_update_soul_after_turn` for callers that want to offload it
to a thread.
"""
from __future__ import annotations

import hashlib
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.operations.per_turn_soul")

# ── Idempotency guard (hotfix/soul-values-and-cleanup-2026-06-30) ────────
# The per-turn hook can fire multiple times per chat turn: SSE proxy
# (hermes_unified.py:484), SSE stream (hermes_unified.py:585), SSE
# gateway (gateway_chat.py:439), POST /api/chat (gateway/chat.py:1314),
# and WS /api/ws/chat (gateway/chat.py:1716) all call
# `fire_and_forget_update`. Same user_message + same workspace within
# a short window = the same turn. Skip the second/third invocation
# so the soul doesn't triple-record mood + entities + values.
_LAST_TURN_HASHES: dict[str, tuple[str, float]] = {}
_DEDUP_WINDOW_SEC = 5.0
_DEDUP_LOCK = threading.Lock()


def _resolve_cvc_root(workspace_path: str | None = None) -> Path:
    """Resolve the .cvc root for the current workspace.

    Resolution order:
      1. CVC_TEST_ROOT env var (used by tests for hermetic isolation)
      2. workspace_path/.cvc — if a workspace path was given
      3. CWD/.cvc — the active project
      4. ~/.cvc — the user-global root
    """
    override = os.environ.get("CVC_TEST_ROOT")
    if override:
        p = Path(override)
        if p.exists() and (p / "cvc.db").exists():
            return p
    if workspace_path:
        ws_cvc = Path(workspace_path) / ".cvc"
        if ws_cvc.exists() and (ws_cvc / "cvc.db").exists():
            return ws_cvc
    cwd_cvc = Path.cwd() / ".cvc"
    if cwd_cvc.exists() and (cwd_cvc / "cvc.db").exists():
        return cwd_cvc
    home_cvc = Path.home() / ".cvc"
    if home_cvc.exists() and (home_cvc / "cvc.db").exists():
        return home_cvc
    # Fall back to cwd so save_model creates the dir if needed
    return cwd_cvc


def _is_duplicate_turn(user_message: str, workspace_path: str | None) -> bool:
    """Return True if the same (workspace, message_hash) was processed
    within the dedup window. Prevents 2-3x triple-firing of mood/entity
    extraction on a single chat turn when multiple SSE/WS handlers all
    call fire_and_forget_update at end-of-turn.
    """
    key = (workspace_path or "").strip()
    msg_hash = hashlib.sha1(
        user_message.strip().lower().encode("utf-8", errors="ignore")
    ).hexdigest()[:16]
    now = time.monotonic()
    with _DEDUP_LOCK:
        # Garbage-collect stale entries (older than 60s) on every call.
        stale = [k for k, (_, ts) in _LAST_TURN_HASHES.items() if now - ts > 60.0]
        for k in stale:
            _LAST_TURN_HASHES.pop(k, None)
        last = _LAST_TURN_HASHES.get(key)
        if last and last[0] == msg_hash and (now - last[1]) < _DEDUP_WINDOW_SEC:
            return True
        _LAST_TURN_HASHES[key] = (msg_hash, now)
        return False


def _synthesise_narrative(model) -> str:
    """Build a deterministic 3-5 sentence narrative from the current
    snapshot. Runs on every per-turn update so the dashboard sees the
    soul respond immediately, not only after a session ends.

    Synthesis rules:
      - Always start with the user's name if known.
      - Mention the people + projects the soul cares about.
      - Reflect the top values the soul has learned.
      - End with the emotional tone of recent activity.
      - Never invent claims that aren't supported by what's stored.
    """
    name = (getattr(model, "name", "") or "").strip()
    parts: list[str] = []

    # Identity opener
    if name:
        opener = f"{name} is the human behind this soul"
    else:
        opener = "The soul is still learning who this user is"

    # What we know about who they are
    people = sorted(
        [e for e in model.entities if e.entity_type == "person"],
        key=lambda x: x.mention_count,
        reverse=True,
    )[:3]
    projects = sorted(
        [e for e in model.entities if e.entity_type == "project"],
        key=lambda x: x.mention_count,
        reverse=True,
    )[:3]

    relationship_words = {
        e.name for e in people if e.relationship
    }
    if relationship_words:
        opener += f", with {len(relationship_words)} close relationship{'s' if len(relationship_words) != 1 else ''}"

    parts.append(opener + ".")

    # Projects + people
    if projects:
        proj_names = ", ".join(p.name for p in projects[:3])
        parts.append(f"They spend most of their energy on {proj_names}.")
    if people:
        # Only top 3, with relationship if known
        ppl = []
        for p in people[:3]:
            if p.relationship:
                ppl.append(f"{p.name} ({p.relationship})")
            else:
                ppl.append(p.name)
        parts.append(
            "The people who come up most often in their work are "
            + ", ".join(ppl)
            + "."
        )

    # Values
    active_values = [v for v in model.values if not v.superseded_by]
    if active_values:
        # Sort by confidence, take top 3
        active_values.sort(key=lambda v: v.confidence, reverse=True)
        statements = [v.statement for v in active_values[:3]]
        parts.append(
            "What they stand for: "
            + "; ".join(statements)
            + "."
        )

    # Mood tone
    if model.emotional_context:
        recent = model.emotional_context[-15:]
        moods = [e.mood for e in recent]
        from collections import Counter
        mood_counts = Counter(moods)
        top_mood, top_count = mood_counts.most_common(1)[0]
        if top_count >= len(moods) * 0.4 and top_mood != "neutral":
            parts.append(
                f"Lately they've been mostly {top_mood} — "
                f"{top_count} of the last {len(moods)} conversations."
            )

    narrative = " ".join(parts).strip()
    # Cap to keep the prompt injection + UI display sane.
    return narrative[:1200]


def _synthesise_name(model) -> str:
    """Best-effort name detection. Only writes a name when one is
    explicitly present in user text or entity attributes — never
    guesses from ambient conversation. Returns "" if no name found.
    """
    # If a user typed "I'm Jai" or "my name is Jai" — the entity
    # extractor may have already captured it as an entity with
    # entity_type="person" and relationship like "self". We don't
    # risk promoting that to the top-level `name` field because it's
    # too error-prone. The CLI's session-stop LLM path is the
    # authoritative source for `name`. The dashboard just leaves it
    # blank if the CLI hasn't filled it in yet.
    return (getattr(model, "name", "") or "").strip()


def update_soul_after_turn(
    user_message: str,
    assistant_text: str | None = None,
    workspace_path: str | None = None,
) -> dict[str, Any]:
    """Run H2 auto-encoders after a single chat turn and persist.

    Args:
        user_message: the latest user turn text
        assistant_text: the latest assistant response text (may be empty)
        workspace_path: optional workspace root; resolves to <path>/.cvc

    Returns:
        {
            "ok": bool,
            "cvc_root": str,
            "mood": str | None,
            "intensity": float,
            "entities_added": int,
            "entities_seen": [str, ...],
            "values_added": int,
            "values_seen": [str, ...],
            "snapshot_written": bool,
            "error": str | None (only on hard failure),
        }

    Safe-by-default:
        - Never raises. Returns error in dict.
        - Heuristic pass is synchronous and fast (no LLM call).
        - Empty user_message → no-op (returns ok=True with zeros).
        - Missing .cvc/ → no-op (returns ok=False with explanation).
    """
    result: dict[str, Any] = {
        "ok": True,
        "cvc_root": "",
        "mood": None,
        "intensity": 0.0,
        "entities_added": 0,
        "entities_seen": [],
        "values_added": 0,
        "values_seen": [],
        "snapshot_written": False,
        "error": None,
    }

    user_message = (user_message or "").strip()
    if not user_message:
        # Nothing to learn from an empty turn. Don't touch the soul.
        return result

    # ── Idempotency guard ─────────────────────────────────────────────
    # Multiple SSE/WS handlers fire fire_and_forget_update at end of
    # one turn. Skip subsequent calls for the same message within a
    # short window so the soul only learns once per turn.
    if _is_duplicate_turn(user_message, workspace_path):
        result["ok"] = True
        result["deduped"] = True
        return result

    cvc_root = _resolve_cvc_root(workspace_path)
    result["cvc_root"] = str(cvc_root)  # workspace root (for the chat/project)
    # hotfix/soul-singularity-2026-06-30 — also expose the singular
    # soul root so the dashboard can show "your soul lives here" once.
    try:
        from cvc.operations.soul_singularity import _soul_root
        result["soul_root"] = str(_soul_root())
    except Exception:
        pass

    # Strict check: only operate on a real, initialized .cvc root.
    # Creating a fresh empty root silently is misleading — the soul
    # needs cvc.db to exist. If the user opens the dashboard without
    # `cvc setup` having been run, we don't want to fake-write a soul.
    if not cvc_root.exists() or not (cvc_root / "cvc.db").exists():
        result["ok"] = False
        result["error"] = f".cvc root not initialized at {cvc_root}"
        return result

    try:
        from cvc.core.user_model import (
            EmotionalContext,
            UserModelManager,
        )
        from cvc.operations.emotional_classifier import classify_text
        from cvc.operations.entity_extractor import (
            extract_from_message,
            merge_into_snapshot,
        )

        # hotfix/soul-singularity-2026-06-30 — the per-turn soul hook
        # used to write to <workspace>/.cvc/user_model.json, fragmenting
        # the soul across workspaces. Now it writes to ~/.cvc/soul/
        # (the global soul store). The workspace's cvc_root is still
        # used to gate the operation (only operate when cvc.db exists,
        # so we don't create ghost workspaces), but the model itself
        # is loaded from and saved to the global store.
        from cvc.operations.soul_singularity import _soul_root, ensure_migrated

        ensure_migrated()
        soul_root = _soul_root()
        um = UserModelManager(soul_root)
        model = um.load_current_model()

        # ── 0. Cleanup legacy garbage ──────────────────────────────────
        # hotfix/soul-values-and-cleanup-2026-06-30 — entities captured
        # before the stopword / owner / soft-override filters shipped
        # persist forever. The Soul page shows "The", "Honestly", "If",
        # "What", "Where" as people. This drops them on the next turn
        # and dedupes owner rows (Jai/Jai/Jai → one). Cheap, idempotent.
        try:
            from cvc.operations.entity_extractor import cleanup_snapshot_entities

            dropped, merged = cleanup_snapshot_entities(model)
            if dropped or merged:
                result["cleanup_dropped"] = dropped
                result["cleanup_merged"] = merged
                # Persist immediately — otherwise we'd cleanup again on the
                # next turn before the merge makes it sticky.
                um.save_model(model, trigger="per_turn_cleanup")
        except Exception as cleanup_exc:
            logger.debug("per-turn cleanup failed: %s", cleanup_exc)

        # ── 1. Mood classification ──────────────────────────────────
        try:
            cls = classify_text(user_message)
            result["mood"] = cls.mood
            result["intensity"] = cls.intensity
            # Only persist if the classifier found something meaningful.
            # Neutral + low intensity is the default for chat pleasantries
            # like "thanks" — don't pollute the soul with those.
            if cls.mood != "neutral" or cls.intensity > 0.25:
                model.emotional_context.append(
                    EmotionalContext(
                        mood=cls.mood,
                        intensity=cls.intensity,
                        trigger=cls.trigger[:200] if cls.trigger else user_message[:200],
                        timestamp=time.time(),
                    )
                )
                # Cap at 200 to prevent unbounded growth
                if len(model.emotional_context) > 200:
                    model.emotional_context = model.emotional_context[-200:]
        except Exception as emo_exc:
            logger.debug("H2 per-turn mood classification failed: %s", emo_exc)

        # ── 2. Entity extraction ────────────────────────────────────
        # Extract from BOTH user message AND assistant response. The
        # assistant often names projects/people the user cares about
        # (e.g. "I know HydroMain is the marketing site, train360 is
        # the real repo" — both are entity mentions worth capturing).
        try:
            extracted = list(extract_from_message(user_message, message_idx=0))
            if assistant_text:
                extracted.extend(
                    extract_from_message(assistant_text, message_idx=1)
                )
            if extracted:
                seen_names = sorted({e.name for e in extracted})
                result["entities_seen"] = seen_names
                added = merge_into_snapshot(extracted, model)
                result["entities_added"] = added
        except Exception as ent_exc:
            logger.debug("H2 per-turn entity extraction failed: %s", ent_exc)

        # ── 2b. Value extraction (hotfix/soul-values-and-cleanup-…) ─
        # Same idea as entity extraction but for declarative
        # values. The LLM-driven path only fires at session-stop,
        # which dashboard chats never reach, so values were 0.
        # Heuristic pass fills them in immediately. The AI cleanup
        # cron later refines and prunes anything that's wrong.
        try:
            from cvc.operations.value_extractor import (
                extract_from_message as extract_values_from_message,
                merge_into_snapshot as merge_values_into_snapshot,
            )
            extracted_vals = list(
                extract_values_from_message(user_message, message_idx=0)
            )
            if assistant_text:
                extracted_vals.extend(
                    extract_values_from_message(assistant_text, message_idx=1)
                )
            if extracted_vals:
                result["values_seen"] = [v.statement[:120] for v in extracted_vals]
                result["values_added"] = merge_values_into_snapshot(
                    extracted_vals, model
                )
        except Exception as val_exc:
            logger.debug("per-turn value extraction failed: %s", val_exc)

        # ── 2c. Narrative synthesis (hotfix/soul-values-and-cleanup-) ─
        # The CLI's on_session_stop hook fires an LLM to write the
        # soul_narrative. Dashboard chats never reach session_stop.
        # Without this, soul_narrative stays "" forever and the Soul
        # page renders an empty hero. We build a deterministic
        # narrative from the accumulated entities/values/mood so the
        # dashboard sees a real narrative immediately. Periodic
        # LLM-driven refresh (every 15 turns) later overrides this
        # with a higher-quality version.
        try:
            new_narrative = _synthesise_narrative(model)
            if new_narrative and new_narrative != model.soul_narrative:
                model.soul_narrative = new_narrative
                result["narrative_updated"] = True
            new_name = _synthesise_name(model)
            if new_name and new_name != model.name:
                model.name = new_name
                result["name_updated"] = True
        except Exception as narr_exc:
            logger.debug("per-turn narrative synthesis failed: %s", narr_exc)

        # ── 3. Persist if anything changed ───────────────────────────
        changed = (
            result["mood"] is not None
            and (result["mood"] != "neutral" or result["intensity"] > 0.25)
        ) or result["entities_added"] > 0 or result.get("values_added", 0) > 0 or result.get("narrative_updated", False) or result.get("name_updated", False)
        if changed:
            # save_model auto-snapshots (H1), so time-machine + soul
            # both advance in lockstep with the user's every turn.
            try:
                um.save_model(model, trigger="per_turn_auto")
                result["snapshot_written"] = True

                # v3.5.1 — TIME PORTAL day consolidation. After every
                # per_turn_auto snapshot, check if TODAY now has enough
                # snapshots to consolidate into a day_canonical frame.
                # Cheap (one indexed lookup, in-memory merge) and idempotent
                # (skips if a day_canonical already exists for the date).
                # Runs in the same try-block as save_model so any exception
                # here is swallowed alongside other non-fatal soul writes.
                try:
                    from cvc.gateway.soul import auto_consolidate_day_if_needed
                    _today = time.strftime("%Y-%m-%d")
                    auto_consolidate_day_if_needed(_today)
                except Exception as consol_exc:  # noqa: BLE001
                    logger.debug(
                        "per-turn day consolidation check failed (non-fatal): %s",
                        consol_exc,
                    )

                # C4: spine capture — log what changed in the soul.
                # One event per change type so the Timeline shows
                # "soul: wrote 3 entities" as a single line.
                try:
                    from cvc.events.spine import capture
                    workspace_resolved = _resolve_cvc_root(workspace_path)
                    if result["entities_added"] > 0:
                        capture(
                            kind="soul.write",
                            workspace=str(workspace_resolved),
                            channel="soul",
                            actor="assistant",
                            summary=f"wrote {result['entities_added']} entit{'y' if result['entities_added'] == 1 else 'ies'}",
                            data={
                                "added": result["entities_added"],
                                "seen": result.get("entities_seen", [])[:20],
                                "kind": "entity",
                            },
                            branch="main",
                        )
                    if result.get("values_added", 0) > 0:
                        capture(
                            kind="soul.write",
                            workspace=str(workspace_resolved),
                            channel="soul",
                            actor="assistant",
                            summary=f"wrote {result['values_added']} value{'s' if result['values_added'] != 1 else ''}",
                            data={
                                "added": result["values_added"],
                                "seen": result.get("values_seen", [])[:20],
                                "kind": "value",
                            },
                            branch="main",
                        )
                    if result["mood"] is not None and result["mood"] != "neutral":
                        capture(
                            kind="soul.write",
                            workspace=str(workspace_resolved),
                            channel="soul",
                            actor="assistant",
                            summary=f"mood={result['mood']} (intensity {result['intensity']:.2f})",
                            data={
                                "kind": "mood",
                                "mood": result["mood"],
                                "intensity": result["intensity"],
                            },
                            branch="main",
                            tags=["emotion"],
                        )
                    if result.get("narrative_updated"):
                        capture(
                            kind="soul.write",
                            workspace=str(workspace_resolved),
                            channel="soul",
                            actor="assistant",
                            summary="soul narrative rewritten",
                            data={
                                "kind": "narrative",
                                "chars": len(model.soul_narrative or ""),
                            },
                            branch="main",
                        )
                except Exception as cap_exc:  # noqa: BLE001
                    logger.debug("per-turn soul capture failed: %s", cap_exc)

            except Exception as sv_exc:
                logger.debug("per-turn save_model failed: %s", sv_exc)
                result["error"] = f"save_model failed: {sv_exc}"

        return result

    except Exception as exc:
        # Hard failure — return error but don't crash the chat stream.
        logger.exception("per-turn soul update failed")
        result["ok"] = False
        result["error"] = str(exc)
        return result


async def async_update_soul_after_turn(
    user_message: str,
    assistant_text: str | None = None,
    workspace_path: str | None = None,
) -> dict[str, Any]:
    """Async wrapper — runs the sync update in a worker thread.

    Use this from async SSE stream code so the heuristic pass doesn't
    block the event loop. The heuristic is fast (microseconds) but
    snapshot-on-save does a JSON serialize + file write which can
    take a few ms.
    """
    import asyncio

    return await asyncio.to_thread(
        update_soul_after_turn,
        user_message,
        assistant_text,
        workspace_path,
    )


# Background-thread variant for fire-and-forget updates that shouldn't
# add latency to the SSE stream. Returns immediately; the actual work
# happens on a daemon thread. Use this when you absolutely cannot
# afford to wait even a few ms for the soul update.
_thread_lock = threading.Lock()


def fire_and_forget_update(
    user_message: str,
    assistant_text: str | None = None,
    workspace_path: str | None = None,
) -> threading.Thread:
    """Spawn a daemon thread to update the soul off the hot path.

    Returns the Thread (caller may .join() if it wants to wait).
    Safe to call many times — threads are daemons and won't block shutdown.
    """

    def _runner():
        try:
            with _thread_lock:
                update_soul_after_turn(user_message, assistant_text, workspace_path)
        except Exception:
            # Defensive — update_soul_after_turn already swallows,
            # this is belt-and-suspenders for the thread wrapper.
            logger.exception("fire-and-forget soul update failed")

    t = threading.Thread(target=_runner, daemon=True, name="per-turn-soul")
    t.start()
    return t