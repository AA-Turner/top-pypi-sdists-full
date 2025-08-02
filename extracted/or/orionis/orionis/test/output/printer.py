import re
from datetime import datetime
from typing import Any, Dict
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from orionis.services.introspection.instances.reflection import ReflectionInstance
from orionis.test.contracts.printer import ITestPrinter
from orionis.test.entities.result import TestResult
from orionis.test.enums import TestStatus

class TestPrinter(ITestPrinter):

    def __init__(
        self,
        print_result: bool = True,
        title: str = "🧪 Orionis Framework - Component Test Suite",
        width: int = 75
    ) -> None:
        """
        Initialize a TestPrinter instance for formatted test output.

        This constructor sets up the Rich Console for rendering output, configures
        the panel title and width for display, and defines keywords used to detect
        debugging calls in test code.

        Parameters
        ----------
        print_result : bool, optional
            Whether to print test results to the console (default is True).
        title : str, optional
            The title to display in the output panel (default is "🧪 Orionis Framework - Component Test Suite").
        width : int, optional
            The width of the output panel as a percentage of the console width (default is 75).

        Returns
        -------
        None
            This method does not return a value. It initializes instance attributes for output formatting.

        Notes
        -----
        - Initializes the following attributes:
          - __rich_console: Rich Console instance for formatted terminal output.
          - __panel_title: Title string for the output panel.
          - __panel_width: Width of the output panel, calculated as a percentage of the console width.
          - __debbug_keywords: List of keywords for identifying debug calls in test code.
          - __print_result: Flag indicating whether to print results.
        """
        # Create a Rich Console instance for output rendering
        self.__rich_console = Console()

        # Set the panel title for display
        self.__panel_title: str = title

        # Calculate the panel width as a percentage of the console width
        self.__panel_width: int = int(self.__rich_console.width * (width / 100))

        # Define keywords to detect debugging or dump calls in test code
        self.__debbug_keywords: list = ['self.dd', 'self.dump']

        # Store the flag indicating whether to print results
        self.__print_result: bool = print_result

    def print(
        self,
        value: Any
    ) -> None:
        """
        Print a value to the console using the Rich library's console.

        This method provides a unified way to output various types of values to the console,
        leveraging Rich's formatting capabilities. It handles strings, objects, and lists,
        ensuring each is displayed appropriately.

        Parameters
        ----------
        value : Any
            The value to be printed. Can be a string, object, or list.

        Returns
        -------
        None
            This method does not return any value. It outputs the provided value(s) to the console.

        Notes
        -----
        - If the value is a string, it is printed directly.
        - If the value is a list, each item in the list is printed on a new line.
        - For any other object, its string representation is printed.
        """

        # If not printing results, return early
        if self.__print_result is False:
            return

        # If the value is a string, print it directly
        if isinstance(value, str):
            self.__rich_console.print(value)

        # If the value is a list, print each item on a new line
        elif isinstance(value, list):
            for item in value:
                self.__rich_console.print(item)

        # For any other object, print its string representation
        else:
            self.__rich_console.print(str(value))

    def startMessage(
        self,
        *,
        length_tests: int,
        execution_mode: str,
        max_workers: int
    ):
        """
        Display a formatted start message for the test execution session.

        This method prints a styled panel to the console at the beginning of a test run,
        providing key information about the test session such as the total number of tests,
        the execution mode (parallel or sequential), and the start time. The output is
        rendered using the Rich library for enhanced readability.

        Parameters
        ----------
        length_tests : int
            The total number of tests to be executed in the session.
        execution_mode : str
            The mode of execution for the tests. Accepts "parallel" or "sequential".
        max_workers : int
            The number of worker threads or processes to use if running in parallel mode.

        Returns
        -------
        None
            This method does not return any value. It only prints formatted output to the console.

        Notes
        -----
        - The message is only printed if the `print_result` flag is set to True.
        - The panel includes the total number of tests, execution mode, and the current timestamp.
        """

        # If not printing results, return early
        if self.__print_result is False:
            return

        # Determine the execution mode text for display
        mode_text = f"[stat]Parallel with {max_workers} workers[/stat]" if execution_mode == "parallel" else "Sequential"

        # Prepare the lines of information to display in the panel
        textlines = [
            f"[bold]Total Tests:[/bold] [dim]{length_tests}[/dim]",
            f"[bold]Mode:[/bold] [dim]{mode_text}[/dim]",
            f"[bold]Started at:[/bold] [dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
        ]

        # Add a blank line before the panel
        self.__rich_console.line(1)

        # Print the panel with the formatted text lines
        self.__rich_console.print(
            Panel(
                str('\n').join(textlines),
                border_style="blue",
                title=self.__panel_title,
                title_align="center",
                width=self.__panel_width,
                padding=(0, 1)
            )
        )

        # Add a blank line after the panel
        self.__rich_console.line(1)

    def finishMessage(
        self,
        *,
        summary: Dict[str, Any]
    ) -> None:
        """
        Display a final summary message for the test suite execution in a styled panel.

        This method prints a completion message at the end of the test run, summarizing the overall
        status and total execution time. The message includes a status icon (✅ for success, ❌ for failure)
        based on whether any tests failed or errored. The output is formatted using the Rich library
        for enhanced readability.

        Parameters
        ----------
        summary : dict
            Dictionary containing the test suite summary. Must include the following keys:
                - 'failed': int, number of failed tests
                - 'errors': int, number of errored tests
                - 'total_time': float, total duration of the test suite execution in seconds

        Returns
        -------
        None
            This method does not return any value. It outputs a formatted completion message to the console.

        Notes
        -----
        - If `self.__print_result` is False, the method returns without displaying anything.
        - The status icon reflects the presence of failures or errors in the test suite.
        - The message is displayed within a styled Rich panel for clarity.
        """

        # If not printing results, return early
        if self.__print_result is False:
            return

        # Determine status icon based on failures and errors
        status_icon = "✅" if (summary['failed'] + summary['errors']) == 0 else "❌"

        # Prepare the completion message with total execution time
        msg = f"Test suite completed in {summary['total_time']:.2f} seconds"

        # Print the message inside a styled Rich panel
        self.__rich_console.print(
            Panel(
                msg,
                border_style="blue",
                title=f"{status_icon} Test Suite Finished",
                title_align='left',
                width=self.__panel_width,
                padding=(0, 1)
            )
        )

        # Add a blank line after the panel for spacing
        self.__rich_console.line(1)

    def executePanel(
        self,
        *,
        flatten_test_suite: list,
        callable: callable
    ):
        """
        Execute a test suite panel with optional live console output and debugging detection.

        This method manages the display of a running message panel using the Rich library,
        adapting its behavior based on whether debugging or dump calls are detected in the test suite
        and whether result printing is enabled. If debugging or dump calls are present in the test code,
        a static panel is shown before executing the test suite. Otherwise, a live panel is displayed
        during execution for a more dynamic user experience.

        Parameters
        ----------
        flatten_test_suite : list
            The flattened list of test case instances or test suite items to be executed.
        callable : callable
            The function or method to execute the test suite.

        Returns
        -------
        Any
            Returns the result produced by the provided callable after execution, which typically
            contains the outcome of the test suite run (such as a summary or result object).

        Notes
        -----
        - If debugging or dump calls are detected in the test code, a static panel is displayed.
        - If no debugging or dump calls are found and result printing is enabled, a live panel is shown.
        - If result printing is disabled, the test suite is executed without any panel display.
        """

        # Determine if the test suite contains active debugging or dump calls
        use_debugger = self.__withDebugger(
            flatten_test_suite=flatten_test_suite
        )

        # Only display output if printing results is enabled
        if self.__print_result:

            # Prepare a minimal running message as a single line, using the configured panel width
            running_panel = Panel(
                "[yellow]⏳ Running...[/yellow]",
                border_style="yellow",
                width=self.__panel_width,
                padding=(0, 1)
            )

            # If no debugger/dump calls, use a live panel for dynamic updates
            if not use_debugger:

                # Execute the test suite and return its result
                with Live(running_panel, console=self.__rich_console, refresh_per_second=4, transient=True):
                    return callable()

            else:

                # If debugger/dump calls are present, print a static panel before running
                self.__rich_console.print(running_panel)
                return callable()

        else:

            # If result printing is disabled, execute the test suite without any panel
            return callable()

    def linkWebReport(
        self,
        path: str
    ):
        """
        Display a styled message inviting the user to view the test results report.

        This method prints an elegant invitation to the console, indicating that the test results
        have been saved and providing a clickable or visually distinct path to the report. The output
        uses Rich's Text styling to highlight the message and underline the report path for emphasis.

        Parameters
        ----------
        path : str
            The file system path or URL to the test results report.

        Returns
        -------
        None
            This method does not return any value. It outputs a formatted message to the console.

        Notes
        -----
        - The invitation message is styled with green text for success and an underlined blue path for visibility.
        - Intended to be called after test execution to direct users to the generated report.
        """

        # If not printing results, do not display the link
        if self.__print_result is False:
            return

        # Create the base invitation text with a green style
        invite_text = Text("Test results saved. ", style="green")

        # Append a bold green prompt to view the report
        invite_text.append("View report: ", style="bold green")

        # Append the report path, styled as underlined blue for emphasis
        invite_text.append(str(path), style="underline blue")

        # Print the composed invitation message to the console
        self.__rich_console.print(invite_text)

    def summaryTable(
        self,
        summary: Dict[str, Any]
    ) -> None:
        """
        Display a summary table of test results using the Rich library.

        This method prints a formatted table summarizing the results of a test suite execution.
        The table includes the total number of tests, counts of passed, failed, errored, and skipped tests,
        the total execution duration, and the overall success rate. The output is styled for readability
        and is only displayed if result printing is enabled.

        Parameters
        ----------
        summary : dict
            Dictionary containing the test summary data. Must include the following keys:
                - total_tests (int): Total number of tests executed.
                - passed (int): Number of tests that passed.
                - failed (int): Number of tests that failed.
                - errors (int): Number of tests that had errors.
                - skipped (int): Number of tests that were skipped.
                - total_time (float): Total duration of the test execution in seconds.
                - success_rate (float): Percentage of tests that passed.

        Returns
        -------
        None
            This method does not return any value. It outputs a formatted summary table to the console
            if result printing is enabled.

        Notes
        -----
        - The table is only displayed if the `print_result` flag is set to True.
        - The table uses Rich's styling features for enhanced readability.
        """

        # If result printing is disabled, do not display the summary table
        if self.__print_result is False:
            return

        # Create a Rich Table with headers and styling
        table = Table(
            show_header=True,
            header_style="bold white",
            width=self.__panel_width,
            border_style="blue"
        )
        # Add columns for each summary metric
        table.add_column("Total", justify="center")
        table.add_column("Passed", justify="center")
        table.add_column("Failed", justify="center")
        table.add_column("Errors", justify="center")
        table.add_column("Skipped", justify="center")
        table.add_column("Duration", justify="center")
        table.add_column("Success Rate", justify="center")

        # Add a row with the summary values, formatting duration and success rate
        table.add_row(
            str(summary["total_tests"]),
            str(summary["passed"]),
            str(summary["failed"]),
            str(summary["errors"]),
            str(summary["skipped"]),
            f"{summary['total_time']:.2f}s",
            f"{summary['success_rate']:.2f}%"
        )

        # Print the summary table to the console
        self.__rich_console.print(table)

        # Add a blank line after the table for spacing
        self.__rich_console.line(1)

    def displayResults(
        self,
        *,
        summary: Dict[str, Any]
    ) -> None:
        """
        Display a detailed summary of test execution results, including a summary table and
        grouped panels for failed or errored tests.

        This method prints a summary table of the test results and, if there are any failed or
        errored tests, displays them grouped by their test class. For each failed or errored test,
        a syntax-highlighted traceback panel is shown, along with metadata such as the test method
        name and execution time. Different icons and border colors are used to distinguish between
        failed and errored tests.

        Parameters
        ----------
        summary : dict
            Dictionary containing the overall summary and details of the test execution. It must
            include keys such as 'test_details' (list of test result dicts), 'total_tests',
            'passed', 'failed', 'errors', 'skipped', 'total_time', and 'success_rate'.

        Returns
        -------
        None
            This method does not return any value. It outputs the formatted summary table and
            detailed panels for failed or errored tests to the console.

        Notes
        -----
        - The summary table provides an overview of the test results.
        - Failed and errored tests are grouped and displayed by their test class.
        - Each failed or errored test is shown in a panel with a syntax-highlighted traceback,
          test method name, and execution time.
        - Icons and border colors visually distinguish between failed (❌, yellow) and errored
          (💥, red) tests.
        - No output is produced if result printing is disabled.
        """

        # If result printing is disabled, do not display results
        if not self.__print_result:
            return

        # Print one blank line before the summary
        self.__rich_console.line(1)

        # Print the summary table of test results
        self.summaryTable(summary)

        # Group failed and errored tests by their test class
        failures_by_class = {}
        for test in summary["test_details"]:
            if test["status"] in (TestStatus.FAILED.name, TestStatus.ERRORED.name):
                class_name = test["class"]
                if class_name not in failures_by_class:
                    failures_by_class[class_name] = []
                failures_by_class[class_name].append(test)

        # Display grouped failures and errors for each test class
        for class_name, tests in failures_by_class.items():

            # Print a panel with the class name as the header
            class_panel = Panel.fit(
                f"[bold]{class_name}[/bold]",
                border_style="red",
                padding=(0, 2)
            )
            self.__rich_console.print(class_panel)

            for test in tests:
                # Sanitize the traceback to show only relevant parts
                traceback_str = self.__sanitizeTraceback(test['file_path'], test['traceback'])

                # Create a syntax-highlighted panel for the traceback
                syntax = Syntax(
                    traceback_str,
                    lexer="python",
                    line_numbers=False,
                    background_color="default",
                    word_wrap=True,
                    theme="monokai"
                )

                # Choose icon and border color based on test status
                icon = "❌" if test["status"] == TestStatus.FAILED.name else "💥"
                border_color = "yellow" if test["status"] == TestStatus.FAILED.name else "red"

                # Ensure execution time is never zero for display purposes
                if not test['execution_time'] or test['execution_time'] == 0:
                    test['execution_time'] = 0.001

                # Print the panel with traceback and test metadata
                panel = Panel(
                    syntax,
                    title=f"{icon} {test['method']}",
                    subtitle=f"Duration: {test['execution_time']:.3f}s",
                    border_style=border_color,
                    title_align="left",
                    padding=(1, 1),
                    subtitle_align="right",
                    width=self.__panel_width
                )
                self.__rich_console.print(panel)
                self.__rich_console.line(1)

    def unittestResult(
        self,
        test_result: TestResult
    ) -> None:
        """
        Display the result of a single unit test in a formatted manner using the Rich library.

        This method prints the outcome of an individual unit test to the console, showing a status icon
        (✅ for passed, ❌ for failed) along with the test name. If the test failed, the first line of the
        error message is also displayed for quick reference. The output is styled for clarity and does not
        use syntax highlighting.

        Parameters
        ----------
        test_result : Any
            An object representing the result of a unit test. It must have the following attributes:
                - status: An enum or object with a 'name' attribute indicating the test status (e.g., "PASSED", "FAILED").
                - name: The name of the test.
                - error_message: The error message string (present if the test failed).

        Returns
        -------
        None
            This method does not return any value. It outputs the formatted test result to the console.

        Notes
        -----
        - If the test passed, only the status and test name are displayed.
        - If the test failed, the status, test name, and the first line of the error message are shown.
        - Output is printed using the Rich console without syntax highlighting.
        """

        # If result printing is disabled, do not display results
        if not self.__print_result:
            return

        # Determine the status icon and label based on the test result
        if test_result.status.name == "PASSED":
            status = "✅ PASSED"
        elif test_result.status.name == "FAILED":
            status = "❌ FAILED"
        elif test_result.status.name == "SKIPPED":
            status = "⏩ SKIPPED"
        elif test_result.status.name == "ERRORED":
            status = "💥 ERRORED"
        else:
            status = f"🔸 {test_result.status.name}"

        msg = f"[{status}] {test_result.name}"

        if test_result.status.name == "FAILED":
            msg += f" | Error: {test_result.error_message.splitlines()[0].strip()}"

        max_width = self.__rich_console.width - 2
        display_msg = msg if len(msg) <= max_width else msg[:max_width - 3] + "..."
        self.__rich_console.print(display_msg, highlight=False)

    def __withDebugger(
        self,
        flatten_test_suite: list
    ) -> bool:
        """
        Determine if any test case in the provided flattened test suite contains active debugging or dumping calls.

        This method inspects the source code of each test case instance in the given list to check for the presence
        of specific debugging or dumping method calls (such as 'self.dd' or 'self.dump'). Only lines that are not
        commented out are considered. If any such call is found in the source code, the method immediately returns True,
        indicating that a debugger or dump method is actively used in the test suite.

        Parameters
        ----------
        flatten_test_suite : list
            A list of test case instances whose source code will be inspected for debugging or dumping calls.

        Returns
        -------
        bool
            Returns True if any test case contains an active (non-commented) call to a debugging or dumping method
            (e.g., 'self.dd' or 'self.dump'). Returns False if no such calls are found or if an exception occurs
            during inspection.

        Notes
        -----
        - Lines that are commented out (i.e., start with '#') are ignored during inspection.
        - If an exception occurs while retrieving or processing the source code, the method returns False.
        """

        try:

            # Iterate through each test case in the flattened test suite
            for test_case in flatten_test_suite:

                # Retrieve the source code of the test case using reflection
                source = ReflectionInstance(test_case).getSourceCode()

                # Check each line of the source code
                for line in source.splitlines():

                    # Strip leading and trailing whitespace from the line
                    stripped = line.strip()

                    # Skip lines that are commented out
                    if stripped.startswith('#') or re.match(r'^\s*#', line):
                        continue

                    # If any debug keyword is present in the line, return True
                    if any(keyword in line for keyword in self.__debbug_keywords):
                        return True

            # No debug or dump calls found in any test case
            return False

        except Exception:

            # If any error occurs during inspection, return False
            return False

    def __sanitizeTraceback(
        self,
        test_path: str,
        traceback_test: str
    ) -> str:
        """
        Extract and return the most relevant portion of a traceback string that pertains to a specific test file.

        This method processes a full Python traceback and attempts to isolate the lines that are directly related
        to the provided test file. It does so by searching for the test file's name within the traceback and collecting
        all subsequent lines that are relevant, such as those containing 'File' or non-empty lines. If the test file's
        name cannot be determined or no relevant lines are found, the original traceback is returned. If the traceback
        is empty, a default message is returned.

        Parameters
        ----------
        test_path : str
            The file path of the test file whose related traceback lines should be extracted.
        traceback_test : str
            The complete traceback string to be sanitized.

        Returns
        -------
        str
            Returns a string containing only the relevant traceback lines associated with the test file.
            If no relevant lines are found or the file name cannot be determined, the full traceback is returned.
            If the traceback is empty, returns "No traceback available for this test."
        """

        # Return a default message if the traceback is empty
        if not traceback_test:
            return "No traceback available for this test."

        # Attempt to extract the test file's name (without extension) from the provided path
        file_match = re.search(r'([^/\\]+)\.py', test_path)
        file_name = file_match.group(1) if file_match else None

        # If the file name cannot be determined, return the full traceback
        if not file_name:
            return traceback_test

        # Split the traceback into individual lines for processing
        lines = traceback_test.splitlines()
        relevant_lines = []

        # Determine if the test file is present in the traceback
        # If not found, set found_test_file to True to include all lines
        found_test_file = False if file_name in traceback_test else True

        # Iterate through each line of the traceback
        for line in lines:

            # Mark when the test file is first encountered in the traceback
            if file_name in line and not found_test_file:
                found_test_file = True

            # Once the test file is found, collect relevant lines
            if found_test_file:
                if 'File' in line:
                    relevant_lines.append(line.strip())
                elif line.strip() != '':
                    relevant_lines.append(line)

        # If no relevant lines were found, return the full traceback
        if not relevant_lines:
            return traceback_test

        # Join and return only the relevant lines as a single string
        return str('\n').join(relevant_lines)
