# flake8: noqa: I005

import pyarrow as pa

class arrow_request():

    def __init__(self, arrow_bytes):
        self._arrow_bytes = arrow_bytes

    def to_pandas(self):
        arrow_buffer = pa.BufferReader(self._arrow_bytes)
        table = pa.ipc.open_stream(arrow_buffer).read_all()  # Use the buffer here
        return table.to_pandas()
