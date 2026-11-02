"""Webhook 回调验签。

签名是对原始请求体做 HMAC-SHA256，头部格式为 ``X-Webhook-Signature: sha256=<hex>``。
必须用收到的原始字节验签，不要先解析再重新序列化。
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any, Optional

DEFAULT_TOLERANCE_SECONDS = 12 * 3600


def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    """检查签名是否与原始请求体匹配。"""
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


def parse_webhook(
    payload: bytes,
    signature: str,
    secret: str,
    *,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
    now: Optional[float] = None,
) -> dict[str, Any]:
    """验签并解析回调；签名不符或 timestamp 超出容差时抛出 ValueError。

    失败重试会原样重发，因此时效窗口不要短于最后一次重试（约 8.6 小时）。
    接收端还应按 data.job_id 与 data.status 去重。
    """
    if not verify_webhook(payload, signature, secret):
        raise ValueError("invalid signature")

    event = json.loads(payload)
    current = time.time() if now is None else now
    if abs(current - event["timestamp"]) > tolerance:
        raise ValueError("stale event")
    return event
