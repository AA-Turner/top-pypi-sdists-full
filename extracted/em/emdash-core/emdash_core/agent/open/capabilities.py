"""Capability management for Open Agent.

Capabilities represent learned behaviors, skills, or patterns that the
agent has acquired through interaction with the user.
"""

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


@dataclass
class Capability:
    """A capability the agent has learned.

    Capabilities are like mini-skills that the agent learns from
    user interactions. They include trigger patterns to activate
    and prompt additions to guide behavior.
    """

    name: str
    description: str
    trigger_patterns: List[str]
    tools: List[str]
    prompt_addition: str
    examples: List[str]
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    usage_count: int = 0
    last_used: Optional[str] = None
    enabled: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Capability":
        # Remove any extra fields not in the dataclass
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)

    def matches_message(self, message: str) -> bool:
        """Check if this capability matches a user message.

        Args:
            message: User message to check

        Returns:
            True if any trigger pattern matches
        """
        message_lower = message.lower()
        for pattern in self.trigger_patterns:
            # Support both simple substring and regex patterns
            if pattern.startswith("/") and pattern.endswith("/"):
                # Regex pattern
                try:
                    regex = pattern[1:-1]
                    if re.search(regex, message, re.IGNORECASE):
                        return True
                except re.error:
                    continue
            else:
                # Simple substring match
                if pattern.lower() in message_lower:
                    return True
        return False

    def record_usage(self) -> None:
        """Record that this capability was used."""
        self.usage_count += 1
        self.last_used = datetime.now().isoformat()
        self.updated_at = self.last_used


