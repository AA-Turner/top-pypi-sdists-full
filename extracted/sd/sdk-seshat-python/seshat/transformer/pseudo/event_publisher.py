import logging
import weakref
from typing import Callable, List

from seshat.data_class import SFrame
from seshat.publisher.client.base import QueueClient
from seshat.publisher.event.base import Event
from seshat.transformer import Transformer

logger = logging.getLogger(__name__)


def _flush_or_close(client: QueueClient, owns_client: bool) -> None:
    if owns_client:
        try:
            client.close()
        except Exception as exc:
            logger.warning("EventPublisher client close failed: %s", exc)
    else:
        try:
            client.flush(timeout=5.0)
        except Exception as exc:
            logger.warning("EventPublisher flush failed: %s", exc)


class EventPublisher(Transformer):
    """
    A pass-through transformer that publishes events to a queue without
    interrupting the pipeline. Accepts a user-supplied event_builder callable
    that maps the current SFrame to a list of Event objects.

    Publishing is fire-and-forget: send errors are logged at ERROR level but
    never raised, so the pipeline is never interrupted by broker failures.
    Use client.flush() explicitly if you need a synchronous delivery barrier.

    Parameters
    ----------
    client : QueueClient
        The queue client to use for publishing (e.g. KafkaClient).
    topic : str
        The topic/channel to publish events to.
    event_builder : Callable[[SFrame], List[Event]]
        A callable that receives the SFrame and returns the events to publish.
    create_topic : bool
        If True, ensure the topic exists before the first publish. Default False.
    owns_client : bool
        If True, close() will flush and close the client when the publisher
        shuts down. Default False — the caller is responsible for closing the
        client. Set to True when the publisher exclusively owns the client
        (e.g. created inline). Set to False when sharing a client across
        multiple publishers or managing its lifecycle externally.
    group_keys : dict, optional
        Keys used to identify and retrieve data from a grouped SFrame.
    """

    def __init__(
        self,
        client: QueueClient,
        topic: str,
        event_builder: Callable[[SFrame], List[Event]],
        create_topic: bool = False,
        owns_client: bool = False,
        group_keys=None,
    ):
        super().__init__(group_keys)
        self.client = client
        self.topic = topic
        self.event_builder = event_builder
        self.create_topic = create_topic
        self.owns_client = owns_client
        self._topic_ensured = False
        self._finalizer = weakref.finalize(self, _flush_or_close, client, owns_client)

    def __call__(self, sf_input: SFrame, *args, **kwargs) -> SFrame:
        if self.create_topic and not self._topic_ensured:
            self.client.ensure_topic(self.topic)
            self._topic_ensured = True
        events = self.event_builder(sf_input)
        for event in events:
            self.client.publish(
                topic=self.topic,
                value=event.model_dump_json().encode(),
            )
        return sf_input

    def close(self) -> None:
        self._finalizer()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def calculate_complexity(self):
        return 1
