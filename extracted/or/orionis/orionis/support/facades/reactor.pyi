from typing import Any, List, Optional
from orionis.console.contracts.command import ICommand
from orionis.console.contracts.reactor import IReactor

class Reactor(IReactor):
    """
    Reactor facade class that implements the IReactor interface.

    This class serves as a facade for reactor functionality, providing a simplified
    interface for event-driven programming and asynchronous operations. It acts as
    a wrapper around the underlying reactor implementation, abstracting away the
    complexity of the reactor pattern and providing a clean abstraction layer.

    The Reactor class follows the facade design pattern, offering a unified and
    consistent API for managing events, callbacks, timers, and asynchronous
    operations within the Orionis framework. It encapsulates the complexity of
    event loop management and provides thread-safe access to reactor functionality.

    Parameters
    ----------
    None
        This facade class typically doesn't require initialization parameters
        as it wraps an existing reactor implementation.

    Attributes
    ----------
    None
        Attributes are defined by the underlying IReactor interface implementation.

    Notes
    -----
    This is a type stub file (.pyi) used for type checking and IDE support.
    The actual implementation should be provided in the corresponding .py file.
    The reactor pattern is essential for handling I/O operations, network events,
    and other asynchronous operations in a non-blocking manner.

    See Also
    --------
    IReactor : The interface contract that this facade implements
    """

    @classmethod
    def command(cls, signature: str, handler: Any) -> ICommand:
        """
        Define a new command using a fluent interface.

        Parameters
        ----------
        signature : str
            The unique signature identifier for the command.
        handler : Any
            The function or callable that will be executed when the command is invoked.

        Returns
        -------
        ICommand
            Returns an instance of ICommand that allows further configuration.
        """
        ...

    @classmethod
    def call(cls, signature: str, args: Optional[List[str]] = None) -> Optional[Any]:
        """
        Executes a registered command synchronously by its signature.

        Parameters
        ----------
        signature : str
            The unique signature identifier of the command to execute.
        args : Optional[List[str]], default None
            List of command-line arguments to pass to the command.

        Returns
        -------
        Optional[Any]
            The output produced by the command's handle method if execution is successful.
        """
        ...

    @classmethod
    async def callAsync(cls, signature: str, args: Optional[List[str]] = None) -> Optional[Any]:
        """
        Executes a registered command asynchronously by its signature.

        Parameters
        ----------
        signature : str
            The unique signature identifier of the command to execute.
        args : Optional[List[str]], default None
            List of command-line arguments to pass to the command.

        Returns
        -------
        Optional[Any]
            The output produced by the command's handle method if execution is successful.
        """
        ...
