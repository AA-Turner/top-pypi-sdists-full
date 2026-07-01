import asyncio
import time

from loguru import logger

from dreadnode.app.api.models import HumanInputResponse, HumanPrompt
from dreadnode.tools.interaction import UserCancelled


class SessionPromptRegistry:
    """Owns pending prompt and permission state for one runtime session."""

    def __init__(self) -> None:
        self._pending_permissions: dict[str, asyncio.Event] = {}
        self._permission_decisions: dict[str, str] = {}
        self._session_allowlist: set[str] = set()
        self._pending_human_prompts: dict[str, HumanPrompt] = {}
        self._pending_human_inputs: dict[str, asyncio.Future[HumanInputResponse]] = {}
        self._pending_human_prompt_started_at: dict[str, float] = {}
        self._resolved_human_inputs: dict[str, HumanInputResponse] = {}

    @property
    def pending_permissions(self) -> dict[str, asyncio.Event]:
        """Pending permission requests keyed by request id."""
        return self._pending_permissions

    @property
    def permission_decisions(self) -> dict[str, str]:
        """Resolved permission decisions keyed by request id."""
        return self._permission_decisions

    @property
    def session_allowlist(self) -> set[str]:
        """Session-scoped permission allowlist."""
        return self._session_allowlist

    @property
    def pending_prompt(self) -> HumanPrompt | None:
        """First pending human prompt, if one exists."""
        return next(iter(self._pending_human_prompts.values()), None)

    def turn_phase(self, active_turn_id: str | None) -> str:
        """Project prompt state into the transport snapshot turn phase."""
        if self.pending_prompt is not None:
            return "awaiting_input"
        if self._pending_permissions:
            return "awaiting_permission"
        if active_turn_id is not None:
            return "running"
        return "idle"

    def resolve_permission(self, request_id: str, decision: str) -> None:
        """Resolve a pending permission request with a user decision."""
        self._permission_decisions[request_id] = decision
        if decision == "allow_session":
            self._session_allowlist.add(request_id)
        event = self._pending_permissions.get(request_id)
        if event is not None:
            logger.debug(
                "Permission prompt resolved request_id={} decision={}",
                request_id,
                decision,
            )
            event.set()

    def register_human_prompt(self, prompt: HumanPrompt) -> asyncio.Future[HumanInputResponse]:
        """Register a pending human prompt and return its response future."""
        existing = self._pending_human_inputs.get(prompt.request_id)
        if existing is not None:
            return existing
        loop = asyncio.get_running_loop()
        future: asyncio.Future[HumanInputResponse] = loop.create_future()
        self._pending_human_prompts[prompt.request_id] = prompt
        self._pending_human_inputs[prompt.request_id] = future
        self._pending_human_prompt_started_at[prompt.request_id] = time.perf_counter()
        return future

    def resolve_human_input_response(self, response: HumanInputResponse) -> bool:
        """Resolve a pending human prompt response. Returns True if applied.

        On ``action="submit"`` the future receives the response. On
        ``action="cancel"`` the future is failed with ``UserCancelled`` —
        the awaiting tool sees an exception, not a sentinel response.
        Reserve ``future.cancel()`` (raising ``CancelledError``) for
        turn-abort via ``cancel_all_pending``.
        """
        request_id = response.request_id
        if request_id in self._resolved_human_inputs:
            return True
        future = self._pending_human_inputs.pop(request_id, None)
        self._pending_human_prompts.pop(request_id, None)
        started_at = self._pending_human_prompt_started_at.pop(request_id, None)
        if future is None:
            return False
        if not future.done():
            if response.action == "cancel":
                future.set_exception(UserCancelled("user cancelled prompt"))
            else:
                future.set_result(response)
        self._resolved_human_inputs[request_id] = response
        if started_at is not None:
            elapsed_ms = round((time.perf_counter() - started_at) * 1000)
            logger.debug(
                "Human prompt resolved request_id={} action={} elapsed_ms={}",
                request_id,
                response.action,
                elapsed_ms,
            )
        return True

    def resolve_human_response(self, response: HumanInputResponse) -> bool:
        """Resolve a human response against the human-prompt registry.

        Permission decisions go through their own ``PermissionResponse``
        path (see ``send_permission_response``); this method handles the
        ``ask_user`` flow only.
        """
        return self.resolve_human_input_response(response)

    def cancel_all_pending(self) -> int:
        """Cancel every pending human prompt and permission request.

        Called from the turn processor's cancel branch so a turn
        that was mid-``ask_user()`` when the user interrupted does
        not leave ``pending_prompt`` populated — ``build_snapshot``
        reads that field and would otherwise report an idle session
        as ``awaiting_input`` after reconnect/resync.

        Human-input futures are cancelled rather than resolved with
        a synthetic response: the enclosing turn task is already being
        cancelled by asyncio, so resolving would race with the outer
        ``CancelledError`` unwind. Cancelling the future makes the
        ``return await future`` inside ``_human_prompt_handler`` raise
        ``CancelledError`` which then propagates out of the tool call
        stack cleanly.

        Permission waits are unblocked with an implicit ``deny``
        decision so their waiter ``Event`` fires and any tool waiting
        on it unwinds rather than sitting on a dead event forever.

        Returns the number of pending entries that were cleared, for
        debug logging.
        """
        cleared = 0
        for request_id in list(self._pending_human_inputs):
            future = self._pending_human_inputs.pop(request_id)
            self._pending_human_prompts.pop(request_id, None)
            self._pending_human_prompt_started_at.pop(request_id, None)
            if not future.done():
                future.cancel()
            cleared += 1
        for request_id in list(self._pending_permissions):
            event = self._pending_permissions.pop(request_id)
            self._permission_decisions.setdefault(request_id, "deny")
            event.set()
            cleared += 1
        return cleared
