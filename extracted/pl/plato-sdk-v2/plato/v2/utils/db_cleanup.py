"""Database cleanup operations for truncating audit_log tables."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from plato._generated.api.v1.simulator import get_db_config
from plato._generated.models import DbConfigResponse
from plato.v2.utils.gateway_tunnel import GatewayTunnel, find_free_port
from plato.v2.utils.models import (
    ApiCleanupResult,
    DatabaseCleanupResult,
    EnvironmentCleanupResult,
    EnvironmentInfo,
    SessionCleanupResult,
)
from plato.v2.utils.proxy_tunnel import make_db_url

logger = logging.getLogger(__name__)


class DatabaseCleaner:
    """Handles database audit_log cleanup operations."""

    async def cleanup_session(
        self,
        envs: list[EnvironmentInfo],
        http_client: httpx.AsyncClient,
        api_key: str,
    ) -> SessionCleanupResult:
        """Clean up all databases for all environments in a session.

        Environments and databases are cleaned up in parallel for efficiency.
        Ports are pre-allocated globally to avoid conflicts.

        Args:
            envs: List of EnvironmentInfo objects with cleanup callbacks.
            http_client: HTTP client for API calls.
            api_key: API key for authentication.

        Returns:
            SessionCleanupResult with results for each environment.
        """
        # Step 1: Fetch DB configs for all environments with artifacts, in parallel
        env_db_configs: dict[str, list[DbConfigResponse]] = {}

        async def fetch_db_configs(env: EnvironmentInfo):
            if env.artifact_id:
                try:
                    configs_raw = await get_db_config.asyncio(
                        client=http_client,
                        artifact_id=env.artifact_id,
                        x_api_key=api_key,
                    )
                    # Parse dicts into DbConfigResponse models and filter to configs with db_database
                    configs = [DbConfigResponse(**c) if isinstance(c, dict) else c for c in (configs_raw or [])]
                    valid_configs = [c for c in configs if c.db_database]
                    if valid_configs:
                        return env.alias, valid_configs
                except Exception as e:
                    logger.warning(f"Failed to get DB configs for {env.alias}: {e}")
            return None

        fetch_tasks = [fetch_db_configs(env) for env in envs]
        fetch_results = await asyncio.gather(*fetch_tasks)
        for result in fetch_results:
            if result is not None:
                alias, valid_configs = result
                env_db_configs[alias] = valid_configs

        # Step 2: Pre-allocate ports globally to avoid conflicts
        port_allocations: dict[str, dict[str, int]] = {}  # env_alias -> {db_name -> port}
        port_counter = 55432
        for env_alias, configs in env_db_configs.items():
            port_allocations[env_alias] = {}
            for config in configs:
                db_name = config.db_database
                port_allocations[env_alias][db_name] = find_free_port(port_counter)
                port_counter += 100  # Space out ports to avoid conflicts

        # Step 3: Run all cleanups in parallel
        async def cleanup_env(env: EnvironmentInfo) -> tuple[str, EnvironmentCleanupResult]:
            # Call cleanup API (best effort) if available
            if env.cleanup_fn is not None:
                try:
                    api_result = await env.cleanup_fn()
                    api_cleanup = ApiCleanupResult(success=True, result=api_result)
                except Exception as e:
                    api_cleanup = ApiCleanupResult(skipped=True, reason=str(e))
            else:
                api_cleanup = ApiCleanupResult(skipped=True, reason="cleanup API not available")

            # Clean databases if we have configs
            databases: dict[str, DatabaseCleanupResult] = {}
            if env.alias in env_db_configs:
                configs = env_db_configs[env.alias]
                ports = port_allocations[env.alias]

                async def cleanup_db(config: DbConfigResponse) -> tuple[str, DatabaseCleanupResult]:
                    db_name = config.db_database
                    port = ports[db_name]
                    try:
                        result = await self._cleanup_single_database(env.job_id, config, port)
                        return db_name, result
                    except Exception as e:
                        logger.warning(f"Failed to cleanup database {db_name}: {e}")
                        return db_name, DatabaseCleanupResult(success=False, error=str(e))

                # Run DB cleanups in parallel for this environment
                db_results = await asyncio.gather(*[cleanup_db(c) for c in configs])
                databases = dict(db_results)

            # Call get_state to clear in-memory mutation cache
            cache_cleared = False
            cache_clear_error = None
            try:
                await env.get_state_fn()
                cache_cleared = True
            except Exception as e:
                cache_clear_error = str(e)

            return env.alias, EnvironmentCleanupResult(
                api_cleanup=api_cleanup,
                databases=databases,
                cache_cleared=cache_cleared,
                cache_clear_error=cache_clear_error,
            )

        # Run environment cleanups in parallel
        results_list = await asyncio.gather(*[cleanup_env(env) for env in envs])
        results = dict(results_list)

        return SessionCleanupResult(environments=results)

    async def _cleanup_single_database(
        self,
        job_id: str,
        config: DbConfigResponse,
        local_port: int,
    ) -> DatabaseCleanupResult:
        """Connect to a single DB via gateway tunnel and truncate audit_log tables."""
        db_port = config.db_port

        tunnel = GatewayTunnel(
            job_id=job_id,
            remote_port=db_port,
            local_port=local_port,
        )

        try:
            await tunnel.start()

            db_url = make_db_url(config, local_port)
            engine = create_async_engine(db_url, pool_pre_ping=True, pool_recycle=30, pool_size=100, max_overflow=20)

            async with engine.begin() as conn:
                tables_truncated = await self._find_and_truncate_audit_logs(conn, config.db_type)

            await engine.dispose()

            return DatabaseCleanupResult(
                success=True,
                tables_truncated=tables_truncated,
            )
        finally:
            await tunnel.stop()

    async def _find_and_truncate_audit_logs(
        self,
        conn: Any,
        db_type: str,
    ) -> list[str]:
        """Find audit_log tables and truncate them.

        Args:
            conn: SQLAlchemy async connection.
            db_type: Database type (postgresql, mysql, sqlite).

        Returns:
            List of truncated table names.
        """
        db_type = db_type.lower()
        truncated: list[str] = []

        if db_type == "postgresql":
            # Find audit_log tables in all schemas
            result = await conn.execute(
                text("SELECT schemaname, tablename FROM pg_tables WHERE tablename = 'audit_log'")
            )
            tables = result.fetchall()

            for schema, table in tables:
                await conn.execute(text(f"TRUNCATE TABLE {schema}.{table} RESTART IDENTITY CASCADE"))
                truncated.append(f"{schema}.{table}")

        elif db_type == "mysql":
            # Find audit_log tables
            result = await conn.execute(
                text(
                    "SELECT table_schema, table_name FROM information_schema.tables "
                    "WHERE table_name = 'audit_log' AND table_schema = DATABASE()"
                )
            )
            tables = result.fetchall()

            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            for schema, table in tables:
                await conn.execute(text(f"DELETE FROM `{table}`"))
                truncated.append(table)
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        elif db_type == "sqlite":
            # Check if audit_log exists
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_log'"))
            if result.fetchone():
                await conn.execute(text("DELETE FROM audit_log"))
                truncated.append("audit_log")

        return truncated
