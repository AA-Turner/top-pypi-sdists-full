"""
AGENTICSTAR Platform SDK - API PostgreSQL Manager
API経由でデータベースアクセスを行うPostgreSQLManager実装（CLIモード用）
"""

from __future__ import annotations

import asyncio
import email.utils
import logging
import math
import random
import re
import time
from typing import Any, Callable, Dict, List, Mapping, Optional

import httpx

from .config import PostgreSQLConfig
from .wire_types import param_type_hint, serialize_param

# 3.0.14 までこのモジュールにあった名前。wire の片割れとして wire_types へ移した (本体は同じ)
_serialize_param = serialize_param

logger = logging.getLogger(__name__)

# Connection-failure retry policy for transient cli-api routing issues
# (warm pool → adopt stale pool, K8s Service endpoint rolling update, conntrack expiry).
# 5 attempts with exponential backoff + jitter covers ~31s — long enough to ride out
# a typical kube-proxy / endpoint update window without leaving the user waiting too long
# on a genuinely down upstream.
_CONNECT_RETRY_MAX_ATTEMPTS = 5
_CONNECT_RETRY_BASE_SEC = 1.0  # waits 1, 2, 4, 8 s (± 20% jitter) between the 5 attempts

# 3.1.0: the proxy (cli-api) answers 503 *before* the request is processed while a replica is being recycled and
# when it cannot check the calling Pod yet, so resending those is safe. Only these exact JSON `detail` values are
# resent (a 503 from anything else on the way, which may come after the query ran, is not), within the same attempt
# budget, waiting at least Retry-After (capped). Any other 503 / 5xx is returned as before.
_RESENDABLE_503_DETAILS = frozenset({
    "cli-api is draining for memory recycle, retry on another replica",  # memory guard (src/api/memory_guard.py)
    "caller binding unavailable (retryable)",  # caller binding (src/api/caller_binding.py)
})
_DRAIN_RETRY_AFTER_CAP_SEC = 10.0

# 3.1.0: idle connections are dropped after 4 s. The proxy (uvicorn) closes idle keep-alive connections after
# 5 s; reusing one at that moment fails with "Server disconnected without sending a response" after the request
# was sent, which cannot be retried safely. The pool sizes are httpx's defaults, stated because passing
# `httpx.Limits(...)` replaces them (an explicit Limits without them would mean "no limit").
_HTTP_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20, keepalive_expiry=4.0)

# 3.1.0 headers_provider: a header name must be an RFC 9110 token and a value visible ASCII (inner spaces allowed,
# no leading / trailing space), so h11 / httpx can always send it. Headers the client itself owns cannot be set.
# fullmatch で使う (`$` は末尾の改行を許すので使わない)
_HEADER_NAME_RE = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
_HEADER_VALUE_RE = re.compile(r"[\x21-\x7e](?:[\x20-\x7e]*[\x21-\x7e])?")
_RESERVED_HEADERS = frozenset({"authorization", "host", "content-length", "content-type", "transfer-encoding",
                               "connection", "te", "upgrade", "trailer", "expect"})


def _backoff_sec(attempt: int) -> float:
    base = _CONNECT_RETRY_BASE_SEC * (2 ** (attempt - 1))
    jitter = base * 0.2 * (random.random() * 2 - 1)
    return max(0.1, base + jitter)


def _retry_after_sec(value: Optional[str]) -> float:
    """Retry-After (delta-seconds or HTTP-date) → seconds, 0 when missing or unusable."""
    if not value:
        return 0.0
    try:
        sec = float(value)
    except ValueError:
        try:
            sec = email.utils.parsedate_to_datetime(value).timestamp() - time.time()
        except (TypeError, ValueError, IndexError, OverflowError):
            return 0.0
    return sec if math.isfinite(sec) and sec > 0 else 0.0


