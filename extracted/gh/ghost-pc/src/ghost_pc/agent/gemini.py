"""GhostPC Agent definition using Google ADK.

Builds the full multi-agent topology:
  Root (Router) ─── gemini-3-flash, cheap intent classification
    ├── ChatAgent ─── gemini-3-flash, conversational (no tools)
    ├── SimpleExecutor ─── gemini-3-flash (native CU), single-action desktop tasks
    └── ComplexTaskPipeline ─── SequentialAgent for multi-step tasks
          ├── TaskPlanner ─── flash + thinking, breaks task into steps
          ├── StepExecutor ─── LoopAgent
          │     ├── ActionAgent ─── gemini-3-flash (native CU), stateless executor
          │     └── StepAdvancer ─── flash, checks result + advances
          └── TaskSummarizer ─── flash, summarizes what was accomplished

Each agent has the appropriate model, tools, and include_contents setting.
All models default to gemini-3-flash-preview and can be overridden via env vars.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools.computer_use.computer_use_toolset import ComputerUseToolset
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from ghost_pc.agent.desktop_computer import DesktopComputer
from ghost_pc.agent.tools import (
    click_label,
    double_click_at,
    find_files,
    get_open_windows,
    inspect_ui,
    list_files,
    manage_window,
    open_application,
    read_clipboard,
    read_text_file,
    right_click_at,
    run_terminal,
    send_screenshot_to_user,
    set_reminder,
    switch_to_window,
    task_complete,
    type_into_label,
    uia_click,
    uia_get_value,
    uia_type,
    write_clipboard,
)

if TYPE_CHECKING:
    from ghost_pc.agent.action_loop import AgentRunner
    from ghost_pc.config.settings import Settings

# ── Gemini 3 generate config ─────────────────────────────────────────────────
# Gemini 3's reasoning engine is optimized for temperature=1.0.
# Lowering it causes looping or degraded performance in complex tasks.
_GENERATE_CONFIG = types.GenerateContentConfig(temperature=1.0)

# ── Default models ──────────────────────────────────────────────────────────
# Used when no Settings object is provided (backward compat).
_DEFAULT_MODEL = "gemini-3-flash-preview"

# ── Static instruction (cached by Gemini, never changes) ────────────────────
STATIC_INSTRUCTION = """\
You are GhostPC, an AI agent that has full control of a Windows desktop computer.
The user is chatting with you remotely (via WhatsApp or a web viewer on their phone).
You see their screen through screenshots and can perform any action on it.

