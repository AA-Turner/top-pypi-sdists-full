// ClearCodec decoder — MS-RDPEGFX section 2.2.4 (T-023 to T-027)
//
// ClearCodec is a composite subcodec for RDP EGFX that carries UI text and
// crisp bitmaps as three optional layers:
//
//   Residual layer  — zlib-compressed RGB triplets (always present)
//   Bands layer     — horizontal color runs (CLEARCODEC_FLAG_BANDS_PRESENT)
//   Subbands layer  — 8x8 subband blocks (CLEARCODEC_FLAG_SUBBANDS_PRESENT)
//
// ClearCodec also supports a glyph cache (T-063, T-064 in Tier 1).
//
// AC-1: Residual-only PDU decodes to correct RGBA pixel data.
// AC-2: Bands layer decoded with correct run positioning.
// AC-3: Subbands layer decoded to correct pixel data.
// AC-4: Three-layer composite produces correct composite pixel data.
// AC-5: Malformed PDU (truncated, invalid geometry) → error, not panic.

use std::io::Read;

use flate2::read::ZlibDecoder;

// ── ClearCodec header flags ─────────────────────────────────────────────────

const FLAG_GLYPH_INDEX: u8 = 0x01; // PDU contains a glyph index for cache lookup or store
const FLAG_GLYPH_HIT: u8 = 0x02; // Use cached glyph at glyph_index; skip residual/bands/subbands
const FLAG_CACHE_RESET: u8 = 0x04; // Reset glyph cache before processing this PDU

/// A decoded ClearCodec bitmap in RGBA-32 format (4 bytes per pixel, row-major).
#[derive(Debug, Clone)]
pub struct ClearCodecBitmap {
    pub rgba: Vec<u8>,
    pub width: u32,
    pub height: u32,
    /// Glyph index to store this bitmap under, if the GLYPH_INDEX flag was set.
    pub store_as_glyph: Option<u16>,
}

// ── Glyph cache (T-063 / T-064 — used here for decode; full cache is in Tier 1) ──

/// Per-session ClearCodec glyph cache.
///
/// The cache is created once per RDP session and passed into every
/// `decode_clearcodec` call. It persists decoded glyphs by index so
/// subsequent PDUs with GLYPH_HIT can skip re-decoding.
pub struct ClearCodecGlyphCache {
    entries: std::collections::HashMap<u16, Vec<u8>>, // index → RGBA pixels
}

impl ClearCodecGlyphCache {
    pub fn new() -> Self {
        Self {
            entries: std::collections::HashMap::new(),
        }
    }

    fn store(&mut self, index: u16, rgba: Vec<u8>) {
        self.entries.insert(index, rgba);
    }

    fn get(&self, index: u16) -> Option<&[u8]> {
        self.entries.get(&index).map(|v| v.as_slice())
    }

    fn reset(&mut self) {
        self.entries.clear();
    }
}

impl Default for ClearCodecGlyphCache {
    fn default() -> Self {
        Self::new()
    }
}

// ── Main decoder ─────────────────────────────────────────────────────────────

