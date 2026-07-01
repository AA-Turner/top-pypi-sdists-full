"""
cvc.dashboard.dx_api — Developer-experience (DX) routes for the dashboard chat.

Telegram-style features wired into the existing conversations.db store:

  • Slash-command registry + executor      → /api/dx/slash/*
  • Message reply / quote (telegram-style) → /api/dx/messages/{id}/reply
  • Pin messages                            → /api/dx/messages/{id}/pin
  • Persistent insights (self-learning)     → /api/dx/insights/*
  • Workspace file fuzzy search (@-picker)  → /api/dx/files/search
  • Session cost ticker                     → /api/dx/cost
  • Session export (md/json)                → /api/dx/threads/{id}/export
  • Context build helper                    → /api/dx/threads/{id}/context

All endpoints are additive — they never mutate the existing /api/chat
or /api/conversations contracts. Schema extensions on `messages` and
new `insights`/`pins` rows are gated behind `ALTER TABLE ... IF NOT
EXISTS` semantics (SQLite quirks handled).

Mounted by gateway.py via include_router(router).
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, List, Optional

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

# Re-use the same DB the conversations router uses.
from cvc.dashboard.conversations_api import DB_PATH, HOSTNAME, _conn as _conv_conn  # type: ignore

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dx", tags=["dx"])


# ── Schema extensions ───────────────────────────────────────────────────


def _table_columns(c: sqlite3.Connection, table: str) -> set[str]:
    cur = c.execute(f"PRAGMA table_info({table})")
    return {r[1] for r in cur.fetchall()}


def _ensure_dx_schema() -> None:
    """Idempotently extend the conversations DB with DX columns / tables."""
    with _conv_conn() as c:  # type: sqlite3.Connection
        cols = _table_columns(c, "messages")
        # Add columns one-by-one — SQLite has no ADD COLUMN IF NOT EXISTS.
        if "reply_to" not in cols:
            c.execute("ALTER TABLE messages ADD COLUMN reply_to INTEGER")
        if "pinned" not in cols:
            c.execute("ALTER TABLE messages ADD COLUMN pinned INTEGER DEFAULT 0")
        if "meta" not in cols:
            c.execute("ALTER TABLE messages ADD COLUMN meta TEXT")

        c.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_messages_pinned
              ON messages(thread_id, pinned) WHERE pinned = 1;
            CREATE INDEX IF NOT EXISTS idx_messages_reply
              ON messages(reply_to);

            CREATE TABLE IF NOT EXISTS insights (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                workspace_path TEXT NOT NULL,
                thread_id   TEXT,
                kind        TEXT NOT NULL,    -- preference | fact | pitfall | decision | rule
                content     TEXT NOT NULL,
                source      TEXT,             -- "manual" | "auto" | message_id
                weight      REAL DEFAULT 1.0, -- decays over time, boosted on reuse
                created_at  REAL NOT NULL,
                last_used   REAL NOT NULL,
                use_count   INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_insights_ws
              ON insights(workspace_path, weight DESC);
            CREATE INDEX IF NOT EXISTS idx_insights_kind
              ON insights(kind);

            CREATE TABLE IF NOT EXISTS slash_runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id   TEXT,
                command     TEXT NOT NULL,
                args        TEXT,
                result      TEXT,
                ok          INTEGER DEFAULT 1,
                created_at  REAL NOT NULL
            );
            """
        )


_ensure_dx_schema()


# ── Models ──────────────────────────────────────────────────────────────


class ReplyRequest(BaseModel):
    role: str = Field("user", pattern="^(user|assistant|system|tool)$")
    content: str
    reply_to: int


class PinRequest(BaseModel):
    pinned: bool = True


class InsightCreate(BaseModel):
    workspace_path: str
    kind: str = Field("fact", pattern="^(preference|fact|pitfall|decision|rule)$")
    content: str
    thread_id: Optional[str] = None
    source: Optional[str] = "manual"


class InsightUpdate(BaseModel):
    content: Optional[str] = None
    kind: Optional[str] = None
    weight: Optional[float] = None


class SlashRunRequest(BaseModel):
    command: str
    thread_id: Optional[str] = None
    args: Optional[dict] = None


# ════════════════════════════════════════════════════════════════════════
# 1. REPLY  (telegram-style quote: each message can reference an earlier one)
# ════════════════════════════════════════════════════════════════════════


@router.post("/threads/{thread_id}/reply")
def reply_to_message(thread_id: str, body: ReplyRequest) -> dict:
    """
    Append a message that quotes an earlier message by ID.
    The quoted message's id is stored in `reply_to`; the agent loop will
    surface it as a `> quoted text` prefix when building LLM context.
    """
    now = time.time()
    with _conv_conn() as c:
        thread = c.execute(
            "SELECT id FROM threads WHERE id = ?", (thread_id,)
        ).fetchone()
        if not thread:
            raise HTTPException(404, f"Thread not found: {thread_id}")

        parent = c.execute(
            "SELECT id, role, content FROM messages WHERE id = ? AND thread_id = ?",
            (body.reply_to, thread_id),
        ).fetchone()
        if not parent:
            raise HTTPException(404, f"Parent message {body.reply_to} not in thread")

        cur = c.execute(
            "INSERT INTO messages (thread_id, role, content, created_at, reply_to) "
            "VALUES (?, ?, ?, ?, ?)",
            (thread_id, body.role, body.content, now, body.reply_to),
        )
        c.execute("UPDATE threads SET updated_at = ? WHERE id = ?", (now, thread_id))
        new_id = cur.lastrowid

    return {
        "ok": True,
        "message_id": new_id,
        "thread_id": thread_id,
        "reply_to": body.reply_to,
        "parent_preview": (parent["content"] or "")[:140],
    }


