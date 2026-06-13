"""Shared fixtures for all tests."""

from __future__ import annotations

import pytest

import smplkit._metrics as _metrics_module
from smplkit._ws import SharedWebSocket


class _NoOpMetricsReporter:
    """Drop-in replacement for _MetricsReporter that never touches the network."""

    def __init__(self, **_kwargs) -> None:  # noqa: ANN003
        pass

    def record(self, *_args, **_kwargs) -> None:  # noqa: ANN002, ANN003
        pass

    def record_gauge(self, *_args, **_kwargs) -> None:  # noqa: ANN002, ANN003
        pass

    def flush(self) -> None:
        pass

    def close(self) -> None:
        pass


class _NoOpAsyncMetricsReporter(_NoOpMetricsReporter):
    """Drop-in replacement for _AsyncMetricsReporter that never touches the network."""

    async def flush(self) -> None:  # type: ignore[override]
        pass

    async def close(self) -> None:  # type: ignore[override]
        pass


@pytest.fixture(autouse=True)
def _disable_telemetry_in_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent any SmplClient instantiation from firing real metrics HTTP calls.

    Unit tests must never hit the network.  The metrics reporters start a
    60-second daemon timer on construction; if tests don't call close() the
    timer fires against the live app service with fake API keys → 401s in
    production CloudWatch logs.

    This fixture patches the two reporter classes at the module level so
    that SmplClient / AsyncSmplClient constructors receive no-ops instead.
    Tests in test_metrics.py that import the real classes directly are
    unaffected because they reference the original objects, not the patched
    module attribute.
    """
    monkeypatch.setattr(_metrics_module, "_MetricsReporter", _NoOpMetricsReporter)
    monkeypatch.setattr(_metrics_module, "_AsyncMetricsReporter", _NoOpAsyncMetricsReporter)


@pytest.fixture(autouse=True)
def _no_real_websocket(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stop unit tests from opening a real WebSocket to the app service.

    Any client that reaches its live surface (``config.subscribe``,
    ``flag.on_change``, ``wait_until_ready``, …) lazily constructs a
    :class:`SharedWebSocket` and calls ``.start()``, which spawns a daemon
    thread that dials ``wss://app.smplkit.com/api/ws/v1/events``. With the
    fake API keys unit tests use, the dial is rejected by CloudFront with an
    HTTP 403 and the background reconnect loop logs warnings on a backoff
    schedule — forever, since the thread is a daemon that outlives the test
    that spawned it. Those stray ``smplkit.ws`` warnings leak across tests
    and once flaked a ``caplog`` assertion in the logging suite.

    Patching ``start`` to a no-op keeps the ``SharedWebSocket`` object (so
    listener registration and ``connection_status`` still behave) while never
    spawning the dialing thread. The real ``start`` / ``_connect`` /
    ``_reconnect`` machinery is exercised directly — with the network mocked
    — in ``test_shared_ws.py``, which overrides this fixture with a no-op so
    it keeps the genuine method.
    """
    monkeypatch.setattr(SharedWebSocket, "start", lambda self: None)


@pytest.fixture(autouse=True)
def _set_smplkit_service(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure SMPLKIT_SERVICE is set for every test.

    ``service`` is now required by SmplClient / AsyncSmplClient.  This
    autouse fixture keeps existing tests green without individual changes.
    Tests that need to exercise the service-missing error path should
    explicitly ``monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)``.
    """
    monkeypatch.setenv("SMPLKIT_SERVICE", "test-service")
