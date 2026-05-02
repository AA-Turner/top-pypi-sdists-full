"""Random strategy: Pick random columns and shoot from bottom up."""

import random
from typing import TYPE_CHECKING, Iterator

from .base_strategy import Action, BaseStrategy

if TYPE_CHECKING:
    from ..game_state import GameState


class RandomStrategy(BaseStrategy):
    """
    Ship uses weighted random selection to pick columns based on distance.

    Takes the 8 closest columns and applies distance-based weights for selection,
    creating a balanced mix of efficiency and unpredictability.
    """

    def generate_actions(self, game_state: "GameState") -> Iterator[Action]:
        """
        Generate actions using weighted random selection based on distance.

        Sorts columns by distance, takes the 8 closest, and applies weights:
        - Distance 0 (same position): weight 3
        - Distance 1-3: weight 5 (highest priority)
        - Distance 4+: weight 1 (lowest priority)

        Args:
            game_state: The current game state with living enemies

        Yields:
            Action objects representing ship movements and shots
        """
        while game_state.enemies:
            columns_with_enemies = list(set(e.x for e in game_state.enemies))
            ship_x = game_state.ship.x

            # Take the first 8 closest columns
            columns_by_distance = sorted(columns_with_enemies, key=lambda col: abs(col - ship_x))
            candidate_columns = columns_by_distance[:8]

            # Assign weights based on distance
            weights = []
            for col in candidate_columns:
                distance = abs(col - ship_x)
                if distance == 0:
                    weights.append(10)
                elif 1 <= distance <= 3:
                    weights.append(100)
                else:  # distance >= 4
                    weights.append(1)

            # Choose randomly with weights
            target_column = random.choices(candidate_columns, weights=weights)[0]

            enemies_in_column = [e for e in game_state.enemies if e.x == target_column]
            lowest_enemy = max(enemies_in_column, key=lambda e: e.y)

            for _ in range(lowest_enemy.health):
                yield Action(x=target_column, shoot=True)
