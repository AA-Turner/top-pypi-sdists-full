import abc
from typing import Any, Callable, Dict, Optional, Literal, List

import requests
from requests import Response

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.source.base import Source
from seshat.source.exceptions import APIError
from seshat.transformer.merger import Merger

HttpMethods = Literal[
    "GET",
    "POST",
    "PUT",
    "DELETE",
]


class APIClient(abc.ABC):
    @abc.abstractmethod
    def request(self, method: HttpMethods, url, **kwargs) -> Response: ...


class RestClient(APIClient):
    def request(self, method: HttpMethods, url, **kwargs) -> Response:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response


class APISource(Source):
    """
    A general-purpose data source for fetching data from any API endpoint.
    Supports all HTTP methods, optional schema transformation, and integration with SFrame.
    Optionally accepts a result_processor function to process the API response data before SFrame conversion.

    Parameters
    ----------
    api_url: str
        The API endpoint URL.
    api_method: str
        HTTP method (GET, POST, etc.).
    api_params: dict, optional
        Query or body parameters.
    api_headers: dict, optional
        HTTP headers.
    response_processor: callable, optional
        Function to process API response object before SFrame conversion.
        Should accept a Response object and return processed data.
    request_args_extractor: callable, optional
        Function to extract request arguments from SFrame input.
    schema: Schema, optional
        Schema for data transformation.
    mode: str, optional
        SFrame mode.
    group_keys: dict, optional
        Group keys for SFrame grouping.
    merge_result: bool
        Whether to merge results.
    merger: Merger
        Merger instance for combining results.
    """

    client: APIClient

    def __init__(
        self,
        api_url: str,
        api_method: str = "GET",
        api_params: Optional[Dict[str, Any]] = None,
        api_headers: Optional[Dict[str, str]] = None,
        response_processor: Optional[Callable[[requests.Response], Any]] = None,
        request_args_extractor: Optional[Callable[[SFrame], dict]] = None,
        schema=None,
        mode=configs.DEFAULT_MODE,
        group_keys=None,
        merge_result=False,
        merger: Merger = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            mode=mode,
            schema=schema,
            group_keys=group_keys,
            merge_result=merge_result,
            merger=merger,
            *args,
            **kwargs,
        )
        self.api_url = api_url
        self.api_method = api_method.upper()
        self.api_params = api_params or {}
        self.api_headers = api_headers or {}
        self.result_processor = response_processor
        self.request_args_extractor = request_args_extractor
        self.client = RestClient()

    def fetch(self, sf_input: SFrame = None, *args, **kwargs):
        """
        Fetch data from the API, optionally process the result, convert to SFrame, and apply schema if provided.
        """
        try:
            req_args = self._build_request_args()
            if self.request_args_extractor:
                req_args |= self.request_args_extractor(sf_input)
            response = self.client.request(**req_args)
        except Exception as e:
            raise APIError(e)

        # Process the result if a processor is provided
        if self.result_processor:
            data = self.result_processor(response)
        else:
            data = response.json()

        # If the API returns a list of records, use it directly; otherwise, try to find the main data key
        if isinstance(data, dict):
            # Try to find the first list value in the dict
            records = None
            for v in data.values():
                if isinstance(v, list):
                    records = v
                    break
            if records is None:
                records = [data]
        elif isinstance(data, list):
            records = data
        else:
            raise ValueError("API response is not a list or dict")

        sf = self.convert_data_type(records)
        if self.schema:
            sf = self.schema(sf)
        return sf

    def _build_request_args(self):
        return dict(
            method=self.api_method,
            url=self.api_url,
            params=self.api_params if self.api_method == "GET" else None,
            json=(
                self.api_params if self.api_method in ("POST", "PUT", "PATCH") else None
            ),
            headers=self.api_headers,
            timeout=30,
        )


class APISourceStory(BaseTransformerStory):
    transformer = APISource

    use_cases = [
        "Fetch data from REST APIs with any HTTP method (GET, POST, PUT, DELETE)",
        "Process API responses with custom logic before converting to SFrame",
        "Build dynamic API requests based on pipeline input data",
        "Integrate API data into pipelines with automatic JSON parsing",
        "Consume APIs with varying response structures (arrays, objects, nested data)",
    ]

    logic_overview = (
        "APISource fetches data from REST APIs using configurable HTTP methods, parameters, and headers. "
        "It inherits from Source and uses the standard Source.__call__() for pipeline integration. "
        "The fetch() method is overridden to handle API requests, optional response processing, "
        "and automatic conversion of JSON responses to SFrame format."
    )

    steps = [
        "Build HTTP request arguments using _build_request_args() with api_url, api_method, api_params, and api_headers",
        "If request_args_extractor is provided, extract additional request args from sf_input and merge with built args",
        "Send HTTP request using self.client.request() (default client: RestClient with requests library)",
        "If response_processor is provided, process the response; otherwise parse as JSON",
        "Handle response format: if dict, extract first list value or wrap in list; if list, use directly",
        "Convert records to SFrame using convert_data_type()",
        "Apply schema transformation if schema is provided in fetch() method",
        "Follow standard Source logic: merge or add to GroupSFrame as needed (from parent __call__)",
    ]

    tags = ["source", "api", "rest", "http", "data-fetching", "integration"]

    def get_scenarios(self) -> List[TransformerScenario]:
        from test.transformer.source.test_api_source import APISourceTestCase

        return TransformerScenario.from_testcase(
            APISourceTestCase, transformer=self.transformer
        )
