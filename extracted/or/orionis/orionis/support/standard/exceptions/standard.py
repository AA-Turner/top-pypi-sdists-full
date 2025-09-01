class OrionisStdValueException(Exception):
    """
    Exception raised for errors related to invalid or unexpected values in the Orionis standard support module.

    This exception should be used when a function or operation encounters a value that does not satisfy the required criteria or constraints.

    Parameters
    ----------
    message : str, optional
        Error message describing the reason for the exception.

    Returns
    -------
    OrionisStdValueException
        An instance of the exception with an optional error message.

    Attributes
    ----------
    message : str
        Optional error message describing the reason for the exception.
    """
    # Inherits from the built-in Exception class to define a custom exception
    pass