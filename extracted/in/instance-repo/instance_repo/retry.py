"""retry.py — 瞬时故障重试（指数退避 + 抖动）。

只重试**瞬时**故障：网络超时/连接重置、HTTP 5xx、HTTP 429/408、oss2 ServerError（5xx）。
**永不**重试其余 4xx（权限/参数错误，重试无意义且会放大压力）。

429 是唯一"该退避重试"的限流信号：apiserver 的凭据限流器在自身有界重试耗尽后会回 429，
客户端若当作永久 4xx 立刻放弃，就把本可恢复的限流变成了调用方可见的失败
（真机压测：200 并发 → 400 次里 34 次 429 直接暴露给调用方）。
"""
from __future__ import annotations

import random
import socket
import time
from typing import Callable, TypeVar

T = TypeVar("T")

# 可注入以便测试（避免真实 sleep / 固定抖动）
_DEFAULT_SLEEP = time.sleep

#: 可重试的 4xx：429=限流（退避后可成功）、408=请求超时（服务端主动断，重发安全）。
RETRIABLE_4XX = frozenset({408, 429})

#: Tengine 等反向代理偶发返回的重定向状态码；SDK 应视为瞬时故障并重试。
REDIRECT_STATUSES = frozenset({301, 302, 307, 308})


def _status_of(exc: BaseException) -> int | None:
    """尽力从异常里取 HTTP 状态码：TransportError.status / oss2.*.status / .code。"""
    for attr in ("status", "code"):
        val = getattr(exc, attr, None)
        if isinstance(val, int):
            return val
    return None


def is_transient(exc: BaseException) -> bool:
    """判定是否瞬时故障：可安全重试返回 True，否则 False。

    真正的网络抖动以 ``socket.timeout`` / ``ConnectionError`` / ``TimeoutError``
    形式直接抛出（HTTP 层未包装），一律重试；带 HTTP 状态码的异常：5xx 与
    ``RETRIABLE_4XX``（429 限流 / 408 超时）视为瞬时、其余 4xx 永不重试；
    oss2 把网络层错误包成 ``RequestError`` 且 ``.status<0``（哨兵 -2），亦视为瞬时；
    无状态码的 ``TransportError``（如契约字段缺失）是确定性错误，不重试。
    """
    if isinstance(exc, (socket.timeout, ConnectionError, TimeoutError)):
        return True
    status = _status_of(exc)
    if status is not None:
        return (status < 0 or 500 <= status <= 599
                or status in RETRIABLE_4XX
                or status in REDIRECT_STATUSES)
    return False


def retry_transient(
    fn: Callable[[], T],
    *,
    attempts: int = 3,
    base: float = 0.2,
    cap: float = 5.0,
    jitter: bool = True,
    sleep: Callable[[float], None] = _DEFAULT_SLEEP,
    rand: Callable[[], float] = random.random,
) -> T:
    """执行 ``fn``，对瞬时故障最多尝试 ``attempts`` 次（含首次）。

    退避 = min(cap, base * 2**(i-1))，jitter=True 时乘 [0.5,1.5) 抖动后再夹到 cap。
    非瞬时故障或耗尽次数后原样抛出最后一次异常。
    """
    last: BaseException | None = None
    for i in range(1, attempts + 1):
        try:
            return fn()
        except BaseException as exc:  # noqa: BLE001 — 由 is_transient 精确筛选
            last = exc
            if i >= attempts or not is_transient(exc):
                raise
            delay = min(cap, base * (2 ** (i - 1)))
            if jitter:
                delay = min(cap, delay * (0.5 + rand()))
            sleep(delay)
    assert last is not None  # pragma: no cover — 循环保证已 return 或 raise
    raise last  # pragma: no cover
