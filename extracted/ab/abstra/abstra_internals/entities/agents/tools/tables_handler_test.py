import json
from unittest.mock import MagicMock

from abstra_internals.entities.agents.tools.tables_handler import (
    TablesDeleteHandler,
    TablesInsertHandler,
    TablesSelectHandler,
    TablesUpdateHandler,
    _safe_identifier,
)


class TestSafeIdentifier:
    def test_normal_name(self):
        assert _safe_identifier("users") == "users"

    def test_name_with_double_quotes(self):
        assert _safe_identifier('my"table') == 'my""table'

    def test_name_with_multiple_double_quotes(self):
        assert _safe_identifier('"a"b"') == '""a""b""'

    def test_empty_string(self):
        assert _safe_identifier("") == ""


def _make_mock_repo(rows=None, ok=True, status_code=200, errors=None):
    """Create a mock TablesRepository whose execute() returns a mock response."""
    mock_repo = MagicMock()
    mock_response = MagicMock()
    mock_response.ok = ok
    mock_response.status_code = status_code
    mock_response.json.return_value = {
        "errors": errors or [],
        "returns": {"result": rows if rows is not None else []},
    }
    mock_repo.execute.return_value = mock_response
    return mock_repo


class TestTablesSelectHandler:
    def test_name(self):
        handler = TablesSelectHandler(table_name="users", tables_repo=MagicMock())
        assert handler.name == "tables_select_users"

    def test_description(self):
        handler = TablesSelectHandler(table_name="orders", tables_repo=MagicMock())
        assert "orders" in handler.description

    def test_input_schema_has_columns_where_limit_offset(self):
        handler = TablesSelectHandler(table_name="t", tables_repo=MagicMock())
        schema = handler.input_schema
        assert "columns" in schema["properties"]
        assert "where" in schema["properties"]
        assert "limit" in schema["properties"]
        assert "offset" in schema["properties"]

    def test_execute_basic_select(self):
        rows = [{"id": 1, "name": "Alice"}]
        mock_repo = _make_mock_repo(rows=rows)
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        result = handler.execute({})
        parsed = json.loads(result)
        assert parsed == rows

        # Verify the query was called
        call_args = mock_repo.execute.call_args
        query = call_args[0][0]
        assert "SELECT * FROM" in query
        assert '"users"' in query

    def test_execute_with_columns(self):
        mock_repo = _make_mock_repo(rows=[])
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        handler.execute({"columns": ["name", "email"]})

        query = mock_repo.execute.call_args[0][0]
        assert '"name"' in query
        assert '"email"' in query
        assert "*" not in query

    def test_execute_with_where_clause(self):
        mock_repo = _make_mock_repo(rows=[{"id": 1}])
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        handler.execute({"where": {"status": "active"}})

        query = mock_repo.execute.call_args[0][0]
        params = mock_repo.execute.call_args[0][1]
        assert "WHERE" in query
        assert '"status" = $1' in query
        assert "active" in params

    def test_execute_limit_clamped_to_100(self):
        mock_repo = _make_mock_repo(rows=[])
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        handler.execute({"limit": 5000})

        params = mock_repo.execute.call_args[0][1]
        # limit is clamped to 100, should be in params
        assert 100 in params

    def test_execute_limit_negative_uses_negative(self):
        """When limit is negative, min(-5, 100) = -5, so it passes through."""
        mock_repo = _make_mock_repo(rows=[])
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        handler.execute({"limit": -5})

        params = mock_repo.execute.call_args[0][1]
        assert -5 in params

    def test_execute_default_limit(self):
        mock_repo = _make_mock_repo(rows=[])
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        handler.execute({})

        params = mock_repo.execute.call_args[0][1]
        # Default limit is 10, offset is 0
        assert 10 in params
        assert 0 in params

    def test_execute_query_failure(self):
        mock_repo = _make_mock_repo(ok=False, status_code=500)
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        result = handler.execute({})
        assert "Error" in result
        assert "500" in result

    def test_execute_query_errors_in_response(self):
        mock_repo = _make_mock_repo(errors=[{"message": "syntax error"}])
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        result = handler.execute({})
        assert "Error" in result
        assert "syntax error" in result

    def test_execute_exception(self):
        mock_repo = MagicMock()
        mock_repo.execute.side_effect = RuntimeError("connection refused")
        handler = TablesSelectHandler(table_name="users", tables_repo=mock_repo)

        result = handler.execute({})
        assert "Error" in result
        assert "connection refused" in result


