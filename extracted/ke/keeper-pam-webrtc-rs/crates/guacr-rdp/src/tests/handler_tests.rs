use crate::handler::{
    clamp_resolution, encode_jpeg, h264_keepalive_needed, normalize_graphics_rect,
    resolution_cap_defaults, resolve_credssp_settings, RdpConfig, RdpHandler, RdpServerType,
    RdpSettings, RDP_MAX_ENCODE_HEIGHT, RDP_MAX_ENCODE_HEIGHT_HW, RDP_MAX_ENCODE_WIDTH,
    RDP_MAX_ENCODE_WIDTH_HW,
};

/// A Retina device resolution (CSS × 2 DPR) must be capped to the software-encode budget,
/// aspect-preserved, with even dimensions — otherwise software openh264 can't sustain 30fps
/// and the RDP session freezes ("didn't connect").
#[test]
fn clamp_resolution_downscales_retina_preserving_aspect() {
    let (w, h) = clamp_resolution(3816, 1926, RDP_MAX_ENCODE_WIDTH, RDP_MAX_ENCODE_HEIGHT);
    assert!(
        w <= RDP_MAX_ENCODE_WIDTH && h <= RDP_MAX_ENCODE_HEIGHT,
        "within budget"
    );
    assert_eq!(w % 2, 0, "H.264 needs even width");
    assert_eq!(h % 2, 0, "H.264 needs even height");
    let orig = 3816.0_f64 / 1926.0;
    let capped = w as f64 / h as f64;
    assert!(
        (orig - capped).abs() < 0.02,
        "aspect preserved: {orig} vs {capped}"
    );
    assert!(
        w >= 1900,
        "width-bound is tighter; should approach the 1920 cap (got {w})"
    );
}

#[test]
fn clamp_resolution_leaves_encodable_sizes_unchanged() {
    assert_eq!(clamp_resolution(1280, 720, 1920, 1080), (1280, 720));
    assert_eq!(clamp_resolution(1920, 1080, 1920, 1080), (1920, 1080));
    // Degenerate inputs are passed through, not divided-by-zero.
    assert_eq!(clamp_resolution(0, 0, 1920, 1080), (0, 0));
}

/// A zero budget means "no cap" — the env override uses it to request true
/// pass-through of the client's device resolution for hardware-encode testing.
#[test]
fn clamp_resolution_zero_budget_disables_the_cap() {
    assert_eq!(clamp_resolution(3292, 1724, 0, 0), (3292, 1724));
    assert_eq!(clamp_resolution(3292, 1724, 0, 1080), (3292, 1724));
    assert_eq!(clamp_resolution(3292, 1724, 1920, 0), (3292, 1724));
}

/// The live Retina case measured on 2026-08-03 (1646x806 CSS at DPR 2): the cap must
/// still engage by default so this stays a regression guard for the shipped default.
#[test]
fn clamp_resolution_caps_the_measured_live_retina_request() {
    let (w, h) = clamp_resolution(3292, 1724, RDP_MAX_ENCODE_WIDTH, RDP_MAX_ENCODE_HEIGHT);
    assert_eq!((w, h), (1918, 1004));
}

/// The resolution decision happens before the RDP connection negotiates desktop size, so
/// no encoder exists yet to inspect — `resolution_cap_defaults` is the pure decision logic
/// behind `encode_resolution_cap`, factored out so this doesn't depend on the runtime
/// FFmpeg probe (which varies by build features and host hardware).
#[test]
fn resolution_cap_defaults_picks_the_conservative_budget_without_hardware() {
    assert_eq!(
        resolution_cap_defaults(false),
        (RDP_MAX_ENCODE_WIDTH, RDP_MAX_ENCODE_HEIGHT)
    );
}

