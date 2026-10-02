from __future__ import annotations

import pytest

import listentome as ltm
from listentome._portaudio import default_backend

pytestmark = pytest.mark.hardware


def test_devices_enumerate() -> None:
    devices = ltm.devices(backend=default_backend())
    assert devices
    assert all(d.default_samplerate > 0 for d in devices)


def test_record_from_real_device() -> None:
    data = ltm.record(0.1, samplerate=48_000, channels=1, backend=default_backend())
    assert len(data) == int(0.1 * 48_000) * 4


def test_play_on_real_device() -> None:
    ltm.play(bytes(48_000 * 4 // 10), samplerate=48_000, channels=1, backend=default_backend())
