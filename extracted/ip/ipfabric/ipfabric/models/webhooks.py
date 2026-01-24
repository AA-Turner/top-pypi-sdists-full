from datetime import datetime
from typing import Optional, Literal, Annotated

from pydantic import BaseModel, Field, AliasPath, BeforeValidator, AliasChoices

WEBHOOK_TYPES = Literal["snapshot", "intent-verification"]


class BaseEvent(BaseModel):
    test: Optional[bool] = Field(False, description="Indicates if this is a test event.")
    reason: Optional[str] = None
    requester: str = Field(examples=["cron", "user:<id>", "snapshot:<action>", "recalculateSites"])
    timestamp: datetime = Field(description="Timestamp of the event.")
    status: str = Field(examples=["started", "completed", "failed", "resumed", "resumed (stopping)", "stopped"])


class SnapshotEvent(BaseEvent, BaseModel):
    type: Literal["snapshot"] = "snapshot"
    action: Literal["discover", "clone", "delete", "download", "load", "unload"] = Field(
        examples=["discover", "clone", "delete", "download", "load", "unload"]
    )
    snapshotId: Optional[str] = Field(None, validation_alias=AliasChoices("snapshotId", AliasPath("snapshot", "id")))
    name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("name", AliasPath("snapshot", "name")),
        description="Name of the snapshot.",
    )
    cloneId: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("cloneId", AliasPath("snapshot", "cloneId")),
        description="ID of the snapshot being cloned.",
    )
    file: Optional[str] = Field(
        None,
        validation_alias=AliasChoices(AliasPath("snapshot", "file")),
        description="Filename associated with the snapshot download.",
    )


class IntentEvent(BaseEvent, BaseModel):
    type: Literal["intent-verification"] = "intent-verification"
    action: Literal["calculate"] = "calculate"
    reportId: Optional[Annotated[str, BeforeValidator(str)]] = None
    snapshotId: Optional[str] = None


try:
    from sqlmodel import Field as SField, SQLModel

    class WebhookEvent(SnapshotEvent, IntentEvent, SQLModel, table=True):
        __tablename__ = "webhook_events"
        dbId: Optional[int] = SField(default=None, primary_key=True, description="Auto-generated database ID")
        snapshotId: Optional[str] = SField(None, index=True)
        type: str = SField(index=True, description="One of 'intent-verification' or 'snapshot'")
        action: str = Field(examples=["discover", "clone", "delete", "download", "load", "unload", "calculate"])

except ImportError:
    WebhookEvent = None
