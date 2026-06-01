"""Subagent support for codrninja."""

from __future__ import annotations

import copy
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from .agent import Agent, AgentMode

if TYPE_CHECKING:
    from .core import AICode


class Subagent(Agent):
    """Child agent with isolated history and parent messaging."""

    def __init__(
        self,
        ai: "AICode",
        session_name: str,
        task: str,
        parent_agent: Agent,
        name: str,
        max_iterations: int = 10,
        mode: str = AgentMode.BUILD,
    ):
        self.parent_agent = parent_agent
        self.name = name
        self.task = task
        self.messages_to_parent: List[Dict[str, Any]] = []
        self.last_active_at = time.time()
        self.parent_context = copy.deepcopy(parent_agent.message_history)
        super().__init__(
            ai=ai,
            session_name=session_name,
            max_iterations=max_iterations,
            mode=AgentMode.SUBAGENT,
            parent_permission_manager=parent_agent.permissions,
            max_steps=parent_agent.max_steps,
        )

    def _build_system_prompt(self) -> str:
        base_prompt = super()._build_system_prompt()
        return (
            f"{base_prompt}\n\n"
            f"You are a subagent focused on: {self.task}. Report concisely."
        )

    def _build_context(self, message: str) -> str:
        context = super()._build_context(message)
        if self.parent_context:
            context += "\nParent session context:\n"
            for item in self.parent_context[-6:]:
                role = item.get("role", "unknown")
                content = item.get("content", "")
                context += f"- {role}: {content[:500]}\n"
        return context

    def run(self, message: str, auto_approve: bool = False) -> Dict[str, Any]:
        self.last_active_at = time.time()
        result = super().run(message, auto_approve=auto_approve)
        self.last_active_at = time.time()
        self.send_to_parent(result)
        return result

    def send_to_parent(self, payload: Dict[str, Any]):
        """Record a concise message for the parent agent."""
        self.last_active_at = time.time()
        message = {
            "session_id": self.session_name,
            "name": self.name,
            "task": self.task,
            "result": payload,
            "timestamp": self.last_active_at,
        }
        self.messages_to_parent.append(message)
        self.parent_agent.receive_subagent_message(message)


class SubagentManager:
    """Manage subagents within the current process."""

    def __init__(
        self,
        ai: "AICode",
        parent_agent: Agent,
        timeout_seconds: int = 300,
        time_fn: Optional[Callable[[], float]] = None,
    ):
        self.ai = ai
        self.parent_agent = parent_agent
        self.timeout_seconds = timeout_seconds
        self.time_fn = time_fn or time.time
        self._subagents: Dict[str, Subagent] = {}

    def spawn(self, name: str, task: str, mode: str = AgentMode.BUILD) -> Subagent:
        """Create a subagent with an isolated child session."""
        self._cleanup_inactive()
        suffix = uuid.uuid4().hex[:8]
        session_id = f"{self.parent_agent.session_name}::{name}-{suffix}"
        self.ai.create_session(session_id)
        subagent = Subagent(
            ai=self.ai,
            session_name=session_id,
            task=task,
            parent_agent=self.parent_agent,
            name=name,
            max_iterations=self.parent_agent.max_iterations,
            mode=mode,
        )
        self._subagents[session_id] = subagent
        return subagent

    def kill(self, session_id: str) -> bool:
        """Remove an active subagent."""
        self._cleanup_inactive()
        return self._subagents.pop(session_id, None) is not None

    def list(self) -> List[Dict[str, Any]]:
        """List active subagents."""
        self._cleanup_inactive()
        return [
            {
                "session_id": subagent.session_name,
                "name": subagent.name,
                "task": subagent.task,
                "mode": subagent.mode,
                "last_active_at": subagent.last_active_at,
                "messages_to_parent": len(subagent.messages_to_parent),
            }
            for subagent in self._subagents.values()
        ]

    def get(self, session_id: str) -> Optional[Subagent]:
        """Get a subagent by session identifier."""
        self._cleanup_inactive()
        subagent = self._subagents.get(session_id)
        if subagent:
            subagent.last_active_at = self.time_fn()
        return subagent

    def _cleanup_inactive(self):
        now = self.time_fn()
        expired = [
            session_id
            for session_id, subagent in self._subagents.items()
            if now - subagent.last_active_at > self.timeout_seconds
        ]
        for session_id in expired:
            self._subagents.pop(session_id, None)
