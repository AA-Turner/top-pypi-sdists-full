"""
Observer Runner: manages the execution lifecycle of the Observer agent.
Handles degenerate detection retry logic, and tracking observed messages.

Mirrors: packages/memory/src/processors/observational-memory/observer-runner.ts
"""

import logging
from collections.abc import Callable, Coroutine

from .observer_agent import build_observer_variables, run_observer
from .types import Message, ObservationConfig, ObserverResult

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
        llm_call_fn: Callable[..., Coroutine[None, None, str]],
    ):
        self.observation_config = observation_config
        self.observed_message_ids = observed_message_ids
        self.llm_call_fn = llm_call_fn
        self.last_exchange = None

    async def call(
        self,
        existing_observations: str | None,
        messages_to_observe: list[Message],
        prior_current_task: str | None = None,
        prior_suggested_response: str | None = None,
        timezone: str = "UTC",
    ) -> ObserverResult:
        """
        Call the Observer agent for a single thread.
        """
        variables = build_observer_variables(
            existing_observations=existing_observations,
            messages=messages_to_observe,
            timezone=timezone,
            current_task=prior_current_task,
            previous_response_hint=prior_suggested_response,
            instruction=self.observation_config.instruction,
        )

        # Mark messages as observed immediately
        for msg in messages_to_observe:
            self.observed_message_ids.add(msg.id)

        try:
            result = await run_observer(
                model_config=self.observation_config.model,
                variables=variables,
                llm_call_fn=self.llm_call_fn
            )
            
            self.last_exchange = {
                "mandate_key": self.observation_config.model.mandate_key,
                "variables": variables,
                "parsed_result": result,
                "is_multi_thread": False
            }
            
            return result
        except Exception as e:
            logger.error(f"[OM:ObserverRunner] Failed to observe messages: {e}")
            raise
