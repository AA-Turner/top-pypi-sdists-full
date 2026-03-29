import pytest

from pydifact.parser import AEKParser


@pytest.fixture
def parser():
    return AEKParser()
