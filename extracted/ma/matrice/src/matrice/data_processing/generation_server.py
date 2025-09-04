import logging
import threading
import urllib.request
from typing import Optional, Any, Tuple, List, Dict
import signal
import atexit
import base64
import io
import time
from huggingface_hub import login
import uvicorn
import httpx
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import torch
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import make_image_grid, load_image
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from dataclasses import dataclass
from matrice.utils import dependencies_check
from matrice.utils import handle_response

dependencies_check(["httpx", "opencv-python-headless", "torch", "diffusers"])

class ImageGenerationConfig(BaseModel):
    """Represents image generation parameters."""
    prompt: str
    # strength: Optional[float] = 0.75
    # guidance_scale: Optional[float] = 7.5
    # output_size: Optional[tuple] = (768, 512)

class ImageGenerationRequest(BaseModel):
    """Request model for image generation endpoint."""
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    upload_url: str
    generation_config: ImageGenerationConfig

class ImageGenerationResponse(BaseModel):
    """Response model for image generation endpoint."""
    success: bool
    message: str
    generated_image_url: Optional[str] = None
    generated_bboxes: Optional[List[Dict]] = None

class ImageGenerationServer:
    """Class to handle image generation server."""

    def __init__(self, session: Any, action_record_id: str, port: int, ip_address: str = None):
        self.session = session
        self.rpc = session.rpc
        self.action_record_id = action_record_id
        self.port = port
        self.ip = ip_address or self._get_external_ip()
        self._shutdown_event = threading.Event()
        self._server_thread = None
        self.app = FastAPI(title="Matrice Image Generation Server", version="1.0.0")

        # Track last request time
        self.last_request_time = time.time()
        self.idle_timeout_seconds = 6000  # 10 minutes

        # Fetch Hugging Face token and log in
        try:
            hf_token = self.get_hugging_face_token_for_data_generation()
            logging.info(f"retrieved Hugging Face token: {hf_token}")
            login(token=hf_token)
            logging.info("Successfully logged in to Hugging Face with token")
        except Exception as e:
            logging.error(f"Failed to log in to Hugging Face: {e}")
            raise RuntimeError(f"Failed to authenticate with Hugging Face: {str(e)}")

        # Initialize Stable Diffusion pipeline
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_id = "kandinsky-community/kandinsky-2-2-decoder"
        try:
            self.pipe = AutoPipelineForImage2Image.from_pretrained(
                model_id, torch_dtype=torch.float16, use_safetensors=True
            )
            # self.pipe = DiffusionPipeline.from_pretrained(
            #     model_id, torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            # )
            # self.pipe.enable_model_cpu_offload()
            self.pipe.enable_xformers_memory_efficient_attention()
            self.pipe = self.pipe.to(self.device)
            logging.info("Stable Diffusion pipeline initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Stable Diffusion pipeline: {e}")
            raise

        self._setup_routes()
        self._setup_shutdown_handlers()
        
        self._fetch_action_details()
        self._start_idle_monitor()

        logging.info("Successfully initialized image generation server on IP: %s", self.ip)

    def get_hugging_face_token_for_data_generation(self):
        """Retrieve Hugging Face token for data generation."""
        secret_name = "hugging_face"
        resp, error, message = self.get_model_secret_keys(secret_name)
        if error is not None:
            logging.error("Error getting Hugging Face token: %s", message)
            raise RuntimeError(f"Failed to retrieve Hugging Face token: {message}")
        else:
            hugging_face_token = resp["user_access_token"]
            return hugging_face_token

    def get_model_secret_keys(self, secret_name):
        """Get model secret keys.

        Args:
            secret_name: Name of the secret

        Returns:
            Tuple of (data, error, message) from API response
        """
        path = f"/v1/scaling/get_models_secret_keys?secret_name={secret_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Secret keys fetched successfully",
            "Could not fetch the secret keys",
        )

    def _start_idle_monitor(self):
        """Background thread that shuts down server if idle for too long."""
        def monitor():
            while not self._shutdown_event.is_set():
                time.sleep(60)  # Check every 1 minute
                idle_time = time.time() - self.last_request_time
                if idle_time > self.idle_timeout_seconds:
                    logging.info("No requests received for 10 minutes. Stopping server due to inactivity...")
                    self.stop_server()
                    break
        t = threading.Thread(target=monitor, daemon=True, name="IdleMonitor")
        t.start()

    def _generate_image(self, image_pil: Image.Image, config: ImageGenerationConfig) -> np.ndarray:
        """Generate a new image using the Qwen model."""
        try:
            # Ensure image is in RGB mode
            if image_pil.mode != "RGB":
                image_pil = image_pil.convert("RGB")    

            # Generate image using Qwen model
            generated_images = self.pipe(
                prompt=config.prompt,
                image=image_pil,
                guidance_scale=12.5,
                strength=0.4,
                num_inference_steps=50
            ).images
            generated_image = generated_images[0]

            # Convert back to numpy array for further processing
            generated_image_np = np.array(generated_image)
            return generated_image_np
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                logging.error("CUDA out of memory during image generation")
                raise HTTPException(status_code=500, detail="GPU out of memory. Try reducing image size.")
            logging.error(f"Failed to generate image: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")
        except Exception as e:
            logging.error(f"Failed to generate image: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""
        @self.app.post("/generate", response_model=ImageGenerationResponse)
        async def generate_image(request: ImageGenerationRequest):
            """Generate a new image based on input image and prompt."""
            self.last_request_time = time.time()  # Update last activity
            try:
                logging.info("Received image generation request: %s", request)
                if not request.image_url and not request.image_base64:
                    raise HTTPException(status_code=400, detail="Either image_url or image_base64 must be provided")
                if not request.upload_url:
                    raise HTTPException(status_code=400, detail="An upload_url must be provided")
                if not request.generation_config.prompt:
                    raise HTTPException(status_code=400, detail="A prompt must be provided in generation_config")

                # Load input image
                if request.image_url:
                    image_pil = load_image(request.image_url)
                else:
                    image_pil = await self._load_image(None, request.image_base64)

                # Generate new image
                generated_image_np = self._generate_image(
                    image_pil=image_pil,
                    config=request.generation_config
                )

                # Convert to BGR for OpenCV encoding
                image_bgr = cv2.cvtColor(generated_image_np, cv2.COLOR_RGB2BGR)
                is_success, img_encoded = cv2.imencode(".jpg", image_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                if not is_success:
                    raise HTTPException(status_code=500, detail="Failed to encode generated image")

                # Upload generated image
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
                return ImageGenerationResponse(
                    success=True,
                    message="Image generation completed and uploaded successfully",
                    generated_image_url=permanent_url
                )
            except HTTPException:
                raise
            except Exception as e:
                logging.error(f"Error in image generation: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

        @self.app.get("/health")
        async def health_check():
            self.last_request_time = time.time()  # Update last activity
            return {"status": "healthy", "server": "image_generation_server"}

        @self.app.get("/")
        async def root():
            self.last_request_time = time.time()  # Update last activity
            return {"message": "Matrice Image Generation Server", "version": "1.0.0"}

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
            self.generation_server_id = self.action_details.get(
                "serverId",
                self.job_params.get("serverId", None),
            )
        except Exception as e:
            logging.error(f"Failed to fetch action details: {e}")
            self.action_doc = {}
            self.action_type = "image_generation"
            self.job_params = {}
            self.action_details = {}
            self.generation_server_id = None

    async def _load_image(self, image_url: Optional[str], image_base64: Optional[str]) -> Image.Image:
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
            raise HTTPException(status_code=400, detail=f"Failed to load image: {str(e)}")

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
        """Update status of image generation server."""
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

    def update_server_address(self, status, port, host) -> None:
        """Update server address in the backend."""
        try:
            path = "/v1/actions/synthetic_data_servers"
            payload = {
                "id": self.generation_server_id,
                "host": host,
                "port": int(port),
                "status": status,
                "isShared": True,
                "accountNumber": self.action_doc.get("accountNumber", ""),
            }
            resp = self.rpc.put(path=path, payload=payload)
            logging.info(f"Server address update response: {resp}")
        except Exception as e:
            logging.error(f"Failed to update server address: {e}")

    def start_server(self) -> None:
        """Start the image generation server."""
        try:
            self.update_status("DCKR_PROC", "OK", "Starting image generation server")
            self.update_server_address("running", self.port, self.ip)
            def run_server():
                try:
                    logging.info("Starting uvicorn server on %s:%d", self.ip, int(self.port))
                    uvicorn.run(self.app, host="0.0.0.0", port=int(self.port), log_level="info")
                except Exception as exc:
                    logging.error("Failed to start image generation server: %s", str(exc))
                    self.update_status("ERROR", "ERROR", f"Failed to start server: {str(exc)}")
                    raise
            self._server_thread = threading.Thread(target=run_server, daemon=False, name="ImageGenerationServer")
            self._server_thread.start()
            time.sleep(2)
            self.update_status("SUCCESS", "SUCCESS", f"Image generation server started successfully on {self.ip}:{self.port}")
            logging.info("Image generation server thread started successfully")
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            self.update_status("ERROR", "ERROR", f"Failed to start image generation server: {str(e)}")
            raise

    def stop_server(self) -> None:
        """Stop the image generation server gracefully."""
        if not self._shutdown_event.is_set():
            logging.info("Stopping image generation server...")
            self._shutdown_event.set()
            try:
                self.update_status("STOPPED", "STOPPED", "Image generation server stopped")
                self.update_server_address("stopped", 0, "")
            except Exception as e:
                logging.error(f"Failed to update stop status: {e}")

    def wait_for_shutdown(self) -> None:
        """Wait for the server to be shut down."""
        if self._server_thread and self._server_thread.is_alive():
            self._server_thread.join()