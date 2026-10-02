"""
AGENTICSTAR Platform SDK - API PostgreSQL Manager
API経由でデータベースアクセスを行うPostgreSQLManager実装（CLIモード用）
"""

from __future__ import annotations

import asyncio
import base64
import logging
import random
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID

import httpx

from .config import PostgreSQLConfig

logger = logging.getLogger(__name__)

# Connection-failure retry policy for transient cli-api routing issues
# (warm pool → adopt stale pool, K8s Service endpoint rolling update, conntrack expiry).
# 5 attempts with exponential backoff + jitter covers ~31s — long enough to ride out
# a typical kube-proxy / endpoint update window without leaving the user waiting too long
# on a genuinely down upstream.
_CONNECT_RETRY_MAX_ATTEMPTS = 5
_CONNECT_RETRY_BASE_SEC = 1.0  # 1, 2, 4, 8, 16 (± 20% jitter)


def _serialize_param(value: Any) -> Any:
    """
    SQLパラメータをJSONシリアライズ可能な形式に変換

    Args:
        value: 変換する値

    Returns:
        JSONシリアライズ可能な値
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, bytes):
        # base64エンコーディングでバイナリデータを安全にシリアライズ
        return {"__bytes__": base64.b64encode(value).decode("ascii")}
    if isinstance(value, (list, tuple)):
        return [_serialize_param(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize_param(v) for k, v in value.items()}
    return value


class ApiPostgreSQLManager:
    """
    API経由でDBにアクセスするPostgreSQLManager

    CLIモード用の実装。直接DB接続ではなく、APIプロキシを経由する。
    PostgreSQLManagerと同等のasyncインタフェースを提供。
    """

    def __init__(
        self,
        config: PostgreSQLConfig,
        *,
        token_provider: Callable[[], Optional[str]],
    ):
        """
        Args:
            config: PostgreSQL設定（api_url必須）
            token_provider: 認証トークンを取得する関数（必須、都度呼び出し）

        Raises:
            ValueError: api_url未設定時
        """
        self.config = config
        self._token_provider = token_provider

        # API URL取得・検証
        if config.api_url:
            self.api_url = config.api_url
        else:
            raise ValueError(
                "api_url not configured in PostgreSQLConfig."
            )

        logger.info(f"[ApiPostgreSQLManager] Using API proxy: {self.api_url}")

        # PERF (Tier 7-G1): httpx.AsyncClient を instance 単位で 1 回作成し、
        # execute_query 毎リクエストの new client 生成 (TLS handshake 50-100ms × N) を解消。
        # 旧: 毎リクエストで async with httpx.AsyncClient(...) → handshake 重複
        # 新: instance に 1 つ持って execute_query で再利用、close() で aclose
        self._http_client: Optional[httpx.AsyncClient] = None
        self._http_client_lock = asyncio.Lock()

    def _get_token(self) -> str:
        """トークンを取得（都度呼び出し、期限切れ対応）

        Raises:
            RuntimeError: トークン取得失敗時
        """
        token = self._token_provider()
        if not token:
            raise RuntimeError(
                "Failed to obtain authentication token. "
                "Please re-authenticate with 'agenticai auth login'."
            )
        return token

    def is_initialized(self) -> bool:
        """HTTP API経由のため常に初期化済み"""
        return True

    async def initialize(self) -> None:
        """初期化（HTTP APIモードでは不要）"""
        logger.debug("[ApiPostgreSQLManager] initialize: Skipping in HTTP API mode")

    async def close(self) -> None:
        """接続を閉じる. PERF (Tier 7-G1) 経由で持つ shared httpx client を aclose する."""
        if self._http_client is not None and not self._http_client.is_closed:
            try:
                await self._http_client.aclose()
            except Exception as e:
                logger.warning(f"[ApiPostgreSQLManager] http client close error: {e}")
        self._http_client = None
        logger.debug("[ApiPostgreSQLManager] close: shared http client closed")

    async def _get_http_client(self, timeout: httpx.Timeout) -> httpx.AsyncClient:
        """instance 単位の shared httpx.AsyncClient を返す (lazy + double-checked locking)."""
        if self._http_client is not None and not self._http_client.is_closed:
            return self._http_client
        async with self._http_client_lock:
            if self._http_client is None or self._http_client.is_closed:
                self._http_client = httpx.AsyncClient(timeout=timeout)
            return self._http_client

    async def execute_query(
        self, query: str, params: tuple = ()
    ) -> Dict[str, Any]:
        """
        API経由でクエリを実行

        Args:
            query: 実行するSQLクエリ
            params: クエリパラメータ

        Returns:
            Dict with keys: success, data, error (optional), error_code (optional)
        """
        return await self._api_request("execute", query, params)

    async def fetch_one(
        self, query: str, params: tuple = ()
    ) -> Optional[Dict[str, Any]]:
        """
        API経由で単一行を取得

        Args:
            query: 実行するSQLクエリ
            params: クエリパラメータ

        Returns:
            Dict (結果がある場合) or None
        """
        result = await self._api_request("fetch_one", query, params)
        if result.get("success") and result.get("data"):
            return result["data"]
        return None

    async def fetch_all(
        self, query: str, params: tuple = ()
    ) -> List[Dict[str, Any]]:
        """
        API経由で全行を取得

        Args:
            query: 実行するSQLクエリ
            params: クエリパラメータ

        Returns:
            List[Dict]: クエリ結果のリスト
        """
        result = await self._api_request("fetch_all", query, params)
        if result.get("success") and result.get("data"):
            return result["data"]
        return []

    async def _api_request(
        self,
        operation: str,
        query: str,
        params: tuple,
    ) -> Dict[str, Any]:
        """API共通リクエスト処理。

        TCP 接続確立失敗 (httpx.ConnectError) のみ retry する。
        ConnectError は SYN が通らなかった = サーバ側に request が届いていない
        ことが保証されるので、INSERT/UPDATE 等の non-idempotent な query でも
        retry 安全。

        ReadError / WriteError は request が既に流れた後の失敗で、サーバ側に
        部分的に処理されている可能性があるため retry しない (二重書込防止)。
        """
        try:
            token = self._get_token()
        except RuntimeError as e:
            logger.error(f"[ApiPostgreSQLManager] Token error: {e}")
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "error_code": "AUTH_ERROR",
            }

        headers = {"Authorization": f"Bearer {token}"}
        serialized_params = [_serialize_param(p) for p in params]
        timeout = httpx.Timeout(30.0, connect=10.0)

        # PERF (Tier 7-G1): shared httpx client を再利用 (毎リクエスト new 解消)
        client = await self._get_http_client(timeout)

        last_connect_error: Optional[httpx.ConnectError] = None
        for attempt in range(1, _CONNECT_RETRY_MAX_ATTEMPTS + 1):
            try:
                if True:  # 元 async with の body をそのまま保持
                    response = await client.post(
                        f"{self.api_url}/{operation}",
                        json={"query": query, "params": serialized_params},
                        headers=headers,
                    )

                    if response.status_code == 401:
                        logger.warning("[ApiPostgreSQLManager] Authentication failed (401)")
                        return {
                            "success": False,
                            "data": None,
                            "error": "Authentication failed. Please re-authenticate.",
                            "error_code": "UNAUTHORIZED",
                        }

                    if response.status_code >= 400:
                        error_text = response.text
                        logger.error(
                            f"[ApiPostgreSQLManager] API error: {response.status_code}"
                        )
                        return {
                            "success": False,
                            "data": None,
                            "error": f"API error: {response.status_code} - {error_text}",
                            "error_code": "API_ERROR",
                        }

                    return response.json()

            except httpx.ConnectError as e:
                # TCP 接続未確立 — request は送信されていないので retry 安全
                last_connect_error = e
                if attempt >= _CONNECT_RETRY_MAX_ATTEMPTS:
                    break
                base = _CONNECT_RETRY_BASE_SEC * (2 ** (attempt - 1))
                jitter = base * 0.2 * (random.random() * 2 - 1)
                wait_sec = max(0.1, base + jitter)
                logger.warning(
                    f"[ApiPostgreSQLManager] ConnectError "
                    f"(attempt {attempt}/{_CONNECT_RETRY_MAX_ATTEMPTS}), "
                    f"retrying in {wait_sec:.1f}s. err={str(e)[:120]}"
                )
                await asyncio.sleep(wait_sec)
                continue

            except httpx.TimeoutException as e:
                # connect timeout は ConnectError 同等扱いで retry したいが、
                # read/write timeout は request が流れた後の可能性があるので一律 retry しない。
                # httpx は ConnectTimeout を ConnectError とは別系統で投げるため判別する。
                if isinstance(e, httpx.ConnectTimeout):
                    last_connect_error = e  # type: ignore[assignment]
                    if attempt >= _CONNECT_RETRY_MAX_ATTEMPTS:
                        break
                    base = _CONNECT_RETRY_BASE_SEC * (2 ** (attempt - 1))
                    jitter = base * 0.2 * (random.random() * 2 - 1)
                    wait_sec = max(0.1, base + jitter)
                    logger.warning(
                        f"[ApiPostgreSQLManager] ConnectTimeout "
                        f"(attempt {attempt}/{_CONNECT_RETRY_MAX_ATTEMPTS}), "
                        f"retrying in {wait_sec:.1f}s"
                    )
                    await asyncio.sleep(wait_sec)
                    continue
                logger.error("[ApiPostgreSQLManager] Request timeout (non-connect)")
                return {
                    "success": False,
                    "data": None,
                    "error": "API request timeout",
                    "error_code": "TIMEOUT",
                }

            except Exception as e:
                logger.error(f"[ApiPostgreSQLManager] Request failed: {e}")
                return {
                    "success": False,
                    "data": None,
                    "error": f"Failed to execute query via API: {str(e)}",
                    "error_code": "REQUEST_ERROR",
                }

        # retry 全て失敗。caller に返す message は内部情報を漏らさないよう短く trim。
        # 詳細 (URL 等が str() に含まれる場合に備えて) は logger.error のみ。
        err_summary = f"{type(last_connect_error).__name__}: {str(last_connect_error)[:120]}"
        logger.error(
            f"[ApiPostgreSQLManager] All {_CONNECT_RETRY_MAX_ATTEMPTS} connect attempts failed: "
            f"{last_connect_error}"
        )
        return {
            "success": False,
            "data": None,
            "error": f"Connection failed after {_CONNECT_RETRY_MAX_ATTEMPTS} attempts: {err_summary}",
            "error_code": "CONNECTION_ERROR",
        }
