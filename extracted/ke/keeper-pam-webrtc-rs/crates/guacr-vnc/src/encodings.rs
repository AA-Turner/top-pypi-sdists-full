// VNC encoding decoders: ZRLE, Hextile, RRE
//
// ZRLE (T-013 to T-015): zlib-compressed tile-based RLE encoding.
//   The zlib stream is continuous across FBU messages within a session —
//   `ZrleState` must be kept per-session and threaded in.
//
// Hextile (T-016 to T-017): 16x16-tile encoding with subencoding flags.
//   Background/foreground colors persist across tiles within one rectangle.
//
// RRE (T-018 to T-019): background pixel + list of colored subrectangles.
//
// Unrecognized encodings (T-020 to T-022): terminate the connection.
//
// Status: decoders are complete and tested but not yet wired into the VNC
// handler (which currently proxies raw RFB). Wire-up is the next step.
#![allow(dead_code)]

use flate2::Decompress;
use log::warn;

// ============================================================================
// ZRLE
// ============================================================================

/// Per-session zlib state for ZRLE decoding.
///
/// The ZRLE specification (RFB protocol §6.6) requires that the zlib
/// decompression stream is continuous across all FBU messages in a
/// session. This struct owns the `flate2::Decompress` context.
pub struct ZrleState {
    decompress: Decompress,
    /// Scratch buffer to avoid per-call allocation.
    decompress_buf: Vec<u8>,
}

impl ZrleState {
    pub fn new() -> Self {
        Self {
            // TigerVNC sends zlib RFC 1950 (with 0x78 header). The original "incorrect
            // header check" error was a symptom of TCP-fragmented data being passed
            // mid-stream; the streaming read_exact reader fixes that root cause.
            decompress: Decompress::new(true),
            decompress_buf: Vec::with_capacity(64 * 1024),
        }
    }

    /// Decompress `compressed` bytes into a freshly returned Vec.
    /// Returns `Err` if zlib fails; the caller should terminate the connection.
    pub fn decompress(&mut self, compressed: &[u8], max_out: usize) -> Result<Vec<u8>, String> {
        if !compressed.is_empty() {
            log::debug!(
                "ZRLE: decompressing {} bytes, first byte = 0x{:02x}",
                compressed.len(),
                compressed[0]
            );
        }

        self.decompress_buf.clear();
        self.decompress_buf.resize(max_out, 0u8);

        let before_in = self.decompress.total_in();
        let before_out = self.decompress.total_out();

        let status = self
            .decompress
            .decompress(
                compressed,
                &mut self.decompress_buf,
                flate2::FlushDecompress::Sync,
            )
            .map_err(|e| format!("ZRLE: zlib decompress error: {e}"))?;

        let consumed_in = (self.decompress.total_in() - before_in) as usize;
        let produced_out = (self.decompress.total_out() - before_out) as usize;

        if consumed_in < compressed.len() && status != flate2::Status::BufError {
            // Extra compressed bytes — not necessarily an error (zlib may buffer).
        }

        Ok(self.decompress_buf[..produced_out].to_vec())
    }
}

impl Default for ZrleState {
    fn default() -> Self {
        Self::new()
    }
}

