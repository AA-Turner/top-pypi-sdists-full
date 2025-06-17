######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.875775                                                            #
######################################################################################################

from __future__ import annotations

import typing

from .metaflow_runner import Runner as Runner
from .utils import get_current_cell as get_current_cell
from .utils import format_flowfile as format_flowfile

class NBRunnerInitializationError(Exception, metaclass=type):
    """
    Custom exception for errors during NBRunner initialization.
    """
    ...

class NBRunner(object, metaclass=type):
    """
    A  wrapper over `Runner` for executing flows defined in a Jupyter
    notebook cell.
    
    Instantiate this class on the last line of a notebook cell where
    a `flow` is defined. In contrast to `Runner`, this class is not
    meant to be used in a context manager. Instead, use a blocking helper
    function like `nbrun` (which calls `cleanup()` internally) or call
    `cleanup()` explictly when using non-blocking APIs.
    
    ```python
    run = NBRunner(FlowName).nbrun()
    ```
    
    Parameters
    ----------
    flow : FlowSpec
        Flow defined in the same cell
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default,
        Only applicable for synchronous 'run' and 'resume' functions.
    profile : str, optional, default None
        Metaflow profile to use to run this run. If not specified, the default
        profile is used (or the one already set using `METAFLOW_PROFILE`)
    env : Dict[str, str], optional, default None
        Additional environment variables to set for the Run. This overrides the
        environment set for this process.
    base_dir : str, optional, default None
        The directory to run the subprocess in; if not specified, the current
        working directory is used.
    file_read_timeout : int, default 3600
        The timeout until which we try to read the runner attribute file (in seconds).
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` before
        the `run` command.
    """
    def __init__(self, flow, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, base_dir: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def nbrun(self, **kwargs):
        """
        Blocking execution of the run. This method will wait until
        the run has completed execution.
        
        Note that in contrast to `run`, this method returns a
        `metaflow.Run` object directly and calls `cleanup()` internally
        to support a common notebook pattern of executing a flow and
        retrieving its results immediately.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `run` command, in particular, any parameters accepted by the flow.
        
        Returns
        -------
        Run
            A `metaflow.Run` object representing the finished run.
        """
        ...
    def nbresume(self, **kwargs):
        """
        Blocking resuming of a run. This method will wait until
        the resumed run has completed execution.
        
        Note that in contrast to `resume`, this method returns a
        `metaflow.Run` object directly and calls `cleanup()` internally
        to support a common notebook pattern of executing a flow and
        retrieving its results immediately.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments that you would pass to `python myflow.py` after
            the `resume` command.
        
        Returns
        -------
        Run
            A `metaflow.Run` object representing the resumed run.
        """
        ...
    def run(self, **kwargs):
        """
        Runs the flow.
        """
        ...
    def resume(self, **kwargs):
        """
        Resumes the flow.
        """
        ...
    def async_run(self, **kwargs):
        """
        Non-blocking execution of the run. This method will return as soon as the
        run has launched. This method is equivalent to `Runner.async_run`.
        
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
    def async_resume(self, **kwargs):
        """
        Non-blocking execution of the run. This method will return as soon as the
        run has launched. This method is equivalent to `Runner.async_resume`.
        
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
    def cleanup(self):
        """
        Delete any temporary files created during execution.
        
        Call this method after using `async_run` or `async_resume`. You don't
        have to call this after `nbrun` or `nbresume`.
        """
        ...
    ...

