from deciphon_schema import Gencode, HMMFile

from deciphon_core._cffi import ffi, lib
from deciphon_core.error import DeciphonError

__all__ = ["PressContext"]


class PressContext:
    def __init__(self, hmm: HMMFile, gencode: Gencode, epsilon: float = 0.01):
        self._cpress = lib.dcp_press_new()
        self._hmm = hmm

        if self._cpress == ffi.NULL:
            raise MemoryError()

        if rc := lib.dcp_press_setup(self._cpress, gencode, epsilon):
            raise DeciphonError(rc)

    def open(self):
        hmmpath = bytes(self._hmm.path)
        dbpath = bytes(self._hmm.dbpath.path)
        if rc := lib.dcp_press_open(self._cpress, hmmpath, dbpath):
            raise DeciphonError(rc)

    def close(self):
        if rc := lib.dcp_press_close(self._cpress):
            raise DeciphonError(rc)

    def end(self) -> bool:
        return lib.dcp_press_end(self._cpress)

    def next(self):
        if rc := lib.dcp_press_next(self._cpress):
            raise DeciphonError(rc)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *_):
        self.close()

    @property
    def nproteins(self) -> int:
        return lib.dcp_press_nproteins(self._cpress)

    def __del__(self):
        if getattr(self, "_cpress", ffi.NULL) != ffi.NULL:
            lib.dcp_press_del(self._cpress)
