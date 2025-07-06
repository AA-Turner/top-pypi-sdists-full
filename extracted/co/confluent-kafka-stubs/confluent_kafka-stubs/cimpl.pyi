"""Type hints for the confluent_kafka.cimpl module."""

from types import TracebackType
from typing import Any, Callable, Optional

# Types
ConfigDict = dict[str, Any]
# TODO: find the metadata definition
ClusterMetadata = Any
KafkaValue = str | bytes
KeyValueTuple = tuple[str, KafkaValue]

# Constants
ACL_OPERATION_ALL: int
ACL_OPERATION_ALTER: int
ACL_OPERATION_ALTER_CONFIGS: int
ACL_OPERATION_ANY: int
ACL_OPERATION_CLUSTER_ACTION: int
ACL_OPERATION_CREATE: int
ACL_OPERATION_DELETE: int
ACL_OPERATION_DESCRIBE: int
ACL_OPERATION_DESCRIBE_CONFIGS: int
ACL_OPERATION_IDEMPOTENT_WRITE: int
ACL_OPERATION_READ: int
ACL_OPERATION_UNKNOWN: int
ACL_OPERATION_WRITE: int
ACL_PERMISSION_TYPE_ALLOW: int
ACL_PERMISSION_TYPE_ANY: int
ACL_PERMISSION_TYPE_DENY: int
ACL_PERMISSION_TYPE_UNKNOWN: int
CONFIG_SOURCE_DEFAULT_CONFIG: int
CONFIG_SOURCE_DYNAMIC_BROKER_CONFIG: int
CONFIG_SOURCE_DYNAMIC_DEFAULT_BROKER_CONFIG: int
CONFIG_SOURCE_DYNAMIC_TOPIC_CONFIG: int
CONFIG_SOURCE_STATIC_BROKER_CONFIG: int
CONFIG_SOURCE_UNKNOWN_CONFIG: int
CONSUMER_GROUP_STATE_COMPLETING_REBALANCE: int
CONSUMER_GROUP_STATE_DEAD: int
CONSUMER_GROUP_STATE_EMPTY: int
CONSUMER_GROUP_STATE_PREPARING_REBALANCE: int
CONSUMER_GROUP_STATE_STABLE: int
CONSUMER_GROUP_STATE_UNKNOWN: int
OFFSET_BEGINNING: int
OFFSET_END: int
OFFSET_INVALID: int
OFFSET_STORED: int
RESOURCE_ANY: int
RESOURCE_BROKER: int
RESOURCE_GROUP: int
RESOURCE_PATTERN_ANY: int
RESOURCE_PATTERN_LITERAL: int
RESOURCE_PATTERN_MATCH: int
RESOURCE_PATTERN_PREFIXED: int
RESOURCE_PATTERN_UNKNOWN: int
RESOURCE_TOPIC: int
RESOURCE_UNKNOWN: int
TIMESTAMP_CREATE_TIME: int
TIMESTAMP_LOG_APPEND_TIME: int
TIMESTAMP_NOT_AVAILABLE: int

