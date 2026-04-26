"""Shared status wording for explicit memory-save results."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MemorySaveStatusMessage:
    """User-facing text plus compact metadata for a memory-save result."""

    text: str
    metadata: dict[str, Any]


def format_memory_save_result(result: dict[str, Any], *, data_dir: str | Path | None = None) -> MemorySaveStatusMessage:
    """Format an authoritative ``save_memory`` result without lifecycle hedging."""

    if "error" in result:
        return MemorySaveStatusMessage(
            text=f"Memory save failed: {result['error']}",
            metadata={"memory_save": {"error": result.get("error")}},
        )

    status = str(result.get("memory_status") or "candidate")
    fqn = str(result.get("fqn") or "")
    scope = str(result.get("scope") or "user")
    category = str(result.get("category") or "preference")
    storage_hint = _storage_hint(data_dir)
    recallable = status == "active"
    review_required = status in {"candidate", "pending_review"}

    location = f" in Anteroom's configured app data database ({storage_hint})"
    fqn_sentence = f" FQN: {fqn}." if fqn else ""
    if status == "active":
        text = f"Saved as an active memory{location}; it is eligible for recall.{fqn_sentence}"
    elif status in {"candidate", "pending_review"}:
        label = "candidate" if status == "candidate" else "pending-review item"
        text = f"Saved as a memory {label}{location}; it is not active or recallable until approved.{fqn_sentence}"
    elif status in {"rejected", "archived"}:
        text = f"Saved with memory status '{status}'{location}; it is not active or recallable.{fqn_sentence}"
    else:
        text = f"Saved with memory status '{status}'{location}.{fqn_sentence}"

    return MemorySaveStatusMessage(
        text=text,
        metadata={
            "memory_save": {
                "fqn": fqn,
                "memory_status": status,
                "scope": scope,
                "category": category,
                "storage": storage_hint,
                "recallable": recallable,
                "review_required": review_required,
            }
        },
    )


def _storage_hint(data_dir: str | Path | None) -> str:
    if data_dir is None:
        return "configured Anteroom app data directory"
    raw = str(data_dir)
    home = str(Path.home())
    if raw == home:
        return "~"
    if raw.startswith(home + "/"):
        return "~/" + raw[len(home) + 1 :]
    return raw or "configured Anteroom app data directory"
