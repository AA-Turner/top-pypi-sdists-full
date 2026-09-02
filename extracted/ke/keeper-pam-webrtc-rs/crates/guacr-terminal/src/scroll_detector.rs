//! RDP Scroll Detection
//!
//! Detects scroll operations in RDP framebuffer to optimize bandwidth using copy instructions.
//! Unlike terminal scroll detection (which uses cell hashing), RDP scroll detection uses
//! pixel-level comparison of framebuffer rows.
//!
//! ## Algorithm
//!
//! 1. Compare current framebuffer with previous framebuffer
//! 2. Detect if most rows shifted up/down by N pixels
//! 3. If scroll detected, use `copy` instruction instead of re-encoding
//! 4. Only encode the new content (scrolled-in region)
//!
//! ## Performance
//!
//! - Scroll up/down: 90%+ bandwidth savings (copy is tiny, only encode new line)
//! - Non-scroll: No overhead (fast row hash comparison)

use std::collections::HashMap;

/// Scroll direction
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ScrollDirection {
    Up,   // Content moved up (new content at bottom)
    Down, // Content moved down (new content at top)
}

/// Detected scroll operation
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ScrollOperation {
    pub direction: ScrollDirection,
    pub pixels: u32, // Number of pixels scrolled
}

/// Scroll detector for RDP framebuffer
///
/// Uses row hashing to quickly detect if content shifted vertically.
/// Much faster than full pixel comparison.
pub struct ScrollDetector {
    /// Hash of each row in the previous frame
    pub(crate) row_hashes: Vec<u64>,
    /// Width of framebuffer in pixels
    width: u32,
    /// Height of framebuffer in pixels
    height: u32,
    /// Bytes per pixel (4 for BGRA32)
    bytes_per_pixel: u32,
}

impl ScrollDetector {
    /// Create a new scroll detector
    pub fn new(width: u32, height: u32) -> Self {
        Self {
            row_hashes: vec![0; height as usize],
            width,
            height,
            bytes_per_pixel: 4, // BGRA32
        }
    }

    /// Detect scroll operation by comparing current framebuffer with previous
    ///
    /// Returns Some(ScrollOperation) if scrolling detected, None otherwise.
    ///
    /// ## Algorithm
    ///
    /// 1. Hash each row of current framebuffer
    /// 2. Compare with previous row hashes to find matches
    /// 3. If most rows shifted by same amount, it's a scroll
    /// 4. Update row hashes for next frame
    ///
    /// ## Heuristics
    ///
    /// - Must have >70% row matches (not a full screen change)
    /// - Scroll distance must be consistent (same shift for most rows)
    /// - Scroll distance must be reasonable (1-50% of screen height)
    pub fn detect_scroll(&mut self, framebuffer: &[u8]) -> Option<ScrollOperation> {
        if framebuffer.len() != (self.width * self.height * self.bytes_per_pixel) as usize {
            return None;
        }

        // Hash each row of current framebuffer
        let mut current_hashes = Vec::with_capacity(self.height as usize);
        for row in 0..self.height {
            let hash = self.hash_row(framebuffer, row);
            current_hashes.push(hash);
        }

        // Find where each current row came from in previous frame
        // Map: current_row -> previous_row
        let mut matches: HashMap<u32, u32> = HashMap::new();

        for current_row in 0..self.height {
            let current_hash = current_hashes[current_row as usize];

            // Look for matching row in previous frame (within reasonable scroll distance)
            let max_scroll = (self.height / 2).min(500); // Max 50% of screen or 500 pixels

            for prev_row in 0..self.height {
                // Only consider matches within reasonable scroll distance
                let distance = (current_row as i32 - prev_row as i32).unsigned_abs();
                if distance > max_scroll {
                    continue;
                }

                if current_hash == self.row_hashes[prev_row as usize] && current_hash != 0 {
                    matches.insert(current_row, prev_row);
                    break;
                }
            }
        }

        // Analyze matches to detect scroll
        let scroll_op = self.analyze_matches(&matches);

        // Update row hashes for next frame
        self.row_hashes = current_hashes;

        scroll_op
    }

