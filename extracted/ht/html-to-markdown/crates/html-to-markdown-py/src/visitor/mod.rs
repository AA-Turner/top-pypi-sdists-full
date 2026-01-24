//! Visitor support for Python bindings.
//!
//! This module provides the bridge between Python visitor objects and the Rust HtmlVisitor trait.

#[cfg(feature = "visitor")]
pub mod types;

#[cfg(feature = "visitor")]
pub mod bridge;

#[cfg(feature = "async-visitor")]
pub mod async_bridge;

#[cfg(feature = "visitor")]
pub use bridge::PyVisitorBridge;

#[cfg(feature = "async-visitor")]
pub use async_bridge::PyAsyncVisitorBridge;

#[cfg(feature = "visitor")]
pub use types::*;
