use crate::simd::convert_bgr_to_rgba_simd;

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
