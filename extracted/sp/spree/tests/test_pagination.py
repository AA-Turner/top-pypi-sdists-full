import pytest
from spree.spree import Pagination


@pytest.fixture
def page():
    return Pagination()
