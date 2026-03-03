"""Database cleanup operations for truncating audit_log tables."""

from __future__ import annotations

import asyncio
import logging
import socket
from typing import Any
from urllib.parse import quote_plus

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from plato._generated.api.v1.simulator import get_db_config
from plato._generated.models import DbConfigResponse
from plato.v2.sync.sandbox import Tunnel
from plato.v2.utils.models import (
    ApiCleanupResult,
    DatabaseCleanupResult,
    EnvironmentCleanupResult,
    EnvironmentInfo,
    SessionCleanupResult,
)

logger = logging.getLogger(__name__)


def _make_db_url(config: DbConfigResponse, port: int) -> str:
    """Create SQLAlchemy async connection URL via localhost tunnel."""
    db = config.db_type.lower()
    user = quote_plus(config.db_user)
    password = quote_plus(config.db_password)
    database = quote_plus(config.db_database)

    if db == "postgresql":
        return f"postgresql+asyncpg://{user}:{password}@127.0.0.1:{port}/{database}"
    elif db == "mysql":
        return f"mysql+aiomysql://{user}:{password}@127.0.0.1:{port}/{database}"
    elif db == "sqlite":
        return f"sqlite+aiosqlite:///{config.db_database}"
    raise ValueError(f"Unsupported database type: {db}")


class DatabaseCleaner:
    """Handles database audit_log cleanup operations."""

    async def cleanup_session(
        self,
        envs: list[EnvironmentInfo],
        http_client: httpx.AsyncClient,
        api_key: str,
    ) -> SessionCleanupResult:
        """Clean up all databases for all environments in a session."""
        # Step 1: Fetch DB configs
        env_db_configs: dict[str, list[DbConfigResponse]] = {}

        async def fetch_db_configs(env: EnvironmentInfo):
            if env.artifact_id:
                try:
                    configs_raw = await get_db_config.asyncio(
                        client=http_client,
                        artifact_id=env.artifact_id,
                        x_api_key=api_key,
                    )
                    configs = [DbConfigResponse(**c) if isinstance(c, dict) else c for c in (configs_raw or [])]
                    valid_configs = [c for c in configs if c.db_database]
                    if valid_configs:
                        logger.info(
                            f"[cleanup] {env.alias}: {len(valid_configs)} DB(s): {[c.db_database for c in valid_configs]}"
                        )
                        return env.alias, valid_configs
                    else:
                        logger.warning(f"[cleanup] {env.alias}: no valid DB configs")
                except Exception as e:
                    logger.warning(f"[cleanup] {env.alias}: failed to get DB configs: {e}")
            return None

        fetch_results = await asyncio.gather(*[fetch_db_configs(env) for env in envs])
        for result in fetch_results:
            if result is not None:
                alias, valid_configs = result
                env_db_configs[alias] = valid_configs

        # Step 2: Run cleanups
        async def cleanup_env(env: EnvironmentInfo) -> tuple[str, EnvironmentCleanupResult]:
            if env.cleanup_fn is not None:
                try:
                    api_result = await env.cleanup_fn()
                    api_cleanup = ApiCleanupResult(success=True, result=api_result)
                except Exception as e:
                    api_cleanup = ApiCleanupResult(skipped=True, reason=str(e))
            else:
                api_cleanup = ApiCleanupResult(skipped=True, reason="cleanup API not available")

            databases: dict[str, DatabaseCleanupResult] = {}
            if env.alias in env_db_configs:
                configs = env_db_configs[env.alias]

                async def cleanup_db(config: DbConfigResponse) -> tuple[str, DatabaseCleanupResult]:
                    db_name = config.db_database
                    try:
                        result = await self._cleanup_single_database(env.job_id, config)
                        logger.info(f"[cleanup] {env.alias}/{db_name}: truncated {result.tables_truncated}")
                        return db_name, result
                    except Exception as e:
                        logger.warning(f"[cleanup] {env.alias}/{db_name}: failed: {e}")
                        return db_name, DatabaseCleanupResult(success=False, error=str(e))

                db_results = await asyncio.gather(*[cleanup_db(c) for c in configs])
                databases = dict(db_results)

            cache_cleared = False
            cache_clear_error = None
            try:
                await env.get_state_fn()
                cache_cleared = True
                logger.info(f"[cleanup] {env.alias}: mutation cache cleared")
            except Exception as e:
                cache_clear_error = str(e)
                logger.warning(f"[cleanup] {env.alias}: cache clear failed: {e}")

            return env.alias, EnvironmentCleanupResult(
                api_cleanup=api_cleanup,
                databases=databases,
                cache_cleared=cache_cleared,
                cache_clear_error=cache_clear_error,
            )

        results_list = await asyncio.gather(*[cleanup_env(env) for env in envs])
        return SessionCleanupResult(environments=dict(results_list))

    async def _cleanup_single_database(
        self,
        job_id: str,
        config: DbConfigResponse,
    ) -> DatabaseCleanupResult:
        """Connect to DB via sandbox Tunnel and truncate audit_log."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            local_port = s.getsockname()[1]

        tunnel = Tunnel(job_id=job_id, remote_port=config.db_port, local_port=local_port)
        try:
            tunnel.start()
            await asyncio.sleep(0.5)  # Let tunnel accept loop settle
            logger.info(f"[cleanup] Tunnel: localhost:{local_port} -> {job_id}:{config.db_port}/{config.db_database}")

            db_url = _make_db_url(config, local_port)
            engine = create_async_engine(db_url, pool_pre_ping=True, pool_size=2, max_overflow=2)
            try:
                async with engine.begin() as conn:
                    return DatabaseCleanupResult(
                        success=True,
                        tables_truncated=await self._find_and_truncate_audit_logs(conn, config.db_type),
                    )
            finally:
                await engine.dispose()
        finally:
            tunnel.stop()

    async def _find_and_truncate_audit_logs(
        self,
        conn: Any,
        db_type: str,
    ) -> list[str]:
        """Find audit_log tables and truncate them."""
        db_type = db_type.lower()
        truncated: list[str] = []

        if db_type == "postgresql":
            result = await conn.execute(
                text("SELECT schemaname, tablename FROM pg_tables WHERE tablename = 'audit_log'")
            )
            tables = result.fetchall()
            logger.info(f"[cleanup] PostgreSQL: found {len(tables)} audit_log table(s)")
            for schema, table in tables:
                await conn.execute(text(f"TRUNCATE TABLE {schema}.{table} RESTART IDENTITY CASCADE"))
                truncated.append(f"{schema}.{table}")

        elif db_type == "mysql":
            result = await conn.execute(
                text(
                    "SELECT table_schema, table_name FROM information_schema.tables "
                    "WHERE table_name = 'audit_log' AND table_schema = DATABASE()"
                )
            )
            tables = result.fetchall()
            logger.info(f"[cleanup] MySQL: found {len(tables)} audit_log table(s)")
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            for schema, table in tables:
                await conn.execute(text(f"TRUNCATE TABLE `{table}`"))
                truncated.append(table)
            await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        elif db_type == "sqlite":
            result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_log'"))
            if result.fetchone():
                await conn.execute(text("DELETE FROM audit_log"))
                truncated.append("audit_log")

        if not truncated:
            logger.warning(f"[cleanup] No audit_log tables found ({db_type})")

        return truncated
