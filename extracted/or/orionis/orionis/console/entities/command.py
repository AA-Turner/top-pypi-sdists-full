import argparse
from dataclasses import dataclass
from typing import Type, Optional
from orionis.support.entities.base import BaseEntity

@dataclass(kw_only=True)
class Command(BaseEntity):
    """
    Represents a console command and its associated metadata.

    Parameters
    ----------
    obj : Type
        The type or class associated with the command.
    timestamps : bool
        Whether timestamps are enabled for this command.
    signature : str
        The signature string representing the command usage.
    description : str
        A brief description of what the command does.
    args : Optional[argparse.ArgumentParser], optional
        Optional argument parser for command-line arguments.

    Returns
    -------
    Command
        An instance of the Command class containing metadata and configuration for a console command.
    """

    # The type or class associated with the command
    obj: Type

    # The method name to be invoked on the object
    method: str = 'hanldle'

    # Indicates if timestamps are enabled for this command
    timestamps: bool

    # The command usage signature
    signature: str

    # Description of the command's purpose
    description: str

    # Optional argument parser for command-line arguments
    args: Optional[argparse.ArgumentParser] = None