## Your Capabilities
1. **Vision**: You see the user's live screen through screenshots after every action.
2. **Mouse**: Click, double-click, right-click, hover, scroll, drag-and-drop anywhere.
3. **Keyboard**: Type text, press key combinations (Ctrl+C, Alt+Tab, etc.).
4. **Terminal**: Run PowerShell/cmd commands directly via the run_terminal tool.
5. **Apps**: Launch any installed Windows application via open_application. \
Smart discovery: focuses existing windows instead of opening duplicates, \
discovers installed apps automatically (not limited to a hardcoded list). \
Some apps support protocol deep-links (discord://, spotify://, vscode://) \
— use run_terminal('start <protocol-url>') when you need to open a specific \
page or resource inside an app.
6. **Windows**: List, focus, minimize, maximize, or close any open window.
7. **Screenshots**: Send the current screen to the user via send_screenshot_to_user.
8. **Clipboard**: Read/write the system clipboard via read_clipboard/write_clipboard.
9. **Files**: Browse and read files via list_files, find_files, read_text_file.
10. **UIA Controls**: Inspect and interact with UI elements by name via inspect_ui, \
uia_click, uia_type, uia_get_value for more reliable interaction than pixel clicking.
11. **Label Clicking**: click_label(#) and type_into_label(#, text) — click numbered \
SoM labels drawn on annotated screenshots. Most precise method when labels are visible.

## Click Behavior — Be Smart About It
- **Single click** (click_at): Select items, press buttons, focus input fields, click links.
- **Double-click** (double_click_at): Open files, folders, desktop icons, select words in text.
- **Right-click** (right_click_at): Open context menus (copy/paste, properties, new folder, etc.).

You MUST choose the correct click type based on context.

## Structured UI Interaction
Screenshots are annotated with numbered labels (#0, #1, #2, ...) on interactive controls.
When these labels are visible, use them for precise interaction:
- click_label(5) — clicks the element at label #5, most precise method.
- type_into_label(3, "hello") — focuses label #3 and types text into it.

When labels aren't available or you know the control name, use:
- uia_click("Save") — finds control by name, no coordinate guessing.
- uia_type("Filename", "report.pdf") — types into a named input field.
- uia_get_value("Status") — reads control values without screenshots.

Fall back to visual clicking only when neither labels nor UIA names cover the target.

## Fallback Chain (prefer top, fall back down)
1. API tool (COM automation, terminal command) — fastest, most reliable
2. Label click (click_label, type_into_label) — precise, uses known coordinates from SoM
3. UIA-guided click (uia_click, uia_type) — structured, by control name
4. Visual click (click_at with coordinates) — works everywhere, least precise
5. Ask the user — when stuck or unsure

## Guidelines
- Be concise — the user is on their phone. Short messages are better.
- After each action, look at the new screenshot to verify it worked.
- For multi-step tasks, do one step at a time and check the result.
- If you're unsure where to click, describe what you see and ask.
- For text-heavy content (emails, documents), summarize rather than reading verbatim.
- If something goes wrong, explain what happened and try an alternative approach.
- When you finish a task, call task_complete with a brief summary.

## Safety Rules
- NEVER execute dangerous terminal commands (format, del /s, rm -rf, etc.).
- NEVER access or modify system files, registry, or boot configuration.
- NEVER send the user's personal data (passwords, private files) in chat.
- If a command seems destructive, refuse and explain why.

## IMPORTANT: No Browser
- You are in desktop-first mode. Do NOT open web browsers or navigate to URLs.
- Do NOT call search(), navigate(), or open_web_browser() — they are disabled.
- When the user asks to open an app (Discord, Slack, Spotify, etc.), use open_application
  to launch the native desktop app, then use switch_to_window to focus it.
- If the app is already open, use get_open_windows to find it and switch_to_window to focus it.

## Efficiency Tips
- Use keyboard shortcuts when faster than clicking.
- Use the terminal for file operations instead of clicking through Explorer.
- Use switch_to_window instead of Alt+Tab for reliable window switching.
- If an app needs time to load, use the wait action before taking the next step.
"""


def _dynamic_instruction(ctx: Any) -> str:
    """Generate context-aware instruction additions based on session state.

    Called on every LLM invocation. Reads temp state to adapt behavior
    to the currently active app and available UI controls.
    """
    parts: list[str] = []
    state = ctx.state if hasattr(ctx, "state") else {}

    # ── Adapt to active application (knowledge base) ──
    active_app = state.get("temp:active_app", "")
    if active_app:
        from ghost_pc.agent.app_knowledge import get_app_hints

        hints = get_app_hints(active_app)
        if hints:
            parts.append(hints)
        else:
            # Generic fallback for unknown apps
            app_lower = active_app.lower()
            if any(kw in app_lower for kw in ("word", "winword", "excel", "outlook", "powerpoint")):
                parts.append(
                    "Office app detected. Prefer COM API tools or terminal commands "
                    "over clicking for document operations."
                )

    # ── UIA controls available — inline the list ──
    uia_controls = state.get("temp:uia_controls")
    if uia_controls:
        # Truncate to keep prompt reasonable
        controls_text = str(uia_controls)
        if len(controls_text) > 2000:
            controls_text = controls_text[:2000] + "\n... (truncated)"
        parts.append(
            "Labeled UI controls detected on screenshot. "
            "Use click_label(#) for fastest interaction, "
            "uia_click('name') if you know the control name, "
            "click_at(x,y) as last resort.\n\n"
            f"```\n{controls_text}\n```"
        )

    # ── OCR results available — inline the text ──
    ocr_results = state.get("temp:ocr_results")
    if ocr_results and not uia_controls:
        # Only show OCR if UIA didn't provide controls (avoid duplication)
        ocr_text = str(ocr_results)
        if len(ocr_text) > 1500:
            ocr_text = ocr_text[:1500] + "\n... (truncated)"
        parts.append(
            "OCR text detected on screen (no labeled controls available). "
            "Use coordinates from OCR data with click_at(x,y).\n\n"
            f"```\n{ocr_text}\n```"
        )

    # ── Previous session context ──
    session_summary = state.get("user:session_summary")
    if session_summary:
        parts.append(f"Previous session summary (for context):\n{session_summary}")

    return "\n\n".join(parts) if parts else ""


def _build_desktop_tools(
    computer: DesktopComputer,
    runner: AgentRunner | None = None,
) -> list[Any]:
    """Build the complete tool list for desktop-capable agents."""
    return [
        # ADK's ComputerUseToolset — auto-wraps all BaseComputer methods as tools
        ComputerUseToolset(computer=computer),
        # Memory
        PreloadMemoryTool(),
        # Custom click variants (not in BaseComputer)
        double_click_at,
        right_click_at,
        # Window management
        get_open_windows,
        switch_to_window,
        manage_window,
        # Terminal & apps
        run_terminal,
        open_application,
        # Communication
        send_screenshot_to_user,
        task_complete,
        # Clipboard
        read_clipboard,
        write_clipboard,
        # Filesystem
        list_files,
        find_files,
        read_text_file,
        # UIA interaction
        inspect_ui,
        uia_click,
        uia_type,
        uia_get_value,
        # Label-based interaction (SoM bridge)
        click_label,
        type_into_label,
        # Reminders (Phase 4)
        set_reminder,
    ]


# ── Router instruction ──────────────────────────────────────────────────────
ROUTER_INSTRUCTION = """\
You are the GhostPC router. Your ONLY job is to classify the user's intent and
delegate to the right specialist agent. Do NOT try to perform actions yourself.

Classification rules:
- **CHAT**: Questions, casual conversation, jokes, time, weather, general knowledge.
  Examples: "what time is it?", "tell me a joke", "who won the game?"
  → Transfer to chat_agent

- **SIMPLE**: Single desktop actions that need 1-2 steps.
  Examples: "open Chrome", "click the start menu", "type hello", "take a screenshot",
  "minimize this window", "what's on my clipboard?"
  → Transfer to simple_executor

- **COMPLEX**: Multi-step tasks requiring planning and verification.
  Examples: "download the PDF from my email, rename it, and move it to Documents",
  "create a PowerPoint presentation about AI", "set up a new folder structure",
  "find all PDFs in Downloads and move them to a new folder called Reports"
  → Transfer to complex_pipeline

When in doubt between SIMPLE and COMPLEX, prefer SIMPLE — it's faster.
"""

# ── Chat agent instruction ──────────────────────────────────────────────────
CHAT_INSTRUCTION = """\
You are GhostPC's conversational assistant. Answer the user's questions naturally.
You don't have access to desktop tools — just have a helpful conversation.
Keep responses concise since the user is on their phone.
"""

# ── Task planner instruction ────────────────────────────────────────────────
TASK_PLANNER_INSTRUCTION = """\
You are a task planner for a desktop automation agent. Break the user's request
into a numbered step-by-step plan. Each step should be a single, clear action.

Output format:
1. [First action]
2. [Second action]
3. [Third action]
...

Rules:
- Each step should be independently executable
- Include verification steps ("Check that the file was saved")
- Keep steps concrete and specific (not "do the thing", but "click the Save button")
- Maximum 10 steps per plan
"""

# ── Step advancer instruction ───────────────────────────────────────────────
STEP_ADVANCER_INSTRUCTION = """\
You are a step coordinator. Review the result of the last executed step and decide:

1. If the step succeeded → advance to the next step by setting state
2. If the step failed → suggest a retry or alternative approach
3. If all steps are complete → signal completion

Read the current step from temp:current_step and the plan from temp:task_plan.
After advancing, update temp:current_step to the next step number.
When all steps are done, call task_complete with a summary.
"""

# ── Task summarizer instruction ─────────────────────────────────────────────
TASK_SUMMARIZER_INSTRUCTION = """\
Summarize what was accomplished during the multi-step task.
Read the plan from temp:task_plan and the results.
Provide a concise 1-2 sentence summary for the user.
"""


def create_ghost_agent(
    screen_width: int,
    screen_height: int,
    runner: AgentRunner | None = None,
    settings: Settings | None = None,
) -> Agent:
    """Create the full GhostPC multi-agent topology.

    Args:
        screen_width: Actual screen width in pixels.
        screen_height: Actual screen height in pixels.
        runner: Optional AgentRunner for wiring after_tool_callback.
        settings: Optional Settings for model/browser configuration.
    """
    # Resolve model names from settings (or fall back to defaults)
    main_model = settings.gemini_model if settings else _DEFAULT_MODEL
    cu_model = settings.gemini_computer_use_model if settings else _DEFAULT_MODEL

    computer = DesktopComputer(
        screen_width=screen_width,
        screen_height=screen_height,
    )
    desktop_tools = _build_desktop_tools(computer, runner)

    # ── ChatAgent ── (no tools, just conversation)
    chat_agent = Agent(
        name="chat_agent",
        model=main_model,
        description="Handles questions, casual chat, and general conversation. No desktop tools.",
        instruction=CHAT_INSTRUCTION,
        include_contents="default",
        generate_content_config=_GENERATE_CONFIG,
    )

    # ── SimpleExecutor ── (single-action desktop tasks)
    simple_executor = Agent(
        name="simple_executor",
        model=cu_model,
        description=(
            "Executes single desktop actions: open apps, click buttons, type text, "
            "take screenshots, manage windows, run commands. For tasks needing 1-2 steps."
        ),
        static_instruction=STATIC_INSTRUCTION,
        instruction=_dynamic_instruction,
        tools=desktop_tools,
        include_contents="default",
        generate_content_config=_GENERATE_CONFIG,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(thinking_budget=1024),
        ),
        after_tool_callback=runner.after_tool_callback if runner else None,
    )

    # ── ComplexTaskPipeline ── (multi-step tasks)
    # Step 1: Plan the task
    task_planner = Agent(
        name="task_planner",
        model=main_model,
        description="Breaks complex tasks into numbered step-by-step plans.",
        instruction=TASK_PLANNER_INSTRUCTION,
        include_contents="default",
        output_key="temp:task_plan",
        generate_content_config=_GENERATE_CONFIG,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(thinking_budget=4096),
        ),
    )

    # Step 2a: Execute each step
    def _action_agent_instruction(ctx: Any) -> str:
        """Inject current step from the plan into the action agent's instruction."""
        state = ctx.state if hasattr(ctx, "state") else {}
        plan = state.get("temp:task_plan", "")
        current_step = state.get("temp:current_step", 1)
        return (
            f"Execute step {current_step} from the plan below. "
            f"Focus on completing this single step.\n\nPlan:\n{plan}"
        )

    action_agent = Agent(
        name="action_agent",
        model=cu_model,
        description="Executes the current step from the task plan on the desktop.",
        static_instruction=STATIC_INSTRUCTION,
        instruction=_action_agent_instruction,
        tools=desktop_tools,
        include_contents="default",
        output_key="temp:step_result",
        generate_content_config=_GENERATE_CONFIG,
        planner=BuiltInPlanner(
            thinking_config=types.ThinkingConfig(thinking_budget=1024),
        ),
        after_tool_callback=runner.after_tool_callback if runner else None,
    )

    # Step 2b: Check result, advance or escalate
    step_advancer = Agent(
        name="step_advancer",
        model=main_model,
        description="Reviews step results and coordinates progression through the plan.",
        instruction=STEP_ADVANCER_INSTRUCTION,
        tools=[task_complete, send_screenshot_to_user],
        include_contents="default",
        generate_content_config=_GENERATE_CONFIG,
    )

    # Step 2: Loop through steps
    step_executor = LoopAgent(
        name="step_executor",
        description="Loops through plan steps: execute → check → advance → repeat.",
        sub_agents=[action_agent, step_advancer],
        max_iterations=20,
    )

    # Step 3: Summarize results
    task_summarizer = Agent(
        name="task_summarizer",
        model=main_model,
        description="Summarizes the completed multi-step task for the user.",
        instruction=TASK_SUMMARIZER_INSTRUCTION,
        output_key="temp:final_summary",
        include_contents="default",
        generate_content_config=_GENERATE_CONFIG,
    )

    # Full pipeline
    complex_pipeline = SequentialAgent(
        name="complex_pipeline",
        description=(
            "Handles complex multi-step desktop tasks that need planning: "
            "download files, create documents, organize folders, multi-app workflows."
        ),
        sub_agents=[task_planner, step_executor, task_summarizer],
    )

    # ── Root Router ── (classifies intent and delegates)
    root_agent = Agent(
        name="ghost_pc",
        model=main_model,
        description="GhostPC root agent — routes user requests to specialist agents.",
        instruction=ROUTER_INSTRUCTION,
        sub_agents=[chat_agent, simple_executor, complex_pipeline],
        include_contents="default",
        generate_content_config=_GENERATE_CONFIG,
    )

    return root_agent
