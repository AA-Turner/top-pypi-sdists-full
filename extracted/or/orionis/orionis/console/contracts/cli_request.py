from abc import ABC, abstractmethod
from typing import Any

class ICLIRequest(ABC):

    @abstractmethod
    def command(self) -> str:
        """
        Retrieve the command name associated with this CLI request.

        This method provides access to the command string that was specified during
        the initialization of the CLIRequest object. The command represents the
        primary action or operation that should be executed based on the CLI input.

        Returns
        -------
        str
            The command name stored as a string. This is the exact command value
            that was passed to the constructor during object initialization.

        Notes
        -----
        The returned command string is immutable and represents the core action
        identifier for this CLI request. This value is essential for determining
        which operation should be performed by the CLI handler.
        """
        pass

    @abstractmethod
    def all(self) -> dict:
        """
        Retrieve all command line arguments as a complete dictionary.

        This method provides access to the entire collection of command line arguments
        that were passed during the initialization of the CLIRequest object. It returns
        a reference to the internal arguments dictionary, allowing for comprehensive
        access to all parsed CLI parameters.

        Returns
        -------
        dict
            A dictionary containing all the parsed command line arguments as key-value
            pairs, where keys are argument names (str) and values are the corresponding
            argument values of any type. If no arguments were provided during
            initialization, returns an empty dictionary.

        Notes
        -----
        This method returns a reference to the internal arguments dictionary rather
        than a copy. Modifications to the returned dictionary will affect the
        internal state of the CLIRequest object.
        """
        pass

    @abstractmethod
    def argument(self, name: str, default: Any = None):
        """
        Retrieve the value of a specific command line argument by its name.

        This method provides access to individual command line arguments that were
        passed during initialization. It safely retrieves argument values without
        raising exceptions if the argument doesn't exist.

        Parameters
        ----------
        name : str
            The name of the command line argument to retrieve. This should match
            the key used when the argument was originally parsed and stored.
        default : Any, optional
            The default value to return if the specified argument name does not
            exist in the arguments dictionary. Defaults to None.

        Returns
        -------
        Any or None
            The value associated with the specified argument name if it exists
            in the arguments dictionary. Returns None if the argument name is
            not found or was not provided during CLI execution.

        Notes
        -----
        This method uses the dictionary's get() method to safely access values,
        ensuring that missing arguments return None rather than raising a KeyError.
        """
        pass

    def getCWD(self) -> str:
        """
        Retrieve the current working directory (CWD) as an absolute path.

        This method returns the absolute path of the directory from which the Python process was started.
        It is useful for determining the context in which the CLI command is being executed, especially
        when dealing with relative file paths or when the working directory may affect application behavior.

        Returns
        -------
        str
            The absolute path to the current working directory as a string.
        """
        pass

    def getPID(self) -> int:
        """
        Retrieve the process ID (PID) of the current Python process.

        This method returns the unique identifier assigned by the operating system
        to the currently running Python process. The PID can be useful for logging,
        debugging, or managing process-related operations.

        Returns
        -------
        int
            The process ID (PID) of the current Python process as an integer.
        """
        pass

    def getParentPID(self) -> int:
        """
        Retrieve the parent process ID (PPID) of the current Python process.

        This method returns the process ID of the parent process that spawned the current
        Python process. The parent process ID can be useful for tracking process hierarchies,
        debugging, or managing process relationships in CLI applications.

        Returns
        -------
        int
            The parent process ID (PPID) as an integer. This value is assigned by the operating
            system and uniquely identifies the parent process of the current Python process.

        Notes
        -----
        The returned PPID is determined by the operating system and may vary depending on how
        the Python process was started. If the parent process has terminated, the PPID may refer
        to the init process or another system-defined process.
        """
        pass

    def getExecutable(self) -> str:
        """
        Retrieve the absolute path to the Python interpreter executable.

        This method returns the full filesystem path to the Python interpreter
        that is currently executing the script. This can be useful for debugging,
        spawning subprocesses, or determining the runtime environment.

        Returns
        -------
        str
            The absolute path to the Python executable as a string.
        """
        pass

    def getPlatform(self) -> str:
        """
        Retrieve the name of the current operating system platform.

        This method determines the name of the operating system on which the Python
        interpreter is currently running. It uses the standard library's `platform`
        module to obtain a human-readable string representing the platform, such as
        'Windows', 'Linux', or 'Darwin' (for macOS).

        Returns
        -------
        str
            A string representing the name of the operating system platform. Typical
            return values include 'Windows', 'Linux', or 'Darwin'.

        Notes
        -----
        The returned value is determined by the underlying system and may vary
        depending on the environment in which the code is executed.
        """
        pass