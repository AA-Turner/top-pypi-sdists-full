"""
nx_mcp_client.py — minimal MCP client over Streamable HTTP (the transport remote
MCP servers use). Speaks JSON-RPC to a connected server with the bearer token
from nx_mcp_oauth, so a connection is actually USABLE:
    initialize → tools/list → tools/call

Handles both response shapes: a single application/json body, or an SSE
(text/event-stream) stream where the result arrives in a `data:` event. Honest:
raises MCPAuthError on 401 (sign in first) and never fabricates a tool result.
"""
import json
import ssl
import urllib.error
import urllib.request

PROTOCOL = "2025-06-18"
_CTX = ssl.create_default_context()
_UA = "NX-MCP/1.0 (Nexplora)"


class MCPError(Exception):
    pass


class MCPAuthError(MCPError):
    pass


def _parse(content_type, body):
    """Return the JSON-RPC object from either a JSON body or an SSE stream."""
    text = body.decode("utf-8", "ignore") if isinstance(body, (bytes, bytearray)) else (body or "")
    if "text/event-stream" in (content_type or ""):
        result = {}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                chunk = line[5:].strip()
                try:
                    obj = json.loads(chunk)
                except Exception:
                    continue
                if isinstance(obj, dict) and ("result" in obj or "error" in obj):
                    result = obj
        return result
    try:
        return json.loads(text)
    except Exception:
        return {}


def _rpc(url, token, method, params=None, session_id=None, notif=False, rid=1, timeout=45):
    payload = {"jsonrpc": "2.0", "method": method}
    if not notif:
        payload["id"] = rid
    if params is not None:
        payload["params"] = params
    headers = {
        "User-Agent": _UA,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTOCOL,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(url, method="POST", headers=headers,
                                 data=json.dumps(payload).encode())
    try:
        r = urllib.request.urlopen(req, timeout=timeout, context=_CTX)
        sid = r.headers.get("Mcp-Session-Id") or session_id
        return r.status, sid, _parse(r.headers.get("Content-Type"), r.read())
    except urllib.error.HTTPError as e:
        sid = (e.headers.get("Mcp-Session-Id") if e.headers else None) or session_id
        return e.code, sid, _parse(e.headers.get("Content-Type") if e.headers else "",
                                   e.read() if e.fp else b"")


class MCPSession:
    """An initialized JSON-RPC session against one remote MCP server."""

    def __init__(self, url, token=None):
        self.url = url
        self.token = token
        self.session_id = None
        self.server_info = {}
        self.protocol = None

    def initialize(self):
        st, sid, obj = _rpc(self.url, self.token, "initialize", {
            "protocolVersion": PROTOCOL,
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "NX", "version": "0.7"},
        })
        if st == 401:
            raise MCPAuthError("not authorized — connect/sign in first")
        if st >= 400 or not isinstance(obj, dict) or "result" not in obj:
            # Surface WHY: the HTTP status + a snippet of the server's own response (often a JSON-RPC
            # error like "account not configured" / "resource not found") so a failed connect is
            # diagnosable, not an opaque "MCPError". This is what turns mcp_unreachable into an answer.
            try:
                _snip = json.dumps(obj)[:220] if obj else "empty body / no result field"
            except Exception:
                _snip = str(obj)[:220]
            raise MCPError(f"http {st} · {_snip}")
        self.session_id = sid
        res = obj["result"]
        self.server_info = res.get("serverInfo", {})
        self.protocol = res.get("protocolVersion")
        # required: notify the server the handshake is done
        _rpc(self.url, self.token, "notifications/initialized", {}, self.session_id, notif=True)
        return self.server_info

    def list_tools(self):
        st, _, obj = _rpc(self.url, self.token, "tools/list", {}, self.session_id)
        if st == 401:
            raise MCPAuthError("not authorized")
        tools = ((obj or {}).get("result") or {}).get("tools", [])
        # Sanitize at the wire boundary: the server controls this array, so a
        # null/string element must never reach callers that do t.get(...).
        return [t for t in tools if isinstance(t, dict)] if isinstance(tools, list) else []

    def call_tool(self, name, arguments=None):
        st, _, obj = _rpc(self.url, self.token, "tools/call",
                          {"name": name, "arguments": arguments or {}}, self.session_id)
        if st == 401:
            raise MCPAuthError("not authorized")
        if "error" in (obj or {}):
            raise MCPError(obj["error"].get("message", "tool error"))
        return (obj or {}).get("result", {})


def connect_session(slug):
    """Open an authed session for a connected remote MCP server (token from the
    Keychain via nx_mcp_oauth). Returns an initialized MCPSession, or None if the
    service isn't a known remote MCP / isn't connected yet."""
    from nx_mcp_oauth import get_server, usable_token
    entry = get_server(slug)
    if not entry:
        return None
    token = usable_token(slug)   # refreshes silently if the stored token expired
    if not token:
        return None
    s = MCPSession(entry["url"], token)
    s.initialize()
    return s
