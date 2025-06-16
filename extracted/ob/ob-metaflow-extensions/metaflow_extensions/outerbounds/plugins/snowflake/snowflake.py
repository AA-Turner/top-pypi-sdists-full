"""
This library is an abstraction layer for connecting to snowflake using Outerbounds
OIDC tokens. It expects that a security integration that authenticates tokens minted
by Outerbounds has already been configured in the target snowflake account.
"""
from metaflow.metaflow_config import SERVICE_URL
from metaflow.metaflow_config_funcs import init_config
from typing import Dict
from os import environ
import sys
import json
import requests
import random
import time


class OuterboundsSnowflakeConnectorException(Exception):
    pass


class OuterboundsSnowflakeIntegrationSpecApiResponse:
    def __init__(self, response):
        self.response = response

    @property
    def account(self):
        return self.response["account"]

    @property
    def user(self):
        return self.response["user"]

    @property
    def default_role(self):
        return self.response["default_role"]

    @property
    def warehouse(self):
        return self.response["warehouse"]

    @property
    def database(self):
        return self.response["database"]


def get_snowflake_token(user: str = "", role: str = "", integration: str = "") -> str:
    """
    Uses the Outerbounds source token to request for a snowflake compatible OIDC
    token. This token can then be used to connect to snowflake.
    user: str
        The user the token will be minted for
    role: str
        The role to which the token will be scoped to
    integration: str
        The name of the snowflake integration to use. If not set, an existing integration will be used provided that only one exists per perimeter. If integration is not set and more than one exists, then we raise an exception.
    """
    provisioner = SnowflakeIntegrationProvisioner(integration)
    if not user or not role or not integration:
        integration_spec = provisioner.get_snowflake_integration_spec()
        if not user:
            user = integration_spec.user

        if not role:
            role = integration_spec.default_role

        if not integration:
            integration = provisioner.get_integration_name()

    snowflake_token_url = provisioner.get_snowflake_token_url()
    perimeter = provisioner.get_perimeter()
    payload = {
        "perimeterName": perimeter,
        "snowflakeUser": user,
        "snowflakeRole": role,
        "integrationName": integration,
    }
    json_payload = json.dumps(payload)
    headers = provisioner.get_service_auth_header()
    response = _api_server_get(
        snowflake_token_url, data=json_payload, headers=headers, conn_error_retries=5
    )
    response.raise_for_status()
    return response.json()["token"]


def connect(user: str = "", role: str = "", integration: str = "", **kwargs):
    """
    Connect to snowflake using the token minted by Outerbounds
    user: str
        The user name used to authenticate with snowflake
    role: str
        The role to request when connect with snowflake
    integration: str
        The name of the snowflake integration to use. If not set, an existing integration will be used provided that only one exists in the current perimeter. If integration is not set and more than one exists in the current perimeter, then we raise an exception.
    kwargs: dict
        Additional arguments to pass to the python snowflake connector
    """
    # ensure password is not set
    if "password" in kwargs:
        raise OuterboundsSnowflakeConnectorException(
            "Password should not be set when using Outerbounds snowflake connector."
        )

    provisioner = SnowflakeIntegrationProvisioner(integration)
    get_defaults = any(
        key not in kwargs for key in ["account", "warehouse", "database"]
    )
    if not user or not role or not integration or get_defaults:
        integration_spec = provisioner.get_snowflake_integration_spec()
        if not user:
            user = integration_spec.user

        if not role:
            role = integration_spec.default_role

        if not integration:
            integration = provisioner.get_integration_name()

        if "account" not in kwargs:
            kwargs["account"] = integration_spec.account

        if "warehouse" not in kwargs:
            kwargs["warehouse"] = integration_spec.warehouse

        # if the user is attempting to use a warehouse different from what is specified in the
        # integration we will not set the database
        if (
            "database" not in kwargs
            and kwargs["warehouse"] == integration_spec.warehouse
        ):
            kwargs["database"] = integration_spec.database

    # get snowflake token
    token = get_snowflake_token(user=user, role=role, integration=integration)
    kwargs["token"] = token
    kwargs["authenticator"] = "oauth"
    kwargs["role"] = role
    kwargs["user"] = user

    # connect to snowflake
    try:
        from snowflake.connector import connect

        cn = connect(**kwargs)
        return cn
    except ImportError as ie:
        raise OuterboundsSnowflakeConnectorException(
            f"Error importing snowflake connector: {ie}.\nPlease make sure the 'snowflake-connector-python' package has been installed by running 'pip install -U \"outerbounds[snowflake]\"' or using the Metaflow decorators @pypi or @conda."
        )
    except Exception as e:
        raise OuterboundsSnowflakeConnectorException(
            f"Error connecting to snowflake: {e}"
        )


