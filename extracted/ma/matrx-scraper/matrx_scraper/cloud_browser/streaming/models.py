"""Pydantic wire models for the mint/claim/renew/release/revoke seam.

Authority: contracts/S4-stream-tickets.md §2 (call shapes). Every field name and
shape here is the frozen contract three repos template against; renaming one is a
breaking change.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Mode = Literal["control", "view"]
ClientKind = Literal["web_panel", "desktop", "other"]
ControllerKind = Literal["agent", "human"]


# --- requests -------------------------------------------------------------


class MintControlRequest(BaseModel):
    """Body of POST /handoffs/{handoff_id}/stream-ticket."""

    model_config = {"extra": "forbid"}
    mode: Literal["control"] = "control"
    client_kind: ClientKind = "web_panel"
    takeover: bool = False


class MintViewRequest(BaseModel):
    """Body of POST /runs/{run_id}/stream-ticket (S4 §2.2)."""

    model_config = {"extra": "forbid"}
    mode: Literal["view"] = "view"
    client_kind: ClientKind = "web_panel"


class ClaimRequest(BaseModel):
    model_config = {"extra": "forbid"}
    ticket: str


class RenewRequest(BaseModel):
    model_config = {"extra": "forbid"}
    control_revision: int | None = None


class ReleaseRequest(BaseModel):
    model_config = {"extra": "forbid"}
    control_revision: int
    reason: str = "returned"


class RevokeRequest(BaseModel):
    model_config = {"extra": "forbid"}
    control_revision: int
    reason: str = "owner_revoked"
    confirm: bool = False


# --- response sub-models --------------------------------------------------


class ControlBlock(BaseModel):
    control_revision: int
    lease_expires_at: int
    renew_interval_seconds: int


class MediaBlock(BaseModel):
    video: bool
    audio: bool
    clipboard: bool
    microphone: bool
    camera: bool
    file_transfer: bool


class IceBlock(BaseModel):
    stun_urls: list[str]
    turn_urls: list[str]
    turn_username: str
    turn_credential: str
    turn_expires_at: int


class ViewportBlock(BaseModel):
    width: int
    height: int
    resize_negotiation: Literal["disabled"] = "disabled"


class MintResponse(BaseModel):
    """S4 §2.1 / §2.2. `endpoint` is DATA — the client never constructs it."""

    ticket: str
    expires_at: int
    endpoint: str
    protocol: Literal["selkies_webrtc"] = "selkies_webrtc"
    stream_session_id: str
    mode: Mode
    control: ControlBlock | None
    media: MediaBlock
    ice: IceBlock
    viewport: ViewportBlock


class RenewResponse(BaseModel):
    lease_expires_at: int
    control_revision: int | None
    grant_revision: int
    next_renew_in_seconds: int


class ControllerInfo(BaseModel):
    kind: ControllerKind
    display_name: str | None = None