class TestTablesInsertHandler:
    def test_name(self):
        handler = TablesInsertHandler(table_name="orders", tables_repo=MagicMock())
        assert handler.name == "tables_insert_orders"

    def test_description(self):
        handler = TablesInsertHandler(table_name="orders", tables_repo=MagicMock())
        assert "orders" in handler.description

    def test_input_schema_requires_values(self):
        handler = TablesInsertHandler(table_name="t", tables_repo=MagicMock())
        assert "values" in handler.input_schema.get("required", [])

    def test_execute_insert(self):
        inserted = [{"id": 1, "name": "Bob", "age": 30}]
        mock_repo = _make_mock_repo(rows=inserted)
        handler = TablesInsertHandler(table_name="users", tables_repo=mock_repo)

        result = handler.execute({"values": {"name": "Bob", "age": 30}})
        parsed = json.loads(result)
        assert parsed == inserted

        query = mock_repo.execute.call_args[0][0]
        assert "INSERT INTO" in query
        assert "RETURNING *" in query

    def test_execute_empty_values_returns_error(self):
        handler = TablesInsertHandler(table_name="users", tables_repo=MagicMock())

        result = handler.execute({"values": {}})
        assert "Error" in result

    def test_execute_missing_values_returns_error(self):
        handler = TablesInsertHandler(table_name="users", tables_repo=MagicMock())

        result = handler.execute({})
        assert "Error" in result


class TestTablesUpdateHandler:
    def test_name(self):
        handler = TablesUpdateHandler(table_name="items", tables_repo=MagicMock())
        assert handler.name == "tables_update_items"

    def test_description(self):
        handler = TablesUpdateHandler(table_name="items", tables_repo=MagicMock())
        assert "items" in handler.description

    def test_execute_update(self):
        updated = [{"id": 1, "status": "done"}]
        mock_repo = _make_mock_repo(rows=updated)
        handler = TablesUpdateHandler(table_name="tasks", tables_repo=mock_repo)

        result = handler.execute({"set": {"status": "done"}, "where": {"id": 1}})
        parsed = json.loads(result)
        assert parsed == updated

        query = mock_repo.execute.call_args[0][0]
        assert "UPDATE" in query
        assert "SET" in query
        assert "WHERE" in query
        assert "RETURNING *" in query

    def test_execute_missing_where_returns_error(self):
        handler = TablesUpdateHandler(table_name="tasks", tables_repo=MagicMock())

        result = handler.execute({"set": {"status": "done"}, "where": {}})
        assert "Error" in result
        assert "where" in result.lower()

    def test_execute_missing_set_returns_error(self):
        handler = TablesUpdateHandler(table_name="tasks", tables_repo=MagicMock())

        result = handler.execute({"set": {}, "where": {"id": 1}})
        assert "Error" in result
        assert "set" in result.lower()


class TestTablesDeleteHandler:
    def test_name(self):
        handler = TablesDeleteHandler(table_name="logs", tables_repo=MagicMock())
        assert handler.name == "tables_delete_logs"

    def test_description(self):
        handler = TablesDeleteHandler(table_name="logs", tables_repo=MagicMock())
        assert "logs" in handler.description

    def test_execute_delete(self):
        deleted = [{"id": 5}]
        mock_repo = _make_mock_repo(rows=deleted)
        handler = TablesDeleteHandler(table_name="logs", tables_repo=mock_repo)

        result = handler.execute({"where": {"id": 5}})
        parsed = json.loads(result)
        assert parsed == deleted

        query = mock_repo.execute.call_args[0][0]
        assert "DELETE FROM" in query
        assert "WHERE" in query
        assert "RETURNING *" in query

    def test_execute_missing_where_returns_error(self):
        handler = TablesDeleteHandler(table_name="logs", tables_repo=MagicMock())

        result = handler.execute({"where": {}})
        assert "Error" in result
        assert "where" in result.lower()

    def test_execute_no_where_key_returns_error(self):
        handler = TablesDeleteHandler(table_name="logs", tables_repo=MagicMock())

        result = handler.execute({})
        assert "Error" in result
