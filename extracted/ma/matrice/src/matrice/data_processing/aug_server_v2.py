"""Module providing augmentation server functionality."""

import logging
import threading
import urllib.request
from typing import List, Dict, Any, Optional
import signal
import atexit
import base64
import io
from abc import ABC, abstractmethod
from dataclasses import dataclass

import uvicorn
import httpx
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image

from matrice.utils import dependencies_check
from matrice.data_processing.augmentation_utils.strategies import *

dependencies_check(["albumentations", "httpx", "opencv-python-headless"])

class ImageAugmentationStrategy(ABC):
    def __init__(self, **kwargs):
        pass
    def apply(self, image, bboxes, bbox_format='coco'):
        logging.warning(f"Using placeholder for: {self.__class__.__name__}")
        return image, image.shape[0], image.shape[1], bboxes


@dataclass
class AugmentationStep:
    """Represents a single augmentation step."""
    name: str
    params: Dict[str, Any]


class AugmentationStrategyFactory:
    """Factory class to create augmentation strategy instances."""

    STRATEGIES = {
        'blur': BlurAugmentation,
        'bit_depth_reduction': BitDepthReductionAugmentation,
        'brightness_contrast': BrightnessContrastAugmentation,
        'color_jitter': ColorJitterAugmentation,
        'compression_artifacts': CompressionArtifactsAugmentation,
        'downscale_upscale': DownscaleUpscaleAugmentation,
        'film_grain': FilmGrainAugmentation,
        'flip': HorizontalFlipAugmentation,
        'fog': FogAugmentation,
        'hsv': HueSaturationValueAugmentation,
        'iso_noise': ISONoiseAugmentation,
        'low_light': LowLightSimulationAugmentation,
        'posterize': PosterizeAugmentation,
        'rain': RainAugmentation,
        'random_affine': RandomAffineAugmentation,
        'salt_pepper': SaltAndPepperNoiseAugmentation,
        'shadows': ShadowAugmentation,
        'snow': SnowAugmentation,
        'speckle': SpeckleNoiseAugmentation,
        'sunflare': SunFlareAugmentation
    }

    @classmethod
    def create_strategy(cls, aug_step: AugmentationStep) -> ImageAugmentationStrategy:
        strategy_name_lower = aug_step.name.lower()
        
        # Handle both snake_case and PascalCase keys from requests
        pascal_case_map = {k.replace('_', ''): v for k, v in cls.STRATEGIES.items()}
        
        if strategy_name_lower in cls.STRATEGIES:
            strategy_class = cls.STRATEGIES[strategy_name_lower]
        elif strategy_name_lower in pascal_case_map:
            strategy_class = pascal_case_map[strategy_name_lower]
        else:
            raise ValueError(f"Unknown augmentation strategy: {aug_step.name}")

        return strategy_class(**aug_step.params)


class AugmentationRequest(BaseModel):
    """Request model for augmentation endpoint."""
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    upload_url: str
    image_bboxes: List[Dict] = []
    augmentation_configs: Dict[str, Dict[str, Any]] = {}


class AugmentationResponse(BaseModel):
    """Response model for augmentation endpoint."""
    success: bool
    message: str
    augmented_image_url: Optional[str] = None
    augmented_bboxes: Optional[List[Dict]] = None


