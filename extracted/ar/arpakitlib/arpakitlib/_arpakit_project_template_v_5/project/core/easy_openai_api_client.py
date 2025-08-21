import asyncio
from functools import lru_cache

import httpx
from openai import OpenAI, AsyncOpenAI

from arpakitlib.ar_openai_api_client_util import EasyOpenAIAPIClient
from project.core.settings import get_cached_settings


def create_easy_openai_api_client() -> EasyOpenAIAPIClient | None:
    if get_cached_settings().openai_api_key is None:
        return None

    return EasyOpenAIAPIClient(
        open_ai=OpenAI(
            api_key=get_cached_settings().openai_api_key,
            base_url=get_cached_settings().openai_api_base_url,
            timeout=httpx.Timeout(
                timeout=60,
                connect=15,
                read=60,
                write=60,
                pool=15
            )
        ),
        async_open_ai=AsyncOpenAI(
            api_key=get_cached_settings().openai_api_key,
            base_url=get_cached_settings().openai_api_base_url
        )
    )


@lru_cache()
def get_cached_easy_openai_api_client() -> EasyOpenAIAPIClient | None:
    return create_easy_openai_api_client()


async def __async_example():
    pass


if __name__ == '__main__':
    asyncio.run(__async_example())
