"""REST API endpoints for Agent Teams.

Provides HTTP/SSE interface for CLI, Web, and Desktop clients to:
- Create and manage teams
- Spawn and control teammates
- Send messages and view message history
- Stream real-time team events

All endpoints are prefixed with /api/agent-teams/.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Any, Optional

router = APIRouter(prefix="/agent-teams", tags=["agent-teams"])


# ─────────────────────────────────────────────────────────────
# Request/Response models
# ─────────────────────────────────────────────────────────────


class CreateTeamRequest(BaseModel):
    """Request to create a new agent team."""
    name: str = Field(..., description="Team name")
    lead_agent_id: str = Field(..., description="Lead's session/agent ID")
    settings: dict[str, Any] = Field(default_factory=dict)


class SpawnTeammateRequest(BaseModel):
    """Request to spawn a new teammate."""
    name: str = Field(..., description="Teammate name")
    prompt: str = Field(..., description="Spawn instructions")
    model: str = Field("", description="LLM model override")
    labels: list[str] = Field(default_factory=list)
    require_plan_approval: bool = False
    use_worktree: bool = False


class SendMessageRequest(BaseModel):
    """Request to send a message between agents."""
    from_agent: str = Field(..., description="Sender name")
    to_agent: str = Field(..., description="Recipient name or 'all'")
    content: str = Field(..., description="Message body")
    message_type: str = Field("message", description="Message type")


class CreateTaskRequest(BaseModel):
    """Request to create a team task."""
    title: str
    description: str = ""
    labels: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)
    priority: int = 0
    assigned_to: str | None = None


class ApprovePlanRequest(BaseModel):
    """Request to approve/reject a teammate's plan."""
    approved: bool = True
    feedback: str = ""


class DelegateModeRequest(BaseModel):
    """Request to toggle delegate mode."""
    enabled: bool


# ─────────────────────────────────────────────────────────────
# Team lifecycle
# ─────────────────────────────────────────────────────────────


# In-memory registry of active teams (one per server process)
_active_teams: dict[str, Any] = {}  # team_name -> TeamManager


def _get_manager(team_name: str):
    """Get the TeamManager for a team, or raise 404."""
    manager = _active_teams.get(team_name)
    if not manager:
        raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")
    return manager


@router.post("/teams")
async def create_team(request: CreateTeamRequest):
    """Create a new agent team."""
    from pathlib import Path
    from ..agent.teams.manager import TeamManager, is_agent_teams_enabled
    from ..core.config import enable_experimental

    # Auto-enable agent teams on first use
    if not is_agent_teams_enabled():
        enable_experimental("agent_teams")

    if request.name in _active_teams:
        raise HTTPException(status_code=409, detail=f"Team '{request.name}' already exists")

    repo_root = Path.cwd()  # TODO: from request or config
    manager = TeamManager(
        team_name=request.name,
        repo_root=repo_root,
        lead_agent_id=request.lead_agent_id,
    )
    manager.activate()
    _active_teams[request.name] = manager

    return {"team": manager.get_status()}


@router.get("/teams")
async def list_teams():
    """List all active teams."""
    return {
        "teams": [
            manager.get_status()
            for manager in _active_teams.values()
        ]
    }


@router.get("/teams/{team_name}")
async def get_team(team_name: str):
    """Get team status."""
    manager = _get_manager(team_name)
    return {"team": manager.get_status()}


@router.delete("/teams/{team_name}")
async def cleanup_team(team_name: str, force: bool = False):
    """Clean up a team and release resources."""
    manager = _get_manager(team_name)
    await manager.cleanup(force=force)
    del _active_teams[team_name]
    return {"status": "cleaned_up", "team_name": team_name}


# ─────────────────────────────────────────────────────────────
# Teammate management
# ─────────────────────────────────────────────────────────────


