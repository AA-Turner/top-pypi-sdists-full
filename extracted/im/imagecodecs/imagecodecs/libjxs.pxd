# imagecodecs/libjxs.pxd

# Cython declarations for the `libjxs 3.0.2` library.
# https://jpeg.org/jpegxs/software.html

from libc.stdint cimport int8_t, int32_t, uint8_t, uint16_t, uint32_t

ctypedef bint bool

cdef extern from 'libjxs.h' nogil:

    ctypedef int32_t xs_data_in_t

    int MAX_NDECOMP_H
    int MAX_NDECOMP_V
    int MAX_NCOMPS

    int MAX_NFILTER_TYPES
    int MAX_NBANDS

    ctypedef enum xs_gains_mode_t:
        XS_GAINS_OPT_PSNR
        XS_GAINS_OPT_VISUAL
        XS_GAINS_OPT_EXPLICIT

    ctypedef enum xs_profile_t:
        XS_PROFILE_AUTO
        XS_PROFILE_UNRESTRICTED
        XS_PROFILE_LIGHT_422_10
        XS_PROFILE_LIGHT_444_12
        XS_PROFILE_LIGHT_SUBLINE_422_10
        XS_PROFILE_MAIN_420_12
        XS_PROFILE_MAIN_422_10
        XS_PROFILE_MAIN_444_12
        XS_PROFILE_MAIN_4444_12
        XS_PROFILE_HIGH_420_12
        XS_PROFILE_HIGH_444_12
        XS_PROFILE_HIGH_4444_12
        XS_PROFILE_MLS_12
        XS_PROFILE_MLS_16
        XS_PROFILE_LIGHT_BAYER
        XS_PROFILE_MAIN_BAYER
        XS_PROFILE_HIGH_BAYER
        XS_PROFILE_CHIGH_444_12
        XS_PROFILE_TDC_444_12
        XS_PROFILE_TDC_MLS_444_12

    ctypedef enum xs_level_t:
        XS_LEVEL_AUTO
        XS_LEVEL_UNRESTRICTED
        XS_LEVEL_1K_1
        XS_LEVEL_2K_1
        XS_LEVEL_4K_1
        XS_LEVEL_4K_2
        XS_LEVEL_4K_3
        XS_LEVEL_8K_1
        XS_LEVEL_8K_2
        XS_LEVEL_8K_3
        XS_LEVEL_10K_1
        XS_LEVEL_MASK

    ctypedef enum xs_sublevel_t:
        XS_SUBLEVEL_AUTO
        XS_SUBLEVEL_UNRESTRICTED
        XS_SUBLEVEL_FULL
        XS_SUBLEVEL_12_BPP
        XS_SUBLEVEL_9_BPP
        XS_SUBLEVEL_6_BPP
        XS_SUBLEVEL_4_BPP
        XS_SUBLEVEL_3_BPP
        XS_SUBLEVEL_2_BPP
        XS_SUBLEVEL_MASK

    ctypedef enum xs_fbblevel_t:
        XS_FBBLEVEL_AUTO
        XS_FBBLEVEL_UNRESTRICTED
        XS_FBBLEVEL_3_BPP
        XS_FBBLEVEL_4_5_BPP
        XS_FBBLEVEL_12_BPP
        XS_FBBLEVEL_FULL
        XS_FBBLEVEL_MASK

    ctypedef enum xs_cpih_t:
        XS_CPIH_AUTO
        XS_CPIH_NONE
        XS_CPIH_RCT
        XS_CPIH_TETRIX

    ctypedef enum xs_cap_t:
        XS_CAP_AUTO
        XS_CAP_STAR_TETRIX
        XS_CAP_NLT_Q
        XS_CAP_NLT_E
        XS_CAP_SY
        XS_CAP_SD
        XS_CAP_MLS
        XS_CAP_RAW_PER_PKT
        XS_CAP_FRAMEBUFFER

    ctypedef enum xs_nlt_t:
        XS_NLT_NONE
        XS_NLT_QUADRATIC
        XS_NLT_EXTENDED

    ctypedef struct _xs_nlt_parameters_1:
        uint16_t sigma
        uint16_t alpha

    ctypedef struct _xs_nlt_parameters_2:
        uint32_t T1
        uint32_t T2
        uint8_t E

    ctypedef union xs_nlt_parameters_t:
        _xs_nlt_parameters_1 quadratic
        _xs_nlt_parameters_2 extended

    ctypedef enum xs_tetrix_t:
        XS_TETRIX_FULL
        XS_TETRIX_INLINE

    ctypedef struct xs_cts_parameters_t:
        xs_tetrix_t Cf
        uint8_t e1
        uint8_t e2

    ctypedef struct xs_tpc_parameters_t:
        uint8_t S_i
        int8_t Qbi
        int8_t Qbr
        uint8_t[41] Yh  # MAX_NBANDS + 1
        uint8_t[41] Sh  # MAX_NBANDS + 1
        bool enabled

    ctypedef enum xs_cfa_pattern_t:
        XS_CFA_RGGB
        XS_CFA_BGGR
        XS_CFA_GRBG
        XS_CFA_GBRG

    int XS_CFA_NONE

    ctypedef struct xs_config_parameters_t:
        xs_cpih_t color_transform
        uint16_t Cw
        uint16_t slice_height
        uint8_t N_g
        uint8_t S_s
        uint8_t Bw
        uint8_t Fq
        uint8_t B_r
        uint8_t Fslc
        uint8_t Ppoc
        int8_t NLx
        int8_t NLy
        uint8_t Lh
        uint8_t Rl
        uint8_t Qpih
        uint8_t Fs
        uint8_t Rm
        int8_t Sd
        uint8_t[2][41] lvl_gain  # MAX_NBANDS + 1
        uint8_t[2][41] lvl_prio  # MAX_NBANDS + 1
        xs_nlt_t Tnlt
        xs_nlt_parameters_t Tnlt_params
        xs_cts_parameters_t tetrix_params
        xs_cfa_pattern_t cfa_pattern
        xs_tpc_parameters_t tpc

    ctypedef struct xs_config_t:
        size_t bitstream_size_in_bytes
        float ra_budget_lines
        uint8_t tdc_enc_refresh_cycle
        float Bf
        int verbose
        xs_gains_mode_t gains_mode
        bool refresh_gains_explicit
        xs_profile_t profile
        xs_level_t level
        xs_sublevel_t sublevel
        xs_fbblevel_t fbblevel
        xs_cap_t cap_bits
        bool use_long_precinct_headers
        bool use_tdc_mode
        xs_config_parameters_t p

    ctypedef struct xs_buffer_model_parameters_t:
        int Nbpp
        int Nsbu
        int Ssbo
        int Wcmax
        int Ssbu
        int N_g

    ctypedef struct xs_image_t:
        int width
        int height
        int8_t ncomps
        int8_t[4] sx  # MAX_NCOMPS
        int8_t[4] sy  # MAX_NCOMPS
        int8_t depth
        (xs_data_in_t*)[4] comps_array  # MAX_NCOMPS

    bool xs_allocate_image(
        xs_image_t* ptr,
        const bool set_zero
    )

    void xs_free_image(
        xs_image_t* ptr
    )

    ctypedef struct xs_enc_context_t:
        pass

    xs_enc_context_t* xs_enc_init(
        xs_config_t* xs_config,
        xs_image_t* image
    )

    void xs_enc_close(
        xs_enc_context_t* ctx
    )

    bool xs_enc_image(
        xs_enc_context_t* ctx,
        uint32_t frame_num,
        xs_image_t* image,
        uint8_t* bitstream_buf,
        size_t bitstream_buf_byte_size,
        size_t* bitstream_byte_size
    )

    bool xs_enc_preprocess_image(
        const xs_config_t* xs_config,
        xs_image_t* image
    )

    ctypedef struct xs_dec_context_t:
        pass

    ctypedef void (*xs_fragment_info_cb_t)(
        void* context,
        const int f_id,
        const int f_Sbits,
        const int f_Ncg,
        const int f_padding_bits
    ) nogil

    ctypedef void (*xs_fbc_bpc_info_cb_t)(
        void* context,
        int bp_count
    ) nogil

    bool xs_dec_probe(
        uint8_t* bitstream_buf,
        size_t codestream_size,
        xs_config_t* xs_config,
        xs_image_t* image
    )

    xs_dec_context_t* xs_dec_init(
        xs_config_t* xs_config,
        xs_image_t* image
    )

    bool xs_dec_set_fragment_info_cb(
        xs_dec_context_t* ctx,
        xs_fragment_info_cb_t ficb,
        void* fictx
    )

    bool xs_dec_set_fbc_bpc_info_cb(
        xs_dec_context_t* ctx,
        xs_fbc_bpc_info_cb_t fbcb,
        void* fbctx
    )

    void xs_dec_close(
        xs_dec_context_t* ctx
    )

    bool xs_dec_bitstream(
        xs_dec_context_t* ctx,
        uint32_t frame_num,
        uint8_t* bitstream_buf,
        size_t bitstream_buf_byte_size,
        xs_image_t* image_out
    )

    bool xs_dec_postprocess_image(
        const xs_config_t* xs_config,
        xs_image_t* image_out
    )

    bool xs_config_parse_and_init(
        xs_config_t* cfg,
        const xs_image_t* im,
        const char* config_str,
        const size_t config_str_max_len
    )

    bool xs_config_dump(
        const xs_config_t* cfg,
        const xs_image_t* im,
        char* config_str,
        size_t config_str_max_len,
        int details
    )

    bool xs_config_validate(
        const xs_config_t* cfg,
        const xs_image_t* im
    )

    bool xs_config_retrieve_buffer_model_parameters(
        const xs_config_t* cfg,
        xs_buffer_model_parameters_t* bmp
    )

    void xs_config_nlt_extended_auto_thresholds(
        xs_config_t* cfg,
        const uint8_t bpp,
        const xs_data_in_t th1,
        const xs_data_in_t th2
    )

    char* xs_get_version_str()

    int* xs_get_version()
