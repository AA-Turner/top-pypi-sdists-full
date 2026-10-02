from __future__ import annotations

from ._backend import Backend
from ._devices import Device


def _resolve(backend: Backend | None) -> Backend:
    if backend is None:  # pragma: no cover - requires the real PortAudio library and audio hardware
        from ._portaudio import default_backend

        return default_backend()
    return backend


def devices(*, backend: Backend | None = None) -> list[Device]:
    return _resolve(backend).devices()


def default_input(*, backend: Backend | None = None) -> Device | None:
    return _resolve(backend).default_input()


def default_output(*, backend: Backend | None = None) -> Device | None:
    return _resolve(backend).default_output()
