import os
import sys

from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow.plugins.parallel_decorator import ParallelDecorator
from metaflow.metadata_provider.util import sync_local_metadata_to_datastore
from metaflow.metaflow_config import DATASTORE_LOCAL_DIR
from metaflow.sidecar import Sidecar
from metaflow.plugins.timeout_decorator import get_run_time_limit_for_task
from metaflow.metadata_provider import MetaDatum

from .utils import get_ngc_api_key
from .exceptions import (
    UnsupportedNvctDatastoreException,
    NvctTimeoutTooShortException,
    RequestedGPUTypeUnavailableException,
    UnsupportedNvctConfigurationException,
)


DEFAULT_GPU_TYPE = "H100"

SUPPORTABLE_GPU_TYPES = {
    "L40": [
        {
            "n_gpus": 1,
            "instance_type": "gl40_1.br20_2xlarge",
            "backend": "GFN",
        },
    ],
    "L40S": [
        {
            "n_gpus": 1,
            "instance_type": "gl40s_1.br25_2xlarge",
            "backend": "GFN",
        },
    ],
    "L40G": [
        {
            "n_gpus": 1,
            "instance_type": "gl40g_1.br25_2xlarge",
            "backend": "GFN",
        },
    ],
    "H100": [
        {
            "n_gpus": 1,
            "instance_type": "OCI.GPU.H100_1x",
            "backend": "nvcf-dgxc-k8s-oci-nrt-prd8",
        },
        {
            "n_gpus": 2,
            "instance_type": "OCI.GPU.H100_2x",
            "backend": "nvcf-dgxc-k8s-oci-nrt-prd8",
        },
        {
            "n_gpus": 4,
            "instance_type": "OCI.GPU.H100_4x",
            "backend": "nvcf-dgxc-k8s-oci-nrt-prd8",
        },
        {
            "n_gpus": 8,
            "instance_type": "OCI.GPU.H100_8x",
            "backend": "nvcf-dgxc-k8s-oci-nrt-prd8",
        },
    ],
    "NEBIUS_H100": [
        {
            "n_gpus": 1,
            "instance_type": "ON-PREM.GPU.H100_1x",
            "backend": "default-project-eu-north1",
        },
        {
            "n_gpus": 2,
            "instance_type": "ON-PREM.GPU.H100_2x",
            "backend": "default-project-eu-north1",
        },
        {
            "n_gpus": 4,
            "instance_type": "ON-PREM.GPU.H100_4x",
            "backend": "default-project-eu-north1",
        },
        {
            "n_gpus": 8,
            "instance_type": "ON-PREM.GPU.H100_8x",
            "backend": "default-project-eu-north1",
        },
    ],
}


