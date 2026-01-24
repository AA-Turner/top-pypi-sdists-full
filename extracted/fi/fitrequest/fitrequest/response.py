from http import HTTPStatus

import aiofiles
import httpx
from pydantic import BaseModel

from fitrequest.errors import HTTPStatusError
from fitrequest.response_formatter import ResponseFormatter


class Response:
    def __init__(
        self,
        httpx_response: httpx.Response,
        raise_for_status: bool = True,
        json_path: str | None = None,
        response_model: type[BaseModel] | None = None,
        client_name: str = 'fitrequest',
    ) -> None:
        self.client_name = client_name
        self.httpx_response = httpx_response

        if raise_for_status:
            self.handle_http_error()

        formatter = ResponseFormatter(
            httpx_response=httpx_response,
            json_path=json_path,
            response_model=response_model,
        )
        self.data = formatter.data
        self.data_bytes = formatter.data_bytes

    def handle_http_error(self) -> None:
        try:
            self.httpx_response.raise_for_status()
        except httpx.HTTPError as err:
            status_code = self.httpx_response.status_code
            content = self.httpx_response.content
            details = None

            if status_code == HTTPStatus.UNAUTHORIZED:
                details = (
                    f'\nInvalid {self.client_name} credentials. '
                    'Make sure settings are provided during initialization or set as environment variables.'
                ).strip()

            raise HTTPStatusError(status_code, content, details) from err

    def save_data(self, filepath: str, mode: str = 'xb') -> None:
        with open(filepath, mode=mode) as data_file:
            data_file.write(self.data_bytes)

    async def async_save_data(self, filepath: str, mode: str = 'xb') -> None:
        async with aiofiles.open(filepath, mode=mode) as data_file:
            await data_file.write(self.data_bytes)
