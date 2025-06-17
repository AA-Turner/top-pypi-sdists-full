######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.895952                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.runner.subprocess_manager
    import typing
    import metaflow.runner.click_api


TYPE_CHECKING: bool

def get_current_cell(ipython):
    ...

def format_flowfile(cell):
    """
    Formats the given cell content to create a valid Python script that can be
    executed as a Metaflow flow.
    """
    ...

def check_process_exited(command_obj: "metaflow.runner.subprocess_manager.CommandManager") -> bool:
    ...

def temporary_fifo() -> typing.ContextManager[typing.Tuple[str, int]]:
    """
    Create and open the read side of a temporary FIFO in a non-blocking mode.
    
    Returns
    -------
    str
        Path to the temporary FIFO.
    int
        File descriptor of the temporary FIFO.
    """
    ...

def read_from_fifo_when_ready(fifo_fd: int, command_obj: "metaflow.runner.subprocess_manager.CommandManager", encoding: str = 'utf-8', timeout: int = 3600) -> str:
    """
    Read the content from the FIFO file descriptor when it is ready.
    
    Parameters
    ----------
    fifo_fd : int
        File descriptor of the FIFO.
    command_obj : CommandManager
        Command manager object that handles the write side of the FIFO.
    encoding : str, optional
        Encoding to use while reading the file, by default "utf-8".
    timeout : int, optional
        Timeout for reading the file in seconds, by default 3600.
    
    Returns
    -------
    str
        Content read from the FIFO.
    
    Raises
    ------
    TimeoutError
        If no event occurs on the FIFO within the timeout.
    CalledProcessError
        If the process managed by `command_obj` has exited without writing any
        content to the FIFO.
    """
    ...

def async_read_from_fifo_when_ready(fifo_fd: int, command_obj: "metaflow.runner.subprocess_manager.CommandManager", encoding: str = 'utf-8', timeout: int = 3600) -> str:
    """
    Read the content from the FIFO file descriptor when it is ready.
    
    Parameters
    ----------
    fifo_fd : int
        File descriptor of the FIFO.
    command_obj : CommandManager
        Command manager object that handles the write side of the FIFO.
    encoding : str, optional
        Encoding to use while reading the file, by default "utf-8".
    timeout : int, optional
        Timeout for reading the file in seconds, by default 3600.
    
    Returns
    -------
    str
        Content read from the FIFO.
    
    Raises
    ------
    TimeoutError
        If no event occurs on the FIFO within the timeout.
    CalledProcessError
        If the process managed by `command_obj` has exited without writing any
        content to the FIFO.
    """
    ...

def make_process_error_message(command_obj: "metaflow.runner.subprocess_manager.CommandManager"):
    ...

def handle_timeout(attribute_file_fd: int, command_obj: "metaflow.runner.subprocess_manager.CommandManager", file_read_timeout: int):
    """
    Handle the timeout for a running subprocess command that reads a file
    and raises an error with appropriate logs if a TimeoutError occurs.
    
    Parameters
    ----------
    attribute_file_fd : int
        File descriptor belonging to the FIFO containing the attribute data.
    command_obj : CommandManager
        Command manager object that encapsulates the running command details.
    file_read_timeout : int
        Timeout for reading the file, in seconds
    
    Returns
    -------
    str
        Content read from the temporary file.
    
    Raises
    ------
    RuntimeError
        If a TimeoutError occurs, it raises a RuntimeError with the command's
        stdout and stderr logs.
    """
    ...

def async_handle_timeout(attribute_file_fd: int, command_obj: "metaflow.runner.subprocess_manager.CommandManager", file_read_timeout: int):
    """
    Handle the timeout for a running subprocess command that reads a file
    and raises an error with appropriate logs if a TimeoutError occurs.
    
    Parameters
    ----------
    attribute_file_fd : int
        File descriptor belonging to the FIFO containing the attribute data.
    command_obj : CommandManager
        Command manager object that encapsulates the running command details.
    file_read_timeout : int
        Timeout for reading the file, in seconds
    
    Returns
    -------
    str
        Content read from the temporary file.
    
    Raises
    ------
    RuntimeError
        If a TimeoutError occurs, it raises a RuntimeError with the command's
        stdout and stderr logs.
    """
    ...

def get_lower_level_group(api: "metaflow.runner.click_api.MetaflowAPI", top_level_kwargs: typing.Dict[str, typing.Any], sub_command: str, sub_command_kwargs: typing.Dict[str, typing.Any]) -> "metaflow.runner.click_api.MetaflowAPI":
    """
    Retrieve a lower-level group from the API based on the type and provided arguments.
    
    Parameters
    ----------
    api : MetaflowAPI
        Metaflow API instance.
    top_level_kwargs : Dict[str, Any]
        Top-level keyword arguments to pass to the API.
    sub_command : str
        Sub-command of API to get the API for
    sub_command_kwargs : Dict[str, Any]
        Sub-command arguments
    
    Returns
    -------
    MetaflowAPI
        The lower-level group object retrieved from the API.
    
    Raises
    ------
    ValueError
        If the `_type` is None.
    """
    ...

def with_dir(new_dir):
    ...

