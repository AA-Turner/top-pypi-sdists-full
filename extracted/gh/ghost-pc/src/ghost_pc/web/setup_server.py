"""Web-based setup wizard backend — aiohttp server on port 9876."""

from __future__ import annotations

import asyncio
import json
import logging
import shutil
import subprocess
import sys
import webbrowser
from typing import Any

from aiohttp import WSMsgType, web

from ghost_pc import __version__
from ghost_pc._node import find_node, find_npm, get_node_env
from ghost_pc.config.schema import GHOST_HOME, GhostConfig
from ghost_pc.web import get_web_root

logger = logging.getLogger(__name__)

_SETUP_PORT = 9876


class SetupServer:
    """Standalone aiohttp server for the browser-based setup wizard."""

    def __init__(self) -> None:
        self._app: web.Application | None = None
        self._runner: web.AppRunner | None = None
        self._done = asyncio.Event()
        self._auto_start: bool = False
        self._ws_clients: list[web.WebSocketResponse] = []

    # ── Routes ──────────────────────────────────────────────────────

    async def _handle_setup_page(self, request: web.Request) -> web.Response:
        """Serve the setup wizard HTML."""
        template = get_web_root() / "templates" / "setup.html"
        html = template.read_text(encoding="utf-8")
        return web.Response(text=html, content_type="text/html")

    async def _handle_static(self, request: web.Request) -> web.FileResponse:
        """Serve static files (CSS/JS/images)."""
        rel_path = request.match_info["path"]
        file_path = get_web_root() / "static" / rel_path
        if not file_path.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(file_path)

    async def _handle_prerequisites(self, request: web.Request) -> web.Response:
        """Check prerequisites and return results."""
        checks: list[dict[str, Any]] = []

        # Python version
        py = sys.version_info
        checks.append(
            {
                "name": "Python",
                "status": "ok" if py >= (3, 12) else "fail",
                "detail": f"{py.major}.{py.minor}.{py.micro}",
                "required": "3.12+",
            }
        )

        # Platform
        checks.append(
            {
                "name": "Platform",
                "status": "ok" if sys.platform == "win32" else "warn",
                "detail": sys.platform,
                "required": "win32",
            }
        )

        # Node.js (check bundled location first, then system PATH)
        node_path = find_node()
        if node_path:
            try:
                result = subprocess.run(
                    [node_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                checks.append(
                    {
                        "name": "Node.js",
                        "status": "ok",
                        "detail": result.stdout.strip(),
                    }
                )
            except (subprocess.SubprocessError, OSError):
                checks.append(
                    {
                        "name": "Node.js",
                        "status": "warn",
                        "detail": "Found but version check failed",
                    }
                )
        else:
            checks.append(
                {
                    "name": "Node.js",
                    "status": "fail",
                    "detail": "Not found — install from https://nodejs.org",
                }
            )

        # npm
        npm_path = find_npm()
        checks.append(
            {
                "name": "npm",
                "status": "ok" if npm_path else "fail",
                "detail": "Available" if npm_path else "Not found",
            }
        )

        return web.json_response({"checks": checks})

    async def _handle_get_config(self, request: web.Request) -> web.Response:
        """Return current config as JSON."""
        cfg = GhostConfig.load()
        data = cfg.model_dump()
        data["version"] = __version__
        # Mask the API key for display
        if data.get("gemini_api_key"):
            data["gemini_api_key_masked"] = data["gemini_api_key"][:8] + "..."
        else:
            data["gemini_api_key_masked"] = ""
        return web.json_response(data)

    async def _handle_validate_key(self, request: web.Request) -> web.Response:
        """Validate a Gemini API key."""
        body = await request.json()
        api_key = body.get("api_key", "").strip()
        if not api_key:
            return web.json_response({"valid": False, "error": "No API key provided"})

        try:
            from google import genai

            client = genai.Client(api_key=api_key)
            next(iter(client.models.list()))
            return web.json_response({"valid": True})
        except Exception as exc:
            return web.json_response({"valid": False, "error": str(exc)})

    async def _handle_save(self, request: web.Request) -> web.Response:
        """Validate and save the full config."""
        body = await request.json()

        cfg = GhostConfig.load()

        # Apply fields from the wizard
        if "gemini_api_key" in body:
            cfg.gemini_api_key = body["gemini_api_key"]
        if "model_tier" in body:
            cfg.model_tier = body["model_tier"]
            from ghost_pc.config.settings import _resolve_model_tier

            model, cu_model = _resolve_model_tier(body["model_tier"])
            cfg.gemini_model = model
            cfg.gemini_computer_use_model = cu_model
        if "browser_method" in body:
            cfg.browser_method = body["browser_method"]
        if "features" in body:
            cfg.installed_extras = body["features"]
        if "allowed_numbers" in body:
            cfg.allowed_numbers = body["allowed_numbers"]
        if "stream_port" in body:
            cfg.stream_port = int(body["stream_port"])
        if "screen_fps" in body:
            cfg.screen_fps = int(body["screen_fps"])
        if "jpeg_quality" in body:
            cfg.jpeg_quality = int(body["jpeg_quality"])
        if "autostart_enabled" in body:
            cfg.autostart_enabled = body["autostart_enabled"]

        cfg.setup_completed = True
        cfg.save()

        # Silently set up the WhatsApp bridge (copy files + pre-bundled node_modules)
        self._setup_bridge_silent(cfg)

        return web.json_response({"ok": True, "path": str(GHOST_HOME / "config.json")})

    def _setup_bridge_silent(self, cfg: GhostConfig) -> None:
        """Copy bridge files (and pre-bundled node_modules) to the bridge dir.

        Called automatically on save so the user never needs a separate install step.
        """
        import shutil as sh

        try:
            from ghost_pc._bridge import get_bundled_bridge_path

            src_dir = get_bundled_bridge_path()
            if src_dir is None:
                return

            bridge_dir = cfg.get_bridge_dir()
            bridge_dir.mkdir(parents=True, exist_ok=True)

            for filename in ("index.js", "package.json"):
                src_file = src_dir / filename
                if src_file.exists():
                    sh.copy2(src_file, bridge_dir / filename)

            # Copy pre-bundled node_modules if available
            src_nm = src_dir / "node_modules"
            dst_nm = bridge_dir / "node_modules"
            if src_nm.is_dir() and not dst_nm.exists():
                sh.copytree(src_nm, dst_nm)

        except Exception:
            logger.debug("Bridge silent setup skipped", exc_info=True)

    def _ensure_bridge_deps(self, cfg: GhostConfig) -> None:
        """Re-run npm install if package.json changed (e.g. Baileys version upgrade).

        Compares a stored hash of the installed package.json against the current
        one.  If they differ, wipes node_modules and runs a blocking npm install
        so the bridge has correct dependencies before pairing.
        """
        bridge_dir = cfg.get_bridge_dir()
        pkg_json = bridge_dir / "package.json"
        marker = bridge_dir / ".pkg_hash"

        if not pkg_json.exists():
            return

        import hashlib

        current_hash = hashlib.sha256(pkg_json.read_bytes()).hexdigest()[:16]
        stored_hash = marker.read_text().strip() if marker.exists() else ""

        if current_hash == stored_hash:
            return  # Dependencies are up to date

        logger.info("package.json changed — reinstalling bridge dependencies")
        node_modules = bridge_dir / "node_modules"
        if node_modules.is_dir():
            shutil.rmtree(node_modules, ignore_errors=True)

        npm_path = find_npm()
        if not npm_path:
            logger.warning("npm not found — cannot reinstall bridge deps")
            return

        try:
            result = subprocess.run(
                [npm_path, "install", "--production"],
                cwd=str(bridge_dir),
                capture_output=True,
                text=True,
                timeout=120,
                env=get_node_env(),
            )
            if result.returncode == 0:
                marker.write_text(current_hash)
                logger.info("Bridge dependencies reinstalled successfully")
            else:
                logger.warning("npm install failed: %s", result.stderr.strip())
        except (subprocess.TimeoutExpired, OSError) as exc:
            logger.warning("npm install error: %s", exc)

    async def _handle_install_bridge(self, request: web.Request) -> web.Response:
        """Install the WhatsApp bridge — copies files and runs npm install.

        In installer builds the bridge is pre-bundled with node_modules,
        so npm install is skipped entirely.  Streams progress via WebSocket.
        """
        cfg = GhostConfig.load()
        bridge_dir = cfg.get_bridge_dir()
        bridge_dir.mkdir(parents=True, exist_ok=True)

        await self._ws_send(
            {"type": "progress", "step": "bridge", "message": "Setting up WhatsApp bridge..."}
        )

        # --- Locate bundled bridge source ---
        try:
            from ghost_pc._bridge import get_bundled_bridge_path

            src_dir = get_bundled_bridge_path()
            if src_dir is None:
                return web.json_response(
                    {"ok": False, "error": "Bridge files not found in this build."}
                )
        except ImportError:
            return web.json_response({"ok": False, "error": "Bridge bundle not available"})

        import shutil as sh

        # --- Copy bridge source files ---
        for filename in ("index.js", "package.json"):
            src_file = src_dir / filename
            dst_file = bridge_dir / filename
            if src_file.exists():
                sh.copy2(src_file, dst_file)
                await self._ws_send(
                    {"type": "progress", "step": "bridge", "message": f"Copied {filename}"}
                )

        # --- Copy pre-bundled node_modules if available (installer build) ---
        src_node_modules = src_dir / "node_modules"
        if src_node_modules.is_dir():
            dst_node_modules = bridge_dir / "node_modules"
            if not dst_node_modules.exists():
                await self._ws_send(
                    {
                        "type": "progress",
                        "step": "bridge",
                        "message": "Installing dependencies...",
                    }
                )
                sh.copytree(src_node_modules, dst_node_modules)
            await self._ws_send(
                {
                    "type": "progress",
                    "step": "bridge",
                    "message": "Bridge ready",
                    "done": True,
                }
            )
            return web.json_response({"ok": True})

        # --- Fallback: run npm install (pip/dev installs without pre-bundled deps) ---
        npm_path = find_npm()
        if not npm_path:
            return web.json_response(
                {"ok": False, "error": "npm not found — install Node.js from https://nodejs.org"}
            )

        await self._ws_send(
            {"type": "progress", "step": "bridge", "message": "Downloading dependencies..."}
        )

        try:
            result = subprocess.run(
                [npm_path, "install", "--production"],
                cwd=str(bridge_dir),
                capture_output=True,
                text=True,
                timeout=120,
                env=get_node_env(),
            )
            if result.returncode == 0:
                # Write hash marker so _ensure_bridge_deps skips next time
                import hashlib

                pkg_json = bridge_dir / "package.json"
                marker = bridge_dir / ".pkg_hash"
                if pkg_json.exists():
                    h = hashlib.sha256(pkg_json.read_bytes()).hexdigest()[:16]
                    marker.write_text(h)

                await self._ws_send(
                    {
                        "type": "progress",
                        "step": "bridge",
                        "message": "Bridge ready",
                        "done": True,
                    }
                )
                return web.json_response({"ok": True})
            else:
                return web.json_response({"ok": False, "error": result.stderr.strip()})
        except subprocess.TimeoutExpired:
            return web.json_response({"ok": False, "error": "Download timed out"})
        except OSError as exc:
            return web.json_response({"ok": False, "error": str(exc)})

    async def _handle_install_extras(self, request: web.Request) -> web.Response:
        """Install selected pip extras.

        In standalone (frozen) builds everything is pre-bundled, so this
        is a no-op that reports success.
        """
        if getattr(sys, "frozen", False):
            return web.json_response(
                {"ok": True, "message": "All features are included in this install."}
            )

        body = await request.json()
        extras: list[str] = body.get("extras", [])
        if not extras:
            return web.json_response({"ok": True, "message": "No extras to install"})

        extras_str = ",".join(extras)
        pip_spec = f"ghost-pc[{extras_str}]"

        await self._ws_send(
            {
                "type": "progress",
                "step": "extras",
                "message": f"Installing {pip_spec}...",
            }
        )

        # Use the Python that owns this process (not sys.executable in frozen builds)
        python = sys.executable
        if getattr(sys, "frozen", False):
            python = shutil.which("python") or shutil.which("python3") or "python"

        try:
            result = subprocess.run(
                [python, "-m", "pip", "install", pip_spec],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if result.returncode == 0:
                await self._ws_send(
                    {
                        "type": "progress",
                        "step": "extras",
                        "message": f"Installed {pip_spec}",
                        "done": True,
                    }
                )
                return web.json_response({"ok": True})
            else:
                err_lines = result.stderr.strip().splitlines()
                last_err = err_lines[-1] if err_lines else "Unknown error"
                return web.json_response({"ok": False, "error": last_err})
        except subprocess.TimeoutExpired:
            return web.json_response({"ok": False, "error": "pip install timed out"})
        except OSError as exc:
            return web.json_response({"ok": False, "error": str(exc)})

    async def _handle_pair_whatsapp(self, request: web.Request) -> web.Response:
        """Start the WhatsApp bridge for pairing — sends QR via WebSocket."""
        cfg = GhostConfig.load()
        bridge_dir = cfg.get_bridge_dir()

        # Always copy fresh bridge files so code changes take effect immediately.
        self._setup_bridge_silent(cfg)

        # If package.json changed (e.g. Baileys version upgrade), re-install deps.
        self._ensure_bridge_deps(cfg)

        index_js = bridge_dir / "index.js"
        if not index_js.exists():
            await self._ws_send({"type": "error", "message": f"Bridge not found at {bridge_dir}"})
            return web.json_response({"ok": False, "error": "Bridge not installed"})

        # Check node_modules exist
        node_modules = bridge_dir / "node_modules"
        if not node_modules.is_dir():
            await self._ws_send(
                {"type": "error", "message": "Bridge dependencies missing — click Install Bridge"}
            )
            return web.json_response(
                {"ok": False, "error": "node_modules missing — install bridge first"}
            )

        node_path = find_node()
        if not node_path:
            await self._ws_send({"type": "error", "message": "Node.js not found on this system"})
            return web.json_response({"ok": False, "error": "Node.js not found"})

        # Clear any leftover/corrupt credentials so the bridge generates a fresh QR.
        # Partial creds from a previously-killed session cause the bridge to enter
        # an infinite reconnection loop instead of showing a QR code.
        auth_dir = cfg.get_credentials_dir() / "whatsapp"
        if auth_dir.is_dir():
            logger.info("Clearing old WhatsApp credentials for fresh pairing")
            shutil.rmtree(auth_dir, ignore_errors=True)

        env = {
            **get_node_env(),
            "GHOST_CREDENTIALS_DIR": str(cfg.get_credentials_dir()),
            "LOG_LEVEL": "info",  # Verbose during pairing for diagnostics
        }

        logger.info("Starting bridge for pairing: %s %s", node_path, index_js)

        try:
            proc = subprocess.Popen(
                [node_path, str(index_js)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(bridge_dir),
                env=env,
            )

            await self._ws_send(
                {
                    "type": "progress",
                    "step": "pairing",
                    "message": "Waiting for QR code...",
                }
            )

            # Read stdout lines for QR data (bridge outputs JSON-RPC)
            # Also monitor stderr for crash diagnostics.
            loop = asyncio.get_running_loop()
            paired = False
            stderr_lines: list[str] = []

            def _read_stderr() -> None:
                """Capture stderr in background for error diagnostics."""
                if proc.stderr is None:
                    return
                for raw in proc.stderr:
                    line = raw.decode("utf-8", errors="replace").strip()
                    if line:
                        stderr_lines.append(line)
                        logger.debug("[bridge stderr] %s", line)

            def _read_bridge() -> None:
                nonlocal paired
                if proc.stdout is None:
                    return
                for line in proc.stdout:
                    line_str = line.decode("utf-8", errors="replace").strip()
                    if not line_str:
                        continue
                    try:
                        msg = json.loads(line_str)
                        # Parse JSON-RPC event notifications from the bridge
                        if msg.get("method") != "event":
                            continue
                        params = msg.get("params", {})
                        event_type = params.get("type")
                        event_data = params.get("data", {})

                        # Diagnostic lifecycle events from the bridge
                        if event_type == "bridge.status":
                            stage = event_data.get("stage", "")
                            logger.info("[bridge] %s", stage)
                            _stage_labels = {
                                "starting": "Bridge starting...",
                                "loading_auth": "Loading auth state...",
                                "auth_loaded": "Auth loaded",
                                "version_fetched": "WhatsApp version OK",
                                "version_fetch_failed": "Version fetch failed (using default)",
                                "creating_socket": "Connecting to WhatsApp...",
                                "socket_created": "Socket created, waiting for QR...",
                            }
                            label = _stage_labels.get(stage)
                            if label:
                                asyncio.run_coroutine_threadsafe(
                                    self._ws_send(
                                        {
                                            "type": "progress",
                                            "step": "pairing",
                                            "message": label,
                                        }
                                    ),
                                    loop,
                                )
                        elif event_type == "bridge.error":
                            err_msg = event_data.get("message", "Unknown error")
                            logger.error("[bridge] fatal: %s", err_msg)
                            asyncio.run_coroutine_threadsafe(
                                self._ws_send(
                                    {"type": "error", "message": f"Bridge error: {err_msg}"}
                                ),
                                loop,
                            )
                        elif event_type == "qr":
                            qr_string = event_data.get("qr", "")
                            asyncio.run_coroutine_threadsafe(
                                self._ws_send({"type": "qr", "data": qr_string}),
                                loop,
                            )
                        elif event_type == "connection.update":
                            if event_data.get("connection") == "open":
                                paired = True
                                asyncio.run_coroutine_threadsafe(
                                    self._ws_send(
                                        {
                                            "type": "paired",
                                            "message": "WhatsApp connected!",
                                        }
                                    ),
                                    loop,
                                )
                                return  # Done — stop reading
                    except json.JSONDecodeError:
                        pass

            import threading

            # Run both readers in daemon threads (they die when process is killed)
            stderr_thread = threading.Thread(target=_read_stderr, daemon=True)
            stdout_thread = threading.Thread(target=_read_bridge, daemon=True)
            stderr_thread.start()
            stdout_thread.start()

            # Wait up to 60 seconds for QR + pairing
            stdout_thread.join(timeout=60)

            if stdout_thread.is_alive():
                # Timed out — kill process to unblock reader threads
                logger.warning("Bridge pairing timed out after 60s")
                if proc.poll() is None:
                    proc.kill()
                    proc.wait(timeout=5)
                stderr_thread.join(timeout=2)
                stdout_thread.join(timeout=2)

                err_summary = "\n".join(stderr_lines[-10:]) if stderr_lines else "No output"
                logger.warning("Bridge stderr: %s", err_summary)
                await self._ws_send(
                    {"type": "error", "message": f"Pairing timed out. Bridge: {err_summary[:200]}"}
                )
            elif not paired and proc.poll() is not None:
                # Bridge crashed without pairing
                stderr_thread.join(timeout=2)
                err_summary = "\n".join(stderr_lines[-5:]) if stderr_lines else "No output"
                logger.warning("Bridge exited (code %d): %s", proc.returncode, err_summary)
                await self._ws_send(
                    {
                        "type": "error",
                        "message": f"Bridge crashed (exit {proc.returncode}): {err_summary[:200]}",
                    }
                )

            # Let Baileys finish saving credentials to disk before terminating
            if paired:
                await asyncio.sleep(3)

            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()

            if paired:
                return web.json_response({"ok": True})

            # Collect error context for the HTTP response
            err_summary = "\n".join(stderr_lines[-5:]) if stderr_lines else "No output from bridge"
            return web.json_response(
                {"ok": False, "error": f"Pairing failed. Bridge: {err_summary[:200]}"}
            )

        except Exception as exc:
            logger.error("Pairing failed: %s", exc, exc_info=True)
            await self._ws_send({"type": "error", "message": str(exc)})
            return web.json_response({"ok": False, "error": str(exc)})

    async def _handle_set_autostart(self, request: web.Request) -> web.Response:
        """Configure Windows scheduled task for autostart."""
        if sys.platform != "win32":
            return web.json_response({"ok": False, "error": "Only supported on Windows"})

        body = await request.json()
        enable = body.get("enable", False)

        if enable:
            ghost_cmd = (
                sys.executable
                if getattr(sys, "frozen", False)
                else (shutil.which("ghost") or "ghost")
            )
            try:
                subprocess.run(
                    [
                        "schtasks",
                        "/Create",
                        "/TN",
                        "GhostPC",
                        "/SC",
                        "ONLOGON",
                        "/RL",
                        "LIMITED",
                        "/TR",
                        f'"{ghost_cmd}" start',
                        "/F",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return web.json_response({"ok": True})
            except (subprocess.SubprocessError, OSError) as exc:
                return web.json_response({"ok": False, "error": str(exc)})
        else:
            try:
                subprocess.run(
                    ["schtasks", "/Delete", "/TN", "GhostPC", "/F"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            except (subprocess.SubprocessError, OSError):
                pass
            return web.json_response({"ok": True})

    async def _handle_ws(self, request: web.Request) -> web.WebSocketResponse:
        """WebSocket for real-time feedback (QR codes, install progress)."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._ws_clients.append(ws)

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data.get("action") == "done":
                        self._auto_start = bool(data.get("autoStart", False))
                        self._done.set()
                elif msg.type in (WSMsgType.ERROR, WSMsgType.CLOSE):
                    break
        finally:
            self._ws_clients.remove(ws)

        return ws

    # ── Helpers ─────────────────────────────────────────────────────

    async def _ws_send(self, data: dict[str, Any]) -> None:
        """Broadcast a message to all connected WebSocket clients."""
        dead: list[web.WebSocketResponse] = []
        for ws in self._ws_clients:
            try:
                await ws.send_json(data)
            except (ConnectionResetError, RuntimeError):
                dead.append(ws)
        for ws in dead:
            self._ws_clients.remove(ws)

    # ── Server lifecycle ────────────────────────────────────────────

    async def _start(self) -> None:
        """Create and start the aiohttp server."""
        self._app = web.Application()
        self._app.router.add_get("/setup", self._handle_setup_page)
        self._app.router.add_get("/static/{path:.*}", self._handle_static)
        self._app.router.add_get("/api/setup/prerequisites", self._handle_prerequisites)
        self._app.router.add_get("/api/setup/config", self._handle_get_config)
        self._app.router.add_post("/api/setup/validate-key", self._handle_validate_key)
        self._app.router.add_post("/api/setup/save", self._handle_save)
        self._app.router.add_post("/api/setup/install-bridge", self._handle_install_bridge)
        self._app.router.add_post("/api/setup/install-extras", self._handle_install_extras)
        self._app.router.add_post("/api/setup/pair-whatsapp", self._handle_pair_whatsapp)
        self._app.router.add_post("/api/setup/set-autostart", self._handle_set_autostart)
        self._app.router.add_get("/ws/setup", self._handle_ws)

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, "127.0.0.1", _SETUP_PORT)
        await site.start()

        logger.info("Setup wizard running on http://127.0.0.1:%d/setup", _SETUP_PORT)

    async def _stop(self) -> None:
        """Shut down the server."""
        if self._runner:
            await self._runner.cleanup()

    async def run(self) -> bool:
        """Start server, open browser, wait until wizard signals done, then stop.

        Returns ``True`` if the user chose "Save & Start" (auto-start requested).
        """
        await self._start()

        # Open browser
        url = f"http://127.0.0.1:{_SETUP_PORT}/setup"
        webbrowser.open(url)

        # Wait for the wizard to finish (signalled via WebSocket "done" action)
        # Also allow Ctrl+C to stop
        try:
            await self._done.wait()
        except asyncio.CancelledError:
            pass
        finally:
            await self._stop()

        return self._auto_start


def run_setup_gui() -> bool:
    """Entry point for ``ghost setup`` — starts the web wizard.

    Returns ``True`` if the user chose "Save & Start GhostPC".
    """
    from rich.console import Console

    console = Console()
    console.print(
        f"[bold cyan]GhostPC Setup Wizard[/] v{__version__}\n"
        f"Opening browser at http://127.0.0.1:{_SETUP_PORT}/setup ...\n"
        "[dim]Press Ctrl+C to cancel.[/]\n"
    )

    server = SetupServer()
    try:
        auto_start: bool = asyncio.run(server.run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled.[/]")
        return False

    return auto_start
