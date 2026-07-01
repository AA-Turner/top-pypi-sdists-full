from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrackerCapabilities:
    supports_webhooks: bool = False
    supports_comments: bool = True
    supports_hierarchy: bool = True
    supports_dependencies: bool = True
    supports_custom_fields: bool = True
    supports_multi_assignee: bool = True
    supports_sprints_or_cycles: bool = False
    supports_bulk_read: bool = False
    supports_bulk_write: bool = False
    supports_delete: bool = False

    def as_dict(self) -> dict[str, bool]:
        return {
            "supports_webhooks": self.supports_webhooks,
            "supports_comments": self.supports_comments,
            "supports_hierarchy": self.supports_hierarchy,
            "supports_dependencies": self.supports_dependencies,
            "supports_custom_fields": self.supports_custom_fields,
            "supports_multi_assignee": self.supports_multi_assignee,
            "supports_sprints_or_cycles": self.supports_sprints_or_cycles,
            "supports_bulk_read": self.supports_bulk_read,
            "supports_bulk_write": self.supports_bulk_write,
            "supports_delete": self.supports_delete,
        }
