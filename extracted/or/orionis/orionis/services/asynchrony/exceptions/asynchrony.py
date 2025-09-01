class OrionisCoroutineException(Exception):
    """
    Exception raised for errors that occur within Orionis coroutines.

    This exception serves as a base for coroutine-related errors in the Orionis framework,
    allowing for more specific exception handling in asynchronous operations.

    Attributes:
        message (str): Optional error message describing the exception.
    """
    pass