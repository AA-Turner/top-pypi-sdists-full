"""S11a — _wire_editor_storage: DB path vs legacy path, gating, safeguard."""

import importlib
from unittest.mock import MagicMock

import pytest

import abstra_internals.environment as environment
import abstra_internals.interface.cli.editor as editor


@pytest.fixture(autouse=True)
def _restore_env():
    yield
    importlib.reload(environment)


def _set_db_uri(monkeypatch, value):
    if value is None:
        monkeypatch.delenv("ABSTRA_WEB_EDITOR_DATABASE_URI", raising=False)
    else:
        monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", value)
    importlib.reload(environment)


def test_db_mode_starts_poller_and_skips_legacy_components(monkeypatch):
    _set_db_uri(monkeypatch, "postgresql://u:p@h:5432/db")

    apply_migrations = MagicMock()
    delete_old = MagicMock()
    poller_stop = MagicMock()
    poller_thread = MagicMock()
    start_poller = MagicMock(return_value=(poller_stop, poller_thread))
    monkeypatch.setattr(
        "abstra_internals.services.db.migrations.apply_migrations", apply_migrations
    )
    monkeypatch.setattr(
        "abstra_internals.services.db.cleanup.delete_old_records", delete_old
    )
    monkeypatch.setattr(
        "abstra_internals.services.db.poller.start_poller", start_poller
    )
    heartbeat_cls = MagicMock()
    logs_watcher_cls = MagicMock()
    tasks_watcher_cls = MagicMock()
    broadcast_consumer = MagicMock()
    monkeypatch.setattr(editor, "WebEditorHeartbeat", heartbeat_cls)
    monkeypatch.setattr(editor, "LogsWatcher", logs_watcher_cls)
    monkeypatch.setattr(editor, "TasksWatcher", tasks_watcher_cls)
    monkeypatch.setattr(editor, "start_stdio_broadcast_consumer", broadcast_consumer)

    mc = MagicMock()
    handles = editor._wire_editor_storage(
        mc, is_web_editor=True, use_rabbitmq_workers=True
    )

    apply_migrations.assert_called_once()
    delete_old.assert_called_once()
    start_poller.assert_called_once()
    assert handles.poller_stop_event is poller_stop
    assert handles.poller_thread is poller_thread
    assert handles.heartbeat is None
    assert handles.logs_watcher is None
    assert handles.tasks_watcher is None
    assert handles.stdio_broadcast_stop_event is None
    # Legacy components must NOT run on the DB path (gating §3/§18).
    heartbeat_cls.assert_not_called()
    logs_watcher_cls.assert_not_called()
    tasks_watcher_cls.assert_not_called()
    broadcast_consumer.assert_not_called()
    mc.reset_repositories.assert_not_called()


def test_legacy_web_mode_starts_heartbeat_and_watchers(monkeypatch):
    _set_db_uri(monkeypatch, None)

    hb = MagicMock()
    hb.is_stale.return_value = False
    lw = MagicMock()
    tw = MagicMock()
    start_poller = MagicMock()
    monkeypatch.setattr(editor, "WebEditorHeartbeat", MagicMock(return_value=hb))
    monkeypatch.setattr(editor, "LogsWatcher", MagicMock(return_value=lw))
    monkeypatch.setattr(editor, "TasksWatcher", MagicMock(return_value=tw))
    monkeypatch.setattr(editor, "WORKER_LOG_TO_QUEUE", False)
    monkeypatch.setattr(
        "abstra_internals.services.db.poller.start_poller", start_poller
    )

    mc = MagicMock()
    handles = editor._wire_editor_storage(
        mc, is_web_editor=True, use_rabbitmq_workers=True
    )

    assert handles.heartbeat is hb
    hb.start.assert_called_once()
    assert handles.logs_watcher is lw
    lw.start.assert_called_once()
    assert handles.tasks_watcher is tw
    tw.start.assert_called_once()
    assert handles.poller_stop_event is None
    start_poller.assert_not_called()


def test_fails_fast_when_db_set_without_rabbitmq(monkeypatch):
    _set_db_uri(monkeypatch, "postgresql://u:p@h:5432/db")

    mc = MagicMock()
    # DB set but RabbitMQ absent → must fail fast (not silently fall back to
    # file mode), symmetric with the worker.
    with pytest.raises(RuntimeError) as exc:
        editor._wire_editor_storage(mc, is_web_editor=True, use_rabbitmq_workers=False)
    assert "RABBITMQ_CONNECTION_URI" in str(exc.value)
