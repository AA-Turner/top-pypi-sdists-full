"""
Checkpoint functionality for workflow verification and human-in-the-loop automation.

This module provides functionality to pause automation execution for human review
when potentially destructive actions (form submissions, navigation) are detected.
"""

import json
import logging

from pydantic import BaseModel, Field
from va.code import inspect_with_block_from_frame
from ..agent.agent import Agent
from ..review import review

log = logging.getLogger("va.playwright.checkpoint")


class ActionIntentResponse(BaseModel):
    """Pydantic model for LLM response about action intent."""

    will_submit_form: bool = Field(description="Whether the action will submit a form")
    will_navigate: bool = Field(
        description="Whether the action will navigate to a different page"
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0"
    )
    reasoning: str = Field(description="Explanation of the assessment")


class ActionIntentResult(BaseModel):
    """Result wrapper for action intent checking."""

    success: bool = Field(description="Whether the intent check was successful")
    intent: ActionIntentResponse | None = Field(
        default=None, description="The intent analysis if successful"
    )
    error: str | None = Field(default=None, description="Error message if unsuccessful")


async def check_action_intent(
    command: str, screenshot: str, code_context: str, agent: Agent
) -> ActionIntentResult:
    """Check if the action is likely to submit a form or navigate to a different page."""
    prompt = f"""
Analyze the following automation command and context to determine if it will likely:
1. Submit a form (clicking submit/save buttons, pressing Enter in forms, etc.)
2. Navigate to a different page (clicking links, changing URLs, etc.)

Command: {command}

Code context:
{code_context}

Based on the command and screenshot, respond with JSON in this exact format:
{{
    "will_submit_form": true/false,
    "will_navigate": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "explanation of your assessment"
}}

Look for keywords like:
- Form submission: "submit", "save", "send", "post", "confirm", "apply"
- Navigation: "click link", "go to", "navigate", "visit", "open page"
- Button/element types that typically cause navigation or submission

Consider the visual context from the screenshot when making your decision.
"""

    try:
        # Create user message with screenshot
        user_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": screenshot,
                    },
                },
            ],
        }

        # Call the LLM
        response = agent.client.messages.create(
            model=agent.model, max_tokens=1000, messages=[user_message]
        )

        # Extract response text
        if response.content and len(response.content) > 0:
            content = response.content[0]
            response_text = content.text if hasattr(content, "text") else str(content)

            # Parse JSON response using Pydantic
            try:
                # Handle JSON wrapped in markdown code blocks
                json_text = response_text.strip()
                if json_text.startswith("```json") and json_text.endswith("```"):
                    json_text = json_text[7:-3].strip()
                elif json_text.startswith("```") and json_text.endswith("```"):
                    json_text = json_text[3:-3].strip()

                result_dict = json.loads(json_text)
                intent = ActionIntentResponse(**result_dict)
                return ActionIntentResult(success=True, intent=intent)
            except (json.JSONDecodeError, ValueError) as e:
                log.warning(
                    f"Failed to parse LLM response as valid JSON/Pydantic model: {response_text}. Error: {e}"
                )
                # Fallback: check for keywords in response
                text_lower = response_text.lower()
                fallback_intent = ActionIntentResponse(
                    will_submit_form="submit" in text_lower or "form" in text_lower,
                    will_navigate="navigate" in text_lower or "page" in text_lower,
                    confidence=0.3,
                    reasoning="Fallback keyword analysis",
                )
                return ActionIntentResult(success=True, intent=fallback_intent)
        else:
            return ActionIntentResult(success=False, error="No response from LLM")

    except Exception as e:
        log.error(f"Error in action intent check: {e}")
        return ActionIntentResult(success=False, error=str(e))


