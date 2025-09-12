import re
from datetime import datetime
import unittest
from typing import Any, Dict, List
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from orionis.foundation.config.testing.enums.verbosity import VerbosityMode
from orionis.test.contracts.printer import ITestPrinter
from orionis.test.entities.result import TestResult
from orionis.test.enums import TestStatus

class TestPrinter(ITestPrinter):

    def __init__(
        self,
        verbosity: VerbosityMode | int = VerbosityMode.DETAILED,
        title: str = "🧪 Orionis Framework - Component Test Suite",
        width: int = 75
    ) -> None:
        """
        Initializes a TestPrinter instance for formatted test output using the Rich library.

        Parameters
        ----------
        print_result : bool, optional
            If True, enables printing of test results to the console. If False, suppresses all output.
        verbosity : VerbosityMode or int, optional
            Specifies the verbosity level for output. Accepts either a VerbosityMode enum or an integer value.
            Default is VerbosityMode.DETAILED.
        title : str, optional
            The title displayed in the output panel. Default is "🧪 Orionis Framework - Component Test Suite".
        width : int, optional
            The width of the output panel as a percentage of the console width. Must be between 10 and 100.
            Default is 75.

        Returns
        -------
        None
            This constructor does not return any value. It initializes the TestPrinter instance.

        Raises
        ------
        ValueError
            If any of the input parameters are of invalid type or out of allowed range.

        Notes
        -----
        - The Rich Console instance is created for rendering output.
        - The verbosity level, panel width, panel title, and print_result flag are validated and set.
        """
        # Create a Rich Console instance for output rendering
        self.__rich_console = Console()

        # Validate and set verbosity level
        if not isinstance(verbosity, (int, VerbosityMode)):
            raise ValueError("The 'verbosity' parameter must be an integer or VerbosityMode enum.")
        self.__verbosity: int = verbosity if isinstance(verbosity, int) else verbosity.value

        # Validate and set panel width (must be between 10% and 100% of console width)
        if not isinstance(width, int) or not (10 <= width <= 100):
            raise ValueError("The 'width' parameter must be an integer between 10 and 100.")
        self.__panel_width: int = int(self.__rich_console.width * (width / 100))

        # Validate and set panel title
        if not isinstance(title, str):
            raise ValueError("The 'title' parameter must be a string.")
        self.__panel_title: str = title

    def print(
        self,
        value: Any
    ) -> None:
        """
        Print a value to the console using the Rich library, supporting strings, lists, and other objects.

        Parameters
        ----------
        value : Any
            The value to be printed. Can be a string, a list of items, or any other object.

        Returns
        -------
        None
            This method does not return any value. Output is sent directly to the console.

        Notes
        -----
        - If result printing is disabled (`self.__print_result` is False), no output will be produced.
        - Strings are printed as-is.
        - Lists are iterated and each item is printed on a separate line.
        - Other objects are converted to string before printing.
        """

        # If printing results is disabled, do not output anything
        if self.__verbosity == VerbosityMode.SILENT.value:
            return

        # Print string values directly
        if isinstance(value, str):
            self.__rich_console.print(value)

        # Print each item of a list on a new line
        elif isinstance(value, list):
            for item in value:
                self.__rich_console.print(item)

        # For other object types, print their string representation
        else:
            self.__rich_console.print(str(value))

    def line(
        self,
        count: int = 1
    ) -> None:
        """
        Print a specified number of blank lines to the console for spacing.

        Parameters
        ----------
        count : int, optional
            The number of blank lines to print (default is 1).
        Returns
        -------
        None
            This method does not return any value. Blank lines are printed directly to the console.
        Notes
        -----
        - If result printing is disabled (`self.__print_result` is False), no output will be produced.
        - The method uses the Rich console's built-in line printing functionality.
        """

        # If printing results is disabled, do not output anything
        if self.__verbosity == VerbosityMode.SILENT.value:
            return

        # Print the specified number of blank lines
        self.__rich_console.line(count)

    def zeroTestsMessage(self) -> None:
        """
        Display a styled message indicating that no tests were found to execute.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. The message is printed directly to the console.

        Notes
        -----
        - If result printing is disabled (`self.__print_result` is False), no output will be produced.
        - The message is displayed in a Rich panel with a yellow border and centered title.
        """
        # If printing results is disabled, do not output anything
        if self.__verbosity == VerbosityMode.SILENT.value:
            return

        # Print a styled panel to indicate that no tests were found
        self.__rich_console.print(
            Panel(
                "No tests found to execute.",
                border_style="yellow",              # Use yellow to indicate a warning or neutral state
                title="No Tests",                   # Panel title
                title_align="center",               # Center the title
                width=self.__panel_width,           # Set panel width based on console configuration
                padding=(0, 1)                      # Add horizontal padding for better appearance
            )
        )

        # Add a blank line after the panel for visual spacing
        self.__rich_console.line(1)

    def startMessage(
        self,
        *,
        length_tests: int,
        execution_mode: str,
        max_workers: int
    ):
        """
        Display a formatted start message for the beginning of a test execution session.

        Parameters
        ----------
        length_tests : int
            Total number of tests scheduled for execution in the session.
        execution_mode : str
            The mode of test execution. Should be either "parallel" or "sequential".
        max_workers : int
            Number of worker threads or processes to use if running in parallel mode.

        Returns
        -------
        None
            This method does not return any value. It prints a styled panel to the console with session details.

        Notes
        -----
        - If result printing is disabled (`self.__print_result` is False), no output will be produced.
        - The panel displays the total number of tests, execution mode, and the timestamp when the session started.
        - The execution mode text will indicate parallel execution with the number of workers if applicable.
        """

        # If printing results is disabled, do not output anything
        if self.__verbosity == VerbosityMode.SILENT.value:
            return

        # Format the execution mode text for display
        mode_text = f"[stat]Parallel with {max_workers} workers[/stat]" if execution_mode == "parallel" else "Sequential"

        # Prepare the lines of information to display in the panel
        textlines = [
            f"[bold]Total Tests:[/bold] [dim]{length_tests}[/dim]",                                 # Show total number of tests
            f"[bold]Mode:[/bold] [dim]{mode_text}[/dim]",                                           # Show execution mode
            f"[bold]Started at:[/bold] [dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"   # Show start timestamp
        ]

        # Print the panel with the formatted text lines
        self.__rich_console.print(
            Panel(
                str('\n').join(textlines),           # Join all lines for panel content
                border_style="blue",                 # Use blue border for the panel
                title=self.__panel_title,            # Set the panel title
                title_align="center",                # Center the panel title
                width=self.__panel_width,            # Set panel width based on console configuration
                padding=(0, 1)                       # Add horizontal padding for better appearance
            )
        )

        # Add a blank line after the panel for spacing
        self.__rich_console.line(1)

    def progressBar(
        self
    ) -> Progress:
        """
        Create and return a Rich Progress bar instance for tracking task progress in the console.

        Parameters
        ----------
        self : TestPrinter
            The instance of the TestPrinter class.

        Returns
        -------
        Progress
            A Rich Progress object configured with:
                - A cyan-colored task description column.
                - A visual progress bar.
                - A percentage completion indicator.
                - Output directed to the configured Rich console.
                - Transient display (disappears after completion).
                - Disabled if result printing is turned off.

        Notes
        -----
        - If printing is disabled (`self.__print_result` is False), the progress bar will not be shown.
        - The progress bar is suitable for tracking the progress of tasks such as test execution.
        """

        # Flag to disable the progress bar if printing is off or verbosity is silent/minimal
        disable = self.__verbosity <= VerbosityMode.MINIMAL.value

        # Create and return a Rich Progress bar instance with custom columns and settings
        return Progress(
            TextColumn("[cyan]{task.description}"),         # Task description in cyan
            BarColumn(bar_width=self.__panel_width - 30),   # Set custom bar width (adjust -30 as needed)
            TaskProgressColumn(),                           # Percentage completion indicator
            console=self.__rich_console,                    # Output to the configured Rich console
            transient=True,                                 # Remove the bar after completion
            disable=disable                                 # Disable if printing is off
        )

    def finishMessage(
        self,
        *,
        summary: Dict[str, Any]
    ) -> None:
        """
        Display a final summary message for the test suite execution in a styled panel.

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
        """
        # If not printing results, return early
        if self.__verbosity == VerbosityMode.SILENT.value:
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
        func: callable,
        live_console: bool = True
    ) -> unittest.TestResult:
        """
        Executes a callable within a styled Rich panel, optionally using a live console for dynamic updates.

        Parameters
        ----------
        func : callable
            The function or method to execute. It should take no arguments and return a result.
        live_console : bool, optional
            If True, displays a live updating panel during execution (default is True).
            If False, displays a static panel before execution.

        Returns
        -------
        unittest.TestResult
            The result returned by the executed callable, typically a `unittest.TestResult` object.

        Notes
        -----
        - If result printing is disabled, the callable is executed without any panel or output.
        - If `live_console` is True, a transient live panel is shown while the callable executes.
        - If `live_console` is False, a static panel is printed before execution.
        - The method always returns the result of the provided callable, regardless of output mode.
        """

        # Ensure the provided func is actually callable
        if not callable(func):
            raise ValueError("The 'func' parameter must be a callable (function or method).")

        # Only display output if printing results is enabled
        if self.__verbosity != VerbosityMode.SILENT.value:

            # If live_console is True, use a live panel for dynamic updates
            if live_console:

                # Prepare a minimal running message as a single line, using the configured panel width
                running_panel = Panel(
                    "[yellow]⏳ Running...[/yellow]",
                    border_style="yellow",
                    width=self.__panel_width,
                    padding=(0, 1)
                )

                # Execute the callable within a live Rich panel context
                with Live(running_panel, console=self.__rich_console, refresh_per_second=4, transient=True):
                    return func()
            else:

                # Prepare a panel with a message indicating that test results will follow
                running_panel = Panel(
                    "[yellow]🧪 Running tests...[/yellow]",
                    border_style="green",
                    width=self.__panel_width,
                    padding=(0, 1)
                )

                # If live_console is False, print a static panel before running
                self.__rich_console.print(running_panel)
                return func()

        else:

            # If result printing is disabled, execute the callable without any panel
            return func()

    def linkWebReport(
        self,
        path: str
    ):
        """
        Display a styled message inviting the user to view the test results report.

        Parameters
        ----------
        path : str
            The file system path or URL to the test results report.

        Returns
        -------
        None
        """
        # If not printing results, do not display the link
        if self.__verbosity == VerbosityMode.SILENT.value:
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
        """
        # If result printing is disabled, do not display the summary table
        if self.__verbosity == VerbosityMode.SILENT.value:
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

        Parameters
        ----------
        summary : dict
            Dictionary containing the overall summary and details of the test execution. It must
            include keys such as 'test_details' (list of test result dicts), 'total_tests',
            'passed', 'failed', 'errors', 'skipped', 'total_time', and 'success_rate'.

        Returns
        -------
        None
        """
        # If result printing is disabled, do not display results
        if self.__verbosity == VerbosityMode.SILENT.value:
            return

        # Print one blank line before the summary
        self.__rich_console.line(1)

        # Print the summary table of test results
        self.summaryTable(summary)

        # Get the list of individual test results
        test_details: List[Dict] = summary.get("test_details", [])

        # Iterate through each test result to display failures and errors
        for test in test_details:

            # If there are no failures or errors, skip to the next test
            if test["status"] in (TestStatus.FAILED.name, TestStatus.ERRORED.name):

                # Determine the status icon based on the test status
                status_icon = "❌ FAILED:" if test["status"] == TestStatus.FAILED.name else "💥 ERRORED:"

                # Print separator line before each test result with class name and method name
                self.__rich_console.rule(title=f'🧪 {test["class"]}.{test["method"]}()', align="left")

                # Add clickable file:line info if available
                last_trace_frame = test.get('traceback_frames')
                if last_trace_frame and last_trace_frame is not None:

                    # Get the last frame details
                    last_trace_frame: dict = last_trace_frame[-1]
                    _file = last_trace_frame.get('file')
                    _line = last_trace_frame.get('line')
                    _code = last_trace_frame.get('code')

                    # Print the file and line number if available
                    text = Text("📂 ")
                    text.append(f'{_file}:{_line}', style="underline blue")
                    self.__rich_console.print(text)

                    # Print the error message with better formatting
                    text = Text(f"{status_icon} ", style="red")
                    error_msg = test["error_message"] if test["error_message"] else "Unknown error"
                    text.append(error_msg, style="yellow")
                    self.__rich_console.print(text)

                    # If verbosity is detailed, include file path, line number, error message, and traceback
                    if self.__verbosity == VerbosityMode.DETAILED.value:

                        try:

                            # Open the file and read its lines
                            if isinstance(_file, str) and _file:
                                with open(_file, 'r', encoding='utf-8') as f:
                                    file_lines = f.readlines()
                            else:
                                raise ValueError(f"Invalid file path: {_file}")

                            # Convert to 0-based index
                            error_line_num = int(_line) - 1
                            start_line = max(0, error_line_num - 1)
                            end_line = min(len(file_lines), error_line_num + 3)

                            # Create a code block with syntax highlighting
                            code_lines = []
                            for i in range(start_line, end_line):
                                line_num = i + 1
                                line_content = file_lines[i].rstrip()
                                if line_num == int(_line):
                                    # Highlight the error line
                                    code_lines.append(f"* {line_num:3d} | {line_content}")
                                else:
                                    code_lines.append(f"  {line_num:3d} | {line_content}")

                            code_block = '\n'.join(code_lines)
                            syntax = Syntax(code_block, "python", theme="monokai", line_numbers=False)
                            self.__rich_console.print(syntax)

                        except Exception:

                            # Fallback to original behavior if file cannot be read
                            text = Text(f"{_line} | {_code}", style="dim")
                            self.__rich_console.print(text)

                else:

                    # Print the file and line number if available
                    text = Text("📂 ")
                    text.append(f'{test["file_path"]}', style="underline blue")
                    self.__rich_console.print(text)

                    # Print the error message with better formatting
                    text = Text(f"{status_icon} ", style="bold red")
                    self.__rich_console.print(text)

                    # Print traceback if available
                    if test["traceback"]:
                        sanitized_traceback = self.__sanitizeTraceback(
                            test_path=test["file_path"],
                            traceback_test=test["traceback"]
                        )
                        syntax = Syntax(sanitized_traceback, "python", theme="monokai", line_numbers=False)
                        self.__rich_console.print(syntax)

                # Print a separator line after each test result
                if self.__verbosity == VerbosityMode.DETAILED.value:
                    self.__rich_console.rule()

                # Print one blank line after the results
                self.__rich_console.line(1)

    def unittestResult(
        self,
        test_result: TestResult
    ) -> None:
        """
        Display the result of a single unit test in a formatted manner using the Rich library.

        Parameters
        ----------
        test_result : TestResult
            An object representing the result of a unit test. It must have the following attributes:
                - status: An enum or object with a 'name' attribute indicating the test status (e.g., "PASSED", "FAILED").
                - name: The name of the test.
                - error_message: The error message string (present if the test failed).

        Returns
        -------
        None
        """
        # If result printing is disabled, do not display results
        if self.__verbosity < VerbosityMode.DETAILED.value:
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

    def __sanitizeTraceback(
        self,
        test_path: str,
        traceback_test: str
    ) -> str:
        """
        Extract and return the most relevant portion of a traceback string that pertains to a specific test file.

        Parameters
        ----------
        test_path : str
            The file path of the test file whose related traceback lines should be extracted.
        traceback_test : str
            The complete traceback string to be sanitized.

        Returns
        -------
        str
            String containing only the relevant traceback lines associated with the test file.
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
