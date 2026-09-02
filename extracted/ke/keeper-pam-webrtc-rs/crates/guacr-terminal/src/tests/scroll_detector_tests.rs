use crate::scroll_detector::{ScrollDetector, ScrollDirection};

/// Create a test framebuffer filled with a pattern
fn create_test_framebuffer(width: u32, height: u32, pattern: u8) -> Vec<u8> {
    let size = (width * height * 4) as usize;
    let mut buffer = vec![0u8; size];

    // Fill with pattern (VERY different for each row to avoid false matches)
    for row in 0..height {
        let row_offset = (row * width * 4) as usize;
        // Use row number prominently in the pattern to make rows VERY distinct
        let row_id = row.to_le_bytes();
        for pixel in 0..width {
            let pixel_offset = row_offset + (pixel * 4) as usize;
            // Encode row number in every pixel so rows are unmistakably unique
            buffer[pixel_offset] = row_id[0].wrapping_add(pattern); // B
            buffer[pixel_offset + 1] = row_id[1].wrapping_add(pattern); // G
            buffer[pixel_offset + 2] = row_id[2].wrapping_add(pattern); // R
            buffer[pixel_offset + 3] = row_id[3].wrapping_add(pattern); // A
        }
    }

    buffer
}

/// Create a scrolled version of a framebuffer
fn scroll_framebuffer(
    original: &[u8],
    width: u32,
    height: u32,
    scroll_pixels: u32,
    direction: ScrollDirection,
) -> Vec<u8> {
    let stride = (width * 4) as usize;
    let mut scrolled = vec![0u8; original.len()];

    match direction {
        ScrollDirection::Up => {
            // Content moves up: copy rows [scroll_pixels..height] to [0..height-scroll_pixels]
            for row in scroll_pixels..height {
                let src_offset = (row * width * 4) as usize;
                let dst_offset = ((row - scroll_pixels) * width * 4) as usize;
                scrolled[dst_offset..dst_offset + stride]
                    .copy_from_slice(&original[src_offset..src_offset + stride]);
            }
            // New content at bottom (fill with different pattern)
            for row in (height - scroll_pixels)..height {
                let offset = (row * width * 4) as usize;
                for i in 0..stride {
                    scrolled[offset + i] = 0xFF; // New content
                }
            }
        }
        ScrollDirection::Down => {
            // Content moves down: copy rows [0..height-scroll_pixels] to [scroll_pixels..height]
            for row in 0..(height - scroll_pixels) {
                let src_offset = (row * width * 4) as usize;
                let dst_offset = ((row + scroll_pixels) * width * 4) as usize;
                scrolled[dst_offset..dst_offset + stride]
                    .copy_from_slice(&original[src_offset..src_offset + stride]);
            }
            // New content at top (fill with different pattern)
            for row in 0..scroll_pixels {
                let offset = (row * width * 4) as usize;
                for i in 0..stride {
                    scrolled[offset + i] = 0xFF; // New content
                }
            }
        }
    }

    scrolled
}

#[test]
fn test_scroll_up_detection() {
    let width = 800;
    let height = 600;
    let mut detector = ScrollDetector::new(width, height);

    // Create initial framebuffer
    let fb1 = create_test_framebuffer(width, height, 0x10);

    // Initialize detector with first frame
    detector.detect_scroll(&fb1);

    // Create scrolled framebuffer (scroll up by 20 pixels)
    let fb2 = scroll_framebuffer(&fb1, width, height, 20, ScrollDirection::Up);

    // Detect scroll
    let scroll = detector.detect_scroll(&fb2);
    assert!(scroll.is_some());

    let scroll = scroll.unwrap();
    assert_eq!(scroll.direction, ScrollDirection::Up);
    assert_eq!(scroll.pixels, 20);
}

#[test]
fn test_scroll_down_detection() {
    let width = 800;
    let height = 600;
    let mut detector = ScrollDetector::new(width, height);

    // Create initial framebuffer
    let fb1 = create_test_framebuffer(width, height, 0x20);

    // Initialize detector
    detector.detect_scroll(&fb1);

    // Create scrolled framebuffer (scroll down by 15 pixels)
    let fb2 = scroll_framebuffer(&fb1, width, height, 15, ScrollDirection::Down);

    // Detect scroll
    let scroll = detector.detect_scroll(&fb2);
    assert!(scroll.is_some());

    let scroll = scroll.unwrap();
    assert_eq!(scroll.direction, ScrollDirection::Down);
    assert_eq!(scroll.pixels, 15);
}

#[test]
fn test_no_scroll_detection() {
    let width = 800;
    let height = 600;
    let mut detector = ScrollDetector::new(width, height);

    // Create initial framebuffer
    let fb1 = create_test_framebuffer(width, height, 0x30);

    // Initialize detector
    detector.detect_scroll(&fb1);

    // Create completely different framebuffer (not a scroll)
    let fb2 = create_test_framebuffer(width, height, 0x40);

    // Should not detect scroll
    let scroll = detector.detect_scroll(&fb2);
    assert!(scroll.is_none());
}

#[test]
fn test_reset() {
    let mut detector = ScrollDetector::new(800, 600);

    detector.reset(1024, 768);

    assert_eq!(detector.dimensions(), (1024, 768));
    assert_eq!(detector.row_hashes.len(), 768);
}

#[test]
fn test_large_scroll() {
    let width = 800;
    let height = 600;
    let mut detector = ScrollDetector::new(width, height);

    // Create initial framebuffer
    let fb1 = create_test_framebuffer(width, height, 0x50);

    // Initialize detector
    detector.detect_scroll(&fb1);

    // Create framebuffer with very large scroll (>50% of screen)
    let fb2 = scroll_framebuffer(&fb1, width, height, 400, ScrollDirection::Up);

    // Should not detect (too large)
    let scroll = detector.detect_scroll(&fb2);
    assert!(scroll.is_none());
}
