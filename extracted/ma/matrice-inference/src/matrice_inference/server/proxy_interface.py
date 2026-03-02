"""Module providing proxy_interface functionality."""

import logging
import time
import threading
from datetime import datetime, timezone
from typing import Optional, Set
import httpx
import uvicorn
import asyncio

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from matrice_inference.server.inference_interface import InferenceInterface


class MatriceProxyInterface:
    """Interface for proxying requests to model servers."""

    def __init__(
        self,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        external_port: int,
        inference_interface: Optional[InferenceInterface] = None,
        auth_refresh_interval_minutes: int = 1,
    ):
        """Initialize proxy server.

        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            deployment_instance_id: ID of the deployment instance
            external_port: Port to expose externally
            inference_interface: Interface for model inference. Can be None if not configured.
            auth_refresh_interval_minutes: Minimum minutes between auth key refreshes
        """
        self.session = session
        self.rpc = self.session.rpc
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.external_port = external_port
        self.app = FastAPI()
        self.logger = logging.getLogger(__name__)
        self.inference_interface = inference_interface
        self._shutdown_event = threading.Event()
        self._server = None
        self._server_thread = None
        
        # Auth key management
        self.auth_keys: Set[str] = set()
        self.auth_keys_info = []
        self.auth_refresh_interval_minutes = auth_refresh_interval_minutes
        self.last_auth_refresh_time = 0.0
        self._auth_lock = threading.Lock()
        
        # Initialize auth keys on startup
        self._initialize_auth_keys()
        self._register_routes()

    def _initialize_auth_keys(self):
        """Initialize auth keys on startup."""
        try:
            self.update_auth_keys()
            self.logger.info("Auth keys initialized successfully")
        except Exception as exc:
            self.logger.error("Failed to initialize auth keys: %s", str(exc))
            # Continue without auth keys - they will be retried on first request

    def _should_refresh_auth_keys(self) -> bool:
        """Check if auth keys should be refreshed based on time interval."""
        current_time = time.time()
        time_since_last_refresh = current_time - self.last_auth_refresh_time
        return time_since_last_refresh >= (self.auth_refresh_interval_minutes * 60)

    def _refresh_auth_keys_if_needed(self):
        """Refresh auth keys if the refresh interval has passed."""
        if self._should_refresh_auth_keys():
            with self._auth_lock:
                # Double-check after acquiring lock
                if self._should_refresh_auth_keys():
                    try:
                        self.update_auth_keys()
                        self.logger.debug("Auth keys refreshed successfully")
                    except Exception as exc:
                        self.logger.error("Failed to refresh auth keys: %s", str(exc))

    def validate_auth_key(self, auth_key):
        """Validate auth key.

        Args:
            auth_key: Authentication key to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not auth_key:
            return False
        
        # Refresh auth keys if needed before validation
        self._refresh_auth_keys_if_needed()
        
        with self._auth_lock:
            return auth_key in self.auth_keys

    def _parse_expiry_time(self, expiry_time_str: str) -> float:
        """Parse expiry time string to timestamp."""
        # Handle different ISO format variations
        try:
            # Replace Z with timezone if needed
            if expiry_time_str.endswith("Z"):
                expiry_time_str = expiry_time_str.replace("Z", "+00:00")
            
            # Normalize ISO format for proper parsing
            if '.' in expiry_time_str:
                main, rest = expiry_time_str.split('.', 1)
                if '+' in rest:
                    frac, tz = rest.split('+', 1)
                    frac = (frac + '000000')[:6]  # pad/truncate to 6 digits
                    expiry_time_str = f"{main}.{frac}+{tz}"
                elif '-' in rest:
                    frac, tz = rest.split('-', 1)
                    frac = (frac + '000000')[:6]  # pad/truncate to 6 digits
                    expiry_time_str = f"{main}.{frac}-{tz}"
        except Exception as err:
            self.logger.error("Error parsing expiry time: %s", str(err))
            expiry_time_str = expiry_time_str.replace("Z", "+00:00")
        return datetime.fromisoformat(expiry_time_str).timestamp()

    def update_auth_keys(self) -> None:
        """Fetch and validate auth keys for the deployment."""      
        try:
            response = self.rpc.get(f"/v1/inference/{self.deployment_id}", raise_exception=False)
            if not response.get("success"):
                self.logger.error("Failed to fetch auth keys")
                return
            
            if response["data"]["authKeys"]:
                self.auth_keys_info = response["data"]["authKeys"]
            else:
                self.auth_keys_info = []
            
            if not self.auth_keys_info:
                self.logger.debug("No auth keys found for deployment")
                return
            
            current_time = time.time()
            self.auth_keys.clear()
            
            for auth_key_info in self.auth_keys_info:
                try:
                    expiry_time = self._parse_expiry_time(auth_key_info["expiryTime"])
                    if expiry_time > current_time:
                        self.auth_keys.add(auth_key_info["key"])
                    else:
                        self.logger.debug("Skipping expired auth key")
                except (ValueError, KeyError) as err:
                    self.logger.error("Invalid auth key data: %s", err)
                    continue
            
            # Update last refresh time
            self.last_auth_refresh_time = current_time
            
            self.logger.debug(
                "Successfully loaded %d valid auth keys",
                len(self.auth_keys),
            )
        except Exception as err:
            self.logger.error("Error fetching auth keys: %s", str(err))
            raise

    def _register_routes(self):
        """Register proxy routes."""

        @self.app.post("/inference")
        async def proxy_request(request: Request):
            # Check if server is shutting down
            if self._shutdown_event.is_set():
                raise HTTPException(
                    status_code=503,
                    detail="Server is shutting down",
                )
            
            # Parse form data manually
            try:
                form_data = await request.form()
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to parse form data: {str(e)}",
                ) from e
            
            # Extract parameters from form data
            auth_key = form_data.get("auth_key") or form_data.get("authKey")
            input_file = form_data.get("input")
            input_url_value = form_data.get("input_url") or form_data.get("inputUrl")
            extra_params = form_data.get("extra_params")
            apply_post_processing = form_data.get("apply_post_processing", "false")
            
            # if not self.validate_auth_key(auth_key): # TODO: enable once fixed to send the external auth key for FR server
            #     raise HTTPException(
            #         status_code=401,
            #         detail="Invalid auth key",
            #     )
            
            # Handle file input
            input_data = None
            if input_file and hasattr(input_file, 'read'):
                input_data = await input_file.read()
            elif isinstance(input_file, bytes):
                input_data = input_file
            
            if input_url_value:
                try:
                    # Use timeout and error handling for URL downloads
                    timeout = httpx.Timeout(60.0)  # 60 second timeout
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        response = await client.get(input_url_value)
                        response.raise_for_status()  # Raise exception for HTTP errors
                        input_data = response.content
                except asyncio.CancelledError:
                    # Handle shutdown during request
                    raise HTTPException(
                        status_code=503,
                        detail="Request cancelled due to server shutdown",
                    )
                except httpx.TimeoutException:
                    raise HTTPException(
                        status_code=408,
                        detail="Timeout fetching input URL",
                    )
                except httpx.HTTPStatusError as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"HTTP error fetching input URL: {e.response.status_code}",
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Error fetching input URL: {str(e)}",
                    )
            
            if not input_data:
                raise HTTPException(
                    status_code=400,
                    detail="No input provided",
                )
            
            # Parse apply_post_processing parameter
            apply_post_processing_flag = False
            if apply_post_processing:
                apply_post_processing_flag = apply_post_processing.lower() in ("true", "1", "yes")
            
            try:
                # Check shutdown again before inference
                if self._shutdown_event.is_set():
                    raise HTTPException(
                        status_code=503,
                        detail="Server is shutting down",
                    )
                
                # Check if inference interface is available
                if self.inference_interface is None:
                    raise HTTPException(
                        status_code=501,
                        detail="Direct inference API not available. "
                               "No inference interface configured.",
                    )
                
                # Direct API calls (e.g., identity images) are high priority
                # They should always complete successfully, even if streaming frames get skipped
                result, post_processing_result = await self.inference_interface.inference(
                    input=input_data,
                    extra_params=extra_params,
                    apply_post_processing=apply_post_processing_flag,
                    is_high_priority=True
                )
                

                response_data = {
                    "status": 1,
                    "message": "Request success",
                    "result": result,
                }
                
                # Include post-processing results if available
                if post_processing_result is not None:
                    response_data["post_processing_result"] = post_processing_result
                    response_data["post_processing_applied"] = True
                else:
                    response_data["post_processing_applied"] = False

                return JSONResponse(
                    content=jsonable_encoder(response_data)
                )
            except asyncio.CancelledError:
                # Handle shutdown during inference
                self.logger.info("Request cancelled during inference due to shutdown")
                raise HTTPException(
                    status_code=503,
                    detail="Request cancelled due to server shutdown",
                )
            except Exception as exc:
                self.logger.error("Proxy error: %s", str(exc))
                raise HTTPException(
                    status_code=500,
                    detail=str(exc),
                ) from exc


    def start(self):
        """Start the proxy server in a background thread."""
        def run_server():
            """Run the uvicorn server."""
            try:
                self.logger.info(
                    "Starting proxy server on port %d",
                    self.external_port,
                )
                config = uvicorn.Config(
                    app=self.app,
                    host="0.0.0.0",
                    port=self.external_port,
                    log_level="info",
                )
                self._server = uvicorn.Server(config)
                self._server.run()

            except Exception as exc:
                if not self._shutdown_event.is_set():
                    self.logger.error(
                        "Failed to start proxy server: %s",
                        str(exc),
                    )
                else:
                    self.logger.info("Proxy server stopped during shutdown")
        
        # Start the server in a background thread
        self._server_thread = threading.Thread(target=run_server, daemon=False, name="ProxyServer")
        self._server_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(0.5)
        self.logger.info("Proxy server thread started successfully")

    def stop(self):
        """Stop the proxy server gracefully."""
        try:
            self.logger.info("Stopping proxy server...")
            
            # Signal shutdown to prevent new requests
            self._shutdown_event.set()
            
            # Stop the uvicorn server if it exists
            if self._server:
                try:
                    # Force shutdown the server
                    if hasattr(self._server, 'should_exit'):
                        self._server.should_exit = True
                    if hasattr(self._server, 'force_exit'):
                        self._server.force_exit = True
                except Exception as exc:
                    self.logger.warning("Error stopping uvicorn server: %s", str(exc))
            
            # Wait for the server thread to finish
            if self._server_thread and self._server_thread.is_alive():
                self.logger.info("Waiting for proxy server thread to stop...")
                self._server_thread.join(timeout=5.0)
                if self._server_thread.is_alive():
                    self.logger.warning("Proxy server thread did not stop within timeout")
                else:
                    self.logger.info("Proxy server thread stopped successfully")
            
            self.logger.info("Proxy server stopped")
        except Exception as exc:
            self.logger.error("Error stopping proxy server: %s", str(exc))
