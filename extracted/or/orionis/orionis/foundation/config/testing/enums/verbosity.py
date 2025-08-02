from enum import Enum

class VerbosityMode(Enum):
    """
    Enumeration of verbosity levels for output during testing.

    Attributes
    ----------
    SILENT : int
        No output will be shown.
    MINIMAL : int
        Minimal output will be displayed.
    DETAILED : int
        Detailed output will be provided (default).
    """
    SILENT = 0        # 0: Silent
    MINIMAL = 1       # 1: Minimal output
    DETAILED = 2      # 2: Detailed output (default)