
from typing import Any, Dict, List, Optional
from code_loader.experiment_api.epoch import Epoch
from code_loader.experiment_api.api import Api, SetExperimentPropertiesRequest, InitExperimentRequest
from code_loader.experiment_api.experiment_context import ExperimentContext
from code_loader.experiment_api.types import Metrics
from code_loader.experiment_api.workingspace_config_utils import load_workspace_config
from code_loader.experiment_api.utils import generate_experiment_name
from code_loader.experiment_api.client import  Client

        
class Experiment:
    """
    Represents an experiment in the system.

    Attributes:
        ctx (ExperimentContext): The context of the experiment, including API client and identifiers.
        default_epoch_tag (str): The default tag for epochs. Defaults to 'latest'.
    """

    def __init__(self, ctx: ExperimentContext, default_epoch_tag: str = 'latest'):
        """
        Initializes the Experiment instance.

        Args:
            ctx (ExperimentContext): The context of the experiment.
            default_epoch_tag (str): The default tag for epochs. Defaults to 'latest'.
        """
        self.ctx = ctx
        self.default_epoch_tag = default_epoch_tag

    def init_epoch(self, epoch: int) -> Epoch:
        """
        Initializes a new epoch for the experiment.

        Args:
            epoch (int): The epoch number to initialize.

        Returns:
            Epoch: An instance of the Epoch class.
        """
        return Epoch(self.ctx, epoch, self.default_epoch_tag)
    
    def log_epoch(self, epoch: int, metrics: Optional[Metrics] = None, model_path: Optional[str] = None, tags: Optional[List[str]] = None, override: bool = False) -> None:
        """
        Logs an epoch with optional metrics, model path, and tags.

        Args:
            epoch (int): The epoch number to log.
            metrics (Optional[Metrics]): The metrics to log for the epoch. Defaults to None.
            model_path (Optional[str]): The path to the model file. Defaults to None.
            tags (Optional[List[str]]): A list of tags to associate with the epoch model. Will always include the default tag. Unless the default tag is set to '', all previous epoch model with the same tag will be removed.
            override (bool): Whether to override the epoch if it already exists. Defaults to False.
        """
        epoch_o = self.init_epoch(epoch)
        if metrics is not None:
            epoch_o.set_metrics(metrics)
        epoch_o.log(model_path, tags, override)

    def set_properties(self, properties: Dict[str, Any]) -> None:
        """
        Sets properties for the experiment.

        Args:
            properties (Dict[str, Any]): A dictionary of properties to set for the experiment.
        """
        print(f"Setting experiment({self.ctx.experiment_id}) properties")
        self.ctx.api.set_experiment_properties(SetExperimentPropertiesRequest(
            experimentId=self.ctx.experiment_id,
            projectId=self.ctx.project_id,
            properties=properties
        ))
    
def init_experiment(
        experiment_name: Optional[str] = None, 
        description: str = "", 
        project_name: Optional[str] = None,
        code_integration_name: Optional[str] = None,
        working_dir: Optional[str] = None,
        client: Optional[Client] = None,
        default_epoch_tag: str = 'latest',
        ) -> 'Experiment':
    """
    Initializes and starts a new experiment.

    Args:
        experiment_name (Optional[str]): The name of the experiment. If not provided, a name will be generated.
            Example generated names:
            - Bold Crimson Serpent
            - Brave Sun Raven
            - Griffin of the Pearl Wings
        description (str): A description of the experiment.
        project_name (Optional[str]): The name of the project. If it does not exist, a new project will be created. If not provided, the project ID is loaded from the workspace config.
        code_integration_name (Optional[str]): The name of the code integration.
        working_dir (Optional[str]): The working directory. If not provided, the current directory is used.
            The working directory should contain a leap.yaml file with the project ID and optionally the code integration ID.
            This configuration is used if the project name is not provided.
        client (Optional[Client]): The client to use for the experiment. If not provided, the client will be taken from the leap CLI configuration.
            Ensure that the user has initialized the authentication by running `leap auth [url] [token]`.
        default_epoch_tag (str): The default tag to use for epoch model. Default is 'latest', set to '' for no default tag.

    Returns:
        Experiment: An instance of the Experiment class.

    Raises:
        Exception: If the project name is not supplied and no workspace config is found or the project ID is missing from the leap.yaml file.
        Exception: If the client is not supplied and the user has not initialized the authentication by running `leap auth [url] [token]`.
    """
    if client is None:
        client = Client()
    
    if experiment_name is None:
        experiment_name = generate_experiment_name()
        print(f"Experiment name not provided, generated name: {experiment_name}")


    api = Api(client)
    project_id: Optional[str] = None
    code_integration_id: Optional[str] = None

    if not project_name:
        workspace_config = load_workspace_config(working_dir)
        if workspace_config is None or workspace_config.projectId is None:
            raise Exception("No leap workspace config found or projectId is missing, make sure you are in a leap workspace directory or provide a working_dir")
        project_id = workspace_config.projectId
        code_integration_id = workspace_config.codeIntegrationId

    result = api.init_experiment(InitExperimentRequest(
        projectId=project_id,
        experimentName=experiment_name,
        description=description,
        codeIntegrationId=code_integration_id,
        codeIntegrationName=code_integration_name,
        projectName=project_name
    ))
    if result.isCreatedProject:
        print(f"Project name: {project_name} not found, created a new one with id: {result.projectId}")
    ctx = ExperimentContext(api, result.projectId, result.versionId, result.experimentId)
    return Experiment(ctx, default_epoch_tag)
