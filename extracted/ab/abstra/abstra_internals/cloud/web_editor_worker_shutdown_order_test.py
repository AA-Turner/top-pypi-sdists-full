"""Worker SIGTERM ordering (DB path): the consumers must be stopped BEFORE the
logs repo and the pool are closed, so an in-flight handler can't check out from a
closing pool (and silently recreate it)."""

from unittest.mock import MagicMock

import pytest

import abstra_internals.cloud.web_editor_worker as worker
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations


@pytest.fixture
def wired(monkeypatch):
    """Patch run()'s surface; record sigterm callbacks in registration order."""
    registered = []
    signal_handlers = MagicMock(name="SignalHandlers")
    signal_handlers.register_sigterm_callback.side_effect = registered.append

    monkeypatch.setattr(connection, "configure_pool", MagicMock(name="configure_pool"))
    monkeypatch.setattr(connection, "close_pool", MagicMock(name="close_pool"))
    monkeypatch.setattr(migrations, "apply_migrations", MagicMock(name="migrate"))

    repos = MagicMock(name="repos")
    wec = MagicMock(name="WEC")
    wecc = MagicMock(name="WECC")
    monkeypatch.setattr(worker, "build_web_editor_repositories", lambda *a, **k: repos)
    monkeypatch.setattr(worker, "MainController", MagicMock())
    monkeypatch.setattr(worker, "WebEditorConsumer", wec)
    monkeypatch.setattr(worker, "WebEditorControlConsumer", wecc)
    monkeypatch.setattr(worker, "ConsumerController", MagicMock())
    monkeypatch.setattr(worker, "SignalHandlers", signal_handlers)
    monkeypatch.setattr(worker, "DEFAULT_PORT", 8080)
    monkeypatch.setattr(worker, "RABBITMQ_CONNECTION_URI", "amqp://guest@localhost/")

    # `with WebEditorConsumer(uri) as consumer:` → ctor().__enter__() return value.
    consumer = wec.return_value.__enter__.return_value
    control = wecc.return_value.__enter__.return_value
    return registered, repos, consumer, control


def test_consumers_stop_before_pool_and_logs_close(monkeypatch, wired):
    registered, repos, consumer, control = wired
    monkeypatch.setattr(worker, "web_editor_uses_db", lambda: True)

    worker.run()

    close_pool = connection.close_pool
    logs_close = repos.execution_logs.close

    for cb in (consumer.stop_iter, control.stop_iter, close_pool, logs_close):
        assert cb in registered, f"{cb} was not registered"

    assert registered.index(consumer.stop_iter) < registered.index(close_pool)
    assert registered.index(control.stop_iter) < registered.index(close_pool)
    assert registered.index(consumer.stop_iter) < registered.index(logs_close)
    assert registered.index(logs_close) < registered.index(close_pool)


def test_no_db_path_registers_only_consumer_stops(monkeypatch, wired):
    registered, repos, consumer, control = wired
    monkeypatch.setattr(worker, "web_editor_uses_db", lambda: False)

    worker.run()

    assert consumer.stop_iter in registered
    assert control.stop_iter in registered
    assert connection.close_pool not in registered
