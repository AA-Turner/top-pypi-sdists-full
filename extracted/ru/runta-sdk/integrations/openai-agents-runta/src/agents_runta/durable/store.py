from __future__ import annotations

import json
import re
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


DurableRunStatus = Literal["created", "running", "completed", "interrupted", "failed"]


class DurableSessionNotFoundError(FileNotFoundError):
    """Raised when a local durable session pointer cannot be found."""


@dataclass
class DurableSessionRecord:
    durable_id: str
    sqlite_session_id: str
    status: DurableRunStatus = "created"
    state_version: int = 1
    sandbox_session_state: dict[str, Any] | None = None
    run_state_json: dict[str, Any] | None = None
    last_error: dict[str, str] | None = None
    created_at: str = field(default_factory=lambda: _utc_now())
    updated_at: str = field(default_factory=lambda: _utc_now())

    @classmethod
    def new(cls, durable_id: str | None = None) -> DurableSessionRecord:
        resolved_id = durable_id or f"ds_{uuid.uuid4().hex[:16]}"
        return cls(durable_id=resolved_id, sqlite_session_id=resolved_id)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> DurableSessionRecord:
        return cls(
            durable_id=str(payload["durable_id"]),
            sqlite_session_id=str(payload.get("sqlite_session_id") or payload["durable_id"]),
            status=_status(payload.get("status", "created")),
            state_version=int(payload.get("state_version", 1)),
            sandbox_session_state=_optional_dict(payload.get("sandbox_session_state")),
            run_state_json=_optional_dict(payload.get("run_state_json")),
            last_error=_optional_str_dict(payload.get("last_error")),
            created_at=str(payload.get("created_at") or _utc_now()),
            updated_at=str(payload.get("updated_at") or _utc_now()),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_version": self.state_version,
            "durable_id": self.durable_id,
            "sqlite_session_id": self.sqlite_session_id,
            "status": self.status,
            "sandbox_session_state": self.sandbox_session_state,
            "run_state_json": self.run_state_json,
            "last_error": self.last_error,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def touch(self) -> None:
        self.updated_at = _utc_now()


class DurablePointerStore:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = resolve_state_dir(root)

    @property
    def sqlite_path(self) -> Path:
        return self.root / "conversation.sqlite"

    @property
    def last_session_path(self) -> Path:
        return self.root / "last-session.json"

    @property
    def unfinished_session_path(self) -> Path:
        return self.root / "unfinished-session.json"

    @property
    def sessions_dir(self) -> Path:
        return self.root / "sessions"

    def create(self, durable_id: str | None = None) -> DurableSessionRecord:
        record = DurableSessionRecord.new(durable_id)
        self.save(record)
        return record

    def load(self, durable_id: str) -> DurableSessionRecord:
        path = self._session_path(durable_id)
        if not path.exists():
            raise DurableSessionNotFoundError(f"durable session not found: {durable_id}")
        return DurableSessionRecord.from_dict(_read_json(path))

    def load_last(self) -> DurableSessionRecord:
        if not self.last_session_path.exists():
            raise DurableSessionNotFoundError("no last durable session pointer exists")
        payload = _read_json(self.last_session_path)
        durable_id = payload.get("durable_id")
        if not isinstance(durable_id, str) or not durable_id:
            raise DurableSessionNotFoundError("last durable session pointer is invalid")
        return self.load(durable_id)

    def load_unfinished(self) -> DurableSessionRecord:
        if not self.unfinished_session_path.exists():
            raise DurableSessionNotFoundError("no unfinished durable session pointer exists")
        payload = _read_json(self.unfinished_session_path)
        durable_id = payload.get("durable_id")
        if not isinstance(durable_id, str) or not durable_id:
            raise DurableSessionNotFoundError("unfinished durable session pointer is invalid")
        record = self.load(durable_id)
        if record.status == "completed":
            raise DurableSessionNotFoundError("unfinished durable session is already completed")
        return record

    def save(self, record: DurableSessionRecord, *, set_last: bool = True) -> None:
        record.touch()
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        _write_json(self._session_path(record.durable_id), record.to_dict())
        if set_last:
            _write_json(
                self.last_session_path,
                {
                    "durable_id": record.durable_id,
                    "status": record.status,
                    "updated_at": record.updated_at,
                },
            )
        if record.status == "completed":
            self._clear_unfinished_pointer(record)
        else:
            _write_json(
                self.unfinished_session_path,
                {
                    "durable_id": record.durable_id,
                    "status": record.status,
                    "updated_at": record.updated_at,
                },
            )

    def _session_path(self, durable_id: str) -> Path:
        if "/" in durable_id or "\\" in durable_id:
            raise ValueError("durable_id must not contain path separators")
        return self.sessions_dir / f"{durable_id}.json"

    def _clear_unfinished_pointer(self, record: DurableSessionRecord) -> None:
        if not self.unfinished_session_path.exists():
            return
        try:
            payload = _read_json(self.unfinished_session_path)
        except (OSError, ValueError):
            return
        if payload.get("durable_id") == record.durable_id:
            self.unfinished_session_path.unlink()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resolve_state_dir(state_dir: str | Path | None = None) -> Path:
    if state_dir is not None:
        return Path(state_dir)
    return default_state_dir()


def default_state_dir(script_path: str | Path | None = None) -> Path:
    script_name = _script_stem(script_path)
    safe_name = re.sub(r"[^\w.-]+", "_", script_name).strip("._-")
    if not safe_name:
        safe_name = "session"
    return Path.cwd() / f".runta_{safe_name}"


def _script_stem(script_path: str | Path | None = None) -> str:
    raw_path = str(script_path if script_path is not None else (sys.argv[0] if sys.argv else ""))
    if not raw_path or raw_path == "-c":
        return "session"
    return Path(raw_path).stem or "session"


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object in {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f"{path.suffix}.tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _optional_dict(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("expected object or null")
    return value


def _optional_str_dict(value: Any) -> dict[str, str] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("expected object or null")
    return {str(key): str(item) for key, item in value.items()}


def _status(value: Any) -> DurableRunStatus:
    if value in {"created", "running", "completed", "interrupted", "failed"}:
        return value
    raise ValueError(f"invalid durable run status: {value!r}")
