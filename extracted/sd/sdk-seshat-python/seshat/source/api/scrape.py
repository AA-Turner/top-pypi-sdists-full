from typing import Optional, Dict, Any, Callable

import requests
from requests import Response

from seshat.data_class import SFrame
from seshat.general import configs
from seshat.general.transformer_story.base import BaseTransformerStory
from seshat.source.api.base import APIClient, HttpMethods, APISource
from seshat.transformer.merger import Merger


class ScrapFlyClient(APIClient):
    scrapfly_url = "https://api.scrapfly.io/scrape"
    default_query_params = {
        "tags": "player,project:default",
        "asp": True,
        "render_js": True,
    }

    def __init__(self, apikey: str):
        self.apikey = apikey

    def request(self, url, method: HttpMethods, **kwargs) -> Response:
        query_params = {
            **self.default_query_params,
            **kwargs.pop("params", {}),
            "key": self.apikey,
            "url": url,
        }
        kwargs.setdefault("timeout", 90)
        response = requests.request(
            method=method,
            url=self.scrapfly_url,
            params=query_params,
            **kwargs,
        )
        response.raise_for_status()
        return response


class ScrapFlySource(APISource):
    """
    A web scraping data source that fetches rendered web pages using the ScrapFly API.
    Extends APISource with ScrapFly-specific client for JavaScript rendering and anti-scraping protection.

    Parameters
    ----------
    api_url : str
        The target URL to scrape.
    api_key : str
        ScrapFly API key for authentication.
    api_method : str, optional
        HTTP method to use (default: "GET").
    api_params : dict, optional
        Additional query parameters for the ScrapFly API.
    api_headers : dict, optional
        HTTP headers to send with the request.
    response_processor : callable, optional
        Function to process the scraped response before SFrame conversion.
        Should accept a Response object and return processed data.
    schema : Schema, optional
        Schema for data transformation after scraping.
    mode : str, optional
        SFrame mode for data conversion (default: configs.DEFAULT_MODE).
    group_keys : dict, optional
        Group keys for SFrame grouping.
    merge_result : bool, optional
        Whether to merge results with input SFrame (default: False).
    merger : Merger, optional
        Merger instance for combining results.
    """

    def __init__(
        self,
        api_url: str,
        api_key: Optional[str],
        api_method: str = "GET",
        api_params: Optional[Dict[str, Any]] = None,
        api_headers: Optional[Dict[str, str]] = None,
        response_processor: Optional[Callable[[requests.Response], Any]] = None,
        request_args_extractor: Optional[Callable[[SFrame], dict]] = None,
        schema=None,
        mode=configs.DEFAULT_MODE,
        group_keys=None,
        merge_result=False,
        merger: Merger = Merger,
        *args,
        **kwargs
    ):
        super().__init__(
            api_url,
            api_method,
            api_params,
            api_headers,
            response_processor,
            request_args_extractor,
            schema,
            mode,
            group_keys,
            merge_result,
            merger,
            *args,
            **kwargs,
        )
        self.client = ScrapFlyClient(api_key)


class ScrapFlySourceStory(BaseTransformerStory):
    transformer = ScrapFlySource

    use_cases = [
        "Scrape dynamic web pages that require JavaScript rendering",
        "Bypass anti-scraping protections with ScrapFly's proxy and browser fingerprinting",
        "Extract data from modern SPAs (Single Page Applications)",
        "Integrate web scraping into data pipelines with automatic parsing and schema transformation",
        "Process scraped HTML/JSON responses with custom response_processor functions",
    ]

    logic_overview = (
        "ScrapFlySource scrapes web pages using the ScrapFly API service, which provides JavaScript rendering, "
        "anti-scraping protection bypass, and proxy management. It inherits from APISource, using the same fetch() "
        "and __call__() logic, but replaces the APIClient with ScrapFlyClient that wraps the target URL "
        "in a ScrapFly API request."
    )

    steps = [
        "Initialize with ScrapFlyClient using the provided api_key",
        "When fetch() is called, ScrapFlyClient wraps the target URL in a ScrapFly API request",
        "ScrapFly API renders JavaScript, bypasses anti-scraping, and returns the page content",
        "Follow APISource logic: process response with response_processor or parse as JSON",
        "Convert to SFrame and apply schema transformation if provided",
        "Follow standard Source logic: merge or add to GroupSFrame as needed",
    ]

    tags = ["source", "scraping", "api"]
