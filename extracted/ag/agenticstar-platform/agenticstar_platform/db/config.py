"""
AGENTICSTAR Platform SDK - Database Configuration Models
PostgreSQL接続のための設定モデル
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, TypeVar

from .._config_utils import load_toml_section

T = TypeVar("T")


@dataclass
class AzureADConfig:
    """Azure AD認証設定

    Note:
        client_secretはrepr=Falseでログ出力から除外されます。

    Example:
        >>> # 辞書から作成
        >>> config = AzureADConfig.from_dict({
        ...     "tenant_id": "xxx",
        ...     "client_id": "yyy",
        ...     "client_secret": "zzz"
        ... })

        >>> # TOMLファイルから作成
        >>> config = AzureADConfig.from_toml("config.toml", section="database.azure_ad")
    """

    tenant_id: str
    client_id: str
    client_secret: str = field(repr=False)  # シークレット: reprから除外
    username: str = ""  # PostgreSQL Azure AD authentication username

    def __str__(self) -> str:
        return f"AzureADConfig(tenant_id={self.tenant_id!r}, client_id={self.client_id!r}, client_secret=***)"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AzureADConfig":
        """辞書からAzureADConfigを作成

        Args:
            data: 設定辞書

        Returns:
            AzureADConfig instance

        Example:
            >>> config = AzureADConfig.from_dict({
            ...     "tenant_id": "your-tenant-id",
            ...     "client_id": "your-client-id",
            ...     "client_secret": "your-secret"
            ... })
        """
        return cls(
            tenant_id=data["tenant_id"],
            client_id=data["client_id"],
            client_secret=data["client_secret"],
            username=data.get("username", ""),
        )

    @classmethod
    def from_toml(cls, toml_path: str, section: str = "azure_ad") -> "AzureADConfig":
        """TOMLファイルからAzureADConfigを作成

        Args:
            toml_path: TOMLファイルパス
            section: セクション名（ドット区切りでネスト対応）

        Returns:
            AzureADConfig instance

        Example:
            >>> # config.toml の [database.azure_ad] セクションを読み込み
            >>> config = AzureADConfig.from_toml("config.toml", section="database.azure_ad")
        """
        data = load_toml_section(toml_path, section)
        return cls.from_dict(data)


@dataclass
class PostgreSQLConfig:
    """PostgreSQL設定

    Note:
        passwordはrepr=Falseでログ出力から除外されます。

    Example:
        >>> # 辞書から作成
        >>> config = PostgreSQLConfig.from_dict({
        ...     "host": "localhost",
        ...     "port": 5432,
        ...     "database": "mydb",
        ...     "username": "user",
        ...     "password": "pass"
        ... })

        >>> # TOMLファイルから作成
        >>> config = PostgreSQLConfig.from_toml("config.toml", section="database")
    """

    provider: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    database: str = "agenticstar_db"
    use_azure_ad: bool = False

    # 標準認証用（use_azure_ad=Falseの場合）
    username: Optional[str] = None
    password: Optional[str] = field(default=None, repr=False)  # シークレット: reprから除外

    # 接続プール設定
    pool_min_size: int = 5
    pool_max_size: int = 20
    command_timeout: int = 60
    pool_timeout: Optional[int] = 30
    max_overflow: Optional[int] = 10

    # Azure AD認証設定
    azure_ad: Optional[AzureADConfig] = None

    # HTTP API経由時のエンドポイントURL
    api_url: Optional[str] = None

    # SSL設定（デフォルト: require, ローカル開発用: disable）
    ssl_mode: str = "require"

    def __str__(self) -> str:
        return (
            f"PostgreSQLConfig(host={self.host!r}, port={self.port}, "
            f"database={self.database!r}, use_azure_ad={self.use_azure_ad}, password=***)"
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PostgreSQLConfig":
        """辞書からPostgreSQLConfigを作成

        Args:
            data: 設定辞書

        Returns:
            PostgreSQLConfig instance

        Example:
            >>> config = PostgreSQLConfig.from_dict({
            ...     "host": "db.example.com",
            ...     "port": 5432,
            ...     "database": "mydb",
            ...     "username": "user",
            ...     "password": "secret",
            ...     "use_azure_ad": False,
            ...     "pool_max_size": 30
            ... })
        """
        # Azure AD設定がある場合はネストして処理
        azure_ad = None
        if "azure_ad" in data and data.get("use_azure_ad"):
            azure_ad = AzureADConfig.from_dict(data["azure_ad"])

        return cls(
            provider=data.get("provider", "postgresql"),
            host=data.get("host", "localhost"),
            port=data.get("port", 5432),
            database=data.get("database", "agenticstar_db"),
            use_azure_ad=data.get("use_azure_ad", False),
            username=data.get("username"),
            password=data.get("password"),
            pool_min_size=data.get("pool_min_size", 5),
            pool_max_size=data.get("pool_max_size", 20),
            command_timeout=data.get("command_timeout", 60),
            pool_timeout=data.get("pool_timeout", 30),
            max_overflow=data.get("max_overflow", 10),
            azure_ad=azure_ad,
            api_url=data.get("api_url"),
        )

    @classmethod
    def from_toml(cls, toml_path: str, section: str = "database") -> "PostgreSQLConfig":
        """TOMLファイルからPostgreSQLConfigを作成

        Args:
            toml_path: TOMLファイルパス
            section: セクション名（ドット区切りでネスト対応）

        Returns:
            PostgreSQLConfig instance

        Example:
            >>> # config.toml の [database] セクションを読み込み
            >>> config = PostgreSQLConfig.from_toml("config.toml")

            >>> # ネストされたセクション
            >>> config = PostgreSQLConfig.from_toml("config.toml", section="services.database")
        """
        data = load_toml_section(toml_path, section)
        return cls.from_dict(data)

    @classmethod
    def from_env(cls, prefix: str = "DB_") -> "PostgreSQLConfig":
        """環境変数からPostgreSQLConfigを作成

        環境変数名は {prefix}{FIELD_NAME} の形式で読み込みます。

        Args:
            prefix: 環境変数名のプレフィックス（デフォルト: "DB_"）

        Returns:
            PostgreSQLConfig instance

        Example:
            >>> # 環境変数から作成（DB_HOST, DB_PORT, DB_DATABASE, etc.）
            >>> config = PostgreSQLConfig.from_env()

            >>> # カスタムプレフィックス（POSTGRES_HOST, POSTGRES_PORT, etc.）
            >>> config = PostgreSQLConfig.from_env(prefix="POSTGRES_")

        Environment Variables:
            {prefix}HOST: データベースホスト（デフォルト: localhost）
            {prefix}PORT: ポート番号（デフォルト: 5432）
            {prefix}DATABASE: データベース名（デフォルト: agenticstar_db）
            {prefix}USER / {prefix}USERNAME: ユーザー名
            {prefix}PASSWORD: パスワード
            {prefix}USE_AZURE_AD: Azure AD認証を使用するか（true/false）
            {prefix}POOL_MIN_SIZE: 最小プールサイズ（デフォルト: 5）
            {prefix}POOL_MAX_SIZE: 最大プールサイズ（デフォルト: 20）
            {prefix}API_PROXY_URL: API Proxy URL（CLIモード用）
        """
        def get_env(key: str, default: str = "") -> str:
            return os.environ.get(f"{prefix}{key}", default)

        def get_env_int(key: str, default: int) -> int:
            val = os.environ.get(f"{prefix}{key}")
            return int(val) if val else default

        def get_env_bool(key: str, default: bool = False) -> bool:
            val = os.environ.get(f"{prefix}{key}", "").lower()
            return val in ("true", "1", "yes") if val else default

        # ユーザー名は USER または USERNAME どちらでも可
        username = get_env("USER") or get_env("USERNAME")

        return cls(
            host=get_env("HOST", "localhost"),
            port=get_env_int("PORT", 5432),
            database=get_env("DATABASE", "agenticstar_db"),
            username=username or None,
            password=get_env("PASSWORD") or None,
            use_azure_ad=get_env_bool("USE_AZURE_AD"),
            pool_min_size=get_env_int("POOL_MIN_SIZE", 5),
            pool_max_size=get_env_int("POOL_MAX_SIZE", 20),
            command_timeout=get_env_int("COMMAND_TIMEOUT", 60),
            pool_timeout=get_env_int("POOL_TIMEOUT", 30),
            max_overflow=get_env_int("MAX_OVERFLOW", 10),
            api_url=get_env("API_PROXY_URL") or None,
        )
