"""End-to-end turn orchestration for the TUI.

The TUI equivalent of the server's
:class:`dreadnode.app.server.turn_coordinator.SessionTurnCoordinator`.
It owns the execution of a single chat/shell/permission/human-input
turn from start to finish: stream events off the runtime client, feed
them through :class:`SessionsManager.handle_event`, handle auth and
generic errors, and run the post-turn cleanup (commit draft, drain
queue, transition to idle).

It does NOT own:

* The per-turn state machine — that's
  :class:`dreadnode.app.tui.turn_lifecycle.TurnLifecycle`, accessed
  through the port as ``turn_lifecycle``. The coordinator drives
  ``start_turn`` / ``finish_turn`` / ``interrupt`` on the lifecycle;
  the lifecycle owns the IDLE/GENERATING/RUNNING_TOOLS/etc phase
  transitions for each turn.
* Event dispatch — that's :class:`SessionsManager.handle_event`. The
  coordinator just calls it for each event it pulls off the stream.
* Session-record lifecycle (create/reset/switch/resume) — those are
  session-state operations on :class:`SessionsManager` + a thin
  ``ensure_active_session`` port method that the coordinator calls
  when a chat arrives before a session exists.

The Textual ``@work`` wrappers stay on :class:`DreadnodeTextualApp`
because Textual's worker tracking (used by ``workers.cancel_group``)
requires them to live on the ``App`` instance. The app's wrappers are
thin: they ``await coordinator.X(...)`` and nothing else. When the
coordinator wants to schedule a follow-up turn (e.g., draining a
queued message after the current turn ends), it calls back into the
app through the ``schedule_send_chat``/``schedule_execute_shell`` port
methods so the new work stays tracked.
"""

import re
import typing as t

from loguru import logger

from dreadnode.app.api.client import AuthenticationError
from dreadnode.app.api.models import HumanInputResponse, HumanPrompt, QuestionAnswer
from dreadnode.generators.message import Message

if t.TYPE_CHECKING:
    from dreadnode.app.client.models import SessionInfo
    from dreadnode.app.tui.sessions_manager import SessionRecord
    from dreadnode.app.tui.turn_lifecycle import TurnLifecycle
    from dreadnode.app.tui.turn_reducer import TurnState
    from dreadnode.app.tui.widgets import HumanPromptWidget, ToolProgress
    from dreadnode.app.tui.widgets.composer import ComposerInput


# =============================================================================
# Port
# =============================================================================


