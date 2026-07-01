"""
cvc.cogs.models — Pydantic schemas for Cogs (compiled cognitive artifacts).

A Cog is a content-addressed executable artifact distilled from an LLM
reasoning trace.  Its ``cog_id`` is the SHA-256 of its envelope (all fields
except mutable telemetry), which makes Cogs mergeable across branches and
shareable across agents / swarms in the same way cognitive commits are.

Design invariants
-----------------
* The envelope (``signature`` + ``body`` + ``test_fixture`` + ``provenance``)
  is immutable.  Mutation produces a *new* Cog that ``supersedes`` the old one.
* ``telemetry`` is the only mutable field and is excluded from ``cog_id``.
* ``body.source`` must be either Python source (``kind="python"``) or a
  JSON-serialisable rule DAG (``kind="rule_dag"``).
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CogBodyKind(StrEnum):
    """Execution backend for a Cog body."""

    PYTHON = "python"
    RULE_DAG = "rule_dag"


class CogSignature(BaseModel):
    """Typed intent + I/O contract used for cache routing."""

    intent_summary: str
    input_schema: dict[str, str] = Field(default_factory=dict)
    output_schema: dict[str, str] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.model_dump(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")


class CogBody(BaseModel):
    """Executable body of a Cog."""

    kind: CogBodyKind = CogBodyKind.PYTHON
    source: str = ""
    entrypoint: str = "run"

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.model_dump(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")


class CogTelemetry(BaseModel):
    """Mutable usage / ROI telemetry. Excluded from cog_id."""

    invocations: int = 0
    successes: int = 0
    failures: int = 0
    shadow_runs: int = 0
    shadow_agreements: int = 0
    promoted: bool = False
    success_rate_ewma: float = 1.0
    tokens_saved_cumulative: int = 0
    last_failure_cause: str = ""
    last_invoked_at: float = 0.0

    def record_success(self, tokens_saved: int, alpha: float = 0.2) -> None:
        self.invocations += 1
        self.successes += 1
        self.tokens_saved_cumulative += max(0, tokens_saved)
        self.last_invoked_at = time.time()
        self.success_rate_ewma = alpha * 1.0 + (1.0 - alpha) * self.success_rate_ewma

    def record_failure(self, cause: str, alpha: float = 0.2) -> None:
        self.invocations += 1
        self.failures += 1
        self.last_failure_cause = cause[:500]
        self.last_invoked_at = time.time()
        self.success_rate_ewma = alpha * 0.0 + (1.0 - alpha) * self.success_rate_ewma

    def record_shadow(self, agreed: bool) -> None:
        self.shadow_runs += 1
        if agreed:
            self.shadow_agreements += 1


def compute_cog_id(
    signature: CogSignature,
    body: CogBody,
    provenance: list[str],
    test_fixture: dict[str, Any],
) -> str:
    """Deterministic SHA-256 of the Cog envelope (telemetry-independent)."""
    h = hashlib.sha256()
    h.update(signature.canonical_bytes())
    h.update(body.canonical_bytes())
    for p in sorted(provenance):
        h.update(p.encode("utf-8"))
    h.update(
        json.dumps(test_fixture, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    )
    return h.hexdigest()


class Cog(BaseModel):
    """A compiled cognitive artifact — the unit of CVC's compiled-cognition store."""

    cog_id: str = ""
    version: int = 1
    signature: CogSignature
    body: CogBody
    test_fixture: dict[str, Any] = Field(default_factory=dict)
    provenance: list[str] = Field(default_factory=list)
    supersedes: str | None = None
    superseded_by: str | None = None
    created_at: float = Field(default_factory=time.time)
    agent_id: str = "sofia"
    originating_tokens: int = 0
    telemetry: CogTelemetry = Field(default_factory=CogTelemetry)
    extra: dict[str, Any] = Field(default_factory=dict)

    def recompute_id(self) -> str:
        self.cog_id = compute_cog_id(self.signature, self.body, self.provenance, self.test_fixture)
        return self.cog_id

    @classmethod
    def build(
        cls,
        *,
        signature: CogSignature,
        body: CogBody,
        provenance: list[str],
        test_fixture: dict[str, Any] | None = None,
        originating_tokens: int = 0,
        agent_id: str = "sofia",
    ) -> "Cog":
        fixture = test_fixture or {}
        cog = cls(
            signature=signature,
            body=body,
            test_fixture=fixture,
            provenance=list(provenance),
            originating_tokens=originating_tokens,
            agent_id=agent_id,
        )
        cog.recompute_id()
        return cog

    @property
    def short_id(self) -> str:
        return self.cog_id[:12] if self.cog_id else ""

    def is_eligible_for_cache(
        self,
        *,
        min_success_rate: float = 0.8,
        require_promoted: bool = True,
    ) -> bool:
        """Return True if this Cog may serve a cache hit."""
        t = self.telemetry
        if require_promoted and not t.promoted:
            return False
        if t.invocations == 0:
            return True
        return t.success_rate_ewma >= min_success_rate


def new_fixture_id() -> str:
    return uuid.uuid4().hex[:16]
