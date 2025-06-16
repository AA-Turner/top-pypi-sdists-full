import asyncio
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from whiskerrag_types.model.multi_modal import Image


class BaseEmbedding(ABC):

    @classmethod
    def sync_health_check(cls) -> bool:
        def run_async_in_thread() -> bool:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(cls.health_check())
            finally:
                loop.close()

        if threading.current_thread() is threading.main_thread():
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(run_async_in_thread)
                return future.result()
        else:
            return run_async_in_thread()

    @classmethod
    @abstractmethod
    async def health_check(cls) -> bool:
        pass

    @abstractmethod
    async def embed_text(self, text: str, timeout: Optional[int]) -> List[float]:
        pass

    @abstractmethod
    async def embed_text_query(self, text: str, timeout: Optional[int]) -> List[float]:
        pass

    @abstractmethod
    async def embed_image(self, image: Image, timeout: Optional[int]) -> List[float]:
        pass
