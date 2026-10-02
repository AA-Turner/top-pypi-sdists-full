"""
AGENTICSTAR Platform SDK - Secret Masking Utilities
シークレット値のマスキングユーティリティ
"""

import re
from typing import Any, Dict, List, Optional, Set


class SecretMasker:
    """シークレット値をマスクするユーティリティクラス

    Example:
        masker = SecretMasker(secret_keys=["password", "api_key"])
        safe_dict = masker.mask_dict({"username": "user", "password": "secret123"})
        # {"username": "user", "password": "***"}
    """

    DEFAULT_SECRET_KEYS = frozenset({
        "password",
        "secret",
        "api_key",
        "apikey",
        "access_key",
        "secret_key",
        "token",
        "bearer",
        "authorization",
        "credential",
        "private_key",
        "connection_string",
        "client_secret",
    })

    def __init__(
        self,
        secret_keys: Optional[Set[str]] = None,
        mask_string: str = "***",
        case_sensitive: bool = False,
    ):
        """
        Args:
            secret_keys: マスク対象のキー名セット（デフォルト: DEFAULT_SECRET_KEYS）
            mask_string: マスク文字列
            case_sensitive: キー名の大文字小文字を区別するか
        """
        self.secret_keys = secret_keys or self.DEFAULT_SECRET_KEYS
        self.mask_string = mask_string
        self.case_sensitive = case_sensitive

    def _is_secret_key(self, key: str) -> bool:
        """キー名がシークレットかどうかを判定"""
        check_key = key if self.case_sensitive else key.lower()
        for secret_key in self.secret_keys:
            secret_check = secret_key if self.case_sensitive else secret_key.lower()
            if secret_check in check_key:
                return True
        return False

    def mask_value(self, key: str, value: Any) -> Any:
        """キー名に基づいて値をマスク

        Args:
            key: キー名
            value: 値

        Returns:
            シークレットキーの場合はマスク文字列、それ以外は元の値
        """
        if self._is_secret_key(key) and value is not None:
            return self.mask_string
        return value

    def mask_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """辞書内のシークレット値をマスク

        Args:
            data: マスク対象の辞書

        Returns:
            シークレット値がマスクされた新しい辞書
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                result[key] = self.mask_dict(value)
            elif isinstance(value, list):
                result[key] = [
                    self.mask_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = self.mask_value(key, value)
        return result


def mask_secret(value: str, visible_chars: int = 0, mask_string: str = "***") -> str:
    """文字列をマスク

    Args:
        value: マスク対象の文字列
        visible_chars: 表示する先頭文字数（0の場合は完全マスク）
        mask_string: マスク文字列

    Returns:
        マスクされた文字列

    Example:
        mask_secret("secret123")  # "***"
        mask_secret("secret123", visible_chars=3)  # "sec***"
    """
    if not value:
        return mask_string

    if visible_chars <= 0:
        return mask_string

    return value[:visible_chars] + mask_string