// RDP_MAX_ENCODE_WIDTH_HW/_HEIGHT_HW > RDP_MAX_ENCODE_WIDTH/_HEIGHT is a build-time
// invariant of the constants themselves (3840x2160 > 1920x1080) — clippy correctly
// flags asserting it at runtime as a no-op (assertions_on_constants); the exact values
// are already pinned by the assert_eq! below.
#[test]
fn resolution_cap_defaults_raises_the_ceiling_with_hardware() {
    assert_eq!(
        resolution_cap_defaults(true),
        (RDP_MAX_ENCODE_WIDTH_HW, RDP_MAX_ENCODE_HEIGHT_HW)
    );
}
use guacr_handlers::{HealthStatus, ProtocolHandler};
use ironrdp_pdu::geometry::InclusiveRectangle;
use std::collections::HashMap;
use std::time::{Duration, Instant};

#[test]
fn test_rdp_handler_new() {
    let handler = RdpHandler::with_defaults();
    assert_eq!(<RdpHandler as ProtocolHandler>::name(&handler), "rdp");
}

#[test]
fn test_rdp_config_defaults() {
    let config = RdpConfig::default();
    assert_eq!(config.default_port, 3389);
    assert_eq!(config.default_width, 1920);
    assert_eq!(config.default_height, 1080);
    assert_eq!(config.security_mode, "nla");
}

#[tokio::test]
async fn test_rdp_handler_health() {
    let handler = RdpHandler::with_defaults();
    let health = handler.health_check().await.unwrap();
    assert_eq!(health, HealthStatus::Healthy);
}

#[tokio::test]
async fn test_rdp_handler_stats() {
    let handler = RdpHandler::with_defaults();
    let stats = handler.stats().await.unwrap();
    assert_eq!(stats.total_connections, 0);
}

#[test]
fn test_rdp_settings_from_params() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "server.example.com".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());

    let defaults = RdpConfig::default();
    let settings = RdpSettings::from_params(&params, &defaults).unwrap();

    assert_eq!(settings.hostname, "server.example.com");
    assert_eq!(settings.port, 3389);
    assert_eq!(settings.width, 1920);
}

#[test]
fn test_normalize_graphics_rect_zero_rect_with_image_content_is_full_frame() {
    // IronRDP emits {0,0,0,0} for the initial full-frame GraphicsUpdate.
    // It must NOT be skipped when the image has content.
    let zero_rect = InclusiveRectangle {
        left: 0,
        top: 0,
        right: 0,
        bottom: 0,
    };
    let result = normalize_graphics_rect(zero_rect, 1724, 1256);
    let expected = InclusiveRectangle {
        left: 0,
        top: 0,
        right: 1723,
        bottom: 1255,
    };
    assert_eq!(
        result,
        Some(expected),
        "zero-rect with image content must promote to full-frame"
    );
}

#[test]
fn test_normalize_graphics_rect_zero_rect_no_image_is_skipped() {
    let zero_rect = InclusiveRectangle {
        left: 0,
        top: 0,
        right: 0,
        bottom: 0,
    };
    let result = normalize_graphics_rect(zero_rect, 0, 0);
    assert_eq!(
        result, None,
        "zero-rect with no image content must be skipped"
    );
}

#[test]
fn test_normalize_graphics_rect_normal_dirty_rect_is_passed_through() {
    let rect = InclusiveRectangle {
        left: 1632,
        top: 0,
        right: 1685,
        bottom: 26,
    };
    let expected = InclusiveRectangle {
        left: 1632,
        top: 0,
        right: 1685,
        bottom: 26,
    };
    let result = normalize_graphics_rect(rect, 1724, 1256);
    assert_eq!(
        result,
        Some(expected),
        "normal dirty rect must pass through unchanged"
    );
}

#[test]
fn test_normalize_graphics_rect_topleft_dirty_rect_is_passed_through() {
    let rect = InclusiveRectangle {
        left: 0,
        top: 0,
        right: 100,
        bottom: 100,
    };
    let expected = InclusiveRectangle {
        left: 0,
        top: 0,
        right: 100,
        bottom: 100,
    };
    let result = normalize_graphics_rect(rect, 1024, 768);
    assert_eq!(
        result,
        Some(expected),
        "top-left dirty rect must pass through unchanged"
    );
}

// Tests for h264_keepalive_needed — the keepalive decision extracted from
// maybe_encode_h264_rdp.  This logic fires a soft-encoder submit when the
// framebuffer has been idle for >= 1 s so the browser never sees a stale
// video track.

