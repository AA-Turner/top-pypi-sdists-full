"""Macro CRUD operations and persistence."""

import json
import time
from pathlib import Path

from g13_linux._paths import get_macros_dir

from .macro_types import Macro


class MacroManager:
    """
    Manages macro CRUD operations and persistence.

    Macros are stored as individual JSON files in the macros directory.
    """

    def __init__(self, macros_dir: str | None = None):
        if macros_dir is None:
            macros_dir = get_macros_dir()

        self.macros_dir = Path(macros_dir)
        self.macros_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, Macro] = {}

    def list_macros(self) -> list[str]:
        """Return list of macro IDs."""
        return [p.stem for p in self.macros_dir.glob("*.json")]

    def list_macro_summaries(self) -> list[dict]:
        """Return list of macro summaries (id, name, step_count, duration)."""
        summaries = []
        for macro_id in self.list_macros():
            try:
                macro = self.load_macro(macro_id)
                summaries.append(
                    {
                        "id": macro.id,
                        "name": macro.name,
                        "step_count": macro.step_count,
                        "duration_ms": macro.duration_ms,
                        "assigned_button": macro.assigned_button,
                        "global_hotkey": macro.global_hotkey,
                    }
                )
            except Exception:
                continue
        return summaries

    def load_macro(self, macro_id: str) -> Macro:
        """Load macro from file."""
        if macro_id in self._cache:
            return self._cache[macro_id]

        path = self.macros_dir / f"{macro_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Macro '{macro_id}' not found")

        with open(path) as f:
            data = json.load(f)

        macro = Macro.from_dict(data)
        self._cache[macro_id] = macro
        return macro

    def save_macro(self, macro: Macro) -> None:
        """Save macro to file."""
        macro.modified_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if not macro.created_at:
            macro.created_at = macro.modified_at

        path = self.macros_dir / f"{macro.id}.json"
        with open(path, "w") as f:
            json.dump(macro.to_dict(), f, indent=2)

        self._cache[macro.id] = macro

    def delete_macro(self, macro_id: str) -> None:
        """Delete macro file."""
        path = self.macros_dir / f"{macro_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Macro '{macro_id}' not found")

        path.unlink()
        self._cache.pop(macro_id, None)

    def duplicate_macro(self, macro_id: str, new_name: str) -> Macro:
        """Create a copy of an existing macro."""
        import uuid

        original = self.load_macro(macro_id)

        new_macro = Macro(
            id=str(uuid.uuid4()),
            name=new_name,
            description=original.description,
            steps=original.steps.copy(),
            speed_multiplier=original.speed_multiplier,
            repeat_count=original.repeat_count,
            repeat_delay_ms=original.repeat_delay_ms,
            playback_mode=original.playback_mode,
            fixed_delay_ms=original.fixed_delay_ms,
        )

        self.save_macro(new_macro)
        return new_macro

    def macro_exists(self, macro_id: str) -> bool:
        """Check if macro exists."""
        return (self.macros_dir / f"{macro_id}.json").exists()

    def create_macro(self, name: str = "New Macro") -> Macro:
        """Create a new empty macro."""
        macro = Macro(name=name)
        self.save_macro(macro)
        return macro

    def import_macro(self, file_path: str) -> Macro:
        """Import macro from external file."""
        import uuid

        with open(file_path) as f:
            data = json.load(f)

        macro = Macro.from_dict(data)
        # Generate new ID to avoid conflicts
        macro.id = str(uuid.uuid4())
        self.save_macro(macro)
        return macro

    def export_macro(self, macro_id: str, file_path: str) -> None:
        """Export macro to external file."""
        macro = self.load_macro(macro_id)
        with open(file_path, "w") as f:
            json.dump(macro.to_dict(), f, indent=2)

    def clear_cache(self) -> None:
        """Clear the macro cache."""
        self._cache.clear()

    def get_macro_by_button(self, button_id: str) -> Macro | None:
        """Find macro assigned to a specific button."""
        for macro_id in self.list_macros():
            try:
                macro = self.load_macro(macro_id)
                if macro.assigned_button == button_id:
                    return macro
            except Exception:
                continue
        return None

    def get_macro_by_hotkey(self, hotkey: str) -> Macro | None:
        """Find macro with a specific global hotkey."""
        for macro_id in self.list_macros():
            try:
                macro = self.load_macro(macro_id)
                if macro.global_hotkey == hotkey:
                    return macro
            except Exception:
                continue
        return None
