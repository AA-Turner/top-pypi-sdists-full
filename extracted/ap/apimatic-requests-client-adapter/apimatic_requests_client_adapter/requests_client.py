# -*- coding: utf-8 -*-
from apimatic_core_interfaces.client.http_client_provider import HttpClientProvider
from requests.packages import urllib3
from cachecontrol import CacheControl
from apimatic_core_interfaces.client.http_client import HttpClient
from apimatic_core_interfaces.types.http_method_enum import HttpMethodEnum
from requests import session, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RequestsClient(HttpClient):
    """An implementation of CoreHttpClient that uses Requests as its HTTP Client

    Attributes:
        timeout (int): The default timeout for all API requests.

    """

    def __init__(self,
                 timeout=60,
                 cache=False,
                 max_retries=None,
                 backoff_factor=None,
                 retry_statuses=None,
                 retry_methods=None,
                 verify=True,
                 http_client_instance=None,
                 override_http_client_configuration=False,
                 response_factory=None,
                 proxies=None):
        """Initialize the HTTP client configuration.

        Args:
            timeout (float): Default timeout (in seconds) for all HTTP requests.
            cache (bool): Whether to enable caching in the HTTP client.
            max_retries (int): Total number of retries to allow.
            backoff_factor (float): Backoff factor between retry attempts after failures.
            retry_statuses (iterable): HTTP status codes that should trigger retries.
            retry_methods (iterable): HTTP methods that should be retried.
            verify (bool): Whether to verify SSL certificates for requests.
            http_client_instance (Union[Session, HttpClientProvider, Any]): Custom HTTP client instance to use.
            override_http_client_configuration (bool): Whether to override settings for a custom HTTP client.
            response_factory (ResponseFactory): Converts raw responses to SDK response objects.
            proxies (Dict[str, str]): Proxy mapping for network requests.
        """
        if not verify:
            # Disable SSL warnings if verification is disabled
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        http_session = self._get_http_session(http_client_instance)

        if http_session is not None:
            self._configure_http_session(
                http_session,
                override_http_client_configuration,
                verify,
                max_retries,
                backoff_factor,
                retry_statuses,
                retry_methods,
            )
            self.timeout = http_client_instance.timeout\
                if not override_http_client_configuration and hasattr(http_client_instance, "timeout")\
                else timeout
            self.session = http_session
        else:
            # When No custom HTTP client provided → create a default client
            self.create_default_http_client(
                timeout,
                cache,
                max_retries,
                backoff_factor,
                retry_statuses,
                retry_methods,
                verify,
                proxies,
            )

        self.response_factory = response_factory

    def create_default_http_client(self,
                                   timeout=60,
                                   cache=False,
                                   max_retries=None,
                                   backoff_factor=None,
                                   retry_statuses=None,
                                   retry_methods=None,
                                   verify=True,
                                   proxies=None):
        """creates the default instance of HTTP client.

        Args:
            timeout (float): The default global timeout(seconds).
            cache (bool): Flag to enable/disable cache in the http client.
            max_retries (int): Total number of retries to allow.
            backoff_factor (float): A backoff factor to apply between attempts after the second try.
            retry_statuses (iterable): A set of integer HTTP status codes that we should force a retry on.
            retry_methods (iterable): Set of HTTP method verbs that we should retry on.
            verify (bool): Flag to enable/disable verification of SSL certificate on the host.
            proxies (Dict[str, str]): A dictionary mapping protocol to the URL of the proxy.

        """
        self.timeout = timeout
        self.session = session()

        if cache:
            self.session = CacheControl(self.session)

        retry_strategy = Retry(total=max_retries, backoff_factor=backoff_factor, status_forcelist=retry_statuses,
                               allowed_methods=retry_methods, raise_on_status=False, raise_on_redirect=False)
        self.session.mount('http://', HTTPAdapter(max_retries=retry_strategy))
        self.session.mount('https://', HTTPAdapter(max_retries=retry_strategy))
        if proxies is not None:
            self.session.proxies.update(proxies)
        self.session.verify = verify

    def _configure_http_session(self, client_session, should_override, verify_ssl,
                                max_retries, backoff_factor,
                                retry_statuses, retry_methods):
        """Configure retry strategy and SSL verification for a given session.

        Args:
            client_session (Session): The HTTP session object to configure.
            should_override (bool): Flag to determine if configuration should be overridden.
            verify_ssl (bool): Whether to verify SSL certificates.
            max_retries (int): Total number of retries to allow.
            backoff_factor (float): A backoff factor to apply between retry attempts.
            retry_statuses (iterable): Set of HTTP status codes that should trigger a retry.
            retry_methods (iterable): Set of HTTP methods that should be retried.
        """
        if not should_override:
            return

        # Apply SSL verification and retry configuration
        client_session.verify = verify_ssl
        self.update_retry_strategy(
            client_session,
            max_retries,
            backoff_factor,
            retry_statuses,
            retry_methods,
        )

    def force_retries(self, request, should_retry=None):
        """Reset retries according to each request

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            should_retry (boolean): whether to retry on a particular request

        """
        adapters = self.session.adapters
        if should_retry is False:
            for adapter in adapters.values():
                adapter.max_retries = False
        elif should_retry is True:
            for adapter in adapters.values():
                adapter.max_retries.allowed_methods = [request.http_method]

    def execute(self, request, endpoint_configuration):
        """Execute a given HttpRequest to get a string response back

        Args:
            request (HttpRequest): The given HttpRequest to execute.
            endpoint_configuration (EndpointConfiguration): The endpoint configurations to use.

        Returns:
            CoreHttpResponse: The response of the HttpRequest.

        """

        old_adapters = self.session.adapters
        self.force_retries(request, endpoint_configuration.should_retry)
        response = self.session.request(
            HttpMethodEnum.to_string(request.http_method),
            request.query_url,
            headers=request.headers,
            params=request.query_parameters,
            data=request.parameters,
            files=request.files,
            timeout=self.timeout
        )

        self.session.adapters = old_adapters
        return self.convert_response(response, endpoint_configuration.contains_binary_response, request)

    def convert_response(self, response, contains_binary_response, http_request):
        """Converts the Response object of the CoreHttpClient into an
        CoreHttpResponse object.

        Args:
            response (dynamic): The original response object.
            contains_binary_response (bool): The flag to check if the response is of binary type.
            http_request (HttpRequest): The original HttpRequest object.

        Returns:
            CoreHttpResponse: The converted CoreHttpResponse object.

        """
        response_body = response.content if contains_binary_response else response.text

        return self.response_factory.create(
            response.status_code,
            response.reason,
            response.headers,
            response_body,
            http_request
        )

    @staticmethod
    def update_retry_strategy(custom_session,
                              max_retries=None,
                              backoff_factor=None,
                              retry_statuses=None,
                              retry_methods=None):
        """Updates the retry strategy for the provided http client instance

        Args:
            custom_session (Session): The session of the http client instance to update.
            max_retries (int): Total number of retries to allow.
            backoff_factor (float): A backoff factor to apply between attempts after the second try.
            retry_statuses (iterable): A set of integer HTTP status codes that we should force a retry on.
            retry_methods (iterable): Set of HTTP method verbs that we should retry on.
        """
        adapters = custom_session.adapters
        for adapter in adapters.values():
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'total'):
                adapter.max_retries.total = max_retries
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'backoff_factor'):
                adapter.max_retries.backoff_factor = backoff_factor
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'status_forcelist'):
                adapter.max_retries.status_forcelist = retry_statuses
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'allowed_methods'):
                adapter.max_retries.allowed_methods = retry_methods
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'raise_on_status'):
                adapter.max_retries.raise_on_status = False
            if hasattr(adapter, 'max_retries') and hasattr(adapter.max_retries, 'raise_on_redirect'):
                adapter.max_retries.raise_on_redirect = False

    @staticmethod
    def _get_http_session(http_client_instance):
        if http_client_instance is None:
            return None

        if isinstance(http_client_instance, Session):
            return http_client_instance

        if isinstance(http_client_instance, HttpClientProvider):
            return http_client_instance.session

        return getattr(http_client_instance, "session", None)
