import os
import asyncio
import base64
from typing import Dict, List, Tuple
from fsd.log.logger_config import get_logger
from fsd.util.portkey import AIGateway
from PIL import Image
import io
import aiohttp
import ssl
import certifi
from pathlib import Path
import platform

logger = get_logger(__name__)

class ImageGenAgent:
    """
    An agent responsible for generating images based on provided prompts and parameters.
    """

    def __init__(self, repo):
        self.repo = repo
        self.ai = AIGateway()
        # Create SSL context with certifi certificates
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.is_windows = platform.system() == 'Windows'

    def validate_dimensions(self, dalle_dimension: str) -> str:
        """
        Validates the requested image dalle_dimension against supported sizes.
        """
        supported_sizes = ['1024x1024', '1792x1024', '1024x1792']
        if dalle_dimension in supported_sizes:
            return dalle_dimension
        else:
            logger.debug(f" #### Unsupported size '{dalle_dimension}'. Defaulting to '1024x1024'.")
            return '1024x1024'  # Default to a supported size

    def normalize_image_format(self, image_format: str) -> str:
        """
        Normalizes the image format string for compatibility with PIL.
        """
        format_upper = image_format.upper()
        return 'JPEG' if format_upper == 'JPG' else format_upper

    async def save_image_data(self, image_data: str, file_path: str, image_format: str):
        """
        Saves base64-encoded image data to a file asynchronously.
        """
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image_format = self.normalize_image_format(image_format)
            folder_path = Path(file_path).parent

            # Handle case where folder path exists as a file
            if folder_path.exists() and not folder_path.is_dir():
                os.remove(str(folder_path))

            # Create folder if it doesn't exist
            folder_path.mkdir(parents=True, exist_ok=True)

            # Check write permissions
            try:
                test_file = folder_path / '.test'
                test_file.touch()
                test_file.unlink()
            except (PermissionError, OSError):
                logger.error(f"  Folder {folder_path} is not writable. Attempting to fix permissions.")
                if self.is_windows:
                    os.system(f'icacls "{folder_path}" /grant Everyone:F')
                else:
                    os.system(f'chmod 777 "{folder_path}"')

            await asyncio.to_thread(image.save, str(file_path), format=image_format)
            logger.debug(f"\n #### `SnowX` saved image to {Path(file_path).name}.")
        except Exception as e:
            logger.error(f"  Error saving image: {str(e)}")
            raise

    async def save_and_resize_image(self, image_data: str, file_path: str, image_format: str, target_size: Tuple[int, int]):
        """
        Saves and resizes base64-encoded image data to a file asynchronously.
        """
        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            image = await asyncio.to_thread(self.resize_image_with_aspect_ratio, image, target_size)
            image_format = self.normalize_image_format(image_format)
            folder_path = Path(file_path).parent

            # Handle case where folder path exists as a file
            if folder_path.exists() and not folder_path.is_dir():
                os.remove(str(folder_path))

            # Create folder if it doesn't exist
            folder_path.mkdir(parents=True, exist_ok=True)

            # Check write permissions
            try:
                test_file = folder_path / '.test'
                test_file.touch()
                test_file.unlink()
            except (PermissionError, OSError):
                logger.error(f"  Folder {folder_path} is not writable. Attempting to fix permissions.")
                if self.is_windows:
                    os.system(f'icacls "{folder_path}" /grant Everyone:F')
                else:
                    os.system(f'chmod 777 "{folder_path}"')

            await asyncio.to_thread(image.save, str(file_path), format=image_format)
            logger.info(f" #### `SnowX` saved and resized image to {target_size} at {Path(file_path).name}.")
        except Exception as e:
            logger.error(f"  Error saving and resizing image: {str(e)}")
            raise

    def resize_image_with_aspect_ratio(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """
        Resizes an image while maintaining aspect ratio and crops it to fit the target size.
        """
        target_width, target_height = target_size
        target_aspect = target_width / target_height
        image_aspect = image.width / image.height
        if image_aspect > target_aspect:
            new_height = target_height
            new_width = int(new_height * image_aspect)
        else:
            new_width = target_width
            new_height = int(new_width / image_aspect)
        image = image.resize((new_width, new_height), Image.LANCZOS)
        left = (new_width - target_width) / 2
        top = (new_height - target_height) / 2
        right = (new_width + target_width) / 2
        bottom = (new_height + target_height) / 2
        return image.crop((left, top, right, bottom))

    def extract_image_data(self, response):
        """
        Extracts image data from the API response, either base64-encoded or via URL.
        """
        try:
            if hasattr(response, 'error') and response.error:
                error_message = getattr(response.error, 'message', 'Unknown error')
                raise Exception(f"API error: {error_message}")
            if hasattr(response, 'data') and response.data:
                data_item = response.data[0]
            else:
                raise ValueError("No image data in response.")
            image_data_b64 = getattr(data_item, 'b64_json', None)
            if image_data_b64:
                return image_data_b64, 'base64'
            else:
                image_url = getattr(data_item, 'url', None)
                if image_url:
                    return image_url, 'url'
                else:
                    raise ValueError("No image data (base64 or URL) found.")
        except Exception as e:
            logger.error(f"  Failed to extract image data: {str(e)}")
            logger.debug(f" #### Response content: {response}")
            raise

    async def fetch_and_save_image_from_url(self, url: str, file_path: str, image_format: str, target_size: Tuple[int, int] = None):
        """
        Fetches an image from a URL and saves (and optionally resizes) it to a file.
        """
        try:
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        image_bytes = await resp.read()
                        image = Image.open(io.BytesIO(image_bytes))
                        if target_size:
                            image = await asyncio.to_thread(self.resize_image_with_aspect_ratio, image, target_size)
                        image_format = self.normalize_image_format(image_format)
                        folder_path = Path(file_path).parent

                        # Handle case where folder path exists as a file
                        if folder_path.exists() and not folder_path.is_dir():
                            os.remove(str(folder_path))

                        # Create folder if it doesn't exist
                        folder_path.mkdir(parents=True, exist_ok=True)

                        # Check write permissions
                        try:
                            test_file = folder_path / '.test'
                            test_file.touch()
                            test_file.unlink()
                        except (PermissionError, OSError):
                            logger.error(f"  Folder {folder_path} is not writable. Attempting to fix permissions.")
                            if self.is_windows:
                                os.system(f'icacls "{folder_path}" /grant Everyone:F')
                            else:
                                os.system(f'chmod 777 "{folder_path}"')

                        await asyncio.to_thread(image.save, str(file_path), format=image_format)
                        logger.debug(f" #### `SnowX` fetched and saved image to {Path(file_path).name}")
                    else:
                        raise Exception(f"Failed to fetch image. HTTP status: {resp.status}")
        except Exception as e:
            logger.error(f"  Error fetching and saving image: {str(e)}")
            raise

    async def generate_image(self, prompt: str, dalle_dimension: str, actual_dimension: str, image_format: str, file_path: str,  tier: str):
        """
        Generates an image using the AI model and saves it to a file.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                supported_size = self.validate_dimensions(dalle_dimension)
                response = await asyncio.to_thread(self.ai.generate_image, prompt=prompt, size=supported_size, tier=tier)
                image_data, data_type = self.extract_image_data(response)
                if data_type == 'base64':
                    if dalle_dimension != actual_dimension:
                        target_size = tuple(map(int, actual_dimension.lower().split('x')))
                        await self.save_and_resize_image(image_data, file_path, image_format, target_size)
                    else:
                        await self.save_image_data(image_data, file_path, image_format)
                elif data_type == 'url':
                    target_size = tuple(map(int, actual_dimension.lower().split('x'))) if dalle_dimension != actual_dimension else None
                    await self.fetch_and_save_image_from_url(image_data, file_path, image_format, target_size)
                else:
                    raise ValueError("Unsupported image data type.")
                logger.info(f" #### `SnowX` generated {Path(file_path).name}.")
                break
            except Exception as e:
                logger.error(f"  Error during attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                else:
                    logger.error("\n #### Max retries reached. Operation aborted.")
                    logger.debug(f" #### Prompt: {prompt}")
                    raise

    async def process_image_generation_pro(self, steps: List[Dict], tier: str):
        """
        Processes image generation steps concurrently, limited to exactly 2 active tasks at a time.
        When one task completes, the next task starts immediately to maintain 2 concurrent tasks.
        """
        async def generate_image_task(step):
            try:
                await self.generate_image(
                    prompt=step['prompt'],
                    dalle_dimension=step['dalle_dimension'],
                    actual_dimension=step['actual_dimension'],
                    image_format=step['format'],
                    file_path=step['file_path'],
                    tier=tier
                )
                filename = Path(step['file_path']).name
                full_path = step['file_path']
                logger.info(f"![{filename}](<{full_path}>)")
            except Exception as e:
                logger.error(f"  Failed to generate image {step}: {str(e)}")

        active_tasks = set()
        pending_steps = steps.copy()

        while pending_steps or active_tasks:
            # Start new tasks if we have less than 2 active and there are pending steps
            while len(active_tasks) < 2 and pending_steps:
                step = pending_steps.pop(0)
                task = asyncio.create_task(generate_image_task(step))
                active_tasks.add(task)

            # Wait for any task to complete
            if active_tasks:
                done, pending = await asyncio.wait(active_tasks, return_when=asyncio.FIRST_COMPLETED)
                active_tasks = pending  # Update active tasks to only include pending ones

                # Handle any exceptions from completed tasks
                for task in done:
                    try:
                        await task
                    except Exception as e:
                        logger.error(f"Task failed with error: {str(e)}")

    async def process_image_generation(self, steps: List[Dict], tier: str):
        """
        Processes each image generation step sequentially.
        """
        for step in steps:
            try:
                await self.generate_image(
                    prompt=step['prompt'],
                    dalle_dimension=step['dalle_dimension'],
                    actual_dimension=step['actual_dimension'],
                    image_format=step['format'],
                    file_path=step['file_path'],
                    tier=tier
                )

                filename = Path(step['file_path']).name
                full_path = step['file_path']
                logger.info(f"![{filename}](<{full_path}>)")

            except Exception as e:
                logger.error(f"  Failed to generate image {step}: {str(e)}")
                continue

    async def generate_images(self, task: Dict, tier):
        """
        Generates images based on the given task.
        """
        steps = task.get('steps', [])
        
        # Filter for eligible image formats
        eligible_formats = {'png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'ico'}
        filtered_steps = [
            step for step in steps 
            if step.get('format', '').lower() in {fmt.lower() for fmt in eligible_formats}
        ]

        if not filtered_steps:
            logger.debug("\n #### No eligible steps for image generation.")
            return

        logger.info(f" #### `SnowX` starting generation of {len(filtered_steps)} image(s).")
        
        logger.info(" #### `SnowX` starting image generation.")
        await self.process_image_generation(filtered_steps, tier)
       
        logger.info(" #### `SnowX` completed image generation.")
        logger.info("-------------------------------------------------")