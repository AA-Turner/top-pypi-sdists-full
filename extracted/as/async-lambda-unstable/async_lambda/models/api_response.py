import json
from typing import Any, Callable, Dict, Optional


class Response:
    """
    Represents an HTTP response for async Lambda functions.

    Attributes:
        status_code (int): HTTP status code of the response.
        headers (Dict[str, str]): HTTP headers of the response.
        body (Optional[str]): Body of the response, if any.
    """

    status_code: int
    headers: Dict[str, str]
    body: Optional[str] = None

    def __init__(
        self,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
    ):
        """
        Initialize a Response instance.

        Args:
            status_code (int, optional): HTTP status code. Defaults to 200.
            headers (Optional[Dict[str, str]], optional): HTTP headers. Defaults to None.
            body (Optional[str], optional): Response body. Defaults to None.
        """
        self.status_code = status_code
        self.body = body
        self.headers = dict() if headers is None else headers

    def __async_lambda_response__(self):
        """
        Return the response as a dictionary formatted for AWS Lambda proxy integration.

        Returns:
            dict: Dictionary containing status code, headers, and body.
        """
        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.body,
        }


class JSONResponse(Response):
    """
    Response subclass for returning JSON data.

    Attributes:
        status_code (int): HTTP status code of the response.
        headers (Dict[str, str]): HTTP headers, with "Content-Type" set to "application/json".
        body (str): JSON-encoded response body.
    """

    def __init__(
        self,
        body: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        encoder: Callable[[Any], str] = json.dumps,
    ):
        """
        Initialize a JSONResponse instance.

        Args:
            body (Any): Data to be serialized to JSON and returned in the response body.
            status_code (int, optional): HTTP status code. Defaults to 200.
            headers (Optional[Dict[str, str]], optional): Additional headers. Defaults to None.
            encoder (Callable[[Any], str], optional): Function to serialize the body to a JSON string. Defaults to json.dumps.
        """
        self.status_code = status_code
        self.headers = dict() if headers is None else headers
        self.headers["Content-Type"] = "application/json"
        self.body = encoder(body)
