"""
Vortex producer module for sending data to Kafka.

This module provides the client and utilities needed to produce messages
to Kafka in the Vortex message format.
"""

# this must be preloaded to suppress ddtrace logs at import time.
import dbtlabs_vortex.producer.ddtrace  # noqa
from dbtlabs_vortex.producer.client import VortexProducerClient, log_proto, shutdown

__all__ = ["VortexProducerClient", "log_proto", "shutdown"]
