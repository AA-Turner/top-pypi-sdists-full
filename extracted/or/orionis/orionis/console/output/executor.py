from datetime import datetime
from orionis.console.output.contracts.executor import IExecutor
from orionis.console.output.enums.styles import ANSIColors

class Executor(IExecutor):

    def __ansiOutput(self, program: str, state: str, state_color: str, time: str = ''):
        """
        Outputs a formatted console message with timestamp, program name, and execution state using ANSI colors.

        This private method creates a structured log line that displays execution information
        in a consistent format. The output includes a timestamp, program name, dotted line
        separator, optional execution time, and colored state indicator.

        Parameters
        ----------
        program : str
            The name of the program or process being executed.
        state : str
            The current execution state (e.g., 'RUNNING', 'DONE', 'FAIL').
        state_color : str
            The ANSI color code used to colorize the state text.
        time : str, optional
            The execution time duration with units (e.g., '30s', '2m 15s').
            Default is an empty string if no time information is available.

        Returns
        -------
        None
            This method does not return any value. It prints the formatted message
            directly to the console output.
        """
        # Define the total width for the formatted output line
        width = 60

        # Calculate the length of state and time strings for spacing calculations
        len_state = len(state)
        len_time = len(time)

        # Create a dotted line that fills the remaining space between program name and state/time
        line = '.' * (width - (len(program) + len_state + len_time))

        # Format the timestamp with muted color and current date/time
        timestamp = f"{ANSIColors.TEXT_MUTED.value}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{ANSIColors.DEFAULT.value}"

        # Keep program name without additional formatting
        program_formatted = f"{program}"

        # Format time with muted color if provided, otherwise use empty string
        time_formatted = f"{ANSIColors.TEXT_MUTED.value}{time}{ANSIColors.DEFAULT.value}" if time else ""

        # Format state with the specified color and reset to default
        state_formatted = f"{state_color}{state}{ANSIColors.DEFAULT.value}"

        # Add line breaks for RUNNING state at start, for other states at end
        start = "\n\r" if state == 'RUNNING' else ''
        end = "\n\r" if state != 'RUNNING' else ''

        # Print the complete formatted message to console
        print(f"{start}{timestamp} | {program_formatted} {line} {time_formatted} {state_formatted}{end}")

    def running(self, program: str, time: str = ''):
        """
        Logs the execution of a program in a "RUNNING" state with console output formatting.

        This method outputs a formatted console message indicating that a program or process
        is currently running. It uses ANSI color coding to highlight the running state with
        a warning color (typically yellow/orange) to draw attention to active processes.
        The output includes timestamp, program name, optional execution time, and colored
        state indicator in a structured format.

        Parameters
        ----------
        program : str
            The name of the program or process that is currently being executed.
            This will be displayed in the console output to identify which process
            is in the running state.
        time : str, optional
            The current execution time duration with appropriate units (e.g., '30s', '2m 15s').
            If not provided, defaults to an empty string and no time information will be
            displayed in the output. Default is ''.

        Returns
        -------
        None
            This method does not return any value. It prints the formatted running state
            message directly to the console output via the private __ansiOutput method.
        """

        # Call the private ANSI output method with RUNNING state and warning color formatting
        self.__ansiOutput(program, "RUNNING", ANSIColors.TEXT_BOLD_WARNING.value, time)

    def done(self, program: str, time: str = ''):
        """
        Logs the execution of a program in a "DONE" state with console output formatting.

        This method outputs a formatted console message indicating that a program or process
        has completed successfully. It uses ANSI color coding to highlight the completion state
        with a success color (typically green) to indicate successful execution. The output
        includes timestamp, program name, optional execution time, and colored state indicator
        in a structured format consistent with other execution state methods.

        Parameters
        ----------
        program : str
            The name of the program or process that has completed execution.
            This will be displayed in the console output to identify which process
            has finished successfully.
        time : str, optional
            The total execution time duration with appropriate units (e.g., '30s', '2m 15s').
            If not provided, defaults to an empty string and no time information will be
            displayed in the output. Default is ''.

        Returns
        -------
        None
            This method does not return any value. It prints the formatted completion state
            message directly to the console output via the private __ansiOutput method.
        """

        # Call the private ANSI output method with DONE state and success color formatting
        self.__ansiOutput(program, "DONE", ANSIColors.TEXT_BOLD_SUCCESS.value, time)

    def fail(self, program: str, time: str = ''):
        """
        Logs the execution of a program in a "FAIL" state with console output formatting.

        This method outputs a formatted console message indicating that a program or process
        has failed during execution. It uses ANSI color coding to highlight the failure state
        with an error color (typically red) to clearly indicate unsuccessful execution. The output
        includes timestamp, program name, optional execution time, and colored state indicator
        in a structured format consistent with other execution state methods.

        Parameters
        ----------
        program : str
            The name of the program or process that has failed during execution.
            This will be displayed in the console output to identify which process
            encountered an error or failure.
        time : str, optional
            The execution time duration before failure with appropriate units (e.g., '30s', '2m 15s').
            If not provided, defaults to an empty string and no time information will be
            displayed in the output. Default is ''.

        Returns
        -------
        None
            This method does not return any value. It prints the formatted failure state
            message directly to the console output via the private __ansiOutput method.
        """

        # Call the private ANSI output method with FAIL state and error color formatting
        self.__ansiOutput(program, "FAIL", ANSIColors.TEXT_BOLD_ERROR.value, time)
