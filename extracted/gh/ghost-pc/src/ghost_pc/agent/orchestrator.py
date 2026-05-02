"""Main orchestrator — wires everything together.

Starts:
1. WhatsApp bridge (Node.js subprocess)
2. System tray icon
3. Live screen streaming server (with chat)
4. Emergency hotkey listener
5. ADK agent runner (handles AI actions) with:
   - DatabaseSessionService (persistent sessions)
   - InMemoryMemoryService (cross-session recall)
   - Plugins (safety, cost tracking, observability)
   - Multi-agent topology (router → chat/simple/complex)
6. Voice controller (optional, Phase 5)
"""

from __future__ import annotations

import asyncio
import logging
import os
import tempfile
import time
from typing import TYPE_CHECKING

from rich.console import Console

from ghost_pc.agent.action_loop import AgentRunner
from ghost_pc.agent.confirmation import (
    ConfirmationManager,
    PendingConfirmation,
    parse_confirmation_reply,
)
from ghost_pc.agent.gemini import create_ghost_agent
from ghost_pc.agent.plugins import (
    ConfirmationPlugin,
    CostBudgetPlugin,
    CostTrackingPlugin,
    ObservabilityPlugin,
    SafetyPlugin,
)
from ghost_pc.config.settings import Settings
from ghost_pc.desktop.capture import get_screen_dimensions

if TYPE_CHECKING:
    from ghost_pc.streaming.mjpeg_server import MJPEGServer
    from ghost_pc.tray.tray import GhostTray
    from ghost_pc.voice.controller import VoiceController
    from ghost_pc.web.log_handler import DashboardLogHandler
    from ghost_pc.whatsapp.bridge import BaileysBridge

logger = logging.getLogger(__name__)
console = Console()


def _build_plugins(
    confirmation_manager: ConfirmationManager | None = None,
) -> list:
    """Build the plugin list for the runner.

    Plugin order: Safety → Confirmation → Cost → Observability → ReflectAndRetry
    """
    plugins: list = [
        SafetyPlugin(max_repeated_actions=3),
    ]

    # Confirmation sits right after safety (sensitive, not catastrophic)
    if confirmation_manager is not None:
        plugins.append(ConfirmationPlugin(confirmation_manager))

    plugins.extend(
        [
            CostBudgetPlugin(max_tokens_per_invocation=500_000),
            CostTrackingPlugin(),
            ObservabilityPlugin(),
        ]
    )

    # Try to load the built-in ReflectAndRetryToolPlugin
    try:
        from google.adk.plugins import ReflectAndRetryToolPlugin

        plugins.append(ReflectAndRetryToolPlugin(max_retries=3))
    except ImportError:
        logger.debug("ReflectAndRetryToolPlugin not available in this ADK version")

    return plugins


