# arpakit

from __future__ import annotations

import asyncio
import logging

import httpx
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion

from arpakitlib.ar_base64_util import convert_file_to_base64_string

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

"""
https://platform.openai.com/docs/
"""


class EasyOpenAIAPIClient:
    def __init__(
            self,
            *,
            open_ai: OpenAI,
            async_open_ai: AsyncOpenAI
    ):
        self._logger = logging.getLogger(self.__class__.__name__)

        self.open_ai = open_ai
        self.async_open_ai = async_open_ai

    @classmethod
    def create_easily(
            cls,
            openai_api_key: str,
            openai_api_base_url: str | None = "https://api.proxyapi.ru/openai/v1"
    ) -> EasyOpenAIAPIClient:
        return EasyOpenAIAPIClient(
            open_ai=OpenAI(
                api_key=openai_api_key,
                base_url=openai_api_base_url,
                timeout=httpx.Timeout(
                    timeout=300,  # общий таймаут
                    connect=60,  # таймаут подключения
                    read=300,  # чтение ответа
                    write=60,  # запись запроса
                    pool=60  # пул соединений
                )
            ),
            async_open_ai=AsyncOpenAI(
                api_key=openai_api_key,
                base_url=openai_api_base_url,
                http_client=httpx.AsyncClient(
                    timeout=httpx.Timeout(
                        timeout=300,
                        connect=60,
                        read=300,
                        write=60,
                        pool=60
                    )
                )
            )
        )

    def check_conn(self):
        self.open_ai.models.list()

    def is_conn_good(self) -> bool:
        try:
            self.check_conn()
            return True
        except Exception as e:
            self._logger.error(e)
        return False

    async def async_check_conn(self):
        await self.async_open_ai.models.list()

    async def async_is_conn_good(self) -> bool:
        try:
            await self.async_check_conn()
            return True
        except Exception as e:
            self._logger.error(e)
        return False

    def simple_ask(
            self,
            *,
            prompt: str | None = None,
            text: str,
            model: str = "gpt-4o",
            image_links: str | list[str] | None = None,
            image_filepaths: str | list[str] | None = None
    ) -> ChatCompletion:
        if isinstance(image_links, str):
            image_links = [image_links]
        if isinstance(image_filepaths, str):
            image_filepaths = [image_filepaths]

        messages = []

        if prompt is not None:
            messages.append({
                "role": "system",
                "content": prompt
            })

        content = [{"type": "text", "text": text}]

        if image_links:
            for link in image_links:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": link}
                })

        if image_filepaths:
            for path in image_filepaths:
                base64_url = convert_file_to_base64_string(filepath=path, raise_for_error=True)
                content.append({
                    "type": "image_url",
                    "image_url": {"url": base64_url}
                })

        messages.append({
            "role": "user",
            "content": content
        })

        response: ChatCompletion = self.open_ai.chat.completions.create(
            model=model,
            messages=messages,
            n=1,
            temperature=0.1,
            top_p=0.9,
            max_tokens=1000
        )

        return response

    async def async_simple_ask(
            self,
            *,
            prompt: str | None = None,
            text: str,
            model: str = "gpt-4o",
            image_links: str | list[str] | None = None,
            image_filepaths: str | list[str] | None = None
    ) -> ChatCompletion:
        if isinstance(image_links, str):
            image_links = [image_links]
        if isinstance(image_filepaths, str):
            image_filepaths = [image_filepaths]

        messages = []

        if prompt is not None:
            messages.append({
                "role": "system",
                "content": prompt
            })

        content = [{"type": "text", "text": text}]

        if image_links:
            for link in image_links:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": link}
                })

        if image_filepaths:
            for path in image_filepaths:
                base64_url = convert_file_to_base64_string(filepath=path, raise_for_error=True)
                content.append({
                    "type": "image_url",
                    "image_url": {"url": base64_url}
                })

        messages.append({
            "role": "user",
            "content": content
        })

        response: ChatCompletion = await self.async_open_ai.chat.completions.create(
            model=model,
            messages=messages,
            n=1,
            temperature=0.1,
            top_p=0.9,
            max_tokens=1000
        )

        return response


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
