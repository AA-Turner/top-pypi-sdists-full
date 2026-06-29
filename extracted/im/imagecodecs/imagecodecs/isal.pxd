# imagecodecs/isal.pxd

# Cython declarations for the `ISA-L 2.32.0` library.
# https://github.com/intel/isa-l

from libc.stdint cimport (
    int16_t,
    int32_t,
    uint8_t,
    uint16_t,
    uint32_t,
    uint64_t,
)


cdef extern from 'isa-l.h' nogil:

    int ISAL_MAJOR_VERSION
    int ISAL_MINOR_VERSION
    int ISAL_PATCH_VERSION

    # igzip_lib.h

    int ISAL_DEF_MAX_HDR_SIZE
    int ISAL_DEF_MAX_CODE_LEN
    int ISAL_DEF_HIST_SIZE
    int ISAL_DEF_MAX_HIST_BITS
    int ISAL_DEF_MAX_MATCH
    int ISAL_DEF_MIN_MATCH

    int ISAL_DEF_LIT_SYMBOLS
    int ISAL_DEF_LEN_SYMBOLS
    int ISAL_DEF_DIST_SYMBOLS
    int ISAL_DEF_LIT_LEN_SYMBOLS

    int NO_FLUSH
    int SYNC_FLUSH
    int FULL_FLUSH

    int IGZIP_DEFLATE
    int IGZIP_GZIP
    int IGZIP_GZIP_NO_HDR
    int IGZIP_ZLIB
    int IGZIP_ZLIB_NO_HDR

    int COMP_OK
    int STATELESS_OVERFLOW
    int ISAL_INVALID_STATE
    int ISAL_INVALID_LEVEL
    int ISAL_INVALID_LEVEL_BUF
    int INVALID_FLUSH
    int INVALID_PARAM
    int ISAL_INVALID_OPERATION

    int IGZIP_HUFFTABLE_CUSTOM
    int IGZIP_HUFFTABLE_DEFAULT
    int IGZIP_HUFFTABLE_STATIC

    int ISAL_DEFLATE
    int ISAL_GZIP
    int ISAL_GZIP_NO_HDR
    int ISAL_ZLIB
    int ISAL_ZLIB_NO_HDR
    int ISAL_ZLIB_NO_HDR_VER
    int ISAL_GZIP_NO_HDR_VER

    int ISAL_DECOMP_OK
    int ISAL_END_INPUT
    int ISAL_OUT_OVERFLOW
    int ISAL_NAME_OVERFLOW
    int ISAL_COMMENT_OVERFLOW
    int ISAL_EXTRA_OVERFLOW
    int ISAL_NEED_DICT
    int ISAL_INVALID_BLOCK
    int ISAL_INVALID_SYMBOL
    int ISAL_INVALID_LOOKBACK
    int ISAL_INVALID_WRAPPER
    int ISAL_UNSUPPORTED_METHOD
    int ISAL_INCORRECT_CHECKSUM

    int ISAL_DEF_MIN_LEVEL
    int ISAL_DEF_MAX_LEVEL

    int ISAL_DEF_LVL0_DEFAULT
    int ISAL_DEF_LVL1_DEFAULT
    int ISAL_DEF_LVL2_DEFAULT
    int ISAL_DEF_LVL3_DEFAULT

    enum isal_zstate_state:
        ZSTATE_NEW_HDR
        ZSTATE_HDR
        ZSTATE_CREATE_HDR
        ZSTATE_BODY
        ZSTATE_FLUSH_READ_BUFFER
        ZSTATE_FLUSH_ICF_BUFFER
        ZSTATE_TYPE0_HDR
        ZSTATE_TYPE0_BODY
        ZSTATE_SYNC_FLUSH
        ZSTATE_FLUSH_WRITE_BUFFER
        ZSTATE_TRL
        ZSTATE_END
        ZSTATE_TMP_NEW_HDR
        ZSTATE_TMP_HDR
        ZSTATE_TMP_CREATE_HDR
        ZSTATE_TMP_BODY
        ZSTATE_TMP_FLUSH_READ_BUFFER
        ZSTATE_TMP_FLUSH_ICF_BUFFER
        ZSTATE_TMP_TYPE0_HDR
        ZSTATE_TMP_TYPE0_BODY
        ZSTATE_TMP_SYNC_FLUSH
        ZSTATE_TMP_FLUSH_WRITE_BUFFER
        ZSTATE_TMP_TRL
        ZSTATE_TMP_END

    enum isal_block_state:
        ISAL_BLOCK_NEW_HDR
        ISAL_BLOCK_HDR
        ISAL_BLOCK_TYPE0
        ISAL_BLOCK_CODED
        ISAL_BLOCK_INPUT_DONE
        ISAL_BLOCK_FINISH
        ISAL_GZIP_EXTRA_LEN
        ISAL_GZIP_EXTRA
        ISAL_GZIP_NAME
        ISAL_GZIP_COMMENT
        ISAL_GZIP_HCRC
        ISAL_ZLIB_DICT
        ISAL_CHECKSUM_CHECK

    struct isal_huff_histogram:
        uint64_t[286] lit_len_histogram  # ISAL_DEF_LIT_LEN_SYMBOLS
        uint64_t[30] dist_histogram  # ISAL_DEF_DIST_SYMBOLS
        uint16_t[8192] hash_table  # IGZIP_LVL0_HASH_SIZE

    struct isal_mod_hist:
        uint32_t[30] d_hist
        uint32_t[513] ll_hist

    struct isal_hufftables:
        uint8_t[328] deflate_hdr  # ISAL_DEF_MAX_HDR_SIZE
        uint32_t deflate_hdr_count
        uint32_t deflate_hdr_extra_bits
        uint32_t[2] dist_table  # IGZIP_DIST_TABLE_SIZE
        uint32_t[256] len_table  # IGZIP_LEN_TABLE_SIZE
        uint16_t[257] lit_table  # IGZIP_LIT_TABLE_SIZE
        uint8_t[257] lit_table_sizes  # IGZIP_LIT_TABLE_SIZE
        uint16_t[30] dcodes  # IGZIP_DECODE_OFFSET
        uint8_t[30] dcodes_sizes  # IGZIP_DECODE_OFFSET

    # zlib / gzip headers

    struct isal_zlib_header:
        uint32_t info
        uint32_t level
        uint32_t dict_id
        uint32_t dict_flag

    struct isal_gzip_header:
        uint32_t text
        uint32_t time
        uint32_t xflags
        uint32_t os
        uint8_t* extra
        uint32_t extra_buf_len
        uint32_t extra_len
        char* name
        uint32_t name_buf_len
        char* comment
        uint32_t comment_buf_len
        uint32_t hcrc
        uint32_t flags

    struct isal_zstate:
        pass

    struct isal_zstream:
        uint8_t* next_in
        uint32_t avail_in
        uint32_t total_in
        uint8_t* next_out
        uint32_t avail_out
        uint32_t total_out
        isal_hufftables* hufftables
        uint32_t level
        uint32_t level_buf_size
        uint8_t* level_buf
        uint16_t end_of_stream
        uint16_t flush
        uint16_t gzip_flag
        uint16_t hist_bits
        isal_zstate internal_state

    struct inflate_huff_code_large:
        uint32_t[4096] short_code_lookup  # 1 << ISAL_DECODE_LONG_BITS
        uint16_t[1264] long_code_lookup  # ISAL_HUFF_CODE_LARGE_LONG_ALIGNED

    struct inflate_huff_code_small:
        uint16_t[1024] short_code_lookup  # 1 << ISAL_DECODE_SHORT_BITS
        uint16_t[80] long_code_lookup  # ISAL_HUFF_CODE_SMALL_LONG_ALIGNED

    struct inflate_state:
        uint8_t* next_out
        uint32_t avail_out
        uint32_t total_out
        uint8_t* next_in
        uint64_t read_in
        uint32_t avail_in
        int32_t read_in_length
        inflate_huff_code_large lit_huff_code
        inflate_huff_code_small dist_huff_code
        isal_block_state block_state
        uint32_t dict_length
        uint32_t bfinal
        uint32_t crc_flag
        uint32_t crc
        uint32_t hist_bits
        int32_t type0_block_len  # union { type0_block_len, count, dict_id }
        int32_t write_overflow_lits
        int32_t write_overflow_len
        int32_t copy_overflow_length
        int32_t copy_overflow_distance
        int16_t wrapper_flag
        int16_t tmp_in_size
        int32_t tmp_out_valid
        int32_t tmp_out_processed
        uint8_t[328] tmp_in_buffer  # ISAL_DEF_MAX_HDR_SIZE
        uint8_t[65824] tmp_out_buffer  # 2*ISAL_DEF_HIST_SIZE + ISAL_LOOK_AHEAD

    struct isal_dict:
        uint32_t params
        uint32_t level
        uint32_t hist_size
        uint32_t hash_size
        uint8_t[32768] history  # ISAL_DEF_HIST_SIZE
        uint16_t[32768] hashtable  # IGZIP_LVL3_HASH_SIZE

    void isal_deflate_init(
        isal_zstream* stream
    )

    void isal_deflate_reset(
        isal_zstream* stream
    )

    void isal_gzip_header_init(
        isal_gzip_header* gz_hdr
    )

    void isal_zlib_header_init(
        isal_zlib_header* z_hdr
    )

    uint32_t isal_write_gzip_header(
        isal_zstream* stream,
        isal_gzip_header* gz_hdr
    )

    uint32_t isal_write_zlib_header(
        isal_zstream* stream,
        isal_zlib_header* z_hdr
    )

    int isal_deflate_set_hufftables(
        isal_zstream* stream,
        isal_hufftables* hufftables,
        int type
    )

    void isal_deflate_stateless_init(
        isal_zstream* stream
    )

    int isal_deflate_set_dict(
        isal_zstream* stream,
        uint8_t* dict,
        uint32_t dict_len
    )

    int isal_deflate_process_dict(
        isal_zstream* stream,
        isal_dict* dict_str,
        uint8_t* dict,
        uint32_t dict_len
    )

    int isal_deflate_reset_dict(
        isal_zstream* stream,
        isal_dict* dict_str
    )

    int isal_deflate(
        isal_zstream* stream
    )

    int isal_deflate_stateless(
        isal_zstream* stream
    )

    void isal_inflate_init(
        inflate_state* state
    )

    void isal_inflate_reset(
        inflate_state* state
    )

    int isal_inflate_set_dict(
        inflate_state* state,
        uint8_t* dict,
        uint32_t dict_len
    )

    int isal_read_gzip_header(
        inflate_state* state,
        isal_gzip_header* gz_hdr
    )

    int isal_read_zlib_header(
        inflate_state* state,
        isal_zlib_header* zlib_hdr
    )

    int isal_inflate(
        inflate_state* state
    )

    int isal_inflate_stateless(
        inflate_state* state
    )

    uint32_t isal_adler32_c "isal_adler32"(
        uint32_t init,
        const unsigned char* buf,
        uint64_t len
    )

    void isal_update_histogram(
        uint8_t* in_stream,
        int length,
        isal_huff_histogram* histogram
    )

    int isal_create_hufftables(
        isal_hufftables* hufftables,
        isal_huff_histogram* histogram
    )

    int isal_create_hufftables_subset(
        isal_hufftables* hufftables,
        isal_huff_histogram* histogram
    )

    # crc.h

    uint16_t crc16_t10dif(
        uint16_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint16_t crc16_t10dif_copy(
        uint16_t init_crc,
        uint8_t* dst,
        uint8_t* src,
        uint64_t len
    )

    uint32_t crc32_ieee(
        uint32_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint32_t crc32_gzip_refl(
        uint32_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    unsigned int crc32_iscsi(
        unsigned char* buffer,
        int len,
        unsigned int init_crc
    )

    # crc64.h

    uint64_t crc64_ecma_refl(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint64_t crc64_ecma_norm(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint64_t crc64_iso_refl(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint64_t crc64_iso_norm(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint64_t crc64_jones_refl(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint64_t crc64_jones_norm(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint64_t crc64_rocksoft_refl(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )

    uint64_t crc64_rocksoft_norm(
        uint64_t init_crc,
        const unsigned char* buf,
        uint64_t len
    )
