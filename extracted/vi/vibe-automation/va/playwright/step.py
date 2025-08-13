import json
import logging
from typing import Any, Dict, Optional
from playwright.async_api import Page

from va.code import (
    inspect_with_block_from_frame,
    record_step_execution,
)
from va.constants import VA_DISABLE_FALLBACK
from ..agent.agent import Agent, create_user_message
from .web_agent import WebAgent
from .checkpoint import create_action_checkpoint, _extract_with_block_code

log = logging.getLogger("va.playwright")


def build_step_script_prompt(
    command: str,
    context: Dict[str, Any],
    accessibility_tree: Optional[str] = None,
) -> str:
    """Build the prompt for the LLM to generate Python code."""
    context_str = json.dumps(context, indent=2) if context else "{}"
    accessibility_section = (
        f"\n\nAccessibility Tree:\n{accessibility_tree}\n" if accessibility_tree else ""
    )

    return f"""
You are an expert Python automation engineer. Generate Python code to execute the following command on a web page using Playwright.

Command: {command}

Context dictionary: {context_str}{accessibility_section}

Context:
- You have access to a Playwright page object called 'page'
- You have access to a context dictionary called 'context' with the values shown above
- The page is already loaded and ready for interaction
- Generate code that uses standard Playwright methods like click(), fill(), select_option(), etc.
- The code should be executable Python that accomplishes the requested task
- Use the accessibility tree above to understand the page structure and identify elements

Requirements:
- Return your response as JSON in this exact format: {{"script": "# Python script here"}}
- The script should be complete and executable
- Use the 'page' variable for page interactions and 'context' dictionary for accessing values
- Access context values DIRECTLY using context["key"] syntax. For example, if context contains {{"email": "john@example.com"}}, use context["email"]
- Include error handling where appropriate
- Use async/await syntax for page interactions
- Use element selectors based on the accessibility tree when possible

Example response:
{{"script": "await page.fill('#username', context['username'])\\nawait page.click('#login-button')"}}

Generate the Python script now:
"""


async def call_llm_for_code_generation(agent: Agent, prompt: str) -> str:
    """Call the LLM to generate Python code based on the prompt."""
    try:
        # Create user message for the agent
        user_message = create_user_message(prompt)

        # Call the Anthropic API using the agent's client
        response = agent.client.messages.create(
            model=agent.model, max_tokens=4000, messages=[user_message]
        )

        # Extract the text content from the response
        if response.content and len(response.content) > 0:
            content = response.content[0]
            if hasattr(content, "text"):
                return content.text
            else:
                return str(content)
        else:
            return '{"script": "# No response from LLM"}'

    except Exception as e:
        log.error(f"Error calling LLM for code generation: {e}")
        return '{"script": "# Error calling LLM"}'


async def execute_script(
    script: str, context_vars: Dict[str, Any], page: Page
) -> Dict[str, Any]:
    """Execute the generated Python script with the page context."""
    try:
        # Prepare the execution context - pass context as a variable instead of unwrapping
        execution_context = {"page": page, "context": context_vars}

        # Check if the script contains await statements
        if "await " in script:
            # Wrap the script in an async function and execute it
            async_script = f"""
async def __execute_script():
{chr(10).join("    " + line for line in script.split(chr(10)))}

__result = __execute_script()
"""
            # Execute the script to define the function
            exec(compile(async_script, "<string>", "exec"), execution_context)

            # Get the coroutine and await it
            if "__result" in execution_context:
                await execution_context["__result"]
        else:
            # Execute synchronous script normally
            exec(script, execution_context)

        return {"success": True, "error": None}

    except Exception as e:
        return {"success": False, "error": str(e)}


