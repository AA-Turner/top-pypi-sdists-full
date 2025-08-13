import base64
import json
import logging
from typing import Any, Dict, List, Optional, Type
from dataclasses import dataclass
from pydantic import BaseModel
from playwright.async_api import Page
from ..agent.agent import Agent
from .tools import PLAYWRIGHT_TOOLS, GENERIC_TOOLS, ALL_TOOL_HANDLERS
from mcp import types
from .extract_schemas import FormVerification

log = logging.getLogger("va.playwright.web_agent")


# Utility functions to convert between MCP types and Anthropic format
def mcp_tool_to_anthropic_tool(mcp_tool: types.Tool) -> Dict[str, Any]:
    """Convert MCP Tool to Anthropic tool format."""
    return {
        "name": mcp_tool.name,
        "description": mcp_tool.description,
        "input_schema": mcp_tool.inputSchema,
    }


def mcp_content_to_anthropic_content(
    mcp_content: List[types.TextContent | types.ImageContent],
) -> Any:
    """Convert MCP content to Anthropic format."""
    if len(mcp_content) == 1:
        content = mcp_content[0]
        if isinstance(content, types.TextContent):
            return content.text
        elif isinstance(content, types.ImageContent):
            return [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": content.mimeType,
                        "data": content.data,
                    },
                }
            ]
    # For multiple content items, properly format each one
    return [
        {"type": "text", "text": content.text}
        if isinstance(content, types.TextContent)
        else {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": content.mimeType,
                "data": content.data,
            },
        }
        for content in mcp_content
    ]


# Convert all tools to Anthropic format
TOOLS = [
    *(mcp_tool_to_anthropic_tool(tool) for tool in PLAYWRIGHT_TOOLS + GENERIC_TOOLS),
]


def build_system_prompt(command: str, context: Dict[str, Any]) -> str:
    """Build the system prompt for the interactive executor."""
    context_str = json.dumps(context, indent=2) if context else "{}"

    return f"""You are an expert web automation engineer helping to execute this command with Playwright: "{command}"

Context variables available: {context_str}

You have access to the following tools:
1. get_page_snapshot() - Get the current page structure as an AI-optimized accessibility tree
2. execute_python_command(command) - Execute Python code to interact with the page (automatically includes updated screenshot and snapshot after successful execution). You can execute multiple lines of code in a single call.
3. find_element_by_ref(ref) - Find an element by its ref from the snapshot and get a locator string
4. get_page_screenshot() - Take a screenshot of the current page
5. report_result(success, result_type, code, description) - Report the final result of your task with structured information

Note:
- The initial screenshot and/or page structure snapshot may be included with this message for your reference.
- After each successful execute_python_command, you'll automatically receive an updated screenshot and page snapshot (if size permits), so you don't need to call get_page_screenshot() or get_page_snapshot() after executing commands.

Your goal is to:
1. If a page structure is provided, review it; otherwise use get_page_snapshot() to understand the page
2. Identify the elements you need to interact with
3. Test different approaches using execute_python_command()
4. Build up the final script gradually, testing each step
5. Use refs from the snapshot to locate elements precisely
6. ALWAYS end by calling report_result() with success=True/False and relevant details

Guidelines:
- The execute_python_command tool automatically provides updated screenshot and page snapshot after successful execution
- You can execute multiple lines of code in a single execute_python_command call - this is more efficient than making multiple tool calls
- Use refs directly in your Python code with page.get_by_ref("ref_value") - for example:
  await page.get_by_ref("e123").click()
  await page.get_by_ref("e456").fill("text")
  This is more efficient than calling find_element_by_ref separately
- For multi-step operations, combine them in a single execute_python_command when they're logically related:
  ```
  # Good: Multiple related actions in one call
  await page.get_by_ref("e10").click()  # Open dropdown
  await page.get_by_text("Option A").click()  # Select option
  ```
- Test each command or command group before adding it to the final script
- Keep track of the resolved locators shown in "Resolved command:" output
- Build the script incrementally, verifying each step works
- Use context variables with context["key"] syntax, don't directly use the variable value directly since we want the generated code to be reusable.
- Always use async/await for page interactions
- Prefer to use Playwright native methods to achieve the task, instead of using page.evaluate with custom JavaScript code.
- IMPORTANT: When you need data that is not available in the context, throw an error describing what information is missing
- DO NOT use placeholder or dummy data (like "example@email.com", "John Doe", "123-456-7890") - instead throw an error
- If context is missing required information, fail immediately with a clear error message describing what is needed
- IMPORTANT: Your final script should use the resolved locators (e.g., page.get_by_label("Submit")) not the ref-based calls (e.g., page.get_by_ref("e123"))
- You don't need to call get_page_screenshot() or get_page_snapshot() after execute_python_command since they're included automatically
- You don't need to close dropdowns, date pickers, or dialogs after completing your task - just complete the requested action

IMPORTANT: You MUST conclude every task by calling report_result() with:
- success: True if you successfully completed the task, False if you failed
- result_type: Type of result (e.g., 'locator', 'action', 'information', 'script')
- code: Any relevant code or locator expression you found/used
- description: Human-readable description of what was accomplished or what failed
- Do not provide any additional response after calling report_result() - the task is complete once you report the result

NOTE that Python Playwright APIs uses snake_case naming such as select_option instead of selectOption.

IMPORTANT: In your final script, use the resolved locators from the "Resolved command" output, NOT the original page.get_by_ref() calls. For example:
- If you tested: await page.get_by_ref("e50").click()
- And got: Resolved command: await page.get_by_label("Date").click()
- Use in final script: await page.get_by_label("Date").click()

This makes the final script more readable and doesn't depend on dynamic ref values.

Start by examining any provided context (screenshot and/or page structure), then proceed with your analysis."""


