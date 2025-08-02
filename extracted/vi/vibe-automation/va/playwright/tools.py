import re
import logging
import base64
from mcp import types

log = logging.getLogger("va.playwright.tools")


# Core set of tools provided by our Playwright page, shared between the MCP server and the neural fallback agent.
# all the tool names directly map to the corresponding Playwright method with parameters, reducing boilerplate.
PLAYWRIGHT_TOOLS = [
    types.Tool(
        name="get_page_snapshot",
        description="Get AI-optimized page structure. Use this first to understand what you're working with.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    types.Tool(
        name="inspect_element",
        description="Inspect an element by coordinates. Use this to get the element's ref. The result looks similar to Chrome DevTools' element inspector.",
        inputSchema={
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "X coordinate of the element",
                },
                "y": {
                    "type": "integer",
                    "description": "Y coordinate of the element",
                },
                "num_ancestors": {
                    "type": "integer",
                    "description": "Number of ancestors to inspect",
                    "default": 3,
                },
            },
            "required": ["x", "y"],
        },
    ),
    types.Tool(
        name="inspect_html",
        description="Inspect an element by coordinates and optionally its ancestors, returning the raw HTML of the element. Use this to help get locator strings for elements.",
        inputSchema={
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "X coordinate of the element",
                },
                "y": {
                    "type": "integer",
                    "description": "Y coordinate of the element",
                },
                "num_ancestors": {
                    "type": "integer",
                    "description": "Number of ancestors to inspect",
                    "default": 3,
                },
                "max_characters": {
                    "type": "integer",
                    "description": "Maximum characters in response.",
                    "default": 1024,
                },
            },
            "required": ["x", "y"],
        },
    ),
    types.Tool(
        name="find_element_by_ref",
        description="Find element by ref from snapshot. Use refs from page snapshots to locate elements precisely.",
        inputSchema={
            "type": "object",
            "properties": {
                "ref": {
                    "type": "string",
                    "description": "Element ref (e.g., 'e3')",
                }
            },
            "required": ["ref"],
        },
    ),
    types.Tool(
        name="get_page_screenshot",
        description="Take screenshot for visual understanding. Use when you need to see the page visually.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
]

PLAYWRIGHT_TOOL_NAMES = [tool.name for tool in PLAYWRIGHT_TOOLS]


# Generic tools that work with the page but aren't strictly Playwright-specific
GENERIC_TOOLS = [
    types.Tool(
        name="execute_python_command",
        description="Execute Python code to interact with the page. You can use page.get_by_ref('ref_value') directly in your code - it will be automatically resolved to the correct locator. Supports multi-line code for complex operations. After successful execution, returns updated screenshot and page snapshot.",
        inputSchema={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Python code to execute (supports multiple lines)",
                }
            },
            "required": ["command"],
        },
    ),
    types.Tool(
        name="report_result",
        description="Report the final result of a task with structured information. Use this when you've completed finding an element or performing an action to provide the result in a structured format.",
        inputSchema={
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Whether the task was completed successfully",
                },
                "result_type": {
                    "type": "string",
                    "description": "Type of result (e.g., 'locator', 'action', 'information')",
                },
                "code": {
                    "type": "string",
                    "description": "The code snippet or locator expression (e.g., page.get_by_role('button', name='Search'))",
                },
                "description": {
                    "type": "string",
                    "description": "Human-readable description of what was found or done",
                },
            },
            "required": ["success", "result_type"],
        },
    ),
]


async def _handle_get_page_snapshot(page, arguments):
    """Handler for get_page_snapshot tool."""
    result = await page.snapshot_for_ai()
    return [types.TextContent(type="text", text=result)]


async def _handle_inspect_element(page, arguments):
    """Handler for inspect_element tool."""
    x = arguments.get("x", 0)
    y = arguments.get("y", 0)
    num_ancestors = arguments.get("num_ancestors", 3)
    result = await page.inspect_element(x, y, num_ancestors)
    return [types.TextContent(type="text", text=str(result))]


async def _handle_inspect_html(page, arguments):
    """Handler for inspect_html tool."""
    x = arguments.get("x", 0)
    y = arguments.get("y", 0)
    num_ancestors = arguments.get("num_ancestors", 3)
    max_characters = arguments.get("max_characters", 1024)
    result = await page.inspect_html(x, y, num_ancestors, max_characters)
    return [types.TextContent(type="text", text=str(result))]


async def _handle_find_element_by_ref(page, arguments):
    """Handler for find_element_by_ref tool."""
    ref = arguments.get("ref", "")
    try:
        locator = page.locator(f"aria-ref={ref}")
        if await locator.count() > 0:
            locator_string = await locator.generate_locator_string()
            result = f"page.{locator_string}"
        else:
            result = "Element not found"
    except Exception as e:
        result = f"Error finding element: {e}"
    return [types.TextContent(type="text", text=result)]


async def _handle_get_page_screenshot(page, arguments):
    """Handler for get_page_screenshot tool."""
    try:
        screenshot_bytes = await page.screenshot()
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
        return [
            types.ImageContent(
                type="image", data=screenshot_base64, mimeType="image/png"
            )
        ]
    except Exception as e:
        error_msg = f"Error taking screenshot: {e}"
        return [types.TextContent(type="text", text=error_msg)]


