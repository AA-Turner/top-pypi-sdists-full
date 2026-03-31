//! Visitor support for Python bindings.
//!
//! This module provides the bridge between Python visitor objects and the Rust HtmlVisitor trait.

#[cfg(feature = "visitor")]
pub mod types;

#[cfg(feature = "visitor")]
pub mod bridge;

#[cfg(feature = "visitor")]
pub use bridge::PyVisitorBridge;

#[cfg(feature = "visitor")]
pub use types::*;
