"""
Observer Runner: manages the execution lifecycle of the Observer agent.
Handles degenerate detection retry logic, and tracking observed messages.

Mirrors: packages/memory/src/processors/observational-memory/observer-runner.ts
"""

import logging
from typing import Callable, Coroutine, Optional

from .observer_agent import (
    build_observer_prompt,
    build_observer_system_prompt,
    run_observer,
)
from .types import Message, ModelConfig, ObservationConfig, ObserverResult

logger = logging.getLogger(__name__)


class ObserverRunner:
    """
    Runs the Observer agent for extracting observations from messages.
    Handles degenerate detection and retry logic.
    """
    
    def __init__(
        self,
        observation_config: ObservationConfig,
        observed_message_ids: set[str],
        llm_call_fn: Callable[[str, list[dict], float, int], Coroutine[None, None, str]],
    ):
        self.observation_config = observation_config
        self.observed_message_ids = observed_message_ids
        self.llm_call_fn = llm_call_fn
        self.last_exchange = None

    async def call(
        self,
        existing_observations: Optional[str],
        messages_to_observe: list[Message],
        prior_current_task: Optional[str] = None,
        prior_suggested_response: Optional[str] = None,
        timezone: str = "UTC",
    ) -> ObserverResult:
        """
        Call the Observer agent for a single thread.
        """
        system_prompt = build_observer_system_prompt(
            multi_thread=False,
            instruction=self.observation_config.instruction,
        )
        
        user_prompt = build_observer_prompt(
            existing_observations=existing_observations,
            messages=messages_to_observe,
            timezone=timezone,
            current_task=prior_current_task,
            previous_response_hint=prior_suggested_response,
        )

        # Mark messages as observed immediately
        for msg in messages_to_observe:
            self.observed_message_ids.add(msg.id)

        try:
            result = await run_observer(
                model_config=self.observation_config.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                llm_call_fn=self.llm_call_fn
            )
            
            self.last_exchange = {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "parsed_result": result,
                "is_multi_thread": False
            }
            
            return result
        except Exception as e:
            logger.error(f"[OM:ObserverRunner] Failed to observe messages: {e}")
            raise
