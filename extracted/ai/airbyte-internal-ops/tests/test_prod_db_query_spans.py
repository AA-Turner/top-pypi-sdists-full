# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Prod DB query span attributes.

Bind values are not recorded by Sentry's SQLAlchemy integration — enabling
`record_sql_params` is all-or-nothing and would ship operator search strings.
These attributes are the selective, redacted alternative, so the redaction and
the cast-safe placeholder parsing both need guarding.
"""

import pytest
import sqlalchemy

from airbyte_ops_mcp.prod_db_access import queries, sql


@pytest.mark.unit
def test_population_query_placeholders_exclude_casts() -> None:
    names = queries._sql_placeholder_names(sql.SELECT_SOURCE_ACTOR_POPULATION_BY_ORG)

    assert names == [
        "actor_definition_id",
        "rollout_created_at",
        "target_version_id",
    ]


@pytest.mark.unit
def test_unknown_parameters_are_redacted_by_default() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE email = :customer_email"),
        {"customer_email": "someone@customer.example"},
        query_name="SELECT_PROBE",
    )

    assert attributes["db.param.customer_email"] == queries._REDACTED_VALUE
    assert "customer.example" not in str(attributes)


@pytest.mark.unit
@pytest.mark.parametrize(
    "excluded",
    ["email_domain", "name_contains", "stream_name"],
)
def test_customer_identifying_parameters_are_excluded(excluded: str) -> None:
    assert excluded not in queries._RECORDED_PARAMETERS

    attributes = queries._query_span_attributes(
        sqlalchemy.text(f"SELECT 1 WHERE col = :{excluded}"),
        {excluded: "Acme Corporation"},
        query_name="SELECT_PROBE",
    )

    assert attributes[f"db.param.{excluded}"] == queries._REDACTED_VALUE
    assert "Acme Corporation" not in str(attributes)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("placeholder", "value"),
    [
        pytest.param("organization_id", "org-uuid", id="identifier"),
        pytest.param("cutoff_date", "2026-09-01T00:00:00Z", id="time_window"),
        pytest.param("limit", 1000, id="query_shaping"),
        pytest.param("docker_repository", "airbyte/source-faker", id="artifact"),
    ],
)
def test_allowlisted_parameters_record_their_value(
    placeholder: str, value: object
) -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text(f"SELECT 1 WHERE col = :{placeholder}"),
        {placeholder: value},
        query_name="SELECT_PROBE",
    )

    assert attributes[f"db.param.{placeholder}"] == str(value)


@pytest.mark.unit
def test_declared_but_unbound_placeholders_are_flagged() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE a = :organization_id AND b = :workspace_id"),
        {"organization_id": "org-uuid"},
        query_name="SELECT_PROBE",
    )

    assert attributes["db.param.organization_id"] == "org-uuid"
    assert attributes["db.param.workspace_id"] == queries._UNBOUND_VALUE
    assert attributes["db.unbound_params.count"] == 1


@pytest.mark.unit
def test_unbound_wins_over_redaction() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE col = :name_contains"),
        {},
        query_name="SEARCH_PROBE",
    )

    assert "name_contains" not in queries._RECORDED_PARAMETERS
    assert attributes["db.param.name_contains"] == queries._UNBOUND_VALUE
    assert attributes["db.unbound_params.count"] == 1


@pytest.mark.unit
def test_fully_bound_query_reports_no_unbound_params() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE a = :organization_id"),
        {"organization_id": "org-uuid"},
        query_name="SELECT_PROBE",
    )

    assert "db.unbound_params.count" not in attributes


@pytest.mark.unit
@pytest.mark.parametrize(
    ("size", "id_suffix"),
    [
        pytest.param(500, "large", id="large"),
        pytest.param(2, "small", id="small_is_not_special_cased"),
        pytest.param(0, "empty", id="empty"),
    ],
)
def test_collections_record_only_their_count(size: int, id_suffix: str) -> None:
    ids = [f"id-{index}" for index in range(size)]
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE id = ANY(:connection_ids)"),
        {"connection_ids": ids},
        query_name="SELECT_PROBE",
    )

    assert attributes["db.param.connection_ids.count"] == size
    assert isinstance(attributes["db.param.connection_ids.count"], int)
    assert "db.param.connection_ids" not in attributes
    for one_id in ids:
        assert one_id not in str(attributes)


@pytest.mark.unit
def test_unlisted_collection_still_records_its_count() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE e = ANY(:customer_emails)"),
        {"customer_emails": ["a@x.com", "b@y.com", "c@z.com"]},
        query_name="SELECT_PROBE",
    )

    assert "customer_emails" not in queries._RECORDED_PARAMETERS
    assert attributes["db.param.customer_emails.count"] == 3
    assert "db.param.customer_emails" not in attributes
    assert "x.com" not in str(attributes)


@pytest.mark.unit
def test_unbound_collection() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE id = ANY(:connection_ids)"),
        {},
        query_name="SELECT_PROBE",
    )

    assert attributes["db.param.connection_ids"] == queries._UNBOUND_VALUE
    assert "db.param.connection_ids.count" not in attributes
    assert attributes["db.unbound_params.count"] == 1


@pytest.mark.unit
def test_string_params_are_not_treated_as_collections() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE repo = :docker_repository"),
        {"docker_repository": "airbyte/source-faker"},
        query_name="SELECT_PROBE",
    )

    assert attributes["db.param.docker_repository"] == "airbyte/source-faker"
    assert "db.param.docker_repository.count" not in attributes


@pytest.mark.unit
def test_long_scalar_values_are_truncated() -> None:
    """Span attributes stay bounded regardless of the bound value."""
    rendered = queries._format_parameter_value("x" * 5_000)

    assert rendered.endswith("...")
    assert len(rendered) == queries._MAX_ATTRIBUTE_CHARS + len("...")


@pytest.mark.unit
def test_none_parameter_is_recorded_rather_than_dropped() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE a = :target_version_id"),
        {"target_version_id": None},
        query_name="SELECT_PROBE",
    )

    assert attributes["db.param.target_version_id"] == "None"
    assert "db.unbound_params.count" not in attributes


@pytest.mark.unit
def test_multiple_unbound() -> None:
    attributes = queries._query_span_attributes(
        sqlalchemy.text("SELECT 1 WHERE a = :organization_id AND b = :workspace_id"),
        {},
        query_name="SELECT_PROBE",
    )

    assert attributes["db.unbound_params.count"] == 2
    assert attributes["db.param.organization_id"] == queries._UNBOUND_VALUE
    assert attributes["db.param.workspace_id"] == queries._UNBOUND_VALUE
