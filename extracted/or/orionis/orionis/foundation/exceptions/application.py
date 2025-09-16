class OrionisIntegrityException(Exception):
    """
    Exception raised for integrity-related errors in the Orionis framework.

    This exception is intended to signal violations of data integrity or
    consistency constraints within the application.

    Returns
    -------
    OrionisIntegrityException
        An instance of the exception.
    """

    # No additional logic; inherits from base Exception
    pass


class OrionisRuntimeError(RuntimeError):
    """
    Exception raised for runtime errors specific to the Orionis framework.

    This exception should be used when an error occurs that is only detectable
    during program execution.

    Returns
    -------
    OrionisRuntimeError
        An instance of the exception.
    """

    # Inherits from Python's built-in RuntimeError
    pass


class OrionisTypeError(TypeError):
    """
    Exception raised for type errors in the Orionis framework.

    This exception is used when an operation or function receives an argument
    of an inappropriate type.

    Returns
    -------
    OrionisTypeError
        An instance of the exception.
    """

    # Inherits from Python's built-in TypeError
    pass


class OrionisValueError(ValueError):
    """
    Exception raised for value errors in the Orionis framework.

    This exception is used when an operation or function receives an argument
    with the right type but an inappropriate value.

    Returns
    -------
    OrionisValueError
        An instance of the exception.
    """

    # Inherits from Python's built-in ValueError
    pass