#![allow(clippy::cast_precision_loss, clippy::cast_sign_loss, clippy::unused_self)]
//! Coordinate types and parsing from hOCR bbox attributes

/// Represents a word extracted from hOCR with position and confidence information
#[derive(Debug, Clone)]
pub struct HocrWord {
    /// The text content of the word
    pub text: String,
    /// X-coordinate of the left edge (pixels)
    pub left: u32,
    /// Y-coordinate of the top edge (pixels)
    pub top: u32,
    /// Width of the word bounding box (pixels)
    pub width: u32,
    /// Height of the word bounding box (pixels)
    pub height: u32,
    /// OCR confidence score (0.0 to 100.0)
    pub confidence: f64,
}

impl HocrWord {
    /// Get the right edge position
    #[must_use]
    pub const fn right(&self) -> u32 {
        self.left + self.width
    }

    /// Get the bottom edge position
    #[must_use]
    pub const fn bottom(&self) -> u32 {
        self.top + self.height
    }

    /// Get the vertical center position
    #[must_use]
    pub fn y_center(&self) -> f64 {
        f64::from(self.top) + (f64::from(self.height) / 2.0)
    }

    /// Get the horizontal center position
    #[must_use]
    pub fn x_center(&self) -> f64 {
        f64::from(self.left) + (f64::from(self.width) / 2.0)
    }
}

/// Parse bbox attribute from hOCR title attribute
///
/// Example: "bbox 100 50 180 80; `x_wconf` 95" -> (100, 50, 80, 30)
pub fn parse_bbox(title: &str) -> Option<(u32, u32, u32, u32)> {
    for part in title.split(';') {
        let part = part.trim();

        if let Some(bbox_str) = part.strip_prefix("bbox ") {
            let coords: Vec<&str> = bbox_str.split_whitespace().collect();
            if coords.len() == 4 {
                if let (Ok(x1), Ok(y1), Ok(x2), Ok(y2)) = (
                    coords[0].parse::<u32>(),
                    coords[1].parse::<u32>(),
                    coords[2].parse::<u32>(),
                    coords[3].parse::<u32>(),
                ) {
                    let width = x2.saturating_sub(x1);
                    let height = y2.saturating_sub(y1);
                    return Some((x1, y1, width, height));
                }
            }
        }
    }
    None
}

/// Parse confidence from hOCR title attribute
///
/// Example: "bbox 100 50 180 80; `x_wconf` 95" -> 95.0
pub fn parse_confidence(title: &str) -> f64 {
    for part in title.split(';') {
        let part = part.trim();
        if let Some(conf_str) = part.strip_prefix("x_wconf ") {
            if let Ok(conf) = conf_str.trim().parse::<f64>() {
                return conf;
            }
        }
    }
    0.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_bbox() {
        assert_eq!(parse_bbox("bbox 100 50 180 80"), Some((100, 50, 80, 30)));
        assert_eq!(parse_bbox("bbox 0 0 100 200"), Some((0, 0, 100, 200)));
        assert_eq!(parse_bbox("bbox 100 50 180 80; x_wconf 95"), Some((100, 50, 80, 30)));
        assert_eq!(parse_bbox("invalid"), None);
        assert_eq!(parse_bbox("bbox 100 50"), None);
    }

    #[test]
    fn test_parse_confidence() {
        assert_eq!(parse_confidence("x_wconf 95.5"), 95.5);
        assert_eq!(parse_confidence("bbox 100 50 180 80; x_wconf 92"), 92.0);
        assert_eq!(parse_confidence("invalid"), 0.0);
    }

    #[test]
    fn test_hocr_word_methods() {
        let word = HocrWord {
            text: "Hello".to_string(),
            left: 100,
            top: 50,
            width: 80,
            height: 30,
            confidence: 95.5,
        };

        assert_eq!(word.right(), 180);
        assert_eq!(word.bottom(), 80);
        assert_eq!(word.y_center(), 65.0);
        assert_eq!(word.x_center(), 140.0);
    }
}