class KafkaError:
    # Class constants
    BROKER_NOT_AVAILABLE: int
    CLUSTER_AUTHORIZATION_FAILED: int
    CONCURRENT_TRANSACTIONS: int
    COORDINATOR_LOAD_IN_PROGRESS: int
    COORDINATOR_NOT_AVAILABLE: int
    DELEGATION_TOKEN_AUTH_DISABLED: int
    DELEGATION_TOKEN_AUTHORIZATION_FAILED: int
    DELEGATION_TOKEN_EXPIRED: int
    DELEGATION_TOKEN_NOT_FOUND: int
    DELEGATION_TOKEN_OWNER_MISMATCH: int
    DELEGATION_TOKEN_REQUEST_NOT_ALLOWED: int
    DUPLICATE_RESOURCE: int
    DUPLICATE_SEQUENCE_NUMBER: int
    ELECTION_NOT_NEEDED: int
    ELIGIBLE_LEADERS_NOT_AVAILABLE: int
    FEATURE_UPDATE_FAILED: int
    FENCED_INSTANCE_ID: int
    FENCED_LEADER_EPOCH: int
    FETCH_SESSION_ID_NOT_FOUND: int
    GROUP_AUTHORIZATION_FAILED: int
    GROUP_ID_NOT_FOUND: int
    GROUP_MAX_SIZE_REACHED: int
    GROUP_SUBSCRIBED_TO_TOPIC: int
    ILLEGAL_GENERATION: int
    ILLEGAL_SASL_STATE: int
    INCONSISTENT_GROUP_PROTOCOL: int
    INCONSISTENT_VOTER_SET: int
    INVALID_COMMIT_OFFSET_SIZE: int
    INVALID_CONFIG: int
    INVALID_FETCH_SESSION_EPOCH: int
    INVALID_GROUP_ID: int
    INVALID_MSG: int
    INVALID_MSG_SIZE: int
    INVALID_PARTITIONS: int
    INVALID_PRINCIPAL_TYPE: int
    INVALID_PRODUCER_EPOCH: int
    INVALID_PRODUCER_ID_MAPPING: int
    INVALID_RECORD: int
    INVALID_REPLICA_ASSIGNMENT: int
    INVALID_REPLICATION_FACTOR: int
    INVALID_REQUEST: int
    INVALID_REQUIRED_ACKS: int
    INVALID_SESSION_TIMEOUT: int
    INVALID_TIMESTAMP: int
    INVALID_TRANSACTION_TIMEOUT: int
    INVALID_TXN_STATE: int
    INVALID_UPDATE_VERSION: int
    KAFKA_STORAGE_ERROR: int
    LEADER_NOT_AVAILABLE: int
    LISTENER_NOT_FOUND: int
    LOG_DIR_NOT_FOUND: int
    MEMBER_ID_REQUIRED: int
    MSG_SIZE_TOO_LARGE: int
    NETWORK_EXCEPTION: int
    NO_ERROR: int
    NON_EMPTY_GROUP: int
    NO_REASSIGNMENT_IN_PROGRESS: int
    NOT_CONTROLLER: int
    NOT_COORDINATOR: int
    NOT_ENOUGH_REPLICAS: int
    NOT_ENOUGH_REPLICAS_AFTER_APPEND: int
    NOT_LEADER_FOR_PARTITION: int
    OFFSET_METADATA_TOO_LARGE: int
    OFFSET_NOT_AVAILABLE: int
    OFFSET_OUT_OF_RANGE: int
    OPERATION_NOT_ATTEMPTED: int
    OUT_OF_ORDER_SEQUENCE_NUMBER: int
    POLICY_VIOLATION: int
    PREFERRED_LEADER_NOT_AVAILABLE: int
    PRINCIPAL_DESERIALIZATION_FAILURE: int
    PRODUCER_FENCED: int
    REASSIGNMENT_IN_PROGRESS: int
    REBALANCE_IN_PROGRESS: int
    RECORD_LIST_TOO_LARGE: int
    REPLICA_NOT_AVAILABLE: int
    REQUEST_TIMED_OUT: int
    RESOURCE_NOT_FOUND: int
    SASL_AUTHENTICATION_FAILED: int
    SECURITY_DISABLED: int
    STALE_BROKER_EPOCH: int
    STALE_CTRL_EPOCH: int
    THROTTLING_QUOTA_EXCEEDED: int
    TOPIC_ALREADY_EXISTS: int
    TOPIC_AUTHORIZATION_FAILED: int
    TOPIC_DELETION_DISABLED: int
    TOPIC_EXCEPTION: int
    TRANSACTIONAL_ID_AUTHORIZATION_FAILED: int
    TRANSACTION_COORDINATOR_FENCED: int
    UNACCEPTABLE_CREDENTIAL: int
    UNKNOWN: int
    UNKNOWN_LEADER_EPOCH: int
    UNKNOWN_MEMBER_ID: int
    UNKNOWN_PRODUCER_ID: int
    UNKNOWN_TOPIC_OR_PART: int
    UNSTABLE_OFFSET_COMMIT: int
    UNSUPPORTED_COMPRESSION_TYPE: int
    UNSUPPORTED_FOR_MESSAGE_FORMAT: int
    UNSUPPORTED_SASL_MECHANISM: int
    UNSUPPORTED_VERSION: int

    # Private class constants
    _ALL_BROKERS_DOWN: int
    _APPLICATION: int
    _ASSIGNMENT_LOST: int
    _ASSIGN_PARTITIONS: int
    _AUTHENTICATION: int
    _AUTO_OFFSET_RESET: int
    _BAD_COMPRESSION: int
    _BAD_MSG: int
    _CONFLICT: int
    _CRIT_SYS_RESOURCE: int
    _DESTROY: int
    _EXISTING_SUBSCRIPTION: int
    _FAIL: int
    _FATAL: int
    _FENCED: int
    _FS: int
    _GAPLESS_GUARANTEE: int
    _INCONSISTENT: int
    _INTR: int
    _INVALID_ARG: int
    _INVALID_TYPE: int
    _IN_PROGRESS: int
    _ISR_INSUFF: int
    _KEY_DESERIALIZATION: int
    _KEY_SERIALIZATION: int
    _LOG_TRUNCATION: int
    _MAX_POLL_EXCEEDED: int
    _MSG_TIMED_OUT: int
    _NODE_UPDATE: int
    _NOENT: int
    _NOOP: int
    _NOT_CONFIGURED: int
    _NOT_IMPLEMENTED: int
    _NO_OFFSET: int
    _OUTDATED: int
    _PARTIAL: int
    _PARTITION_EOF: int
    _PREV_IN_PROGRESS: int
    _PURGE_INFLIGHT: int
    _PURGE_QUEUE: int
    _QUEUE_FULL: int
    _READ_ONLY: int
    _RESOLVE: int
    _RETRY: int
    _REVOKE_PARTITIONS: int
    _SSL: int
    _STATE: int
    _TIMED_OUT: int
    _TIMED_OUT_QUEUE: int
    _TRANSPORT: int
    _UNDERFLOW: int
    _UNKNOWN_BROKER: int
    _UNKNOWN_GROUP: int
    _UNKNOWN_PARTITION: int
    _UNKNOWN_PROTOCOL: int
    _UNKNOWN_TOPIC: int
    _UNSUPPORTED_FEATURE: int
    _VALUE_DESERIALIZATION: int
    _VALUE_SERIALIZATION: int
    _WAIT_CACHE: int
    _WAIT_COORD: int

    def __init__(
        self,
        error_code: int,
        reason: Optional[str] = None,
        fatal: bool = False,
        retriable: bool = False,
        txn_requires_abort: bool = False,
    ) -> None: ...
    def code(self) -> int: ...
    def fatal(self) -> bool: ...
    def name(self) -> str: ...
    def retriable(self) -> bool: ...
    def str(self) -> str: ...
    def txn_requires_abort(self) -> bool: ...

