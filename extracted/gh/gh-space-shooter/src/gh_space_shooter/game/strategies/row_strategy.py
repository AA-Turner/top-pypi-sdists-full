"""Row-by-row strategy: Process enemies row by row (day by day)."""

from typing import TYPE_CHECKING, Iterator

from ...constants import NUM_DAYS
from .base_strategy import Action, BaseStrategy

if TYPE_CHECKING:
    from ..game_state import GameState


class RowStrategy(BaseStrategy):
    """
    Ship processes enemies row by row (day by day) from top to bottom.

    For each row (day), the ship moves to each enemy position in that row
    and shoots until all enemies in the row are destroyed.
    """

    def generate_actions(self, game_state: "GameState") -> Iterator[Action]:
        """
        Generate actions processing enemies row by row.

        The ship processes each day (row) from Sunday (0) to Saturday (6),
        moving horizontally to shoot at all enemies in that row before
        proceeding to the next row.

        Args:
            game_state: The current game state with living enemies

        Yields:
            Action objects representing ship movements and shots
        """
        # Process each day (row) from top to bottom
        for day_idx in range(NUM_DAYS - 1, -1, -1):
            enemies_in_row = [e for e in game_state.enemies if e.y == day_idx]
            enemies_in_row.sort(key=lambda e: e.x * (day_idx % 2 * 2 - 1)) # zig-zag

            for enemy in enemies_in_row:
                for _ in range(enemy.health):
                    yield Action(x=enemy.x, shoot=True)
