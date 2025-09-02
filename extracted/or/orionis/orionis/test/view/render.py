import json
import os
import sys
from pathlib import Path
from orionis.test.contracts.render import ITestingResultRender
from orionis.test.records.logs import TestLogs

class TestingResultRender(ITestingResultRender):

    def __init__(
        self,
        result,
        storage_path: str,
        persist: bool = False
    ) -> None:
        """
        Initializes the TestingResultRender instance.

        Parameters
        ----------
        result : Any
            The test result data to be rendered in the report.
        storage_path : str
            Directory path where the HTML report will be saved. The directory is created if it does not exist.
        persist : bool, optional
            If True, enables persistent storage for test reports (default is False).

        Returns
        -------
        None
        """
        self.__filename = 'orionis-test-results.html'
        self.__result = result
        self.__persist = persist
        self.__storage_path = storage_path

        # Ensure storage_path is a Path object and create the directory if it doesn't exist
        storage_dir = Path(storage_path)
        storage_dir.mkdir(parents=True, exist_ok=True)

        # Set the absolute path for the report file
        self.__report_path = (storage_dir / self.__filename).resolve()

    def render(
        self
    ) -> str:
        """
        Renders the test results into an HTML report file.

        If persistence is enabled, retrieves the last 10 reports from the database and includes them in the report.
        Otherwise, only the current in-memory test result is used. The method reads a template file, replaces
        placeholders with the test results and persistence mode, writes the rendered content to a report file,
        and attempts to open the report in the default web browser on supported platforms.

        Returns
        -------
        str
            The absolute path to the generated HTML report file.
        """
        # Determine the source of test results based on persistence mode
        if self.__persist:

            # If persistence is enabled, fetch the last 10 reports from SQLite
            logs = TestLogs(self.__storage_path)
            reports = logs.get(last=10)

            # Parse each report's JSON data into a list
            results_list = [json.loads(report[1]) for report in reports]

        else:

            # If not persistent, use only the current in-memory result
            results_list = [self.__result]

        # Set placeholder values for the template
        persistence_mode = 'Database' if self.__persist else 'Memory'
        test_results_json = json.dumps(
            results_list,
            ensure_ascii=False,
            indent=None
        )

        # Locate the HTML template file
        template_path = Path(__file__).parent / 'report.stub'

        # Read the template content
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template_content = template_file.read()

        # Replace placeholders with actual values
        rendered_content = template_content.replace('{{orionis-testing-result}}', test_results_json)\
                                           .replace('{{orionis-testing-persistent}}', persistence_mode)

        # Write the rendered HTML report to the specified path
        with open(self.__report_path, 'w', encoding='utf-8') as report_file:
            report_file.write(rendered_content)

        # Open the generated report in the default web browser if running on Windows or macOS.
        try:

            # Check the operating system and open the report in a web browser if applicable
            if ((os.name == 'nt') or (os.name == 'posix' and sys.platform == 'darwin')):
                import webbrowser
                webbrowser.open(self.__report_path.as_uri())

        finally:

            # Return the absolute path to the generated report
            return str(self.__report_path)