"""Web Content routes mixin."""

import json
import logging
import re

from salmalm.constants import DATA_DIR, VERSION, WORKSPACE_DIR, MEMORY_DIR, BASE_DIR, AUDIT_DB  # noqa: F401
from salmalm.core.core import get_usage_report  # noqa: F401
from salmalm.security.crypto import vault, log  # noqa: F401

log = logging.getLogger(__name__)

_RE_SESSION_SUMMARY = re.compile(r"^/api/sessions/([^/]+)/summary")
_RE_SESSION_ALT = re.compile(r"^/api/sessions/([^/]+)/alternatives/(\d+)")


class ContentMixin:
    GET_ROUTES = {
        "/api/groups": "_get_groups",
        "/api/soul": "_get_soul",
        "/api/memory/files": "_get_memory_files",
        "/api/mcp": "_get_mcp",
        "/api/rag": "_get_rag",
        "/api/personas": "_get_personas",
        "/api/thoughts": "_get_thoughts",
        "/api/thoughts/stats": "_get_thoughts_stats",
        "/api/tools/list": "_get_tools_list",
        "/api/browser/status": "_get_api_browser_status",
        "/api/commands": "_get_commands",
        "/api/dashboard": "_get_api_dashboard",
        "/manifest.json": "_get_manifest_json",
    }
    POST_ROUTES = {
        "/api/bookmarks": "_post_api_bookmarks",
        "/api/thoughts": "_post_api_thoughts",
    }
    GET_PREFIX_ROUTES = [
        ("/api/search", "_get_api_search", None),
        ("/api/rag/search", "_get_api_rag_search", None),
        ("/api/sessions/", "_get_api_sessions_summary", "/summary"),
        ("/api/sessions/", "_get_api_sessions_alternatives", "/alternatives"),
        ("/api/memory/read?", "_get_api_memory_read", None),
    ]

    def _get_thoughts(self):
        """Get thoughts."""
        if not self._require_auth("user"):
            return
        from salmalm.features.thoughts import thought_stream
        import urllib.parse as _up

        qs = _up.parse_qs(_up.urlparse(self.path).query)
        search_q = qs.get("q", [""])[0]
        if search_q:
            results = thought_stream.search(search_q)
        else:
            try:
                n = max(1, min(int(qs.get("limit", ["20"])[0]), 200))
            except (TypeError, ValueError):
                n = 20
            results = thought_stream.list_recent(n)
        self._json({"thoughts": results})

    def _get_thoughts_stats(self):
        """Get thoughts stats."""
        if not self._require_auth("user"):
            return
        from salmalm.features.thoughts import thought_stream

        self._json(thought_stream.stats())

    def _get_tools_list(self):
        """Get tools list."""
        tools = []
        try:
            from salmalm.tools.tool_registry import _HANDLERS, _ensure_modules

            _ensure_modules()
            for name in sorted(_HANDLERS.keys()):
                tools.append({"name": name, "description": ""})
        except Exception as e:
            log.debug(f"Suppressed: {e}")
        if not tools:
            # Fallback: list all known tools from INTENT_TOOLS
            try:
                from salmalm.core.engine import INTENT_TOOLS

                seen = set()
                for cat_tools in INTENT_TOOLS.values():
                    for t in cat_tools:
                        n = t.get("function", {}).get("name", "")
                        if n and n not in seen:
                            seen.add(n)
                            tools.append(
                                {
                                    "name": n,
                                    "description": t.get("function", {}).get("description", ""),
                                }
                            )
            except Exception as e:  # noqa: broad-except
                tools = [
                    {"name": "web_search", "description": "Search the web"},
                    {"name": "bash", "description": "Execute shell commands"},
                    {"name": "file_read", "description": "Read files"},
                    {"name": "file_write", "description": "Write files"},
                    {"name": "browser", "description": "Browser automation"},
                ]
        self._json({"tools": tools, "count": len(tools)})

    def _get_personas(self):
        """Get personas."""
        from salmalm.core.prompt import list_personas, get_active_persona

        session_id = self.headers.get("X-Session-Id", "web")
        personas = list_personas()
        active = get_active_persona(session_id)
        self._json({"personas": personas, "active": active})

    def _get_memory_files(self):
        """Get memory files."""
        if not self._require_auth("user"):
            return
        mem_dir = BASE_DIR / "memory"
        files = []
        # Main memory file
        main_mem = DATA_DIR / "memory.json"
        if main_mem.exists():
            files.append(
                {
                    "name": "memory.json",
                    "size": main_mem.stat().st_size,
                    "path": "memory.json",
                }
            )
        # Memory directory files
        if mem_dir.exists():
            for f in sorted(mem_dir.iterdir(), reverse=True):
                if f.is_file() and f.suffix in (".json", ".md", ".txt"):
                    files.append(
                        {
                            "name": f.name,
                            "size": f.stat().st_size,
                            "path": f"memory/{f.name}",
                        }
                    )
        # Soul file
        soul = DATA_DIR / "soul.md"
        if soul.exists():
            files.append({"name": "soul.md", "size": soul.stat().st_size, "path": "soul.md"})
        self._json({"files": files})

    def _get_mcp(self):
        """Get mcp."""
        if not self._require_auth("user"):
            return
        from salmalm.features.mcp import mcp_manager

        servers = mcp_manager.list_servers()
        all_tools = mcp_manager.get_all_tools()
        self._json({"servers": servers, "total_tools": len(all_tools)})

    def _get_rag(self):
        """Get rag."""
        if not self._require_auth("user"):
            return
        from salmalm.features.rag import rag_engine

        self._json(rag_engine.get_stats())

    def _get_groups(self):
        """Get groups."""
        if not self._require_auth("user"):
            return
        from salmalm.features.edge_cases import session_groups

        self._json({"groups": session_groups.list_groups()})

    def _get_soul(self):
        """Get soul."""
        if not self._require_auth("user"):
            return
        from salmalm.core.prompt import get_user_soul, USER_SOUL_FILE

        self._json({"content": get_user_soul(), "path": str(USER_SOUL_FILE)})

    def _get_commands(self):
        """Get commands."""
        cmds = [
            {"name": "/help", "desc": "Show help"},
            {"name": "/status", "desc": "Session status"},
            {"name": "/model", "desc": "Switch model"},
            {"name": "/compact", "desc": "Compress context"},
            {"name": "/context", "desc": "Token breakdown"},
            {"name": "/usage", "desc": "Token/cost tracking"},
            {"name": "/think", "desc": "Record thought / thinking level"},
            {"name": "/persona", "desc": "Switch persona"},
            {"name": "/branch", "desc": "Branch conversation"},
            {"name": "/rollback", "desc": "Rollback messages"},
            {"name": "/life", "desc": "Life dashboard"},
            {"name": "/remind", "desc": "Set reminder"},
            {"name": "/expense", "desc": "Track expense"},
            {"name": "/pomodoro", "desc": "Pomodoro timer"},
            {"name": "/note", "desc": "Save note"},
            {"name": "/link", "desc": "Save link"},
            {"name": "/routine", "desc": "Manage routines"},
            {"name": "/shadow", "desc": "Shadow mode"},
            {"name": "/vault", "desc": "Encrypted vault"},
            {"name": "/capsule", "desc": "Time capsule"},
            {"name": "/deadman", "desc": "Dead man's switch"},
            {"name": "/a2a", "desc": "Agent-to-agent"},
            {"name": "/workflow", "desc": "Workflow engine"},
            {"name": "/mcp", "desc": "MCP management"},
            {"name": "/subagents", "desc": "Sub-agents"},
            {"name": "/oauth", "desc": "OAuth setup"},
            {"name": "/bash", "desc": "Run shell command"},
            {"name": "/screen", "desc": "Browser control"},
            {"name": "/evolve", "desc": "Evolving prompt"},
            {"name": "/mood", "desc": "Mood detection"},
            {"name": "/split", "desc": "A/B split response"},
        ]
        self._json({"commands": cmds, "count": len(cmds)})

    def _get_manifest_json(self):
        """Get manifest json."""
        manifest = {
            "name": "SalmAlm — Personal AI Gateway",
            "short_name": "SalmAlm",
            "description": "Your personal AI gateway. 66 tools, 6 providers, 3 core dependencies (uvicorn, fastapi, websockets).",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0b0d14",
            "theme_color": "#6366f1",
            "orientation": "any",
            "categories": ["productivity", "utilities"],
            "icons": [
                {
                    "src": "/icon-192.svg",
                    "sizes": "192x192",
                    "type": "image/svg+xml",
                    "purpose": "any",
                },
                {
                    "src": "/icon-512.svg",
                    "sizes": "512x512",
                    "type": "image/svg+xml",
                    "purpose": "any maskable",
                },
            ],
        }
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/manifest+json")
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(json.dumps(manifest).encode())


