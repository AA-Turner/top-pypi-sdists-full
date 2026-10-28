import io
import json
import logging
import os
import re
import ssl
import urllib3
from typing import Any, Optional

from istari_digital_client._transfer.request_options import transport_request_options
from istari_digital_client.sdk._exceptions import ApiException, ApiValueError
from istari_digital_client.sdk._proxy import (
    proxy_headers_for,
    proxy_url_for,
    resolve_ca_certs,
    resolve_proxies,
)

logger = logging.getLogger(__name__)

SUPPORTED_SOCKS_PROXIES = {"socks5", "socks5h", "socks4", "socks4a"}
RESTResponseType = urllib3.HTTPResponse


def is_socks_proxy_url(url):
    if url is None:
        return False
    split_section = url.split("://")
    if len(split_section) < 2:
        return False
    else:
        return split_section[0].lower() in SUPPORTED_SOCKS_PROXIES



def _transfer_pool_maxsize(configuration) -> int:
    """Per-host connection pool size: 4 x transfer_concurrency (16 at the default).

    ``transfer_concurrency`` is read defensively: the legacy stack is often handed
    the sdk ``Configuration``, and a post-construction assignment skips validation.
    """
    concurrency = getattr(configuration, "transfer_concurrency", None)
    try:
        concurrency = int(concurrency) if concurrency is not None else 4
    except (TypeError, ValueError):
        concurrency = 4
    return max(1, min(concurrency, 16)) * 4


class RESTResponse(io.IOBase):
    def __init__(self, resp) -> None:
        self.response = resp
        self.status = resp.status
        self.reason = resp.reason
        self.data = None

    def read(self):
        if self.data is None:
            self.data = self.response.data
        return self.data

    def getheaders(self):
        """Returns a dictionary of the response headers."""
        return self.response.headers

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.response.headers.get(name, default)


def _build_ssl_context(ca_bundle: Optional[str]) -> ssl.SSLContext:
    """OS trust store plus ``ca_bundle`` if given; passing ``ca_certs`` to urllib3 would drop the OS store."""
    context = urllib3.util.ssl_.create_urllib3_context(cert_reqs=ssl.CERT_REQUIRED)
    context.load_default_certs()
    if ca_bundle:
        ca_bundle = os.path.expanduser(ca_bundle)
        try:
            context.load_verify_locations(cafile=ca_bundle)
        except OSError as e:
            raise ApiValueError(
                f"CA bundle {ca_bundle!r} could not be loaded: {e}"
            ) from e
    return context


