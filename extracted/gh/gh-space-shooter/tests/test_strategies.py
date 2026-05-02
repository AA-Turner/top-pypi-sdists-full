"""Tests for game strategies (column, row, random)."""

import pytest
from gh_space_shooter.game.game_state import GameState
from gh_space_shooter.game.drawables import Enemy, Bullet
from gh_space_shooter.game.strategies.column_strategy import ColumnStrategy
from gh_space_shooter.game.strategies.row_strategy import RowStrategy
from gh_space_shooter.game.strategies.random_strategy import RandomStrategy


class TestColumnStrategy:
    """Tests for ColumnStrategy."""

    @pytest.fixture
    def column_strategy(self):
        """Create a ColumnStrategy instance."""
        return ColumnStrategy()

    def testdefault_game_state_game_state(self, default_game_state: GameState, column_strategy: ColumnStrategy) -> None:
        """Test that strategy handles empty game state (no enemies)."""
        actions = list(column_strategy.generate_actions(default_game_state))
        assert actions == []

    def test_single_enemy(self, default_game_state: GameState, column_strategy: ColumnStrategy) -> None:
        """Test strategy with a single enemy."""
        default_game_state.enemies = [Enemy(x=5, y=3, health=1, game_state=default_game_state)]

        action_gen = column_strategy.generate_actions(default_game_state)

        action = next(action_gen)
        assert action.x == 5
        assert action.shoot is True

    def test_multiple_enemies_same_column(self, default_game_state: GameState, column_strategy: ColumnStrategy) -> None:
        """Test strategy with multiple enemies in the same column."""

        default_game_state.enemies = [
            Enemy(x=3, y=0, health=2, game_state=default_game_state),
            Enemy(x=3, y=5, health=1, game_state=default_game_state),
        ]

        action_gen = column_strategy.generate_actions(default_game_state)

        actions = []
        for _ in range(3):  # Total health is 3
            action = next(action_gen)
            actions.append(action)
            default_game_state.bullets.append(Bullet(x=3, game_state=default_game_state))

        assert len(actions) == 3
        assert all(action.x == 3 for action in actions)
        assert all(action.shoot for action in actions)

    def test_processes_columns_left_to_right(self, default_game_state: GameState, column_strategy: ColumnStrategy) -> None:
        """Test that strategy processes columns from left to right."""

        default_game_state.enemies = [
            Enemy(x=10, y=0, health=1, game_state=default_game_state),
            Enemy(x=2, y=0, health=1, game_state=default_game_state),
            Enemy(x=5, y=0, health=1, game_state=default_game_state),
        ]

        action_gen = column_strategy.generate_actions(default_game_state)

        actions = []
        for col in [2, 5, 10]:
            action = next(action_gen)
            actions.append(action)
            default_game_state.bullets.append(Bullet(x=col, game_state=default_game_state))

        # Should process in order: column 2, then 5, then 10
        assert len(actions) == 3
        assert actions[0].x == 2
        assert actions[1].x == 5
        assert actions[2].x == 10

    def test_bullets_already_in_flight(self, default_game_state: GameState, column_strategy: ColumnStrategy) -> None:
        """Test that strategy accounts for bullets already in flight."""

        default_game_state.enemies = [Enemy(x=4, y=0, health=2, game_state=default_game_state)]
        bullet = Bullet(x=4, game_state=default_game_state)
        default_game_state.bullets = [bullet]

        action_gen = column_strategy.generate_actions(default_game_state)

        # Should only shoot 1 more time since 1 bullet is already in flight
        action = next(action_gen)
        assert action.x == 4

        # Add second bullet to reach total health
        default_game_state.bullets.append(Bullet(x=4, game_state=default_game_state))


class TestRowStrategy:
    """Tests for RowStrategy."""

    @pytest.fixture
    def row_strategy(self):
        """Create a RowStrategy instance."""
        return RowStrategy()


    def testdefault_game_state_game_state(self, default_game_state: GameState, row_strategy: RowStrategy) -> None:
        """Test that strategy handles empty game state (no enemies)."""
        actions = list(row_strategy.generate_actions(default_game_state))
        assert actions == []

    def test_single_enemy(self, default_game_state: GameState, row_strategy: RowStrategy) -> None:
        """Test strategy with a single enemy."""
        default_game_state.enemies = [Enemy(x=5, y=3, health=2, game_state=default_game_state)]

        actions = list(row_strategy.generate_actions(default_game_state))

        # Should shoot twice (health=2) at position 5
        assert len(actions) == 2
        assert all(action.x == 5 for action in actions)
        assert all(action.shoot for action in actions)

    def test_processes_rows_bottom_to_top(self, default_game_state: GameState, row_strategy: RowStrategy) -> None:
        """Test that strategy processes rows from bottom (day 6) to top (day 0)."""

        default_game_state.enemies = [
            Enemy(x=0, y=0, health=1, game_state=default_game_state),  # Top row
            Enemy(x=1, y=3, health=1, game_state=default_game_state),  # Middle row
            Enemy(x=2, y=6, health=1, game_state=default_game_state),  # Bottom row
        ]

        actions = list(row_strategy.generate_actions(default_game_state))
        assert len(actions) == 3
        assert actions[0].x == 2  # Day 6
        assert actions[1].x == 1  # Day 3
        assert actions[2].x == 0  # Day 0

    def test_zigzag_pattern_in_same_row(self, default_game_state: GameState, row_strategy: RowStrategy) -> None:
        """Test that enemies in the same row are processed in zig-zag pattern."""

        default_game_state.enemies = [
            Enemy(x=0, y=5, health=1, game_state=default_game_state),
            Enemy(x=5, y=5, health=1, game_state=default_game_state),
            Enemy(x=10, y=5, health=1, game_state=default_game_state),
        ]

        actions = list(row_strategy.generate_actions(default_game_state))
        assert len(actions) == 3
        assert actions[0].x == 0
        assert actions[1].x == 5
        assert actions[2].x == 10

    def test_respects_enemy_health(self, default_game_state: GameState, row_strategy: RowStrategy) -> None:
        """Test that strategy shoots multiple times for enemies with high health."""

        default_game_state.enemies = [
            Enemy(x=3, y=2, health=4, game_state=default_game_state),
        ]

        actions = list(row_strategy.generate_actions(default_game_state))

        assert len(actions) == 4
        assert all(action.x == 3 for action in actions)
        assert all(action.shoot for action in actions)


