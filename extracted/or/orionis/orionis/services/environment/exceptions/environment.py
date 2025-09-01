class OrionisEnvironmentValueException(Exception):
    """
    Exception raised for invalid or unexpected values in the Orionis environment configuration.

    This exception is used to indicate that an environment variable or configuration setting
    within the Orionis framework does not conform to the expected value constraints.

    Parameters
    ----------
    message : str, optional
        Explanation of the error.

    Returns
    -------
    OrionisEnvironmentValueException
        An instance of this exception is raised when an invalid environment value is encountered.

    Attributes
    ----------
    message : str
        Optional explanation of the error.
    """
    # No additional implementation; inherits from Exception
    pass

class OrionisEnvironmentTypeException(Exception):
    """
    Exception raised for invalid or unsupported environment types in the Orionis framework.

    This exception signals that an environment type provided to the framework is not recognized
    or is not supported according to the framework's requirements.

    Parameters
    ----------
    message : str, optional
        Description of the error.

    Returns
    -------
    OrionisEnvironmentTypeException
        An instance of this exception is raised when an invalid environment type is encountered.

    Attributes
    ----------
    message : str
        Optional error message describing the exception.
    """
    # No additional implementation; inherits from Exception
    pass

class OrionisEnvironmentValueError(Exception):
    """
    Exception raised when a value does not meet the required criteria in the Orionis environment configuration.

    This exception is typically used to indicate that a provided value violates constraints or
    requirements defined by the environment settings in the Orionis framework.

    Parameters
    ----------
    message : str, optional
        Explanation of the error.

    Returns
    -------
    OrionisEnvironmentValueError
        An instance of this exception is raised when a value fails validation.

    Attributes
    ----------
    message : str
        Optional explanation of the error.
    """
    # No additional implementation; inherits from Exception
    pass

class OrionisOperatingSystemError(OSError):
    """
    Exception raised when a value or parameter in the Orionis environment configuration has an incorrect type.

    This exception is used to signal that a provided value does not match the expected type as required by
    the Orionis framework's environment settings, which may lead to misconfiguration or runtime errors.

    Parameters
    ----------
    message : str, optional
        Description of the type mismatch error.

    Returns
    -------
    OrionisOperatingSystemError
        An instance of this exception is raised when a type mismatch is detected in the environment configuration.

    Attributes
    ----------
    message : str
        Optional error message describing the exception.
    """
    # No additional implementation; inherits from OSError
    pass

class OrionisEnvironmentException(Exception):
    """
    General exception for errors related to the Orionis environment configuration.

    This exception serves as a base class for more specific environment-related exceptions
    within the Orionis framework. It can be used to catch all environment-related errors
    in a single exception handler.

    Parameters
    ----------
    message : str, optional
        Description of the error.

    Returns
    -------
    OrionisEnvironmentException
        An instance of this exception is raised for general environment-related errors.

    Attributes
    ----------
    message : str
        Optional error message describing the exception.
    """
    # No additional implementation; inherits from Exception
    pass