/// Decode a ClearCodec PDU payload into an RGBA bitmap.
///
/// `data`: the raw `bitmap_data` bytes from `WireToSurface1Pdu` (codec_id=ClearCodec).
/// `width`, `height`: destination rectangle dimensions.
/// `cache`: per-session glyph cache; mutated by GLYPH_INDEX / CACHE_RESET flags.
///
/// Returns `Err(String)` on any malformed input (AC-5).
pub fn decode_clearcodec(
    data: &[u8],
    width: u32,
    height: u32,
    cache: &mut ClearCodecGlyphCache,
) -> Result<ClearCodecBitmap, String> {
    // Minimum: 1 byte flags.
    if data.is_empty() {
        return Err("ClearCodec: empty payload".to_string());
    }

    let flags = data[0];
    let mut pos = 1usize;

    // CACHE_RESET: clear glyph cache before processing.
    if flags & FLAG_CACHE_RESET != 0 {
        cache.reset();
    }

    // Read glyph index (2 bytes) when either flag is set.
    let glyph_index = if flags & (FLAG_GLYPH_INDEX | FLAG_GLYPH_HIT) != 0 {
        if pos + 2 > data.len() {
            return Err("ClearCodec: truncated glyph index".to_string());
        }
        let idx = u16::from_le_bytes([data[pos], data[pos + 1]]);
        pos += 2;
        Some(idx)
    } else {
        None
    };

    // GLYPH_HIT: return cached glyph without re-decoding.
    if flags & FLAG_GLYPH_HIT != 0 {
        let idx = glyph_index.unwrap();
        let cached = cache
            .get(idx)
            .ok_or_else(|| format!("ClearCodec: glyph cache miss at index {idx}"))?;
        return Ok(ClearCodecBitmap {
            rgba: cached.to_vec(),
            width,
            height,
            store_as_glyph: None,
        });
    }

    // Allocate RGBA output buffer (pre-filled transparent black).
    // Reject unreasonably large dimensions before allocation.
    // 16384×16384 is far beyond any real RDP session; use as an upper bound.
    const MAX_DIM: u32 = 16384;
    if width > MAX_DIM || height > MAX_DIM {
        return Err(format!(
            "ClearCodec: dimensions ({width}×{height}) exceed maximum {MAX_DIM}×{MAX_DIM}"
        ));
    }
    let pixel_count = (width as usize)
        .checked_mul(height as usize)
        .ok_or_else(|| format!("ClearCodec: dimension overflow ({width}×{height})"))?;
    let rgba_size = pixel_count
        .checked_mul(4)
        .ok_or_else(|| "ClearCodec: RGBA buffer size overflow".to_string())?;
    let mut rgba = vec![0u8; rgba_size];

    // ── Residual layer (always present, AC-1) ─────────────────────────────

    if pos + 2 > data.len() {
        return Err("ClearCodec: missing residual length".to_string());
    }
    let residual_compressed_len = u16::from_le_bytes([data[pos], data[pos + 1]]) as usize;
    pos += 2;

    if residual_compressed_len > 0 {
        if pos + residual_compressed_len > data.len() {
            return Err(format!(
                "ClearCodec: residual layer truncated (need {residual_compressed_len}, have {})",
                data.len() - pos
            ));
        }
        let residual_bytes = &data[pos..pos + residual_compressed_len];
        pos += residual_compressed_len;
        apply_residual_layer(residual_bytes, &mut rgba, width, height)?;
    }

    // ── Bands layer (optional, AC-2) ──────────────────────────────────────

    if pos + 2 > data.len() {
        // No bands/subbands — residual-only PDU.
        let result = finalize(rgba, width, height, glyph_index, flags, cache);
        return Ok(result);
    }

    let band_count = u16::from_le_bytes([data[pos], data[pos + 1]]) as usize;
    pos += 2;

    if band_count > 0 {
        pos = apply_bands_layer(&data[pos..], band_count, &mut rgba, width, height, pos)?;
    }

    // ── Subbands layer (optional, AC-3) ──────────────────────────────────

    if pos + 2 <= data.len() {
        let subband_count = u16::from_le_bytes([data[pos], data[pos + 1]]) as usize;
        pos += 2;

        if subband_count > 0 {
            apply_subbands_layer(&data[pos..], subband_count, &mut rgba, width, height)?;
        }
    }

    Ok(finalize(rgba, width, height, glyph_index, flags, cache))
}

// ── Residual layer decoder ────────────────────────────────────────────────────

fn apply_residual_layer(
    compressed: &[u8],
    rgba: &mut [u8],
    width: u32,
    height: u32,
) -> Result<(), String> {
    // Residual is zlib-compressed RGB triplets, row-major.
    let mut decoder = ZlibDecoder::new(compressed);
    let expected = (width * height * 3) as usize;
    let mut rgb = vec![0u8; expected];

    decoder
        .read_exact(&mut rgb)
        .map_err(|e| format!("ClearCodec residual: zlib decode error: {e}"))?;

    // Convert RGB → RGBA.
    for (i, chunk) in rgb.chunks_exact(3).enumerate() {
        let dst = i * 4;
        if dst + 3 < rgba.len() {
            rgba[dst] = chunk[0];
            rgba[dst + 1] = chunk[1];
            rgba[dst + 2] = chunk[2];
            rgba[dst + 3] = 255;
        }
    }

    Ok(())
}

// ── Bands layer decoder ───────────────────────────────────────────────────────

