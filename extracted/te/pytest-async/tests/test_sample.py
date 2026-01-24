# Sample Test passing with nose and pytest
import pytest


@pytest.fixture
async def fix():
    return 1


async def test_pass(fix):
    assert not fix, "dummy sample test"


def test_sync(fix):
    assert not fix
