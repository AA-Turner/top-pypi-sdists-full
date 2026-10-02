"""
AGENTICSTAR Platform SDK - Auth Configuration Models
AgenticStar Auth API接続のための設定モデル

設定ソース: config.toml [auth.agenticstar] セクション
（values.yaml → Helm template → Secret としてマウント）

Note:
    CLIモードでの使用は src.config.auth_config_factory を使用してください。
    SDKはsrc層をインポートしないため、CLI固有の設定は呼び出し側で注入します。
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from .exceptions import AuthConfigError


@dataclass
class AgenticStarAuthConfig:
    """AgenticStar Auth API設定

    Args:
        base_url: APIベースURL (例: "https://auth.example.com")
        api_key: Bearer token（静的トークン認証時）
        auth_type: 認証タイプ ("bearer" or "api_key")
        token_provider: 動的トークン取得コールバック（設定時はapi_keyより優先）
        timeout: HTTPリクエストタイムアウト秒数

    Note:
        api_keyはrepr=Falseでログ出力から除外されます。
        token_providerが設定されている場合、毎リクエスト時にコールバックで
        トークンを取得する（期限切れトークンの自動更新に対応）。

    Example:
        ```python
        # 静的トークン（市民開発者向け）
        config = AgenticStarAuthConfig.create(
            base_url="https://auth.example.com",
            api_key="your-bearer-token",
        )

        # 動的トークン（プラットフォーム内部用）
        config = AgenticStarAuthConfig.create(
            base_url="https://auth.example.com",
            token_provider=my_token_reader,
        )
        ```
    """

    # 必須設定
    base_url: str
    api_key: str = field(repr=False, default="")  # Bearer token

    # オプション設定
    auth_type: str = "bearer"  # "bearer" or "api_key" (legacy)
    token_provider: Optional[Callable[[], Optional[str]]] = field(
        default=None, repr=False
    )  # 動的トークン取得（設定時はapi_keyより優先）
    timeout: float = 30.0

    def __str__(self) -> str:
        """文字列表現（APIキーをマスク）"""
        has_provider = "yes" if self.token_provider else "no"
        return f"AgenticStarAuthConfig(base_url={self.base_url!r}, api_key=***, token_provider={has_provider})"

    @classmethod
    def create(
        cls,
        base_url: str,
        api_key: str = "",
        auth_type: str = "bearer",
        token_provider: Optional[Callable[[], Optional[str]]] = None,
        timeout: float = 30.0,
    ) -> "AgenticStarAuthConfig":
        """コードから直接設定を指定して作成

        Args:
            base_url: APIベースURL
            api_key: Bearer token（静的トークン時）
            auth_type: 認証タイプ ("bearer" or "api_key")
            token_provider: 動的トークン取得コールバック（毎リクエスト呼び出し）
            timeout: タイムアウト秒数

        Returns:
            AgenticStarAuthConfig インスタンス

        Example:
            ```python
            # Bearer token（市民開発者）
            config = AgenticStarAuthConfig.create(
                base_url="https://auth.example.com",
                api_key="oauth-token",
            )

            # 動的トークン（プラットフォーム内部）
            config = AgenticStarAuthConfig.create(
                base_url="https://auth.example.com",
                token_provider=lambda: read_token_from_file(),
            )
            ```
        """
        return cls(
            base_url=base_url,
            api_key=api_key,
            auth_type=auth_type,
            token_provider=token_provider,
            timeout=timeout,
        )

    @classmethod
    def from_config(
        cls,
        config_path: Optional[Path] = None,
    ) -> "AgenticStarAuthConfig":
        """config.tomlから設定を読み込む

        Args:
            config_path: config.tomlのパス（省略時は自動検出）

        Returns:
            AgenticStarAuthConfig インスタンス

        Raises:
            AuthConfigError: 設定ファイルの読み込みに失敗した場合
            ValueError: 必須設定が見つからない場合
        """
        toml_config = cls._load_toml_config(config_path)

        base_url = toml_config.get("base_url")
        api_key = toml_config.get("api_key", "")
        timeout = toml_config.get("timeout", 30.0)

        # バリデーション
        if not base_url:
            raise ValueError(
                "base_url is required. Configure [auth.agenticstar] base_url in config.toml"
            )

        if not api_key:
            raise ValueError(
                "api_key is required. Configure [auth.agenticstar] api_key in config.toml"
            )

        return cls(
            base_url=base_url,
            api_key=api_key,
            auth_type="bearer",
            timeout=float(timeout),
        )

    @staticmethod
    def _load_toml_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
        """config.tomlから[auth.agenticstar]セクションを読み込む

        Raises:
            AuthConfigError: ファイル読み込みやパースに失敗した場合
        """
        import tomllib

        # パスが指定されていない場合は自動検出
        candidates = []
        if config_path is None:
            # 優先順位: カレントディレクトリ > プロジェクトルート
            candidates = [
                Path.cwd() / "config.toml",
                Path(__file__).parent.parent.parent.parent / "config.toml",  # sdk/ の親 = プロジェクトルート
            ]
            for candidate in candidates:
                if candidate.exists():
                    config_path = candidate
                    break

        if config_path is None or not config_path.exists():
            raise AuthConfigError(
                f"config.toml not found. Searched: {[str(c) for c in candidates]}"
            )

        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise AuthConfigError(f"Invalid TOML syntax in {config_path}: {e}")
        except PermissionError as e:
            raise AuthConfigError(f"Permission denied reading {config_path}: {e}")
        except Exception as e:
            raise AuthConfigError(f"Failed to read {config_path}: {e}")

        auth_agenticstar = config.get("auth", {}).get("agenticstar")
        if auth_agenticstar is None:
            raise AuthConfigError(
                f"[auth.agenticstar] section not found in {config_path}"
            )

        return auth_agenticstar