# ════════════════════════════════════════════════════════════════════════
# 2. PIN  (mark message as important — auto-injected into next LLM turn)
# ════════════════════════════════════════════════════════════════════════


@router.post("/messages/{message_id}/pin")
def pin_message(message_id: int, body: PinRequest) -> dict:
    with _conv_conn() as c:
        row = c.execute(
            "SELECT id, thread_id FROM messages WHERE id = ?", (message_id,)
        ).fetchone()
        if not row:
            raise HTTPException(404, f"Message not found: {message_id}")
        c.execute(
            "UPDATE messages SET pinned = ? WHERE id = ?",
            (1 if body.pinned else 0, message_id),
        )
    return {"ok": True, "message_id": message_id, "pinned": body.pinned}


@router.get("/threads/{thread_id}/pinned")
def list_pinned(thread_id: str) -> dict:
    with _conv_conn() as c:
        rows = c.execute(
            "SELECT id, role, content, created_at, reply_to "
            "FROM messages WHERE thread_id = ? AND pinned = 1 "
            "ORDER BY created_at ASC",
            (thread_id,),
        ).fetchall()
    return {
        "thread_id": thread_id,
        "count": len(rows),
        "messages": [dict(r) for r in rows],
    }


# ════════════════════════════════════════════════════════════════════════
# 3. INSIGHTS  (persistent self-learning store)
# ════════════════════════════════════════════════════════════════════════


@router.get("/insights")
def list_insights(
    workspace_path: str = Query(...),
    kind: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
) -> dict:
    with _conv_conn() as c:
        if kind:
            rows = c.execute(
                "SELECT * FROM insights WHERE workspace_path = ? AND kind = ? "
                "ORDER BY weight DESC, last_used DESC LIMIT ?",
                (workspace_path, kind, limit),
            ).fetchall()
        else:
            rows = c.execute(
                "SELECT * FROM insights WHERE workspace_path = ? "
                "ORDER BY weight DESC, last_used DESC LIMIT ?",
                (workspace_path, limit),
            ).fetchall()
    return {"count": len(rows), "insights": [dict(r) for r in rows]}


@router.post("/insights")
def create_insight(body: InsightCreate) -> dict:
    now = time.time()
    content = (body.content or "").strip()
    if not content:
        raise HTTPException(400, "content is required")
    with _conv_conn() as c:
        cur = c.execute(
            "INSERT INTO insights "
            "(workspace_path, thread_id, kind, content, source, weight, created_at, last_used) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (body.workspace_path, body.thread_id, body.kind, content,
             body.source or "manual", 1.0, now, now),
        )
        new_id = cur.lastrowid
    return {"ok": True, "id": new_id, "kind": body.kind, "content": content}


@router.patch("/insights/{insight_id}")
def update_insight(insight_id: int, body: InsightUpdate) -> dict:
    with _conv_conn() as c:
        row = c.execute("SELECT * FROM insights WHERE id = ?", (insight_id,)).fetchone()
        if not row:
            raise HTTPException(404, f"Insight not found: {insight_id}")
        fields, vals = [], []
        if body.content is not None:
            fields.append("content = ?"); vals.append(body.content.strip())
        if body.kind is not None:
            fields.append("kind = ?"); vals.append(body.kind)
        if body.weight is not None:
            fields.append("weight = ?"); vals.append(float(body.weight))
        if not fields:
            return {"ok": True, "id": insight_id, "unchanged": True}
        vals.append(insight_id)
        c.execute(f"UPDATE insights SET {', '.join(fields)} WHERE id = ?", vals)
    return {"ok": True, "id": insight_id}


@router.delete("/insights/{insight_id}")
def delete_insight(insight_id: int) -> dict:
    with _conv_conn() as c:
        cur = c.execute("DELETE FROM insights WHERE id = ?", (insight_id,))
    return {"ok": True, "deleted": cur.rowcount}


def _touch_insight(c: sqlite3.Connection, insight_id: int) -> None:
    """Internal: bump weight + last_used on each use (self-learning signal)."""
    now = time.time()
    c.execute(
        "UPDATE insights SET last_used = ?, use_count = use_count + 1, "
        "weight = MIN(weight + 0.1, 5.0) WHERE id = ?",
        (now, insight_id),
    )


# ════════════════════════════════════════════════════════════════════════
# 4. SLASH COMMANDS  (registry + executor + history)
# ════════════════════════════════════════════════════════════════════════


