"""Abstract class for API resources.
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generator, Union

from pydantic import BaseModel

from databricks_genai_inference.api.abstract.foundation_model_object import FoundationModelObject


class APIResource(ABC):
    """ Abstract class for API resources.
    """

    @classmethod
    @abstractmethod
    def create(cls, **kwargs) -> Union[FoundationModelObject, Generator[FoundationModelObject, None, None]]:
        pass

    @classmethod
    @abstractmethod
    def _parse_and_validate_request(cls, **kwargs) -> BaseModel:
        pass

    @classmethod
    @abstractmethod
    def _get_non_streaming_response(cls, client, url, headers, json, timeout) -> FoundationModelObject:
        pass

    @classmethod
    @abstractmethod
    def _get_streaming_response(cls, url, client, headers, json,
                                timeout) -> Generator[FoundationModelObject, None, None]:
        pass

    @classmethod
    @abstractmethod
    async def acreate(cls, **kwargs) -> Union[FoundationModelObject, AsyncGenerator[FoundationModelObject, None]]:
        pass

    @classmethod
    @abstractmethod
    async def _aget_non_streaming_response(cls, client, url, headers, json, timeout) -> FoundationModelObject:
        pass

    @classmethod
    @abstractmethod
    async def _aget_streaming_response(cls, client, url, headers, json,
                                       timeout) -> AsyncGenerator[FoundationModelObject, None]:
        pass