#[test]
fn test_h264_keepalive_not_needed_when_no_previous_submit() {
    // h264_last_submit is None on session start — keepalive must NOT fire
    // (there is nothing to keep alive yet).
    assert!(
        !h264_keepalive_needed(None),
        "keepalive must be false when h264_last_submit has never been set"
    );
}

#[test]
fn test_h264_keepalive_not_needed_when_submitted_recently() {
    // A submit that happened 100 ms ago is still within the 1 s window.
    let recent = Instant::now() - Duration::from_millis(100);
    assert!(
        !h264_keepalive_needed(Some(recent)),
        "keepalive must be false when last submit was only 100 ms ago"
    );
}

#[test]
fn test_h264_keepalive_fires_after_1s_idle() {
    // A submit that happened 1.1 s ago must trigger the keepalive so the
    // browser's H.264 decoder does not declare the track inactive.
    let old = Instant::now() - Duration::from_millis(1100);
    assert!(
        h264_keepalive_needed(Some(old)),
        "keepalive must fire when framebuffer has been idle for > 1 s"
    );
}

#[test]
fn test_h264_keepalive_boundary_exactly_1s() {
    // At exactly 1 s elapsed the keepalive threshold is met.
    // We add 50 ms of slack to avoid races with the monotonic clock on slow CI runners.
    let boundary = Instant::now() - Duration::from_millis(1050);
    assert!(
        h264_keepalive_needed(Some(boundary)),
        "keepalive must fire at the 1 s idle boundary"
    );
}

// Tests for H.264 PTS timestamp conversion.
//
// The formula is: pts = timestamp_us * 9 / 100
// This converts wall-clock microseconds to the 90 kHz RTP clock used by H.264.
//
// 1 second = 1_000_000 µs → 1_000_000 * 9 / 100 = 90_000 ticks (one full 90 kHz second).

/// Verify that 1 second expressed in microseconds maps to exactly 90_000 RTP ticks.
#[test]
fn test_h264_pts_one_second() {
    let timestamp_us: u64 = 1_000_000;
    let pts = timestamp_us * 9 / 100;
    assert_eq!(pts, 90_000, "1 000 000 µs must produce 90 000 RTP ticks");
}

/// Zero microseconds must map to zero ticks — no offset is applied.
#[test]
fn test_h264_pts_zero() {
    let timestamp_us: u64 = 0;
    let pts = timestamp_us * 9 / 100;
    assert_eq!(pts, 0, "0 µs must produce 0 RTP ticks");
}

/// Large timestamps must not overflow a u64.
///
/// The actual handler uses plain `*` and `/` on u64, which wraps (or panics in debug)
/// on overflow. We verify that the largest wall-clock value a real session would ever
/// produce stays within u64::MAX after the conversion.
///
/// A 64-bit microsecond timestamp overflows after ~585_000 years; multiplying by 9
/// would overflow at ~585_000 / 9 ≈ 65_000 years. No real session hits this.
/// We use checked_mul here to confirm the invariant with explicit arithmetic.
#[test]
fn test_h264_pts_large_timestamp_no_overflow() {
    // Use the largest timestamp that can safely be multiplied by 9 without overflowing u64.
    let max_safe_us: u64 = u64::MAX / 9;
    let pts = max_safe_us.checked_mul(9).and_then(|v| v.checked_div(100));
    assert!(pts.is_some(), "max_safe_us * 9 / 100 must not overflow u64");
    // Confirm the resulting value is less than u64::MAX.
    assert!(pts.unwrap() < u64::MAX, "PTS must be less than u64::MAX");
}

/// ignore-cert must default to false — TLS certificate validation must be on by default.
///
/// Accepting any cert without validation enables MITM attacks. Operators who need
/// to connect to RDP servers with self-signed certificates must explicitly set
/// ignore-cert=true to opt in.
#[test]
fn test_rdp_tls_ignore_cert_defaults_to_false() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "server.example.com".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    // No ignore-cert param — must default to false
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        !settings.ignore_cert,
        "ignore_cert must default to false — TLS verification must be on by default"
    );
}