class RESTClientObject:
    def __init__(self, configuration) -> None:
        trust_env = configuration.trust_env is not False
        pool_args: dict[str, Any] = {
            "cert_reqs": ssl.CERT_REQUIRED,
            "ssl_context": _build_ssl_context(
                resolve_ca_certs(configuration.ca_bundle, trust_env)
            ),
            "cert_file": None,
            "key_file": None,
            "ca_cert_data": None,
        }

        # A finite total would also consume the redirect allowance. Keep error
        # categories finite instead, with redirects independently bounded at 3.
        # Attempts include the initial request; unset uses urllib3's default.
        retries = urllib3.Retry.DEFAULT.total
        if not configuration.retry_enabled:
            retries = 0
        elif configuration.retry_max_attempts is not None:
            retries = max(int(configuration.retry_max_attempts) - 1, 0)
        pool_args["retries"] = urllib3.Retry(
            total=None,
            connect=retries,
            read=retries,
            status=retries,
            other=retries,
            redirect=3,
        )
        # The transfer engine runs ``transfer_concurrency`` parallel PUT/GETs per
        # client against one host; urllib3's per-host default of 1 would churn
        # connections. Overflow only costs extra connections plus a warning.
        pool_args["maxsize"] = _transfer_pool_maxsize(configuration)

        if configuration.proxy_url and is_socks_proxy_url(configuration.proxy_url):
            raise ApiValueError(
                "SOCKS proxies are not supported; configure an HTTP(S) proxy URL"
            )

        # https pool manager (direct connections)
        self.pool_manager: urllib3.PoolManager
        self.pool_manager = urllib3.PoolManager(**pool_args)

        # proxied connections: mapping resolved once, managers built per proxy URL
        self._pool_args = pool_args
        self._proxies = resolve_proxies(configuration.proxy_url, trust_env)
        self._proxy_managers: dict[str, urllib3.ProxyManager] = {}
        self._warned_socks_proxy = False

    def _pool_manager_for(self, url) -> urllib3.PoolManager:
        """Select the direct pool or a proxy manager for the target URL."""
        proxy_url = proxy_url_for(url, self._proxies)
        if proxy_url is None:
            return self.pool_manager
        if is_socks_proxy_url(proxy_url):
            if not self._warned_socks_proxy:
                credential_free_url, _ = proxy_headers_for(proxy_url)
                logger.warning(
                    "Ignoring SOCKS proxy %s from the environment: SOCKS is not "
                    "supported, connecting directly (set NO_PROXY or "
                    "ISTARI_CLIENT_TRUST_ENV=false to silence this)",
                    credential_free_url,
                )
                self._warned_socks_proxy = True
            return self.pool_manager
        manager = self._proxy_managers.get(proxy_url)
        if manager is None:
            proxy_target, proxy_headers = proxy_headers_for(proxy_url)
            logger.info(
                "Using proxy %s for outbound HTTP(S) traffic (NO_PROXY=%s)",
                proxy_target,
                self._proxies.get("no", "-"),
            )
            manager = urllib3.ProxyManager(
                proxy_target,
                proxy_headers=proxy_headers,
                proxy_ssl_context=self._pool_args["ssl_context"],
                **self._pool_args,
            )
            self._proxy_managers[proxy_url] = manager
        return manager

    def close(self) -> None:
        """Close all pooled connections (returns sockets to the OS)."""
        self.pool_manager.clear()
        for manager in self._proxy_managers.values():
            manager.clear()

    def request_raw(
        self,
        method,
        url,
        *,
        headers=None,
        body=None,
        timeout=None,
        preload_content=False,
        decode_content=True,
    ):
        """Send one request as given and return the raw urllib3 response.

        This is the transfer engine's data-plane path for presigned URLs: no
        default headers, no auth, no JSON serialization, no urllib3 retry and no
        redirect following (a 3xx is returned so the caller can rewind ``body``
        and re-send). ``body`` is bytes or a readable; the caller sets
        ``Content-Length`` so a readable is never sent chunked. ``timeout`` is a
        ``urllib3.Timeout`` (or seconds). Proxy and CA handling are shared with
        ``request``. The caller owns retries and must release the response.
        """
        pool_manager = self._pool_manager_for(url)
        if timeout is not None and not isinstance(timeout, urllib3.Timeout):
            timeout = urllib3.Timeout(connect=timeout, read=timeout)
        try:
            return pool_manager.request(
                method.upper(),
                url,
                body=body,
                headers=headers or {},
                timeout=timeout,
                preload_content=preload_content,
                decode_content=decode_content,
                retries=False,
                redirect=False,
            )
        except urllib3.exceptions.SSLError as e:
            msg = "\n".join([type(e).__name__, str(e)])
            raise ApiException(status=0, reason=msg) from e
        except urllib3.exceptions.MaxRetryError as e:
            if not isinstance(e.reason, urllib3.exceptions.SSLError):
                raise
            msg = "\n".join([type(e.reason).__name__, str(e.reason)])
            raise ApiException(status=0, reason=msg) from e

    def request(
        self,
        method,
        url,
        headers=None,
        body=None,
        post_params=None,
        _request_timeout=None,
    ):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in ["GET", "HEAD", "DELETE", "POST", "PUT", "PATCH", "OPTIONS"]

        if post_params and body:
            raise ApiValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        pool_manager = self._pool_manager_for(url)

        timeout = None
        if _request_timeout:
            if isinstance(_request_timeout, (int, float)):
                timeout = urllib3.Timeout(total=_request_timeout)
            elif isinstance(_request_timeout, tuple) and len(_request_timeout) == 2:
                timeout = urllib3.Timeout(
                    connect=_request_timeout[0], read=_request_timeout[1]
                )

        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ["POST", "PUT", "PATCH", "OPTIONS", "DELETE"]:
                # no content type provided or payload is json
                content_type = headers.get("Content-Type")
                if not content_type or re.search("json", content_type, re.IGNORECASE):
                    request_body = None
                    if body is not None:
                        request_body = json.dumps(body)
                    r = pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False,
                        **transport_request_options(),
                    )
                elif content_type == "application/x-www-form-urlencoded":
                    r = pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=False,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False,
                        **transport_request_options(),
                    )
                elif content_type == "multipart/form-data":
                    # must del headers['Content-Type'], or the correct
                    # Content-Type which generated by urllib3 will be
                    # overwritten.
                    del headers["Content-Type"]
                    # Ensures that dict objects are serialized
                    post_params = [
                        (a, json.dumps(b)) if isinstance(b, dict) else (a, b)
                        for a, b in post_params
                    ]
                    r = pool_manager.request(
                        method,
                        url,
                        fields=post_params,
                        encode_multipart=True,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False,
                        **transport_request_options(),
                    )
                # Pass a `string` parameter directly in the body to support
                # other content types than JSON when `body` argument is
                # provided in serialized form.
                elif isinstance(body, str) or isinstance(body, bytes):
                    r = pool_manager.request(
                        method,
                        url,
                        body=body,
                        timeout=timeout,
                        headers=headers,
                        preload_content=False,
                        **transport_request_options(),
                    )
                elif headers["Content-Type"].startswith("text/") and isinstance(
                    body, bool
                ):
                    request_body = "true" if body else "false"
                    r = pool_manager.request(
                        method,
                        url,
                        body=request_body,
                        preload_content=False,
                        timeout=timeout,
                        headers=headers,
                        **transport_request_options(),
                    )
                else:
                    # Cannot generate the request from given parameters
                    msg = """Cannot prepare a request message for provided
                             arguments. Please check that your arguments match
                             declared content type."""
                    raise ApiException(status=0, reason=msg)
            # For `GET`, `HEAD`
            else:
                r = pool_manager.request(
                    method,
                    url,
                    fields={},
                    timeout=timeout,
                    headers=headers,
                    preload_content=False,
                    **transport_request_options(),
                )
        except urllib3.exceptions.SSLError as e:
            msg = "\n".join([type(e).__name__, str(e)])
            raise ApiException(status=0, reason=msg) from e
        except urllib3.exceptions.MaxRetryError as e:
            # retries wrap the underlying SSLError; preserve the complete chain
            # so the transfer engine can classify the certificate failure.
            if not isinstance(e.reason, urllib3.exceptions.SSLError):
                raise
            msg = "\n".join([type(e.reason).__name__, str(e.reason)])
            raise ApiException(status=0, reason=msg) from e

        return RESTResponse(r)
