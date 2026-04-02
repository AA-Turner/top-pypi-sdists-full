"""Configuration change log for tracking paramset modifications."""

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Final

DEFAULT_MAX_ENTRIES: Final = 500


def build_change_diff(
    *,
    old_values: dict[str, Any],
    new_values: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Build a change diff between old and new paramset values."""
    changes: dict[str, dict[str, Any]] = {}
    for param, new_val in new_values.items():
        if (old_val := old_values.get(param)) != new_val:
            changes[param] = {"old": old_val, "new": new_val}
    return changes


@dataclass(frozen=True, slots=True)
class ConfigChangeEntry:
    """A single configuration change record."""

    timestamp: str
    entry_id: str
    interface_id: str
    channel_address: str
    device_name: str
    device_model: str
    paramset_key: str
    changes: dict[str, dict[str, Any]]
    source: str


class ConfigChangeLog:
    """FIFO-capped log of configuration change entries."""

    __slots__ = ("_entries", "_max_entries")

    def __init__(self, *, max_entries: int = DEFAULT_MAX_ENTRIES) -> None:
        """Initialize the change log."""
        self._max_entries: Final = max_entries
        self._entries: list[ConfigChangeEntry] = []

    @property
    def max_entries(self) -> int:
        """Return the maximum number of entries."""
        return self._max_entries

    def add(
        self,
        *,
        entry_id: str,
        interface_id: str,
        channel_address: str,
        device_name: str,
        device_model: str,
        paramset_key: str,
        changes: dict[str, dict[str, Any]],
        source: str,
    ) -> ConfigChangeEntry:
        """Add a new change entry to the log."""
        entry = ConfigChangeEntry(
            timestamp=datetime.now(tz=UTC).isoformat(),
            entry_id=entry_id,
            interface_id=interface_id,
            channel_address=channel_address,
            device_name=device_name,
            device_model=device_model,
            paramset_key=paramset_key,
            changes=changes,
            source=source,
        )
        self._entries.append(entry)
        if len(self._entries) > self._max_entries:
            self._entries = self._entries[-self._max_entries :]
        return entry

    def clear_by_entry_id(self, *, entry_id: str) -> int:
        """Clear entries matching the given entry_id."""
        original_count = len(self._entries)
        self._entries = [e for e in self._entries if e.entry_id != entry_id]
        return original_count - len(self._entries)

    def get_entries(
        self,
        *,
        entry_id: str = "",
        channel_address: str = "",
        limit: int = 50,
    ) -> tuple[list[ConfigChangeEntry], int]:
        """Return filtered entries (most recent first) and total count."""
        filtered = self._entries
        if entry_id:
            filtered = [e for e in filtered if e.entry_id == entry_id]
        if channel_address:
            filtered = [e for e in filtered if e.channel_address.startswith(channel_address)]
        total = len(filtered)
        result = list(reversed(filtered[-limit:]))
        return result, total

    def load_entries(self, *, raw_entries: list[dict[str, Any]]) -> None:
        """Load entries from serialized dicts (replaces existing)."""
        loaded = [
            ConfigChangeEntry(
                timestamp=raw.get("timestamp", ""),
                entry_id=raw.get("entry_id", ""),
                interface_id=raw.get("interface_id", ""),
                channel_address=raw.get("channel_address", ""),
                device_name=raw.get("device_name", ""),
                device_model=raw.get("device_model", ""),
                paramset_key=raw.get("paramset_key", ""),
                changes=raw.get("changes", {}),
                source=raw.get("source", ""),
            )
            for raw in raw_entries
        ]
        if len(loaded) > self._max_entries:
            loaded = loaded[-self._max_entries :]
        self._entries = loaded

    def to_dicts(self) -> list[dict[str, Any]]:
        """Serialize all entries for persistence."""
        return [asdict(e) for e in self._entries]
