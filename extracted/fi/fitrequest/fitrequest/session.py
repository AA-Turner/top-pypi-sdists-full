import logging
from typing import Any

import httpx

from fitrequest.auth import Auth
from fitrequest.method_config import MethodConfig
from fitrequest.response import Response
from fitrequest.utils import extract_method_params, extract_url_params

logger = logging.getLogger(__name__)


class Session:
    synchronous: httpx.Client
    asynchronous: httpx.AsyncClient

    def __init__(
        self,
        client_name: str,
        version: str,
        auth: Auth | dict | None = None,
        base_url: str | None = None,
        headers: dict | None = None,
        **kwargs,
    ) -> None:
        self.update(client_name=client_name, version=version, auth=auth, base_url=base_url, headers=headers, **kwargs)

    def authenticate(self) -> None:
        """
        Retrieve the necessary data for authentication
        and configure the auth attribute for both synchronous and asynchronous clients.
        """
        if self.raw_auth is None:
            return
        auth = Auth(**self.raw_auth) if isinstance(self.raw_auth, dict) else self.raw_auth

        # auth.authentication property retrieves necessary data for authentication
        self.synchronous.auth = auth.authentication
        self.asynchronous.auth = auth.authentication

    def update(
        self,
        client_name: str | None = None,
        version: str | None = None,
        auth: Auth | dict | None = None,
        base_url: str | None = None,
        headers: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Update the session used by generated methods.

        It effectively drops the existing synchronous and asynchronous sessions
        and creates a new ones using the specified arguments.

        Additional keyword arguments are passed directly to the ``httpx`` clients during initialization.

        This method does not trigger a new authentication process.
        If you need to perform a new authentication, use the ``authenticate`` method.
        """
        self.client_name = client_name or getattr(self, 'client_name', None)
        self.version = version or getattr(self, 'version', None)
        self.base_url = base_url or getattr(self, 'base_url', None)
        self.raw_auth = auth or getattr(self, 'raw_auth', None)

        self.default_headers = {'User-Agent': f'fitrequest.{self.client_name}.{self.version}'} | (headers or {})

        self.config = {
            'headers': self.default_headers,
            'follow_redirects': True,
            'timeout': 60,
        } | kwargs

        # Close previous sessions
        if hasattr(self, 'synchronous'):
            self.synchronous.close()

        if hasattr(self, 'asynchronous'):
            self.synchronous.close()

        # Create new session with updated parameters
        self.asynchronous = httpx.AsyncClient(transport=httpx.AsyncHTTPTransport(), **self.config)
        self.synchronous = httpx.Client(transport=httpx.HTTPTransport(), **self.config)

    def request(
        self,
        method_config: MethodConfig,
        raise_for_status: bool | None = None,
        filepath: str | None = None,
        **kwargs,
    ) -> Any:
        """
        Sends a request to a URL created based on the provided MethodConfig.

        Any keyword arguments (kwargs) you provide will be used as named variables to build the final URL,
        and some of these kwargs are also passed directly to the httpx.request method.

        You can optionally supply a custom URL, which will take priority over the generated one.
        If a custom URL with hardcoded parameters is provided along with the argument "params" (in kwargs),
        both sets of parameters are combined, giving priority to those in the custom URL over the ones in "params."
        """

        if raise_for_status is None:
            raise_for_status = method_config.raise_for_status

        if self.base_url:
            method_config.base_url = self.base_url

        method_params = {key: val for key, val in kwargs.pop('params', {}).items() if val is not None}
        custom_url, custom_url_params = extract_url_params(kwargs.pop('url', None))
        config_url, config_url_params = extract_url_params(method_config.url(**kwargs))
        custom_method = kwargs.pop('method', None)

        if custom_url_params:
            params = method_params | custom_url_params
        elif config_url_params:
            params = method_params | config_url_params
        elif method_params:
            params = method_params
        else:
            params = None

        request_args = {
            'method': custom_method or method_config.request_verb.value,
            'url': custom_url or config_url,
            'params': params,
        } | extract_method_params(httpx.request, kwargs)

        logger.info('Sending a synchronous httpx request.', extra=request_args | {'client': self.client_name})
        httpx_response = self.synchronous.request(**request_args)

        response = Response(
            client_name=self.client_name,
            httpx_response=httpx_response,
            json_path=method_config.json_path,
            raise_for_status=raise_for_status,
            response_model=method_config.response_model,
        )

        if filepath and method_config.save_method:
            response.save_data(filepath)
            return None
        return response.data

    async def async_request(
        self,
        method_config: MethodConfig,
        raise_for_status: bool | None = None,
        filepath: str | None = None,
        **kwargs,
    ) -> Any:
        """Async version of the request method."""
        if raise_for_status is None:
            raise_for_status = method_config.raise_for_status

        if self.base_url:
            method_config.base_url = self.base_url

        method_params = {key: val for key, val in kwargs.pop('params', {}).items() if val is not None}
        custom_url, custom_url_params = extract_url_params(kwargs.pop('url', None))
        config_url, config_url_params = extract_url_params(method_config.url(**kwargs))
        custom_method = kwargs.pop('method', None)

        if custom_url_params:
            params = method_params | custom_url_params
        elif config_url_params:
            params = method_params | config_url_params
        elif method_params:
            params = method_params
        else:
            params = None

        request_args = {
            'method': custom_method or method_config.request_verb.value,
            'url': custom_url or config_url,
            'params': params,
        } | extract_method_params(httpx.request, kwargs)

        logger.info('Sending an asynchronous httpx request.', extra=request_args | {'client': self.client_name})
        httpx_response = await self.asynchronous.request(**request_args)

        response = Response(
            client_name=self.client_name,
            httpx_response=httpx_response,
            json_path=method_config.json_path,
            raise_for_status=raise_for_status,
            response_model=method_config.response_model,
        )

        if filepath and method_config.save_method:
            await response.async_save_data(filepath)
            return None
        return response.data
