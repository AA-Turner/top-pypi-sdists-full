"""Typed exceptions raised by binding helpers, caught by step error handlers."""


class AssertionFailureError(AssertionError):
    """Raised by verify_assertion / evaluate_network_assertion on failed status.

    Subclasses AssertionError so legacy generic catches still work; step
    error handlers may use isinstance to discriminate assertion failures
    from other exceptions.
    """

    def __init__(self, message: str = "", result=None):
        super().__init__(message)
        self.result = result
