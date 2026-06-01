"""Core functionality for codrninja."""

import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from .config import Config
from .providers import ProviderManager
from .tools import ToolRegistry
from .sessions import SessionManager
from .git_integration import GitCheckpoint


class Session:
    """Represents a coding session."""

    def __init__(self, id: str, name: str, created_at: str, messages: List[Dict] = None, metadata: Optional[Dict[str, Any]] = None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.messages = messages or []
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "messages": self.messages,
            "metadata": self.metadata,
        }


class AICode:
    """Main class for codrninja functionality."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.config.ensure_db_dir()
        self._init_db()
        self.provider_manager = ProviderManager(self._build_provider_cfg())
        self.tools = ToolRegistry()
        self.session_manager = SessionManager()
        self.git = GitCheckpoint()

    def _init_db(self):
        conn = sqlite3.connect(self.config.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                model TEXT,
                tokens_input INTEGER,
                tokens_output INTEGER,
                created_at TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        conn.commit()
        conn.close()

    def create_session(self, name: str) -> Session:
        file_state = self.session_manager.create(
            name,
            model=self.config.default_model,
            provider=self.config.default_provider,
            git_branch=self.git.get_branch() or "",
        )

        conn = sqlite3.connect(self.config.db_path)
        c = conn.cursor()
        c.execute("SELECT id, created_at FROM sessions WHERE name = ?", (name,))
        existing = c.fetchone()
        if existing:
            conn.close()
            return Session(existing[0], name, existing[1], self._messages_from_file(name), metadata=file_state)

        sid = file_state.get("id") or str(uuid.uuid4())
        now = file_state.get("created_at") or datetime.now(timezone.utc).isoformat()
        c.execute(
            "INSERT INTO sessions (id, name, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (sid, name, now, now)
        )
        conn.commit()
        conn.close()
        return Session(sid, name, now, self._messages_from_file(name), metadata=file_state)

    def get_session(self, name: str) -> Optional[Session]:
        file_state = self.session_manager.get(name)
        if file_state:
            return Session(
                file_state.get("id", ""),
                file_state.get("name", name),
                file_state.get("created_at", ""),
                self._messages_from_file(file_state.get("name", name)),
                metadata=file_state,
            )

        conn = sqlite3.connect(self.config.db_path)
        c = conn.cursor()
        c.execute("SELECT id, name, created_at FROM sessions WHERE name = ?", (name,))
        row = c.fetchone()
        if not row:
            conn.close()
            return None
        c.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at",
            (row[0],)
        )
        messages = [{"role": r[0], "content": r[1]} for r in c.fetchall()]
        conn.close()
        return Session(row[0], row[1], row[2], messages)

    def list_sessions(self) -> List[Dict[str, str]]:
        file_sessions = self.session_manager.list_sessions()
        conn = sqlite3.connect(self.config.db_path)
        c = conn.cursor()
        c.execute("SELECT name, created_at, updated_at FROM sessions ORDER BY updated_at DESC")
        sqlite_sessions = {
            row[0]: {"name": row[0], "created_at": row[1], "updated_at": row[2]}
            for row in c.fetchall()
        }
        conn.close()

        result = []
        seen = set()
        for s in file_sessions:
            result.append({
                "id": s.get("id", ""),
                "name": s.get("name", ""),
                "slug": s.get("slug", ""),
                "created_at": s.get("created_at", ""),
                "updated_at": s.get("updated_at", s.get("created_at", "")),
                "status": s.get("status", "active"),
                "model": s.get("model", ""),
                "provider": s.get("provider", ""),
                "git_branch": s.get("git_branch", ""),
                "files_changed": s.get("files_changed", []),
            })
            seen.add(s.get("name"))

        for name, info in sqlite_sessions.items():
            if name not in seen:
                result.append(info)

        result.sort(key=lambda item: item.get("updated_at", item.get("created_at", "")), reverse=True)
        return result

    def _build_provider_cfg(self) -> dict:
        return {
            "provider": self.config.default_provider,
            "providers": {
                "ollama": {
                    "url": self.config.ollama_url,
                    "model": self.config.default_model,
                    "reasoning_level": self.config.reasoning_level,
                    "api_key": self.config.ollama_api_key,
                },
                "openai": {
                    "api_key": self.config.openai_api_key,
                    "model": self.config.default_model,
                    "reasoning_level": self.config.reasoning_level,
                },
                "anthropic": {
                    "api_key": self.config.anthropic_api_key,
                    "model": self.config.default_model,
                    "reasoning_level": self.config.reasoning_level,
                },
                "openrouter": {
                    "api_key": self.config.openrouter_api_key,
                    "model": self.config.default_model,
                    "reasoning_level": self.config.reasoning_level,
                },
                "claude-cli": {
                    "model": self.config.default_model,
                },
            },
        }

    def refresh_provider(self):
        self.provider_manager = ProviderManager(self._build_provider_cfg())

    def send_message(self, session_name: str, content: str, model: Optional[str] = None) -> Dict[str, Any]:
        session = self.get_session(session_name)
        if not session:
            session = self.create_session(session_name)

        messages = [{"role": "system", "content": self.config.system_prompt}]
        messages.extend(session.messages)
        messages.append({"role": "user", "content": content})

        try:
            provider = self.provider_manager.get_provider()
            result = provider.chat(messages, model)
        except Exception as e:
            return {"success": False, "error": str(e), "session": session_name}

        if result.get("error"):
            return {"success": False, "error": result["error"], "session": session_name}

        self._save_message(session.id, "user", content)
        self._save_message(
            session.id,
            "assistant",
            result.get("content", ""),
            model=result.get("model", model or self.config.default_model),
            tokens_in=result.get("tokens_input", 0),
            tokens_out=result.get("tokens_output", 0)
        )

        self.session_manager.append_message(
            session_name, "user", content,
            model=model or self.config.default_model,
        )
        self.session_manager.append_message(
            session_name, "assistant", result.get("content", ""),
            model=result.get("model", model or self.config.default_model),
            tokens_in=result.get("tokens_input", 0),
            tokens_out=result.get("tokens_output", 0),
        )

        return {
            "success": True,
            "response": result.get("content", ""),
            "session": session_name,
            "model": result.get("model", model or self.config.default_model),
            "tokens": {
                "input": result.get("tokens_input", 0),
                "output": result.get("tokens_output", 0)
            }
        }

    def _save_message(self, session_id: str, role: str, content: str,
                     model: Optional[str] = None, tokens_in: int = 0, tokens_out: int = 0):
        conn = sqlite3.connect(self.config.db_path)
        c = conn.cursor()
        mid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        c.execute(
            "INSERT INTO messages (id, session_id, role, content, model, tokens_input, tokens_output, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (mid, session_id, role, content, model, tokens_in, tokens_out, now)
        )
        c.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now, session_id))
        conn.commit()
        conn.close()

    def get_history(self, session_name: str) -> Optional[Dict[str, Any]]:
        session = self.get_session(session_name)
        if not session:
            return None
        return {
            "session": session.name,
            "created_at": session.created_at,
            "metadata": session.metadata,
            "messages": session.messages
        }

    def _messages_from_file(self, session_name: str) -> List[Dict[str, Any]]:
        return [
            {"role": m.get("role", ""), "content": m.get("content", "")}
            for m in self.session_manager.get_messages(session_name)
        ]
