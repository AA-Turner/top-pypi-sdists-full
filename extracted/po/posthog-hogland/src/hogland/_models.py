"""hogland public types.

This module is the public type surface for the SDK. It does two things:

1. Re-exports the codegen'd Pydantic v2 models from
   :mod:`hogland._generated.models`, which are produced from
   ``internal/clitest/testdata/openapi.yaml`` via
   ``task py:gen-models``. The drift gate
   (``tests/test_spec_drift.py``) fails if the generated file is out of
   date.

2. Holds the small set of types that ``datamodel-code-generator``
   cannot emit — currently only :class:`ExecEvent`, the SSE frame for
   ``POST /v1/hogboxes/{id}/exec/stream``. That endpoint isn't
   registered with Huma so it doesn't appear in ``openapi.yaml``; see
   ``docs/PYTHON_SDK_CODEGEN_RESEARCH.md`` §4.

Friendly aliases (``ExecResult``, ``Limits``, ``Me``) live alongside
the generator-driven names. Both are exported — readers grepping the
spec find the codegen name; readers wanting Pythonic prose use the
alias.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict

# The codegen module is the source of truth for the wire shape; this
# module re-exports a *curated* slice with friendly names that read more
# naturally in user code. The raw ``*Response`` / ``*Request`` codegen
# names are deliberately NOT re-exported from the package root — callers
# wanting verbatim spec types import from ``hogland._generated.models``.
# Otherwise every type would have two names on the public surface (e.g.
# ``Me`` AND ``MeResponse``) which forces a needless naming choice on
# every call site.
from ._generated.models import (
    AccessType,
    BoxSpec,
    BoxView,
    CreateBoxRequest,
    ErrorDetail,
    ErrorModel,
    FileWriteResponse,
    HogboxList,
    NumericLimit,
    Pen,
    PenList,
    SnapshotRecord,
)
from ._generated.models import (
    ExecBoxResponse as _ExecBoxResponse,
)
from ._generated.models import (
    LimitsResponse as _LimitsResponse,
)
from ._generated.models import (
    MeResponse as _MeResponse,
)


# The openapi spec models `disk_class` as a single-value enum, which
# datamodel-codegen inlines as `Literal["mirrored"]` rather than emitting
# a named class. We still want callers to write `DiskClass.MIRRORED` for
# discoverability and to avoid magic strings, so define the enum here.
# Track the spec: if a second value lands, add it here too — the drift
# gate will fail the FE/Go SDKs first, this is a manual mirror.
class DiskClass(StrEnum):
    """Storage backend for the per-VM rootfs (matches ``BoxSpec.disk_class``)."""

    MIRRORED = "mirrored"


ExecResult = _ExecBoxResponse
"""Result of a batch ``Hogbox.exec`` call — captured stdout/stderr/exit_code."""

Limits = _LimitsResponse
"""Server-advertised valid ranges for box sizing (cpus, memory, disk)."""

Me = _MeResponse
"""Caller's identity, as the server sees it (id, email, kind, is_admin)."""


class ExecEvent(BaseModel):
    """One frame from the streaming-exec SSE endpoint.

    The server emits three event kinds:

    * ``stdout`` / ``stderr`` — ``data`` carries a UTF-8 string chunk.
    * ``exit``                — ``exit_code`` and ``duration_ms`` are set.

    Not in ``openapi.yaml``; hand-written and stable.
    """

    model_config = ConfigDict(extra="ignore")

    kind: Literal["stdout", "stderr", "exit"]
    data: str = ""
    exit_code: int | None = None
    duration_ms: int | None = None


__all__ = [
    "AccessType",
    "BoxSpec",
    "BoxView",
    "CreateBoxRequest",
    "DiskClass",
    "ErrorDetail",
    "ErrorModel",
    "ExecEvent",
    "ExecResult",
    "FileWriteResponse",
    "HogboxList",
    "Limits",
    "Me",
    "NumericLimit",
    "Pen",
    "PenList",
    "SnapshotRecord",
]
