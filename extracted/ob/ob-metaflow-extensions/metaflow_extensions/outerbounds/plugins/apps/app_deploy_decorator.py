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

    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        self.logger = logger
        self.environment = environment
        self.step = step
        self.flow_datastore = flow_datastore

    def _resolve_package_url_and_sha(self):
        return os.environ.get("METAFLOW_CODE_URL", self.package_url), os.environ.get(
            "METAFLOW_CODE_SHA", self.package_sha
        )

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
        default_name = "-".join(current.pathspec.split("/")).lower()
        image = os.environ.get("FASTBAKERY_IMAGE", None)

        hash_key = hashlib.sha256(package_url.encode()).hexdigest()[:6]

        default_name = (
            (current.flow_name + "-" + current.step_name)[:12] + "-" + hash_key
        ).lower()

        AppDeployer._set_state(
            perimeter,
            api_server,
            code_package_url=package_url,
            code_package_key=package_sha,
            name=default_name,
            image=image,
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
