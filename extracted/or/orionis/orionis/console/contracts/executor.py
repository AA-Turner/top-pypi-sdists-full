from abc import ABC, abstractmethod

class IExecutor(ABC):

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