fn apply_bands_layer(
    data: &[u8],
    band_count: usize,
    rgba: &mut [u8],
    width: u32,
    height: u32,
    base_pos: usize,
) -> Result<usize, String> {
    // Each CLEARCODEC_BAND_DATA entry:
    //   x_start(2) y_start(2) x_end(2) y_end(2) color(3=BGR) run_count(2) runs...
    let mut pos = 0usize;
    let w = width as usize;

    for band_idx in 0..band_count {
        if pos + 11 > data.len() {
            return Err(format!(
                "ClearCodec bands: band {band_idx} header truncated"
            ));
        }
        let x_start = u16::from_le_bytes([data[pos], data[pos + 1]]) as usize;
        let y_start = u16::from_le_bytes([data[pos + 2], data[pos + 3]]) as usize;
        let x_end = u16::from_le_bytes([data[pos + 4], data[pos + 5]]) as usize;
        let y_end = u16::from_le_bytes([data[pos + 6], data[pos + 7]]) as usize;
        // Background color: BGR24
        let b = data[pos + 8];
        let g = data[pos + 9];
        let r = data[pos + 10];
        pos += 11;

        // Fill band rectangle with background color.
        for y in y_start..=y_end.min(height as usize - 1) {
            for x in x_start..=x_end.min(w - 1) {
                let dst = (y * w + x) * 4;
                if dst + 3 < rgba.len() {
                    rgba[dst] = r;
                    rgba[dst + 1] = g;
                    rgba[dst + 2] = b;
                    rgba[dst + 3] = 255;
                }
            }
        }

        // Run-length encoded color transitions within the band.
        if pos + 2 > data.len() {
            break;
        }
        let run_count = u16::from_le_bytes([data[pos], data[pos + 1]]) as usize;
        pos += 2;

        for _ in 0..run_count {
            // Each run: x_offset(2) y_offset(1) color(3=BGR)
            if pos + 6 > data.len() {
                break;
            }
            let x_off = u16::from_le_bytes([data[pos], data[pos + 1]]) as usize;
            let y_off = data[pos + 2] as usize;
            let rb = data[pos + 3];
            let rg = data[pos + 4];
            let rr = data[pos + 5];
            pos += 6;

            let px = x_start + x_off;
            let py = y_start + y_off;
            if px < w && py < height as usize {
                let dst = (py * w + px) * 4;
                if dst + 3 < rgba.len() {
                    rgba[dst] = rr;
                    rgba[dst + 1] = rg;
                    rgba[dst + 2] = rb;
                    rgba[dst + 3] = 255;
                }
            }
        }
    }

    Ok(base_pos + pos)
}

// ── Subbands layer decoder ────────────────────────────────────────────────────

fn apply_subbands_layer(
    data: &[u8],
    subband_count: usize,
    rgba: &mut [u8],
    width: u32,
    height: u32,
) -> Result<(), String> {
    // Each CLEARCODEC_SUBBAND_DATUM: x(2) y(2) width(2) height(2) data[width*height*3]
    let mut pos = 0usize;
    let w = width as usize;
    let h = height as usize;

    for sub_idx in 0..subband_count {
        if pos + 8 > data.len() {
            return Err(format!(
                "ClearCodec subbands: subband {sub_idx} header truncated"
            ));
        }
        let sx = u16::from_le_bytes([data[pos], data[pos + 1]]) as usize;
        let sy = u16::from_le_bytes([data[pos + 2], data[pos + 3]]) as usize;
        let sw = u16::from_le_bytes([data[pos + 4], data[pos + 5]]) as usize;
        let sh = u16::from_le_bytes([data[pos + 6], data[pos + 7]]) as usize;
        pos += 8;

        let needed = sw
            .checked_mul(sh)
            .and_then(|n| n.checked_mul(3))
            .ok_or_else(|| format!("ClearCodec subbands: subband {sub_idx} dimension overflow"))?;

        if pos + needed > data.len() {
            return Err(format!(
                "ClearCodec subbands: subband {sub_idx} data truncated \
                 (need {needed}, have {})",
                data.len() - pos
            ));
        }

        // Copy RGB pixels into RGBA output.
        let sub_data = &data[pos..pos + needed];
        pos += needed;

        for row in 0..sh {
            for col in 0..sw {
                let src_off = (row * sw + col) * 3;
                let px = sx + col;
                let py = sy + row;
                if px < w && py < h && src_off + 2 < sub_data.len() {
                    let dst = (py * w + px) * 4;
                    if dst + 3 < rgba.len() {
                        rgba[dst] = sub_data[src_off];
                        rgba[dst + 1] = sub_data[src_off + 1];
                        rgba[dst + 2] = sub_data[src_off + 2];
                        rgba[dst + 3] = 255;
                    }
                }
            }
        }
    }

    Ok(())
}

