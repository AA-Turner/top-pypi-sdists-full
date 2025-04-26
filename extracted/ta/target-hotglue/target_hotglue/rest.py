"""Hotglue target sink class, which handles writing streams."""

from datetime import datetime

import backoff
import requests
import json
from typing import Any, Dict, Optional
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from target_hotglue.auth import Authenticator
from target_hotglue.common import HGJSONEncoder


class Rest:
    timeout: int = 300
    http_headers: Dict[str, Any] = {}
    params: Dict[str, Any] = {}
    authenticator: Optional[Authenticator] = None

    @property
    def default_headers(self):
        headers = self.http_headers

        if self.authenticator and isinstance(self.authenticator, Authenticator):
            headers.update(self.authenticator.auth_headers)

        return headers

    @backoff.on_exception(
        backoff.expo,
        (RetriableAPIError, requests.exceptions.ReadTimeout),
        max_tries=5,
        factor=2,
    )
    def _request(
        self, http_method, endpoint, params={}, request_data=None, headers={}, verify=True
    ) -> requests.PreparedRequest:
        """Prepare a request object."""
        url = self.url(endpoint)
        headers.update(self.default_headers)
        headers.update({"Content-Type": "application/json"})
        params.update(self.params)
        data = (
            json.dumps(request_data, cls=HGJSONEncoder)
            if request_data
            else None
        )

        response = requests.request(
            method=http_method,
            url=url,
            params=params,
            headers=headers,
            data=data,
            verify=verify
        )
        self.validate_response(response)
        return response

    def request_api(self, http_method, endpoint=None, params={}, request_data=None, headers={}, verify=True):
        """Request records from REST endpoint(s), returning response records."""
        resp = self._request(http_method, endpoint, params, request_data, headers, verify=verify)
        return resp

    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response."""
        if response.status_code in [429] or 500 <= response.status_code < 600:
            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)
        elif 400 <= response.status_code < 500:
            try:
                msg = response.text
            except:
                msg = self.response_error_message(response)
            raise FatalAPIError(msg)

    def response_error_message(self, response: requests.Response) -> str:
        """Build error message for invalid http statuses."""
        if 400 <= response.status_code < 500:
            error_type = "Client"
        else:
            error_type = "Server"

        return (
            f"{response.status_code} {error_type} Error: "
            f"{response.reason} for path: {self.endpoint}"
        )

    @staticmethod
    def clean_dict_items(dict):
        return {k: v for k, v in dict.items() if v not in [None, ""]}

    def clean_payload(self, item):
        item = self.clean_dict_items(item)
        output = {}
        for k, v in item.items():
            if isinstance(v, datetime):
                dt_str = v.strftime("%Y-%m-%dT%H:%M:%S%z")
                if len(dt_str) > 20:
                    output[k] = f"{dt_str[:-2]}:{dt_str[-2:]}"
                else:
                    output[k] = dt_str
            elif isinstance(v, dict):
                output[k] = self.clean_payload(v)
            else:
                output[k] = v
        return output

