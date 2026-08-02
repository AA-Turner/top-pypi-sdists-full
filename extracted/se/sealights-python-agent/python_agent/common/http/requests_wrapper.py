import logging
import os

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import (
    Timeout,
    ConnectionError as RequestsConnectionError,
    SSLError,
    HTTPError,
)
from urllib3.util.retry import Retry

from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates

log = logging.getLogger(__name__)


_DEFAULT_MAX_RETRIES = 3
_DEFAULT_BACKOFF_FACTOR = 1.0


class Requests(object):
    def __init__(self, config_data):
        self.config_data = config_data
        self.session = requests.Session()
        try:
            max_retries = int(
                os.environ.get("SL_HTTP_MAX_RETRIES", _DEFAULT_MAX_RETRIES)
            )
        except (ValueError, TypeError):
            log.warning(
                "Invalid value for SL_HTTP_MAX_RETRIES: '%s'. Using default %d.",
                os.environ.get("SL_HTTP_MAX_RETRIES"),
                _DEFAULT_MAX_RETRIES,
            )
            max_retries = _DEFAULT_MAX_RETRIES
        try:
            backoff_factor = float(
                os.environ.get("SL_HTTP_BACKOFF_FACTOR", _DEFAULT_BACKOFF_FACTOR)
            )
        except (ValueError, TypeError):
            log.warning(
                "Invalid value for SL_HTTP_BACKOFF_FACTOR: '%s'. Using default %.1f.",
                os.environ.get("SL_HTTP_BACKOFF_FACTOR"),
                _DEFAULT_BACKOFF_FACTOR,
            )
            backoff_factor = _DEFAULT_BACKOFF_FACTOR
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _handle_request_exception(self, exception, method, url):
        """Handle request exceptions and render appropriate console messages."""
        if isinstance(exception, SSLError):
            if "certificate" in str(exception).lower():
                ConsoleMessageTemplates.render_and_print(
                    "common.error-network.invalid-certificate"
                )
            else:
                ConsoleMessageTemplates.render_and_print(
                    "common.error-network.ssl-handshake-error"
                )
        elif isinstance(exception, Timeout):
            ConsoleMessageTemplates.render_and_print(
                "common.error-network.connection-timeout"
            )
        elif isinstance(exception, RequestsConnectionError):
            ConsoleMessageTemplates.render_and_print(
                "common.error-network.network-connectivity-failure"
            )
        elif isinstance(exception, HTTPError):
            status_code = exception.response.status_code if exception.response else None
            if status_code == 401:
                # Determine token type from config
                token_type = (
                    "agent token"
                    if hasattr(self.config_data, "token")
                    else "unknown token"
                )
                ConsoleMessageTemplates.render_and_print(
                    "common.error-network.unauthorized-error", tokenType=token_type
                )
            elif status_code == 408:
                ConsoleMessageTemplates.render_and_print(
                    "common.error-network.request-timeout"
                )
            elif status_code and status_code >= 500:
                ConsoleMessageTemplates.render_and_print(
                    "common.error-network.internal-server-error"
                )

        log.debug(f"Request {method} to {url} failed: {exception}")
        raise

    def patch_request(
        self, url, patch_content_type, kwargs, add_metadata=False, sl_metadata=None
    ):
        kwargs.update({"verify": False, "timeout": 120})
        if self.config_data.proxy:
            kwargs["proxies"] = {
                "http": self.config_data.proxy,
                "https": self.config_data.proxy,
            }
        headers = kwargs.setdefault("headers", {})
        if patch_content_type:
            headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer %s" % self.config_data.token
        if add_metadata:
            headers["x-sl-appname"] = self.config_data.appName
            headers["x-sl-branchname"] = self.config_data.branchName
            headers["x-sl-buildname"] = self.config_data.buildName
            headers["x-sl-bsid"] = self.config_data.buildSessionId
            headers["x-sl-messagetype"] = "1003"
            if self.config_data.labId:
                headers["x-sl-labid"] = self.config_data.labId
        if sl_metadata:
            headers["X-SL-METADATA"] = sl_metadata.to_json()
        if self.config_data.testProjectId:
            headers["x-sl-testprojectid"] = self.config_data.testProjectId
        if self.config_data.prID:
            headers["x-sl-prid"] = self.config_data.prID
        if (url is not None) and (
            url.lower().startswith("http://") or url.lower().startswith("https://")
        ):
            return url
        return self.config_data.server + url

    def get(
        self,
        url,
        params=None,
        patch_content_type=True,
        add_metadata=False,
        sl_metadata=None,
        **kwargs,
    ):
        url = self.patch_request(
            url, patch_content_type, kwargs, add_metadata, sl_metadata
        )
        try:
            response = self.session.get(url, params=params, **kwargs)
            response.raise_for_status()
            return response
        except (SSLError, Timeout, RequestsConnectionError, HTTPError) as e:
            self._handle_request_exception(e, "GET", url)
        except Exception as e:
            log.error(f"Unexpected error during GET request to {url}: {e}")
            raise

    def post(
        self,
        url,
        data=None,
        json=None,
        patch_content_type=True,
        add_metadata=False,
        sl_metadata=None,
        **kwargs,
    ):
        url = self.patch_request(
            url, patch_content_type, kwargs, add_metadata, sl_metadata
        )
        try:
            response = self.session.post(url, data=data, json=json, **kwargs)
            response.raise_for_status()
            return response
        except (SSLError, Timeout, RequestsConnectionError, HTTPError) as e:
            self._handle_request_exception(e, "POST", url)
        except Exception as e:
            log.error(f"Unexpected error during POST request to {url}: {e}")
            raise

    def put(
        self,
        url,
        data=None,
        patch_content_type=True,
        add_metadata=False,
        sl_metadata=None,
        **kwargs,
    ):
        url = self.patch_request(
            url, patch_content_type, kwargs, add_metadata, sl_metadata
        )
        try:
            response = self.session.put(url, data=data, **kwargs)
            response.raise_for_status()
            return response
        except (SSLError, Timeout, RequestsConnectionError, HTTPError) as e:
            self._handle_request_exception(e, "PUT", url)
        except Exception as e:
            log.error(f"Unexpected error during PUT request to {url}: {e}")
            raise

    def patch(
        self,
        url,
        data=None,
        patch_content_type=True,
        add_metadata=False,
        sl_metadata=None,
        **kwargs,
    ):
        url = self.patch_request(
            url, patch_content_type, kwargs, add_metadata, sl_metadata
        )
        try:
            response = self.session.patch(url, data=data, **kwargs)
            response.raise_for_status()
            return response
        except (SSLError, Timeout, RequestsConnectionError, HTTPError) as e:
            self._handle_request_exception(e, "PATCH", url)
        except Exception as e:
            log.error(f"Unexpected error during PATCH request to {url}: {e}")
            raise

    def delete(
        self,
        url,
        patch_content_type=True,
        add_metadata=False,
        sl_metadata=None,
        **kwargs,
    ):
        url = self.patch_request(
            url, patch_content_type, kwargs, add_metadata, sl_metadata
        )
        try:
            response = self.session.delete(url, **kwargs)
            response.raise_for_status()
            return response
        except (SSLError, Timeout, RequestsConnectionError, HTTPError) as e:
            self._handle_request_exception(e, "DELETE", url)
        except Exception as e:
            log.error(f"Unexpected error during DELETE request to {url}: {e}")
            raise