# Static registry. Frontend hits /slash/registry to render the palette.
# Each command names the route it expands to so the FE can fire it directly
# OR let the gateway run it via /slash/run for headless contexts (voice).
# Each entry:
#   cmd            : "/name"  — canonical token (with leading slash)
#   group          : palette grouping (git, workspace, agent, memory, chat, ...)
#   desc           : one-line description shown in palette
#   args           : argument schema (used by future arg-picker UI)
#   exec           : dispatch strategy — one of:
#                      "client" — FE handles via `client_action`
#                      "route"  — FE issues HTTP request to `route`
#                      "agent"  — FE forwards "/cmd arg" to the agent loop
#                                 as a user message (CLI parity passthrough)
#   client_action  : opaque key the FE switches on when exec == "client"
#   route          : "METHOD /api/..." string when exec == "route"
#   alias_of       : if set, this command is an alias of another (collapsed in palette)
SLASH_REGISTRY: list[dict[str, Any]] = [
    # ── Git ────────────────────────────────────────────────────────────
    {"cmd": "/branch",        "group": "git", "desc": "Switch git branch",
     "args": [{"name": "name", "type": "branch"}],
     "exec": "client", "client_action": "open_branch_picker",
     "route": "POST /api/git/checkout"},
    {"cmd": "/branches",      "group": "git", "desc": "List all branches",
     "args": [], "exec": "agent"},
    {"cmd": "/checkout",      "group": "git", "desc": "Checkout branch / commit",
     "args": [{"name": "ref", "type": "string"}], "exec": "agent"},
    {"cmd": "/status",        "group": "git", "desc": "Show git + CVC status",
     "args": [], "exec": "route", "route": "GET /api/git/status"},
    {"cmd": "/sync",          "group": "git", "desc": "Pull + push current branch",
     "args": [], "exec": "route", "route": "POST /api/git/sync"},
    {"cmd": "/commit",        "group": "git", "desc": "Stage all + commit checkpoint",
     "args": [{"name": "message", "type": "string"}],
     "exec": "route", "route": "POST /api/ops/commit"},
    {"cmd": "/diff",          "group": "git", "desc": "Show diff vs HEAD",
     "args": [], "exec": "route", "route": "GET /api/ops/diff"},
    {"cmd": "/log",           "group": "git", "desc": "Show commit log",
     "args": [], "exec": "agent"},
    {"cmd": "/git",           "group": "git", "desc": "Run arbitrary git subcommand",
     "args": [{"name": "subcommand", "type": "string"}], "exec": "agent"},
    {"cmd": "/merge",         "group": "git", "desc": "Merge a branch into current",
     "args": [{"name": "branch", "type": "branch"}], "exec": "agent"},
    {"cmd": "/fork",          "group": "git", "desc": "Fork current branch",
     "args": [{"name": "name", "type": "string"}], "exec": "agent"},
    {"cmd": "/restore",       "group": "git", "desc": "Restore from checkpoint",
     "args": [{"name": "ref", "type": "string"}], "exec": "agent"},
    {"cmd": "/undo",          "group": "git", "desc": "Undo last action",
     "args": [], "exec": "agent"},
    {"cmd": "/rewind",        "group": "git", "desc": "Rewind conversation N turns",
     "args": [{"name": "n", "type": "string"}], "exec": "agent"},

    # ── Workspace ──────────────────────────────────────────────────────
    {"cmd": "/cd",            "group": "workspace", "desc": "Switch workspace directory",
     "args": [{"name": "path", "type": "string"}],
     "exec": "client", "client_action": "open_workspace_picker",
     "route": "POST /api/workspace/switch"},
    {"cmd": "/add-dir",       "group": "workspace", "desc": "Add additional directory to workspace",
     "args": [{"name": "path", "type": "string"}], "exec": "agent"},
    {"cmd": "/files",         "group": "workspace", "desc": "List / search workspace files",
     "args": [{"name": "query", "type": "string"}], "exec": "agent"},
    {"cmd": "/search",        "group": "workspace", "desc": "Grep search across workspace",
     "args": [{"name": "pattern", "type": "string"}], "exec": "agent"},
    {"cmd": "/smartsearch",   "group": "workspace", "desc": "Semantic search via embeddings",
     "args": [{"name": "query", "type": "string"}], "exec": "agent"},
    {"cmd": "/tree",          "group": "workspace", "desc": "Show workspace file tree",
     "args": [], "exec": "route", "route": "GET /api/workspace/tree"},

    # ── Documents / RAG ────────────────────────────────────────────────
    {"cmd": "/ingest",        "group": "docs", "desc": "Ingest a document/folder for RAG",
     "args": [{"name": "path", "type": "string"}], "exec": "agent"},
    {"cmd": "/documents",     "group": "docs", "desc": "List ingested documents",
     "args": [], "exec": "agent"},
    {"cmd": "/docsearch",     "group": "docs", "desc": "Search ingested documents",
     "args": [{"name": "query", "type": "string"}], "exec": "agent"},
    {"cmd": "/web",           "group": "docs", "desc": "Search the web / fetch URL",
     "args": [{"name": "query", "type": "string"}], "exec": "agent"},
    {"cmd": "/image",         "group": "docs", "desc": "Attach an image to the conversation",
     "args": [{"name": "path", "type": "string"}], "exec": "agent"},
    {"cmd": "/paste",         "group": "docs", "desc": "Paste clipboard content",
     "args": [], "exec": "agent"},

    # ── Models / Persona / Reasoning ───────────────────────────────────
    {"cmd": "/model",         "group": "agent", "desc": "Switch agent model",
     "args": [{"name": "model", "type": "model"}],
     "exec": "client", "client_action": "open_model_picker",
     "route": "POST /api/models/switch"},
    {"cmd": "/provider",      "group": "agent", "desc": "Switch model provider",
     "args": [{"name": "provider", "type": "string"}], "exec": "agent"},
    {"cmd": "/persona",       "group": "agent", "desc": "Switch persona",
     "args": [{"name": "persona", "type": "string"}],
     "exec": "client", "client_action": "open_persona_picker"},
    {"cmd": "/think",         "group": "agent", "desc": "Set thinking / reasoning depth",
     "args": [{"name": "level", "type": "enum",
               "choices": ["none", "minimal", "low", "medium", "high", "xhigh"]}],
     "exec": "route", "route": "PUT /api/chat/reasoning_effort"},
    {"cmd": "/effort",        "group": "agent", "desc": "Alias of /think",
     "args": [{"name": "level", "type": "enum",
               "choices": ["none", "minimal", "low", "medium", "high", "xhigh"]}],
     "exec": "route", "route": "PUT /api/chat/reasoning_effort",
     "alias_of": "/think"},
    {"cmd": "/fast",          "group": "agent", "desc": "Toggle fast/cheap model mode",
     "args": [], "exec": "agent"},
    {"cmd": "/agent",         "group": "agent", "desc": "Create / configure a subagent",
     "args": [{"name": "spec", "type": "string"}], "exec": "agent"},
    {"cmd": "/agents",        "group": "agent", "desc": "List registered subagents",
     "args": [], "exec": "agent"},
    {"cmd": "/tasks",         "group": "agent", "desc": "Show active background tasks",
     "args": [], "exec": "agent"},
    {"cmd": "/hooks",         "group": "agent", "desc": "List / configure hooks",
     "args": [], "exec": "agent"},
    {"cmd": "/skill",         "group": "agent", "desc": "Load / inspect a skill",
     "args": [{"name": "name", "type": "string"}], "exec": "agent"},
    {"cmd": "/skills",        "group": "agent", "desc": "List available skills",
     "args": [], "exec": "agent", "alias_of": "/skill"},
    {"cmd": "/plugin",        "group": "agent", "desc": "Manage plugins",
     "args": [], "exec": "agent"},
    {"cmd": "/plugins",       "group": "agent", "desc": "List installed plugins",
     "args": [], "exec": "agent", "alias_of": "/plugin"},
    {"cmd": "/distill",       "group": "agent", "desc": "Distill conversation into a skill",
     "args": [], "exec": "agent"},
    {"cmd": "/cogs",          "group": "agent", "desc": "List / manage cognitive gears",
     "args": [{"name": "name", "type": "string"}], "exec": "agent"},
    {"cmd": "/hive",          "group": "agent", "desc": "Hivemind operations",
     "args": [{"name": "subcommand", "type": "string"}], "exec": "agent"},

    # ── Memory / Self-learning ─────────────────────────────────────────
    {"cmd": "/memory",        "group": "memory", "desc": "Show / edit long-term memory",
     "args": [], "exec": "agent"},
    {"cmd": "/remember",      "group": "memory", "desc": "Save an insight",
     "args": [{"name": "kind", "type": "enum",
               "choices": ["preference", "fact", "pitfall", "decision", "rule"]},
              {"name": "content", "type": "string"}],
     "exec": "route", "route": "POST /api/dx/insights"},
    {"cmd": "/insights",      "group": "memory", "desc": "Show saved insights",
     "args": [], "exec": "client", "client_action": "open_insights_panel",
     "route": "GET /api/dx/insights"},
    {"cmd": "/pin",           "group": "memory", "desc": "Pin the selected message",
     "args": [], "exec": "client", "client_action": "pin_selected_message"},
    {"cmd": "/pins",          "group": "memory", "desc": "List pinned messages",
     "args": [], "exec": "client", "client_action": "open_pins_panel"},
    {"cmd": "/context",       "group": "memory", "desc": "Show current context window",
     "args": [], "exec": "agent"},
    {"cmd": "/summary",       "group": "memory", "desc": "Summarise conversation so far",
     "args": [], "exec": "agent"},
    {"cmd": "/compact",       "group": "memory", "desc": "Compact context (free tokens)",
     "args": [], "exec": "route", "route": "POST /api/hivemind/memory/compact"},
    {"cmd": "/continue",      "group": "memory", "desc": "Continue / resume after compact",
     "args": [], "exec": "agent"},

    # ── Chat lifecycle ─────────────────────────────────────────────────
    {"cmd": "/new",           "group": "chat", "desc": "New chat thread",
     "args": [], "exec": "client", "client_action": "new_thread"},
    {"cmd": "/clear",         "group": "chat", "desc": "Clear current thread",
     "args": [], "exec": "client", "client_action": "clear_thread"},
    {"cmd": "/sessions",      "group": "chat", "desc": "List chat sessions",
     "args": [], "exec": "client", "client_action": "open_sessions_panel"},
    {"cmd": "/rename",        "group": "chat", "desc": "Rename current session",
     "args": [{"name": "title", "type": "string"}], "exec": "agent"},
    {"cmd": "/copy",          "group": "chat", "desc": "Copy last assistant message",
     "args": [], "exec": "client", "client_action": "copy_last_message"},
    {"cmd": "/export",        "group": "chat", "desc": "Export thread (markdown/json)",
     "args": [{"name": "format", "type": "enum", "choices": ["md", "json"]}],
     "exec": "route", "route": "GET /api/dx/threads/{thread_id}/export"},
    {"cmd": "/stop",          "group": "chat", "desc": "Abort current generation",
     "args": [], "exec": "client", "client_action": "abort_stream",
     "route": "POST /api/chat/abort"},
    {"cmd": "/retry",         "group": "chat", "desc": "Retry last assistant turn",
     "args": [], "exec": "agent"},
    {"cmd": "/exit",          "group": "chat", "desc": "End session (dashboard: new thread)",
     "args": [], "exec": "client", "client_action": "new_thread", "alias_of": "/new"},
    {"cmd": "/quit",          "group": "chat", "desc": "End session (dashboard: new thread)",
     "args": [], "exec": "client", "client_action": "new_thread", "alias_of": "/new"},
    {"cmd": "/q",             "group": "chat", "desc": "End session (dashboard: new thread)",
     "args": [], "exec": "client", "client_action": "new_thread", "alias_of": "/new"},

    # ── Trust / Approvals ──────────────────────────────────────────────
    {"cmd": "/autopilot",     "group": "trust", "desc": "Toggle autopilot",
     "args": [], "exec": "route", "route": "POST /api/chat/autopilot"},
    {"cmd": "/mode",          "group": "trust", "desc": "Set agent execution mode",
     "args": [{"name": "mode", "type": "string"}], "exec": "agent"},
    {"cmd": "/plan",          "group": "trust", "desc": "Enter plan mode (no exec)",
     "args": [{"name": "task", "type": "string"}], "exec": "agent"},
    {"cmd": "/plan-mode",     "group": "trust", "desc": "Toggle plan mode",
     "args": [], "exec": "agent", "alias_of": "/plan"},
    {"cmd": "/trust",         "group": "trust", "desc": "Manage trust settings",
     "args": [{"name": "action", "type": "string"}], "exec": "agent"},
    {"cmd": "/permissions",   "group": "trust", "desc": "Show permission settings",
     "args": [], "exec": "agent"},
    {"cmd": "/perms",         "group": "trust", "desc": "Alias of /permissions",
     "args": [], "exec": "agent", "alias_of": "/permissions"},
    {"cmd": "/allowed-tools", "group": "trust", "desc": "Show allowed tool list",
     "args": [], "exec": "agent"},
    {"cmd": "/allowedtools",  "group": "trust", "desc": "Alias of /allowed-tools",
     "args": [], "exec": "agent", "alias_of": "/allowed-tools"},
    {"cmd": "/approve",       "group": "trust", "desc": "Set approval mode",
     "args": [{"name": "mode", "type": "enum",
               "choices": ["default", "bypass", "autopilot"]}],
     "exec": "route", "route": "POST /api/chat/approval-mode"},

    # ── Init / Config / Setup ──────────────────────────────────────────
    {"cmd": "/init",          "group": "config", "desc": "Initialise CVC in current workspace",
     "args": [], "exec": "agent"},
    {"cmd": "/init-rules",    "group": "config", "desc": "Initialise rules file",
     "args": [], "exec": "agent"},
    {"cmd": "/config",        "group": "config", "desc": "Show / edit configuration",
     "args": [{"name": "key", "type": "string"}], "exec": "agent"},
    {"cmd": "/settings",      "group": "config", "desc": "Open settings panel",
     "args": [], "exec": "client", "client_action": "open_settings_panel"},
    {"cmd": "/auth",          "group": "config", "desc": "Manage API auth",
     "args": [], "exec": "agent"},
    {"cmd": "/serve",         "group": "config", "desc": "Start local proxy server",
     "args": [], "exec": "agent"},
    {"cmd": "/health",        "group": "config", "desc": "Run health assessment",
     "args": [], "exec": "agent"},
    {"cmd": "/doctor",        "group": "config", "desc": "Diagnose CVC environment",
     "args": [], "exec": "agent"},
    {"cmd": "/release-notes", "group": "config", "desc": "Show CVC release notes",
     "args": [], "exec": "agent"},

    # ── Observability / Analytics ──────────────────────────────────────
    {"cmd": "/cost",          "group": "observability", "desc": "Show token / cost summary",
     "args": [], "exec": "agent"},
    {"cmd": "/stats",         "group": "observability", "desc": "Show session statistics",
     "args": [], "exec": "agent"},
    {"cmd": "/analytics",     "group": "observability", "desc": "Open analytics dashboard",
     "args": [], "exec": "agent"},

    # ── CVC Core (Cognitive Version Control) ───────────────────────────
    # These mirror the cognitive engine surface exposed by the CLI / MCP
    # server (`cvc_status`, `cvc_log`, `cvc_recall`, `cvc_restore`, …).
    # Routed entries dispatch instantly via REST; agent entries fall
    # through to the model so it can invoke the matching MCP tool.
    {"cmd": "/cvc-status",      "group": "cvc", "desc": "Show CVC engine status (branch, HEAD, branches)",
     "args": [], "exec": "route", "route": "GET /api/ops/status"},
    {"cmd": "/cvc-log",         "group": "cvc", "desc": "Show cognitive commit log",
     "args": [{"name": "limit", "type": "string"}],
     "exec": "route", "route": "GET /api/ops/timeline"},
    {"cmd": "/cvc-timeline",    "group": "cvc", "desc": "Timeline of cognitive commits across branches",
     "args": [{"name": "limit", "type": "string"}],
     "exec": "route", "route": "GET /api/ops/timeline"},
    {"cmd": "/cvc-recall",      "group": "cvc", "desc": "Semantic recall over past conversations",
     "args": [{"name": "query", "type": "string"}],
     "exec": "route", "route": "GET /api/ops/recall"},
    {"cmd": "/cvc-branches",    "group": "cvc", "desc": "List all cognitive branches",
     "args": [], "exec": "route", "route": "GET /api/ops/branches"},
    {"cmd": "/cvc-branch",      "group": "cvc", "desc": "Create new cognitive branch",
     "args": [{"name": "name", "type": "string"}],
     "exec": "route", "route": "POST /api/ops/branch"},
    {"cmd": "/cvc-merge",       "group": "cvc", "desc": "Merge cognitive branch into current",
     "args": [{"name": "source_branch", "type": "branch"}],
     "exec": "route", "route": "POST /api/ops/merge"},
    {"cmd": "/cvc-restore",     "group": "cvc", "desc": "Restore cognitive state to a commit hash",
     "args": [{"name": "hash", "type": "string"}],
     "exec": "route", "route": "POST /api/ops/restore"},
    {"cmd": "/cvc-commit",      "group": "cvc", "desc": "Create cognitive commit (alias of /commit)",
     "args": [{"name": "message", "type": "string"}],
     "exec": "route", "route": "POST /api/ops/commit", "alias_of": "/commit"},
    {"cmd": "/cvc-diff",        "group": "cvc", "desc": "Diff two cognitive commits",
     "args": [{"name": "hash_a", "type": "string"}, {"name": "hash_b", "type": "string"}],
     "exec": "route", "route": "GET /api/ops/diff"},
    {"cmd": "/cvc-stats",       "group": "cvc", "desc": "Aggregated cognitive stats (tokens, costs, files)",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-export",      "group": "cvc", "desc": "Export commit conversation as Markdown",
     "args": [{"name": "commit_hash", "type": "string"}], "exec": "agent"},
    {"cmd": "/cvc-inject",      "group": "cvc", "desc": "Pull context from another CVC project",
     "args": [{"name": "source_project", "type": "string"},
              {"name": "query", "type": "string"}], "exec": "agent"},
    {"cmd": "/cvc-audit",       "group": "cvc", "desc": "Show CVC security audit trail",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-compact",     "group": "cvc", "desc": "Compact context window (preserve key messages)",
     "args": [], "exec": "agent"},

    # ── CVC · Hive Memory (multi-agent shared memory) ──────────────────
    {"cmd": "/cvc-hive-status", "group": "cvc-hive", "desc": "Hive mind status (branches, agents, HEAD)",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-hive-read",   "group": "cvc-hive", "desc": "Read entries from Hive Memory",
     "args": [{"name": "query", "type": "string"}], "exec": "agent"},
    {"cmd": "/cvc-hive-write",  "group": "cvc-hive", "desc": "Write a shared memory entry",
     "args": [{"name": "content", "type": "string"}], "exec": "agent"},
    {"cmd": "/cvc-hive-stats",  "group": "cvc-hive", "desc": "Hive Memory statistics",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-agents",      "group": "cvc-hive", "desc": "List registered agents in the hive mind",
     "args": [], "exec": "agent"},

    # ── CVC · Cognome (smart context compiler) ─────────────────────────
    {"cmd": "/cvc-cognome-status",   "group": "cvc-cognome", "desc": "Cognome substrate status",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-cognome-init",     "group": "cvc-cognome", "desc": "Bootstrap Cognome substrate",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-cognome-enable",   "group": "cvc-cognome", "desc": "Enable Cognome Engram injection",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-cognome-disable",  "group": "cvc-cognome", "desc": "Disable Cognome Engram injection",
     "args": [], "exec": "agent"},
    {"cmd": "/cvc-cognome-compile",  "group": "cvc-cognome", "desc": "Compile query-specific Engram",
     "args": [{"name": "query", "type": "string"}], "exec": "agent"},
    {"cmd": "/cvc-cognome-audit",    "group": "cvc-cognome", "desc": "Recent Cognome compilations",
     "args": [], "exec": "agent"},

    # ── CVC · Sync (team / remote knowledge sync) ──────────────────────
    {"cmd": "/cvc-sync-push",   "group": "cvc-sync", "desc": "Push cognitive commits to a remote",
     "args": [{"name": "remote_path", "type": "string"}], "exec": "agent"},
    {"cmd": "/cvc-sync-pull",   "group": "cvc-sync", "desc": "Pull cognitive commits from a remote",
     "args": [{"name": "remote_path", "type": "string"}], "exec": "agent"},
    {"cmd": "/cvc-sync-status", "group": "cvc-sync", "desc": "Show configured sync remotes",
     "args": [], "exec": "agent"},

    # ── Help ───────────────────────────────────────────────────────────
    {"cmd": "/help",          "group": "help", "desc": "Show all slash commands",
     "args": [], "exec": "client", "client_action": "open_slash_palette"},
    {"cmd": "/shortcuts",     "group": "help", "desc": "Show keyboard shortcuts",
     "args": [], "exec": "client", "client_action": "open_shortcuts_overlay"},
]


