# xpress8.pxd

cdef extern from "Xpress8Wrapper.h":
    ctypedef struct XPRESS8_CONTEXT:
        void* decoder
        void* encoder
        int   max_orig_size
        int   compression_level
    ctypedef unsigned int UINT
    ctypedef unsigned char BYTE
    ctypedef int INT

    XPRESS8_CONTEXT* Xpress8Initialize(int max_orig_size, int compression_level) nogil
    void Xpress8Terminate(XPRESS8_CONTEXT* ctx) nogil
    INT  Xpress8Decompress(XPRESS8_CONTEXT* ctx, const BYTE* compressed, INT compressed_size,
                           BYTE* original, INT uncompressed_size) nogil
    INT  Xpress8Compress(XPRESS8_CONTEXT* ctx, const BYTE* original, INT original_size,
                         BYTE* compressed, INT max_compressed_size) nogil