def build_extract_system_prompt() -> str:
    """Build the system prompt for the interactive executor to extract data from the page."""

    return """You are extracting content on behalf of a user.
If a user asks you to extract a 'list' of information, or 'all' information,
YOU MUST EXTRACT ALL OF THE INFORMATION THAT THE USER REQUESTS.

    You will be given:
    1. An instruction
    2. A list of DOM elements (snapshot) to extract from.
    3. (Optional) A screenshot of the page.

    Print the exact text from the DOM+accessibility tree elements with all symbols, characters, and endlines as is. Do not add any additional text or formatting.
    If a screenshot is provided, you must cross-reference the information with the screenshot.


    If you are given a schema, you must extract the data in the schema format.
    If you are not given a schema, you must extract the data in the format of the DOM+accessibility tree elements.
    
    Print an empty string if no new information is found.
    """


def build_extract_vision_system_prompt() -> str:
    """Build the system prompt for the vision-based extractor."""

    return """You are extracting content from visual information in screenshots.
If a user asks you to extract a 'list' of information, or 'all' information,
YOU MUST EXTRACT ALL OF THE INFORMATION THAT THE USER REQUESTS.

    You will be given:
    1. An instruction
    2. A screenshot of the webpage
    
    Focus on visual elements and their relationships:
    - Text content and its visual presentation
    - Layout and positioning of elements
    - Colors, styles, and visual hierarchies
    - Visual patterns and groupings
    - Images, icons, and visual indicators
    
    Describe visual elements precisely, including:
    - Location (top, bottom, left, right, center)
    - Visual properties (size, color, font, emphasis)
    - Spatial relationships between elements
    
    If you are given a schema, you must extract the data in the schema format.
    If you are not given a schema, describe what you see in natural language.
    
    Print an empty string if no relevant visual information is found.
    """


