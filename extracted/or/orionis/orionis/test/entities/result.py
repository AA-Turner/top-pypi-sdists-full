from dataclasses import dataclass, field
from typing import Any, Optional
from orionis.test.enums import TestStatus

@dataclass(frozen=True, kw_only=True)
class TestResult:
    """
    Data class representing the outcome of a test execution.

    This class encapsulates all relevant information about a test's execution,
    including its unique identifier, name, execution status, timing, and any
    error details if the test did not pass. It also stores optional metadata
    such as the class, method, module, file path, and docstring associated
    with the test, if applicable.

    Attributes:
        id (Any): Unique identifier for the test result.
        name (str): Name of the test.
        status (TestStatus): Status of the test execution (e.g., passed, failed).
        execution_time (float): Time taken to execute the test, in seconds.
        error_message (Optional[str]): Error message if the test failed, otherwise None.
        traceback (Optional[str]): Traceback information if an error occurred, otherwise None.
        class_name (Optional[str]): Name of the class containing the test, if applicable.
        method (Optional[str]): Name of the method representing the test, if applicable.
        module (Optional[str]): Name of the module containing the test, if applicable.
        file_path (Optional[str]): Path to the file containing the test, if applicable.
        doc_string (Optional[str]): Docstring of the test, if applicable.

    Returns:
        TestResult: An immutable instance containing all details about a single test execution.
    """

    # Unique identifier for the test result
    id: Any = field(
        metadata={
            "description": "Unique identifier for the test result."
        }
    )

    # Name of the test
    name: str = field(
        metadata={
            "description": "Name of the test."
        }
    )

    # Status of the test execution (e.g., passed, failed)
    status: TestStatus = field(
        metadata={
            "description": "Status of the test execution (e.g., passed, failed)."
        }
    )

    # Time taken to execute the test, in seconds
    execution_time: float = field(
        metadata={
            "description": "Time taken to execute the test, in seconds."
        }
    )

    # Error message if the test failed, otherwise None
    error_message: Optional[str] = field(
        default=None,
        metadata={
            "description": "Error message if the test failed, otherwise None."
        }
    )

    # Traceback information if an error occurred, otherwise None
    traceback: Optional[str] = field(
        default=None,
        metadata={
            "description": "Traceback information if an error occurred, otherwise None."
        }
    )

    # Name of the class containing the test, if applicable
    class_name: Optional[str] = field(
        default=None,
        metadata={
            "description": "Name of the class containing the test, if applicable."
        }
    )

    # Name of the method representing the test, if applicable
    method: Optional[str] = field(
        default=None,
        metadata={
            "description": "Name of the method representing the test, if applicable."
        }
    )

    # Name of the module containing the test, if applicable
    module: Optional[str] = field(
        default=None,
        metadata={
            "description": "Name of the module containing the test, if applicable."
        }
    )

    # Path to the file containing the test, if applicable
    file_path: Optional[str] = field(
        default=None,
        metadata={
            "description": "Path to the file containing the test, if applicable."
        }
    )

    # Docstring of the test, if applicable
    doc_string: Optional[str] = field(
        default=None,
        metadata={
            "description": "Docstring of the test, if applicable."
        }
    )