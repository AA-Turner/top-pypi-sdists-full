"""OmniDoc 开放 API 的 Python 客户端。"""

from .client import DEFAULT_BASE_URL, OmniDocClient
from .errors import JobFailedError, OmniDocError
from .webhooks import parse_webhook, verify_webhook

__all__ = [
    "DEFAULT_BASE_URL",
    "JobFailedError",
    "OmniDocClient",
    "OmniDocError",
    "parse_webhook",
    "verify_webhook",
]

__version__ = "0.1.8"
