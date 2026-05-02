"""Base strategy interface for enemy clearing strategies."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ..game_state import GameState


class Action:
    """Represents a single action in the game."""

    def __init__(self, x: int, shoot: bool = False):
        """
        Initialize an action.

        Args:
            x: Week position (0-51) where ship should move
            shoot: Whether to shoot at this position
        """
        self.x = x
        self.shoot = shoot

    def __repr__(self) -> str:
        action_type = "SHOOT" if self.shoot else "MOVE"
        return f"Action({action_type} x={self.x})"


class BaseStrategy(ABC):
    """Abstract base class for enemy clearing strategies."""

    @abstractmethod
    def generate_actions(self, game_state: "GameState") -> Iterator[Action]:
        """
        Generate sequence of actions for the ship to clear enemies.

        Args:
            game_state: The current game state with enemies, ship, and bullets

        Yields:
            Action objects representing ship movements and shots
        """
        pass
