from __future__ import annotations

import pyarrow as pa
import pyarrow.ipc as ipc


def decode_ipc_stream(data: bytes) -> list[pa.RecordBatch]:
    """Eagerly decode all batches, for callers that need the complete stream.

    For incremental processing, iterate over ``ipc.open_stream(data)`` instead.
    """
    with ipc.open_stream(data) as reader:
        return list(reader)


def encode_record_batch(batch: pa.RecordBatch) -> bytes:
    """Encode a RecordBatch as Arrow IPC stream bytes."""
    sink = pa.BufferOutputStream()
    with ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)
    return sink.getvalue().to_pybytes()
