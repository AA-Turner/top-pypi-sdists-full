"""S9 — factory branching by WEB_EDITOR_DATABASE_URI (tabela-verdade §12, D1/D8/D11).

No Docker: repos are constructed but never connect. The log-flush daemon of the
Pg logs repo only touches the DB when its buffer is non-empty (it stays empty
here), so no connection is opened.
"""

import importlib
from unittest.mock import patch

import pytest

import abstra_internals.environment as environment
import abstra_internals.repositories.factory as factory
from abstra_internals.repositories.execution import (
    PgWebEditorExecutionRepository,
    WebEditorExecutionRepository,
)
from abstra_internals.repositories.execution_logs import (
    LocalExecutionLogsRepository,
    PgWebEditorExecutionLogsRepository,
)
from abstra_internals.repositories.tasks import (
    LocalTasksRepository,
    PgWebEditorTasksRepository,
)
from abstra_internals.settings import SettingsController

RABBIT = "amqp://guest:rabbitsecret@localhost/"


@pytest.fixture(autouse=True)
def _root_path(tmp_path):
    # The file-based repos build SqlStorage under Settings.root_path.
    SettingsController.set_root_path(str(tmp_path))
    yield


def _build(monkeypatch, db_uri):
    if db_uri is None:
        monkeypatch.delenv("ABSTRA_WEB_EDITOR_DATABASE_URI", raising=False)
    else:
        monkeypatch.setenv("ABSTRA_WEB_EDITOR_DATABASE_URI", db_uri)
    importlib.reload(environment)
    return factory.build_web_editor_repositories(RABBIT)


def _cleanup(monkeypatch, repos):
    logs_repo = getattr(repos, "execution_logs", None)
    if isinstance(logs_repo, PgWebEditorExecutionLogsRepository):
        logs_repo._stop.set()
    monkeypatch.undo()
    importlib.reload(environment)


def test_db_env_builds_pg_repos_and_does_not_migrate(monkeypatch):
    with patch(
        "abstra_internals.services.db.migrations.apply_migrations"
    ) as apply_migrations:
        repos = _build(monkeypatch, "postgresql://u:p@h:5432/db")
    try:
        assert isinstance(repos.tasks, PgWebEditorTasksRepository)
        assert isinstance(repos.execution, PgWebEditorExecutionRepository)
        assert isinstance(repos.execution_logs, PgWebEditorExecutionLogsRepository)
        # D11: the factory must NEVER migrate (it also runs in executor warmup).
        apply_migrations.assert_not_called()
    finally:
        _cleanup(monkeypatch, repos)


def test_no_db_env_builds_file_repos(monkeypatch):
    repos = _build(monkeypatch, None)
    try:
        assert isinstance(repos.tasks, LocalTasksRepository)
        assert isinstance(repos.execution, WebEditorExecutionRepository)
        assert isinstance(repos.execution_logs, LocalExecutionLogsRepository)
    finally:
        _cleanup(monkeypatch, repos)


def test_shared_repos_identical_across_paths(monkeypatch):
    db_repos = None
    file_repos = None
    try:
        db_repos = _build(monkeypatch, "postgresql://u:p@h:5432/db")
        # producer/project/kv etc. are the same classes regardless of backend
        assert type(db_repos.producer).__name__ == "WebEditorProducerRepository"
        if isinstance(db_repos.execution_logs, PgWebEditorExecutionLogsRepository):
            db_repos.execution_logs._stop.set()
        monkeypatch.undo()
        file_repos = _build(monkeypatch, None)
        assert type(file_repos.producer) is type(db_repos.producer)
        assert type(file_repos.kv) is type(db_repos.kv)
        assert type(file_repos.project) is type(db_repos.project)
    finally:
        monkeypatch.undo()
        importlib.reload(environment)


def test_no_db_password_logged(monkeypatch):
    captured = []
    monkeypatch.setattr(
        "abstra_internals.logger.AbstraLogger.info",
        lambda message, *a, **k: captured.append(message),
    )
    repos = _build(monkeypatch, "postgresql://user:DBSECRET@h:5432/db")
    try:
        joined = " ".join(captured)
        assert "DBSECRET" not in joined
        assert "SET" in joined  # logs presence, not the value
    finally:
        _cleanup(monkeypatch, repos)
