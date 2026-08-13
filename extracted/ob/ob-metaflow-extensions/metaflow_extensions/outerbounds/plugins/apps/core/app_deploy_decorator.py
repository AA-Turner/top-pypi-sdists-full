from typing import List, Optional
from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow.flowspec import FlowMutator
from metaflow import current
from metaflow.metaflow_config import KUBERNETES_CONTAINER_IMAGE
from .deployer import AppDeployer, DeployedApp, PackagedCode
from .perimeters import PerimeterExtractor
import os


# Valid cleanup policy values (internal use)
_CLEANUP_POLICIES = ("none", "scale_down", "delete")


def _fetch_current_run_apps(run) -> List[DeployedApp]:
    return AppDeployer.list_deployments(
        tags=[
            {"metaflow/run_id": run.id},
            {"metaflow/flow_name": run.parent.id},
        ]
    )


def scale_down_apps_on_exit(run):
    if run is None:
        print("No Apps to delete since run was None")
        return
    for app in _fetch_current_run_apps(run):
        try:
            app.scale_to_zero()
        except Exception as e:
            print("Failed to scale %s down to zero" % app.id, str(e))


def delete_apps_on_exit(run):
    if run is None:
        print("No Apps to delete since run was None")
        return
    for app in _fetch_current_run_apps(run):
        try:
            app.delete()
        except Exception as e:
            print("Failed to delete %s" % app.id, str(e))


class app_deploy(FlowMutator):
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
        cleanup_policy = kwargs.get("cleanup_policy", "none")
        if cleanup_policy not in _CLEANUP_POLICIES:
            raise MetaflowException(
                f"Invalid cleanup_policy '{cleanup_policy}'. "
                f"Must be one of: {', '.join(_CLEANUP_POLICIES)}"
            )
        self.cleanup_policy = cleanup_policy

    def pre_mutate(self, mutable_flow):
        # Add exit_hook for cleanup if cleanup_policy is not "none"
        hook = None
        if self.cleanup_policy == "delete":
            hook = delete_apps_on_exit.__name__
        elif self.cleanup_policy == "scale_down":
            hook = scale_down_apps_on_exit.__name__
        if hook is None:
            return
        # @exit_hook keeps only `fn.__name__` when handed a function object, and
        # the runner then looks that name up in the flow file -- where these
        # hooks do not live. A dotted import path is resolved by import instead,
        # so it survives the round trip out of this module.
        hook = "%s.%s" % (__name__, hook)
        mutable_flow.add_decorator(
            "exit_hook",
            deco_kwargs={
                "on_success": [hook],
                "on_error": [hook],
            },
        )

    def mutate(self, mutable_flow):
        for step_name, step in mutable_flow.steps:
            step.add_decorator(
                "app_deploy_internal",
                duplicates=step.IGNORE,
            )