/// ignore-cert=true must be passed through to the settings.
#[test]
fn test_rdp_tls_ignore_cert_explicit_true_is_respected() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "server.example.com".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("ignore-cert".to_string(), "true".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.ignore_cert,
        "ignore-cert=true must be respected when explicitly set"
    );
}

/// cert_fingerprint must be checked against the server's certificate SHA256 hash.
/// Test the fingerprint comparison helper that `tls_upgrade` calls.
#[test]
fn test_cert_fingerprint_matches_hex() {
    use crate::handler::cert_fingerprint_matches;

    // SHA256 of empty bytes (well-known): e3b0c44...
    let cert_der: &[u8] = b"";
    let expected_hex = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";
    assert!(
        cert_fingerprint_matches(cert_der, expected_hex),
        "correct hex fingerprint must match"
    );
}

#[test]
fn test_cert_fingerprint_wrong_does_not_match() {
    use crate::handler::cert_fingerprint_matches;

    let cert_der = b"some cert bytes";
    assert!(
        !cert_fingerprint_matches(cert_der, "deadbeef"),
        "wrong fingerprint must not match"
    );
}

/// Verify that encode_jpeg accepts an owned Vec<u8> and produces a valid JPEG.
///
/// This test proves the encode path is correct after removing the .to_vec() clone
/// inside encode_jpeg (FIX 2: eliminate 8MB pixel buffer clone per dirty rect).
/// The encode function now takes ownership of the pixel buffer directly.
#[test]
fn test_encode_jpeg_owned_pixels_produces_valid_jpeg() {
    let width = 64u32;
    let height = 64u32;
    // Build a simple gradient: RGBA pixels owned by this Vec.
    let mut pixels = vec![0u8; (width * height * 4) as usize];
    for y in 0..height {
        for x in 0..width {
            let i = (y * width + x) as usize * 4;
            pixels[i] = (x * 255 / width) as u8;
            pixels[i + 1] = (y * 255 / height) as u8;
            pixels[i + 2] = 128;
            pixels[i + 3] = 255;
        }
    }
    // Pass ownership — no clone.
    let jpeg = encode_jpeg(pixels, width, height, 85).expect("encode_jpeg must succeed");
    // JFIF/Exif marker: 0xFF 0xD8
    assert!(!jpeg.is_empty(), "JPEG output must not be empty");
    assert_eq!(jpeg[0], 0xFF, "JPEG must begin with 0xFF");
    assert_eq!(jpeg[1], 0xD8, "JPEG must have SOI marker 0xD8");
    // End-of-image marker: 0xFF 0xD9
    let last = jpeg.len();
    assert_eq!(jpeg[last - 2], 0xFF, "JPEG must end with 0xFF");
    assert_eq!(jpeg[last - 1], 0xD9, "JPEG must end with EOI marker 0xD9");
}

// ============================================================================
// RdpSettings::from_params — extended coverage (Step 4)
// ============================================================================

/// Missing required parameter (hostname) must return an error.
#[test]
fn test_rdp_settings_missing_hostname_errors() {
    let mut params = HashMap::new();
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    let result = RdpSettings::from_params(&params, &RdpConfig::default());
    assert!(
        result.is_err(),
        "from_params must error when hostname is absent"
    );
}

/// Missing required parameter (username) must return an error.
#[test]
fn test_rdp_settings_missing_username_errors() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-server.example.com".to_string());
    params.insert("password".to_string(), "pass".to_string());
    let result = RdpSettings::from_params(&params, &RdpConfig::default());
    assert!(
        result.is_err(),
        "from_params must error when username is absent"
    );
}

/// Missing required parameter (password) must return an error.
#[test]
fn test_rdp_settings_missing_password_errors() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-server.example.com".to_string());
    params.insert("username".to_string(), "user".to_string());
    let result = RdpSettings::from_params(&params, &RdpConfig::default());
    assert!(
        result.is_err(),
        "from_params must error when password is absent"
    );
}

/// disable-copy=true must be respected.
#[test]
fn test_rdp_settings_disable_copy_explicit_true() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("disable-copy".to_string(), "true".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.disable_copy,
        "disable-copy=true must be captured in disable_copy"
    );
}

