# distutils: language = c
# cython: boundscheck=False, wraparound=False, initializedcheck=False

from libc.stdlib cimport malloc, free
from libc.string cimport memcpy
from cpython.bytearray cimport PyByteArray_Resize, PyByteArray_AS_STRING
from xpress8 cimport (XPRESS8_CONTEXT, Xpress8Initialize, Xpress8Terminate,
                     Xpress8Decompress, Xpress8Compress, BYTE, INT)

DEF XPRESS_MAX_BLOCK = 1 << 16


cdef class Xpress8:
    """Python wrapper for Microsoft's Xpress8 (ESE) compression library."""

    cdef XPRESS8_CONTEXT* context
    cdef int _max_orig_size

    def __cinit__(self, int max_original_size=XPRESS_MAX_BLOCK,
                  int compression_level=9):
        if max_original_size <= 0 or max_original_size > XPRESS_MAX_BLOCK:
            raise ValueError(
                "max_original_size must be in 1..%d" % XPRESS_MAX_BLOCK)
        self._max_orig_size = max_original_size
        self.context = Xpress8Initialize(max_original_size, compression_level)
        if self.context is NULL:
            raise MemoryError("Failed to initialize Xpress8 context.")

    def __dealloc__(self):
        if self.context is not NULL:
            Xpress8Terminate(self.context)
            self.context = NULL

    def compress(self, data, int max_compressed_size=-1):
        """Compress `data` (bytes-like). Returns compressed bytes."""
        cdef const unsigned char[::1] inview = data
        cdef INT in_size = inview.shape[0]
        if in_size == 0:
            return b""
        if max_compressed_size <= 0:
            max_compressed_size = in_size + 64
        cdef BYTE* out_ptr = <BYTE*>malloc(max_compressed_size)
        if not out_ptr:
            raise MemoryError("Failed to allocate compression output buffer.")
        cdef INT out_size
        with nogil:
            out_size = Xpress8Compress(self.context, &inview[0], in_size,
                                      out_ptr, max_compressed_size)
        if out_size <= 0:
            free(out_ptr)
            raise ValueError("Xpress8 compression failed.")
        result = bytes(out_ptr[:out_size])
        free(out_ptr)
        return result

    def decompress(self, data, int uncompressed_size):
        """Decompress `data` into exactly `uncompressed_size` bytes."""
        cdef const unsigned char[::1] inview = data
        cdef INT in_size = inview.shape[0]
        if uncompressed_size <= 0:
            return b""
        cdef BYTE* out_ptr = <BYTE*>malloc(uncompressed_size)
        if not out_ptr:
            raise MemoryError("Failed to allocate decompression output buffer.")
        cdef INT decoded
        cdef const BYTE* in_ptr = &inview[0] if in_size else NULL
        with nogil:
            decoded = Xpress8Decompress(self.context, in_ptr, in_size,
                                       out_ptr, uncompressed_size)
        if decoded != uncompressed_size:
            free(out_ptr)
            raise ValueError(
                "Decompression failed: expected %d bytes, got %d" %
                (uncompressed_size, decoded))
        result = bytes(out_ptr[:uncompressed_size])
        free(out_ptr)
        return result

    def decompress_chunked(self, data):
        """Decompress a PBIX-style chunked stream.

        Each chunk is prefixed by a 4-byte header of two little-endian uint16
        values (uncompressed_size, compressed_size). When they are equal the
        chunk is stored as-is; otherwise it's Xpress8-compressed.
        """
        cdef const unsigned char[::1] inview = data
        cdef Py_ssize_t total = inview.shape[0]
        if total == 0:
            return b""

        cdef const BYTE* src = &inview[0]
        cdef Py_ssize_t pos = 0
        cdef unsigned int u_size, c_size
        cdef INT decoded
        cdef bytearray out = bytearray()
        cdef Py_ssize_t out_pos = 0
        cdef BYTE* dst

        while pos + 4 <= total:
            u_size = src[pos] | (src[pos + 1] << 8)
            c_size = src[pos + 2] | (src[pos + 3] << 8)
            pos += 4
            if pos + <Py_ssize_t>c_size > total:
                break
            out_pos = len(out)
            if PyByteArray_Resize(out, out_pos + <Py_ssize_t>u_size) != 0:
                raise MemoryError("Failed to grow output bytearray.")
            dst = <BYTE*>PyByteArray_AS_STRING(out)
            with nogil:
                decoded = Xpress8Decompress(self.context,
                                           src + pos, <INT>c_size,
                                           dst + out_pos, <INT>u_size)
            if decoded != <INT>u_size:
                raise ValueError(
                    "Chunk decompression failed: expected %d bytes, got %d "
                    "(chunk at offset %d)" % (u_size, decoded, pos - 4))
            pos += <Py_ssize_t>c_size

        return bytes(out)
