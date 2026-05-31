"""S14 — migrations ship in the wheel as embedded SQL (no .sql data files, D2)."""

import abstra_internals.services.db.connection as connection
import abstra_internals.services.db.migrations as migrations


def test_ddl_is_embedded_as_python_strings():
    # No dependency on __file__ or packaged .sql files: the DDL is a module-level
    # Python list (setup.py package_data only ships templates/*, so .sql would not
    # land in the wheel — decision D2).
    assert isinstance(migrations.MIGRATIONS, list) and migrations.MIGRATIONS
    version, sql = migrations.MIGRATIONS[0]
    assert version == 1
    assert "CREATE TABLE executions" in sql
    assert "CREATE TABLE tasks" in sql
    assert "CREATE TABLE execution_logs" in sql


def test_no_sql_data_files_shipped():
    # The DDL is embedded in Python; there must be no .sql data files in the
    # package (setup.py package_data would not ship them anyway — D2).
    import pathlib

    import abstra_internals.services.db as dbpkg

    db_dir = pathlib.Path(dbpkg.__file__).parent
    assert list(db_dir.rglob("*.sql")) == []


def test_log_pool_stats_is_noop_without_pool():
    # Observability helper must be safe to call when no pool exists.
    connection._reset_pool_for_tests()
    connection.log_pool_stats()  # must not raise
