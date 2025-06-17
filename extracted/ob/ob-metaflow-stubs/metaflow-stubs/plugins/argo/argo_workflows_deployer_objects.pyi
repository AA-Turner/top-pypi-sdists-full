######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.999055                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.argo.argo_workflows_deployer_objects
    import metaflow.runner.deployer

from ...client.core import get_metadata as get_metadata
from ...exception import MetaflowException as MetaflowException
from .argo_client import ArgoClient as ArgoClient
from .argo_workflows import ArgoWorkflows as ArgoWorkflows
from ...runner.deployer import Deployer as Deployer
from ...runner.deployer import DeployedFlow as DeployedFlow
from ...runner.deployer import TriggeredRun as TriggeredRun
from ...runner.deployer import generate_fake_flow_file_contents as generate_fake_flow_file_contents
from ...runner.utils import get_lower_level_group as get_lower_level_group
from ...runner.utils import handle_timeout as handle_timeout
from ...runner.utils import temporary_fifo as temporary_fifo

KUBERNETES_NAMESPACE: str

class ArgoWorkflowsTriggeredRun(metaflow.runner.deployer.TriggeredRun, metaclass=type):
    """
    A class representing a triggered Argo Workflow execution.
    """
    def suspend(self, **kwargs) -> bool:
        """
        Suspend the running workflow.
        
        Parameters
        ----------
        authorize : str, optional, default None
            Authorize the suspension with a production token.
        
        Returns
        -------
        bool
            True if the command was successful, False otherwise.
        """
        ...
    def unsuspend(self, **kwargs) -> bool:
        """
        Unsuspend the suspended workflow.
        
        Parameters
        ----------
        authorize : str, optional, default None
            Authorize the unsuspend with a production token.
        
        Returns
        -------
        bool
            True if the command was successful, False otherwise.
        """
        ...
    def terminate(self, **kwargs) -> bool:
        """
        Terminate the running workflow.
        
        Parameters
        ----------
        authorize : str, optional, default None
            Authorize the termination with a production token.
        
        Returns
        -------
        bool
            True if the command was successful, False otherwise.
        """
        ...
    def wait_for_completion(self, check_interval: int = 5, timeout: typing.Optional[int] = None):
        """
        Wait for the workflow to complete or timeout.
        
        Parameters
        ----------
        check_interval: int, default: 5
            Frequency of checking for workflow completion, in seconds.
        timeout : int, optional, default None
            Maximum time in seconds to wait for workflow completion.
            If None, waits indefinitely.
        
        Raises
        ------
        TimeoutError
            If the workflow does not complete within the specified timeout period.
        """
        ...
    @property
    def is_running(self):
        """
        Check if the workflow is currently running.
        
        Returns
        -------
        bool
            True if the workflow status is either 'Pending' or 'Running',
            False otherwise.
        """
        ...
    @property
    def status(self) -> typing.Optional[str]:
        """
        Get the status of the triggered run.
        
        Returns
        -------
        str, optional
            The status of the workflow considering the run object, or None if
            the status could not be retrieved.
        """
        ...
    ...

class ArgoWorkflowsDeployedFlow(metaflow.runner.deployer.DeployedFlow, metaclass=metaflow.runner.deployer.DeployedFlowMeta):
    """
    A class representing a deployed Argo Workflow template.
    """
    @classmethod
    def from_deployment(cls, identifier: str, metadata: typing.Optional[str] = None):
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
    @property
    def production_token(self) -> typing.Optional[str]:
        """
        Get the production token for the deployed flow.
        
        Returns
        -------
        str, optional
            The production token, None if it cannot be retrieved.
        """
        ...
    def delete(self, **kwargs) -> bool:
        """
        Delete the deployed workflow template.
        
        Parameters
        ----------
        authorize : str, optional, default None
            Authorize the deletion with a production token.
        
        Returns
        -------
        bool
            True if the command was successful, False otherwise.
        """
        ...
    def trigger(self, **kwargs) -> ArgoWorkflowsTriggeredRun:
        """
        Trigger a new run for the deployed flow.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments to pass to the trigger command,
            `Parameters` in particular.
        
        Returns
        -------
        ArgoWorkflowsTriggeredRun
            The triggered run instance.
        
        Raises
        ------
        Exception
            If there is an error during the trigger process.
        """
        ...
    ...

