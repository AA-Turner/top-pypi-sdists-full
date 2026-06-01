"""Tests for MariaAdapter and PGAdapter.

These tests patch runtime driver imports so they run without pymysql/psycopg
installed in the unit-test environment.
"""

from types import SimpleNamespace

import pytest

from csrd.repository import MariaAdapter, PGAdapter


class _FakeUndefinedColumn(Exception):
    pass


class _FakeMariaConn:
    def __init__(self, last_id: int = 42):
        self._last_id = last_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def cursor(self):
        return self

    def execute(self, query, params):
        self._last = (query, params)

    def fetchone(self):
        return {"ok": True}

    def fetchall(self):
        return [{"ok": True}]

    @property
    def rowcount(self):
        return 1

    @property
    def lastrowid(self):
        return self._last_id


class _FakePGCursor:
    def __init__(self, last_id: int | None = 42):
        self.rowcount = 1
        self._last_id = last_id

    def fetchone(self):
        if self._last_id is not None:
            return {"id": self._last_id}
        return None

    def fetchall(self):
        return [{"ok": True}]


class _FakePGConn:
    def __init__(self, last_id: int | None = 42):
        self._last_id = last_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def execute(self, query, params):
        self._last = (query, params)
        return _FakePGCursor(self._last_id)


def _patch_maria_import(monkeypatch: pytest.MonkeyPatch) -> None:
    import csrd.repository.adapters.maria_adapter as maria_mod

    def fake_import(name: str):
        if name == "pymysql":
            return SimpleNamespace(connect=lambda **kwargs: _FakeMariaConn())
        if name == "pymysql.cursors":
            return SimpleNamespace(DictCursor=object)
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(maria_mod, "import_module", fake_import)


def _patch_pg_import(monkeypatch: pytest.MonkeyPatch) -> None:
    import csrd.repository.adapters.pg_adapter as pg_mod

    def fake_import(name: str):
        if name == "psycopg":
            return SimpleNamespace(
                connect=lambda conninfo, row_factory=None, autocommit=True: _FakePGConn(),
                errors=SimpleNamespace(UndefinedColumn=_FakeUndefinedColumn),
            )
        if name == "psycopg.rows":
            return SimpleNamespace(dict_row=object)
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(pg_mod, "import_module", fake_import)


class TestMariaAdapter:
    @pytest.mark.asyncio
    async def test_upsert_sql_shape(self, monkeypatch: pytest.MonkeyPatch):
        _patch_maria_import(monkeypatch)
        adapter = MariaAdapter(host="db", port=3306, user="u", password="p", database="d")

        captured: dict[str, object] = {}

        async def fake_execute(query, params):
            captured["query"] = query
            captured["params"] = params
            return 1

        monkeypatch.setattr(adapter, "execute", fake_execute)

        rows = await adapter.upsert(
            "items",
            {"name": "Widget", "updated_at": "2026-01-01T00:00:00Z"},
            {"id": "123"},
        )

        assert rows == 1
        assert "ON DUPLICATE KEY UPDATE" in str(captured["query"])

    @pytest.mark.asyncio
    async def test_insert_returns_id(self, monkeypatch: pytest.MonkeyPatch):
        _patch_maria_import(monkeypatch)
        adapter = MariaAdapter(host="db", port=3306, user="u", password="p", database="d")
        result = await adapter.insert("items", {"name": "Widget"})
        assert result["id"] == 42
        assert result["name"] == "Widget"

    @pytest.mark.asyncio
    async def test_execute_returning_has_lastrowid(self, monkeypatch: pytest.MonkeyPatch):
        from csrd.repository import ExecuteResult

        _patch_maria_import(monkeypatch)
        adapter = MariaAdapter(host="db", port=3306, user="u", password="p", database="d")
        result = await adapter.execute_returning(
            "INSERT INTO items (name) VALUES (%(name)s)", {"name": "x"}
        )
        assert isinstance(result, ExecuteResult)
        assert result.lastrowid == 42
        assert result.rowcount == 1


