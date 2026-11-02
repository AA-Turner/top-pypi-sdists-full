from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.executor.json_dump import model_dump_json
from pydantic import BaseModel


class _Payload(BaseModel):
    content: Any


def test_model_dump_json_still_raises_after_scanning_any_bytes() -> None:
    payload = _Payload(content={"signature": b"\x00\xe3\x81\xff\xfe"})
    with pytest.raises(UnicodeDecodeError):
        model_dump_json(payload, context="test")
