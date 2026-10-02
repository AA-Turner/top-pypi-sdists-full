from __future__ import annotations

import pyarrow as pa
import pyarrow.ipc as ipc


def decode_ipc_stream(data: bytes) -> list[pa.RecordBatch]:
    """Decode Arrow IPC stream bytes into a list of RecordBatches."""
    return list(ipc.open_stream(data))


def encode_record_batch(batch: pa.RecordBatch) -> bytes:
    """Encode a RecordBatch as Arrow IPC stream bytes."""
    sink = pa.BufferOutputStream()
    with ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)
    return sink.getvalue().to_pybytes()
