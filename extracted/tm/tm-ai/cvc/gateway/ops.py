"""
Ops router — CVC's cognitive version control (commits, branches, recall, etc.)

Thin wrapper around the cvc mcp tools (mcp_cvc_*). The MCP tools are
the source of truth for CVC's cognitive commits.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("cvc.gateway.ops")

router = APIRouter()


class CommitBody(BaseModel):
    message: str
    commit_type: str = "checkpoint"


class BranchBody(BaseModel):
    name: str
    description: str | None = None


class MergeBody(BaseModel):
    source_branch: str
    target_branch: str = "main"


class RestoreBody(BaseModel):
    commit_hash: str


@router.get("/status")
async def ops_status():
    """Proxy to mcp_cvc_cvc_status."""
    from cvc.gateway.mcp_bridge import call_mcp
    return await call_mcp("cvc_status")


@router.post("/commit")
async def ops_commit(body: CommitBody):
    from cvc.gateway.mcp_bridge import call_mcp
    result = await call_mcp("cvc_commit", message=body.message, commit_type=body.commit_type)
    # C4: spine capture (best-effort, never raises)
    try:
        from cvc.events.spine import capture
        from cvc.gateway.mcp_bridge import _get_workspace_from_mcp_context
        commit_hash = ""
        if isinstance(result, dict):
            commit_hash = result.get("hash") or result.get("commit_hash") or ""
        capture(
            kind="ops.commit",
            workspace=_get_workspace_from_mcp_context(),
            channel="ops",
            actor="Jai",
            summary=body.message[:200],
            data={"message": body.message[:500], "commit_type": body.commit_type},
            branch="main",
            tags=["vcs"],
        )
    except Exception:
        pass
    return result


@router.post("/branch")
async def ops_branch(body: BranchBody):
    from cvc.gateway.mcp_bridge import call_mcp
    result = await call_mcp("cvc_branch", name=body.name, description=body.description)
    try:
        from cvc.events.spine import capture
        from cvc.gateway.mcp_bridge import _get_workspace_from_mcp_context
        capture(
            kind="ops.branch",
            workspace=_get_workspace_from_mcp_context(),
            channel="ops",
            actor="Jai",
            summary=f"branch: {body.name}",
            data={"name": body.name, "description": body.description or ""},
            branch=body.name,
            tags=["vcs"],
        )
    except Exception:
        pass
    return result


@router.post("/merge")
async def ops_merge(body: MergeBody):
    from cvc.gateway.mcp_bridge import call_mcp
    result = await call_mcp("cvc_merge", source_branch=body.source_branch, target_branch=body.target_branch)
    try:
        from cvc.events.spine import capture
        from cvc.gateway.mcp_bridge import _get_workspace_from_mcp_context
        capture(
            kind="ops.merge",
            workspace=_get_workspace_from_mcp_context(),
            channel="ops",
            actor="Jai",
            summary=f"{body.source_branch} → {body.target_branch}",
            data={"source": body.source_branch, "target": body.target_branch},
            branch=body.target_branch,
            tags=["vcs"],
        )
    except Exception:
        pass
    return result


@router.post("/restore")
async def ops_restore(body: RestoreBody):
    from cvc.gateway.mcp_bridge import call_mcp
    result = await call_mcp("cvc_restore", commit_hash=body.commit_hash)
    try:
        from cvc.events.spine import capture
        from cvc.gateway.mcp_bridge import _get_workspace_from_mcp_context
        capture(
            kind="ops.restore",
            workspace=_get_workspace_from_mcp_context(),
            channel="ops",
            actor="Jai",
            summary=f"restored {body.commit_hash[:12]}",
            data={"commit_hash": body.commit_hash},
            branch="main",
            tags=["vcs"],
        )
    except Exception:
        pass
    return result


@router.get("/recall")
async def ops_recall(query: str, limit: int = 5, deep: bool = True):
    from cvc.gateway.mcp_bridge import call_mcp
    return await call_mcp("cvc_recall", query=query, limit=limit, deep=deep)


@router.get("/diff")
async def ops_diff(hash_a: str, hash_b: str | None = None):
    from cvc.gateway.mcp_bridge import call_mcp
    return await call_mcp("cvc_diff", hash_a=hash_a, hash_b=hash_b)


@router.get("/timeline")
async def ops_timeline(limit: int = 50):
    from cvc.gateway.mcp_bridge import call_mcp
    return await call_mcp("cvc_timeline", limit=limit)


@router.get("/branches")
async def ops_branches():
    from cvc.gateway.mcp_bridge import call_mcp
    return await call_mcp("cvc_hive_status")
