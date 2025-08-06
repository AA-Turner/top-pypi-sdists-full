"""Module providing augmentation server functionality."""

import logging
import threading
import urllib.request
from typing import List, Dict, Any, Optional
import signal
import atexit
import base64
import io

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import cv2  # Import OpenCV
import httpx # Use httpx for async uploads

from matrice.utils import dependencies_check

# Add opencv-python-headless to the dependency check
dependencies_check(["albumentations", "httpx", "opencv-python-headless"])

from matrice.data_processing.image_augmentations import (  # noqa: E42
    get_augmentation_compose,
)


class AugmentationRequest(BaseModel):
    """Request model for augmentation endpoint."""

    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    # ADDED: A pre-signed URL from the backend to upload the result to
    upload_url: str
    image_bboxes: List[Dict] = []
    augmentation_configs: Dict[str, Dict[str, Any]] = {}


class AugmentationResponse(BaseModel):
    """Response model for augmentation endpoint."""

    success: bool
    message: str
    # CHANGED: This now returns the URL of the uploaded image, not the base64 data
    augmented_image_url: Optional[str] = None
    augmented_bboxes: Optional[List[Dict]] = None


class AugmentationServer:
    """Class to handle dataset augmentation server."""

    def __init__(
        self, session: Any, action_record_id: str, port: int, ip_address: str = None
    ):
        """Initialize AugmentationServer.

        Args:
            session: Session object with RPC client
            action_record_id: ID of action record
            port: Port to run the server on
            ip_address: IP address to bind to (optional)
        """

        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id
        self.port = port
        self.ip = ip_address or self._get_external_ip()
        self._shutdown_event = threading.Event()
        self._server_thread = None

        # Initialize FastAPI app
        self.app = FastAPI(title="Matrice Augmentation Server", version="1.0.0")
        self._setup_routes()
        self._setup_shutdown_handlers()

        # Fetch action details
        self._fetch_action_details()

        logging.info(f"Job parameters: {self.job_params}")
        logging.info("Successfully initialized augmentation server on IP: %s", self.ip)

    def _get_external_ip(self) -> str:
        """Get external IP address."""
        try:
            response = urllib.request.urlopen("https://ident.me", timeout=60)
            return response.read().decode("utf8").strip()
        except Exception as e:
            logging.warning(f"Failed to get external IP: {e}, using localhost")
            return "localhost"

    def _fetch_action_details(self) -> None:
        """Fetch action details from the API."""
        try:
            url = f"/v1/project/action/{self.action_record_id}/details"
            response = self.rpc.get(url)
            self.action_doc = response["data"]

            # Extract the appropriate fields from the nested structure
            self.action_type = self.action_doc.get("action")
            self.job_params = self.action_doc.get("jobParams", {})
            self.action_details = self.action_doc.get("actionDetails", {})
            self.augmentation_server_id = self.action_details.get(
                "augmentation_server_id",
                self.job_params.get("augmentation_server_id", None),
            )
        except Exception as e:
            logging.error(f"Failed to fetch action details: {e}")
            # Set defaults
            self.action_doc = {}
            self.action_type = "augmentation"
            self.job_params = {}
            self.action_details = {}
            self.augmentation_server_id = None

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""

        @self.app.post("/augment", response_model=AugmentationResponse)
        async def augment_dataset_item(request: AugmentationRequest):
            """Augment dataset item and upload to a pre-signed URL."""
            try:
                # Validate input
                if not request.image_url and not request.image_base64:
                    raise HTTPException(
                        status_code=400,
                        detail="Either image_url or image_base64 must be provided",
                    )
                if not request.upload_url:
                    raise HTTPException(
                        status_code=400, detail="An upload_url must be provided"
                    )
                if not request.image_bboxes:
                    raise HTTPException(status_code=400, detail="No bboxes provided")
                if not request.augmentation_configs:
                    raise HTTPException(
                        status_code=400, detail="No augmentation configs provided"
                    )

                # Load image from URL or Base64
                image = await self._load_image(request.image_url, request.image_base64)

                # Apply augmentations
                augmentation_fn = get_augmentation_compose(request.augmentation_configs)
                augmented_result = augmentation_fn(
                    image=image,
                    bboxes=request.image_bboxes,
                    class_labels=[None for _ in range(len(request.image_bboxes))],
                )

                # --- NEW UPLOAD LOGIC ---
                augmented_image_np = augmented_result["image"]

                # Convert RGB numpy array (from albumentations) to BGR for OpenCV
                image_bgr = cv2.cvtColor(augmented_image_np, cv2.COLOR_RGB2BGR)

                # Encode image to JPEG format in memory
                is_success, img_encoded = cv2.imencode(".jpg", image_bgr)
                if not is_success:
                    raise HTTPException(
                        status_code=500, detail="Failed to encode augmented image."
                    )
                
                img_bytes = img_encoded.tobytes()

                # Upload the image bytes to the pre-signed S3 URL using httpx
                async with httpx.AsyncClient() as client:
                    upload_response = await client.put(
                        request.upload_url,
                        content=img_bytes,
                        headers={'Content-Type': 'image/jpeg'},
                        timeout=60.0,
                    )

                # Check for a successful upload
                if upload_response.status_code not in [200, 201, 204]:
                    error_detail = f"Failed to upload image. Cloud storage responded with status: {upload_response.status_code}. Response: {upload_response.text}"
                    logging.error(error_detail)
                    raise HTTPException(status_code=500, detail=error_detail)

                # Get the permanent URL (the part of the URL before the '?' query string)
                permanent_url = request.upload_url.split('?')[0]
                # --- END OF NEW LOGIC ---

                return AugmentationResponse(
                    success=True,
                    message="Augmentation completed and image uploaded successfully",
                    augmented_image_url=permanent_url,  # Return the permanent URL
                    augmented_bboxes=augmented_result.get("bboxes", []),
                )

            except HTTPException:
                raise
            except Exception as e:
                logging.error(f"Error in augmentation: {str(e)}", exc_info=True)
                raise HTTPException(
                    status_code=500, detail=f"Internal server error: {str(e)}"
                )

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "server": "augmentation_server"}

        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {"message": "Matrice Augmentation Server", "version": "1.0.0"}

    async def _load_image(
        self, image_url: Optional[str], image_base64: Optional[str]
    ) -> Any:
        """Load image from URL or base64 string."""
        try:
            if image_url:
                # Handle both local file paths and URLs
                if image_url.startswith(("http://", "https://")):
                    async with httpx.AsyncClient() as client:
                        response = await client.get(image_url)
                        response.raise_for_status()
                        image = Image.open(io.BytesIO(response.content))
                else:
                    # Local file path
                    image = Image.open(image_url)
            else:
                # Base64 image
                image_data = base64.b64decode(image_base64)
                image = Image.open(io.BytesIO(image_data))

            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")

            return image

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to load image: {str(e)}"
            )

    def _image_to_base64(self, image: Any) -> str:
        """Convert PIL Image or NumPy array to base64 string."""
        try:
            # Convert numpy array to PIL Image if necessary
            if hasattr(image, "shape"):  # numpy array
                import numpy as np

                if image.dtype != np.uint8:
                    image = (image * 255).astype(np.uint8)
                image = Image.fromarray(image)

            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            return image_base64

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to convert image to base64: {str(e)}"
            )
            
    # ... The rest of the file (setup_shutdown_handlers, update_status, etc.) remains the same ...
    def _setup_shutdown_handlers(self) -> None:
        """Setup shutdown signal handlers."""

        def signal_handler(signum, frame):
            """Handle shutdown signals."""
            logging.info(f"Received signal {signum}, shutting down gracefully...")
            self.stop_server()

        def atexit_handler():
            """Handle atexit cleanup."""
            try:
                self.stop_server()
            except Exception as exc:
                logging.error("Error during atexit shutdown: %s", str(exc))

        # Register signal handlers
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Register atexit handler
        atexit.register(atexit_handler)

        logging.info("Shutdown handlers registered successfully")

    def update_status(
        self,
        stepCode: str,
        status: str,
        status_description: str,
    ) -> None:
        """Update status of augmentation server.

        Args:
            stepCode: Code indicating current step
            status: Status of step
            status_description: Description of status
        """
        try:
            logging.info(status_description)
            url = "/v1/actions"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            logging.error(
                "Exception in update_status: %s",
                str(e),
            )
            # Don't raise here to avoid breaking the server

    def update_server_address(self) -> None:
        """Update server address in the backend."""
        try:
            path = "/v1/actions/augmentation_servers"
            payload = {
                "action_id": self.action_record_id,
                "ip_address": self.ip,
                "port": self.port,
                "augmentation_server_id": self.augmentation_server_id,
            }
            resp = self.rpc.put(path=path, payload=payload)
            logging.info(f"Server address update response: {resp}")
        except Exception as e:
            logging.error(f"Failed to update server address: {e}")

    def start_server(self) -> None:
        """Start the augmentation server."""
        try:
            self.update_status(
                "DCKR_PROC",
                "OK",
                "Starting augmentation server",
            )

            # Update server address in backend
            self.update_server_address()

            # Start the server in a background thread
            def run_server():
                """Run the uvicorn server."""
                try:
                    logging.info(
                        "Starting augmentation server on %s:%d",
                        self.ip,
                        self.port,
                    )
                    server = uvicorn.Server(
                        uvicorn.Config(
                            app=self.app,
                            host="0.0.0.0",
                            port=self.port,
                            log_level="info",
                        )
                    )
                    server.run()
                except Exception as exc:
                    logging.error(
                        "Failed to start augmentation server: %s",
                        str(exc),
                    )
                    self.update_status(
                        "ERROR",
                        "ERROR",
                        f"Failed to start server: {str(exc)}",
                    )
                    raise

            # Start the server in a background thread
            self._server_thread = threading.Thread(
                target=run_server, daemon=False, name="AugmentationServer"
            )
            self._server_thread.start()

            # Wait a moment to ensure server started
            import time

            time.sleep(2)

            self.update_status(
                "SUCCESS",
                "SUCCESS",
                f"Augmentation server started successfully on {self.ip}:{self.port}",
            )

            logging.info("Augmentation server thread started successfully")

        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            self.update_status(
                "ERROR",
                "ERROR",
                f"Failed to start augmentation server: {str(e)}",
            )
            raise

    def stop_server(self) -> None:
        """Stop the augmentation server gracefully."""
        if not self._shutdown_event.is_set():
            logging.info("Stopping augmentation server...")
            self._shutdown_event.set()

            # Update status
            try:
                self.update_status(
                    "STOPPED",
                    "STOPPED",
                    "Augmentation server stopped",
                )
            except Exception as e:
                logging.error(f"Failed to update stop status: {e}")

    def wait_for_shutdown(self) -> None:
        """Wait for the server to be shut down."""
        if self._server_thread and self._server_thread.is_alive():
            self._server_thread.join()

# Flow
# 1. Start the server by creating action and adding the aggmentaion server in the DB
# 2. Once the server with the action starts it will use the update address api call to save its ip and port
# 3. The client will make request to augment an image
# 4. We will get the address and port from the DB
# 5. Make request to the server "http://ip:port/augment" and get the augmented image