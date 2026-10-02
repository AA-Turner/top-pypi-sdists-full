# Copyright 2023 Agnostiq Inc.

import re
from urllib.parse import parse_qs, urlparse

import requests
import requests.adapters
from furl import furl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from covalent_cloud.service_account_interface.auth_config_manager import AuthConfigManager
from covalent_cloud.shared.classes.settings import Settings, settings


class APIClient:

    api_key: str
    uri_components: furl
    auth_config: AuthConfigManager

    @property
    def host(self):
        return self.uri_components.host

    @property
    def port(self):
        return self.uri_components.port

    @property
    def scheme(self):
        return self.uri_components.scheme

    def __init__(
        self, host_uri, port=None, headers=None, settings=None, url_prefix="", max_retries=5
    ) -> None:
        if headers is None:
            headers = {}
        if settings is None:
            settings = Settings()

        self.uri_components = furl(host_uri)
        self.settings = settings
        self.headers = headers
        self.url_prefix = url_prefix

        self._adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)

        if port:
            self.uri_components.set(port=port)

    def get_global_headers(self):
        auth_headers = AuthConfigManager.get_auth_request_headers(self.settings)
        return {**auth_headers, **self.headers}

    def get_request_options(self, request_options):
        request_options = request_options or {}
        provided_headers = request_options.get("headers") or {}
        options = {
            **request_options,
            "headers": {
                **self.get_global_headers(),
                **provided_headers,
            },
        }
        return options

    def prepare_request(self, endpoint, request_options=None):
        uri_components = self.uri_components.copy()
        uri_components.path = uri_components.path / self.url_prefix / endpoint
        uri = uri_components.url
        options = self.get_request_options(request_options)
        return uri, options

    def post(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)
        with requests.Session() as session:
            session.mount("http://", self._adapter)
            session.mount("https://", self._adapter)
            res = session.post(uri, **options)

        res.raise_for_status()
        return res

    def get(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)

        with requests.Session() as session:
            session.mount("http://", self._adapter)
            session.mount("https://", self._adapter)
            res = session.get(uri, **options)
        res.raise_for_status()
        return res

    def delete(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)
        with requests.Session() as session:
            session.mount("http://", self._adapter)
            session.mount("https://", self._adapter)
            res = session.delete(uri, **options)
        res.raise_for_status()
        return res

    def put(self, endpoint, request_options=None):
        uri, options = self.prepare_request(endpoint, request_options)
        with requests.Session() as session:
            session.mount("http://", self._adapter)
            session.mount("https://", self._adapter)
            res = session.put(uri, **options)
        res.raise_for_status()
        return res


class DispatcherAPI(APIClient):
    def __init__(self, headers=None, settings: Settings = settings) -> None:
        if headers is None:
            headers = {}

        super().__init__(
            host_uri=settings.dispatcher_uri,
            port=settings.dispatcher_port,
            headers=headers,
            settings=settings,
        )


class DeploymentAPI(APIClient):
    def __init__(self, headers=None, settings: Settings = settings) -> None:
        if headers is None:
            headers = {}

        # To test local run:
        # super().__init__(
        #     host_uri="http://127.0.0.1",
        #     port=8080,
        #     headers=headers,
        #     settings=settings,
        #     url_prefix="/api/v0",
        # )

        # This uses the same uri and port as the dispatcher but with url_prefix added
        super().__init__(
            host_uri=settings.dispatcher_uri,
            port=settings.dispatcher_port,
            headers=headers,
            settings=settings,
            url_prefix="/fn/api/v0",
        )


