"""Column-by-column strategy: Ship moves week by week (left to right)."""

from typing import TYPE_CHECKING, Iterator

from ...constants import NUM_WEEKS
from .base_strategy import Action, BaseStrategy

if TYPE_CHECKING:
    from ..game_state import GameState


class ColumnStrategy(BaseStrategy):
    """
    Ship moves column by column (week by week) from left to right.

    For each week, the ship shoots at all enemies in that column until destroyed,
    reacting to the actual game state rather than planning ahead.
    """

    def generate_actions(self, game_state: "GameState") -> Iterator[Action]:
        """
        Generate actions moving week by week, reacting to living enemies.

        The ship moves through each week (column), shooting at enemies
        until all enemies in that week are destroyed, then moves to the next week.
        Uses actual game state to determine which enemies are still alive.

        Args:
            game_state: The current game state with living enemies

        Yields:
            Action objects representing ship movements and shots
        """
        # Process each week (column) from left to right
        for week_idx in range(NUM_WEEKS):
            # Keep shooting at enemies in this week until none remain
            while True:
                # Find all living enemies in this week
                enemies_in_week = [e for e in game_state.enemies if e.x == week_idx]
                total_health = sum(e.health for e in enemies_in_week)
                flying_bullets = len([b for b in game_state.bullets if int(b.x) == week_idx])

                if flying_bullets >= total_health:
                    break

                yield Action(x=week_idx, shoot=True)
