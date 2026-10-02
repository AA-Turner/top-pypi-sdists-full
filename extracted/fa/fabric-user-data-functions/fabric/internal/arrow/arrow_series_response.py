# flake8: noqa: I005
import pyarrow as pa

class arrow_series_response():

    def __init__(self, series):
        self._series = series

    def to_bytes(self) -> bytes:
        sink = pa.BufferOutputStream()
        arrow_array = pa.array(self._series)
        arrow_name = self._series.name if self._series.name else "data"
        writer = pa.ipc.new_stream(sink, schema=pa.schema([(arrow_name, arrow_array.type)]))
        batch_arrow = pa.record_batch([arrow_array], names=[arrow_name])
        writer.write_batch(batch_arrow)
        writer.close()
        return sink.getvalue().to_pybytes()
