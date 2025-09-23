import os
import functools
import json
import signal
import time
from typing import Dict, List, Optional, Tuple

from metaflow import current
from metaflow.decorators import StepDecorator
from .exceptions import S3ProxyException
from .constants import S3_PROXY_WRITE_MODES
from collections import namedtuple

S3ProxyBinaryConfig = namedtuple(
    "S3ProxyBinaryConfig", ["integration_name", "write_mode", "debug"]
)


def monkey_patch_environment(
    environment, step_name_and_deco_attrs: Dict[str, S3ProxyBinaryConfig]
):
    wrapping_func = environment.bootstrap_commands

    @functools.wraps(wrapping_func)
    def wrapper(step_name, ds_type, *args):
        base_boostrap_cmd = wrapping_func(step_name, ds_type, *args)
        additional_cmd = []

        if step_name in step_name_and_deco_attrs:
            integration_name = step_name_and_deco_attrs[step_name].integration_name
            write_mode = step_name_and_deco_attrs[step_name].write_mode
            debug = step_name_and_deco_attrs[step_name].debug
            additional_cmd = [
                "echo 'Setting up the S3 proxy.'",
                f"python -m metaflow_extensions.outerbounds.plugins.s3_proxy.proxy_bootstrap bootstrap --integration-name {integration_name} --write-mode {write_mode} --debug {debug} --uc-proxy-cfg-write-path ./.uc_proxy_cfg_file --proxy-status-write-path ./.proxy_status_file",
                "export METAFLOW_S3_PROXY_USER_CODE_CONFIG=$(cat ./.uc_proxy_cfg_file)",
                "export METAFLOW_S3_PROXY_STATUS=$(cat ./.proxy_status_file)",
                "export METAFLOW_S3_PROXY_SETUP_SUCCESS=True",
                "flush_mflogs",
            ]
        return base_boostrap_cmd + additional_cmd

    environment.bootstrap_commands = wrapper


