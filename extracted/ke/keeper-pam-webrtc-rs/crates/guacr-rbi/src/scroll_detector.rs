// Scroll Detection for RBI
//
// Detects scroll events via JavaScript and sends scroll instructions
// instead of full frames, improving UX and reducing bandwidth.

use log::{debug, info};
use tokio::time::Instant;

/// JavaScript to install scroll event listener
pub const SCROLL_TRACKER_JS: &str = r#"
(function() {
    if (window.__guacr_scroll_installed) return;
    window.__guacr_scroll_installed = true;
    
    window.__guacr_scroll_x = window.scrollX || 0;
    window.__guacr_scroll_y = window.scrollY || 0;
    window.__guacr_scroll_changed = false;
    
    const updateScroll = () => {
        const newX = window.scrollX || 0;
        const newY = window.scrollY || 0;
        
        if (newX !== window.__guacr_scroll_x || newY !== window.__guacr_scroll_y) {
            window.__guacr_scroll_changed = true;
            window.__guacr_scroll_x = newX;
            window.__guacr_scroll_y = newY;
        }
    };
    
    // Listen to scroll events
    window.addEventListener('scroll', updateScroll, { passive: true });
    
    // Also check on resize (can cause scroll position changes)
    window.addEventListener('resize', updateScroll, { passive: true });
    
    console.log('[guacr] Scroll tracker installed');
})();
"#;

/// JavaScript to poll for scroll changes
pub const GET_SCROLL_DATA_JS: &str = r#"
(function() {
    if (!window.__guacr_scroll_installed) return null;
    
    if (window.__guacr_scroll_changed) {
        window.__guacr_scroll_changed = false;
        return {
            x: window.__guacr_scroll_x,
            y: window.__guacr_scroll_y,
            maxX: document.documentElement.scrollWidth - window.innerWidth,
            maxY: document.documentElement.scrollHeight - window.innerHeight
        };
    }
    
    return null;
})();
"#;

/// Scroll position data
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct ScrollPosition {
    pub x: i32,
    pub y: i32,
    pub max_x: i32,
    pub max_y: i32,
}

impl ScrollPosition {
    pub fn new(x: i32, y: i32, max_x: i32, max_y: i32) -> Self {
        Self { x, y, max_x, max_y }
    }

    /// Calculate delta from another position
    pub fn delta_from(&self, other: &ScrollPosition) -> (i32, i32) {
        (self.x - other.x, self.y - other.y)
    }

    /// Check if scroll position is at top
    pub fn is_at_top(&self) -> bool {
        self.y == 0
    }

    /// Check if scroll position is at bottom
    pub fn is_at_bottom(&self) -> bool {
        self.y >= self.max_y
    }

    /// Check if scroll position is at left edge
    pub fn is_at_left(&self) -> bool {
        self.x == 0
    }

    /// Check if scroll position is at right edge
    pub fn is_at_right(&self) -> bool {
        self.x >= self.max_x
    }
}

/// Scroll detector state
pub struct ScrollDetector {
    last_position: Option<ScrollPosition>,
    last_scroll_time: Option<Instant>,
    scroll_velocity: f32, // pixels per second
    scroll_events: u64,
    total_distance_x: i32,
    total_distance_y: i32,
}

impl ScrollDetector {
    pub fn new() -> Self {
        Self {
            last_position: None,
            last_scroll_time: None,
            scroll_velocity: 0.0,
            scroll_events: 0,
            total_distance_x: 0,
            total_distance_y: 0,
        }
    }