class AugmentationServer:
    """Class to handle dataset augmentation server."""

    def __init__(self, session: Any, action_record_id: str, port: int, ip_address: str = None):
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id
        self.port = port
        self.ip = ip_address or self._get_external_ip()
        self._shutdown_event = threading.Event()
        self._server_thread = None
        self.app = FastAPI(title="Matrice Augmentation Server", version="1.0.0")

        self._setup_routes()
        self._setup_shutdown_handlers()
        self._fetch_action_details()
        logging.info("Successfully initialized augmentation server on IP: %s", self.ip)
    
    def _apply_augmentations(self, image_np: np.ndarray, bboxes_coco: List[List[float]], configs: Dict) -> Dict:
        """Applies a sequence of augmentations using the factory."""
        current_image = image_np.copy()
        current_bboxes = bboxes_coco

        for aug_name, aug_params in configs.items():
            try:
                aug_step = AugmentationStep(name=aug_name, params=aug_params)
                strategy = AugmentationStrategyFactory.create_strategy(aug_step)
                
                augmented_image, _, _, new_bboxes = strategy.apply(
                    current_image, current_bboxes, bbox_format='coco'
                )

                current_image = augmented_image
                current_bboxes = new_bboxes
                logging.info(f"Successfully applied augmentation: {aug_name}")

            except Exception as e:
                logging.error(f"Failed to apply augmentation {aug_name}: {e}", exc_info=True)
                raise HTTPException(status_code=400, detail=f"Error applying {aug_name}: {e}")

        return {"image": current_image, "bboxes": current_bboxes}

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""
        @self.app.post("/augment", response_model=AugmentationResponse)
        async def augment_dataset_item(request: AugmentationRequest):
            """Augment dataset item using the new strategy-based approach."""
            try:
                logging.info("Received augmentation request: %s", request)
                if not request.image_url and not request.image_base64:
                    raise HTTPException(status_code=400, detail="Either image_url or image_base64 must be provided")
                if not request.upload_url:
                    raise HTTPException(status_code=400, detail="An upload_url must be provided")
                if not request.augmentation_configs:
                    raise HTTPException(status_code=400, detail="No augmentation configs provided")

                image_pil = await self._load_image(request.image_url, request.image_base64)
                image_np = np.array(image_pil)

                augmented_result = self._apply_augmentations(
                    image_np=image_np,
                    bboxes_coco=request.image_bboxes,
                    configs=request.augmentation_configs
                )
                
                augmented_image_np = augmented_result["image"]
                image_bgr = cv2.cvtColor(augmented_image_np, cv2.COLOR_RGB2BGR)
                is_success, img_encoded = cv2.imencode(".jpg", image_bgr)
                if not is_success:
                    raise HTTPException(status_code=500, detail="Failed to encode augmented image.")
                
                img_bytes = img_encoded.tobytes()

                async with httpx.AsyncClient() as client:
                    upload_response = await client.put(
                        request.upload_url,
                        content=img_bytes,
                        headers={'Content-Type': 'image/jpeg'},
                        timeout=60.0,
                    )

                if upload_response.status_code not in [200, 201, 204]:
                    error_detail = f"Failed to upload image. Status: {upload_response.status_code}. Response: {upload_response.text}"
                    logging.error(error_detail)
                    raise HTTPException(status_code=500, detail=error_detail)

                permanent_url = request.upload_url.split('?')[0]

                return AugmentationResponse(
                    success=True,
                    message="Augmentation completed and image uploaded successfully",
                    augmented_image_url=permanent_url,
                    augmented_bboxes=augmented_result.get("bboxes", []),
                )

            except HTTPException:
                raise
            except Exception as e:
                logging.error(f"Error in augmentation: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "server": "augmentation_server"}

        @self.app.get("/")
        async def root():
            return {"message": "Matrice Augmentation Server", "version": "1.0.0"}

    def _get_external_ip(self) -> str:
        """Get external IP address."""
        try:
            with urllib.request.urlopen("https://ident.me", timeout=60) as response:
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
            self.action_type = self.action_doc.get("action")
            self.job_params = self.action_doc.get("jobParams", {})
            self.action_details = self.action_doc.get("actionDetails", {})
            self.augmentation_server_id = self.action_details.get(
                "serverId",
                self.job_params.get("serverId", None),
            )
        except Exception as e:
            logging.error(f"Failed to fetch action details: {e}")
            self.action_doc = {}
            self.action_type = "augmentation"
            self.job_params = {}
            self.action_details = {}
            self.augmentation_server_id = None

    async def _load_image(
        self, image_url: Optional[str], image_base64: Optional[str]
    ) -> Image.Image:
        """Load image from URL or base64 string and return PIL Image."""
        try:
            if image_url:
                if image_url.startswith(("http://", "https://")):
                    async with httpx.AsyncClient() as client:
                        response = await client.get(image_url)
                        response.raise_for_status()
                        image = Image.open(io.BytesIO(response.content))
                else:
                    image = Image.open(image_url)
            elif image_base64:
                image_data = base64.b64decode(image_base64)
                image = Image.open(io.BytesIO(image_data))
            else:
                 raise ValueError("No image source provided.")

            if image.mode != "RGB":
                image = image.convert("RGB")
            return image
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to load image: {str(e)}"
            )

    def _setup_shutdown_handlers(self) -> None:
        """Setup shutdown signal handlers."""
        def signal_handler(signum, frame):
            logging.info(f"Received signal {signum}, shutting down gracefully...")
            self.stop_server()
        def atexit_handler():
            try:
                self.stop_server()
            except Exception as exc:
                logging.error("Error during atexit shutdown: %s", str(exc))
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        atexit.register(atexit_handler)
        logging.info("Shutdown handlers registered successfully")

    def update_status(self, stepCode: str, status: str, status_description: str) -> None:
        """Update status of augmentation server."""
        try:
            logging.info(status_description)
            url = "/v1/actions"
            payload = {
                "_id": self.action_record_id,
                "action": self.action_type,
                "serviceName": self.action_doc.get("serviceName", "Unknown"),
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            logging.error("Exception in update_status: %s", str(e))

    def update_server_address(self) -> None:
        """Update server address in the backend."""
        try:
            path = "/v1/actions/augmentation_servers"
            payload = {
                "id": self.augmentation_server_id,
                "host": self.ip,
                "port": int(self.port),
                "status": "running",
                "isShared": True,
            }
            resp = self.rpc.put(path=path, payload=payload)
            logging.info(f"Server address update response: {resp}")
        except Exception as e:
            logging.error(f"Failed to update server address: {e}")

    def start_server(self) -> None:
        """Start the augmentation server."""
        try:
            self.update_status("DCKR_PROC", "OK", "Starting augmentation server")
            self.update_server_address()
            def run_server():
                try:
                    logging.info("Starting uvicorn server on %s:%d", self.ip, self.port)
                    uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")
                except Exception as exc:
                    logging.error("Failed to start augmentation server: %s", str(exc))
                    self.update_status("ERROR", "ERROR", f"Failed to start server: {str(exc)}")
                    raise
            self._server_thread = threading.Thread(target=run_server, daemon=False, name="AugmentationServer")
            self._server_thread.start()
            import time
            time.sleep(2)
            self.update_status("SUCCESS", "SUCCESS", f"Augmentation server started successfully on {self.ip}:{self.port}")
            logging.info("Augmentation server thread started successfully")
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            self.update_status("ERROR", "ERROR", f"Failed to start augmentation server: {str(e)}")
            raise

    def stop_server(self) -> None:
        """Stop the augmentation server gracefully."""
        if not self._shutdown_event.is_set():
            logging.info("Stopping augmentation server...")
            self._shutdown_event.set()
            try:
                self.update_status("STOPPED", "STOPPED", "Augmentation server stopped")
            except Exception as e:
                logging.error(f"Failed to update stop status: {e}")

    def wait_for_shutdown(self) -> None:
        """Wait for the server to be shut down."""
        if self._server_thread and self._server_thread.is_alive():
            self._server_thread.join()
