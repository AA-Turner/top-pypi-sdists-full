//! Tests for `scale_rgba`, the downscaler behind BWE resolution steps.

use crate::scale_rgba;

fn solid(w: usize, h: usize, px: [u8; 4]) -> Vec<u8> {
    px.iter()
        .copied()
        .cycle()
        .take(w * h * 4)
        .collect::<Vec<u8>>()
}

/// A solid-colour image must stay byte-identical at every tier percentage — the
/// bilinear weights are applied exactly, so no rounding drift is acceptable.
#[test]
fn solid_colour_survives_every_tier() {
    let src = solid(64, 48, [200, 150, 100, 255]);
    for pct in [75u32, 50, 33] {
        let (dw, dh) = apply_pct(64, 48, pct);
        let mut dst = Vec::new();
        scale_rgba(&src, 64, 48, &mut dst, dw, dh);
        assert_eq!(dst.len(), (dw * dh * 4) as usize);
        assert!(
            dst.chunks_exact(4).all(|p| p == [200, 150, 100, 255]),
            "solid colour drifted at {pct}%"
        );
    }
}

/// Mirror of guacr_handlers::video::scaled_encode_size's arithmetic for test
/// geometry (that helper lives in another crate; only the shape matters here).
fn apply_pct(w: u32, h: u32, pct: u32) -> (u32, u32) {
    let s = |v: u32| ((v as u64 * pct as u64 / 100) as u32).max(2) & !1;
    (s(w), s(h))
}

/// Equal dimensions must degrade to an exact copy.
#[test]
fn identity_scale_is_a_copy() {
    let src: Vec<u8> = (0..16u32 * 8 * 4).map(|i| (i % 251) as u8).collect();
    let mut dst = Vec::new();
    scale_rgba(&src, 16, 8, &mut dst, 16, 8);
    assert_eq!(dst, src);
}

/// A horizontal gradient must remain monotonically non-decreasing after scaling —
/// bilinear can smooth it but must never reorder it.
#[test]
fn gradient_stays_monotonic() {
    let (w, h) = (100usize, 4usize);
    let mut src = Vec::with_capacity(w * h * 4);
    for _ in 0..h {
        for x in 0..w {
            let v = (x * 255 / (w - 1)) as u8;
            src.extend_from_slice(&[v, v, v, 255]);
        }
    }
    let mut dst = Vec::new();
    scale_rgba(&src, 100, 4, &mut dst, 50, 2);
    let row: Vec<u8> = dst[..50 * 4].chunks_exact(4).map(|p| p[0]).collect();
    assert!(
        row.windows(2).all(|p| p[0] <= p[1]),
        "gradient reordered: {row:?}"
    );
}

/// The live geometry: 3292x1724 natural scaled to the 75% tier must produce the
/// even-rounded dimensions and the right buffer length. (Kept small by scaling a
/// same-aspect miniature; the arithmetic is what matters.)
#[test]
fn output_length_matches_requested_dimensions() {
    let src = solid(329, 172, [1, 2, 3, 4]);
    let mut dst = Vec::new();
    scale_rgba(&src, 329, 172, &mut dst, 246, 128);
    assert_eq!(dst.len(), 246 * 128 * 4);
}

/// Degenerate inputs leave dst empty instead of panicking: zero dimensions and a
/// source shorter than its claimed geometry.
#[test]
fn degenerate_inputs_do_not_panic() {
    let mut dst = vec![9u8; 4];
    scale_rgba(&[], 0, 0, &mut dst, 10, 10);
    assert!(dst.is_empty());

    let mut dst = Vec::new();
    scale_rgba(&[0u8; 16], 4, 4, &mut dst, 2, 2); // claims 4x4 but only 4 px given
    assert!(dst.is_empty());

    let mut dst = Vec::new();
    scale_rgba(&solid(4, 4, [7, 7, 7, 7]), 4, 4, &mut dst, 0, 0);
    assert!(dst.is_empty());
}

/// 2x2 downscaled to 1x1 with top-left-aligned sampling picks the top-left texel
/// exactly (fx = fy = 0). Pins the documented alignment so a future switch to
/// centre-aligned sampling is a deliberate change, not an accident.
#[test]
fn half_scale_of_two_by_two_picks_top_left_texel() {
    let src = [
        10, 10, 10, 255, 20, 20, 20, 255, //
        30, 30, 30, 255, 40, 40, 40, 255,
    ];
    let mut dst = Vec::new();
    scale_rgba(&src, 2, 2, &mut dst, 1, 1);
    assert_eq!(&dst[..], &[10, 10, 10, 255]);
}
