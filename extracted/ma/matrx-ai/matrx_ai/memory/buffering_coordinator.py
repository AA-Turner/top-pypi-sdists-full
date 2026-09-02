"""
Buffering Coordinator
Manages static state for background async buffering tasks to prevent race conditions.

Mirrors: packages/memory/src/processors/observational-memory/buffering-coordinator.ts
"""

import asyncio
import logging
from typing import Optional

from .types import MemoryScope, ObservationConfig, ReflectionConfig, ObservationalMemoryRecord

logger = logging.getLogger(__name__)

class BufferingCoordinator:
    """
    Manages the static buffering state machine for async observation and reflection.
    Static maps are shared across all ObservationalMemory instances in a process.
    """
    
    # Track in-flight async buffering operations
    async_buffering_ops: dict[str, asyncio.Task] = {}
    
    # Track the last token boundary at which we started buffering
    last_buffered_boundary: dict[str, int] = {}
    
    # Track cycleId for in-flight buffered reflections
    reflection_buffer_cycle_ids: dict[str, str] = {}

    def __init__(
        self,
        observation_config: ObservationConfig,
        reflection_config: ReflectionConfig,
        scope: MemoryScope,
    ):
        self.observation_config = observation_config
        self.reflection_config = reflection_config
        self.scope = scope

    def get_lock_key(self, thread_id: Optional[str], resource_id: Optional[str]) -> str:
        if self.scope == MemoryScope.RESOURCE and resource_id:
            return f"resource:{resource_id}"
        return f"thread:{thread_id or 'unknown'}"

    def is_async_observation_enabled(self) -> bool:
        return (
            self.observation_config.buffer_tokens is not None 
            and self.observation_config.buffer_tokens > 0
        )

    def is_async_reflection_enabled(self) -> bool:
        return (
            self.reflection_config.buffer_activation is not None 
            and self.reflection_config.buffer_activation > 0
        )

    def get_observation_buffer_key(self, lock_key: str) -> str:
        return f"obs:{lock_key}"

    def get_reflection_buffer_key(self, lock_key: str) -> str:
        return f"refl:{lock_key}"

    def is_async_buffering_in_progress(self, buffer_key: str) -> bool:
        task = self.async_buffering_ops.get(buffer_key)
        if task and not task.done():
            return True
        if task and task.done():
            # Clean up finished task
            self.async_buffering_ops.pop(buffer_key, None)
        return False

    def should_trigger_async_observation(
        self,
        current_tokens: int,
        lock_key: str,
        record: ObservationalMemoryRecord,
        message_tokens_threshold: int,
    ) -> bool:
        if not self.is_async_observation_enabled():
            return False

        if record.is_buffering_observation:
            # We don't have a reliable process-level op registry in this basic port,
            # so we'll assume the flag is cleared on success/failure.
            pass

        buffer_key = self.get_observation_buffer_key(lock_key)
        if self.is_async_buffering_in_progress(buffer_key):
            return False

        # In a real dynamic shared budget, buffer_tokens could be a fraction
        buffer_tokens = self.observation_config.buffer_tokens
        if isinstance(buffer_tokens, float) and buffer_tokens < 1.0:
            buffer_tokens = int(message_tokens_threshold * buffer_tokens)
            
        db_boundary = record.last_buffered_at_tokens or 0
        mem_boundary = self.last_buffered_boundary.get(buffer_key, 0)
        last_boundary = max(db_boundary, mem_boundary)

        # Simplify ramp logic for python MVP
        effective_buffer_tokens = buffer_tokens
        
        if effective_buffer_tokens <= 0:
            return False

        current_interval = current_tokens // effective_buffer_tokens
        last_interval = last_boundary // effective_buffer_tokens

        should_trigger = current_interval > last_interval

        logger.debug(
            f"[OM:shouldTriggerAsyncObs] tokens={current_tokens}, "
            f"bufferTokens={buffer_tokens}, "
            f"currentInterval={current_interval}, lastInterval={last_interval}, "
            f"lastBoundary={last_boundary}, shouldTrigger={should_trigger}"
        )

        return should_trigger

    @classmethod
    async def await_buffering(
        cls,
        thread_id: Optional[str],
        resource_id: Optional[str],
        scope: MemoryScope,
        timeout_ms: int = 30000,
    ) -> None:
        lock_key = f"resource:{resource_id}" if scope == MemoryScope.RESOURCE and resource_id else f"thread:{thread_id or 'unknown'}"
        obs_key = f"obs:{lock_key}"
        refl_key = f"refl:{lock_key}"
        
        tasks = []
        if obs_key in cls.async_buffering_ops and not cls.async_buffering_ops[obs_key].done():
            tasks.append(cls.async_buffering_ops[obs_key])
        if refl_key in cls.async_buffering_ops and not cls.async_buffering_ops[refl_key].done():
            tasks.append(cls.async_buffering_ops[refl_key])
            
        if not tasks:
            return
            
        try:
            await asyncio.wait(tasks, timeout=timeout_ms / 1000.0)
        except Exception as e:
            logger.warning(f"[OM:awaitBuffering] Exception while awaiting: {e}")
