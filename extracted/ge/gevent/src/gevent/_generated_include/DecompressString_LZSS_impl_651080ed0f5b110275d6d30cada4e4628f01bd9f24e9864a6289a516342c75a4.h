#ifndef __Pyx_DecompressString_LZSS_UNUSED
CYTHON_UNUSED
static CYTHON_SMALL_CODE size_t __pyx_lzss_decompress(const uint8_t* src, uint8_t* dst, size_t dst_len) {
    size_t pos = 0, out_pos = 0;
    while (1) {
        uint32_t flags = src[pos++] | 0xFF00;
        while (flags & 0x100) {
            if (flags & 1) {
                dst[out_pos++] = src[pos++];
            } else {
                uint32_t lo = src[pos++], hi = src[pos++];
                uint32_t end_offset_of_last_occurrence, match_length;
                if (!(lo & 0x80)) {
                    end_offset_of_last_occurrence = lo;
                    match_length = hi;
                } else if (!(hi & 0x80)) {
                    end_offset_of_last_occurrence = 0x80 + (((hi << 2) & 0x180) | (lo & 0x7F));
                    match_length = hi & 0x1F;
                } else {
                    end_offset_of_last_occurrence = 0x80 + ((hi & 0x7F) << 7 | (lo & 0x7F));
                    match_length = src[pos++];
                }
                match_length += 3;
                size_t ref_pos = out_pos - end_offset_of_last_occurrence - match_length;
                memcpy(dst + out_pos, dst + ref_pos, match_length);
                out_pos += match_length;
            }
            if (out_pos >= dst_len) return pos;
            flags >>= 1;
        }
    }
}
#endif
static CYTHON_SMALL_CODE PyObject *__Pyx_DecompressString_LZSS(const char *s, size_t compressed_length, size_t uncompressed_length) {
#ifdef __Pyx_DecompressString_LZSS_UNUSED
    CYTHON_UNUSED_VAR(s);
    CYTHON_UNUSED_VAR(compressed_length);
    CYTHON_UNUSED_VAR(uncompressed_length);
    return NULL;
#else
    PyObject *result;
    unsigned char *result_data;
    size_t src_length;
    result = PyBytes_FromStringAndSize(NULL, (Py_ssize_t) uncompressed_length);
    if (unlikely(!result)) return NULL;
    result_data = __Pyx_PyBytes_AsWritableUString(result);
    if (unlikely(!result_data)) goto bad;
    src_length = __pyx_lzss_decompress((const uint8_t*) s, result_data, uncompressed_length);
    if (unlikely(src_length != compressed_length)) goto decompression_failed;
    return result;
decompression_failed:
    PyErr_SetString(PyExc_RuntimeError, "LZSS string data decompression failed");
bad:
    Py_DECREF(result);
    return NULL;
#endif
}

