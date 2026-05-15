#!/usr/bin/env python3
"""
Comprehensive usage examples for the MatriceStream unified streaming interface.

This is an example script (not library API). Run directly; LOG_LEVEL controls
verbosity. Demonstrates MatriceStream for Kafka and Redis with sync/async operations.
"""
import asyncio
import logging
import os
from matrice_common.logging_config import configure_logging
from matrice_common.stream import MatriceStream, StreamType

configure_logging()
logger = logging.getLogger(__name__)


def kafka_sync_example():
    """Example of synchronous Kafka streaming operations."""
    logger.info("=== Kafka Synchronous Operations ===")

    # Initialize Kafka stream with connection configuration
    kafka_stream = MatriceStream(
        StreamType.KAFKA,
        bootstrap_servers="localhost:9092",
        sasl_mechanism="SCRAM-SHA-256",
        sasl_username=os.environ.get("KAFKA_SASL_USERNAME", ""),
        sasl_password=os.environ.get("KAFKA_SASL_PASSWORD", ""),
        security_protocol="SASL_PLAINTEXT"
    )

    try:
        # Setup the stream for a specific topic with consumer group
        topic_name = "my-kafka-topic"
        consumer_group = "my-consumer-group"
        kafka_stream.setup(topic_name, consumer_group_id=consumer_group)

        logger.info("Stream setup complete: %s", kafka_stream.is_setup())
        logger.info("Configured topics: %s", kafka_stream.get_topics_or_channels())
        logger.info("Consumer group: %s", kafka_stream.get_consumer_group_id())

        # Produce messages
        for i in range(5):
            message = {
                "id": i,
                "message": f"Hello Kafka message {i}",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            kafka_stream.add_message(topic_name, message, key=f"key-{i}")
            logger.info("Produced message %s", i)

        # Consume messages
        for i in range(5):
            msg = kafka_stream.get_message(timeout=10.0)
            if msg:
                logger.info("Consumed: %s", msg.get("value"))
            else:
                logger.info("No message received")

    except Exception as e:
        logger.warning("Error in Kafka sync example: %s", e)
    finally:
        kafka_stream.close()
        logger.info("Kafka stream closed")


async def kafka_async_example():
    """Example of asynchronous Kafka streaming operations."""
    logger.info("\n=== Kafka Asynchronous Operations ===")

    # Initialize Kafka stream with connection configuration
    kafka_stream = MatriceStream(
        StreamType.KAFKA,
        bootstrap_servers="localhost:9092",
        sasl_mechanism="SCRAM-SHA-256",
        sasl_username=os.environ.get("KAFKA_SASL_USERNAME", ""),
        sasl_password=os.environ.get("KAFKA_SASL_PASSWORD", ""),
        security_protocol="SASL_PLAINTEXT"
    )

    try:
        # Setup the async stream
        topic_name = "my-async-kafka-topic"
        consumer_group = "my-async-consumer-group"
        await kafka_stream.async_setup(topic_name, consumer_group_id=consumer_group)

        logger.info("Async stream setup complete: %s", kafka_stream.is_async_setup())

        # Async context manager example
        async with kafka_stream:
            # Produce messages asynchronously
            for i in range(3):
                message = {
                    "id": i,
                    "message": f"Async Kafka message {i}",
                    "timestamp": "2024-01-01T12:00:00Z"
                }
                await kafka_stream.async_add_message(topic_name, message, key=f"async-key-{i}")
                logger.info("Async produced message %s", i)

            # Consume messages asynchronously
            for i in range(3):
                msg = await kafka_stream.async_get_message(timeout=10.0)
                if msg:
                    logger.info("Async consumed: %s", msg.get("value"))
                else:
                    logger.info("No async message received")

    except Exception as e:
        logger.warning("Error in Kafka async example: %s", e)


def redis_sync_example():
    """Example of synchronous Redis streaming operations."""
    logger.info("\n=== Redis Synchronous Operations ===")

    # Initialize Redis stream with connection configuration
    redis_stream = MatriceStream(
        StreamType.REDIS,
        host="localhost",
        port=6379,
        password="redis_password",  # nosec B106
        db=0
    )

    try:
        # Setup the stream for a specific Redis stream
        stream_name = "my-redis-stream"
        consumer_group = "my-consumer-group"
        redis_stream.setup(stream_name, consumer_group_id=consumer_group)

        logger.info("Redis stream setup complete: %s", redis_stream.is_setup())
        logger.info("Configured streams: %s", redis_stream.get_topics_or_channels())
        logger.info("Consumer group: %s", redis_stream.get_consumer_group_id())

        # Add messages to stream
        for i in range(3):
            message = {
                "id": i,
                "message": f"Hello Redis stream message {i}",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            message_id = redis_stream.add_message(stream_name, message, key=f"msg-{i}")
            logger.info("Added message %s with ID: %s", i, message_id)

        # Get messages from stream
        for i in range(3):
            msg = redis_stream.get_message(timeout=5.0)
            if msg:
                logger.info("Received from stream '%s': %s", msg.get("stream"), msg.get("data"))
                logger.info("Message ID: %s", msg.get("message_id"))
            else:
                logger.info("No Redis stream message received")

    except Exception as e:
        logger.warning("Error in Redis sync example: %s", e)
    finally:
        redis_stream.close()
        logger.info("Redis stream closed")


async def redis_async_example():
    """Example of asynchronous Redis streaming operations."""
    logger.info("\n=== Redis Asynchronous Operations ===")

    # Initialize Redis stream
    redis_stream = MatriceStream(
        StreamType.REDIS,
        host="localhost",
        port=6379,
        password="redis_password",  # nosec B106
        db=0
    )

    try:
        # Setup the async stream
        stream_name = "my-async-redis-stream"
        consumer_group = "my-async-consumer-group"
        await redis_stream.async_setup(stream_name, consumer_group_id=consumer_group)

        logger.info("Redis async stream setup complete: %s", redis_stream.is_async_setup())

        # Add messages to stream asynchronously
        for i in range(3):
            message = {
                "id": i,
                "message": f"Async Redis stream message {i}",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            message_id = await redis_stream.async_add_message(stream_name, message, key=f"async-msg-{i}")
            logger.info("Async added message %s with ID: %s", i, message_id)

        # Get messages from stream asynchronously
        for i in range(3):
            msg = await redis_stream.async_get_message(timeout=5.0)
            if msg:
                logger.info("Async received from stream '%s': %s", msg.get("stream"), msg.get("data"))
                logger.info("Message ID: %s", msg.get("message_id"))
            else:
                    logger.info("No async Redis stream message received")

    except Exception as e:
        logger.warning("Error in Redis async example: %s", e)
    finally:
        await redis_stream.async_close()
        logger.info("Redis async stream closed")


def metrics_example():
    """Example of configuring metrics reporting."""
    logger.info("\n=== Metrics Configuration Example ===")

    # This would typically use a real RPC client from a session
    # For demo purposes, we'll show the API

    kafka_stream = MatriceStream(
        StreamType.KAFKA,
        bootstrap_servers="localhost:9092",
        sasl_username="user",
        sasl_password="pass",  # nosec B106
    )

    try:
        # Configure metrics reporting (would need real RPC client)
        # kafka_stream.configure_metrics_reporting(
        #     rpc_client=session.rpc,
        #     deployment_id="my-deployment-123",
        #     interval=120,
        #     batch_size=1000
        # )

        # Get current metrics
        metrics = kafka_stream.get_metrics()
        logger.info("Current metrics: %s", metrics)

        logger.info("Metrics configuration completed (demo)")

    except Exception as e:
        logger.warning("Error in metrics example: %s", e)
    finally:
        kafka_stream.close()


def context_manager_example():
    """Example using context managers for automatic cleanup."""
    logger.info("\n=== Context Manager Example ===")

    # Synchronous context manager
    with MatriceStream(StreamType.KAFKA, bootstrap_servers="localhost:9092") as stream:
        stream.setup("test-topic", consumer_group_id="test-group")
        # Stream operations here
        logger.info("Working with stream in sync context manager")

    logger.info("Stream automatically closed by context manager")


async def async_context_manager_example():
    """Example using async context managers."""
    logger.info("\n=== Async Context Manager Example ===")

    # Asynchronous context manager
    async with MatriceStream(StreamType.REDIS, host="localhost") as stream:
        await stream.async_setup("test-channel")
        # Async stream operations here
        logger.info("Working with stream in async context manager")

    logger.info("Async stream automatically closed by context manager")


def multi_stream_example():
    """Example of working with multiple streams simultaneously."""
    logger.info("\n=== Multi-Stream Example ===")

    # Create both Kafka and Redis streams
    kafka_stream = MatriceStream(
        StreamType.KAFKA,
        bootstrap_servers="localhost:9092"
    )

    redis_stream = MatriceStream(
        StreamType.REDIS,
        host="localhost",
        port=6379
    )

    try:
        # Setup both streams
        kafka_stream.setup("multi-kafka-topic", "multi-group")
        redis_stream.setup("multi-redis-stream", "multi-redis-group")

        # Cross-platform message relay example
        message = {"data": "Cross-platform message", "source": "kafka"}

        # Send to Kafka
        kafka_stream.add_message("multi-kafka-topic", message)
        logger.info("Message sent to Kafka")

        # Relay to Redis stream
        message_id = redis_stream.add_message("multi-redis-stream", message, key="relay")
        logger.info("Message relayed to Redis stream with ID: %s", message_id)

        logger.info("Kafka stream type: %s", kafka_stream.get_stream_type())
        logger.info("Redis stream type: %s", redis_stream.get_stream_type())

    except Exception as e:
        logger.warning("Error in multi-stream example: %s", e)
    finally:
        kafka_stream.close()
        redis_stream.close()
        logger.info("All streams closed")


async def main():
    """Main function running all examples."""
    logger.info("MatriceStream Usage Examples")
    logger.info("============================")

    # Note: These examples assume Kafka and Redis servers are running
    # In a real environment, you would have actual connection details

    try:
        # Synchronous examples
        kafka_sync_example()
        redis_sync_example()

        # Asynchronous examples
        await kafka_async_example()
        await redis_async_example()

        # Other examples
        metrics_example()
        context_manager_example()
        await async_context_manager_example()
        multi_stream_example()

    except Exception as e:
        logger.warning("Error running examples: %s", e)
        logger.warning("Note: Make sure Kafka and Redis servers are running and accessible")


if __name__ == "__main__":
    asyncio.run(main())
