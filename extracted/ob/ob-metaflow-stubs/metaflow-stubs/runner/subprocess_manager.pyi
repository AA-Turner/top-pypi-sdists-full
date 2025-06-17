######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.897018                                                            #
######################################################################################################

from __future__ import annotations

import typing

from .utils import check_process_exited as check_process_exited

def kill_processes_and_descendants(pids: typing.List[str], termination_timeout: float):
    ...

def async_kill_processes_and_descendants(pids: typing.List[str], termination_timeout: float):
    ...

class LogReadTimeoutError(Exception, metaclass=type):
    """
    Exception raised when reading logs times out.
    """
    ...

class SubprocessManager(object, metaclass=type):
    """
    A manager for subprocesses. The subprocess manager manages one or more
    CommandManager objects, each of which manages an individual subprocess.
    """
    def __init__(self):
        ...
    def __aenter__(self) -> "SubprocessManager":
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def run_command(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None, show_output: bool = False) -> int:
        """
        Run a command synchronously and return its process ID.
        
        Note: in no case does this wait for the process to *finish*. Use sync_wait()
        to wait for the command to finish.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        show_output : bool, default False
            Suppress the 'stdout' and 'stderr' to the console by default.
            They can be accessed later by reading the files present in the
            CommandManager object:
                - command_obj.log_files["stdout"]
                - command_obj.log_files["stderr"]
        Returns
        -------
        int
            The process ID of the subprocess.
        """
        ...
    def async_run_command(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None) -> int:
        """
        Run a command asynchronously and return its process ID.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        
        Returns
        -------
        int
            The process ID of the subprocess.
        """
        ...
    def get(self, pid: int) -> typing.Optional["CommandManager"]:
        """
        Get one of the CommandManager managed by this SubprocessManager.
        
        Parameters
        ----------
        pid : int
            The process ID of the subprocess (returned by run_command or async_run_command).
        
        Returns
        -------
        Optional[CommandManager]
            The CommandManager object for the given process ID, or None if not found.
        """
        ...
    def cleanup(self):
        """
        Clean up log files for all running subprocesses.
        """
        ...
    ...

class CommandManager(object, metaclass=type):
    """
    A manager for an individual subprocess.
    """
    def __init__(self, command: typing.List[str], env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None):
        """
        Create a new CommandManager object.
        This does not run the process itself but sets it up.
        
        Parameters
        ----------
        command : List[str]
            The command to run in List form.
        env : Optional[Dict[str, str]], default None
            Environment variables to set for the subprocess; if not specified,
            the current enviornment variables are used.
        cwd : Optional[str], default None
            The directory to run the subprocess in; if not specified, the current
            directory is used.
        """
        ...
    def __aenter__(self) -> "CommandManager":
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def wait(self, timeout: typing.Optional[float] = None, stream: typing.Optional[str] = None):
        """
        Wait for the subprocess to finish, optionally with a timeout
        and optionally streaming its output.
        
        You can only call `wait` if `async_run` has already been called.
        
        Parameters
        ----------
        timeout : Optional[float], default None
            The maximum time to wait for the subprocess to finish.
            If the timeout is reached, the subprocess is killed.
        stream : Optional[str], default None
            If specified, the specified stream is printed to stdout. `stream` can
            be one of `stdout` or `stderr`.
        """
        ...
    def sync_wait(self):
        ...
    def run(self, show_output: bool = False):
        """
        Run the subprocess synchronously. This can only be called once.
        
        This also waits on the process implicitly.
        
        Parameters
        ----------
        show_output : bool, default False
            Suppress the 'stdout' and 'stderr' to the console by default.
            They can be accessed later by reading the files present in:
                - self.log_files["stdout"]
                - self.log_files["stderr"]
        """
        ...
    def async_run(self):
        """
        Run the subprocess asynchronously. This can only be called once.
        
        Once this is called, you can then wait on the process (using `wait`), stream
        logs (using `stream_logs`) or kill it (using `kill`).
        """
        ...
    def stream_log(self, stream: str, position: typing.Optional[int] = None, timeout_per_line: typing.Optional[float] = None, log_write_delay: float = 0.01) -> typing.Iterator[typing.Tuple[int, str]]:
        """
        Stream logs from the subprocess line by line.
        
        Parameters
        ----------
        stream : str
            The stream to stream logs from. Can be one of "stdout" or "stderr".
        position : Optional[int], default None
            The position in the log file to start streaming from. If None, it starts
            from the beginning of the log file. This allows resuming streaming from
            a previously known position
        timeout_per_line : Optional[float], default None
            The time to wait for a line to be read from the log file. If None, it
            waits indefinitely. If the timeout is reached, a LogReadTimeoutError
            is raised. Note that this timeout is *per line* and not cumulative so this
            function may take significantly more time than `timeout_per_line`
        log_write_delay : float, default 0.01
            Improves the probability of getting whole lines. This setting is for
            advanced use cases.
        
        Yields
        ------
        Tuple[int, str]
            A tuple containing the position in the log file and the line read. The
            position returned can be used to feed into another `stream_logs` call
            for example.
        """
        ...
    def emit_logs(self, stream: str = 'stdout', custom_logger: typing.Callable[..., None] = ...):
        """
        Helper function that can easily emit all the logs for a given stream.
        
        This function will only terminate when all the log has been printed.
        
        Parameters
        ----------
        stream : str, default "stdout"
            The stream to emit logs for. Can be one of "stdout" or "stderr".
        custom_logger : Callable[..., None], default print
            A custom logger function that takes in a string and "emits" it. By default,
            the log is printed to stdout.
        """
        ...
    def cleanup(self):
        """
        Clean up log files for a running subprocesses.
        """
        ...
    def kill(self, termination_timeout: float = 2):
        """
        Kill the subprocess and its descendants.
        
        Parameters
        ----------
        termination_timeout : float, default 2
            The time to wait after sending a SIGTERM to the process and its descendants
            before sending a SIGKILL.
        """
        ...
    ...

def main():
    ...

