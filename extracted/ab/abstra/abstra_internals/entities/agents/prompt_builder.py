"""Prompt builder for agent ReAct execution.

Builds system instructions and step prompts for each iteration
of the ReAct loop, including tool descriptions and conversation history.
"""

import base64
import pathlib
import re
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

SYSTEM_INSTRUCTIONS = """\
You are an AI agent that completes tasks by reasoning step-by-step and using tools.

For each step, you must:
1. Think briefly about what to do next (keep it short)
2. Choose a tool to use (or 'finish' if done)
3. Provide ALL required input parameters for that tool

## Critical rules

- Use the tools listed in "Available Tools" below. Check each tool's input_schema for required parameters.
- If a tool fails with a schema/validation error, do NOT retry it — move on to the next step of the task.
- If a tool fails for other reasons (timeout, element not found), try a different approach.
- Be efficient: minimize the number of steps. Batch operations when possible.
- Keep your reasoning concise — do not repeat previous observations.
- When you have completed the task (or done as much as possible), use 'finish' with a summary.

## Core principles

- **Observation-First:** After EVERY action, READ THE FULL OBSERVATION TEXT. Downloads, errors, and success messages appear there. The observation text is your primary feedback channel.
- **Persistence:** Do not give up at the first error (403, 404). Try alternatives (root domain, different path) or check for anti-bot blocks.
- **Flexibility:** If you don't find the expected element, look for semantic synonyms (e.g., "Sign in" → "Log in", "Account", profile icon).
- **Verification:** After submitting a form or clicking a link, verify the outcome. Did the URL change? Did a success/error message appear in the observation?
- **Resourcefulness:** If standard actions (click, type) fail, use `run_javascript` to manipulate the DOM directly.

## Self-correction

- If you find yourself looping (repeating the same action 2+ times):
  1. STOP and analyze why the action is failing.
  2. CHANGE STRATEGY: try a different element, a different tool (e.g. run_javascript), or a different URL.
  3. Do NOT repeat the same failed action hoping for a different result.

## Images

If the task includes images, you can see them directly — they are part of this conversation.
You do NOT need any tool to analyze, describe, or extract text from images.
Just look at the image and respond based on what you see.

## Browser tools

If you have browser tools, you CAN and SHOULD use them to navigate websites, click elements, type text, and interact with web pages.

Tips for efficiency:
- When downloading multiple files, do all downloads first, then move them all at the end.
- Use `run_javascript` for repetitive actions (e.g., clicking all download buttons programmatically).
- After `move_download`, you don't need to call `list_downloads` — the observation already confirms success.
- Use `extract_text` with a CSS selector to read page content (tables, lists). Always provide the `selector` parameter.

### Handling errors & blocks
- **Anti-Bot/Cloudflare ("Attention Required", "Just a moment", CAPTCHA):**
  1. Do NOT click random elements. Save the block information with `save_fact`.
  2. Try a DIFFERENT service provider or approach immediately.
  3. Use `new_tab` to preserve the blocked session while trying alternatives.
- **"0 Interactive Elements":**
  1. The page may be loading, use iframes, or use Shadow DOM.
  2. Use `run_javascript` to inspect: `document.querySelectorAll('*').length`.
  3. Use `wait` and retry — the system will re-extract elements automatically.

### Download handling
Downloads are INVISIBLE on screenshots. The ONLY confirmation is in the OBSERVATION TEXT.
- After clicking a download button, look for "DOWNLOAD DETECTED" or "DOWNLOAD COMPLETED" in the observation.
- If the observation confirms the download, the file is saved — do NOT click again.
- Only retry if the observation explicitly says the download FAILED.
- For multiple downloads, wait for confirmation of each before starting the next.

### Multi-tab workflows
For tasks requiring email verification, 2FA, or parallel browsing:
1. Keep the main tab OPEN (e.g. a registration form).
2. Open the second service (email, authenticator) in a `new_tab`.
3. Extract the code/link, then `switch_tab` back.
4. NEVER navigate away from a pending form.

### Memory management
When you find emails, codes, IDs, URLs, or other key data during browsing, save it using `save_fact` right away. Do not rely on your conversation history to retain it across many steps.

## Connection tools (external services like Slack, Salesforce, etc.)

To interact with external services (Slack, Salesforce, etc.), use these two tools:
- `get_connection_action_details`: discover available actions and get their parameter schemas
- `execute_connection_action`: run an action

Typical flow:
1. `get_connection_action_details(connection_name="slack", search="message|chat")` → find the right action name
2. `get_connection_action_details(connection_name="slack", action_name="post_chat")` → get the parameter schema
3. `execute_connection_action(connection_name="slack", action_name="post_chat", parameters={...})` → execute

You can skip step 1 if you already know the exact action name, and skip step 2 if you already know the parameters.

## File tools

There are two separate file locations:
- **Project files** (`source_code_read`, `source_code_list`): your project's files (images, configs, scripts). Read-only. Use these to access files referenced in the task (e.g. "logo.png").
- **Working directory** (`files_read`, `files_write`, `files_list`): a temporary directory for files YOU create or download during execution. Starts empty.

To share a file (image, PDF, etc.) via Slack or email, use `create_public_link` to get a public URL, then include that URL in your message.

## Send task tools (IMPORTANT)

If you have `send_task_*` tools available, you MUST use them to forward results to the next stage BEFORE calling 'finish'.
This is how the workflow continues — if you skip this step, the next stage will never receive the data.
Always provide the required fields according to the tool's schema (check its input_schema).\
"""