class Orchestrator:
    """Top-level controller that manages all subsystems."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.screen_width, self.screen_height = get_screen_dimensions()
        self._shutdown_event = asyncio.Event()
        self._bridge: BaileysBridge | None = None
        self._stream_server: MJPEGServer | None = None
        self._agent_runner: AgentRunner | None = None
        self._tray: GhostTray | None = None
        self._voice_controller: VoiceController | None = None
        self._confirmation_manager = ConfirmationManager()
        self._notification_engine: object | None = None
        self._paused = False
        self._start_time = time.monotonic()
        self._plugins: list = []
        self._tunnel_url: str | None = None
        self.dashboard_log_handler: DashboardLogHandler | None = None
        # Per-user locks to prevent concurrent agent execution for the same user
        self._user_locks: dict[str, asyncio.Lock] = {}

    def _get_user_lock(self, user_id: str) -> asyncio.Lock:
        """Get or create a per-user processing lock."""
        if user_id not in self._user_locks:
            self._user_locks[user_id] = asyncio.Lock()
        return self._user_locks[user_id]

    def pause(self) -> None:
        """Pause the agent — incoming messages get a "paused" reply."""
        self._paused = True
        logger.info("Agent paused")

    def resume(self) -> None:
        """Resume the agent."""
        self._paused = False
        logger.info("Agent resumed")

    @property
    def is_paused(self) -> bool:
        return self._paused

    def get_status(self) -> dict:
        """Return current agent status for the dashboard."""
        # Base status
        status: dict = {
            "paused": self._paused,
            "whatsapp_connected": bool(self._bridge and getattr(self._bridge, "_connected", False)),
            "processing": bool(self._tray and self._tray._processing),
            "uptime_seconds": time.monotonic() - self._start_time,
        }

        # Feature statuses
        status["notifications"] = {
            "enabled": self.settings.notifications_enabled,
            "active": self._notification_engine is not None,
        }

        status["voice"] = {
            "enabled": self._voice_controller is not None,
            "active": bool(
                self._voice_controller and getattr(self._voice_controller, "_running", False)
            ),
        }

        status["memory"] = {
            "backend": self._get_memory_backend(),
        }

        status["confirmations"] = {
            "enabled": self.settings.confirmation_enabled,
            "pending_count": self._confirmation_manager.pending_count,
        }

        return status

    def _get_memory_backend(self) -> str:
        """Return the name of the active memory backend."""
        if not self._agent_runner:
            return "none"
        try:
            name = type(self._agent_runner._memory_service).__name__
            return {
                "ChromaDBMemoryService": "chromadb",
                "SQLiteMemoryService": "sqlite",
                "InMemoryMemoryService": "in-memory",
            }.get(name, name)
        except AttributeError:
            return "unknown"

    def get_cost_summary(self) -> dict:
        """Return aggregated cost data from the CostTrackingPlugin."""
        for plugin in self._plugins:
            if isinstance(plugin, CostTrackingPlugin):
                return plugin.get_cost_summary()
        return {"total_tokens": 0, "total_llm_calls": 0, "total_tool_calls": 0}

    async def run(self) -> None:
        """Start all subsystems and run until shutdown."""
        # Install dashboard log handler on root logger
        from ghost_pc.web.log_handler import DashboardLogHandler

        self.dashboard_log_handler = DashboardLogHandler(max_records=500)
        self.dashboard_log_handler.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger().addHandler(self.dashboard_log_handler)

        console.print(f"[dim]Screen: {self.screen_width}x{self.screen_height}[/]")

        # Build plugins (confirmation manager enables sensitive action gating)
        plugins = _build_plugins(
            confirmation_manager=self._confirmation_manager
            if self.settings.confirmation_enabled
            else None,
        )
        self._plugins = plugins
        console.print(f"[dim]Plugins: {', '.join(type(p).__name__ for p in plugins)}[/]")

        # Create the ADK agent and runner
        # We use __new__ + __init__ pattern so the agent can reference
        # the runner's after_tool_callback during construction
        self._agent_runner = AgentRunner.__new__(AgentRunner)
        agent = create_ghost_agent(
            self.screen_width,
            self.screen_height,
            runner=self._agent_runner,
            settings=self.settings,
        )
        self._agent_runner.__init__(agent, plugins=plugins)
        self._agent_runner.start_cleanup_loop()
        console.print("[dim]ADK agent initialized (multi-agent topology)[/]")

        # Start proactive notifications
        if self.settings.notifications_enabled:
            self._start_notifications()

        # Start system tray
        self._start_tray()

        # Start subsystems concurrently
        tasks = [
            asyncio.create_task(self._run_whatsapp_bridge()),
            asyncio.create_task(self._run_stream_server()),
            asyncio.create_task(self._run_hotkey_listener()),
        ]

        # Optionally start voice controller
        voice_task = asyncio.create_task(self._run_voice_controller())
        tasks.append(voice_task)

        console.print("[green]GhostPC is running.[/] Waiting for WhatsApp messages...")

        # Wait for shutdown signal
        await self._shutdown_event.wait()

        # Cleanup
        if self._agent_runner:
            await self._agent_runner.close()

        if self._tray:
            self._tray.stop()

        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

        console.print("[yellow]GhostPC stopped.[/]")

    async def shutdown(self) -> None:
        """Signal graceful shutdown."""
        self._shutdown_event.set()
        if self._bridge:
            await self._bridge.stop()
        # Clean up temp files created during operation
        self._cleanup_temp_files()

    def _cleanup_temp_files(self) -> None:
        """Remove temporary files created by the orchestrator."""
        import glob

        patterns = [
            os.path.join(tempfile.gettempdir(), "ghost_screenshot.jpg"),
            os.path.join(tempfile.gettempdir(), "ghost_reply.mp3"),
            os.path.join(tempfile.gettempdir(), "ghost_reply.ogg"),
        ]
        for pattern in patterns:
            for path in glob.glob(pattern):
                try:
                    os.unlink(path)
                except OSError:
                    pass

    async def handle_message(self, from_id: str, body: str, media_path: str | None = None) -> None:
        """Handle an incoming message (from WhatsApp or viewer chat).

        Args:
            from_id: User identifier (phone number or viewer session ID).
            body: The message text.
            media_path: Optional path to attached media (voice note, image).
        """
        console.print(f"[cyan]Message from {from_id}:[/] {body}")

        # Reject messages while paused
        if self._paused:
            await self._send_text(
                from_id, "GhostPC is paused. Please wait or ask the admin to resume."
            )
            return

        # Check allowlist (only for WhatsApp numbers, not viewer sessions)
        if (
            self.settings.allowed_numbers
            and from_id.startswith("+")
            and from_id not in self.settings.allowed_numbers
        ):
            logger.warning("Blocked message from non-allowed number: %s", from_id)
            return

        body_lower = body.lower().strip()

        # Special commands
        if body_lower in ("screenshot", "screen", "show me my screen", "ss"):
            await self._send_screenshot(from_id, "Here's your screen right now")
            return

        if body_lower in ("watch", "live", "stream", "watch my screen"):
            await self._send_stream_link(from_id)
            return

        if body_lower in ("stop", "cancel", "halt"):
            # Reset session clears conversation context
            if self._agent_runner:
                await self._agent_runner.reset_session(from_id)
            await self._send_text(from_id, "Cancelled and reset.")
            return

        if body_lower in ("reset", "clear", "new"):
            if self._agent_runner:
                await self._agent_runner.reset_session(from_id)
            await self._send_text(from_id, "Session cleared. Fresh start!")
            return

        if body_lower in ("help", "?"):
            await self._send_text(
                from_id,
                (
                    "*GhostPC Commands:*\n"
                    "- Just type what you want done\n"
                    "- *screenshot* — see your screen\n"
                    "- *watch* — live screen stream\n"
                    "- *stop* — cancel and reset\n"
                    "- *reset* — clear conversation\n"
                    "- *help* — show this message"
                ),
            )
            return

        # Handle voice notes — transcribe and process
        if media_path and media_path.endswith((".ogg", ".mp3", ".wav", ".m4a")):
            transcribed = await self._transcribe_voice_note(media_path)
            if not transcribed:
                await self._send_text(from_id, "Sorry, I couldn't understand that voice note.")
                return
            body = transcribed
            console.print(f"[dim]Transcribed:[/] {body}")

        if not self._agent_runner:
            await self._send_text(from_id, "Agent not ready yet. Please wait...")
            return

        # ── Confirmation reply interception ──
        if self._confirmation_manager.has_pending(from_id):
            reply = parse_confirmation_reply(body)
            if reply is True:
                pending = self._confirmation_manager.pop(from_id)
                if pending:
                    result = await self._execute_confirmed_action(pending)
                    await self._send_text(from_id, result)
                    return
            elif reply is False:
                self._confirmation_manager.pop(from_id)
                await self._send_text(from_id, "Action cancelled.")
                return
            else:
                # Ambiguous reply — re-prompt
                pending = self._confirmation_manager.get(from_id)
                if pending:
                    await self._send_text(
                        from_id,
                        f"Reply *YES* or *NO*.\nAction: {pending.description}",
                    )
                    return

        # Per-user lock prevents concurrent actions from the same user
        # Other users can still send messages concurrently
        lock = self._get_user_lock(from_id)
        async with lock:
            # Send typing indicator
            if self._bridge and from_id.startswith("+"):
                await self._bridge.send_composing(from_id)

            # Set tray to processing
            if self._tray:
                self._tray.set_processing(True)

            # Execute through ADK agent
            try:
                result = await self._agent_runner.execute(
                    user_id=from_id,
                    message=body,
                    on_screenshot_request=lambda caption: self._send_screenshot(from_id, caption),
                )
                await self._send_text(from_id, result)

                # Check for reminder requests from agent tools
                await self._check_reminder_request(from_id)

                # If the original message was a voice note, also reply with voice
                if media_path and media_path.endswith((".ogg", ".mp3", ".wav", ".m4a")):
                    await self._send_voice_reply(from_id, result)

            except Exception as e:
                logger.error("Agent execution error: %s", e, exc_info=True)
                await self._send_text(from_id, f"Error: {e}")
            finally:
                if self._tray:
                    self._tray.set_processing(False)

    # --- Private methods ---

    async def _check_reminder_request(self, user_id: str) -> None:
        """Check if the agent set a reminder via the set_reminder tool."""
        if not self._agent_runner or not self._notification_engine:
            return

        try:
            session_id = self._agent_runner._sessions.get(user_id)
            if not session_id:
                return

            session = await self._agent_runner.session_service.get_session(
                app_name="ghost_pc",
                user_id=user_id,
                session_id=session_id,
            )
            if not session:
                return

            reminder_data = session.state.get("temp:set_reminder")
            if reminder_data and isinstance(reminder_data, dict):
                engine = self._notification_engine
                if hasattr(engine, "add_reminder"):
                    engine.add_reminder(  # type: ignore[union-attr]
                        description=reminder_data["description"],
                        delay_minutes=reminder_data["delay_minutes"],
                    )
                # Clear the temp state
                session.state.pop("temp:set_reminder", None)
        except Exception as e:
            logger.debug("Reminder check failed: %s", e)

    async def _execute_confirmed_action(
        self,
        pending: PendingConfirmation,
    ) -> str:
        """Execute a previously confirmed tool call."""
        from ghost_pc.agent import tools

        tool_fn = getattr(tools, pending.tool_name, None)
        if not tool_fn:
            return f"Tool '{pending.tool_name}' not found."

        try:
            # Filter out tool_context from args — it's auto-injected by ADK
            call_args = {k: v for k, v in pending.tool_args.items() if k != "tool_context"}
            result = await tool_fn(**call_args)
            if isinstance(result, dict):
                output = result.get("output", result.get("summary", result.get("status", "done")))
                return f"Done. {output}"
            return f"Done. {result}"
        except Exception as e:
            logger.error("Confirmed action failed: %s", e, exc_info=True)
            return f"Error executing action: {e}"

    async def _transcribe_voice_note(self, media_path: str) -> str | None:
        """Transcribe a voice note to text."""
        try:
            from ghost_pc.agent.transcribe import transcribe_audio

            return await transcribe_audio(media_path)
        except Exception as e:
            logger.error("Transcription failed: %s", e)
            return None

    async def _send_voice_reply(self, to: str, text: str) -> None:
        """Convert text to speech and send as a WhatsApp voice note."""
        if not self._bridge or not to.startswith("+"):
            return

        try:
            from ghost_pc.agent.voice_agent import speech_to_ogg, text_to_speech

            mp3_path = os.path.join(tempfile.gettempdir(), "ghost_reply.mp3")
            ogg_path = os.path.join(tempfile.gettempdir(), "ghost_reply.ogg")

            if await text_to_speech(text, mp3_path):
                if await speech_to_ogg(mp3_path, ogg_path):
                    await self._bridge.send_voice(to, ogg_path)
                    return

            # Fallback: just send text if voice generation fails
            logger.debug("Voice reply failed, text already sent")
        except Exception as e:
            logger.debug("Voice reply error: %s", e)

    def _start_notifications(self) -> None:
        """Start the proactive notification engine."""
        try:
            from ghost_pc.notifications.engine import NotificationEngine

            primary_user = (
                self.settings.allowed_numbers[0] if self.settings.allowed_numbers else None
            )
            if primary_user:
                self._notification_engine = NotificationEngine(
                    send_fn=self._send_text,
                    user_id=primary_user,
                    watch_dirs=self.settings.notification_watch_dirs,
                    daily_limit=self.settings.notification_rate_limit,
                )
                asyncio.create_task(self._notification_engine.start())
                console.print("[dim]Proactive notifications enabled[/]")
            else:
                logger.debug("No allowed_numbers set — notifications disabled")
        except ImportError:
            logger.debug("Notification dependencies not installed")
        except Exception as e:
            logger.debug("Failed to start notifications: %s", e)

    def _start_tray(self) -> None:
        """Start the system tray icon."""
        try:
            from ghost_pc.tray.tray import GhostTray

            loop = asyncio.get_running_loop()

            def on_quit() -> None:
                loop.call_soon_threadsafe(lambda: asyncio.ensure_future(self.shutdown()))

            def on_pause() -> None:
                if self._paused:
                    self.resume()
                else:
                    self.pause()

            dashboard_url = f"http://localhost:{self.settings.stream_port}/dashboard"

            self._tray = GhostTray(
                on_pause=on_pause,
                on_quit=on_quit,
                dashboard_url=dashboard_url,
            )
            self._tray.start()
            console.print("[dim]System tray icon started[/]")
        except Exception as e:
            logger.debug("Tray not available: %s", e)

    async def _run_whatsapp_bridge(self) -> None:
        """Start the Node.js Baileys bridge subprocess."""
        from ghost_pc.whatsapp.bridge import BaileysBridge

        self._bridge = BaileysBridge(
            bridge_dir=self.settings.bridge_dir,
            credentials_dir=self.settings.credentials_dir,
            on_message=self.handle_message,
            on_qr=self._on_qr_code,
            on_connection_change=self._on_connection_change,
        )

        try:
            await self._bridge.run()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("WhatsApp bridge error: %s", e)
            console.print(f"[red]WhatsApp bridge failed:[/] {e}")

    async def _run_stream_server(self) -> None:
        """Start the MJPEG live screen streaming server with chat."""
        from ghost_pc.streaming.mjpeg_server import MJPEGServer

        server = MJPEGServer(
            port=self.settings.stream_port,
            fps=self.settings.screen_fps,
            jpeg_quality=self.settings.jpeg_quality,
            on_chat_message=self._handle_viewer_chat,
            orchestrator=self,
        )
        self._stream_server = server

        # Start a tunnel so the viewer is accessible from any network
        asyncio.create_task(self._start_tunnel())

        try:
            await server.run()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("Stream server error: %s", e)

    async def _start_tunnel(self) -> None:
        """Start a Cloudflare tunnel for the stream server (best-effort)."""
        try:
            from ghost_pc.streaming.tunnel import start_tunnel

            url = await start_tunnel(self.settings.stream_port)
            if url:
                self._tunnel_url = url
                token = self._stream_server.session_token if self._stream_server else ""
                console.print(f"[cyan]Remote access:[/] {url}/view?token={token}")
            else:
                from ghost_pc.streaming.tunnel import get_local_ip

                ip = get_local_ip()
                token = self._stream_server.session_token if self._stream_server else ""
                console.print(
                    f"[dim]No tunnel available — LAN access only: "
                    f"http://{ip}:{self.settings.stream_port}/view?token={token}[/]"
                )
        except Exception:
            logger.debug("Tunnel startup failed", exc_info=True)

    async def _handle_viewer_chat(self, session_id: str, message: str) -> str:
        """Handle a chat message from the web viewer.

        Returns the agent's response text.
        """
        viewer_id = f"viewer_{session_id}"
        console.print(f"[magenta]Viewer chat ({session_id[:8]}):[/] {message}")

        if not self._agent_runner:
            return "Agent not ready yet."

        try:
            result = await self._agent_runner.execute(
                user_id=viewer_id,
                message=message,
            )
            return result
        except Exception as e:
            logger.error("Viewer chat error: %s", e)
            return f"Error: {e}"

    async def _run_hotkey_listener(self) -> None:
        """Listen for emergency stop hotkey."""
        try:
            from pynput import keyboard

            hotkey_parts = self.settings.emergency_hotkey.split("+")
            loop = asyncio.get_running_loop()

            def on_activate() -> None:
                console.print("[red bold]EMERGENCY STOP — hotkey pressed[/]")
                # Use call_soon_threadsafe since pynput callbacks run in a separate thread
                loop.call_soon_threadsafe(lambda: asyncio.ensure_future(self._emergency_stop()))

            keys = set()
            for part in hotkey_parts:
                part = part.strip().lower()
                if part == "ctrl":
                    keys.add(keyboard.Key.ctrl_l)
                elif part == "alt":
                    keys.add(keyboard.Key.alt_l)
                elif part == "shift":
                    keys.add(keyboard.Key.shift_l)
                elif len(part) == 1:
                    keys.add(keyboard.KeyCode.from_char(part))

            hotkey = keyboard.GlobalHotKeys(
                {"+".join(f"<{k}>" if hasattr(k, "name") else k.char for k in keys): on_activate}
            )

            await loop.run_in_executor(None, hotkey.run)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.debug("Hotkey listener not available: %s", e)

    async def _run_voice_controller(self) -> None:
        """Start the voice controller for wake-word activated interaction."""
        try:
            from ghost_pc.voice.controller import VoiceController

            controller = VoiceController(
                on_wake=lambda: logger.info("Wake word detected!"),
                on_visual_delegate=self._handle_visual_delegation,
            )
            self._voice_controller = controller
            console.print("[dim]Voice controller started (wake word: 'hey jarvis')[/]")
            await controller.start()
        except ImportError:
            logger.debug("Voice dependencies not installed — voice control disabled")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.debug("Voice controller not available: %s", e)

    async def _handle_visual_delegation(self, description: str) -> str:
        """Handle a visual task delegated from the voice agent.

        Routes the description through the main text agent which has
        ComputerUseToolset and can see/click the screen.
        """
        if not self._agent_runner:
            return "Agent not ready for visual tasks."

        primary_user = (
            self.settings.allowed_numbers[0] if self.settings.allowed_numbers else "voice_user"
        )
        try:
            result = await self._agent_runner.execute(
                user_id=primary_user,
                message=f"[Visual task from voice agent] {description}",
            )
            return result
        except Exception as e:
            logger.error("Visual delegation failed: %s", e)
            return f"Visual task failed: {e}"

    async def _emergency_stop(self) -> None:
        """Handle emergency stop — close agent and reset all sessions."""
        if self._agent_runner:
            await self._agent_runner.close()
        if self._tray:
            self._tray.set_connected(False)

    def _on_qr_code(self, qr_data: str) -> None:
        """Handle QR code from Baileys — display for user to scan."""
        try:
            import qrcode

            qr = qrcode.QRCode(box_size=1, border=1)
            qr.add_data(qr_data)
            qr.make(fit=True)
            console.print("\n[bold]Scan this QR code with WhatsApp:[/]")
            qr.print_ascii(out=console.file)
            console.print()
        except ImportError:
            console.print(f"[yellow]QR code data:[/] {qr_data[:50]}...")
            console.print("[dim]Install qrcode for visual QR: uv add qrcode[/]")

    def _on_connection_change(self, connected: bool) -> None:
        """Handle WhatsApp connection state change."""
        if self._tray:
            self._tray.set_connected(connected)
        if connected:
            console.print("[green]WhatsApp connected![/]")
            asyncio.create_task(self._send_welcome())
        else:
            console.print("[yellow]WhatsApp disconnected[/]")

    async def _send_welcome(self) -> None:
        """Send a welcome message to the primary user when WhatsApp connects."""
        if not self._bridge or not self.settings.allowed_numbers:
            return

        # Wait briefly for the Cloudflare tunnel to establish (starts concurrently)
        if not self._tunnel_url:
            for _ in range(15):
                if self._tunnel_url:
                    break
                await asyncio.sleep(1)

        primary = self.settings.allowed_numbers[0]
        lines = [
            "Hey! GhostPC is online and ready.",
            "Send me a message to control your PC.",
            "",
            "Try: *take a screenshot*, *open Chrome*, or *what's on my screen?*",
        ]

        # Include viewer link if stream server is running
        if self._stream_server:
            token = self._stream_server.session_token
            if self._tunnel_url:
                url = f"{self._tunnel_url}/view?token={token}"
            else:
                from ghost_pc.streaming.tunnel import get_local_ip

                ip = get_local_ip()
                url = f"http://{ip}:{self.settings.stream_port}/view?token={token}"
            lines.append(f"\nLive screen: {url}")

        try:
            await self._bridge.send_text(primary, "\n".join(lines))
        except Exception:
            logger.debug("Failed to send welcome message", exc_info=True)

    async def _send_text(self, to: str, text: str) -> None:
        """Send a text message — routes to WhatsApp or viewer as appropriate."""
        if to.startswith("+") and self._bridge:
            await self._bridge.send_text(to, text)
        elif to.startswith("viewer_") and self._stream_server:
            # Viewer responses are returned directly from handle_viewer_chat
            pass

    async def _send_screenshot(self, to: str, caption: str) -> None:
        """Capture screen and send as image."""
        from ghost_pc.desktop.capture import grab_and_encode

        jpg = grab_and_encode(quality=self.settings.jpeg_quality)
        if not jpg:
            return

        if to.startswith("+") and self._bridge:
            path = os.path.join(tempfile.gettempdir(), "ghost_screenshot.jpg")
            with open(path, "wb") as f:
                f.write(jpg)
            await self._bridge.send_image(to, path, caption)

    async def _send_stream_link(self, to: str) -> None:
        """Send the live stream URL to the user.

        Prefers a public tunnel URL (Cloudflare) so the phone can reach
        it from any network.  Falls back to the LAN IP URL.
        """
        # Wait briefly for tunnel if not yet established
        if not self._tunnel_url:
            for _ in range(5):
                if self._tunnel_url:
                    break
                await asyncio.sleep(1)

        if self._tunnel_url and self._stream_server:
            url = f"{self._tunnel_url}/view?token={self._stream_server.session_token}"
        elif self._stream_server:
            url = self._stream_server.get_viewer_url()
        else:
            url = f"http://localhost:{self.settings.stream_port}/view"
        await self._send_text(to, f"Watch your screen live:\n{url}")
