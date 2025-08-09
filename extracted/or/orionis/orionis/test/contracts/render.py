from abc import ABC, abstractmethod

class ITestingResultRender(ABC):

    @abstractmethod
    def render(
        self
    ) -> str:
        """
        Generates a report file by rendering test results into a template.

        Returns
        -------
        str
            The absolute path to the generated report file.

        Notes
        -----
        - If persistence is enabled, retrieves the last 10 reports from the SQLite database.
        - If persistence is disabled, uses only the current test result stored in memory.
        - Reads a template file, replaces placeholders with test results and persistence mode,
          and writes the rendered content to the report file.
        """
        pass
