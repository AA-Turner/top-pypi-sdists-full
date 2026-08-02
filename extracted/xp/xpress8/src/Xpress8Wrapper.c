#include "Xpress8Wrapper.h"
#include "xpress_compat.h"
#include "xpress.h"

#include <stdlib.h>
#include <string.h>

static void* XPRESS_CALL Xpress8Alloc(void* ctx, int size) {
    (void)ctx;
    return malloc((size_t)size);
}

static void XPRESS_CALL Xpress8Free(void* ctx, void* addr) {
    (void)ctx;
    free(addr);
}

XPRESS8_CONTEXT* Xpress8Initialize(int max_orig_size, int compression_level) {
    XPRESS8_CONTEXT* ctx;

    if (max_orig_size <= 0 || max_orig_size > (1 << 16)) {
        return NULL;
    }
    if (compression_level < 0) compression_level = 0;
    if (compression_level > 9) compression_level = 9;

    ctx = (XPRESS8_CONTEXT*)calloc(1, sizeof(*ctx));
    if (!ctx) return NULL;

    ctx->max_orig_size     = max_orig_size;
    ctx->compression_level = compression_level;

    ctx->decoder = (void*)XpressDecodeCreate(NULL, Xpress8Alloc);
    if (!ctx->decoder) {
        free(ctx);
        return NULL;
    }
    return ctx;
}

void Xpress8Terminate(XPRESS8_CONTEXT* ctx) {
    if (!ctx) return;
    if (ctx->decoder) {
        XpressDecodeClose((XpressDecodeStream)ctx->decoder, NULL, Xpress8Free);
        ctx->decoder = NULL;
    }
    if (ctx->encoder) {
        XpressEncodeClose((XpressEncodeStream)ctx->encoder, NULL, Xpress8Free);
        ctx->encoder = NULL;
    }
    free(ctx);
}

INT Xpress8Decompress(XPRESS8_CONTEXT* ctx,
                     const BYTE* compressed, INT compressed_size,
                     BYTE* original,   INT uncompressed_size) {
    int decoded;
    if (!ctx || !ctx->decoder || !compressed || !original) return 0;
    if (compressed_size < 0 || uncompressed_size < 0) return 0;

    /* Stored chunk: compressed_size == uncompressed_size — XpressDecode
     * returns the size but doesn't actually copy. Handle that explicitly. */
    if (compressed_size == uncompressed_size) {
        memcpy(original, compressed, (size_t)uncompressed_size);
        return uncompressed_size;
    }

    decoded = XpressDecode((XpressDecodeStream)ctx->decoder,
                           original, uncompressed_size, uncompressed_size,
                           compressed, compressed_size);
    if (decoded < 0) return 0;
    return decoded;
}

INT Xpress8Compress(XPRESS8_CONTEXT* ctx,
                    const BYTE* original,   INT original_size,
                    BYTE* compressed, INT max_compressed_size) {
    int produced;
    if (!ctx || !original || !compressed) return 0;
    if (original_size <= 0 || max_compressed_size <= 0) return 0;

    if (!ctx->encoder) {
        ctx->encoder = (void*)XpressEncodeCreate(ctx->max_orig_size,
                                                 NULL, Xpress8Alloc,
                                                 ctx->compression_level);
        if (!ctx->encoder) return 0;
    }

    produced = XpressEncode((XpressEncodeStream)ctx->encoder,
                            compressed, max_compressed_size,
                            original,   original_size,
                            NULL, NULL, 0);

    /* XpressEncode returns `original_size` when the data didn't compress and
     * leaves `compressed` undefined; caller is expected to use the original.
     * Surface that as a clean failure. */
    if (produced <= 0 || produced >= original_size) return 0;
    return produced;
}
