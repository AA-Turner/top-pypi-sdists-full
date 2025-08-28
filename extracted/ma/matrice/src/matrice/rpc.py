"""Module for RPC client handling Matrice.ai backend API requests."""

import os
import logging
from datetime import datetime, timedelta, timezone
from importlib.metadata import version
import requests
from matrice.token_auth import (
    AuthToken,
    RefreshToken,
)
from matrice.utils import log_errors

class RPC:
    """RPC class for handling backend API requests with token-based authentication."""

    def __init__(
        self,
        access_key=None,
        secret_key=None,
        project_id=None,
    ):
        """Initialize the RPC client with optional project ID."""
        self.project_id = project_id
        self.BASE_URL = (
            f"https://{os.environ.get('ENV', 'prod')}.backend.app.matrice.ai"
        )

        access_key = access_key or os.environ.get("MATRICE_ACCESS_KEY_ID")
        secret_key = secret_key or os.environ.get("MATRICE_SECRET_ACCESS_KEY")

        if not access_key or not secret_key:
            raise ValueError(
                "Access key and Secret key are required. "
                "Set them as environment variables MATRICE_ACCESS_KEY_ID and MATRICE_SECRET_ACCESS_KEY or pass them explicitly."
            )


        os.environ["MATRICE_ACCESS_KEY_ID"] = access_key
        os.environ["MATRICE_SECRET_ACCESS_KEY"] = secret_key

        self.access_key = access_key
        self.secret_key = secret_key
        self.Refresh_Token = RefreshToken(access_key, secret_key)
        self.AUTH_TOKEN = AuthToken(
            access_key,
            secret_key,
            self.Refresh_Token,
        )
        self.url_projectID = f"projectId={self.project_id}" if self.project_id else ""
        try:
            self.sdk_version = version("matrice")
        except Exception:
            self.sdk_version = "0.0.0"

    @log_errors(default_return=None, raise_exception=True, log_error=True)
    def send_request(
        self,
        method,
        path,
        headers=None,
        payload=None,
        files=None,
        data=None,
        timeout=60,
        raise_exception=True,
    ):
        """Send an HTTP request to the specified endpoint."""
        self.refresh_token()
        request_url = f"{self.BASE_URL}{path}"
        request_url = self.add_project_id(request_url)

        if headers is None:
            headers = {}
        if payload is None:
            payload = {}

        headers["sdk_version"] = self.sdk_version
        response = None
        response_data = {"success": False, "data": None, "error": None}
        error_text = None
        try:
            response = requests.request(
                method,
                request_url,
                auth=self.AUTH_TOKEN,
                headers=headers,
                json=payload,
                data=data,
                files=files,
                timeout=timeout,
                allow_redirects=True,
            )
            response.raise_for_status()
            response_data = response.json()
        except Exception as e:
            try:
                response_text = response.text
            except Exception:
                response_text = "No response"

            try:
                response_status_code = response.status_code
            except Exception:
                response_status_code = "failed to get status code"

            error_text = f"""
                Error in api call
                request:{payload}
                url:{request_url}
                response:{response_text}
                status_code:{response_status_code}
                exception:{str(e)}
                """
            if raise_exception:
                raise Exception(error_text)

        return response_data

    @log_errors(default_return=None, raise_exception=True, log_error=True)
    async def async_send_request(
        self,
        method,
        path,
        headers=None,
        payload=None,
        files=None,
        data=None,
        timeout=60,
        raise_exception=True,
    ):
        import aiohttp
        """Send an async HTTP request to the specified endpoint."""
        self.refresh_token()
        request_url = f"{self.BASE_URL}{path}"
        request_url = self.add_project_id(request_url)

        if headers is None:
            headers = {}
        if payload is None:
            payload = {}

        headers["sdk_version"] = self.sdk_version
        
        # Set up authorization header like the sync version
        # First call the auth token to ensure bearer_token is set
        self.AUTH_TOKEN.set_bearer_token()
        headers["Authorization"] = self.AUTH_TOKEN.bearer_token
        
        response = None
        response_data = {"success": False, "data": None, "error": None}
        error_text = None
        
        try:
            timeout_config = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession(timeout=timeout_config) as session:
                kwargs = {
                    'method': method,
                    'url': request_url,
                    'headers': headers,
                    'allow_redirects': True,
                }
                
                if files:
                    # For file uploads, use data with FormData
                    form_data = aiohttp.FormData()
                    for key, value in files.items():
                        form_data.add_field(key, value)
                    if payload:
                        for key, value in payload.items():
                            form_data.add_field(key, str(value))
                    kwargs['data'] = form_data
                elif data:
                    kwargs['data'] = data
                elif payload:
                    kwargs['json'] = payload
                
                async with session.request(**kwargs) as response:
                    response.raise_for_status()
                    response_data = await response.json()
                    
        except Exception as e:
            try:
                response_text = await response.text() if response else "No response"
            except Exception:
                response_text = "No response"

            try:
                response_status_code = response.status if response else "failed to get status code"
            except Exception:
                response_status_code = "failed to get status code"

            error_text = f"""
                Error in api call
                request:{payload}
                url:{request_url}
                response:{response_text}
                status_code:{response_status_code}
                exception:{str(e)}
                """
            if raise_exception:
                raise Exception(error_text)

        return response_data

    async def get_async(self, path, params=None, timeout=60, raise_exception=True):
        """Send an async GET request to the specified endpoint."""
        return await self.async_send_request("GET", path, payload=params or {}, timeout=timeout, raise_exception=raise_exception)

    async def post_async(
        self,
        path,
        payload=None,
        headers=None,
        files=None,
        data=None,
        timeout=60,
        raise_exception=True,
    ):
        """Send an async POST request to the specified endpoint."""
        return await self.async_send_request(
            "POST",
            path,
            headers=headers or {},
            payload=payload or {},
            files=files,
            data=data,
            timeout=timeout,
            raise_exception=raise_exception,
        )

    async def put_async(self, path, payload=None, headers=None, timeout=60, raise_exception=True):
        """Send an async PUT request to the specified endpoint."""
        return await self.async_send_request(
            "PUT",
            path,
            headers=headers or {},
            payload=payload or {},
            timeout=timeout,
            raise_exception=raise_exception,
        )

    async def delete_async(self, path, payload=None, headers=None, timeout=60, raise_exception=True):
        """Send an async DELETE request to the specified endpoint."""
        return await self.async_send_request(
            "DELETE",
            path,
            headers=headers or {},
            payload=payload or {},
            timeout=timeout,
            raise_exception=raise_exception,
        )

    def get(self, path, params=None, timeout=60, raise_exception=True):
        """Send a GET request to the specified endpoint."""
        return self.send_request("GET", path, payload=params or {}, timeout=timeout, raise_exception=raise_exception)

    def post(
        self,
        path,
        payload=None,
        headers=None,
        files=None,
        data=None,
        timeout=60,
        raise_exception=True,
    ):
        """Send a POST request to the specified endpoint."""
        return self.send_request(
            "POST",
            path,
            headers=headers or {},
            payload=payload or {},
            files=files,
            data=data,
            timeout=timeout,
            raise_exception=raise_exception,
        )

    def put(self, path, payload=None, headers=None, timeout=60, raise_exception=True):
        """Send a PUT request to the specified endpoint."""
        return self.send_request(
            "PUT",
            path,
            headers=headers or {},
            payload=payload or {},
            timeout=timeout,
            raise_exception=raise_exception,
        )

    def delete(self, path, payload=None, headers=None, timeout=60, raise_exception=True):
        """Send a DELETE request to the specified endpoint."""
        return self.send_request(
            "DELETE",
            path,
            headers=headers or {},
            payload=payload or {},
            timeout=timeout,
            raise_exception=raise_exception,
        )
      
    def refresh_token(self):
        """Refresh the authentication token if expired."""
        try:
            time_difference = datetime.now(timezone.utc) - self.AUTH_TOKEN.expiry_time.replace(tzinfo=timezone.utc)
            time_diff = time_difference - timedelta(0)
            if time_diff.total_seconds() >= 0:
                self.AUTH_TOKEN = AuthToken(
                    self.access_key,
                    self.secret_key,
                    self.Refresh_Token,
                )
                logging.debug("Authentication token refreshed")
        except Exception as e:
            logging.error(f"Error refreshing token: {e}")
            # Create a new token anyway to ensure we have a valid one
            self.AUTH_TOKEN = AuthToken(
                self.access_key,
                self.secret_key,
                self.Refresh_Token,
            )

    def add_project_id(self, url):
        """Add project ID to the URL if present and not already included."""
        if not self.url_projectID or "?projectId" in url or "&projectId" in url:
            return url
        if "?" in url:
            url = url + "&" + self.url_projectID
        else:
            url = url + "?" + self.url_projectID
        return url
