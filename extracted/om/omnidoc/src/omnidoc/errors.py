"""OmniDoc 客户端的异常类型。"""

from __future__ import annotations

from typing import Any, Optional

import requests


class OmniDocError(Exception):
    """API 返回的错误（HTTP 状态码 >= 400）。

    code 来自响应体的 code 字段；只有部分错误带 code，缺失时为 UNKNOWN_ERROR。
    request_id 对应响应头 X-Request-Id，排查问题时请一并提供。
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        *,
        detail: Any = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(f"HTTP {status_code} {code}: {message}")
        self.status_code = status_code
        self.code = code
        self.message = message
        self.detail = detail
        self.request_id = request_id


class JobFailedError(RuntimeError):
    """翻译任务以 failed 结束。

    quota_exceeded 为 True 时表示余额不足以开始该文件，任务未扣费。
    """

    def __init__(self, job: dict) -> None:
        self.job = job
        self.quota_exceeded = bool(job.get("quota_exceeded"))
        super().__init__(job.get("error_msg") or "translation failed")


def error_from_response(response: requests.Response) -> OmniDocError:
    """把错误响应转换成 OmniDocError，兼容无 JSON 或 422 字段列表的情况。"""
    try:
        body = response.json()
    except ValueError:
        body = {}
    if not isinstance(body, dict):
        body = {}

    code = body.get("code") or "UNKNOWN_ERROR"
    detail = body.get("detail")
    message = body.get("message")
    if not message:
        if isinstance(detail, str):
            message = detail
        elif isinstance(detail, list):
            message = "参数校验失败"
        else:
            message = response.reason or "request failed"

    return OmniDocError(
        response.status_code,
        code,
        message,
        detail=detail,
        request_id=response.headers.get("X-Request-Id"),
    )
