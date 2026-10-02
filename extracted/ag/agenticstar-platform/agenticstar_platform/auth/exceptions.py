"""
AGENTICSTAR Platform SDK - Auth Exceptions
AgenticStar Auth API操作の例外定義
"""

from typing import Optional


class AuthError(Exception):
    """Auth操作の基底エラー"""

    pass


class AuthConfigError(AuthError):
    """Auth設定エラー

    Raises:
        設定が不正または不足している場合
    """

    pass


class AuthAPIError(AuthError):
    """Auth API呼び出しエラー

    Attributes:
        status_code: HTTPステータスコード
        error_code: エラーコード文字列
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: str = "API_ERROR",
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code


class AuthUnauthorizedError(AuthAPIError):
    """認証エラー（401 Unauthorized）

    Raises:
        APIキーが無効または未設定の場合
    """

    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")


class AuthNotFoundError(AuthAPIError):
    """リソース未発見エラー（404 Not Found）

    Raises:
        指定されたユーザーまたはリソースが存在しない場合
    """

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class AuthRateLimitError(AuthAPIError):
    """レート制限エラー（429 Too Many Requests）

    Raises:
        APIレート制限に達した場合
    """

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429, error_code="RATE_LIMITED")
