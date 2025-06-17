######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.876155                                                            #
######################################################################################################

from __future__ import annotations

import typing

from .deployer import Deployer as Deployer
from .utils import get_current_cell as get_current_cell
from .utils import format_flowfile as format_flowfile

class NBDeployerInitializationError(Exception, metaclass=type):
    """
    Custom exception for errors during NBDeployer initialization.
    """
    ...

class NBDeployer(object, metaclass=type):
    """
    A  wrapper over `Deployer` for deploying flows defined in a Jupyter
    notebook cell.
    
    Instantiate this class on the last line of a notebook cell where
    a `flow` is defined. In contrast to `Deployer`, this class is not
    meant to be used in a context manager.
    
    ```python
    deployer = NBDeployer(FlowName)
    ar = deployer.argo_workflows(name="madhur")
    ar_obj = ar.create()
    result = ar_obj.trigger(alpha=300)
    print(result.status)
    print(result.run)
    result.terminate()
    ```
    
    Parameters
    ----------
    flow : FlowSpec
        Flow defined in the same cell
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default,
    profile : str, optional, default None
        Metaflow profile to use to deploy this run. If not specified, the default
        profile is used (or the one already set using `METAFLOW_PROFILE`)
    env : Dict[str, str], optional, default None
        Additional environment variables to set. This overrides the
        environment set for this process.
    base_dir : str, optional, default None
        The directory to run the subprocess in; if not specified, the current
        working directory is used.
    file_read_timeout : int, default 3600
        The timeout until which we try to read the deployer attribute file (in seconds).
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` i.e. options
        listed in `python myflow.py --help`
    """
    def __init__(self, flow, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, base_dir: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    def __getattr__(self, name):
        """
        Forward all attribute access to the underlying `Deployer` instance.
        """
        ...
    def cleanup(self):
        """
        Delete any temporary files created during execution.
        """
        ...
    ...