# ── FastAPI router ────────────────────────────────────────────────────────────
import asyncio as _asyncio
from fastapi import APIRouter as _APIRouter, Request as _Request, Depends as _Depends, Query as _Query
from fastapi.responses import JSONResponse as _JSON, Response as _Response, HTMLResponse as _HTML, StreamingResponse as _SR, RedirectResponse as _RR
from salmalm.web.fastapi_deps import require_auth as _auth, optional_auth as _optauth

router = _APIRouter()

@router.get("/api/groups")
async def get_groups(_u=_Depends(_auth)):
    from salmalm.features.edge_cases import session_groups
    return _JSON(content={"groups": session_groups.list_groups()})

@router.get("/api/soul")
async def get_soul(_u=_Depends(_auth)):
    from salmalm.core.prompt import get_user_soul, USER_SOUL_FILE
    return _JSON(content={"content": get_user_soul(), "path": str(USER_SOUL_FILE)})

@router.get("/api/memory/files")
async def get_memory_files(_u=_Depends(_auth)):
    from salmalm.constants import DATA_DIR, BASE_DIR
    mem_dir = BASE_DIR / "memory"
    files = []
    main_mem = DATA_DIR / "memory.json"
    if main_mem.exists():
        files.append({"name": "memory.json", "size": main_mem.stat().st_size, "path": "memory.json"})
    if mem_dir.exists():
        for f in sorted(mem_dir.iterdir(), reverse=True):
            if f.is_file() and f.suffix in (".json", ".md", ".txt"):
                files.append({"name": f.name, "size": f.stat().st_size, "path": f"memory/{f.name}"})
    soul = DATA_DIR / "soul.md"
    if soul.exists():
        files.append({"name": "soul.md", "size": soul.stat().st_size, "path": "soul.md"})
    return _JSON(content={"files": files})

