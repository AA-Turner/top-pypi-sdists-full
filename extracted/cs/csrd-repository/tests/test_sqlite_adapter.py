"""Tests for SQLiteAdapter."""

import aiosqlite
import pytest

from csrd.repository.adapters.sqlite_adapter import SQLiteAdapter, SQLiteExtractor


@pytest.fixture
async def seeded_adapter(tmp_path):
    """Adapter with a pre-seeded table using the async context manager lifecycle."""
    db_path = str(tmp_path / "test.db")

    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, price REAL)"
        )
        await db.execute("INSERT INTO items (name, price) VALUES ('Widget', 9.99)")
        await db.execute("INSERT INTO items (name, price) VALUES ('Gadget', 19.99)")
        await db.commit()

    async with SQLiteAdapter(db_path) as adapter:
        yield adapter


class TestSQLiteExtractor:
    def test_extract_dict(self):
        ext = SQLiteExtractor()
        result = ext.extract({"name": "test", "value": 42})
        assert result == {"name": "test", "value": 42}

    def test_extract_list_passthrough(self):
        ext = SQLiteExtractor()
        result = ext.extract([{"name": "a"}, {"name": "b"}])
        # With real Row objects this extracts keys; with plain dicts it handles gracefully
        assert isinstance(result, list)


class TestSQLiteAdapter:
    @pytest.mark.asyncio
    async def test_not_connected_raises(self, tmp_path):
        adapter = SQLiteAdapter(str(tmp_path / "unused.db"))
        with pytest.raises(RuntimeError, match="not connected"):
            await adapter.fetch_one("SELECT 1")

    @pytest.mark.asyncio
    async def test_connect_is_idempotent(self, tmp_path):
        adapter = SQLiteAdapter(str(tmp_path / "idem.db"))
        await adapter.connect()
        db1 = adapter._db
        await adapter.connect()  # second call is a no-op
        assert adapter._db is db1
        await adapter.close()

    @pytest.mark.asyncio
    async def test_insert_and_fetch(self, seeded_adapter):
        result = await seeded_adapter.fetch_one(
            "SELECT * FROM items WHERE name = :name", {"name": "Widget"}
        )
        assert result is not None
        assert result["name"] == "Widget"
        assert result["price"] == 9.99

    @pytest.mark.asyncio
    async def test_fetch_all(self, seeded_adapter):
        results = await seeded_adapter.fetch_all("SELECT * FROM items")
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_fetch_one_missing(self, seeded_adapter):
        result = await seeded_adapter.fetch_one(
            "SELECT * FROM items WHERE name = :name", {"name": "NonExistent"}
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_insert(self, seeded_adapter):
        result = await seeded_adapter.insert("items", {"name": "New", "price": 5.0})
        assert result["name"] == "New"
        assert "id" in result

    @pytest.mark.asyncio
    async def test_update(self, seeded_adapter):
        rows = await seeded_adapter.update("items", {"price": 99.99}, {"name": "Widget"})
        assert rows == 1
        updated = await seeded_adapter.fetch_one(
            "SELECT * FROM items WHERE name = :name", {"name": "Widget"}
        )
        assert updated["price"] == 99.99

    @pytest.mark.asyncio
    async def test_delete(self, seeded_adapter):
        rows = await seeded_adapter.delete("items", {"name": "Widget"})
        assert rows == 1
        remaining = await seeded_adapter.fetch_all("SELECT * FROM items")
        assert len(remaining) == 1

    @pytest.mark.asyncio
    async def test_upsert_insert(self, seeded_adapter):
        rows = await seeded_adapter.upsert(
            "items", {"name": "Brand New", "price": 1.0}, {"name": "Brand New"}
        )
        assert rows == 1
        result = await seeded_adapter.fetch_one(
            "SELECT * FROM items WHERE name = :name", {"name": "Brand New"}
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_upsert_update(self, seeded_adapter):
        rows = await seeded_adapter.upsert(
            "items", {"name": "Widget", "price": 0.01}, {"name": "Widget"}
        )
        assert rows == 1
        result = await seeded_adapter.fetch_one(
            "SELECT * FROM items WHERE name = :name", {"name": "Widget"}
        )
        assert result["price"] == 0.01

    @pytest.mark.asyncio
    async def test_execute(self, seeded_adapter):
        rowcount = await seeded_adapter.execute(
            "DELETE FROM items WHERE name = :name", {"name": "Widget"}
        )
        assert rowcount == 1

    @pytest.mark.asyncio
    async def test_execute_returning(self, seeded_adapter):
        from csrd.repository import ExecuteResult

        result = await seeded_adapter.execute_returning(
            "INSERT INTO items (name, price) VALUES (:name, :price)",
            {"name": "Thingamajig", "price": 3.50},
        )
        assert isinstance(result, ExecuteResult)
        assert result.lastrowid is not None
        assert result.rowcount == 1
