"""Stub for module: restart_policy."""
from __future__ import annotations

import logging
from typing import Callable, Dict, List, Optional

log: logging.Logger

_DEFAULT_COOLDOWN_SEC: float
_DEFAULT_EOF_COOLDOWN_SEC: float
_DEFAULT_GIVEUP_COOLDOWN_SEC: float
_DEFAULT_MAX_RESTARTS: int
_DEFAULT_WINDOW_SEC: float


class _CameraState:
    restarts: List[float]
    last_attempt: float
    given_up: bool
    def __init__(self) -> None: ...


class StreamSupervisor:
    cooldown_sec: float
    eof_cooldown_sec: float
    giveup_cooldown_sec: float
    max_restarts: int
    window_sec: float

    def __init__(
        self,
        cooldown_sec: float = ...,
        eof_cooldown_sec: float = ...,
        max_restarts: int = ...,
        window_sec: float = ...,
        clock: Optional[Callable[[], float]] = ...,
        on_give_up: Optional[Callable[[str], None]] = ...,
        giveup_cooldown_sec: float = ...,
    ) -> None: ...
    def on_eof(self, camera_id: str) -> bool: ...
    def on_error(self, camera_id: str, exc: Optional[Exception] = ...) -> bool: ...
    def reset(self, camera_id: str) -> None: ...
    def should_give_up(self, camera_id: str) -> bool: ...
