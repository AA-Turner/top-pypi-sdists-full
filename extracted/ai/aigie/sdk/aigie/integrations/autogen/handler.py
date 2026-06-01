"""
AutoGen/AG2 callback handler for Aigie SDK.

Provides automatic tracing for AutoGen multi-agent conversations,
including agent-to-agent messaging, group chats, and code execution.
"""

import uuid
from datetime import datetime
from typing import Any

from ...buffer import EventType
from ...context_manager import merge_metadata


class AutoGenHandler:
    """
    AutoGen/AG2 callback handler for Aigie.

    Automatically traces AutoGen workflow executions including:
    - Conversation initiation and completion
    - Agent-to-agent message exchanges
    - Group chat orchestration
    - LLM calls with tokens/cost
    - Tool/function invocations
    - Code execution blocks

    Example:
        >>> from autogen import ConversableAgent, AssistantAgent
        >>> from aigie.integrations.autogen import AutoGenHandler
        >>>
        >>> handler = AutoGenHandler(
        ...     trace_name='agent-conversation',
        ...     metadata={'project': 'research'}
        ... )
        >>>
        >>> assistant = AssistantAgent("assistant", llm_config={...})
        >>> user = UserProxyAgent("user")
        >>> user.initiate_chat(assistant, message="Hello")
    """

    def __init__(
        self,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        capture_messages: bool = True,
        capture_code: bool = True,
    ):
        """
        Initialize AutoGen handler.

        Args:
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            capture_messages: Whether to capture message content
            capture_code: Whether to capture code blocks
        """
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id
        self.capture_messages = capture_messages
        self.capture_code = capture_code

        # State tracking
        self.trace_id: str | None = None
        self.conversation_span_id: str | None = None
        self.turn_map: dict[int, dict[str, Any]] = {}  # turn_number -> {spanId, startTime}
        self.message_map: dict[str, dict[str, Any]] = {}  # message_id -> {spanId, startTime}
        self.llm_call_map: dict[str, dict[str, Any]] = {}  # call_id -> {spanId, startTime}
        self.tool_call_map: dict[str, dict[str, Any]] = {}  # tool_id -> {spanId, startTime}
        self.code_exec_map: dict[str, dict[str, Any]] = {}  # exec_id -> {spanId, startTime}
        self.group_chat_map: dict[str, dict[str, Any]] = {}  # chat_id -> {spanId, startTime}

        # Current context for parent relationships
        self._current_turn_span_id: str | None = None
        self._current_message_span_id: str | None = None
        self._aigie = None
        self._trace_context: Any | None = None

        # Statistics
        self.total_turns = 0
        self.total_messages = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.total_tool_calls = 0
        self.total_code_executions = 0

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    def set_trace_context(self, trace_context: Any) -> None:
        """Set an existing trace context to use."""
        self._trace_context = trace_context
        if hasattr(trace_context, "id"):
            self.trace_id = str(trace_context.id)

    async def handle_conversation_start(
        self,
        initiator: str,
        recipient: str,
        message: str | None = None,
        max_turns: int | None = None,
        conversation_type: str = "two_agent",
    ) -> None:
        """
        Called when a conversation starts.

        Args:
            initiator: Name/role of the initiating agent
            recipient: Name/role of the recipient agent
            message: Initial message content
            max_turns: Maximum number of turns
            conversation_type: Type of conversation (two_agent, group_chat)
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        # Generate trace ID if not set
        if not self.trace_id:
            if self._trace_context and hasattr(self._trace_context, "id"):
                self.trace_id = str(self._trace_context.id)
            else:
                self.trace_id = str(uuid.uuid4())

        # Build trace name
        trace_name = self.trace_name or f"Conversation: {initiator} -> {recipient}"

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "initiator": initiator,
                "recipient": recipient,
                "conversation_type": conversation_type,
                "max_turns": max_turns,
                "framework": "autogen",
            }
        )

        # Only create trace if we don't have a trace context
        if not self._trace_context:
            trace_data = {
                "id": self.trace_id,
                "name": trace_name,
                "type": "chain",
                "input": {
                    "initiator": initiator,
                    "recipient": recipient,
                    "initial_message": message[:500] if message else None,
                },
                "status": "pending",
                "tags": [*self.tags, "autogen", conversation_type],
                "metadata": merge_metadata(trace_metadata),
                "start_time": datetime.now().isoformat(),
                "created_at": datetime.now().isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            # Send trace via buffer
            if aigie._buffer:
                await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)

        # Create conversation span
        self.conversation_span_id = str(uuid.uuid4())
        conv_span_data = {
            "id": self.conversation_span_id,
            "trace_id": self.trace_id,
            "name": f"conversation:{initiator}->{recipient}",
            "type": "chain",
            "input": {
                "initiator": initiator,
                "recipient": recipient,
                "max_turns": max_turns,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": trace_metadata,
            "start_time": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, conv_span_data)

    async def handle_conversation_end(
        self,
        success: bool,
        result: Any | None = None,
        error: str | None = None,
        termination_reason: str | None = None,
    ) -> None:
        """
        Called when a conversation completes.

        Args:
            success: Whether the conversation succeeded
            result: The conversation result
            error: Error message if failed
            termination_reason: Reason for termination
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return

        end_time = datetime.now()

        # Update conversation span
        if self.conversation_span_id:
            conv_update = {
                "id": self.conversation_span_id,
                "status": "success" if success else "failed",
                "output": {
                    "success": success,
                    "total_turns": self.total_turns,
                    "total_messages": self.total_messages,
                    "total_tokens": self.total_tokens,
                    "total_cost": self.total_cost,
                    "termination_reason": termination_reason,
                },
                "end_time": end_time.isoformat(),
            }
            if result:
                conv_update["output"]["result"] = str(result)[:1000]
            if error:
                conv_update["error"] = error
                conv_update["error_message"] = error

            if aigie._buffer:
                await aigie._buffer.add(EventType.SPAN_UPDATE, conv_update)

        # Update trace
        update_data = {
            "id": self.trace_id,
            "status": "success" if success else "failed",
            "output": {
                "success": success,
                "total_turns": self.total_turns,
                "total_tokens": self.total_tokens,
                "total_cost": self.total_cost,
            },
            "end_time": end_time.isoformat(),
        }

        if result:
            update_data["output"]["result"] = str(result)[:1000]
        if error:
            update_data["error"] = error
            update_data["error_message"] = error

        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_UPDATE, update_data)

    async def handle_turn_start(
        self,
        turn_number: int,
        sender: str,
        recipient: str,
    ) -> str:
        """
        Called when a conversation turn starts.

        Args:
            turn_number: The turn number
            sender: Name of the sending agent
            recipient: Name of the receiving agent

        Returns:
            The span ID for this turn
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_turns = max(self.total_turns, turn_number)
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.turn_map[turn_number] = {
            "spanId": span_id,
            "startTime": start_time,
            "sender": sender,
            "recipient": recipient,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self.conversation_span_id,
            "name": f"turn:{turn_number}",
            "type": "chain",
            "input": {
                "turn_number": turn_number,
                "sender": sender,
                "recipient": recipient,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "turnNumber": turn_number,
                    "sender": sender,
                    "recipient": recipient,
                    "turnType": "autogen_turn",
                    "framework": "autogen",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        self._current_turn_span_id = span_id

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_turn_end(
        self,
        turn_number: int,
        messages_exchanged: int = 0,
    ) -> None:
        """
        Called when a turn completes.

        Args:
            turn_number: The turn number
            messages_exchanged: Number of messages exchanged
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        turn_data = self.turn_map.get(turn_number)
        if not turn_data:
            return

        end_time = datetime.now()
        duration = (end_time - turn_data["startTime"]).total_seconds()

        update_data = {
            "id": turn_data["spanId"],
            "output": {
                "messages_exchanged": messages_exchanged,
            },
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.turn_map[turn_number]

    async def handle_message_start(
        self,
        message_id: str,
        sender: str,
        recipient: str,
        content: str | None = None,
        turn_number: int | None = None,
    ) -> str:
        """
        Called when a message is being sent.

        Args:
            message_id: Unique message identifier
            sender: Name of the sending agent
            recipient: Name of the receiving agent
            content: Message content
            turn_number: Parent turn number

        Returns:
            The span ID for this message
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_messages += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = None
        if turn_number and turn_number in self.turn_map:
            parent_id = self.turn_map[turn_number]["spanId"]
        elif self._current_turn_span_id:
            parent_id = self._current_turn_span_id
        else:
            parent_id = self.conversation_span_id

        self.message_map[message_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"message:{sender}->{recipient}",
            "type": "chain",
            "input": {
                "sender": sender,
                "recipient": recipient,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "messageId": message_id,
                    "sender": sender,
                    "recipient": recipient,
                    "messageType": "autogen_message",
                    "framework": "autogen",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if self.capture_messages and content:
            span_data["input"]["content"] = content[:1000]

        self._current_message_span_id = span_id

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_message_end(
        self,
        message_id: str,
        response: str | None = None,
    ) -> None:
        """
        Called when a message exchange completes.

        Args:
            message_id: Unique message identifier
            response: Response content
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        message_data = self.message_map.get(message_id)
        if not message_data:
            return

        end_time = datetime.now()
        duration = (end_time - message_data["startTime"]).total_seconds()

        output = {}
        if self.capture_messages and response:
            output["response"] = response[:1000]

        update_data = {
            "id": message_data["spanId"],
            "output": output,
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.message_map[message_id]

    async def handle_llm_start(
        self,
        call_id: str,
        model: str,
        messages: Any,
        agent_name: str | None = None,
    ) -> str:
        """
        Called when an LLM call starts.

        Args:
            call_id: Unique ID for this call
            model: Model name
            messages: Input messages
            agent_name: Name of the calling agent

        Returns:
            The span ID for this LLM call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = (
            self._current_message_span_id or self._current_turn_span_id or self.conversation_span_id
        )

        self.llm_call_map[call_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"llm:{model}",
            "type": "llm",
            "input": self._serialize_messages(messages),
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "model": model,
                    "agentName": agent_name,
                    "framework": "autogen",
                }
            ),
            "model": model,
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_llm_end(
        self,
        call_id: str,
        output: Any,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float = 0.0,
    ) -> None:
        """
        Called when an LLM call completes.

        Args:
            call_id: Unique ID for this call
            output: LLM output
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Cost of this call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        call_data = self.llm_call_map.get(call_id)
        if not call_data:
            return

        # Track totals
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += cost

        end_time = datetime.now()
        duration = (end_time - call_data["startTime"]).total_seconds()

        update_data = {
            "id": call_data["spanId"],
            "output": self._serialize_output(output),
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        }

        if cost > 0:
            update_data["total_cost"] = cost

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.llm_call_map[call_id]

    async def handle_llm_error(self, call_id: str, error: str) -> None:
        """Called when an LLM call fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        call_data = self.llm_call_map.get(call_id)
        if not call_data:
            return

        end_time = datetime.now()
        duration = (end_time - call_data["startTime"]).total_seconds()

        update_data = {
            "id": call_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.llm_call_map[call_id]

    async def handle_tool_start(
        self,
        tool_id: str,
        tool_name: str,
        tool_input: Any,
        agent_name: str | None = None,
    ) -> str:
        """
        Called when a tool/function invocation starts.

        Args:
            tool_id: Unique ID for this tool call
            tool_name: Name of the tool/function
            tool_input: Input to the tool
            agent_name: Name of the calling agent

        Returns:
            The span ID for this tool call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_tool_calls += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = self._current_message_span_id or self._current_turn_span_id

        self.tool_call_map[tool_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"tool:{tool_name}",
            "type": "tool",
            "input": self._serialize_tool_input(tool_input),
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "toolName": tool_name,
                    "toolId": tool_id,
                    "agentName": agent_name,
                    "framework": "autogen",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_tool_end(
        self,
        tool_id: str,
        output: Any,
        success: bool = True,
    ) -> None:
        """
        Called when a tool/function invocation completes.

        Args:
            tool_id: Unique ID for this tool call
            output: Tool output
            success: Whether the tool succeeded
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        tool_data = self.tool_call_map.get(tool_id)
        if not tool_data:
            return

        end_time = datetime.now()
        duration = (end_time - tool_data["startTime"]).total_seconds()

        update_data = {
            "id": tool_data["spanId"],
            "output": {"result": str(output)[:1000] if output else None, "success": success},
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.tool_call_map[tool_id]

    async def handle_tool_error(self, tool_id: str, error: str) -> None:
        """Called when a tool invocation fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        tool_data = self.tool_call_map.get(tool_id)
        if not tool_data:
            return

        end_time = datetime.now()
        duration = (end_time - tool_data["startTime"]).total_seconds()

        update_data = {
            "id": tool_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.tool_call_map[tool_id]

    async def handle_code_execution_start(
        self,
        exec_id: str,
        language: str,
        code: str,
        agent_name: str | None = None,
    ) -> str:
        """
        Called when code execution starts.

        Args:
            exec_id: Unique execution identifier
            language: Programming language
            code: Code to execute
            agent_name: Name of the executing agent

        Returns:
            The span ID for this execution
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_code_executions += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span ID
        parent_id = self._current_message_span_id or self._current_turn_span_id

        self.code_exec_map[exec_id] = {
            "spanId": span_id,
            "startTime": start_time,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"code_exec:{language}",
            "type": "tool",
            "input": {},
            "status": "pending",
            "tags": [*self.tags, "code_execution"],
            "metadata": merge_metadata(
                {
                    "execId": exec_id,
                    "language": language,
                    "codeLength": len(code),
                    "agentName": agent_name,
                    "framework": "autogen",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if self.capture_code:
            span_data["input"]["code"] = code[:2000]

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_code_execution_end(
        self,
        exec_id: str,
        exit_code: int,
        output: str | None = None,
        error: str | None = None,
    ) -> None:
        """
        Called when code execution completes.

        Args:
            exec_id: Unique execution identifier
            exit_code: Exit code of the execution
            output: Standard output
            error: Standard error
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        exec_data = self.code_exec_map.get(exec_id)
        if not exec_data:
            return

        end_time = datetime.now()
        duration = (end_time - exec_data["startTime"]).total_seconds()

        success = exit_code == 0

        update_data = {
            "id": exec_data["spanId"],
            "output": {
                "exit_code": exit_code,
                "stdout": output[:1000] if output else None,
                "stderr": error[:500] if error else None,
            },
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if not success and error:
            update_data["error"] = error[:500]
            update_data["error_message"] = error[:500]

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.code_exec_map[exec_id]

    async def handle_group_chat_start(
        self,
        chat_id: str,
        agents: list[str],
        max_rounds: int | None = None,
        speaker_selection_method: str = "auto",
    ) -> str:
        """
        Called when a group chat starts.

        Args:
            chat_id: Unique chat identifier
            agents: List of agent names participating
            max_rounds: Maximum number of rounds
            speaker_selection_method: Method for selecting next speaker

        Returns:
            The span ID for this group chat
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.group_chat_map[chat_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "agents": agents,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self.conversation_span_id,
            "name": f"group_chat:{len(agents)}_agents",
            "type": "chain",
            "input": {
                "agents": agents,
                "max_rounds": max_rounds,
                "speaker_selection_method": speaker_selection_method,
            },
            "status": "pending",
            "tags": [*self.tags, "group_chat"],
            "metadata": merge_metadata(
                {
                    "chatId": chat_id,
                    "agentCount": len(agents),
                    "speakerSelectionMethod": speaker_selection_method,
                    "framework": "autogen",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_group_chat_end(
        self,
        chat_id: str,
        rounds_completed: int,
        final_speaker: str | None = None,
        success: bool = True,
    ) -> None:
        """
        Called when a group chat completes.

        Args:
            chat_id: Unique chat identifier
            rounds_completed: Number of rounds completed
            final_speaker: Name of the final speaker
            success: Whether the chat succeeded
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        chat_data = self.group_chat_map.get(chat_id)
        if not chat_data:
            return

        end_time = datetime.now()
        duration = (end_time - chat_data["startTime"]).total_seconds()

        update_data = {
            "id": chat_data["spanId"],
            "output": {
                "rounds_completed": rounds_completed,
                "final_speaker": final_speaker,
                "success": success,
            },
            "status": "success" if success else "failed",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.group_chat_map[chat_id]

    def _serialize_messages(self, messages: Any) -> Any:
        """Serialize messages for tracing."""
        if isinstance(messages, list):
            return [self._serialize_message(m) for m in messages]
        return self._serialize_message(messages)

    def _serialize_message(self, message: Any) -> Any:
        """Serialize a single message."""
        if isinstance(message, dict):
            return {k: str(v)[:500] if isinstance(v, str) else v for k, v in message.items()}
        if hasattr(message, "model_dump"):
            return message.model_dump()
        if hasattr(message, "dict"):
            return message.dict()
        if hasattr(message, "content"):
            return {
                "role": getattr(message, "role", "unknown"),
                "content": str(message.content)[:1000],
            }
        return str(message)[:1000]

    def _serialize_output(self, output: Any) -> Any:
        """Serialize output for tracing."""
        if isinstance(output, str):
            return output[:2000]
        if hasattr(output, "model_dump"):
            return output.model_dump()
        if hasattr(output, "dict"):
            return output.dict()
        return str(output)[:2000]

    def _serialize_tool_input(self, tool_input: Any) -> Any:
        """Serialize tool input for tracing."""
        if isinstance(tool_input, dict):
            return {k: str(v)[:500] for k, v in tool_input.items()}
        if isinstance(tool_input, str):
            return tool_input[:1000]
        return str(tool_input)[:1000]

    def __repr__(self) -> str:
        return (
            f"AutoGenHandler("
            f"trace_id={self.trace_id}, "
            f"turns={self.total_turns}, "
            f"messages={self.total_messages}, "
            f"tokens={self.total_tokens}, "
            f"cost=${self.total_cost:.4f})"
        )