async def _resolve_get_by_ref_calls(page, command):
    """
    Find and replace all page.get_by_ref() calls with actual locators.

    Args:
        page: The Playwright page object
        command: The Python command string containing potential get_by_ref calls

    Returns:
        The command with all get_by_ref calls replaced with actual locators
    """
    # Pattern to match page.get_by_ref("ref_value") or await page.get_by_ref('ref_value')
    pattern = r'((?:await\s+)?page\.get_by_ref\(["\']([^"\']+)["\']\))'

    # Find all matches
    matches = list(re.finditer(pattern, command))

    # If no matches, return original command
    if not matches:
        return command

    # Log that we found get_by_ref calls
    log.debug(f"Found {len(matches)} page.get_by_ref() calls to resolve")

    # Process matches in reverse order to maintain string positions
    modified_command = command
    for match in reversed(matches):
        full_match = match.group(1)
        ref_value = match.group(2)

        try:
            # Use the existing find_element_by_ref logic
            locator = page.locator(f"aria-ref={ref_value}")
            if await locator.count() > 0:
                locator_string = await locator.generate_locator_string()
                # Replace the get_by_ref call with the actual locator
                # Preserve 'await' if it was present
                if "await" in full_match:
                    replacement = f"await page.{locator_string}"
                else:
                    replacement = f"page.{locator_string}"

                # Replace in the command
                start, end = match.span(1)
                modified_command = (
                    modified_command[:start] + replacement + modified_command[end:]
                )
                log.debug(f"Replaced page.get_by_ref('{ref_value}') with {replacement}")
            else:
                # If element not found, leave it as is (will fail during execution)
                log.warning(
                    f"Element with ref '{ref_value}' not found, leaving get_by_ref call as is"
                )
        except Exception:
            # If any error, leave the original call (will fail during execution)
            pass

    return modified_command


async def _handle_execute_python_command(page, arguments, context=None):
    """Handler for execute_python_command tool with optional context support."""
    command = arguments.get("command", "")
    try:
        # Resolve any page.get_by_ref() calls to actual locators
        resolved_command = await _resolve_get_by_ref_calls(page, command)

        # Create execution context with captured output
        captured_output = []
        execution_context = {
            "page": page,
            "print": lambda *args: captured_output.append(
                " ".join(str(arg) for arg in args)
            ),
        }

        # Add context if provided (used by web agent)
        if context is not None:
            execution_context["context"] = context

        result = None
        # Handle async commands
        if "await " in resolved_command:
            # Wrap in async function and capture return value
            async_command = f"""
async def __execute_command():
    {resolved_command.replace(chr(10), chr(10) + "    ")}
    
__result = __execute_command()
"""
            exec(compile(async_command, "<string>", "exec"), execution_context)
            if "__result" in execution_context:
                result = await execution_context["__result"]
        else:
            # Execute synchronous command and capture return value
            result = exec(resolved_command, execution_context)

        # Build response message
        response_parts = []

        # If we resolved any get_by_ref calls, show the resolved command
        if resolved_command != command:
            response_parts.append(f"Resolved command: {resolved_command}")

        if captured_output:
            response_parts.append("Output: " + "\n".join(captured_output))
        if result is not None:
            response_parts.append(f"Return value: {result}")
        if not response_parts:
            response_parts.append("Command executed successfully")

        success_msg = f"Success: True\n{chr(10).join(response_parts)}"

        # Prepare response content - start with empty list
        response_content = []

        # Collect all text parts
        text_parts = [success_msg]

        # After successful execution, include updated screenshot and snapshot
        screenshot_included = False
        try:
            # Capture screenshot
            screenshot_bytes = await page.screenshot()
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            response_content.append(
                types.ImageContent(
                    type="image", data=screenshot_base64, mimeType="image/png"
                )
            )
            screenshot_included = True
        except Exception as e:
            log.warning(f"Failed to capture post-execution screenshot: {e}")

        try:
            # Capture snapshot if size is reasonable
            snapshot = await page.snapshot_for_ai()
            # Limit snapshot to ~50KB (approximately 50,000 characters)
            if len(snapshot) <= 50000:
                text_parts.append(f"\n\nUpdated page structure:\n```\n{snapshot}\n```")
            else:
                log.info(
                    f"Post-execution snapshot too large ({len(snapshot)} chars), excluding from response"
                )
        except Exception as e:
            log.warning(f"Failed to capture post-execution snapshot: {e}")

        # Combine all text parts into a single text content
        combined_text = "\n".join(text_parts)

        # If we have a screenshot, add text first then image
        if screenshot_included:
            response_content.insert(
                0, types.TextContent(type="text", text=combined_text)
            )
        else:
            # Only text content
            response_content = [types.TextContent(type="text", text=combined_text)]

        return response_content
    except Exception as e:
        error_msg = f"Success: False\nError executing command: {e}"
        return [types.TextContent(type="text", text=error_msg)]


# Dictionary mapping tool names to their handler functions
PLAYWRIGHT_TOOL_HANDLERS = {
    "get_page_snapshot": _handle_get_page_snapshot,
    "inspect_element": _handle_inspect_element,
    "inspect_html": _handle_inspect_html,
    "find_element_by_ref": _handle_find_element_by_ref,
    "get_page_screenshot": _handle_get_page_screenshot,
}


async def _handle_report_result(page, arguments):
    """Handler for report_result tool."""
    success = arguments.get("success", False)
    result_type = arguments.get("result_type", "")
    code = arguments.get("code", "")
    description = arguments.get("description", "")

    # Format the result message
    result_parts = [f"Result Type: {result_type}"]
    result_parts.append(f"Success: {success}")

    if code:
        result_parts.append(f"Code: {code}")

    if description:
        result_parts.append(f"Description: {description}")

    result_message = "\n".join(result_parts)

    return [types.TextContent(type="text", text=result_message)]


# Dictionary mapping generic tool names to their handler functions
GENERIC_TOOL_HANDLERS = {
    "execute_python_command": _handle_execute_python_command,
    "report_result": _handle_report_result,
}

# Combined handlers dictionary
ALL_TOOL_HANDLERS = {**PLAYWRIGHT_TOOL_HANDLERS, **GENERIC_TOOL_HANDLERS}