// ── Finalize (glyph cache store) ──────────────────────────────────────────────

fn finalize(
    rgba: Vec<u8>,
    width: u32,
    height: u32,
    glyph_index: Option<u16>,
    flags: u8,
    cache: &mut ClearCodecGlyphCache,
) -> ClearCodecBitmap {
    let store_as_glyph = if flags & FLAG_GLYPH_INDEX != 0 {
        if let Some(idx) = glyph_index {
            cache.store(idx, rgba.clone());
            Some(idx)
        } else {
            None
        }
    } else {
        None
    };

    ClearCodecBitmap {
        rgba,
        width,
        height,
        store_as_glyph,
    }
}

// ── Tests ─────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    fn make_cache() -> ClearCodecGlyphCache {
        ClearCodecGlyphCache::new()
    }

    /// Build a minimal ClearCodec payload with only a residual layer.
    fn residual_only_payload(rgb: &[u8]) -> Vec<u8> {
        use flate2::write::ZlibEncoder;
        let mut enc = ZlibEncoder::new(Vec::new(), flate2::Compression::default());
        enc.write_all(rgb).unwrap();
        let compressed = enc.finish().unwrap();

        let mut payload = vec![0u8]; // flags = 0
        let clen = compressed.len() as u16;
        payload.extend_from_slice(&clen.to_le_bytes());
        payload.extend_from_slice(&compressed);
        payload
    }

    // AC-1: residual-only PDU decodes to correct RGBA.
    #[test]
    fn test_residual_only() {
        // 2×1 pixels: (255,0,0) and (0,255,0) in RGB.
        let rgb = [255u8, 0, 0, 0, 255, 0];
        let payload = residual_only_payload(&rgb);
        let mut cache = make_cache();
        let bmp = decode_clearcodec(&payload, 2, 1, &mut cache).unwrap();
        assert_eq!(bmp.width, 2);
        assert_eq!(bmp.height, 1);
        assert_eq!(bmp.rgba.len(), 8); // 2 × 4 bytes
                                       // First pixel: red.
        assert_eq!(&bmp.rgba[0..4], &[255, 0, 0, 255]);
        // Second pixel: green.
        assert_eq!(&bmp.rgba[4..8], &[0, 255, 0, 255]);
    }

    // AC-5: empty payload returns error, not panic.
    #[test]
    fn test_empty_payload_error() {
        let mut cache = make_cache();
        assert!(decode_clearcodec(&[], 4, 4, &mut cache).is_err());
    }

    // AC-5: overflow dimensions return error.
    #[test]
    fn test_dimension_overflow_error() {
        let payload = vec![0u8, 0, 0]; // flags + empty residual
        let mut cache = make_cache();
        let result = decode_clearcodec(&payload, 65535, 65535, &mut cache);
        assert!(result.is_err(), "65535×65535 must return error");
    }

    // AC-5: truncated residual zlib returns error.
    #[test]
    fn test_truncated_residual_error() {
        let mut payload = vec![0u8]; // flags
        payload.extend_from_slice(&[4u8, 0u8]); // residual_len = 4 bytes
        payload.extend_from_slice(&[1u8, 2u8]); // only 2 bytes of compressed data
        let mut cache = make_cache();
        assert!(decode_clearcodec(&payload, 2, 2, &mut cache).is_err());
    }

    // AC-4: Three-layer composite (residual + bands + subbands) produces a non-empty RGBA buffer.
    //
    // Layout: 4×4 pixels.
    //   Residual: all pixels set to blue (0, 0, 255).
    //   Bands: one band covering columns 0-1 of rows 0-1, overwritten with red (255, 0, 0).
    //   Subbands: one 2×2 subband at (2, 2), overwritten with green (0, 255, 0).
    //
    // After decode the RGBA buffer must be non-empty and at least one pixel must be non-zero.
    #[test]
    fn test_three_layer_composite_produces_non_empty_rgba() {
        use flate2::write::ZlibEncoder;
        use std::io::Write;

        // Residual: 4×4 = 16 pixels, all blue RGB = (0, 0, 255).
        let mut rgb_residual = Vec::with_capacity(16 * 3);
        for _ in 0..16 {
            rgb_residual.extend_from_slice(&[0u8, 0, 255]); // R=0, G=0, B=255
        }
        let mut enc = ZlibEncoder::new(Vec::new(), flate2::Compression::default());
        enc.write_all(&rgb_residual).unwrap();
        let compressed = enc.finish().unwrap();

        let mut payload = vec![0u8]; // flags = 0

        // Residual length (u16 LE) + compressed data.
        let clen = compressed.len() as u16;
        payload.extend_from_slice(&clen.to_le_bytes());
        payload.extend_from_slice(&compressed);

        // Bands layer: band_count = 1 (u16 LE).
        payload.extend_from_slice(&1u16.to_le_bytes());
        // Band header: x_start=0, y_start=0, x_end=1, y_end=1, color=BGR(0,0,255) = red in RGB.
        // BGR order: B=0, G=0, R=255 encodes as bytes [0, 0, 255].
        payload.extend_from_slice(&0u16.to_le_bytes()); // x_start
        payload.extend_from_slice(&0u16.to_le_bytes()); // y_start
        payload.extend_from_slice(&1u16.to_le_bytes()); // x_end
        payload.extend_from_slice(&1u16.to_le_bytes()); // y_end
        payload.push(0); // B
        payload.push(0); // G
        payload.push(255); // R (stored as R byte, becomes red in output)
                           // run_count = 0 (no individual pixel runs).
        payload.extend_from_slice(&0u16.to_le_bytes());

        // Subbands layer: subband_count = 1 (u16 LE).
        payload.extend_from_slice(&1u16.to_le_bytes());
        // Subband header: x=2, y=2, width=2, height=2.
        payload.extend_from_slice(&2u16.to_le_bytes()); // sx
        payload.extend_from_slice(&2u16.to_le_bytes()); // sy
        payload.extend_from_slice(&2u16.to_le_bytes()); // sw
        payload.extend_from_slice(&2u16.to_le_bytes()); // sh
                                                        // 4 pixels of green RGB = (0, 255, 0).
        for _ in 0..4 {
            payload.extend_from_slice(&[0u8, 255, 0]);
        }

        let mut cache = make_cache();
        let bmp = decode_clearcodec(&payload, 4, 4, &mut cache).unwrap();

        assert_eq!(bmp.width, 4);
        assert_eq!(bmp.height, 4);
        // 4×4 pixels × 4 bytes = 64 bytes.
        assert_eq!(
            bmp.rgba.len(),
            64,
            "three-layer composite RGBA buffer must be 64 bytes for 4×4"
        );
        // At least one pixel must be non-zero (composite is not all-black).
        assert!(
            bmp.rgba.iter().any(|&b| b != 0),
            "three-layer composite must produce at least one non-zero pixel"
        );
        // Verify band pixel at (0,0) is red: RGBA = (255, 0, 0, 255).
        assert_eq!(
            &bmp.rgba[0..4],
            &[255, 0, 0, 255],
            "band pixel at (0,0) must be red"
        );
        // Verify subband pixel at (2,2): offset = (2*4 + 2) * 4 = 40.
        assert_eq!(
            &bmp.rgba[40..44],
            &[0, 255, 0, 255],
            "subband pixel at (2,2) must be green"
        );
    }

    // Glyph cache: store and retrieve (matches T-063 requirements).
    #[test]
    fn test_glyph_cache_store_and_hit() {
        // Build payload with FLAG_GLYPH_INDEX = 0x01, glyph_index = 7.
        let rgb = [100u8, 150, 200]; // 1×1 pixel
        let payload_base = residual_only_payload(&rgb);

        let mut store_payload = vec![FLAG_GLYPH_INDEX]; // flags
        store_payload.extend_from_slice(&7u16.to_le_bytes()); // glyph_index = 7
                                                              // Skip the flags byte from residual_only_payload (it starts at [0]).
        store_payload.extend_from_slice(&payload_base[1..]);

        let mut cache = make_cache();
        let stored = decode_clearcodec(&store_payload, 1, 1, &mut cache).unwrap();
        assert_eq!(stored.store_as_glyph, Some(7));

        // Now build a GLYPH_HIT payload for index 7.
        let hit_payload = [FLAG_GLYPH_HIT, 7, 0]; // flags + glyph_index (LE)
        let hit = decode_clearcodec(&hit_payload, 1, 1, &mut cache).unwrap();
        assert_eq!(hit.rgba[0], 100);
        assert_eq!(hit.rgba[1], 150);
        assert_eq!(hit.rgba[2], 200);
    }
}
