######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.29.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-05-12T17:11:58.030700                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators
    import metaflow.user_decorators.user_flow_decorator
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config

from ......exception import MetaflowException as MetaflowException
from ......user_decorators.user_flow_decorator import FlowMutator as FlowMutator
from ......metaflow_current import current as current
from .deployer import AppDeployer as AppDeployer
from .deployer import DeployedApp as DeployedApp
from .config.unified_config import PackagedCode as PackagedCode
from .perimeters import PerimeterExtractor as PerimeterExtractor

KUBERNETES_CONTAINER_IMAGE: None

def scale_down_apps_on_exit(run):
    ...

def delete_apps_on_exit(run):
    ...

class app_deploy(metaflow.user_decorators.user_flow_decorator.FlowMutator, metaclass=metaflow.user_decorators.user_flow_decorator.FlowMutatorMeta):
    """
    Simplify bookkeeping and lifecycle management for apps deployed from Metaflow flows.
    
    While you can deploy apps from within a flow using the `AppDeployer` API directly,
    doing so at scale introduces operational challenges: tracking which apps belong to
    which run, cleaning up apps when flows complete or fail, and discovering apps
    deployed across many runs. This decorator addresses these concerns automatically.
    
    When applied to a flow, `@app_deploy` provides:
    
    1. **Automatic Tagging**: Every app deployed gains Metaflow metadata tags
       (flow name, run ID, step, task ID, project/branch info) enabling easy
       discovery and association with specific flow executions.
    
    2. **Lifecycle Management**: Configure automatic cleanup policies to scale down
       or delete apps when the flow exits (on success or failure), preventing
       orphaned apps from accumulating.
    
    3. **Convenient Access**: Exposes `current.apps` with the flow's code package
       and container image, plus a `list()` method to discover all apps deployed
       in the current run.
    
    Parameters
    ----------
    cleanup_policy : str, default "none"
        Action to perform on all apps deployed in this run when the flow exits:
        - "none": No cleanup; apps remain running after flow completion.
        - "scale_down": Scale all deployed apps to zero replicas.
        - "delete": Delete all deployed apps.
    
    Examples
    --------
    
    ```python
    from metaflow import FlowSpec, step, current, app_deploy
    from metaflow.apps import AppDeployer
    
    @app_deploy
    class MyFlow(FlowSpec):
    
        @step
        def start(self):
            # Deploy an app using the flow's code package
            deployer = AppDeployer(
                name="my-service",
                port=8000,
                image=current.apps.current_image,
                code_package=current.apps.metaflow_code_package,
                commands=["python server.py"],
            )
            self.app = deployer.deploy()
            self.next(self.end)
    
        @step
        def end(self):
            # List all apps deployed in this run
            apps = current.apps.list()
            print(f"Deployed {len(apps)} app(s)")
    ```
    
    With cleanup policy to prevent orphaned apps:
    
    ```python
    @app_deploy(cleanup_policy="scale_down")
    class MyFlow(FlowSpec):
        # Apps will be scaled to zero when flow completes or fails,
        # preventing resource waste from forgotten deployments
        ...
    ```
    """
    def init(self, *args, **kwargs):
        ...
    def pre_mutate(self, mutable_flow):
        ...
    def mutate(self, mutable_flow):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

class AppDeployInternalDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    MF Add To Current
    -----------------
    apps -> metaflow_extensions.outerbounds.plugins.apps.core.app_deploy_decorator.FlowAppManager
    
        @@ Returns
        ----------
        FlowAppManager
    """
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_post_step(self, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    def runtime_init(self, flow, graph, package, run_id):
        ...
    def runtime_task_created(self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context):
        ...
    ...

class FlowAppManager(object, metaclass=type):
    """
    Manager for apps deployed within a Metaflow flow execution.
    
    Accessible via `current.apps` when using the `@app_deploy` decorator.
    Provides access to the flow's code package, container image, and
    methods to list apps deployed in the current run.
    
    Attributes
    ----------
    metaflow_code_package : PackagedCode
        The code package for the current flow, ready to use with AppDeployer.
    current_image : str
        The container image used by the current task (from fast_bakery or similar).
    default_image : str
        The default Kubernetes container image from Metaflow config.
    
    Examples
    --------
    
    ```python
    # python myflow.py --environment=fast-bakery run --with kubernetes
    from metaflow.apps import AppDeployer
    
    @pypi(packages={"flask": ">=2.0", "requests": ">=2.28"})
    @step
    def deploy_step(self):
        image = current.apps.current_image
        if image is None:
            image = current.apps.default_image
        # Use the flow's code package directly
        deployer = AppDeployer(
            name="my-app",
            port=8000,
            image=image,
            code_package=current.apps.metaflow_code_package,
            commands=["python app.py"],
        )
        deployed = deployer.deploy()
    
        # List apps from this run
        apps = current.apps.list()
    ```
    """
    def __init__(self, flow_name: str, run_id: str, package: metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.PackagedCode, image: typing.Union[str, None] = None, default_image: typing.Union[str, None] = None):
        ...
    @property
    def metaflow_code_package(self) -> metaflow.mf_extensions.outerbounds.plugins.apps.core.config.unified_config.PackagedCode:
        """
        The flow's code package for use with AppDeployer.
        
        Returns
        -------
        PackagedCode
            A namedtuple with `url` and `key` fields pointing to the
            packaged metaflow's code package stored in the datastore.
        """
        ...
    @property
    def current_image(self) -> str:
        """
        The container image for the current task.
        
        Returns
        -------
        str
            Image URI from fast bakery image or None if not set.
        """
        ...
    @property
    def default_image(self) -> str:
        """
        The default Kubernetes container image from Metaflow config.
        
        Returns
        -------
        str
            The KUBERNETES_CONTAINER_IMAGE from Metaflow configuration.
        """
        ...
    def list(self) -> typing.List["DeployedApp"]:
        """
        List apps deployed in the current Metaflow run.
        
        Returns apps tagged with this flow's name and run ID.
        
        Returns
        -------
        List[DeployedApp]
            Apps deployed during this flow execution.
        
        Examples
        --------
        
        ```python
        apps = current.apps.list()
        for app in apps:
            print(f"{app.name}: {app.public_url}")
        ```
        """
        ...
    ...