class TestPGAdapter:
    @pytest.mark.asyncio
    async def test_upsert_sql_shape(self, monkeypatch: pytest.MonkeyPatch):
        _patch_pg_import(monkeypatch)
        adapter = PGAdapter(host="db", port=5432, user="u", password="p", database="d")

        captured: dict[str, object] = {}

        async def fake_execute(query, params):
            captured["query"] = query
            captured["params"] = params
            return 1

        monkeypatch.setattr(adapter, "execute", fake_execute)

        rows = await adapter.upsert(
            "items",
            {"name": "Widget", "updated_at": "2026-01-01T00:00:00Z"},
            {"id": "123"},
        )

        assert rows == 1
        assert "ON CONFLICT" in str(captured["query"])

    @pytest.mark.asyncio
    async def test_insert_returns_id_and_uses_returning(self, monkeypatch: pytest.MonkeyPatch):
        _patch_pg_import(monkeypatch)
        adapter = PGAdapter(host="db", port=5432, user="u", password="p", database="d")
        result = await adapter.insert("items", {"name": "Widget"})
        assert result["id"] == 42
        assert result["name"] == "Widget"

    @pytest.mark.asyncio
    async def test_insert_falls_back_when_table_has_no_id_column(
        self, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_pg_import(monkeypatch)
        adapter = PGAdapter(host="db", port=5432, user="u", password="p", database="d")

        def fake_execute_returning_sync(query, params):
            raise _FakeUndefinedColumn('column "id" does not exist')

        captured: dict[str, object] = {}

        async def fake_execute(query, params):
            captured["query"] = query
            captured["params"] = params
            return 1

        monkeypatch.setattr(adapter, "_execute_returning_sync", fake_execute_returning_sync)
        monkeypatch.setattr(adapter, "execute", fake_execute)

        result = await adapter.insert(
            "inventory_items", {"item_id": "wrench-1", "item_name": "Wrench"}
        )

        assert result == {"item_id": "wrench-1", "item_name": "Wrench"}
        assert "RETURNING id" not in str(captured["query"])

    @pytest.mark.asyncio
    async def test_execute_returning_has_lastrowid(self, monkeypatch: pytest.MonkeyPatch):
        from csrd.repository import ExecuteResult

        _patch_pg_import(monkeypatch)
        adapter = PGAdapter(host="db", port=5432, user="u", password="p", database="d")
        result = await adapter.execute_returning(
            "INSERT INTO items (name) VALUES (%(name)s) RETURNING id", {"name": "y"}
        )
        assert isinstance(result, ExecuteResult)
        assert result.lastrowid == 42
        assert result.rowcount == 1


def test_repository_exports_network_adapters(monkeypatch: pytest.MonkeyPatch):
    _patch_maria_import(monkeypatch)
    _patch_pg_import(monkeypatch)

    maria = MariaAdapter(host="db", port=3306, user="u", password="p", database="d")
    pg = PGAdapter(host="db", port=5432, user="u", password="p", database="d")

    assert maria is not None
    assert pg is not None


# ---------------------------------------------------------------------------
# :param → %(param)s normalisation
# ---------------------------------------------------------------------------


class TestPGNormalizeQuery:
    """Verify the PGAdapter converts :param placeholders to %(param)s."""

    def test_basic_named_params(self):
        from csrd.repository.adapters.pg_adapter import _normalize_query

        result = _normalize_query("SELECT * FROM t WHERE id = :id AND name = :name")
        assert result == "SELECT * FROM t WHERE id = %(id)s AND name = %(name)s"

    def test_double_colon_cast_preserved(self):
        from csrd.repository.adapters.pg_adapter import _normalize_query

        result = _normalize_query("SELECT value::text FROM t WHERE id = :id")
        assert result == "SELECT value::text FROM t WHERE id = %(id)s"

    def test_no_params_unchanged(self):
        from csrd.repository.adapters.pg_adapter import _normalize_query

        query = "CREATE TABLE IF NOT EXISTS t (id TEXT PRIMARY KEY)"
        assert _normalize_query(query) == query

    def test_already_pyformat_unchanged(self):
        from csrd.repository.adapters.pg_adapter import _normalize_query

        query = "INSERT INTO t (name) VALUES (%(name)s)"
        assert _normalize_query(query) == query

    @pytest.mark.asyncio
    async def test_execute_normalizes_colon_params(self, monkeypatch: pytest.MonkeyPatch):
        captured: dict[str, object] = {}
        orig_conn_cls = _FakePGConn

        class CapturingConn(orig_conn_cls):
            def execute(self, query, params):
                captured["query"] = query
                captured["params"] = params
                return super().execute(query, params)

        import csrd.repository.adapters.pg_adapter as pg_mod

        monkeypatch.setattr(
            pg_mod,
            "import_module",
            lambda name: (
                SimpleNamespace(
                    connect=lambda conninfo, row_factory=None, autocommit=True: CapturingConn(),
                    errors=SimpleNamespace(UndefinedColumn=_FakeUndefinedColumn),
                )
                if name == "psycopg"
                else SimpleNamespace(dict_row=object)
            ),
        )
        adapter2 = PGAdapter(host="db", port=5432, user="u", password="p", database="d")
        await adapter2.execute(
            "INSERT INTO signing_keys (kid) VALUES (:kid)",
            {"kid": "key-123"},
        )
        assert captured["query"] == "INSERT INTO signing_keys (kid) VALUES (%(kid)s)"


class TestMariaNormalizeQuery:
    """Verify the MariaAdapter converts :param placeholders to %(param)s."""

    def test_basic_named_params(self):
        from csrd.repository.adapters.maria_adapter import _normalize_query

        result = _normalize_query("SELECT * FROM t WHERE id = :id AND name = :name")
        assert result == "SELECT * FROM t WHERE id = %(id)s AND name = %(name)s"

    def test_no_params_unchanged(self):
        from csrd.repository.adapters.maria_adapter import _normalize_query

        query = "CREATE TABLE IF NOT EXISTS t (id TEXT PRIMARY KEY)"
        assert _normalize_query(query) == query