class TurnCoordinatorActions(t.Protocol):
    """Single fat port the coordinator uses to drive the app.

    Intentionally one protocol rather than several — the coordinator
    touches session state, server transport, model manager, auth
    handler, UI widgets, turn lifecycle, and worker scheduling, and
    splitting those into six ports would explode the app-side adapter
    surface without adding type safety (one concrete adapter would
    still implement them all). Keep it as one port; the adapter on
    ``DreadnodeTextualApp`` is the concrete impl.
    """

    # ------------------------------------------------------------------
    # Server transport
    # ------------------------------------------------------------------

    def stream_chat(
        self,
        *,
        session_id: str,
        message: str,
        model: str,
        agent: str | None,
        generate_params_extra: dict[str, t.Any] | None,
    ) -> t.AsyncIterator[dict[str, t.Any]]: ...

    async def execute_shell(self, command: str) -> dict[str, t.Any]: ...

    async def cancel_session(self, session_id: str) -> None: ...

    async def send_permission_response(
        self, session_id: str, request_id: str, decision: str
    ) -> None: ...

    async def send_human_input_response(
        self, session_id: str, response: HumanInputResponse
    ) -> None: ...

    # ------------------------------------------------------------------
    # App state
    # ------------------------------------------------------------------

    def active_session(self) -> "SessionRecord | None": ...

    def active_session_id(self) -> str | None: ...

    def current_model(self) -> str: ...

    def generate_params_extra(self) -> dict[str, t.Any]: ...

    def is_authenticated(self) -> bool: ...

    # ------------------------------------------------------------------
    # Session manager side effects
    # ------------------------------------------------------------------

    def handle_event(self, event: dict[str, t.Any], session_id: str) -> None: ...

    def commit_draft_to_transcript(self, session_id: str) -> None: ...

    def session_turn_state(self, session_id: str) -> "TurnState | None": ...

    def abort_running_tools(self, session_id: str) -> None:
        """Finalize in-flight tools for a session on interrupt.

        Marks all running tool runs as errored and drops any cached
        ``ToolCall`` widget refs for them so the widget cache does
        not accumulate dead entries across successive interrupts.
        """
        ...

    def apply_human_prompt_response(self, session_id: str, action: str) -> None: ...

    def active_human_prompt(self) -> HumanPrompt | None: ...

    def display_agent_for(self, session_info: "SessionInfo") -> str: ...

    def sync_queue(self) -> None: ...

    def sync_sessions(self) -> None: ...

    def schedule_runtime_session_subscription_sync(self) -> None: ...

    # ------------------------------------------------------------------
    # Model manager
    # ------------------------------------------------------------------

    async def ensure_litellm_key_fresh(self) -> None: ...

    # ------------------------------------------------------------------
    # Auth handler
    # ------------------------------------------------------------------

    def handle_authentication_error(self, message: str) -> None: ...

    # ------------------------------------------------------------------
    # Turn lifecycle (fat access — the state machine has many methods)
    # ------------------------------------------------------------------

    def turn_lifecycle(self) -> "TurnLifecycle": ...

    # ------------------------------------------------------------------
    # UI widgets
    # ------------------------------------------------------------------

    def query_tool_progress(self) -> "ToolProgress": ...

    def query_composer(self) -> "ComposerInput": ...

    def query_permission_prompt(self) -> "HumanPromptWidget": ...

    def append_transcript(
        self, message: Message, session_id: str, *, scroll: bool = True
    ) -> None: ...

    def write_activity(self, message: str, *, style: str = "info") -> None: ...

    def notify_agent_output_available(self, session_id: str) -> None:
        """If the just-finished turn reported structured items, drop a
        clickable end-of-turn pointer to the web Agent Output page.

        No-op when the turn reported nothing, when the session isn't the
        visible one, or when there's no platform link to offer (local /
        unauthenticated). The per-row links scroll away in a long session;
        this keeps one pointer at the foot of the turn.
        """
        ...

    def flash(self, message: str, *, severity: str = "info") -> None: ...

    # ------------------------------------------------------------------
    # Session creation — needed when a chat arrives before any session
    # ------------------------------------------------------------------

    async def ensure_active_session(self) -> "SessionRecord | None":
        """Create a new session if none is active and return it."""
        ...

    # ------------------------------------------------------------------
    # Worker scheduling — re-enter the app's ``@work`` wrappers so
    # follow-up turns (queue drain after current turn ends) stay
    # tracked by Textual's worker group for cancellation.
    # ------------------------------------------------------------------

    def schedule_send_chat(self, message: str, *, agent: str | None = None) -> None: ...

    def schedule_send_human_input_response(
        self,
        request_id: str,
        action: t.Literal["submit", "cancel"],
        *,
        answers: list[QuestionAnswer] | None = None,
    ) -> None:
        """Schedule a human-input response via the app's ``@work`` wrapper.

        Used by :meth:`cancel_active_prompt` so the cancel write stays
        tracked by Textual's worker group for cancellation.
        """
        ...

    def cancel_session_workers(self) -> None: ...

    def cancel_server_turn(self) -> None:
        """Fire-and-forget: ask the server to cancel the active turn.

        Implemented on the app side so the coordinator doesn't have to
        reach for ``asyncio.get_running_loop`` directly. The adapter
        handles task creation and failure logging.
        """
        ...

    # ------------------------------------------------------------------
    # Session count, for message_count updates after a turn ends
    # ------------------------------------------------------------------

    def session_transcript_length(self, session_id: str) -> int: ...

    def set_session_message_count(self, session_id: str, count: int) -> None: ...


# =============================================================================
# TurnCoordinator
# =============================================================================


