#!/usr/bin/env python3
"""
Comprehensive usage examples for the MatriceStream unified streaming interface.

This example demonstrates how to use MatriceStream for both Kafka and Redis
with synchronous and asynchronous operations.
"""

import asyncio
import logging
import os
from matrice_common.stream import MatriceStream, StreamType

# Configure logging
logging.basicConfig(level=logging.INFO)


def kafka_sync_example():
    """Example of synchronous Kafka streaming operations."""
    print("=== Kafka Synchronous Operations ===")
    
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
        
        print(f"Stream setup complete: {kafka_stream.is_setup()}")
        print(f"Configured topics: {kafka_stream.get_topics_or_channels()}")
        print(f"Consumer group: {kafka_stream.get_consumer_group_id()}")
        
        # Produce messages
        for i in range(5):
            message = {
                "id": i,
                "message": f"Hello Kafka message {i}",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            kafka_stream.add_message(topic_name, message, key=f"key-{i}")
            print(f"Produced message {i}")
        
        # Consume messages
        for i in range(5):
            msg = kafka_stream.get_message(timeout=10.0)
            if msg:
                print(f"Consumed: {msg.get('value')}")
            else:
                print("No message received")
                
    except Exception as e:
        print(f"Error in Kafka sync example: {e}")
    finally:
        kafka_stream.close()
        print("Kafka stream closed")


async def kafka_async_example():
    """Example of asynchronous Kafka streaming operations."""
    print("\n=== Kafka Asynchronous Operations ===")
    
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
        
        print(f"Async stream setup complete: {kafka_stream.is_async_setup()}")
        
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
                print(f"Async produced message {i}")
            
            # Consume messages asynchronously
            for i in range(3):
                msg = await kafka_stream.async_get_message(timeout=10.0)
                if msg:
                    print(f"Async consumed: {msg.get('value')}")
                else:
                    print("No async message received")
                    
    except Exception as e:
        print(f"Error in Kafka async example: {e}")


def redis_sync_example():
    """Example of synchronous Redis streaming operations."""
    print("\n=== Redis Synchronous Operations ===")
    
    # Initialize Redis stream with connection configuration
    redis_stream = MatriceStream(
        StreamType.REDIS,
        host="localhost",
        port=6379,
        password="redis_password",
        db=0
    )
    
    try:
        # Setup the stream for a specific Redis stream
        stream_name = "my-redis-stream"
        consumer_group = "my-consumer-group"
        redis_stream.setup(stream_name, consumer_group_id=consumer_group)
        
        print(f"Redis stream setup complete: {redis_stream.is_setup()}")
        print(f"Configured streams: {redis_stream.get_topics_or_channels()}")
        print(f"Consumer group: {redis_stream.get_consumer_group_id()}")
        
        # Add messages to stream
        for i in range(3):
            message = {
                "id": i,
                "message": f"Hello Redis stream message {i}",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            message_id = redis_stream.add_message(stream_name, message, key=f"msg-{i}")
            print(f"Added message {i} with ID: {message_id}")
        
        # Get messages from stream
        for i in range(3):
            msg = redis_stream.get_message(timeout=5.0)
            if msg:
                print(f"Received from stream '{msg.get('stream')}': {msg.get('data')}")
                print(f"Message ID: {msg.get('message_id')}")
            else:
                print("No Redis stream message received")
                
    except Exception as e:
        print(f"Error in Redis sync example: {e}")
    finally:
        redis_stream.close()
        print("Redis stream closed")


async def redis_async_example():
    """Example of asynchronous Redis streaming operations."""
    print("\n=== Redis Asynchronous Operations ===")
    
    # Initialize Redis stream
    redis_stream = MatriceStream(
        StreamType.REDIS,
        host="localhost",
        port=6379,
        password="redis_password",
        db=0
    )
    
    try:
        # Setup the async stream
        stream_name = "my-async-redis-stream"
        consumer_group = "my-async-consumer-group"
        await redis_stream.async_setup(stream_name, consumer_group_id=consumer_group)
        
        print(f"Redis async stream setup complete: {redis_stream.is_async_setup()}")
        
        # Add messages to stream asynchronously
        for i in range(3):
            message = {
                "id": i,
                "message": f"Async Redis stream message {i}",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            message_id = await redis_stream.async_add_message(stream_name, message, key=f"async-msg-{i}")
            print(f"Async added message {i} with ID: {message_id}")
        
        # Get messages from stream asynchronously
        for i in range(3):
            msg = await redis_stream.async_get_message(timeout=5.0)
            if msg:
                print(f"Async received from stream '{msg.get('stream')}': {msg.get('data')}")
                print(f"Message ID: {msg.get('message_id')}")
            else:
                print("No async Redis stream message received")
                
    except Exception as e:
        print(f"Error in Redis async example: {e}")
    finally:
        await redis_stream.async_close()
        print("Redis async stream closed")


def metrics_example():
    """Example of configuring metrics reporting."""
    print("\n=== Metrics Configuration Example ===")
    
    # This would typically use a real RPC client from a session
    # For demo purposes, we'll show the API
    
    kafka_stream = MatriceStream(
        StreamType.KAFKA,
        bootstrap_servers="localhost:9092",
        sasl_username="user",
        sasl_password="pass"
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
        print(f"Current metrics: {metrics}")
        
        print("Metrics configuration completed (demo)")
        
    except Exception as e:
        print(f"Error in metrics example: {e}")
    finally:
        kafka_stream.close()


def context_manager_example():
    """Example using context managers for automatic cleanup."""
    print("\n=== Context Manager Example ===")
    
    # Synchronous context manager
    with MatriceStream(StreamType.KAFKA, bootstrap_servers="localhost:9092") as stream:
        stream.setup("test-topic", consumer_group_id="test-group")
        # Stream operations here
        print("Working with stream in sync context manager")
        
    print("Stream automatically closed by context manager")


async def async_context_manager_example():
    """Example using async context managers."""
    print("\n=== Async Context Manager Example ===")
    
    # Asynchronous context manager
    async with MatriceStream(StreamType.REDIS, host="localhost") as stream:
        await stream.async_setup("test-channel")
        # Async stream operations here
        print("Working with stream in async context manager")
        
    print("Async stream automatically closed by context manager")


def multi_stream_example():
    """Example of working with multiple streams simultaneously."""
    print("\n=== Multi-Stream Example ===")
    
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
        print("Message sent to Kafka")
        
        # Relay to Redis stream
        message_id = redis_stream.add_message("multi-redis-stream", message, key="relay")
        print(f"Message relayed to Redis stream with ID: {message_id}")
        
        print(f"Kafka stream type: {kafka_stream.get_stream_type()}")
        print(f"Redis stream type: {redis_stream.get_stream_type()}")
        
    except Exception as e:
        print(f"Error in multi-stream example: {e}")
    finally:
        kafka_stream.close()
        redis_stream.close()
        print("All streams closed")


async def main():
    """Main function running all examples."""
    print("MatriceStream Usage Examples")
    print("============================")
    
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
        print(f"Error running examples: {e}")
        print("Note: Make sure Kafka and Redis servers are running and accessible")


if __name__ == "__main__":
    asyncio.run(main())
