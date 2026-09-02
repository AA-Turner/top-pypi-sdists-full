"""
Board adapters for abstracting platform differences

These adapters provide a common interface for Trello, Jira, Notion, and Linear
while working with existing domain objects.
"""

from .base_adapter import (
    BaseBoardAdapter,
    BoardAdapterError,
    BoardCapabilityError,
    BoardCredentialError,
)
from .jira_adapter import JiraBoardAdapter
from .linear_adapter import LinearBoardAdapter
from .notion_adapter import NotionBoardAdapter
from .trello_adapter import TrelloBoardAdapter

__all__ = [
    "BaseBoardAdapter",
    "BoardAdapterError",
    "BoardCapabilityError",
    "BoardCredentialError",
    "TrelloBoardAdapter",
    "JiraBoardAdapter",
    "NotionBoardAdapter",
    "LinearBoardAdapter",
]
