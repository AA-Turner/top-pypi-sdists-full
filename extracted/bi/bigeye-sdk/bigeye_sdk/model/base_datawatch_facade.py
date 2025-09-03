from __future__ import annotations

import abc

from pydantic.v1.dataclasses import dataclass

# create logger
from bigeye_sdk import DatawatchObject
from bigeye_sdk.log import get_logger

log = get_logger(__name__)

@dataclass
class DatawatchFacade(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_datawatch_object(cls, obj: DatawatchObject) -> DatawatchFacade:
        pass

    @abc.abstractmethod
    def to_datawatch_object(self, **kwargs) -> DatawatchObject:
        pass