import pytest
from mockito import unstub


@pytest.fixture(autouse=True, scope="function")
def auto_unstub():
    """
    Automatically unstub after all tests.  Especially relevant if verifyNoUnwantedInteractions
    is used, as if the test fails during that call, the test exits and doesn't reach any code
    after.
    """
    yield
    unstub()
