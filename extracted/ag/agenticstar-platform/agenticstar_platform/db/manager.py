"""
AGENTICSTAR Platform SDK - PostgreSQL Database Manager
Azure AD認証対応のPostgreSQL接続とクエリ実行
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional, Union

import asyncpg
from azure.identity import ClientSecretCredential

from .config import PostgreSQLConfig

# Azure AD認証の詳細ログを抑制
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)
logging.getLogger("azure.identity._internal.get_token_mixin").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def _sanitize_text_params(params):
    """Strip NUL characters (\\x00) from string values in query params.

    PostgreSQL text/varchar columns reject \\x00 with UntranslatableCharacterError.
    NUL has no semantic meaning in text fields, so removal is safe and lossless.
    Recursively walks list/tuple/dict; bytes pass through unchanged (bytea allows \\x00).
    """
    if not params:
        return params

    stripped_count = 0

    def clean(v):
        nonlocal stripped_count
        if isinstance(v, str):
            if "\x00" in v:
                stripped_count += v.count("\x00")
                return v.replace("\x00", "")
            return v
        if isinstance(v, list):
            return [clean(x) for x in v]
        if isinstance(v, tuple):
            return tuple(clean(x) for x in v)
        if isinstance(v, dict):
            return {k: clean(val) for k, val in v.items()}
        return v

    cleaned = tuple(clean(p) for p in params)
    if stripped_count:
        logger.warning(
            "Stripped %d NUL character(s) from query params before asyncpg call",
            stripped_count,
        )
    return cleaned


def _is_multi_command_error(exc: BaseException) -> bool:
    """PostgreSQL が複数文の prepare を拒否した（SQLSTATE 42601）エラーかを判定する。

    メッセージは "cannot insert multiple commands into a prepared statement"。
    """
    return "multiple commands" in str(exc)


def _legacy_dispatch_used_fetch(query: str) -> bool:
    """0.5.40 以前のテキスト判定で conn.fetch() 側に振られていたクエリか。

    複数文フォールバックの互換範囲を「旧実装で simple protocol に流れていた
    クエリ」に限定するためだけに使う（結果セット判定には使わない）。
    """
    normalized = query.strip().upper()
    return normalized.startswith("SELECT") or "RETURNING" in normalized


def _looks_row_producing(query: str) -> bool:
    """複数文フォールバック時の警告用ヒューリスティック（dispatch には使わない）。"""
    upper = query.upper()
    return any(k in upper for k in ("SELECT", "RETURNING", "VALUES", "SHOW", "EXPLAIN"))


class PostgreSQLManager:
    """PostgreSQL接続とクエリ実行クラス

    Azure AD認証またはユーザー名/パスワード認証でPostgreSQLに接続し、
    クエリを実行します。接続プールを使用して効率的に接続を管理します。

    Features:
        - Azure AD認証対応（トークン自動更新）
        - 標準認証（ユーザー名/パスワード）対応
        - 接続プール管理
        - 非同期コンテキストマネージャー対応
        - SQL Injection防止（パラメータ化クエリ）

    Example:
        >>> from agenticstar_platform import PostgreSQLManager, PostgreSQLConfig
        >>>
        >>> # 設定を作成
        >>> config = PostgreSQLConfig.from_toml("config.toml")
        >>>
        >>> # コンテキストマネージャーで使用（推奨）
        >>> async with PostgreSQLManager(config) as db:
        ...     # SELECT実行
        ...     result = await db.fetch_all("SELECT * FROM users WHERE status = $1", ("active",))
        ...     print(f"Active users: {len(result)}")
        ...
        ...     # INSERT実行
        ...     await db.execute(
        ...         "INSERT INTO logs (message) VALUES ($1)",
        ...         ("Operation completed",)
        ...     )
        >>>
        >>> # 明示的な初期化・クローズ
        >>> db = PostgreSQLManager(config)
        >>> await db.initialize()
        >>> try:
        ...     result = await db.fetch_one("SELECT COUNT(*) as cnt FROM users")
        ...     print(f"Total users: {result['cnt']}")
        ... finally:
        ...     await db.close()
    """

    def __init__(self, config: PostgreSQLConfig):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[float] = None
        self._token_refresh_lock: Optional[asyncio.Lock] = None

    async def __aenter__(self) -> "PostgreSQLManager":
        """Context Manager: 開始時に接続プールを初期化"""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager: 終了時に接続プールをクローズ"""
        await self.close()

    async def _get_azure_ad_token(self) -> str:
        """Azure AD認証でアクセストークンを取得"""
        logger.info("[IN] _get_azure_ad_token: Getting Azure AD token")

        if not self.config.azure_ad:
            logger.error("[ERROR] _get_azure_ad_token: Azure AD configuration is required")
            raise ValueError("Azure AD configuration is required")

        # トークンの有効期限をチェック（5分前に更新）
        if (
            self._access_token
            and self._token_expiry
            and time.time() < self._token_expiry - 300
        ):
            logger.info("[OUT] _get_azure_ad_token: Using cached token")
            return self._access_token

        # トークン取得中の同期処理（複数API同時実行時の重複取得防止）
        # Note: Lockはinitialize()で作成済み（イベントループ紐付けを保証）
        async with self._token_refresh_lock:
            # ロック取得後に再チェック（他のAPIコールが既に更新した可能性）
            if (
                self._access_token
                and self._token_expiry
                and time.time() < self._token_expiry - 300
            ):
                return self._access_token

            try:
                credential = ClientSecretCredential(
                    tenant_id=self.config.azure_ad.tenant_id,
                    client_id=self.config.azure_ad.client_id,
                    client_secret=self.config.azure_ad.client_secret,
                )

                # Try different scopes for Azure PostgreSQL Flexible Server
                scopes_to_try = [
                    "https://ossrdbms-aad.database.windows.net/.default",
                    "https://database.windows.net/.default",
                    "https://management.azure.com/.default",
                ]

                token = None
                last_error = None

                for scope in scopes_to_try:
                    try:
                        token = await asyncio.to_thread(credential.get_token, scope)
                        break
                    except Exception as e:
                        last_error = e
                        continue

                if not token:
                    raise last_error or Exception("All token scopes failed")

                self._access_token = token.token
                self._token_expiry = token.expires_on

                logger.info("[OUT] _get_azure_ad_token: Azure AD token acquired successfully")
                return self._access_token

            except Exception as e:
                logger.error(
                    "[ERROR] _get_azure_ad_token: Failed to acquire Azure AD token - error_type=%s",
                    type(e).__name__,
                )
                raise

    async def _create_connection_params(self) -> Dict[str, Any]:
        """接続パラメータを作成"""
        logger.info("[IN] _create_connection_params: Creating database connection parameters")
        params = {
            "host": self.config.host,
            "port": self.config.port,
            "database": self.config.database,
            "command_timeout": self.config.command_timeout,
        }

        # SSL設定（disable以外は設定する）
        ssl_mode = getattr(self.config, 'ssl_mode', 'require')
        if ssl_mode != "disable":
            params["ssl"] = ssl_mode

        if self.config.use_azure_ad:
            token = await self._get_azure_ad_token()

            # Use configured username if available, otherwise fallback to client_id
            if self.config.azure_ad and self.config.azure_ad.username:
                username = self.config.azure_ad.username
            elif self.config.azure_ad:
                username = self.config.azure_ad.client_id
            else:
                raise ValueError("Azure AD configuration is required when use_azure_ad is True")

            params.update(
                {
                    "user": username,
                    "password": token,
                }
            )
        else:
            # 標準認証の場合（ユーザー名/パスワード）
            if not self.config.username or not self.config.password:
                raise ValueError("Username and password are required when use_azure_ad is False")

            params.update(
                {
                    "user": self.config.username,
                    "password": self.config.password,
                }
            )

        logger.info("[OUT] _create_connection_params: Connection parameters created successfully")
        return params

    def is_initialized(self) -> bool:
        """接続プールが初期化されているか確認"""
        return self.pool is not None

    async def _ensure_initialized(self) -> None:
        """接続プールが初期化されていることを保証"""
        if not self.pool:
            await self.initialize()

    async def initialize(self) -> None:
        """データベース接続プールを初期化"""
        logger.info("[IN] initialize: Initializing PostgreSQL connection pool")
        try:
            # トークンリフレッシュ用のLockを作成（イベントループ内で作成することで紐付けを保証）
            if self._token_refresh_lock is None:
                self._token_refresh_lock = asyncio.Lock()

            logger.info("[IN] initialize.create_connection_params: Creating connection parameters")
            connection_params = await self._create_connection_params()
            logger.info("[OUT] initialize.create_connection_params: Connection parameters created")

            logger.info(
                "[IN] initialize.create_pool: Creating connection pool - min_size=%s, max_size=%s",
                self.config.pool_min_size,
                self.config.pool_max_size,
            )
            self.pool = await asyncpg.create_pool(
                min_size=self.config.pool_min_size,
                max_size=self.config.pool_max_size,
                statement_cache_size=0,
                **connection_params,
            )
            logger.info("[OUT] initialize.create_pool: Connection pool created successfully")
            logger.info("[OUT] initialize: PostgreSQL connection pool initialized successfully")

        except Exception as e:
            logger.error(
                "[ERROR] initialize: PostgreSQL initialization failed - error_type=%s, error=%s",
                type(e).__name__,
                str(e),
            )
            raise

    async def close(self) -> None:
        """接続プールを閉じる

        Note:
            例外が発生してもリソースを確実にクリーンアップします。
        """
        logger.info("[IN] close: Closing PostgreSQL connection pool")
        try:
            if self.pool:
                await self.pool.close()
                logger.info("[OUT] close: PostgreSQL connection pool closed successfully")
            else:
                logger.info("[OUT] close: No connection pool to close")
        except Exception as e:
            logger.warning(f"Error closing PostgreSQL connection pool: {e}")
        finally:
            self.pool = None
            self._access_token = None
            self._token_expiry = None

    async def execute_query(
        self, query: str, params: tuple = ()
    ) -> Dict[str, Any]:
        """
        汎用クエリ実行メソッド

        SELECT/INSERT/UPDATE/DELETE等のSQLクエリを実行し、
        結果を統一フォーマットで返します。

        Args:
            query: 実行するSQLクエリ。プレースホルダーは $1, $2 形式
            params: クエリパラメータ（タプル）

        Returns:
            Dict[str, Any]: 実行結果
                - success: bool - 実行成功/失敗
                - data: 文が結果セットを返す場合は List[Dict]、返さない場合は
                  ``{"result": <status>}``（例 ``{"result": "INSERT 0 1"}``）
                - error: Optional[str] - エラーメッセージ（失敗時のみ）
                - error_code: Optional[str] - エラーコード（失敗時のみ）

        Note:
            結果セットの有無はクエリ文字列の先頭語ではなく、PostgreSQL が
            prepared statement の Describe で返す行記述（``get_attributes()``）で
            判定します。``SELECT`` 以外でも ``WITH ... SELECT`` / ``VALUES`` /
            ``TABLE`` / ``SHOW`` / ``EXPLAIN`` / ``... RETURNING`` は List[Dict] に
            なります。逆に結果セットを持たない文（``WITH ... INSERT`` など
            RETURNING 無しの data-modifying CTE を含む）は status dict です。
            ``;`` 区切りの複数文は、旧実装で通っていた経路（パラメータ無し・
            先頭が ``SELECT`` でなく ``RETURNING`` を含まない）のみ simple
            protocol で実行され、status dict（最後の文のもの）を返します。
            それ以外の複数文は失敗（``DB_QUERY_ERROR``）です。
            0 列の結果セット（``SELECT FROM t``）は行があれば ``[{}, ...]``、
            0 行なら結果セットと区別できず ``{"result": "SELECT 0"}`` になります
            （既知のエッジ。列を 1 つ以上返すよう書けば通常の ``[]`` です）。

        Example:
            >>> # SELECTクエリ
            >>> result = await db.execute_query(
            ...     "SELECT * FROM users WHERE created_at > $1",
            ...     (datetime(2024, 1, 1),)
            ... )
            >>> if result["success"]:
            ...     for user in result["data"]:
            ...         print(user["name"])
            >>>
            >>> # INSERT with RETURNING
            >>> result = await db.execute_query(
            ...     "INSERT INTO users (name) VALUES ($1) RETURNING id",
            ...     ("John",)
            ... )
            >>> if result["success"]:
            ...     new_id = result["data"][0]["id"]
        """
        logger.debug(
            "[IN] execute_query: Executing SQL query - query_type=%s, params_count=%s",
            (query.strip().upper().split()[0] if query.strip() else "EMPTY"),
            len(params),
        )
        try:
            await self._ensure_initialized()
            params = _sanitize_text_params(params)

            async with self.pool.acquire() as conn:
                # 結果セットの有無はテキスト判定（先頭 "SELECT" / "RETURNING" 含有）
                # ではなくサーバの Describe 結果で決める。テキスト判定では
                # WITH ... SELECT / VALUES / TABLE などの行が conn.execute() 側へ
                # 流れて黙って捨てられていた（agentcore#330）。
                #
                # - name="": 無名 prepared statement を使う。asyncpg 0.29/0.30 は
                #   statement_cache_size=0 でも prepare() 既定で名前付き statement を
                #   作るため、PgBouncer transaction pooling 下で backend が変わると
                #   壊れる。無名なら従来の conn.fetch() と同じ経路になる。
                # - timeout: prepare と fetch で command_timeout を分けて二重に
                #   消費しないよう、従来どおり 1 クエリ分の予算を共有する。
                budget = self.config.command_timeout or None
                started = time.monotonic()
                try:
                    stmt = await conn.prepare(query, name="", timeout=budget)
                except asyncpg.PostgresSyntaxError as e:
                    # "a; b" 形式の複数文は prepared statement 化できない。
                    # 旧実装で simple protocol（conn.execute(query)）に流れていた
                    # 経路 = パラメータ無し かつ 先頭が SELECT でなく RETURNING も
                    # 含まない、に限って従来どおり通す。それ以外の複数文は従来も
                    # 同じエラーで失敗していたので、そのまま失敗させる（行を返す
                    # 文を含む batch を黙って通さない）。
                    if (
                        params
                        or not _is_multi_command_error(e)
                        or _legacy_dispatch_used_fetch(query)
                    ):
                        raise
                    if _looks_row_producing(query):
                        logger.warning(
                            "execute_query: multi-statement query contains a row-producing "
                            "statement but rows are not returned via simple protocol; "
                            "split it into single statements to receive rows"
                        )
                    result = await conn.execute(query)
                    logger.debug(
                        "[OUT] execute_query: Multi-statement query executed via simple protocol"
                    )
                    return {"success": True, "data": {"result": result}}

                remaining = None
                if budget is not None:
                    remaining = budget - (time.monotonic() - started)
                    if remaining <= 0:
                        raise TimeoutError(
                            f"execute_query: command_timeout ({budget}s) exhausted during prepare"
                        )
                rows = await stmt.fetch(*params, timeout=remaining)
                # 列記述があれば結果セット。列が 0 個でも行が返っていれば結果セット
                # （SELECT FROM t のような 0 列 SELECT は attributes が空になる）。
                if stmt.get_attributes() or rows:
                    # 文が結果セットを持つ（SELECT/WITH/VALUES/TABLE/SHOW/EXPLAIN/RETURNING 等）
                    result_data = [dict(row) for row in rows]
                    logger.debug(
                        "[OUT] execute_query: Query executed successfully - result_count=%s",
                        len(result_data),
                    )
                    return {"success": True, "data": result_data}

                # 結果セットを持たない文（INSERT/UPDATE/DELETE/DDL 等）は status 文字列
                logger.debug("[OUT] execute_query: Query executed successfully")
                return {"success": True, "data": {"result": stmt.get_statusmsg()}}

        except Exception as e:
            logger.error(
                "[ERROR] execute_query: Query execution failed - error_type=%s, error=%s",
                type(e).__name__,
                str(e),
            )
            return {
                "success": False,
                "data": None,
                "error": f"Database query error: {str(e)}",
                "error_code": "DB_QUERY_ERROR",
            }

    async def fetch_one(
        self, query: str, params: tuple = ()
    ) -> Optional[Dict[str, Any]]:
        """
        単一行を取得

        1行だけ返すことが期待されるクエリに使用します。
        結果が複数行ある場合でも最初の1行のみ返します。

        Args:
            query: 実行するSQLクエリ。プレースホルダーは $1, $2 形式
            params: クエリパラメータ（タプル）

        Returns:
            Optional[Dict[str, Any]]: 結果行（辞書形式）、結果がない場合はNone

        Example:
            >>> # ユーザーを1件取得
            >>> user = await db.fetch_one(
            ...     "SELECT * FROM users WHERE id = $1",
            ...     (user_id,)
            ... )
            >>> if user:
            ...     print(f"Found: {user['name']}")
            ... else:
            ...     print("User not found")
            >>>
            >>> # 集計結果を取得
            >>> count = await db.fetch_one("SELECT COUNT(*) as total FROM users")
            >>> print(f"Total: {count['total']}")
        """
        await self._ensure_initialized()
        params = _sanitize_text_params(params)
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *params)
            return dict(row) if row else None

    async def fetch_all(
        self, query: str, params: tuple = ()
    ) -> List[Dict[str, Any]]:
        """
        全行を取得

        複数行を返すSELECTクエリに使用します。
        結果がない場合は空のリストを返します。

        Args:
            query: 実行するSQLクエリ。プレースホルダーは $1, $2 形式
            params: クエリパラメータ（タプル）

        Returns:
            List[Dict[str, Any]]: 結果行のリスト（各行は辞書形式）

        Example:
            >>> # 全ユーザーを取得
            >>> users = await db.fetch_all("SELECT * FROM users ORDER BY created_at DESC")
            >>> for user in users:
            ...     print(f"{user['id']}: {user['name']}")
            >>>
            >>> # 条件付きで取得
            >>> active_users = await db.fetch_all(
            ...     "SELECT * FROM users WHERE status = $1 AND role = $2",
            ...     ("active", "admin")
            ... )
            >>> print(f"Found {len(active_users)} admin users")
        """
        await self._ensure_initialized()
        params = _sanitize_text_params(params)
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(row) for row in rows]

    async def execute(self, query: str, params: tuple = ()) -> str:
        """
        実行のみ（結果を返さないクエリ用）

        INSERT/UPDATE/DELETE等の結果データが不要なクエリに使用します。
        DDL文（CREATE TABLE等）の実行にも使用できます。

        Args:
            query: 実行するSQLクエリ。プレースホルダーは $1, $2 形式
            params: クエリパラメータ（タプル）

        Returns:
            str: 実行結果のステータス（例: "INSERT 0 1", "UPDATE 5", "DELETE 3"）

        Example:
            >>> # データ挿入
            >>> result = await db.execute(
            ...     "INSERT INTO logs (level, message) VALUES ($1, $2)",
            ...     ("INFO", "Operation completed")
            ... )
            >>> print(result)  # "INSERT 0 1"
            >>>
            >>> # データ更新
            >>> result = await db.execute(
            ...     "UPDATE users SET status = $1 WHERE last_login < $2",
            ...     ("inactive", datetime(2024, 1, 1))
            ... )
            >>> print(result)  # "UPDATE 15"
            >>>
            >>> # データ削除
            >>> result = await db.execute(
            ...     "DELETE FROM sessions WHERE expired_at < $1",
            ...     (datetime.now(),)
            ... )
            >>> print(result)  # "DELETE 100"
        """
        await self._ensure_initialized()
        params = _sanitize_text_params(params)
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *params)
