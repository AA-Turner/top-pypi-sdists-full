"""
AGENTICSTAR Platform SDK - Auth Response Models
AgenticStar Auth APIのレスポンスモデル（Pydantic v2）
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator


# ============================================================
# OAuth Provider Types
# ============================================================

# DBのoauth_providers.serviceから取得した値を使用
OAuthProviderName = str


# ============================================================
# User Models
# ============================================================


class UserPagination(BaseModel):
    """ページネーション情報"""

    page: int
    limit: int
    total: int
    total_pages: int = Field(alias="totalPages")
    has_next: bool = Field(alias="hasNext")
    has_previous: bool = Field(alias="hasPrevious")

    model_config = {"populate_by_name": True}


class ApiUser(BaseModel):
    """ユーザー情報

    chatboardloginのAPIレスポンス形式に対応:
    - attributes.organization: { id: string, label: string }
    - attributes.job: { id: string, label: string }
    """

    id: str
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    display_name: Optional[str] = Field(None, alias="displayName")
    email_verified: bool = Field(False, alias="emailVerified")
    enabled: bool = True
    created_timestamp: Optional[int] = Field(None, alias="created_timestamp")
    attributes: Optional[Dict[str, Any]] = None
    organization: Optional[str] = None
    organization_label: Optional[str] = Field(None, alias="organizationLabel")
    job: Optional[str] = None
    job_label: Optional[str] = Field(None, alias="jobLabel")
    bio: Optional[str] = None
    last_login_at: Optional[str] = Field(None, alias="lastLoginAt")

    model_config = {"populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def extract_from_attributes(cls, data: Any) -> Any:
        """attributesからorganization/jobのid/labelを抽出

        chatboardloginのレスポンス形式:
        {
            "attributes": {
                "organization": { "id": "se_bd1", "label": "日本語ラベル" },
                "job": { "id": "frontend", "label": "日本語ラベル" },
                "bio": "自己紹介"
            }
        }
        """
        if not isinstance(data, dict):
            return data

        attributes = data.get("attributes")
        if not attributes or not isinstance(attributes, dict):
            return data

        # organization: { id, label } からid/labelを抽出
        org_data = attributes.get("organization")
        if isinstance(org_data, dict):
            if "id" in org_data and data.get("organization") is None:
                data["organization"] = org_data["id"]
            if "label" in org_data and data.get("organization_label") is None:
                data["organization_label"] = org_data["label"]

        # job: { id, label } からid/labelを抽出
        job_data = attributes.get("job")
        if isinstance(job_data, dict):
            if "id" in job_data and data.get("job") is None:
                data["job"] = job_data["id"]
            if "label" in job_data and data.get("job_label") is None:
                data["job_label"] = job_data["label"]

        # bio: 文字列として直接取得
        bio_data = attributes.get("bio")
        if isinstance(bio_data, str) and data.get("bio") is None:
            data["bio"] = bio_data

        return data

    # ID取得メソッド
    def get_org_id(self) -> Optional[str]:
        """組織IDを取得"""
        return self.organization

    def get_job_id(self) -> Optional[str]:
        """職種IDを取得"""
        return self.job

    # ラベル（表示値）取得メソッド
    def get_display_name(self) -> Optional[str]:
        """表示名を取得"""
        return self.display_name

    def get_organization_label(self) -> Optional[str]:
        """組織ラベルを取得"""
        return self.organization_label

    def get_job_label(self) -> Optional[str]:
        """職種ラベルを取得"""
        return self.job_label

    def get_bio(self) -> Optional[str]:
        """自己紹介を取得"""
        return self.bio


# ============================================================
# User Detail Models
# ============================================================


class DeviceInfo(BaseModel):
    """デバイス情報"""

    id: Optional[str] = None
    device_code: str
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    device_info: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None
    last_used_at: Optional[str] = None


class LoginHistoryEntry(BaseModel):
    """ログイン履歴エントリ"""

    timestamp: int
    ip_address: str = Field(alias="ipAddress")
    user_agent: str = Field(alias="userAgent")
    platform: str
    location: Optional[Dict[str, Optional[str]]] = None
    success: bool

    model_config = {"populate_by_name": True}


# ============================================================
# MCP OAuth Token Models
# ============================================================


class MCPTokenInfo(BaseModel):
    """MCPトークン情報

    expires_at は None が「期限なし」を表す。個人トークン (PAT,
    authMode='api_token') は長期/無期限のため、供給 API (chatboardlogin) が
    expires_at=null を明示返却する。
    """

    access_token: str
    token_type: str
    expires_at: Optional[datetime] = None
    scopes: List[str]


class MCPTokenError(BaseModel):
    """MCPトークン取得エラー

    Attributes:
        code: エラーコード (CONNECTION_NOT_FOUND, TOKEN_EXPIRED, REFRESH_FAILED等)
        message: エラーメッセージ
    """

    code: str
    message: str


# ============================================================
# Result Types (SDK戻り値)
# ============================================================


class GetUsersResult(BaseModel):
    """ユーザー一覧取得結果

    Attributes:
        success: 成功したかどうか
        users: ユーザーリスト
        pagination: ページネーション情報
        error: エラーメッセージ（失敗時）
        error_code: エラーコード（失敗時）
    """

    success: bool
    users: List[ApiUser] = Field(default_factory=list)
    pagination: Optional[UserPagination] = None
    error: Optional[str] = None
    error_code: Optional[str] = None


class GetUserResult(BaseModel):
    """ユーザー詳細取得結果

    Attributes:
        success: 成功したかどうか
        user: ユーザー情報
        devices: デバイス情報リスト（空配列も保持）
        login_history: ログイン履歴（空配列も保持）
        error: エラーメッセージ（失敗時）
        error_code: エラーコード（失敗時）
    """

    success: bool
    user: Optional[ApiUser] = None
    devices: List[DeviceInfo] = Field(default_factory=list)
    login_history: List[LoginHistoryEntry] = Field(default_factory=list)
    is_deleted: bool = False
    deleted_at: Optional[str] = None
    deleted_by: Optional[str] = None
    deletion_reason: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[str] = None


class GetMCPTokensResult(BaseModel):
    """MCPトークン取得結果

    Attributes:
        success: 成功したかどうか
        tokens: プロバイダー別トークン情報
        errors: プロバイダー別エラー情報
        error: 全体エラーメッセージ（失敗時）
        error_code: 全体エラーコード（失敗時）

    Example:
        ```python
        result = await client.get_mcp_tokens("user-id", ["github", "slack"])
        if result.success:
            for provider, token in result.tokens.items():
                print(f"{provider}: expires at {token.expires_at}")
            if result.errors:
                for provider, err in result.errors.items():
                    print(f"{provider} error: {err.message}")
        ```
    """

    success: bool
    tokens: Dict[str, MCPTokenInfo] = Field(default_factory=dict)
    errors: Optional[Dict[str, MCPTokenError]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
