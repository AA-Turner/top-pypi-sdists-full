######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.897571                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing
    import metaflow.runner.deployer

from .subprocess_manager import SubprocessManager as SubprocessManager
from .utils import get_lower_level_group as get_lower_level_group
from .utils import handle_timeout as handle_timeout
from .utils import temporary_fifo as temporary_fifo
from .utils import with_dir as with_dir

TYPE_CHECKING: bool

CLICK_API_PROCESS_CONFIG: bool

class DeployerImpl(object, metaclass=type):
    """
    Base class for deployer implementations. Each implementation should define a TYPE
    class variable that matches the name of the CLI group.
    
    Parameters
    ----------
    flow_file : str
        Path to the flow file to deploy, relative to current directory.
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default.
    profile : Optional[str], default None
        Metaflow profile to use for the deployment. If not specified, the default
        profile is used.
    env : Optional[Dict], default None
        Additional environment variables to set for the deployment.
    cwd : Optional[str], default None
        The directory to run the subprocess in; if not specified, the current
        directory is used.
    file_read_timeout : int, default 3600
        The timeout until which we try to read the deployer attribute file (in seconds).
    **kwargs : Any
        Additional arguments that you would pass to `python myflow.py` before
        the deployment command.
    """
    def __init__(self, flow_file: str, show_output: bool = True, profile: typing.Optional[str] = None, env: typing.Optional[typing.Dict] = None, cwd: typing.Optional[str] = None, file_read_timeout: int = 3600, **kwargs):
        ...
    @property
    def deployer_kwargs(self) -> typing.Dict[str, typing.Any]:
        ...
    @staticmethod
    def deployed_flow_type() -> typing.Type["metaflow.runner.deployer.DeployedFlow"]:
        ...
    def __enter__(self) -> "DeployerImpl":
        ...
    def create(self, **kwargs) -> "metaflow.runner.deployer.DeployedFlow":
        """
        Create a sub-class of a `DeployedFlow` depending on the deployer implementation.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments to pass to `create` corresponding to the
            command line arguments of `create`
        
        Returns
        -------
        DeployedFlow
            DeployedFlow object representing the deployed flow.
        
        Raises
        ------
        Exception
            If there is an error during deployment.
        """
        ...
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleanup resources on exit.
        """
        ...
    def cleanup(self):
        """
        Cleanup resources.
        """
        ...
    ...

