//! Callback management, macros, and async-to-sync bridge.
//!
//! This module provides helper macros for common visitor patterns and an async-to-sync
//! visitor bridge for integrating async visitors with synchronous converters.

mod bridge;
mod bridge_visitor;
mod macros;

#[cfg(feature = "async-visitor")]
pub use bridge::AsyncToSyncVisitorBridge;
#[cfg(feature = "async-visitor")]
pub use macros::dispatch_async_visitor;

/// Type alias for an async visitor handle (Arc-wrapped `Mutex` for interior mutability).
///
/// This allows async visitors to be passed around and shared while still being mutable.
/// Uses Arc<Mutex<>> instead of Rc<RefCell<>> to enable Send across thread boundaries.
/// The + Send + 'static bounds allow the visitor to be moved to other threads.
#[cfg(feature = "async-visitor")]
pub type AsyncVisitorHandle = std::sync::Arc<tokio::sync::Mutex<dyn crate::visitor::AsyncHtmlVisitor + Send + 'static>>;