/// Decode a ZRLE-encoded rectangle (T-013, T-014, T-015).
///
/// `compressed_data`: raw zlib bytes (length field already consumed by caller).
/// `width`, `height`: rectangle dimensions in pixels.
/// `state`: per-session ZRLE decompressor.
///
/// Returns RGB-24 pixel data (3 bytes per pixel, row-major).
pub fn decode_zrle(
    compressed_data: &[u8],
    width: u16,
    height: u16,
    state: &mut ZrleState,
) -> Result<Vec<u8>, String> {
    // Upper bound for decompressed output.
    // Each 64x64 tile: 1 byte subencoding + up to 64*64*3 = 12288 bytes.
    let tile_cols = width.div_ceil(64) as usize;
    let tile_rows = height.div_ceil(64) as usize;
    let max_out = (tile_cols * tile_rows) * (1 + 64 * 64 * 4);

    // AC-4: corrupted zlib data → error, not panic.
    let decompressed = state.decompress(compressed_data, max_out)?;

    let w = width as usize;
    let h = height as usize;

    // Output: RGB-24 pixels.
    let mut out = vec![0u8; w * h * 3];

    let mut pos = 0usize;

    // Walk 64x64 tiles left-to-right, top-to-bottom.
    for ty in (0..h).step_by(64) {
        for tx in (0..w).step_by(64) {
            let tw = (w - tx).min(64);
            let th = (h - ty).min(64);

            if pos >= decompressed.len() {
                return Err(format!("ZRLE: truncated stream at tile ({tx},{ty})"));
            }

            let subenc = decompressed[pos];
            pos += 1;

            match subenc {
                // AC-3: subencoding 0 — raw tile (no RLE).
                0 => {
                    let needed = tw * th * 3;
                    if pos + needed > decompressed.len() {
                        return Err(format!(
                            "ZRLE subenc 0: need {needed} bytes but only {} remain",
                            decompressed.len() - pos
                        ));
                    }
                    for row in 0..th {
                        let src_off = pos + row * tw * 3;
                        let dst_row = ty + row;
                        let dst_off = (dst_row * w + tx) * 3;
                        out[dst_off..dst_off + tw * 3]
                            .copy_from_slice(&decompressed[src_off..src_off + tw * 3]);
                    }
                    pos += needed;
                }

                // AC-3: subencoding 1 — solid fill (palette size 1).
                1 => {
                    if pos + 3 > decompressed.len() {
                        return Err("ZRLE subenc 1: truncated solid pixel".to_string());
                    }
                    let r = decompressed[pos];
                    let g = decompressed[pos + 1];
                    let b = decompressed[pos + 2];
                    pos += 3;
                    for row in 0..th {
                        for col in 0..tw {
                            let dst_off = ((ty + row) * w + (tx + col)) * 3;
                            out[dst_off] = r;
                            out[dst_off + 1] = g;
                            out[dst_off + 2] = b;
                        }
                    }
                }

                // AC-3: subencodings 2-16 — packed palette.
                n @ 2..=16 => {
                    let palette_size = n as usize;
                    let needed = palette_size * 3;
                    if pos + needed > decompressed.len() {
                        return Err(format!("ZRLE subenc {n}: need {needed} bytes for palette"));
                    }
                    let palette: Vec<(u8, u8, u8)> = (0..palette_size)
                        .map(|i| {
                            let o = pos + i * 3;
                            (decompressed[o], decompressed[o + 1], decompressed[o + 2])
                        })
                        .collect();
                    pos += needed;

                    // Bits per pixel index (ceiling of log2(palette_size)).
                    let bpp = if palette_size <= 2 {
                        1
                    } else if palette_size <= 4 {
                        2
                    } else {
                        4
                    };
                    let pixels_per_byte = 8 / bpp;
                    let row_bytes = tw.div_ceil(pixels_per_byte);

                    for row in 0..th {
                        if pos + row_bytes > decompressed.len() {
                            return Err(format!("ZRLE subenc {n}: truncated row {row}"));
                        }
                        let mut bit_pos = 0usize;
                        for col in 0..tw {
                            let byte_idx = bit_pos / 8;
                            let bit_shift = bit_pos % 8;
                            let byte = decompressed[pos + byte_idx];
                            let mask = (1u8 << bpp) - 1;
                            let idx = ((byte >> (8 - bpp - bit_shift)) & mask) as usize;
                            let (r, g, b) = palette.get(idx).copied().unwrap_or((0, 0, 0));
                            let dst_off = ((ty + row) * w + (tx + col)) * 3;
                            out[dst_off] = r;
                            out[dst_off + 1] = g;
                            out[dst_off + 2] = b;
                            bit_pos += bpp;
                        }
                        pos += row_bytes;
                    }
                }

                // AC-3: subencodings 17-127 — unused/reserved; treat as error.
                17..=127 => {
                    return Err(format!("ZRLE: reserved subencoding {subenc}"));
                }

                // AC-3: subencoding 128 — plain RLE.
                128 => {
                    let total_pixels = tw * th;
                    let mut written = 0usize;
                    while written < total_pixels {
                        if pos + 3 > decompressed.len() {
                            return Err("ZRLE subenc 128: truncated RLE pixel".to_string());
                        }
                        let r = decompressed[pos];
                        let g = decompressed[pos + 1];
                        let b = decompressed[pos + 2];
                        pos += 3;

                        // Run length: 1 or more bytes, each < 255 continues the run.
                        let mut run = 1usize;
                        loop {
                            if pos >= decompressed.len() {
                                return Err("ZRLE subenc 128: truncated RLE length".to_string());
                            }
                            let v = decompressed[pos] as usize;
                            pos += 1;
                            run += v;
                            if v < 255 {
                                break;
                            }
                        }

                        for _ in 0..run {
                            if written >= total_pixels {
                                break;
                            }
                            let px = written % tw;
                            let py = written / tw;
                            let dst_off = ((ty + py) * w + (tx + px)) * 3;
                            if dst_off + 3 <= out.len() {
                                out[dst_off] = r;
                                out[dst_off + 1] = g;
                                out[dst_off + 2] = b;
                            }
                            written += 1;
                        }
                    }
                }

                // AC-3: subencodings 129-255 — palette RLE with 2-127 palette entries.
                n @ 129..=255 => {
                    let palette_size = (n - 128) as usize;
                    let needed = palette_size * 3;
                    if pos + needed > decompressed.len() {
                        return Err(format!(
                            "ZRLE subenc {n}: need {needed} bytes for palette RLE"
                        ));
                    }
                    let palette: Vec<(u8, u8, u8)> = (0..palette_size)
                        .map(|i| {
                            let o = pos + i * 3;
                            (decompressed[o], decompressed[o + 1], decompressed[o + 2])
                        })
                        .collect();
                    pos += needed;

                    let total_pixels = tw * th;
                    let mut written = 0usize;
                    while written < total_pixels {
                        if pos >= decompressed.len() {
                            return Err(format!("ZRLE subenc {n}: truncated palette RLE"));
                        }
                        let idx_byte = decompressed[pos];
                        pos += 1;

                        if idx_byte & 0x80 == 0 {
                            // Single pixel (run length = 1, MSB = 0).
                            let idx = idx_byte as usize;
                            let (r, g, b) = palette.get(idx).copied().unwrap_or((0, 0, 0));
                            let px = written % tw;
                            let py = written / tw;
                            let dst_off = ((ty + py) * w + (tx + px)) * 3;
                            if dst_off + 3 <= out.len() {
                                out[dst_off] = r;
                                out[dst_off + 1] = g;
                                out[dst_off + 2] = b;
                            }
                            written += 1;
                        } else {
                            // Run: MSB = 1, lower 7 bits = palette index.
                            let idx = (idx_byte & 0x7F) as usize;
                            let (r, g, b) = palette.get(idx).copied().unwrap_or((0, 0, 0));
                            // Run length: 1 or more following bytes.
                            let mut run = 1usize;
                            loop {
                                if pos >= decompressed.len() {
                                    return Err(format!("ZRLE subenc {n}: truncated run length"));
                                }
                                let v = decompressed[pos] as usize;
                                pos += 1;
                                run += v;
                                if v < 255 {
                                    break;
                                }
                            }
                            for _ in 0..run {
                                if written >= total_pixels {
                                    break;
                                }
                                let px = written % tw;
                                let py = written / tw;
                                let dst_off = ((ty + py) * w + (tx + px)) * 3;
                                if dst_off + 3 <= out.len() {
                                    out[dst_off] = r;
                                    out[dst_off + 1] = g;
                                    out[dst_off + 2] = b;
                                }
                                written += 1;
                            }
                        }
                    }
                }
            }
        }
    }

    Ok(out)
}

