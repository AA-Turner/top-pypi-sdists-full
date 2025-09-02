import logging
import requests
import warnings
from odecloud.api.exceptions import (
    HttpClientError,
    HttpNotFoundError,
    HttpServerError,
)

logger = logging.getLogger(__name__)


class RestResource:
    """
    Represents a RESTful resource to interact with Django REST Framework APIs.
    This class provides methods to make GET, POST, PATCH, and DELETE HTTP requests
    and dynamically constructs child resources through attribute access.

    Attributes:
        _session (requests.Session): The session to be used for HTTP requests.
        _base_url (str): The base URL of the REST resource.
        _store (dict): Additional data passed to the resource.
    """

    def __init__(self, session, base_url, **kwargs):
        """
        Initializes the RestResource instance.

        Args:
            session (requests.Session): The HTTP session for requests.
            base_url (str): The base URL for the resource.
            **kwargs: Additional keyword arguments for resource customization.
        """
        self._session = session
        self._base_url = base_url.rstrip('/') + '/'
        self._store = kwargs

    def __call__(self, id=None):
        """
        Allows calling an instance of RestResource with an ID to fetch a specific resource.

        Args:
            id (str, optional): The unique identifier of the resource.

        Returns:
            RestResource: A new RestResource instance for the specified ID.
        """
        return self._get_resource(id)

    def __getattr__(self, item):
        """
        Access child resources dynamically as attributes of the parent resource.

        Args:
            item (str): The name of the child resource.

        Returns:
            RestResource: A new RestResource instance representing the child resource.
        """
        if item.startswith("_"):
            raise AttributeError(item)
        return self._get_resource(item)

    def _get_resource(self, item=None):
        """
        Internal helper to create a new RestResource with an extended URL path.

        Args:
            item (str, optional): The path extension for the resource.

        Returns:
            RestResource: A new instance with the constructed URL path.
        """
        resource_url = f"{self._base_url}{item}/" if item else self._base_url
        return self.__class__(self._session, resource_url, **self._store)

    def _check_for_errors(self, resp):
        """
        Inspects the HTTP response and raises an appropriate exception for errors.

        Args:
            resp (requests.Response): The HTTP response to check.

        Raises:
            HttpNotFoundError: If the response indicates a 404 error.
            HttpClientError: If the response indicates a client-side error (4xx).
            HttpServerError: If the response indicates a server-side error (5xx).
        """
        if resp.status_code >= 400:
            if resp.status_code == 404:
                raise HttpNotFoundError(f"404 NOT FOUND: {resp.url}", response=resp)
            if 400 <= resp.status_code < 500:
                raise HttpClientError(f"{resp.status_code} CLIENT ERROR: {resp.url}", response=resp)
            if 500 <= resp.status_code < 600:
                raise HttpServerError(f"{resp.status_code} SERVER ERROR: {resp.url}", response=resp)

    def _process_response(self, resp):
        """
        Processes the HTTP response, checking for errors and decoding JSON content.

        Args:
            resp (requests.Response): The response from the server.

        Returns:
            dict or None: The JSON response content if status is 200, otherwise None.
        """
        self._check_for_errors(resp)
        return resp.json() if resp.status_code == 200 else None

    def get(self, **kwargs):
        """
        Makes a GET request to the resource.

        Args:
            **kwargs: Query parameters for the GET request.

        Returns:
            dict or None: The JSON response content.
        """
        resp = self._session.get(self._base_url, params=kwargs)
        return self._process_response(resp)

    def post(self, data=None, **kwargs):
        """
        Makes a POST request to the resource.

        Args:
            data (dict, optional): The JSON data to send in the request body.
            **kwargs: Additional parameters for the request.

        Returns:
            dict or None: The JSON response content.
        """
        resp = self._session.post(self._base_url, json=data, params=kwargs)
        return self._process_response(resp)

    def patch(self, data=None, **kwargs):
        """
        Makes a PATCH request to the resource.

        Args:
            data (dict, optional): The JSON data to send in the request body.
            **kwargs: Additional parameters for the request.

        Returns:
            dict or None: The JSON response content.
        """
        resp = self._session.patch(self._base_url, json=data, params=kwargs)
        return self._process_response(resp)

    def delete(self, data=None, **kwargs):
        """
        Makes a DELETE request to the resource.

        Args:
            data (dict, optional): The JSON data to send in the request body.
            **kwargs: Additional parameters for the request.

        Returns:
            bool: True if the resource was successfully deleted (status 204).
        """
        resp = self._session.delete(self._base_url, json=data, params=kwargs)
        return resp.status_code == 204


