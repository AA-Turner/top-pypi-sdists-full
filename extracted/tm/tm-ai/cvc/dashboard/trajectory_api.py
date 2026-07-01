"""REST surface for trajectory JSONL files written by TrajectoryRecorder."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query

logger = logging.getLogger(__name__)


def _default_dir() -> Path:
    return Path.home() / ".cvc" / "trajectories"


def _list_files(dir_path: Path) -> List[Dict[str, Any]]:
    if not dir_path.exists():
        return []
    out: List[Dict[str, Any]] = []
    for p in sorted(dir_path.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            st = p.stat()
            out.append(
                {
                    "name": p.name,
                    "path": str(p),
                    "size_bytes": st.st_size,
                    "modified": st.st_mtime,
                }
            )
        except OSError:
            continue
    return out


def _tail_jsonl(path: Path, limit: int) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    # Cheap full-file read; trajectories are small (<5 MB typical)
    lines: List[str] = []
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return []
    out: List[Dict[str, Any]] = []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def register_trajectory_routes(app: FastAPI) -> None:
    """Mount /api/trajectory/* routes."""

    from cvc.dashboard import loop_state

    @app.get("/api/trajectory/files")
    async def list_trajectories(dir: Optional[str] = None) -> Dict[str, Any]:
        d = Path(dir).expanduser() if dir else _default_dir()
        return {"dir": str(d), "files": _list_files(d)}

    @app.get("/api/trajectory/tail")
    async def tail_trajectory(
        file: Optional[str] = None,
        limit: int = Query(50, ge=1, le=500),
    ) -> Dict[str, Any]:
        path: Optional[Path] = None
        if file:
            path = Path(file).expanduser()
        else:
            # try active recorder
            snap = loop_state.snapshot()
            rec = snap.get("recorder", {})
            if rec.get("path"):
                path = Path(rec["path"]).expanduser()
            else:
                # fall back to most recent file in default dir
                files = _list_files(_default_dir())
                if files:
                    path = Path(files[0]["path"])
        if path is None or not path.exists():
            raise HTTPException(status_code=404, detail="No trajectory file found")
        return {
            "path": str(path),
            "turns": _tail_jsonl(path, limit),
        }

    @app.get("/api/trajectory/summary")
    async def trajectory_summary(file: Optional[str] = None) -> Dict[str, Any]:
        path: Optional[Path] = Path(file).expanduser() if file else None
        if path is None:
            files = _list_files(_default_dir())
            if files:
                path = Path(files[0]["path"])
        if path is None or not path.exists():
            return {"path": None, "turns": 0, "tokens": {"prompt": 0, "completion": 0}}
        turns = _tail_jsonl(path, 10_000)
        ptot = sum(int(t.get("prompt_tokens") or 0) for t in turns)
        ctot = sum(int(t.get("completion_tokens") or 0) for t in turns)
        cache = sum(int(t.get("cache_read_tokens") or 0) for t in turns)
        models = sorted({(t.get("provider") or "?") + ":" + (t.get("model") or "?") for t in turns})
        return {
            "path": str(path),
            "turns": len(turns),
            "tokens": {"prompt": ptot, "completion": ctot, "cache_read": cache},
            "models": models,
        }
