"""Persona management for Open Agent.

Manages the agent's evolving personality and preferences.
Learns from user interactions over time.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any


@dataclass
class Preference:
    """A single learned user preference."""

    value: str
    confidence: float = 1.0
    context: str = "general"
    learned_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    usage_count: int = 1

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Preference":
        return cls(**data)


class PersonaManager:
    """Manages the agent's evolving personality and preferences.

    Learns from user interactions over time and builds personalized
    system prompts based on accumulated knowledge about the user.
    """

    DEFAULT_BASE_PROMPT = "I am your personal assistant. I learn from our conversations and adapt to help you better."

    def __init__(
        self,
        user_id: str = "default",
        storage_path: Optional[Path] = None,
        emdash_dir: Optional[Path] = None,
    ):
        """Initialize the persona manager.

        Args:
            user_id: Unique identifier for the user/session
            storage_path: Optional explicit path to persona storage
            emdash_dir: Optional path to .emdash directory (for default storage location)
        """
        self.user_id = user_id
        self.preferences: Dict[str, Preference] = {}
        self.interaction_count = 0
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

        # Determine storage path
        if storage_path:
            self._storage_path = Path(storage_path)
        elif emdash_dir:
            self._storage_path = emdash_dir / "personas" / user_id / "persona.json"
        else:
            # Default to current working directory
            self._storage_path = Path(".emdash") / "personas" / user_id / "persona.json"

        self._ensure_storage_exists()
        self._load()

    def _ensure_storage_exists(self) -> None:
        """Ensure the storage directory exists."""
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        """Load persona from storage."""
        if self._storage_path.exists():
            try:
                with open(self._storage_path, "r") as f:
                    data = json.load(f)

                self.user_id = data.get("user_id", self.user_id)
                self.interaction_count = data.get("interaction_count", 0)
                self.created_at = data.get("created_at", self.created_at)
                self.updated_at = data.get("updated_at", self.updated_at)

                # Load preferences
                prefs_data = data.get("preferences", {})
                self.preferences = {
                    k: Preference.from_dict(v) for k, v in prefs_data.items()
                }
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # If loading fails, start fresh
                print(f"Warning: Could not load persona: {e}")
                pass

    def _save(self) -> None:
        """Save persona to storage."""
        self.updated_at = datetime.now().isoformat()

        data = {
            "version": "1.0",
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "interaction_count": self.interaction_count,
            "preferences": {
                k: v.to_dict() for k, v in self.preferences.items()
            },
        }

        with open(self._storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def learn_preference(
        self,
        context: str,
        preference: str,
        confidence: float = 1.0,
    ) -> None:
        """Learn a user preference.

        Args:
            context: The context/category for this preference (e.g., "python.framework")
            preference: The preference value (e.g., "fastapi")
            confidence: Confidence level (0.0-1.0) in this preference
        """
        now = datetime.now().isoformat()

        if context in self.preferences:
            # Update existing preference
            existing = self.preferences[context]
            existing.value = preference
            existing.confidence = confidence
            existing.updated_at = now
            existing.usage_count += 1
        else:
            # Create new preference
            self.preferences[context] = Preference(
                value=preference,
                confidence=confidence,
                context=context.split(".")[0] if "." in context else "general",
                learned_at=now,
                updated_at=now,
                usage_count=1,
            )

        self._save()

    def get_preference(self, context: str, default: Optional[str] = None) -> Optional[str]:
        """Get a learned preference.

        Args:
            context: The preference context to look up
            default: Default value if preference not found

        Returns:
            The preference value or default
        """
        if context in self.preferences:
            return self.preferences[context].value
        return default

    def get_preference_details(self, context: str) -> Optional[Preference]:
        """Get full preference details including confidence and metadata.

        Args:
            context: The preference context to look up

        Returns:
            The Preference object or None
        """
        return self.preferences.get(context)

    def remove_preference(self, context: str) -> bool:
        """Remove a learned preference.

        Args:
            context: The preference context to remove

        Returns:
            True if removed, False if not found
        """
        if context in self.preferences:
            del self.preferences[context]
            self._save()
            return True
        return False

    def build_system_prompt(self, base_prompt: str = "") -> str:
        """Build a personalized system prompt from learned preferences.

        Args:
            base_prompt: Optional base prompt to extend (defaults to DEFAULT_BASE_PROMPT)

        Returns:
            The personalized system prompt
        """
        if not base_prompt:
            base_prompt = self.DEFAULT_BASE_PROMPT

        sections = [base_prompt]

        # Add learned preferences section if we have any
        if self.preferences:
            sections.append("\n## What I've Learned About You\n")

            # Group preferences by context
            by_context: Dict[str, List[tuple]] = {}
            for key, pref in self.preferences.items():
                ctx = pref.context
                if ctx not in by_context:
                    by_context[ctx] = []
                by_context[ctx].append((key, pref))

            # Build preference text, sorted by context and confidence
            for context in sorted(by_context.keys()):
                prefs = by_context[context]
                # Sort by confidence (highest first) and usage count
                prefs.sort(key=lambda x: (-x[1].confidence, -x[1].usage_count))

                sections.append(f"\n### {context.title()}\n")
                for key, pref in prefs:
                    confidence_str = ""
                    if pref.confidence < 0.8:
                        confidence_str = f" (confidence: {pref.confidence:.0%})"
                    sections.append(f"- {key}: {pref.value}{confidence_str}\n")

        return "".join(sections)

    def get_preference_summary(self) -> str:
        """Get a human-readable summary of learned preferences.

        Returns:
            Summary string for display
        """
        if not self.preferences:
            return "I haven't learned any preferences about you yet."

        lines = ["Here's what I know about your preferences:\n"]

        for key, pref in sorted(self.preferences.items()):
            lines.append(f"- {key}: {pref.value}")
            if pref.confidence < 1.0:
                lines.append(f"  (confidence: {pref.confidence:.0%})")

        lines.append(f"\nTotal preferences: {len(self.preferences)}")
        lines.append(f"Interactions: {self.interaction_count}")

        return "\n".join(lines)

    def export_persona(self) -> dict:
        """Export the persona as a dictionary.

        Returns:
            Complete persona data for export/import
        """
        return {
            "version": "1.0",
            "export_date": datetime.now().isoformat(),
            "user_id": self.user_id,
            "preferences": {k: v.to_dict() for k, v in self.preferences.items()},
            "interaction_count": self.interaction_count,
            "created_at": self.created_at,
        }

    def import_persona(self, data: dict) -> None:
        """Import persona from a dictionary.

        Args:
            data: Persona data to import
        """
        # Validate version
        version = data.get("version", "1.0")
        if version != "1.0":
            raise ValueError(f"Unsupported persona version: {version}")

        # Import preferences
        prefs_data = data.get("preferences", {})
        self.preferences = {
            k: Preference.from_dict(v) for k, v in prefs_data.items()
        }

        # Import metadata
        self.interaction_count = data.get("interaction_count", 0)
        self.created_at = data.get("created_at", datetime.now().isoformat())

        self._save()

    def reset(self) -> None:
        """Reset the persona to initial state."""
        self.preferences.clear()
        self.interaction_count = 0
        self.created_at = datetime.now().isoformat()
        self._save()

    def record_interaction(self) -> None:
        """Record that an interaction occurred."""
        self.interaction_count += 1
        # Save periodically (every 10 interactions)
        if self.interaction_count % 10 == 0:
            self._save()

    def get_all_preferences(self) -> Dict[str, Preference]:
        """Get all learned preferences.

        Returns:
            Dictionary of all preferences
        """
        return dict(self.preferences)

    def suggest_capability(
        self,
        message: str,
        conversation_history: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """Analyze conversation to suggest a new capability.

        This is a simple heuristic-based suggestion. More sophisticated
        analysis would use an LLM to detect patterns.

        Args:
            message: Current user message
            conversation_history: Recent conversation history

        Returns:
            Suggested capability dict or None
        """
        # Simple pattern detection
        teaching_patterns = [
            "i want you to",
            "always",
            "remember that",
            "from now on",
            "whenever i",
        ]

        message_lower = message.lower()
        for pattern in teaching_patterns:
            if pattern in message_lower:
                # User might be teaching us something
                return {
                    "suggested": True,
                    "pattern": pattern,
                    "message": "It looks like you're teaching me something. Would you like me to remember this?",
                }

        return None