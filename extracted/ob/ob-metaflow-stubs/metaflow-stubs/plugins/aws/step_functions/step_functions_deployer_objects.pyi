######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.018977                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.aws.step_functions.step_functions_deployer_objects
    import metaflow.runner.deployer

from .step_functions import StepFunctions as StepFunctions
from ....runner.deployer import DeployedFlow as DeployedFlow
from ....runner.deployer import TriggeredRun as TriggeredRun
from ....runner.utils import get_lower_level_group as get_lower_level_group
from ....runner.utils import handle_timeout as handle_timeout
from ....runner.utils import temporary_fifo as temporary_fifo

class StepFunctionsTriggeredRun(metaflow.runner.deployer.TriggeredRun, metaclass=type):
    """
    A class representing a triggered AWS Step Functions state machine execution.
    """
    def terminate(self, **kwargs) -> bool:
        """
        Terminate the running state machine execution.
        
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
    ...

class StepFunctionsDeployedFlow(metaflow.runner.deployer.DeployedFlow, metaclass=metaflow.runner.deployer.DeployedFlowMeta):
    """
    A class representing a deployed AWS Step Functions state machine.
    """
    @classmethod
    def from_deployment(cls, identifier: str, metadata: typing.Optional[str] = None):
        """
        This method is not currently implemented for Step Functions.
        
        Raises
        ------
        NotImplementedError
            This method is not implemented for Step Functions.
        """
        ...
    @property
    def production_token(self: metaflow.runner.deployer.DeployedFlow) -> typing.Optional[str]:
        """
        Get the production token for the deployed flow.
        
        Returns
        -------
        str, optional
            The production token, None if it cannot be retrieved.
        """
        ...
    def list_runs(self, states: typing.Optional[typing.List[str]] = None) -> typing.List[metaflow.plugins.aws.step_functions.step_functions_deployer_objects.StepFunctionsTriggeredRun]:
        """
        List runs of the deployed flow.
        
        Parameters
        ----------
        states : List[str], optional, default None
            A list of states to filter the runs by. Allowed values are:
            RUNNING, SUCCEEDED, FAILED, TIMED_OUT, ABORTED.
            If not provided, all states will be considered.
        
        Returns
        -------
        List[StepFunctionsTriggeredRun]
            A list of TriggeredRun objects representing the runs of the deployed flow.
        
        Raises
        ------
        ValueError
            If any of the provided states are invalid or if there are duplicate states.
        """
        ...
    def delete(self, **kwargs) -> bool:
        """
        Delete the deployed state machine.
        
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
    def trigger(self, **kwargs) -> StepFunctionsTriggeredRun:
        """
        Trigger a new run for the deployed flow.
        
        Parameters
        ----------
        **kwargs : Any
            Additional arguments to pass to the trigger command,
            `Parameters` in particular
        
        Returns
        -------
        StepFunctionsTriggeredRun
            The triggered run instance.
        
        Raises
        ------
        Exception
            If there is an error during the trigger process.
        """
        ...
    ...

