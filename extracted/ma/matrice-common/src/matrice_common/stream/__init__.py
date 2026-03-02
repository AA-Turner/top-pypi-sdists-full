"""Matrice streaming module providing unified interface for Kafka and Redis operations."""

from .kafka_stream import (
    KafkaUtils,
    AsyncKafkaUtils,
    MatriceKafkaDeployment
)
from .redis_stream import (
    RedisUtils,
    AsyncRedisUtils,
    MatriceRedisDeployment
)
from .matrice_stream import (
    MatriceStream,
    StreamType
)
from .event_listener import EventListener

__all__ = [
    # Main unified streaming interface
    'MatriceStream',
    'StreamType',

    # Kafka utilities
    'KafkaUtils',
    'AsyncKafkaUtils',
    'MatriceKafkaDeployment',

    # Event listening
    'EventListener',

    # Redis utilities
    'RedisUtils',
    'AsyncRedisUtils',
    'MatriceRedisDeployment'
]
