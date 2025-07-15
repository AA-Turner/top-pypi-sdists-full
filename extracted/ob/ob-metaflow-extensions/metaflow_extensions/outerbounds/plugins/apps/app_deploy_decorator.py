from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow import current
from .core import AppDeployer, apps
from .core.perimeters import PerimeterExtractor
import os
import hashlib


class AppDeployDecorator(StepDecorator):

    """
    MF Add To Current
    -----------------
    apps -> metaflow_extensions.outerbounds.plugins.apps.core.apps

        @@ Returns
        ----------
        apps
            The object carrying the Deployer class to deploy apps.
    """

    name = "app_deploy"
    defaults = {}

    package_url = None
    package_sha = None

    MAX_ENTROPY = 6
    MAX_NAME_LENGTH = 15 - MAX_ENTROPY - 1  # -1 for the hyphen

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

    def _resolve_default_image(self, flow):
        # TODO : Resolve the default image over here.
        pass

    def _resolve_default_name_prefix(self, flow, step_name):
        # TODO: Only tweek MAX_NAME_LENGTH as backend support allows longer names.
        base_prefix = (flow.name + "-" + step_name).lower()
        if len(base_prefix) > self.MAX_NAME_LENGTH:
            base_prefix = "mf-app"
        return base_prefix

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
        perimeter, api_server = PerimeterExtractor.during_metaflow_execution()
        package_url, package_sha = self._resolve_package_url_and_sha()
        if package_url is None or package_sha is None:
            raise MetaflowException(
                "METAFLOW_CODE_URL or METAFLOW_CODE_SHA is not set. "
                "Please set METAFLOW_CODE_URL and METAFLOW_CODE_SHA in your environment."
            )
        image = os.environ.get("FASTBAKERY_IMAGE", None)

        # TODO [Apps] - This is temporary. Backend will support longer names in the future.
        default_name = self._resolve_default_name_prefix(flow, step_name)
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

        AppDeployer._set_state(
            perimeter,
            api_server,
            code_package_url=package_url,
            code_package_key=package_sha,
            name_prefix=default_name,
            image=image,
            max_entropy=self.MAX_ENTROPY,
            default_tags=[{k: str(v)} for k, v in default_tags.items()],
        )
        current._update_env(
            {
                "apps": apps(),
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
        if cls.package_url is None:
            cls.package_url, cls.package_sha = flow_datastore.save_data(
                [package.blob], len_hint=1
            )[0]
            os.environ["METAFLOW_CODE_URL"] = cls.package_url
            os.environ["METAFLOW_CODE_SHA"] = cls.package_sha
