from enum import Enum, auto

class TestStatus(Enum):
    """
    Enumeration of possible statuses for a test during execution.

    Members
    -------
    PASSED : enum
        Indicates the test completed successfully without errors or failures.
    FAILED : enum
        Indicates the test completed but did not produce the expected results.
    ERRORED : enum
        Indicates an unexpected error occurred during test execution.
    SKIPPED : enum
        Indicates the test was intentionally not executed.
    """
    PASSED = auto()   # Test executed successfully
    FAILED = auto()   # Test executed but failed
    ERRORED = auto()  # Error occurred during test execution
    SKIPPED = auto()  # Test was intentionally skipped
