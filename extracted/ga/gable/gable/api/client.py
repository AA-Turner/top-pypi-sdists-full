import base64
import copy
import json
import os
import re
from typing import Any, Callable, Literal, TypeVar, Union, cast, Optional
from urllib.parse import urljoin

import requests
from gable.openapi import (
    CheckComplianceDataAssetsPySparkRequest,
    CheckComplianceDataAssetsS3Request,
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetMissingAssetResponse,
    CheckDataAssetNoChangeResponse,
    CheckDataAssetNoContractResponse,
    CheckDataAssetResponse,
    ContractOutput,
    CreateTelemetryRequest,
    CreateTelemetryResponse,
    DataAsset,
    DataAssetsCheckComplianceRequest,
    DeleteDataAssetsResponse,
    ErrorResponse,
    ErrorResponseDeprecated,
    GetNpmCredentialsResponse,
    GetPipCredentialsResponse,
    IngestDataAssetResponse,
    PostContractRequest,
    PostContractResponse,
    RegisterDataAssetPySparkRequest,
    RegisterDataAssetS3Request,
    RegisterDataAssetsRequest,
    RegisterDataAssetsResponse,
    ResponseType,
    PostScaStartRunRequest,
    PostScaStartRunResponse
)
from loguru import logger
from pydantic import parse_obj_as

T = TypeVar("T")

GET_NPM_AUTH_TOKEN_RESPONSE_FILTER_LAMBDA = lambda x: re.sub(
    r'("authToken"\s*:\s*".{10})[^"]*', r"\1*************************", x
)


