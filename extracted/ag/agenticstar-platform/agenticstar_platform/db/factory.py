"""
AGENTICSTAR Platform SDK - PostgreSQL Manager Factory
実行モードに応じて適切なPostgreSQLManagerを作成
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Optional, Union

if TYPE_CHECKING:
    from .api_manager import ApiPostgreSQLManager
    from .config import PostgreSQLConfig
    from .manager import PostgreSQLManager

logger = logging.getLogger(__name__)


def create_postgresql_manager(
    config: "PostgreSQLConfig",
    *,
    token_provider: Optional[Callable[[], Optional[str]]] = None,
) -> Union["PostgreSQLManager", "ApiPostgreSQLManager"]:
    """
    PostgreSQLManagerを作成

    接続方式はconfigのapi_urlの有無で自動判定:
    - api_url設定あり → HTTP API経由（ApiPostgreSQLManager）
    - api_url設定なし → DB直結（PostgreSQLManager）

    Args:
        config: PostgreSQL設定
        token_provider: 認証トークン取得関数（api_url設定時は必須）

    Returns:
        PostgreSQLManager または ApiPostgreSQLManager インスタンス

    Raises:
        ValueError: api_url設定時に token_provider が未指定の場合
    """
    if config.api_url:
        if token_provider is None:
            raise ValueError(
                "token_provider is required when api_url is configured."
            )

        logger.info("Creating ApiPostgreSQLManager for HTTP API mode")
        from .api_manager import ApiPostgreSQLManager

        return ApiPostgreSQLManager(config, token_provider=token_provider)
    else:
        logger.info("Creating PostgreSQLManager for direct DB connection")
        from .manager import PostgreSQLManager

        return PostgreSQLManager(config)
