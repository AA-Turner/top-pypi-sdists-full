"""Offline guard for the ai_providers/copilot unit tests.

All tests in this package use injected fakes (FakeTransport, FakeDiscovery).
The fixture below raises immediately if any test accidentally wires a real
socket connection, a live ``requests`` session, or the real
``RequestsHttpTransport`` so that offline validation always fails before any
external side effect reaches the network.
"""

import socket

import pytest
import requests


@pytest.fixture(autouse=True)
def _offline_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    def _no_network(*args: object, **kwargs: object) -> None:
        raise RuntimeError(
            "Network access is forbidden in ai_providers/copilot unit tests. "
            "Inject a FakeTransport instead of using a live connection."
        )

    monkeypatch.setattr(socket.socket, "connect", _no_network)
    monkeypatch.setattr(requests.Session, "send", _no_network)
