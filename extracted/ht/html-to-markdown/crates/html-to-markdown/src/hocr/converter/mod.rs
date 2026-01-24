//! hOCR to Markdown conversion module
//!
//! Converts structured hOCR elements to Markdown while preserving document hierarchy.
//!
//! This module is organized into several submodules:
//! - `core`: Main conversion functions and entry points
//! - `elements`: Element-specific conversion logic
//! - `hierarchy`: Document hierarchy and code block detection
//! - `layout`: Spatial layout analysis and table reconstruction
//! - `output`: Output formatting utilities

#![allow(clippy::branches_sharing_code, clippy::option_if_let_else)]

mod code_analysis;
mod core;
mod elements;
mod hierarchy;
mod keywords;
mod layout;
mod output;

// Re-export public API
pub use core::{convert_to_markdown, convert_to_markdown_with_options};

// Re-export commonly used types from spatial module for downstream use
pub use super::spatial::HocrWord;
