class CLIOrionisException(Exception):
    """
    Base exception for Orionis CLI errors.

    This exception is raised for errors that are specific to the Orionis command-line interface (CLI)
    operations. It serves as the base class for all CLI-related exceptions within the Orionis framework,
    allowing for consistent error handling and identification of CLI-specific issues.

    Parameters
    ----------
    message : str, optional
        An optional error message describing the exception.

    Returns
    -------
    CLIOrionisException
        An instance of the CLIOrionisException class.

    Notes
    -----
    Subclass this exception to create more specific CLI-related exceptions as needed.
    """
    pass  # No additional implementation; serves as a base exception class.


class CLIOrionisValueError(ValueError):
    """
    Exception for invalid CLI input values in Orionis.

    Raised when a function receives an argument of the correct type but an inappropriate value
    during CLI operations within the Orionis framework.

    Parameters
    ----------
    message : str, optional
        An optional error message describing the value error.

    Returns
    -------
    CLIOrionisValueError
        An instance of the CLIOrionisValueError class.

    Notes
    -----
    Use this exception to signal invalid or inappropriate values encountered during CLI operations.
    """
    pass  # Inherits from ValueError to indicate value-related errors.


class CLIOrionisRuntimeError(RuntimeError):
    """
    Exception for runtime errors in Orionis CLI.

    Raised when a runtime error occurs during the execution of CLI commands within the Orionis framework,
    distinguishing these errors from other runtime errors.

    Parameters
    ----------
    message : str, optional
        An optional error message describing the runtime error.

    Returns
    -------
    CLIOrionisRuntimeError
        An instance of the CLIOrionisRuntimeError class.

    Notes
    -----
    Use this exception to handle runtime errors specific to CLI contexts.
    """
    pass  # Inherits from RuntimeError for CLI-specific runtime issues.


class CLIOrionisScheduleException(Exception):
    """
    Exception for scheduling errors in Orionis CLI.

    Raised when issues are encountered during scheduling tasks within the Orionis command-line interface.

    Parameters
    ----------
    message : str, optional
        An optional error message describing the scheduling exception.

    Returns
    -------
    CLIOrionisScheduleException
        An instance of the CLIOrionisScheduleException class.

    Notes
    -----
    Use this exception to signal errors related to scheduling operations in the CLI.
    """
    pass  # Used for errors related to scheduling operations.


class CLIOrionisTypeError(TypeError):
    """
    Exception for invalid types in Orionis CLI.

    Raised when an invalid type is encountered during command-line interface operations in the Orionis framework,
    providing clearer context than the built-in TypeError.

    Parameters
    ----------
    message : str, optional
        An optional error message describing the type error.

    Returns
    -------
    CLIOrionisTypeError
        An instance of the CLIOrionisTypeError class.

    Notes
    -----
    Use this exception to handle type-related errors specific to CLI operations.
    """
    pass  # Inherits from TypeError for CLI-specific type errors.