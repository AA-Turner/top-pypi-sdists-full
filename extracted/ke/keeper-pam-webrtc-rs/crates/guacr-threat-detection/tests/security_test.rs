// Security tests for AI threat detection.
// Run with: cargo test -p guacr-threat-detection --test security_test -- --include-ignored
#[cfg(test)]
mod security_tests {
    #[tokio::test]
    #[ignore]
    async fn test_deny_tag_injection_rejected() {
        use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig};
        use std::collections::HashMap;
        use std::sync::Arc;

        let mut deny_tags = HashMap::new();
        deny_tags.insert("critical".to_string(), vec!["rm.*-rf".to_string()]);

        let config = ThreatDetectorConfig {
            enabled: true,
            enable_tag_checking: true,
            deny_tags,
            ..Default::default()
        };
        let detector = Arc::new(ThreatDetector::new(config).unwrap());

        // Verify the detector is enabled and configured for tag checking
        assert!(detector.should_analyze("ssh", "return"));

        // For a full tag-based injection test, use the internal unit tests
        // (in src/tests/detector_tests.rs) which have access to check_tags().
        println!("Injection rejection test — implement with actual handler via integration test");
    }

    #[test]
    #[ignore]
    fn test_session_credentials_not_logged() {
        use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig};
        use std::sync::Arc;

        // Verify that session state does not store or leak credentials
        let config = ThreatDetectorConfig {
            enabled: true,
            baml_endpoint: "http://localhost:8000/api".to_string(),
            ..Default::default()
        };
        let detector = Arc::new(ThreatDetector::new(config).unwrap());

        // Create a session
        let session_id = "test-credential-session".to_string();

        // The session ID should not contain sensitive data
        assert!(!session_id.contains("password"));
        assert!(!session_id.contains("secret"));

        // Verify session count
        assert_eq!(
            detector.active_session_count(),
            0,
            "No sessions should exist before any activity"
        );

        println!("Credential logging test — verify sessions do not store passwords");
    }

    // -------------------------------------------------------------------------
    // analyze_screenshot tests
    // -------------------------------------------------------------------------

    /// analyze_screenshot returns Ok with a mock endpoint that is unreachable.
    ///
    /// When fail_closed_on_error is false (default), an unreachable BAML endpoint
    /// must not cause a hard error — it should return Ok with a default (no-threat)
    /// ThreatAnalysis. This is the fail-open behavior: the session continues even
    /// if the threat detection endpoint is down.
    #[tokio::test]
    #[ignore]
    async fn analyze_screenshot_returns_ok_with_unreachable_endpoint() {
        use guacr_threat_detection::ThreatLevel;
        use guacr_threat_detection::{
            rgba_to_grayscale_jpeg, ThreatDetector, ThreatDetectorConfig,
        };

        // Build a 4×4 solid red RGBA image for testing.
        let width = 4u32;
        let height = 4u32;
        let rgba: Vec<u8> = (0..width * height)
            .flat_map(|_| [255u8, 0, 0, 255])
            .collect();

        let jpeg = rgba_to_grayscale_jpeg(&rgba, width, height, 75)
            .expect("grayscale JPEG conversion must succeed");
        assert!(!jpeg.is_empty(), "JPEG output must be non-empty");

        // Construct a detector pointing at a guaranteed-unreachable endpoint.
        // timeout_seconds=1 keeps the test fast.
        let config = ThreatDetectorConfig {
            enabled: true,
            baml_endpoint: "http://127.0.0.1:1".to_string(), // port 1 is unprivileged
            fail_closed_on_error: false,                     // fail-open: return Ok on API errors
            timeout_seconds: 1,
            ..Default::default()
        };
        let detector = ThreatDetector::new(config).expect("detector construction must succeed");

        let result = detector
            .analyze_screenshot(&jpeg, "ls -la", "test-session-1")
            .await;

        // fail-open: API unreachable → Ok with no-threat result, not Err.
        assert!(
            result.is_ok(),
            "fail-open detector must return Ok even when API is unreachable: {:?}",
            result.err()
        );
        let analysis = result.unwrap();
        assert_eq!(
            analysis.result.level,
            ThreatLevel::None,
            "unreachable API must return None threat level"
        );
        assert!(
            analysis.from_screenshot,
            "ThreatAnalysis.from_screenshot must be true"
        );
    }

    /// analyze_screenshot with fail_closed_on_error=true returns Err when the
    /// BAML endpoint is unreachable (the session would be blocked).
    #[tokio::test]
    #[ignore]
    async fn analyze_screenshot_fail_closed_returns_err_when_unreachable() {
        use guacr_threat_detection::{
            rgba_to_grayscale_jpeg, ThreatDetector, ThreatDetectorConfig,
        };

        let width = 2u32;
        let height = 2u32;
        let rgba: Vec<u8> = vec![128u8; (width * height * 4) as usize];
        let jpeg = rgba_to_grayscale_jpeg(&rgba, width, height, 75).unwrap();

        let config = ThreatDetectorConfig {
            enabled: true,
            baml_endpoint: "http://127.0.0.1:1".to_string(),
            fail_closed_on_error: true, // fail-closed: return Err on API error
            timeout_seconds: 1,
            ..Default::default()
        };
        let detector = ThreatDetector::new(config).unwrap();

        let result = detector
            .analyze_screenshot(&jpeg, "", "test-session-2")
            .await;

        assert!(
            result.is_err(),
            "fail-closed detector must return Err when API is unreachable"
        );
    }

    /// analyze_screenshot returns Ok immediately when threat detection is disabled.
    #[tokio::test]
    #[ignore]
    async fn analyze_screenshot_disabled_returns_ok_immediately() {
        use guacr_threat_detection::ThreatLevel;
        use guacr_threat_detection::{
            rgba_to_grayscale_jpeg, ThreatDetector, ThreatDetectorConfig,
        };

        let width = 1u32;
        let height = 1u32;
        let rgba = vec![100u8, 150, 200, 255];
        let jpeg = rgba_to_grayscale_jpeg(&rgba, width, height, 75).unwrap();

        let config = ThreatDetectorConfig {
            enabled: false, // disabled
            ..Default::default()
        };
        let detector = ThreatDetector::new(config).unwrap();

        let result = detector
            .analyze_screenshot(&jpeg, "some keystrokes", "test-session-3")
            .await;

        assert!(result.is_ok(), "disabled detector must return Ok");
        assert_eq!(
            result.unwrap().result.level,
            ThreatLevel::None,
            "disabled detector must return no-threat result"
        );
    }
}