@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation."""

    role: str  # "user", "tool" or "assistant"
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None
    tool_name: Optional[str] = None  # Only if role is tool


class WebAgent(Agent):
    """
    Web automation agent that allows the LLM to gradually build a script
    by using tools to explore and interact with the page.
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.conversation_history: List[ConversationTurn] = []
        self.final_script = ""
        self.working_script_lines: List[str] = []

    def add_conversation_turn(
        self,
        role: str,
        content: str,
        tool_calls=None,
        tool_results=None,
        tool_name=None,
    ):
        """Add a turn to the conversation history and print it immediately."""
        turn = ConversationTurn(
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_results=tool_results,
            tool_name=tool_name,
        )
        self.conversation_history.append(turn)

        # Stream the conversation turn immediately
        self._print_conversation_turn(len(self.conversation_history), turn)

    def _print_conversation_turn(
        self,
        turn_number: int,
        turn: ConversationTurn,
        log_level: str = "debug",
    ):
        """Print a single conversation turn in a formatted way."""

        if log_level == "debug":
            log_fn = log.debug
        else:
            log_fn = log.info

        log_fn(f"\n--- Turn {turn_number}: {turn.role.upper()} {turn.tool_name} ---")

        if turn.content:
            log_fn(f"Content: {turn.content}")

        if turn.tool_calls:
            log_fn("Tool Calls:")
            for j, tool_call in enumerate(turn.tool_calls, 1):
                log_fn(f"  {j}. {tool_call.name}")
                if hasattr(tool_call, "input") and tool_call.input:
                    for key, value in tool_call.input.items():
                        # Truncate long values for readability
                        display_value = str(value)
                        if len(display_value) > 100:
                            display_value = display_value[:97] + "..."
                        log_fn(f"     {key}: {display_value}")

        if turn.tool_results:
            log_fn("Tool Results:")
            for j, result in enumerate(turn.tool_results, 1):
                result_content = result.get("content", "No content")

                # Replace image data fields with [redacted] to avoid cluttering output
                if isinstance(result_content, list):
                    filtered_content = []
                    for item in result_content:
                        if isinstance(item, dict) and item.get("type") == "image":
                            # Keep the structure but replace the data field
                            filtered_item = item.copy()
                            if "source" in filtered_item and isinstance(
                                filtered_item["source"], dict
                            ):
                                filtered_source = filtered_item["source"].copy()
                                if "data" in filtered_source:
                                    filtered_source["data"] = "[redacted]"
                                filtered_item["source"] = filtered_source
                            filtered_content.append(filtered_item)
                        else:
                            filtered_content.append(item)
                    result_content = filtered_content

                # Truncate long results for readability
                result_str = str(result_content)
                if len(result_str) > 200:
                    result_str = result_str[:197] + "..."
                log_fn(f"  {j}. {result_str}")

    async def process_anthropic_tool_call(
        self, tool_call, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a single Anthropic tool call and return the result."""
        tool_name = tool_call.name
        arguments = tool_call.input

        try:
            if tool_name in ALL_TOOL_HANDLERS:
                # Use centralized tool handlers
                handler = ALL_TOOL_HANDLERS[tool_name]

                # For execute_python_command, add context support and handle working script
                if tool_name == "execute_python_command":
                    # Use centralized handler with context support
                    mcp_content = await handler(self.page, arguments, context)
                    anthropic_content = mcp_content_to_anthropic_content(mcp_content)

                    # Add successful commands to our working script
                    command = arguments.get("command", "")
                    # Check for success in the content
                    success_detected = False
                    if isinstance(anthropic_content, str):
                        success_detected = "Success: True" in anthropic_content
                    elif isinstance(anthropic_content, list):
                        # Check first text content for success message
                        for item in anthropic_content:
                            if isinstance(item, dict) and item.get("type") == "text":
                                if "Success: True" in item.get("text", ""):
                                    success_detected = True
                                    break

                    if not command.strip().startswith("print") and success_detected:
                        self.working_script_lines.append(command)

                    return {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": anthropic_content,
                    }
                else:
                    # Use the centralized handler for other tools
                    mcp_content = await handler(self.page, arguments)
                    anthropic_content = mcp_content_to_anthropic_content(mcp_content)
                    return {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": anthropic_content,
                    }

            else:
                return {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": f"Unknown tool: {tool_name}",
                }

        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": f"Error: {e}",
            }

    def build_messages(
        self,
        command: str,
        context: Dict[str, Any],
        initial_screenshot_base64: Optional[str] = None,
        initial_snapshot: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Build the message history for the LLM (Anthropic format)."""
        # Build initial message content
        initial_content = []
        initial_content.append(
            {"type": "text", "text": f"Please execute this command: {command}"}
        )

        # Add snapshot if provided
        if initial_snapshot:
            initial_content.append(
                {
                    "type": "text",
                    "text": f"\n\nHere is the current page structure:\n```\n{initial_snapshot}\n```",
                }
            )

        # Add screenshot if provided
        if initial_screenshot_base64:
            initial_content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": initial_screenshot_base64,
                    },
                }
            )

        messages = [{"role": "user", "content": initial_content}]

        # Add conversation history
        # Note: Old screenshots/snapshots from execute_python_command are cleaned up
        # to save context space, keeping only success messages and resolved commands
        # Find the last execute_python_command turn to preserve its screenshot/snapshot
        last_execute_python_turn_index = -1
        for i in range(len(self.conversation_history) - 1, -1, -1):
            turn = self.conversation_history[i]
            if (
                turn.role == "tool"
                and turn.tool_name
                and "execute_python_command" in turn.tool_name
            ):
                last_execute_python_turn_index = i
                break

        for i, turn in enumerate(self.conversation_history):
            if turn.role == "assistant":
                content = []
                if turn.content:
                    content.append({"type": "text", "text": turn.content})

                # Add tool calls
                if turn.tool_calls:
                    for tool_call in turn.tool_calls:
                        content.append(
                            {
                                "type": "tool_use",
                                "id": tool_call.id,
                                "name": tool_call.name,
                                "input": tool_call.input,
                            }
                        )

                messages.append({"role": "assistant", "content": content})

            elif turn.role == "tool":
                # Tool results are added as user messages in Anthropic format
                if turn.tool_results:
                    content = []
                    for tool_result in turn.tool_results:
                        # Clean up screenshots and snapshots from old execute_python_command results
                        # but preserve the most recent one
                        should_clean = (
                            turn.tool_name
                            and "execute_python_command" in turn.tool_name
                            and i
                            != last_execute_python_turn_index  # Don't clean the last one
                        )

                        if should_clean:
                            cleaned_content = self._clean_old_screenshots_and_snapshots(
                                tool_result["content"]
                            )
                        else:
                            cleaned_content = tool_result["content"]

                        content.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_result["tool_use_id"],
                                "content": cleaned_content,
                            }
                        )
                    messages.append({"role": "user", "content": content})

            elif turn.role == "user":
                messages.append({"role": "user", "content": turn.content})

        return messages

    def _clean_old_screenshots_and_snapshots(self, content):
        """
        Remove screenshots and page snapshots from old tool results to save context space.
        Keep only the text content (success/error messages and resolved commands).
        """
        if isinstance(content, str):
            # If it's a string, check if it contains page structure and remove it
            if "Updated page structure:" in content:
                # Split on the page structure marker and keep only the part before it
                parts = content.split("\n\nUpdated page structure:")
                return parts[0]  # Keep only the success message and resolved command
            return content
        elif isinstance(content, list):
            # If it's a list, filter out image content and page structure text
            filtered_content = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "image":
                        # Skip image content (screenshots)
                        continue
                    elif item.get("type") == "text":
                        text = item.get("text", "")
                        if "Updated page structure:" in text:
                            # Remove page structure from text content
                            parts = text.split("\n\nUpdated page structure:")
                            if parts[
                                0
                            ].strip():  # Only keep if there's meaningful content
                                filtered_content.append(
                                    {"type": "text", "text": parts[0]}
                                )
                        else:
                            # Keep other text content (success messages, resolved commands)
                            filtered_content.append(item)
                    else:
                        # Keep other types as-is
                        filtered_content.append(item)
                else:
                    # Keep non-dict items as-is
                    filtered_content.append(item)

            # If we filtered everything out, return a simple success message
            if not filtered_content:
                return "Command executed successfully"

            return filtered_content
        else:
            # For other types, return as-is
            return content

    async def execute_interactive_step(
        self, command: str, context: Dict[str, Any], max_turns: int = 20
    ) -> Dict[str, Any]:
        """
        Execute a step using interactive conversation with the LLM.

        Parameters:
        -----------
        command (str): The natural language command to execute
        context (Dict[str, Any]): Context variables
        max_turns (int): Maximum number of conversation turns

        Returns:
        --------
        Dict[str, Any]: Result with success status and final script
        """
        # Capture initial screenshot and snapshot to include in the first message
        initial_screenshot_base64 = None
        initial_snapshot = None
        if len(self.conversation_history) == 0:
            try:
                screenshot_bytes = await self.page.screenshot()
                initial_screenshot_base64 = base64.b64encode(screenshot_bytes).decode(
                    "utf-8"
                )
            except Exception as e:
                log.warning(f"Failed to capture initial screenshot: {e}")

            try:
                # Get page snapshot and check its size
                snapshot = await self.page.snapshot_for_ai()
                # Limit snapshot to ~50KB (approximately 50,000 characters)
                if len(snapshot) <= 50000:
                    initial_snapshot = snapshot
                else:
                    log.info(
                        f"Page snapshot too large ({len(snapshot)} chars), excluding from initial message"
                    )
            except Exception as e:
                log.warning(f"Failed to capture initial snapshot: {e}")

        consecutive_empty_responses = 0
        max_consecutive_empty = (
            3  # Allow up to 3 consecutive empty responses before giving up
        )
        report_result_called = False
        report_result_success = False

        for turn in range(max_turns):
            try:
                # Build messages for this turn
                messages = self.build_messages(
                    command, context, initial_screenshot_base64, initial_snapshot
                )
                # Clear initial screenshot and snapshot after first use
                initial_screenshot_base64 = None
                initial_snapshot = None

                # Call the LLM
                try:
                    # Log request details for debugging if we get empty responses
                    total_message_length = sum(len(str(msg)) for msg in messages)
                    log.debug(
                        f"Sending request to LLM: {len(messages)} messages, ~{total_message_length} chars total"
                    )

                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=4000,
                        messages=messages,
                        tools=TOOLS,
                        system=build_system_prompt(command, context),
                    )

                    log.debug(
                        f"LLM response received: content_length={len(response.content) if response.content else 0}"
                    )
                except Exception as api_error:
                    log.error(f"LLM API call failed: {api_error}")
                    raise

                # Process response
                if response.content:
                    # Reset empty response counter on successful response
                    consecutive_empty_responses = 0

                    assistant_content = ""
                    tool_calls = []

                    # Process each content block
                    for content in response.content:
                        if content.type == "text":
                            assistant_content += content.text
                        elif content.type == "tool_use":
                            tool_calls.append(content)
                        else:
                            log.warning(
                                f"Unknown content type in response: {content.type}"
                            )

                    # Check if we got content but it's all empty
                    if not assistant_content and not tool_calls:
                        log.warning(
                            f"Response had {len(response.content)} content blocks but no text or tool calls"
                        )
                        for i, content in enumerate(response.content):
                            log.warning(
                                f"  Content block {i}: type={content.type}, text='{getattr(content, 'text', '')}'"
                            )

                    # Check for tool calls
                    if tool_calls:
                        self.add_conversation_turn(
                            "assistant", assistant_content, tool_calls=tool_calls
                        )

                        # Process each tool call
                        tool_results = []
                        for tool_call in tool_calls:
                            result = await self.process_anthropic_tool_call(
                                tool_call, context
                            )
                            tool_results.append(result)

                        # Add tool results to conversation
                        self.add_conversation_turn(
                            "tool",
                            "",
                            tool_results=tool_results,
                            tool_name=", ".join(
                                tool_call.name for tool_call in tool_calls
                            ),
                        )

                        # Check if report_result was called - if so, we're done
                        for tool_call in tool_calls:
                            if (
                                hasattr(tool_call, "name")
                                and tool_call.name == "report_result"
                            ):
                                # Set flag to terminate the conversation after report_result
                                report_result_called = True
                                # Check if it was successful
                                if hasattr(tool_call, "input") and tool_call.input.get(
                                    "success"
                                ):
                                    report_result_success = True
                                break
                    else:
                        # No tool calls, just add the response
                        self.add_conversation_turn("assistant", assistant_content)
                elif response.stop_reason == "end_turn" and not report_result_called:
                    # Ask the LLM to call report_result to properly conclude the conversation
                    log.info(
                        "Prompting LLM to call report_result after stop_reason='end_turn'"
                    )
                    self.add_conversation_turn(
                        "user",
                        "Please call the report_result tool to indicate whether the task was completed successfully or not. Include the final script and a description of what was accomplished.",
                    )
                    continue
                else:
                    # Log the full response object to help debug empty responses
                    log.warning(
                        f"No content in LLM response. Full response: {response}"
                    )

                    if report_result_called:
                        break

                    consecutive_empty_responses += 1
                    if consecutive_empty_responses >= max_consecutive_empty:
                        log.error(
                            f"Got {consecutive_empty_responses} consecutive empty responses, giving up"
                        )
                        break

                    # Add a small delay before retrying to handle potential rate limiting
                    import asyncio

                    await asyncio.sleep(1)
                    continue

            except Exception as e:
                # Log the error but continue to next turn
                log.error(f"Error in conversation turn {turn}: {e}")
                # Add error message to conversation to inform the LLM
                self.add_conversation_turn(
                    "user", f"An error occurred: {e}. Please try a different approach."
                )
                continue

            # Break out of main loop if report_result was called
            if report_result_called:
                break

        # report_result_called is already properly tracked in the main loop

        # Return the result - only consider successful if report_result was called with success=True
        if report_result_called:
            fallback_script = "\n".join(self.working_script_lines)
            return {
                "success": report_result_success,
                "message": "Interactive step completed with report_result"
                + (" (successful)" if report_result_success else " (failed)"),
                "script": self.final_script or fallback_script,
                "conversation_turns": len(self.conversation_history),
                "conversation_history": self.conversation_history,
            }
        else:
            # No report_result call - mark as failure
            fallback_script = "\n".join(self.working_script_lines)
            return {
                "success": False,
                "message": "Interactive step completed but no report_result was called",
                "script": self.final_script or fallback_script,
                "conversation_turns": len(self.conversation_history),
                "conversation_history": self.conversation_history,
            }

    async def extract(
        self,
        prompt: str,
        schema: Optional[Type[BaseModel]] = None,
        include_screenshot: bool = False,
    ) -> Any:
        """
        Extract data from the page using natural language.
        """
        # Get accessibility tree
        snapshot = await self.page.snapshot_for_ai()  # type: ignore

        # Setup content for the LLM call
        content = (
            f"""Instruction: {prompt} DOM+accessibility tree (snapshot): {snapshot}"""
        )

        # If include_screenshot is True, capture and include the screenshot
        if include_screenshot:
            try:
                screenshot_bytes = await self.page.screenshot(full_page=True)
                screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

                # Create content with both text and image
                content_list = [
                    {"type": "text", "text": content + " \n Screenshot: "},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": screenshot_base64,
                        },
                    },
                ]
            except Exception as e:
                log.warning(f"Failed to capture screenshot for extraction: {e}")
                content_list = [{"type": "text", "text": content}]
        else:
            content_list = [{"type": "text", "text": content}]

        # If schema is provided, use structured output
        if schema:
            response = self.instructor_client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": content_list}],
                system=build_extract_system_prompt(),
                response_model=schema,  # specify output format
            )
            return response
        else:
            # Simple text extraction
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": content_list}],
                system=build_extract_system_prompt(),
            )
            # Extract text from TextBlock object
            return response.content[0].text

    async def extract_vision_only(
        self,
        prompt: str,
        schema: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """
        Extract data from the page using only visual information from screenshot.
        Similar to extract() but relies purely on visual analysis rather than DOM structure.

        Parameters:
        -----------
        prompt (str): The natural language instruction for what to extract
        schema (Optional[Type[BaseModel]]): Optional Pydantic model to structure the output

        Returns:
        --------
        Any: Extracted data, either as raw text or structured according to schema
        """
        try:
            # Capture full page screenshot
            screenshot_bytes = await self.page.screenshot(full_page=True)
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            # Create content with instruction and screenshot
            content_list = [
                {
                    "type": "text",
                    "text": f"Instruction: {prompt}\nAnalyze the following screenshot: ",
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": screenshot_base64,
                    },
                },
            ]
        except Exception as e:
            log.error(f"Failed to capture screenshot for vision extraction: {e}")
            raise

        # If schema is provided, use structured output
        if schema:
            response = self.instructor_client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": content_list}],
                system=build_extract_vision_system_prompt(),
                response_model=schema,  # specify output format
            )
            return response
        else:
            # Simple text extraction
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": content_list}],
                system=build_extract_vision_system_prompt(),
            )
            # Extract text from TextBlock object
            return response.content[0].text

    async def verify_form_values(self, expected_form_data: str) -> FormVerification:
        """
        Verify if the form values match with the expected form data.
        Using snapshot only.
        """

        result = await self.extract(
            f"""Expected form data: {expected_form_data}

After normalization (ignoring formats), do expected form data values match with the values in the page snapshot?
CRITICAL: You MUST normalize values before comparing them. Remove all formatting characters (dashes, spaces, parentheses, dots, etc.) and compare only the core alphanumeric content.

IMPORTANT: You should be matching form values, not form structures/keys.
If the snapshot has an empty/placeholder field that is filled in expected form data, it is a missing value and considered a mismatch.
For dropdowns, focus only on the SELECTED option. If the selected option is empty/placeholder/wrong, it is a mismatch even if the correct value is available for selection.

They are only not matching if:
1. there are conflicting field values between them after normalization. e.g. a field in snapshot shows different core values with expected form data.
2. there are missing/unfilled values in snapshot. E.g. expected form data has values, but snapshot shows empty/placeholder values

Examples of MATCHES (should return form_match_expected: true):
    - One expected data field value is split into multiple elements on the snapshot, vice versa.
    - Formatting differences in values - these are ALWAYS matches when core content is the same:
        - Tax ID: "912913457" vs "912-91-3457" (same numbers, different formatting) ✓ MATCH
        - Tax ID: "912-91-3457" vs "912 91 3457" (same numbers, different formatting) ✓ MATCH
        - Tax ID: "912.91.3457" vs "912-91-3457" (same numbers, different formatting) ✓ MATCH
        - Phone: "5551234567" vs "(555) 123-4567" (same numbers, different formatting) ✓ MATCH
        - Phone: "555-123-4567" vs "555.123.4567" (same numbers, different formatting) ✓ MATCH
        - ZIP: "12345" vs "12345-6789" (same first 5 digits) ✓ MATCH
        - Date: "01/15/2024" vs "1/15/24" (same date, different format) ✓ MATCH
        - Currency: "$1,234.56" vs "1234.56" (same amount, different formatting) ✓ MATCH
        - SSN: "123456789" vs "123-45-6789" (same numbers, different formatting) ✓ MATCH
        - Account numbers: "1234567890" vs "1234-5678-90" (same numbers, different formatting) ✓ MATCH

Examples of NON-MATCHES (should return form_match_expected: false):
    - Missing values: e.g. expected form data has State: Texas, but snapshot shows "Please select a state"
    - Wrong values: e.g. expected form data has '12345' while snapshot has '123456' (different numbers)
    - Extra conflicting fields: snapshot has an extra field that conflicts with expected form data
    - Completely different values: "John Doe" vs "Jane Smith" (different names)
    - Different core numbers: "912913457" vs "912913458" (different tax ID numbers)

REMEMBER: Always strip formatting and compare only the core alphanumeric content. If the core content is identical, it's a MATCH regardless of formatting.""",
            schema=FormVerification,
        )
        return result
