import typing as t
from dataclasses import dataclass

from loguru import logger

if t.TYPE_CHECKING:
    from dreadnode.app.server.app import SessionRuntime
    from dreadnode.capabilities.capability import Capability
    from dreadnode.capabilities.types import AgentDef
    from dreadnode.storage import SessionRecord


@dataclass(slots=True)
class SessionHydrator:
    """Restore sessions from persisted local records or platform transcripts."""

    sessions: dict[str, "SessionRuntime"]
    resolve_persisted_binding: t.Callable[
        [str | None, str | None],
        tuple[str | None, "Capability | None", "AgentDef | None"],
    ]
    get_api_context: t.Callable[[], tuple[t.Any, str, str, str] | None]
    session_factory: t.Callable[..., "SessionRuntime"]

    def hydrate_record(self, record: "SessionRecord") -> "SessionRuntime":
        """Restore a session from a local persisted session record."""
        capability_name, capability_obj, agent_def = self.resolve_persisted_binding(
            record.capability,
            record.agent,
        )
        session = self.session_factory(
            record.session_id,
            model=record.model,
            project=record.project,
            capability_name=capability_name or record.capability,
            capability=capability_obj,
            agent_def=agent_def,
        )
        self._apply_restored_metadata(
            session,
            title=record.title,
            message_count=record.message_count,
            agent_name=record.agent,
            created_at=record.created_at,
            agent_def=agent_def,
        )
        if record.trajectory is not None:
            session.restore_trajectory(record.trajectory, persist=False)
        # If the persisted model is empty (e.g. the session was saved before
        # the first turn resolved a canonical model), try to recover it from
        # the restored trajectory's last generation step.
        if not session.model and record.trajectory is not None:
            recovered = _model_from_trajectory(record.trajectory)
            if recovered:
                session.model = recovered
        self.sessions[record.session_id] = session
        return session

    def hydrate_from_api(self, session_id: str) -> "SessionRuntime | None":
        """Restore a session from the platform transcript endpoint."""
        ctx = self.get_api_context()
        if ctx is None:
            return None

        api, org, workspace, _user_id = ctx
        data = self._fetch_transcript(api, org, workspace, session_id)
        if data is None:
            return None

        session_data = data.get("session")
        messages_data = self._fetch_transcript_messages(
            api,
            org,
            workspace,
            session_id,
            first_page=data,
        )
        if not session_data:
            return None

        agent_name = session_data.get("agent")
        capability_name, capability_obj, agent_def = self.resolve_persisted_binding(
            None, agent_name
        )
        session = self.session_factory(
            session_id,
            model=session_data.get("model", ""),
            project=session_data.get("project_name"),
            capability_name=capability_name,
            capability=capability_obj,
            agent_def=agent_def,
        )
        self._apply_restored_metadata(
            session,
            title=session_data.get("title"),
            message_count=session_data.get("message_count", 0),
            agent_name=agent_name,
            created_at=None,
            agent_def=agent_def,
        )
        if messages_data:
            self._restore_api_transcript(
                session,
                messages_data=messages_data,
                current_system_prompt=data.get("current_system_prompt"),
            )
            # If the session-level model is empty (e.g. the session was
            # registered before the first turn resolved a canonical model),
            # recover it from the last assistant message's model field.
            # Without this, ``to_info()`` returns ``model=None`` and the
            # TUI resume path falls back to the default model instead of
            # preserving the model the session actually used.
            if not session.model:
                for msg in reversed(messages_data):
                    if msg.get("role") == "assistant" and msg.get("model"):
                        session.model = msg["model"]
                        break

        session._platform_registered = True
        session.mark_sync_ok()
        self.sessions[session_id] = session
        return session

    def _fetch_transcript(
        self,
        api: t.Any,
        org: str,
        workspace: str,
        session_id: str,
    ) -> dict[str, t.Any] | None:
        try:
            return api.get_transcript(org, workspace, session_id, limit=5000)
        except Exception:
            logger.debug("Failed to fetch transcript from API for {}", session_id[:8])
            return None

    def _fetch_transcript_messages(
        self,
        api: t.Any,
        org: str,
        workspace: str,
        session_id: str,
        *,
        first_page: dict[str, t.Any],
    ) -> list[dict[str, t.Any]]:
        messages_data: list[dict[str, t.Any]] = list(first_page.get("messages", []))
        data = first_page
        while data.get("has_more"):
            last_seq = messages_data[-1].get("seq", 0) if messages_data else 0
            try:
                data = api.get_transcript(
                    org,
                    workspace,
                    session_id,
                    after_seq=last_seq,
                    limit=5000,
                )
                page = data.get("messages", [])
                if not page:
                    break
                messages_data.extend(page)
            except Exception:
                logger.debug("Failed to paginate transcript for {}", session_id[:8])
                break
        return messages_data

    def _apply_restored_metadata(
        self,
        session: "SessionRuntime",
        *,
        title: str | None,
        message_count: int,
        agent_name: str | None,
        created_at: t.Any,
        agent_def: "AgentDef | None",
    ) -> None:
        session.title = title
        session._message_count = message_count
        session._last_turn_agent = agent_name
        if created_at is not None:
            session.created_at = created_at
        if agent_def is None and agent_name is not None:
            session._agent_name_override = agent_name

    def _restore_api_transcript(
        self,
        session: "SessionRuntime",
        *,
        messages_data: list[dict[str, t.Any]],
        current_system_prompt: str | None,
    ) -> None:
        from dreadnode.agents.trajectory import trajectory_from_openai_format

        trajectory = trajectory_from_openai_format(_api_messages_to_openai_format(messages_data))
        session._trajectory = trajectory
        if current_system_prompt:
            session._trajectory.system_prompt = current_system_prompt

        last_msg = messages_data[-1]
        session.persistence.last_persisted_seq = last_msg.get("seq", -1)
        session.persistence.persisted_message_count = len(session._trajectory.messages)
        session.persistence.restore_segment_context(
            agent=last_msg.get("agent"),
            model=last_msg.get("model"),
            system_prompt=current_system_prompt,
        )


