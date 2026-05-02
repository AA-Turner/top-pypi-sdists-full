import math
import os.path
from io import BytesIO
from sys import getsizeof
from tempfile import TemporaryDirectory
from typing import Optional

from PIL.Image import open as open_image, Image

from spotipyio.logic.consts.image_consts import RGB
from spotipyio.logic.internal_tools.logging import logger
from spotipyio.logic.utils import get_current_timestamp, read_image


class ImageCompressor:
    def compress(
        self, image: bytes, target_size_in_kb: int = 256, quality_interval: int = 5, file_type: str = "jpeg"
    ) -> Optional[bytes]:
        with TemporaryDirectory() as dir_path:
            logger.info(f"Starting to compress image. Target size: {target_size_in_kb}")
            serialized_image = self._serialize_image(image)
            compressed_image_path = self._apply_compression_loop(
                image=serialized_image,
                dir_path=dir_path,
                target_size_in_kb=target_size_in_kb,
                quality_interval=quality_interval,
                file_type=file_type,
            )

            return self._read_compressed_image(compressed_image_path)

    @staticmethod
    def _serialize_image(image: bytes) -> Image:
        image_io = BytesIO(image)
        serialized_image = open_image(image_io)

        if serialized_image.mode.lower() != RGB:
            serialized_image = serialized_image.convert(RGB)

        return serialized_image

    def _apply_compression_loop(
        self, image: Image, dir_path: str, target_size_in_kb: int, quality_interval: int, file_type: str
    ) -> Optional[str]:
        quality = 100
        image_path = None
        image_size = math.inf

        while image_size > target_size_in_kb and quality > 0:
            logger.debug(f"Compressing image using {quality} quality ratio")
            timestamp = get_current_timestamp()
            image_path = os.path.join(dir_path, f"{timestamp}.{file_type}")
            image.save(image_path, quality=quality)
            image_size = self._get_encoded_image_size_in_kb(image_path)
            quality -= quality_interval

        return self._get_compressed_image_path(quality, image_path, image_size)

    @staticmethod
    def _get_encoded_image_size_in_kb(image_path: str) -> float:
        image = read_image(image_path)
        return getsizeof(image) / 1024

    @staticmethod
    def _get_compressed_image_path(quality: int, image_path: str, image_size: float) -> Optional[str]:
        if quality > 0:
            logger.info(
                f"Successfully compressed image using {quality} quality ratio to size of {image_size} KB. Returning "
                f"saved image path"
            )
            return image_path

        else:
            logger.warn("Could not compress image below requested target size. Returning None instead.")

    @staticmethod
    def _read_compressed_image(path: Optional[str]) -> Optional[bytes]:
        if path is None:
            return

        with open(path, "rb") as f:
            return f.read()
