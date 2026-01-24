from typing import Callable, Optional
from urllib.parse import urljoin

import requests
import semver
import warnings

from nexuscli import exception
from nexuscli.nexus_config import NexusConfig


class NexusHttp:
    def __init__(self, config: NexusConfig = None):
        self.config: NexusConfig = config or NexusConfig()
        self._server_version: Optional[str] = None

        self._create_method_attributes()

    def _create_method_attributes(self) -> None:
        def request_stub(http_method) -> Callable:
            def f(endpoint, **kwargs):
                return self.request(http_method, endpoint, **kwargs)
            return f

        for method_name in ['head', 'post', 'put', 'delete']:
            setattr(self, method_name, request_stub(method_name))

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Performs a HTTP GET request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        """
        return self.request('get', endpoint, stream=True, **kwargs)

    @property
    def rest_url(self) -> str:
        """
        Full URL to the Nexus REST API, based on the ``url`` and ``version``
        from :attr:`config`.

        :rtype: str
        """
        return urljoin(self.config.url, 'service/rest/')

    @property
    def service_url(self) -> str:
        """
        Full URL to the Nexus REST API, based on the ``url`` and ``version``
        from :attr:`config`.

        :rtype: str
        """
        return urljoin(self.rest_url, self.config.api_version + '/')

    def request(
            self, method: str, endpoint: str, service_url: Optional[str] = None,
            **kwargs) -> requests.Response:
        """
        Performs a HTTP request to the Nexus REST API on the specified
        endpoint.

        :param method: one of ``get``, ``put``, ``post``, ``delete``.
        :param endpoint: URI path to be appended to the service URL.
        :param service_url: override the default URL to use for the request,
            which is created by joining :attr:`rest_url` and ``endpoint``.
        :param kwargs: as per :py:func:`requests.request`.
        """
        service_url = service_url or self.service_url
        url = urljoin(service_url, endpoint)

        try:
            response = requests.request(
                method=method, auth=self.config.auth, url=url,
                verify=self.config.x509_verify, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise exception.NexusClientConnectionError(str(e)) from None

        if response.status_code == 401:
            raise exception.NexusClientInvalidCredentials('Try running `nexus3 login`')

        return response

    @property
    def server_version(self) -> Optional[semver.VersionInfo]:
        """
        Parse the Server header from a Nexus request response and return
        as version information. The method expects the header Server to be
        present and formatted as, e.g., 'Nexus/3.19.1-01 (OSS)'

        :return: the parsed version. If it can't be determined, return None.
        :rtype: Union[None,semver.VersionInfo]
        """
        if self._server_version is None:
            response = self.get('', service_url=self.config.url)

            if response.status_code != 200:
                raise exception.NexusClientAPIError(response.reason)

            server = response.headers.get('Server')

            if server is None:
                return None

            try:
                maybe_semver = server.split(' ')[0].split('/')[1].split('-')[0]
                version = semver.VersionInfo.parse(maybe_semver)
            except (IndexError, ValueError):
                warnings.warn(f'Nexus server version cannot be parsed: {server}')
                version = None

            self._server_version = version
        return self._server_version
