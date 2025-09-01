class ReflectionAttributeError(Exception):
    """
    Exception raised when an attribute cannot be found during reflection or introspection operations.

    This exception is typically raised when attempting to access an attribute that does not exist
    or is not accessible on the target object during reflection or introspection.

    Parameters
    ----------
    *args : tuple
        Variable length argument list passed to the base Exception.
    **kwargs : dict
        Arbitrary keyword arguments passed to the base Exception.

    Returns
    -------
    ReflectionAttributeError
        An instance of the ReflectionAttributeError exception.

    Notes
    -----
    This exception does not define additional attributes beyond those provided by Exception.
    """
    pass  # Custom exception for attribute errors during reflection


class ReflectionTypeError(Exception):
    """
    Exception raised when a type-related error occurs during reflection or introspection operations.

    This exception signals issues such as invalid type usage, type mismatches, or unsupported types
    encountered while performing reflection-based logic.

    Parameters
    ----------
    *args : tuple
        Variable length argument list passed to the base Exception.
    **kwargs : dict
        Arbitrary keyword arguments passed to the base Exception.

    Returns
    -------
    ReflectionTypeError
        An instance of the ReflectionTypeError exception.

    Notes
    -----
    This exception does not define additional attributes beyond those provided by Exception.
    """
    pass  # Custom exception for type errors during reflection


class ReflectionValueError(Exception):
    """
    Exception raised when a reflection operation encounters an invalid or unexpected value.

    This exception is used within introspection services to indicate that a value obtained or
    manipulated via reflection does not meet the expected criteria or format.

    Parameters
    ----------
    *args : tuple
        Variable length argument list passed to the base Exception.
    **kwargs : dict
        Arbitrary keyword arguments passed to the base Exception.

    Returns
    -------
    ReflectionValueError
        An instance of the ReflectionValueError exception.

    Notes
    -----
    This exception does not define additional attributes beyond those provided by Exception.
    """
    pass  # Custom exception for value errors during reflection