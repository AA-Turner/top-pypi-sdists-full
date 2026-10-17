"""Door names and the reproducible door pick (CONTRACT v2 §4.3)."""

from __future__ import annotations

import hashlib

__all__ = ["DOORS", "PICK_FN", "pick_door"]

DOORS: tuple[str, ...] = ("manual", "manual_chat", "agents", "mandates", "mcp_agent_run", "agent_call")
PICK_FN = "sha256_mod_v1"


def pick_door(eligible: list[str], *, seed: str, case_id: str, setup_key: str, repeat: int) -> str:
    """Same seed and same eligible set → same door, on every machine (``sha256_mod_v1``)."""
    doors = sorted(set(eligible))
    if not doors:
        raise ValueError("no eligible door")
    unknown = [d for d in doors if d not in DOORS]
    if unknown:
        raise ValueError(f"unknown door(s): {unknown}")
    digest = hashlib.sha256(f"{seed}:{case_id}:{setup_key}:{repeat}".encode()).hexdigest()
    return doors[int(digest, 16) % len(doors)]
