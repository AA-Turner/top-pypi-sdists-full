import json
import time
import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.repositories.producer import RabbitMQProducerRepository


def _make_mock_conn(messages):
    """Create a mock connection that returns messages sequentially from poll/recv."""
    mock_conn = MagicMock()
    remaining = list(messages)

    def poll_side_effect(timeout=0.0):
        if not remaining:
            return False
        return True

    def recv_side_effect(*args, **kwargs):
        if not remaining:
            raise EOFError("No more messages")
        return remaining.pop(0)

    mock_conn.poll.side_effect = poll_side_effect
    mock_conn.recv.side_effect = recv_side_effect
    type(mock_conn).closed = property(lambda self: False)
    return mock_conn


class TestFireAndForgetBroadcast(unittest.TestCase):
    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", False)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    def test_fire_and_forget_without_flag_closes_after_first_msg(
        self, MockBlockingConn, MockRabbitConn
    ):
        mock_pika = MagicMock()
        mock_pika.__enter__ = MagicMock(return_value=mock_pika)
        mock_pika.__exit__ = MagicMock(return_value=False)
        MockBlockingConn.return_value = mock_pika
        mock_pika.channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_pika.channel.return_value.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.poll.return_value = True
        mock_conn.recv.return_value = json.dumps({"type": "execution:started"})
        MockRabbitConn.return_value = mock_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        from abstra_internals.entities.execution_context import (
            HookContext,
            Request,
            Response,
        )

        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        repo.enqueue_fire_and_forget("stage1", ctx)

        # Wait for daemon thread to finish
        time.sleep(0.5)

        # With flag off, should close after first recv (old behavior)
        mock_conn.close.assert_called()
        # recv called exactly once
        mock_conn.recv.assert_called_once()

    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", True)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_fire_and_forget_with_flag_does_not_broadcast_stdio(
        self, MockBroadcast, MockBlockingConn, MockRabbitConn
    ):
        """consume_and_forward should NOT broadcast stdio (fanout consumer handles it)."""
        mock_pika = MagicMock()
        mock_pika.__enter__ = MagicMock(return_value=mock_pika)
        mock_pika.__exit__ = MagicMock(return_value=False)
        MockBlockingConn.return_value = mock_pika
        mock_pika.channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_pika.channel.return_value.__exit__ = MagicMock(return_value=False)

        # Messages: stdio dict, then execution:ended string
        stdio_msg = {"type": "stdio", "payload": {"type": "stdout", "log": "hello"}}
        ended_msg = json.dumps(
            {
                "type": "execution:ended",
                "exitStatus": "SUCCESS",
                "execution_id": "exec1",
            }
        )
        mock_conn = _make_mock_conn([stdio_msg, ended_msg])
        MockRabbitConn.return_value = mock_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        from abstra_internals.entities.execution_context import (
            HookContext,
            Request,
            Response,
        )

        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        repo.enqueue_fire_and_forget("stage1", ctx)
        time.sleep(0.5)

        # stdio should NOT be broadcast from consume_and_forward (fanout handles it)
        # Only execution:update from execution:ended should be broadcast
        self.assertEqual(MockBroadcast.broadcast.call_count, 1)
        broadcast_msg = json.loads(MockBroadcast.broadcast.call_args[1]["msg"])
        self.assertEqual(broadcast_msg["type"], "execution:update")

    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", True)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_fire_and_forget_skips_task_in_consume_and_forward(
        self, MockBroadcast, MockBlockingConn, MockRabbitConn
    ):
        """consume_and_forward should NOT broadcast task (fanout consumer handles it)."""
        mock_pika = MagicMock()
        mock_pika.__enter__ = MagicMock(return_value=mock_pika)
        mock_pika.__exit__ = MagicMock(return_value=False)
        MockBlockingConn.return_value = mock_pika
        mock_pika.channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_pika.channel.return_value.__exit__ = MagicMock(return_value=False)

        task_msg = {"type": "task", "payload": {"id": "t1", "status": "pending"}}
        ended_msg = json.dumps(
            {
                "type": "execution:ended",
                "exitStatus": "SUCCESS",
                "execution_id": "exec1",
            }
        )
        mock_conn = _make_mock_conn([task_msg, ended_msg])
        MockRabbitConn.return_value = mock_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        from abstra_internals.entities.execution_context import (
            HookContext,
            Request,
            Response,
        )

        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        repo.enqueue_fire_and_forget("stage1", ctx)
        time.sleep(0.5)

        # Only execution:update from execution:ended should be broadcast, not the task
        self.assertEqual(MockBroadcast.broadcast.call_count, 1)
        broadcast_msg = json.loads(MockBroadcast.broadcast.call_args[1]["msg"])
        self.assertEqual(broadcast_msg["type"], "execution:update")

    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", True)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_fire_and_forget_stops_on_execution_ended(
        self, MockBroadcast, MockBlockingConn, MockRabbitConn
    ):
        mock_pika = MagicMock()
        mock_pika.__enter__ = MagicMock(return_value=mock_pika)
        mock_pika.__exit__ = MagicMock(return_value=False)
        MockBlockingConn.return_value = mock_pika
        mock_pika.channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_pika.channel.return_value.__exit__ = MagicMock(return_value=False)

        ended_msg = json.dumps(
            {
                "type": "execution:ended",
                "exitStatus": "SUCCESS",
                "execution_id": "exec1",
            }
        )
        mock_conn = _make_mock_conn([ended_msg])
        MockRabbitConn.return_value = mock_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        from abstra_internals.entities.execution_context import (
            HookContext,
            Request,
            Response,
        )

        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        repo.enqueue_fire_and_forget("stage1", ctx)
        time.sleep(0.5)

        mock_conn.close.assert_called()
        # Only execution:update broadcast from execution:ended
        self.assertEqual(MockBroadcast.broadcast.call_count, 1)
        broadcast_msg = json.loads(MockBroadcast.broadcast.call_args[1]["msg"])
        self.assertEqual(broadcast_msg["type"], "execution:update")

    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", True)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.BroadcastController",
    )
    def test_fire_and_forget_does_not_broadcast_stdio_batch(
        self, MockBroadcast, MockBlockingConn, MockRabbitConn
    ):
        """consume_and_forward should NOT broadcast stdio_batch (fanout consumer handles it)."""
        mock_pika = MagicMock()
        mock_pika.__enter__ = MagicMock(return_value=mock_pika)
        mock_pika.__exit__ = MagicMock(return_value=False)
        MockBlockingConn.return_value = mock_pika
        mock_pika.channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_pika.channel.return_value.__exit__ = MagicMock(return_value=False)

        batch_msg = {
            "type": "stdio_batch",
            "payload": [
                {
                    "type": "stdout",
                    "log": "line1",
                    "execution_id": "e1",
                    "stage_id": "s1",
                },
                {
                    "type": "stderr",
                    "log": "line2",
                    "execution_id": "e1",
                    "stage_id": "s1",
                },
            ],
        }
        ended_msg = json.dumps(
            {
                "type": "execution:ended",
                "exitStatus": "SUCCESS",
                "execution_id": "exec1",
            }
        )
        mock_conn = _make_mock_conn([batch_msg, ended_msg])
        MockRabbitConn.return_value = mock_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        from abstra_internals.entities.execution_context import (
            HookContext,
            Request,
            Response,
        )

        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        repo.enqueue_fire_and_forget("stage1", ctx)
        time.sleep(0.5)

        # stdio_batch should NOT be broadcast (fanout handles it)
        # Only execution:update from execution:ended should be broadcast
        self.assertEqual(MockBroadcast.broadcast.call_count, 1)
        broadcast_msg = json.loads(MockBroadcast.broadcast.call_args[1]["msg"])
        self.assertEqual(broadcast_msg["type"], "execution:update")

    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", True)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    def test_fire_and_forget_handles_conn_error(self, MockBlockingConn, MockRabbitConn):
        mock_pika = MagicMock()
        mock_pika.__enter__ = MagicMock(return_value=mock_pika)
        mock_pika.__exit__ = MagicMock(return_value=False)
        MockBlockingConn.return_value = mock_pika
        mock_pika.channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_pika.channel.return_value.__exit__ = MagicMock(return_value=False)

        mock_conn = MagicMock()
        mock_conn.poll.side_effect = Exception("Connection lost")
        type(mock_conn).closed = property(lambda self: False)
        MockRabbitConn.return_value = mock_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        from abstra_internals.entities.execution_context import (
            HookContext,
            Request,
            Response,
        )

        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        # Should not raise
        repo.enqueue_fire_and_forget("stage1", ctx)
        time.sleep(0.5)

        # Connection should be closed in finally
        mock_conn.close.assert_called()

    @patch("abstra_internals.repositories.producer.CONSUMER_INACTIVITY_TIMEOUT", 0.3)
    @patch("abstra_internals.repositories.producer.WORKER_LOG_TO_QUEUE", True)
    @patch("abstra_internals.repositories.producer.RabbitMQConnection")
    @patch("abstra_internals.repositories.producer.pika.BlockingConnection")
    def test_consume_and_forward_disconnects_on_inactivity(
        self, MockBlockingConn, MockRabbitConn
    ):
        mock_pika = MagicMock()
        mock_pika.__enter__ = MagicMock(return_value=mock_pika)
        mock_pika.__exit__ = MagicMock(return_value=False)
        MockBlockingConn.return_value = mock_pika
        mock_pika.channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_pika.channel.return_value.__exit__ = MagicMock(return_value=False)

        # Connection that never has data (poll always returns False)
        mock_conn = MagicMock()
        mock_conn.poll.return_value = False
        type(mock_conn).closed = property(lambda self: False)
        MockRabbitConn.return_value = mock_conn

        repo = RabbitMQProducerRepository("amqp://uri", "test_queue")

        from abstra_internals.entities.execution_context import (
            HookContext,
            Request,
            Response,
        )

        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )

        repo.enqueue_fire_and_forget("stage1", ctx)
        # With CONSUMER_INACTIVITY_TIMEOUT=0.3s, should disconnect within ~2s
        time.sleep(2.0)

        mock_conn.close.assert_called()


if __name__ == "__main__":
    unittest.main()
