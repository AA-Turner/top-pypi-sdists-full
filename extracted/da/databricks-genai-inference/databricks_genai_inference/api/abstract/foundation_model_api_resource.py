"""Foundation Model API Resource.
"""
import asyncio
import json as json_lib
import os
from typing import Optional

import httpx
import requests
from databricks.sdk import WorkspaceClient
from pydantic import BaseModel, ConfigDict, ValidationError
from tenacity import retry, retry_if_result, stop_after_attempt, wait_random_exponential

from databricks_genai_inference.api.abstract.api_resource import APIResource
from databricks_genai_inference.api.abstract.foundation_model_object import FoundationModelObject
from databricks_genai_inference.api.exception import FoundationModelAPIException
from databricks_genai_inference.api.util import asend_request, is_internal_server_error, send_request

DATABRICKS_MODEL_URL_ENV = 'DATABRICKS_MODEL_URL'
DATABRICKS_HOST_ENV = 'DATABRICKS_HOST'
MODEL_URL_TEMPLATE = '{host}/serving-endpoints/{endpoint}/invocations'


def get_url(
    host: str,
    endpoint: str,
):
    """
    Returns the URL for the API.

    Args:
        host (str): The host for the API.
        endpoint (str): The model endpoint id for the API.

    Returns:
        The URL for the API.
    """

    env_url = os.getenv(DATABRICKS_MODEL_URL_ENV)
    if env_url:
        return env_url

    env_host = os.getenv(DATABRICKS_HOST_ENV)
    if env_host:
        host = env_host

    return MODEL_URL_TEMPLATE.format(host=host, endpoint=endpoint)


class FoundationModelAPIInput(BaseModel):
    """
    A class representing the input schema for a Foundation Model API request.

    Attributes:
        model (str): The name of the model to use.
        timeout (Optional[int]): The timeout for the API request.
        max_retries (Optional[int]): The maximum number of retries for the API request.
    """
    model_config = ConfigDict(extra='forbid')

    model: str
    timeout: Optional[int] = None
    max_retries: Optional[int] = None