    /// Update scroll position and return delta if changed
    ///
    /// Returns Some((delta_x, delta_y)) if position changed, None otherwise
    pub fn update(&mut self, position: ScrollPosition) -> Option<(i32, i32)> {
        let now = Instant::now();

        if let Some(last) = self.last_position {
            let (delta_x, delta_y) = position.delta_from(&last);

            if delta_x != 0 || delta_y != 0 {
                self.scroll_events += 1;
                self.total_distance_x += delta_x.abs();
                self.total_distance_y += delta_y.abs();

                // Calculate scroll velocity (pixels per second)
                if let Some(last_time) = self.last_scroll_time {
                    let elapsed = last_time.elapsed().as_secs_f32();
                    if elapsed > 0.0 {
                        let distance = ((delta_x * delta_x + delta_y * delta_y) as f32).sqrt();
                        self.scroll_velocity = distance / elapsed;
                    }
                }
                self.last_scroll_time = Some(now);

                debug!(
                    "Scroll detected: delta=({}, {}), position=({}, {}), velocity={:.0}px/s",
                    delta_x, delta_y, position.x, position.y, self.scroll_velocity
                );

                self.last_position = Some(position);
                return Some((delta_x, delta_y));
            }
        } else {
            // First position
            self.last_position = Some(position);
            self.last_scroll_time = Some(now);
            info!(
                "Scroll tracking initialized at ({}, {})",
                position.x, position.y
            );
        }

        None
    }

    /// Get statistics
    pub fn stats(&self) -> ScrollStats {
        ScrollStats {
            scroll_events: self.scroll_events,
            total_distance_x: self.total_distance_x,
            total_distance_y: self.total_distance_y,
        }
    }

    /// Reset statistics
    pub fn reset_stats(&mut self) {
        self.scroll_events = 0;
        self.total_distance_x = 0;
        self.total_distance_y = 0;
    }

    /// Get current position
    pub fn current_position(&self) -> Option<ScrollPosition> {
        self.last_position
    }

    /// Check if currently scrolling (scrolled within last 2 seconds)
    pub fn is_scrolling(&self) -> bool {
        self.last_scroll_time
            .map(|t| t.elapsed().as_secs() < 2)
            .unwrap_or(false)
    }

    /// Check if scrolling fast (> 500 pixels/second)
    pub fn is_fast_scrolling(&self) -> bool {
        self.scroll_velocity > 500.0
    }

    /// Check if scroll is significant (> 5% of viewport)
    pub fn is_significant_scroll(&self, delta_y: i32, viewport_height: i32) -> bool {
        if viewport_height == 0 {
            return false;
        }
        let scroll_percent = (delta_y.abs() * 100) / viewport_height;
        scroll_percent > 5
    }

    /// Check if this is a page scroll (> 80% of viewport)
    pub fn is_page_scroll(&self, delta_y: i32, viewport_height: i32) -> bool {
        if viewport_height == 0 {
            return false;
        }
        let scroll_percent = (delta_y.abs() * 100) / viewport_height;
        scroll_percent > 80
    }

    /// Get current scroll velocity in pixels per second
    pub fn velocity(&self) -> f32 {
        self.scroll_velocity
    }
}

impl Default for ScrollDetector {
    fn default() -> Self {
        Self::new()
    }
}

/// Scroll statistics
#[derive(Debug, Clone, Copy, Default)]
pub struct ScrollStats {
    pub scroll_events: u64,
    pub total_distance_x: i32,
    pub total_distance_y: i32,
}

impl ScrollStats {
    pub fn avg_distance_per_scroll(&self) -> (f32, f32) {
        if self.scroll_events == 0 {
            return (0.0, 0.0);
        }
        (
            self.total_distance_x as f32 / self.scroll_events as f32,
            self.total_distance_y as f32 / self.scroll_events as f32,
        )
    }
}

/// Format scroll instruction for Guacamole protocol
///
/// Note: Guacamole doesn't have a native scroll instruction,
/// so we use mouse events to simulate scrolling
pub fn format_scroll_instruction(layer: u32, delta_x: i32, delta_y: i32) -> String {
    // Use mouse instruction with scroll wheel
    // Format: mouse,<x>,<y>,<button_mask>;
    // For scroll: button_mask bit 3 (value 8) = scroll up, bit 4 (value 16) = scroll down

    if delta_y < 0 {
        // Scroll up
        format!("5.mouse,{},{},{};", layer, 0, 8)
    } else if delta_y > 0 {
        // Scroll down
        format!("5.mouse,{},{},{};", layer, 0, 16)
    } else if delta_x < 0 {
        // Scroll left (less common)
        format!("5.mouse,{},{},{};", layer, 0, 32)
    } else if delta_x > 0 {
        // Scroll right (less common)
        format!("5.mouse,{},{},{};", layer, 0, 64)
    } else {
        // No scroll
        String::new()
    }
}
