"""S11b — editor shutdown wiring: poller stop + pool close on the DB path."""

import threading
from typing import cast
from unittest.mock import MagicMock

import abstra_internals.interface.cli.editor as editor

# A no-op thread factory so shutdown_editor_components doesn't spawn a real thread.
_fake_thread_factory = cast("type[threading.Thread]", MagicMock())


def test_shutdown_stops_poller_and_closes_pool(monkeypatch):
    close_pool = MagicMock()
    monkeypatch.setattr(
        "abstra_internals.services.db.connection.close_pool", close_pool
    )
    poller_stop = MagicMock()

    editor.shutdown_editor_components(
        server=MagicMock(),
        watchers=(),
        editor_consumer=None,
        consumer_controller=None,
        stdio_broadcast_stop_event=None,
        poller_stop_event=poller_stop,
        thread_factory=_fake_thread_factory,
    )

    poller_stop.set.assert_called_once()
    close_pool.assert_called_once()


def test_shutdown_without_poller_does_not_close_pool(monkeypatch):
    close_pool = MagicMock()
    monkeypatch.setattr(
        "abstra_internals.services.db.connection.close_pool", close_pool
    )

    editor.shutdown_editor_components(
        server=MagicMock(),
        watchers=(),
        editor_consumer=None,
        consumer_controller=None,
        stdio_broadcast_stop_event=None,
        poller_stop_event=None,
        thread_factory=_fake_thread_factory,
    )

    close_pool.assert_not_called()
