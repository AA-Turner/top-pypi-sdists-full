import functools
from typing import Optional

from metaflow import current
from metaflow.decorators import StepDecorator

from .s3_proxy_manager import S3ProxyManager
from .exceptions import S3ProxyException
from .constants import S3_PROXY_WRITE_MODES


class S3ProxyDecorator(StepDecorator):
    """
    S3 Proxy decorator for routing S3 requests through a local proxy service.

    Parameters
    ----------
    integration_name : str, optional
        Name of the S3 proxy integration. If not specified, will use the only
        available S3 proxy integration in the namespace (fails if multiple exist).
    write_mode : str, optional
        The desired behavior during write operations to target (origin) S3 bucket.
        allowed options are:
            "origin-and-cache" -> write to both the target S3 bucket and local object
                storage
            "origin" -> only write to the target S3 bucket
            "cache" -> only write to the object storage service used for caching
    debug : bool, optional
        Enable debug logging for proxy operations.
    """

    name = "s3_proxy"
    defaults = {
        "integration_name": None,
        "write_mode": None,
        "debug": False,
    }

    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        write_mode = self.attributes["write_mode"]
        if write_mode and write_mode not in S3_PROXY_WRITE_MODES:
            raise S3ProxyException(
                f"unexpected write_mode specified: {write_mode}. Allowed values are: {','.join(S3_PROXY_WRITE_MODES)}."
            )

        self.manager = S3ProxyManager(
            integration_name=self.attributes["integration_name"],
            write_mode=self.attributes["write_mode"],
            debug=self.attributes["debug"],
        )

        current._update_env({"s3_proxy": self.manager})

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
        """Setup S3 proxy before step execution"""
        self.manager.setup_proxy()

    def task_finished(
        self, step_name, flow, graph, is_task_ok, retry_count, max_retries
    ):
        """Cleanup S3 proxy after step execution"""
        if self.manager:
            self.manager.cleanup()


class NebiusS3ProxyDecorator(S3ProxyDecorator):
    """
    Nebius-specific S3 Proxy decorator for routing S3 requests through a local proxy service.
    It exists to make it easier for users to know that this decorator should only be used with
    a Neo Cloud like Nebius.
    """

    name = "nebius_s3_proxy"
    defaults = {
        "integration_name": None,
        "write_mode": None,
        "debug": False,
    }


class CoreWeaveS3ProxyDecorator(S3ProxyDecorator):
    """
    CoreWeave-specific S3 Proxy decorator for routing S3 requests through a local proxy service.
    It exists to make it easier for users to know that this decorator should only be used with
    a Neo Cloud like CoreWeave.
    """

    name = "coreweave_s3_proxy"
    defaults = {
        "integration_name": None,
        "write_mode": None,
        "debug": False,
    }
