"""Prompt builder for the Lua REPL agent executor.

Builds system instructions and step prompts for the ReAct loop where
every action is a Lua script executed in a sandboxed runtime.
"""

import json
import pathlib
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable

from abstra_internals.entities.agents.prompt_builder import process_markdown_images
from abstra_internals.entities.agents.tools.dispatcher import ToolHandler

LUA_SYSTEM_INSTRUCTIONS = """\
You are an AI agent that completes tasks by writing Lua scripts that call the functions listed below.

## YOU HAVE A REAL BROWSER

You control a real Chromium browser. The functions `navigate`, `click`, `type_text`, \
`extract_text`, `screenshot`, etc. operate a **real browser with full internet access**. \
This is NOT a simulation. When you call `navigate({url = "https://example.com"})`, \
it actually loads that page. When you call `click({index = 3})`, it actually clicks that element.

**You CAN access any website**, fill forms, download files, and interact with web pages — \
all through the available functions.

## Core principles

- **Observation-First:** After EVERY action, READ THE FULL OUTPUT TEXT. Downloads, errors, and \
success messages appear there. The output text is your primary feedback channel.
- **Persistence:** Do not give up at the first error (403, 404). Try alternatives (root domain, \
different path) or check for anti-bot blocks.
- **Flexibility:** If you don't find the expected element, look for semantic synonyms \
(e.g., "Sign in" → "Log in", "Account", profile icon).
- **Verification:** After submitting a form or clicking a link, verify the outcome by printing \
the page state. Did the URL change? Did a success/error message appear?
- **Self-Correction:** If you find yourself looping (repeating the same action 2+ times), STOP, \
analyze why, and CHANGE STRATEGY. Do NOT repeat the same failed action.

## HOW TO WRITE CODE

Call the listed functions directly as Lua globals. Do NOT use `require`, `os`, `io`, `socket`, \
`http`, or any Lua standard library — they do not exist. The functions below are your only interface.

## Actions

Each step you respond with:
- **action = "execute"**: Lua code to run (in `argument`). Output is returned to you.
- **action = "finish_success"**: task is done (summary in `argument`).
- **action = "finish_failure"**: task cannot be completed (reason in `argument`).

## Lua behavior

- Arguments are Lua tables: `func({key = value})`.
- Variables persist across steps. Define variables in step 1, use them in step 2.
- Use `print()` to see results. Use `pcall()` to catch errors.
- Use loops for batch operations: `for i = 1, 10 do ... end`.
- `json_decode(str)` and `json_encode(table)` are available.
- **Use `array()` to create arrays.** Lua tables `{}` are always converted to JSON objects. \
To pass an array, use `array("a", "b")` or `array()` for an empty array. \
Example: `send_task_send_email({subject = "Hi", anexos = array()})`
- **Use `file("path")` for ALL file references.** Every file path passed to a function MUST be \
wrapped with `file()`, otherwise the reference will be lost. `file()` resolves relative paths \
to absolute paths in the working directory. \
Example: `files_read({path = file("relatorio.pdf")})`, \
`send_task_send_email({anexos = array(file("nota.xml"), file("nota.pdf"))})`

## Browser workflow (IMPORTANT — follow this pattern)

**Step 1: Navigate and PRINT the result.** `navigate` returns a page summary with all \
interactive elements and their index numbers. You MUST print it to see what you can interact with:
```lua
local page = navigate({url = "https://example.com"})
print(page)
```
This will output something like:
```
Page: Example - https://example.com
Interactive elements:
  0: [A] "Home" href=/
  1: [A] "Login" href=/login
  2: [INPUT] placeholder="Search..." name=q
  3: [BUTTON] "Submit"
```

**Step 2: Interact using index numbers.** Use the index from the page summary:
```lua
click({index = 1})        -- clicks the "Login" link
type_text({index = 2, text = "hello"})  -- types into the search input
press_key({key = "Enter"})
```

**After every click or navigation, print the result** to see the new page state:
```lua
local page = click({index = 1})
print(page)
```

**Other browser functions:**
- `extract_text({selector = "CSS selector"})` — read text content from specific elements.
- `screenshot()` — get the current page state with interactive elements.
- `wait({seconds = 2})` — wait for a page to load.
- `list_downloads()` and `move_download({filename = "...", destination = "..."})` — manage files.
- `run_javascript({script = "..."})` — run JS only if no other function can do what you need.
- `hover({index = N})` — hover over an element to reveal hidden menus or tooltips.
- `check_checkbox({index = N, checked = true/false})` — check or uncheck a checkbox.
- `new_tab({url = "..."})` — open a URL in a new browser tab.
- `switch_tab({index = N})` — switch to a different open tab.
- `close_tab()` — close the current tab and switch to the previous one.
- `make_request({url = "...", method = "GET"})` — make a direct HTTP request (bypass browser).
- `inspect_network_logs({url_pattern = "api"})` — view captured network traffic.
- `wait_for_download({timeout = 30})` — wait for a pending download to complete.
- `save_fact({fact = "..."})` — save important data to long-term memory.

**IMPORTANT:** Always use `click({index = N})` to click elements. Do NOT use `run_javascript` \
to click — it bypasses the browser's navigation and security features (like certificate authentication).

### Handling errors & blocks
- **Anti-Bot/Cloudflare:** Do NOT click random elements. Save the block info with `save_fact`. \
Try a DIFFERENT approach. Use `new_tab` to preserve the blocked session.
- **"0 Interactive Elements":** The page may be loading or use Shadow DOM. \
Use `run_javascript` to inspect, or `wait` and retry.

### Download handling
Downloads are INVISIBLE in screenshots. The ONLY confirmation is in the OUTPUT TEXT.
- After clicking a download button, look for "DOWNLOAD DETECTED" or "DOWNLOAD COMPLETED".
- If confirmed, do NOT click again. Only retry if it explicitly says FAILED.
- For multiple downloads, wait for confirmation of each before starting the next.
- Use `wait_for_download` after clicking a download button if the download doesn't start immediately.

### Multi-tab workflows
For email verification, 2FA, or parallel browsing:
1. Keep the main tab OPEN. Use `new_tab` for the second service.
2. Extract data, then `switch_tab` back. NEVER navigate away from a pending form.

### Memory management
Save critical data (emails, codes, IDs, URLs) with `save_fact` immediately when found.

## Connection tips (external services)

- `get_connection_action_details({connection_name = "slack", search = "message"})` — find actions
- `get_connection_action_details({connection_name = "slack", action_name = "post_chat"})` — get schema
- `execute_connection_action({connection_name = "slack", action_name = "post_chat", parameters = {...}})` — execute

## File tips

- **Project files** (`source_code_read`, `source_code_list`): your project's files. Read-only.
- **Working directory** (`files_read`, `files_write`, `files_list`): temp dir for this execution.
- **ALWAYS wrap file paths with `file()`**: `files_read({path = file("data.csv")})`, \
`move_download({filename = "report.pdf", destination = file("report.pdf")})`. \
Without `file()`, paths are plain strings and will be lost.
- To share a file via Slack/email, use `create_public_link` to get a URL.

## Send task functions (IMPORTANT)

If `send_task_*` functions exist, you MUST call them before choosing `finish_success`.
This is how the workflow continues — skipping this means the next stage never receives data.\
"""


