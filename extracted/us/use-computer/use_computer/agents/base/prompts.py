"""Prompt loading and template rendering."""

from __future__ import annotations

from pathlib import Path

PROMPTS_DIR = Path(__file__).parents[1] / "prompts"


def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text()


def build_system_prompt(
    template: str,
    width: int,
    height: int,
    instruction: str = "",
    step: int = 1,
    max_steps: int = 50,
    os_type: str = "macOS",
    os_article: str = "a",
    platform_notes: str = "",
) -> str:
    notes_section = f"{platform_notes.strip()}\n\n" if platform_notes.strip() else ""
    prompt = (
        template.replace("{OS_TYPE}", os_type)
        .replace("{OS_ARTICLE}", os_article)
        .replace("{TASK_INSTRUCTION}", instruction)
        .replace("{SCREENSHOT_WIDTH}", str(width))
        .replace("{SCREENSHOT_HEIGHT}", str(height))
        .replace("{SCREENSHOT_MAX_X}", str(width - 1))
        .replace("{SCREENSHOT_MAX_Y}", str(height - 1))
        .replace("{SCREENSHOT_CENTER_X}", str(width // 2))
        .replace("{SCREENSHOT_CENTER_Y}", str(height // 2))
        .replace("{STEP_NUMBER}", str(step))
        .replace("{MAX_STEPS}", str(max_steps))
        .replace("{PLATFORM_NOTES}", platform_notes.strip())
        .replace("{PLATFORM_NOTES_SECTION}", notes_section)
    )
    return prompt.rstrip()
