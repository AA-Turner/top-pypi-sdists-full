"""hogland — Python client for hogland's Firecracker-backed sandboxes.

Quickstart:

.. code-block:: python

    from hogland import Hogland

    client = Hogland()  # reads HOG_TOKEN + HOG_HOST from env
    with client.create(cpus=4, memory_mib=8192, disk_gib=50) as box:
        box.write_file("/work/run.py", b"print('hi')\\n")
        result = box.exec(["python", "/work/run.py"])
        print(result.stdout)

        for event in box.exec_stream(
            ["bash", "-c", "for i in 1 2 3; do echo $i; sleep 1; done"]
        ):
            if event.kind == "stdout":
                print(event.data, end="")

        snap = box.snapshot()
        # snap.id can be passed back as snapshot_id on the next create.

See ``docs/PYTHON_SDK_CODEGEN_RESEARCH.md`` for the design rationale
and ``python/examples/`` for migration recipes.
"""

from __future__ import annotations

from ._async import AsyncHogland
from ._box import AsyncHogbox, Hogbox
from ._client import Hogland
from ._errors import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    ConflictError,
    HoglandError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from ._models import (
    AccessType,
    BoxSpec,
    BoxView,
    CreateBoxRequest,
    DiskClass,
    ErrorDetail,
    ErrorModel,
    ExecEvent,
    ExecResult,
    FileWriteResponse,
    HogboxList,
    Limits,
    Me,
    NumericLimit,
    Pen,
    PenList,
    SnapshotRecord,
)
from ._sse import AsyncStreamResult, StreamResult
from ._version import __version__

# The codegen'd `*Response` / `*Request` model names (ExecBoxResponse,
# MeResponse, LimitsResponse, ExecBoxRequest) live in ``hogland._generated``
# for power users who want to map back to the OpenAPI spec verbatim. The
# public surface intentionally keeps only the friendly aliases so callers
# don't have to choose between two names for the same shape.
__all__ = [
    "APIError",
    "AccessType",
    "AsyncHogbox",
    "AsyncHogland",
    "AsyncStreamResult",
    "AuthenticationError",
    "BoxSpec",
    "BoxView",
    "ConfigurationError",
    "ConflictError",
    "CreateBoxRequest",
    "DiskClass",
    "ErrorDetail",
    "ErrorModel",
    "ExecEvent",
    "ExecResult",
    "FileWriteResponse",
    "Hogbox",
    "HogboxList",
    "Hogland",
    "HoglandError",
    "Limits",
    "Me",
    "NotFoundError",
    "NumericLimit",
    "Pen",
    "PenList",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "SnapshotRecord",
    "StreamResult",
    "ValidationError",
    "__version__",
]