class FoundationModelAPIResource(APIResource):
    """
    A class representing a foundation model API resource.

    Attributes:
        SUPPORTED_MODEL_LIST (list): A list of supported models.
        DEFAULT_TIMEOUT (int): The default timeout for API requests.
        model_input (FoundationModelAPIInput): The input schema for the API.
        model_output (FoundationModelObject): The output schema for the API.
        model_streaming_output (FoundationModelObject): The streaming output schema for the API.
        config (Config): The configuration object for the API.
    """

    SUPPORTED_MODEL_LIST = []
    DEFAULT_TIMEOUT = 60
    MAX_RETRIES = 1
    model_input = FoundationModelAPIInput
    model_output = FoundationModelObject
    model_streaming_output = FoundationModelObject

    @classmethod
    def create(cls, client: requests.Session = None, **kwargs):
        """
        Creates a new API response.

        Args:
        **kwargs: The keyword arguments for the API.

        Returns:
        The result of the API query.
        """
        api_input, endpoint = cls._parse_and_validate_request(**kwargs)
        return cls._make_query(client, api_input, endpoint)

    @classmethod
    def _parse_and_validate_request(cls, **kwargs) -> FoundationModelAPIInput:
        """
        Parses and validates the request parameters.

        Args:
            **kwargs: The request parameters.

        Returns:
            A (FoundationModelAPIInput, endpoint:str) pair.

        Raises:
            FoundationModelAPIException: If the request parameters are invalid.
        """
        try:
            api_input = cls.model_input(**kwargs)
            # If this is a 'supported' model, map it to a pay-per-token name. Otherwise assume this is a custom endpoint.
            if api_input.model in cls.SUPPORTED_MODEL_LIST:
                endpoint = f'databricks-{api_input.model}'
            else:
                endpoint = api_input.model
            return api_input, endpoint
        except ValidationError as e:
            raise FoundationModelAPIException(message=str(e)) from e

    @classmethod
    def _make_query(cls, client: requests.Session, model_input: FoundationModelAPIInput, endpoint: str):
        """
        Makes a query to the API.

        Args:
        model_input (FoundationModelAPIInput): The input for the API.

        Returns:
        The response of the API query.

        Raises:
        FoundationModelAPIException: If the API query fails.
        """

        w = WorkspaceClient()
        url = get_url(host=w.config.host, endpoint=endpoint)
        headers = {
            'Content-Type': 'application/json',
            'X-Databricks-Endpoints-API-Client': 'Generative AI Inference (Mosaic) SDK'
        }
        headers = headers | w.config.authenticate()
        json = model_input.model_dump(exclude_unset=True)
        timeout = json.pop("timeout", cls.DEFAULT_TIMEOUT)
        max_retries = json.pop("max_retries", cls.MAX_RETRIES)
        model = json.pop("model")
        try:
            if model_input.model_dump().get("stream", False):
                return cls._get_streaming_response(client=client,
                                                   url=url,
                                                   headers=headers,
                                                   json=json,
                                                   timeout=timeout,
                                                   max_retries=max_retries)
            else:
                return cls._get_non_streaming_response(client=client,
                                                       url=url,
                                                       headers=headers,
                                                       json=json,
                                                       timeout=timeout,
                                                       max_retries=max_retries)
        except requests.exceptions.ReadTimeout as e:
            raise FoundationModelAPIException(message=f'API request timed out after {timeout} seconds') from e
        except requests.exceptions.ConnectionError as e:
            raise FoundationModelAPIException(message="API request failed with connection error") from e
        except FoundationModelAPIException as e:
            raise e

    @classmethod
    def _get_non_streaming_response(cls, client, url, headers, json, timeout, max_retries):
        """
        Sends a request to the API and returns the non-streaming response.

        Args:
        url (str): The URL for the API.
        headers (dict): The headers for the API request.
        json (dict): The JSON data for the API request.
        timeout (int): The timeout for the API request.

        Raises:
        NotImplementedError: If the method is not implemented.
        """
        retry_req = retry(retry=retry_if_result(is_internal_server_error),
                          wait=wait_random_exponential(min=1, max=timeout),
                          stop=stop_after_attempt(max_retries),
                          retry_error_callback=lambda retry: retry.outcome.result())(send_request)
        response = retry_req(client=client, url=url, headers=headers, json=json, timeout=timeout)
        if response.ok:
            try:
                return cls.model_output(response.json())
            except requests.JSONDecodeError as e:
                raise FoundationModelAPIException(response=response, url=url) from e
        else:
            raise FoundationModelAPIException(response=response, url=url)

    @classmethod
    def _get_streaming_response(cls, client, url, headers, json, timeout, max_retries):
        """
        Sends a request to the API and returns the streaming response.

        Args:
        url (str): The URL for the API.
        headers (dict): The headers for the API request.
        json (dict): The JSON data for the API request.
        timeout (int): The timeout for the API request.

        Raises:
        NotImplementedError: If the method is not implemented.
        """
        retry_req = retry(retry=retry_if_result(is_internal_server_error),
                          wait=wait_random_exponential(min=1, max=timeout),
                          stop=stop_after_attempt(max_retries),
                          retry_error_callback=lambda retry: retry.outcome.result())(send_request)
        response = retry_req(url=url, headers=headers, json=json, timeout=timeout, client=client)
        if response:
            try:
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith("data: "):
                            line = line[len("data: "):]
                        if line == '[DONE]':
                            break
                        loaded_json = json_lib.loads(line)
                        if loaded_json:
                            yield cls.model_streaming_output(loaded_json)
            except json_lib.decoder.JSONDecodeError as e:
                raise FoundationModelAPIException(response=response, message="JSONDecodeError", url=url) from e
        else:
            raise FoundationModelAPIException(response=response, url=url)

    @classmethod
    async def acreate(cls, client: httpx.AsyncClient = None, **kwargs):
        """
        Creates a new API response.

        Args:
        client (httpx.AsyncClient): The client for http call.
        **kwargs: The keyword arguments for the API.

        Returns:
        The result of the API query.
        """
        model_input, endpoint = cls._parse_and_validate_request(**kwargs)
        return await cls._amake_query(client, model_input, endpoint)

    @classmethod
    async def _amake_query(cls, client: httpx.AsyncClient, model_input: FoundationModelAPIInput, endpoint: str):
        """
        Makes a query to the API.

        Args:
        client (httpx.AsyncClient): The client for http call.
        model_input (FoundationModelAPIInput): The input for the API.

        Returns:
        The response of the API query.

        Raises:
        FoundationModelAPIException: If the API query fails.
        """
        w = WorkspaceClient()
        url = f'{w.config.host}/serving-endpoints/{endpoint}/invocations'
        headers = {
            'Content-Type': 'application/json',
            'X-Databricks-Endpoints-API-Client': 'Generative AI Inference (Mosaic) SDK'
        }
        headers = w.config.authenticate() | headers
        json = model_input.model_dump(exclude_unset=True)
        timeout = json.pop("timeout", cls.DEFAULT_TIMEOUT)
        max_retries = json.pop("max_retries", cls.MAX_RETRIES)
        model = json.pop("model")

        try:
            if model_input.model_dump().get("stream", False):
                return await cls._aget_streaming_response(client=client,
                                                          url=url,
                                                          headers=headers,
                                                          json=json,
                                                          timeout=timeout,
                                                          max_retries=max_retries)
            else:
                return await cls._aget_non_streaming_response(client=client,
                                                              url=url,
                                                              headers=headers,
                                                              json=json,
                                                              timeout=timeout,
                                                              max_retries=max_retries)
        except httpx.ReadTimeout as e:
            raise FoundationModelAPIException(message=f'API request timed out after {timeout} seconds') from e
        except httpx.ConnectError as e:
            raise FoundationModelAPIException(message="API request failed with connection error") from e
        except FoundationModelAPIException as e:
            raise e

    @classmethod
    async def _aget_non_streaming_response(cls, client, url, headers, json, timeout, max_retries):
        """
        Parse and returns the non-streaming response.

        Args:
        url (str): The URL for the API.
        response (httpx.Resonse): The response from the post request.
        """
        asend_request_with_retry = retry(retry=retry_if_result(is_internal_server_error),
                                         wait=wait_random_exponential(min=1, max=timeout),
                                         stop=stop_after_attempt(max_retries),
                                         retry_error_callback=lambda retry: retry.outcome.result())(asend_request)
        response = await asend_request_with_retry(client=client, url=url, headers=headers, json=json, timeout=timeout)
        if response.status_code < 400:
            try:
                response_body = response.json()
                return cls.model_output(response_body)
            except httpx.DecodingError as e:
                raise FoundationModelAPIException(url=url, response=response) from e
        else:
            raise FoundationModelAPIException(url=url, response=response)

    @classmethod
    async def _aget_streaming_response(cls, client, url, headers, json, timeout, max_retries):
        """
        Parse and returns the streaming response.

        Args:
        url (str): The URL for the API.
        response (httpx.Resonse): The response from the post request.
        """
        asend_request_with_retry = retry(retry=retry_if_result(is_internal_server_error),
                                         wait=wait_random_exponential(min=1, max=timeout),
                                         stop=stop_after_attempt(max_retries),
                                         retry_error_callback=lambda retry: retry.outcome.result())(asend_request)
        response = await asend_request_with_retry(client=client, url=url, headers=headers, json=json, timeout=timeout)
        return AsyncStreamResponse(url, response, cls.model_streaming_output)


class AsyncStreamResponse:
    """
    A class representing the async stream response, which works as a async iterator.
    """

    def __init__(self, url, response, model_streaming_output_cls):
        self._url = url
        self._response = response
        self._model_streaming_output_cls = model_streaming_output_cls
        self._closed = False
        self._iterator = self.__stream__()

    def __del__(self):
        if not self._closed:
            asyncio.run(self._response.aclose())

    async def __aiter__(self):
        try:
            async for item in self._iterator:
                yield item
        finally:
            await self._response.aclose()
            self._closed = True

    async def __stream__(self):
        if self._response.status_code < 400:
            try:
                async for line in self._response.aiter_lines():
                    if line:
                        if line.startswith("data: "):
                            line = line[len("data: "):]
                        if line == '[DONE]':
                            break
                        loaded_json = json_lib.loads(line)
                        if loaded_json:
                            yield self._model_streaming_output_cls(loaded_json)
            except json_lib.decoder.JSONDecodeError as e:
                raise FoundationModelAPIException(url=self._url, message="JSONDecodeError",
                                                  response=self._response) from e
        else:
            raise FoundationModelAPIException(url=self._url, response=self._response)
