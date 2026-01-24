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

#[cfg(feature = "inline-images")]
pub use crate::convert_with_inline_images;

#[cfg(feature = "metadata")]
pub use crate::convert_with_metadata;

#[cfg(feature = "visitor")]
pub use crate::convert_with_visitor;

#[cfg(feature = "async-visitor")]
pub use crate::convert_with_async_visitor;