@router.get("/api/mcp")
async def get_mcp(_u=_Depends(_auth)):
    from salmalm.features.mcp import mcp_manager
    servers = mcp_manager.list_servers()
    all_tools = mcp_manager.get_all_tools()
    return _JSON(content={"servers": servers, "total_tools": len(all_tools)})

@router.get("/api/rag")
async def get_rag(_u=_Depends(_auth)):
    from salmalm.features.rag import rag_engine
    return _JSON(content=rag_engine.get_stats())

@router.get("/api/personas")
async def get_personas(request: _Request, _u=_Depends(_auth)):
    # BUG-CC fix: added _auth dependency — unauthenticated callers could enumerate
    # any session's active persona via x-session-id header (information disclosure)
    from salmalm.core.prompt import list_personas, get_active_persona
    session_id = request.headers.get("x-session-id", "web")
    personas = list_personas()
    active = get_active_persona(session_id)
    return _JSON(content={"personas": personas, "active": active})

@router.get("/api/thoughts")
async def get_thoughts(q: str = _Query(None), limit: int = _Query(20, ge=1, le=200), _u=_Depends(_auth)):
    from salmalm.features.thoughts import thought_stream
    if q:
        results = thought_stream.search(q)
    else:
        results = thought_stream.list_recent(max(1, min(limit, 200)))
    return _JSON(content={"thoughts": results})

@router.get("/api/thoughts/stats")
async def get_thoughts_stats(_u=_Depends(_auth)):
    from salmalm.features.thoughts import thought_stream
    return _JSON(content=thought_stream.stats())

@router.get("/api/tools/list")
async def get_tools_list(_u=_Depends(_auth)):
    tools = []
    try:
        from salmalm.tools.tool_registry import _HANDLERS, _ensure_modules
        _ensure_modules()
        for name in sorted(_HANDLERS.keys()):
            tools.append({"name": name, "description": ""})
    except Exception:
        pass
    if not tools:
        try:
            from salmalm.core.engine import INTENT_TOOLS
            seen = set()
            for cat_tools in INTENT_TOOLS.values():
                for t in cat_tools:
                    n = t.get("function", {}).get("name", "")
                    if n and n not in seen:
                        seen.add(n)
                        tools.append({"name": n, "description": t.get("function", {}).get("description", "")})
        except Exception:
            tools = [{"name": "web_search", "description": "Search the web"}, {"name": "bash", "description": "Execute shell commands"},
                     {"name": "file_read", "description": "Read files"}, {"name": "file_write", "description": "Write files"},
                     {"name": "browser", "description": "Browser automation"}]
    return _JSON(content={"tools": tools, "count": len(tools)})

