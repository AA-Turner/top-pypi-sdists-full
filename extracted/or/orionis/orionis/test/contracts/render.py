from abc import ABC, abstractmethod

class ITestingResultRender(ABC):

    @abstractmethod
    def render(
        self
    ) -> str:
        """
        Otherwise, uses the current test result stored in memory. The method replaces placeholders in a
        template file with the test results and the persistence mode, then writes the rendered content
        to a report file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The full path to the generated report file.

        Notes
        -----
        - If persistence is enabled, the last 10 reports are fetched from the SQLite database.
        - If persistence is not enabled, only the current test result in memory is used.
        - The method reads a template file, replaces placeholders with the test results and persistence mode,
          and writes the final content to the report file.
        """
        pass