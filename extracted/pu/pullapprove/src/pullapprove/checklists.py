"""
Configuration models for approval checklists.

A simpler alternative to forms for compliance sign-off before approval.
Each item is a checkbox with configurable requirement and notes settings.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class NotesOption(StrEnum):
    """Controls when/if notes are shown/required for a checklist item."""

    DISABLED = "disabled"  # No notes field
    OPTIONAL = "optional"  # Notes field available but not required
    REQUIRED = "required"  # Notes always required
    REQUIRED_IF_CHECKED = "required_if_checked"  # Notes required when item is checked
    REQUIRED_IF_UNCHECKED = "required_if_unchecked"  # Notes required when not checked


class ChecklistItem(BaseModel):
    """A single checklist item.

    Settings:
    - required: Whether the item must be checked (default: True)
    - notes: Controls when/if notes are shown/required (default: "optional")
    - help: Optional help text displayed below the label

    Notes options:
    - "disabled": No notes field
    - "optional": Notes field available but not required (default)
    - "required": Notes always required
    - "required_if_checked": Notes required when item is checked
    - "required_if_unchecked": Notes required when item is not checked
    """

    model_config = ConfigDict(extra="forbid")

    label: str = Field(min_length=1)
    required: bool = True
    notes: NotesOption = NotesOption.OPTIONAL
    help: str = ""

    # Runtime values (not part of config, populated during submission)
    checked: bool = False
    notes_value: str = ""

    def notes_required_for_state(self, checked: bool) -> bool:
        """Check if notes are required given the checked state."""
        if self.notes == NotesOption.REQUIRED:
            return True
        if self.notes == NotesOption.REQUIRED_IF_CHECKED and checked:
            return True
        if self.notes == NotesOption.REQUIRED_IF_UNCHECKED and not checked:  # noqa: SIM103
            return True
        return False


class Checklist(BaseModel):
    """Configuration for approval checklists."""

    model_config = ConfigDict(extra="forbid")

    items: list[ChecklistItem] = Field(min_length=1)

    def compute_hash(self) -> str:
        """Compute deterministic hash of checklist definition.

        Only includes semantic attributes that define the checklist:
        - label, required, notes, help
        Excludes runtime values:
        - checked, notes_value
        """
        serialized: list[dict[str, Any]] = []
        for item in self.items:
            semantic: dict[str, Any] = {
                "label": item.label,
                "required": item.required,
                "notes": item.notes.value,
                "help": item.help,
            }
            serialized.append(semantic)
        canonical = json.dumps(serialized, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()
