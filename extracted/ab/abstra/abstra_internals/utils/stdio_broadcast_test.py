import json
import threading
import unittest
from typing import Type, cast
from unittest.mock import MagicMock, Mock, patch

from pika.adapters.blocking_connection import BlockingConnection
from pika.exceptions import AMQPConnectionError, AMQPError

from abstra_internals.utils.stdio_broadcast import (
    STDIO_BROADCAST_EXCHANGE,
    StdioBroadcastPublisher,
    start_stdio_broadcast_consumer,
)


def _make_mock_pika_connection():
    """Create a mock pika BlockingConnection with channel."""
    mock_conn = MagicMock()
    mock_conn.is_open = True
    mock_conn.is_closed = False
    mock_channel = MagicMock()
    mock_channel.is_open = True
    mock_channel.is_closed = False
    mock_conn.channel.return_value = mock_channel
    return mock_conn, mock_channel


class TestStdioBroadcastPublisher(unittest.TestCase):
    def setUp(self):
        StdioBroadcastPublisher.reset()

    def tearDown(self):
        StdioBroadcastPublisher.reset()

    def test_publish_sends_to_exchange(self):
        """Publisher should publish JSON messages to the stdio_broadcast fanout exchange."""
        mock_conn, mock_channel = _make_mock_pika_connection()
        factory = Mock(return_value=mock_conn)

        publisher = StdioBroadcastPublisher(
            "amqp://localhost",
            connection_factory=cast(Type[BlockingConnection], factory),
        )

        message = {
            "type": "stdio_batch",
            "payload": [{"type": "stdout", "log": "hello"}],
        }
        publisher.publish(message)

        mock_channel.basic_publish.assert_called_once()
        call_kwargs = mock_channel.basic_publish.call_args
        self.assertEqual(call_kwargs[1]["exchange"], STDIO_BROADCAST_EXCHANGE)
        self.assertEqual(call_kwargs[1]["routing_key"], "")

        body = call_kwargs[1]["body"]
        parsed = json.loads(body.decode("utf-8"))
        self.assertEqual(parsed["type"], "stdio_batch")

        publisher.close()

    def test_publish_declares_fanout_exchange(self):
        """Publisher should declare a durable fanout exchange on connect."""
        mock_conn, mock_channel = _make_mock_pika_connection()
        factory = Mock(return_value=mock_conn)

        publisher = StdioBroadcastPublisher(
            "amqp://localhost",
            connection_factory=cast(Type[BlockingConnection], factory),
        )

        mock_channel.exchange_declare.assert_called_once_with(
            exchange=STDIO_BROADCAST_EXCHANGE,
            exchange_type="fanout",
            durable=True,
        )

        publisher.close()

    def test_publish_reconnects_on_failure(self):
        """If publish fails, publisher should reconnect and retry."""
        mock_conn, mock_channel = _make_mock_pika_connection()
        factory = Mock(return_value=mock_conn)

        publisher = StdioBroadcastPublisher(
            "amqp://localhost",
            connection_factory=cast(Type[BlockingConnection], factory),
        )

        # First publish fails
        mock_channel.basic_publish.side_effect = [AMQPError("connection lost"), None]
        # After reconnect, connection is open
        mock_conn.is_closed = False
        mock_channel.is_closed = False

        publisher.publish({"type": "stdio", "payload": {}})

        # Should have been called twice (first fails, second succeeds after reconnect)
        self.assertEqual(mock_channel.basic_publish.call_count, 2)

        publisher.close()

    def test_publish_silently_drops_on_persistent_failure(self):
        """If both publish attempts fail, no exception should be raised."""
        mock_conn, mock_channel = _make_mock_pika_connection()
        factory = Mock(return_value=mock_conn)

        publisher = StdioBroadcastPublisher(
            "amqp://localhost",
            connection_factory=cast(Type[BlockingConnection], factory),
        )

        mock_channel.basic_publish.side_effect = AMQPError("persistent failure")

        # Should not raise
        publisher.publish({"type": "stdio", "payload": {}})

        publisher.close()

    def test_singleton_returns_same_instance(self):
        """get_or_create should return the same instance on repeated calls."""
        mock_conn, _ = _make_mock_pika_connection()
        factory = Mock(return_value=mock_conn)

        with patch(
            "abstra_internals.utils.stdio_broadcast.pika.BlockingConnection",
            factory,
        ):
            pub1 = StdioBroadcastPublisher.get_or_create("amqp://localhost")
            pub2 = StdioBroadcastPublisher.get_or_create("amqp://localhost")
            self.assertIs(pub1, pub2)

            pub1.close()

    def test_singleton_reset_clears_instance(self):
        """reset() should allow creating a new instance."""
        mock_conn, _ = _make_mock_pika_connection()
        factory = Mock(return_value=mock_conn)

        with patch(
            "abstra_internals.utils.stdio_broadcast.pika.BlockingConnection",
            factory,
        ):
            pub1 = StdioBroadcastPublisher.get_or_create("amqp://localhost")
            StdioBroadcastPublisher.reset()
            pub2 = StdioBroadcastPublisher.get_or_create("amqp://localhost")
            self.assertIsNot(pub1, pub2)

            pub2.close()

    def test_publish_after_close_is_noop(self):
        """Publishing after close should silently do nothing."""
        mock_conn, mock_channel = _make_mock_pika_connection()
        factory = Mock(return_value=mock_conn)

        publisher = StdioBroadcastPublisher(
            "amqp://localhost",
            connection_factory=cast(Type[BlockingConnection], factory),
        )
        publisher.close()

        mock_channel.basic_publish.reset_mock()
        publisher.publish({"type": "stdio", "payload": {}})
        mock_channel.basic_publish.assert_not_called()

    def test_connection_failure_on_init_does_not_raise(self):
        """If RabbitMQ is unavailable on init, publisher should not raise."""
        factory = Mock(side_effect=AMQPConnectionError("connection refused"))

        # Should not raise
        publisher = StdioBroadcastPublisher(
            "amqp://localhost",
            connection_factory=cast(Type[BlockingConnection], factory),
        )

        publisher.close()


