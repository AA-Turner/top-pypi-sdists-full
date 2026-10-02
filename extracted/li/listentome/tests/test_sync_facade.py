from __future__ import annotations

import listentome as ltm
from tests.fake_backend import FakeBackend


def test_play(backend: FakeBackend) -> None:
    payload = bytes(range(64)) * 8
    ltm.play(payload, samplerate=48_000, channels=1, dtype="int16", backend=backend)
    assert payload in bytes(backend.streams[0].written)


def test_record(backend: FakeBackend) -> None:
    data = ltm.record(0.01, samplerate=48_000, channels=1, backend=backend)
    assert len(data) == int(0.01 * 48_000) * 4