class AppDeployInternalDecorator(StepDecorator):
    """
    MF Add To Current
    -----------------
    apps -> metaflow_extensions.outerbounds.plugins.apps.core.app_deploy_decorator.FlowAppManager

        @@ Returns
        ----------
        FlowAppManager
    """

    name = "app_deploy_internal"
    defaults = {}

    packaged_code = None

    package_url = None
    package_sha = None

    MAX_ENTROPY = 6
    MAX_NAME_LENGTH = 150

    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        self.logger = logger
        self.environment = environment
        self.step = step
        self.flow_datastore = flow_datastore

    def _resolve_package_url_and_sha(self):
        return os.environ.get("METAFLOW_CODE_URL", self.package_url), os.environ.get(
            "METAFLOW_CODE_SHA", self.package_sha
        )

    def _extract_project_info(self):
        project = current.get("project_name")
        branch = current.get("branch_name")
        is_production = current.get("is_production")
        return project, branch, is_production

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_user_code_retries,
        ubf_context,
        inputs,
    ):
        package_url, package_sha = self._resolve_package_url_and_sha()
        if package_url is None or package_sha is None:
            # TODO: Think through if we need this abstraction
            raise MetaflowException(
                "METAFLOW_CODE_URL or METAFLOW_CODE_SHA is not set. "
                "Please set METAFLOW_CODE_URL and METAFLOW_CODE_SHA in your environment."
            )
        self.packaged_code = PackagedCode(package_url, package_sha)

        perimeter, api_server = PerimeterExtractor.during_programmatic_access()
        config = PerimeterExtractor.config_during_programmatic_access()

        # Generally we DONT have the default image always present in the config
        # vars set to the Task. This is why its important to retrieve it so
        # that we can offer it to the user at runtime in the properties
        # displayed by current.
        default_image = config.get("METAFLOW_KUBERNETES_CONTAINER_IMAGE")
        # TODO: Currently we are only displaying fast bakery image
        # but we should be displaying the current image the task
        # is executing in. Which ever it maybe.
        current_fb_image = os.environ.get("FASTBAKERY_IMAGE", None)

        project, branch, is_production = self._extract_project_info()

        project_info = {}
        if project is not None:
            project_info["metaflow/project"] = project
            project_info["metaflow/branch"] = branch
            project_info["metaflow/is_production"] = is_production

        default_tags = {
            "metaflow/flow_name": flow.name,
            "metaflow/step_name": step_name,
            "metaflow/run_id": run_id,
            "metaflow/task_id": task_id,
            "metaflow/retry_count": retry_count,
            "metaflow/pathspec": current.pathspec,
            **project_info,
        }

        # Set state on AppDeployer using the new API
        AppDeployer._set_state("perimeter", perimeter)
        AppDeployer._set_state("api_url", api_server)
        AppDeployer._set_state(
            "default_tags", [{k: str(v)} for k, v in default_tags.items()]
        )

        current._update_env(
            {
                "apps": FlowAppManager(
                    flow.name,
                    run_id,
                    self.packaged_code,
                    current_fb_image,
                    default_image,
                )
            }
        )

    def task_post_step(
        self, step_name, flow, graph, retry_count, max_user_code_retries
    ):
        pass

    def runtime_init(self, flow, graph, package, run_id):
        # Set some more internal state.
        self.flow = flow
        self.graph = graph
        self.package = package
        self.run_id = run_id

    def runtime_task_created(
        self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context
    ):
        # To execute the Kubernetes job, the job container needs to have
        # access to the code package. We store the package in the datastore
        # which the pod is able to download as part of it's entrypoint.
        if not is_cloned:
            self._save_package_once(self.flow_datastore, self.package)

    @classmethod
    def _save_package_once(cls, flow_datastore, package):
        if cls.packaged_code is None:
            cls.package_url, cls.package_sha = flow_datastore.save_data(
                [package.blob], len_hint=1
            )[0]
            cls.packaged_code = PackagedCode(cls.package_url, cls.package_sha)
            os.environ["METAFLOW_CODE_URL"] = cls.package_url
            os.environ["METAFLOW_CODE_SHA"] = cls.package_sha


class FlowAppManager:
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

    def __init__(
        self,
        flow_name: str,
        run_id: str,
        package: PackagedCode,
        image: Optional[str] = None,
        default_image: Optional[str] = None,
    ) -> None:
        self._package = package
        self._image = image
        self._default_image = default_image
        self._runid = run_id
        self._flowname = flow_name

    @property
    def metaflow_code_package(self) -> PackagedCode:
        """
        The flow's code package for use with AppDeployer.

        Returns
        -------
        PackagedCode
            A namedtuple with `url` and `key` fields pointing to the
            packaged metaflow's code package stored in the datastore.
        """
        return self._package

    @property
    def current_image(self) -> str:
        """
        The container image for the current task.

        Returns
        -------
        str
            Image URI from fast bakery image or None if not set.
        """
        return self._image

    @property
    def default_image(self) -> str:
        """
        The default Kubernetes container image from Metaflow config.

        Returns
        -------
        str
            The KUBERNETES_CONTAINER_IMAGE from Metaflow configuration.
        """
        return self._default_image

    def list(self) -> List["DeployedApp"]:
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
        return AppDeployer.list_deployments(
            tags=[
                {"metaflow/run_id": self._runid},
                {"metaflow/flow_name": self._flowname},
            ]
        )
