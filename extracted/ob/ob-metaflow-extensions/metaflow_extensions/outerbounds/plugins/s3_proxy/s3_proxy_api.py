import json
import time
from typing import Dict, Optional

from .exceptions import S3ProxyConfigException, S3ProxyApiException


class S3ProxyConfigResponse:
    def __init__(self, data: Dict):
        self.bucket_name = data.get("bucket_name")
        self.endpoint_url = data.get("endpoint_url")
        self.access_key_id = data.get("access_key_id")
        self.secret_access_key = data.get("secret_access_key")
        self.region = data.get("region")


class S3ProxyApiClient:
    def __init__(self):
        self.perimeter, self.integrations_url = self._get_api_configs()

    def _get_api_configs(self):
        from metaflow_extensions.outerbounds.remote_config import init_config
        from os import environ

        conf = init_config()
        perimeter = conf.get("OBP_PERIMETER") or environ.get("OBP_PERIMETER", "")
        integrations_url = conf.get("OBP_INTEGRATIONS_URL") or environ.get(
            "OBP_INTEGRATIONS_URL", ""
        )

        if not perimeter:
            raise S3ProxyConfigException(
                "No perimeter set. Please run `outerbounds configure` command."
            )

        if not integrations_url:
            raise S3ProxyConfigException(
                "No integrations URL set. Please contact your Outerbounds support team."
            )

        return perimeter, integrations_url

    def fetch_s3_proxy_config(
        self, integration_name: Optional[str] = None
    ) -> S3ProxyConfigResponse:
        url = f"{self.integrations_url}/s3proxy"

        payload = {"perimeter_name": self.perimeter}
        if integration_name:
            payload["integration_name"] = integration_name

        headers = {"Content-Type": "application/json"}

        try:
            from metaflow.metaflow_config import SERVICE_HEADERS

            headers.update(SERVICE_HEADERS or {})
        except ImportError:
            pass

        response = self._make_request(url, headers, payload)
        return S3ProxyConfigResponse(response)

    def _make_request(self, url: str, headers: Dict, payload: Dict) -> Dict:
        from metaflow_extensions.outerbounds.plugins.secrets.secrets import (
            _api_server_get,
        )

        retryable_status_codes = [409]
        json_payload = json.dumps(payload)

        for attempt in range(3):
            response = _api_server_get(
                url, data=json_payload, headers=headers, conn_error_retries=5
            )

            if response.status_code not in retryable_status_codes:
                break

            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))

        if response.status_code != 200:
            error_msg = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                if "message" in error_data:
                    error_msg = error_data["message"]
            except:
                pass
            raise S3ProxyApiException(error_msg)

        return response.json()
