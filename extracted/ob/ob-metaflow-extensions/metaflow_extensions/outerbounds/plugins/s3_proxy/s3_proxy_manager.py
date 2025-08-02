import os
import json
import gzip
import time
import threading
import subprocess
from pathlib import Path
from typing import Optional

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

    def setup_proxy(self) -> bool:
        try:
            if self._is_running_in_kubernetes():
                config_data = self.api_client.fetch_s3_proxy_config(
                    self.integration_name
                )
                self.binary_path = self._download_binary()
                self.config_path = self._write_config_file(config_data)
                self.process = self._start_proxy_process()
                self._setup_proxy_config(config_data)
                return True

            print(
                "[@s3_proxy] skipping s3-proxy set up because metaflow has not detected a Kubernetes environment"
            )
            return False
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
        cmd = [self.binary_path, "--bucket-config", self.config_path, "serve"]

        if self.debug:
            print(f"[@s3_proxy] Starting proxy: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout
            text=True,
            start_new_session=True,
        )

        self._setup_log_streaming(process)

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

    def _setup_log_streaming(self, process: subprocess.Popen):
        def stream_logs():
            try:
                # Read stdout line by line (stderr is redirected to stdout)
                while True:
                    line = process.stdout.readline()
                    if not line:
                        # Process has ended
                        break
                    line = line.strip()
                    if line and self.debug:
                        print(f"[@s3_proxy] {line}")

            except Exception as e:
                if self.debug:
                    print(f"[@s3_proxy] Log streaming error: {e}")

        log_thread = threading.Thread(target=stream_logs, daemon=True)
        log_thread.start()

    def _setup_proxy_config(self, config_data):
        from metaflow_extensions.outerbounds.toplevel.global_aliases_for_metaflow_package import (
            set_s3_proxy_config,
        )
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

        set_s3_proxy_config(proxy_config)
        self.proxy_config = proxy_config

        if self.debug:
            print("[@s3_proxy] Global S3 proxy configuration activated")

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
