from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity

@dataclass(kw_only=True)
class CLIRequest(BaseEntity):
    """
    Represents a command-line interface (CLI) request.

    Parameters
    ----------
    command : str
        The command to be executed by the CLI.
    args : list of str, optional
        A list of arguments passed to the command. Defaults to an empty list.

    Returns
    -------
    CLIRequest
        An instance of the CLIRequest class encapsulating the command and its arguments.

    Attributes
    ----------
    command : str
        The command to be executed.
    args : list of str
        The arguments associated with the command.
    """

    # The command to execute
    command: str

    # Arguments for the command; defaults to an empty list if not provided
    args: list[str] = field(
        default_factory=list
    )