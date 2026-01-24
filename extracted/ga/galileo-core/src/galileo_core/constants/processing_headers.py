from enum import Enum


class ProcessingHeaders(str, Enum):
    received_at = "Galileo-Request-Received-At-Nanoseconds"
    execution_time = "Galileo-Request-Execution-Time-Seconds"
    response_at = "Galileo-Request-Response-At-Nanoseconds"
