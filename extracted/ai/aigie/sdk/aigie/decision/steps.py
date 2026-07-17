"""Shared vocabulary for RemediationStep dispatch.

These primitives are imported by both the executor and every handler, so they
live in their own module to keep the ``executor -> handlers`` dependency
one-directional (no import cycle).
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol

from google.protobuf import json_format

from aigie.rewind.coordinator import RewindCoordinator


class StepStatus(str, Enum):
    APPLIED = "applied"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass(frozen=True)
class StepContext:
    trace_id: str
    span_id: str
    execution_id: str
    span: Any
    rewind_coordinator: RewindCoordinator | None
    logger: logging.Logger


@dataclass(frozen=True)
class StepOutcome:
    step_id: str
    verb: str
    status: StepStatus
    reason: str = ""
    observed: Mapping[str, Any] | None = None
    latency_ms: int = 0


class StepHandler(Protocol):
    async def invoke(self, step: Any, ctx: StepContext) -> StepOutcome: ...


@dataclass(frozen=True)
class VerbSpec:
    """A verb the SDK can execute, as advertised to the platform."""

    name: str
    description: str
    param_schema: dict[str, Any]


@dataclass(frozen=True)
class VerbBinding:
    """Binds an advertised verb to the handler that executes it. A handler may
    back several verbs (e.g. the prompt handler serves repair_request +
    inject_context), so each verb is one binding."""

    spec: VerbSpec
    handler: StepHandler


def params_to_dict(step: Any) -> dict[str, Any]:
    if not step.HasField("params"):
        return {}
    return json_format.MessageToDict(step.params)  # type: ignore[no-any-return]