def _make_consumer_channel(messages):
    """Create a mock channel that yields the given messages from consume().

    Each message is a dict that will be JSON-encoded as the body.
    The channel.consume() generator yields (method, properties, body) tuples,
    followed by (None, None, None) for inactivity timeouts.
    """
    mock_conn = MagicMock()
    mock_conn.is_open = True
    mock_channel = MagicMock()
    mock_conn.channel.return_value = mock_channel

    # queue_declare returns result with method.queue
    queue_result = MagicMock()
    queue_result.method.queue = "auto-gen-queue-123"
    mock_channel.queue_declare.return_value = queue_result

    method_frame = MagicMock()
    encoded_messages = []
    for msg in messages:
        encoded_messages.append((method_frame, None, json.dumps(msg).encode("utf-8")))
    # Add a None frame to end the loop iteration
    encoded_messages.append((None, None, None))

    mock_channel.consume.return_value = iter(encoded_messages)
    return mock_conn, mock_channel


class TestStdioBroadcastConsumer(unittest.TestCase):
    """Tests for start_stdio_broadcast_consumer."""

    @patch("abstra_internals.utils.stdio_broadcast.pika.BlockingConnection")
    @patch("abstra_internals.controllers.execution.execution_stdio.BroadcastController")
    def test_consumer_unpacks_stdio_batch_and_broadcasts(
        self, mock_bc, mock_pika_conn_cls
    ):
        """stdio_batch messages should be unpacked into individual stdio broadcasts."""
        batch_msg = {
            "type": "stdio_batch",
            "payload": [
                {"type": "stdout", "log": "line1"},
                {"type": "stderr", "log": "line2"},
                {"type": "stdout", "log": "line3"},
            ],
        }
        mock_conn, mock_channel = _make_consumer_channel([batch_msg])
        mock_pika_conn_cls.return_value = mock_conn

        stop_event = threading.Event()

        # Make consume raise after yielding messages to stop the loop
        def consume_then_stop(*args, **kwargs):
            yield from _make_consumer_channel([batch_msg])[1].consume.return_value
            stop_event.set()

        mock_channel.consume.side_effect = consume_then_stop

        thread, _ = start_stdio_broadcast_consumer(
            "amqp://localhost", stop_event=stop_event
        )
        thread.join(timeout=2.0)

        # Should have broadcast 3 individual stdio messages
        self.assertEqual(mock_bc.broadcast.call_count, 3)

    @patch("abstra_internals.utils.stdio_broadcast.pika.BlockingConnection")
    @patch("abstra_internals.controllers.execution.execution_stdio.BroadcastController")
    def test_consumer_broadcasts_stdio_directly(self, mock_bc, mock_pika_conn_cls):
        """stdio messages should be broadcast directly."""
        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        mock_conn, mock_channel = _make_consumer_channel([stdio_msg])
        mock_pika_conn_cls.return_value = mock_conn

        stop_event = threading.Event()

        def consume_then_stop(*args, **kwargs):
            yield from _make_consumer_channel([stdio_msg])[1].consume.return_value
            stop_event.set()

        mock_channel.consume.side_effect = consume_then_stop

        thread, _ = start_stdio_broadcast_consumer(
            "amqp://localhost", stop_event=stop_event
        )
        thread.join(timeout=2.0)

        self.assertEqual(mock_bc.broadcast.call_count, 1)

    @patch("abstra_internals.utils.stdio_broadcast.pika.BlockingConnection")
    @patch("abstra_internals.controllers.execution.execution_stdio.BroadcastController")
    def test_consumer_broadcasts_task_messages(self, mock_bc, mock_pika_conn_cls):
        """task messages should be broadcast directly via fanout consumer."""
        task_msg = {"type": "task", "payload": {"id": "t1", "status": "completed"}}
        mock_conn, mock_channel = _make_consumer_channel([task_msg])
        mock_pika_conn_cls.return_value = mock_conn

        stop_event = threading.Event()

        def consume_then_stop(*args, **kwargs):
            yield from _make_consumer_channel([task_msg])[1].consume.return_value
            stop_event.set()

        mock_channel.consume.side_effect = consume_then_stop

        thread, _ = start_stdio_broadcast_consumer(
            "amqp://localhost", stop_event=stop_event
        )
        thread.join(timeout=2.0)

        mock_bc.broadcast.assert_called_once()
        broadcast_msg = json.loads(mock_bc.broadcast.call_args[1]["msg"])
        self.assertEqual(broadcast_msg["type"], "task")
        self.assertEqual(broadcast_msg["payload"]["id"], "t1")
