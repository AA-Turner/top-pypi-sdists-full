r"""Contain factories for data processors."""

from __future__ import annotations

__all__ = ["BaseProcessorFactory", "ConfigurableProcessorFactory", "ProcessorFactory"]

from zenpyre.data_processors.factory.base import BaseProcessorFactory
from zenpyre.data_processors.factory.configurable import ConfigurableProcessorFactory
from zenpyre.data_processors.factory.vanilla import ProcessorFactory
