"""
Reflector Runner: manages the execution lifecycle of the Reflector agent.
Handles progressive compression levels and execution.

Mirrors: packages/memory/src/processors/observational-memory/reflector-runner.ts
"""

import logging
from typing import Callable, Coroutine, Optional

from .reflector_agent import run_reflector
from .types import ModelConfig, ReflectionConfig, ReflectorResult

logger = logging.getLogger(__name__)


class ReflectorRunner:
    """
    Runs the Reflector agent for compressing observations.
    Handles escalating compression levels and retry logic.
    """
    
    def __init__(
        self,
        reflection_config: ReflectionConfig,
        llm_call_fn: Callable[[str, list[dict], float, int], Coroutine[None, None, str]],
        count_tokens_fn: Callable[[str], int],
    ):
        self.reflection_config = reflection_config
        self.llm_call_fn = llm_call_fn
        self.count_tokens_fn = count_tokens_fn
        
        # Resolve target threshold
        if isinstance(self.reflection_config.token_threshold, int):
            self.target_threshold = self.reflection_config.token_threshold
        else:
            self.target_threshold = self.reflection_config.token_threshold.max

    async def call(
        self,
        observations: str,
        manual_prompt: Optional[str] = None,
        compression_start_level: int = 0,
        observation_tokens_threshold: Optional[int] = None,
    ) -> ReflectorResult:
        target_threshold = observation_tokens_threshold or self.target_threshold
        return await run_reflector(
            model_config=self.reflection_config.model,
            observations=observations,
            current_task=None,
            target_threshold=target_threshold,
            count_tokens_fn=self.count_tokens_fn,
            llm_call_fn=self.llm_call_fn,
            instruction=manual_prompt or self.reflection_config.instruction,
            max_compression_levels=4,
        )

    async def do_async_buffered_reflection(
        self,
        record_id: str,
        observations: str,
        storage, # ObservationalMemoryStorage
        observation_tokens_threshold: Optional[int] = None,
    ) -> None:
        """
        Slice a piece off the oldest observations and reflect them in the background.
        """
        import asyncio
        lines = observations.split("\n")
        # Take the top half of lines for reflection (oldest)
        lines_to_reflect = lines[:len(lines)//2]

        if not lines_to_reflect:
            return

        text_to_reflect = "\n".join(lines_to_reflect)
        input_tokens = self.count_tokens_fn(text_to_reflect)
        
        try:
            result = await self.call(
                observations=text_to_reflect,
                observation_tokens_threshold=observation_tokens_threshold,
                compression_start_level=1
            )
            
            await storage.update_buffered_reflection(
                record_id=record_id,
                reflection=result.reflections,
                token_count=self.count_tokens_fn(result.reflections),
                input_token_count=input_tokens,
                reflected_observation_line_count=len(lines_to_reflect)
            )
        except Exception as e:
            logger.error(f"[OM:ReflectorRunner] Background reflection failed: {e}")
        finally:
            await storage.set_buffering_reflection_flag(record_id, False)
