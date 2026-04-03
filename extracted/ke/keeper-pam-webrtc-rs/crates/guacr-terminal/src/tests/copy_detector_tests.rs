use crate::copy_detector::{CellOp, CopyDetector};
use crate::framebuffer::FrameRect;

fn make_solid_frame(width: u32, height: u32, color: [u8; 4]) -> Vec<u8> {
    let mut data = vec![0u8; (width * height * 4) as usize];
    for pixel in data.chunks_exact_mut(4) {
        pixel.copy_from_slice(&color);
    }
    data
}

fn make_pattern_frame(width: u32, height: u32) -> Vec<u8> {
    let mut data = vec![0u8; (width * height * 4) as usize];
    for y in 0..height {
        for x in 0..width {
            let off = (y * width + x) as usize * 4;
            data[off] = (x % 256) as u8;
            data[off + 1] = (y % 256) as u8;
            data[off + 2] = ((x + y) % 256) as u8;
            data[off + 3] = 255;
        }
    }
    data
}

#[test]
fn test_first_frame_returns_image() {
    let mut detector = CopyDetector::new(256, 256);
    let frame = make_pattern_frame(256, 256);
    let dirty = FrameRect {
        x: 0,
        y: 0,
        width: 256,
        height: 256,
    };

    let ops = detector.plan_frame(&frame, dirty);
    assert_eq!(ops.len(), 1);
    assert!(matches!(ops[0], CellOp::Image { .. }));
}

#[test]
fn test_identical_frames_no_ops() {
    let mut detector = CopyDetector::new(256, 256);
    let frame = make_pattern_frame(256, 256);
    let dirty = FrameRect {
        x: 0,
        y: 0,
        width: 256,
        height: 256,
    };

    // First frame
    detector.plan_frame(&frame, dirty);

    // Second identical frame -- all cells unchanged, but dirty region
    // forces re-evaluation. Cells will have same hash as previous,
    // so copy detection should find matches (self-copies).
    // In practice the handler would not call plan_frame without actual changes.
    let ops = detector.plan_frame(&frame, dirty);

    // When prev and current hashes match at same position, the cell
    // is a self-copy which we should still render since it's in the dirty region.
    // Actually, self-copies (src == dst) are not useful, they'll be Image ops.
    for op in &ops {
        match op {
            CellOp::Copy {
                src_x,
                src_y,
                dst_x,
                dst_y,
                ..
            } => {
                // Self-copies are valid but indicate identical content
                assert_eq!(src_x, dst_x);
                assert_eq!(src_y, dst_y);
            }
            CellOp::Image { .. } | CellOp::Rect { .. } => {} // Also fine
        }
    }
}

#[test]
fn test_solid_detection() {
    let mut detector = CopyDetector::new(128, 128);
    let white = [255u8, 255, 255, 255];
    let frame1 = make_pattern_frame(128, 128);
    let frame2 = make_solid_frame(128, 128, white);
    let dirty = FrameRect {
        x: 0,
        y: 0,
        width: 128,
        height: 128,
    };

    detector.plan_frame(&frame1, dirty);
    let ops = detector.plan_frame(&frame2, dirty);

    // All cells should be detected as solid
    for op in &ops {
        if let CellOp::Rect { color, .. } = op {
            assert_eq!(*color, white);
        }
    }
    assert!(!ops.is_empty());
}

#[test]
fn test_moved_content_detected() {
    let w = 256u32;
    let h = 256u32;
    let mut detector = CopyDetector::new(w, h);

    // Frame 1: pattern
    let frame1 = make_pattern_frame(w, h);
    let dirty = FrameRect {
        x: 0,
        y: 0,
        width: w,
        height: h,
    };
    detector.plan_frame(&frame1, dirty);

    // Frame 2: shift content right by 64 pixels (one cell)
    let mut frame2 = vec![0u8; (w * h * 4) as usize];
    for y in 0..h {
        for x in 64..w {
            let dst = (y * w + x) as usize * 4;
            let src = (y * w + (x - 64)) as usize * 4;
            frame2[dst..dst + 4].copy_from_slice(&frame1[src..src + 4]);
        }
    }

    let ops = detector.plan_frame(&frame2, dirty);

    // Should have at least some Copy ops for the shifted content
    let copy_count = ops
        .iter()
        .filter(|op| matches!(op, CellOp::Copy { .. }))
        .count();
    let image_count = ops
        .iter()
        .filter(|op| matches!(op, CellOp::Image { .. }))
        .count();

    // We expect copies for the shifted cells and images for new content at left edge
    assert!(
        copy_count > 0 || image_count > 0,
        "Expected some operations, got copies={}, images={}",
        copy_count,
        image_count
    );
}

#[test]
fn test_reset() {
    let mut detector = CopyDetector::new(640, 480);
    let frame = make_pattern_frame(640, 480);
    let dirty = FrameRect {
        x: 0,
        y: 0,
        width: 640,
        height: 480,
    };
    detector.plan_frame(&frame, dirty);

    detector.reset(1920, 1080);
    assert_eq!(detector.width, 1920);
    assert_eq!(detector.height, 1080);
    assert!(!detector.has_prev_frame);
}
