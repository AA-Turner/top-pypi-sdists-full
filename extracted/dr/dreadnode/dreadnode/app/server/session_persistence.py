import asyncio
import typing as t
from dataclasses import dataclass

from loguru import logger

if t.TYPE_CHECKING:
    from dreadnode.agents.trajectory import Trajectory


@dataclass(slots=True)
class _PersistSnapshot:
    """Immutable snapshot of session state needed for one persistence attempt."""

    api: t.Any
    org: str
    workspace: str
    update_messages: bool
    platform_registered: bool
    model: str
    title: str | None
    agent_name: str | None
    persisted_message_count: int
    all_messages_count: int = 0
    new_messages: list[t.Any] | None = None
    new_message_uuids: list[str] | None = None
    usage_by_uuid: dict[str, dict[str, t.Any]] | None = None
    needs_context: bool = False
    context: dict[str, t.Any] | None = None
    current_agent: str | None = None
    current_model: str | None = None
    current_system_prompt: str | None = None


@dataclass(slots=True)
class _PersistResult:
    """Result of one persistence attempt."""

    succeeded: bool = True
    last_seq: int | None = None


class SessionPersistenceCoordinator:
    """Owns transcript persistence state and flush coordination for one session."""

    def __init__(
        self,
        *,
        session_id: str,
        resolve_api_context: t.Callable[[], tuple[t.Any, str, str] | None],
        register_session: t.Callable[[], None],
        get_platform_registered: t.Callable[[], bool],
        get_model: t.Callable[[], str],
        get_title: t.Callable[[], str | None],
        get_agent_name: t.Callable[[], str | None],
        get_trajectory: t.Callable[[], "Trajectory | None"],
        resolve_agent_system_prompt: t.Callable[[str | None], str | None],
    ) -> None:
        self._session_id = session_id
        self._resolve_api_context = resolve_api_context
        self._register_session = register_session
        self._get_platform_registered = get_platform_registered
        self._get_model = get_model
        self._get_title = get_title
        self._get_agent_name = get_agent_name
        self._get_trajectory = get_trajectory
        self._resolve_agent_system_prompt = resolve_agent_system_prompt
        self._last_persisted_seq: int = -1
        self._persisted_message_count: int = 0
        # Track persisted messages by stable uuid, not positional index:
        # ``Trajectory.messages`` reorders buffered tool results relative to
        # assistant messages, so positional slicing can skip a freshly-added
        # assistant (tool-call) message that got reordered behind the boundary
        # (orphan tool results, lost calls — pronounced under foreign engines
        # that emit tool bursts). uuid tracking is order-independent.
        self._persisted_message_uuids: set[str] = set()
        self._current_segment_agent: str | None = None
        self._current_segment_model: str | None = None
        self._current_segment_system_prompt: str | None = None
        self._persist_lock = asyncio.Lock()
        self._pending_persist_tasks: set[asyncio.Task[None]] = set()
        self._flush_failure_reported = False
        self._persist_inflight = False
        self._persist_retry_requested = False

    @property
    def last_persisted_seq(self) -> int:
        return self._last_persisted_seq

    @last_persisted_seq.setter
    def last_persisted_seq(self, value: int) -> None:
        self._last_persisted_seq = value

    @property
    def persisted_message_count(self) -> int:
        return self._persisted_message_count

    @persisted_message_count.setter
    def persisted_message_count(self, value: int) -> None:
        self._persisted_message_count = value
        # Restore/hydration marks already-present messages as persisted via this
        # setter (without re-sending them). Seed the uuid set too, or the
        # uuid-based new-message filter would treat the hydrated messages as new
        # and re-persist them on the next flush.
        trajectory = self._get_trajectory()
        if trajectory is not None:
            for message in list(trajectory.messages)[:value]:
                uuid = getattr(message, "uuid", None)
                if uuid is not None:
                    self._persisted_message_uuids.add(str(uuid))

    @property
    def persist_lock(self) -> asyncio.Lock:
        return self._persist_lock

    @property
    def pending_persist_tasks(self) -> set[asyncio.Task[None]]:
        return self._pending_persist_tasks

    def restore_segment_context(
        self,
        *,
        agent: str | None,
        model: str | None,
        system_prompt: str | None,
    ) -> None:
        """Restore the last persisted transcript segment context from platform state."""
        self._current_segment_agent = agent
        self._current_segment_model = model
        self._current_segment_system_prompt = system_prompt

    def begin_turn(self) -> None:
        """Reset per-turn persistence warning state."""
        self._flush_failure_reported = False

    def track_flush_task(self, task: asyncio.Task[None]) -> None:
        """Track a fire-and-forget mid-turn flush task."""
        self._pending_persist_tasks.add(task)
        task.add_done_callback(self._pending_persist_tasks.discard)

    async def drain_pending_flushes(self) -> None:
        """Wait for any in-flight background flushes to complete."""
        if self._pending_persist_tasks:
            await asyncio.gather(*self._pending_persist_tasks, return_exceptions=True)
            self._pending_persist_tasks.clear()

    async def cancel_path_flush(self, *, slow_warning_after_s: float = 2.0) -> int:
        """Drain cancel-path persistence and log if it takes longer than expected."""

        async def _cancel_persist() -> None:
            if self._pending_persist_tasks:
                await asyncio.gather(*self._pending_persist_tasks, return_exceptions=True)
            await self.persist_state_locked()

        try:
            cancel_task = asyncio.create_task(_cancel_persist())
            await asyncio.wait_for(asyncio.shield(cancel_task), timeout=slow_warning_after_s)
        except TimeoutError:
            logger.warning(
                "Session {}: cancel-path persist is still running after {}s; waiting for completion",
                self._session_id,
                slow_warning_after_s,
            )
            await cancel_task
        finally:
            self._pending_persist_tasks.clear()
        return 0

    def close(self) -> None:
        """Cancel any tracked background flush tasks."""
        for task in list(self._pending_persist_tasks):
            if not task.done():
                task.cancel()
        self._pending_persist_tasks.clear()

    async def persist_state_locked(self, *, update_messages: bool = True) -> None:
        """Serialize transcript persistence without holding the lock across I/O."""
        async with self._persist_lock:
            if self._persist_inflight:
                self._persist_retry_requested = True
                return
            self._persist_inflight = True

        try:
            while True:
                async with self._persist_lock:
                    snapshot = self._build_persist_snapshot(update_messages=update_messages)
                    self._persist_retry_requested = False

                if snapshot is None:
                    return

                persist_result = await asyncio.to_thread(self._persist_snapshot, snapshot)

                async with self._persist_lock:
                    self._apply_persist_result(snapshot, persist_result)
                    if not persist_result.succeeded and not self._persist_retry_requested:
                        return
                    if not self._persist_retry_requested:
                        follow_up_snapshot = self._build_persist_snapshot(
                            update_messages=update_messages
                        )
                        if follow_up_snapshot is None:
                            return
        finally:
            async with self._persist_lock:
                self._persist_inflight = False

    def persist_state(self, *, update_messages: bool = True) -> None:
        """Persist session state to the platform API when sync is available."""
        snapshot = self._build_persist_snapshot(update_messages=update_messages)
        if snapshot is None:
            return
        persist_result = self._persist_snapshot(snapshot)
        self._apply_persist_result(snapshot, persist_result)

    def _build_persist_snapshot(self, *, update_messages: bool) -> _PersistSnapshot | None:
        """Capture the state needed for one persistence attempt."""
        ctx = self._resolve_api_context()
        if ctx is None:
            return None

        api, org, workspace = ctx
        model = self._get_model()
        agent_name = self._get_agent_name()
        title = self._get_title()
        platform_registered = self._get_platform_registered()

        if not update_messages:
            return _PersistSnapshot(
                api=api,
                org=org,
                workspace=workspace,
                update_messages=False,
                platform_registered=platform_registered,
                model=model,
                title=title,
                agent_name=agent_name,
                persisted_message_count=self._persisted_message_count,
            )

        trajectory = self._get_trajectory()
        if trajectory is None:
            return None

        all_messages = list(trajectory.messages)
        if not all_messages:
            return None

        persisted_message_count = self._persisted_message_count
        # Filter by stable uuid rather than positional slice (see __init__):
        # any message whose uuid hasn't been persisted is new, regardless of
        # where reordering placed it in the list.
        persisted_uuids = self._persisted_message_uuids
        new_messages = [
            m for m in all_messages if str(getattr(m, "uuid", None)) not in persisted_uuids
        ]
        if not new_messages:
            return None
        new_message_uuids = [str(getattr(m, "uuid", None)) for m in new_messages]

        from dreadnode.agents.events import GenerationStep

        usage_by_uuid: dict[str, dict[str, t.Any]] = {}
        for step in trajectory.steps:
            if not isinstance(step, GenerationStep) or not step.messages:
                continue
            assistant = next((m for m in step.messages if str(m.role) == "assistant"), None)
            if assistant is None or getattr(assistant, "uuid", None) is None:
                continue
            entry: dict[str, t.Any] = {
                "input_tokens": step.usage.input_tokens,
                "output_tokens": step.usage.output_tokens,
                "cache_read_input_tokens": step.usage.cache_read_input_tokens,
                "cache_creation_input_tokens": step.usage.cache_creation_input_tokens,
            }
            cost = step.estimated_cost
            if cost is not None:
                entry["cost_usd"] = cost
            usage_by_uuid[str(assistant.uuid)] = entry

        current_system_prompt = self._resolve_agent_system_prompt(agent_name)
        needs_context = (
            persisted_message_count == 0
            or agent_name != self._current_segment_agent
            or model != self._current_segment_model
            or current_system_prompt != self._current_segment_system_prompt
        )
        context: dict[str, t.Any] | None = None
        if needs_context:
            context = {"model": model or ""}
            if agent_name is not None:
                context["agent"] = agent_name
            if current_system_prompt is not None:
                context["system_prompt"] = current_system_prompt

        return _PersistSnapshot(
            api=api,
            org=org,
            workspace=workspace,
            update_messages=True,
            platform_registered=platform_registered,
            model=model,
            title=title,
            agent_name=agent_name,
            persisted_message_count=persisted_message_count,
            all_messages_count=len(all_messages),
            new_messages=new_messages,
            new_message_uuids=new_message_uuids,
            usage_by_uuid=usage_by_uuid or None,
            needs_context=needs_context,
            context=context,
            current_agent=agent_name,
            current_model=model,
            current_system_prompt=current_system_prompt,
        )

    def _persist_snapshot(self, snapshot: _PersistSnapshot) -> _PersistResult:
        """Perform one persistence request from a previously captured snapshot."""
        api = snapshot.api

        if not snapshot.update_messages:
            try:
                if snapshot.platform_registered:
                    api.update_session(
                        snapshot.org,
                        snapshot.workspace,
                        self._session_id,
                        model=snapshot.model or None,
                        agent=snapshot.agent_name,
                        title=snapshot.title,
                    )
            except Exception:
                logger.opt(exception=True).debug("Failed to sync session metadata")
            return _PersistResult()

        try:
            if not snapshot.platform_registered:
                self._register_session()

            result = api.append_transcript(
                snapshot.org,
                snapshot.workspace,
                self._session_id,
                snapshot.new_messages,
                context=snapshot.context,
                usage_by_uuid=snapshot.usage_by_uuid,
            )
        except Exception:
            if not self._flush_failure_reported:
                self._flush_failure_reported = True
                logger.opt(exception=True).warning(
                    "Failed to persist transcript to API (further failures "
                    "in this turn will be logged at debug)"
                )
            else:
                logger.opt(exception=True).debug("Failed to persist transcript to API")
            return _PersistResult(succeeded=False)

        return _PersistResult(last_seq=result.get("last_seq"))

    def _apply_persist_result(
        self,
        snapshot: _PersistSnapshot,
        persist_result: _PersistResult,
    ) -> None:
        """Apply a completed persistence attempt back onto local state."""
        if not snapshot.update_messages or not persist_result.succeeded:
            return

        if persist_result.last_seq is not None:
            self._last_persisted_seq = persist_result.last_seq

        self._persisted_message_count = max(
            self._persisted_message_count,
            snapshot.all_messages_count,
        )
        if snapshot.new_message_uuids:
            self._persisted_message_uuids.update(snapshot.new_message_uuids)
        if snapshot.needs_context:
            self._current_segment_agent = snapshot.current_agent
            self._current_segment_model = snapshot.current_model
            self._current_segment_system_prompt = snapshot.current_system_prompt
