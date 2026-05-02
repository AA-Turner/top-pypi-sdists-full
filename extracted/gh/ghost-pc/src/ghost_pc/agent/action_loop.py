"""ADK-powered agent runner with persistent sessions, memory, and plugins.

Uses ADK's full Runner (not InMemoryRunner) for production-grade features:
- DatabaseSessionService: sessions survive restarts (SQLite)
- InMemoryMemoryService: agent remembers past conversations
- Plugins: safety, cost tracking, observability applied globally
- Session rotation: after 30+ events, summarize and start fresh
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncGenerator, Awaitable, Callable
from pathlib import Path
from typing import Any

from google.adk.memory.base_memory_service import BaseMemoryService
from google.adk.plugins import BasePlugin
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# Persistent memory fallback chain:
#   1. ChromaDB (pip install ghost-pc[memory]) — vector search, best quality
#   2. SQLite FTS5 (always available) — full-text search, zero extra deps
#   3. InMemory (last resort) — lost on restart
try:
    from ghost_pc.agent.chromadb_memory import ChromaDBMemoryService as _MemoryServiceCls
except ImportError:
    from ghost_pc.agent.sqlite_memory import (
        SQLiteMemoryService as _MemoryServiceCls,  # type: ignore[assignment]
    )

logger = logging.getLogger(__name__)

# Sessions expire after this many seconds of inactivity
SESSION_TTL_SECONDS = 30 * 60  # 30 minutes
SESSION_CLEANUP_INTERVAL = 5 * 60  # check every 5 minutes

# Rotate session after this many events to keep context fresh
SESSION_ROTATION_THRESHOLD = 30


# Default SQLite DB path for persistent sessions (inside GHOST_HOME so it
# works even when the CWD is System32 on frozen-exe startup).
def _default_session_db_path() -> Path:
    from ghost_pc.config.schema import GHOST_HOME

    return GHOST_HOME / "ghost_pc_sessions.db"


def _build_db_url(db_path: str | None = None) -> str:
    """Build an async SQLite URL for DatabaseSessionService."""
    path = Path(db_path).resolve() if db_path else _default_session_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite+aiosqlite:///{path}"


class AgentRunner:
    """Manages ADK agent sessions and execution for GhostPC.

    One runner instance serves all users. Each user gets their own
    persistent session with conversation history that survives restarts.
    """

    def __init__(
        self,
        agent: Any,
        plugins: list[BasePlugin] | None = None,
        db_path: str | None = None,
    ) -> None:
        db_url = _build_db_url(db_path)
        self._session_service = DatabaseSessionService(db_url=db_url)
        self._memory_service = _MemoryServiceCls()

        self.runner = Runner(
            agent=agent,
            app_name="ghost_pc",
            session_service=self._session_service,
            memory_service=self._memory_service,
            plugins=plugins or [],
        )

        self._sessions: dict[str, str] = {}  # user_id -> session_id
        self._last_activity: dict[str, float] = {}  # user_id -> timestamp
        self._event_counts: dict[str, int] = {}  # session_id -> event count
        self._screenshot_queue: asyncio.Queue[str] = asyncio.Queue()
        self._cleanup_task: asyncio.Task[None] | None = None

    @property
    def session_service(self) -> DatabaseSessionService:
        return self._session_service

    @property
    def memory_service(self) -> BaseMemoryService:
        return self._memory_service

    def start_cleanup_loop(self) -> None:
        """Start the background session cleanup task."""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._session_cleanup_loop())

    async def _session_cleanup_loop(self) -> None:
        """Periodically remove expired sessions."""
        try:
            while True:
                await asyncio.sleep(SESSION_CLEANUP_INTERVAL)
                now = time.monotonic()
                expired = [
                    uid for uid, ts in self._last_activity.items() if now - ts > SESSION_TTL_SECONDS
                ]
                for uid in expired:
                    logger.info("Expiring idle session for user %s", uid)
                    await self.reset_session(uid)
        except asyncio.CancelledError:
            pass

    async def execute(
        self,
        user_id: str,
        message: str,
        on_text: Callable[[str], Awaitable[None]] | None = None,
        on_screenshot_request: Callable[[str], Awaitable[None]] | None = None,
    ) -> str:
        """Execute a user message through the ADK agent.

        Args:
            user_id: Unique user identifier (phone number or viewer session).
            message: The user's text message.
            on_text: Callback for streaming intermediate text responses.
            on_screenshot_request: Callback when agent wants to send a screenshot.
                                   Receives the caption string.

        Returns:
            The agent's final text response.
        """
        self._last_activity[user_id] = time.monotonic()

        # Get or create session for this user
        session_id = await self._ensure_session(user_id)

        # Build user message
        user_content = types.Content(
            role="user",
            parts=[types.Part(text=message)],
        )

        # Run the agent and collect events
        final_text = ""
        event_count = 0
        try:
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_content,
            ):
                event_count += 1
                if not event.content or not event.content.parts:
                    continue

                for part in event.content.parts:
                    if part.text:
                        final_text = part.text

                # Check for screenshot requests queued by the tool
                if on_screenshot_request:
                    await self._drain_screenshot_queue(on_screenshot_request)

        except Exception as e:
            logger.error("Agent execution error: %s", e, exc_info=True)
            return f"Error: {e}"

        # Final drain in case last tool call was send_screenshot_to_user
        if on_screenshot_request:
            await self._drain_screenshot_queue(on_screenshot_request)

        # Track event count for session rotation
        self._event_counts[session_id] = self._event_counts.get(session_id, 0) + event_count
        if self._event_counts[session_id] >= SESSION_ROTATION_THRESHOLD:
            await self._rotate_session(user_id, session_id)

        return final_text or "Done."

    async def _drain_screenshot_queue(
        self,
        callback: Callable[[str], Awaitable[None]],
    ) -> None:
        """Process all pending screenshot requests."""
        while not self._screenshot_queue.empty():
            try:
                caption = self._screenshot_queue.get_nowait()
                await callback(caption)
            except asyncio.QueueEmpty:
                break

    def after_tool_callback(
        self,
        tool: Any,
        args: dict[str, Any],
        tool_context: ToolContext,
        tool_response: Any,
    ) -> Any:
        """ADK after_tool_callback — picks up screenshot requests from state.

        Also injects ``current_url`` into dict tool responses so Gemini CU
        doesn't reject them with 400 INVALID_ARGUMENT.  ComputerUseToolset
        methods already return ``ComputerState(url=...)`` which includes the
        field, but custom FunctionTools (click_label, open_application, etc.)
        return plain dicts that lack it.
        """
        if tool_context.state.get("screenshot_requested"):
            caption = tool_context.state.get("screenshot_caption", "Here's your screen")
            self._screenshot_queue.put_nowait(caption)
            tool_context.state["screenshot_requested"] = False
            tool_context.state["screenshot_caption"] = ""

        # Inject current_url for Gemini CU compatibility
        if isinstance(tool_response, dict) and "current_url" not in tool_response:
            tool_response["current_url"] = ""

        return tool_response

    async def stream_events(
        self, user_id: str, message: str
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream agent events for real-time UI updates (used by viewer chat).

        Yields dicts with event info:
            {"type": "text", "content": "..."}
            {"type": "tool_call", "name": "click_at", "args": {...}}
            {"type": "done", "content": "final response"}
        """
        self._last_activity[user_id] = time.monotonic()
        session_id = await self._ensure_session(user_id)

        user_content = types.Content(
            role="user",
            parts=[types.Part(text=message)],
        )

        final_text = ""
        try:
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_content,
            ):
                if not event.content or not event.content.parts:
                    continue

                for part in event.content.parts:
                    if part.text:
                        final_text = part.text
                        yield {"type": "text", "content": part.text, "author": event.author}
                    if part.function_call:
                        yield {
                            "type": "tool_call",
                            "name": part.function_call.name,
                            "args": dict(part.function_call.args)
                            if part.function_call.args
                            else {},
                        }

        except Exception as e:
            logger.error("Agent stream error: %s", e, exc_info=True)
            yield {"type": "error", "content": str(e)}

        yield {"type": "done", "content": final_text or "Done."}

    async def reset_session(self, user_id: str) -> None:
        """Clear a user's conversation history."""
        if user_id in self._sessions:
            session_id = self._sessions[user_id]
            try:
                await self._session_service.delete_session(
                    app_name="ghost_pc",
                    user_id=user_id,
                    session_id=session_id,
                )
            except Exception:
                pass
            self._event_counts.pop(session_id, None)
            del self._sessions[user_id]
        self._last_activity.pop(user_id, None)

    async def close(self) -> None:
        """Clean up the runner."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        await self.runner.close()

    async def _ensure_session(self, user_id: str) -> str:
        """Get or create a session for the given user."""
        if user_id not in self._sessions:
            session = await self._session_service.create_session(
                app_name="ghost_pc",
                user_id=user_id,
            )
            self._sessions[user_id] = session.id
        return self._sessions[user_id]

    async def _rotate_session(self, user_id: str, old_session_id: str) -> None:
        """Rotate session: save to memory, create fresh session with summary.

        After 30+ events the context gets bloated. We use Gemini to generate
        a proper summary, save it to memory, and start a new session with
        the summary injected via ``user:session_summary`` state.
        """
        try:
            # Save current session to memory service for future recall
            session = await self._session_service.get_session(
                app_name="ghost_pc",
                user_id=user_id,
                session_id=old_session_id,
            )
            if session:
                await self._memory_service.add_session_to_memory(session)

                # Build conversation text from recent exchanges
                conversation_parts: list[str] = []
                for event in session.events or []:
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                role = event.content.role or "agent"
                                conversation_parts.append(f"{role}: {part.text[:300]}")

                conversation_text = "\n".join(conversation_parts[-20:])

                # Use Gemini to generate a proper summary
                summary = await self._generate_session_summary(conversation_text)

                # Delete old session
                await self._session_service.delete_session(
                    app_name="ghost_pc",
                    user_id=user_id,
                    session_id=old_session_id,
                )

                # Create new session with summary in state
                new_session = await self._session_service.create_session(
                    app_name="ghost_pc",
                    user_id=user_id,
                    state={"user:session_summary": summary},
                )
                self._sessions[user_id] = new_session.id
                self._event_counts.pop(old_session_id, None)
                logger.info(
                    "Rotated session for user %s (old=%s, new=%s)",
                    user_id,
                    old_session_id,
                    new_session.id,
                )
        except Exception as e:
            logger.warning("Session rotation failed for %s: %s", user_id, e)

    async def _generate_session_summary(self, conversation_text: str) -> str:
        """Use Gemini to generate a concise session summary.

        Falls back to naive truncation if the API call fails.
        """
        try:
            from google import genai

            client = genai.Client()
            response = await client.aio.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(
                                text=(
                                    "Summarize this desktop agent conversation"
                                    " in 3-5 bullet points. "
                                    "Focus on: what the user asked for, "
                                    "what actions were taken, "
                                    "what was the outcome, and any preferences"
                                    " or context for next time.\n\n"
                                    f"{conversation_text}"
                                )
                            )
                        ],
                    )
                ],
            )
            if response.text:
                return response.text.strip()
        except Exception as e:
            logger.debug("LLM summary generation failed, using fallback: %s", e)

        # Fallback: extract last few exchanges
        lines = conversation_text.split("\n")
        return "\n".join(lines[-6:])
