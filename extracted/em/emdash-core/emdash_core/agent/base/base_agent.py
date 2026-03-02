"""Abstract base class for all agent types.

This module provides the BaseAgent abstract class that defines the core
agent loop, message management, and tool execution infrastructure.
Concrete agent types (CodingMainAgent, CoworkerAgent) inherit from this.
"""

import json
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional, TYPE_CHECKING

from ...utils.logger import log
from ...core.exceptions import ContextLengthError
from ...core.config import get_config
from ..events import AgentEventEmitter, NullEmitter
from ..providers import get_provider
from ..providers.factory import DEFAULT_MODEL, get_vision_provider, get_vision_model
from ..context_manager import (
    truncate_tool_output,
    reduce_context_for_retry,
    is_context_overflow_error,
)
from ..tools.base import ToolResult
from ..compaction_strategy import CompactionResult, CompactionStrategy, get_compaction_strategy

if TYPE_CHECKING:
    from ..toolkits.base import BaseToolkit


class SafeJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles non-serializable objects."""

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


def summarize_tool_result(result: ToolResult) -> str:
    """Create a brief summary of a tool result for logging/display."""
    if not result.success:
        return f"Error: {result.error or 'Unknown error'}"
    if result.data and isinstance(result.data, dict):
        # Try to create a meaningful summary
        if "content" in result.data:
            content = result.data["content"]
            if isinstance(content, str) and len(content) > 100:
                return f"{content[:100]}..."
            return str(content)[:200]
        if "files" in result.data:
            files = result.data["files"]
            if isinstance(files, list):
                return f"Found {len(files)} files"
        if "matches" in result.data:
            matches = result.data["matches"]
            if isinstance(matches, list):
                return f"Found {len(matches)} matches"
        if "message" in result.data:
            return str(result.data["message"])[:200]
    elif result.data:
        # Handle case where data is not a dict (shouldn't happen, but defensive)
        return str(result.data)[:200]
    return "Success"


class BaseAgent(ABC):
    """Abstract base class for all agent types.

    Provides core infrastructure:
    - LLM provider integration
    - Event emission framework
    - Message history management
    - Token usage tracking
    - Tool execution loop (sequential and parallel)
    - Context management and compaction
    - Vision provider switching

    Subclasses must implement:
    - _get_toolkit(): Return the appropriate toolkit for the agent type
    - _build_system_prompt(): Build the system prompt for the agent
    - _get_available_subagents(): Return dict of available sub-agent types

    Example:
        class CodingMainAgent(BaseAgent):
            def _get_toolkit(self) -> CodingToolkit:
                return CodingToolkit(repo_root=self.repo_root)

            def _build_system_prompt(self) -> str:
                return build_coding_prompt(self.toolkit)
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = int(os.getenv("EMDASH_MAX_ITERATIONS", "100")),
        verbose: bool = False,
        enable_thinking: Optional[bool] = None,
        session_id: Optional[str] = None,
    ):
        """Initialize the base agent.

        Args:
            model: LLM model to use.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            enable_thinking: Enable extended thinking. If None, auto-detect from model.
            session_id: Session ID for isolation.
        """
        self.model = model
        self.provider = get_provider(model)
        self.emitter = emitter or NullEmitter()
        self.max_iterations = max_iterations
        self.verbose = verbose

        # Get toolkit from subclass
        self.toolkit = self._get_toolkit()
        self.toolkit.set_emitter(self.emitter)

        # Build system prompt from subclass
        self.system_prompt = self._build_system_prompt()

        # Extended thinking support
        if enable_thinking is None:
            self.enable_thinking = (
                hasattr(self.provider, "supports_thinking")
                and self.provider.supports_thinking()
            )
        else:
            self.enable_thinking = enable_thinking

        # Conversation history for multi-turn support
        self._messages: list[dict] = []

        # Token usage tracking
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._total_thinking_tokens: int = 0

        # Store query for context
        self._current_query: str = ""

        # Session ID
        self._session_id = session_id

        # Thread pool for parallel tool execution
        config = get_config()
        self._tool_parallel_workers = config.agent.tool_parallel_workers
        self._tool_executor: Optional[ThreadPoolExecutor] = None

        # Vision provider (lazily initialized)
        self._vision_provider = None

        # Track consecutive malformed tool calls
        self._consecutive_malformed_iterations = 0

        # Flag for external compaction
        self._messages_compacted_externally = False

        # Compaction strategy (pluggable: llm_summary or observational_memory)
        self._compaction_strategy: CompactionStrategy = get_compaction_strategy(
            thread_id=session_id or "default"
        )

    # -------------------------------------------------------------------------
    # Abstract methods - subclasses must implement
    # -------------------------------------------------------------------------

    @abstractmethod
    def _get_toolkit(self) -> "BaseToolkit":
        """Return the toolkit appropriate for this agent type.

        Returns:
            BaseToolkit instance with registered tools
        """
        pass

    @abstractmethod
    def _build_system_prompt(self) -> str:
        """Build the system prompt for this agent type.

        Returns:
            System prompt string
        """
        pass

    @abstractmethod
    def _get_available_subagents(self) -> dict[str, str]:
        """Return dict of available sub-agent types.

        Returns:
            Dict mapping subagent_type name to description
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the display name for this agent (e.g., 'Emdash Code').

        Returns:
            Agent display name
        """
        pass

    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Return the agent type identifier (e.g., 'coding', 'coworker').

        Returns:
            Agent type string
        """
        pass

    # -------------------------------------------------------------------------
    # Optional hooks - subclasses can override
    # -------------------------------------------------------------------------

    def _on_tool_result(self, tool_name: str, result: ToolResult) -> None:
        """Hook called after each tool execution.

        Subclasses can override to handle specific tool results
        (e.g., checkpoint creation, mode changes).

        Args:
            tool_name: Name of the tool that was executed
            result: The tool result
        """
        pass

    def _on_run_complete(self, response: str) -> None:
        """Hook called when a run completes successfully.

        Args:
            response: The final response text
        """
        pass

    # -------------------------------------------------------------------------
    # Vision provider support
    # -------------------------------------------------------------------------

    def _get_vision_provider(self):
        """Get or create a vision-capable provider."""
        if self._vision_provider is None:
            self._vision_provider = get_vision_provider()
            log.info(
                "Created vision provider model={} for image support",
                get_vision_model(),
            )
        return self._vision_provider

    def _needs_vision_provider(self, images: Optional[list]) -> bool:
        """Check if we need to switch to vision provider."""
        if not images:
            return False
        if hasattr(self.provider, "supports_vision") and self.provider.supports_vision():
            return False
        return True

    # -------------------------------------------------------------------------
    # Thread pool management
    # -------------------------------------------------------------------------

    def _get_tool_executor(self) -> ThreadPoolExecutor:
        """Get the persistent thread pool executor, creating it if needed."""
        if self._tool_executor is None:
            self._tool_executor = ThreadPoolExecutor(
                max_workers=self._tool_parallel_workers,
                thread_name_prefix="tool-exec-"
            )
        return self._tool_executor

    def close(self) -> None:
        """Clean up resources, including the thread pool executor."""
        if self._tool_executor is not None:
            self._tool_executor.shutdown(wait=False)
            self._tool_executor = None

    def __enter__(self):
        """Support context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up on exit from context manager."""
        self.close()
        return False

    # -------------------------------------------------------------------------
    # Token tracking
    # -------------------------------------------------------------------------

    def get_token_usage(self) -> dict:
        """Get current token usage statistics.

        Returns:
            Dict with input, output, and thinking token counts
        """
        return {
            "input": self._total_input_tokens,
            "output": self._total_output_tokens,
            "thinking": self._total_thinking_tokens,
            "total": self._total_input_tokens + self._total_output_tokens,
        }

    # -------------------------------------------------------------------------
    # Core execution methods
    # -------------------------------------------------------------------------

    def run(
        self,
        query: str,
        context: Optional[str] = None,
        images: Optional[list] = None,
    ) -> str:
        """Run the agent to answer a query.

        Args:
            query: User's question or request
            context: Optional additional context
            images: Optional list of images to include

        Returns:
            Agent's final response
        """
        self._current_query = query

        # Switch to vision provider if needed
        original_provider = None
        if self._needs_vision_provider(images):
            original_provider = self.provider
            self.provider = self._get_vision_provider()
            vision_model = getattr(self.provider, 'model', 'vision-model')
            log.info("Switched to vision provider: {}", vision_model)
            self.emitter.emit_thinking(f"Processing image with vision model ({vision_model})...")

        # Build user message content
        if context:
            text_content = f"Context:\n{context}\n\nQuestion: {query}"
        else:
            text_content = query

        # Format content with images if provided
        if images:
            content = self.provider.format_content_with_images(text_content, images)
        else:
            content = text_content

        user_message = {"role": "user", "content": content}

        # Save to history before running
        self._messages.append(user_message)
        messages = list(self._messages)

        # Get tool schemas
        tools = self.toolkit.get_all_schemas()

        try:
            response, final_messages = self._run_loop(messages, tools)

            if not self._messages_compacted_externally:
                self._messages = final_messages
            else:
                self._messages_compacted_externally = False

            self.emitter.emit_end(success=True)
            self._on_run_complete(response)
            return response

        except TypeError as e:
            if "string indices must be integers" in str(e):
                log.error("DEBUG STRING INDEX ERROR in run(): {}", e)
                import traceback
                log.error("Traceback: {}", traceback.format_exc())
            raise

        except Exception as e:
            log.exception("Agent run failed")
            self.emitter.emit_error(str(e))
            return f"Error: {str(e)}"

        finally:
            if original_provider is not None:
                self.provider = original_provider

    def chat(self, message: str, images: Optional[list] = None) -> str:
        """Continue a conversation with a new message.

        Args:
            message: User's follow-up message
            images: Optional list of images to include

        Returns:
            Agent's response
        """
        if not self._messages:
            return self.run(message, images=images)

        self._current_query = message

        # Switch to vision provider if needed
        original_provider = None
        if self._needs_vision_provider(images):
            original_provider = self.provider
            self.provider = self._get_vision_provider()

        # Format content with images if provided
        if images:
            content = self.provider.format_content_with_images(message, images)
        else:
            content = message

        self._messages.append({"role": "user", "content": content})
        tools = self.toolkit.get_all_schemas()

        try:
            response, final_messages = self._run_loop(self._messages, tools)

            if not self._messages_compacted_externally:
                self._messages = final_messages
            else:
                self._messages_compacted_externally = False

            self.emitter.emit_end(success=True)
            self._on_run_complete(response)
            return response

        except Exception as e:
            log.exception("Agent chat failed")
            self.emitter.emit_error(str(e))
            return f"Error: {str(e)}"

        finally:
            if original_provider is not None:
                self.provider = original_provider

    def reset(self) -> None:
        """Reset the agent state."""
        self.toolkit.reset_session()
        self._messages = []
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._total_thinking_tokens = 0
        self._current_query = ""

    # -------------------------------------------------------------------------
    # Agent loop
    # -------------------------------------------------------------------------

    def _run_loop(
        self,
        messages: list[dict],
        tools: list[dict],
    ) -> tuple[str, list[dict]]:
        """Run the agent loop until completion.

        Args:
            messages: Initial messages
            tools: Tool schemas

        Returns:
            Tuple of (final response text, conversation messages)
        """
        from ..runner.context import maybe_compact_context

        max_retries = 3

        for iteration in range(self.max_iterations):
            # Warn when approaching limit
            if iteration == self.max_iterations - 2:
                messages.append({
                    "role": "user",
                    "content": "[SYSTEM: Approaching iteration limit. Please provide findings now.]",
                })

            # Try API call with retry on context overflow
            retry_count = 0
            response = None

            while retry_count < max_retries:
                try:
                    compaction_result = maybe_compact_context(
                        messages, self.provider, self.emitter, self.system_prompt,
                        toolkit=self.toolkit,
                        strategy=self._compaction_strategy,
                        thread_id=self._session_id,
                    )

                    # Unpack CompactionResult
                    if isinstance(compaction_result, CompactionResult):
                        messages = compaction_result.messages
                        _system_override = compaction_result.system_prompt
                    else:
                        messages = compaction_result
                        _system_override = None

                    log.debug(
                        "Calling LLM iteration={} messages={} tools={}",
                        iteration, len(messages), len(tools) if tools else 0,
                    )

                    # Build dynamic system prompt
                    dynamic_system = _system_override or self.system_prompt
                    files_read = self.toolkit.get_files_read()
                    if files_read:
                        files_list = ", ".join(files_read[-20:])
                        dynamic_system += f"\n\n## Files Already Read\n{files_list}"

                    response = self.provider.chat(
                        messages=messages,
                        system=dynamic_system,
                        tools=tools,
                        thinking=self.enable_thinking,
                    )
                    break

                except Exception as exc:
                    if is_context_overflow_error(exc):
                        retry_count += 1
                        log.warning(
                            "Context overflow attempt {}/{}", retry_count, max_retries
                        )
                        if retry_count >= max_retries:
                            raise ContextLengthError(
                                f"Failed to reduce context after {max_retries} attempts"
                            )
                        messages = reduce_context_for_retry(
                            messages, keep_recent=max(2, 6 - retry_count * 2)
                        )
                    else:
                        raise

            if response is None:
                raise RuntimeError("Failed to get response from provider")

            # Track tokens
            self._total_input_tokens += response.input_tokens
            self._total_output_tokens += response.output_tokens
            self._total_thinking_tokens += getattr(response, "thinking_tokens", 0)

            # Emit thinking if present
            if response.thinking:
                self.emitter.emit_thinking(response.thinking)

            # Handle tool calls
            if response.tool_calls:
                if response.content and response.content.strip():
                    self.emitter.emit_assistant_text(response.content)

                result = self._handle_tool_calls(response, messages, tools)
                if result is not None:
                    # Agent needs to pause (clarification, plan submitted, etc.)
                    return result

            else:
                # No tool calls - handle final response
                if response.stop_reason in ("max_tokens", "length"):
                    if response.content:
                        messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": "Your response was cut off. Please continue.",
                    })
                    continue

                # Final response
                if response.content:
                    self.emitter.emit_message_start()
                    self.emitter.emit_message_delta(response.content)
                    self.emitter.emit_message_end()
                    messages.append({"role": "assistant", "content": response.content})
                    return response.content, messages

                # Empty response - try to recover
                log.warning("Agent returned empty content without tool calls")
                return self._handle_empty_response(messages)

        # Max iterations reached
        return self._handle_max_iterations(messages)

    def _handle_tool_calls(
        self,
        response,
        messages: list[dict],
        tools: list[dict],
    ) -> Optional[tuple[str, list[dict]]]:
        """Process tool calls from LLM response.

        Returns:
            None to continue loop, or (response, messages) tuple to stop
        """
        needs_user_input = False

        # Parse tool call arguments
        parsed_calls = []
        malformed_count = 0
        total_calls = len(response.tool_calls)

        for tool_call in response.tool_calls:
            args = tool_call.arguments
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError as e:
                    malformed_count += 1
                    log.error("Failed to parse tool arguments for {}: {}", tool_call.name, e)
                    self.emitter.emit_tool_start(tool_call.name, {}, tool_id=tool_call.id)
                    self.emitter.emit_tool_result(
                        tool_call.name, success=False,
                        summary=f"Failed to parse arguments: {e}",
                        tool_id=tool_call.id,
                    )
                    continue
            parsed_calls.append((tool_call, args))

        # Track consecutive malformed iterations
        if total_calls > 0 and malformed_count == total_calls:
            self._consecutive_malformed_iterations += 1
            if self._consecutive_malformed_iterations >= 2:
                messages.append({
                    "role": "user",
                    "content": "[SYSTEM: Tool calls are malformed. Use valid JSON arguments.]",
                })
        elif parsed_calls:
            self._consecutive_malformed_iterations = 0

        # Deduplicate tool calls
        seen_calls = set()
        deduped_calls = []
        for tool_call, args in parsed_calls:
            args_key = json.dumps(args, sort_keys=True)
            call_key = (tool_call.name, args_key)
            if call_key not in seen_calls:
                seen_calls.add(call_key)
                deduped_calls.append((tool_call, args))
        parsed_calls = deduped_calls

        # Execute tools
        if len(parsed_calls) > 1:
            results = self._execute_tools_parallel(parsed_calls)
        elif parsed_calls:
            tool_call, args = parsed_calls[0]
            self.emitter.emit_tool_start(tool_call.name, args, tool_id=tool_call.id)
            result = self.toolkit.execute(tool_call.name, **args)
            self.emitter.emit_tool_result(
                tool_call.name, result.success,
                summarize_tool_result(result),
                data=result.data, tool_id=tool_call.id,
            )
            results = [(tool_call, args, result)]
        else:
            results = []

        # Add assistant message with all tool calls
        all_tool_calls = []
        for tool_call, args in parsed_calls:
            all_tool_calls.append({
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.name,
                    "arguments": json.dumps(args),
                },
            })

        messages.append({
            "role": "assistant",
            "content": response.content or "",
            "tool_calls": all_tool_calls,
        })

        # Process results
        for tool_call, args, result in results:
            # Call hook for subclass-specific handling
            self._on_tool_result(tool_call.name, result)

            # Check for user input requirements
            if result.success and result.data and isinstance(result.data, dict):
                status = result.data.get("status")
                if status == "awaiting_response" and "question" in result.data:
                    self.emitter.emit_clarification(
                        question=result.data["question"],
                        context="",
                        options=result.data.get("options", []),
                    )
                    needs_user_input = True
                elif status == "awaiting_choices" and "questions" in result.data:
                    self.emitter.emit_choice_questions(
                        choices=result.data["questions"],
                        context=result.data.get("context", "approach"),
                    )
                    needs_user_input = True
                elif status == "plan_mode_requested":
                    self.emitter.emit_plan_mode_requested(
                        reason=result.data.get("reason", ""),
                    )
                    needs_user_input = True
                elif status == "plan_submitted":
                    self.emitter.emit_plan_submitted(
                        plan=result.data.get("plan", ""),
                    )
                    needs_user_input = True

            # Serialize and add tool result
            result_json = json.dumps(result.to_dict(), cls=SafeJSONEncoder)
            result_json = truncate_tool_output(result_json)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_json,
            })

        # If user input needed, pause
        if needs_user_input:
            log.debug("Pausing agent loop - waiting for user input")
            self.emitter.emit_message_start()
            self.emitter.emit_message_end()
            return "", messages

        return None  # Continue loop

    def _execute_tools_parallel(self, parsed_calls: list) -> list:
        """Execute multiple tool calls in parallel."""
        # Emit start events
        for tool_call, args in parsed_calls:
            self.emitter.emit_tool_start(tool_call.name, args, tool_id=tool_call.id)

        def execute_one(item):
            tool_call, args = item
            try:
                result = self.toolkit.execute(tool_call.name, **args)
                return (tool_call, args, result)
            except Exception as e:
                log.exception(f"Tool {tool_call.name} failed")
                return (tool_call, args, ToolResult.error_result(str(e)))

        executor = self._get_tool_executor()
        results: list = [None] * len(parsed_calls)
        futures = {executor.submit(execute_one, item): i for i, item in enumerate(parsed_calls)}

        for future in as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()

        # Emit result events
        for tool_call, args, result in results:
            self.emitter.emit_tool_result(
                tool_call.name, result.success,
                summarize_tool_result(result),
                data=result.data, tool_id=tool_call.id,
            )

        return results

    def _handle_empty_response(self, messages: list[dict]) -> tuple[str, list[dict]]:
        """Handle case where LLM returns empty content without tool calls."""
        try:
            retry_response = self.provider.chat(
                messages=messages + [{
                    "role": "user",
                    "content": "[SYSTEM: Your response was empty. Please respond to the user.]",
                }],
                system=self.system_prompt,
                tools=None,
                thinking=self.enable_thinking,
            )
            if retry_response.content:
                self.emitter.emit_message_start()
                self.emitter.emit_message_delta(retry_response.content)
                self.emitter.emit_message_end()
                messages.append({"role": "assistant", "content": retry_response.content})
                return retry_response.content, messages
        except Exception as e:
            log.warning(f"Failed to get retry response: {e}")

        fallback = "I apologize, but I wasn't able to generate a response. Could you please rephrase?"
        self.emitter.emit_message_start()
        self.emitter.emit_message_delta(fallback)
        self.emitter.emit_message_end()
        return fallback, messages

    def _handle_max_iterations(self, messages: list[dict]) -> tuple[str, list[dict]]:
        """Handle case where max iterations is reached."""
        try:
            final_response = self.provider.chat(
                messages=messages + [{
                    "role": "user",
                    "content": "[SYSTEM: Maximum iterations reached. Provide your final response now.]",
                }],
                system=self.system_prompt,
                tools=None,
                thinking=self.enable_thinking,
            )
            if final_response.thinking:
                self.emitter.emit_thinking(final_response.thinking)
            if final_response.content:
                self.emitter.emit_message_start()
                self.emitter.emit_message_delta(final_response.content)
                self.emitter.emit_message_end()
                return final_response.content, messages
        except Exception as e:
            log.warning(f"Failed to get final response: {e}")

        fallback = "Reached maximum iterations. Unable to complete the task."
        self.emitter.emit_message_start()
        self.emitter.emit_message_delta(fallback)
        self.emitter.emit_message_end()
        return fallback, messages
