//! Tests for the aligned-row RGBA copy used by the FFmpeg backend.
//!
//! These run on every build, including ones without the `ffmpeg` feature — the feature
//! is compiled by nothing in CI, so the stride logic would otherwise be untested.

use crate::copy_rgba_rows;

/// Align `n` up to a multiple of `align`, matching av_frame_get_buffer's row padding.
fn align_up(n: usize, align: usize) -> usize {
    n.div_ceil(align) * align
}

/// Each source row must land at its own stride offset, leaving the pad bytes untouched.
/// A flat copy would place row N at N*row_bytes instead of N*stride, shifting every row
/// after the first — the shear this function exists to prevent.
#[test]
fn rows_land_on_stride_boundaries_when_padded() {
    let (rows, row_bytes, stride) = (4usize, 12usize, 16usize);
    let src: Vec<u8> = (0..rows)
        .flat_map(|r| std::iter::repeat_n(r as u8 + 1, row_bytes))
        .collect();
    let mut dst = vec![0u8; stride * rows];

    copy_rgba_rows(&mut dst, stride, &src, row_bytes);

    for r in 0..rows {
        let start = r * stride;
        assert!(
            dst[start..start + row_bytes]
                .iter()
                .all(|&b| b == r as u8 + 1),
            "row {r} must sit at offset {start}"
        );
        assert!(
            dst[start + row_bytes..start + stride]
                .iter()
                .all(|&b| b == 0),
            "row {r} padding must be left untouched"
        );
    }
}

/// The exact geometry measured live on 2026-08-03: the vault requested 3292x1724 at DPR 2
/// and clamp_resolution produced 1918x1004. 1918*4 = 7672 bytes per row, which pads to
/// 7680 under 32-byte alignment — so this is the real-world case that sheared.
#[test]
fn live_rdp_geometry_1918_is_a_padded_stride_case() {
    let (w, h) = (1918usize, 4usize); // 4 rows is enough; width is what matters
    let row_bytes = w * 4;
    let stride = align_up(row_bytes, 32);
    assert_eq!(row_bytes, 7672);
    assert_eq!(
        stride, 7680,
        "1918 is not a multiple of 8, so rows get padded"
    );

    let src: Vec<u8> = (0..h)
        .flat_map(|r| std::iter::repeat_n(r as u8 + 1, row_bytes))
        .collect();
    let mut dst = vec![0u8; stride * h];

    copy_rgba_rows(&mut dst, stride, &src, row_bytes);

    for r in 0..h {
        let start = r * stride;
        assert!(
            dst[start..start + row_bytes]
                .iter()
                .all(|&b| b == r as u8 + 1),
            "row {r} misplaced — this is the shear bug"
        );
    }
}

/// A width that is a multiple of 8 needs no padding, so the fast path must be byte-exact.
/// 1280x720 (the pre-existing hardware test's geometry) is this case, which is why that
/// test could pass while the bug was live.
#[test]
fn unpadded_stride_copies_exactly() {
    let row_bytes = 1280 * 4;
    let stride = align_up(row_bytes, 32);
    assert_eq!(stride, row_bytes, "1280 needs no row padding");

    let src: Vec<u8> = (0..row_bytes * 3).map(|i| (i % 251) as u8).collect();
    let mut dst = vec![0u8; src.len()];
    copy_rgba_rows(&mut dst, stride, &src, row_bytes);
    assert_eq!(dst, src);
}

/// A destination shorter than the source implies must stop cleanly, not panic.
#[test]
fn short_destination_does_not_panic() {
    let (row_bytes, stride) = (12usize, 16usize);
    let src = vec![7u8; row_bytes * 8];
    let mut dst = vec![0u8; stride * 2];
    copy_rgba_rows(&mut dst, stride, &src, row_bytes);
    assert!(dst[..row_bytes].iter().all(|&b| b == 7));
}

/// Degenerate input is a no-op rather than a divide-by-zero or panic.
#[test]
fn zero_row_bytes_is_a_noop() {
    let mut dst = vec![9u8; 8];
    copy_rgba_rows(&mut dst, 0, &[1, 2, 3], 0);
    assert_eq!(dst, vec![9u8; 8]);
}
