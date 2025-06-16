from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Dict, List, Optional, Type, Union

import httpx
from pydantic import BaseModel


class BaseClient(ABC):
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 10,
    ):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self.timeout = timeout

    @abstractmethod
    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json: Union[Dict[str, Any], List[Dict[str, Any]], None] = None,
        params: Optional[Union[Dict[str, Any], List[tuple[str, Any]]]] = None,
    ) -> Any:
        pass


class HttpClient(BaseClient):
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 10,
    ):
        super().__init__(base_url, token, timeout)
        self.client = httpx.AsyncClient()

    async def __aenter__(self) -> "HttpClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json: Union[Dict[str, Any], List[Dict[str, Any]], None] = None,
        params: Optional[Union[Dict[str, Any], List[tuple[str, Any]]]] = None,
        **kwargs: Dict[str, Any],
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": self.headers,
            "params": params,
        }
        if json is not None:
            if isinstance(json, BaseModel):
                request_kwargs["json"] = json.model_dump(exclude_none=True)
            elif isinstance(json, (dict, list)):
                request_kwargs["json"] = json  # type: ignore
            else:
                raise ValueError(f"Unsupported JSON type: {type(json)}")
        for key, value in kwargs.items():
            if key not in request_kwargs:
                request_kwargs[key] = value

        response = await self.client.request(
            **request_kwargs, timeout=self.timeout  # type: ignore
        )
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        if self.client:
            await self.client.aclose()
