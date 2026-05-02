"""App profile rules for per-application profile switching.

Manages rules that map window patterns to G13 profiles.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal

from g13_linux._paths import get_app_profiles_path


@dataclass
class AppProfileRule:
    """A rule that maps a window pattern to a profile.

    Attributes:
        name: Human-readable rule name (e.g., "EVE Online")
        pattern: Regex pattern to match against window name/class
        match_type: What to match against ("window_name", "wm_class", or "both")
        profile_name: Name of the G13 profile to activate
        enabled: Whether this rule is active
    """

    name: str
    pattern: str
    match_type: str  # "window_name" | "wm_class" | "both"
    profile_name: str
    enabled: bool = True

    def matches(self, window_name: str, wm_class: str) -> bool:
        """Check if this rule matches the given window.

        Args:
            window_name: The window title
            wm_class: The WM_CLASS property

        Returns:
            True if the rule matches
        """
        if not self.enabled:
            return False

        try:
            regex = re.compile(self.pattern, re.IGNORECASE)
        except re.error:
            return False

        if self.match_type == "window_name":
            return bool(regex.search(window_name))
        elif self.match_type == "wm_class":
            return bool(regex.search(wm_class))
        elif self.match_type == "both":
            return bool(regex.search(window_name) or regex.search(wm_class))
        return False

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "pattern": self.pattern,
            "match_type": self.match_type,
            "profile_name": self.profile_name,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AppProfileRule":
        """Create from dictionary."""
        return cls(
            name=data.get("name", "Unnamed Rule"),
            pattern=data.get("pattern", ""),
            match_type=data.get("match_type", "window_name"),
            profile_name=data.get("profile_name", ""),
            enabled=data.get("enabled", True),
        )


@dataclass
class AppProfileConfig:
    """Configuration for app profile switching.

    Attributes:
        rules: List of matching rules (first match wins)
        default_profile: Profile to use when no rules match (None = keep current)
        enabled: Master switch for auto-switching
    """

    rules: list[AppProfileRule] = field(default_factory=list)
    default_profile: str | None = None
    enabled: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "rules": [r.to_dict() for r in self.rules],
            "default_profile": self.default_profile,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AppProfileConfig":
        """Create from dictionary."""
        rules = [AppProfileRule.from_dict(r) for r in data.get("rules", [])]
        return cls(
            rules=rules,
            default_profile=data.get("default_profile"),
            enabled=data.get("enabled", True),
        )


class AppProfileRulesManager(QObject):
    """Manages app-to-profile mapping rules.

    Handles rule matching, persistence, and emits signals when
    a profile switch is needed.

    Signals:
        profile_switch_requested(profile_name): Emitted when a rule matches
        rules_changed(): Emitted when rules are modified
    """

    profile_switch_requested = pyqtSignal(str)
    rules_changed = pyqtSignal()

    def __init__(self, config_path: Path | None = None, parent=None):
        """Initialize the rules manager.

        Args:
            config_path: Path to config file (default: configs/app_profiles.json)
            parent: Parent QObject
        """
        super().__init__(parent)
        if config_path is None:
            self.config_path = get_app_profiles_path()
        else:
            self.config_path = config_path

        self._config = AppProfileConfig()
        self._last_matched_profile: str | None = None
        self.load()

    @property
    def enabled(self) -> bool:
        """Whether auto-switching is enabled."""
        return self._config.enabled

    @enabled.setter
    def enabled(self, value: bool):
        """Set whether auto-switching is enabled."""
        self._config.enabled = value
        self.save()
        self.rules_changed.emit()

    @property
    def rules(self) -> list[AppProfileRule]:
        """Get the list of rules."""
        return self._config.rules

    @property
    def default_profile(self) -> str | None:
        """Get the default profile name."""
        return self._config.default_profile

    @default_profile.setter
    def default_profile(self, value: str | None):
        """Set the default profile name."""
        self._config.default_profile = value
        self.save()
        self.rules_changed.emit()

    def match(self, window_name: str, wm_class: str) -> str | None:
        """Find the first matching profile for a window.

        Args:
            window_name: The window title
            wm_class: The WM_CLASS property

        Returns:
            Profile name if a rule matches, default_profile if no match,
            or None if no default is set.
        """
        if not self._config.enabled:
            return None

        for rule in self._config.rules:
            if rule.matches(window_name, wm_class):
                return rule.profile_name

        return self._config.default_profile

    def on_window_changed(self, window_id: str, name: str, wm_class: str):
        """Handle window change event from WindowMonitorThread.

        Args:
            window_id: X11 window ID
            name: Window title
            wm_class: WM_CLASS property
        """
        profile = self.match(name, wm_class)

        # Only emit if profile changed
        if profile and profile != self._last_matched_profile:
            self._last_matched_profile = profile
            self.profile_switch_requested.emit(profile)
        elif profile is None:
            # Reset last matched so we can switch back later
            self._last_matched_profile = None

    def add_rule(self, rule: AppProfileRule, index: int | None = None):
        """Add a rule to the list.

        Args:
            rule: The rule to add
            index: Position to insert at (default: end of list)
        """
        if index is None:
            self._config.rules.append(rule)
        else:
            self._config.rules.insert(index, rule)
        self.save()
        self.rules_changed.emit()

    def remove_rule(self, index: int):
        """Remove a rule by index."""
        if 0 <= index < len(self._config.rules):
            del self._config.rules[index]
            self.save()
            self.rules_changed.emit()

    def update_rule(self, index: int, rule: AppProfileRule):
        """Update a rule at the given index."""
        if 0 <= index < len(self._config.rules):
            self._config.rules[index] = rule
            self.save()
            self.rules_changed.emit()

    def move_rule(self, from_index: int, to_index: int):
        """Move a rule from one position to another."""
        if 0 <= from_index < len(self._config.rules) and 0 <= to_index < len(self._config.rules):
            rule = self._config.rules.pop(from_index)
            self._config.rules.insert(to_index, rule)
            self.save()
            self.rules_changed.emit()

    def load(self):
        """Load rules from config file."""
        if self.config_path.exists():
            try:
                with open(self.config_path) as f:
                    data = json.load(f)
                self._config = AppProfileConfig.from_dict(data)
            except (OSError, json.JSONDecodeError) as e:
                print(f"Error loading app profiles config: {e}")
                self._config = AppProfileConfig()
        else:
            self._config = AppProfileConfig()

    def save(self):
        """Save rules to config file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self._config.to_dict(), f, indent=2)
        except OSError as e:
            print(f"Error saving app profiles config: {e}")
