//! Tests for resolution-aware initial bitrate.
//!
//! Bitrate must track pixel count. Both backends previously hardcoded 3 Mbps, which made
//! quality fall off as resolution rose — measured 2026-08-03: 0.0519 bits/px at 1918x1004
//! versus 0.0176 at 3292x1724. Raising the resolution cap without this would look *worse*,
//! so these two have to move together.

use crate::initial_bitrate_bps;

/// The live clamped geometry must still land on ~3 Mbps, so making bitrate
/// resolution-aware is not a silent quality or bandwidth shift for sessions that
/// behave the way they do today.
#[test]
fn preserves_todays_rate_at_the_clamped_geometry() {
    let bps = initial_bitrate_bps(1918, 1004, 30);
    assert!(
        (2_900_000..=3_100_000).contains(&bps),
        "expected ~3 Mbps at 1918x1004, got {bps}"
    );
}

/// Native Retina has ~2.95x the pixels, so it needs ~2.95x the bits to hold quality.
#[test]
fn scales_up_for_native_retina() {
    let clamped = initial_bitrate_bps(1918, 1004, 30);
    let native = initial_bitrate_bps(3292, 1724, 30);
    let ratio = native as f64 / clamped as f64;
    assert!(
        (2.7..=3.2).contains(&ratio),
        "native should need ~2.95x the bitrate, got {ratio:.2}x ({clamped} -> {native})"
    );
}

/// Bits per pixel staying roughly constant across geometries is the whole point.
#[test]
fn holds_bits_per_pixel_roughly_constant() {
    for (w, h) in [(1280u32, 720u32), (1918, 1004), (2560, 1440)] {
        let bpp = initial_bitrate_bps(w, h, 30) as f64 / (w as f64 * h as f64 * 30.0);
        assert!(
            (0.045..=0.060).contains(&bpp),
            "{w}x{h}: bits/px {bpp:.4} drifted outside the target band"
        );
    }
}

/// Clamped at both ends: a tiny desktop still gets enough bits to look clean, and a huge
/// one cannot open by demanding tens of Mbps before any BWE feedback has arrived.
#[test]
fn is_clamped_at_both_ends() {
    assert_eq!(initial_bitrate_bps(320, 240, 30), 1_500_000);
    assert_eq!(initial_bitrate_bps(7680, 4320, 60), 12_000_000);
}

/// Degenerate inputs must not panic or divide by zero. fps 0 is treated as 1.
#[test]
fn handles_degenerate_input() {
    assert_eq!(initial_bitrate_bps(0, 0, 30), 1_500_000);
    assert_eq!(
        initial_bitrate_bps(1920, 1080, 0),
        initial_bitrate_bps(1920, 1080, 1),
        "fps 0 must be treated as 1, not divide by zero"
    );
}

/// Monotonic in pixel count within the unclamped band.
#[test]
fn is_monotonic_in_pixel_count() {
    let a = initial_bitrate_bps(1280, 720, 30);
    let b = initial_bitrate_bps(1918, 1004, 30);
    let c = initial_bitrate_bps(2560, 1440, 30);
    assert!(a < b && b < c, "expected {a} < {b} < {c}");
}
