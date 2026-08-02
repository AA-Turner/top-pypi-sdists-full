r"""Contain factories for document ingestors."""

from __future__ import annotations

__all__ = ["BaseIngestorFactory", "ConfigurableIngestorFactory", "IngestorFactory"]

from zenpyre.ingestors.factory.base import BaseIngestorFactory
from zenpyre.ingestors.factory.configurable import ConfigurableIngestorFactory
from zenpyre.ingestors.factory.vanilla import IngestorFactory