# Matches markdown images with base64 data URIs: ![alt](data:image/...;base64,...)
_BASE64_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(data:image/(\w+);base64,([A-Za-z0-9+/=\s]+)\)"
)

# Matches markdown images with relative file paths (not URLs, not base64)
_IMAGE_EXTENSIONS = r"\.(?:png|jpe?g|gif|webp|svg|bmp|ico)"
_RELATIVE_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(([^):\s]+?" + _IMAGE_EXTENSIONS + r')(?:\s+"[^"]*")?\)'
)


def process_markdown_images(
    text: str,
    base_dir: Optional[pathlib.Path] = None,
) -> List[Union[str, pathlib.Path]]:
    """Extract images from markdown, return mixed list of text and image paths.

    Handles two kinds of markdown images:
    - Base64 data URIs: decoded and saved to temp files.
    - Relative file paths: resolved against base_dir (if provided).

    Returns a list of text segments (str) and image file paths (pathlib.Path)
    interleaved, so the prompt SDK can process them as multimodal content.

    Example:
        ["some text", Path("/tmp/abc123.png"), "more text"]
    """
    # Collect all image matches (base64 and relative) sorted by position
    image_matches: List[tuple] = []  # (start, end, path_or_none)

    for match in _BASE64_IMAGE_RE.finditer(text):
        ext = match.group(1)
        b64_data = match.group(2).replace("\n", "").replace("\r", "").replace(" ", "")
        try:
            image_bytes = base64.b64decode(b64_data)
            tmp = tempfile.NamedTemporaryFile(
                suffix=f".{ext}", delete=False, prefix="agent_img_"
            )
            tmp.write(image_bytes)
            tmp.flush()
            tmp.close()
            image_matches.append((match.start(), match.end(), pathlib.Path(tmp.name)))
        except Exception as e:
            print(
                f"[AGENT] Warning: Failed to decode base64 image "
                f"(position {match.start()}): {e}. "
                f"The image will be skipped from the prompt."
            )

    if base_dir is not None:
        for match in _RELATIVE_IMAGE_RE.finditer(text):
            # Skip if this region overlaps with a base64 match
            if any(s <= match.start() < e for s, e, _ in image_matches):
                continue
            rel_path = match.group(1)
            abs_path = base_dir / rel_path
            if abs_path.is_file():
                image_matches.append((match.start(), match.end(), abs_path))
            else:
                print(
                    f"[AGENT] Warning: Image '{rel_path}' referenced in the "
                    f"prompt was not found at '{abs_path}'. "
                    f"Make sure the file exists next to the .md template. "
                    f"The image will be sent as text instead of visual content."
                )

    image_matches.sort(key=lambda x: x[0])

    if not image_matches:
        return [text]

    parts: List[Union[str, pathlib.Path]] = []
    last_end = 0

    for start, end, img_path in image_matches:
        before = text[last_end:start].strip()
        if before:
            parts.append(before)
        parts.append(img_path)
        last_end = end

    after = text[last_end:].strip()
    if after:
        parts.append(after)

    return parts if parts else [text]


