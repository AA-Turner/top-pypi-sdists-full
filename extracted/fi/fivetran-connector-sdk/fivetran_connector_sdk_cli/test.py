"""The result a connector's setup test returns: `Test.success()` or `Test.failure(message)`."""
from dataclasses import dataclass
from typing import Optional

from fivetran_connector_sdk_cli import wire


@dataclass(frozen=True)
class TestResponse:
    """Exactly one of `success` (True) or `failure` (a message) is set; neither is, if built with no message."""
    success: Optional[bool] = None
    failure: Optional[str] = None


class Test:
    """Factory for connector setup test responses.

    Instantiate once per test function, then call success() or failure().

    Example:
        def connection_test(configuration: dict):
            test = Test()
            try:
                connect(configuration)
                return test.success()
            except Exception as e:
                return test.failure(str(e))
    """

    @staticmethod
    def success() -> TestResponse:
        """Returns a successful test response."""
        return TestResponse(success=True)

    @staticmethod
    def failure(message: str) -> TestResponse:
        """Returns a failed test response.

        Args:
            message: Human-readable description of why the test failed.
        """
        if message is None:
            return TestResponse()
        return TestResponse(failure=wire.text(message))