// ============================================================================
// Hextile
// ============================================================================

/// Decode a Hextile-encoded rectangle from a stream slice (T-016, T-017).
///
/// Returns `(rgb_pixels, bytes_consumed)`.
/// Used by the buffer parser which doesn't know the Hextile payload length upfront.
/// Errors on truncated stream (AC-3 of vnc-codecs R2).
pub fn decode_hextile_from_stream(
    data: &[u8],
    width: u16,
    height: u16,
) -> Result<(Vec<u8>, usize), String> {
    let (pixels, consumed) = decode_hextile_internal(data, width, height)?;
    Ok((pixels, consumed))
}

/// Decode a Hextile-encoded rectangle (T-016, T-017).
///
/// Returns RGB-24 pixel data (3 bytes per pixel, row-major).
/// Errors on truncated stream (AC-3 of vnc-codecs R2).
pub fn decode_hextile(data: &[u8], width: u16, height: u16) -> Result<Vec<u8>, String> {
    let (pixels, _consumed) = decode_hextile_internal(data, width, height)?;
    Ok(pixels)
}

fn decode_hextile_internal(
    data: &[u8],
    width: u16,
    height: u16,
) -> Result<(Vec<u8>, usize), String> {
    let w = width as usize;
    let h = height as usize;
    let mut out = vec![0u8; w * h * 3];
    let mut pos = 0usize;

    // Background and foreground colors persist across tiles within this rectangle.
    let mut bg = (0u8, 0u8, 0u8);
    let mut fg = (0u8, 0u8, 0u8);

    for ty in (0..h).step_by(16) {
        for tx in (0..w).step_by(16) {
            let tw = (w - tx).min(16);
            let th = (h - ty).min(16);

            if pos >= data.len() {
                return Err(format!("Hextile: truncated at tile ({tx},{ty})"));
            }

            let subenc = data[pos];
            pos += 1;

            // Subencoding flags (AC-2):
            const RAW: u8 = 0x01;
            const BACKGROUND_SPECIFIED: u8 = 0x02;
            const FOREGROUND_SPECIFIED: u8 = 0x04;
            const ANY_SUBRECTS: u8 = 0x08;
            const SUBRECTS_COLOURED: u8 = 0x10;

            if subenc & RAW != 0 {
                // Raw tile: tw*th*3 bytes of RGB.
                let needed = tw * th * 3;
                if pos + needed > data.len() {
                    return Err(format!(
                        "Hextile raw tile ({tx},{ty}): need {needed}, have {}",
                        data.len() - pos
                    ));
                }
                for row in 0..th {
                    let src_off = pos + row * tw * 3;
                    let dst_off = ((ty + row) * w + tx) * 3;
                    out[dst_off..dst_off + tw * 3]
                        .copy_from_slice(&data[src_off..src_off + tw * 3]);
                }
                pos += needed;
                // Update bg to match first pixel of raw tile (per spec suggestion).
                bg = (
                    out[(ty * w + tx) * 3],
                    out[(ty * w + tx) * 3 + 1],
                    out[(ty * w + tx) * 3 + 2],
                );
                continue;
            }

            if subenc & BACKGROUND_SPECIFIED != 0 {
                if pos + 3 > data.len() {
                    return Err(format!(
                        "Hextile: truncated background pixel at ({tx},{ty})"
                    ));
                }
                bg = (data[pos], data[pos + 1], data[pos + 2]);
                pos += 3;
            }

            if subenc & FOREGROUND_SPECIFIED != 0 {
                if pos + 3 > data.len() {
                    return Err(format!(
                        "Hextile: truncated foreground pixel at ({tx},{ty})"
                    ));
                }
                fg = (data[pos], data[pos + 1], data[pos + 2]);
                pos += 3;
            }

            // Fill tile with background color.
            for row in 0..th {
                for col in 0..tw {
                    let dst_off = ((ty + row) * w + (tx + col)) * 3;
                    out[dst_off] = bg.0;
                    out[dst_off + 1] = bg.1;
                    out[dst_off + 2] = bg.2;
                }
            }

            if subenc & ANY_SUBRECTS == 0 {
                continue;
            }

            if pos >= data.len() {
                return Err(format!("Hextile: missing subrect count at ({tx},{ty})"));
            }
            let num_subrects = data[pos] as usize;
            pos += 1;

            for _ in 0..num_subrects {
                let subrect_colored = subenc & SUBRECTS_COLOURED != 0;
                let needed = if subrect_colored { 5 } else { 2 };
                if pos + needed > data.len() {
                    return Err(format!("Hextile: truncated subrect at ({tx},{ty})"));
                }

                let (r, g, b) = if subrect_colored {
                    let c = (data[pos], data[pos + 1], data[pos + 2]);
                    pos += 3;
                    c
                } else {
                    fg
                };

                let xy = data[pos];
                let wh = data[pos + 1];
                pos += 2;

                let sx = ((xy >> 4) & 0xF) as usize;
                let sy = (xy & 0xF) as usize;
                let sw = ((wh >> 4) & 0xF) as usize + 1;
                let sh = (wh & 0xF) as usize + 1;

                for row in 0..sh {
                    for col in 0..sw {
                        let px = tx + sx + col;
                        let py = ty + sy + row;
                        if px < w && py < h {
                            let dst_off = (py * w + px) * 3;
                            out[dst_off] = r;
                            out[dst_off + 1] = g;
                            out[dst_off + 2] = b;
                        }
                    }
                }
            }
        }
    }

    Ok((out, pos))
}

