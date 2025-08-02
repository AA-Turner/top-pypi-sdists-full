from typing import Dict

import base64
import json
import requests
import random
import time
import sys

from .utils import safe_requests_wrapper, TODOException


class OuterboundsSecretsException(Exception):
    pass


class SecretNotFound(OuterboundsSecretsException):
    pass


class OuterboundsSecretsApiResponse:
    def __init__(self, response):
        self.response = response

    @property
    def secret_resource_id(self):
        return self.response["secret_resource_id"]

    @property
    def secret_backend_type(self):
        return self.response["secret_backend_type"]


class SecretRetriever:
    def get_secret_as_dict(self, secret_id, options={}, role=None):
        """
        Supports a special way of specifying secrets sources in outerbounds using the format:
            @secrets(sources=["outerbounds.<integrations_name>"])

        When invoked it makes a requests to the integrations secrets metadata endpoint on the
        keywest server to get the cloud resource id for a secret. It then uses that to invoke
        secrets manager on the core oss and returns the secrets.
        """
        headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        perimeter, integrations_url = self._get_secret_configs()
        integration_name = secret_id
        request_payload = {
            "perimeter_name": perimeter,
            "integration_name": integration_name,
        }
        response = self._make_request(integrations_url, headers, request_payload)
        secret_resource_id = response.secret_resource_id
        secret_backend_type = response.secret_backend_type

        from metaflow.plugins.secrets.secrets_decorator import (
            get_secrets_backend_provider,
        )

        secrets_provider = get_secrets_backend_provider(secret_backend_type)
        secret_dict = secrets_provider.get_secret_as_dict(
            secret_resource_id, options={}, role=role
        )

        # Outerbounds stores secrets as binaries. Hence we expect the returned secret to be
        # {<cloud-secret-name>: <base64 encoded full secret>}. We decode the secret here like:
        # 1. decode the base64 encoded full secret
        # 2. load the decoded secret as a json
        # 3. decode the base64 encoded values in the dict
        # 4. return the decoded dict
        binary_secret = next(iter(secret_dict.values()))
        return self._decode_secret(binary_secret)

    def _is_base64_encoded(self, data):
        try:
            if isinstance(data, str):
                # Check if the string can be base64 decoded
                base64.b64decode(data).decode("utf-8")
                return True
            return False
        except Exception:
            return False

    def _decode_secret(self, secret):
        try:
            result = {}
            secret_str = secret
            if self._is_base64_encoded(secret):
                # we check if the secret string is base64 encoded because the returned secret from
                # AWS secret manager is base64 encoded while the secret from GCP is not
                secret_str = base64.b64decode(secret).decode("utf-8")

            secret_dict = json.loads(secret_str)
            for key, value in secret_dict.items():
                result[key] = base64.b64decode(value).decode("utf-8")

            return result
        except Exception as e:
            raise OuterboundsSecretsException(f"Error decoding secret: {e}")

    def _get_secret_configs(self):
        from metaflow_extensions.outerbounds.remote_config import init_config  # type: ignore
        from os import environ

        conf = init_config()
        if "OBP_PERIMETER" in conf:
            perimeter = conf["OBP_PERIMETER"]
        else:
            # if the perimeter is not in metaflow config, try to get it from the environment
            perimeter = environ.get("OBP_PERIMETER", "")

        if "OBP_INTEGRATIONS_URL" in conf:
            integrations_url = conf["OBP_INTEGRATIONS_URL"]
        else:
            # if the integrations is not in metaflow config, try to get it from the environment
            integrations_url = environ.get("OBP_INTEGRATIONS_URL", "")

        if not perimeter:
            raise OuterboundsSecretsException(
                "No perimeter set. Please make sure to run `outerbounds configure <...>` command which can be found on the Outerbounds UI or reach out to your Outerbounds support team."
            )

        if not integrations_url:
            raise OuterboundsSecretsException(
                "No integrations url set. Please notify your Outerbounds support team about this issue."
            )

        integrations_secrets_metadata_url = f"{integrations_url}/secrets/metadata"
        return perimeter, integrations_secrets_metadata_url

    def _make_request(self, url, headers: Dict, payload: Dict):
        try:
            from metaflow.metaflow_config import SERVICE_HEADERS

            request_headers = {**headers, **(SERVICE_HEADERS or {})}
        except ImportError:
            raise OuterboundsSecretsException(
                "Failed to create app: No Metaflow service headers found"
            )

        response = safe_requests_wrapper(
            requests.get,
            url,
            data=json.dumps(payload),
            headers=request_headers,
            conn_error_retries=5,
            retryable_status_codes=[409],
        )
        self._handle_error_response(response)
        return OuterboundsSecretsApiResponse(response.json())

    @staticmethod
    def _handle_error_response(response: requests.Response):
        if response.status_code >= 500:
            raise OuterboundsSecretsException(
                f"Server error: {response.text}. Please reach out to your Outerbounds support team."
            )
        status_code = response.status_code
        if status_code == 404:
            raise SecretNotFound(f"Secret not found: {response.text}")

        if status_code >= 400:
            raise OuterboundsSecretsException(
                f"status_code={status_code}\t\n\t\t{response.text}"
            )
