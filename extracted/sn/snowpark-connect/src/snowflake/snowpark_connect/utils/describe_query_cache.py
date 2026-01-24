#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import hashlib
import inspect
import random
import re
import time
from typing import Any

from snowflake import snowpark
from snowflake.connector.cursor import ResultMetadataV2
from snowflake.snowpark._internal.server_connection import ServerConnection
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.concurrent import (
    SynchronizedDict,
    SynchronizedList,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import telemetry

USE_DESCRIBE_QUERY_CACHE = True

DDL_DETECTION_PATTERN = re.compile(r"\s*(CREATE|ALTER|DROP)\b", re.IGNORECASE)
PLAIN_CREATE_PATTERN = re.compile(
    r"\s*CREATE\s+((LOCAL|GLOBAL)\s+)?(TRANSIENT\s+)?TABLE\b", re.IGNORECASE
)

# Pattern for simple constant queries like: SELECT 3 :: INT AS "3-80000030-0" FROM ( SELECT $1 AS "__DUMMY" FROM  VALUES (NULL :: STRING))
# Using exact spacing pattern from generated SQL for deterministic matching
# Column ID format: {original_name}-{8_digit_hex_plan_id}-{column_index}
# Examples: "i-8000002a-0", "1-8000002c-0"
SIMPLE_CONSTANT_PATTERN = re.compile(
    r'^\s*SELECT (\d+) :: INT AS "([^"]+)" FROM \( SELECT \$1 AS "__DUMMY" FROM  VALUES \(NULL :: STRING\)\)\s*$',
    re.IGNORECASE,
)


class DescribeQueryCache:
    def __init__(self) -> None:
        self._cache = SynchronizedDict()

    @staticmethod
    def _hash_query(sql_query: str) -> str:
        return hashlib.md5(sql_query.encode("utf-8")).hexdigest()

    @staticmethod
    def _get_cache_key(sql_query: str) -> str:
        """Get cache key for a query, normalizing simple constants."""
        if SIMPLE_CONSTANT_PATTERN.match(sql_query):
            # Normalize simple constants to share cache entries
            return 'SELECT PLACEHOLDER :: INT AS "PLACEHOLDER" FROM ( SELECT $1 AS "__DUMMY" FROM  VALUES (NULL :: STRING))'
        return sql_query

    def get(self, sql_query: str) -> list[ResultMetadataV2] | None:
        from snowflake.snowpark_connect.config import get_describe_cache_ttl_seconds

        telemetry.report_describe_query_cache_lookup()

        cache_key = self._get_cache_key(sql_query)
        key = self._hash_query(cache_key)
        current_time = time.monotonic()

        if key in self._cache:
            result, timestamp = self._cache[key]

            expired_by = current_time - (timestamp + get_describe_cache_ttl_seconds())
            if expired_by < 0:
                logger.debug(
                    f"Returning query result from cache for query: {sql_query[:20]}"
                )
                self._cache[key] = (result, current_time)

                # If this is a constant query, we need to transform the result metadata
                # to match the actual query's column name
                if cache_key != sql_query:  # Only transform if we normalized the key
                    match = SIMPLE_CONSTANT_PATTERN.match(sql_query)
                    if match:
                        number, column_id = match.groups()
                        expected_column_name = column_id

                        # Transform the cached result to match this query's column name
                        # There should only be one column in these constant queries
                        metadata = result[0]
                        new_metadata = ResultMetadataV2(
                            name=expected_column_name,
                            type_code=metadata.type_code,
                            display_size=metadata.display_size,
                            internal_size=metadata.internal_size,
                            precision=metadata.precision,
                            scale=metadata.scale,
                            is_nullable=metadata.is_nullable,
                        )

                        telemetry.report_describe_query_cache_hit()
                        return [new_metadata]

                telemetry.report_describe_query_cache_hit()
                return result
            else:
                telemetry.report_describe_query_cache_expired(expired_by)
                del self._cache[key]
        return None

    def put(self, sql_query: str, result: list[ResultMetadataV2] | None) -> None:
        if result is None:
            return

        cache_key = self._get_cache_key(sql_query)
        key = self._hash_query(cache_key)

        logger.debug(f"Putting query into cache: {sql_query[:50]}...")

        self._cache[key] = (result, time.monotonic())

    def clear(self) -> None:
        self._cache.clear()

    def update_cache_for_query(self, query: str) -> None:
        # Clear cache for DDL operations that modify existing objects (exclude CREATE TABLE)
        if DDL_DETECTION_PATTERN.search(query) and not PLAIN_CREATE_PATTERN.search(
            query
        ):
            self.clear()
            telemetry.report_describe_query_cache_clear()


def instrument_session_for_describe_cache(session: snowpark.Session):
    if hasattr(session, "_describe_query_cache"):
        logger.debug(
            "Session already instrumented for describe query cache, skipping..."
        )
        return

    session._describe_query_cache = DescribeQueryCache()
    session._snowpark_api_describe_calls = SynchronizedList()

    def update_cache_for_query(query: str):
        cache = None
        cache_instance = getattr(session, "_describe_query_cache", None)
        if isinstance(cache_instance, DescribeQueryCache):
            cache = cache_instance

        cache.update_cache_for_query(query)

    def wrap_execute(wrapped_fn):
        def fn(query: str, **kwargs):
            update_cache_for_query(query)
            try:
                result = wrapped_fn(query, **kwargs)
                telemetry.report_query(result, **kwargs)
            except Exception as e:
                telemetry.report_query(e, **kwargs)
                attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
                raise e
            return result

        return fn

    # This is a wrapper to cache describe queries.
    def cached_describe_internal(session, wrapped_fn):
        def fn(*args: Any, **kwargs: Any) -> list[ResultMetadataV2] | None:
            def _should_skip_query():
                # We skip queries that are not relevant, but can introduce non-determinism since many tests share the same session
                f = inspect.currentframe().f_back
                while f is not None:
                    if "resources_initializer" in f.f_code.co_filename:
                        # async resource initialization
                        return True
                    f = f.f_back
                return False

            # In tests, we want to record describe queries before reaching to cache (`_test_name` is only present in expectation tests).
            if hasattr(session, "_test_name") and not _should_skip_query():
                session._snowpark_api_describe_calls.append(
                    {
                        "test_name": session._test_name,
                        "query_hash": DescribeQueryCache._hash_query(args[0])
                        if isinstance(args[0], str)
                        else f"unknown{random.randint(0, 2**32)}",
                    }
                )

            if not USE_DESCRIBE_QUERY_CACHE:
                return wrapped_fn(*args, **kwargs)

            # Query should be first arg
            if args and isinstance(args[0], str):
                query = args[0]
            else:
                logger.debug(
                    "Warning: Could not extract query string from args in cached_describe_internal. Skipping cache."
                )
                return wrapped_fn(*args, **kwargs)  # Call original

            # TODO cache on cursor - does it make sense?
            cache = None
            cache_instance = getattr(session, "_describe_query_cache", None)
            if isinstance(cache_instance, DescribeQueryCache):
                cache = cache_instance

            if cache:
                cached_result = cache.get(query)
                if cached_result is not None:
                    return cached_result

            # No cache hit, so we call the orig describe function and make a snowflake query
            result = wrapped_fn(*args, **kwargs)

            if cache and result is not None:
                cache.put(query, result)

            return result

        return fn

    # TODO: is there a better way to intercept queries?
    orig_cursor_getter = ServerConnection._cursor.fget

    def cursor_wrapper(conn):
        cursor = orig_cursor_getter(conn)
        if hasattr(cursor, "_instrumented_describe") and cursor._instrumented_describe:
            return cursor

        cursor.execute = wrap_execute(cursor.execute)

        # Override describe so that we can stop queries from being sent to Snowflake if they are
        # already in the cache.
        # TODO: Test with multiple sessions to confirm we don't cross them
        cursor._describe_internal = cached_describe_internal(
            session, cursor._describe_internal
        )

        cursor._instrumented_describe = True
        return cursor

    setattr(ServerConnection, "_cursor", property(cursor_wrapper))  # noqa: B010