// ============================================================================
// RRE
// ============================================================================

/// Decode an RRE-encoded rectangle (T-018, T-019).
///
/// Returns RGB-24 pixel data (3 bytes per pixel, row-major).
pub fn decode_rre(data: &[u8], width: u16, height: u16) -> Result<Vec<u8>, String> {
    // Minimum: 4-byte count + 3-byte background pixel.
    if data.len() < 7 {
        return Err("RRE: payload too short (need at least 7 bytes)".to_string());
    }

    let num_subrects = u32::from_be_bytes([data[0], data[1], data[2], data[3]]) as usize;
    let bg_r = data[4];
    let bg_g = data[5];
    let bg_b = data[6];
    let mut pos = 7usize;

    let w = width as usize;
    let h = height as usize;

    // AC-2: validate subrectangle count before allocating.
    // Each subrect is 11 bytes (3 color + 2 x + 2 y + 2 w + 2 h).
    let subrect_bytes = num_subrects
        .checked_mul(11)
        .ok_or_else(|| "RRE: subrect count overflow".to_string())?;
    if pos + subrect_bytes > data.len() {
        return Err(format!(
            "RRE: declared {num_subrects} subrects ({subrect_bytes} bytes) \
             but only {} bytes remain",
            data.len() - pos
        ));
    }

    let mut out = vec![0u8; w * h * 3];

    // Fill with background color.
    for row in 0..h {
        for col in 0..w {
            let dst_off = (row * w + col) * 3;
            out[dst_off] = bg_r;
            out[dst_off + 1] = bg_g;
            out[dst_off + 2] = bg_b;
        }
    }

    // Apply subrectangles.
    for _ in 0..num_subrects {
        if pos + 11 > data.len() {
            return Err("RRE: truncated subrectangle data".to_string());
        }
        let r = data[pos];
        let g = data[pos + 1];
        let b = data[pos + 2];
        let sx = u16::from_be_bytes([data[pos + 3], data[pos + 4]]) as usize;
        let sy = u16::from_be_bytes([data[pos + 5], data[pos + 6]]) as usize;
        let sw = u16::from_be_bytes([data[pos + 7], data[pos + 8]]) as usize;
        let sh = u16::from_be_bytes([data[pos + 9], data[pos + 10]]) as usize;
        pos += 11;

        for row in 0..sh {
            for col in 0..sw {
                let px = sx + col;
                let py = sy + row;
                if px < w && py < h {
                    let dst_off = (py * w + px) * 3;
                    out[dst_off] = r;
                    out[dst_off + 1] = g;
                    out[dst_off + 2] = b;
                }
            }
        }
    }

    Ok(out)
}

