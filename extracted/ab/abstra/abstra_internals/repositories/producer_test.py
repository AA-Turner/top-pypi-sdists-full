import unittest
from unittest.mock import MagicMock, patch

from ..entities.execution_context import HookContext, Request, Response
from .producer import (
    LocalProducerRepository,
    RabbitMQProducerRepository,
    WebEditorControlProducerRepository,
)


class TestLocalProducerRepository(unittest.TestCase):
    def test_enqueue(self):
        queue = MagicMock()
        repo = LocalProducerRepository(queue)

        req = Request(query_params={}, headers={}, method="GET", body="")
        res = Response(headers={}, status=200, body="")
        context = HookContext(request=req, response=res)

        # Enqueue returns a connection (Pipe)
        conn = repo.enqueue("stage1", context)

        # Check queue has message
        queue.put.assert_called_once()
        msg = queue.put.call_args[0][0]
        self.assertEqual(msg.preexecution.stage_id, "stage1")
        self.assertIsNotNone(msg.connection)

        conn.close()


class TestRabbitMQProducerRepository(unittest.TestCase):
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    def test_enqueue_publishes_and_returns_connection(
        self, MockRabbitConn, MockBlockingConnection
    ):
        # Setup mocks
        mock_pika_conn = MagicMock()
        # Ensure context manager returns the mock itself
        mock_pika_conn.__enter__.return_value = mock_pika_conn
        MockBlockingConnection.return_value = mock_pika_conn

        mock_channel = MagicMock()
        # Ensure context manager for channel also works
        mock_channel.__enter__.return_value = mock_channel
        mock_pika_conn.channel.return_value = mock_channel

        mock_rabbit_conn = MagicMock()
        MockRabbitConn.return_value = mock_rabbit_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        req = Request(query_params={}, headers={}, method="GET", body="")
        res = Response(headers={}, status=200, body="")
        context = HookContext(request=req, response=res)

        # Execute
        conn = repo.enqueue("stage1", context)

        # Verify connection and channel creation
        MockBlockingConnection.assert_called()
        mock_pika_conn.channel.assert_called()
        mock_channel.queue_declare.assert_called_with(queue="test_queue", durable=True)

        # Verify publish
        mock_channel.basic_publish.assert_called_once()
        _, kwargs = mock_channel.basic_publish.call_args
        self.assertEqual(kwargs["routing_key"], "test_queue")
        # Body is json string, Serializable converts to camelCase
        self.assertIn(
            '"stageId": "stage1"',
            kwargs["body"].decode()
            if isinstance(kwargs["body"], bytes)
            else kwargs["body"],
        )

        # Verify RabbitMQConnection creation
        MockRabbitConn.assert_called_once()
        _, kwargs = MockRabbitConn.call_args
        self.assertEqual(kwargs["connection_uri"], "amqp://uri")
        self.assertTrue(kwargs["send_queue"].startswith("server_to_worker_"))
        self.assertTrue(kwargs["recv_queue"].startswith("worker_to_server_"))

        # Returns the connection object
        self.assertEqual(conn, mock_rabbit_conn)

    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("time.sleep")
    def test_connect_retry_logic(
        self, mock_sleep, MockRabbitConn, MockBlockingConnection
    ):
        from pika.exceptions import AMQPConnectionError

        # Fail twice, then succeed
        mock_success_conn = MagicMock()
        MockBlockingConnection.side_effect = [
            AMQPConnectionError("Fail 1"),
            AMQPConnectionError("Fail 2"),
            mock_success_conn,
        ]

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        req = Request(query_params={}, headers={}, method="GET", body="")
        res = Response(headers={}, status=200, body="")
        context = HookContext(request=req, response=res)

        repo.enqueue("stage1", context)

        self.assertEqual(MockBlockingConnection.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    def test_web_editor_control_stop_execution(self, MockBlockingConnection):
        mock_pika_conn = MagicMock()
        mock_pika_conn.__enter__.return_value = mock_pika_conn
        MockBlockingConnection.return_value = mock_pika_conn

        mock_channel = MagicMock()
        mock_channel.__enter__.return_value = mock_channel
        mock_pika_conn.channel.return_value = mock_channel

        repo = WebEditorControlProducerRepository("amqp://uri")

        repo.stop_execution("exec-123")

        # Verify exchange is declared as fanout (not queue)
        mock_channel.exchange_declare.assert_called_once_with(
            exchange="web_editor_control",
            exchange_type="fanout",
            durable=True,
        )

        # Verify publish to exchange with empty routing key
        mock_channel.basic_publish.assert_called_once()
        _, kwargs = mock_channel.basic_publish.call_args

        self.assertEqual(kwargs["routing_key"], "")  # Empty for fanout
        self.assertEqual(kwargs["exchange"], "web_editor_control")
        import json

        body_json = json.loads(
            kwargs["body"].decode()
            if isinstance(kwargs["body"], bytes)
            else kwargs["body"]
        )
        self.assertEqual(body_json["type"], "stop")
        self.assertEqual(body_json["payload"], {"executionId": "exec-123"})


class TestRabbitMQFireAndForgetPublishOnly(unittest.TestCase):
    """In DB mode (and file mode without the flag), enqueue_fire_and_forget
    must only publish to the main queue: no RabbitMQConnection (2 TCP +
    heartbeat thread), no NATSConnection (asyncio loop thread), no daemon
    thread."""

    def _make_repo(self):
        repo = RabbitMQProducerRepository.__new__(RabbitMQProducerRepository)
        repo.connection_uri = "amqp://test"
        repo.queue_name = "test_queue"
        return repo

    def _ctx(self):
        return HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )

    # NOTE: patching WORKER_LOG_TO_QUEUE with a literal (new=True) does NOT
    # inject a mock arg; only web_editor_uses_db / the three class patches do.
    # So the method takes 4 injected args, not 5.
    @patch(
        "abstra_internals.repositories.producer.web_editor_uses_db", return_value=True
    )
    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", True)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.NATSConnection")
    @patch("abstra_internals.repositories.producer.threading.Thread")
    def test_db_mode_is_publish_only(self, mock_Thread, mock_NATS, mock_Rabbit, _db):
        repo = self._make_repo()
        fake_channel = MagicMock()
        fake_conn = MagicMock()
        fake_conn.__enter__.return_value = fake_conn
        fake_conn.channel.return_value.__enter__.return_value = fake_channel
        repo._connect_with_retry = MagicMock(return_value=fake_conn)

        repo.enqueue_fire_and_forget("stage-1", self._ctx())

        fake_channel.queue_declare.assert_called_once()
        fake_channel.basic_publish.assert_called_once()
        kwargs = fake_channel.basic_publish.call_args.kwargs
        self.assertEqual(kwargs["routing_key"], "test_queue")
        self.assertIn("stage-1", kwargs["body"])
        mock_Rabbit.assert_not_called()
        mock_NATS.assert_not_called()
        mock_Thread.assert_not_called()

    @patch(
        "abstra_internals.repositories.producer.web_editor_uses_db", return_value=False
    )
    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", False)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.NATSConnection")
    @patch("abstra_internals.repositories.producer.threading.Thread")
    def test_flag_off_is_publish_only(self, mock_Thread, mock_NATS, mock_Rabbit, _db):
        repo = self._make_repo()
        fake_channel = MagicMock()
        fake_conn = MagicMock()
        fake_conn.__enter__.return_value = fake_conn
        fake_conn.channel.return_value.__enter__.return_value = fake_channel
        repo._connect_with_retry = MagicMock(return_value=fake_conn)

        repo.enqueue_fire_and_forget("stage-2", self._ctx())

        fake_channel.basic_publish.assert_called_once()
        mock_Rabbit.assert_not_called()
        mock_NATS.assert_not_called()
        mock_Thread.assert_not_called()


if __name__ == "__main__":
    unittest.main()
