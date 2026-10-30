"""Tests for optional prod DB query limits and query-execution behavior."""

import pytest
import sqlalchemy
import sqlalchemy.exc

from airbyte_ops_mcp.prod_db_access import queries, sql


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


def test_query_failed_sync_attempts_for_connector_selects_actor_side(
    monkeypatch,
) -> None:
    captured: list[tuple[str, str]] = []

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        *,
        query_name: str,
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured.append((query_name, str(statement.text)))
        return []

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    queries.query_failed_sync_attempts_for_connector("definition-id")
    queries.query_failed_sync_attempts_for_connector(
        "definition-id", is_destination=True
    )

    (source_name, source_sql), (dest_name, dest_sql) = captured
    assert source_name == "SELECT_FAILED_SYNC_ATTEMPTS_FOR_CONNECTOR"
    assert "ON connection.source_id = actor.id" in source_sql
    assert dest_name == "SELECT_FAILED_SYNC_ATTEMPTS_FOR_DESTINATION_CONNECTOR"
    assert "ON connection.destination_id = actor.id" in dest_sql
    assert "attempts.failure_summary" in dest_sql


@pytest.mark.parametrize("is_destination", [False, True])
@pytest.mark.parametrize(
    "organization_id", [None, "11111111-1111-1111-1111-111111111111"]
)
def test_failed_sync_organization_filter_runs_before_limit(
    monkeypatch: pytest.MonkeyPatch,
    is_destination: bool,
    organization_id: str | None,
) -> None:
    captured: list[tuple[str, dict[str, object]]] = []
    rows = [{"organization_id": organization_id, "failed_attempt_id": 1}]

    def fake_run_sql_query(
        statement: sqlalchemy.sql.elements.TextClause,
        parameters: dict[str, object],
        **_kwargs: object,
    ) -> list[dict[str, object]]:
        captured.append((str(statement), parameters))
        return rows

    monkeypatch.setattr(queries, "_run_sql_query", fake_run_sql_query)

    result = queries.query_failed_sync_attempts_for_connector(
        "definition-id",
        organization_id=organization_id,
        limit=1,
        is_destination=is_destination,
    )

    statement, parameters = captured[0]
    assert parameters["organization_id"] == organization_id
    assert parameters["limit"] == 1
    predicate = "workspace.organization_id = CAST(:organization_id AS uuid)"
    assert statement.index(predicate) < statement.index("ORDER BY")
    assert statement.index("ORDER BY") < statement.index("LIMIT :limit")
    assert "CAST(:organization_id AS uuid) IS NULL" in statement
    assert result is rows


@pytest.mark.parametrize(
    ("statement", "side", "successful_only"),
    [
        (sql.SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION, "source", False),
        (sql.SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION, "source", True),
        (sql.SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION, "destination", False),
        (sql.SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION, "destination", True),
    ],
)
def test_version_sync_sql_restricts_actor_definition_and_keeps_job_version_filter(
    statement: sqlalchemy.sql.elements.TextClause,
    side: str,
    successful_only: bool,
) -> None:
    text = " ".join(str(statement).split())
    assert (
        "actor.actor_definition_id = ( SELECT actor_definition_id "
        "FROM actor_definition_version "
        "WHERE id = CAST(:actor_definition_version_id AS uuid) )"
    ) in text
    assert f"ON connection.{side}_id = actor.id" in text
    assert (
        f"jobs.config->'sync'->>'{side}DefinitionVersionId' "
        "= :actor_definition_version_id"
    ) in text
    assert ("AND jobs.status = 'succeeded'" in text) is successful_only


@pytest.mark.parametrize(
    "statement",
    [
        sql.SELECT_FAILED_SYNC_ATTEMPTS_FOR_CONNECTOR,
        sql.SELECT_FAILED_SYNC_ATTEMPTS_FOR_DESTINATION_CONNECTOR,
        sql.SELECT_SOURCE_SYNC_RESULTS_FOR_VERSION,
        sql.SELECT_SOURCE_SUCCESSFUL_SYNCS_FOR_VERSION,
        sql.SELECT_DESTINATION_SYNC_RESULTS_FOR_VERSION,
        sql.SELECT_DESTINATION_SUCCESSFUL_SYNCS_FOR_VERSION,
    ],
)
def test_sync_pin_joins_constrain_every_composite_index_column(
    statement: sqlalchemy.sql.elements.TextClause,
) -> None:
    text = str(statement)
    for alias, scope in (
        ("actor_pin", "actor"),
        ("ws_pin", "workspace"),
        ("org_pin", "organization"),
    ):
        join = text.split(f"LEFT JOIN scoped_configuration AS {alias}")[1]
        join = join.split("LEFT JOIN")[0].split("WHERE")[0]
        assert f"{alias}.key = 'connector_version'" in join
        assert f"{alias}.resource_type = 'actor_definition'" in join
        assert f"{alias}.resource_id = actor.actor_definition_id" in join
        assert f"{alias}.scope_type = '{scope}'" in join
        assert f"{alias}.scope_id = " in join