class NvctDecorator(StepDecorator):

    """
    Specifies that this step should execute on DGX cloud.

    Parameters
    ----------
    gpu : int
        Number of GPUs to use.
    gpu_type : str
        Type of Nvidia GPU to use.
    """

    name = "nvct"
    defaults = {
        "gpu": 1,
        "gpu_type": None,
        "ngc_api_key": None,
        "instance_type": None,
        "backend": None,
    }

    package_url = None
    package_sha = None

    # Refer https://github.com/Netflix/metaflow/blob/master/docs/lifecycle.png
    # to understand where these functions are invoked in the lifecycle of a
    # Metaflow flow.
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        # Executing NVCT functions requires a non-local datastore.
        if flow_datastore.TYPE not in ("s3", "azure", "gs"):
            raise UnsupportedNvctDatastoreException(flow_datastore.TYPE)

        # Set internal state.
        self.logger = logger
        self.environment = environment
        self.step = step
        self.flow_datastore = flow_datastore

        if any([deco.name == "kubernetes" for deco in decos]):
            raise MetaflowException(
                "Step *{step}* is marked for execution both on Kubernetes and "
                "Nvct. Please use one or the other.".format(step=step)
            )
        if any([isinstance(deco, ParallelDecorator) for deco in decos]):
            raise MetaflowException(
                "Step *{step}* contains a @parallel decorator "
                "with the @nvct decorator. @parallel decorators are not currently supported with @nvct.".format(
                    step=step
                )
            )

        # Set run time limit for NVCT.
        self.run_time_limit = get_run_time_limit_for_task(decos)
        if self.run_time_limit < 60:
            raise NvctTimeoutTooShortException(step)

        self.attributes["ngc_api_key"] = get_ngc_api_key()

        requested_gpu_type = self.attributes["gpu_type"]
        requested_n_gpus = self.attributes["gpu"]

        if requested_gpu_type is None:
            requested_gpu_type = DEFAULT_GPU_TYPE
        if requested_gpu_type not in SUPPORTABLE_GPU_TYPES:
            raise RequestedGPUTypeUnavailableException(
                requested_gpu_type, list(SUPPORTABLE_GPU_TYPES.keys())
            )

        valid_config = None
        available_configurations = SUPPORTABLE_GPU_TYPES[requested_gpu_type]
        for each_config in available_configurations:
            if each_config["n_gpus"] == requested_n_gpus:
                valid_config = each_config
                break

        if valid_config is None:
            raise UnsupportedNvctConfigurationException(
                requested_n_gpus,
                requested_gpu_type,
                available_configurations,
                step,
            )

        self.attributes["instance_type"] = valid_config["instance_type"]
        self.attributes["gpu_type"] = requested_gpu_type
        if self.attributes["gpu_type"] == "NEBIUS_H100":
            self.attributes["gpu_type"] = "H100"
        self.attributes["backend"] = valid_config["backend"]

    def runtime_init(self, flow, graph, package, run_id):
        # Set some more internal state.
        self.flow = flow
        self.graph = graph
        self.package = package
        self.run_id = run_id

    def runtime_task_created(
        self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context
    ):
        if not is_cloned:
            self._save_package_once(self.flow_datastore, self.package)

    def runtime_step_cli(
        self, cli_args, retry_count, max_user_code_retries, ubf_context
    ):
        if retry_count <= max_user_code_retries:
            # after all attempts to run the user code have failed, we don't need
            # to execute on NVCF anymore. We can execute possible fallback
            # code locally.
            cli_args.commands = ["nvct", "step"]
            cli_args.command_args.append(self.package_sha)
            cli_args.command_args.append(self.package_url)
            cli_options = {
                "gpu_type": self.attributes["gpu_type"],
                "instance_type": self.attributes["instance_type"],
                "backend": self.attributes["backend"],
                "ngc_api_key": self.attributes["ngc_api_key"],
            }
            cli_args.command_options.update(cli_options)
            cli_args.entrypoint[0] = sys.executable

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
        max_retries,
        ubf_context,
        inputs,
    ):
        self.metadata = metadata
        self.task_datastore = task_datastore

        # task_pre_step may run locally if fallback is activated for @catch
        # decorator.

        if "NVCT_CONTEXT" in os.environ:
            meta = {}

            meta["nvct-task-id"] = os.environ.get("NVCT_TASK_ID")
            meta["nvct-task-name"] = os.environ.get("NVCT_TASK_NAME")
            meta["nvct-ncaid"] = os.environ.get("NVCT_NCA_ID")
            meta["nvct-progress-file-path"] = os.environ.get("NVCT_PROGRESS_FILE_PATH")
            meta["nvct-results-dir"] = os.environ.get("NVCT_RESULTS_DIR")

            entries = [
                MetaDatum(
                    field=k,
                    value=v,
                    type=k,
                    tags=["attempt_id:{0}".format(retry_count)],
                )
                for k, v in meta.items()
                if v is not None
            ]
            # Register book-keeping metadata for debugging.
            metadata.register_metadata(run_id, step_name, task_id, entries)

            self._save_logs_sidecar = Sidecar("save_logs_periodically")
            self._save_logs_sidecar.start()

    def task_finished(
        self, step_name, flow, graph, is_task_ok, retry_count, max_retries
    ):
        # task_finished may run locally if fallback is activated for @catch
        # decorator.
        if "NVCT_CONTEXT" in os.environ:
            # If `local` metadata is configured, we would need to copy task
            # execution metadata from the NVCT container to user's
            # local file system after the user code has finished execution.
            # This happens via datastore as a communication bridge.
            if hasattr(self, "metadata") and self.metadata.TYPE == "local":
                sync_local_metadata_to_datastore(
                    DATASTORE_LOCAL_DIR, self.task_datastore
                )

        try:
            self._save_logs_sidecar.terminate()
        except:
            # Best effort kill
            pass

    @classmethod
    def _save_package_once(cls, flow_datastore, package):
        if cls.package_url is None:
            cls.package_url, cls.package_sha = flow_datastore.save_data(
                [package.blob], len_hint=1
            )[0]
