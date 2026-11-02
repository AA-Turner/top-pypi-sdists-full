"""`files.*` may only ever resolve to the ONE database (Matrx Main).

matrx-files once resolved its pool through a fallback ladder
(``FILES_DATABASE_URL`` → ``DATABASE_URL`` → ``MATRX_FILES_POSTGRES_*`` →
``SUPABASE_MATRIX_*``). The identical ladder in matrx-scraper was LIVE in
production and forked 14 rows onto a Coolify-local Postgres the platform never
saw. Here the blast radius is worse: ``files.files`` rows are referenced by
``file_id`` from tables across every repo, so a second files database means
dangling ``file_id``s and unresolvable media.

These tests pin the invariant structurally: the platform prefix is the ONLY
accepted resolution, every retired env var is IGNORED even when set, and a
missing platform env RAISES instead of falling back.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_files.db import __init__ as _files_db_module  # noqa: F401  (import guard)
from matrx_files import db as files_db

RETIRED_ENV_VARS = {
    "FILES_DATABASE_URL": "postgresql://a:b@files-postgres.internal:5434/files_db",
    "DATABASE_URL": "postgresql://a:b@files-postgres.internal:5434/files_db",
    "MATRX_FILES_POSTGRES_HOST": "files-postgres.internal",
    "MATRX_FILES_POSTGRES_PORT": "5434",
    "MATRX_FILES_POSTGRES_NAME": "files_db",
    "MATRX_FILES_POSTGRES_USER": "postgres",
    "MATRX_FILES_POSTGRES_PASSWORD": "secret",
}


def _capture_register_from_env(
    monkeypatch: pytest.MonkeyPatch, *, ok: bool = True
) -> list[dict[str, Any]]:
    """Stub matrx-orm registration; return the list of captured kwargs."""
    captured: list[dict[str, Any]] = []

    def fake_register_from_env(**kwargs: Any) -> bool:
        captured.append(kwargs)
        return ok

    monkeypatch.setattr("matrx_orm.is_database_registered", lambda name: False)
    monkeypatch.setattr("matrx_orm.register_database_from_env", fake_register_from_env)
    monkeypatch.setattr(
        "matrx_orm.register_database",
        lambda config: pytest.fail(
            "matrx-files must never register a pool from a raw connection URL — "
            "`files.*` binds to the ONE database via SUPABASE_MATRIX_*"
        ),
    )
    monkeypatch.setattr(files_db, "_register_models", lambda: None)
    return captured


def _set_platform_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPABASE_MATRIX_HOST", "aws-0-us-west-1.pooler.supabase.com")
    monkeypatch.setenv("SUPABASE_MATRIX_PORT", "6543")
    monkeypatch.setenv("SUPABASE_MATRIX_DATABASE_NAME", "postgres")
    monkeypatch.setenv("SUPABASE_MATRIX_USER", "postgres.exampleprojectref00")
    monkeypatch.setenv("SUPABASE_MATRIX_PASSWORD", "pw")


def test_bootstrap_binds_files_schema_to_the_one_platform_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`files.*` resolves from SUPABASE_MATRIX_* — the same ONE database as everything else."""
    captured = _capture_register_from_env(monkeypatch)

    assert files_db.bootstrap_db() == files_db.PACKAGE_DB_NAME

    assert len(captured) == 1
    kwargs = captured[0]
    assert kwargs["name"] == files_db.PACKAGE_DB_NAME
    assert kwargs["env_prefix"] == "SUPABASE_MATRIX"
    assert kwargs["env_var_overrides"] == {"NAME": "SUPABASE_MATRIX_DATABASE_NAME"}
    assert kwargs["additional_schemas"] == ["files", "iam", "auth", "platform"]
    # TLS is a DEPLOYMENT input (SUPABASE_MATRIX_SSL), never hardcoded here —
    # hardcoding "require" is what makes a local or client-owned Postgres
    # unreachable, i.e. it breaks the package's independence.
    assert kwargs["ssl"] is None


