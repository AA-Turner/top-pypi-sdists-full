"""
Custom exceptions for Vortex client operations.

This module defines the exceptions that might be raised during Vortex client operations.
"""


class VortexClientError(Exception):
    """Base exception class for all Vortex client errors."""

    pass


class ValidationError(VortexClientError):
    """Raised when a message fails validation."""

    pass


class ConnectionError(VortexClientError):
    """Raised when a connection to Kafka or Iceberg cannot be established."""

    pass


class ProducerError(VortexClientError):
    """Raised when there is an error producing messages to Kafka."""

    pass


class ConsumerError(VortexClientError):
    """Raised when there is an error consuming messages from Kafka."""

    pass


class AnalysisError(VortexClientError):
    """Raised when there is an error during data analysis or querying."""

    pass
