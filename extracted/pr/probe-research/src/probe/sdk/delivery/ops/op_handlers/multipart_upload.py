"""MultipartUploadHandler (OpHandler): one deadline-bounded slice of work on a queued multipart_upload op."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from .....foundation.durable.durable import write_text_atomic
#: Wall clock one drain visit may spend sending parts before it saves and yields, so the
#: rest of the queue is never more than this far behind.
SLICE_SECONDS = 20.0


def execute_op(journal: Any, client: Any, op_path: Path, op: dict) -> dict | None:
    """The drain's hook (`journal._execute`): one slice of work. An op a closing
    `finish()` is seeing through (``until: verifying``) is done once the server has every byte."""

    def save() -> None:
        write_text_atomic(op_path, json.dumps(op, indent=2) + "\n", mode=0o600)

    until = (op.get("multipart") or {}).get("until")
    return advance(
        client,
        op,
        save,
        deadline=time.monotonic() + SLICE_SECONDS,
        wait_for_verify=until != "verifying",
        hash_inline=False,
    )
from probe.sdk.artifact.storage_handlers.multipart.multipart import advance  # noqa: E402 -- pieces need each other; the front door loads this one first
