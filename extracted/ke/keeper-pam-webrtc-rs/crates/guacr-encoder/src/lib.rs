//! H.264 encoder backends for guacr protocol handlers.

#[cfg(feature = "software")]
pub mod openh264_backend;
// FFmpeg is the single hardware backend on every platform: VAAPI/NVENC (Linux),
// Media Foundation/QSV/NVENC (Windows), VideoToolbox (macOS). openh264 is the software
// fallback. The former raw nvenc/videotoolbox backends were removed in favor of this.
#[cfg(feature = "ffmpeg")]
pub mod ffmpeg_backend;
pub mod pipeline;

#[cfg(test)]
mod tests;

use anyhow::Result;

pub use guacr_handlers::EncodedFrame;

#[derive(Clone)]
pub struct RgbaFrame {
    pub data: Vec<u8>,
    pub width: u32,
    pub height: u32,
    pub timestamp_us: u64,
}

/// Which family of encoder is live. Lets a handler raise its resolution ceiling once it
/// knows hardware encode is actually running — software cannot hold 30fps at native
/// resolution even after the `read_rgb8` fix (measured 2026-08-04: 19.6 fps best case at
/// 3292x1724), while FFmpeg/NVENC clears it easily (32.9 fps). VAAPI's stub fails before
/// `FfmpegEncoder::new` returns Ok, so any live instance is a real hardware backend.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EncoderBackendKind {
    Software,
    Hardware,
}

pub trait VideoEncoder: Send {
    fn encode(&mut self, frame: &RgbaFrame) -> Result<EncodedFrame>;
    fn request_keyframe(&mut self);
    fn set_target_bitrate(&mut self, bps: u32);
    fn frame_count(&self) -> u64;
    /// The frame dimensions this encoder was configured for. `EncoderPipeline`
    /// compares submitted frames against this and rebuilds the encoder (via its
    /// factory) when a BWE resolution step changes the encode geometry.
    fn dimensions(&self) -> (u32, u32);
    /// Which family of encoder this is — see `EncoderBackendKind`.
    fn backend_kind(&self) -> EncoderBackendKind;
}

/// Bits per pixel per second the encoder aims for. Derived from what shipped before
/// bitrate was resolution-aware: a fixed 3 Mbps at the 1918x1004 geometry measured live
/// on 2026-08-03, i.e. 3e6 / (1918 * 1004 * 30) = 0.0519. Keeping the same figure means
/// that geometry still gets ~3 Mbps while larger frames scale up instead of starving.
const TARGET_BITS_PER_PIXEL: f64 = 0.0519;

/// Floor and ceiling for the *initial* bitrate. BWE adjusts from here at runtime, so these
/// only bound the starting guess: small desktops still get enough bits to look clean, and a
/// very large one cannot open by demanding tens of Mbps before any feedback has arrived.
const MIN_INITIAL_BITRATE_BPS: u32 = 1_500_000;
const MAX_INITIAL_BITRATE_BPS: u32 = 12_000_000;

/// Initial encoder bitrate scaled to the frame size.
///
/// A fixed bitrate makes quality fall off as resolution rises: 3 Mbps is 0.052 bits/px at
/// 1918x1004 but only 0.018 at 3292x1724, so raising the resolution cap *without* scaling
/// the bitrate looks worse rather than better — a soft clean upscale beats a sharp blocky
/// under-bitrated stream. This makes the two move together. `BweController` then adapts from
/// this starting point via `VideoEncoder::set_target_bitrate`.
pub fn initial_bitrate_bps(width: u32, height: u32, fps: u32) -> u32 {
    let pixels_per_sec = (width as f64) * (height as f64) * (fps.max(1) as f64);
    let bps = pixels_per_sec * TARGET_BITS_PER_PIXEL;
    if !bps.is_finite() || bps <= 0.0 {
        return MIN_INITIAL_BITRATE_BPS;
    }
    (bps as u32).clamp(MIN_INITIAL_BITRATE_BPS, MAX_INITIAL_BITRATE_BPS)
}

