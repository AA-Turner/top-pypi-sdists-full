"""Pool service models: warm-VM reset and reclaim lifecycle."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PoolResetRequest(BaseModel):
    workspace_paths: list[str] = Field(default_factory=list)


class PoolResetStep(BaseModel):
    name: str
    ok: bool
    detail: str = ""


class PoolResetResult(BaseModel):
    # Overall ok stays True even when individual steps fail — reset is
    # best-effort per step (parity with the SSH chain's `(cmd) || true`), so a
    # single failing step never causes the pool to needlessly destroy a VM.
    ok: bool = True
    steps: list[PoolResetStep] = Field(default_factory=list)


class PoolReclaimResponse(BaseModel):
    ok: bool = True
    reclaimed: bool = True