def _api_server_get(*args, conn_error_retries=2, **kwargs):
    """
    There are two categories of errors that we need to handle when dealing with any API server.
    1. HTTP errors. These are are errors that are returned from the API server.
        - How to handle retries for this case will be application specific.
    2. Errors when the API server may not be reachable (DNS resolution / network issues)
        - In this scenario, we know that something external to the API server is going wrong causing the issue.
        - Failing pre-maturely in the case might not be the best course of action since critical user jobs might crash on intermittent issues.
        - So in this case, we can just planely retry the request.

    This function handles the second case. It's a simple wrapper to handle the retry logic for connection errors.
    If this function is provided a `conn_error_retries` of 5, then the last retry will have waited 32 seconds.
    Generally this is a safe enough number of retries after which we can assume that something is really broken. Until then,
    there can be intermittent issues that would resolve themselves if we retry gracefully.
    """
    _num_retries = 0
    noise = random.uniform(-0.5, 0.5)
    while _num_retries < conn_error_retries:
        try:
            return requests.get(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            if _num_retries <= conn_error_retries - 1:
                # Exponential backoff with 2^(_num_retries+1) seconds
                time.sleep((2 ** (_num_retries + 1)) + noise)
                _num_retries += 1
            else:
                print(
                    "[@snowflake] Failed to connect to the API server. ",
                    file=sys.stderr,
                )
                raise


class Snowflake:
    def __init__(
        self, user: str = "", role: str = "", integration: str = "", **kwargs
    ) -> None:
        self.cn = connect(user, role, integration, **kwargs)

    def __enter__(self):
        return self.cn

    def __exit__(self, exception_type, exception_value, traceback):
        self.cn.close()

    def close(self):
        self.cn.close()


class SnowflakeIntegrationProvisioner:
    def __init__(self, integration_name: str) -> None:
        self.conf = init_config()
        self.integration_name = integration_name

    def get_snowflake_integration_spec(
        self,
    ) -> OuterboundsSnowflakeIntegrationSpecApiResponse:
        integrations_url = self._get_integration_url()
        perimeter = self.get_perimeter()
        headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        request_payload = {
            "perimeter_name": perimeter,
        }
        # if integration is not set, list all integrations
        if not self.integration_name:
            list_snowflake_integrations_url = f"{integrations_url}/snowflake"
            response = self._make_request(
                list_snowflake_integrations_url, headers, request_payload
            )
            snowflake_integrations = response.get("integrations", [])
            if not snowflake_integrations:
                raise OuterboundsSnowflakeConnectorException(
                    "No snowflake integrations found. Please make sure you have created a Snowflake integration on the Outerbounds UI first."
                )

            if len(snowflake_integrations) > 1:
                raise OuterboundsSnowflakeConnectorException(
                    f"Multiple snowflake integrations found. Please specify a specific integration name you would like to use."
                )

            self.integration_name = snowflake_integrations[0]["integration_name"]
            return OuterboundsSnowflakeIntegrationSpecApiResponse(
                snowflake_integrations[0]["integration_spec"]
            )

        get_snowflake_integration_url = (
            f"{integrations_url}/snowflake/{self.integration_name}"
        )
        response = self._make_request(
            get_snowflake_integration_url, headers, request_payload
        )
        self.integration_name = response["integration_name"]
        return OuterboundsSnowflakeIntegrationSpecApiResponse(
            response["integration_spec"]
        )

    def get_integration_name(self) -> str:
        return self.integration_name

    def get_perimeter(self) -> str:
        if "OBP_PERIMETER" in self.conf:
            perimeter = self.conf["OBP_PERIMETER"]
        else:
            # if the perimeter is not in metaflow config, try to get it from the environment
            perimeter = environ.get("OBP_PERIMETER", "")
        if not perimeter:
            raise OuterboundsSnowflakeConnectorException(
                "No perimeter set. Please make sure to run `outerbounds configure <...>` command which can be found on the Ourebounds UI or reach out to your Outerbounds support team."
            )

        return perimeter

    def get_snowflake_token_url(self) -> str:
        if "OBP_AUTH_SERVER" in self.conf:
            auth_host = self.conf["OBP_AUTH_SERVER"]
        else:
            from urllib.parse import urlparse

            auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]

        return "https://" + auth_host + "/generate/snowflake"

    def get_service_auth_header(self) -> str:
        if "METAFLOW_SERVICE_AUTH_KEY" in self.conf:
            return {"x-api-key": self.conf["METAFLOW_SERVICE_AUTH_KEY"]}
        else:
            return json.loads(environ.get("METAFLOW_SERVICE_HEADERS"))

    def _get_integration_url(self) -> str:
        from metaflow_extensions.outerbounds.remote_config import init_config
        from os import environ

        if "OBP_INTEGRATIONS_URL" in self.conf:
            integrations_url = self.conf["OBP_INTEGRATIONS_URL"]
        else:
            # if the integrations url is not in metaflow config, try to get it from the environment
            integrations_url = environ.get("OBP_INTEGRATIONS_URL", "")

        if not integrations_url:
            raise OuterboundsSnowflakeConnectorException(
                "No integrations url set. Please notify your Outerbounds support team about this issue."
            )

        return integrations_url

    def _make_request(self, url, headers: Dict, payload: Dict) -> Dict:
        try:
            from metaflow.metaflow_config import SERVICE_HEADERS

            request_headers = {**headers, **(SERVICE_HEADERS or {})}
        except ImportError:
            headers = headers

        retryable_status_codes = [409]
        json_payload = json.dumps(payload)
        for attempt in range(2):  # 0 = initial attempt, 1-2 = retries
            response = _api_server_get(
                url, data=json_payload, headers=request_headers, conn_error_retries=5
            )
            if response.status_code not in retryable_status_codes:
                break

            if attempt < 2:  # Don't sleep after the last attempt
                sleep_time = 0.5 * (attempt + 1)
                time.sleep(sleep_time)

        response = _api_server_get(
            url, data=json_payload, headers=request_headers, conn_error_retries=5
        )
        self._handle_error_response(response)
        return response.json()

    @staticmethod
    def _handle_error_response(response: requests.Response):
        if response.status_code >= 500:
            raise OuterboundsSnowflakeConnectorException(
                f"Server error: {response.text}. Please reach out to your Outerbounds support team."
            )

        body = response.json()
        status_code = body.get("error", {}).get("statusCode", response.status_code)
        if status_code == 404:
            raise OuterboundsSnowflakeConnectorException(f"Secret not found: {body}")

        if status_code >= 400:
            try:
                raise OuterboundsSnowflakeConnectorException(
                    f"status_code={status_code}\t*{body['error']['details']['kind']}*\n{body['error']['details']['message']}"
                )
            except KeyError:
                raise OuterboundsSnowflakeConnectorException(
                    f"status_code={status_code} Unexpected error: {body}"
                )
