"""Agent runner for LLM-powered exploration.

This module contains the main AgentRunner class that orchestrates
the agent loop, tool execution, and conversation management.
"""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional

from ...utils.logger import log
from ...core.exceptions import ContextLengthError
from ...core.config import get_config
from ..toolkit import AgentToolkit
from ..events import AgentEventEmitter, NullEmitter
from ..providers import get_provider
from ..providers.factory import DEFAULT_MODEL, get_vision_provider, get_vision_model
from ..context_manager import (
    truncate_tool_output,
    reduce_context_for_retry,
    is_context_overflow_error,
    is_transient_network_error,
)
from ..prompts import build_system_prompt
from ..tools.tasks import TaskState
from ...checkpoint import CheckpointManager

from .utils import SafeJSONEncoder, summarize_tool_result
from .context import (
    estimate_context_tokens,
    get_context_breakdown,
    maybe_compact_context,
    emit_context_frame,
    get_reranked_context,
)
from .plan import PlanMixin
from ..background import BackgroundTaskManager
from ..compaction_strategy import CompactionResult, CompactionStrategy, get_compaction_strategy


class AgentRunner(PlanMixin):
    """Runs an LLM agent with tool access for code exploration.

    Example:
        runner = AgentRunner()
        response = runner.run("How does authentication work in this codebase?")
        print(response)
    """

    def __init__(
        self,
        toolkit: Optional[AgentToolkit] = None,
        model: str = DEFAULT_MODEL,
        system_prompt: Optional[str] = None,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = int(os.getenv("EMDASH_MAX_ITERATIONS", "100")),
        verbose: bool = False,
        show_tool_results: bool = False,
        enable_thinking: Optional[bool] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
        session_id: Optional[str] = None,
        compaction_strategy: Optional[CompactionStrategy] = None,
    ):
        """Initialize the agent runner.

        Args:
            toolkit: AgentToolkit instance. If None, creates default.
            model: LLM model to use.
            system_prompt: Custom system prompt. If None, uses default.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            show_tool_results: Whether to show detailed tool results.
            enable_thinking: Enable extended thinking. If None, auto-detect from model.
            checkpoint_manager: Optional checkpoint manager for git-based checkpoints.
            session_id: Session ID for plan file isolation. If None, generates on demand.
        """
        self.toolkit = toolkit or AgentToolkit()
        self.provider = get_provider(model)
        self.model = model
        # Build system prompt
        if system_prompt:
            self.system_prompt = system_prompt
        else:
            self.system_prompt = build_system_prompt(self.toolkit)
        self.emitter = emitter or NullEmitter()
        # Inject emitter into tools that need it (e.g., TaskTool for sub-agent streaming)
        self.toolkit.set_emitter(self.emitter)
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.show_tool_results = show_tool_results
        # Extended thinking support
        if enable_thinking is None:
            # Auto-detect from provider capabilities
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
        # Store query for reranking
        self._current_query: str = ""
        # Todo state tracking for injection
        self._last_todo_snapshot: str = ""
        # Checkpoint manager for git-based checkpoints
        self._checkpoint_manager = checkpoint_manager
        # Track tools used during current run (for checkpoint metadata)
        self._tools_used_this_run: set[str] = set()
        # Plan approval state (from PlanMixin)
        self._pending_plan: Optional[dict] = None
        # Context frame injection flag
        self._inject_context_frame = os.getenv("EMDASH_INJECT_CONTEXT_FRAME", "").lower() in ("1", "true", "yes")
        # Session ID for plan file isolation
        self._session_id = session_id
        # Persistent thread pool executor for parallel tool execution
        config = get_config()
        self._tool_parallel_workers = config.agent.tool_parallel_workers
        self._tool_executor: Optional[ThreadPoolExecutor] = None
        # Vision provider (lazily initialized when images are used with non-vision model)
        self._vision_provider = None
        # Track consecutive iterations with all malformed tool calls
        self._consecutive_malformed_iterations = 0
        # Flag to prevent overwriting messages after external compaction
        self._messages_compacted_externally = False
        # Compaction strategy (pluggable: llm_summary or observational_memory)
        self._compaction_strategy: CompactionStrategy = (
            compaction_strategy
            or get_compaction_strategy(thread_id=session_id or "default")
        )

    @property
    def name(self) -> str:
        """Return the display name for this agent."""
        return "Emdash Code"

    @property
    def agent_type(self) -> str:
        """Return the agent type identifier."""
        return "coding"

    def _get_vision_provider(self):
        """Get or create a vision-capable provider.

        Lazily initializes the vision provider on first use.

        Returns:
            LLMProvider that supports vision
        """
        if self._vision_provider is None:
            self._vision_provider = get_vision_provider()
            log.info(
                "Created vision provider model={} for image support",
                get_vision_model(),
            )
        return self._vision_provider

    def _needs_vision_provider(self, images: Optional[list]) -> bool:
        """Check if we need to switch to vision provider.

        Args:
            images: List of images or None

        Returns:
            True if images are present and current provider doesn't support vision
        """
        if not images:
            return False
        # Check if current provider supports vision
        if hasattr(self.provider, "supports_vision") and self.provider.supports_vision():
            return False
        return True

    def _get_todo_snapshot(self) -> str:
        """Get current todo state as string for comparison."""
        state = TaskState.get_instance()
        return json.dumps(state.get_all_tasks(), sort_keys=True)

    def _format_todo_reminder(self) -> str:
        """Format current todos as XML reminder for injection into context."""
        state = TaskState.get_instance()
        tasks = state.get_all_tasks()
        if not tasks:
            return ""

        counts = {"pending": 0, "in_progress": 0, "completed": 0}
        lines = []
        for t in tasks:
            status = t.get("status", "pending")
            counts[status] = counts.get(status, 0) + 1
            status_icon = {"pending": "⬚", "in_progress": "🔄", "completed": "✅"}.get(status, "?")
            lines.append(f'  {t["id"]}. {status_icon} {t["title"]}')

        header = f'Tasks: {counts["completed"]} completed, {counts["in_progress"]} in progress, {counts["pending"]} pending'
        task_list = "\n".join(lines)
        return f"<todo-state>\n{header}\n{task_list}\n</todo-state>"

    def _check_background_notifications(self) -> list[str]:
        """Check for completed background tasks and format notifications.

        Returns:
            List of notification messages to inject into context
        """
        try:
            manager = BackgroundTaskManager.get_instance()
            completed_tasks = manager.get_pending_notifications()

            notifications = []
            for task in completed_tasks:
                msg = manager.format_notification(task)
                notifications.append(msg)
                log.info(f"Background task {task.task_id} notification ready")

            return notifications
        except Exception as e:
            log.warning(f"Failed to check background notifications: {e}")
            return []

    def _format_context_reminder(self) -> str:
        """Format reranked context items as XML reminder for injection.

        Only called when EMDASH_INJECT_CONTEXT_FRAME is enabled.

        Returns:
            Formatted context reminder string, or empty if no context
        """
        if not self._current_query:
            return ""

        reading = get_reranked_context(self.toolkit, self._current_query)
        items = reading.get("items", [])

        if not items:
            return ""

        lines = [
            "<context-frame>",
            f"Relevant context for query: {self._current_query[:100]}",
            f"Found {len(items)} relevant items (ranked by relevance score):",
            "",
        ]

        for item in items[:15]:  # Top 15 items
            name = item.get("name", "?")
            item_type = item.get("type", "?")
            score = item.get("score")
            file_path = item.get("file", "")
            description = item.get("description", "")

            score_str = f" (score: {score:.3f})" if score is not None else ""
            file_str = f" in {file_path}" if file_path else ""

            lines.append(f"  - [{item_type}] {name}{score_str}{file_str}")
            if description:
                lines.append(f"    {description[:150]}")

        lines.append("</context-frame>")
        return "\n".join(lines)

    def _get_tool_executor(self) -> ThreadPoolExecutor:
        """Get the persistent thread pool executor, creating it if needed.

        Uses lazy initialization to avoid creating threads until actually needed.
        """
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

    def _execute_tools_parallel(self, parsed_calls: list) -> list:
        """Execute multiple tool calls in parallel using a thread pool.

        Uses a persistent thread pool executor for better performance by avoiding
        thread creation/destruction overhead on each batch of tool calls.

        Args:
            parsed_calls: List of (tool_call, args) tuples

        Returns:
            List of (tool_call, args, result) tuples in original order
        """
        from ..tools.base import ToolResult

        # Check for cancellation before starting
        if self.emitter.is_cancelled():
            log.info("Agent cancelled before tool execution")
            return [(tc, args, ToolResult.error_result("Cancelled")) for tc, args in parsed_calls]

        # Emit tool start events for all calls
        for tool_call, args in parsed_calls:
            self.emitter.emit_tool_start(tool_call.name, args, tool_id=tool_call.id)

        # Reference to emitter for closure
        emitter = self.emitter

        def execute_one(item):
            tool_call, args = item
            # Check cancellation before each tool execution
            if emitter.is_cancelled():
                return (tool_call, args, ToolResult.error_result("Cancelled"))
            try:
                result = self.toolkit.execute(tool_call.name, **args)
                return (tool_call, args, result)
            except Exception as e:
                log.exception(f"Tool {tool_call.name} failed")
                return (tool_call, args, ToolResult.error_result(str(e)))

        # Execute in parallel using persistent executor
        executor = self._get_tool_executor()
        results: list = [None] * len(parsed_calls)
        futures = {executor.submit(execute_one, item): i for i, item in enumerate(parsed_calls)}

        # Collect results maintaining order, with cancellation check
        for future in as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
            # Check for cancellation after each result
            if self.emitter.is_cancelled():
                log.info("Agent cancelled during tool execution, cancelling remaining futures")
                # Cancel any remaining futures
                for f in futures:
                    if not f.done():
                        f.cancel()
                # Fill remaining results with cancelled
                for i, r in enumerate(results):
                    if r is None:
                        tc, args = parsed_calls[i]
                        results[i] = (tc, args, ToolResult.error_result("Cancelled"))
                break

        # Emit tool result events for all calls
        for tool_call, args, result in results:
            self.emitter.emit_tool_result(
                tool_call.name,
                result.success,
                summarize_tool_result(result),
                data=result.data,
                tool_id=tool_call.id,
            )

        return results

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
        # Store query for reranking context frame
        self._current_query = query

        # Reset per-cycle mode state
        from ..tools.modes import ModeState
        ModeState.get_instance(self._session_id).reset_cycle()

        # Switch to vision provider if needed (images present, current model doesn't support vision)
        original_provider = None
        if self._needs_vision_provider(images):
            original_provider = self.provider
            self.provider = self._get_vision_provider()
            vision_model = self.provider.model if hasattr(self.provider, 'model') else 'gpt-4o-mini'
            log.info(
                "Switched to vision provider for image processing: {} -> {}",
                original_provider.model if hasattr(original_provider, 'model') else 'unknown',
                vision_model,
            )
            # Notify user that vision provider is being used
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

        user_message = {
            "role": "user",
            "content": content,
        }

        # Save user message to history BEFORE running (so it's preserved even if interrupted)
        self._messages.append(user_message)
        messages = list(self._messages)  # Copy for the loop

        # Get tool schemas
        tools = self.toolkit.get_all_schemas()

        try:
            response, final_messages = self._run_loop(messages, tools)
            # Update conversation history with full exchange
            # But don't overwrite if external compaction happened during the loop
            if self._messages_compacted_externally:
                log.info("Skipping message update - external compaction detected")
                self._messages_compacted_externally = False  # Reset flag
            else:
                self._messages = final_messages
            from ..providers.models import calculate_cost
            self.emitter.emit_end(
                success=True,
                raw_response={
                    "input_tokens": self._total_input_tokens,
                    "output_tokens": self._total_output_tokens,
                    "thinking_tokens": self._total_thinking_tokens,
                    "cost": calculate_cost(
                        self._total_input_tokens,
                        self._total_output_tokens,
                        self.model,
                        self._total_thinking_tokens,
                    ),
                },
            )
            # Create checkpoint if manager is configured
            self._create_checkpoint()
            return response

        except Exception as e:
            log.exception("Agent run failed")
            self.emitter.emit_error(str(e))
            # Keep user message in history even on error (already appended above)
            return f"Error: {str(e)}"

        finally:
            # Restore original provider if we switched for vision
            if original_provider is not None:
                self.provider = original_provider
                log.debug("Restored original provider after vision processing")

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
        max_retries = 3

        for iteration in range(self.max_iterations):
            # Check if client has disconnected (cancelled)
            if self.emitter.is_cancelled():
                log.info("Agent cancelled by client disconnect at iteration {}", iteration)
                return "", messages

            # Check for completed background tasks and inject notifications
            bg_notifications = self._check_background_notifications()
            for notification in bg_notifications:
                messages.append({
                    "role": "user",
                    "content": notification,
                })
                # Emit event so UI can show notification
                self.emitter.emit_assistant_text(f"[Background task completed - see notification]")

            # When approaching max iterations, ask agent to wrap up
            if iteration == self.max_iterations - 2:
                messages.append({
                    "role": "user",
                    "content": "[SYSTEM: You are approaching your iteration limit. Please provide your findings and conclusions now, even if incomplete. Summarize what you've learned and any recommendations.]",
                })

            # Try API call with retry on context overflow and transient errors
            retry_count = 0
            network_retry_count = 0
            max_network_retries = 3
            response = None

            while retry_count < max_retries:
                try:
                    # Proactively compact context if approaching limit
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
                        # Legacy path (shouldn't happen but defensive)
                        messages = compaction_result
                        _system_override = None

                    log.debug(
                        "Calling LLM iteration={} messages={} tools={}",
                        iteration,
                        len(messages),
                        len(tools) if tools else 0,
                    )

                    # Build dynamic system prompt with files already read
                    # Use strategy-enhanced prompt if available
                    dynamic_system = _system_override or self.system_prompt
                    files_read = self.toolkit.get_files_read()
                    if files_read:
                        files_list = ", ".join(files_read[-20:])  # Limit to last 20 files
                        dynamic_system += f"\n\n## Files Already Read (DO NOT re-read these)\n{files_list}"

                    import time
                    _llm_start_time = time.time()
                    response = self.provider.chat(
                        messages=messages,
                        system=dynamic_system,
                        tools=tools,
                        thinking=self.enable_thinking,
                    )
                    _llm_duration_ms = int((time.time() - _llm_start_time) * 1000)

                    log.debug("LLM response received iteration={}", iteration)
                    break  # Success

                except Exception as exc:
                    if is_context_overflow_error(exc):
                        retry_count += 1
                        log.warning(
                            "Context overflow on attempt {}/{}, reducing context...",
                            retry_count,
                            max_retries,
                        )

                        if retry_count >= max_retries:
                            raise ContextLengthError(
                                f"Failed to reduce context after {max_retries} attempts: {exc}",
                            )

                        # Reduce context by removing old messages
                        messages = reduce_context_for_retry(
                            messages,
                            keep_recent=max(2, 6 - retry_count * 2),  # Fewer messages each retry
                        )
                    elif is_transient_network_error(exc):
                        network_retry_count += 1
                        if network_retry_count > max_network_retries:
                            raise

                        import time as _time
                        delay = min(2 ** network_retry_count, 8)  # 2s, 4s, 8s
                        log.warning(
                            "Transient network error on attempt {}/{}: {}. Retrying in {}s...",
                            network_retry_count,
                            max_network_retries,
                            type(exc).__name__,
                            delay,
                        )
                        self.emitter.emit_assistant_text(
                            f"[Network error: {type(exc).__name__}. Retrying in {delay}s ({network_retry_count}/{max_network_retries})...]"
                        )
                        _time.sleep(delay)
                    else:
                        raise  # Re-raise non-retryable errors

            if response is None:
                raise RuntimeError("Failed to get response from provider")

            # Accumulate token usage
            self._total_input_tokens += response.input_tokens
            self._total_output_tokens += response.output_tokens
            self._total_thinking_tokens += getattr(response, "thinking_tokens", 0)

            # Emit per-iteration LLM usage (before processing tool calls)
            from ..providers.models import calculate_cost
            self.emitter.emit_llm_step(
                iteration=iteration,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                thinking_tokens=getattr(response, "thinking_tokens", 0),
                cost=calculate_cost(
                    response.input_tokens,
                    response.output_tokens,
                    self.model,
                    getattr(response, "thinking_tokens", 0),
                ),
                response_text=response.content,
                has_tool_calls=bool(response.tool_calls),
                tool_call_names=[tc.name for tc in response.tool_calls] if response.tool_calls else None,
                cache_creation_input_tokens=getattr(response, "cache_creation_input_tokens", None),
                cache_read_input_tokens=getattr(response, "cache_read_input_tokens", None),
                duration_ms=_llm_duration_ms,
                model=self.model,
            )

            # Emit thinking if present
            if response.thinking:
                self.emitter.emit_thinking(response.thinking, raw_response=response.to_dict(self.model))

            # Check for tool calls
            if response.tool_calls:
                # Emit assistant text if present (shown as bullets between tool calls)
                if response.content and response.content.strip():
                    self.emitter.emit_assistant_text(response.content)

                # Track if we need to pause for user input
                needs_user_input = False

                # Parse all tool call arguments first
                parsed_calls = []
                malformed_count = 0
                total_tool_calls = len(response.tool_calls)
                for tool_call in response.tool_calls:
                    args = tool_call.arguments
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError as e:
                            malformed_count += 1
                            log.error(
                                "Failed to parse tool arguments for {}: {} - args: {}",
                                tool_call.name,
                                e,
                                args[:200] if len(args) > 200 else args,
                            )
                            # Emit error and skip this tool call
                            self.emitter.emit_tool_start(tool_call.name, {}, tool_id=tool_call.id)
                            self.emitter.emit_tool_result(
                                tool_call.name,
                                success=False,
                                summary=f"Failed to parse arguments: {e}",
                                tool_id=tool_call.id,
                            )
                            continue
                    parsed_calls.append((tool_call, args))

                # Track consecutive iterations with all malformed tool calls
                if total_tool_calls > 0 and malformed_count == total_tool_calls:
                    self._consecutive_malformed_iterations += 1
                    log.warning(
                        "All {} tool calls malformed (consecutive iterations: {})",
                        total_tool_calls,
                        self._consecutive_malformed_iterations,
                    )
                    # After 2 consecutive iterations, inject corrective guidance
                    if self._consecutive_malformed_iterations >= 2:
                        messages.append({
                            "role": "user",
                            "content": "[SYSTEM: Your tool calls are malformed and cannot be parsed. "
                            "Tool arguments must be valid JSON objects, not XML or key=value syntax. "
                            "For example, use {\"path\": \"README.md\"} not path=\"README.md\". "
                            "Please retry with proper JSON argument formatting.]",
                        })
                        self.emitter.emit_assistant_text(
                            "[System: Detected malformed tool calls, sending corrective guidance]"
                        )
                elif parsed_calls:
                    # At least one call parsed successfully, reset counter
                    self._consecutive_malformed_iterations = 0

                # Deduplicate tool calls with identical name and arguments
                # Some models call the same tool multiple times with exact same args
                seen_calls = set()
                deduped_calls = []
                for tool_call, args in parsed_calls:
                    # Create a hashable key from tool name and sorted args
                    args_key = json.dumps(args, sort_keys=True)
                    call_key = (tool_call.name, args_key)
                    if call_key not in seen_calls:
                        seen_calls.add(call_key)
                        deduped_calls.append((tool_call, args))
                    else:
                        log.warning(
                            "Skipping duplicate tool call: {}({})",
                            tool_call.name,
                            args_key[:100],
                        )
                parsed_calls = deduped_calls

                if not parsed_calls:
                    # All tool calls were malformed or deduplicated away - skip execution
                    continue

                if len(parsed_calls) > 1:
                    # No exit_plan - execute tools in parallel
                    results = self._execute_tools_parallel(parsed_calls)
                else:
                    # Single tool - execute directly
                    tool_call, args = parsed_calls[0]
                    # Check for cancellation before executing
                    if self.emitter.is_cancelled():
                        log.info("Agent cancelled before single tool execution")
                        from ..tools.base import ToolResult
                        result = ToolResult.error_result("Cancelled")
                    else:
                        self.emitter.emit_tool_start(tool_call.name, args, tool_id=tool_call.id)
                        result = self.toolkit.execute(tool_call.name, **args)
                    self.emitter.emit_tool_result(
                        tool_call.name,
                        result.success,
                        summarize_tool_result(result),
                        data=result.data,
                        tool_id=tool_call.id,
                    )
                    results = [(tool_call, args, result)]

                # CRITICAL FIX: Add ONE assistant message with ALL tool calls
                # This prevents the LLM from seeing multiple assistant messages
                # which causes it to loop repeating the same tools
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

                # Now process results and add tool result messages
                for tool_call, args, result in results:
                    # Track tool for checkpoint metadata
                    self._tools_used_this_run.add(tool_call.name)

                    # Check if tool is asking a clarification question
                    if (result.success and
                        result.data and
                        isinstance(result.data, dict) and
                        result.data.get("status") == "awaiting_response" and
                        "question" in result.data):
                        self.emitter.emit_clarification(
                            question=result.data["question"],
                            context="",
                            options=result.data.get("options", []),
                        )
                        needs_user_input = True

                    # Check if tool is presenting choice questions
                    if (result.success and
                        result.data and
                        isinstance(result.data, dict) and
                        result.data.get("status") == "awaiting_choices" and
                        "questions" in result.data):
                        # Emit browser handoff event if this is a handoff request
                        if result.data.get("context") == "browser_handoff":
                            self.emitter.emit_browser_handoff(
                                reason=result.data.get("reason", ""),
                                session_id=result.data.get("session_id"),
                                live_view_url=result.data.get("live_view_url"),
                                action="requested",
                            )
                        self.emitter.emit_choice_questions(
                            choices=result.data["questions"],
                            context=result.data.get("context", "approach"),
                        )
                        needs_user_input = True

                    # Serialize and truncate tool result to prevent context overflow
                    result_json = json.dumps(result.to_dict(), cls=SafeJSONEncoder)
                    result_json = truncate_tool_output(result_json)

                    # Check if todos changed and inject reminder
                    if tool_call.name in ("write_todo", "update_todo_list"):
                        new_snapshot = self._get_todo_snapshot()
                        if new_snapshot != self._last_todo_snapshot:
                            self._last_todo_snapshot = new_snapshot
                            reminder = self._format_todo_reminder()
                            if reminder:
                                result_json += f"\n\n{reminder}"

                    # Add tool result
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_json,
                    })

                # Inject context frame reminder if enabled (append to last tool result)
                if self._inject_context_frame and messages and messages[-1].get("role") == "tool":
                    context_reminder = self._format_context_reminder()
                    if context_reminder:
                        messages[-1]["content"] += f"\n\n{context_reminder}"

                # Feed new messages into compaction strategy (for observational memory)
                self._compaction_strategy.on_turn_complete(
                    thread_id=self._session_id or "default",
                    new_messages=messages[-len(results):] if results else [],
                )

                # Emit context frame after each iteration (for autosave and UI updates)
                self._emit_context_frame(messages)

                # Check for cancellation after tool execution
                if self.emitter.is_cancelled():
                    log.info("Agent cancelled after tool execution")
                    return "", messages

                # If a clarification question was asked, pause and wait for user input
                if needs_user_input:
                    log.debug("Pausing agent loop - waiting for user input")
                    # Emit empty response to signal session pause (not an error)
                    # This ensures the CLI knows the session ended intentionally
                    self.emitter.emit_message_start()
                    self.emitter.emit_message_end()
                    return "", messages

            else:
                # No tool calls - check if response was truncated
                if response.stop_reason in ("max_tokens", "length"):
                    # Response was truncated, request continuation
                    log.debug("Response truncated ({}), requesting continuation", response.stop_reason)
                    if response.content:
                        messages.append({
                            "role": "assistant",
                            "content": response.content,
                        })
                    messages.append({
                        "role": "user",
                        "content": "Your response was cut off. Please continue.",
                    })
                    continue

                # Agent is done - emit final response
                if response.content:
                    # Check for unhelpful generic responses that some models produce
                    content_lower = response.content.strip().lower()
                    unhelpful_responses = {
                        "task completed.", "task completed",
                        "done.", "done",
                        "completed.", "completed",
                        "finished.", "finished",
                        "ok.", "ok",
                        "okay.", "okay",
                    }
                    if content_lower in unhelpful_responses:
                        log.warning(
                            "Model returned unhelpful response: '{}' - retrying",
                            response.content.strip(),
                        )
                        # Retry with clearer prompt
                        try:
                            retry_response = self.provider.chat(
                                messages=messages + [{
                                    "role": "user",
                                    "content": "[SYSTEM: Your response was not helpful. The user needs an actual response to their message, not just 'task completed' or similar. Please engage with what they said and provide a meaningful reply. If they said hello, greet them back. If they asked a question, answer it. If unclear, ask for clarification.]",
                                }],
                                system=self.system_prompt,
                                tools=None,  # Force text response
                                thinking=self.enable_thinking,
                            )
                            if retry_response.content and retry_response.content.strip().lower() not in unhelpful_responses:
                                self.emitter.emit_message_start()
                                self.emitter.emit_message_delta(retry_response.content)
                                self.emitter.emit_message_end(raw_response=retry_response.to_dict(self.model))
                                messages.append({
                                    "role": "assistant",
                                    "content": retry_response.content,
                                })
                                self._emit_context_frame(messages)
                                return retry_response.content, messages
                        except Exception as e:
                            log.warning(f"Failed to get retry response for unhelpful output: {e}")
                        # If retry also fails, fall through to show the unhelpful response
                        # (better than nothing)

                    self.emitter.emit_message_start()
                    self.emitter.emit_message_delta(response.content)
                    self.emitter.emit_message_end(raw_response=response.to_dict(self.model))
                    # Add final assistant message to history
                    messages.append({
                        "role": "assistant",
                        "content": response.content,
                    })
                    # Emit final context frame summary
                    self._emit_context_frame(messages)
                    return response.content, messages

                # Agent returned empty response without tool calls - try to get a proper response
                log.warning(
                    "Agent returned empty content without tool calls iteration={} stop_reason={}",
                    iteration,
                    response.stop_reason,
                )

                # Retry: Ask the model to respond properly
                try:
                    retry_response = self.provider.chat(
                        messages=messages + [{
                            "role": "user",
                            "content": "[SYSTEM: Your response was empty. Please respond to the user's message. If you're unsure what they need, ask for clarification.]",
                        }],
                        system=self.system_prompt,
                        tools=None,  # Force text response to avoid infinite empty loops
                        thinking=self.enable_thinking,
                    )
                    if retry_response.content:
                        self.emitter.emit_message_start()
                        self.emitter.emit_message_delta(retry_response.content)
                        self.emitter.emit_message_end(raw_response=retry_response.to_dict(self.model))
                        messages.append({
                            "role": "assistant",
                            "content": retry_response.content,
                        })
                        self._emit_context_frame(messages)
                        return retry_response.content, messages
                except Exception as e:
                    log.warning(f"Failed to get retry response: {e}")

                # Fallback if retry fails - provide helpful message
                fallback_message = "I apologize, but I wasn't able to generate a response. Could you please rephrase your request or provide more details?"
                self.emitter.emit_message_start()
                self.emitter.emit_message_delta(fallback_message)
                self.emitter.emit_message_end()
                self._emit_context_frame(messages)
                return fallback_message, messages

        # Hit max iterations - try one final request without tools to force a response
        try:
            final_response = self.provider.chat(
                messages=messages + [{
                    "role": "user",
                    "content": "[SYSTEM: Maximum iterations reached. Provide your final response now with whatever information you have gathered. Do not use any tools.]",
                }],
                system=self.system_prompt,
                tools=None,  # No tools - force text response
                thinking=self.enable_thinking,
            )
            # Emit thinking if present
            if final_response.thinking:
                self.emitter.emit_thinking(final_response.thinking, raw_response=final_response.to_dict(self.model))
            if final_response.content:
                self.emitter.emit_message_start()
                self.emitter.emit_message_delta(final_response.content)
                self.emitter.emit_message_end(raw_response=final_response.to_dict(self.model))
                self._emit_context_frame(messages)
                return final_response.content, messages
        except Exception as e:
            log.warning(f"Failed to get final response: {e}")

        # Fallback message if final response fails
        final_message = "Reached maximum iterations. The agent was unable to complete the task within the allowed iterations."
        self.emitter.emit_message_start()
        self.emitter.emit_message_delta(final_message)
        self.emitter.emit_message_end()
        self._emit_context_frame(messages)
        return final_message, messages

    def _emit_context_frame(self, messages: list[dict] | None = None) -> None:
        """Emit a context frame event with current exploration state.

        Args:
            messages: Current conversation messages to estimate context size
        """
        emit_context_frame(
            toolkit=self.toolkit,
            emitter=self.emitter,
            messages=messages or [],
            system_prompt=self.system_prompt,
            current_query=self._current_query,
            total_input_tokens=self._total_input_tokens,
            total_output_tokens=self._total_output_tokens,
        )

    def chat(self, message: str, images: Optional[list] = None) -> str:
        """Continue a conversation with a new message.

        This method maintains conversation history for multi-turn interactions.
        Call run() first to start a conversation, then chat() for follow-ups.

        Args:
            message: User's follow-up message
            images: Optional list of images to include

        Returns:
            Agent's response
        """
        if not self._messages:
            # No history, just run fresh
            return self.run(message, images=images)

        # Reset per-cycle mode state
        from ..tools.modes import ModeState
        ModeState.get_instance(self._session_id).reset_cycle()

        # Store query for reranking context frame
        self._current_query = message

        # Switch to vision provider if needed (images present, current model doesn't support vision)
        original_provider = None
        if self._needs_vision_provider(images):
            original_provider = self.provider
            self.provider = self._get_vision_provider()
            vision_model = self.provider.model if hasattr(self.provider, 'model') else 'gpt-4o-mini'
            log.info(
                "Switched to vision provider for image processing: {} -> {}",
                original_provider.model if hasattr(original_provider, 'model') else 'unknown',
                vision_model,
            )
            # Notify user that vision provider is being used
            self.emitter.emit_thinking(f"Processing image with vision model ({vision_model})...")

        # Format content with images if provided
        if images:
            content = self.provider.format_content_with_images(message, images)
        else:
            content = message

        # Add new user message to history
        self._messages.append({
            "role": "user",
            "content": content,
        })

        # Get tool schemas
        tools = self.toolkit.get_all_schemas()

        try:
            response, final_messages = self._run_loop(self._messages, tools)
            # Update conversation history
            # But don't overwrite if external compaction happened during the loop
            if self._messages_compacted_externally:
                log.info("Skipping message update - external compaction detected")
                self._messages_compacted_externally = False  # Reset flag
            else:
                self._messages = final_messages
            from ..providers.models import calculate_cost
            self.emitter.emit_end(
                success=True,
                raw_response={
                    "input_tokens": self._total_input_tokens,
                    "output_tokens": self._total_output_tokens,
                    "thinking_tokens": self._total_thinking_tokens,
                    "cost": calculate_cost(
                        self._total_input_tokens,
                        self._total_output_tokens,
                        self.model,
                        self._total_thinking_tokens,
                    ),
                },
            )
            # Create checkpoint if manager is configured
            self._create_checkpoint()
            return response

        except Exception as e:
            log.exception("Agent chat failed")
            self.emitter.emit_error(str(e))
            return f"Error: {str(e)}"

        finally:
            # Restore original provider if we switched for vision
            if original_provider is not None:
                self.provider = original_provider
                log.debug("Restored original provider after vision processing")

    def _create_checkpoint(self) -> None:
        """Create a git checkpoint after successful run.

        Only creates a checkpoint if:
        - A checkpoint manager is configured
        - There are file changes to commit
        """
        if not self._checkpoint_manager:
            return

        try:
            self._checkpoint_manager.create_checkpoint(
                messages=self._messages,
                model=self.model,
                system_prompt=self.system_prompt,
                tools_used=list(self._tools_used_this_run),
                token_usage={
                    "input": self._total_input_tokens,
                    "output": self._total_output_tokens,
                    "thinking": self._total_thinking_tokens,
                },
            )
        except Exception as e:
            log.warning(f"Failed to create checkpoint: {e}")
        finally:
            # Clear tools for next run
            self._tools_used_this_run.clear()

    def reset(self) -> None:
        """Reset the agent state."""
        self.toolkit.reset_session()
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._current_query = ""

    def answer_clarification(self, answer: str) -> str:
        """Answer a pending clarification question and resume the agent.

        This method is called when the user responds to a clarification question
        asked via ask_choice_questions tool. It clears the pending question state
        and resumes the agent loop with the user's answer.

        Args:
            answer: The user's answer to the clarification question

        Returns:
            Agent's response after processing the answer
        """
        # Get current task state and clear the pending question
        state = TaskState.get_instance()
        pending_question = state.pending_question

        # Clear the pending question state
        state.pending_question = None
        state.user_response = answer

        # Build a context message that indicates this is the answer to the question
        if pending_question:
            context_message = f"[User answered the clarification question]\nQuestion: {pending_question}\nAnswer: {answer}"
        else:
            context_message = f"[User response]: {answer}"

        # Continue the conversation with the answer
        return self.chat(context_message)

    def answer_choice_questions(self, responses: list[dict]) -> str:
        """Answer pending choice questions and resume the agent.

        This method is called when the user responds to choice questions
        asked via ask_choice_questions tool. It clears the pending choices
        state and resumes the agent loop with the user's selections.

        Args:
            responses: List of dicts with question index and selected answer
                       e.g., [{"question": "Which auth?", "answer": "JWT"}]

        Returns:
            Agent's response after processing the answers
        """
        # Get current task state and clear the pending choices
        state = TaskState.get_instance()
        pending_choices = state.pending_choices
        context = state.choice_context or "approach"

        # Clear the pending choices state
        state.clear_pending_choices()
        state.choice_responses = responses

        # Build a context message with the user's selections
        if pending_choices:
            lines = [f"[User made {context} selections]"]
            for i, resp in enumerate(responses):
                question = resp.get("question", f"Choice {i+1}")
                answer = resp.get("answer", "")
                lines.append(f"- {question}: {answer}")
            context_message = "\n".join(lines)
        else:
            context_message = f"[User selections]: {responses}"

        # Continue the conversation with the answers
        return self.chat(context_message)
