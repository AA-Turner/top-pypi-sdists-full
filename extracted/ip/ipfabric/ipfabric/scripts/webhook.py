import hmac
import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import Optional, Union, Annotated, Any

from fastapi import Request, status, BackgroundTasks, Response
from pydantic import Field, BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import func
from sqlmodel import Session, select, or_

from ipfabric.models.webhooks import IntentEvent, SnapshotEvent, WebhookEvent

AnnotatedWebhookEvent = Annotated[Union[IntentEvent, SnapshotEvent], Field(discriminator="type")]


class WebhookResponse(BaseModel):
    total: int
    size: int
    start: int
    limit: int
    next: Optional[str] = None
    items: list[WebhookEvent]


class WebhookConfig(BaseSettings, cli_parse_args=True):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    # uvicorn settings
    uvicorn_ip: str = Field("0.0.0.0", description="IP address to bind the FastAPI server.")
    uvicorn_port: int = Field(8000, description="Port to bind the FastAPI server.")
    uvicorn_reload: bool = Field(False, description="Enable auto-reload for the FastAPI server.")

    # API settings
    ipf_secret: Optional[str] = Field(
        None, description="Secret token to validate incoming webhook requests. Validation will be skipped if not set."
    )
    database_url: str = Field("sqlite:///database.db", description="Database URL for storing webhook events.")
    title: str = Field("IP Fabric Webhook Receiver", description="Title of the FastAPI application.")
    webhook_path: str = Field(
        "/ipfabric", description="Path where the webhook endpoint will be available, default '/ipfabric'."
    )
    custom_settings: Optional[Any] = Field(
        None, description="Settings to pass to your custom functions. You functions must handle this parameter."
    )

    # Snapshot event settings
    snapshot_method: Optional[str] = Field(
        None,
        description="Path to the Python file containing the snapshot processing method in 'path:function' format.",
        examples=["my_script.py:snapshot_event"],
    )
    snapshot_scheduled_only: bool = Field(
        True, description="If set to True, only process webhooks from scheduled snapshots"
    )

    # Intent verification event settings
    intent_method: Optional[str] = Field(
        None,
        description="Path to the Python file containing the intent processing method in 'path:function' format.",
        examples=["my_script.py:intent_event"],
    )
    intent_scheduled_only: bool = Field(
        True,
        description="If set to True, only process webhooks from scheduled snapshots' intent verifications. "
        "Requires 'snapshot_event' to be configured and received for intent calculations.",
    )

    @field_validator("snapshot_method", "intent_method", mode="after")
    @classmethod
    def load_methods(cls, value: Optional[str]):
        if not value:
            return value
        _ = value.split(":")
        if len(_) != 2:
            raise ValueError("Method must be in 'path:function' format.")
        path = Path(_[0])
        if not path.is_file():
            raise ValueError(f"File '{str(path)}' does not exist.")
        module_name = str(path)
        if module_name not in sys.modules:
            spec = spec_from_file_location(module_name, path)
            module = module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        else:
            module = sys.modules[module_name]
        if not hasattr(module, _[1]):
            raise ValueError(f"Function '{_[1]}' not found in module '{module_name}'.")
        return getattr(module, _[1])


async def verify_signature(request: Request, x_ipf_signature: str, secret: Optional[str] = None) -> tuple[bool, str]:
    """Verify the HMAC signature of the incoming request"""
    if secret:
        if x_ipf_signature is None:
            return False, "X-IPF-Signature header missing."

        input_hmac = hmac.new(key=secret.encode(), msg=await request.body(), digestmod="sha256")
        if not hmac.compare_digest(input_hmac.hexdigest(), x_ipf_signature):
            # Signature does not match, possible tampering
            return False, "X-IPF-Signature does not match."
    return True, ""


def calc_method(event: AnnotatedWebhookEvent, bg_tasks: BackgroundTasks, session: Session, settings: WebhookConfig):
    """Determine and execute the appropriate method for the event"""
    etype = "snapshot" if event.type == "snapshot" else "intent"
    if not getattr(settings, f"{etype}_event"):
        # If event type processing is disabled, return 204 No Content
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # Store the event in the database
    record = WebhookEvent.model_validate(event)
    session.add(record)
    session.commit()
    session.refresh(record)

    if etype == "snapshot" and settings.snapshot_scheduled_only and event.requester != "cron":
        # If not a scheduled snapshot, skip processing
        return record

    # Check if the related snapshot was a scheduled one
    query = (
        select(WebhookEvent)
        .where(WebhookEvent.type == "snapshot")
        .where(WebhookEvent.action == "discover")
        .where(WebhookEvent.snapshotId == event.snapshotId)
        .where(WebhookEvent.status == "completed")
    )
    if (
        etype == "intent"
        and settings.intent_scheduled_only
        and (
            event.requester != "snapshot:discover"  # Intent not from snapshot discover
            or not session.exec(query.where(WebhookEvent.requester == "cron")).first()  # No scheduled snapshot found
            or session.exec(query.where(WebhookEvent.requester != "cron")).first()  # Snapshot was modified by user
        )
    ):
        # If not a scheduled snapshot's (or modified scheduled snapshot) intent verification, skip processing
        return record

    if method := getattr(settings, f"{etype}_method"):
        bg_tasks.add_task(method, event=record, settings=settings.custom_settings)
    return record


def query_db(
    session: Session,
    endpoint: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    snapshotId: Optional[str] = None,
):
    """Generic database query function"""
    query = or_(WebhookEvent.type == "snapshot", WebhookEvent.type == "intent-verification")
    if endpoint == "snapshots":
        query = WebhookEvent.type == "snapshot"
    elif endpoint == "intents":
        query = WebhookEvent.type == "intent-verification"
    if snapshotId:
        count = session.exec(
            select(func.count(WebhookEvent.dbId)).where(query).where(WebhookEvent.snapshotId == snapshotId)
        ).one()
        items = session.exec(
            select(WebhookEvent).where(query).where(WebhookEvent.snapshotId == snapshotId).offset(offset).limit(limit)
        ).all()
    else:
        count = session.exec(select(func.count(WebhookEvent.dbId)).where(query)).one()
        items = session.exec(select(WebhookEvent).where(query).offset(offset).limit(limit)).all()
    link = f"/{endpoint}/?offset={offset + limit}&limit={limit}" if count > len(items) + offset else None
    if link and snapshotId:
        link += f"&snapshotId={snapshotId}"
    return {
        "total": count,
        "size": len(items),
        "items": items,
        "start": offset,
        "limit": limit,
        "next": link,
    }
