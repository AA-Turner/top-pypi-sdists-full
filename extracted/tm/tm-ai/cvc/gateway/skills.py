"""
Skills / Toolsets / Capabilities router — /api/skills, /api/toolsets, /api/capabilities

Proxies the vendored api_server's catalog endpoints but in-process.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

logger = logging.getLogger("cvc.gateway.skills")

router = APIRouter()

# Skills directories to scan — vendored + CVC bundled + CVC's own ~/.cvc/skills/ + project-local
def _default_search_paths() -> list[Path]:
    """Resolve the CVC bundled-skills tree relative to this file's package."""
    paths: list[Path] = []
    try:
        # /.../cvc/gateway/skills.py → /.../cvc/  →  /.../cvc/bundled_skills/
        pkg_root = Path(__file__).resolve().parent.parent
        bundled = pkg_root / "bundled_skills"
        if bundled.exists():
            paths.append(bundled)
    except Exception:
        pass
    # Dev-tree fallbacks (only relevant when running from a checkout, not the wheel)
    for dev_path in (
        Path("/Users/jkm/Projects/cvc/cvc/bundled_skills"),
        Path("/Users/jkm/Projects/cvc/cvc/agent/_vendor/hermes/skills"),
        Path("/Users/jkm/Projects/cvc/cvc/agent/_vendor/hermes/optional-skills"),
        Path("/Users/jkm/Projects/cvc/cvc/skills"),
        Path("/Users/jkm/.cvc/skills"),
        Path("/Users/jkm/.cvc/skills"),
    ):
        if dev_path.exists() and dev_path not in paths:
            paths.append(dev_path)
    return paths


SKILL_SEARCH_PATHS: list[Path] = _default_search_paths()  # fmt: skip


@router.get("/skills")
async def list_skills():
    """List all available skills. Format: [{name, description, category, path}]"""
    skills: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()  # (name, category) dedup key

    def _maybe_add(skill: dict[str, Any]) -> None:
        key = (skill.get("name", ""), skill.get("category", ""))
        if key not in seen and skill.get("name"):
            seen.add(key)
            skills.append(skill)

    for base in SKILL_SEARCH_PATHS:
        if not base.exists():
            continue
        try:
            # Structure: <base>/<category>/<skill>/[SKILL.md|scripts/]
            # But some bases have skills directly: <base>/<skill>/...
            # Walk one or two levels deep to find skill dirs.
            for entry in base.iterdir():
                if not entry.is_dir():
                    continue
                if (entry / "SKILL.md").exists() or (entry / "scripts").exists() or (entry / "scripts").is_dir():
                    # entry is itself a skill
                    skill = _describe_skill(entry)
                    if skill:
                        _maybe_add(skill)
                else:
                    # entry is a category — recurse one level
                    try:
                        for sub in entry.iterdir():
                            if not sub.is_dir():
                                continue
                            if (sub / "SKILL.md").exists() or (sub / "scripts").exists() or (sub / "scripts").is_dir():
                                skill = _describe_skill(sub)
                                if skill:
                                    _maybe_add(skill)
                    except Exception as e:
                        logger.debug("recurse %s: %s", entry, e)
        except Exception as e:
            logger.debug("scan %s: %s", base, e)

    # Also pick up the workspace's CVC skills if a workspace is configured
    try:
        from cvc.gateway.agent import get_config
        cfg = get_config()
        ws = cfg.get("workspace_path")
        if ws:
            ws_path = Path(ws) / ".cvc" / "skills"
            if ws_path.exists():
                for entry in ws_path.iterdir():
                    if not entry.is_dir():
                        continue
                    skill = _describe_skill(entry)
                    if skill:
                        _maybe_add(skill)
    except Exception:
        pass

    return {"skills": skills}


@router.get("/toolsets")
async def list_toolsets():
    """List available toolsets and the tools they include."""
    try:
        from cvc.agent._vendor.hermes.toolsets import TOOLSETS, resolve_toolset
    except Exception as e:
        logger.exception("import toolsets")
        return {"toolsets": [], "error": str(e)}

    toolsets = []
    for name, info in TOOLSETS.items():
        try:
            resolved = sorted(resolve_toolset(name))
        except Exception:
            resolved = list(info.get("tools", []))
        toolsets.append({
            "name": name,
            "description": info.get("description", ""),
            "tools": resolved,
            "tool_count": len(resolved),
        })
    return {"toolsets": toolsets}


@router.get("/capabilities")
async def list_capabilities():
    """List all the surface area the CVC gateway exposes to the dashboard."""
    return {
        "capabilities": {
            "chat": {
                "methods": ["POST"],
                "path": "/api/chat",
                "transport": "SSE",
                "description": "Streaming chat (OpenAI-style messages array).",
            },
            "chat_websocket": {
                "methods": ["WS"],
                "path": "/api/ws/chat",
                "transport": "WebSocket",
                "description": "Streaming chat over WebSocket.",
            },
            "sessions": {
                "methods": ["GET", "POST"],
                "path": "/api/sessions",
                "description": "List / create chat sessions.",
            },
            "session_detail": {
                "methods": ["GET", "DELETE"],
                "path": "/api/sessions/{id}",
                "description": "Get or delete a session.",
            },
            "session_messages": {
                "methods": ["GET"],
                "path": "/api/sessions/{id}/messages",
                "description": "Get the message history for a session.",
            },
            "runs": {
                "methods": ["GET", "POST"],
                "path": "/api/runs",
                "description": "List or create structured runs.",
            },
            "run_detail": {
                "methods": ["GET"],
                "path": "/api/runs/{id}",
                "description": "Get a run's status.",
            },
            "run_events": {
                "methods": ["GET"],
                "path": "/api/runs/{id}/events",
                "description": "Get run events (pollable).",
            },
            "skills": {
                "methods": ["GET"],
                "path": "/api/skills",
                "description": "List available skills.",
            },
            "toolsets": {
                "methods": ["GET"],
                "path": "/api/toolsets",
                "description": "List available toolsets and their tools.",
            },
            "models": {
                "methods": ["GET"],
                "path": "/api/models",
                "description": "List available LLM models.",
            },
            "capabilities": {
                "methods": ["GET"],
                "path": "/api/capabilities",
                "description": "This endpoint.",
            },
        }
    }


