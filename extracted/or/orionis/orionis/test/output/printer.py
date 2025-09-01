import re
from datetime import datetime
from typing import Any, Dict, List
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
        Print a value to the console using the Rich library.

        Parameters
        ----------
        value : Any
            The value to be printed. Can be a string, object, or list.

        Returns
        -------
        None
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

    def zeroTestsMessage(self) -> None:
        """
        Display a message indicating that no tests were found to execute.

        Returns
        -------
        None
        """
        # If not printing results, return early
        if self.__print_result is False:
            return

        # Print the message inside a styled Rich panel (not as an error)
        self.__rich_console.print(
            Panel(
                "No tests found to execute.",
                border_style="yellow",
                title="No Tests",
                title_align="center",
                width=self.__panel_width,
                padding=(0, 1)
            )
        )

        # Add a blank line after the panel for spacing
        self.__rich_console.line(1)

    def startMessage(
        self,
        *,
        length_tests: int,
        execution_mode: str,
        max_workers: int
    ):
        """
        Display a formatted start message for the test execution session.

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

        Parameters
        ----------
        flatten_test_suite : list
            The flattened list of test case instances or test suite items to be executed.
        callable : callable
            The function or method to execute the test suite.

        Returns
        -------
        Any
            Returns the result produced by the provided callable after execution.
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

        Parameters
        ----------
        path : str
            The file system path or URL to the test results report.

        Returns
        -------
        None
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
        if not self.__print_result:
            return

        # Print one blank line before the summary
        self.__rich_console.line(1)

        # Print the summary table of test results
        self.summaryTable(summary)

        # Print failed and errored tests
        test_details: List[Dict] = summary.get("test_details", [])
        for test in test_details:

            # If there are no failures or errors, skip to the next test
            if test["status"] in (TestStatus.FAILED.name, TestStatus.ERRORED.name):

                # Determine the status icon based on the test status
                if test["status"] == TestStatus.FAILED.name:
                    status_icon = "❌ FAILED: "
                else:
                    status_icon = "💥 ERRORED: "

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
                    _function = last_trace_frame.get('function')

                    # Print the file and line number if available
                    text = Text("📂 ")
                    text.append(f'{_file}:{_line}', style="underline blue")
                    self.__rich_console.print(text)

                    # Print the error message with better formatting
                    text = Text(status_icon, style="red")
                    error_msg = test["error_message"] if test["error_message"] else "Unknown error"
                    text.append(error_msg, style="yellow")
                    self.__rich_console.print(text)

                    # Print the code context (1 line before and 2 lines after the error)
                    try:

                        # Open the file and read its lines
                        with open(_file, 'r', encoding='utf-8') as f:
                            file_lines = f.readlines()

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

                    except (FileNotFoundError, ValueError, IndexError):

                        # Fallback to original behavior if file cannot be read
                        text = Text(f"{_line} | {_code}", style="dim")
                        self.__rich_console.print(text)

                else:

                    # Print the file and line number if available
                    text = Text("📂 ")
                    text.append(f'{test["file_path"]}', style="underline blue")
                    self.__rich_console.print(text)

                    # Print the error message with better formatting
                    text = Text(status_icon, style="bold red")
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

        Parameters
        ----------
        flatten_test_suite : list
            A list of test case instances whose source code will be inspected for debugging or dumping calls.

        Returns
        -------
        bool
            True if any test case contains an active (non-commented) call to a debugging or dumping method.
            False if no such calls are found or if an exception occurs during inspection.
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
