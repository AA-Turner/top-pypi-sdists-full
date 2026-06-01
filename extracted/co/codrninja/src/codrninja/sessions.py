"""Improved session management with persistent files and machine-readable state."""

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class SessionManager:
    """Manages sessions with file-based persistence alongside SQLite.

    Each session gets a directory under ~/.codrninja/sessions/<slug>/ containing:
      - state.json       : metadata (id, name, created, model, provider, status, git_branch)
      - messages.jsonl   : append-only chat history
      - events.jsonl     : tool calls, diffs, errors, status changes
      - artifacts.jsonl  : files created/modified references
    """

    SESSIONS_DIR = os.path.expanduser("~/.codrninja/sessions")

    def __init__(self, sessions_dir: Optional[str] = None):
        self.sessions_dir = Path(sessions_dir or self.SESSIONS_DIR)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_name(self, name: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", name.strip()).strip("-._").lower()
        return slug or f"session-{uuid.uuid4().hex[:8]}"

    def resolve_session_name(self, name: str) -> Optional[str]:
        state = self.get(name)
        if state:
            return state.get("name", name)
        return None

    def create(self, name: str, model: str = "", provider: str = "",
               git_branch: str = "") -> Dict[str, Any]:
        """Create a new session directory with state.json."""
        existing = self.get(name)
        if existing:
            return existing

        slug = self.sanitize_name(name)
        session_dir = self.sessions_dir / slug
        if session_dir.exists() and self._read_state(session_dir):
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
            session_dir = self.sessions_dir / slug

        session_dir.mkdir(parents=True, exist_ok=True)
        return self._init_state(session_dir, name, model, provider, git_branch, slug)

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get session state by name, slug, or id."""
        direct = self._read_state(self.sessions_dir / name)
        if direct:
            return direct

        for entry in self.sessions_dir.iterdir():
            if not entry.is_dir():
                continue
            state = self._read_state(entry)
            if not state:
                continue
            if state.get("name") == name or state.get("id") == name or state.get("slug") == name:
                return state
        return None

    def get_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.get(session_id)

    def list_sessions(self) -> List[Dict[str, Any]]:
        sessions = []
        for entry in self.sessions_dir.iterdir():
            if not entry.is_dir():
                continue
            state = self._read_state(entry)
            if state:
                sessions.append(state)
        sessions.sort(key=lambda item: item.get("updated_at", item.get("created_at", "")), reverse=True)
        return sessions

    def delete(self, name: str) -> bool:
        """Delete a session directory. Returns True if deleted, False if not found."""
        import shutil
        state = self.get(name)
        if not state:
            return False
        slug = state.get("slug") or self.sanitize_name(name)
        session_dir = self.sessions_dir / slug
        if session_dir.exists():
            shutil.rmtree(str(session_dir))
        return True

    def rename(self, old_name: str, new_name: str) -> bool:
        """Rename a session. Returns True on success, False if not found."""
        state = self.get(old_name)
        if not state:
            return False
        slug = state.get("slug") or self.sanitize_name(old_name)
        session_dir = self.sessions_dir / slug
        if not session_dir.exists():
            return False
        state["name"] = new_name
        state_file = session_dir / "state.json"
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
        return True

    def get_last_updated(self, name: str) -> Optional[str]:
        state = self.get(name)
        if not state:
            return None
        return state.get("updated_at") or state.get("created_at")

    def append_message(self, name: str, role: str, content: str,
                       model: str = "", tokens_in: int = 0, tokens_out: int = 0) -> Dict[str, Any]:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "role": role,
            "content": content,
            "model": model,
            "tokens_input": tokens_in,
            "tokens_output": tokens_out,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._append_jsonl(name, "messages.jsonl", entry)
        self._touch_state(name)
        return entry

    def get_messages(self, name: str, limit: Optional[int] = None,
                     since: Optional[str] = None) -> List[Dict[str, Any]]:
        messages = self._read_jsonl(name, "messages.jsonl")
        if since:
            messages = [m for m in messages if m.get("timestamp", "") > since]
        if limit:
            messages = messages[-limit:]
        return messages

    def append_event(self, name: str, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._append_jsonl(name, "events.jsonl", entry)
        self._touch_state(name)
        return entry

    def get_events(self, name: str, event_type: Optional[str] = None,
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        events = self._read_jsonl(name, "events.jsonl")
        if event_type:
            events = [e for e in events if e.get("type") == event_type]
        if limit:
            events = events[-limit:]
        return events

    def append_artifact(self, name: str, path: str, action: str,
                        diff: str = "") -> Dict[str, Any]:
        entry = {
            "id": uuid.uuid4().hex[:12],
            "path": path,
            "action": action,
            "diff": diff,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._append_jsonl(name, "artifacts.jsonl", entry)
        state = self.get(name)
        files_changed = list(state.get("files_changed", [])) if state else []
        if path not in files_changed:
            files_changed.append(path)
        self.update_state(name, files_changed=files_changed)
        return entry

    def get_artifacts(self, name: str, action: Optional[str] = None) -> List[Dict[str, Any]]:
        artifacts = self._read_jsonl(name, "artifacts.jsonl")
        if action:
            artifacts = [a for a in artifacts if a.get("action") == action]
        return artifacts

    def update_state(self, name: str, **kwargs) -> Optional[Dict[str, Any]]:
        state = self.get(name)
        if not state:
            return None
        state.update(kwargs)
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._write_state(state.get("slug") or name, state)
        return state

    def set_status(self, name: str, status: str) -> Optional[Dict[str, Any]]:
        return self.update_state(name, status=status)

    def save_patch(self, name: str, patch_content: str, label: str = "") -> Dict[str, Any]:
        state = self.get(name)
        if not state:
            raise FileNotFoundError(f"Unknown session: {name}")
        slug = state.get("slug") or self.sanitize_name(name)
        patches_dir = self.sessions_dir / slug / "patches"
        patches_dir.mkdir(exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        patch_id = f"{ts}-{uuid.uuid4().hex[:6]}"
        patch_file = patches_dir / f"{patch_id}.patch"
        patch_file.write_text(patch_content)
        meta = {
            "id": patch_id,
            "label": label or patch_id,
            "file": str(patch_file),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.append_event(name, "patch_saved", meta)
        return meta

    def list_patches(self, name: str) -> List[Dict[str, Any]]:
        return self.get_events(name, event_type="patch_saved")

    def _session_dir(self, name: str) -> Path:
        state = self.get(name)
        if state and state.get("slug"):
            return self.sessions_dir / state["slug"]
        return self.sessions_dir / self.sanitize_name(name)

    def _init_state(self, session_dir: Path, name: str, model: str,
                    provider: str, git_branch: str, slug: str) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        state = {
            "id": str(uuid.uuid4()),
            "name": name,
            "slug": slug,
            "status": "active",
            "created_at": now,
            "updated_at": now,
            "model": model,
            "provider": provider,
            "git_branch": git_branch,
            "message_count": 0,
            "event_count": 0,
            "files_changed": [],
        }
        (session_dir / "state.json").write_text(json.dumps(state, indent=2))
        for fname in ("messages.jsonl", "events.jsonl", "artifacts.jsonl"):
            (session_dir / fname).touch()
        return state

    def _read_state(self, session_dir: Path) -> Optional[Dict[str, Any]]:
        state_file = session_dir / "state.json"
        if not state_file.exists():
            return None
        try:
            state = json.loads(state_file.read_text())
            if "slug" not in state:
                state["slug"] = session_dir.name
            return state
        except (json.JSONDecodeError, OSError):
            return None

    def update_model(self, name: str, model: str, provider: str = "") -> bool:
        """Persist a model (and optionally provider) change to a session's state.json."""
        state = self.get(name)
        if not state:
            return False
        state["model"] = model
        if provider:
            state["provider"] = provider
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._write_state(state.get("slug") or name, state)
        return True

    def _write_state(self, name: str, state: Dict[str, Any]):
        state_file = self._session_dir(name) / "state.json"
        state_file.write_text(json.dumps(state, indent=2))

    def _touch_state(self, name: str):
        state = self.get(name)
        if state:
            state["updated_at"] = datetime.now(timezone.utc).isoformat()
            state["message_count"] = len(self.get_messages(name))
            state["event_count"] = len(self.get_events(name))
            self._write_state(state.get("slug") or name, state)

    def _append_jsonl(self, name: str, filename: str, entry: Dict[str, Any]):
        path = self._session_dir(name) / filename
        with open(path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _read_jsonl(self, name: str, filename: str) -> List[Dict[str, Any]]:
        path = self._session_dir(name) / filename
        if not path.exists():
            return []
        entries = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return entries
