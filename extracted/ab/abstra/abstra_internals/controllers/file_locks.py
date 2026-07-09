import dataclasses
import threading
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.logger import AbstraLogger

DEFAULT_HEARTBEAT_TTL = 90.0
DEFAULT_SWEEP_INTERVAL = 5.0


@dataclass(frozen=True)
class LockState:
    file_path: str
    holder_email: str
    holder_name: str
    session_id: str
    acquired_at: float
    last_heartbeat_at: float

    def to_dict(self) -> dict:
        return {
            "filePath": self.file_path,
            "holderEmail": self.holder_email,
            "holderName": self.holder_name,
            "sessionId": self.session_id,
            "acquiredAt": self.acquired_at,
            "lastHeartbeatAt": self.last_heartbeat_at,
        }


@dataclass(frozen=True)
class PresenceState:
    session_id: str
    email: str
    name: str
    current_file_path: Optional[str]
    last_heartbeat_at: float

    def to_dict(self) -> dict:
        return {
            "sessionId": self.session_id,
            "email": self.email,
            "name": self.name,
            "currentFilePath": self.current_file_path,
            "lastHeartbeatAt": self.last_heartbeat_at,
        }


class FileLockedException(Exception):
    def __init__(self, holder: LockState):
        self.holder = holder
        super().__init__(
            f"File '{holder.file_path}' is locked by "
            f"{holder.holder_name or holder.holder_email} ({holder.holder_email}), "
            "who is currently editing it in the web editor. "
            "Do not retry until the lock is released."
        )


