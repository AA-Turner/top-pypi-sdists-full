# Copyright 2025 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import requests
from gql.transport import Transport
from gql.transport.exceptions import (
    TransportAlreadyConnected,
    TransportClosed,
    TransportProtocolError,
    TransportServerError,
)
from graphql import (
    DocumentNode,
    ExecutionResult,
    print_ast,
)

if TYPE_CHECKING:
    from qctrlclient.auth.base import BaseAuth


class RequestsTransport(Transport):
    """Transport class using the `requests` package."""

    def __init__(
        self,
        url: str,
        auth: BaseAuth | None = None,
        headers: dict[str, str] | None = None,
        retries: int = 0,
        json_encoder: type[json.JSONEncoder] = json.JSONEncoder,
    ):
        self._url = url
        self._auth = auth
        self._headers = headers or {}
        self._retries = retries
        self._json_encoder = json_encoder

        self._session: requests.Session | None = None

    def connect(self) -> None:
        """Creates a `requests` session."""
        if self._session is None:
            self._session = requests.Session()

            if self._retries > 0:
                adapter = requests.adapters.HTTPAdapter(
                    max_retries=requests.adapters.Retry(
                        total=self._retries,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504],
                        allowed_methods=None,
                    )
                )
                for prefix in "http://", "https://":
                    self._session.mount(prefix, adapter)
        else:
            raise TransportAlreadyConnected("Transport is already connected")

    def _send_request(self, payload: dict[str, Any]) -> requests.Response:
        headers = {"Content-Type": "application/json"}
        headers.update(self._headers)

        if self._session is None:
            raise RuntimeError("Session not created. Run `connect`.")

        return self._session.post(
            self._url,
            auth=self._auth,
            headers=headers,
            data=json.dumps(payload, cls=self._json_encoder),
        )

    def _build_payload(
        self,
        document: DocumentNode,
        variable_values: dict[str, Any] | None = None,
        operation_name: str | None = None,
    ) -> dict[str, Any]:
        query_str = print_ast(document)
        payload: dict[str, Any] = {"query": query_str}

        if variable_values:
            payload["variables"] = variable_values

        if operation_name:
            payload["operationName"] = operation_name

        return payload

    def _get_result_data(self, response: requests.Response) -> dict[str, Any]:
        try:
            response.raise_for_status()
            result = response.json()

        # invalid HTTP response
        except requests.HTTPError as exc:
            status_code = exc.response.status_code
            raise TransportServerError(str(exc), status_code) from exc

        # invalid response body
        except requests.exceptions.JSONDecodeError as exc:
            raise TransportProtocolError(f"Invalid response format: {exc!s}") from exc

        # invalid response data
        if "errors" not in result and "data" not in result:
            raise TransportProtocolError('No "data" or "errors" keys in response data')

        return result

    def execute(
        self,
        document: DocumentNode,
        variable_values: dict[str, Any] | None = None,
        operation_name: str | None = None,
        **__: Any,
    ) -> ExecutionResult:
        """Sends the GraphQL request."""
        if not self._session:
            raise TransportClosed("Transport is not connected")

        payload = self._build_payload(document, variable_values, operation_name)
        response = self._send_request(payload)
        result = self._get_result_data(response)

        return ExecutionResult(
            errors=result.get("errors"),
            data=result.get("data"),
            extensions=result.get("extensions"),
        )

    def close(self) -> None:
        """Closes the `requests` session."""
        if self._session:
            self._session.close()
            self._session = None
