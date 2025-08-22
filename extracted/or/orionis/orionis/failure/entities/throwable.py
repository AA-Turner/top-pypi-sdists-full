from dataclasses import dataclass

@dataclass(kw_only=True)
class Throwable:
    """
    Represents a throwable entity (such as an exception or error) within the framework.

    Parameters
    ----------
    classtype : type
        The class type of the throwable, typically an exception class.
    message : str
        The error message describing the throwable.
    args : tuple
        Arguments passed to the throwable, usually corresponding to the exception arguments.
    traceback : str, optional
        The traceback information as a string, if available. Defaults to None.

    Returns
    -------
    Throwable
        An instance of the Throwable dataclass encapsulating exception details.

    Notes
    -----
    This class is used to standardize the representation of exceptions and errors
    throughout the framework, making error handling and logging more consistent.
    """

    classtype: type          # The type of the throwable (e.g., Exception class)
    message: str             # The error message associated with the throwable
    args: tuple              # Arguments passed to the throwable
    traceback: str = None    # Optional traceback information as a string