class FileLockController:
    _locks: Dict[str, LockState] = {}
    _presence: Dict[str, PresenceState] = {}
    _lock = threading.Lock()
    _sweeper_started: bool = False

    @classmethod
    def reset_state(cls) -> None:
        with cls._lock:
            cls._locks.clear()
            cls._presence.clear()

    @classmethod
    def acquire(
        cls,
        file_path: str,
        session_id: str,
        email: str,
        name: str,
    ) -> Tuple[bool, Optional[LockState]]:
        now = time.time()
        broadcast_state: Optional[LockState] = None
        granted = False
        holder: Optional[LockState] = None

        with cls._lock:
            existing = cls._locks.get(file_path)
            if existing is None:
                created = LockState(
                    file_path=file_path,
                    holder_email=email,
                    holder_name=name,
                    session_id=session_id,
                    acquired_at=now,
                    last_heartbeat_at=now,
                )
                cls._locks[file_path] = created
                granted = True
                holder = created
                broadcast_state = created
            elif existing.holder_email == email and existing.session_id == session_id:
                renewed = dataclasses.replace(existing, last_heartbeat_at=now)
                cls._locks[file_path] = renewed
                granted = True
                holder = renewed
            else:
                granted = False
                holder = existing

        if broadcast_state is not None:
            cls._broadcast_lock_event("lock_acquired", broadcast_state)

        return granted, holder

    @classmethod
    def release(
        cls,
        file_path: str,
        session_id: str,
        email: str,
    ) -> bool:
        released_state: Optional[LockState] = None

        with cls._lock:
            existing = cls._locks.get(file_path)
            if existing is None:
                return False
            if existing.holder_email != email or existing.session_id != session_id:
                return False
            del cls._locks[file_path]
            released_state = existing

        cls._broadcast_lock_event("lock_released", released_state)
        return True

    @classmethod
    def heartbeat_lock(
        cls,
        file_path: str,
        session_id: str,
        email: str,
    ) -> Tuple[bool, Optional[LockState]]:
        now = time.time()
        with cls._lock:
            existing = cls._locks.get(file_path)
            if existing is None:
                return False, None
            if existing.holder_email != email or existing.session_id != session_id:
                return False, existing
            renewed = dataclasses.replace(existing, last_heartbeat_at=now)
            cls._locks[file_path] = renewed
            return True, renewed

    @classmethod
    def update_presence(
        cls,
        session_id: str,
        email: str,
        name: str,
        current_file_path: Optional[str],
    ) -> PresenceState:
        now = time.time()
        is_new = False

        with cls._lock:
            existing = cls._presence.get(session_id)
            if existing is None:
                is_new = True
                state = PresenceState(
                    session_id=session_id,
                    email=email,
                    name=name,
                    current_file_path=current_file_path,
                    last_heartbeat_at=now,
                )
            else:
                state = dataclasses.replace(
                    existing,
                    email=email,
                    name=name,
                    current_file_path=current_file_path,
                    last_heartbeat_at=now,
                )
            cls._presence[session_id] = state

        cls._broadcast_presence_event(
            "presence_joined" if is_new else "presence_update", state
        )
        return state

    @classmethod
    def remove_presence(cls, session_id: str) -> bool:
        removed_state: Optional[PresenceState] = None

        with cls._lock:
            existing = cls._presence.get(session_id)
            if existing is None:
                return False
            del cls._presence[session_id]
            removed_state = existing

        cls._broadcast_presence_event("presence_left", removed_state)
        return True

    @classmethod
    def release_for_path(cls, file_path: str) -> List[LockState]:
        released: List[LockState] = []
        prefix = file_path.rstrip("/") + "/"
        with cls._lock:
            for path in list(cls._locks.keys()):
                if path == file_path or path.startswith(prefix):
                    released.append(cls._locks.pop(path))

        for state in released:
            cls._broadcast_lock_event("lock_released", state)
        return released

    @classmethod
    def find_blocking_lock(
        cls, file_path: str, email: str, session_id: str
    ) -> Optional[LockState]:
        prefix = file_path.rstrip("/") + "/"
        with cls._lock:
            for path, state in cls._locks.items():
                if path != file_path and not path.startswith(prefix):
                    continue
                if state.holder_email == email and state.session_id == session_id:
                    continue
                return state
        return None

    @classmethod
    def get_all_locks(cls) -> List[LockState]:
        with cls._lock:
            return list(cls._locks.values())

    @classmethod
    def get_all_presence(cls) -> List[PresenceState]:
        with cls._lock:
            return list(cls._presence.values())

    @classmethod
    def sweep_once(
        cls, ttl: float = DEFAULT_HEARTBEAT_TTL
    ) -> Tuple[List[LockState], List[PresenceState]]:
        now = time.time()
        expired_locks: List[LockState] = []
        expired_presence: List[PresenceState] = []

        with cls._lock:
            for file_path, state in list(cls._locks.items()):
                if now - state.last_heartbeat_at > ttl:
                    expired_locks.append(state)
                    del cls._locks[file_path]
            for session_id, presence in list(cls._presence.items()):
                if now - presence.last_heartbeat_at > ttl:
                    expired_presence.append(presence)
                    del cls._presence[session_id]

        for state in expired_locks:
            cls._broadcast_lock_event("lock_released", state)
        for presence in expired_presence:
            cls._broadcast_presence_event("presence_left", presence)

        return expired_locks, expired_presence

    @classmethod
    def _broadcast_lock_event(cls, event_type: str, state: LockState) -> None:
        try:
            CodebaseEventController.broadcast_raw(
                {
                    "filepath": state.file_path,
                    "event": event_type,
                    "lock": state.to_dict(),
                }
            )
        except Exception as e:
            AbstraLogger.capture_exception(e)

    @classmethod
    def _broadcast_presence_event(
        cls, event_type: str, presence: PresenceState
    ) -> None:
        try:
            CodebaseEventController.broadcast_raw(
                {
                    "filepath": presence.current_file_path or "",
                    "event": event_type,
                    "presence": presence.to_dict(),
                }
            )
        except Exception as e:
            AbstraLogger.capture_exception(e)


def start_sweeper(
    interval: float = DEFAULT_SWEEP_INTERVAL,
    ttl: float = DEFAULT_HEARTBEAT_TTL,
    log_exception: Optional[Callable[[Exception], None]] = None,
) -> Optional[threading.Thread]:
    if FileLockController._sweeper_started:
        return None

    def _loop() -> None:
        while True:
            try:
                time.sleep(interval)
                FileLockController.sweep_once(ttl=ttl)
            except Exception as exc:
                if log_exception is not None:
                    log_exception(exc)
                else:
                    AbstraLogger.capture_exception(exc)

    thread = threading.Thread(target=_loop, daemon=True, name="FileLockSweeper")
    thread.start()
    FileLockController._sweeper_started = True
    return thread