class _TimeoutHTTPAdapter(requests.adapters.HTTPAdapter):
    """Custom HTTP adapter for setting timeouts on HTTP requests."""

    def __init__(self, timeout=None, *args, **kwargs):
        """
        Initializes the adapter with a specified timeout.

        Args:
            timeout (float, optional): The timeout in seconds for HTTP requests.
        """
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        """
        Sends the HTTP request with the specified timeout.

        Args:
            *args: Arguments for the send method.
            **kwargs: Keyword arguments for the send method.

        Returns:
            requests.Response: The response object.
        """
        kwargs['timeout'] = self.timeout
        return super().send(*args, **kwargs)


class Api:
    """API client to interact with a Django REST Framework API."""

    resource_class = RestResource

    def __init__(self, base_url, client_key=None, client_secret=None, user_id=None, verify=True, timeout=None, retries=None):
        """
        Initializes the API client with credentials and session settings.

        Args:
            base_url (str): The base URL of the API.
            client_key (str, optional): Client key for authentication.
            client_secret (str, optional): Client secret for authentication.
            user_id (str, optional): User identifier for authentication.
            verify (bool): SSL verification for requests.
            timeout (float, optional): Timeout for HTTP requests.
            retries (int, optional): Number of retry attempts.
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = verify
        self._user_id = user_id

        if client_key and client_secret and user_id:
            self.session.headers.update({
                'x-client-key': client_key,
                'x-client-secret': client_secret
            })
        elif any((client_key, client_secret, user_id)):
            raise HttpClientError('Incomplete credentials provided.')

        warnings.warn("Please login, via login(), to access the API.")

        if timeout or retries is not None:
            adapter = _TimeoutHTTPAdapter(timeout=timeout)
            self.session.mount('https://', adapter)
            self.session.mount('http://', adapter)

    def url(self, section):
        """Constructs the URL for a specific API section."""
        return f'{self.base_url}/{section}/'
    
    def user_id(self):
        return self._user_id
    
    def user_auth_token(self):
        return self.session.headers

    def login(self, email, password, app_url):
        """Log in to the API using provided credentials."""
        secret_code = self._request_secret(email, password, app_url)
        response = self.session.post(self.url('oauth/login'), json={'secret': secret_code})
        if response.status_code == 201:
            self._update_credentials(response.json())
        else:
            raise HttpServerError(f'ERROR {response.status_code}: {response.content.decode()}')

    def _request_secret(self, email, password, app_url):
        """Request a secret code for login."""
        response = self.session.post(self.url('oauth/request'), json={'email': email, 'password': password, 'appUrl': app_url})
        if response.status_code == 201:
            secret_data = response.json()
            return secret_data.get('secret')
        raise HttpServerError(f'ERROR {response.status_code}: {response.content.decode()}')

    def _update_credentials(self, client_credentials):
        """Update client credentials after successful login."""
        self._user_id = client_credentials.get('userId')
        self.session.headers.update({
            'x-client-key': client_credentials.get('clientKey'),
            'x-client-secret': client_credentials.get('clientSecret'),
        })

    def logout(self):
        """Log out of the API."""
        self._user_id = None
        self.session.headers.pop('x-client-key', None)
        self.session.headers.pop('x-client-secret', None)

    def __call__(self, id):
        return self.resource_class(session=self.session, base_url=self.url(id))

    def __getattr__(self, item):
        """Dynamic attribute access for resources."""
        if item.startswith("_"):
            raise AttributeError(item)
        return self.resource_class(session=self.session, base_url=self.url(item))
