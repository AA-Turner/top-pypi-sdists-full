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


def test_model_dump_json_dumps_a_good_model_once_and_never_walks_it(monkeypatch: pytest.MonkeyPatch) -> None:
    """A step output that serializes is dumped ONCE: the bytes scan is for the failure only
    (dump-twice + a per-leaf walk on success was a top event-loop stall, PF-WF 2026-11-02)."""
    from matrx_graph.executor import json_dump

    walked: list[int] = []
    real_walk = json_dump._find_bytes_paths
    monkeypatch.setattr(json_dump, "_find_bytes_paths", lambda obj, path="root": walked.append(1) or real_walk(obj, path))
    calls: list[str] = []
    real_dump = _Payload.model_dump

    def spy(self: _Payload, **kwargs: Any) -> Any:
        calls.append(kwargs.get("mode", "python"))
        return real_dump(self, **kwargs)

    monkeypatch.setattr(_Payload, "model_dump", spy)
    big = _Payload(content={"rows": [{"i": i, "text": "x" * 20} for i in range(20_000)]})
    out = model_dump_json(big, context="test")
    assert out["content"]["rows"][19_999]["i"] == 19_999
    assert calls == ["json"]
    assert walked == []


def test_model_dump_json_names_the_bytes_path_when_it_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_graph.executor import json_dump

    said: list[str] = []
    monkeypatch.setattr(json_dump, "vcprint", lambda text, **_: said.append(str(text)))
    payload = _Payload(content={"parts": [{"signature": b"\xff\xfe"}]})
    with pytest.raises(UnicodeDecodeError):
        model_dump_json(payload, context="named")
    assert any("root.content.parts[0].signature" in line for line in said)
