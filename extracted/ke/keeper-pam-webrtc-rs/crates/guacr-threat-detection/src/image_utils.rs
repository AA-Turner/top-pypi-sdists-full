// Image utilities for threat detection.
//
// Provides grayscale JPEG encoding used by analyze_screenshot() to reduce
// the payload sent to the BAML vision endpoint. Color is not needed for
// content analysis; grayscale halves the data per pixel vs. RGB.

use image::{GrayImage, ImageEncoder};

/// Convert RGBA pixel data to a single-channel (grayscale) JPEG.
///
/// This is the canonical encoding for screenshots sent to the threat detection
/// vision endpoint. Reasons:
/// - Grayscale reduces payload size vs. RGB (one channel instead of three).
/// - Color is not needed for threat analysis — text, UI elements, and code are
///   legible in grayscale.
/// - Consistent encoding simplifies the BAML endpoint contract.
///
/// # Arguments
///
/// * `rgba` — Raw RGBA pixel bytes, `width * height * 4` bytes in row-major order.
/// * `width` — Image width in pixels.
/// * `height` — Image height in pixels.
/// * `quality` — JPEG quality (1–100). 75 is a good default for analysis use.
///
/// # Returns
///
/// JPEG-encoded grayscale image bytes, or an error string if encoding fails.
pub fn rgba_to_grayscale_jpeg(
    rgba: &[u8],
    width: u32,
    height: u32,
    quality: u8,
) -> Result<Vec<u8>, String> {
    let expected = (width * height * 4) as usize;
    if rgba.len() != expected {
        return Err(format!(
            "rgba buffer length mismatch: expected {} bytes ({}x{}x4), got {}",
            expected,
            width,
            height,
            rgba.len()
        ));
    }

    // Convert RGBA → grayscale using the standard luminance formula
    // Y = 0.2126 R + 0.7152 G + 0.0722 B  (ITU-R BT.709)
    let luma_bytes: Vec<u8> = rgba
        .as_chunks::<4>()
        .0
        .iter()
        .map(|px| {
            let r = px[0] as f32;
            let g = px[1] as f32;
            let b = px[2] as f32;
            // Alpha is ignored — screen captures have opaque pixels.
            (0.2126 * r + 0.7152 * g + 0.0722 * b).round() as u8
        })
        .collect();

    let gray_image = GrayImage::from_raw(width, height, luma_bytes)
        .ok_or_else(|| "failed to construct GrayImage from luma bytes".to_string())?;

    let mut jpeg_buf = Vec::new();
    let encoder = image::codecs::jpeg::JpegEncoder::new_with_quality(&mut jpeg_buf, quality);
    encoder
        .write_image(
            gray_image.as_raw(),
            width,
            height,
            image::ExtendedColorType::L8,
        )
        .map_err(|e| format!("JPEG encode failed: {e}"))?;

    Ok(jpeg_buf)
}