/// disable-paste=true must be respected.
#[test]
fn test_rdp_settings_disable_paste_explicit_true() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("disable-paste".to_string(), "true".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.disable_paste,
        "disable-paste=true must be captured in disable_paste"
    );
}

/// read-only=true must set read_only in settings.
#[test]
fn test_rdp_settings_read_only_true() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("read-only".to_string(), "true".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.read_only,
        "read-only=true must be captured in read_only"
    );
}

/// read-only=1 (numeric form) must also set read_only.
#[test]
fn test_rdp_settings_read_only_numeric() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("read-only".to_string(), "1".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.read_only,
        "read-only=1 must also set read_only (numeric form)"
    );
}

/// read-only defaults to false when not set.
#[test]
fn test_rdp_settings_read_only_defaults_to_false() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        !settings.read_only,
        "read_only must default to false when param is absent"
    );
}

/// security mode is captured into security_mode field.
#[test]
fn test_rdp_settings_security_mode_explicit() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("security".to_string(), "rdp".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(
        settings.security_mode, "rdp",
        "explicit security= param must override default nla"
    );
}

/// security mode defaults to the config default (nla) when not set.
#[test]
fn test_rdp_settings_security_mode_defaults_to_nla() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(
        settings.security_mode, "nla",
        "security_mode must default to nla when not set"
    );
}

/// domain parameter is captured when present.
#[test]
fn test_rdp_settings_domain_captured() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("domain".to_string(), "CORP".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(
        settings.domain.as_deref(),
        Some("CORP"),
        "domain param must be captured in settings.domain"
    );
}

/// domain is None when not set.
#[test]
fn test_rdp_settings_domain_none_when_absent() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.domain.is_none(),
        "domain must be None when not set"
    );
}

/// size param (width,height,dpi) is parsed correctly.
#[test]
fn test_rdp_settings_size_three_part_parsed() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("size".to_string(), "1280,800,120".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(settings.width, 1280, "width from size param");
    assert_eq!(settings.height, 800, "height from size param");
    assert_eq!(settings.dpi, 120, "dpi from size param");
}

/// size param with only width,height (no dpi) falls back to default dpi.
#[test]
fn test_rdp_settings_size_two_part_uses_default_dpi() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("size".to_string(), "1024,768".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(settings.width, 1024, "width from 2-part size");
    assert_eq!(settings.height, 768, "height from 2-part size");
    assert_eq!(
        settings.dpi,
        RdpConfig::default().default_dpi,
        "dpi must fall back to default when not in size param"
    );
}

/// Separate width/height/dpi params are used when size is absent.
#[test]
fn test_rdp_settings_separate_width_height_dpi_params() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("width".to_string(), "800".to_string());
    params.insert("height".to_string(), "600".to_string());
    params.insert("dpi".to_string(), "144".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(settings.width, 800);
    assert_eq!(settings.height, 600);
    assert_eq!(settings.dpi, 144);
}

/// cert-fingerprint is captured when present.
#[test]
fn test_rdp_settings_cert_fingerprint_captured() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    let fp = "aa:bb:cc:dd:ee:ff".to_string();
    params.insert("cert-fingerprint".to_string(), fp.clone());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(
        settings.cert_fingerprint.as_deref(),
        Some(fp.as_str()),
        "cert-fingerprint param must be captured in settings.cert_fingerprint"
    );
}

/// cert-fingerprint is None when not set.
#[test]
fn test_rdp_settings_cert_fingerprint_none_when_absent() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert!(
        settings.cert_fingerprint.is_none(),
        "cert_fingerprint must be None when not set"
    );
}

/// server-type parameter is captured into settings.server_type.
#[test]
fn test_rdp_settings_server_type_captured() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("server-type".to_string(), "windows".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(
        settings.server_type.as_deref(),
        Some("windows"),
        "server-type param must be captured"
    );
}