class TestRandomStrategy:
    """Tests for RandomStrategy."""

    @pytest.fixture
    def random_strategy(self):
        """Create a RandomStrategy instance."""
        return RandomStrategy()


    def testdefault_game_state_game_state(self, default_game_state: GameState, random_strategy: RandomStrategy) -> None:
        """Test that strategy handles empty game state (no enemies)."""
        actions = list(random_strategy.generate_actions(default_game_state))
        assert actions == []

    def test_single_enemy(self, default_game_state: GameState, random_strategy: RandomStrategy) -> None:
        """Test strategy with a single enemy."""

        enemy = Enemy(x=5, y=3, health=3, game_state=default_game_state)
        default_game_state.enemies = [enemy]

        action_gen = random_strategy.generate_actions(default_game_state)

        actions = []
        for i in range(3):  # Health is 3
            action = next(action_gen)
            actions.append(action)
            enemy.health -= 1
            if enemy.health == 0:
                default_game_state.enemies.remove(enemy)

        # Should shoot 3 times (health=3) at position 5
        assert len(actions) == 3
        assert all(action.x == 5 for action in actions)
        assert all(action.shoot for action in actions)

    def test_targets_lowest_enemy_in_column(self, default_game_state: GameState, random_strategy: RandomStrategy) -> None:
        """Test that strategy targets the lowest enemy (highest y value) in a column."""

        # Multiple enemies in same column, different y positions
        enemy1 = Enemy(x=5, y=1, health=1, game_state=default_game_state)
        enemy2 = Enemy(x=5, y=4, health=2, game_state=default_game_state)
        enemy3 = Enemy(x=5, y=2, health=1, game_state=default_game_state)
        default_game_state.enemies = [enemy1, enemy2, enemy3]

        action_gen = random_strategy.generate_actions(default_game_state)

        action1 = next(action_gen)
        assert action1.x == 5
        enemy2.health -= 1

        action2 = next(action_gen)
        assert action2.x == 5
        enemy2.health -= 1
        if enemy2.health == 0:
            default_game_state.enemies.remove(enemy2)

    def test_clears_all_enemies(self, default_game_state: GameState, random_strategy: RandomStrategy) -> None:
        """Test that strategy eventually clears all enemies."""

        default_game_state.enemies = [
            Enemy(x=1, y=0, health=2, game_state=default_game_state),
            Enemy(x=5, y=3, health=1, game_state=default_game_state),
            Enemy(x=10, y=1, health=1, game_state=default_game_state),
        ]

        total_health = sum(e.health for e in default_game_state.enemies)
        actions = []

        for action in random_strategy.generate_actions(default_game_state):
            actions.append(action)
            column_enemies = [e for e in default_game_state.enemies if e.x == action.x]
            if column_enemies:
                target = max(column_enemies, key=lambda e: e.y)
                target.health -= 1
                if target.health <= 0:
                    default_game_state.enemies.remove(target)

        assert len(actions) == total_health
        assert len(default_game_state.enemies) == 0
    

    def test_selects_from_closest_columns(self, default_game_state: GameState, random_strategy: RandomStrategy) -> None:
        """Test that strategy only considers the 8 closest columns."""

        for i in range(0, 52, 5):
            default_game_state.enemies.append(Enemy(x=i, y=0, health=1, game_state=default_game_state))

        default_game_state.ship.x = 25.0

        action_gen = random_strategy.generate_actions(default_game_state)
        first_action = next(action_gen)

        # Closest columns: 20, 25, 30, 15, 35, 10, 40, 5
        closest_8 = sorted([i for i in range(0, 52, 5)], key=lambda x: abs(x - 25))[:8]
        assert first_action.x in closest_8

    def test_respects_enemy_health_counts(self, default_game_state: GameState, random_strategy: RandomStrategy) -> None:
        """Test that multiple shots are generated for high-health enemies."""

        enemy = Enemy(x=10, y=5, health=4, game_state=default_game_state)
        default_game_state.enemies = [enemy]
        action_gen = random_strategy.generate_actions(default_game_state)

        actions = []
        for i in range(4):
            action = next(action_gen)
            actions.append(action)
            enemy.health -= 1
            if enemy.health == 0:
                default_game_state.enemies.remove(enemy)

        assert len(actions) == 4
        assert all(action.x == 10 for action in actions)
        assert all(action.shoot for action in actions)
