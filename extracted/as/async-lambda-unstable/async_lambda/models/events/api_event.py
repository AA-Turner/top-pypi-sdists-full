from typing import Any, Dict, List, Optional

from ..case_insensitive_dict import CaseInsensitiveDict
from .base_event import BaseEvent


class APIEvent(BaseEvent):
    """
    Represents the execution event for an async Lambda task triggered by an API Gateway event.

    Attributes:
        path (str): Request path.
        method (str): HTTP method.
        headers (CaseInsensitiveDict[str, str]): HTTP headers.
        multi_value_headers (CaseInsensitiveDict[str, List[str]]): Multi-value HTTP headers.
        querystring_params (Dict[str, str]): Query string parameters.
        multi_value_querystring_params (Dict[str, List[str]]): Multi-value query string parameters.
        path_parameters (Dict[str, str]): Path parameters.
        request_context (Dict[str, Any]): Request context from API Gateway.
        body (Optional[str]): Request body.
        is_base64_encoded (bool): Whether the body is base64 encoded.
    """

    path: str
    method: str
    headers: CaseInsensitiveDict[str, str]
    multi_value_headers: CaseInsensitiveDict[str, List[str]]
    querystring_params: Dict[str, str]
    multi_value_querystring_params: Dict[str, List[str]]
    path_parameters: Dict[str, str]
    request_context: Dict[str, Any]
    body: Optional[str]
    is_base64_encoded: bool

    def _hydrate_event(self):
        """
        Populate instance attributes from the API Gateway event payload.

        Sets all relevant HTTP and API Gateway fields as attributes on the instance.
        """
        self.path = self._event["path"]
        self.method = self._event["httpMethod"]
        self.headers = CaseInsensitiveDict(self._event["headers"])
        self.multi_value_headers = CaseInsensitiveDict(self._event["multiValueHeaders"])
        self.querystring_params = self._event.get("queryStringParameters", dict())
        self.multi_value_querystring_params = self._event.get(
            "multiValueQueryStringParameters", dict()
        )
        self.path_parameters = self._event.get("pathParameters", dict())
        self.request_context = self._event["requestContext"]
        self.body = self._event.get("body")
        self.is_base64_encoded = self._event["isBase64Encoded"]
