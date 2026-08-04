"""Per-workspace web session: owns chat history + DEV/PENTEST engines and
fans engine events (emitted on worker threads) out to connected WS clients.

Both DevSession and PentestSession call an ``on_event(type, data)`` callback
from a background thread. We marshal each event onto every client's asyncio
queue via ``loop.call_soon_threadsafe`` so the async WS handlers stay simple.
"""
from __future__ import annotations

import asyncio
import threading
from pathlib import Path
from typing import Any

from .bridge import PentestSession, extract_target
from .dev import DevSession, extract_code_block, parse_file_hint
from .history import ChatHistory


class WebSession:
    def __init__(self, root: Path, config) -> None:
        self.root = Path(root).resolve()
        self.config = config
        self.history = ChatHistory(self.root)
        self._clients: set[asyncio.Queue] = set()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._lock = threading.Lock()
        self._dev = DevSession(config, self._on_dev_event)
        self._pentest = PentestSession(config, self._on_pentest_event)
        self._dev_buf = ""  # accumulates streamed reply for history
        self.findings: list[dict] = []  # for reconnect replay
        self.stats: dict = {}
        self._auth: dict = {"active": False}  # in-memory creds only, never saved

    # ── client registry ──────────────────────────────────────────
    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def attach(self, q: asyncio.Queue) -> None:
        with self._lock:
            self._clients.add(q)

    def detach(self, q: asyncio.Queue) -> None:
        with self._lock:
            self._clients.discard(q)

    def broadcast(self, etype: str, data: dict[str, Any]) -> None:
        """Thread-safe fan-out to every connected WS client."""
        msg = {"type": etype, "data": data}
        if self._loop is None:
            return
        with self._lock:
            clients = list(self._clients)
        for q in clients:
            self._loop.call_soon_threadsafe(self._safe_put, q, msg)

    @staticmethod
    def _safe_put(q: asyncio.Queue, msg: dict) -> None:
        try:
            q.put_nowait(msg)
        except asyncio.QueueFull:
            pass

    # ── DEV mode ──────────────────────────────────────────────────
    def dev_ask(self, message: str, file_name: str = "", file_text: str = "") -> None:
        self.history.add("user", message)
        self._dev_buf = ""
        self._dev.ask(message, file_name, file_text, history=self.history.context())

    def _on_dev_event(self, etype: str, data: dict) -> None:
        if etype == "dev_chunk":
            self._dev_buf += data.get("text", "")
        elif etype == "dev_done":
            full = data.get("full", "") or self._dev_buf
            if full:
                self.history.add("assistant", full)
            data = {"full": full, "file": self._dev_extract_file(full)}
        self.broadcast(etype, data)

    @staticmethod
    def _dev_extract_file(full: str) -> dict | None:
        """Pull an updated file (FILE: hint + fenced block) out of a reply."""
        code = extract_code_block(full)
        if not code:
            return None
        name = ""
        for line in full.splitlines():
            hint = parse_file_hint(line)
            if hint:
                name = hint
                break
        return {"name": name, "text": code}

    # ── PENTEST mode ──────────────────────────────────────────────
    def pentest_start(self, message: str) -> str:
        target = extract_target(message)
        if not target:
            self.broadcast("dev_error", {"error": "No target URL in message."})
            return ""
        self.history.add("user", message)
        self._pentest.start(target, message)
        return target

    def pentest_hint(self, text: str) -> None:
        self._pentest.send_hint(text)

    def pentest_stop(self) -> None:
        self._pentest.stop()

    @property
    def pentest_running(self) -> bool:
        return self._pentest.running

    # ── slash commands (web port of the classic CLI palette) ──────
    def run_command(self, name: str, arg: str = "") -> dict:
        """Execute a /command. Returns {text?, action?, ok}.

        `action` is a hint for the client (clear|export|history|settings|
        retry|help). Engine-heavy commands reuse the existing sessions.
        """
        from .commands import dispatch_command
        return dispatch_command(self, name.lower().strip(), arg.strip())

    def target_hint(self) -> str:
        return getattr(self._pentest, "target", "") or ""

    def build_report(self, arg: str = "") -> dict:
        n = len(self.findings)
        if n == 0:
            return {"ok": True, "text": "No confirmed findings yet. "
                    "Run a pentest to gather proof-by-exploitation evidence."}
        lines = [f"Report — {n} finding(s):"]
        for f in self.findings[:40]:
            sev = str(f.get("severity", "info")).upper()
            title = f.get("title") or f.get("name") or f.get("type") or "finding"
            lines.append(f"  [{sev}] {title}")
        return {"ok": True, "text": "\n".join(lines)}

    def crack_hash(self, arg: str) -> dict:
        h = arg.strip()
        if not h:
            return {"ok": False, "text": "Usage: /crack <hash>"}
        try:
            from ..tools.hash_crack import HashCracker, detect_hash_type
            info = detect_hash_type(h)
            res = HashCracker().crack(h)
        except Exception as exc:
            return {"ok": False, "text": f"Crack error: {exc}"}
        if res.cracked:
            return {"ok": True,
                    "text": f"CRACKED [{info.hash_type}] → {res.plaintext}"}
        return {"ok": True, "text": f"Not cracked [{info.hash_type}] "
                f"({res.error or 'no match in wordlist'})"}

    # Credentials live in-memory only; never persisted, secrets never echoed.
    def manage_creds(self, arg: str) -> dict:
        parts = arg.split()
        if not parts or parts[0] == "list":
            a = self._auth
            if not a.get("active"):
                return {"ok": True, "text": "No saved credentials."}
            return {"ok": True, "text": "Saved credentials:\n"
                    f"  URL: {a.get('login_url') or '(N/A)'}\n"
                    f"  ID:  {a.get('username')}\n"
                    f"  PW:  {'*' * len(a.get('password', ''))}"}
        if parts[0] in ("del", "clear"):
            self._auth = {"active": False}
            return {"ok": True, "text": "Credentials cleared."}
        if len(parts) < 2:
            return {"ok": False,
                    "text": "Usage: /cred <username> <password>  |  /cred list  |  /cred del"}
        self._auth = {"active": True, "login_url": self._auth.get("login_url", ""),
                      "username": parts[0], "password": parts[1]}
        return {"ok": True,
                "text": f"Credentials saved (in-memory). ID: {parts[0]}  PW: {'*' * len(parts[1])}"}

    def register_login(self, arg: str) -> dict:
        parts = arg.split()
        if not parts:
            return {"ok": False,
                    "text": "Usage: /login <url> [user] [pass]"}
        self._auth = {"active": True, "login_url": parts[0],
                      "username": parts[1] if len(parts) > 1 else "",
                      "password": parts[2] if len(parts) > 2 else ""}
        pw = self._auth["password"]
        return {"ok": True, "text": f"Login target set: {parts[0]}"
                + (f"  ID: {self._auth['username']}" if self._auth["username"] else "")
                + (f"  PW: {'*' * len(pw)}" if pw else "")}

    def load_session_file(self, arg: str) -> dict:
        import os
        import re
        p = arg.strip()
        if not p:
            return {"ok": False, "text": "Usage: /load <session-file-path>"}
        path = os.path.expanduser(os.path.expandvars(p))
        if not os.path.isfile(path):
            return {"ok": False, "text": f"File not found: {path}"}
        try:
            raw = open(path, encoding="utf-8", errors="replace").read()
        except OSError as exc:
            return {"ok": False, "text": f"Read error: {exc}"}
        pat = re.compile(r"###\s+\*\*(YOU|bingo)\*\*[^\n]*\n(.*?)"
                         r"(?=\n###\s+\*\*(?:YOU|bingo)\*\*|\Z)", re.DOTALL)
        m = pat.findall(raw)
        if not m:
            return {"ok": False, "text": "Not a Bingo session file (no turns parsed)."}
        self.history.clear()
        for speaker, content in m:
            self.history.add("user" if speaker == "YOU" else "assistant",
                             content.strip())
        return {"ok": True, "action": "history",
                "text": f"Session loaded — {len(m)} messages restored."}

    def _on_pentest_event(self, etype: str, data: dict) -> None:
        if etype == "finding":
            self.findings.append(data)
        elif etype == "stats":
            self.stats = data
        self.broadcast(etype, data)

    # ── file tree ─────────────────────────────────────────────────
    _SKIP = {".git", "__pycache__", "node_modules", ".venv", "venv",
             ".bingo", ".mypy_cache", ".pytest_cache", "dist", "build"}

    def list_tree(self, rel: str = "") -> list[dict]:
        """One directory level under ``rel``; dirs first, name-sorted."""
        from .security import safe_resolve

        base = safe_resolve(self.root, rel) if rel else self.root
        if base is None or not base.is_dir():
            return []
        out: list[dict] = []
        try:
            entries = sorted(base.iterdir(),
                             key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError:
            return []
        for p in entries:
            if p.name in self._SKIP or p.name.startswith("."):
                continue
            out.append({
                "name": p.name,
                "path": str(p.relative_to(self.root)),
                "dir": p.is_dir(),
            })
        return out

    # ── automation (scan / waf) ───────────────────────────────────
    def run_scan(self, target: str) -> None:
        """Full RedTeam pipeline; streams progress as auto_* events."""
        target = extract_target(target) or target

        def _work() -> None:
            self.broadcast("auto_start", {"mode": "scan", "target": target})
            try:
                from ..redteam.pipeline import RedTeamPipeline
                from ..redteam.log_i18n import localize_log
                from ..core.authorization import create_auth_context

                lang = getattr(self.config, "lang", "en")
                model_cfg = (self.config.get_active_model_config()
                             if self.config.models else None)
                pipeline = RedTeamPipeline(
                    target=target, model_config=model_cfg, output_dir=".",
                    on_progress=lambda m: self.broadcast(
                        "auto_log", {"msg": localize_log(m, lang)}),
                    auth_ctx=create_auth_context(target),
                )
                report = pipeline.run()
                self.broadcast("auto_done", {"mode": "scan", "report": str(report)})
            except Exception as exc:
                self.broadcast("auto_error", {"mode": "scan", "error": str(exc)})

        threading.Thread(target=_work, daemon=True, name="bingo-scan").start()

    def run_waf(self, target: str) -> None:
        """WAF detect + bypass probe; streams progress as auto_* events."""
        target = extract_target(target) or target

        def _work() -> None:
            self.broadcast("auto_start", {"mode": "waf", "target": target})
            try:
                from ..tools.http_probe import HttpProbe
                from ..tools.waf_bypass import WafDetector, WafBypassEngine
                from ..redteam.log_i18n import localize_log

                lang = getattr(self.config, "lang", "en")
                probe = HttpProbe(target)
                result = WafDetector(probe).detect(target)
                self.broadcast("auto_log", {
                    "msg": f"WAF detected={result.detected} "
                           f"type={result.waf_type} conf={result.confidence}"})
                if result.detected:
                    engine = WafBypassEngine(
                        probe,
                        on_progress=lambda m: self.broadcast(
                            "auto_log", {"msg": localize_log(m, lang)}))
                    ok, att = engine.auto_bypass(target + "?id=1", "' OR 1=1--")
                    self.broadcast("auto_log", {
                        "msg": f"bypass ok={ok} "
                               f"technique={getattr(att, 'technique', '')}"})
                self.broadcast("auto_done", {"mode": "waf"})
            except Exception as exc:
                self.broadcast("auto_error", {"mode": "waf", "error": str(exc)})

        threading.Thread(target=_work, daemon=True, name="bingo-waf").start()
