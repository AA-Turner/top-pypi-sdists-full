"""Domain-specific helpers and re-exports from tui_wizard for generate flows."""

import re

from tui_wizard import (
    GoBack,
    MenuItem,
    WizardCleanup,
    WizardStep,
    cbreak_mode,
    filter_visible,
    print_basic_menu,
    prompt_multi_select,
    prompt_single_select,
    prompt_text,
    prompt_yes_no,
    render_tty_menu,
    resolve_non_tty_selection,
    run_menu,
    run_wizard,
)
from tui_wizard.wizard import WIZARD_INTERRUPTED as _WIZARD_INTERRUPTED

__all__ = [
    "_WIZARD_INTERRUPTED",
    "GoBack",
    "MenuItem",
    "WizardCleanup",
    "WizardStep",
    "cbreak_mode",
    "filter_visible",
    "normalize_service_name",
    "print_basic_menu",
    "prompt_multi_select",
    "prompt_single_select",
    "prompt_text",
    "prompt_yes_no",
    "render_tty_menu",
    "resolve_non_tty_selection",
    "resolve_workspace_name",
    "run_menu",
    "run_wizard",
]


# ---------------------------------------------------------------------------
# Domain-specific name helpers
# ---------------------------------------------------------------------------


def resolve_workspace_name(value: str, fallback: str = "my-workspace") -> str:
    """Normalize and validate workspace directory names.

    - collapses whitespace runs into ``-``
    - rejects path separators to keep generation scoped to cwd child folders
    """

    candidate = value.strip() or fallback
    candidate = re.sub(r"\s+", "-", candidate)
    if "/" in candidate or "\\" in candidate:
        raise ValueError("Workspace name must not contain path separators")
    return candidate


def normalize_service_name(value: str) -> str:
    """Normalize a service name to kebab-case and append ``-service`` if missing."""

    candidate = re.sub(r"\s+", "-", value.strip().lower())
    if not candidate.endswith("-service"):
        candidate = f"{candidate}-service"
    return candidate