@dataclass
class ReActStep:
    """A single step in the ReAct loop."""

    step_number: int
    thought: str
    action: str
    action_input: Dict[str, Any]
    observation: str = ""


class AgentPromptBuilder:
    """Builds prompts for the ReAct loop."""

    def __init__(self, system_instructions: Optional[str] = None) -> None:
        self._system_instructions = system_instructions or SYSTEM_INSTRUCTIONS

    def build_system_prompt(
        self,
        tool_descriptions: str,
        secrets_context: str = "",
    ) -> str:
        parts = [self._system_instructions]
        if secrets_context:
            parts.append(secrets_context)
        parts.append(f"## Available Tools\n\n{tool_descriptions}")
        return "\n\n".join(parts)

    def build_step_prompt(
        self,
        rendered_template: str,
        history: List[ReActStep],
        base_dir: Optional[pathlib.Path] = None,
        dynamic_context: str = "",
        memory_summary: str = "",
    ) -> List[Union[str, pathlib.Path]]:
        """Build the step prompt, returning a list of text (str) and image paths (Path).

        Images in the rendered template (base64 or relative paths) are resolved
        so the prompt SDK can process them as multimodal content. Image paths
        are pathlib.Path objects so they are not confused with text segments.

        Args:
            dynamic_context: Injected context from action tracker, action
                intelligence, exploration strategy, and memory manager.
            memory_summary: Compressed step history from MemoryReducer, used
                instead of full step history when history grows too large.
        """
        # Process the template to extract images into file paths
        template_parts = process_markdown_images(rendered_template, base_dir=base_dir)

        # Prepend task header to first text part
        if template_parts and isinstance(template_parts[0], str):
            template_parts[0] = f"## Task\n\n{template_parts[0]}"
        else:
            template_parts.insert(0, "## Task\n\n")

        # Build history suffix as plain text
        history_text = ""
        if history:
            # When memory_summary is provided and history is long, use the
            # compressed summary for older steps and only show recent steps in full.
            if memory_summary and len(history) > 5:
                history_text += "\n\n## Session Summary (older steps)\n"
                history_text += memory_summary
                history_text += "\n\n## Recent Steps\n"
                for step in history[-5:]:
                    history_text += (
                        f"\n### Step {step.step_number}\n"
                        f"**Thought:** {step.thought}\n"
                        f"**Action:** {step.action}\n"
                        f"**Observation:** {step.observation}"
                    )
            else:
                history_text += "\n\n## Previous Steps\n"
                for step in history:
                    history_text += (
                        f"\n### Step {step.step_number}\n"
                        f"**Thought:** {step.thought}\n"
                        f"**Action:** {step.action}\n"
                        f"**Observation:** {step.observation}"
                    )
            # Inject dynamic context (action tracker, intelligence, etc.) before the
            # final instruction so the LLM considers it when deciding the next action.
            if dynamic_context:
                history_text += "\n\n" + dynamic_context
            history_text += "\n\nBased on the previous steps, decide your next action."
        else:
            history_text += "\n\nDecide your first action."

        # Append history to last text part
        if template_parts and isinstance(template_parts[-1], str):
            template_parts[-1] += history_text
        else:
            template_parts.append(history_text)

        return template_parts