@router.get("/slash/registry")
def slash_registry() -> dict:
    return {"count": len(SLASH_REGISTRY), "commands": SLASH_REGISTRY}


@router.post("/slash/run")
async def slash_run(req: SlashRunRequest, request: Request) -> dict:
    """
    Headless slash-command runner. The FE normally executes commands
    directly against their named routes (better UX, no double-hop).
    This endpoint exists for voice / API clients that want a single
    entry point.
    """
    cmd = (req.command or "").strip()
    if not cmd.startswith("/"):
        cmd = "/" + cmd
    entry = next((c for c in SLASH_REGISTRY if c["cmd"] == cmd), None)
    if not entry:
        raise HTTPException(404, f"Unknown slash command: {cmd}")

    now = time.time()
    result: dict[str, Any] = {"cmd": cmd, "entry": entry}
    ok = True
    # Built-in handlers for memory-related commands (others delegate to FE).
    try:
        if cmd == "/remember":
            args = req.args or {}
            ws = args.get("workspace_path") or ""
            if not ws:
                raise HTTPException(400, "/remember requires workspace_path in args")
            with _conv_conn() as c:
                cur = c.execute(
                    "INSERT INTO insights "
                    "(workspace_path, thread_id, kind, content, source, weight, created_at, last_used) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (ws, req.thread_id,
                     args.get("kind", "fact"),
                     (args.get("content") or "").strip(),
                     "slash", 1.0, now, now),
                )
                result["insight_id"] = cur.lastrowid
        elif cmd == "/insights":
            ws = (req.args or {}).get("workspace_path") or ""
            with _conv_conn() as c:
                rows = c.execute(
                    "SELECT * FROM insights WHERE workspace_path = ? "
                    "ORDER BY weight DESC LIMIT 50",
                    (ws,),
                ).fetchall()
            result["insights"] = [dict(r) for r in rows]
        else:
            # Pure FE-handled command — just echo back the registry entry
            # so the FE knows what to do.
            result["delegate"] = True
    except HTTPException:
        ok = False
        raise
    except Exception as exc:
        ok = False
        result["error"] = str(exc)
        logger.exception("slash_run failed for %s", cmd)
    finally:
        try:
            with _conv_conn() as c:
                c.execute(
                    "INSERT INTO slash_runs (thread_id, command, args, result, ok, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (req.thread_id, cmd,
                     json.dumps(req.args or {}),
                     json.dumps(result)[:4000], 1 if ok else 0, now),
                )
        except Exception:
            pass
    return result


