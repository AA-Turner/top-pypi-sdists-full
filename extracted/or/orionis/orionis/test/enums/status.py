from enum import Enum, auto

class TestStatus(Enum):
    """
    TestStatus(Enum)
    An enumeration representing the possible statuses that a test can have during its execution.

    Attributes
    ----------
    PASSED : auto()
        The test completed successfully without any errors or failures.
    FAILED : auto()
        The test ran to completion but did not produce the expected results.
    ERRORED : auto()
        An unexpected error occurred during the execution of the test, preventing it from completing.
    SKIPPED : auto()
        The test was intentionally not executed, typically due to configuration or conditional logic.

    Returns
    -------
    TestStatus
        An instance of the TestStatus enumeration indicating the current status of a test.
    """
    PASSED = auto()   # Test executed successfully
    FAILED = auto()   # Test executed but failed
    ERRORED = auto()  # Error occurred during test execution
    SKIPPED = auto()  # Test was intentionally skipped