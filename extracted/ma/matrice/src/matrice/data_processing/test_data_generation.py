import logging
import threading
import time
import base64
import io
from typing import Optional
from dataclasses import dataclass

import uvicorn
import httpx
import cv2
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import torch
from diffusers import StableDiffusionImg2ImgPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class ImageGenerationConfig:
    """Represents image generation parameters."""
    prompt: str
    strength: float = 0.75
    guidance_scale: float = 7.5
    output_size: tuple = (768, 512)

class ImageGenerationRequest(BaseModel):
    """Request model for image generation endpoint."""
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    generation_config: ImageGenerationConfig

class ImageGenerationResponse(BaseModel):
    """Response model for image generation endpoint."""
    success: bool
    message: str
    generated_image_path: Optional[str] = None

class ImageGenerationServer:
    """Class to handle image generation server for local testing."""

    def __init__(self, port: int = 8000):
        self.port = port
        print(f"Initializing local image generation server on port: {self.port}")
        self._shutdown_event = threading.Event()
        self._server_thread = None
        self.app = FastAPI(title="Local Image Generation Server", version="1.0.0")

        # Track last request time for idle timeout
        self.last_request_time = time.time()
        self.idle_timeout_seconds = 600  # 10 minutes

        # Initialize Stable Diffusion pipeline
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_id = "runwayml/stable-diffusion-v1-5"
        try:
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_id, torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.pipe = self.pipe.to(self.device)
            logging.info("Stable Diffusion pipeline initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Stable Diffusion pipeline: {e}")
            raise

        self._setup_routes()
        self._start_idle_monitor()

        logging.info("Successfully initialized local image generation server on port: %d", self.port)

    def _start_idle_monitor(self):
        """Background thread that shuts down server if idle for too long."""
        def monitor():
            while not self._shutdown_event.is_set():
                time.sleep(60)  # Check every 1 minute
                idle_time = time.time() - self.last_request_time
                if idle_time > self.idle_timeout_seconds:
                    logging.info("No requests received for 10 minutes. Stopping server...")
                    self.stop_server()
                    break
        t = threading.Thread(target=monitor, daemon=True, name="IdleMonitor")
        t.start()

    def _generate_image(self, image_np: np.ndarray, config: ImageGenerationConfig) -> np.ndarray:
        """Generate a new image using Stable Diffusion."""
        try:
            # Convert numpy array to PIL Image
            image_pil = Image.fromarray(image_np).convert("RGB")
            # Resize to specified output size
            image_pil = image_pil.resize(config.output_size)

            # Generate image using Stable Diffusion
            generated_images = self.pipe(
                prompt=config.prompt,
                image=image_pil,
                strength=config.strength,
                guidance_scale=config.guidance_scale
            ).images
            generated_image = generated_images[0]

            # Convert back to numpy array
            generated_image_np = np.array(generated_image)
            return generated_image_np
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
                if not request.generation_config.prompt:
                    raise HTTPException(status_code=400, detail="A prompt must be provided in generation_config")

                # Load input image
                image_pil = await self._load_image(request.image_url, request.image_base64)
                image_np = np.array(image_pil)

                # Generate new image
                generated_image_np = self._generate_image(
                    image_np=image_np,
                    config=request.generation_config
                )

                # Convert to BGR for OpenCV encoding
                image_bgr = cv2.cvtColor(generated_image_np, cv2.COLOR_RGB2BGR)
                is_success, img_encoded = cv2.imencode(".jpg", image_bgr)
                if not is_success:
                    raise HTTPException(status_code=500, detail="Failed to encode generated image")

                # Save generated image locally
                output_path = f"generated_image_{int(time.time())}.jpg"
                cv2.imwrite(output_path, image_bgr)
                logging.info(f"Generated image saved to {output_path}")

                return ImageGenerationResponse(
                    success=True,
                    message="Image generation completed and saved locally",
                    generated_image_path=output_path
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
            return {"message": "Local Image Generation Server", "version": "1.0.0"}

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

    def start_server(self) -> None:
        """Start the image generation server."""
        try:
            logging.info("Starting uvicorn server on localhost:%d", self.port)
            def run_server():
                try:
                    uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")
                except Exception as exc:
                    logging.error("Failed to start server: %s", str(exc))
                    raise
            self._server_thread = threading.Thread(target=run_server, daemon=False, name="ImageGenerationServer")
            self._server_thread.start()
            time.sleep(2)
            logging.info("Image generation server started successfully on localhost:%d", self.port)
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            raise

    def stop_server(self) -> None:
        """Stop the image generation server."""
        if not self._shutdown_event.is_set():
            logging.info("Stopping image generation server...")
            self._shutdown_event.set()

    def wait_for_shutdown(self) -> None:
        """Wait for the server to be shut down."""
        if self._server_thread and self._server_thread.is_alive():
            self._server_thread.join()

if __name__ == "__main__":
    server = ImageGenerationServer(port=8000)
    server.start_server()
