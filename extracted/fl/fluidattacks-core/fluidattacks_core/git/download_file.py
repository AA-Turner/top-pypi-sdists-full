import logging
from pathlib import Path

import aiofiles
import aiohttp

LOGGER = logging.getLogger(__name__)


async def download_file(url: str, destination_path: str) -> bool:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3600)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(destination_path, "wb") as file:
                    while True:
                        try:
                            chunk = await response.content.read(1024 * 10)
                        except TimeoutError:
                            LOGGER.warning("Read timeout")
                            return False
                        if not chunk:
                            break
                        await file.write(chunk)
                return Path(destination_path).exists()

    return False
