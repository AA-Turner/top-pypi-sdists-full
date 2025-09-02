class PoolSenseError(Exception):
    """Raised when PoolSense request ended in error.

    Attributes:
        status_code - error code returned by the PoolSense server
        status - more detailed description
        """

    def __init__(self, status_code, status):
        self.status_code = status_code
        self.status = status