class CapabilityRegistry:
    """Discovers, registers, and manages agent capabilities.

    Provides pattern matching to find relevant capabilities for
    user messages and tracks usage statistics.
    """

    MAX_CAPABILITIES = 20  # Limit to prevent context overflow

    def __init__(self, storage_path: Optional[Path] = None, emdash_dir: Optional[Path] = None):
        """Initialize the capability registry.

        Args:
            storage_path: Optional explicit path to capabilities storage
            emdash_dir: Optional path to .emdash directory
        """
        self.capabilities: Dict[str, Capability] = {}

        # Determine storage path
        if storage_path:
            self._storage_path = Path(storage_path)
        elif emdash_dir:
            self._storage_path = emdash_dir / "capabilities.json"
        else:
            self._storage_path = Path(".emdash") / "capabilities.json"

        self._ensure_storage_exists()
        self._load()

    def _ensure_storage_exists(self) -> None:
        """Ensure the storage directory exists."""
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        """Load capabilities from storage."""
        if self._storage_path.exists():
            try:
                with open(self._storage_path, "r") as f:
                    data = json.load(f)

                caps_data = data.get("capabilities", {})
                self.capabilities = {
                    k: Capability.from_dict(v) for k, v in caps_data.items()
                }
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Warning: Could not load capabilities: {e}")
                pass

    def _save(self) -> None:
        """Save capabilities to storage."""
        data = {
            "version": "1.0",
            "updated_at": datetime.now().isoformat(),
            "capabilities": {
                k: v.to_dict() for k, v in self.capabilities.items()
            },
        }

        with open(self._storage_path, "w") as f:
            json.dump(data, f, indent=2)

    def register(self, capability: Capability) -> None:
        """Register a new capability.

        Args:
            capability: The capability to register

        Raises:
            ValueError: If max capabilities reached
        """
        if len(self.capabilities) >= self.MAX_CAPABILITIES:
            raise ValueError(
                f"Maximum number of capabilities ({self.MAX_CAPABILITIES}) reached. "
                f"Remove some capabilities before adding new ones."
            )

        self.capabilities[capability.name] = capability
        self._save()

    def unregister(self, name: str) -> bool:
        """Remove a capability.

        Args:
            name: Name of the capability to remove

        Returns:
            True if removed, False if not found
        """
        if name in self.capabilities:
            del self.capabilities[name]
            self._save()
            return True
        return False

    def get(self, name: str) -> Optional[Capability]:
        """Get a capability by name.

        Args:
            name: Capability name

        Returns:
            The capability or None
        """
        return self.capabilities.get(name)

    def list_all(self) -> List[Capability]:
        """List all capabilities.

        Returns:
            List of all capabilities
        """
        return list(self.capabilities.values())

    def find_matching(self, message: str) -> List[Capability]:
        """Find capabilities that match a user message.

        Args:
            message: User message to match

        Returns:
            List of matching capabilities, sorted by relevance
        """
        matches = []
        for cap in self.capabilities.values():
            if cap.enabled and cap.matches_message(message):
                matches.append(cap)

        # Sort by usage count (most used first) and recency
        matches.sort(key=lambda c: (-c.usage_count, c.last_used or "", c.name))
        return matches

    def get_active(self, limit: int = 5) -> List[Capability]:
        """Get the most active capabilities.

        Args:
            limit: Maximum number to return

        Returns:
            List of most used capabilities
        """
        enabled = [c for c in self.capabilities.values() if c.enabled]
        # Sort by usage count descending
        enabled.sort(key=lambda c: (-c.usage_count, c.name))
        return enabled[:limit]

    def record_usage(self, capability_name: str) -> bool:
        """Record usage of a capability.

        Args:
            capability_name: Name of the capability used

        Returns:
            True if found and updated, False otherwise
        """
        if capability_name in self.capabilities:
            self.capabilities[capability_name].record_usage()
            self._save()
            return True
        return False

    def suggest_new(
        self,
        message: str,
        conversation_history: List[Dict[str, Any]],
    ) -> Optional[Dict[str, Any]]:
        """Suggest creating a new capability based on conversation.

        Uses heuristics to detect when user is teaching the agent
        something that could be a reusable capability.

        Args:
            message: Current user message
            conversation_history: Recent conversation history

        Returns:
            Suggestion dict with capability draft or None
        """
        message_lower = message.lower()

        # Patterns that suggest user wants recurring behavior
        capability_patterns = [
            ("i want you to always", "behavior"),
            ("from now on", "behavior"),
            ("whenever i ask", "trigger"),
            ("remember to always", "behavior"),
            ("can you make it so", "automation"),
            ("i'd like you to", "behavior"),
        ]

        for pattern, cap_type in capability_patterns:
            if pattern in message_lower:
                # Extract potential capability name and description
                name_hint = self._extract_name_hint(message)

                return {
                    "suggested": True,
                    "type": cap_type,
                    "trigger_pattern": pattern,
                    "name_hint": name_hint,
                    "message": f"It looks like you want me to {pattern}. "
                               f"Should I create a reusable capability for this?",
                    "draft": {
                        "name": name_hint,
                        "description": f"Learned from: {message[:100]}...",
                        "trigger_patterns": [pattern.replace("i ", "").strip()],
                    },
                }

        return None

    def _extract_name_hint(self, message: str) -> str:
        """Extract a potential name from a capability request.

        Args:
            message: User message

        Returns:
            Suggested capability name
        """
        # Simple extraction - take first few words and sanitize
        words = message.lower().split()[:5]
        name = "-".join(w for w in words if w.isalnum())
        name = name[:30]  # Limit length
        if not name:
            name = "learned-capability"
        return name

    def enable(self, name: str) -> bool:
        """Enable a capability.

        Args:
            name: Capability name

        Returns:
            True if found and enabled, False otherwise
        """
        if name in self.capabilities:
            self.capabilities[name].enabled = True
            self._save()
            return True
        return False

    def disable(self, name: str) -> bool:
        """Disable a capability without removing it.

        Args:
            name: Capability name

        Returns:
            True if found and disabled, False otherwise
        """
        if name in self.capabilities:
            self.capabilities[name].enabled = False
            self._save()
            return True
        return False

    def reset(self) -> None:
        """Clear all capabilities."""
        self.capabilities.clear()
        self._save()

    def export(self) -> dict:
        """Export all capabilities as a dictionary.

        Returns:
            Export data
        """
        return {
            "version": "1.0",
            "export_date": datetime.now().isoformat(),
            "capabilities": {
                k: v.to_dict() for k, v in self.capabilities.items()
            },
        }

    def import_data(self, data: dict) -> None:
        """Import capabilities from a dictionary.

        Args:
            data: Import data
        """
        version = data.get("version", "1.0")
        if version != "1.0":
            raise ValueError(f"Unsupported capabilities version: {version}")

        caps_data = data.get("capabilities", {})
        for name, cap_data in caps_data.items():
            self.capabilities[name] = Capability.from_dict(cap_data)

        self._save()