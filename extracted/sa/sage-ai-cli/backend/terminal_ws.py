"""WebSocket terminal handler for running sage-ai-cli in the browser.

Provides:
- PTY-based terminal emulation via WebSocket (when available)
- Simulated terminal for serverless environments (Cloud Run, etc.)
- Auto-update checking and application for sage-ai-cli
- WebGL-accelerated rendering support via xterm.js
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect
from sage.core.updater import (
    CLIAutoUpdater,
    CLIVersion,
    build_sage_run_command,
)

# PTY imports - may not be available on all platforms
try:
    import pty
    import select
    import signal
    import struct
    import termios
    import fcntl
    PTY_AVAILABLE = True
except ImportError:
    PTY_AVAILABLE = False

logger = logging.getLogger("ai-platform.terminal")

class SimulatedTerminalSession:
    """Simulated terminal session for serverless environments (no PTY required).

    This provides a SAGE CLI-like experience using the chat API,
    allowing the terminal to work on Cloud Run and other serverless platforms.
    """

    # ANSI color codes for terminal styling
    RESET = "\x1b[0m"
    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    GREEN = "\x1b[32m"
    CYAN = "\x1b[36m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    WHITE = "\x1b[37m"

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self._running = False
        self._input_buffer = ""
        self._history: list[dict] = []
        self._model_id = "ollama:llama3.2"  # Default local model via Ollama

    async def start(self, command: list[str] | None = None):
        """Start the simulated terminal session."""
        self._running = True

        # Send welcome banner
        await self._send_output(self._get_welcome_banner())
        await self._send_prompt()

    def _get_welcome_banner(self) -> str:
        """Generate the SAGE CLI welcome banner."""
        current_version = cli_updater.get_current_version()

        banner = f"""
{self.CYAN}╔══════════════════════════════════════════════════════════════════╗{self.RESET}
{self.CYAN}║{self.RESET}  {self.BOLD}{self.GREEN}🌿 SAGE AI CLI{self.RESET} v{current_version}                                      {self.CYAN}║{self.RESET}
{self.CYAN}║{self.RESET}  {self.DIM}Local-first AI coding assistant (Web Terminal){self.RESET}                 {self.CYAN}║{self.RESET}
{self.CYAN}╚══════════════════════════════════════════════════════════════════╝{self.RESET}

{self.YELLOW}Model:{self.RESET} {self.GREEN}{self._model_id}{self.RESET} (local via Ollama)

{self.DIM}Type your message and press Enter. Commands:{self.RESET}
  {self.CYAN}/model <name>{self.RESET}  - Switch model (e.g., /model ollama:qwen2.5-coder:7b)
  {self.CYAN}/models{self.RESET}        - Show common local Ollama tags
  {self.CYAN}/clear{self.RESET}         - Clear conversation history
  {self.CYAN}/update{self.RESET}        - Update SAGE AI to the latest CLI release
  {self.CYAN}/help{self.RESET}          - Show help

"""
        return banner

    async def _send_output(self, text: str):
        """Send output to the terminal."""
        await self.websocket.send_json({
            "type": "output",
            "data": text,
        })

    async def _send_prompt(self):
        """Send the input prompt."""
        prompt = f"\r\n{self.GREEN}sage>{self.RESET} "
        await self._send_output(prompt)

    async def write(self, data: str):
        """Handle terminal input."""
        for char in data:
            if char == "\r" or char == "\n":
                # Enter pressed - process input
                await self._process_input()
            elif char == "\x7f" or char == "\x08":
                # Backspace
                if self._input_buffer:
                    self._input_buffer = self._input_buffer[:-1]
                    await self._send_output("\x08 \x08")  # Erase character
            elif char == "\x03":
                # Ctrl+C
                self._input_buffer = ""
                await self._send_output("^C")
                await self._send_prompt()
            elif char >= " " or char == "\t":
                # Regular character
                self._input_buffer += char
                await self._send_output(char)

    async def _process_input(self):
        """Process the entered command/message."""
        user_input = self._input_buffer.strip()
        self._input_buffer = ""

        await self._send_output("\r\n")

        if not user_input:
            await self._send_prompt()
            return

        # Handle commands
        if user_input.startswith("/"):
            await self._handle_command(user_input)
            return

        # Regular chat message - send to AI
        await self._chat(user_input)

    async def _handle_command(self, cmd: str):
        """Handle terminal commands."""
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command == "/help":
            help_text = f"""
{self.BOLD}SAGE CLI Commands:{self.RESET}

  {self.CYAN}/model <name>{self.RESET}   Switch to a different model
                    Example: /model ollama:llama3.2

  {self.CYAN}/models{self.RESET}         Show common Ollama model tags

  {self.CYAN}/clear{self.RESET}          Clear conversation history

  {self.CYAN}/update{self.RESET}         Update SAGE AI to the latest CLI version

  {self.CYAN}/help{self.RESET}           Show this help message

