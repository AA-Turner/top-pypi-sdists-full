""" Generic GraphQL Helpers """
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Type, TypeVar

ModelT = TypeVar('ModelT', bound='DeserializableModel')


class DeserializableModel(ABC):
    """ A model type that is deserializable
    """

    @classmethod
    @abstractmethod
    def from_mapi_response(cls: Type[ModelT], response: Dict[str, Any]) -> ModelT:
        ...


def convert_datetime(timestring: str) -> datetime:
    """Convert a PostgresQL timestring to a datetime object
    """
    timestring = timestring.replace('Z', '+00:00')
    return datetime.fromisoformat(timestring)
