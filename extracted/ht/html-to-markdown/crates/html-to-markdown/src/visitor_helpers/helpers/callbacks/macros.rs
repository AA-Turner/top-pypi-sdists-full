//! Async visitor dispatch function and helper macros.
//!
//! This module provides:
//! - `dispatch_async_visitor` function for async visitor callback dispatch
//! - `try_async_visitor!` macro for common visitor patterns
//! - `try_async_visitor_element_start!` macro for element start callbacks
//! - `try_async_visitor_element_end!` macro for element end callbacks

#[cfg(feature = "async-visitor")]
use super::super::content::VisitorDispatch;
#[cfg(feature = "async-visitor")]
use super::AsyncVisitorHandle;
#[cfg(feature = "async-visitor")]
use crate::error::{ConversionError, Result};
#[cfg(feature = "async-visitor")]
use crate::visitor::AsyncHtmlVisitor;

/// Dispatch an async visitor callback and handle the result.
///
/// This is the async version of `dispatch_visitor`, supporting async visitor implementations.
/// It safely handles the optional visitor, calls the callback function, and translates the
/// `VisitResult` into concrete control flow decisions.
///
/// # Type Parameters
///
/// - `F`: Async visitor callback function type
///
/// # Parameters
///
/// - `visitor`: Optional async visitor (wrapped in Rc<`RefCell`<>>)
/// - `callback`: Async closure that invokes the appropriate async visitor method
///
/// # Returns
///
/// - `Ok(VisitorDispatch::Custom(String))`: Custom markdown output from `VisitResult::Custom`
/// - `Ok(VisitorDispatch::Continue)`: Continue with default behavior (`VisitResult::Continue`)
/// - `Err(ConversionError)`: Stop conversion with error (`VisitResult::Error`)
///
/// # Errors
///
/// - If the visitor returns `VisitResult::Error`, this is converted to `Error::Visitor`
/// - `RefCell` borrow failures panic (should never happen with correct usage)
///
/// # Performance
///
/// - Zero-cost when visitor is None (common case)
/// - Single dynamic dispatch when visitor is present
/// - No allocations except for error messages
///
/// # Examples
///
/// ```ignore
/// let result = dispatch_async_visitor(
///     &visitor,
///     |v| Box::pin(v.visit_heading(&ctx, level, text, id)),
/// ).await?;
///
/// match result {
///     VisitorDispatch::Custom(output) => return Ok(output),
///     VisitorDispatch::Continue => { /* proceed with default conversion */ }
///     _ => {}
/// }
/// ```
#[cfg(feature = "async-visitor")]
#[allow(dead_code, clippy::future_not_send)]
#[inline]
pub async fn dispatch_async_visitor<F, Fut>(
    visitor: &Option<AsyncVisitorHandle>,
    callback: F,
) -> Result<VisitorDispatch>
where
    F: FnOnce(&mut dyn AsyncHtmlVisitor) -> Fut,
    Fut: std::future::Future<Output = crate::visitor::VisitResult>,
{
    let Some(visitor_mutex) = visitor else {
        return Ok(VisitorDispatch::Continue);
    };

    let future = {
        let mut visitor_ref = visitor_mutex.lock().await;
        callback(&mut *visitor_ref)
    };

    let result = future.await;

    match result {
        crate::visitor::VisitResult::Continue => Ok(VisitorDispatch::Continue),
        crate::visitor::VisitResult::Custom(output) => Ok(VisitorDispatch::Custom(output)),
        crate::visitor::VisitResult::Skip => Ok(VisitorDispatch::Skip),
        crate::visitor::VisitResult::PreserveHtml => Ok(VisitorDispatch::PreserveHtml),
        crate::visitor::VisitResult::Error(msg) => Err(ConversionError::Visitor(msg)),
    }
}

