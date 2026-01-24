#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake.snowpark_connect.error.error_codes import ErrorCodes


class SnowparkConnectException(Exception):
    """Parent class to all SnowparkConnect related exceptions."""

    def __init__(self, *args, custom_error_code=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.custom_error_code = custom_error_code


class MissingDatabase(SnowparkConnectException):
    def __init__(self, custom_error_code=None) -> None:
        super().__init__(
            "No default database found in session",
            custom_error_code=custom_error_code or ErrorCodes.MISSING_DATABASE,
        )


class MissingSchema(SnowparkConnectException):
    def __init__(self, custom_error_code=None) -> None:
        super().__init__(
            "No default schema found in session",
            custom_error_code=custom_error_code or ErrorCodes.MISSING_SCHEMA,
        )


class MaxRetryExceeded(SnowparkConnectException):
    def __init__(
        self,
        message="Maximum retry attempts exceeded",
    ) -> None:
        super().__init__(message)
