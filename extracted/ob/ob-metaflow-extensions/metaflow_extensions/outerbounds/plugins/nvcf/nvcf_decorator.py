import os
import sys
import json
import requests
from urllib.parse import urlparse

from metaflow import current
from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow.plugins.parallel_decorator import ParallelDecorator
from metaflow.metadata_provider.util import sync_local_metadata_to_datastore
from metaflow.metaflow_config import DATASTORE_LOCAL_DIR
from metaflow.sidecar import Sidecar
from metaflow.plugins.timeout_decorator import get_run_time_limit_for_task
from metaflow.metadata_provider import MetaDatum
from metaflow.metaflow_config_funcs import init_config
from .constants import SUPPORTABLE_GPU_TYPES, DEFAULT_GPU_TYPE
from .exceptions import (
    RequestedGPUTypeUnavailableException,
    UnsupportedNvcfConfigurationException,
    UnsupportedNvcfDatastoreException,
    NvcfTimeoutTooShortException,
    NvcfQueueTimeoutTooShortException,
)

from metaflow.metaflow_config import SERVICE_URL


class NvcfDecorator(StepDecorator):

    """
    Specifies that this step should execute on DGX cloud.

    Parameters
    ----------
    gpu : int
        Number of GPUs to use.
    gpu_type : str
        Type of Nvidia GPU to use.
    queue_timeout : int
        Time to keep the job in NVCF's queue.
    """

    name = "nvidia"
    defaults = {
        "gpu": 1,
        "gpu_type": None,
        "queue_timeout": 5 * 24 * 3600,  # Default 5 days in seconds
    }

    package_url = None
    package_sha = None

    # Refer https://github.com/Netflix/metaflow/blob/master/docs/lifecycle.png
    # to understand where these functions are invoked in the lifecycle of a
    # Metaflow flow.
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        # Executing NVCF functions requires a non-local datastore.
        if flow_datastore.TYPE not in ("s3", "azure", "gs"):
            raise UnsupportedNvcfDatastoreException(flow_datastore.TYPE)

        # Set internal state.
        self.logger = logger
        self.environment = environment
        self.step = step
        self.flow_datastore = flow_datastore

        if any([deco.name == "kubernetes" for deco in decos]):
            raise MetaflowException(
                "Step *{step}* is marked for execution both on Kubernetes and "
                "Nvidia. Please use one or the other.".format(step=step)
            )
        if any([isinstance(deco, ParallelDecorator) for deco in decos]):
            raise MetaflowException(
                "Step *{step}* contains a @parallel decorator "
                "with the @nvidia decorator. @parallel decorators are not currently supported with @nvidia.".format(
                    step=step
                )
            )

        # Set run time limit for the NVCF function.
        self.run_time_limit = get_run_time_limit_for_task(decos)
        if self.run_time_limit < 60:
            raise NvcfTimeoutTooShortException(step)

        conf = init_config()
        if "OBP_AUTH_SERVER" in conf:
            auth_host = conf["OBP_AUTH_SERVER"]
        else:
            auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]

        # NOTE: reusing the same auth_host as the one used in NimMetadata,
        # however, user should not need to use nim container to use @nvidia.
        # May want to refactor this to a common endpoint.
        nim_info_url = "https://" + auth_host + "/generate/nim"

        if "METAFLOW_SERVICE_AUTH_KEY" in conf:
            headers = {"x-api-key": conf["METAFLOW_SERVICE_AUTH_KEY"]}
            res = requests.get(nim_info_url, headers=headers)
        else:
            headers = json.loads(os.environ.get("METAFLOW_SERVICE_HEADERS"))
            res = requests.get(nim_info_url, headers=headers)

        res.raise_for_status()
        self.attributes["ngc_api_key"] = res.json()["nvcf"]["api_key"]

        available_functions_info = res.json()["nvcf"]["functions"]
        requested_gpu_type = self.attributes["gpu_type"]
        n_gpu = self.attributes["gpu"]

        if requested_gpu_type is None:
            requested_gpu_type = DEFAULT_GPU_TYPE
        if requested_gpu_type not in SUPPORTABLE_GPU_TYPES:
            raise RequestedGPUTypeUnavailableException(requested_gpu_type)

        desired_configuration = (n_gpu, requested_gpu_type)
        available_configurations = {}
        for f in available_functions_info:
            if f["model_key"] == "metaflow_task_executor":
                available_configurations[(f["gpu"], f["gpu_type"])] = f["id"]

        if desired_configuration not in available_configurations:
            raise UnsupportedNvcfConfigurationException(
                n_gpu, requested_gpu_type, available_configurations, step
            )
        self.attributes["function_id"] = available_configurations[desired_configuration]

        queue_timeout = self.attributes["queue_timeout"]
        if not isinstance(queue_timeout, int) or queue_timeout < 60:
            raise NvcfQueueTimeoutTooShortException(step)

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
            cli_args.commands = ["nvidia", "step"]
            cli_args.command_args.append(self.package_sha)
            cli_args.command_args.append(self.package_url)
            cli_options = {
                "function_id": self.attributes["function_id"],
                "ngc_api_key": self.attributes["ngc_api_key"],
                "queue_timeout": self.attributes["queue_timeout"],
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

        if "NVCF_CONTEXT" in os.environ:
            meta = {}

            meta["nvcf-function-id"] = os.environ.get("NVCF_FUNCTION_ID")
            meta["nvcf-function-version-id"] = os.environ.get(
                "NVCF_FUNCTION_VERSION_ID"
            )
            meta["nvcf-region"] = os.environ.get("NVCF_REGION")
            meta["nvcf-ncaid"] = os.environ.get("NVCF_NCAID")
            meta["nvcf-sub"] = os.environ.get("NVCF_SUB")
            meta["nvcf-instancetype"] = os.environ.get("NVCF_INSTANCETYPE")
            meta["nvcf-reqid"] = os.environ.get("NVCF_REQID")
            meta["nvcf-env"] = os.environ.get("NVCF_ENV")
            meta["nvcf-backend"] = os.environ.get("NVCF_BACKEND")
            meta["nvcf-function-name"] = os.environ.get("NVCF_FUNCTION_NAME")
            meta["nvcf-nspectid"] = os.environ.get("NVCF_NSPECTID")

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
        if "NVCF_CONTEXT" in os.environ:
            # If `local` metadata is configured, we would need to copy task
            # execution metadata from the NVCF container to user's
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