def test_bootstrap_ignores_every_retired_second_database_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A service-local Postgres URL must NOT be able to fork `files.*`."""
    for key, value in RETIRED_ENV_VARS.items():
        monkeypatch.setenv(key, value)
    captured = _capture_register_from_env(monkeypatch)

    files_db.bootstrap_db()

    # register_database (the URL path) is a hard fail in the stub above; the only
    # accepted resolution is the platform env prefix.
    assert [k["env_prefix"] for k in captured] == ["SUPABASE_MATRIX"]


def test_connection_url_ignores_every_retired_second_database_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key, value in RETIRED_ENV_VARS.items():
        monkeypatch.setenv(key, value)
    _set_platform_env(monkeypatch)

    url = files_db.connection_url()

    assert "aws-0-us-west-1.pooler.supabase.com:6543" in url
    assert "files-postgres.internal" not in url
    assert "files_db" not in url


def test_connection_url_raises_when_the_one_database_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No fallback, no 'optional' — an unresolvable platform DB is fatal."""
    for key, value in RETIRED_ENV_VARS.items():
        monkeypatch.setenv(key, value)
    for key in ("SUPABASE_MATRIX_HOST", "SUPABASE_MATRIX_USER", "SUPABASE_MATRIX_PASSWORD"):
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(RuntimeError, match="SUPABASE_MATRIX"):
        files_db.connection_url()


def test_bootstrap_raises_when_the_one_database_cannot_be_resolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _capture_register_from_env(monkeypatch, ok=False)

    with pytest.raises(files_db.FilesDBNotConfiguredError, match="SUPABASE_MATRIX"):
        files_db.bootstrap_db()


def test_no_files_specific_connection_env_var_survives_in_source() -> None:
    """Structural pin: the ladder cannot come back by editing one branch."""
    from pathlib import Path

    package_root = Path(files_db.__file__).parents[1]
    for path in package_root.rglob("*.py"):
        source = path.read_text()
        assert "FILES_DATABASE_URL" not in source, path
        assert "MATRX_FILES_POSTGRES" not in source, path


def test_standalone_app_has_no_alternate_database_branch() -> None:
    """The standalone boot path calls the ONE resolver, unparameterized."""
    from pathlib import Path

    from matrx_files.standalone import app as standalone_app

    source = Path(standalone_app.__file__).read_text()
    assert "bootstrap_db()" in source
    assert "env_prefix=" not in source


def test_package_default_cors_ships_no_matrx_domain() -> None:
    """The shipped CORS default is loopback ONLY — never our production domains.

    Shipping `aimatrx.com` / `aidream.ai` / `matrxserver.com` / `*.vercel.app` as
    the DEFAULT made the package carry AI Dream's identity — the "package
    hardwired to us" failure in
    common-docs/policies/package-vs-implementation.md. A deployment names its own
    browser origins via MATRX_FILES_CORS_ALLOWED_ORIGINS (exact list) or
    MATRX_FILES_CORS_ALLOWED_ORIGIN_REGEX (patterns); our production host does.
    """
    from matrx_files.standalone.app import _DEFAULT_CORS_ORIGIN_REGEX

    for domain in ("aimatrx", "aidream", "matrxserver", "vercel"):
        assert domain not in _DEFAULT_CORS_ORIGIN_REGEX, (
            f"package CORS default ships an AI Dream domain ({domain}); a "
            "deployment names its own origins via the env vars"
        )
    # ...and still works out of the box for a developer on loopback.
    import re

    pattern = re.compile(_DEFAULT_CORS_ORIGIN_REGEX)
    assert pattern.match("http://localhost:3000")
    assert pattern.match("http://127.0.0.1:8000")
    assert not pattern.match("https://www.aimatrx.com")
    assert not pattern.match("https://evil.example.com")