class AssetAPIClient:
    """
    Specialized API client for asset upload/download operations that intelligently
    handles authentication headers based on the target URL type.

    For AWS S3 presigned URLs, no authentication headers are added since S3 expects
    the authentication to be embedded in the presigned URL itself.
    For other URLs, standard authentication headers are included.
    """

    def __init__(self, settings: Settings = None) -> None:
        if settings is None:
            settings = Settings()
        self.settings = settings

    def is_s3_presigned_url(self, url: str) -> bool:
        """
        Determine if a URL is an AWS S3 presigned URL.

        Args:
            url: The URL to check

        Returns:
            True if the URL appears to be an S3 presigned URL, False otherwise
        """
        try:
            parsed = urlparse(url)
            hostname = parsed.hostname

            if not hostname:
                return False

            # Check for S3 hostname patterns
            s3_patterns = [
                r"\.s3\.amazonaws\.com$",
                r"\.s3-[a-z0-9-]+\.amazonaws\.com$",
                r"^s3\.[a-z0-9-]+\.amazonaws\.com$",
                r"\.s3\.[a-z0-9-]+\.amazonaws\.com$",
            ]

            is_s3_hostname = any(re.search(pattern, hostname.lower()) for pattern in s3_patterns)

            if not is_s3_hostname:
                return False

            # Additional check for S3 presigned URL query parameters
            query_params = parse_qs(parsed.query)

            # Check for both Signature V4 and V2 presigned URL parameters.
            # Different backends currently return different signature versions:
            # - Function Serve backend (/fn/api/v0/assets) returns Signature V2 URLs
            # - Dispatch backend (/api/v2/lattices) returns Signature V4 URLs
            # Both are valid AWS presigned URL formats that embed authentication in the URL,
            # so no additional auth headers should be added for either version.
            s3_presigned_params_v4 = ["X-Amz-Signature", "X-Amz-Algorithm", "X-Amz-Credential"]
            s3_presigned_params_v2 = ["AWSAccessKeyId", "Signature", "Expires"]

            has_v4_params = any(param in query_params for param in s3_presigned_params_v4)
            has_v2_params = any(param in query_params for param in s3_presigned_params_v2)

            return has_v4_params or has_v2_params

        except Exception:
            # If URL parsing fails, assume it's not S3
            return False

    def get_headers(self, url: str) -> dict:
        """
        Get appropriate headers for uploading/downloading to/from the given URL.

        Args:
            url: The target upload/download URL

        Returns:
            Dictionary of headers to include in the request
        """
        if self.is_s3_presigned_url(url):
            # For S3 presigned URLs, don't include auth headers
            return {}
        else:
            # For non-S3 URLs, include authentication headers
            return AuthConfigManager.get_auth_request_headers(self.settings)

    def upload_asset(
        self, url: str, data: bytes, additional_headers: dict = None
    ) -> requests.Response:
        """
        Upload asset data to the given URL with appropriate headers.

        Args:
            url: The target upload URL
            data: The asset data to upload
            additional_headers: Optional additional headers to include

        Returns:
            The response from the upload request

        Raises:
            requests.exceptions.HTTPError: If the upload fails
        """
        headers = self.get_headers(url)

        # Add any additional headers (like Content-Length for empty files)
        if additional_headers:
            headers.update(additional_headers)

        # Set up retry strategy
        retry_strategy = Retry(
            total=5,
            backoff_factor=0.1,
            allowed_methods={"PUT"},
            status_forcelist=[500, 502, 503, 504],
        )

        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        session.mount("http://", HTTPAdapter(max_retries=retry_strategy))

        response = session.put(url, headers=headers, data=data)
        response.raise_for_status()

        return response

    def download_asset(self, url: str) -> requests.Response:
        """
        Download asset from the given URL with appropriate headers.

        For S3 presigned URLs, no authentication headers are added since authentication
        is embedded in the presigned URL itself.
        For proxy URLs (e.g., /api/v2/assets/), authentication headers are included.

        Args:
            url: The source download URL

        Returns:
            The streaming response from the download request

        Raises:
            requests.exceptions.HTTPError: If the download fails
        """
        # Reuse the same header logic as uploads
        headers = self.get_headers(url)

        # Set up retry strategy for GET requests
        retry_strategy = Retry(
            total=5,
            backoff_factor=0.1,
            allowed_methods={"GET", "HEAD"},
            status_forcelist=[500, 502, 503, 504],
        )

        session = requests.Session()
        session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        session.mount("http://", HTTPAdapter(max_retries=retry_strategy))

        response = session.get(url, headers=headers, stream=True)

        return response
