import enum


class Queue(enum.Enum):
    HIGH_PRIORITY = "high_priority"  # High priority (for urgent, short tasks)
    DEFAULT = "default"  # for normal tasks
    BACKGROUND = "background"  # Less urgent, medium - length tasks (few minutes)
    EXTENDED_BACKGROUND = "extended_background"  # Very long-lasting background tasks (tasks lasting hours)
