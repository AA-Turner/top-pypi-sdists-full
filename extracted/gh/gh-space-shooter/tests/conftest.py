"""Shared test fixtures for gh-space-shooter tests."""

import pytest
from gh_space_shooter.game.game_state import GameState
from gh_space_shooter.github_client import ContributionData


@pytest.fixture
def empty_contribution_data() -> ContributionData:
    """Create contribution data with no contributions."""
    return {
        "weeks": [
            {
                "days": [
                    {"level": 0, "date": "", "count": 0} for _ in range(7)
                ]
            }
            for _ in range(52)
        ],
        "total_contributions": 0,
        "username": "test_user",
    }

@pytest.fixture
def default_game_state(empty_contribution_data):
    """Create a game state with no enemies."""
    return GameState(empty_contribution_data)