    /// Analyze row matches to detect scroll operation
    ///
    /// Returns Some(ScrollOperation) if consistent scroll detected.
    fn analyze_matches(&self, matches: &HashMap<u32, u32>) -> Option<ScrollOperation> {
        if matches.is_empty() {
            return None;
        }

        // Calculate shift for each match (current_row - prev_row)
        // Negative shift = scroll up (content moved up, row 0 now has what was in row 20)
        // Positive shift = scroll down (content moved down, row 20 now has what was in row 0)
        let mut shifts: HashMap<i32, u32> = HashMap::new(); // shift -> count

        for (current_row, prev_row) in matches.iter() {
            let shift = *current_row as i32 - *prev_row as i32;
            *shifts.entry(shift).or_insert(0) += 1;
        }

        // Find most common shift
        let (most_common_shift, shift_count) = shifts
            .iter()
            .max_by_key(|(_, count)| *count)
            .map(|(shift, count)| (*shift, *count))?;

        // Check if enough rows have the same shift (>70% of matched rows)
        let match_percentage = (shift_count * 100) / matches.len() as u32;
        if match_percentage < 70 {
            return None; // Not a consistent scroll
        }

        // Check if enough total rows matched (>50% of screen)
        let total_match_percentage = (matches.len() * 100) / self.height as usize;
        if total_match_percentage < 50 {
            return None; // Too much changed, not a scroll
        }

        // Check if shift is reasonable (not zero, not too large)
        if most_common_shift == 0 {
            return None; // No shift
        }

        let shift_abs = most_common_shift.unsigned_abs();
        let max_reasonable_shift = (self.height / 2).min(500);
        if shift_abs > max_reasonable_shift {
            return None; // Shift too large
        }

        // Determine direction
        // Negative shift = current row is above prev row = content moved up = scroll up
        // Positive shift = current row is below prev row = content moved down = scroll down
        let direction = if most_common_shift < 0 {
            ScrollDirection::Up
        } else {
            ScrollDirection::Down
        };

        Some(ScrollOperation {
            direction,
            pixels: shift_abs,
        })
    }

    /// Hash a single row of the framebuffer
    ///
    /// Uses sampling to avoid hashing every pixel (too slow).
    /// Samples every 8th pixel for better uniqueness while staying fast.
    fn hash_row(&self, framebuffer: &[u8], row: u32) -> u64 {
        let stride = self.width * self.bytes_per_pixel;
        let row_offset = (row * stride) as usize;

        if row_offset >= framebuffer.len() {
            return 0;
        }

        let row_end = (row_offset + stride as usize).min(framebuffer.len());
        let row_data = &framebuffer[row_offset..row_end];

        // Sample every 8th pixel (4 bytes per pixel, so every 32 bytes)
        // This gives better uniqueness than every 16th pixel
        const SAMPLE_STRIDE: usize = 32;

        let mut hash: u64 = 0;
        let mut i = 0;
        let mut sample_count = 0;
        while i < row_data.len() {
            // Hash 4 bytes at once (BGRA)
            if i + 3 < row_data.len() {
                let pixel = u32::from_le_bytes([
                    row_data[i],
                    row_data[i + 1],
                    row_data[i + 2],
                    row_data[i + 3],
                ]);
                // Use a better hash function with position weighting
                hash = hash.wrapping_mul(31).wrapping_add(pixel as u64);
                hash = hash.wrapping_mul(17).wrapping_add(sample_count);
                sample_count += 1;
            }
            i += SAMPLE_STRIDE;
        }

        // Include row length to catch size changes
        hash = hash.wrapping_mul(31).wrapping_add(row_data.len() as u64);

        hash
    }

    /// Reset detector (e.g., after screen resize)
    pub fn reset(&mut self, width: u32, height: u32) {
        self.width = width;
        self.height = height;
        self.row_hashes = vec![0; height as usize];
    }

    /// Get dimensions
    pub fn dimensions(&self) -> (u32, u32) {
        (self.width, self.height)
    }
}
