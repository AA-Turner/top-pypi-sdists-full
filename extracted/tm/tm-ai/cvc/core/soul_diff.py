"""
cvc.core.soul_diff — Compare two soul snapshots for the time-portal.

Per CVC_FOUNDATION.md H1: "Time-portal UX: when restoring, show a
side-by-side of 'what you said then' vs 'what you know now.' The
rewind is not just context — it's recognition."

The portal needs a structured diff, not a free-text rendering. This
module produces the structured comparison: entities added/removed/
strengthened, values added/superseded, life events that happened
between, emotional context drift, and a human-readable summary.

Operates on UserIdentitySnapshot JSON (not the pydantic models) so
historical snapshots from any prior version stay diffable.
"""
from __future__ import annotations

from typing import Any


def _index_by_name(items: list[dict[str, Any]], key: str = "name") -> dict[str, dict[str, Any]]:
    """Index a list of dicts by a string field, for diff lookup."""
    out: dict[str, dict[str, Any]] = {}
    for it in items:
        k = it.get(key)
        if isinstance(k, str):
            out[k] = it
    return out


def _index_by_statement(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """For values which use 'statement' as the identity field."""
    out: dict[str, dict[str, Any]] = {}
    for it in items:
        s = it.get("statement")
        if isinstance(s, str):
            out[s] = it
    return out


def _index_by_description(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for it in items:
        d = it.get("description")
        if isinstance(d, str):
            out[d] = it
    return out


def diff_soul_models(then: dict[str, Any], now: dict[str, Any]) -> dict[str, Any]:
    """Compute the structured diff between two soul snapshots.

    Both inputs are UserIdentitySnapshot JSON dicts (not pydantic
    instances). Returns a structured comparison suitable for the
    time-portal side-by-side view.
    """
    # ── Entities: name-keyed ──────────────────────────────────────────────
    then_ents = _index_by_name(then.get("entities", []) or [])
    now_ents = _index_by_name(now.get("entities", []) or [])
    added_entities = sorted(set(now_ents) - set(then_ents))
    removed_entities = sorted(set(then_ents) - set(now_ents))
    strengthened_entities = []
    for name in sorted(set(then_ents) & set(now_ents)):
        before_mc = int(then_ents[name].get("mention_count", 0) or 0)
        after_mc = int(now_ents[name].get("mention_count", 0) or 0)
        if after_mc > before_mc:
            strengthened_entities.append(
                {
                    "name": name,
                    "mentions_before": before_mc,
                    "mentions_after": after_mc,
                    "delta": after_mc - before_mc,
                }
            )

    # ── Values: statement-keyed ──────────────────────────────────────────
    then_vals = _index_by_statement(then.get("values", []) or [])
    now_vals = _index_by_statement(now.get("values", []) or [])
    added_values = sorted(set(now_vals) - set(then_vals))
    superseded_values = sorted(set(then_vals) - set(now_vals))

    # ── Life events: description-keyed (events that happened in between) ─
    then_events = _index_by_description(then.get("life_events", []) or [])
    now_events = _index_by_description(now.get("life_events", []) or [])
    new_events = sorted(set(now_events) - set(then_events))

    # ── Emotional drift: count moods, mean intensity ─────────────────────
    then_emotions = then.get("emotional_context", []) or []
    now_emotions = now.get("emotional_context", []) or []
    def _mood_stats(items):
        if not items:
            return {"count": 0, "mean_intensity": 0.0, "dominant_mood": None}
        intensities = [float(e.get("intensity", 0.0) or 0.0) for e in items]
        moods = [str(e.get("mood", "")) for e in items if e.get("mood")]
        dominant = max(set(moods), key=moods.count) if moods else None
        return {
            "count": len(items),
            "mean_intensity": round(sum(intensities) / len(intensities), 3) if intensities else 0.0,
            "dominant_mood": dominant,
        }
    then_mood = _mood_stats(then_emotions)
    now_mood = _mood_stats(now_emotions)
    intensity_delta = round(now_mood["mean_intensity"] - then_mood["mean_intensity"], 3)

    # ── Narrative change: did the soul's own self-story shift? ───────────
    then_narrative = str(then.get("soul_narrative", "") or "")
    now_narrative = str(now.get("soul_narrative", "") or "")
    narrative_changed = then_narrative.strip() != now_narrative.strip()
    narrative_grew = len(now_narrative) - len(then_narrative)

    # ── Human-readable summary ──────────────────────────────────────────
    summary_lines = []
    if added_entities:
        summary_lines.append(
            f"You met {len(added_entities)} new "
            f"{'person' if len(added_entities) == 1 else 'people'}: "
            + ", ".join(added_entities[:5])
            + (f" and {len(added_entities) - 5} more" if len(added_entities) > 5 else "")
            + "."
        )
    if new_events:
        summary_lines.append(
            f"{len(new_events)} new milestone{'s' if len(new_events) != 1 else ''} "
            "happened between then and now."
        )
    if added_values:
        summary_lines.append(
            f"You articulated {len(added_values)} new value{'s' if len(added_values) != 1 else ''} "
            "you hold."
        )
    if narrative_changed:
        if narrative_grew > 0:
            summary_lines.append(
                f"Your soul's self-understanding grew by {narrative_grew} characters."
            )
        elif narrative_grew < 0:
            summary_lines.append(
                f"Your soul's self-understanding was refined "
                f"({abs(narrative_grew)} chars tightened)."
            )
        else:
            summary_lines.append("Your soul's self-understanding was rewritten.")
    if intensity_delta != 0 and then_mood["count"] and now_mood["count"]:
        direction = "more" if intensity_delta > 0 else "less"
        summary_lines.append(
            f"Emotionally, you've been {direction} intense on average "
            f"(Δ {intensity_delta:+.2f})."
        )

    return {
        "entities": {
            "added": added_entities,
            "removed": removed_entities,
            "strengthened": strengthened_entities,
        },
        "values": {
            "added": added_values,
            "superseded": superseded_values,
        },
        "life_events": {
            "new_in_between": new_events,
        },
        "emotional_drift": {
            "then": then_mood,
            "now": now_mood,
            "intensity_delta": intensity_delta,
        },
        "narrative": {
            "changed": narrative_changed,
            "length_delta": narrative_grew,
        },
        "summary": " ".join(summary_lines) if summary_lines else "Nothing material changed between these two moments.",
        "then_meta": {
            "name": then.get("name", ""),
            "timestamp": then.get("_snapshot_timestamp"),
        },
        "now_meta": {
            "name": now.get("name", ""),
            "timestamp": now.get("_snapshot_timestamp"),
        },
    }