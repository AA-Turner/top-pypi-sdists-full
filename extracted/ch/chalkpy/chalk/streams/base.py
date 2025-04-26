from __future__ import annotations

from typing import Any, Optional


class StreamSource:
    """Base class for all stream sources generated from `@stream`."""

    registry: "list[StreamSource]" = []
    name: Optional[str] = None

    def _config_to_json(self) -> Any:
        return self.config_to_json()  # for backcompat

    def config_to_json(self):
        raise NotImplementedError()

    def _recreate_integration_variables(self) -> dict[str, str]:
        raise NotImplementedError()

    @property
    def streaming_type(self) -> str:
        """e.g. 'kafka' or 'kinesis' or 'pubsub'"""
        raise NotImplementedError()

    @property
    def dlq_name(self) -> str | None:
        """
        Identifier for the dead-letter queue (DLQ) for the stream.
        If not specified, failed messages will be dropped.
        Stream name for Kinesis, topic name for Kafka, subscription id for PubSub.
        """
        raise NotImplementedError()

    @property
    def stream_or_topic_name(self) -> str:
        """
        Identifier for the stream to consume.
        Stream name for Kinesis, topic name for Kafka, subscription id for PubSub
        """
        raise NotImplementedError()
