"""S10 — worker boot: migrates once before building repos (DB path); legacy intact."""

from unittest.mock import MagicMock

import pytest

import abstra_internals.cloud.web_editor_worker as worker
import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations


@pytest.fixture
def patched(monkeypatch):
    """Patch the full surface so run() returns without RabbitMQ / blocking loop,
    and attach the ordering-relevant mocks to a single parent for call ordering."""
    parent = MagicMock()

    apply_migrations = MagicMock(name="apply_migrations")
    build_repos = MagicMock(name="build_web_editor_repositories")
    close_pool = MagicMock(name="close_pool")
    signal_handlers = MagicMock(name="SignalHandlers")

    monkeypatch.setattr(migrations, "apply_migrations", apply_migrations)
    monkeypatch.setattr(connection, "close_pool", close_pool)
    monkeypatch.setattr(worker, "build_web_editor_repositories", build_repos)
    monkeypatch.setattr(worker, "MainController", MagicMock())
    monkeypatch.setattr(worker, "WebEditorConsumer", MagicMock())
    monkeypatch.setattr(worker, "WebEditorControlConsumer", MagicMock())
    monkeypatch.setattr(worker, "ConsumerController", MagicMock())
    monkeypatch.setattr(worker, "SignalHandlers", signal_handlers)
    monkeypatch.setattr(worker, "DEFAULT_PORT", 8080)
    monkeypatch.setattr(worker, "RABBITMQ_CONNECTION_URI", "amqp://guest@localhost/")

    parent.attach_mock(apply_migrations, "apply_migrations")
    parent.attach_mock(build_repos, "build_repos")
    parent.attach_mock(close_pool, "close_pool")
    parent.attach_mock(signal_handlers, "signal_handlers")
    return parent, monkeypatch


def test_db_path_migrates_before_building_repos(patched):
    parent, monkeypatch = patched
    monkeypatch.setattr(worker, "web_editor_uses_db", lambda: True)

    worker.run()

    names = [c[0] for c in parent.mock_calls]
    assert "apply_migrations" in names
    assert "build_repos" in names
    assert names.index("apply_migrations") < names.index("build_repos")
    # close_pool wired as a sigterm callback
    parent.signal_handlers.register_sigterm_callback.assert_any_call(parent.close_pool)


def test_no_db_path_does_not_migrate_or_close_pool(patched):
    parent, monkeypatch = patched
    monkeypatch.setattr(worker, "web_editor_uses_db", lambda: False)

    worker.run()

    parent.apply_migrations.assert_not_called()
    parent.close_pool.assert_not_called()
    parent.build_repos.assert_called_once()