{self.DIM}Just type your message to chat with the AI.{self.RESET}
"""
            await self._send_output(help_text)

        elif command == "/models":
            models_text = f"""
{self.BOLD}Common local models (Ollama){self.RESET}

  {self.GREEN}ollama:llama3.2{self.RESET}
  {self.GREEN}ollama:qwen2.5-coder:7b{self.RESET}
  {self.GREEN}ollama:deepseek-r1:8b{self.RESET}
  {self.GREEN}ollama:gemma3:4b{self.RESET}

{self.DIM}Install: ollama pull <tag>  ·  Use /model ollama:<tag>{self.RESET}
"""
            await self._send_output(models_text)

        elif command == "/model":
            if arg:
                # Normalize model name
                if not arg.startswith("ollama:") and not arg.startswith("llama_cpp:"):
                    arg = f"ollama:{arg}"
                self._model_id = arg
                await self._send_output(f"{self.GREEN}✓{self.RESET} Switched to model: {self.CYAN}{self._model_id}{self.RESET}\r\n")
            else:
                await self._send_output(f"{self.YELLOW}Current model:{self.RESET} {self.CYAN}{self._model_id}{self.RESET}\r\n")
                await self._send_output(f"{self.DIM}Usage: /model <name>{self.RESET}\r\n")

        elif command == "/clear":
            self._history = []
            await self._send_output(f"{self.GREEN}✓{self.RESET} Conversation history cleared.\r\n")

        elif command == "/update":
            await self._send_output(
                f"{self.DIM}Checking for the latest SAGE AI release...{self.RESET}\r\n"
            )
            result = await asyncio.to_thread(cli_updater.ensure_latest)
            color = self.GREEN if result.ok else self.YELLOW
            symbol = "✓" if result.ok else "⚠"
            await self._send_output(
                f"{color}{symbol}{self.RESET} {result.message}\r\n"
            )
            if result.updated:
                await self._send_output(
                    f"{self.DIM}Restart this web terminal session to load the freshly updated CLI runtime.{self.RESET}\r\n"
                )

        else:
            await self._send_output(f"{self.YELLOW}Unknown command:{self.RESET} {command}\r\n")
            await self._send_output(f"{self.DIM}Type /help for available commands.{self.RESET}\r\n")

        await self._send_prompt()

    async def _chat(self, message: str):
        """Send message to local Ollama."""
        self._history.append({"role": "user", "content": message})
        await self._send_output(f"{self.DIM}Thinking...{self.RESET}")
        try:
            await self._chat_ollama()
        except Exception as e:
            await self._send_output(f"\r\n{self.YELLOW}Error: {e}{self.RESET}\r\n")
        await self._send_prompt()

    async def _chat_ollama(self) -> None:
        """Call Ollama HTTP API (localhost)."""
        import httpx

        await self._send_output("\r" + " " * 20 + "\r")

        mid = self._model_id
        if mid.startswith("ollama:"):
            model_name = mid.split(":", 1)[1]
        elif mid.startswith("llama_cpp:"):
            raise RuntimeError("Web terminal uses Ollama only — switch with /model ollama:<tag>")
        else:
            model_name = mid

        payload = {
            "model": model_name,
            "messages": self._history[-20:],
            "stream": False,
            "options": {"temperature": 0.7},
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post("http://127.0.0.1:11434/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            text = (data.get("message") or {}).get("content") or ""
            if text:
                await self._send_output(text + "\r\n")
                self._history.append({"role": "assistant", "content": text})

    async def resize(self, cols: int, rows: int):
        """Handle terminal resize (no-op for simulated terminal)."""
        pass

    async def stop(self):
        """Stop the simulated terminal session."""
        self._running = False


class TerminalSession:
    """Manages a PTY session for a WebSocket connection."""

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.master_fd: int | None = None
        self.pid: int | None = None
        self._running = False
        self._read_task: asyncio.Task | None = None

    async def start(self, command: list[str] | None = None):
        """Start the terminal session with sage-ai-cli."""
        if not PTY_AVAILABLE:
            raise RuntimeError("PTY not available on this platform")

        if command is None:
            command = build_sage_run_command()

        # Create PTY
        pid, master_fd = pty.fork()

        if pid == 0:
            # Child process
            os.environ["TERM"] = "xterm-256color"
            os.environ["COLORTERM"] = "truecolor"
            os.environ["SAGE_TERMINAL"] = "web"
            try:
                os.execvp(command[0], command)
            except Exception:
                # Fallback to bash if sage not found
                os.execvp("/bin/bash", ["/bin/bash"])
        else:
            # Parent process
            self.pid = pid
            self.master_fd = master_fd
            self._running = True

            # Set non-blocking
            flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
            fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

            # Start reading task
            self._read_task = asyncio.create_task(self._read_loop())

    async def _read_loop(self):
        """Read output from PTY and send to WebSocket."""
        while self._running and self.master_fd is not None:
            try:
                # Use select with timeout to check for data
                readable, _, _ = select.select([self.master_fd], [], [], 0.1)

                if readable:
                    try:
                        data = os.read(self.master_fd, 4096)
                        if data:
                            await self.websocket.send_json({
                                "type": "output",
                                "data": data.decode("utf-8", errors="replace"),
                            })
                        else:
                            # EOF
                            break
                    except OSError:
                        break
                else:
                    # No data, yield to event loop
                    await asyncio.sleep(0.01)

            except Exception as e:
                logger.error("Error in read loop: %s", e)
                break

        self._running = False

    async def write(self, data: str):
        """Write input to the PTY."""
        if self.master_fd is not None:
            try:
                os.write(self.master_fd, data.encode("utf-8"))
            except OSError as e:
                logger.error("Error writing to PTY: %s", e)

    async def resize(self, cols: int, rows: int):
        """Resize the PTY window."""
        if PTY_AVAILABLE and self.master_fd is not None:
            try:
                winsize = struct.pack("HHHH", rows, cols, 0, 0)
                fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
            except OSError as e:
                logger.error("Error resizing PTY: %s", e)

    async def stop(self):
        """Stop the terminal session."""
        self._running = False

        if self._read_task:
            self._read_task.cancel()
            try:
                await self._read_task
            except asyncio.CancelledError:
                pass

        if PTY_AVAILABLE and self.pid is not None:
            try:
                os.kill(self.pid, signal.SIGTERM)
                os.waitpid(self.pid, os.WNOHANG)
            except OSError:
                pass

        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except OSError:
                pass


# Global auto-updater instance
cli_updater = CLIAutoUpdater()


# ══════════════════════════════════════════════════════════════════════════════
# TERMINAL SECURITY - Authentication and Rate Limiting
# ══════════════════════════════════════════════════════════════════════════════

def _require_terminal_auth(
    token: str | None,
    production_mode: bool,
    valid_tokens: set[str] | None = None
) -> bool:
    """Require authentication for terminal WebSocket.

    Accepts either:
    - A valid Firebase ID token (any logged-in SAGE user)
    - The admin_token secret (legacy / admin access)

    In development mode, allows unauthenticated access.
    """
    from backend.config import settings

    # Test mode override
    if valid_tokens is not None:
        return token in valid_tokens

    # Development mode — open access for local testing
    if not production_mode:
        return True

    if not token:
        return False

    # 1. Try Firebase ID token (standard user auth, same as all other endpoints)
    try:
        import os, httpx, time

        _FIREBASE_API_KEY = os.environ.get("VITE_FIREBASE_API_KEY", "")
        if _FIREBASE_API_KEY:
            r = httpx.post(
                f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={_FIREBASE_API_KEY}",
                json={"idToken": token},
                timeout=8,
            )
            if r.is_success and r.json().get("users"):
                return True
    except Exception:
        pass

    # 2. Fall back to admin_token secret
    expected = (settings.admin_token or "").strip()
    if expected and token == expected:
        return True

    return False


def _check_terminal_rate_limit(client_ip: str) -> tuple[bool, str]:
    """Check if client has exceeded terminal connection rate limit.

    Args:
        client_ip: Client IP address

    Returns:
        Tuple of (allowed, reason)
    """
    from backend.app import get_app_state

    state = get_app_state()
    rate_limiter = _get_terminal_rate_limiter()

    # Check connection count
    if not rate_limiter.is_allowed(client_ip):
        return False, "Terminal connection rate limit exceeded"

    return True, ""


class _TerminalRateLimiter:
    """Rate limiter specifically for terminal WebSocket connections."""

    def __init__(self, max_connections_per_ip: int = 5, time_window_seconds: int = 60):
        """Initialize rate limiter.

        Args:
            max_connections_per_ip: Maximum connections per IP in time window
            time_window_seconds: Time window in seconds
        """
        self.max_connections_per_ip = max_connections_per_ip
        self.time_window_seconds = time_window_seconds
        self._connection_counts: dict[str, list[float]] = {}

    def is_allowed(self, client_ip: str) -> bool:
        """Check if client is allowed to connect.

        Args:
            client_ip: Client IP address

        Returns:
            True if allowed, False if rate limit exceeded
        """
        import time

        now = time.time()
        cutoff = now - self.time_window_seconds

        # Get connection timestamps for this IP
        if client_ip not in self._connection_counts:
            self._connection_counts[client_ip] = []

        # Remove old connections outside the time window
        self._connection_counts[client_ip] = [
            ts for ts in self._connection_counts[client_ip]
            if ts > cutoff
        ]

        # Check if under limit
        if len(self._connection_counts[client_ip]) >= self.max_connections_per_ip:
            return False

        # Record this connection
        self._connection_counts[client_ip].append(now)
        return True


# Global terminal rate limiter — generous enough to survive normal page-mount churn
# (React StrictMode double-mounts, tab switches) without locking users out.
_terminal_rate_limiter = _TerminalRateLimiter(
    max_connections_per_ip=30,
    time_window_seconds=60
)


def _get_terminal_rate_limiter() -> _TerminalRateLimiter:
    """Get the global terminal rate limiter."""
    return _terminal_rate_limiter


def _should_use_simulated_terminal() -> bool:
    """Check if we should use the simulated terminal instead of PTY.

    Returns True if:
    - PTY is not available (Windows, serverless platforms)
    - Running in Cloud Run or similar serverless environment
    - PTY fork fails
    """
    # Check if PTY module is available
    if not PTY_AVAILABLE:
        logger.info("PTY not available, using simulated terminal")
        return True

    # Check for Cloud Run environment
    if os.environ.get("K_SERVICE") or os.environ.get("CLOUD_RUN_JOB"):
        logger.info("Cloud Run detected, using simulated terminal")
        return True

    # Check for other serverless indicators
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        logger.info("AWS Lambda detected, using simulated terminal")
        return True

    if os.environ.get("FUNCTIONS_WORKER_RUNTIME"):
        logger.info("Azure Functions detected, using simulated terminal")
        return True

    # Check if we can actually fork (some containers restrict this)
    try:
        # Quick test - try to access pty functions
        if PTY_AVAILABLE:
            # Test if /dev/ptmx exists (required for PTY)
            if not os.path.exists("/dev/ptmx"):
                logger.info("/dev/ptmx not found, using simulated terminal")
                return True
    except Exception as e:
        logger.info(f"PTY check failed ({e}), using simulated terminal")
        return True

    return False


async def terminal_websocket_handler(websocket: WebSocket):
    """Handle WebSocket connection for terminal."""
    from backend.config import settings

    # CRITICAL: Accept the WebSocket BEFORE any close() so our custom close codes
    # (4003 auth, 4029 rate limit) actually reach the client. If we close before
    # accept, the browser sees "WebSocket closed before connection established"
    # with generic code 1006 — and our frontend retries, hitting the rate limit
    # again, creating an infinite reconnect loop.
    await websocket.accept()

    # Rate limit check (DoS protection)
    client_ip = websocket.client.host if websocket.client else "unknown"
    allowed, reason = _check_terminal_rate_limit(client_ip)
    if not allowed:
        await websocket.close(code=4029, reason=reason)
        return

    # Authentication — extract token from query params or Authorization header
    token = websocket.query_params.get("token", "")
    if not token:
        auth_header = websocket.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

    if not _require_terminal_auth(token, settings.is_production):
        await websocket.close(code=4003, reason="Authentication required")
        return

    # Decide which terminal session type to use
    use_simulated = _should_use_simulated_terminal()

    if use_simulated:
        session = SimulatedTerminalSession(websocket)
    else:
        session = TerminalSession(websocket)

    try:
        # Auto-update only makes sense for a real local PTY terminal (the user's
        # machine). For simulated/Cloud Run sessions we skip it — running
        # `pip install --upgrade` on the server from a WebSocket handler is
        # slow, dangerous, and the user can't benefit from it anyway.
        if not use_simulated:
            try:
                update_result = await asyncio.wait_for(
                    asyncio.to_thread(cli_updater.ensure_latest),
                    timeout=15,
                )
                if update_result.updated:
                    await websocket.send_json({
                        "type": "update_applied",
                        "info": {
                            "current_version": update_result.current,
                            "latest_version": update_result.latest,
                            "message": update_result.message,
                        },
                    })
                elif update_result.attempted and not update_result.ok:
                    await websocket.send_json({
                        "type": "update_failed",
                        "info": {
                            "current_version": update_result.current,
                            "latest_version": update_result.latest,
                            "message": update_result.message,
                        },
                    })

                version_info = cli_updater.check_for_update()
                if version_info.update_available:
                    await websocket.send_json({
                        "type": "update_available",
                        "info": {
                            "current_version": version_info.current,
                            "latest_version": version_info.latest,
                        },
                    })
            except (asyncio.TimeoutError, Exception) as e:
                logger.debug("Update check skipped: %s", e)

        # Start terminal session
        try:
            await session.start()
        except RuntimeError as e:
            # PTY failed, fall back to simulated
            if not use_simulated:
                logger.warning(f"PTY session failed ({e}), falling back to simulated terminal")
                session = SimulatedTerminalSession(websocket)
                await session.start()

        # Handle incoming messages
        while True:
            try:
                message = await websocket.receive_json()
                msg_type = message.get("type")

                if msg_type == "input":
                    await session.write(message.get("data", ""))
                elif msg_type == "resize":
                    cols = message.get("cols", 80)
                    rows = message.get("rows", 24)
                    # Bounds check to prevent DoS via extreme values
                    cols = max(10, min(500, int(cols) if isinstance(cols, (int, float)) else 80))
                    rows = max(5, min(200, int(rows) if isinstance(rows, (int, float)) else 24))
                    await session.resize(cols, rows)

            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error("Error handling message: %s", e)
                break

    finally:
        await session.stop()


def get_cli_update_info() -> dict[str, Any]:
    """Get CLI update information for REST API."""
    version_info = cli_updater.check_for_update()
    return {
        "current_version": version_info.current,
        "latest_version": version_info.latest,
        "update_available": version_info.update_available,
    }


def apply_cli_update() -> dict[str, Any]:
    """Apply CLI update via REST API."""
    result = cli_updater.ensure_latest()
    return {
        "ok": result.ok,
        "updated": result.updated,
        "current_version": result.current,
        "latest_version": result.latest,
        "message": result.message,
    }
