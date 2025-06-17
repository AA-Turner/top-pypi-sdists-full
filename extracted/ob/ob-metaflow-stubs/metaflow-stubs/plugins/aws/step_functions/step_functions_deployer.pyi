######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.949237                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.runner.deployer_impl
    import typing
    import metaflow.plugins.aws.step_functions.step_functions_deployer_objects

from ....runner.deployer_impl import DeployerImpl as DeployerImpl

TYPE_CHECKING: bool

class StepFunctionsDeployer(metaflow.runner.deployer_impl.DeployerImpl, metaclass=type):
    """
    Deployer implementation for AWS Step Functions.
    
    Parameters
    ----------
    name : str, optional, default None
        State Machine name. The flow name is used instead if this option is not specified.
    """
    def __init__(self, deployer_kwargs: typing.Dict[str, str], **kwargs):
        """
        Initialize the StepFunctionsDeployer.
        
        Parameters
        ----------
        deployer_kwargs : Dict[str, str]
            The deployer-specific keyword arguments.
        **kwargs : Any
            Additional arguments to pass to the superclass constructor.
        """
        ...
    @property
    def deployer_kwargs(self) -> typing.Dict[str, typing.Any]:
        ...
    @staticmethod
    def deployed_flow_type() -> typing.Type["metaflow.plugins.aws.step_functions.step_functions_deployer_objects.StepFunctionsDeployedFlow"]:
        ...
    def create(self, **kwargs) -> "metaflow.plugins.aws.step_functions.step_functions_deployer_objects.StepFunctionsDeployedFlow":
        """
        Create a new AWS Step Functions State Machine deployment.
        
        Parameters
        ----------
        authorize : str, optional, default None
            Authorize using this production token. Required when re-deploying an existing flow
            for the first time. The token is cached in METAFLOW_HOME.
        generate_new_token : bool, optional, default False
            Generate a new production token for this flow. Moves the production flow to a new namespace.
        given_token : str, optional, default None
            Use the given production token for this flow. Moves the production flow to the given namespace.
        tags : List[str], optional, default None
            Annotate all objects produced by AWS Step Functions runs with these tags.
        user_namespace : str, optional, default None
            Change the namespace from the default (production token) to the given tag.
        only_json : bool, optional, default False
            Only print out JSON sent to AWS Step Functions without deploying anything.
        max_workers : int, optional, default 100
            Maximum number of parallel processes.
        workflow_timeout : int, optional, default None
            Workflow timeout in seconds.
        log_execution_history : bool, optional, default False
            Log AWS Step Functions execution history to AWS CloudWatch Logs log group.
        use_distributed_map : bool, optional, default False
            Use AWS Step Functions Distributed Map instead of Inline Map for defining foreach
            tasks in Amazon State Language.
        deployer_attribute_file : str, optional, default None
            Write the workflow name to the specified file. Used internally for Metaflow's Deployer API.
        
        Returns
        -------
        StepFunctionsDeployedFlow
            The Flow deployed to AWS Step Functions.
        """
        ...
    ...