class GableAPIClient:
    def __init__(
        self, endpoint: Union[str, None] = None, api_key: Union[str, None] = None
    ) -> None:
        # Connection settings
        if endpoint is None:
            self.endpoint = os.getenv("GABLE_API_ENDPOINT", "")
        else:
            self.endpoint = endpoint
        if api_key is None:
            self.api_key = os.getenv("GABLE_API_KEY", "")
        else:
            self.api_key = api_key

    @property
    def ui_endpoint(self) -> str:
        self.validate_endpoint()
        return self.endpoint.replace("api-", "", 1).replace("api.", "", 1)

    def validate_api_key(self):
        if not self.api_key:
            raise ValueError(
                "API Key is not set. Use the --api-key argument or set GABLE_API_KEY "
                "environment variable."
            )

    def validate_endpoint(self):
        if not self.endpoint:
            raise ValueError(
                "API Endpoint is not set. Use the --endpoint argument or set GABLE_API_ENDPOINT "
                "environment variable."
            )
        if not self.endpoint.startswith("https://"):
            if not self.endpoint.startswith("http://localhost"):
                raise ValueError(
                    f"Gable API Endpoint must start with 'https://'. Received: {self.endpoint}"
                )

    def _get(
        self,
        path: str,
        **kwargs: Any,
    ) -> tuple[Union[list[Any], dict[str, Any]], bool, int]:
        return self._request(path, method="GET", **kwargs)

    def _post(
        self, path: str, **kwargs: Any
    ) -> tuple[Union[list[Any], dict[str, Any]], bool, int]:
        return self._request(path, method="POST", **kwargs)

    def _request(
        self,
        path: str,
        method: Literal["GET", "POST", "DELETE"],
        log_payload_filter: Callable = lambda json_payload: json_payload,
        log_response_filter: Callable = lambda response_text: response_text,
        **kwargs: Any,
    ) -> tuple[Union[list[Any], dict[str, Any]], bool, int]:
        self.validate_api_key()
        self.validate_endpoint()
        url = urljoin(self.endpoint, path)

        # Filter the JSON payload to remove spammy/secret request data
        kwargs_copy = copy.deepcopy(kwargs)
        if "json" in kwargs_copy:
            kwargs_copy["json"] = log_payload_filter(kwargs_copy["json"])

        logger.debug(f"{method} {url}: {kwargs_copy}")

        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}

        try:
            response = requests.request(method, url, headers=headers, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"Failed to connect to Gable API at {url}: {type(e).__name__}"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Error making request to Gable API at {url}: {type(e).__name__}"
            )

        # Log the response
        logger.debug(
            f"{'OK' if response.ok else 'ERROR'} ({response.status_code}): {log_response_filter(response.text)}"
        )

        # Check for missing api key
        if response.status_code == 403:
            raise PermissionError("Invalid API Key")

        # Try parsing the response as JSON
        try:
            parsed_response = response.json()
        except json.JSONDecodeError:
            raise ValueError(
                f"Unable to parse server response as JSON: {response.text}"
            )

        return (
            cast(dict[str, Any], parsed_response),
            200 <= response.status_code < 300,
            response.status_code,
        )

    def get_data_asset_infer_contract(
        self,
        data_asset_id: str,
    ) -> tuple[dict[str, Any], bool, int]:
        """Use the infer contract endpoint to generate a contract for a data asset"""
        response, success, status_code = self._get(
            f"v0/data-asset/{data_asset_id}/infer-contract"
        )
        return cast(dict[str, Any], response), success, status_code

    def get_auth_npm(self) -> GetNpmCredentialsResponse:
        """
        Get the NPM credentials for the current user
        """
        try:
            response, success, status_code = self._get(
                "v0/auth/npm",
                log_response_filter=GET_NPM_AUTH_TOKEN_RESPONSE_FILTER_LAMBDA,
            )
            response = GetNpmCredentialsResponse.parse_obj(response)
        except Exception as e:
            logger.opt(exception=e).debug("Error getting NPM credentials")
            raise Exception(
                f"Error getting NPM credentials: {e}. Re-run with --debug for more information."
            )
        if not success:
            raise Exception(
                f"Failed to get NPM credentials: ({status_code}) {response}"
            )
        return response

    def get_auth_pip(self) -> GetPipCredentialsResponse:
        """
        Get the PIP credentials for the current user
        """
        try:
            response, success, status_code = self._get(
                "v0/auth/pip",
                log_response_filter=GET_NPM_AUTH_TOKEN_RESPONSE_FILTER_LAMBDA,
            )
            response = GetPipCredentialsResponse.parse_obj(response)
        except Exception as e:
            logger.opt(exception=e).debug("Error getting PIP credentials")
            raise Exception(
                f"Error getting PIP credentials: {e}. Re-run with --debug for more information."
            )
        if not success:
            raise Exception(
                f"Failed to get PIP credentials: ({status_code}) {response}"
            )
        return response

    def post_data_assets_check_compliance(
        self, request: DataAssetsCheckComplianceRequest
    ) -> Union[
        CheckDataAssetCommentMarkdownResponse,
        ErrorResponse,
        list[CheckDataAssetResponse],
    ]:
        result, success, status_code = self._post(
            "v0/data-assets/check-compliance",
            json=json.loads(request.json(by_alias=True, exclude_none=True)),
        )
        if isinstance(result, list):
            return [CheckDataAssetResponse.parse_obj(r) for r in result]
        else:
            if "responseType" in result:
                return CheckDataAssetCommentMarkdownResponse.parse_obj(result)
            else:
                return ErrorResponse.parse_obj(result)

    def post_register_data_assets(
        self, request: RegisterDataAssetsRequest
    ) -> Union[RegisterDataAssetsResponse, ErrorResponse]:
        result, success, status_code = self._post(
            "v0/data-assets/register",
            json=json.loads(request.json(by_alias=True, exclude_none=True)),
        )
        if isinstance(result, dict) and "asset_registration_outcomes" in result:
            return RegisterDataAssetsResponse.parse_obj(result)
        else:
            return ErrorResponse.parse_obj(result)

    def post_data_asset_register_pyspark(
        self, request: RegisterDataAssetPySparkRequest
    ) -> tuple[Union[IngestDataAssetResponse, ErrorResponseDeprecated], bool, int]:
        response, success, status_code = self._post(
            "v0/data-asset/register/pyspark",
            json=request.dict(by_alias=True),
        )
        if isinstance(response, dict) and "registered" in response:
            result = IngestDataAssetResponse.parse_obj(response)
        else:
            result = ErrorResponseDeprecated.parse_obj(response)
        return (
            result,
            success,
            status_code,
        )

    def post_data_asset_register_s3(
        self, request: RegisterDataAssetS3Request
    ) -> tuple[Union[IngestDataAssetResponse, ErrorResponseDeprecated], bool, int]:
        response, success, status_code = self._post(
            "v0/data-asset/register/s3",
            json=json.loads(request.json(by_alias=True, exclude_none=True)),
        )
        if isinstance(response, dict) and "registered" in response:
            result = IngestDataAssetResponse.parse_obj(response)
        else:
            result = ErrorResponseDeprecated.parse_obj(response)
        return (
            result,
            success,
            status_code,
        )

    def post_check_compliance_data_assets_pyspark(
        self, request: CheckComplianceDataAssetsPySparkRequest
    ) -> Union[
        ErrorResponse,
        CheckDataAssetCommentMarkdownResponse,
        list[CheckDataAssetResponse],
    ]:
        response, _success, _status_code = self._post(
            "v0/data-assets/check-compliance/pyspark",
            data=request.json(by_alias=True, exclude_none=True),
        )
        return parse_data_assets_check_compliance_response(
            request.responseType, response
        )

    def post_check_compliance_data_assets_s3(
        self, request: CheckComplianceDataAssetsS3Request
    ) -> Union[
        ErrorResponse,
        CheckDataAssetCommentMarkdownResponse,
        list[CheckDataAssetResponse],
    ]:
        response, _success, _status_code = self._post(
            "v0/data-assets/check-compliance/s3",
            data=request.json(by_alias=True, exclude_none=True),
        )
        return parse_data_assets_check_compliance_response(
            request.responseType, response
        )

    def post_telemetry(
        self, request: CreateTelemetryRequest
    ) -> tuple[Union[CreateTelemetryResponse, ErrorResponse], bool]:
        response, success, _status_code = self._post(
            "v0/telemetry/ingest", data=request.json(by_alias=True, exclude_none=True)
        )
        if success:
            return CreateTelemetryResponse.parse_obj(response), success
        else:
            return ErrorResponse.parse_obj(response), success

    def post_sca_start_run(
        self,
        request: PostScaStartRunRequest,
    ) -> tuple[Union[PostScaStartRunResponse, ErrorResponse], bool, int]:
        """Start a new SCA run with the given parameters."""
        response, success, status_code = self._post("v0/sca/start-run", json=json.loads(request.json(by_alias=True, exclude_none=True)))
        if success:
            return PostScaStartRunResponse.parse_obj(response), success, status_code
        else:
            return ErrorResponse.parse_obj(response), success, status_code

    def get_data_asset(
        self, data_asset_resource_name: str
    ) -> Union[DataAsset, ErrorResponse]:
        encoded_resource_name = base64.b64encode(
            data_asset_resource_name.encode("utf-8")
        ).decode("utf-8")
        response, _success, _status_code = self._get(
            f"v0/data-asset/{encoded_resource_name}"
        )
        logger.debug(f"get_data_asset response: {response}")
        if "dataAssetResourceName" in response:
            return DataAsset.parse_obj(response)
        else:
            return ErrorResponse.parse_obj(response)

    def get_data_assets(self):
        return self._get("v0/data-assets")

    def delete_data_asset(
        self, data_asset_resource_name: str
    ) -> Union[DeleteDataAssetsResponse, ErrorResponse]:
        encoded_resource_name = base64.b64encode(
            data_asset_resource_name.encode("utf-8")
        ).decode("utf-8")
        response, _success, _status_code = self._get(
            f"v0/data-asset/{encoded_resource_name}"
        )
        if _success:
            return DeleteDataAssetsResponse.parse_obj(response)
        else:
            return ErrorResponse.parse_obj(response)

    def get_pyping(self):
        return self._get("v0/pyping")

    def get_ping(self):
        return self._get("v0/ping")

    def get_contract(self, contract_id) -> ContractOutput:
        response, success, status_code = self._get("v0/contract/" + contract_id)
        if not success or not isinstance(response, ContractOutput):
            error_message = (
                response.get("message", "Unknown error")
                if isinstance(response, dict)
                else "Unexpected response format"
            )
            raise Exception(
                f"Failed to retrieve contract {contract_id}: {error_message}, status code: {status_code}"
            )
        return ContractOutput.parse_obj(response)

    def get_contracts(
        self,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        order_dir: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[ContractOutput]:
        # Build query parameters
        params = {}
        if search is not None:
            params["search"] = search
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if order_by is not None:
            params["orderBy"] = order_by
        if order_dir is not None:
            params["orderDir"] = order_dir
        if status is not None:
            params["status"] = status

        response, success, status_code = self._get("v0/contracts", params=params)
        if not success or not isinstance(response, list):
            error_message = (
                response.get("message", "Unknown error")
                if isinstance(response, dict)
                else "Unexpected response format"
            )
            raise Exception(
                f"Failed to retrieve contracts: {error_message}, status code: {status_code}"
            )
        result: list[ContractOutput] = []
        for response_item in response:
            contract = ContractOutput.parse_obj(response_item)
            result.append(contract)
        return result

    def post_contract_validate(self, request: PostContractRequest):
        return self._post(
            "v0/contract/validate", data=request.json(by_alias=True, exclude_none=True)
        )

    def post_contract(
        self, request: PostContractRequest
    ) -> tuple[Union[PostContractResponse, ErrorResponse], bool, int]:
        response, success, status_code = self._post(
            "v0/contract", data=request.json(by_alias=True, exclude_none=True)
        )
        if "contractIds" in response:
            return PostContractResponse.parse_obj(response), success, status_code
        else:
            return ErrorResponse.parse_obj(response), success, status_code

    def get_full_darns(self, partial_darn: str) -> Union[list[str], ErrorResponse]:
        result_darns = list()
        response, success, status_code = self._get(
            f"v0/data-assets?search={partial_darn}"
        )
        if not success or isinstance(response, dict):
            return ErrorResponse.parse_obj(response)
        for data_asset in response:
            full_darn = data_asset.get("dataAssetResourceName")
            if partial_darn.lower() in full_darn.lower():
                result_darns.append(full_darn)
        return result_darns


def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d


def parse_data_assets_check_compliance_response(
    response_type: ResponseType, response: Union[dict, list]
):
    """Parses the response from the /data-assets/check-compliance/* endpoints"""
    if isinstance(response, list) and response_type == ResponseType.DETAILED:
        return [parse_check_data_asset_response(r) for r in response]
    elif (
        isinstance(response, dict)
        and response.get("responseType") == ResponseType.COMMENT_MARKDOWN.value
    ):
        return parse_obj_as(CheckDataAssetCommentMarkdownResponse, response)
    return ErrorResponse.parse_obj(response)


# Pylance was struggling to understand the union type when calling parse_obj_as
# I created this function to prevent a '# type ignore' annotation in the code
def parse_check_data_asset_response(response) -> CheckDataAssetResponse:
    response_mapping = {
        "NO_CONTRACT": CheckDataAssetNoContractResponse,
        "NO_CHANGE": CheckDataAssetNoChangeResponse,
        "DETAILED": CheckDataAssetDetailedResponse,
        "ERROR": CheckDataAssetErrorResponse,
        "MISSING_DATA_ASSET": CheckDataAssetMissingAssetResponse,
    }
    response_type = response["responseType"]
    if response_type in response_mapping:
        return CheckDataAssetResponse(
            __root__=parse_obj_as(response_mapping[response_type], response)
        )
    raise ValueError(f"Unknown response type: {response_type} in response: {response}")