async def create_action_checkpoint(
    command: str,
    page,
    agent: Agent,
    code_context: str = None,
) -> None:
    """
    Create a checkpoint that pauses execution for human review if the action
    is likely to submit a form or navigate to a different page.

    Args:
        command: The natural language command to execute
        page: The page object for taking screenshots
        agent: The agent for LLM calls
        code_context: Optional code context, will be extracted if not provided
    """
    try:
        # Take screenshot for LLM analysis
        screenshot_data = await page.screenshot()
        if isinstance(screenshot_data, bytes):
            import base64

            screenshot_data = base64.b64encode(screenshot_data).decode("utf-8")

        # Get code context if not provided
        if code_context is None:
            inspector = inspect_with_block_from_frame(
                frame_offset=4
            )  # Adjusted for new call stack
            code_context = (
                _extract_with_block_code(inspector)
                if inspector
                else "# No code context available"
            )

        # Call LLM to check action intent
        intent_check = await check_action_intent(
            command=command,
            screenshot=screenshot_data,
            code_context=code_context,
            agent=agent,
        )

        if (
            intent_check.success
            and intent_check.intent
            and (
                intent_check.intent.will_submit_form
                or intent_check.intent.will_navigate
            )
        ):
            intent = intent_check.intent

            log.info(
                f"Checkpoint triggered - Form submission: {intent.will_submit_form}, "
                f"Navigation: {intent.will_navigate}, Confidence: {intent.confidence}"
            )
            log.info(f"Reasoning: {intent.reasoning}")

            await page._checkpoint_review_callback(
                command, intent_check, screenshot_data, code_context
            )
            log.info(f"Checkpoint review completed for command: {command}")
        else:
            log.debug(f"No checkpoint needed for command: {command}")

    except Exception as e:
        log.error(f"Error during checkpoint creation: {e}")
        # Continue with execution even if checkpoint fails


def _extract_with_block_code(inspector):
    """Extract the actual code content from the with block."""
    try:
        # Read the source file
        with open(inspector.filename, "r") as f:
            source_lines = f.readlines()

        # Simple approach: find the with statement line and extract indented block
        target_line = inspector.line_number

        # Find the start of the with block body (line after the with statement)
        start_line = target_line  # Start from the with statement line

        # Look for the first indented line after the with statement
        with_indent = None
        body_lines = []

        for i, line in enumerate(source_lines[start_line:], start_line):
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                continue

            # Determine the indentation level of the with block body
            if with_indent is None:
                # This should be the first line of the with block body
                with_indent = len(line) - len(line.lstrip())
                body_lines.append(line)
            elif line.startswith(" " * with_indent) or line.startswith("\t"):
                # This line is part of the with block body
                body_lines.append(line)
            else:
                # We've reached the end of the with block
                break

        if body_lines:
            # Remove common leading whitespace
            import textwrap

            body_code = "".join(body_lines)
            return textwrap.dedent(body_code).strip()
        else:
            return "# Empty with block"

    except Exception as e:
        log.debug(f"Error extracting with block code: {e}")
        return f"# Error extracting code: {e}"


async def default_checkpoint_callback(command, intent_result, screenshot, code_context):
    """
    Default checkpoint callback that creates a review and waits for user completion.

    Args:
        command: The command being executed
        intent_result: ActionIntentResult from the LLM analysis
        screenshot: Base64 encoded screenshot
        code_context: Code context from the with block
    """
    if not intent_result.intent:
        log.warning("No intent data available for checkpoint review")
        return

    intent = intent_result.intent

    # Create review with detailed information
    review_instruction = f"""
Checkpoint Review Required:

Command: {command}
Will submit form: {intent.will_submit_form}
Will navigate: {intent.will_navigate}
Confidence: {intent.confidence:.2f}
Reasoning: {intent.reasoning}

Code context:
{code_context}

Please review the action and approve to continue or modify as needed.
"""

    # Create review and wait for completion
    r = review(
        key=f"checkpoint-{hash(command) % 10000}",
        instruction=review_instruction,
        artifacts=[{"type": "screenshot", "data": screenshot}],
    )
    await r.wait(timeout=600)  # 10 minute timeout
    log.info(f"Checkpoint review completed for command: {command}")
