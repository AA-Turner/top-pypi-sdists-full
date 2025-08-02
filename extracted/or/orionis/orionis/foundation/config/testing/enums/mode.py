from enum import Enum

class ExecutionMode(Enum):
    """
    Enumeration of possible execution modes for running tests.

    Attributes:
        SEQUENTIAL: Execute tests one after another in sequence.
        PARALLEL: Execute tests concurrently in parallel.
    """
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
