"""Lua REPL executor for AgentStage.

ReAct loop where the action is always a Lua script. Instead of choosing
one tool per step with JSON params, the LLM writes Lua code that can
call multiple tools, use loops, variables, and functions. The Lua
runtime state (variables, functions) persists across steps.

Intelligence modules (all optional, activated when a browser session is present):
- SecretManager: masks/unmasks credentials so the LLM only sees placeholders.
- MemoryManager: long-term fact storage (persists across steps via save_fact tool).
- MemoryReducer: compresses step history when it grows too large.
- ActionTracker: detects loops, forces corrective actions.
- ActionIntelligence: learns success/failure patterns per page and action.
- BFSExplorationStrategy: tracks visited page states, suggests unexplored elements.
"""

import pathlib
import re
from typing import Any, Callable, Dict, List, Optional

from abstra_internals.controllers.sdk.sdk_ai import AiSDKController
from abstra_internals.entities.agents.action_intelligence import ActionIntelligence
from abstra_internals.entities.agents.action_tracker import ActionTracker
from abstra_internals.entities.agents.controller import AgentExecutionResult
from abstra_internals.entities.agents.exploration_strategy import (
    BFSExplorationStrategy,
)
from abstra_internals.entities.agents.lua.prompt_builder import (
    LuaPromptBuilder,
    LuaPromptBuilderProtocol,
    LuaStep,
    build_tool_descriptions,
)
from abstra_internals.entities.agents.lua.runtime import ScriptRuntime
from abstra_internals.entities.agents.lua.tool_adapter import (
    LuaToolAdapter,
    ToolAdapter,
)
from abstra_internals.entities.agents.memory_manager import (
    MemoryManager,
    MemoryReducer,
)
from abstra_internals.entities.agents.secret_manager import SecretManager
from abstra_internals.entities.agents.tools.browser_session import BrowserSession
from abstra_internals.entities.agents.tools.dispatcher import ToolHandler
from abstra_internals.entities.agents.tools.send_task_handler import SendTaskHandler
from abstra_internals.repositories.project.project import AgentPermission

MAX_OUTPUT_LEN = 10_000
MAX_FINISH_REJECTIONS = 3
MAX_FORCE_FINISH_REPEATS = 5

ACTION_EXECUTE = "execute"
ACTION_FINISH_SUCCESS = "finish_success"
ACTION_FINISH_FAILURE = "finish_failure"
VALID_ACTIONS = {ACTION_EXECUTE, ACTION_FINISH_SUCCESS, ACTION_FINISH_FAILURE}

STEP_FORMAT = {
    "thought": {
        "type": "string",
        "description": "Brief reasoning about what to do next.",
    },
    "action": {
        "type": "string",
        "description": (
            "One of: 'execute' (run Lua code), "
            "'finish_success' (task completed), "
            "'finish_failure' (cannot complete task)."
        ),
    },
    "argument": {
        "type": "string",
        "description": (
            "When action='execute': Lua code to run. "
            "When action='finish_success' or 'finish_failure': summary message."
        ),
    },
}


def lua_safe_name(name: str) -> str:
    """Convert a tool name to a valid Lua identifier (replace hyphens with underscores)."""
    return name.replace("-", "_")