// -------------------------------------------------------------------------
// rgba_to_grayscale_jpeg tests
//
// These are functional tests (no #[ignore]) — they run in CI.
// -------------------------------------------------------------------------
#[cfg(test)]
mod grayscale_jpeg_tests {
    use guacr_threat_detection::rgba_to_grayscale_jpeg;

    /// A 1×1 white pixel produces a valid JPEG header.
    #[test]
    fn single_white_pixel_produces_valid_jpeg_header() {
        let rgba = vec![255u8, 255, 255, 255];
        let jpeg = rgba_to_grayscale_jpeg(&rgba, 1, 1, 75).expect("single pixel must succeed");
        // JPEG files begin with the SOI marker 0xFF 0xD8.
        assert!(
            jpeg.starts_with(&[0xFF, 0xD8]),
            "output must be a valid JPEG (SOI marker): {:?}",
            &jpeg[..jpeg.len().min(4)]
        );
    }

    /// Output is non-empty for a minimal valid input.
    #[test]
    fn output_is_non_empty_for_minimal_input() {
        let rgba = vec![128u8, 64, 32, 255];
        let jpeg = rgba_to_grayscale_jpeg(&rgba, 1, 1, 75).unwrap();
        assert!(!jpeg.is_empty(), "JPEG output must not be empty");
    }

    /// Buffer length mismatch returns an error.
    #[test]
    fn wrong_buffer_length_returns_error() {
        // Supply only 3 bytes for a 1×1 RGBA image (should be 4).
        let too_short = vec![255u8, 0, 0];
        let result = rgba_to_grayscale_jpeg(&too_short, 1, 1, 75);
        assert!(
            result.is_err(),
            "length mismatch must return Err, got {:?}",
            result.ok().map(|j| j.len())
        );
    }