def _drain_wait_sec(response: httpx.Response) -> Optional[float]:
    """Seconds to wait before resending if this is one of the proxy's resendable 503 answers, else None."""
    if response.status_code != 503:
        return None
    try:
        body = response.json()
    except Exception:  # noqa: BLE001 - a non-JSON body is not the proxy's answer
        return None
    detail = body.get("detail") if isinstance(body, dict) else None
    if not isinstance(detail, str) or detail not in _RESENDABLE_503_DETAILS:
        return None
    return min(_retry_after_sec(response.headers.get("retry-after")), _DRAIN_RETRY_AFTER_CAP_SEC)




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
        headers_provider: Optional[Callable[[], Optional[Mapping[str, str]]]] = None,
    ):
        """
        Args:
            config: PostgreSQL設定（api_url必須）
            token_provider: 認証トークンを取得する関数（必須、都度呼び出し）
            headers_provider: 3.1.0. 要求ごとに足すヘッダ (mapping) を返す関数（任意、都度呼び出し）。呼び出し元を
                識別するヘッダ (例: 実行の ID) を proxy に渡す用途。送れるものだけ足す (名前は token、値は前後に空白の
                無い可視 ASCII)。Authorization・Host 等 client が持つヘッダは上書きできない。例外は「足さない」

        Raises:
            ValueError: api_url未設定時
        """
        self.config = config
        self._token_provider = token_provider
        self._headers_provider = headers_provider

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
                self._http_client = httpx.AsyncClient(timeout=timeout, limits=_HTTP_LIMITS)
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

    def _extra_headers(self) -> Dict[str, str]:
        """headers_provider の値のうち送れるものだけ (名前は token、値は前後に空白の無い可視 ASCII。Authorization・
        Host・Content-Type 等 client が持つヘッダは除く)。送れない値と provider の失敗は「足さない」。"""
        if self._headers_provider is None:
            return {}
        try:
            extra = self._headers_provider() or {}
            out: Dict[str, str] = {}
            for k, v in dict(extra).items():
                if not isinstance(k, str) or not _HEADER_NAME_RE.fullmatch(k) or k.lower() in _RESERVED_HEADERS:
                    continue
                if v is None or not isinstance(v, (str, int)) or isinstance(v, bool):
                    continue
                value = str(v)
                if _HEADER_VALUE_RE.fullmatch(value):
                    out[k] = value
            return out
        except Exception as e:  # noqa: BLE001 - extra headers must never fail the query
            logger.debug(f"[ApiPostgreSQLManager] headers_provider failed: {type(e).__name__}")
            return {}

    async def _api_request(
        self,
        operation: str,
        query: str,
        params: tuple,
    ) -> Dict[str, Any]:
        """API共通リクエスト処理。

        TCP 接続確立失敗 (httpx.ConnectError) と、proxy が処理の前に返す退避の 503 (本文 `draining`、3.1.0)
        だけ retry する。ConnectError は SYN が通らなかった = サーバ側に request が届いていない
        ことが保証されるので、INSERT/UPDATE 等の non-idempotent な query でも
        retry 安全。退避の 503 も処理の前に返るので同じ。

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

        headers = {**self._extra_headers(), "Authorization": f"Bearer {token}"}
        params = tuple(params)  # 1 回で確定する (iterator を 2 度なぞって params と param_types がずれないように)
        serialized_params = [_serialize_param(p) for p in params]
        # 3.0.15: どの文字列が date / datetime 由来かを params と同じ並びで添える (wire_types 参照)
        param_types = [param_type_hint(p) for p in params]
        timeout = httpx.Timeout(30.0, connect=10.0)

        # PERF (Tier 7-G1): shared httpx client を再利用 (毎リクエスト new 解消)
        client = await self._get_http_client(timeout)

        last_connect_error: Optional[httpx.ConnectError] = None
        for attempt in range(1, _CONNECT_RETRY_MAX_ATTEMPTS + 1):
            try:
                if True:  # 元 async with の body をそのまま保持
                    response = await client.post(
                        f"{self.api_url}/{operation}",
                        json={
                            "query": query,
                            "params": serialized_params,
                            "param_types": param_types,
                        },
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

                    drain_wait = _drain_wait_sec(response)
                    if drain_wait is not None and attempt < _CONNECT_RETRY_MAX_ATTEMPTS:
                        # 処理の前に返る退避の 503。別の replica に届くよう待って送り直す (最後の試行では下の
                        # 4xx/5xx の扱いで今までどおり API_ERROR を返す)
                        wait_sec = max(drain_wait, _backoff_sec(attempt))
                        logger.warning(
                            f"[ApiPostgreSQLManager] proxy is draining (503) "
                            f"(attempt {attempt}/{_CONNECT_RETRY_MAX_ATTEMPTS}), retrying in {wait_sec:.1f}s"
                        )
                        await asyncio.sleep(wait_sec)
                        continue

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
                wait_sec = _backoff_sec(attempt)
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
                    wait_sec = _backoff_sec(attempt)
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
