"""Snowflake cloud-state schema migrations (``scai_cloud_state`` integration)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from scai_cloud_state import Feature
    from scai_cloud_state.connection_manager import SnowflakeConnectionLike


def run_cloud_state_schema_migrations(
    conn: SnowflakeConnectionLike,
    features: Iterable[Feature] | None = None,
) -> None:
    """Apply pending **cloud state** DDL migrations for the requested features.

    Thin pass-through to :func:`scai_cloud_state.run_schema_migrations`.
    The cloud-state schema is split into independently versioned **features**
    (see :class:`scai_cloud_state.Feature`), each with its own migration
    history and its own ``SCHEMA_MIGRATION_<FEATURE>`` tracker table inside
    the COMMON schema.

    Behavior:

    * If ``features`` is ``None`` or empty, this is a logged no-op — nothing
      is created in Snowflake.
    * Otherwise the requested set is expanded to include
      :attr:`scai_cloud_state.Feature.COMMON` plus the transitive closure of
      declared dependencies, then sorted topologically. Each feature's
      :class:`~scai_cloud_state.FeatureMigrationManager` runs its pending
      migrations in turn.

    **Default layout** (used when the corresponding environment variables are
    unset; see ``scai_cloud_state.snowflake_metadata``):

    - ``SNOWCONVERT_AI.COMMON`` — shared metadata, including every per-feature
      ``SCHEMA_MIGRATION_<FEATURE>`` tracker.
    - ``SNOWCONVERT_AI.DATA_MIGRATION`` and ``SNOWCONVERT_AI.DATA_VALIDATION``
      — owned by ``Feature.DATA_MIGRATION_VALIDATION_FRAMEWORK``.
    - ``SNOWCONVERT_AI.ORCHESTRATION`` — owned by ``Feature.ORCHESTRATION``.
    - ``SNOWCONVERT_AI.TESTING`` — owned by ``Feature.TESTING``.

    To target a different database or schema names, set the
    ``CUSTOM_SNOWFLAKE_*`` environment variables **before** opening the
    connection (or before calling this function), as documented in
    ``scai_cloud_state.snowflake_metadata``.

    **Dependency:** requires the ``scai-cloud-state`` distribution (e.g.
    ``pip install 'snowflake-code-unit-registry[cloud-state]'`` or
    ``pip install scai-cloud-state``).

    Args:
        conn: An open Snowflake connection (or any object satisfying
            :class:`~scai_cloud_state.connection_manager.SnowflakeConnectionLike`).
        features: Iterable of :class:`scai_cloud_state.Feature` values to
            deploy. ``Feature.COMMON`` is always included implicitly when
            ``features`` is non-empty.

    Raises:
        ImportError: If ``scai-cloud-state`` is not installed.
        Exception: If a migration step fails (after retries for transient
            Snowflake errors where applicable).

    See Also:
        :class:`scai_cloud_state.FeatureMigrationManager` — lower-level,
        per-feature API.

    Example::

        from scai_cloud_state import Feature
        from snowflake_code_unit_registry import run_cloud_state_schema_migrations

        run_cloud_state_schema_migrations(
            conn,
            [
                Feature.DATA_MIGRATION_VALIDATION_FRAMEWORK,
                Feature.ORCHESTRATION,
                Feature.TESTING,
            ],
        )
    """
    try:
        from scai_cloud_state.run_schema_migrations import run_schema_migrations
    except ImportError as e:
        raise ImportError(
            "run_cloud_state_schema_migrations requires the scai-cloud-state package. "
            "Install with: pip install 'snowflake-code-unit-registry[cloud-state]' "
            "or pip install scai-cloud-state. Then call with a typed Feature list, e.g. "
            "run_cloud_state_schema_migrations(conn, [Feature.TESTING])."
        ) from e
    run_schema_migrations(conn, features)
