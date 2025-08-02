# arpakit

import asyncio
import logging
from typing import Any
from urllib.parse import urljoin

from aiohttp import ClientResponse
from pydantic import ConfigDict, BaseModel

from arpakitlib.ar_base64_util import convert_base64_string_to_bytes
from arpakitlib.ar_http_request_util import async_make_http_request

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseAPIModel(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)


class GenerateImageFromNumberResApiModel(BaseAPIModel):
    image_filename: str
    image_url: str
    image_base64: str

    def save_file(self, filepath: str):
        with open(filepath, mode="wb") as f:
            f.write(convert_base64_string_to_bytes(base64_string=self.image_base64))
        return filepath


class DREAMAIAPIClient:
    def __init__(
            self,
            *,
            base_url: str = "https://api.dreamai.arpakit.com/api/v1",
            api_key: str | None = "1"
    ):
        self._logger = logging.getLogger(__name__)
        self.api_key = api_key
        base_url = base_url.strip()
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key is not None:
            self.headers.update({"apikey": api_key})

    async def _async_make_http_request(
            self,
            *,
            method: str = "GET",
            url: str,
            params: dict[str, Any] | None = None
    ) -> ClientResponse:
        response = await async_make_http_request(
            method=method,
            url=url,
            params=params,
            headers=self.headers,
        )
        response.raise_for_status()
        return response

    async def healthcheck(self) -> bool:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "healthcheck"))
        json_data = await response.json()
        return json_data["data"]["healthcheck"] == "healthcheck"

    async def is_healthcheck_good(self) -> bool:
        try:
            return await self.healthcheck()
        except Exception as exception:
            self._logger.error(exception)
            return False

    async def generate_image_from_number(self, *, number: int) -> GenerateImageFromNumberResApiModel:
        response = await self._async_make_http_request(
            method="GET",
            url=urljoin(self.base_url, "generate_image_from_number"),
            params={"number": number}
        )
        json_data = await response.json()
        return GenerateImageFromNumberResApiModel.model_validate(json_data)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