@router.get("/api/browser/status")
async def get_browser_status():
    available = False
    reason = "playwright not installed"
    try:
        import importlib.util
        if importlib.util.find_spec("playwright") is not None:
            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    import os
                    exe = p.chromium.executable_path
                    available = os.path.isfile(exe)
                    reason = "chromium found" if available else f"chromium missing: {exe}"
            except Exception as _e:
                reason = f"playwright import error: {_e}"
        else:
            reason = "playwright package not installed (pip install salmalm[browser])"
    except Exception as _e:
        reason = str(_e)
    return _JSON(content={"available": available, "reason": reason})

@router.get("/api/commands")
async def get_commands():
    cmds = [
        {"name": "/help", "desc": "Show help"}, {"name": "/status", "desc": "Session status"},
        {"name": "/model", "desc": "Switch model"}, {"name": "/compact", "desc": "Compress context"},
        {"name": "/context", "desc": "Token breakdown"}, {"name": "/usage", "desc": "Token/cost tracking"},
        {"name": "/think", "desc": "Record thought / thinking level"}, {"name": "/persona", "desc": "Switch persona"},
        {"name": "/branch", "desc": "Branch conversation"}, {"name": "/rollback", "desc": "Rollback messages"},
        {"name": "/life", "desc": "Life dashboard"}, {"name": "/remind", "desc": "Set reminder"},
        {"name": "/expense", "desc": "Track expense"}, {"name": "/pomodoro", "desc": "Pomodoro timer"},
        {"name": "/note", "desc": "Save note"}, {"name": "/link", "desc": "Save link"},
        {"name": "/routine", "desc": "Manage routines"}, {"name": "/shadow", "desc": "Shadow mode"},
        {"name": "/vault", "desc": "Encrypted vault"}, {"name": "/capsule", "desc": "Time capsule"},
        {"name": "/deadman", "desc": "Dead man's switch"}, {"name": "/a2a", "desc": "Agent-to-agent"},
        {"name": "/workflow", "desc": "Workflow engine"}, {"name": "/mcp", "desc": "MCP management"},
        {"name": "/subagents", "desc": "Sub-agents"}, {"name": "/oauth", "desc": "OAuth setup"},
        {"name": "/bash", "desc": "Run shell command"}, {"name": "/screen", "desc": "Browser control"},
        {"name": "/evolve", "desc": "Evolving prompt"}, {"name": "/mood", "desc": "Mood detection"},
        {"name": "/split", "desc": "A/B split response"},
    ]
    return _JSON(content={"commands": cmds, "count": len(cmds)})

@router.get("/api/dashboard")
async def get_dashboard(_u=_Depends(_auth)):
    from salmalm.constants import AUDIT_DB
    from salmalm.core import _sessions, _llm_cron, PluginLoader, SubAgent
    from salmalm.core.core import get_usage_report
    from salmalm.db import get_connection
    sessions_info = [{"id": s.id, "messages": len(s.messages), "last_active": s.last_active, "created": s.created}
                     for s in _sessions.values()]
    cron_jobs = _llm_cron.list_jobs() if _llm_cron else []
    plugins = [{"name": n, "tools": len(p["tools"])} for n, p in PluginLoader._plugins.items()]
    subagents = SubAgent.list_agents()
    usage = get_usage_report()
    cost_timeline = []
    try:
        _conn = get_connection(AUDIT_DB)
        cur = _conn.execute("SELECT substr(ts,1,13) as hour, COUNT(*) as cnt FROM audit_log WHERE event='tool_exec' GROUP BY hour ORDER BY hour DESC LIMIT 24")
        cost_timeline = [{"hour": r[0], "count": r[1]} for r in cur.fetchall()]
        _conn.close()
    except Exception:
        pass
    return _JSON(content={"sessions": sessions_info, "usage": usage, "cron_jobs": cron_jobs,
                          "plugins": plugins, "subagents": subagents, "cost_timeline": cost_timeline})

@router.get("/manifest.json")
async def get_manifest():
    manifest = {
        "name": "SalmAlm — Personal AI Gateway", "short_name": "SalmAlm",
        "description": "Your personal AI gateway.", "start_url": "/",
        "display": "standalone", "background_color": "#0b0d14", "theme_color": "#6366f1",
        "orientation": "any", "categories": ["productivity", "utilities"],
        "icons": [{"src": "/icon-192.svg", "sizes": "192x192", "type": "image/svg+xml", "purpose": "any"},
                  {"src": "/icon-512.svg", "sizes": "512x512", "type": "image/svg+xml", "purpose": "any maskable"}],
    }
    return _JSON(content=manifest)

