"""협조적 취소 토큰.

AGENTS.md 원칙: 취소는 모델 텍스트가 아니라 실행 상태(state)가 소유한다.
TUI 입력 스레드가 `set()`으로 신호를 보내고, AgentLoop / _chat_reply 가
iteration·청크 경계에서 `is_set()`을 폴링해 협조적으로 멈춘다.

진행 중인 단일 blocking 작업(예: 긴 HTTP 요청)까지 즉시 죽이지는 않는다.
다음 경계에서 멈춘다 — 구 협조적 cancel(커밋 7826cb9f3)과 동일한 계약.
"""
from __future__ import annotations

import threading


class CancelledError(Exception):
    """CancelToken 이 세팅된 상태에서 raise_if_cancelled() 호출 시 발생."""


class CancelToken:
    """스레드-세이프 협조적 취소 신호.

    - `set()`      : 취소 요청 (입력 스레드에서 호출)
    - `is_set()`   : 실행 스레드가 경계에서 폴링
    - `clear()`    : 다음 실행을 위해 재사용 시 초기화
    - `raise_if_cancelled()` : 세팅됐으면 CancelledError 발생
    """

    __slots__ = ("_event",)

    def __init__(self) -> None:
        self._event = threading.Event()

    def set(self) -> None:
        self._event.set()

    def clear(self) -> None:
        self._event.clear()

    def is_set(self) -> bool:
        return self._event.is_set()

    def raise_if_cancelled(self) -> None:
        if self._event.is_set():
            raise CancelledError()

    def __bool__(self) -> bool:
        return self._event.is_set()
