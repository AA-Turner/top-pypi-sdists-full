"""REST API for automation management and webhook endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

# Management endpoints — /api/automation/*
router = APIRouter(prefix="/automation", tags=["automation"])

# Webhook endpoints — /api/hooks/*
hooks_router = APIRouter(prefix="/hooks", tags=["hooks"])


# ── Pydantic request/response models ───────────────────────────────────────

class JobCreate(BaseModel):
    name: str
    schedule_type: str          # at / every / cron
    schedule_value: str
    payload: str
    mode: str = "main_session"  # main_session / isolated


class JobUpdate(BaseModel):
    name: str | None = None
    schedule_type: str | None = None
    schedule_value: str | None = None
    payload: str | None = None
    mode: str | None = None
    enabled: bool | None = None


class ConfigUpdate(BaseModel):
    cron_enabled: bool | None = None
    max_concurrent_runs: int | None = None
    heartbeat_enabled: bool | None = None
    heartbeat_interval: int | None = None
    heartbeat_active_hours: list[int] | None = None
    heartbeat_payload: str | None = None
    webhooks_enabled: bool | None = None
    webhooks_token: str | None = None
    custom_hooks: dict[str, str] | None = None


class WebhookPayload(BaseModel):
    message: str


# ── Helpers ────────────────────────────────────────────────────────────────

def _get_manager():
    from ..automation.manager import get_automation_manager
    mgr = get_automation_manager()
    if mgr is None:
        raise HTTPException(status_code=503, detail="Automation manager not initialized.")
    return mgr


def _check_webhook_token(authorization: str | None):
    mgr = _get_manager()
    config = mgr.get_config()
    if not config.webhooks.enabled:
        raise HTTPException(status_code=403, detail="Webhooks are not enabled.")
    expected = config.webhooks.token
    if not expected:
        raise HTTPException(status_code=403, detail="Webhook token not configured.")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")
    token = authorization[7:]
    if token != expected:
        raise HTTPException(status_code=401, detail="Invalid webhook token.")


# ── Management endpoints (/api/automation/) ────────────────────────────────

@router.get("/status")
async def automation_status():
    mgr = _get_manager()
    config = mgr.get_config()
    jobs = mgr.list_jobs()
    return {"config": config.to_dict(), "jobs": jobs, "job_count": len(jobs)}


@router.get("/jobs")
async def list_jobs():
    mgr = _get_manager()
    return {"jobs": mgr.list_jobs()}


@router.post("/jobs", status_code=201)
async def create_job(body: JobCreate):
    mgr = _get_manager()
    try:
        job = mgr.add_job(
            name=body.name,
            schedule_type=body.schedule_type,
            schedule_value=body.schedule_value,
            payload=body.payload,
            mode=body.mode,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"job": job.to_dict()}


@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    mgr = _get_manager()
    if mgr.remove_job(job_id):
        return {"deleted": True, "job_id": job_id}
    raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")


@router.patch("/jobs/{job_id}")
async def update_job(job_id: str, body: JobUpdate):
    mgr = _get_manager()
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided.")
    job = mgr.update_job(job_id, **updates)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return {"job": job.to_dict()}


@router.put("/config")
async def update_config(body: ConfigUpdate):
    mgr = _get_manager()
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    config = mgr.update_config(**updates)
    return {"config": config.to_dict()}


# ── Webhook endpoints (/api/hooks/) ────────────────────────────────────────

@hooks_router.post("/wake")
async def webhook_wake(
    body: WebhookPayload,
    authorization: str | None = Header(default=None),
):
    """Inject a system event into the main session (StoredChannel)."""
    _check_webhook_token(authorization)

    from ..channels.stored import StoredChannel
    from ..channels.base import ChannelEvent
    from ..config import get_config

    config = get_config()
    emdash_dir = __import__("pathlib").Path(config.repo_root or ".") / ".emdash"

    stored = StoredChannel(emdash_dir)
    event = ChannelEvent(
        type="webhook",
        content=body.message,
        metadata={"source": "webhook_wake"},
    )
    await stored.send_event("webhook", event)
    return {"status": "injected"}


@hooks_router.post("/agent", status_code=202)
async def webhook_agent(
    body: WebhookPayload,
    authorization: str | None = Header(default=None),
):
    """Run an isolated agent turn and deliver the result via ChannelRouter."""
    _check_webhook_token(authorization)

    import asyncio
    import httpx
    from ..channels.router import get_channel_router
    from ..channels.base import ChannelEvent
    from ..config import get_config
    from ..automation.scheduler import CronScheduler

    config = get_config()
    server_url = f"http://{config.host}:{config.port}"

    async def _run():
        response_text = ""
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                url = f"{server_url}/api/agent/chat"
                async with client.stream("POST", url, json={
                    "message": body.message,
                    "agent_type": "open",
                }) as resp:
                    resp.raise_for_status()
                    response_text = await CronScheduler._read_agent_response_from_sse(resp)
        except Exception:
            pass

        if response_text:
            router = get_channel_router()
            if router:
                event = ChannelEvent(
                    type="text",
                    content=response_text,
                    metadata={"source": "webhook_agent"},
                )
                await router.deliver(event, sender_id="webhook")

    asyncio.create_task(_run())
    return {"status": "accepted"}


@hooks_router.post("/{hook_name}")
async def webhook_custom(
    hook_name: str,
    request: Request,
    authorization: str | None = Header(default=None),
):
    """Fire a custom named webhook with template substitution."""
    _check_webhook_token(authorization)

    mgr = _get_manager()
    config = mgr.get_config()
    template = config.webhooks.custom_hooks.get(hook_name)
    if not template:
        raise HTTPException(status_code=404, detail=f"Custom hook '{hook_name}' not found.")

    # Parse body for template substitution
    try:
        body = await request.json()
    except Exception:
        body = {}

    # Simple template substitution: {{key}} → value
    payload = template
    if isinstance(body, dict):
        for key, value in body.items():
            payload = payload.replace("{{" + key + "}}", str(value))

    from ..channels.stored import StoredChannel
    from ..channels.base import ChannelEvent
    from ..config import get_config as get_server_config

    server_config = get_server_config()
    emdash_dir = __import__("pathlib").Path(server_config.repo_root or ".") / ".emdash"

    stored = StoredChannel(emdash_dir)
    event = ChannelEvent(
        type="webhook",
        content=payload,
        metadata={"source": f"webhook_{hook_name}", "hook_name": hook_name},
    )
    await stored.send_event("webhook", event)
    return {"status": "injected", "hook": hook_name}
