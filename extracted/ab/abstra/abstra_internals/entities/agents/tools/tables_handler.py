"""Tool handlers for table operations.

Each AgentPermission with type="tables" maps to a handler that can
execute SQL queries against the specified table.
"""

import json
from typing import Any, Dict, List

from abstra_internals.repositories.tables import TablesRepository


def _safe_identifier(name: str) -> str:
    """Sanitize a table/column name to prevent SQL injection."""
    return name.replace('"', '""')


class TablesSelectHandler:
    """Handler for SELECT queries on a specific table."""

    def __init__(self, table_name: str, tables_repo: TablesRepository) -> None:
        self._table_name = table_name
        self._tables_repo = tables_repo

    @property
    def name(self) -> str:
        return f"tables_select_{self._table_name}"

    @property
    def description(self) -> str:
        return f"Query rows from the '{self._table_name}' table."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Columns to select. If empty, selects all columns.",
                },
                "where": {
                    "type": "object",
                    "description": "Column-value pairs for WHERE clause (equality filters).",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of rows to return (max 100).",
                    "default": 10,
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of rows to skip.",
                    "default": 0,
                },
            },
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        columns = action_input.get("columns", [])
        where = action_input.get("where", {})
        limit = min(action_input.get("limit", 10), 100)
        offset = action_input.get("offset", 0)

        table = f'"{_safe_identifier(self._table_name)}"'
        cols = (
            ", ".join(f'"{_safe_identifier(c)}"' for c in columns) if columns else "*"
        )
        params: List[Any] = []

        query = f"SELECT {cols} FROM {table}"

        if where:
            conditions = []
            for col, val in where.items():
                params.append(val)
                conditions.append(f'"{_safe_identifier(col)}" = ${len(params)}')
            query += " WHERE " + " AND ".join(conditions)

        params.append(limit)
        query += f" LIMIT ${len(params)}"
        params.append(offset)
        query += f" OFFSET ${len(params)}"

        return _execute_query(self._tables_repo, query, params)


class TablesInsertHandler:
    """Handler for INSERT operations on a specific table."""

    def __init__(self, table_name: str, tables_repo: TablesRepository) -> None:
        self._table_name = table_name
        self._tables_repo = tables_repo

    @property
    def name(self) -> str:
        return f"tables_insert_{self._table_name}"

    @property
    def description(self) -> str:
        return f"Insert a row into the '{self._table_name}' table."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "values": {
                    "type": "object",
                    "description": "Column-value pairs to insert.",
                },
            },
            "required": ["values"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        values = action_input.get("values", {})
        if not values:
            return "Error: 'values' must be a non-empty object."

        table = f'"{_safe_identifier(self._table_name)}"'
        cols = ", ".join(f'"{_safe_identifier(c)}"' for c in values.keys())
        params: List[Any] = list(values.values())
        placeholders = ", ".join(f"${i + 1}" for i in range(len(params)))

        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) RETURNING *"
        return _execute_query(self._tables_repo, query, params)


class TablesUpdateHandler:
    """Handler for UPDATE operations on a specific table."""

    def __init__(self, table_name: str, tables_repo: TablesRepository) -> None:
        self._table_name = table_name
        self._tables_repo = tables_repo

    @property
    def name(self) -> str:
        return f"tables_update_{self._table_name}"

    @property
    def description(self) -> str:
        return f"Update rows in the '{self._table_name}' table."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "set": {
                    "type": "object",
                    "description": "Column-value pairs to update.",
                },
                "where": {
                    "type": "object",
                    "description": "Column-value pairs for WHERE clause (required).",
                },
            },
            "required": ["set", "where"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        set_values = action_input.get("set", {})
        where = action_input.get("where", {})
        if not set_values:
            return "Error: 'set' must be a non-empty object."
        if not where:
            return "Error: 'where' must be a non-empty object (to prevent full-table updates)."

        table = f'"{_safe_identifier(self._table_name)}"'
        params: List[Any] = []

        set_parts = []
        for col, val in set_values.items():
            params.append(val)
            set_parts.append(f'"{_safe_identifier(col)}" = ${len(params)}')

        where_parts = []
        for col, val in where.items():
            params.append(val)
            where_parts.append(f'"{_safe_identifier(col)}" = ${len(params)}')

        query = (
            f"UPDATE {table} SET {', '.join(set_parts)} "
            f"WHERE {' AND '.join(where_parts)} RETURNING *"
        )
        return _execute_query(self._tables_repo, query, params)


class TablesDeleteHandler:
    """Handler for DELETE operations on a specific table."""

    def __init__(self, table_name: str, tables_repo: TablesRepository) -> None:
        self._table_name = table_name
        self._tables_repo = tables_repo

    @property
    def name(self) -> str:
        return f"tables_delete_{self._table_name}"

    @property
    def description(self) -> str:
        return f"Delete rows from the '{self._table_name}' table."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "where": {
                    "type": "object",
                    "description": "Column-value pairs for WHERE clause (required).",
                },
            },
            "required": ["where"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        where = action_input.get("where", {})
        if not where:
            return "Error: 'where' must be a non-empty object (to prevent full-table deletes)."

        table = f'"{_safe_identifier(self._table_name)}"'
        params: List[Any] = []

        where_parts = []
        for col, val in where.items():
            params.append(val)
            where_parts.append(f'"{_safe_identifier(col)}" = ${len(params)}')

        query = f"DELETE FROM {table} WHERE {' AND '.join(where_parts)} RETURNING *"
        return _execute_query(self._tables_repo, query, params)


def _execute_query(tables_repo: TablesRepository, query: str, params: List[Any]) -> str:
    """Execute a SQL query and return the result as a JSON string."""
    try:
        response = tables_repo.execute(query, params)
        if not response.ok:
            return f"Error: Query failed with status {response.status_code}"
        data = response.json()
        if data.get("errors"):
            return f"Error: {json.dumps(data['errors'])}"
        rows = data.get("returns", {}).get("result", [])
        return json.dumps(rows, default=str)
    except Exception as e:
        return f"Error executing query: {str(e)}"
