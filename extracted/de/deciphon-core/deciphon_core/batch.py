from __future__ import annotations

from deciphon_core._cffi import ffi, lib
from deciphon_core.error import DeciphonError
from deciphon_core.sequence import Sequence


class Batch:
    def __init__(self):
        self._cbatch = lib.dcp_batch_new()
        if self._cbatch == ffi.NULL:
            raise MemoryError()

    def add(self, sequence: Sequence):
        id = sequence.id
        name = sequence.name.encode()
        data = sequence.data.encode()
        if rc := lib.dcp_batch_add(self._cbatch, id, name, data):
            raise DeciphonError(rc)

    def reset(self):
        lib.dcp_batch_reset(self._cbatch)

    @property
    def cdata(self):
        return self._cbatch

    def __del__(self):
        if getattr(self, "_cbatch", ffi.NULL) != ffi.NULL:
            lib.dcp_batch_del(self._cbatch)