// ============================================================================
// Unrecognized encoding handler (T-020, T-022)
// ============================================================================

/// Called when an unrecognized VNC encoding type is encountered.
///
/// Logs a warning (AC-3) and returns an error so the caller can terminate
/// the connection (AC-1). Stream desync is prevented by disconnecting (AC-2).
pub fn unrecognized_encoding(encoding: i32) -> String {
    warn!(
        "VNC: unrecognized encoding type {} — terminating connection to prevent stream desync",
        encoding
    );
    format!("VNC: unrecognized encoding {encoding}")
}

// ============================================================================
// Tests (T-021)
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    // --- RRE tests (T-018, T-019) ---

    #[test]
    fn test_rre_solid_background_no_subrects() {
        // 2×2 rectangle, 0 subrects, background = (10, 20, 30).
        let data = [
            0, 0, 0, 0, // num_subrects = 0
            10, 20, 30, // background
        ];
        let out = decode_rre(&data, 2, 2).unwrap();
        assert_eq!(out.len(), 2 * 2 * 3);
        // All pixels should be background color.
        for i in (0..out.len()).step_by(3) {
            assert_eq!((out[i], out[i + 1], out[i + 2]), (10, 20, 30));
        }
    }

    #[test]
    fn test_rre_with_subrect() {
        // 4×4 rectangle, 1 subrect at (1,1) 2×2 painted (255,0,0).
        let mut data = vec![
            0, 0, 0, 1, // num_subrects = 1
            0, 0, 0, // background = black
        ];
        // Subrect: color(3) + x(2) + y(2) + w(2) + h(2)
        data.extend_from_slice(&[255, 0, 0]); // red
        data.extend_from_slice(&[0, 1]); // x=1
        data.extend_from_slice(&[0, 1]); // y=1
        data.extend_from_slice(&[0, 2]); // w=2
        data.extend_from_slice(&[0, 2]); // h=2

        let out = decode_rre(&data, 4, 4).unwrap();
        assert_eq!(out.len(), 4 * 4 * 3);

        // Pixel at (1,1) should be red.
        let off = (4 + 1) * 3;
        assert_eq!((out[off], out[off + 1], out[off + 2]), (255, 0, 0));

        // Pixel at (0,0) should be black.
        assert_eq!((out[0], out[1], out[2]), (0, 0, 0));
    }

    #[test]
    fn test_rre_subrect_count_overflow() {
        // AC-2: num_subrects claims more data than is present → error.
        let data = [
            0, 0, 0, 100, // 100 subrects
            255, 255, 255, // background
                 // No actual subrect data.
        ];
        let result = decode_rre(&data, 4, 4);
        assert!(result.is_err(), "expected error for truncated subrect data");
    }

    // --- Hextile tests (T-016, T-017) ---

    #[test]
    fn test_hextile_background_specified_only() {
        // A single 2×2 tile with BackgroundSpecified flag only (no subrects).
        // subencoding = 0x02 (BackgroundSpecified)
        let data = [0x02u8, 100, 150, 200]; // flag + RGB background
        let out = decode_hextile(&data, 2, 2).unwrap();
        assert_eq!(out.len(), 2 * 2 * 3);
        for i in (0..out.len()).step_by(3) {
            assert_eq!((out[i], out[i + 1], out[i + 2]), (100, 150, 200));
        }
    }

    #[test]
    fn test_hextile_raw_tile() {
        // A 2×2 tile with Raw flag.
        let mut data = vec![0x01u8]; // RAW flag
                                     // 4 pixels × 3 bytes = 12 bytes, alternating red/blue.
        data.extend_from_slice(&[255, 0, 0, 0, 0, 255, 255, 0, 0, 0, 0, 255]);
        let out = decode_hextile(&data, 2, 2).unwrap();
        assert_eq!(out.len(), 2 * 2 * 3);
        assert_eq!((out[0], out[1], out[2]), (255, 0, 0)); // top-left = red
        assert_eq!((out[3], out[4], out[5]), (0, 0, 255)); // top-right = blue
    }

    #[test]
    fn test_hextile_truncated_returns_error() {
        // AC-3: truncated stream → error, not partial render.
        let data = [0x01u8, 100, 150]; // RAW flag but only 3 bytes instead of 12 for 2×2
        let result = decode_hextile(&data, 2, 2);
        assert!(
            result.is_err(),
            "expected error for truncated Hextile stream"
        );
    }

    // --- Unrecognized encoding test (T-021) ---

    #[test]
    fn test_unrecognized_encoding_returns_error_string() {
        // AC-1, AC-3: must return an error string and log a warning.
        let msg = unrecognized_encoding(99);
        assert!(msg.contains("99"), "error must identify the encoding type");
    }

    // --- ZRLE solid fill test (T-013) ---

    #[test]
    fn test_zrle_solid_fill_tile() {
        // Build a minimal ZRLE payload: one 2×2 tile, subencoding=1 (solid fill), color=(1,2,3).
        // Use zlib RFC 1950 — TigerVNC and most VNC servers use proper zlib with 0x78 header.
        use flate2::write::ZlibEncoder;
        use std::io::Write;

        let raw_tile = [1u8, 1, 2, 3]; // subenc=1, R=1, G=2, B=3
        let mut encoder = ZlibEncoder::new(Vec::new(), flate2::Compression::default());
        encoder.write_all(&raw_tile).unwrap();
        let compressed = encoder.finish().unwrap();

        let mut state = ZrleState::new();
        let out = decode_zrle(&compressed, 2, 2, &mut state).unwrap();

        assert_eq!(out.len(), 2 * 2 * 3);
        for i in (0..out.len()).step_by(3) {
            assert_eq!((out[i], out[i + 1], out[i + 2]), (1, 2, 3));
        }
    }

    #[test]
    fn test_zrle_corrupted_data_returns_error() {
        // AC-4: corrupted zlib → error, not panic.
        let mut state = ZrleState::new();
        let result = decode_zrle(b"not valid zlib data", 4, 4, &mut state);
        assert!(
            result.is_err(),
            "expected error for corrupted ZRLE/zlib data"
        );
    }

    #[test]
    fn test_zrle_zlib_stream_starts_with_0x78() {
        // TigerVNC sends proper zlib RFC 1950 (CMF byte 0x78). The original "incorrect
        // header check" was caused by TCP fragmentation — the streaming read_exact
        // reader delivers properly-framed bytes so ZrleState::new(true) now works.
        use flate2::write::ZlibEncoder;
        use std::io::Write;

        let raw_tile = [1u8, 1, 2, 3]; // subenc=1, R=1, G=2, B=3 (2×2 solid-fill tile)
        let mut encoder = ZlibEncoder::new(Vec::new(), flate2::Compression::default());
        encoder.write_all(&raw_tile).unwrap();
        let compressed = encoder.finish().unwrap();

        // Confirm TigerVNC-style zlib header: CMF byte = 0x78
        assert_eq!(
            compressed[0], 0x78,
            "ZlibEncoder produces RFC 1950 (0x78 CMF header)"
        );

        let mut state = ZrleState::new();
        let result = decode_zrle(&compressed, 2, 2, &mut state);
        assert!(
            result.is_ok(),
            "ZrleState(true) must decode RFC 1950 data: {:?}",
            result.err()
        );

        let out = result.unwrap();
        assert_eq!(out.len(), 12);
        for i in (0..12).step_by(3) {
            assert_eq!((out[i], out[i + 1], out[i + 2]), (1, 2, 3));
        }
    }
}