class S3ProxyDecorator(StepDecorator):
    """
    Set up an S3 proxy that caches objects in an external, S3‑compatible bucket
    for S3 read and write requests.

    This decorator requires an integration in the Outerbounds platform that
    points to an external bucket. It affects S3 operations performed via
    Metaflow's `get_aws_client` and `S3` within a `@step`.

    Read operations
    ---------------
    All read operations pass through the proxy. If an object does not already
    exist in the external bucket, it is cached there. For example, if code reads
    from buckets `FOO` and `BAR` using the `S3` interface, objects from both
    buckets are cached in the external bucket.

    During task execution, all S3‑related read requests are routed through the
    proxy:
        - If the object is present in the external object store, the proxy
          streams it directly from there without accessing the requested origin
          bucket.
        - If the object is not present in the external storage, the proxy
          fetches it from the requested bucket, caches it in the external
          storage, and streams the response from the origin bucket.

    Warning
    -------
    All READ operations (e.g., GetObject, HeadObject) pass through the external
    bucket regardless of the bucket specified in user code. Even
    `S3(run=self)` and `S3(s3root="mybucketfoo")` requests go through the
    external bucket cache.

    Write operations
    ----------------
    Write behavior is controlled by the `write_mode` parameter, which determines
    whether writes also persist objects in the cache.

    `write_mode` values:
        - `origin-and-cache`: objects are written both to the cache and to their
          intended origin bucket.
        - `origin`: objects are written only to their intended origin bucket.

    Parameters
    ----------
    integration_name : str, optional
        [Outerbounds integration name](https://docs.outerbounds.com/outerbounds/configuring-secrets/#integrations-view)
        that holds the configuration for the external, S3‑compatible object
        storage bucket. If not specified, the only available S3 proxy
        integration in the namespace is used (fails if multiple exist).
    write_mode : str, optional
        Controls whether writes also go to the external bucket.
            - `origin` (default)
            - `origin-and-cache`
    debug : bool, optional
        Enables debug logging for proxy operations.
    """

    name = "s3_proxy"
    defaults = {
        "integration_name": None,
        "write_mode": None,
        "debug": False,
    }

    _environment_patched = False

    _proxy_status = None

    @classmethod
    def patch_environment(cls, flow, environment):
        """
        We need to patch the environment boostrap command so that
        we can launch the s3 proxy before the step code execution.
        We also want to ensure that we are running the proxy bootstrap
        only for the steps that have the decorator set. This is why we pass down all
        the step names that will change the boostrap commands.
        """
        if cls._environment_patched:
            return

        steps_with_s3_proxy = [
            step
            for step in flow
            if any(deco.name == "s3_proxy" for deco in step.decorators)
        ]
        if len(steps_with_s3_proxy) == 0:  # weird but y not?
            return

        step_names_and_deco_attrs = {}
        for s in steps_with_s3_proxy:
            _decos = [x for x in s.decorators if x.name == "s3_proxy"]
            deco = _decos[0]
            step_names_and_deco_attrs[s.name] = S3ProxyBinaryConfig(
                integration_name=deco.attributes["integration_name"],
                write_mode=deco.attributes["write_mode"],
                debug=deco.attributes["debug"],
            )

        monkey_patch_environment(environment, step_names_and_deco_attrs)
        cls._environment_patched = True

    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        write_mode = self.attributes["write_mode"]
        if write_mode and write_mode not in S3_PROXY_WRITE_MODES:
            raise S3ProxyException(
                f"unexpected write_mode specified: {write_mode}. Allowed values are: {','.join(S3_PROXY_WRITE_MODES)}."
            )

        self.patch_environment(flow, environment)
        if (
            os.environ.get("METAFLOW_S3_PROXY_USER_CODE_CONFIG")
            and os.environ.get("METAFLOW_S3_PROXY_STATUS")
            and self.attributes["debug"]
        ):
            print("[@s3_proxy] S3 Proxy detected. Debug mode is enabled.")

        if os.environ.get("METAFLOW_S3_PROXY_STATUS"):
            proxy_status = json.loads(os.environ.get("METAFLOW_S3_PROXY_STATUS"))
            self._proxy_status = proxy_status

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
        pass

    def task_finished(
        self, step_name, flow, graph, is_task_ok, retry_count, max_retries
    ):
        if not self._proxy_status:
            return

        status = self._proxy_status
        proxy_pid = status.get("proxy_pid")
        config_path = status.get("config_path")
        binary_path = status.get("binary_path")

        # 1) Stop processes: try to terminate the process group for clean child shutdown
        if proxy_pid:
            try:
                pgid = os.getpgid(proxy_pid)
                os.killpg(pgid, signal.SIGTERM)
                time.sleep(1)
            except Exception:
                # Fall back to killing the pid directly if pgid is unavailable
                try:
                    os.kill(proxy_pid, signal.SIGTERM)
                except Exception:
                    pass

        # 2) Clear files based on status
        for path in (config_path, binary_path):
            try:
                if path and os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass


class NebiusS3ProxyDecorator(S3ProxyDecorator):

    __doc__ = (
        """
    `@nebius_s3_proxy` is a Nebius-specific S3 Proxy decorator for routing S3 requests through a local proxy service.
    It exists to make it easier for users to know that this decorator should only be used with
    a Neo Cloud like Nebius. The underlying mechanics of the decorator is the same as the `@s3_proxy`:\n
    """
        + S3ProxyDecorator.__doc__
    )

    name = "nebius_s3_proxy"
    defaults = {
        "integration_name": None,
        "write_mode": None,
        "debug": False,
    }


class CoreWeaveS3ProxyDecorator(S3ProxyDecorator):
    __doc__ = (
        """
    `@coreweave_s3_proxy` is a CoreWeave-specific S3 Proxy decorator for routing S3 requests through a local proxy service.
    It exists to make it easier for users to know that this decorator should only be used with
    a Neo Cloud like CoreWeave. The underlying mechanics of the decorator is the same as the `@s3_proxy`:\n
    """
        + S3ProxyDecorator.__doc__
    )

    name = "coreweave_s3_proxy"
    defaults = {
        "integration_name": None,
        "write_mode": None,
        "debug": False,
    }
