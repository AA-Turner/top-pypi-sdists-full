import requests

from typing import Any
from ..utils import ApiRequestHandler, TokenSource


class WebhookService:
    """Webhook service implementation."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the conversation service.

        Args:
            api_domain: Base URL for the API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def trigger(
        self,
        webhook_id: str,
        data: dict[str, Any] = None,
        extra_headers: dict[str, str] = None,
    ) -> requests.Response:
        """Trigger a webhook by sending a POST request with the provided data.

        Args:
            webhook_id: Webhook ID to trigger
            data: Request body data. Defaults to {"test": "data"} if not provided
            extra_headers: Optional additional HTTP headers (e.g. GitLab's
                X-Gitlab-Token / X-Gitlab-Event webhook delivery headers)

        Returns:
            Response object from requests library
        """
        if data is None:
            data = {"test": "data"}

        return self._api.post(
            f"/v1/webhooks/{webhook_id}",
            response_model=requests.Response,
            json_data=data,
            wrap_response=False,
            raise_on_error=False,
            include_auth=False,
            extra_headers=extra_headers,
        )

    def validate_msgraph_subscription(
        self,
        webhook_id: str,
        validation_token: str,
    ) -> requests.Response:
        """Simulate the Microsoft Graph subscription validation handshake.

        Microsoft Graph sends a POST request with validationToken as a query
        parameter when validating a notification URL. The endpoint must respond
        with HTTP 200, Content-Type: text/plain, and the exact token as the body.

        Args:
            webhook_id: Webhook ID whose notification URL is being validated
            validation_token: The token Microsoft Graph expects echoed back

        Returns:
            Raw Response object for the caller to inspect status, headers, and body
        """
        return self._api.post(
            f"/v1/webhooks/{webhook_id}",
            response_model=requests.Response,
            params={"validationToken": validation_token},
            wrap_response=False,
            raise_on_error=False,
            include_auth=False,
        )
