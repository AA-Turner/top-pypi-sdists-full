#![allow(clippy::cast_precision_loss, clippy::cast_sign_loss, clippy::unused_self)]
//! Spatial table reconstruction from hOCR bounding box coordinates
//!
//! This module provides functions to detect and reconstruct tabular data from OCR'd text
//! by analyzing the spatial positions of words using their bounding box (bbox) coordinates.

mod coords;
mod grouping;
mod layout;
mod output;

pub use coords::{HocrWord, parse_bbox, parse_confidence};
pub use grouping::extract_hocr_words;
pub use layout::reconstruct_table;
pub use output::table_to_markdown;
