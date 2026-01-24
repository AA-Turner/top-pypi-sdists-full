#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Query result fetching utilities for remote client."""

import base64
import logging
from typing import Iterator, Tuple

import pyarrow as pa
from google.protobuf.message import DecodeError
from google.rpc import code_pb2, status_pb2

from snowflake.snowpark import Session
from spark.connect import envelope_pb2

logger = logging.getLogger(__name__)


def fetch_query_result_as_arrow_batches(
    session: Session, query_id: str, arrow_schema: pa.Schema
) -> Iterator[Tuple[int, bytes]]:
    """
    Fetch query results as Arrow batches.
    Used for large result sets that are fetched asynchronously.

    Yields:
        Tuples of (row_count, arrow_batch_bytes)
    """
    conn = session.connection
    cursor = conn.cursor()

    try:
        cursor.get_results_from_sfqid(query_id)

        for arrow_table in cursor.fetch_arrow_batches():
            arrow_table = arrow_table.rename_columns(
                [str(i) for i in range(arrow_table.num_columns)]
            )
            # Cast to expected schema
            arrow_table = arrow_table.cast(arrow_schema, safe=False)

            # Convert table to batches and serialize
            record_batches = arrow_table.to_batches()
            for batch in record_batches:
                sink = pa.BufferOutputStream()
                with pa.ipc.new_stream(sink, batch.schema) as writer:
                    writer.write_batch(batch)
                arrow_batch_bytes = sink.getvalue().to_pybytes()
                yield batch.num_rows, arrow_batch_bytes
    finally:
        cursor.close()


def fetch_query_result_as_protobuf(
    session: Session, query_id: str
) -> envelope_pb2.ResponseEnvelope:
    """
    Fetch query results as a ResponseEnvelope protobuf.
    Polls for async query completion and decodes the result envelope.

    Returns:
        ResponseEnvelope containing the results
    """
    conn = session.connection
    cursor = conn.cursor()

    try:
        cursor.get_results_from_sfqid(query_id)
        # Python connector does not know how to handle new "RAW" result type, so for now we must use
        # internal, private methods directly to work around this limitation
        # TODO: Add proper RAW result handling in Python connector
        cursor._prefetch_hook()  # block while polling till query is complete
        data = cursor._result_set.batches[0]._data
        resp_bytes = base64.b64decode(data)

        try:
            response_envelope = envelope_pb2.ResponseEnvelope()
            response_envelope.ParseFromString(resp_bytes)
            return response_envelope
        except DecodeError:
            logger.error(f"Failed to decode ResponseEnvelope for query_id: {query_id}")
            return envelope_pb2.ResponseEnvelope(
                status=status_pb2.Status(
                    code=code_pb2.INTERNAL, message="Invalid operation or SQL"
                )
            )
    finally:
        cursor.close()
