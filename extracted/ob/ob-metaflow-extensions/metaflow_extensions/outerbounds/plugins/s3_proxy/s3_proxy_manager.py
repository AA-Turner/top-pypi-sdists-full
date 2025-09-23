import os
import json
import gzip
import sys
import time
import threading
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import requests

from .constants import (
    S3_PROXY_BINARY_URLS,
    DEFAULT_PROXY_PORT,
    DEFAULT_PROXY_HOST,
)
from metaflow.metaflow_config import AWS_SECRETS_MANAGER_DEFAULT_REGION
from .s3_proxy_api import S3ProxyApiClient
from .exceptions import S3ProxyException


class S3ProxyManager:
    def __init__(
        self,
        integration_name: Optional[str] = None,
        write_mode: Optional[str] = None,
        debug: bool = False,
    ):
        self.integration_name = integration_name
        self.write_mode = write_mode
        self.debug = debug
        self.process = None
        self.binary_path = None
        self.config_path = None
        self.api_client = S3ProxyApiClient()
        self.proxy_config = None

    def setup_proxy(self) -> Tuple[dict, int, str, str]:
        try:
            if self._is_running_in_kubernetes():
                config_data = self.api_client.fetch_s3_proxy_config(
                    self.integration_name
                )
                self.binary_path = self._download_binary()
                self.config_path = self._write_config_file(config_data)
                # In the new world where the binary is being called
                # before even the metaflow code exection starts,
                # so this implies a few important things:
                # 1, We start the actual proxy process via another python file that safely ships logs to mflog.
                # 2. We passback the right values to the metaflow step process via env vars.
                # 3. Metaflow step code relies on env vars to decide if clients need to have s3 proxy in them.
                self.process = self._start_proxy_process()

                user_code_proxy_config = self._setup_proxy_config(config_data)

                return_tuple = (
                    user_code_proxy_config,  # this is the config that will be used within the metaflow `step` code.
                    self.process.pid,  # This is the pid of the process that will jumpstart, monitor and ship logs to MFLOG for the proxy process
                    self.config_path,  # This is the path to the config that is derived from the integration. It contains the actual bucket path and name where external objects are stored.
                    self.binary_path,  # This is the path to the binary for the proxy.
                )
                # We return a tuple because these values need to be passed down to the metaflow step process where
                # it will handle thier removal gracefully after the step is finished.
                return return_tuple

            print(
                "[@s3_proxy] skipping s3-proxy set up because metaflow has not detected a Kubernetes environment"
            )
            raise S3ProxyException(
                "S3 proxy setup failed because metaflow has not detected a Kubernetes environment"
            )
        except Exception as e:
            if self.debug:
                print(f"[@s3_proxy] Setup failed: {e}")
            self.cleanup()
            raise

    def _is_running_in_kubernetes(self) -> bool:
        """Check if running inside a Kubernetes pod by checking for Kubernetes service account token."""
        return (
            os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token")
            and os.environ.get("KUBERNETES_SERVICE_HOST") is not None
        )

    def _download_binary(self) -> str:
        binary_path = Path("/tmp/s3-proxy")
        if binary_path.exists():
            if self.debug:
                print("[@s3_proxy] Binary already exists, skipping download")
            return str(binary_path.absolute())

        try:
            if self.debug:
                print("[@s3_proxy] Downloading binary...")

            from platform import machine

            arch = machine()
            if arch not in S3_PROXY_BINARY_URLS:
                raise S3ProxyException(
                    f"unsupported platform architecture: {arch}. Please reach out to your Outerbounds Support team for more help."
                )

            response = requests.get(S3_PROXY_BINARY_URLS[arch], stream=True, timeout=60)
            response.raise_for_status()

            with open(binary_path, "wb") as f:
                with gzip.GzipFile(fileobj=response.raw) as gz:
                    f.write(gz.read())

            binary_path.chmod(0o755)

            if self.debug:
                print("[@s3_proxy] Binary downloaded successfully")

            return str(binary_path.absolute())

        except Exception as e:
            if self.debug:
                print(f"[@s3_proxy] Binary download failed: {e}")
            raise S3ProxyException(f"Failed to download S3 proxy binary: {e}")

    def _write_config_file(self, config_data) -> str:
        config_path = Path("/tmp/s3-proxy-config.json")

        proxy_config = {
            "bucketName": config_data.bucket_name,
            "endpointUrl": config_data.endpoint_url,
            "accessKeyId": config_data.access_key_id,
            "accessKeySecret": config_data.secret_access_key,
            "region": config_data.region,
        }

        config_path.write_text(json.dumps(proxy_config, indent=2))

        if self.debug:
            print(f"[@s3_proxy] Config written to {config_path}")

        return str(config_path.absolute())

    def _start_proxy_process(self) -> subprocess.Popen:
        # This command will jump start a process that will then call the proxy binary
        # The reason we do something like this is because we need to run all of this before
        # even the `step` command is called. So we need a python process that will ship the logs
        # of the proxy process to MFLOG instead of setting print statements. We need this process
        # to run independently since the S3ProxyManager gets called in the boostrap_proxy which will
        # exit after jump starting the proxy process.
        cmd = [self.binary_path, "--bucket-config", self.config_path, "serve"]
        _env = os.environ.copy()
        _env["S3_PROXY_BINARY_COMMAND"] = " ".join(cmd)
        if self.debug:
            _env["S3_PROXY_BINARY_DEBUG"] = "True"
        _cmd = [
            sys.executable,
            "-m",
            "metaflow_extensions.outerbounds.plugins.s3_proxy.binary_caller",
        ]
        devnull = subprocess.DEVNULL
        process = subprocess.Popen(
            _cmd,
            stdout=devnull,
            stderr=devnull,
            text=True,
            start_new_session=True,
            env=_env,
        )
        time.sleep(3)

        if process.poll() is None:
            if self.debug:
                print(f"[@s3_proxy] Proxy started successfully (pid: {process.pid})")

            return process
        else:
            stdout_data, stderr_data = process.communicate()
            if self.debug:
                print(f"[@s3_proxy] Proxy failed to start - output: {stdout_data}")
            raise S3ProxyException(f"S3 proxy failed to start: {stdout_data}")

    def _setup_proxy_config(self, config_data):
        from metaflow.metaflow_config import AWS_SECRETS_MANAGER_DEFAULT_REGION

        region = os.environ.get(
            "METAFLOW_AWS_SECRETS_MANAGER_DEFAULT_REGION",
            AWS_SECRETS_MANAGER_DEFAULT_REGION,
        )

        proxy_config = {
            "endpoint_url": f"http://{DEFAULT_PROXY_HOST}:{DEFAULT_PROXY_PORT}",
            "region": region,
            "bucket_name": config_data.bucket_name,
            "active": True,
        }

        if self.write_mode:
            proxy_config["write_mode"] = self.write_mode

        self.proxy_config = proxy_config
        return proxy_config

    def cleanup(self):
        try:
            from metaflow_extensions.outerbounds.toplevel.global_aliases_for_metaflow_package import (
                clear_s3_proxy_config,
            )

            clear_s3_proxy_config()

            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait(timeout=5)
                if self.debug:
                    print("[@s3_proxy] Proxy process stopped")

                from os import remove

                remove(self.config_path)
                remove(self.binary_path)

        except Exception as e:
            if self.debug:
                print(f"[@s3_proxy] Cleanup error: {e}")
        finally:
            self.proxy_config = None
