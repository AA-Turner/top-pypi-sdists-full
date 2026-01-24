#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from google.rpc import status_pb2


class SparkConnectServerException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class InvalidHostException(SparkConnectServerException):
    def __init__(self, message) -> None:
        super().__init__(message)


class MissingAuthException(SparkConnectServerException):
    def __init__(self) -> None:
        super().__init__("Missing authorization information")


class UnexpectedResponseException(SparkConnectServerException):
    def __init__(self, message) -> None:
        super().__init__(message)


class QueryTimeoutException(SparkConnectServerException):
    def __init__(self, message) -> None:
        super().__init__(message)


class GrpcErrorStatusException(SparkConnectServerException):
    def __init__(self, status: status_pb2.Status) -> None:
        super().__init__(f"Error code: {status.code}, message: {status.message}")
        self.status = status
