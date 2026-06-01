"""CompanionService — the core agent loop tying YantrikDB + LLM + instincts together."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any, Optional

from yantrikdb.agent.config import CompanionConfig
from yantrikdb.agent.context import build_messages
from yantrikdb.agent.instincts import load_instincts
from yantrikdb.agent.instincts.protocol import CompanionState, Instinct, UrgeSpec
from yantrikdb.agent.learning import extract_and_learn
from yantrikdb.agent.llm import LLMClient
from yantrikdb.agent.tools import COMPANION_TOOLS, execute_tool
from yantrikdb.agent.urges import UrgeQueue

log = logging.getLogger("yantrik.companion")


@dataclass
class AgentResponse:
    message: str
    memories_recalled: int = 0
    urges_delivered: list[str] = field(default_factory=list)
    tool_calls_made: list[str] = field(default_factory=list)


class CompanionService:
    """The brain of Yantrik — handles conversation, memory, and proactive behavior."""

    def __init__(self, db, config: CompanionConfig):
        self.db = db
        self.config = config
        self.llm = LLMClient(config.llm)
        self.urge_queue = UrgeQueue(db._conn, config.urges)
        self.instincts: list[Instinct] = load_instincts(config.instincts)

        self.conversation_history: list[dict] = []
        self.last_interaction_ts: float = time.time()
        self.session_turn_count: int = 0
        self.proactive_message: Optional[dict] = None

        # Cached from last think()
        self._pending_triggers: list[dict] = []
        self._active_patterns: list[dict] = []
        self._open_conflicts_count: int = 0
        self._recent_valence_avg: Optional[float] = None

        log.info("CompanionService initialized with %d instincts", len(self.instincts))

    def build_state(self) -> CompanionState:
        """Build a read-only state snapshot for instinct evaluation."""
        stats = self.db.stats()
        return CompanionState(
            last_interaction_ts=self.last_interaction_ts,
            current_ts=time.time(),
            session_active=self.session_turn_count > 0,
            conversation_turn_count=self.session_turn_count,
            recent_valence_avg=self._recent_valence_avg,
            pending_triggers=self._pending_triggers,
            active_patterns=self._active_patterns,
            open_conflicts_count=self._open_conflicts_count,
            memory_count=stats.get("active_memories", 0),
            config_user_name=self.config.user_name,
        )

    def _check_session_timeout(self):
        """Check if the conversation session has timed out."""
        timeout_secs = self.config.conversation.session_timeout_minutes * 60
        if (time.time() - self.last_interaction_ts) > timeout_secs and self.session_turn_count > 0:
            log.info("Session timed out after %d turns", self.session_turn_count)
            self.conversation_history.clear()
            self.session_turn_count = 0

    async def handle_message(self, user_text: str) -> AgentResponse:
        """Process a user message through the full agent pipeline."""
        self._check_session_timeout()
        self.last_interaction_ts = time.time()
        self.session_turn_count += 1

        state = self.build_state()

        # 1. Recall relevant memories
        try:
            memories = self.db.recall(
                query=user_text,
                top_k=5,
                expand_entities=True,
            )
        except Exception as e:
            log.warning("Recall failed: %s", e)
            memories = []

        # 2. Pop pending urges for this interaction
        urges = self.urge_queue.pop_for_interaction(limit=2)

        # 3. Evaluate instincts on interaction
        for instinct in self.instincts:
            try:
                specs = instinct.on_interaction(state, user_text)
                for spec in specs:
                    self.urge_queue.push(spec)
            except Exception as e:
                log.warning("Instinct %s on_interaction failed: %s", instinct.name, e)

        # 4. Build LLM context (with personality)
        personality = None
        try:
            personality = self.db.get_personality()
        except Exception:
            pass

        messages = build_messages(
            user_text=user_text,
            config=self.config,
            state=state,
            memories=memories,
            urges=urges,
            patterns=self._active_patterns[:2],
            conversation_history=self.conversation_history,
            personality=personality,
        )

        # 5. Call LLM with tool support
        tools = COMPANION_TOOLS if self.config.tools.enabled else None
        tool_calls_made = []

        for _round in range(self.config.tools.max_tool_rounds):
            llm_resp = await self.llm.chat(messages, tools=tools)

            if not llm_resp.tool_calls:
                break

            # Execute tool calls
            for tc in llm_resp.tool_calls:
                func_name = tc["function"]["name"]
                try:
                    args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError:
                    args = {}

                result = execute_tool(self.db, func_name, args)
                tool_calls_made.append(func_name)

                # Append tool call and result to messages for next round
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tc],
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.get("id", ""),
                    "content": result,
                })

        response_text = llm_resp.content

        # 6. Update conversation history
        self.conversation_history.append({"role": "user", "content": user_text})
        self.conversation_history.append({"role": "assistant", "content": response_text})

        # Trim history to max turns
        max_entries = self.config.conversation.max_history_turns * 2
        if len(self.conversation_history) > max_entries:
            self.conversation_history = self.conversation_history[-max_entries:]

        # 7. Fire-and-forget learning
        asyncio.create_task(extract_and_learn(self.db, self.llm, user_text, response_text))

        return AgentResponse(
            message=response_text,
            memories_recalled=len(memories),
            urges_delivered=[u.get("urge_id", "") for u in urges],
            tool_calls_made=tool_calls_made,
        )

    async def handle_message_stream(self, user_text: str) -> AsyncIterator[str]:
        """Stream a response token-by-token. Skips tool calls for streaming path."""
        self._check_session_timeout()
        self.last_interaction_ts = time.time()
        self.session_turn_count += 1

        state = self.build_state()

        # Recall memories
        try:
            memories = self.db.recall(query=user_text, top_k=5, expand_entities=True)
        except Exception as e:
            log.warning("Recall failed: %s", e)
            memories = []

        # Pop urges
        urges = self.urge_queue.pop_for_interaction(limit=2)

        # Evaluate instincts
        for instinct in self.instincts:
            try:
                for spec in instinct.on_interaction(state, user_text):
                    self.urge_queue.push(spec)
            except Exception as e:
                log.warning("Instinct %s failed: %s", instinct.name, e)

        # Build context (with personality)
        personality = None
        try:
            personality = self.db.get_personality()
        except Exception:
            pass

        messages = build_messages(
            user_text=user_text,
            config=self.config,
            state=state,
            memories=memories,
            urges=urges,
            patterns=self._active_patterns[:2],
            conversation_history=self.conversation_history,
            personality=personality,
        )

        # Stream tokens
        full_response = []
        async for token in self.llm.chat_stream(messages):
            full_response.append(token)
            yield token

        response_text = "".join(full_response)

        # Update history
        self.conversation_history.append({"role": "user", "content": user_text})
        self.conversation_history.append({"role": "assistant", "content": response_text})
        max_entries = self.config.conversation.max_history_turns * 2
        if len(self.conversation_history) > max_entries:
            self.conversation_history = self.conversation_history[-max_entries:]

        # Fire-and-forget learning
        asyncio.create_task(extract_and_learn(self.db, self.llm, user_text, response_text))

    def get_proactive_message(self) -> Optional[dict]:
        """Return and clear any pending proactive message."""
        msg = self.proactive_message
        self.proactive_message = None
        return msg

    async def close(self):
        await self.llm.close()