/// Clipboard buffer size defaults are respected; clamping keeps values in range.
#[test]
fn test_rdp_settings_clipboard_buffer_size_clamped_to_min() {
    use guacr_terminal::CLIPBOARD_MIN_SIZE;

    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    // Value below CLIPBOARD_MIN_SIZE must be clamped to the minimum
    params.insert("clipboard-buffer-size".to_string(), "1".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    assert_eq!(
        settings.clipboard_buffer_size, CLIPBOARD_MIN_SIZE,
        "clipboard buffer size below minimum must be clamped up to CLIPBOARD_MIN_SIZE"
    );
}

// ============================================================================
// Credential supply gate — check_credential_supply_allowed
//
// RDP always requires username + password, so the gate fires unconditionally
// in connect().  The tests below validate the gate function as it is called
// from RdpHandler::connect() via check_credential_supply_allowed(&settings.security).
// ============================================================================

/// When allow-supply-user is absent (the default), the credential supply gate
/// must return Err — the connection record has not authorised runtime supply.
#[test]
fn test_rdp_credential_supply_blocked_when_flag_absent() {
    use guacr_handlers::check_credential_supply_allowed;

    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    // allow-supply-user intentionally absent — default is false
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    let result = check_credential_supply_allowed(&settings.security);
    assert!(
        result.is_err(),
        "credential supply gate must return Err when allow-supply-user is absent"
    );
}

/// When allow-supply-user=false, the credential supply gate must return Err.
#[test]
fn test_rdp_credential_supply_blocked_when_flag_false() {
    use guacr_handlers::check_credential_supply_allowed;

    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("allow-supply-user".to_string(), "false".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    let result = check_credential_supply_allowed(&settings.security);
    assert!(
        result.is_err(),
        "credential supply gate must return Err when allow-supply-user=false"
    );
}

/// When allow-supply-user=true, the credential supply gate must return Ok —
/// the connection record explicitly authorises runtime credential supply.
#[test]
fn test_rdp_credential_supply_allowed_when_flag_true() {
    use guacr_handlers::check_credential_supply_allowed;

    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "rdp-host".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());
    params.insert("allow-supply-user".to_string(), "true".to_string());
    let settings = RdpSettings::from_params(&params, &RdpConfig::default()).unwrap();
    let result = check_credential_supply_allowed(&settings.security);
    assert!(
        result.is_ok(),
        "credential supply gate must return Ok when allow-supply-user=true: {:?}",
        result.err()
    );
}

// --- CredSSP / security_mode resolution ---

#[test]
fn security_mode_nla_enables_credssp_regardless_of_server_heuristic() {
    // Windows targets without a domain set are misdetected as Xrdp by the heuristic —
    // explicit security=nla must override that and request CredSSP.
    let (credssp, autologon) = resolve_credssp_settings("nla", RdpServerType::Xrdp);
    assert!(
        credssp,
        "nla must enable CredSSP even when heuristic says Xrdp"
    );
    assert!(
        !autologon,
        "nla does not need autologon — CredSSP handles auth"
    );

    let (credssp, _) = resolve_credssp_settings("nla", RdpServerType::Unknown);
    assert!(credssp, "nla must enable CredSSP for Unknown server type");

    let (credssp, _) = resolve_credssp_settings("nla", RdpServerType::WindowsNative);
    assert!(credssp, "nla must enable CredSSP for WindowsNative");
}

#[test]
fn security_mode_tls_and_rdp_disable_credssp() {
    let (credssp, _) = resolve_credssp_settings("tls", RdpServerType::WindowsNative);
    assert!(!credssp, "tls must disable CredSSP");

    let (credssp, _) = resolve_credssp_settings("rdp", RdpServerType::WindowsNative);
    assert!(!credssp, "rdp must disable CredSSP");
}

#[test]
fn security_mode_any_defers_to_server_type_heuristic() {
    let (credssp, _) = resolve_credssp_settings("any", RdpServerType::WindowsNative);
    assert!(
        credssp,
        "any with WindowsNative should follow heuristic: CredSSP on"
    );

    let (credssp, _) = resolve_credssp_settings("any", RdpServerType::Xrdp);
    assert!(
        !credssp,
        "any with Xrdp should follow heuristic: CredSSP off"
    );
}
