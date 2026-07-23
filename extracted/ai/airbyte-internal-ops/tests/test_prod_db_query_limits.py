"""Tests for optional prod DB query limits."""

import sqlalchemy

from airbyte_ops_mcp.prod_db_access import queries


def test_query_new_connector_releases_omits_limit_clause_when_unbounded(
    monkeypatch,
) -> None:
    captured_statements: list[sqlalchemy.sql.elements.TextClause] = []
    captured_parameters: list[dict[str, object]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured_statements.append(statement)
        captured_parameters.append(parameters)
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_new_connector_releases(days=30, limit=None)

    assert "LIMIT :limit" not in str(captured_statements[0].text)
    assert "limit" not in captured_parameters[0]
    assert "cutoff_date" in captured_parameters[0]


def test_query_new_connector_releases_keeps_limit_clause_when_limited(
    monkeypatch,
) -> None:
    captured_statements: list[sqlalchemy.sql.elements.TextClause] = []
    captured_parameters: list[dict[str, object]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured_statements.append(statement)
        captured_parameters.append(parameters)
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_new_connector_releases(days=30, limit=100)

    assert "LIMIT :limit" in str(captured_statements[0].text)
    assert captured_parameters[0]["limit"] == 100


def test_query_connector_rollouts_omits_limit_clause_when_unbounded(
    monkeypatch,
) -> None:
    captured_statements: list[sqlalchemy.sql.elements.TextClause] = []
    captured_parameters: list[dict[str, object]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured_statements.append(statement)
        captured_parameters.append(parameters)
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_connector_rollouts(active_only=True, limit=None)

    assert "LIMIT :limit" not in str(captured_statements[0].text)
    assert "limit" not in captured_parameters[0]


def test_query_connector_rollouts_keeps_definition_filter_when_unbounded(
    monkeypatch,
) -> None:
    captured_statements: list[sqlalchemy.sql.elements.TextClause] = []
    captured_parameters: list[dict[str, object]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured_statements.append(statement)
        captured_parameters.append(parameters)
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_connector_rollouts(
        actor_definition_id="definition-id",
        active_only=True,
        limit=None,
    )

    assert "LIMIT :limit" not in str(captured_statements[0].text)
    assert captured_parameters[0] == {"actor_definition_id": "definition-id"}


def test_query_connections_by_connector_omits_limit_clause_when_unbounded(
    monkeypatch,
) -> None:
    captured_statements: list[sqlalchemy.sql.elements.TextClause] = []
    captured_parameters: list[dict[str, object]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured_statements.append(statement)
        captured_parameters.append(parameters)
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_connections_by_connector(
        connector_definition_id="definition-id",
        limit=None,
        exclude_pinned=True,
        enabled_schedules_only=True,
    )

    assert "LIMIT :limit" not in str(captured_statements[0].text)
    assert captured_parameters[0] == {"connector_definition_id": "definition-id"}


def test_query_connections_by_connector_keeps_limit_clause_when_limited(
    monkeypatch,
) -> None:
    captured_statements: list[sqlalchemy.sql.elements.TextClause] = []
    captured_parameters: list[dict[str, object]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured_statements.append(statement)
        captured_parameters.append(parameters)
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_connections_by_connector(
        connector_definition_id="definition-id",
        limit=500,
    )

    assert "LIMIT :limit" in str(captured_statements[0].text)
    assert captured_parameters[0]["limit"] == 500


def test_query_connections_by_destination_connector_omits_limit_when_unbounded(
    monkeypatch,
) -> None:
    captured_statements: list[sqlalchemy.sql.elements.TextClause] = []
    captured_parameters: list[dict[str, object]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured_statements.append(statement)
        captured_parameters.append(parameters)
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_connections_by_destination_connector(
        connector_definition_id="definition-id",
        limit=None,
        exclude_pinned=True,
        enabled_schedules_only=True,
    )

    assert "LIMIT :limit" not in str(captured_statements[0].text)
    assert captured_parameters[0] == {"connector_definition_id": "definition-id"}
