import abc
import logging
import selectors

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

logger = logging.getLogger(__name__)


class QueueClient(abc.ABC):
    @abc.abstractmethod
    def publish(self, topic: str, value: bytes) -> None: ...

    @abc.abstractmethod
    def ensure_topic(self, topic: str) -> None: ...

    @abc.abstractmethod
    def flush(self, timeout: float | None = None) -> None: ...

    @abc.abstractmethod
    def close(self) -> None: ...


class KafkaClient(QueueClient):
    def __init__(
        self,
        bootstrap_servers: str | list[str],
        num_partitions: int = 1,
        replication_factor: int = 1,
        **producer_kwargs,
    ):
        self._bootstrap_servers = bootstrap_servers
        self._num_partitions = num_partitions
        self._replication_factor = replication_factor
        self._producer_kwargs = producer_kwargs
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            **producer_kwargs,
        )

    def publish(self, topic: str, value: bytes) -> None:
        future = self._producer.send(topic, value=value)
        future.add_errback(lambda exc: logger.error("Kafka publish failed for topic %s: %s", topic, exc))

    def ensure_topic(self, topic: str) -> None:
        admin = KafkaAdminClient(
            bootstrap_servers=self._bootstrap_servers,
            selector=selectors.PollSelector,
        )
        try:
            admin.create_topics([NewTopic(
                name=topic,
                num_partitions=self._num_partitions,
                replication_factor=self._replication_factor,
            )])
        except TopicAlreadyExistsError:
            pass
        finally:
            admin.close()

    def flush(self, timeout: float | None = None) -> None:
        self._producer.flush(timeout=timeout)

    def close(self) -> None:
        self._producer.flush()
        self._producer.close()