def _describe_skill(skill_dir: Path) -> dict[str, Any] | None:
    """Read a skill's SKILL.md or scripts/ structure to extract name + description."""
    # Modern format: SKILL.md in the skill dir
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        try:
            content = skill_md.read_text(encoding="utf-8", errors="replace")
            name, desc = _parse_skill_frontmatter(content)
            return {
                "name": name or skill_dir.name,
                "description": desc,
                "category": skill_dir.parent.name,
                "path": str(skill_dir),
                "format": "skill_md",
            }
        except Exception:
            pass

    # Legacy format: scripts/ subdir
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        # Try to read a README.md or any .md for description
        desc = None
        for md_name in ("README.md", "SKILL.md"):
            md = skill_dir / md_name
            if md.exists():
                try:
                    desc = md.read_text(encoding="utf-8", errors="replace").splitlines()[0]
                    break
                except Exception:
                    pass
        return {
            "name": skill_dir.name,
            "description": desc or f"Skill with scripts in {scripts_dir.name}/",
            "category": skill_dir.parent.name,
            "path": str(skill_dir),
            "format": "scripts_dir",
        }
    return None


def _parse_skill_frontmatter(content: str) -> tuple[str | None, str | None]:
    """Parse YAML frontmatter from a SKILL.md file."""
    name = None
    desc = None
    if not content.startswith("---"):
        return None, None
    end = content.find("\n---", 3)
    if end < 0:
        return None, None
    front = content[3:end].strip()
    for line in front.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            desc = line.split(":", 1)[1].strip().strip('"').strip("'")
    return name, desc


# ── Auto-skill drafts endpoints ──────────────────────────────────────
#
# CVC's runtime-independent implementation of the auto-skill-creation
# pattern that upstream ships only as a system-prompt instruction. When a
# turn completes, the chat endpoint's post-turn hook calls
# ``cvc.agent.auto_skill.maybe_create_draft``. The result is a draft
# SKILL.md under ``~/.cvc/skills/.drafts/``. These endpoints let the
# dashboard surface the drafts and the user approve / reject them.


@router.get("/skills/drafts")
async def list_drafts(state: str = "draft"):
    """List pending auto-generated skill drafts awaiting review.

    Pass ``?state=approved`` or ``?state=rejected`` for history.
    """
    try:
        from cvc.skills.drafts import list_drafts as _list_drafts
        records = _list_drafts(state=state)
        return {
            "count": len(records),
            "state": state,
            "drafts": [r.to_jsonable() for r in records],
        }
    except Exception as e:
        logger.exception("list drafts")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/skills/drafts/summary")
async def drafts_summary():
    """Compact summary for the dashboard's 'drafts awaiting review' badge."""
    try:
        from cvc.skills.drafts import drafts_summary as _summarize
        return _summarize()
    except Exception as e:
        logger.exception("drafts summary")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/skills/drafts/{name}")
async def get_draft(name: str):
    """Return the full SKILL.md content for one draft."""
    from cvc.skills.drafts import DRAFTS_DIR
    # Block path traversal
    if "/" in name or ".." in name:
        raise HTTPException(status_code=400, detail="invalid draft name")
    md = DRAFTS_DIR / name / "SKILL.md"
    if not md.exists():
        # Also check .archive/ for approved/rejected drafts
        archived = DRAFTS_DIR / ".archive" / name / "SKILL.md"
        if archived.exists():
            md = archived
        else:
            raise HTTPException(status_code=404, detail=f"draft not found: {name}")
    try:
        content = md.read_text(encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"name": name, "path": str(md), "content": content}


@router.post("/skills/drafts/{name}/approve")
async def approve_draft(name: str, category: str | None = None):
    """Promote a draft to the active skill tree."""
    if "/" in name or ".." in name:
        raise HTTPException(status_code=400, detail="invalid draft name")
    try:
        from cvc.skills.drafts import approve_draft as _approve
        dest = _approve(name, category=category)
        return {"name": name, "promoted_to": str(dest), "state": "approved"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("approve draft")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/skills/drafts/{name}/reject")
async def reject_draft(name: str, reason: str | None = None):
    """Reject and archive a draft."""
    if "/" in name or ".." in name:
        raise HTTPException(status_code=400, detail="invalid draft name")
    try:
        from cvc.skills.drafts import reject_draft as _reject
        _reject(name, reason=reason)
        return {"name": name, "state": "rejected"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("reject draft")
        raise HTTPException(status_code=500, detail=str(e))
