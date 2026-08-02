#ifndef XPRESS8_WRAPPER_H
#define XPRESS8_WRAPPER_H

#ifdef __cplusplus
extern "C" {
#endif

typedef unsigned char BYTE;
typedef int           INT;
typedef unsigned int  UINT;

/* Opaque context bundling encoder + decoder streams. */
typedef struct XPRESS8_CONTEXT {
    void* decoder;
    void* encoder;
    int   max_orig_size;
    int   compression_level;
} XPRESS8_CONTEXT;

/* Create a context with a decoder. Encoder is created lazily on first compress.
 * max_orig_size must be <= XPRESS_MAX_BLOCK (65536).
 * compression_level: 0 (fast) .. 9 (best). */
XPRESS8_CONTEXT* Xpress8Initialize(int max_orig_size, int compression_level);

/* Tear down everything and free the context. */
void Xpress8Terminate(XPRESS8_CONTEXT* ctx);

/* Decompress `compressed` (compressed_size bytes) into `original`, expecting
 * `uncompressed_size` bytes of output. Returns the number of bytes decoded
 * (== uncompressed_size on success) or 0 on failure. */
INT Xpress8Decompress(XPRESS8_CONTEXT* ctx,
                      const BYTE* compressed, INT compressed_size,
                      BYTE* original,   INT uncompressed_size);

/* Compress `original` into `compressed` (up to max_compressed_size bytes).
 * Returns size of compressed output, or 0 on failure / non-effective compression. */
INT Xpress8Compress(XPRESS8_CONTEXT* ctx,
                    const BYTE* original,   INT original_size,
                    BYTE* compressed, INT max_compressed_size);

#ifdef __cplusplus
}
#endif

#endif /* XPRESS8_WRAPPER_H */
