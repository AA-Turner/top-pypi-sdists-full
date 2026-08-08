"""Env service models: /etc/hosts entries and /etc/environment variables.

Replaces the raw ``sed``/``echo >>`` shell in ``setup_agent_env``. The daemon
writes a marker-delimited MANAGED BLOCK in /etc/environment (upsert, not
append), fixing the accumulation-across-warm-pool-reuse bug where every reuse
appended another PLATO_API_KEY line.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class HostsEntry(BaseModel):
    hostname: str
    ip: str


class EnvSetupRequest(BaseModel):
    hosts: list[HostsEntry] = Field(default_factory=list)
    # Upserted into the managed block in /etc/environment.
    env_vars: dict[str, str] = Field(default_factory=dict)


class EnvSetupResponse(BaseModel):
    ok: bool = True
    hosts_written: int = 0
    env_vars_written: int = 0
