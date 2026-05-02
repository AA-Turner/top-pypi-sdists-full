"""WhatsApp bridge — spawns Node.js Baileys process, communicates via JSON-RPC over stdio.

Architecture:
- Node.js subprocess handles ONLY WhatsApp (Baileys socket, auth, media)
- Python handles everything else (AI, screen capture, input injection)
- Communication: NDJSON (newline-delimited JSON) on stdin/stdout
- Node.js logs go to stderr (not stdout) to avoid corrupting the JSON stream
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from collections.abc import Awaitable, Callable

from ghost_pc._node import find_node, find_npm, get_node_env

logger = logging.getLogger(__name__)

# Reconnection backoff settings
INITIAL_BACKOFF = 2.0
MAX_BACKOFF = 60.0
BACKOFF_MULTIPLIER = 2.0


class BaileysBridge:
    """Manages the Node.js Baileys subprocess for WhatsApp connectivity."""

    def __init__(
        self,
        bridge_dir: str,
        credentials_dir: str,
        on_message: Callable[[str, str, str | None], Awaitable[None]],
        on_qr: Callable[[str], None],
        on_connection_change: Callable[[bool], None] | None = None,
    ):
        self.bridge_dir = os.path.abspath(bridge_dir)
        self.credentials_dir = os.path.abspath(credentials_dir)
        self.on_message = on_message  # (from_number, body, media_path) -> None
        self.on_qr = on_qr  # (qr_data) -> None
        self.on_connection_change = on_connection_change  # (connected) -> None
        self._process: asyncio.subprocess.Process | None = None
        self._request_id = 0
        self._pending: dict[int, asyncio.Future[dict | None]] = {}
        self._running = False

    async def run(self) -> None:
        """Start the Node.js bridge with automatic restart on crash."""
        backoff = INITIAL_BACKOFF
        while True:
            try:
                await self._start_bridge()
                # If _start_bridge returns, the process exited
                if not self._running:
                    break  # Intentional stop
                logger.warning(
                    "Bridge process exited unexpectedly, restarting in %.0fs...", backoff
                )
                if self.on_connection_change:
                    self.on_connection_change(False)
                await asyncio.sleep(backoff)
                backoff = min(backoff * BACKOFF_MULTIPLIER, MAX_BACKOFF)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Bridge error: %s, restarting in %.0fs...", e, backoff)
                await asyncio.sleep(backoff)
                backoff = min(backoff * BACKOFF_MULTIPLIER, MAX_BACKOFF)

    async def _start_bridge(self) -> None:
        """Start a single bridge process and wait until it exits."""
        # Check node_modules exists
        node_modules = os.path.join(self.bridge_dir, "node_modules")
        if not os.path.isdir(node_modules):
            logger.info("Installing bridge dependencies...")
            await self._npm_install()

        # Spawn Node.js process (bundled or system)
        node = find_node()
        if not node:
            raise RuntimeError(
                "Node.js not found. If you installed GhostPC via the installer, "
                "please reinstall — the bundled Node.js may be missing."
            )

        entry = os.path.join(self.bridge_dir, "index.js")
        if not os.path.exists(entry):
            raise RuntimeError(f"Bridge entry point not found: {entry}")

        env = {
            **get_node_env(),
            "GHOST_CREDENTIALS_DIR": self.credentials_dir,
        }

        self._process = await asyncio.create_subprocess_exec(
            node,
            entry,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.bridge_dir,
            env=env,
        )

        self._running = True
        logger.info("WhatsApp bridge started (PID: %d)", self._process.pid)

        # Read stdout (JSON events) and stderr (logs) concurrently
        try:
            await asyncio.gather(
                self._read_stdout(),
                self._read_stderr(),
            )
        finally:
            # Cancel all pending RPC futures
            for future in self._pending.values():
                if not future.done():
                    future.cancel()
            self._pending.clear()

    async def stop(self) -> None:
        """Stop the bridge subprocess."""
        self._running = False
        if self._process:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5)
            except TimeoutError:
                self._process.kill()
            self._process = None

    async def send_text(self, to: str, text: str) -> None:
        """Send a text message via WhatsApp."""
        await self._rpc("send_text", {"to": to, "text": text})

    async def send_image(self, to: str, path: str, caption: str = "") -> None:
        """Send an image via WhatsApp."""
        await self._rpc("send_image", {"to": to, "path": os.path.abspath(path), "caption": caption})

    async def send_video(self, to: str, path: str, caption: str = "") -> None:
        """Send a video via WhatsApp."""
        await self._rpc("send_video", {"to": to, "path": os.path.abspath(path), "caption": caption})

    async def send_document(self, to: str, path: str, filename: str = "") -> None:
        """Send a document/file via WhatsApp."""
        await self._rpc(
            "send_document",
            {
                "to": to,
                "path": os.path.abspath(path),
                "filename": filename or os.path.basename(path),
            },
        )

    async def send_voice(self, to: str, path: str) -> None:
        """Send a voice note (OGG Opus) via WhatsApp.

        Args:
            to: Recipient phone number.
            path: Path to the OGG Opus audio file.
        """
        await self._rpc("send_voice", {"to": to, "path": os.path.abspath(path)})

    async def send_composing(self, to: str) -> None:
        """Send typing indicator."""
        await self._rpc("send_composing", {"to": to})

    # --- Internal ---

    async def _rpc(self, method: str, params: dict) -> dict | None:
        """Send a JSON-RPC request to the Node.js process and wait for response."""
        if not self._process or not self._process.stdin:
            logger.warning("Bridge not running, can't send RPC")
            return None

        self._request_id += 1
        request_id = self._request_id

        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }

        future: asyncio.Future[dict | None] = asyncio.get_running_loop().create_future()
        self._pending[request_id] = future

        line = json.dumps(request) + "\n"
        self._process.stdin.write(line.encode())
        await self._process.stdin.drain()

        try:
            result = await asyncio.wait_for(future, timeout=30)
            return result
        except TimeoutError:
            self._pending.pop(request_id, None)
            logger.warning("RPC timeout: %s", method)
            return None

    async def _read_stdout(self) -> None:
        """Read JSON events from Node.js stdout."""
        if not self._process or not self._process.stdout:
            return

        while self._running:
            try:
                line = await self._process.stdout.readline()
                if not line:
                    break  # Process exited

                data = json.loads(line.decode())
                await self._handle_event(data)
            except json.JSONDecodeError:
                logger.debug("Non-JSON from bridge: %r", line)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error reading bridge stdout: %s", e)

    async def _read_stderr(self) -> None:
        """Read logs from Node.js stderr."""
        if not self._process or not self._process.stderr:
            return

        while self._running:
            try:
                line = await self._process.stderr.readline()
                if not line:
                    break
                logger.debug("[bridge] %s", line.decode().strip())
            except asyncio.CancelledError:
                break
            except Exception:
                pass

    async def _handle_event(self, data: dict) -> None:
        """Handle a JSON event from the Node.js bridge.

        IMPORTANT: Message handling is dispatched via create_task (not awaited)
        to avoid deadlocking the stdout reader. The stdout pipe carries both
        incoming events AND RPC responses. If we ``await on_message(...)`` here,
        handle_message will call send_composing / send_text which issue RPCs
        that wait for a response on stdout — but _read_stdout is blocked
        waiting for on_message to finish → deadlock (times out after 30 s,
        silently drops the reply).
        """
        # JSON-RPC response (has "id" field)
        if "id" in data and data["id"] in self._pending:
            future = self._pending.pop(data["id"])
            if "error" in data:
                future.set_exception(RuntimeError(data["error"].get("message", "Unknown error")))
            else:
                future.set_result(data.get("result"))
            return

        # JSON-RPC notification (no "id" field, has "method")
        method = data.get("method")
        params = data.get("params", {})

        if method == "event":
            event_type = params.get("type")

            if event_type == "qr":
                self.on_qr(params["data"]["qr"])

            elif event_type == "connection.update":
                conn = params.get("data", {})
                if conn.get("connection") == "open":
                    logger.info("WhatsApp connected!")
                    if self.on_connection_change:
                        self.on_connection_change(True)
                elif conn.get("connection") == "close":
                    logger.info("WhatsApp disconnected")
                    if self.on_connection_change:
                        self.on_connection_change(False)

            elif event_type == "message":
                from_number = params["data"].get("from", "")
                body = params["data"].get("body", "")
                media_path = params["data"].get("mediaPath")
                # Dispatch without blocking _read_stdout so RPC responses
                # (send_composing, send_text) can still be read from stdout.
                asyncio.create_task(self._dispatch_message(from_number, body, media_path))

    async def _dispatch_message(self, from_number: str, body: str, media_path: str | None) -> None:
        """Process an incoming message in a separate task."""
        try:
            await self.on_message(from_number, body, media_path)
        except Exception:
            logger.error("Error handling message from %s", from_number, exc_info=True)

    async def _npm_install(self) -> None:
        """Run npm install in the bridge directory."""
        npm = find_npm()
        if not npm:
            raise RuntimeError(
                "npm not found. If you installed GhostPC via the installer, "
                "please reinstall — the bundled Node.js may be missing."
            )
        proc = await asyncio.create_subprocess_exec(
            npm,
            "install",
            cwd=self.bridge_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=get_node_env(),
        )
        await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError("npm install failed for bridge dependencies")
