import logging
from pathlib import Path

import aiofiles
import aiohttp

from .constants import DEFAULT_DOWNLOAD_BUFFER_SIZE

LOGGER = logging.getLogger(__name__)


async def download_file(
    *,
    url: str,
    destination_path: str,
    download_buffer_size: int = DEFAULT_DOWNLOAD_BUFFER_SIZE,
) -> bool:
    timeout = aiohttp.ClientTimeout(total=60 * 60, connect=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:  # noqa: SIM117
        async with session.get(url) as response:
            if response.status != 200:
                LOGGER.error(
                    "Failed to download file: HTTP %s, for path %s",
                    response.status,
                    destination_path,
                )
                return False

            async with aiofiles.open(destination_path, "wb") as file:
                while True:
                    try:
                        chunk = await response.content.read(download_buffer_size)
                    except TimeoutError:
                        LOGGER.exception("Read timeout for path %s", destination_path)
                        return False
                    if not chunk:
                        break
                    await file.write(chunk)

            return Path(destination_path).exists()
