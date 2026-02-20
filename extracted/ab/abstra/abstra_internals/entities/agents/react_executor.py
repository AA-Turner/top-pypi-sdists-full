"""ReAct loop executor for AgentStage.

Implements a text-based ReAct (Reasoning + Acting) pattern using
the prompt SDK's format parameter for structured output extraction.
Each iteration: think (LLM call) -> act (tool dispatch) -> observe.

Intelligence modules (all optional, activated when a browser session is present):
- SecretManager: masks/unmasks credentials so the LLM only sees placeholders.
- MemoryManager: long-term fact storage (persists across steps via save_fact tool).
- MemoryReducer: compresses step history when it grows too large.
- ActionTracker: detects loops, forces corrective actions.
- ActionIntelligence: learns success/failure patterns per page and action.
- BFSExplorationStrategy: tracks visited page states, suggests unexplored elements.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from abstra_internals.controllers.sdk.sdk_ai import AiSDKController
from abstra_internals.entities.agents.action_intelligence import ActionIntelligence
from abstra_internals.entities.agents.action_tracker import ActionTracker
from abstra_internals.entities.agents.controller import AgentExecutionResult
from abstra_internals.entities.agents.exploration_strategy import (
    BFSExplorationStrategy,
)
from abstra_internals.entities.agents.memory_manager import (
    MemoryManager,
    MemoryReducer,
)
from abstra_internals.entities.agents.prompt_builder import (
    AgentPromptBuilder,
    ReActStep,
)
from abstra_internals.entities.agents.secret_manager import SecretManager
from abstra_internals.entities.agents.tools.browser_session import BrowserSession
from abstra_internals.entities.agents.tools.dispatcher import ToolDispatcher
from abstra_internals.entities.agents.tools.send_task_handler import SendTaskHandler
from abstra_internals.repositories.project.project import AgentPermission

MAX_LOG_LEN = 500
MAX_FORCE_FINISH_REPEATS = 5


def _truncate(text: str, limit: int = MAX_LOG_LEN) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"... ({len(text)} chars total)"


REACT_FORMAT = {
    "thought": {
        "type": "string",
        "description": "Your reasoning about what to do next.",
    },
    "action": {
        "type": "string",
        "description": "The name of the tool to use, or 'finish' to complete the task.",
    },
    "action_input": {
        "type": "object",
        "description": "The input parameters for the chosen tool.",
        "additionalProperties": True,
    },
}


@dataclass
class ReActState:
    """State maintained across the ReAct loop."""

    prompt: str
    steps: List[ReActStep] = field(default_factory=list)
    result: Optional[str] = None
    error: Optional[str] = None


class ReActExecutor:
    """Executes an agent using the ReAct pattern with the prompt SDK."""

    def __init__(
        self,
        ai_sdk: AiSDKController,
        tool_dispatcher: ToolDispatcher,
        prompt_builder: Optional[AgentPromptBuilder] = None,
        max_steps: int = 30,
        secret_manager: Optional[SecretManager] = None,
        memory_manager: Optional[MemoryManager] = None,
        memory_reducer: Optional[MemoryReducer] = None,
        action_tracker: Optional[ActionTracker] = None,
        action_intelligence: Optional[ActionIntelligence] = None,
        exploration_strategy: Optional[BFSExplorationStrategy] = None,
        browser_session: Optional[BrowserSession] = None,
    ) -> None:
        self._ai_sdk = ai_sdk
        self._tool_dispatcher = tool_dispatcher
        self._prompt_builder = prompt_builder or AgentPromptBuilder()
        self._max_steps = max_steps
        self._secret_manager = secret_manager
        self._memory_manager = memory_manager
        self._memory_reducer = memory_reducer
        self._action_tracker = action_tracker
        self._action_intelligence = action_intelligence
        self._exploration_strategy = exploration_strategy
        self._browser_session = browser_session

    def execute(
        self,
        prompt: str,
        permissions: List[AgentPermission],
        **kwargs: Any,
    ) -> AgentExecutionResult:
        state = ReActState(prompt=prompt)
        self._base_dir = kwargs.get("base_dir")

        # Load secrets from environment if a secret manager is available
        if self._secret_manager:
            count = self._secret_manager.load_secrets()
            if count:
                print(f"[AGENT] Loaded {count} secret(s)")

        try:
            tool_descriptions = self._tool_dispatcher.get_tool_descriptions()
            secrets_context = (
                self._secret_manager.get_secrets_for_prompt()
                if self._secret_manager
                else ""
            )
            system_prompt = self._prompt_builder.build_system_prompt(
                tool_descriptions, secrets_context=secrets_context
            )

            for step_num in range(1, self._max_steps + 1):
                # --- Pre-think: check for forced actions ---
                forced_step = self._check_forced_actions(step_num)
                if forced_step:
                    step = forced_step
                else:
                    # Build dynamic context for the prompt
                    dynamic_context = self._build_dynamic_context()
                    memory_summary = (
                        self._memory_reducer.summary if self._memory_reducer else ""
                    )
                    step = self._think(
                        state, system_prompt, step_num, dynamic_context, memory_summary
                    )

                state.steps.append(step)

                action_input_str = json.dumps(step.action_input, ensure_ascii=False)
                print(
                    f"[AGENT] Step {step_num}: "
                    f"thought={_truncate(step.thought)!r}, "
                    f"action={step.action}, "
                    f"action_input={_truncate(action_input_str)}"
                )

                if step.action == "finish":
                    # Check if agent has send_task tools but hasn't used any
                    if self._has_pending_send_tasks():
                        warning = (
                            "You have send_task tools available but have not "
                            "used any of them yet. You MUST send tasks to the "
                            "next stage before finishing. Check your available "
                            "tools for send_task_* and use them now."
                        )
                        step.observation = warning
                        print("[AGENT] Finish rejected: pending send_task tools")
                        continue

                    state.result = (
                        step.action_input.get("answer", "Task completed.")
                        or "Task completed."
                    )
                    print(f"[AGENT] Finished: {_truncate(state.result or '')}")
                    break

                # --- Pre-act: capture element metadata before dispatch
                # (dispatch may cause navigation, which overwrites cached elements) ---
                pre_element_text = ""
                pre_element_type = None
                if step.action == "click" and "index" in step.action_input:
                    click_index = int(step.action_input["index"])
                    pre_element_text = self._get_element_text(click_index)
                    if self._browser_session and self._browser_session.is_started:
                        elem = self._browser_session.get_element_by_index(click_index)
                        if elem:
                            pre_element_type = elem.get("tag")

                # --- Act: unmask secrets, dispatch, mask observation ---
                action_input = step.action_input
                if self._secret_manager:
                    action_input = self._secret_manager.unmask_dict(action_input)

                observation = self._tool_dispatcher.dispatch(step.action, action_input)

                if self._secret_manager:
                    observation = self._secret_manager.mask(observation)

                step.observation = observation
                print(f"[AGENT] Observation: {_truncate(observation)}")

                # --- Post-act: record in intelligence modules ---
                self._record_action(
                    step,
                    pre_element_text=pre_element_text,
                    pre_element_type=pre_element_type,
                )

            else:
                state.error = (
                    f"Agent reached maximum number of steps ({self._max_steps}) "
                    f"without completing the task."
                )
                print(f"[AGENT] {state.error}")

            sent_tasks = self._collect_sent_tasks()

            return AgentExecutionResult(
                success=state.error is None,
                output=state.result or "",
                tasks_to_send=sent_tasks,
                error=state.error,
            )

        except Exception as e:
            return AgentExecutionResult(
                success=False,
                output="",
                error=f"Agent execution error: {str(e)}",
            )

    def _think(
        self,
        state: ReActState,
        system_prompt: str,
        step_number: int,
        dynamic_context: str = "",
        memory_summary: str = "",
    ) -> ReActStep:
        step_prompts = self._prompt_builder.build_step_prompt(
            rendered_template=state.prompt,
            history=state.steps,
            base_dir=self._base_dir,
            dynamic_context=dynamic_context,
            memory_summary=memory_summary,
        )

        response = self._ai_sdk.prompt(
            prompts=step_prompts,  # type: ignore[arg-type]
            instructions=[system_prompt],
            format=REACT_FORMAT,  # type: ignore[arg-type]
            temperature=0.0,
        )

        if not isinstance(response, dict):
            raise ValueError(
                f"Expected structured response from prompt SDK, got: {type(response)}"
            )

        thought = response.get("thought", "")
        action = response.get("action", "finish")
        action_input = response.get("action_input", {})

        if not isinstance(action_input, dict):
            try:
                action_input = json.loads(str(action_input))
            except (json.JSONDecodeError, TypeError):
                action_input = {}

        return ReActStep(
            step_number=step_number,
            thought=thought,
            action=action,
            action_input=action_input,
        )

    def _check_forced_actions(self, step_number: int) -> Optional[ReActStep]:
        """Check if any intelligence module wants to force a specific action.

        Returns a pre-built ReActStep if an action should be forced, or None
        to proceed with normal LLM-driven thinking.
        """
        if not self._action_tracker:
            return None

        # Force wait_for_download if download buttons were clicked but never waited
        should_force, reason = self._action_tracker.should_force_wait_for_download()
        if should_force:
            print(f"[AGENT] Forcing wait_for_download: {reason}")
            return ReActStep(
                step_number=step_number,
                thought=f"Forced action: {reason}",
                action="wait_for_download",
                action_input={"timeout": 30},
            )

        # Force finish if stuck in a deep loop (consecutive repeats)
        if self._action_tracker.consecutive_repeats >= MAX_FORCE_FINISH_REPEATS:
            print(
                f"[AGENT] Forcing finish: {self._action_tracker.consecutive_repeats} "
                f"consecutive repeats of same action"
            )
            return ReActStep(
                step_number=step_number,
                thought="Forcing finish due to persistent action loop.",
                action="finish",
                action_input={
                    "answer": "Task could not be completed: stuck in action loop."
                },
            )

        return None

    def _build_dynamic_context(self) -> str:
        """Assemble dynamic context from all intelligence modules.

        This context is injected into the step prompt so the LLM can make
        better decisions based on action history, loop detection, memory,
        and exploration state.
        """
        parts: List[str] = []

        if self._memory_manager:
            facts_ctx = self._memory_manager.get_facts_context()
            if facts_ctx:
                parts.append(facts_ctx)

        if self._action_intelligence:
            intel_ctx = self._action_intelligence.get_context_for_prompt()
            if intel_ctx:
                parts.append(intel_ctx)

        if self._action_tracker:
            tracker_ctx = self._action_tracker.get_context_for_prompt()
            if tracker_ctx:
                parts.append(tracker_ctx)

        if self._exploration_strategy:
            summary = self._exploration_strategy.get_exploration_summary()
            if self._exploration_strategy.should_try_alternative_approach():
                parts.append(
                    f"\n## Exploration Status\n{summary}\n"
                    f"WARNING: Consider trying a completely different approach."
                )
            elif self._exploration_strategy.action_history:
                parts.append(f"\n## Exploration Status\n{summary}")

        return "\n".join(parts)

    def _get_current_url(self) -> str:
        if self._browser_session and self._browser_session.is_started:
            return self._browser_session.get_current_url()
        return ""

    def _get_element_text(self, index: int) -> str:
        if self._browser_session and self._browser_session.is_started:
            return self._browser_session.get_element_text_by_index(index)
        return ""

    def _get_element_count(self) -> int:
        if self._browser_session and self._browser_session.is_started:
            return self._browser_session.get_element_count()
        return 0

    def _record_action(
        self,
        step: ReActStep,
        pre_element_text: str = "",
        pre_element_type: Optional[str] = None,
    ) -> None:
        """Record the completed action in all intelligence modules.

        Args:
            step: The completed step to record.
            pre_element_text: Element text captured *before* dispatch (avoids
                stale indices after navigation overwrites cached elements).
            pre_element_type: Element tag captured *before* dispatch.
        """
        action_input_str = json.dumps(step.action_input, ensure_ascii=False)

        # Update memory reducer
        if self._memory_reducer:
            self._memory_reducer.update(
                step=step.step_number,
                action=step.action,
                action_input=action_input_str,
                observation=step.observation,
            )

        # Use pre-captured element metadata (captured before dispatch to avoid
        # stale indices after page navigation overwrites the element cache).
        element_text = pre_element_text
        element_type = pre_element_type

        # Determine success for action intelligence
        success = True
        if self._action_intelligence:
            success = self._action_intelligence.was_action_successful(
                step.observation, step.action
            )

        # Record in action tracker
        if self._action_tracker:
            self._action_tracker.record_action(
                action=step.action,
                action_input=action_input_str,
                outcome=step.observation,
                element_text=element_text,
            )

        # Compute page signature from actual browser state
        page_signature = ""
        if self._action_intelligence:
            current_url = self._get_current_url()
            element_count = self._get_element_count()
            if current_url:
                page_signature = self._action_intelligence.get_page_signature(
                    url=current_url,
                    element_count=element_count,
                )
            self._action_intelligence.record_outcome(
                action=step.action,
                action_input=action_input_str,
                page_signature=page_signature,
                success=success,
                observation=step.observation,
                element_type=element_type,
                step_number=step.step_number,
            )

        # Record in exploration strategy using the actual current page URL
        if self._exploration_strategy and step.action in (
            "navigate",
            "click",
            "press_key",
        ):
            current_url = self._get_current_url() or step.action_input.get(
                "url", "unknown"
            )
            element_count = self._get_element_count()
            self._exploration_strategy.record_action(
                state=self._exploration_strategy.record_state(
                    url=current_url,
                    element_count=element_count,
                ),
                action=step.action,
                action_input=action_input_str,
            )

    def _has_pending_send_tasks(self) -> bool:
        """Check if there are send_task handlers that haven't sent anything."""
        for handler in self._tool_dispatcher._handlers.values():
            if isinstance(handler, SendTaskHandler) and not handler.get_sent_tasks():
                return True
        return False

    def _collect_sent_tasks(self) -> List[Dict[str, Any]]:
        sent_tasks: List[Dict[str, Any]] = []
        for handler in self._tool_dispatcher._handlers.values():
            if isinstance(handler, SendTaskHandler):
                sent_tasks.extend(handler.get_sent_tasks())
        return sent_tasks