@router.get("/slash/history")
def slash_history(limit: int = Query(50, ge=1, le=500)) -> dict:
    with _conv_conn() as c:
        rows = c.execute(
            "SELECT * FROM slash_runs ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return {"count": len(rows), "runs": [dict(r) for r in rows]}


# ════════════════════════════════════════════════════════════════════════
# 5. FILE PICKER  (@-mention fuzzy search inside the active workspace)
# ════════════════════════════════════════════════════════════════════════


_IGNORE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", "web_dist", ".next", ".cache", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "target", ".idea", ".vscode",
}
_IGNORE_EXTS = {
    ".pyc", ".so", ".dll", ".exe", ".bin", ".dat", ".db", ".sqlite",
    ".whl", ".tar", ".gz", ".zip", ".jpg", ".jpeg", ".png", ".gif",
    ".pdf", ".mov", ".mp4", ".webp", ".ico", ".woff", ".woff2", ".ttf",
}


def _score(name: str, query: str) -> int:
    """Simple subsequence + prefix score. Higher is better."""
    if not query:
        return 1
    n, q = name.lower(), query.lower()
    if n == q:
        return 1000
    if n.startswith(q):
        return 500 - len(n)
    if q in n:
        return 200 - len(n)
    # Subsequence match
    it = iter(n)
    if all(ch in it for ch in q):
        return 50 - len(n)
    return 0