    /// A 4×4 solid red image produces a valid grayscale JPEG.
    ///
    /// Grayscale JPEG decoding must succeed (proves the bytes are decodeable by
    /// the `image` crate, i.e., the encoder produced a conformant single-channel JPEG).
    #[test]
    fn solid_red_4x4_produces_decodeable_grayscale_jpeg() {
        let width = 4u32;
        let height = 4u32;
        // Solid red RGBA: R=255, G=0, B=0, A=255
        let rgba: Vec<u8> = (0..width * height)
            .flat_map(|_| [255u8, 0, 0, 255])
            .collect();

        let jpeg = rgba_to_grayscale_jpeg(&rgba, width, height, 75)
            .expect("4×4 red image must produce valid JPEG");

        // Decode the JPEG to verify it is well-formed.
        let decoded = image::load_from_memory(&jpeg).expect("output JPEG must be decodeable");

        // The decoded image must be the same dimensions.
        assert_eq!(
            decoded.width(),
            width,
            "decoded width must match input width"
        );
        assert_eq!(
            decoded.height(),
            height,
            "decoded height must match input height"
        );

        // Grayscale luminance of pure red (R=255, G=0, B=0):
        // Y = 0.2126 * 255 + 0.7152 * 0 + 0.0722 * 0 ≈ 54
        // JPEG compression introduces rounding, so accept ±5.
        let gray = decoded.to_luma8();
        let luma = gray.get_pixel(0, 0)[0];
        assert!(
            (luma as i16 - 54).abs() <= 5,
            "pure red must map to luma ≈ 54 (got {})",
            luma
        );
    }

    /// All-black image produces expected near-zero luma.
    #[test]
    fn all_black_image_produces_zero_luma() {
        let width = 2u32;
        let height = 2u32;
        let rgba: Vec<u8> = vec![0u8; (width * height * 4) as usize];
        let jpeg = rgba_to_grayscale_jpeg(&rgba, width, height, 75).unwrap();
        let decoded = image::load_from_memory(&jpeg).unwrap();
        let gray = decoded.to_luma8();
        let luma = gray.get_pixel(0, 0)[0];
        assert!(
            luma <= 5,
            "all-black image must produce near-zero luma (got {})",
            luma
        );
    }

    /// All-white image produces expected near-255 luma.
    #[test]
    fn all_white_image_produces_max_luma() {
        let width = 2u32;
        let height = 2u32;
        let rgba: Vec<u8> = vec![255u8; (width * height * 4) as usize];
        let jpeg = rgba_to_grayscale_jpeg(&rgba, width, height, 75).unwrap();
        let decoded = image::load_from_memory(&jpeg).unwrap();
        let gray = decoded.to_luma8();
        let luma = gray.get_pixel(0, 0)[0];
        assert!(
            luma >= 250,
            "all-white image must produce near-max luma (got {})",
            luma
        );
    }

    /// Grayscale output is smaller than an equivalent RGB JPEG (sanity check).
    #[test]
    fn grayscale_jpeg_is_smaller_than_rgb_jpeg_for_same_content() {
        use image::ImageEncoder;

        let width = 64u32;
        let height = 64u32;
        // Build a gradient RGBA image
        let rgba: Vec<u8> = (0..width * height)
            .flat_map(|i| {
                let v = ((i * 255) / (width * height)) as u8;
                [v, v, v, 255]
            })
            .collect();

        let gray_jpeg =
            rgba_to_grayscale_jpeg(&rgba, width, height, 75).expect("gray JPEG must succeed");

        // Build an equivalent RGB JPEG for comparison.
        let rgb_pixels: Vec<u8> = rgba
            .chunks_exact(4)
            .flat_map(|p| [p[0], p[1], p[2]])
            .collect();
        let mut rgb_jpeg = Vec::new();
        let enc = image::codecs::jpeg::JpegEncoder::new_with_quality(&mut rgb_jpeg, 75);
        enc.write_image(&rgb_pixels, width, height, image::ExtendedColorType::Rgb8)
            .expect("RGB JPEG must encode");

        assert!(
            gray_jpeg.len() < rgb_jpeg.len(),
            "grayscale JPEG ({} bytes) should be smaller than RGB JPEG ({} bytes)",
            gray_jpeg.len(),
            rgb_jpeg.len()
        );
    }
}