/// Bilinear-downscale a tightly-packed RGBA image into `dst` (cleared first).
///
/// Used when a BWE resolution step asks for encoding below the session's natural size:
/// the handler scales its framebuffer snapshot into a pooled buffer and submits the
/// smaller frame. Top-left-aligned sampling in 16.16 fixed point; weights are applied
/// exactly (u64 accumulate), so a solid-colour image stays byte-identical at any scale.
/// Equal dimensions degrade to a plain copy. Degenerate inputs (zero dimension, short
/// `src`) leave `dst` empty rather than panicking.
pub fn scale_rgba(src: &[u8], src_w: u32, src_h: u32, dst: &mut Vec<u8>, dst_w: u32, dst_h: u32) {
    let (sw, sh, dw, dh) = (
        src_w as usize,
        src_h as usize,
        dst_w as usize,
        dst_h as usize,
    );
    dst.clear();
    if sw == 0 || sh == 0 || dw == 0 || dh == 0 || src.len() < sw * sh * 4 {
        return;
    }
    if (sw, sh) == (dw, dh) {
        dst.extend_from_slice(&src[..sw * sh * 4]);
        return;
    }
    dst.reserve(dw * dh * 4);
    let x_step = ((sw as u64) << 16) / dw as u64;
    let y_step = ((sh as u64) << 16) / dh as u64;
    for dy in 0..dh {
        let sy_fp = dy as u64 * y_step;
        let sy = ((sy_fp >> 16) as usize).min(sh - 1);
        let fy = sy_fp & 0xFFFF;
        let sy1 = (sy + 1).min(sh - 1);
        let row0 = &src[sy * sw * 4..][..sw * 4];
        let row1 = &src[sy1 * sw * 4..][..sw * 4];
        for dx in 0..dw {
            let sx_fp = dx as u64 * x_step;
            let sx = ((sx_fp >> 16) as usize).min(sw - 1);
            let fx = sx_fp & 0xFFFF;
            let sx1 = (sx + 1).min(sw - 1);
            for c in 0..4 {
                let p00 = row0[sx * 4 + c] as u64;
                let p10 = row0[sx1 * 4 + c] as u64;
                let p01 = row1[sx * 4 + c] as u64;
                let p11 = row1[sx1 * 4 + c] as u64;
                let top = p00 * (0x10000 - fx) + p10 * fx;
                let bot = p01 * (0x10000 - fx) + p11 * fx;
                let v = (top * (0x10000 - fy) + bot * fy) >> 32;
                dst.push(v as u8);
            }
        }
    }
}

/// Copy tightly-packed RGBA rows into a destination whose rows are `stride` bytes apart.
///
/// FFmpeg's `av_frame_get_buffer` aligns each row (32 bytes by default), so `stride`
/// exceeds `width * 4` for any width that is not a multiple of 8 — e.g. the 1918-wide
/// RDP geometry measured live on 2026-08-03, where `row_bytes` is 7672 but `stride` is
/// 7680. Copying the source flat in that case shifts every row after the first by the
/// difference and shears the picture progressively down the frame.
///
/// Lives here rather than in `ffmpeg_backend` so it stays under test on every build,
/// including ones without the `ffmpeg` feature (which nothing in CI compiles today).
#[cfg_attr(not(feature = "ffmpeg"), allow(dead_code))]
pub(crate) fn copy_rgba_rows(dst: &mut [u8], stride: usize, src: &[u8], row_bytes: usize) {
    if row_bytes == 0 {
        return;
    }
    // Fast path: destination is tightly packed, so one memcpy is correct.
    if stride == row_bytes {
        let n = src.len().min(dst.len());
        dst[..n].copy_from_slice(&src[..n]);
        return;
    }
    for (row, src_row) in src.chunks_exact(row_bytes).enumerate() {
        let start = row * stride;
        // Stop rather than panic if the destination is shorter than the source implies.
        match dst.get_mut(start..start + row_bytes) {
            Some(slot) => slot.copy_from_slice(src_row),
            None => break,
        }
    }
}

/// Create the best available H.264 encoder for the given frame dimensions.
///
/// Selection order: FFmpeg hardware (VAAPI/NVENC on Linux, Media Foundation/QSV/NVENC on
/// Windows, VideoToolbox on macOS) → openh264 software (guaranteed fallback).
pub fn make_encoder(width: u32, height: u32) -> Result<Box<dyn VideoEncoder>> {
    // FFmpeg unified hardware path — the single HW backend on every platform.
    #[cfg(feature = "ffmpeg")]
    if ffmpeg_backend::probe() {
        match ffmpeg_backend::FfmpegEncoder::new(width, height) {
            Ok(enc) => return Ok(Box::new(enc)),
            Err(e) => {
                log::warn!("guacr-encoder: FFmpeg HW init failed ({}), falling back", e);
            }
        }
    }

    #[cfg(feature = "software")]
    {
        log::info!("guacr-encoder: using openh264 ({}x{})", width, height);
        return Ok(Box::new(openh264_backend::OpenH264Encoder::new(
            width, height,
        )?));
    }

    #[allow(unreachable_code)]
    Err(anyhow::anyhow!("guacr-encoder: no backend compiled in"))
}