class KafkaException(Exception):
    # Attributes
    args: tuple[str | KafkaError]
    # Methods
    # TODO: find out what other arguments the init method takes
    def __init__(self, error: Optional[KafkaError] = None, *args, **kwargs) -> None: ...
    def add_note(self, note: str) -> None: ...
    # TODO: improve return
    def with_traceback(self, traceback: Optional[TracebackType]) -> Any: ...

class Message:
    # Methods
    def error(self) -> Optional[KafkaError]: ...
    def headers(self) -> Optional[list[KeyValueTuple]]: ...
    def key(self) -> Optional[KafkaValue]: ...
    def latency(self) -> Optional[float]: ...
    def leader_epoch(self) -> Optional[int]: ...
    def offset(self) -> Optional[int]: ...
    def partition(self) -> Optional[int]: ...
    # TODO check value types for headers, keys and values
    def set_headers(self, value: list[KeyValueTuple]) -> None: ...
    def set_key(self, value: KafkaValue) -> None: ...
    def set_value(self, value: KafkaValue) -> None: ...
    def timestamp(self) -> tuple[int, int]: ...
    def topic(self) -> Optional[str]: ...
    def value(self) -> Optional[KafkaValue]: ...

class NewPartitions:
    def __init__(
        self, topic: str, new_total_count: int, replica_assignment: Optional[list[list[str]]] = None
    ) -> None: ...

