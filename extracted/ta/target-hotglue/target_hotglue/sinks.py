"""Hotglue target sink class, which handles writing streams."""
from abc import ABC, abstractmethod

from pydantic import BaseModel
from target_hotglue.client import HotglueSink

class ModelSink(HotglueSink):
    """Model target sink class."""

    @abstractmethod
    def preprocess_record(self, record: dict, context: dict) -> dict:
        pass

    @abstractmethod
    def process_record(self, record: dict, context: dict) -> None:
        pass
