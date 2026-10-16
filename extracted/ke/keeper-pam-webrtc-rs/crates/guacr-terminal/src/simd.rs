// SIMD-optimized pixel format conversion for RDP
// Accelerates pixel format conversion using CPU SIMD instructions

/// Convert BGR to RGBA using SIMD (if available)
///
/// RDP often sends BGR format, but we need RGBA for encoding.
/// This function uses SIMD instructions when available for 4-8x speedup.
pub fn convert_bgr_to_rgba_simd(bgr: &[u8], rgba: &mut [u8], width: u32, height: u32) {
    let pixel_count = (width * height) as usize;

    // Ensure output buffer is large enough
    assert!(rgba.len() >= pixel_count * 4);
    assert!(bgr.len() >= pixel_count * 3);

    // Use SIMD if available (SSE/AVX)
    #[cfg(target_arch = "x86_64")]
    {
        // Use std::arch::is_x86_feature_detected! macro
        // Note: This macro can only be used in certain contexts
        // For now, use runtime detection or compile-time features
        // TODO: Implement proper runtime SIMD detection
        // For now, fall back to scalar (will be optimized later)
    }

    #[cfg(target_arch = "aarch64")]
    {
        // Note: NEON is standard on aarch64, but we need proper detection
        // For now, fall back to scalar
    }

    // Fallback to scalar implementation
    // TODO: Add SIMD optimizations (AVX2/SSE4/NEON) for 4-8x speedup
    convert_bgr_to_rgba_scalar(bgr, rgba, pixel_count);
}

/// Convert 32-bit BGRA/BGRX to RGBA.
///
/// Distinct from [`convert_bgr_to_rgba_simd`], which reads a 24-bit source. Callers with a
/// fourth source byte per pixel are an X11 framebuffer grab (`ZPixmap` at depth 24, which
/// X11 hands back in a 32bpp slot) and RDP's cursor bitmaps.
///
/// The source's fourth byte is discarded rather than copied: on a depth-24 X11 visual it is
/// undefined padding, so carrying it into alpha renders the frame transparent whenever the
/// pad happens to be zero. Output alpha is always opaque.
///
/// `rgba` may be longer than the frame -- it typically comes from a buffer pool -- and bytes
/// past `width * height * 4` are left untouched.
///
/// This is a scalar loop. It is deliberately not named `_simd`; see the note on
/// [`convert_bgr_to_rgba_simd`], whose SIMD arms are unimplemented.
pub fn convert_bgra_to_rgba(bgra: &[u8], rgba: &mut [u8], width: u32, height: u32) {
    let pixel_count = (width as usize) * (height as usize);

    assert!(rgba.len() >= pixel_count * 4);
    assert!(bgra.len() >= pixel_count * 4);

    for i in 0..pixel_count {
        let idx = i * 4;
        rgba[idx] = bgra[idx + 2]; // R
        rgba[idx + 1] = bgra[idx + 1]; // G
        rgba[idx + 2] = bgra[idx]; // B
        rgba[idx + 3] = 255; // A
    }
}

/// Scalar fallback implementation (always works, but slower)
fn convert_bgr_to_rgba_scalar(bgr: &[u8], rgba: &mut [u8], pixel_count: usize) {
    for i in 0..pixel_count {
        let src_idx = i * 3;
        let dst_idx = i * 4;

        rgba[dst_idx] = bgr[src_idx + 2]; // R
        rgba[dst_idx + 1] = bgr[src_idx + 1]; // G
        rgba[dst_idx + 2] = bgr[src_idx]; // B
        rgba[dst_idx + 3] = 255; // A
    }
}
