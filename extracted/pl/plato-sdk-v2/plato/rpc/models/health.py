"""Health service models: handshake, ping, diagnostics report."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from plato.rpc.models.common import Limits


class HandshakeResponse(BaseModel):
    """Response of GET /v1/handshake — the compatibility anchor.

    Feature gating is on ``capabilities`` strings, never on version
    comparison. ``protocol_version`` is the max /vN the daemon serves.
    """

    protocol_version: int
    server_sdk_version: str
    capabilities: list[str]
    limits: Limits = Field(default_factory=Limits)
    daemon_started_at: datetime
    state_dir: str


class PingResponse(BaseModel):
    ok: bool = True
    ts: datetime


class HealthReport(BaseModel):
    """Typed VM diagnostics — replaces diagnose_agent_vm's log-only SSH probes
    for the daemon-reachable case. Every field is best-effort."""

    ts: datetime
    uptime_s: float | None = None
    load_1m: float | None = None
    mem_total_kb: int | None = None
    mem_available_kb: int | None = None
    disk_free_bytes: int | None = None
    running_jobs: list[str] = Field(default_factory=list)
    dmesg_errors_tail: list[str] = Field(default_factory=list)
    agent_processes: list[str] = Field(default_factory=list)
