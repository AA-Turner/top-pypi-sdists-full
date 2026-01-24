//! Conversion functions for HTML to Markdown.
//!
//! This module provides the core conversion functionality exposed as Python functions.

#[cfg(feature = "inline-images")]
pub mod inline_images;

#[cfg(feature = "metadata")]
pub mod metadata;

// Re-export all pyfunction-decorated conversion functions
#[cfg(feature = "inline-images")]
pub use inline_images::{
    convert_with_inline_images, convert_with_inline_images_handle, convert_with_inline_images_json,
};

#[cfg(feature = "metadata")]
pub use metadata::{convert_with_metadata, convert_with_metadata_handle, convert_with_metadata_json};
