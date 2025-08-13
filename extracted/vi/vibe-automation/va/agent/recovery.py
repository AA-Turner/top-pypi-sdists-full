import os
import logging
from typing import Dict, List, Any
import json

from va.agent.agent import Agent
from va.agent.prompt import create_system_prompt

from va.agent.tools import RecoverySession, RECOVERY_TOOLS

log = logging.getLogger(__name__)


class WorkflowRecoveryAgent:
    """LLM-powered agent for workflow exception recovery using conversation loop."""

    def __init__(self):
        self.agent = Agent()

    async def recover_from_exception(self, session: RecoverySession) -> bool:
        """
        Attempt to recover from an exception using conversation loop with LLM.

        Args:
            session: Recovery session containing context and tools

        Returns:
            True if recovery was successful, False otherwise
        """
        print(
            f"\n🔧 Entering LLM recovery mode for exception: {session.original_exception}"
        )
        print(f"📋 Workflow goal: {session.workflow_goal}")

        # Initialize conversation with system prompt and first user message
        system_prompt = create_system_prompt(session)

        # Create context-appropriate initial message
        if session.has_browser_context:
            # Browser context - get page state
            page_state = await session.tools.get_page_state()
            initial_content = f"An exception occurred in the workflow: {session.original_exception}\n\nCurrent page URL: {page_state.get('url', 'Unknown')}\n\nPlease analyze the situation and use the available tools to recover from this exception."
        else:
            # General code context - provide file information and actual failing code
            filename = session.execution_context.get("filename", "Unknown")
            line_no = session.exception_line

            # Get the actual failing line from the source code
            failing_line = "Unknown"
            try:
                source_lines = session.original_workflow_code.split("\n")
                if line_no and 1 <= line_no <= len(source_lines):
                    failing_line = source_lines[line_no - 1].strip()
            except Exception:
                pass

            initial_content = f"An exception occurred in general Python code: {session.original_exception}\n\nFile: {filename}\nLine: {line_no}\nException Type: {type(session.original_exception).__name__}\nFailing code: {failing_line}\n\nPlease analyze the situation and use the available tools to recover from this exception. Use replace_code with the EXACT corrected version of the failing line."

        messages = [
            {
                "role": "user",
                "content": initial_content,
            }
        ]

        # Conversation loop
        max_iterations = 10  # Safety limit
        for iteration in range(max_iterations):
            print(f"\n🤖 Recovery conversation turn {iteration + 1}")

            # Get LLM response with tool calls
            response = await self._get_llm_response_with_tools(
                messages, system_prompt, session
            )

            # Check if recovery is complete
            if response.get("recovery_complete", False):
                print("✅ LLM indicates recovery is complete!")
                session.ready_to_continue = True
                return True

            # Add assistant response to conversation
            if response.get("message"):
                print(f"💬 Assistant: {response['message']}")
                messages.append({"role": "assistant", "content": response["message"]})

            # Handle tool calls
            if response.get("tool_calls"):
                tool_results = []
                for tool_call in response["tool_calls"]:
                    print(
                        f"🔧 Tool call: {tool_call['name']} with input: {tool_call.get('input', {})}"
                    )
                    result = await session.handle_tool_call(
                        tool_call["name"], tool_call.get("input", {})
                    )
                    print(f"📊 Tool result: {result}")
                    tool_results.append(
                        {"tool_use_id": tool_call.get("id", ""), "result": result}
                    )

                # Add tool results to conversation
                messages.append(
                    {
                        "role": "user",
                        "content": f"Tool results:\n{json.dumps(tool_results, indent=2)}",
                    }
                )
            else:
                # If no tool calls and no completion marker, something might be wrong
                if not response.get("recovery_complete") and response.get("message"):
                    # Encourage the LLM to use tools or call continue_workflow
                    messages.append(
                        {
                            "role": "user",
                            "content": "Please use the available tools to continue recovery or call continue_workflow when you have fixed the issue and want to return control to the original workflow.",
                        }
                    )

        print("❌ Recovery conversation reached maximum iterations")
        return False

    async def _get_llm_response_with_tools(
        self, messages: List[Dict], system_prompt: str, session: RecoverySession
    ) -> Dict[str, Any]:
        """Get LLM response with tool calling capabilities."""
        response = self.agent.client.messages.create(
            model=self.agent.model,
            max_tokens=4000,
            system=system_prompt,
            messages=messages,
            tools=RECOVERY_TOOLS,
            tool_choice={"type": "auto"},
        )

        result = {"message": "", "tool_calls": [], "recovery_complete": False}

        # Process response
        for content in response.content:
            if content.type == "text":
                result["message"] = content.text
            elif content.type == "tool_use":
                # Check if this is the completion marker
                if content.name == "continue_workflow":
                    result["recovery_complete"] = True
                    result["completion_reason"] = content.input.get(
                        "reason", "Recovery complete"
                    )
                    result["continue_action"] = content.input.get("action", "retry")
                else:
                    result["tool_calls"].append(
                        {"id": content.id, "name": content.name, "input": content.input}
                    )

        return result


async def handle_exception_with_recovery(exc_value, tb):
    """Handle an exception with unified recovery."""
    print(f"\n🔧 Handling exception with recovery: {exc_value}")

    # Find the most relevant execution frame (prioritize browser context if available)
    execution_frame = _find_best_execution_frame(tb or exc_value.__traceback__)

    if not execution_frame:
        print("❌ No suitable execution frame found for recovery")
        return False

    # Determine if we have browser context
    has_browser_context = _has_browser_context(execution_frame)

    # Get workflow code from environment which is set up in __main__.py
    original_workflow_code = os.environ.get(
        "VA_FINAL_WORKFLOW_CODE",  # Use final code if available
        os.environ.get("VA_WORKFLOW_CODE", ""),
    )

    recovery_session = RecoverySession(
        exc_value,
        execution_frame,
        original_workflow_code,
        has_browser_context,
    )

    # Run recovery agent
    recovery_agent = WorkflowRecoveryAgent()
    success = await recovery_agent.recover_from_exception(recovery_session)

    if success and recovery_session.ready_to_continue:
        # Store final code for printing
        final_code = recovery_session.get_final_workflow_code()
        os.environ["VA_FINAL_WORKFLOW_CODE"] = final_code
        print("✅ Unified recovery completed successfully")
        return True
    else:
        print("❌ Unified recovery failed")
        return False


def _find_best_execution_frame(exc_traceback):
    """Find the best execution frame for recovery (prefer browser context, fallback to any frame)."""
    browser_frame = None
    any_frame = None
    tb = exc_traceback

    while tb:
        tb_frame = tb.tb_frame
        any_frame = tb_frame  # Keep track of any frame

        # Look for browser context objects in frame locals
        if any(
            key in tb_frame.f_locals for key in ["page", "browser", "wrapped_context"]
        ):
            browser_frame = tb_frame
            print(f"🔍 Found browser context in frame: {tb_frame.f_code.co_name}")
            # If we find a page, prefer that frame
            if "page" in tb_frame.f_locals:
                break
        tb = tb.tb_next

    # Return browser frame if available, otherwise use the last frame in the traceback
    selected_frame = browser_frame or any_frame
    if selected_frame:
        print(
            f"🔍 Selected execution frame: {selected_frame.f_code.co_name} (browser context: {browser_frame is not None})"
        )

    return selected_frame


def _has_browser_context(frame):
    """Check if the frame has browser context objects."""
    return any(key in frame.f_locals for key in ["page", "browser", "wrapped_context"])
