"""Current discovery membership stays separate from historical model evidence."""
import os
from pathlib import Path
import uuid

import pytest
import psycopg
from psycopg import sql

from hugpy_core.models.current_catalog import replace, refresh_local


@pytest.fixture
def conn():
    dsn = os.environ.get("HUGPY_TEST_CATALOG_DSN")
    if not dsn:
        pytest.skip("HUGPY_TEST_CATALOG_DSN is required for isolated PostgreSQL checks")
    with psycopg.connect(dsn) as connection:
        namespace = "catalog_test_" + uuid.uuid4().hex
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(namespace)))
        connection.execute(sql.SQL("SET LOCAL search_path TO {}").format(sql.Identifier(namespace)))
        connection.execute("CREATE TABLE model_census (model_key text PRIMARY KEY, hub_id text, "
                           "framework text, primary_task text, metadata jsonb NOT NULL DEFAULT '{}', "
                           "updated_at timestamptz NOT NULL DEFAULT now())")
        connection.execute("CREATE TABLE model_key_aliases (alias_key text PRIMARY KEY,model_key text)")
        connection.execute("CREATE VIEW model_dossier_raw_keys AS SELECT model_key FROM model_census")
        migration = Path(__file__).parents[1] / "src/hugpy_core/schema/sql/053_current_model_catalog.sql"
        connection.execute(migration.read_text())
        yield connection
        connection.rollback()


def keys(conn):
    return {r[0] for r in conn.execute("SELECT model_key FROM model_dossier_keys")}


def test_first_snapshot_replaces_historical_catalog_without_deleting_evidence(conn):
    conn.execute("INSERT INTO model_census(model_key) VALUES ('/old/model.gguf')")
    assert keys(conn) == {"/old/model.gguf"}
    replace(conn, "discovery:local", [{"key": "current", "primary_task": "text-generation"}])
    assert keys(conn) == {"current"}
    assert conn.execute("SELECT count(*) FROM model_census").fetchone()[0] == 2
    assert conn.execute("SELECT metadata->'tasks' FROM model_census WHERE model_key='current'").fetchone()[0] == ["text-generation"]


def test_complete_snapshots_remove_absent_models_and_accept_empty_catalog(conn):
    replace(conn, "discovery:local", [{"key": "first"}, {"key": "second"}])
    replace(conn, "discovery:local", [{"key": "second"}])
    assert keys(conn) == {"second"}
    replace(conn, "discovery:local", [])
    assert keys(conn) == set()
    assert conn.execute("SELECT count(*) FROM model_census").fetchone()[0] == 2


def test_sources_are_independent_and_removed_models_remain_on_other_sources(conn):
    replace(conn, "worker:one", [{"id": "shared"}])
    replace(conn, "worker:two", [{"id": "shared"}, {"id": "other"}])
    replace(conn, "worker:one", [])
    assert keys(conn) == {"shared", "other"}


def test_refresh_updates_capabilities_preserves_policy_and_skips_unchanged(conn):
    replace(conn, "worker:one", [{"id": "model", "primary_task": "text-generation"}])
    conn.execute("UPDATE model_census SET metadata=metadata || '{\"serveable\":false}'::jsonb")
    row = {"id": "model", "primary_task": "image-text-to-text"}
    assert replace(conn, "worker:one", [row])
    metadata = conn.execute("SELECT metadata FROM model_census").fetchone()[0]
    assert metadata["serveable"] is False
    assert metadata["tasks"] == ["image-text-to-text"]
    assert replace(conn, "worker:one", [row]) is False


def test_invalid_snapshot_keeps_previous_membership(conn):
    replace(conn, "worker:one", [{"id": "current"}])
    with pytest.raises(ValueError):
        replace(conn, "worker:one", [{"id": "replacement"}, {}])
    assert keys(conn) == {"current"}


def test_unavailable_discovery_keeps_last_successful_snapshot(conn, monkeypatch):
    from hugpy_core.models import catalog_live
    replace(conn, "discovery:local", [{"key": "current"}])
    def fail():
        raise OSError("discovery database unavailable")
    monkeypatch.setattr(catalog_live, "catalog_index", fail)
    refresh_local()
    assert keys(conn) == {"current"}

def test_current_source_identity_is_not_redirected_by_a_historical_alias(conn):
    conn.execute("INSERT INTO model_key_aliases VALUES ('current', '/old/model.gguf')")
    replace(conn, "discovery:local", [{"key": "current"}])
    assert keys(conn) == {"current"}