async def execute_step(
    command: str,
    context: Optional[Dict[str, Any]],
    max_retries: int,
    page: Page,
    agent: Agent,
) -> Dict[str, Any]:
    """
    Execute a natural language command using interactive LLM conversation.

    This function now uses an interactive approach where the LLM can use tools
    to explore the page, test commands, and build the script incrementally.

    Parameters:
    -----------
    command (str): Natural language description of the action to perform
    context (Dict[str, Any], optional): Context variables available to the generated script
    max_retries (int): Maximum number of retry attempts (now used as max_turns)
    page (Any): The page to execute the command on
    agent (Agent): The agent to use for LLM calls

    Returns:
    --------
    Dict[str, Any]: Result containing success status, message, and generated script
    """
    if context is None:
        context = {}

    try:
        executor = WebAgent(page)
        return await executor.execute_interactive_step(command, context, max_retries)

    except Exception as e:
        log.error(f"Error in interactive step execution: {e}")
        return {
            "success": False,
            "message": f"Interactive step execution failed: {e}",
            "script": "",
            "attempt": 1,
        }


class AsyncStepContextManager:
    """Async context manager for Page.step method."""

    def __init__(self, page, command, context, max_retries, agent):
        self.page = page
        self.command = command
        self.context = context
        self.max_retries = max_retries
        self.agent = agent
        self.step_result = None

    async def __aenter__(self):
        # Check if we should pause for review before executing
        await self._check_for_review_pause()

        # Return the context dict so users can access variables
        return self.context

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Check if the with block is empty by examining the source code
        is_empty_block = self._is_with_block_empty()

        if is_empty_block:
            if VA_DISABLE_FALLBACK:
                log.info(
                    f"Empty with block detected but VA_DISABLE_FALLBACK is set, not generating code for: {self.command}"
                )
                raise RuntimeError(
                    f"page.step fallback is disabled by VA_DISABLE_FALLBACK environment variable for command: {self.command}"
                )

            log.info(
                f"Empty with block detected, triggering LLM action generation for: {self.command}"
            )
            # Use the pure function for step execution
            self.step_result = await execute_step(
                command=self.command,
                context=self.context,
                max_retries=self.max_retries,
                page=self.page,
                agent=self.agent,
            )

            # Log the step result
            if self.step_result and self.step_result.get("success"):
                script = self.step_result.get("script", "")
                log.info(
                    f"Step completed successfully: {self.step_result.get('message', 'No message')}"
                )
                if script:
                    log.info(f"Generated Python script:\n{script}")
                    # Replace the empty with block with the generated code
                    self._replace_empty_block_with_code(script)
            else:
                log.error(
                    f"Step failed: {self.step_result.get('message', 'No message')}"
                )
        else:
            # Handle predefined logic execution with exception handling
            if exc_type is not None:
                log.error(
                    f"Exception in predefined logic for step '{self.command}': {exc_val}"
                )
                if VA_DISABLE_FALLBACK:
                    log.info(
                        "VA_DISABLE_FALLBACK is set, not attempting to fix the exception"
                    )
                    # Return False to let the exception propagate
                    return False
                # Trigger web_agent to handle the exception and propose fixes
                await self._handle_predefined_logic_exception(exc_type, exc_val, exc_tb)
                # Return True to suppress the exception since we handled it
                return True
            else:
                self.step_result = {
                    "success": True,
                    "message": "Manual execution completed",
                    "script": "# Manual execution",
                    "attempt": 1,
                }

        return False  # Don't suppress exceptions

    async def _check_for_review_pause(self):
        """Check if the action requires review and pause if needed."""
        # Only run checkpoint if enabled on the page
        if self.page._checkpoint_review_callback is not None:
            await create_action_checkpoint(
                command=self.command, page=self.page, agent=self.agent
            )

    def _is_with_block_empty(self):
        """Check if the with block contains only pass or is empty using va.codegen."""
        try:
            # Frame offset explanation:
            # Frame 0: inspect_with_block_from_frame()
            # Frame 1: _is_with_block_empty() (this method)
            # Frame 2: AsyncStepContextManager.__aexit__()
            # Frame 3: User's "async with page.step(...)" statement ← TARGET
            #
            # We need frame_offset=3 to reach the user's actual with statement
            # that we want to inspect for empty blocks.
            inspector = inspect_with_block_from_frame(frame_offset=3)
            return inspector.is_with_block_empty()
        except Exception as e:
            log.debug(f"Error checking if with block is empty: {e}")
            # If we can't determine, assume it's not empty to be safe
            return False

    def _replace_empty_block_with_code(self, generated_script: str):
        """Record the executed code using the simplified recording system."""
        try:
            # Same frame offset logic as _is_with_block_empty():
            # We need frame_offset=3 to reach the user's "async with" statement
            # so we can record what was executed in that block.
            record_step_execution(
                executed_code=generated_script,
                context_dict=self.context,
                frame_offset=3,
            )

            log.info("Recorded step execution (will generate diff at exit)")
        except Exception as e:
            log.warning(f"Error during step execution recording: {e}")

    async def _handle_predefined_logic_exception(self, exc_type, exc_val, exc_tb):
        """Handle exceptions from predefined logic by triggering web_agent for exploration and fixes."""
        try:
            # Get the existing code from the with block
            inspector = inspect_with_block_from_frame(frame_offset=3)
            existing_code = _extract_with_block_code(inspector)

            # Create a detailed error context for the web_agent
            error_context = {
                "command": self.command,
                "exception_type": exc_type.__name__,
                "exception_message": str(exc_val),
                "existing_code": existing_code,
                "context_variables": self.context,
            }

            # Create a prompt for the web_agent to handle the exception
            error_handling_prompt = f"""
The following predefined automation code failed with an exception:

Command: {self.command}
Exception: {exc_type.__name__}: {exc_val}

Existing code:
{existing_code}

Context variables available: {list(self.context.keys())}

Please:
1. Explore the current page state to understand what went wrong
2. Analyze the exception and existing code to identify the root cause
3. Propose and implement a fixed version of the code
4. Test the fix to ensure it works properly

The fixed code should accomplish the original command while handling the error condition that occurred.
"""

            log.info(
                f"Triggering web_agent to handle exception in predefined logic: {exc_val}"
            )

            # Use WebAgent to handle the exception and propose fixes
            executor = WebAgent(self.page)
            result = await executor.execute_interactive_step(
                error_handling_prompt, error_context, self.max_retries
            )

            # If web_agent successfully generated a fix, replace the code
            if result.get("success") and result.get("script"):
                fixed_script = result.get("script")
                log.info(f"Web_agent proposed fix:\n{fixed_script}")

                # Record the fixed code using the simplified recording system
                record_step_execution(
                    executed_code=fixed_script,
                    context_dict=self.context,
                    frame_offset=3,
                )

                log.info("Recorded web_agent fix for failed code")
                self.step_result = {
                    "success": True,
                    "message": f"Exception handled by web_agent: {result.get('message', 'Fix applied')}",
                    "script": fixed_script,
                    "attempt": result.get("attempt", 1),
                    "original_exception": f"{exc_type.__name__}: {exc_val}",
                }
            else:
                log.error(
                    f"Web_agent failed to provide fix: {result.get('message', 'Unknown error')}"
                )
                self.step_result = {
                    "success": False,
                    "message": f"Web_agent failed to fix exception: {result.get('message', 'Unknown error')}",
                    "script": existing_code,
                    "original_exception": f"{exc_type.__name__}: {exc_val}",
                }

        except Exception as e:
            log.error(f"Error in exception handling: {e}")
            self.step_result = {
                "success": False,
                "message": f"Exception handling failed: {e}",
                "script": "# Exception handling failed",
                "original_exception": f"{exc_type.__name__}: {exc_val}",
            }

    def __getattr__(self, name):
        """Forward attribute access to delegate to page."""
        return getattr(self.page._playwright_page, name)