@router.get("/api/search")
async def get_search(q: str = _Query(""), limit: int = _Query(20, ge=1, le=500), _u=_Depends(_auth)):
    if not q:
        return _JSON(content={"error": "Missing q parameter"}, status_code=400)
    from salmalm.core import search_messages
    results = search_messages(q, limit=min(limit, 500))
    return _JSON(content={"query": q, "results": results, "count": len(results)})

@router.get("/api/rag/search")
async def get_rag_search(q: str = _Query(""), n: int = _Query(5, ge=1, le=50), _u=_Depends(_auth)):
    if not q:
        return _JSON(content={"error": "Missing q parameter"}, status_code=400)
    from salmalm.features.rag import rag_engine
    results = rag_engine.search(q, max_results=min(n, 50))
    return _JSON(content={"query": q, "results": results})

@router.get("/api/memory/read")
async def get_memory_read(file: str = _Query(""), _u=_Depends(_auth)):
    from pathlib import PurePosixPath
    from salmalm.constants import BASE_DIR
    if not file or ".." in file:
        return _JSON(content={"error": "Invalid path"}, status_code=400)
    if PurePosixPath(file).is_absolute() or "\\" in file:
        return _JSON(content={"error": "Invalid path"}, status_code=400)
    full = (BASE_DIR / file).resolve()
    if not full.is_relative_to(BASE_DIR.resolve()):
        return _JSON(content={"error": "Path outside allowed directory"}, status_code=403)
    if not full.exists() or not full.is_file():
        return _JSON(content={"error": "File not found"}, status_code=404)
    try:
        content = full.read_text(encoding="utf-8")[:50000]
        return _JSON(content={"file": file, "content": content, "size": full.stat().st_size})
    except Exception as e:
        log.warning("[FILE] Error: %s", e)
    return _JSON(content={"error": "Internal error — check server logs"}, status_code=500)

@router.get("/api/thoughts/search")
async def get_thoughts_search(q: str = _Query(""), _u=_Depends(_auth)):
    if not q:
        return _JSON(content={"error": "query required"}, status_code=400)
    from salmalm.features.thoughts import thought_stream
    return _JSON(content={"thoughts": thought_stream.search(q)})

@router.post("/api/bookmarks")
async def post_bookmarks(request: _Request, _u=_Depends(_auth)):
    from salmalm.features.edge_cases import bookmark_manager
    body = await request.json()
    action = body.get("action", "add")
    session_id = body.get("session_id", "")
    message_index = body.get("message_index")
    if not session_id or message_index is None:
        return _JSON(content={"error": "Missing session_id or message_index"}, status_code=400)
    # BUG-CD fix: reject negative message_index
    try:
        mi = int(message_index)
    except (TypeError, ValueError):
        return _JSON(content={"error": "Invalid message_index"}, status_code=400)
    if mi < 0:
        return _JSON(content={"error": "message_index must be >= 0"}, status_code=400)
    if action == "add":
        ok = bookmark_manager.add(session_id, mi, content_preview=body.get("preview", ""),
                                  note=body.get("note", ""), role=body.get("role", "assistant"))
        return _JSON(content={"ok": ok})
    elif action == "remove":
        ok = bookmark_manager.remove(session_id, mi)
        return _JSON(content={"ok": ok})
    return _JSON(content={"error": "Unknown action"}, status_code=400)

@router.post("/api/thoughts")
async def post_thoughts(request: _Request, _u=_Depends(_auth)):
    from salmalm.features.thoughts import thought_stream
    body = await request.json()
    content = body.get("content", "").strip()
    if not content:
        return _JSON(content={"error": "content required"}, status_code=400)
    tid = thought_stream.add(content, mood=body.get("mood", "neutral"))
    return _JSON(content={"ok": True, "id": tid})

@router.post("/api/thoughts/search")
async def post_thoughts_search(request: _Request, _u=_Depends(_auth)):
    from salmalm.features.thoughts import thought_stream
    body = await request.json()
    q = body.get("q", body.get("query", ""))
    if not q:
        return _JSON(content={"error": "query required"}, status_code=400)
    return _JSON(content={"thoughts": thought_stream.search(q)})
