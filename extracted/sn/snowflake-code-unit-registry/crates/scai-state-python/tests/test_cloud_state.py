"""Tests for the ``scai_cloud_state`` migration bridge."""

from unittest.mock import MagicMock, patch


def test_run_cloud_state_schema_migrations_forwards_features() -> None:
    from scai_cloud_state import Feature
    from snowflake_code_unit_registry import run_cloud_state_schema_migrations

    conn = MagicMock()
    features = [Feature.DATA_MIGRATION_VALIDATION_FRAMEWORK, Feature.TESTING]
    with patch(
        "scai_cloud_state.run_schema_migrations.run_schema_migrations"
    ) as mocked:
        run_cloud_state_schema_migrations(conn, features)
        mocked.assert_called_once_with(conn, features)


def test_run_cloud_state_schema_migrations_defaults_features_to_none() -> None:
    """If the caller omits ``features``, the bridge passes ``None`` through."""
    from snowflake_code_unit_registry import run_cloud_state_schema_migrations

    conn = MagicMock()
    with patch(
        "scai_cloud_state.run_schema_migrations.run_schema_migrations"
    ) as mocked:
        run_cloud_state_schema_migrations(conn)
        mocked.assert_called_once_with(conn, None)
