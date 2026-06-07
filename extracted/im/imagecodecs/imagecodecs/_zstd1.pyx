# imagecodecs/_zstd1.pyx
# distutils: language = c
# cython: boundscheck = False
# cython: wraparound = False
# cython: cdivision = True
# cython: nonecheck = False
# cython: freethreading_compatible = True

# Copyright (c) 2018-2026, Christoph Gohlke
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""ZSTD1 (Zeiss ZStandard) codec for the imagecodecs package.

ZSTD1 is the Zeiss CZI compression type 6. It wraps a standard Zstd frame
with a small proprietary header and an optional hi/lo byte-shuffle step:

    data[0]               : header_size (uint8, includes itself, min 1)
    data[1..header_size-1]: typed chunks
      chunk type 1        : 1-byte payload; bit 0 = hi/lo shuffle flag
      unknown chunk type  : stop parsing (forward-compatible)
    data[header_size..]   : standard Zstd-compressed frame

"""

include '_shared.pxi'

from zstd cimport *


class ZSTD1:
    """ZSTD1 codec constants."""

    available = True


class Zstd1Error(RuntimeError):
    """ZSTD1 codec exceptions."""

    def __init__(self, func, msg='', err=0):
        cdef:
            const char* errmsg

        if msg:
            msg = f'{func} returned {msg!r}'
        else:
            errmsg = ZSTD_getErrorName(err)
            msg = f'{func} returned {errmsg.decode()!r}'
        super().__init__(msg)


def zstd1_version():
    """Return Zstandard library version string."""
    return 'zstd {}.{}.{}'.format(
        ZSTD_VERSION_MAJOR, ZSTD_VERSION_MINOR, ZSTD_VERSION_RELEASE
    )


def zstd1_check(const uint8_t[::1] data, /):
    """Return whether data is ZSTD1 encoded or None if unknown."""
    cdef:
        ssize_t srcsize = data.nbytes
        uint8_t header_size

    if srcsize < 2:
        return False
    header_size = data[0]
    if header_size < 1 or <ssize_t> header_size >= srcsize:
        return False
    if srcsize - header_size < 4:
        return False
    return bytes(data[header_size:header_size + 4]) == b'\x28\xB5\x2F\xFD'


def zstd1_encode(
    data,
    /,
    level=None,
    *,
    ssize_t itemsize=1,
    hilo=False,
    out=None,
):
    """Return ZSTD1 encoded data."""
    cdef:
        const uint8_t[::1] src = _readable_input(data)
        const uint8_t[::1] dst
        uint8_t* dstptr
        uint8_t* tmpptr
        ssize_t srcsize = src.nbytes
        ssize_t dstsize, hdr_len, items, i, j
        int clevel = 0 if level is None else level
        bint do_hilo = hilo and itemsize > 1
        size_t ret

    if itemsize < 1:
        raise ValueError(f'{itemsize=} < 1')

    if do_hilo and srcsize % itemsize != 0:
        raise ValueError('data size not a multiple of itemsize')

    # header: 1 byte (no chunks) or 3 bytes (type-1 chunk with hilo flag)
    hdr_len = 3 if do_hilo else 1

    out, dstsize, outgiven, outtype = _parse_output(out)

    if out is None:
        if dstsize < 0:
            dstsize = hdr_len + <ssize_t> ZSTD_compressBound(<size_t> srcsize)
            if dstsize <= hdr_len:
                raise Zstd1Error('ZSTD_compressBound', 'input too large')
        if dstsize < hdr_len + 64:
            dstsize = hdr_len + 64
        out = _create_output(outtype, dstsize)

    dst = out
    dstsize = dst.nbytes

    with nogil:
        dstptr = <uint8_t*> &dst[0]
        dstptr[0] = <uint8_t> hdr_len  # header_size includes itself
        if do_hilo:
            dstptr[1] = 1  # chunk type 1
            dstptr[2] = 1  # payload: hilo flag set
            items = srcsize // itemsize
            tmpptr = <uint8_t*> malloc(<size_t> srcsize)
            if tmpptr == NULL:
                raise MemoryError('zstd1_encode malloc failed')
            for j in range(itemsize):
                for i in range(items):
                    tmpptr[j * items + i] = src[i * itemsize + j]
            ret = ZSTD_compress(
                <void*> (dstptr + hdr_len),
                <size_t> (dstsize - hdr_len),
                <void*> tmpptr,
                <size_t> srcsize,
                clevel,
            )
            free(tmpptr)
        else:
            ret = ZSTD_compress(
                <void*> (dstptr + hdr_len),
                <size_t> (dstsize - hdr_len),
                <void*> &src[0],
                <size_t> srcsize,
                clevel,
            )
        if ZSTD_isError(ret):
            raise Zstd1Error('ZSTD_compress', err=ret)
        ret += <size_t> hdr_len

    del dst
    return _return_output(out, dstsize, ret, outgiven)


def zstd1_decode(
    data,
    /,
    *,
    ssize_t itemsize=1,
    ssize_t samples=1,
    out=None,
):
    """Return decoded ZSTD1 data.

    Also accepts plain Zstd streams (magic bytes 0x28B52FFD).
    """
    cdef:
        const uint8_t[::1] src = _readable_input(data)
        const uint8_t[::1] dst  # must be const to write to bytes
        ssize_t srcsize = src.nbytes
        ssize_t dstsize, hdr_pos, items
        uint64_t cntsize
        uint8_t header_size, chunk_type
        bint hilo = False
        size_t ret

    if data is out:
        raise ValueError('cannot decode in-place')

    if srcsize < 2:
        raise ValueError(f'{srcsize=} < 2')

    if itemsize < 1:
        raise ValueError(f'{itemsize=} < 1')

    if samples not in {1, 3, 4}:
        raise ValueError(f'{samples=} not in {{1, 3, 4}}')

    if (
        srcsize >= 4
        and src[0] == 0x28
        and src[1] == 0xB5
        and src[2] == 0x2F
        and src[3] == 0xFD
    ):
        # plain Zstd stream: no ZSTD1 header, no hilo shuffle
        header_size = 0
    else:
        header_size = src[0]
        if header_size < 1:
            raise ValueError(f'{header_size=} < 1')
        if <ssize_t> header_size >= srcsize:
            raise ValueError(f'{header_size=} >= {srcsize=}')

        # parse typed chunks in bytes [1 .. header_size-1]
        hdr_pos = 1
        while hdr_pos < header_size:
            chunk_type = src[hdr_pos]
            hdr_pos += 1
            if chunk_type == 1:
                if hdr_pos >= header_size:
                    raise ValueError('truncated chunk type 1')
                hilo = (src[hdr_pos] & 1) != 0
                hdr_pos += 1
            else:
                break  # unknown chunk type; forward-compatible stop

    out, dstsize, outgiven, outtype = _parse_output(out)

    # compressed frame starts at src[header_size]
    if out is None:
        if dstsize < 0:
            cntsize = _zstd1_content_size(
                <uint8_t*> &src[header_size],
                <size_t> (srcsize - header_size),
            )
            if cntsize == ZSTD_CONTENTSIZE_ERROR:
                raise Zstd1Error('ZSTD_getFrameContentSize', f'{cntsize}')
            if cntsize == ZSTD_CONTENTSIZE_UNKNOWN or cntsize > SIZE_MAX >> 1:
                # use streaming API for unknown or suspiciously large sizes
                return _zstd1_decode_stream(
                    src, header_size, itemsize, samples, hilo, outtype
                )
            dstsize = <ssize_t> cntsize
        out = _create_output(outtype, dstsize)

    dst = out
    dstsize = dst.nbytes

    with nogil:
        ret = ZSTD_decompress(
            <void*> &dst[0],
            <size_t> dstsize,
            <void*> &src[header_size],
            <size_t> (srcsize - header_size),
        )
        if ZSTD_isError(ret):
            raise Zstd1Error('ZSTD_decompress', err=ret)

        if hilo and itemsize > 1:
            items = <ssize_t> ret // itemsize
            if items * itemsize != <ssize_t> ret:
                raise ValueError(
                    'decompressed size not a multiple of itemsize'
                )
            if _zstd1_hilo_unshuffle(<uint8_t*> &dst[0], items, itemsize) < 0:
                raise MemoryError('zstd1_decode malloc failed')

        if samples == 3 or samples == 4:
            items = <ssize_t> ret // (samples * itemsize)
            if items * samples * itemsize != <ssize_t> ret:
                raise ValueError(
                    'decompressed size not a multiple of samples*itemsize'
                )
            _zstd1_bgr_swap(<uint8_t*> &dst[0], items, samples, itemsize)

    del dst
    return _return_output(out, dstsize, ret, outgiven)


cdef _zstd1_decode_stream(
    const uint8_t[::1] src,
    ssize_t header_offset,
    ssize_t itemsize,
    ssize_t samples,
    bint hilo,
    outtype,
):
    """Decompress ZSTD1 using streaming API, then optionally unshuffle."""
    cdef:
        output_t* output = NULL
        ZSTD_DCtx* dctx = NULL
        ZSTD_inBuffer zinput
        ZSTD_outBuffer zoutput
        ssize_t size, items
        size_t srcsize = <size_t> (src.nbytes - header_offset)
        size_t outsize = ZSTD_DStreamOutSize()
        size_t incsize = max((srcsize // outsize) * outsize // 2, outsize)
        size_t ret

    try:
        with nogil:
            dctx = ZSTD_createDCtx()
            if dctx == NULL:
                raise Zstd1Error('ZSTD_createDCtx', 'NULL')

            output = output_new(NULL, incsize * 3)
            if output == NULL:
                raise MemoryError('output_new failed')

            zoutput.dst = <void*> output.data
            zoutput.size = <size_t> output.size
            zoutput.pos = output.pos

            zinput.src = <void*> &src[header_offset]
            zinput.size = srcsize
            zinput.pos = 0

            while zinput.pos < zinput.size:
                if output.size - output.used < outsize:
                    ret = output_resize(output, output.used + incsize)
                    if ret == 0:
                        raise MemoryError('output_resize failed')
                    zoutput.dst = <void*> output.data
                    zoutput.size = <size_t> output.size
                    zoutput.pos = output.pos

                ret = ZSTD_decompressStream(dctx, &zoutput, &zinput)
                if ZSTD_isError(ret):
                    raise Zstd1Error('ZSTD_decompressStream', err=ret)

                # output.pos = zoutput.pos
                output.used = zoutput.pos

            if hilo and itemsize > 1:
                size = <ssize_t> output.pos
                items = size // itemsize
                if items * itemsize != size:
                    raise ValueError(
                        'decompressed size not a multiple of itemsize'
                    )
                if _zstd1_hilo_unshuffle(output.data, items, itemsize) < 0:
                    raise MemoryError('zstd1_decode malloc failed')

            if samples == 3 or samples == 4:
                size = <ssize_t> output.pos
                items = size // (samples * itemsize)
                if items * samples * itemsize != size:
                    raise ValueError(
                        'decompressed size not a multiple of samples*itemsize'
                    )
                _zstd1_bgr_swap(output.data, items, samples, itemsize)

        out = _create_output(outtype, output.pos, <const char*> output.data)

    finally:
        output_del(output)
        ZSTD_freeDCtx(dctx)

    return out


cdef uint64_t _zstd1_content_size(
    const uint8_t* src,
    const size_t srcsize,
) noexcept nogil:
    """Return uncompressed size of all frames in buffer."""
    cdef:
        uint64_t frame_content_size
        size_t frame_compressed_size
        size_t offset = 0
        uint64_t dstsize = 0

    while offset < srcsize:
        frame_compressed_size = ZSTD_findFrameCompressedSize(
            <const void*> (src + offset), srcsize - offset
        )
        if ZSTD_isError(frame_compressed_size):
            return ZSTD_CONTENTSIZE_ERROR  # frame_compressed_size

        frame_content_size = ZSTD_getFrameContentSize(
            <const void*> (src + offset), frame_compressed_size
        )
        if (
            frame_content_size == ZSTD_CONTENTSIZE_ERROR
            or frame_content_size == ZSTD_CONTENTSIZE_UNKNOWN
        ):
            return frame_content_size

        dstsize += frame_content_size
        offset += frame_compressed_size

    return dstsize


cdef int _zstd1_hilo_unshuffle(
    uint8_t* data,
    ssize_t items,
    ssize_t itemsize,
) noexcept nogil:
    """Unshuffle hi/lo bytes in-place. Return 0 on success, -1 on failure."""
    cdef:
        uint8_t* tmp = <uint8_t*> malloc(<size_t> (items * itemsize))
        ssize_t i, j

    if tmp == NULL:
        return -1
    for j in range(itemsize):
        for i in range(items):
            tmp[i * itemsize + j] = data[j * items + i]
    memcpy(<void*> data, <void*> tmp, <size_t> (items * itemsize))
    free(tmp)
    return 0


cdef void _zstd1_bgr_swap(
    uint8_t* data,
    ssize_t items,
    ssize_t samples,
    ssize_t itemsize,
) noexcept nogil:
    """Swap channel 0, 2 in-place (BGR->RGB) and force alpha=255 for BGRA32."""
    cdef:
        ssize_t stride = samples * itemsize
        ssize_t i, j
        uint8_t  tmp_u8
        uint16_t tmp_u16
        uint32_t tmp_u32
        uint64_t tmp_u64
        uint16_t* p16
        uint32_t* p32
        uint64_t* p64

    if itemsize == 1:
        for i in range(items):
            tmp_u8 = data[i * stride]
            data[i * stride] = data[i * stride + 2]
            data[i * stride + 2] = tmp_u8
        if samples == 4:
            for i in range(items):
                data[i * stride + 3] = 0xFF
    elif itemsize == 2:
        for i in range(items):
            p16 = <uint16_t*> (data + i * stride)
            tmp_u16 = p16[0]
            p16[0] = p16[2]
            p16[2] = tmp_u16
    elif itemsize == 4:
        for i in range(items):
            p32 = <uint32_t*> (data + i * stride)
            tmp_u32 = p32[0]
            p32[0] = p32[2]
            p32[2] = tmp_u32
    elif itemsize == 8:
        for i in range(items):
            p64 = <uint64_t*> (data + i * stride)
            tmp_u64 = p64[0]
            p64[0] = p64[2]
            p64[2] = tmp_u64
    else:
        for i in range(items):
            for j in range(itemsize):
                tmp_u8 = data[i * stride + j]
                data[i * stride + j] = data[i * stride + 2 * itemsize + j]
                data[i * stride + 2 * itemsize + j] = tmp_u8


# Output Stream ###############################################################

ctypedef struct output_t:
    uint8_t* data
    size_t size
    size_t pos
    size_t used
    int owner


cdef output_t* output_new(uint8_t* data, size_t size) noexcept nogil:
    """Return new output."""
    cdef:
        output_t* output = <output_t*> calloc(1, sizeof(output_t))

    if output == NULL:
        return NULL
    output.size = size
    output.used = 0
    output.pos = 0
    if data == NULL:
        output.owner = 1
        output.data = <uint8_t*> malloc(size)
    else:
        output.owner = 0
        output.data = data
    if output.data == NULL:
        free(output)
        return NULL
    return output


cdef void output_del(output_t* output) noexcept nogil:
    """Free output."""
    if output != NULL:
        if output.owner != 0:
            free(output.data)
        free(output)


cdef int output_resize(output_t* output, size_t newsize) noexcept nogil:
    """Resize output."""
    cdef:
        uint8_t* tmp

    if output == NULL or newsize == 0 or output.used > output.size:
        return 0
    if newsize == output.size or output.owner == 0:
        return 1

    tmp = <uint8_t*> realloc(<void*> output.data, newsize)
    if tmp == NULL:
        return 0
    output.data = tmp
    output.size = newsize
    return 1
