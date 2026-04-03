use crate::framebuffer::{FrameBuffer, FrameRect};

#[test]
fn test_framebuffer_new() {
    let fb = FrameBuffer::new(1920, 1080);
    assert_eq!(fb.size(), (1920, 1080));
    assert_eq!(fb.dirty_rects().len(), 0);
}

#[test]
fn test_update_region() {
    let mut fb = FrameBuffer::new(100, 100);
    let pixels = vec![255u8; 10 * 10 * 4]; // 10x10 white pixels

    fb.update_region(10, 10, 10, 10, &pixels);

    assert_eq!(fb.dirty_rects().len(), 1);
    assert_eq!(fb.dirty_rects()[0].x, 10);
    assert_eq!(fb.dirty_rects()[0].y, 10);
    assert_eq!(fb.dirty_rects()[0].width, 10);
    assert_eq!(fb.dirty_rects()[0].height, 10);
}

#[test]
fn test_rect_intersects() {
    let rect1 = FrameRect {
        x: 10,
        y: 10,
        width: 20,
        height: 20,
    };
    let rect2 = FrameRect {
        x: 20,
        y: 20,
        width: 20,
        height: 20,
    };
    let rect3 = FrameRect {
        x: 50,
        y: 50,
        width: 10,
        height: 10,
    };

    assert!(rect1.intersects(&rect2));
    assert!(!rect1.intersects(&rect3));
}

#[test]
fn test_rect_union() {
    let rect1 = FrameRect {
        x: 10,
        y: 10,
        width: 20,
        height: 20,
    };
    let rect2 = FrameRect {
        x: 20,
        y: 20,
        width: 20,
        height: 20,
    };

    let union = rect1.union(&rect2);

    assert_eq!(union.x, 10);
    assert_eq!(union.y, 10);
    assert_eq!(union.width, 30);
    assert_eq!(union.height, 30);
}

#[test]
fn test_optimize_dirty_rects() {
    let mut fb = FrameBuffer::new(100, 100);
    let pixels = vec![255u8; 10 * 10 * 4];

    fb.update_region(10, 10, 10, 10, &pixels);
    fb.update_region(15, 15, 10, 10, &pixels); // Overlapping

    assert_eq!(fb.dirty_rects().len(), 2);

    fb.optimize_dirty_rects();

    assert_eq!(fb.dirty_rects().len(), 1); // Should be merged
}

#[test]
fn test_encode_region() {
    let mut fb = FrameBuffer::new(100, 100);
    let pixels = vec![255u8; 20 * 20 * 4];

    fb.update_region(10, 10, 20, 20, &pixels);

    let rect = fb.dirty_rects()[0];
    let png = fb.encode_region(rect);

    assert!(png.is_ok());
    let png_data = png.unwrap();
    assert!(!png_data.is_empty());
    // Check PNG signature
    assert_eq!(&png_data[0..8], b"\x89PNG\r\n\x1a\n");
}

// --- copy_region tests ---

/// Helper: read one RGBA pixel from framebuffer data.
fn get_pixel(data: &[u8], fb_width: u32, x: u32, y: u32) -> [u8; 4] {
    let offset = ((y * fb_width + x) * 4) as usize;
    [
        data[offset],
        data[offset + 1],
        data[offset + 2],
        data[offset + 3],
    ]
}

#[test]
fn test_copy_region_non_overlapping() {
    // Fill a 4x4 src region with red; dst starts black.
    // After copy, dst region should be red and src should still be red.
    let mut fb = FrameBuffer::new(20, 20);

    // Paint src region (0,0)-(4,4) red using update_region.
    let red_pixels: Vec<u8> = (0..4 * 4).flat_map(|_| [255u8, 0, 0, 255]).collect();
    fb.update_region(0, 0, 4, 4, &red_pixels);
    fb.clear_dirty();

    // Dst region is at (10, 10); it starts as all zeros (black).
    assert_eq!(get_pixel(fb.data(), 20, 10, 10), [0, 0, 0, 0]);

    fb.copy_region(0, 0, 10, 10, 4, 4);

    // Dst should now be red.
    assert_eq!(get_pixel(fb.data(), 20, 10, 10), [255, 0, 0, 255]);
    assert_eq!(get_pixel(fb.data(), 20, 13, 13), [255, 0, 0, 255]);

    // Src should still be red (unchanged).
    assert_eq!(get_pixel(fb.data(), 20, 0, 0), [255, 0, 0, 255]);
    assert_eq!(get_pixel(fb.data(), 20, 3, 3), [255, 0, 0, 255]);
}

#[test]
fn test_copy_region_overlapping() {
    // Copy a row 1 pixel down to verify overlap is handled correctly.
    // Fill row 0 (y=0) with distinct per-column values.
    let mut fb = FrameBuffer::new(8, 8);

    // Write 8 pixels on row 0 with unique red components (0..8).
    for col in 0u32..8 {
        let mut pix = vec![0u8; 4];
        pix[0] = col as u8; // unique R
        pix[1] = 0;
        pix[2] = 0;
        pix[3] = 255;
        fb.update_region(col, 0, 1, 1, &pix);
    }
    fb.clear_dirty();

    // Snapshot row 0 before the copy.
    let row0: Vec<[u8; 4]> = (0..8).map(|c| get_pixel(fb.data(), 8, c, 0)).collect();

    // Copy row 0 (src y=0) -> row 1 (dst y=1), same x, width 8, height 1.
    fb.copy_region(0, 0, 0, 1, 8, 1);

    // Row 1 must match the original row 0 values.
    for col in 0u32..8 {
        assert_eq!(
            get_pixel(fb.data(), 8, col, 1),
            row0[col as usize],
            "row 1, col {} should match original row 0",
            col
        );
    }

    // Row 0 must be unchanged.
    for col in 0u32..8 {
        assert_eq!(
            get_pixel(fb.data(), 8, col, 0),
            row0[col as usize],
            "row 0, col {} must be unchanged after copy",
            col
        );
    }
}

#[test]
fn test_copy_region_boundary_clamping_does_not_panic() {
    // src_x + width extends beyond the framebuffer; must not panic.
    let mut fb = FrameBuffer::new(10, 10);
    let red: Vec<u8> = (0..4).flat_map(|_| [255u8, 0, 0, 255]).collect();
    fb.update_region(0, 0, 2, 2, &red);
    fb.clear_dirty();

    // Request a copy that goes well beyond the right edge.
    fb.copy_region(8, 0, 8, 0, 100, 2); // should not panic
}

#[test]
fn test_copy_region_marks_dirty() {
    let mut fb = FrameBuffer::new(20, 20);
    let pixels: Vec<u8> = (0..4 * 4).flat_map(|_| [1u8, 2, 3, 255]).collect();
    fb.update_region(0, 0, 4, 4, &pixels);
    fb.clear_dirty();

    assert_eq!(
        fb.dirty_rects().len(),
        0,
        "dirty list should be empty before copy"
    );

    fb.copy_region(0, 0, 10, 10, 4, 4);

    assert_eq!(
        fb.dirty_rects().len(),
        1,
        "copy_region should mark dst rect dirty"
    );
    let dr = fb.dirty_rects()[0];
    assert_eq!(dr.x, 10);
    assert_eq!(dr.y, 10);
    assert_eq!(dr.width, 4);
    assert_eq!(dr.height, 4);
}