def _api_messages_to_openai_format(messages_data: list[dict[str, t.Any]]) -> list[dict[str, t.Any]]:
    """Convert platform transcript messages into OpenAI-format message dicts."""
    openai_messages: list[dict[str, t.Any]] = []
    for msg in messages_data:
        converted: dict[str, t.Any] = {
            "role": msg.get("role", "user"),
            "content": msg.get("content", ""),
        }
        if msg.get("tool_calls"):
            converted["tool_calls"] = [
                {
                    "id": tool_call["id"],
                    "type": "function",
                    "function": {
                        "name": tool_call["name"],
                        "arguments": tool_call["arguments"],
                    },
                }
                for tool_call in msg["tool_calls"]
            ]
        if msg.get("tool_call_id"):
            converted["tool_call_id"] = msg["tool_call_id"]
        if msg.get("metadata"):
            converted["metadata"] = msg["metadata"]
        openai_messages.append(converted)
    return openai_messages


def _model_from_trajectory(trajectory_data: dict[str, t.Any]) -> str | None:
    """Recover the model from the last generation step in a serialized trajectory.

    The trajectory dict may contain a ``steps`` list with ``GenerationStep``
    entries that carry a ``model`` field. We walk backwards to find the most
    recent one. Returns ``None`` when no step has a usable model.
    """
    steps = trajectory_data.get("steps")
    if not isinstance(steps, list):
        return None
    for step in reversed(steps):
        if not isinstance(step, dict):
            continue
        # GenerationStep stores the model at the top level or inside
        # ``generator_config`` depending on the serialization version.
        step_typed = t.cast("dict[str, t.Any]", step)
        model = step_typed.get("model")
        if not model:
            config = step_typed.get("generator_config")
            if isinstance(config, dict):
                model = t.cast("dict[str, t.Any]", config).get("model")
        if model and isinstance(model, str):
            return model
    return None
