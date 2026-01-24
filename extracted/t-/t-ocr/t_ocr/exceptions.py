"""Module with various exceptions."""


class StepFunctionAWSError(Exception):
    """Class for AWS Step Function error."""

    pass


class LimitExceededError(Exception):
    """Class for limit exceeded error."""

    pass


class TOCRWarning(UserWarning):
    """Class for t_ocr warning."""

    pass
