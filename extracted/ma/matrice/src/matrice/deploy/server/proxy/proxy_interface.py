"""Module providing proxy_interface functionality."""

import logging
import time
import threading
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional
import httpx
import uvicorn

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
)
from fastapi.encoders import jsonable_encoder
from fastapi.params import File, Form
from fastapi.responses import JSONResponse

from matrice.deploy.server.proxy.proxy_utils import (
    AuthKeyValidator,
    RequestsLogger,
)
from matrice.deploy.server.inference.inference_interface import InferenceInterface


class MatriceProxyInterface:
    """Interface for proxying requests to model servers."""

    def __init__(
        self,
        session,
        deployment_id: str,
        deployment_instance_id: str,
        external_port: int,
        inference_interface: InferenceInterface,
    ):
        """Initialize proxy server.

        Args:
            session: Session object for authentication and RPC
            deployment_id: ID of the deployment
            external_port: Port to expose externally
        """
        self.session = session
        self.rpc = self.session.rpc
        self.deployment_id = deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.external_port = external_port
        self.app = FastAPI()
        self.logger = None
        self.auth_key_validator = None
        self.inference_interface = inference_interface
        self._register_event_handlers()
        self._register_routes()

    def validate_auth_key(self, auth_key):
        """Validate auth key.

        Args:
            auth_key: Authentication key to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not auth_key:
            return False
        return self.auth_key_validator(auth_key)

    async def inference(
        self, input1, input2=None, extra_params=None, apply_post_processing=False
    ):
        """Perform inference using the inference interface.

        Args:
            input1: Primary input data
            input2: Secondary input data (optional)
            extra_params: Additional parameters for inference (optional)
            apply_post_processing: Flag to apply post-processing

        Returns:
            Inference result, Post-processing result
        """
        return await self.inference_interface.inference(
            input1, input2, extra_params, apply_post_processing
        )

    def log_prediction_info(self, result, start_time, input1, auth_key):
        """Log prediction info.

        Args:
            result: Prediction result
            start_time: Start time of the request
            input1: Input data
            auth    _key: Authentication key used
        """
        self.logger.add_log_to_queue(
            prediction=result,
            latency=time.time() - start_time,
            request_time=datetime.now(timezone.utc).isoformat(),
            input_data=input1,
            deployment_instance_id=self.deployment_instance_id,
            auth_key=auth_key,
        )

    def on_start(self):
        """Start the proxy server components."""
        self.logger = RequestsLogger(self.deployment_id, self.session)
        self.auth_key_validator = AuthKeyValidator(self.deployment_id, self.session)
        self.auth_key_validator.start()
        self.logger.start()

    async def on_stop(self):
        """Clean up proxy server components."""
        logging.debug("Running cleanup for MatriceProxyInterface")
        if hasattr(self, "auth_key_validator"):
            try:
                self.auth_key_validator.stop()
                logging.debug("Stopped auth key validator")
            except Exception as exc:
                logging.error(
                    "Error stopping auth key validator: %s",
                    exc,
                )
        if hasattr(self, "logger"):
            try:
                self.logger.stop()
                logging.debug("Stopped request logger")
            except Exception as exc:
                logging.error(
                    "Error stopping request logger: %s",
                    exc,
                )
        logging.debug("Cleanup complete")

    def _register_event_handlers(self):
        """Register event handlers."""

        @asynccontextmanager
        async def lifespan(app):
            self.on_start()
            try:
                yield
            finally:
                await self.on_stop()

        self.app.router.lifespan_context = lifespan

    def _register_routes(self):
        """Register proxy routes."""

        @self.app.post("/inference")
        async def proxy_request(
            auth_key: str = Form(None),
            authKey: str = Form(None),
            input: Optional[UploadFile] = File(None),
            input2: Optional[UploadFile] = File(None),
            input_url: Optional[str] = Form(None),
            inputUrl: Optional[str] = Form(None),
            extra_params: Optional[str] = Form(None),
            apply_post_processing: Optional[str] = Form("false"),
        ):
            auth_key = auth_key or authKey
            # if not self.validate_auth_key(auth_key):
            #     raise HTTPException(
            #         status_code=401,
            #         detail="Invalid auth key",
            #     )
            start_time = time.time()
            input1 = await input.read() if input else None
            input2_data = await input2.read() if input2 else None
            input_url_value = input_url or inputUrl
            if input_url_value:
                async with httpx.AsyncClient() as client:
                    response = await client.get(input_url_value)
                    input1 = response.content
            if not input1:
                raise HTTPException(
                    status_code=400,
                    detail="No input provided",
                )
            
            # Parse apply_post_processing parameter
            apply_post_processing_flag = False
            if apply_post_processing:
                apply_post_processing_flag = apply_post_processing.lower() in ("true", "1", "yes")
            
            try:
                result, post_processing_result = await self.inference(
                    input1, input2_data, extra_params, apply_post_processing_flag
                )
                self.log_prediction_info(result, start_time, input1, auth_key)

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
            except Exception as exc:
                logging.error("Proxy error: %s", str(exc))
                raise HTTPException(
                    status_code=500,
                    detail=str(exc),
                ) from exc

    def start(self):
        """Start the proxy server in a background thread."""
        def run_server():
            """Run the uvicorn server."""
            try:
                logging.info(
                    "Starting proxy server on port %d",
                    self.external_port,
                )
                server = uvicorn.Server(
                    uvicorn.Config(
                        app=self.app,
                        host="0.0.0.0",
                        port=self.external_port,
                        log_level="info",
                    )
                )
                server.run()
            except Exception as exc:
                logging.error(
                    "Failed to start proxy server: %s",
                    str(exc),
                )
                raise
        
        # Start the server in a background thread
        server_thread = threading.Thread(target=run_server, daemon=False, name="ProxyServer")
        server_thread.start()
        logging.info("Proxy server thread started successfully")
