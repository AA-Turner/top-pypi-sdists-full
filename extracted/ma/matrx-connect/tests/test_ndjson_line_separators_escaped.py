"""One NDJSON event is exactly one line, even for Unicode-aware splitters.

Records carry raw U+2028 / U+2029 inside strings. ``orjson`` emits them raw, and
``str.splitlines()`` (plus some JS readers) treats them as line breaks, tearing
one event into two broken JSON lines. The shared emitter must escape them.
"""

from __future__ import annotations

import json

import pytest

from matrx_connect.emitters.stream_emitter import StreamEmitter

LS = " "
PS = " "


@pytest.mark.asyncio
async def test_record_with_line_and_paragraph_separators_is_one_line_per_event() -> None:
    emitter = StreamEmitter(heartbeat_interval=3600)
    text = f"a{LS}b{PS}c"
    await emitter.send_chunk(text)
    await emitter.send_data({"record": {"bio": f"x{LS}y{PS}z", "n": 1}})
    await emitter.send_reasoning_chunk(f"r{LS}{PS}")

    lines: list[str] = []
    gen = emitter.generate()
    for _ in range(3):
        item = await anext(gen)
        lines.append(item.decode() if isinstance(item, bytes) else item)
    await gen.aclose()

    blob = "".join(lines)
    assert LS not in blob and PS not in blob, "raw separators leaked onto the wire"
    assert len(blob.splitlines()) == 3
    parsed = [json.loads(line) for line in blob.splitlines()]
    assert parsed[0]["t"] == text
    assert parsed[2]["t"] == f"r{LS}{PS}"
    assert json.dumps(parsed[1]).count("\\u2028") >= 1