@router.post("/teams/{team_name}/teammates")
async def spawn_teammate(team_name: str, request: SpawnTeammateRequest):
    """Spawn a new teammate in the team."""
    manager = _get_manager(team_name)

    try:
        handle = manager.spawn_teammate(
            name=request.name,
            prompt=request.prompt,
            model=request.model,
            labels=request.labels,
            require_plan_approval=request.require_plan_approval,
            use_worktree=request.use_worktree,
        )
        return {
            "name": handle.name,
            "agent_id": handle.agent_id,
            "status": "spawned",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/teams/{team_name}/teammates")
async def list_teammates(team_name: str):
    """List all teammates in a team."""
    manager = _get_manager(team_name)
    handles = manager.get_all_handles()

    return {
        "teammates": [
            {
                "name": h.name,
                "agent_id": h.agent_id,
                "status": h.status.value,
                "is_running": h.is_running,
                "current_task": h.current_task,
                "iterations": h.iterations,
            }
            for h in handles.values()
        ]
    }


@router.post("/teams/{team_name}/teammates/{name}/shutdown")
async def shutdown_teammate(team_name: str, name: str):
    """Request graceful shutdown of a teammate."""
    manager = _get_manager(team_name)
    stopped = await manager.shutdown_teammate(name)

    return {
        "name": name,
        "stopped": stopped,
        "status": "stopped" if stopped else "shutdown_requested",
    }


# ─────────────────────────────────────────────────────────────
# Messaging
# ─────────────────────────────────────────────────────────────


@router.post("/teams/{team_name}/messages")
async def send_message(team_name: str, request: SendMessageRequest):
    """Send a message between agents."""
    manager = _get_manager(team_name)

    if request.to_agent == "all":
        msg_ids = manager.broadcast(request.from_agent, request.content)
        return {"broadcast": True, "message_ids": msg_ids}
    else:
        msg_id = manager.send_message(
            from_name=request.from_agent,
            to_name=request.to_agent,
            content=request.content,
            message_type=request.message_type,
        )
        return {"message_id": msg_id}


@router.get("/teams/{team_name}/messages/{agent_name}")
async def get_messages(team_name: str, agent_name: str, history: bool = False):
    """Get pending or historical messages for an agent."""
    manager = _get_manager(team_name)

    if history:
        messages = manager.broker.get_history(agent_name)
    else:
        messages = manager.broker.receive(agent_name, mark_delivered=False)

    return {
        "agent_name": agent_name,
        "messages": [m.to_dict() for m in messages],
    }


@router.get("/teams/{team_name}/messages")
async def get_all_messages(team_name: str, limit: int = 100):
    """Get recent message history across all agents."""
    manager = _get_manager(team_name)
    messages = manager.broker.get_all_history(limit=limit)
    return {"messages": [m.to_dict() for m in messages]}


# ─────────────────────────────────────────────────────────────
# Tasks
# ─────────────────────────────────────────────────────────────


@router.post("/teams/{team_name}/tasks")
async def create_task(team_name: str, request: CreateTaskRequest):
    """Create a task in the team's shared task list."""
    manager = _get_manager(team_name)

    from ..agent.teams.tasks import create_team_task

    # Resolve assigned_to name to agent_id
    assigned_agent_id = None
    if request.assigned_to:
        member = manager.config.get_member(request.assigned_to)
        if member:
            assigned_agent_id = member.agent_id
        else:
            raise HTTPException(400, f"Unknown teammate: '{request.assigned_to}'")

    result = create_team_task(
        task_list_id=manager.task_list_id,
        title=request.title,
        description=request.description,
        labels=request.labels,
        depends_on=request.depends_on,
        priority=request.priority,
        assigned_to=assigned_agent_id,
    )

    return {"task": result}


@router.get("/teams/{team_name}/tasks")
async def get_tasks(team_name: str):
    """Get the team's shared task list with progress summary."""
    manager = _get_manager(team_name)

    from ..agent.teams.tasks import get_team_task_summary
    return get_team_task_summary(manager.task_list_id)


# ─────────────────────────────────────────────────────────────
# Plan approval
# ─────────────────────────────────────────────────────────────


@router.post("/teams/{team_name}/teammates/{name}/plan")
async def approve_plan(team_name: str, name: str, request: ApprovePlanRequest):
    """Approve or reject a teammate's implementation plan."""
    manager = _get_manager(team_name)

    msg_type = "plan_approved" if request.approved else "plan_rejected"
    content = request.feedback or "Plan approved. Proceed with implementation."

    manager.send_message(
        from_name="lead",
        to_name=name,
        content=content,
        message_type=msg_type,
    )

    return {
        "teammate": name,
        "approved": request.approved,
        "feedback": content,
    }


# ─────────────────────────────────────────────────────────────
# Delegate mode
# ─────────────────────────────────────────────────────────────


@router.post("/teams/{team_name}/delegate-mode")
async def set_delegate_mode(team_name: str, request: DelegateModeRequest):
    """Toggle delegate mode for the lead."""
    manager = _get_manager(team_name)
    manager.set_delegate_mode(request.enabled)
    return {"delegate_mode": request.enabled}


# ─────────────────────────────────────────────────────────────
# SSE event stream
# ─────────────────────────────────────────────────────────────


@router.get("/teams/{team_name}/stream")
async def stream_team_events(team_name: str, request: Request):
    """Stream real-time team events via Server-Sent Events.

    Events include:
    - Teammate lifecycle (spawned, idle, stopped)
    - Messages between agents
    - Task status changes
    - LLM iterations per teammate

    Each event is tagged with the originating teammate name.
    """
    import asyncio
    import json

    manager = _get_manager(team_name)

    async def event_generator():
        """Generate SSE events from the team."""
        # Subscribe to the lead's emitter for team events
        # This is a simplified version — full implementation would
        # use an async event queue connected to the emitter
        yield f"data: {json.dumps({'type': 'connected', 'team': team_name})}\n\n"

        try:
            while True:
                # Check for disconnection
                if await request.is_disconnected():
                    break

                # Poll team status (simplified — real impl uses event queue)
                status = manager.get_status()
                yield f"data: {json.dumps({'type': 'status', 'data': status})}\n\n"

                await asyncio.sleep(2.0)  # Poll interval

        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
