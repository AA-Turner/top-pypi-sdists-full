# flake8: noqa: I005
import pyarrow as pa

class arrow_dataframe_response():

    def __init__(self, df):
        self._df = df

    def to_bytes(self) -> bytes:
        sink = pa.BufferOutputStream()
        batch_arrow = pa.RecordBatch.from_pandas(self._df)
        writer = pa.ipc.new_stream(sink, batch_arrow.schema)
        writer.write_batch(batch_arrow)
        writer.close()
        return sink.getvalue().to_pybytes()