/// Macro to reduce boilerplate when calling async visitor methods.
///
/// This macro wraps the common pattern of:
/// 1. Check if visitor is present
/// 2. Call async visitor method (awaiting the result)
/// 3. Handle early return for Custom/Skip/PreserveHtml/Error
/// 4. Continue with default behavior if visitor returns Continue
///
/// # Syntax
///
/// ```ignore
/// try_async_visitor!(visitor_option, method_name, ctx, arg1, arg2, ...).await?;
/// ```
///
/// # Returns
///
/// - Returns early with custom output if visitor returns Custom/Skip/PreserveHtml
/// - Returns early with Err if visitor returns Error
/// - Continues execution if visitor returns Continue or is None
///
/// # Examples
///
/// ```ignore
/// // Before (verbose):
/// let dispatch = dispatch_async_visitor(&visitor, |v| {
///     Box::pin(v.visit_heading(&ctx, level, text, id))
/// }).await?;
/// match dispatch {
///     VisitorDispatch::Custom(output) => return Ok(output),
///     VisitorDispatch::Skip => return Ok(String::new()),
///     VisitorDispatch::PreserveHtml => return Ok(preserve_html_output),
///     VisitorDispatch::Continue => { /* proceed */ }
/// }
///
/// // After (concise):
/// try_async_visitor!(visitor, visit_heading, &ctx, level, text, id).await?;
/// // Default conversion logic continues here...
/// ```
#[cfg(feature = "async-visitor")]
#[macro_export]
macro_rules! try_async_visitor {
    ($visitor:expr, $method:ident, $ctx:expr $(, $arg:expr)*) => {{
        let dispatch = $crate::visitor_helpers::dispatch_async_visitor(
            $visitor,
            |v| Box::pin(v.$method($ctx $(, $arg)*)),
        ).await?;

        match dispatch {
            $crate::visitor_helpers::VisitorDispatch::Continue => {
            }
            $crate::visitor_helpers::VisitorDispatch::Custom(output) => {
                return Ok(output);
            }
            $crate::visitor_helpers::VisitorDispatch::Skip => {
                return Ok(String::new());
            }
            $crate::visitor_helpers::VisitorDispatch::PreserveHtml => {
                // TODO: Implement HTML preservation logic
            }
        }
    }};
}

/// Convenience macro for async `element_start` visitor calls with early return.
///
/// This is the async version of `try_visitor_element_start!` macro.
/// It handles the common pattern of calling `visit_element_start` at the beginning
/// of element processing.
///
/// # Syntax
///
/// ```ignore
/// try_async_visitor_element_start!(visitor_option, ctx).await?;
/// ```
///
/// # Examples
///
/// ```ignore
/// async fn process_heading(...) -> Result<String> {
///     let ctx = build_node_context(...);
///     try_async_visitor_element_start!(visitor, &ctx).await?;
///
///     // Default heading processing continues here...
/// }
/// ```
#[cfg(feature = "async-visitor")]
#[macro_export]
macro_rules! try_async_visitor_element_start {
    ($visitor:expr, $ctx:expr) => {{
        $crate::try_async_visitor!($visitor, visit_element_start, $ctx);
    }};
}

/// Convenience macro for async `element_end` visitor calls with output inspection.
///
/// This is the async version of `try_visitor_element_end!` macro.
/// It handles the common pattern of calling `visit_element_end` after generating
/// default markdown output.
///
/// # Syntax
///
/// ```ignore
/// try_async_visitor_element_end!(visitor_option, ctx, default_output_string).await?;
/// ```
///
/// # Examples
///
/// ```ignore
/// async fn process_heading(...) -> Result<String> {
///     let ctx = build_node_context(...);
///     let mut output = String::from("# Heading");
///
///     try_async_visitor_element_end!(visitor, &ctx, &output).await?;
///     Ok(output)
/// }
/// ```
#[cfg(feature = "async-visitor")]
#[macro_export]
macro_rules! try_async_visitor_element_end {
    ($visitor:expr, $ctx:expr, $output:expr) => {{
        $crate::try_async_visitor!($visitor, visit_element_end, $ctx, $output);
    }};
}