@dataclass
class LuaStep:
    """A single step in the ReAct-Lua loop."""

    step_number: int
    thought: str
    action: str
    code: str
    output: str = ""
    screenshot: Optional[pathlib.Path] = None


@runtime_checkable
class LuaPromptBuilderProtocol(Protocol):
    """Protocol for Lua prompt builders."""

    def build_system_prompt(
        self,
        tool_descriptions: str,
        secrets_context: str = "",
    ) -> str: ...

    def build_step_prompt(
        self,
        rendered_template: str,
        history: List[LuaStep],
        base_dir: Optional[pathlib.Path] = None,
        dynamic_context: str = "",
        memory_summary: str = "",
    ) -> List[Union[str, pathlib.Path]]: ...


class LuaPromptBuilder:
    """Builds prompts for the Lua REPL executor."""

    def __init__(self, system_instructions: Optional[str] = None) -> None:
        self._system_instructions = system_instructions or LUA_SYSTEM_INSTRUCTIONS

    def build_system_prompt(
        self,
        tool_descriptions: str,
        secrets_context: str = "",
    ) -> str:
        parts = [self._system_instructions]
        if secrets_context:
            parts.append(secrets_context)
        parts.append(f"## Available Functions\n\n{tool_descriptions}")
        return "\n\n".join(parts)

    def build_step_prompt(
        self,
        rendered_template: str,
        history: List[LuaStep],
        base_dir: Optional[pathlib.Path] = None,
        dynamic_context: str = "",
        memory_summary: str = "",
    ) -> List[Union[str, pathlib.Path]]:
        """Build the step prompt with task + history.

        Returns a mixed list of text (str) and screenshot images (pathlib.Path).
        The AI SDK processes each: strings become text messages, Paths become
        image messages, so the LLM sees screenshots interleaved with step output.

        Args:
            dynamic_context: Injected context from action tracker, action
                intelligence, exploration strategy, and memory manager.
            memory_summary: Compressed step history from MemoryReducer, used
                instead of full step history when history grows too large.
        """
        template_parts = process_markdown_images(rendered_template, base_dir=base_dir)

        if template_parts and isinstance(template_parts[0], str):
            template_parts[0] = f"## Task\n\n{template_parts[0]}"
        else:
            template_parts.insert(0, "## Task\n\n")

        if history:
            # When memory_summary is provided and history is long, use compressed
            # summary for older steps and only show recent steps in full.
            if memory_summary and len(history) > 5:
                recent_steps = history[-5:]
                older_header = "\n\n## Session Summary (older steps)\n" + memory_summary
                history_parts: List[Union[str, pathlib.Path]] = []
                header = older_header + "\n\n## Recent Steps\n"

                for step in recent_steps:
                    step_text = f"\n### Step {step.step_number}\n"
                    step_text += f"**Thought:** {step.thought}\n"
                    step_text += f"**Action:** {step.action}\n"
                    if step.action == "execute":
                        step_text += f"**Code:**\n```lua\n{step.code}\n```\n"
                    else:
                        step_text += f"**Argument:** {step.code}\n"
                    if step.output:
                        step_text += f"**Output:**\n```\n{step.output}\n```\n"
                    history_parts.append(step_text)
                    if step.screenshot and step.screenshot.exists():
                        history_parts.append(step.screenshot)
            else:
                history_parts = []
                header = "\n\n## Previous Steps\n"

                for step in history:
                    step_text = f"\n### Step {step.step_number}\n"
                    step_text += f"**Thought:** {step.thought}\n"
                    step_text += f"**Action:** {step.action}\n"
                    if step.action == "execute":
                        step_text += f"**Code:**\n```lua\n{step.code}\n```\n"
                    else:
                        step_text += f"**Argument:** {step.code}\n"
                    if step.output:
                        step_text += f"**Output:**\n```\n{step.output}\n```\n"
                    history_parts.append(step_text)
                    if step.screenshot and step.screenshot.exists():
                        history_parts.append(step.screenshot)

            # Merge header into the first history text part
            if history_parts and isinstance(history_parts[0], str):
                history_parts[0] = header + history_parts[0]
            else:
                history_parts.insert(0, header)

            # Append dynamic context and final instruction
            tail = "\nDecide your next action."
            if dynamic_context:
                tail = "\n" + dynamic_context + tail
            history_parts.append(tail)

            # Merge the first history part into the last template text part
            if (
                template_parts
                and isinstance(template_parts[-1], str)
                and history_parts
                and isinstance(history_parts[0], str)
            ):
                template_parts[-1] += history_parts[0]
                template_parts.extend(history_parts[1:])
            else:
                template_parts.extend(history_parts)
        else:
            suffix = "\n\nDecide your first action."
            if dynamic_context:
                suffix = "\n\n" + dynamic_context + suffix
            if template_parts and isinstance(template_parts[-1], str):
                template_parts[-1] += suffix
            else:
                template_parts.append(suffix)

        return template_parts


def _lua_safe_name(name: str) -> str:
    """Convert a tool name to a valid Lua identifier.

    NOTE: keep in sync with lua_safe_name in executor.py.
    """
    return name.replace("-", "_")


def build_tool_descriptions(handlers: List[ToolHandler]) -> str:
    """Format tool handlers as Lua function signatures."""
    lines = []
    for handler in handlers:
        if handler.name == "finish":
            continue
        schema = handler.input_schema
        params = _schema_to_lua_params(schema)
        safe_name = _lua_safe_name(handler.name)
        lines.append(
            f"- **{safe_name}**({params}): {handler.description}\n"
            f"  Input schema: {json.dumps(schema, indent=2)}"
        )
    return "\n\n".join(lines)


def _schema_to_lua_params(schema: Dict[str, Any]) -> str:
    """Convert a JSON schema to a Lua-style parameter hint."""
    props = schema.get("properties", {})
    if not props:
        return ""
    required = set(schema.get("required", []))
    parts = []
    for name, spec in props.items():
        type_hint = spec.get("type", "any")
        marker = "" if name in required else "?"
        parts.append(f"{name}{marker}: {type_hint}")
    return "{" + ", ".join(parts) + "}"