class LuaExecutor:
    """ReAct executor where every action is a Lua script.

    The LLM chooses one of three actions each step:
    - execute: run a Lua script, get stdout as observation
    - finish_success: task completed
    - finish_failure: task cannot be completed

    Tools are registered as Lua functions in the runtime. The runtime
    state (variables, functions) persists across steps.
    """

    def __init__(
        self,
        ai_sdk: AiSDKController,
        tool_handlers: List[ToolHandler],
        runtime: ScriptRuntime,
        tool_adapter: Optional[ToolAdapter] = None,
        prompt_builder: Optional[LuaPromptBuilderProtocol] = None,
        max_steps: int = 30,
        screenshot_fn: Optional[Callable[[], Optional[str]]] = None,
        secret_manager: Optional[SecretManager] = None,
        memory_manager: Optional[MemoryManager] = None,
        memory_reducer: Optional[MemoryReducer] = None,
        action_tracker: Optional[ActionTracker] = None,
        action_intelligence: Optional[ActionIntelligence] = None,
        exploration_strategy: Optional[BFSExplorationStrategy] = None,
        browser_session: Optional[BrowserSession] = None,
    ) -> None:
        self._ai_sdk = ai_sdk
        self._runtime = runtime
        if tool_adapter is None:
            log_fn = getattr(runtime, "log_output", None)
            tool_adapter = LuaToolAdapter(log_fn=log_fn)
        self._tool_adapter = tool_adapter
        self._prompt_builder = prompt_builder or LuaPromptBuilder()
        self._max_steps = max_steps
        self._screenshot_fn = screenshot_fn
        self._tool_handlers = tool_handlers
        self._send_task_handlers: List[SendTaskHandler] = []
        self._finish_rejection_count = 0
        self._secret_manager = secret_manager
        self._memory_manager = memory_manager
        self._memory_reducer = memory_reducer
        self._action_tracker = action_tracker
        self._action_intelligence = action_intelligence
        self._exploration_strategy = exploration_strategy
        self._browser_session = browser_session

        self._register_tools(tool_handlers)

    def _register_tools(self, handlers: List[ToolHandler]) -> None:
        """Register tool handlers as Lua functions in the runtime."""
        for handler in handlers:
            if handler.name == "finish":
                continue
            if isinstance(handler, SendTaskHandler):
                self._send_task_handlers.append(handler)
            adapted = self._tool_adapter.adapt(handler)
            safe_name = lua_safe_name(handler.name)
            self._runtime.register_function(safe_name, adapted)

    def execute(
        self,
        prompt: str,
        permissions: List[AgentPermission],
        **kwargs: Any,
    ) -> AgentExecutionResult:
        """Run the ReAct loop: think -> execute Lua or finish -> observe."""
        steps: List[LuaStep] = []
        self._finish_rejection_count = 0
        self._base_dir = kwargs.get("base_dir")

        # Load secrets from environment if a secret manager is available
        if self._secret_manager:
            count = self._secret_manager.load_secrets()
            if count:
                print(f"[AGENT] Loaded {count} secret(s)")

        try:
            tool_descriptions = build_tool_descriptions(self._tool_handlers)
            secrets_context = (
                self._secret_manager.get_secrets_for_prompt()
                if self._secret_manager
                else ""
            )
            system_prompt = self._prompt_builder.build_system_prompt(
                tool_descriptions, secrets_context=secrets_context
            )

            tool_names = [
                lua_safe_name(h.name) for h in self._tool_handlers if h.name != "finish"
            ]
            print(
                f"[AGENT] Registered {len(tool_names)} tool(s): {', '.join(tool_names)}"
            )

            for step_num in range(1, self._max_steps + 1):
                # --- Pre-think: check for forced actions ---
                forced_step = self._check_forced_actions(step_num)
                if forced_step:
                    step = forced_step
                    steps.append(step)
                    # Execute the forced Lua code
                    if step.action == ACTION_EXECUTE and step.code.strip():
                        output = self._runtime.execute(step.code)
                        if len(output) > MAX_OUTPUT_LEN:
                            output = (
                                output[:MAX_OUTPUT_LEN]
                                + f"\n... (truncated, {len(output)} chars total)"
                            )
                        step.output = output
                        if self._secret_manager:
                            step.output = self._secret_manager.mask(step.output)
                        print(f"[AGENT] Forced action output: {step.output}")
                        self._record_action(step)
                    elif step.action == ACTION_FINISH_FAILURE:
                        return AgentExecutionResult(
                            success=False,
                            output="",
                            tasks_to_send=self._collect_sent_tasks(),
                            error=step.code or "Agent stuck in loop.",
                        )
                    continue

                # Build dynamic context for the prompt
                dynamic_context = self._build_dynamic_context()
                memory_summary = (
                    self._memory_reducer.summary if self._memory_reducer else ""
                )
                step = self._think(
                    prompt,
                    steps,
                    system_prompt,
                    step_num,
                    dynamic_context,
                    memory_summary,
                )
                steps.append(step)

                print(
                    f"[AGENT] Step {step_num}: "
                    f"thought={step.thought!r}, "
                    f"action={step.action}"
                )

                # --- finish_success ---
                if step.action == ACTION_FINISH_SUCCESS:
                    if self._has_pending_send_tasks():
                        self._finish_rejection_count += 1
                        if self._finish_rejection_count > MAX_FINISH_REJECTIONS:
                            print(
                                f"[AGENT] Finish forced after {MAX_FINISH_REJECTIONS} rejections"
                            )
                        else:
                            pending_names = [
                                lua_safe_name(h.name)
                                for h in self._send_task_handlers
                                if not h.get_sent_tasks()
                            ]
                            step.output = (
                                f"Error: you must call these functions before finishing: "
                                f"{', '.join(pending_names)}. "
                                f'Example: {pending_names[0]}({{field1 = "value1"}})'
                            )
                            step.action = ACTION_EXECUTE
                            print(
                                f"[AGENT] Finish rejected ({self._finish_rejection_count}/{MAX_FINISH_REJECTIONS}): pending {pending_names}"
                            )
                            continue

                    print(f"[AGENT] Finished (success): {step.code}")
                    return AgentExecutionResult(
                        success=True,
                        output=step.code,
                        tasks_to_send=self._collect_sent_tasks(),
                    )

                # --- finish_failure ---
                if step.action == ACTION_FINISH_FAILURE:
                    print(f"[AGENT] Finished (failure): {step.code}")
                    return AgentExecutionResult(
                        success=False,
                        output="",
                        tasks_to_send=self._collect_sent_tasks(),
                        error=step.code or "Agent reported failure.",
                    )

                # --- execute ---
                if not step.code.strip():
                    step.output = (
                        "Error: empty code. Write a Lua script that calls "
                        "the available functions."
                    )
                    print(f"[AGENT] Output: {step.output}")
                    continue

                # Unmask secrets in the Lua code before execution
                code_to_run = step.code
                if self._secret_manager:
                    code_to_run = self._secret_manager.unmask(code_to_run)

                output = self._runtime.execute(code_to_run)
                if len(output) > MAX_OUTPUT_LEN:
                    output = (
                        output[:MAX_OUTPUT_LEN]
                        + f"\n... (truncated, {len(output)} chars total)"
                    )

                # Mask secrets in the output
                if self._secret_manager:
                    output = self._secret_manager.mask(output)

                step.output = output
                print(f"[AGENT] Output: {output}")

                # Record action in intelligence modules
                self._record_action(step)

                # Take screenshot after executing code (if browser is active)
                if self._screenshot_fn:
                    try:
                        screenshot_path = self._screenshot_fn()
                        if screenshot_path:
                            step.screenshot = pathlib.Path(screenshot_path)
                            print(f"[AGENT] Screenshot: {screenshot_path}")
                    except Exception:
                        pass

            else:
                error = (
                    f"Agent reached maximum number of steps ({self._max_steps}) "
                    f"without completing the task."
                )
                print(f"[AGENT] {error}")
                return AgentExecutionResult(
                    success=False,
                    output="",
                    tasks_to_send=self._collect_sent_tasks(),
                    error=error,
                )

        except Exception as e:
            return AgentExecutionResult(
                success=False,
                output="",
                tasks_to_send=self._collect_sent_tasks(),
                error=f"Agent execution error: {str(e)}",
            )

    def _think(
        self,
        prompt: str,
        history: List[LuaStep],
        system_prompt: str,
        step_number: int,
        dynamic_context: str = "",
        memory_summary: str = "",
    ) -> LuaStep:
        """Call the LLM to get the next action."""
        step_prompts = self._prompt_builder.build_step_prompt(
            rendered_template=prompt,
            history=history,
            base_dir=self._base_dir,
            dynamic_context=dynamic_context,
            memory_summary=memory_summary,
        )

        response = self._ai_sdk.prompt(
            prompts=step_prompts,  # type: ignore[arg-type]
            instructions=[system_prompt],
            format=STEP_FORMAT,  # type: ignore[arg-type]
            temperature=0.2,
        )

        if not isinstance(response, dict):
            raise ValueError(
                f"Expected structured response from prompt SDK, got: {type(response)}"
            )

        thought = response.get("thought", "")
        action = response.get("action", ACTION_EXECUTE)
        argument = response.get("argument", "")

        if not isinstance(argument, str):
            argument = str(argument) if argument else ""

        if action not in VALID_ACTIONS:
            action = ACTION_EXECUTE

        return LuaStep(
            step_number=step_number,
            thought=thought,
            action=action,
            code=argument,
        )

    def _check_forced_actions(self, step_number: int) -> Optional[LuaStep]:
        """Check if any intelligence module wants to force a specific action.

        Returns a pre-built LuaStep if an action should be forced, or None
        to proceed with normal LLM-driven thinking.
        """
        if not self._action_tracker:
            return None

        # Force wait_for_download if download buttons were clicked but never waited
        should_force, reason = self._action_tracker.should_force_wait_for_download()
        if should_force:
            print(f"[AGENT] Forcing wait_for_download: {reason}")
            return LuaStep(
                step_number=step_number,
                thought=f"Forced action: {reason}",
                action=ACTION_EXECUTE,
                code="local result = wait_for_download({timeout = 30})\nprint(result)",
            )

        # Force finish if stuck in a deep loop (consecutive repeats)
        if self._action_tracker.consecutive_repeats >= MAX_FORCE_FINISH_REPEATS:
            print(
                f"[AGENT] Forcing finish: {self._action_tracker.consecutive_repeats} "
                f"consecutive repeats of same action"
            )
            return LuaStep(
                step_number=step_number,
                thought="Forcing finish due to persistent action loop.",
                action=ACTION_FINISH_FAILURE,
                code="Task could not be completed: stuck in action loop.",
            )

        return None

    def _build_dynamic_context(self) -> str:
        """Assemble dynamic context from all intelligence modules."""
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

    def _get_element_count(self) -> int:
        if self._browser_session and self._browser_session.is_started:
            return self._browser_session.get_element_count()
        return 0

    def _record_action(self, step: LuaStep) -> None:
        """Record the completed action in all intelligence modules."""
        primary_action = self._extract_primary_action(step.code)
        action_input_str = step.code[:200]

        # Update memory reducer
        if self._memory_reducer:
            self._memory_reducer.update(
                step=step.step_number,
                action=primary_action,
                action_input=action_input_str,
                observation=step.output,
            )

        # Determine success
        success = True
        if self._action_intelligence:
            success = self._action_intelligence.was_action_successful(
                step.output, primary_action
            )

        # Record in action tracker
        if self._action_tracker:
            self._action_tracker.record_action(
                action=primary_action,
                action_input=action_input_str,
                outcome=step.output,
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
                action=primary_action,
                action_input=action_input_str,
                page_signature=page_signature,
                success=success,
                observation=step.output,
                step_number=step.step_number,
            )

        # Record in exploration strategy using actual current page URL
        if self._exploration_strategy and primary_action in (
            "navigate",
            "click",
            "press_key",
        ):
            current_url = self._get_current_url() or "lua_execution"
            element_count = self._get_element_count()
            state = self._exploration_strategy.record_state(
                url=current_url, element_count=element_count
            )
            self._exploration_strategy.record_action(
                state=state,
                action=primary_action,
                action_input=action_input_str,
            )

    _LUA_BUILTINS = frozenset(
        {
            "print",
            "pcall",
            "tostring",
            "tonumber",
            "type",
            "pairs",
            "ipairs",
            "string",
            "table",
            "math",
            "error",
            "assert",
            "select",
            "unpack",
            "rawget",
            "rawset",
            "setmetatable",
            "getmetatable",
        }
    )

    @staticmethod
    def _extract_primary_action(code: str) -> str:
        """Extract the primary tool function name from Lua code.

        Looks for the first function call pattern like `navigate(`, `click(`, etc.
        Falls back to 'execute' if no known tool call is found.
        """
        match = re.search(r"\b([a-z_]+)\s*\(", code)
        if match:
            name = match.group(1)
            if name not in LuaExecutor._LUA_BUILTINS:
                return name
        return "execute"

    def _has_pending_send_tasks(self) -> bool:
        """Check if there are send_task handlers that haven't sent anything."""
        for handler in self._send_task_handlers:
            if not handler.get_sent_tasks():
                return True
        return False

    def _collect_sent_tasks(self) -> List[Dict[str, Any]]:
        """Collect all tasks sent via send_task_* handlers."""
        sent_tasks: List[Dict[str, Any]] = []
        for handler in self._send_task_handlers:
            sent_tasks.extend(handler.get_sent_tasks())
        return sent_tasks