class NewTopic:
    def __init__(
        self,
        topic: str,
        num_partitions: int = -1,
        replication_factor: int = -1,
        replica_assignment: Optional[list[list[str]]] = None,
        config: Optional[dict[str, str]] = None,
    ) -> None: ...

class TopicPartition:
    def __init__(
        self,
        topic: str,
        partition: int = -1,
        offset: int = -1001,
        metadata: Optional[str] = None,
        leader_epoch: Optional[int] = None,
    ) -> None: ...

class _AdminClientImpl:
    pass

class Producer:
    # Methods
    def __init__(self, config: ConfigDict) -> None: ...
    def abort_transaction(self, timeout: Optional[float] = None) -> None: ...
    def begin_transaction(self) -> None: ...
    def commit_transaction(self, timeout: Optional[float] = None) -> None: ...
    def flush(self, timeout: Optional[float] = None) -> int: ...
    def init_transactions(self, timeout: Optional[float] = None) -> None: ...
    def list_topics(self, topic: Optional[str] = None, timeout: float = -1) -> ClusterMetadata: ...
    def poll(self, timeout: Optional[float] = None) -> int: ...
    def produce(
        self,
        topic: str,
        value: Optional[KafkaValue] = None,
        key: Optional[KafkaValue] = None,
        partition: Optional[int] = None,
        on_delivery: Optional[Callable] = None,
        # Default value for timestamp is actually current time, but setting it to zero is fine for a stub
        timestamp: int = 0,
        headers: Optional[dict[str, KafkaValue] | list[tuple[str, KafkaValue]]] = None,
    ) -> None: ...
    def purge(self, in_queue: bool = True, in_flight: bool = True, blocking: bool = True) -> None: ...
    def send_offsets_to_transactions(
        self, positions: list[TopicPartition], group_metadata: object, timeout: Optional[float] = None
    ) -> None: ...
    def set_sasl_credentials(self, username: str, password: str) -> None: ...

class Consumer:
    def __init__(self, config: ConfigDict) -> None: ...
    def assign(self, partitions: list[TopicPartition]) -> None: ...
    def assignment(self) -> list[TopicPartition]: ...
    def close(self) -> None: ...
    def commit(
        self,
        message: Optional[Message] = None,
        offsets: Optional[list[TopicPartition]] = None,
        asynchronous: bool = True,
    ) -> Optional[list[TopicPartition]]: ...
    def committed(
        self, partitions: list[TopicPartition], timeout: Optional[float | int] = None
    ) -> list[TopicPartition]: ...
    def consume(self, num_messages: int = 1, timeout: float | int = -1) -> list[TopicPartition]: ...
    def consumer_group_metadata(self) -> object: ...
    def get_watermark_offsets(
        self, partition: TopicPartition, timeout: Optional[float | int] = None, cached: bool = False
    ) -> tuple[int, int]: ...
    def incremental_assign(self, partitions: list[TopicPartition]) -> None: ...
    def incremental_unassign(self, partitions: list[TopicPartition]) -> None: ...
    def list_topics(self, topics: Optional[str] = None, timeout: float | int = -1) -> ClusterMetadata: ...
    def memberid(self) -> Optional[str]: ...
    def offsets_for_times(
        self, partitions: list[TopicPartition], timeout: Optional[float | int] = None
    ) -> list[TopicPartition]: ...
    def pause(self, partitions: list[TopicPartition]) -> None: ...
    def poll(self, poll: Optional[float | int]) -> Optional[Message]: ...
    def position(self, partitions: list[TopicPartition]) -> list[TopicPartition]: ...
    def resume(self, partitions: list[TopicPartition]) -> None: ...
    def seek(self, partition: TopicPartition) -> None: ...
    def set_sasl_credentials(self, username: str, password: str) -> None: ...
    def store_offsets(
        self, message: Optional[Message] = None, offsets: Optional[list[TopicPartition]] = None
    ) -> None: ...
    def subscribe(
        self,
        topics: list[str],
        on_assign: Optional[Callable] = None,
        on_revoke: Optional[Callable] = None,
        on_lost: Optional[Callable] = None,
    ) -> None: ...
    def unassign(self) -> None: ...
    def unsubscribe(self) -> None: ...

def libversion() -> tuple[str, int]: ...
def version() -> tuple[str, int]: ...
