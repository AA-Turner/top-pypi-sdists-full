"""Tests for the csrd.message.rabbit adapter package."""

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError

pytest.importorskip("aio_pika", reason="aio-pika not installed (optional rabbit extra)")

from csrd.message import Message
from csrd.message.rabbit import (
    AMQPState,
    QueueConfig,
    RabbitConsumer,
    RabbitMessageHandler,
    RabbitPublisher,
)

# ---------------------------------------------------------------------------
# QueueConfig
# ---------------------------------------------------------------------------


class TestQueueConfig:
    def test_minimal(self):
        cfg = QueueConfig(exchange_name="ex", queue_name="q", routing_key="rk")
        assert cfg.exchange_name == "ex"
        assert cfg.queue_name == "q"
        assert cfg.routing_key == "rk"
        assert cfg.queue_type == "quorum"

    def test_custom_queue_type(self):
        cfg = QueueConfig(
            exchange_name="ex",
            queue_name="q",
            routing_key="rk",
            queue_type="classic",
        )
        assert cfg.queue_type == "classic"

    def test_retry_interval_minimum(self):
        with pytest.raises(ValidationError):
            QueueConfig(
                exchange_name="ex",
                queue_name="q",
                routing_key="rk",
                retry_interval=500,
            )

    def test_requires_all_fields(self):
        with pytest.raises((ValidationError, TypeError)):
            QueueConfig(exchange_name="ex")


# ---------------------------------------------------------------------------
# RabbitMessageHandler
# ---------------------------------------------------------------------------


class _TestHandler(RabbitMessageHandler[dict[str, Any]]):
    """Concrete handler for testing."""

    received: list[Any]

    def __init__(self):
        super().__init__(message_type=dict)
        self.received = []

    async def handle_message(self, message, headers):
        self.received.append(message)


class TestRabbitMessageHandler:
    @pytest.mark.asyncio
    async def test_receive_message_deserializes(self):
        handler = _TestHandler()
        msg = MagicMock()
        msg.body = json.dumps({"key": "value"}).encode()
        msg.headers = {}

        await handler.receive_message(msg)
        assert len(handler.received) == 1
        assert handler.received[0]["key"] == "value"


# ---------------------------------------------------------------------------
# RabbitConsumer
# ---------------------------------------------------------------------------


class TestRabbitConsumer:
    def _make_message(
        self, body: bytes = b'{"ok": true}', headers: dict | None = None
    ) -> MagicMock:
        msg = AsyncMock()
        msg.body = body
        msg.headers = headers or {}
        msg.message_id = "test-msg-1"
        msg.process = MagicMock(return_value=AsyncMock())
        # Make process() work as async context manager
        ctx = AsyncMock()
        ctx.__aenter__ = AsyncMock(return_value=None)
        ctx.__aexit__ = AsyncMock(return_value=False)
        msg.process.return_value = ctx
        return msg

    @pytest.mark.asyncio
    async def test_poison_message_detection(self):
        assert RabbitConsumer._is_poison(None) is False
        assert RabbitConsumer._is_poison({}) is False
        assert RabbitConsumer._is_poison({"x-death": [{"reason": "rejected", "count": 5}]}) is True
        assert RabbitConsumer._is_poison({"x-death": [{"reason": "rejected", "count": 3}]}) is False


# ---------------------------------------------------------------------------
# RabbitPublisher
# ---------------------------------------------------------------------------


class TestRabbitPublisher:
    @pytest.mark.asyncio
    async def test_publish_sends_message(self):
        exchange = AsyncMock()
        exchange.name = "test-exchange"

        publisher = RabbitPublisher(exchange, default_routing_key="default")

        msg = Message(
            topic="orders.created",
            payload={"id": "o-1"},
            key="orders",
            headers={"trace": "abc"},
            message_id="msg-123",
        )

        await publisher.publish(msg)

        exchange.publish.assert_called_once()
        call_args = exchange.publish.call_args
        amqp_msg = call_args[0][0]  # first positional arg
        assert json.loads(amqp_msg.body) == {"id": "o-1"}
        assert call_args[1]["routing_key"] == "orders"

    @pytest.mark.asyncio
    async def test_publish_uses_default_routing_key(self):
        exchange = AsyncMock()
        exchange.name = "test-exchange"

        publisher = RabbitPublisher(exchange, default_routing_key="fallback")

        msg = Message(topic="events", payload={"x": 1})

        await publisher.publish(msg)

        call_args = exchange.publish.call_args
        assert call_args[1]["routing_key"] == "fallback"


# ---------------------------------------------------------------------------
# AMQPState
# ---------------------------------------------------------------------------


class TestAMQPState:
    def test_construction(self):
        from aio_pika.abc import AbstractChannel, AbstractConnection

        state = AMQPState(
            connection=MagicMock(spec=AbstractConnection),
            channel=MagicMock(spec=AbstractChannel),
        )
        assert state.exchanges == {}
        assert state.queues == {}


# ---------------------------------------------------------------------------
# RabbitLifespan
# ---------------------------------------------------------------------------


class TestRabbitLifespan:
    def test_requires_connection_url(self):
        from csrd.message.rabbit import RabbitLifespan

        with pytest.raises(ValueError, match="connection_url"):
            RabbitLifespan("")

    def test_construction(self):
        from csrd.message.rabbit import RabbitLifespan

        lifespan = RabbitLifespan("amqp://guest:guest@localhost:5672/")
        assert lifespan._connection_url == "amqp://guest:guest@localhost:5672/"
        assert lifespan._queues == []
        assert lifespan._prefetch_count == 100

    def test_consumer_tag_format(self):
        from csrd.message.rabbit._lifespan import RabbitLifespan

        queue = MagicMock()
        queue.name = "test-queue"
        tag = RabbitLifespan._consumer_tag(queue)
        assert tag.startswith("csrd-test-queue-")
        assert len(tag) > len("csrd-test-queue-")
