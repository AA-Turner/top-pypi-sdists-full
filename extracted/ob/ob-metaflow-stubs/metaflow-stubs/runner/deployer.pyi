######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.041088                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow
    import metaflow.runner.deployer
    import metaflow.plugins.aws.step_functions.step_functions_deployer
    import metaflow.plugins.argo.argo_workflows_deployer
    import metaflow.plugins.argo.argo_workflows_deployer_objects
    import metaflow.plugins.aws.step_functions.step_functions_deployer_objects

from ..exception import MetaflowNotFound as MetaflowNotFound

TYPE_CHECKING: bool

DEFAULT_FROM_DEPLOYMENT_IMPL: str

def generate_fake_flow_file_contents(flow_name: str, param_info: dict, project_name: typing.Optional[str] = None):
    ...

class DeployerMeta(type, metaclass=type):
    @staticmethod
    def __new__(mcs, name, bases, dct):
        ...
    ...

class Deployer(object, metaclass=DeployerMeta):
    """
    Use the `Deployer` class to configure and access one of the production
    orchestrators supported by Metaflow.
    
    Parameters
    ----------
    flow_file : str
        Path to the flow file to deploy, relative to current directory.
    show_output : bool, default True
        Show the 'stdout' and 'stderr' to the console by default.
    profile : Optional[str], default None
        Metaflow profile to use for the deployment. If not specified, the default
        profile is used.
    env : Optional[Dict[str, str]], default None
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
    def argo_workflows(self, *, name: typing.Optional[str] = None) -> "metaflow.plugins.argo.argo_workflows_deployer.ArgoWorkflowsDeployer":
        """
        Deployer implementation for Argo Workflows.
        
        Parameters
        ----------
        name : str, optional, default None
            Argo workflow name. The flow name is used instead if this option is not specified.
        """
        ...
    def step_functions(self, *, name: typing.Optional[str] = None) -> "metaflow.plugins.aws.step_functions.step_functions_deployer.StepFunctionsDeployer":
        """
        Deployer implementation for AWS Step Functions.
        
        Parameters
        ----------
        name : str, optional, default None
            State Machine name. The flow name is used instead if this option is not specified.
        """
        ...
    ...

class TriggeredRun(object, metaclass=type):
    """
    TriggeredRun class represents a run that has been triggered on a
    production orchestrator.
    """
    def wait_for_run(self, check_interval: int = 5, timeout: typing.Optional[int] = None):
        """
        Wait for the `run` property to become available.
        
        The `run` property becomes available only after the `start` task of the triggered
        flow starts running.
        
        Parameters
        ----------
        check_interval: int, default: 5
            Frequency of checking for the `run` to become available, in seconds.
        timeout : int, optional, default None
            Maximum time to wait for the `run` to become available, in seconds. If
            None, wait indefinitely.
        
        Raises
        ------
        TimeoutError
            If the `run` is not available within the specified timeout.
        """
        ...
    @property
    def run(self) -> typing.Optional["metaflow.Run"]:
        """
        Retrieve the `Run` object for the triggered run.
        
        Note that Metaflow `Run` becomes available only when the `start` task
        has started executing.
        
        Returns
        -------
        Run, optional
            Metaflow Run object if the `start` step has started executing, otherwise None.
        """
        ...
    ...

class DeployedFlowMeta(type, metaclass=type):
    @staticmethod
    def __new__(mcs, name, bases, dct):
        ...
    ...

class DeployedFlow(object, metaclass=DeployedFlowMeta):
    """
    DeployedFlow class represents a flow that has been deployed.
    
    This class is not meant to be instantiated directly. Instead, it is returned from
    methods of `Deployer`.
    """
    @classmethod
    def from_deployment(cls, *, identifier: str, metadata: typing.Optional[str] = None, impl: typing.Optional[str] = 'given by METAFLOW_DEFAULT_FROM_DEPLOYMENT_IMPL') -> typing.Union["metaflow.plugins.argo.argo_workflows_deployer_objects.ArgoWorkflowsDeployedFlow", "metaflow.plugins.aws.step_functions.step_functions_deployer_objects.StepFunctionsDeployedFlow"]:
        """
        Retrieves a `DeployedFlow` object from an identifier and optional
        metadata. The `impl` parameter specifies the deployer implementation
        to use (like `argo-workflows`).
        
        
        
        Parameters
        ----------
        identifier : str
            Deployer specific identifier for the workflow to retrieve
        metadata : str, optional, default None
            Optional deployer specific metadata.
        impl : str, optional, default given by METAFLOW_DEFAULT_FROM_DEPLOYMENT_IMPL
            The default implementation to use if not specified
        
        
        
        Returns
        -------
        typing.Union[ForwardRef('metaflow.plugins.argo.argo_workflows_deployer_objects.ArgoWorkflowsDeployedFlow'), ForwardRef('metaflow.plugins.aws.step_functions.step_functions_deployer_objects.StepFunctionsDeployedFlow')]
        A `DeployedFlow` object
        """
        ...
    @classmethod
    def from_argo_workflows(cls, *, identifier: str, metadata: typing.Optional[str] = None) -> "metaflow.plugins.argo.argo_workflows_deployer_objects.ArgoWorkflowsDeployedFlow":
        """
        Retrieves a `ArgoWorkflowsDeployedFlow` object from an identifier and optional
        metadata.
        
        
        
        Parameters
        ----------
        identifier : str
            Deployer specific identifier for the workflow to retrieve
        metadata : str, optional, default None
            Optional deployer specific metadata.
        
        
        
        Returns
        -------
        ArgoWorkflowsDeployedFlow
            A `ArgoWorkflowsDeployedFlow` object representing the
            deployed flow on argo workflows.
        """
        ...
    @classmethod
    def from_step_functions(cls) -> "metaflow.plugins.aws.step_functions.step_functions_deployer_objects.StepFunctionsDeployedFlow":
        """
        This method is not currently implemented for Step Functions.
        
        Raises
        ------
        NotImplementedError
            This method is not implemented for Step Functions.
        
        Parameters
        ----------
        
        
        Returns
        -------
        """
        ...
    ...

