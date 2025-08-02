from abc import ABC, abstractmethod

class IImports(ABC):

    @abstractmethod
    def collect(self):
        """
        Collects information about user-defined Python modules currently loaded in `sys.modules`.

        This method should scan the current Python runtime environment and gather details about
        all user-defined modules that have been imported and are present in `sys.modules`. The
        collected information may include module names, file paths, and other relevant metadata,
        depending on the implementation.

        Returns
        -------
        IImports
            Returns the current instance (`self`) with its internal imports information updated
            to reflect the latest state of loaded modules.

        Notes
        -----
        This method does not modify the actual modules loaded in memory; it only updates the
        internal collection maintained by the implementation. Subclasses should implement the
        logic for identifying and storing relevant module information.
        """

        # Subclasses should implement logic to scan sys.modules and update internal imports collection.
        pass

    @abstractmethod
    def display(self) -> None:
        """
        Displays a formatted table summarizing the collected import statements.

        This method should present the information about the currently collected Python module imports
        in a human-readable tabular format. The display may include details such as module names,
        file paths, and other relevant metadata, depending on the implementation.

        Returns
        -------
        None
            This method does not return any value. Its sole purpose is to output the collected import
            information for inspection or debugging.

        Notes
        -----
        The actual formatting and output destination (e.g., console, log, GUI) are determined by the
        implementing subclass.
        """

        # Subclasses should implement logic to format and output the collected imports.
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Removes all entries from the collected imports list, resetting the internal state.

        This method should be called when you want to discard all previously collected import
        information and start fresh. It does not affect the actual Python modules loaded in memory,
        only the internal collection maintained by the implementation.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Subclasses should implement logic to clear their internal imports collection.
        pass