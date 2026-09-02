"""
Observational Memory Orchestrator
The core processor that manages the lifecycle of the memory system.

Mirrors: packages/memory/src/processors/observational-memory/observational-memory.ts
"""

import asyncio
import logging
from collections.abc import Callable, Coroutine

from .buffering_coordinator import BufferingCoordinator
from .constants import OBSERVATION_CONTEXT_PROMPT
from .observer_runner import ObserverRunner
from .reflector_runner import ReflectorRunner
from .storage import ObservationalMemoryStorage, get_or_create_record
from .thresholds import calculate_dynamic_threshold
from .types import (
    BufferedObservationChunk,
    Message,
    MessageRole,
    ObservationalMemoryConfig,
    ObservationalMemoryStatus,
)

logger = logging.getLogger(__name__)


class ObservationalMemory:
    """
    ObservationalMemory - A three-agent memory system for long conversations.
    """

    def __init__(
        self,
        config: ObservationalMemoryConfig,
        storage: ObservationalMemoryStorage,
        count_tokens_fn: Callable[[str], int],
        llm_call_fn: Callable[[str, list[dict], float, int], Coroutine[None, None, str]],
    ):
        self.config = config
        self.storage = storage
        self.count_tokens_fn = count_tokens_fn
        self.llm_call_fn = llm_call_fn

        # In a real async environment, these would be per-instance locks
        self.observed_message_ids: set[str] = set()

        self.observer = ObserverRunner(
            observation_config=self.config.observation,
            observed_message_ids=self.observed_message_ids,
            llm_call_fn=self.llm_call_fn,
        )

        self.reflector = ReflectorRunner(
            reflection_config=self.config.reflection,
            llm_call_fn=self.llm_call_fn,
            count_tokens_fn=self.count_tokens_fn,
        )

        self.buffering = BufferingCoordinator(
            observation_config=self.config.observation,
            reflection_config=self.config.reflection,
            scope=self.config.scope,
        )

    async def get_or_create_record(self, thread_id: str, resource_id: str):
        return await get_or_create_record(
            storage=self.storage,
            resource_id=resource_id,
            thread_id=thread_id,
            scope=self.config.scope,
        )

    async def get_status(
        self, thread_id: str, resource_id: str, messages: list[Message]
    ) -> ObservationalMemoryStatus:
        """Calculate token budgets and determine if action is needed."""
        record = await self.get_or_create_record(thread_id, resource_id)

        # Calculate unobserved message tokens
        unobserved_messages = [
            msg for msg in messages if msg.id not in self.observed_message_ids and not msg.observed
        ]

        # The first tiktoken call constructs a large CoreBPE synchronously. Keep
        # both that cold start and large-message encoding off the server loop.
        uncached_messages = [msg for msg in unobserved_messages if msg.token_count is None]
        if uncached_messages:
            token_counts = await asyncio.to_thread(
                lambda: [self.count_tokens_fn(msg.get_text()) for msg in uncached_messages]
            )
            for msg, token_count in zip(uncached_messages, token_counts, strict=True):
                msg.token_count = token_count

        pending_message_tokens = sum(msg.token_count or 0 for msg in unobserved_messages)

        # Dynamic thresholds based on shared budget
        current_observation_tokens = record.observation_token_count

        if self.config.share_token_budget:
            effective_msg_threshold = calculate_dynamic_threshold(
                self.config.observation.token_threshold, current_observation_tokens
            )
        else:
            effective_msg_threshold = (
                self.config.observation.token_threshold
                if isinstance(self.config.observation.token_threshold, int)
                else self.config.observation.token_threshold.max
            )

        effective_obs_threshold = (
            self.config.reflection.token_threshold
            if isinstance(self.config.reflection.token_threshold, int)
            else self.config.reflection.token_threshold.max
        )

        # Should buffer? Check interval boundary using DB-backed state
        async_observation_enabled = self.buffering.is_async_observation_enabled()
        should_buffer = False
        if async_observation_enabled and pending_message_tokens < effective_msg_threshold:
            lock_key = self.buffering.get_lock_key(thread_id, resource_id)
            should_buffer = self.buffering.should_trigger_async_observation(
                pending_message_tokens,
                lock_key,
                record,
                effective_msg_threshold,
            )

        # Can activate?
        buffered_chunk_count = len(record.buffered_observations)
        can_activate = buffered_chunk_count > 0

        should_observe = pending_message_tokens >= effective_msg_threshold
        should_reflect = current_observation_tokens >= effective_obs_threshold

        return ObservationalMemoryStatus(
            should_observe=should_observe,
            should_buffer=should_buffer,
            should_reflect=should_reflect,
            message_tokens=pending_message_tokens,
            observation_tokens=current_observation_tokens,
            unobserved_message_tokens=pending_message_tokens,
            pending_buffered_tokens=0,
            message_token_threshold=effective_msg_threshold,
            observation_token_threshold=effective_obs_threshold,
            buffer_token_threshold=0,
            has_buffered_chunks=can_activate,
            buffered_chunk_count=buffered_chunk_count,
        )

    async def process_input_step(
        self, messages: list[Message], thread_id: str, resource_id: str
    ) -> list[Message]:
        """
        Invoked before calling the Actor LLM.
        - Loads the OM record.
        - Injects observations into the system prompt.
        - Filters out messages that have already been observed.
        """
        record = await self.get_or_create_record(thread_id, resource_id)

        if not record.active_observations:
            return messages

        from .constants import OBSERVATION_CONTEXT_INSTRUCTIONS

        context_prompt = f"{OBSERVATION_CONTEXT_PROMPT}\n\n<observations>\n{record.active_observations}\n</observations>\n\n{OBSERVATION_CONTEXT_INSTRUCTIONS}"
        if record.current_task:
            context_prompt = context_prompt.replace(
                "{{currentTask}}", f"<current-task>\n{record.current_task}\n</current-task>"
            )
        else:
            context_prompt = context_prompt.replace("{{currentTask}}", "")

        if record.suggested_response:
            context_prompt = context_prompt.replace(
                "{{suggestedResponse}}",
                f"<suggested-response>\n{record.suggested_response}\n</suggested-response>",
            )
        else:
            context_prompt = context_prompt.replace("{{suggestedResponse}}", "")

        # Strip out already observed messages
        unobserved = []
        for msg in messages:
            if msg.id in self.observed_message_ids or msg.observed:
                continue
            unobserved.append(msg)

        # Prepend OM context as a system message
        om_sys_msg = Message(
            id="om-context",
            thread_id=thread_id,
            resource_id=resource_id,
            role=MessageRole.SYSTEM,
            content=context_prompt,
        )

        return [om_sys_msg] + unobserved

    async def buffer(self, thread_id: str, resource_id: str, messages: list[Message]) -> None:
        """Summarize unobserved messages into a buffer chunk (same coordinator as caller)."""
        record = await self.get_or_create_record(thread_id, resource_id)
        record = await self.storage.upsert_record(record)

        unobserved = [
            msg for msg in messages if msg.id not in self.observed_message_ids and not msg.observed
        ]

        if not unobserved:
            return

        try:
            obs_result = await self.observer.call(
                existing_observations=record.active_observations,
                messages_to_observe=unobserved,
                prior_current_task=record.current_task,
                prior_suggested_response=record.suggested_response,
            )

            import uuid
            from datetime import UTC, datetime

            chunk = BufferedObservationChunk(
                cycle_id=str(uuid.uuid4()),
                observations=obs_result.observations,
                message_tokens=sum(msg.token_count or 0 for msg in unobserved),
                observation_tokens=self.count_tokens_fn(obs_result.observations),
                message_count=len(unobserved),
                message_ids=[m.id for m in unobserved],
                message_range=(unobserved[0].id, unobserved[-1].id),
            )
            # Mutate in-memory + upsert — do not RMW from DB. The OM row may
            # still be a pending INSERT on this coordinator and a SELECT would
            # miss it (then silently drop the chunk).
            record.buffered_observations = list(record.buffered_observations or []) + [chunk]
            record.last_buffered_at_tokens = int(record.last_buffered_at_tokens or 0) + int(
                chunk.message_tokens or 0
            )
            record.observed_message_ids = list(record.observed_message_ids or []) + [
                m.id for m in unobserved
            ]
            record.last_buffered_at_time = unobserved[-1].created_at or datetime.now(UTC)
            record.is_buffering_observation = False
            await self.storage.upsert_record(record)
        except Exception as e:
            logger.error(f"[OM:buffer] Failed background observation: {e}")
            await self.storage.set_buffering_observation_flag(record.id, False)

    async def activate(self, thread_id: str, resource_id: str) -> None:
        """Merge pending buffer chunks into active observations."""
        record = await self.get_or_create_record(thread_id, resource_id)
        if not record.buffered_observations:
            return

        combined = []
        if record.active_observations:
            combined.append(record.active_observations)

        for chunk in record.buffered_observations:
            combined.append(chunk.observations)

        new_text = "\n\n".join(combined)
        record.active_observations = new_text
        record.observation_token_count = self.count_tokens_fn(new_text)
        record.buffered_observations = []
        record.is_buffering_observation = False
        record.last_buffered_at_tokens = 0
        record.generation_count = int(record.generation_count or 0) + 1
        await self.storage.upsert_record(record)

    async def process_output_step(
        self, messages: list[Message], thread_id: str, resource_id: str
    ) -> None:
        """
        Invoked after the Actor LLM replies.
        - Calculates unobserved token count.
        - Triggers Observer if threshold is reached.
        - Triggers Reflector if observation threshold is reached.
        """
        status = await self.get_status(thread_id, resource_id, messages)
        record = await self.get_or_create_record(thread_id, resource_id)
        record = await self.storage.upsert_record(record)

        if status.should_buffer:
            # Await in-lane: the OM post-hook already runs as a background task
            # under standalone_coordinator. A nested create_task + new coordinator
            # would race the parent's still-pending OM INSERT. Same coordinator
            # → queue create then buffer updates in one flush.
            logger.info("[OM] Running observation buffer under active coordinator.")
            await self.storage.set_buffering_observation_flag(record.id, True)
            await self.buffer(thread_id, resource_id, messages)

        if status.should_observe:
            if status.has_buffered_chunks:
                logger.info("[OM] Activating buffered chunks before sync observation.")
                await self.activate(thread_id, resource_id)
                # Re-fetch record since activate() modifies it
                record = await self.get_or_create_record(thread_id, resource_id)

            logger.info(
                f"[OM] Triggering Observer (tokens: {status.message_tokens}/{status.message_token_threshold})"
            )

            unobserved = [
                msg
                for msg in messages
                if msg.id not in self.observed_message_ids and not msg.observed
            ]

            try:
                obs_result = await self.observer.call(
                    existing_observations=record.active_observations,
                    messages_to_observe=unobserved,
                    prior_current_task=record.current_task,
                    prior_suggested_response=record.suggested_response,
                )

                # Update record
                record.active_observations = obs_result.observations
                record.observation_token_count = self.count_tokens_fn(obs_result.observations)
                record.current_task = obs_result.current_task
                record.suggested_response = obs_result.suggested_response

                await self.storage.upsert_record(record)

            except Exception as e:
                logger.error(f"[OM] Observer failed: {e}")

        # Re-fetch status to check reflection threshold post-observation
        status = await self.get_status(thread_id, resource_id, messages)

        # Check if we should activate buffered reflection
        if record.buffered_reflection:
            logger.info("[OM] Activating buffered reflection.")
            current_lines = (record.active_observations or "").split("\n")
            line_count = int(record.reflected_observation_line_count or 0)
            unreflected_lines = current_lines[line_count:] if line_count else []
            new_obs = record.buffered_reflection
            if unreflected_lines:
                new_obs += "\n\n" + "\n".join(unreflected_lines)
            record.active_observations = new_obs
            record.observation_token_count = self.count_tokens_fn(new_obs)
            record.buffered_reflection = None
            record.buffered_reflection_tokens = 0
            record.buffered_reflection_input_tokens = 0
            record.reflected_observation_line_count = 0
            record.generation_count = int(record.generation_count or 0) + 1
            await self.storage.upsert_record(record)

        async_reflection_enabled = self.buffering.is_async_reflection_enabled()
        should_buffer_reflection = False
        if (
            async_reflection_enabled
            and status.observation_tokens < status.observation_token_threshold
        ):
            buffer_activation = self.config.reflection.buffer_activation or 0.5
            if status.observation_tokens >= (
                status.observation_token_threshold * buffer_activation
            ):
                should_buffer_reflection = True

        if should_buffer_reflection and not record.is_buffering_reflection:
            logger.info("[OM] Running reflection buffer under active coordinator.")
            await self.storage.set_buffering_reflection_flag(record.id, True)
            await self.reflector.do_async_buffered_reflection(
                record_id=record.id,
                observations=record.active_observations,
                storage=self.storage,
                observation_tokens_threshold=status.observation_token_threshold,
            )

        if status.should_reflect:
            logger.info(
                f"[OM] Triggering Reflector (tokens: {status.observation_tokens}/{status.observation_token_threshold})"
            )
            try:
                ref_result = await self.reflector.call(
                    observations=record.active_observations,
                    observation_tokens_threshold=status.observation_token_threshold,
                )

                # Update record
                record.active_observations = ref_result.reflections
                record.observation_token_count = self.count_tokens_fn(ref_result.reflections)
                record.generation_count += 1

                await self.storage.upsert_record(record)

            except Exception as e:
                logger.error(f"[OM] Reflector failed: {e}")
