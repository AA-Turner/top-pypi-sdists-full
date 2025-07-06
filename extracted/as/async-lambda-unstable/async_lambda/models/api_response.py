import json
from typing import Any, Callable, Dict, Optional


class Response:
    status_code: int
    headers: Dict[str, str]
    body: Optional[str] = None

    def __init__(
        self,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
    ):
        self.status_code = status_code
        self.body = body
        self.headers = dict() if headers is None else headers

    def __async_lambda_response__(self):
        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.body,
        }


class JSONResponse(Response):
    def __init__(
        self,
        body: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        encoder: Callable[[Any], str] = json.dumps,
    ):
        self.status_code = status_code
        self.headers = dict() if headers is None else headers
        self.headers["Content-Type"] = "application/json"
        self.body = encoder(body)