@router.get("/files/search")
def files_search(
    workspace_path: str = Query(...),
    q: str = Query(""),
    limit: int = Query(40, ge=1, le=200),
) -> dict:
    root = Path(workspace_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise HTTPException(404, f"workspace_path not found: {workspace_path}")

    results: list[dict[str, Any]] = []
    scanned = 0
    HARD_LIMIT = 8000  # files visited before we bail out

    for p in root.rglob("*"):
        scanned += 1
        if scanned > HARD_LIMIT:
            break
        try:
            if p.is_dir():
                if p.name in _IGNORE_DIRS:
                    # rglob won't auto-prune; just skip and let traversal continue
                    continue
                continue
            if p.suffix.lower() in _IGNORE_EXTS:
                continue
            # Skip files inside ignored dirs (path-level check)
            if any(part in _IGNORE_DIRS for part in p.parts):
                continue
            rel = str(p.relative_to(root))
            s = _score(p.name, q)
            if s <= 0 and q:
                # Also score against the relative path for nested matches
                s = _score(rel, q)
            if s <= 0 and q:
                continue
            results.append({
                "path": rel,
                "name": p.name,
                "size": p.stat().st_size,
                "score": s,
            })
        except Exception:
            continue

    results.sort(key=lambda r: (-r["score"], r["path"]))
    return {
        "workspace_path": str(root),
        "query": q,
        "scanned": scanned,
        "count": min(len(results), limit),
        "files": results[:limit],
    }


# ════════════════════════════════════════════════════════════════════════
# 6. COST TICKER
# ════════════════════════════════════════════════════════════════════════


@router.get("/cost")
def session_cost(thread_id: Optional[str] = Query(None)) -> dict:
    """
    Best-effort cost summary. Reads the active CostTracker from the
    gateway module if available; otherwise returns zeros.
    """
    out: dict[str, Any] = {
        "thread_id": thread_id,
        "available": False,
        "summary": "",
        "data": {},
    }
    try:
        from cvc import gateway as gw  # type: ignore
        tracker = getattr(gw, "_cost_tracker", None)
        if tracker is not None:
            out["available"] = True
            try:
                out["summary"] = tracker.format_summary()
            except Exception:
                out["summary"] = ""
            try:
                out["data"] = tracker.to_dict()
            except Exception:
                out["data"] = {}
    except Exception as exc:
        out["error"] = str(exc)
    return out


# ════════════════════════════════════════════════════════════════════════
# 7. EXPORT  (markdown / json — share a chat thread)
# ════════════════════════════════════════════════════════════════════════


@router.get("/threads/{thread_id}/export")
def export_thread(
    thread_id: str,
    format: str = Query("md", pattern="^(md|json)$"),
) -> dict:
    with _conv_conn() as c:
        thread = c.execute("SELECT * FROM threads WHERE id = ?", (thread_id,)).fetchone()
        if not thread:
            raise HTTPException(404, f"Thread not found: {thread_id}")
        msgs = c.execute(
            "SELECT id, role, content, created_at, reply_to, pinned, meta "
            "FROM messages WHERE thread_id = ? ORDER BY created_at ASC, id ASC",
            (thread_id,),
        ).fetchall()

    if format == "json":
        return {
            "thread": dict(thread),
            "messages": [dict(m) for m in msgs],
        }

    # Markdown
    lines: list[str] = [
        f"# {thread['title']}",
        "",
        f"- **Thread:** `{thread['id']}`",
        f"- **Workspace:** `{thread['workspace_path']}`",
        f"- **Persona:** {thread['persona_id'] or '—'}",
        f"- **Created:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(thread['created_at']))}",
        f"- **Messages:** {len(msgs)}",
        "",
        "---",
        "",
    ]
    by_id = {m["id"]: m for m in msgs}
    for m in msgs:
        ts = time.strftime("%H:%M:%S", time.localtime(m["created_at"]))
        role = m["role"].upper()
        pin = " 📌" if m["pinned"] else ""
        lines.append(f"## {role}{pin} · {ts}")
        if m["reply_to"] and m["reply_to"] in by_id:
            quoted = by_id[m["reply_to"]]["content"] or ""
            for q in quoted.splitlines()[:3]:
                lines.append(f"> {q}")
            lines.append("")
        lines.append(m["content"] or "")
        lines.append("")
    return {
        "thread_id": thread_id,
        "format": "md",
        "filename": f"{thread['title'][:40].strip() or 'thread'}-{thread_id}.md",
        "content": "\n".join(lines),
    }


# ════════════════════════════════════════════════════════════════════════
# 8. CONTEXT BUILDER  (used by /api/chat agent loop to inject pinned + insights)
# ════════════════════════════════════════════════════════════════════════


def build_dx_context(
    thread_id: Optional[str],
    workspace_path: Optional[str],
    *,
    max_pins: int = 10,
    max_insights: int = 20,
) -> Optional[dict]:
    """
    Build a single `system` message dict the agent loop can prepend.
    Returns None if nothing to inject so caller can no-op cheaply.
    """
    if not thread_id and not workspace_path:
        return None

    pins: list[sqlite3.Row] = []
    insights: list[sqlite3.Row] = []
    used_insight_ids: list[int] = []
    try:
        with _conv_conn() as c:
            if thread_id:
                pins = c.execute(
                    "SELECT id, role, content FROM messages "
                    "WHERE thread_id = ? AND pinned = 1 "
                    "ORDER BY created_at ASC LIMIT ?",
                    (thread_id, max_pins),
                ).fetchall()
            if workspace_path:
                insights = c.execute(
                    "SELECT id, kind, content FROM insights "
                    "WHERE workspace_path = ? "
                    "ORDER BY weight DESC, last_used DESC LIMIT ?",
                    (workspace_path, max_insights),
                ).fetchall()
            # Self-learning: bump weights of insights we're about to inject
            now = time.time()
            for r in insights:
                used_insight_ids.append(r["id"])
                c.execute(
                    "UPDATE insights SET last_used = ?, use_count = use_count + 1, "
                    "weight = MIN(weight + 0.05, 5.0) WHERE id = ?",
                    (now, r["id"]),
                )
    except Exception as exc:
        logger.debug("build_dx_context failed: %s", exc)
        return None

    if not pins and not insights:
        return None

    parts: list[str] = ["[CVC-DX Persistent Context]"]
    if pins:
        parts.append("\n📌 Pinned messages (user marked these as important):")
        for p in pins:
            preview = (p["content"] or "").strip().replace("\n", " ")
            parts.append(f"  • [{p['role']}] {preview[:240]}")
    if insights:
        parts.append("\n🧠 Workspace insights (self-learning, ordered by importance):")
        # group by kind for readability
        grouped: dict[str, list[str]] = {}
        for r in insights:
            grouped.setdefault(r["kind"], []).append((r["content"] or "").strip())
        for kind in ("rule", "preference", "decision", "pitfall", "fact"):
            items = grouped.get(kind) or []
            if not items:
                continue
            parts.append(f"  [{kind}]")
            for it in items:
                parts.append(f"    - {it[:300]}")
    parts.append(
        "\nFollow pinned context and insights. Treat rules and preferences "
        "as authoritative; they reflect Jai's explicit decisions."
    )

    return {
        "role": "system",
        "content": "\n".join(parts),
        "_dx_meta": {
            "pin_count": len(pins),
            "insight_count": len(insights),
            "insight_ids": used_insight_ids,
        },
    }


# ════════════════════════════════════════════════════════════════════════
# 9. AUTO-LEARN  (heuristic: capture insights from explicit user phrasing)
# ════════════════════════════════════════════════════════════════════════


_AUTO_LEARN_PATTERNS = [
    (re.compile(r"\b(remember|note|don'?t forget)\s*(that)?\s*[:\-]?\s*(.+)", re.I), "fact"),
    (re.compile(r"\balways\s+(.+)", re.I), "rule"),
    (re.compile(r"\bnever\s+(.+)", re.I), "rule"),
    (re.compile(r"\bi (prefer|like|want)\s+(.+)", re.I), "preference"),
    (re.compile(r"\bwe decided\s+(to\s+)?(.+)", re.I), "decision"),
    (re.compile(r"\b(gotcha|pitfall|warning)\s*[:\-]\s*(.+)", re.I), "pitfall"),
]


def auto_learn_from_message(
    workspace_path: str,
    thread_id: Optional[str],
    content: str,
) -> Optional[int]:
    """
    Inspect a user message for self-learning triggers and store an insight.
    Returns the new insight id, or None if nothing matched. Never raises.
    """
    if not workspace_path or not content:
        return None
    text = content.strip()
    if len(text) < 8 or len(text) > 2000:
        return None
    for pat, kind in _AUTO_LEARN_PATTERNS:
        m = pat.search(text)
        if not m:
            continue
        captured = m.group(m.lastindex or 0).strip().rstrip(".!?")
        if len(captured) < 4:
            continue
        try:
            now = time.time()
            with _conv_conn() as c:
                # Dedupe — same kind + similar content within this workspace
                existing = c.execute(
                    "SELECT id FROM insights "
                    "WHERE workspace_path = ? AND kind = ? AND content = ? LIMIT 1",
                    (workspace_path, kind, captured),
                ).fetchone()
                if existing:
                    c.execute(
                        "UPDATE insights SET last_used = ?, use_count = use_count + 1, "
                        "weight = MIN(weight + 0.2, 5.0) WHERE id = ?",
                        (now, existing["id"]),
                    )
                    return existing["id"]
                cur = c.execute(
                    "INSERT INTO insights "
                    "(workspace_path, thread_id, kind, content, source, weight, created_at, last_used) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (workspace_path, thread_id, kind, captured, "auto", 1.2, now, now),
                )
                return cur.lastrowid
        except Exception as exc:
            logger.debug("auto_learn store failed: %s", exc)
            return None
    return None
