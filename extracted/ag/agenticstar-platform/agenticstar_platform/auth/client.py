"""
AGENTICSTAR Platform SDK - AgenticStar Auth Client
AgenticStar Auth API統合クライアント

機能:
- ユーザー一覧取得
- ユーザー詳細取得
- MCP OAuth トークン取得

Example:
    ```python
    from agenticstar_platform.auth import AgenticStarAuthClient, AgenticStarAuthConfig

    config = AgenticStarAuthConfig.create(
        base_url="https://auth.example.com",
        api_key="your-api-key",
    )

    async with AgenticStarAuthClient(config) as client:
        # ユーザー一覧取得
        result = await client.get_users(page=1, limit=20)

        # ユーザー詳細取得
        result = await client.get_user("user-id-123")

        # MCPトークン取得
        result = await client.get_mcp_tokens("user-id-123", ["github", "slack"])
    ```
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx

from .config import AgenticStarAuthConfig
from .exceptions import (
    AuthAPIError,
    AuthConfigError,
    AuthNotFoundError,
    AuthRateLimitError,
    AuthUnauthorizedError,
)
from .models import (
    ApiUser,
    DeviceInfo,
    GetMCPTokensResult,
    GetUserResult,
    GetUsersResult,
    LoginHistoryEntry,
    MCPTokenError,
    MCPTokenInfo,
    OAuthProviderName,
    UserPagination,
)

logger = logging.getLogger(__name__)


class AgenticStarAuthClient:
    """
    AgenticStar Auth API クライアント

    認証API（ユーザー管理、MCP OAuthトークン）へのアクセスを提供。
    X-Internal-API-Key認証を使用します。

    Attributes:
        config: AgenticStarAuthConfig設定

    Example:
        ```python
        config = AgenticStarAuthConfig.create(
            base_url="https://auth.example.com",
            api_key="xxx",
        )
        async with AgenticStarAuthClient(config) as client:
            users = await client.get_users()
        ```
    """

    def __init__(self, config: AgenticStarAuthConfig):
        """
        AgenticStar Auth Clientを初期化

        Args:
            config: AgenticStarAuthConfig インスタンス

        Raises:
            AuthConfigError: 設定が不正な場合
        """
        if not config.base_url:
            raise AuthConfigError("base_url is required")

        if not config.api_key and not config.token_provider:
            raise AuthConfigError("api_key or token_provider is required")

        self._config = config
        self._http_client: Optional[httpx.AsyncClient] = None

        auth_mode = "token_provider" if config.token_provider else config.auth_type
        logger.info(
            f"AgenticStarAuthClient initialized - base_url={config.base_url[:30]}..., auth_mode={auth_mode}"
        )

    async def __aenter__(self) -> "AgenticStarAuthClient":
        """Context Manager: 開始時の処理"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context Manager: 終了時にリソースをクローズ"""
        await self.close()

    def _get_http_client(self) -> httpx.AsyncClient:
        """HTTP clientを取得（遅延初期化）"""
        if self._http_client is None or self._http_client.is_closed:
            self._http_client = httpx.AsyncClient(timeout=self._config.timeout)
        return self._http_client

    def _get_headers(self) -> Dict[str, str]:
        """共通ヘッダーを取得

        token_providerが設定されている場合は毎回コールバックでトークン取得（動的トークン）。
        それ以外はapi_keyを使用。
        """
        headers = {"Content-Type": "application/json"}

        # token_provider があれば最優先（プラットフォーム内部の動的トークン用）
        if self._config.token_provider:
            token = self._config.token_provider()
            if token:
                headers["Authorization"] = f"Bearer {token}"
            else:
                logger.warning("token_provider returned None, request will be unauthenticated")
            return headers

        auth_type = getattr(self._config, 'auth_type', 'bearer')
        if auth_type == "bearer":
            headers["Authorization"] = f"Bearer {self._config.api_key}"
        else:
            # Legacy: Internal API Key
            headers["X-Internal-API-Key"] = self._config.api_key

        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """HTTPリクエスト実行

        Args:
            method: HTTPメソッド (GET, POST, etc.)
            endpoint: APIエンドポイント（baseURLからの相対パス）
            params: クエリパラメータ
            json_body: JSONリクエストボディ

        Returns:
            JSONレスポンス

        Raises:
            AuthUnauthorizedError: 認証失敗 (401)
            AuthNotFoundError: リソース未発見 (404)
            AuthRateLimitError: レート制限 (429)
            AuthAPIError: その他のAPIエラー
        """
        url = f"{self._config.base_url.rstrip('/')}{endpoint}"
        client = self._get_http_client()
        headers = self._get_headers()

        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=json_body)
            else:
                raise AuthAPIError(f"Unsupported HTTP method: {method}")

            # ステータスコード別処理
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise AuthUnauthorizedError()
            elif response.status_code == 404:
                raise AuthNotFoundError()
            elif response.status_code == 429:
                raise AuthRateLimitError()
            else:
                error_msg = f"Status {response.status_code}: {response.text}"
                raise AuthAPIError(error_msg, response.status_code)

        except httpx.RequestError as e:
            raise AuthAPIError(f"Request failed: {e}")

    # ============================================================
    # ユーザー一覧取得
    # ============================================================

    async def get_users(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        is_approved: Optional[str] = None,
        job: Optional[str] = None,
        organization: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
        include_last_login: bool = False,
    ) -> GetUsersResult:
        """
        ユーザー一覧を取得

        Args:
            page: ページ番号（デフォルト: 1）
            limit: 1ページあたりの件数（デフォルト: 20）
            search: 検索キーワード（email, username, displayNameで検索）
            is_approved: 承認状態フィルター ('true', 'false', 'all')
            job: 職種でフィルター
            organization: 組織でフィルター
            sort_by: ソート項目 ('created_timestamp', 'email', 'username')
            order: ソート順 ('asc', 'desc')
            include_last_login: 最終ログイン時刻を取得するか

        Returns:
            GetUsersResult: ユーザー一覧結果

        Example:
            ```python
            result = await client.get_users(
                page=1,
                limit=20,
                is_approved="true",
                sort_by="created_timestamp",
                order="desc",
            )
            if result.success:
                for user in result.users:
                    print(f"User: {user.email}")
            ```
        """
        try:
            params: Dict[str, Any] = {
                "page": page,
                "limit": limit,
            }

            if search:
                params["search"] = search
            if is_approved:
                params["is_approved"] = is_approved
            if job:
                params["job"] = job
            if organization:
                params["organization"] = organization
            if sort_by:
                params["sort_by"] = sort_by
            if order:
                params["order"] = order
            if include_last_login:
                params["include_last_login"] = "true"

            response = await self._request(
                "GET", "/api/v1/admin/users", params=params
            )

            # レスポンス解析
            data = response.get("data", {})
            items_raw = data.get("items", [])
            pagination_raw = data.get("pagination", {})

            users = [ApiUser.model_validate(item) for item in items_raw]
            pagination = (
                UserPagination.model_validate(pagination_raw)
                if pagination_raw
                else None
            )

            return GetUsersResult(
                success=True,
                users=users,
                pagination=pagination,
            )

        except (AuthUnauthorizedError, AuthNotFoundError, AuthRateLimitError, AuthAPIError) as e:
            logger.error(f"Failed to get users: {e}")
            return GetUsersResult(
                success=False,
                error=str(e),
                error_code=getattr(e, "error_code", "API_ERROR"),
            )
        except Exception as e:
            logger.error(f"Unexpected error getting users: {e}")
            return GetUsersResult(
                success=False,
                error=str(e),
                error_code="UNKNOWN_ERROR",
            )

    # ============================================================
    # ユーザー詳細取得
    # ============================================================

    async def get_user(self, user_id: str) -> GetUserResult:
        """
        ユーザー詳細を取得

        Args:
            user_id: ユーザーID

        Returns:
            GetUserResult: ユーザー詳細結果

        Example:
            ```python
            result = await client.get_user("c45005f6-b715-47bb-a3d7-44ab208cecc4")
            if result.success:
                print(f"User: {result.user.email}")
                if result.devices:
                    print(f"Devices: {len(result.devices)}")
            ```
        """
        if not user_id:
            return GetUserResult(
                success=False,
                error="user_id is required",
                error_code="INVALID_PARAMETER",
            )

        if user_id in (".", ".."):
            # quote しても残り、URL の正規化で親のパスになる
            return GetUserResult(
                success=False,
                error="user_id is invalid",
                error_code="INVALID_PARAMETER",
            )

        try:
            response = await self._request(
                "GET", f"/api/v1/admin/users/{quote(user_id, safe='')}"
            )

            user_raw = response.get("user", {})
            devices_raw = response.get("devices", [])
            login_history_raw = response.get("loginHistory", [])

            user = ApiUser.model_validate(user_raw)
            # 空配列はそのまま空配列として返す（Noneに変換しない）
            devices = [DeviceInfo.model_validate(d) for d in devices_raw]
            login_history = [LoginHistoryEntry.model_validate(h) for h in login_history_raw]

            # ソフトデリート情報
            is_deleted = user_raw.get("isDeleted", False)
            deleted_at = user_raw.get("deletedAt")
            deleted_by = user_raw.get("deletedBy")
            deletion_reason = user_raw.get("deletionReason")

            return GetUserResult(
                success=True,
                user=user,
                devices=devices,
                login_history=login_history,
                is_deleted=is_deleted,
                deleted_at=deleted_at,
                deleted_by=deleted_by,
                deletion_reason=deletion_reason,
            )

        except AuthNotFoundError:
            return GetUserResult(
                success=False,
                error=f"User not found: {user_id}",
                error_code="NOT_FOUND",
            )
        except (AuthUnauthorizedError, AuthRateLimitError, AuthAPIError) as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            return GetUserResult(
                success=False,
                error=str(e),
                error_code=getattr(e, "error_code", "API_ERROR"),
            )
        except Exception as e:
            logger.error(f"Unexpected error getting user {user_id}: {e}")
            return GetUserResult(
                success=False,
                error=str(e),
                error_code="UNKNOWN_ERROR",
            )

    # ============================================================
    # MCP OAuth トークン取得
    # ============================================================

    async def get_mcp_tokens(
        self,
        user_id: str,
        providers: Optional[List[OAuthProviderName]] = None,
        rejected_token_sha256: Optional[Dict[str, str]] = None,
    ) -> GetMCPTokensResult:
        """
        MCP用OAuthトークンを取得

        Args:
            user_id: ユーザーID
            providers: 取得するプロバイダー（省略時は全プロバイダー）
                      例: ["github", "slack", "google", "office365"]
            rejected_token_sha256: provider → 接続先に 401 で拒否されたアクセストークンの SHA-256
                      (トークン文字列の UTF-8。16 進の小文字 64 桁)。供給側は保存中のトークンがこれと同じなら
                      期限前でも取り直す (SDK ≥ 3.0.10 / chatboardlogin が対応している場合)。トークンそのものは渡さない

        Returns:
            GetMCPTokensResult: MCPトークン取得結果

        Example:
            ```python
            result = await client.get_mcp_tokens(
                "user-id-123",
                providers=["github", "slack"],
            )
            if result.success:
                for provider, token in result.tokens.items():
                    print(f"{provider}: expires at {token.expires_at}")
                if result.errors:
                    for provider, err in result.errors.items():
                        print(f"{provider} error: {err.message}")
            ```
        """
        if not user_id:
            return GetMCPTokensResult(
                success=False,
                error="user_id is required",
                error_code="INVALID_PARAMETER",
            )

        try:
            body: Dict[str, Any] = {"user_id": user_id}
            if providers:
                body["providers"] = providers
            if rejected_token_sha256:
                body["rejected_token_sha256"] = dict(rejected_token_sha256)

            response = await self._request(
                "POST", "/api/v1/oauth/mcp/token", json_body=body
            )

            tokens_raw = response.get("tokens", {})
            errors_raw = response.get("errors", {})

            # トークン変換（expires_at: string -> datetime）
            tokens: Dict[str, MCPTokenInfo] = {}
            token_errors: Dict[str, MCPTokenError] = {}

            for provider, token_data in tokens_raw.items():
                expires_at_raw = token_data.get("expires_at")

                # 期限なし (null / キー欠損) は個人トークン (PAT) の正常形として
                # None で受理する (供給 API は PAT で expires_at=null を明示返却する)。
                # それ以外は ISO 8601 文字列のみ受理し、不正値 (非文字列・空文字・
                # 解釈不能) は provider 単位の INVALID_EXPIRES_AT で fail-closed。
                # ⚠️ isinstance を先に確認する: 非文字列に .replace() すると
                # AttributeError が外側の broad except へ漏れ、provider 単位でなく
                # 取得全体が UNKNOWN_ERROR になってしまう (Codex レビュー指摘)。
                expires_at: Optional[datetime] = None
                if expires_at_raw is not None:
                    if not isinstance(expires_at_raw, str):
                        token_errors[provider] = MCPTokenError(
                            code="INVALID_EXPIRES_AT",
                            message=f"Invalid expires_at format: {expires_at_raw!r}",
                        )
                        continue
                    try:
                        expires_at = datetime.fromisoformat(
                            expires_at_raw.replace("Z", "+00:00")
                        )
                    except ValueError:
                        token_errors[provider] = MCPTokenError(
                            code="INVALID_EXPIRES_AT",
                            message=f"Invalid expires_at format: {expires_at_raw}",
                        )
                        continue

                tokens[provider] = MCPTokenInfo(
                    access_token=token_data.get("access_token", ""),
                    token_type=token_data.get("token_type", "Bearer"),
                    expires_at=expires_at,
                    scopes=token_data.get("scopes", []),
                )

            # APIからのエラーを追加
            for provider, err in errors_raw.items():
                token_errors[provider] = MCPTokenError(
                    code=err.get("code", "UNKNOWN"),
                    message=err.get("message", "Unknown error"),
                )

            # エラーがあればerrorsに設定
            final_errors = token_errors if token_errors else None

            return GetMCPTokensResult(
                success=True,
                tokens=tokens,
                errors=final_errors,
            )

        except (AuthUnauthorizedError, AuthRateLimitError, AuthAPIError) as e:
            logger.error(f"Failed to get MCP tokens for {user_id}: {e}")
            return GetMCPTokensResult(
                success=False,
                error=str(e),
                error_code=getattr(e, "error_code", "API_ERROR"),
            )
        except Exception as e:
            logger.error(f"Unexpected error getting MCP tokens for {user_id}: {e}")
            return GetMCPTokensResult(
                success=False,
                error=str(e),
                error_code="UNKNOWN_ERROR",
            )

    # ============================================================
    # リソースクローズ
    # ============================================================

    async def close(self) -> None:
        """クライアントリソースをクローズ"""
        try:
            if self._http_client and not self._http_client.is_closed:
                await self._http_client.aclose()
        except Exception as e:
            logger.warning(f"Error closing HTTP client: {e}")
        finally:
            self._http_client = None
            logger.debug("AgenticStarAuthClient closed")
