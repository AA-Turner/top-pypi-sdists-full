"""Team layer — Sofia / Tina / Samantha / Robin (the Core 4).

Idempotent registration of the canonical 4-agent team into the hive-mind
agent index, plus a small REST surface for the dashboard.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

# Canonical Core-4 roster — Sofia is the Master Orchestrator.
CORE_TEAM: List[Dict[str, Any]] = [
    {
        "agent_id": "SOFIA-01",
        "name": "Sofia",
        "role": "orchestrator",
        "rank": "zeus",
        "squad": "core",
        "capabilities": ["orchestration", "strategy", "comms"],
        "metadata": {"description": "Master Orchestrator & Chief Intelligence."},
    },
    {
        "agent_id": "TINA-01",
        "name": "Tina",
        "role": "developer",
        "rank": "specialist",
        "squad": "core",
        "capabilities": ["coding", "implementation", "debugging"],
        "metadata": {"description": "Main Developer."},
    },
    {
        "agent_id": "SAM-01",
        "name": "Samantha",
        "role": "researcher",
        "rank": "specialist",
        "squad": "core",
        "capabilities": ["research", "science", "forecasting"],
        "metadata": {"description": "AI Researcher & Scientist."},
    },
    {
        "agent_id": "ROBIN-01",
        "name": "Robin",
        "role": "cto",
        "rank": "captain",
        "squad": "core",
        "capabilities": ["deployment", "scaling", "business"],
        "metadata": {"description": "Business & Scalability CTO."},
    },
]


def ensure_core_team(db) -> List[Dict[str, Any]]:
    """Insert any missing Core-4 agents into the agent index. Idempotent."""
    inserted: List[Dict[str, Any]] = []
    if db is None or not hasattr(db, "index"):
        return inserted
    idx = db.index
    for spec in CORE_TEAM:
        try:
            existing = idx.get_agent(spec["agent_id"]) if hasattr(idx, "get_agent") else None
        except Exception:
            existing = None
        if existing:
            continue
        try:
            idx.insert_agent(
                agent_id=spec["agent_id"],
                name=spec["name"],
                role=spec["role"],
                rank=spec["rank"],
                squad=spec["squad"],
            )
            inserted.append(spec)
            logger.info("Core-team: registered %s", spec["agent_id"])
        except Exception as exc:  # noqa: BLE001
            logger.warning("Core-team: failed to register %s: %s", spec["agent_id"], exc)
    return inserted


def register_team_routes(app: FastAPI) -> None:
    """Mount /api/team routes."""

    @app.get("/api/team")
    async def get_team() -> Dict[str, Any]:
        # Lazy hive lookup — gateway exposes _get_db()
        from cvc import gateway as gw  # type: ignore

        try:
            gw._ensure()
            db = gw._get_db()
            ensure_core_team(db)
            agents = db.index.list_agents() if hasattr(db.index, "list_agents") else []
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(500, f"Hive lookup failed: {exc}")

        wanted = {a["agent_id"] for a in CORE_TEAM}
        roster: List[Dict[str, Any]] = []
        for a in agents:
            d = a if isinstance(a, dict) else {
                k: getattr(a, k, None)
                for k in ("agent_id", "name", "role", "rank", "squad", "status")
            }
            if d.get("agent_id") in wanted:
                # Merge canonical metadata (description, capabilities)
                spec = next(s for s in CORE_TEAM if s["agent_id"] == d["agent_id"])
                d["description"] = spec["metadata"].get("description")
                d["capabilities"] = spec["capabilities"]
                roster.append(d)
        # Maintain canonical order
        order = {s["agent_id"]: i for i, s in enumerate(CORE_TEAM)}
        roster.sort(key=lambda x: order.get(x.get("agent_id"), 99))
        return {"team": roster, "total": len(roster), "canonical": CORE_TEAM}

    @app.post("/api/team/ensure")
    async def post_ensure_team() -> Dict[str, Any]:
        from cvc import gateway as gw  # type: ignore

        gw._ensure()
        inserted = ensure_core_team(gw._get_db())
        return {"inserted": inserted, "count": len(inserted)}
