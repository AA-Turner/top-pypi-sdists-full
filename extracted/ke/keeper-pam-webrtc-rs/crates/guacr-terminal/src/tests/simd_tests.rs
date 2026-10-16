use crate::simd::{convert_bgr_to_rgba_simd, convert_bgra_to_rgba};

#[test]
fn test_convert_bgr_to_rgba() {
    // BGR: Blue=255, Green=128, Red=64
    let bgr = vec![255u8, 128, 64];
    let mut rgba = vec![0u8; 4];

    convert_bgr_to_rgba_simd(&bgr, &mut rgba, 1, 1);

    assert_eq!(rgba[0], 64); // R
    assert_eq!(rgba[1], 128); // G
    assert_eq!(rgba[2], 255); // B
    assert_eq!(rgba[3], 255); // A
}

#[test]
fn test_convert_bgr_to_rgba_multiple_pixels() {
    // 2 pixels: (255,128,64) and (0,255,128)
    let bgr = vec![255u8, 128, 64, 0, 255, 128];
    let mut rgba = vec![0u8; 8];

    convert_bgr_to_rgba_simd(&bgr, &mut rgba, 2, 1);

    // First pixel
    assert_eq!(rgba[0], 64);
    assert_eq!(rgba[1], 128);
    assert_eq!(rgba[2], 255);
    assert_eq!(rgba[3], 255);

    // Second pixel
    assert_eq!(rgba[4], 128);
    assert_eq!(rgba[5], 255);
    assert_eq!(rgba[6], 0);
    assert_eq!(rgba[7], 255);
}

/// 32-bit conversions, for sources that already carry a fourth byte per pixel: an X11
/// framebuffer grab (`ZPixmap` at depth 24 in a 32bpp slot) and RDP's cursor bitmaps.
///
/// Channel order is the whole point. A red/blue swap produces a picture that is clearly
/// *there* -- correct geometry, correct motion, plausible-looking colours -- so it survives
/// casual inspection and is caught only by an assertion that names the channels.
mod bgra_to_rgba {
    use super::*;

    #[test]
    fn test_channels_are_swapped_not_copied() {
        // BGRA: Blue=255, Green=128, Red=64, Alpha=200
        let bgra = vec![255u8, 128, 64, 200];
        let mut rgba = vec![0u8; 4];

        convert_bgra_to_rgba(&bgra, &mut rgba, 1, 1);

        assert_eq!(rgba[0], 64, "R must come from the third source byte");
        assert_eq!(rgba[1], 128, "G is unchanged");
        assert_eq!(rgba[2], 255, "B must come from the first source byte");
    }

    #[test]
    fn test_alpha_is_forced_opaque() {
        // X11 hands back BGRX at depth 24: the fourth byte is undefined padding, not
        // alpha. Passing it through makes a framebuffer grab render fully transparent
        // when the pad happens to be zero.
        let bgrx = vec![10u8, 20, 30, 0];
        let mut rgba = vec![0u8; 4];

        convert_bgra_to_rgba(&bgrx, &mut rgba, 1, 1);

        assert_eq!(
            rgba[3], 255,
            "the source's fourth byte is undefined padding on a depth-24 X11 visual and \
             must not be carried into alpha"
        );
    }

    #[test]
    fn test_every_pixel_is_converted() {
        // Guards against a loop that converts the first pixel and stops, which a
        // single-pixel test cannot see.
        let bgra = vec![
            255u8, 128, 64, 0, // px0
            0, 255, 128, 0, // px1
            1, 2, 3, 0, // px2
            9, 8, 7, 0, // px3
        ];
        let mut rgba = vec![0u8; 16];

        convert_bgra_to_rgba(&bgra, &mut rgba, 2, 2);

        assert_eq!(
            rgba,
            vec![64, 128, 255, 255, 128, 255, 0, 255, 3, 2, 1, 255, 7, 8, 9, 255]
        );
    }

    #[test]
    fn test_a_larger_destination_leaves_the_tail_untouched() {
        // The destination comes from EncoderPipeline::acquire_frame_buffer(), a pooled
        // buffer that may be longer than the frame. Writing past width*height*4 would
        // corrupt whatever the pool reuses it for next.
        let bgra = vec![255u8, 128, 64, 0];
        let mut rgba = vec![0xAAu8; 8];

        convert_bgra_to_rgba(&bgra, &mut rgba, 1, 1);

        assert_eq!(
            &rgba[4..],
            &[0xAA; 4],
            "bytes beyond the frame must be left alone"
        );
    }
}
