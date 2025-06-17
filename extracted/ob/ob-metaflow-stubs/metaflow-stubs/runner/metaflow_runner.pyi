######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.875166                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.client.core
    import metaflow.runner.metaflow_runner
    import metaflow.runner.subprocess_manager

from ..client.core import Run as Run
from ..plugins import get_runner_cli as get_runner_cli
from .utils import temporary_fifo as temporary_fifo
from .utils import handle_timeout as handle_timeout
from .utils import async_handle_timeout as async_handle_timeout
from .utils import with_dir as with_dir
from .subprocess_manager import CommandManager as CommandManager
from .subprocess_manager import SubprocessManager as SubprocessManager

CLICK_API_PROCESS_CONFIG: bool

class ExecutingRun(object, metaclass=type):
    """
    This class contains a reference to a `metaflow.Run` object representing
    the currently executing or finished run, as well as metadata related
    to the process.
    
    `ExecutingRun` is returned by methods in `Runner` and `NBRunner`. It is not
    meant to be instantiated directly.
    
    This class works as a context manager, allowing you to use a pattern like
    ```python
    with Runner(...).run() as running:
        ...
    ```
    Note that you should use either this object as the context manager or
    `Runner`, not both in a nested manner.
    """
    def __init__(self, runner: Runner, command_obj: metaflow.runner.subprocess_manager.CommandManager, run_obj: metaflow.client.core.Run):
        """
        Create a new ExecutingRun -- this should not be done by the user directly but
        instead user Runner.run()
        
        Parameters
        ----------
        runner : Runner
            Parent runner for this run.
        command_obj : CommandManager
            CommandManager containing the subprocess executing this run.
        run_obj : Run
            Run object corresponding to this run.
        """
        ...
    def __enter__(self) -> "ExecutingRun":
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        ...
    def wait(self, timeout: typing.Optional[float] = None, stream: typing.Optional[str] = None) -> "ExecutingRun":
        """
        Wait for this run to finish, optionally with a timeout
        and optionally streaming its output.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        timeout : float, optional, default None
            The maximum time, in seconds, to wait for the run to finish.
            If the timeout is reached, the run is terminated. If not specified, wait
            forever.
        stream : str, optional, default None
            If specified, the specified stream is printed to stdout. `stream` can
            be one of `stdout` or `stderr`.
        
        Returns
        -------
        ExecutingRun
            This object, allowing you to chain calls.
        """
        ...
    @property
    def returncode(self) -> typing.Optional[int]:
        """
        Gets the return code of the underlying subprocess. A non-zero
        code indicates a failure, `None` a currently executing run.
        
        Returns
        -------
        Optional[int]
            The return code of the underlying subprocess.
        """
        ...
    @property
    def status(self) -> str:
        """
        Returns the status of the underlying subprocess that is responsible
        for executing the run.
        
        The return value is one of the following strings:
        - `timeout` indicates that the run timed out.
        - `running` indicates a currently executing run.
        - `failed` indicates a failed run.
        - `successful` indicates a successful run.
        
        Returns
        -------
        str
            The current status of the run.
        """
        ...
    @property
    def stdout(self) -> str:
        """
        Returns the current stdout of the run. If the run is finished, this will
        contain the entire stdout output. Otherwise, it will contain the
        stdout up until this point.
        
        Returns
        -------
        str
            The current snapshot of stdout.
        """
        ...
    @property
    def stderr(self) -> str:
        """
        Returns the current stderr of the run. If the run is finished, this will
        contain the entire stderr output. Otherwise, it will contain the
        stderr up until this point.
        
        Returns
        -------
        str
            The current snapshot of stderr.
        """
        ...
    def stream_log(self, stream: str, position: typing.Optional[int] = None) -> typing.Iterator[typing.Tuple[int, str]]:
        """
        Asynchronous iterator to stream logs from the subprocess line by line.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        stream : str
            The stream to stream logs from. Can be one of `stdout` or `stderr`.
        position : int, optional, default None
            The position in the log file to start streaming from. If None, it starts
            from the beginning of the log file. This allows resuming streaming from
            a previously known position
        
        Yields
        ------
        Tuple[int, str]
            A tuple containing the position in the log file and the line read. The
            position returned can be used to feed into another `stream_logs` call
            for example.
        """
        ...
    ...

class RunnerMeta(type, metaclass=type):
    @staticmethod
    def __new__(mcs, name, bases, dct):
        ...
    ...

class Runner(object, metaclass=RunnerMeta):
    """
    Metaflow's Runner API that presents a programmatic interface
    to run flows and perform other operations either synchronously or asynchronously.
    The class expects a path to the flow file along with optional arguments
    that match top-level options on the command-line.
    
    This class works as a context manager, calling `cleanup()` to remove
    temporary files at exit.
    
    Example:
    ```python
    with Runner('slowflow.py', pylint=False) as runner:
        result = runner.run(alpha=5, tags=["abc", "def"], max_workers=5)
        print(result.run.finished)
    ```
    
    Parameters
    ----------
    flow_file : str
        Path to the flow file to run, relative to current directory.
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default,
        Only applicable for synchronous 'run' and 'resume' functions.
    profile : str, optional, default None
        Metaflow profile to use to run this run. If not specified, the default
        profile is used (or the one already set using `METAFLOW_PROFILE`)
    env : Dict[str, str], optional, default None
        Additional environment variables to set for the Run. This overrides the
        environment set for this process.
    cwd : str, optional, default None
        The directory to run the subprocess in; if not specified, the current
        directory is used.
    file_read_timeout : int, default 3600
        The timeout until which we try to read the runner attribute file (in seconds).
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` before
        the `run` command.
    """
    def __init__(self, flow_file: str, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict[str, str]] = None, cwd: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def __enter__(self) -> "Runner":
        ...
    def __aenter__(self) -> "Runner":
        ...
    def _Runner__get_executing_run(self, attribute_file_fd, command_obj):
        ...
    def _Runner__async_get_executing_run(self, attribute_file_fd, command_obj):
        ...
    def run(self, **kwargs) -> ExecutingRun:
        """
        Blocking execution of the run. This method will wait until
        the run has completed execution.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun containing the results of the run.
        """
        ...
    def resume(self, **kwargs) -> ExecutingRun:
        """
        Blocking resume execution of the run.
        This method will wait until the resumed run has completed execution.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python ./myflow.py` after
            the `resume` command.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun containing the results of the resumed run.
        """
        ...
    def async_run(self, **kwargs) -> ExecutingRun:
        """
        Non-blocking execution of the run. This method will return as soon as the
        run has launched.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun representing the run that was started.
        """
        ...
    def async_resume(self, **kwargs) -> ExecutingRun:
        """
        Non-blocking resume execution of the run.
        This method will return as soon as the resume has launched.
        
        Note that this method is asynchronous and needs to be `await`ed.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `resume` command.
        
        Returns
        -------
        ExecutingRun
            ExecutingRun representing the resumed run that was started.
        """
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        ...
    def __aexit__(self, exc_type, exc_value, traceback):
        ...
    def cleanup(self):
        """
        Delete any temporary files created during execution.
        """
        ...
    ...