class TurnCoordinator:
    """Drives one turn to completion: chat, shell, or permission/input response.

    All methods are plain ``async``/sync. The Textual ``@work`` wrapper
    stays on the app so Textual can track and cancel the worker. The
    app's wrapper is a one-liner: ``await coordinator.send_chat(...)``.
    """

    def __init__(self, *, actions: TurnCoordinatorActions) -> None:
        self._actions = actions

    # ------------------------------------------------------------------
    # Chat turn
    # ------------------------------------------------------------------

    async def send_chat(
        self,
        message: str,
        *,
        user_entry_shown: bool = False,
    ) -> None:
        """Stream a chat turn using the session's bound agent.

        When ``user_entry_shown`` is ``True`` the caller has already
        appended the user message to the transcript and started the
        turn lifecycle — this matches the fast-path in
        ``_on_composer_submitted`` that pre-renders the user row before
        the worker schedules.
        """
        lifecycle = self._actions.turn_lifecycle()
        my_generation = lifecycle.generation

        session = self._actions.active_session()
        if session is None:
            session = await self._actions.ensure_active_session()
            if session is None:
                self._actions.flash("Failed to create a session", severity="error")
                return

        tp = self._actions.query_tool_progress()
        if not user_entry_shown:
            sid = session.info.session_id
            my_generation = lifecycle.start_turn("Thinking", owner=sid)
            tp.show_activity("thinking")
            session.turn_count += 1
            self._actions.append_transcript(
                Message(
                    role="user",
                    content=message,
                    metadata={"turn": session.turn_count},
                ),
                sid,
            )

        logger.info(
            "Chat send | session={} model={} agent={} length={}",
            session.info.session_id[:8],
            self._actions.current_model(),
            self._actions.display_agent_for(session.info),
            len(message),
        )

        try:
            await self._actions.ensure_litellm_key_fresh()
            async for event in self._actions.stream_chat(
                session_id=session.info.session_id,
                message=message,
                model=self._actions.current_model(),
                agent=None if session.info.agent == "default" else session.info.agent,
                generate_params_extra=self._actions.generate_params_extra() or None,
            ):
                self._actions.handle_event(event, session.info.session_id)
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Chat stream failed")
            self._actions.append_transcript(
                Message(
                    role="system",
                    content=str(exc),
                    metadata={"error": True, "error_title": "error"},
                ),
                session.info.session_id,
            )
            self._actions.write_activity(str(exc), style="error")
        finally:
            self.finish_turn_cleanup(session.info.session_id, my_generation)

    async def send_chat_to_agent(self, message: str, agent_name: str) -> None:
        """Stream a chat turn with an explicit ``@agent`` override."""
        session = self._actions.active_session()
        if session is None:
            session = await self._actions.ensure_active_session()
        if session is None:
            return

        lifecycle = self._actions.turn_lifecycle()
        my_generation = lifecycle.start_turn("Thinking", owner=session.info.session_id)
        tp = self._actions.query_tool_progress()
        tp.show_activity("thinking")

        logger.info(
            "Chat send @agent | session={} model={} agent={} length={}",
            session.info.session_id[:8],
            self._actions.current_model(),
            agent_name,
            len(message),
        )

        try:
            await self._actions.ensure_litellm_key_fresh()
            sid = session.info.session_id
            session.turn_count += 1
            self._actions.append_transcript(
                Message(
                    role="user",
                    content=message,
                    metadata={"turn": session.turn_count},
                ),
                sid,
            )
            async for event in self._actions.stream_chat(
                session_id=session.info.session_id,
                message=message,
                model=self._actions.current_model(),
                agent=agent_name,
                generate_params_extra=self._actions.generate_params_extra() or None,
            ):
                self._actions.handle_event(event, session.info.session_id)
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Agent chat failed")
            self._actions.append_transcript(
                Message(
                    role="system",
                    content=str(exc),
                    metadata={"error": True, "error_title": "error"},
                ),
                session.info.session_id,
            )
            self._actions.write_activity(str(exc), style="error")
        finally:
            self.finish_turn_cleanup(session.info.session_id, my_generation)

    # ------------------------------------------------------------------
    # Shell turn
    # ------------------------------------------------------------------

    async def execute_shell(self, command: str) -> None:
        """Run a one-shot shell command and record the output inline."""
        session = self._actions.active_session()
        sid = session.info.session_id if session else "shell"
        self._actions.append_transcript(
            Message(role="user", content=f"$ {command}", metadata={"shell": True}),
            sid,
        )

        lifecycle = self._actions.turn_lifecycle()
        my_generation = lifecycle.start_turn("Running", owner=sid)
        tp = self._actions.query_tool_progress()
        tp.show_activity("running")

        try:
            result = await self._actions.execute_shell(command)
            stdout = result.get("stdout", "").strip()
            stderr = result.get("stderr", "").strip()
            exit_code = result.get("exitCode", 0)
            output = stdout
            if stderr:
                output = f"{output}\n{stderr}" if output else stderr
            if exit_code != 0:
                output = f"{output}\n[exit {exit_code}]"
            if exit_code == 0:
                self._actions.append_transcript(
                    Message(
                        role="tool",
                        content=output or "(no output)",
                        metadata={
                            "tool_name": "shell",
                            "tool_args": {},
                            "summary": f"exit {exit_code}",
                        },
                    ),
                    sid,
                )
            else:
                self._actions.append_transcript(
                    Message(
                        role="system",
                        content=output or "(no output)",
                        metadata={
                            "error": True,
                            "error_title": "shell",
                            "summary": f"exit {exit_code}",
                        },
                    ),
                    sid,
                )
        except Exception as exc:
            logger.exception("Shell execution failed")
            self._actions.append_transcript(
                Message(
                    role="system",
                    content=str(exc),
                    metadata={"error": True, "error_title": "shell"},
                ),
                sid,
            )
        finally:
            tp.hide_tool()
            if lifecycle.finish_turn(my_generation):
                lifecycle.go_idle(authenticated=self._actions.is_authenticated())

    # ------------------------------------------------------------------
    # Permission / human-input mid-turn responses
    # ------------------------------------------------------------------

    async def send_permission_response(
        self,
        request_id: str,
        decision: str,
        *,
        tool_name: str = "",
    ) -> None:
        """Send a permission decision back to the server mid-turn."""
        logger.info("Permission response | decision={} tool={}", decision, tool_name or "n/a")
        session = self._actions.active_session()
        if session is None:
            return

        if decision == "allow_session" and tool_name:
            session.allowlisted_tools.add(tool_name)

        lifecycle = self._actions.turn_lifecycle()
        try:
            await self._actions.send_permission_response(
                session.info.session_id,
                request_id,
                decision,
            )
            lifecycle.resume_from_awaiting("Resuming")
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Permission response failed")
            self._actions.write_activity(f"Permission response error: {exc}", style="error")
            lifecycle.go_idle_with_error("Ready", authenticated=self._actions.is_authenticated())

    async def send_human_input_response(
        self,
        request_id: str,
        action: t.Literal["submit", "cancel"],
        *,
        answers: list[QuestionAnswer] | None = None,
    ) -> None:
        """Send a human input response back to the server mid-turn."""
        logger.info("Human input response | action={}", action)
        session = self._actions.active_session()
        if session is None:
            return

        response = HumanInputResponse(
            request_id=request_id,
            action=action,
            answers=answers,
        )

        lifecycle = self._actions.turn_lifecycle()
        try:
            await self._actions.send_human_input_response(session.info.session_id, response)
            if action == "submit":
                lifecycle.resume_from_awaiting("Resuming")
            else:
                lifecycle.go_idle(authenticated=self._actions.is_authenticated())
            self._actions.apply_human_prompt_response(session.info.session_id, action)
        except AuthenticationError:
            self._actions.handle_authentication_error("Session expired — please sign in again")
        except Exception as exc:
            logger.exception("Human input response failed")
            self._actions.write_activity(f"Human response error: {exc}", style="error")
            lifecycle.go_idle_with_error("Ready", authenticated=self._actions.is_authenticated())

    # ------------------------------------------------------------------
    # Interrupt / cancel
    # ------------------------------------------------------------------

    def interrupt(self) -> bool:
        """Cancel the active turn, draining any queued follow-up.

        Single owner of the interrupt sequence. Returns ``True`` if a
        turn (or an active human prompt) was in progress and cancelled,
        ``False`` if nothing was active.
        """
        lifecycle = self._actions.turn_lifecycle()
        if not lifecycle.is_busy:
            return False

        # If a human prompt is active, cancel just that — the turn continues.
        if self.cancel_active_prompt():
            return True

        lifecycle.interrupt()
        self._actions.cancel_session_workers()
        self._actions.cancel_server_turn()
        self._actions.commit_draft_to_transcript(self._actions.active_session_id() or "")

        # Finalize in-flight tools so their state goes to ``errored``
        # AND their cached widget refs are dropped — otherwise
        # ``SessionsManager._tool_call_widgets`` accumulates dead
        # entries across every interrupt until the session is switched.
        sid = self._actions.active_session_id()
        if sid:
            self._actions.abort_running_tools(sid)

        # Drain the message queue — interrupt bumps the generation so
        # the worker's finally block will bail before reaching the
        # queue drain. We own the lifecycle now, so schedule the next
        # queued message here.
        next_msg: str | None = None
        if sid:
            session = self._actions.active_session()
            queue = session.queued_messages if session is not None else []
            if queue:
                next_msg = queue.pop(0)
                self._actions.sync_queue()

        # Only hide the spinner when nothing is taking over. A queued
        # follow-up will re-show it synchronously via ``send_chat`` —
        # hiding it here would either flicker (off → on) or, if the
        # new worker's first ``await`` interleaves with the cancelled
        # worker's ``finally``, leave the spinner stuck off while the
        # turn is actually running.
        if next_msg is None:
            self._actions.query_tool_progress().hide_tool()
        else:
            self._dispatch_next_message(next_msg)

        return True

    def cancel_active_prompt(self) -> bool:
        """Cancel the active human prompt if one is present.

        Routes the cancel write through the app's worker scheduler so
        it's tracked by Textual's cancellation machinery — same path
        an interactive cancel via the prompt widget would take.
        """
        prompt = self._actions.active_human_prompt()
        if prompt is None:
            return False
        self._actions.query_permission_prompt().hide_prompt()
        composer = self._actions.query_composer()
        composer.placeholder = ""
        composer.disabled = False
        self._actions.schedule_send_human_input_response(
            prompt.request_id,
            "cancel",
        )
        return True

    # ------------------------------------------------------------------
    # Post-turn cleanup
    # ------------------------------------------------------------------

    def finish_turn_cleanup(self, session_id: str, generation: int) -> None:
        """Shared cleanup for ``send_chat``/``send_chat_to_agent`` finally blocks.

        Commits the draft, hides the progress spinner, updates the
        message count, then either auto-sends the next queued message
        via :meth:`TurnCoordinatorActions.schedule_send_chat` or
        transitions to idle.

        Public so tests and app-side code can invoke it directly —
        ``send_chat``/``send_chat_to_agent`` call it from their
        ``finally`` blocks; the message-queue tests call it to verify
        the queue-drain routing.

        Stale generations bail before any UI side-effect. An interrupt
        or a fresh queue-drain turn already owns the spinner / draft /
        composer state; replaying the cleanup would race the live turn
        — most visibly hiding the spinner the new ``send_chat`` just
        turned on for a queued follow-up.
        """
        lifecycle = self._actions.turn_lifecycle()
        if not lifecycle.finish_turn(generation):
            return

        self._actions.commit_draft_to_transcript(session_id)
        self._actions.query_tool_progress().hide_tool()
        # After the turn's content is committed, nudge the user toward the web
        # Agent Output page if this turn reported any structured items.
        self._actions.notify_agent_output_available(session_id)

        # Best-effort count + metadata update for the session.
        count = self._actions.session_transcript_length(session_id)
        if count:
            self._actions.set_session_message_count(session_id, count)
            self._actions.sync_sessions()
            self._actions.schedule_runtime_session_subscription_sync()

        # We own the transition — drain queue or go idle.
        session = self._actions.active_session()
        queue = session.queued_messages if session is not None else []
        if queue and session is not None and self._actions.active_session_id() == session_id:
            next_msg = queue.pop(0)
            self._actions.sync_queue()
            self._dispatch_next_message(next_msg)
        else:
            lifecycle.go_idle(authenticated=self._actions.is_authenticated())

    def _dispatch_next_message(self, message: str) -> None:
        """Schedule the next queued message through the app's @work wrapper."""
        at_match = re.match(r"^@(\S+)\s+([\s\S]+)$", message)
        if at_match:
            self._actions.schedule_send_chat(
                at_match.group(2),
                agent=at_match.group(1),
            )
        else:
            self._actions.schedule_send_chat(message)
