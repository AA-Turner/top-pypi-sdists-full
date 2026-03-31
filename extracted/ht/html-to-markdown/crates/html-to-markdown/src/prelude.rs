//! Prelude module for convenient imports.
//!
//! Re-exports the most commonly used types and functions from the crate.
//! Users can import everything they need with:
//! ```
//! use html_to_markdown_rs::prelude::*;
//! ```

pub use crate::convert;
pub use crate::error::{ConversionError, Result};
pub use crate::options::{ConversionOptions, HeadingStyle};
pub use crate::types::ConversionResult;
