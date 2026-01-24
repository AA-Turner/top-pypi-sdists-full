//! Helper functions for visitor pattern integration.
//!
//! This module provides efficient utilities for building visitor contexts,
//! dispatching visitor callbacks, and handling visitor results during the
//! HTML→Markdown conversion process.
//!
//! # Design Goals
//!
//! - **Zero allocation when possible**: Reuse existing data structures
//! - **Minimal overhead**: Inline hot paths, avoid unnecessary clones
//! - **Type safety**: Leverage Rust's type system for correct visitor handling
//! - **Ergonomics**: Reduce boilerplate for common visitor patterns
//!
//! # Usage
//!
//! These helpers are designed to be used within the converter module during
//! the DOM traversal. They bridge the gap between the internal conversion
//! state and the public visitor API.

use std::cell::RefCell;
use std::collections::BTreeMap;
use std::rc::Rc;

use crate::error::{ConversionError, Result};
use crate::visitor::{HtmlVisitor, NodeContext, NodeType, VisitResult};

#[cfg(feature = "async-visitor")]
use crate::visitor::AsyncHtmlVisitor;

/// Build a `NodeContext` from current parsing state.
///
/// Creates a complete `NodeContext` suitable for passing to visitor callbacks.
/// This function collects metadata about the current node from various sources:
/// - Tag name and attributes from the HTML element
/// - Depth and parent information from the DOM tree
/// - Index among siblings for positional awareness
/// - Inline/block classification
///
/// # Parameters
///
/// - `node_type`: Coarse-grained classification (Link, Image, Heading, etc.)
/// - `tag_name`: Raw HTML tag name (e.g., "div", "h1", "custom-element")
/// - `attributes`: All HTML attributes as key-value pairs
/// - `depth`: Nesting depth in the DOM tree (0 = root)
/// - `index_in_parent`: Zero-based index among siblings
/// - `parent_tag`: Parent element's tag name (None if root)
/// - `is_inline`: Whether this element is treated as inline vs block
///
/// # Returns
///
/// A fully populated `NodeContext` ready for visitor dispatch.
///
/// # Performance
///
/// This function performs minimal allocations:
/// - Clones `tag_name` (typically 2-10 bytes)
/// - Clones `parent_tag` if present (typically 2-10 bytes)
/// - Clones the attributes `BTreeMap` (heap allocation if non-empty)
///
/// For text nodes and simple elements without attributes, allocations are minimal.
///
/// # Examples
///
/// ```ignore
/// let ctx = build_node_context(
///     NodeType::Heading,
///     "h1",
///     &attrs,
///     1,
///     0,
///     Some("body"),
///     false,
/// );
/// ```
#[allow(dead_code)]
#[inline]
pub fn build_node_context(
    node_type: NodeType,
    tag_name: &str,
    attributes: &BTreeMap<String, String>,
    depth: usize,
    index_in_parent: usize,
    parent_tag: Option<&str>,
    is_inline: bool,
) -> NodeContext {
    NodeContext {
        node_type,
        tag_name: tag_name.to_string(),
        attributes: attributes.clone(),
        depth,
        index_in_parent,
        parent_tag: parent_tag.map(String::from),
        is_inline,
    }
}

/// Dispatch a visitor callback and handle the result.
///
/// This is the core dispatcher for all visitor callbacks. It safely handles the
/// optional visitor, calls the callback function, and translates the `VisitResult`
/// into concrete control flow decisions.
///
/// # Type Parameters
///
/// - `F`: Visitor callback function type
///
/// # Parameters
///
/// - `visitor`: Optional visitor (wrapped in Rc<`RefCell`<>>)
/// - `callback`: Closure that invokes the appropriate visitor method
///
/// # Returns
///
/// - `Ok(Some(String))`: Custom markdown output from `VisitResult::Custom`
/// - `Ok(None)`: Continue with default behavior (`VisitResult::Continue`)
/// - `Err(Error)`: Stop conversion with error (`VisitResult::Error`)
///
/// The `VisitResult::Skip` and `VisitResult::PreserveHtml` variants are handled
/// by the caller based on context.
///
/// # Error Handling
///
/// - If the visitor panics during callback, the panic propagates normally
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
/// let result = dispatch_visitor(
///     &visitor,
///     |v| v.visit_heading(&ctx, level, text, id),
/// )?;
///
/// match result {
///     Some(custom_output) => return Ok(custom_output),
///     None => { /* proceed with default conversion */ }
/// }
/// ```
#[allow(dead_code)]
#[inline]
/// # Errors
///
/// Returns an error if visitor dispatch fails.
pub fn dispatch_visitor<F>(visitor: &Option<Rc<RefCell<dyn HtmlVisitor>>>, callback: F) -> Result<VisitorDispatch>
where
    F: FnOnce(&mut dyn HtmlVisitor) -> VisitResult,
{
    let Some(visitor_rc) = visitor else {
        return Ok(VisitorDispatch::Continue);
    };

    let mut visitor_ref = visitor_rc.borrow_mut();
    let result = callback(&mut *visitor_ref);

    match result {
        VisitResult::Continue => Ok(VisitorDispatch::Continue),
        VisitResult::Custom(output) => Ok(VisitorDispatch::Custom(output)),
        VisitResult::Skip => Ok(VisitorDispatch::Skip),
        VisitResult::PreserveHtml => Ok(VisitorDispatch::PreserveHtml),
        VisitResult::Error(msg) => Err(ConversionError::Visitor(msg)),
    }
}

/// Result of dispatching a visitor callback.
///
/// This enum represents the outcome of a visitor callback dispatch,
/// providing a more ergonomic interface for control flow than the
/// raw `VisitResult` type.
#[allow(dead_code)]
#[derive(Debug)]
pub enum VisitorDispatch {
    /// Continue with default conversion behavior
    Continue,

    /// Replace default output with custom markdown
    Custom(String),

    /// Skip this element entirely (don't output anything)
    Skip,

    /// Preserve original HTML (don't convert to markdown)
    PreserveHtml,
}

impl VisitorDispatch {
    /// Check if this dispatch result indicates continuation.
    #[allow(dead_code)]
    #[inline]
    #[must_use]
    pub const fn is_continue(&self) -> bool {
        matches!(self, Self::Continue)
    }

    /// Check if this dispatch result contains custom output.
    #[allow(dead_code)]
    #[inline]
    #[must_use]
    pub const fn is_custom(&self) -> bool {
        matches!(self, Self::Custom(_))
    }

    /// Check if this dispatch result indicates skipping.
    #[allow(dead_code)]
    #[inline]
    #[must_use]
    pub const fn is_skip(&self) -> bool {
        matches!(self, Self::Skip)
    }

    /// Check if this dispatch result indicates HTML preservation.
    #[allow(dead_code)]
    #[inline]
    #[must_use]
    pub const fn is_preserve_html(&self) -> bool {
        matches!(self, Self::PreserveHtml)
    }

    /// Extract custom output if present.
    #[allow(dead_code)]
    #[inline]
    #[must_use]
    pub fn into_custom(self) -> Option<String> {
        match self {
            Self::Custom(output) => Some(output),
            _ => None,
        }
    }

    /// Extract custom output reference if present.
    #[allow(dead_code)]
    #[inline]
    #[must_use]
    pub fn as_custom(&self) -> Option<&str> {
        match self {
            Self::Custom(output) => Some(output),
            _ => None,
        }
    }
}

/// Type alias for an async visitor handle (Arc-wrapped `Mutex` for interior mutability).
///
/// This allows async visitors to be passed around and shared while still being mutable.
/// Uses Arc<Mutex<>> instead of Rc<RefCell<>> to enable Send across thread boundaries.
/// The + Send + 'static bounds allow the visitor to be moved to other threads.
#[cfg(feature = "async-visitor")]
pub type AsyncVisitorHandle = std::sync::Arc<tokio::sync::Mutex<dyn AsyncHtmlVisitor + Send + 'static>>;

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
    visitor: &Option<Rc<RefCell<dyn AsyncHtmlVisitor>>>,
    callback: F,
) -> Result<VisitorDispatch>
where
    F: FnOnce(&mut dyn AsyncHtmlVisitor) -> Fut,
    Fut: std::future::Future<Output = VisitResult>,
{
    let Some(visitor_rc) = visitor else {
        return Ok(VisitorDispatch::Continue);
    };

    let future = {
        let mut visitor_ref = visitor_rc.borrow_mut();
        callback(&mut *visitor_ref)
    };

    let result = future.await;

    match result {
        VisitResult::Continue => Ok(VisitorDispatch::Continue),
        VisitResult::Custom(output) => Ok(VisitorDispatch::Custom(output)),
        VisitResult::Skip => Ok(VisitorDispatch::Skip),
        VisitResult::PreserveHtml => Ok(VisitorDispatch::PreserveHtml),
        VisitResult::Error(msg) => Err(ConversionError::Visitor(msg)),
    }
}

/// Macro to reduce boilerplate when calling async visitor methods.
///
/// This macro wraps the common pattern of:
/// 1. Check if visitor is present
/// 2. Call visitor method
/// 3. Handle early return for Custom/Skip/PreserveHtml/Error
/// 4. Continue with default behavior if visitor returns Continue
///
/// # Syntax
///
/// ```ignore
/// try_visitor!(visitor_option, method_name, ctx, arg1, arg2, ...);
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
/// let dispatch = dispatch_visitor(&visitor, |v| v.visit_heading(&ctx, level, text, id))?;
/// match dispatch {
///     VisitorDispatch::Custom(output) => return Ok(output),
///     VisitorDispatch::Skip => return Ok(String::new()),
///     VisitorDispatch::PreserveHtml => return Ok(preserve_html_output),
///     VisitorDispatch::Continue => { /* proceed */ }
/// }
///
/// // After (concise):
/// try_visitor!(visitor, visit_heading, &ctx, level, text, id);
/// // Default conversion logic continues here...
/// ```
#[macro_export]
macro_rules! try_visitor {
    ($visitor:expr, $method:ident, $ctx:expr $(, $arg:expr)*) => {{
        let dispatch = $crate::visitor_helpers::dispatch_visitor(
            $visitor,
            |v| v.$method($ctx $(, $arg)*),
        )?;

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

/// Convenience macro for `element_start` visitor calls with early return.
///
/// This specialized macro handles the common pattern of calling `visit_element_start`
/// at the beginning of element processing. Unlike `try_visitor!`, this macro
/// understands that `element_start` callbacks typically want to abort processing
/// entirely if they return anything other than Continue.
///
/// # Syntax
///
/// ```ignore
/// try_visitor_element_start!(visitor_option, ctx);
/// ```
///
/// # Examples
///
/// ```ignore
/// fn process_heading(...) -> Result<String> {
///     let ctx = build_node_context(...);
///     try_visitor_element_start!(visitor, &ctx)?;
///
///     // Default heading processing continues here...
/// }
/// ```
#[macro_export]
macro_rules! try_visitor_element_start {
    ($visitor:expr, $ctx:expr) => {{
        $crate::try_visitor!($visitor, visit_element_start, $ctx);
    }};
}

/// Convenience macro for `element_end` visitor calls with output inspection.
///
/// This specialized macro handles the common pattern of calling `visit_element_end`
/// after generating default markdown output. The visitor receives the default
/// output and can choose to replace it or let it pass through.
///
/// # Syntax
///
/// ```ignore
/// try_visitor_element_end!(visitor_option, ctx, default_output_string);
/// ```
///
/// # Examples
///
/// ```ignore
/// fn process_heading(...) -> Result<String> {
///     let ctx = build_node_context(...);
///     let mut output = String::from("# Heading");
///
///     try_visitor_element_end!(visitor, &ctx, &output)?;
///     Ok(output)
/// }
/// ```
#[macro_export]
macro_rules! try_visitor_element_end {
    ($visitor:expr, $ctx:expr, $output:expr) => {{
        $crate::try_visitor!($visitor, visit_element_end, $ctx, $output);
    }};
}

/// Macro to reduce boilerplate when calling async visitor methods.
///
/// This is the async version of `try_visitor!` macro. It wraps the common pattern of:
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

/// Bridge that wraps an async visitor and implements the sync `HtmlVisitor` trait.
///
/// This bridge uses a channel-based approach to avoid blocking:
/// 1. Sync converter sends visitor call request through channel
/// 2. Async runtime receives request and awaits JS callback
/// 3. Result sent back through response channel
/// 4. Sync converter receives result and continues
///
/// This approach avoids deadlock by never blocking on async operations.
/// The response_rx is wrapped in a Mutex to provide interior mutability,
/// avoiding the need for external RefCell wrapping that causes borrow conflicts.
#[cfg(feature = "async-visitor")]
pub struct AsyncToSyncVisitorBridge {
    async_visitor: AsyncVisitorHandle,
    // Using tokio::sync::mpsc for async communication (request) and std::sync::mpsc for sync (response)
    request_tx: tokio::sync::mpsc::UnboundedSender<VisitorRequest>,
    // Wrapped in Mutex for interior mutability - allows recv() without &mut self
    response_rx: std::sync::Mutex<std::sync::mpsc::Receiver<crate::visitor::VisitResult>>,
}

#[cfg(feature = "async-visitor")]
enum VisitorRequest {
    ElementStart(crate::visitor::NodeContext),
    ElementEnd(crate::visitor::NodeContext, String),
    Text(crate::visitor::NodeContext, String),
    Link(crate::visitor::NodeContext, String, String, Option<String>),
    Image(crate::visitor::NodeContext, String, String, Option<String>),
    Heading(crate::visitor::NodeContext, u32, String, Option<String>),
    CodeBlock(crate::visitor::NodeContext, Option<String>, String),
    CodeInline(crate::visitor::NodeContext, String),
    ListItem(crate::visitor::NodeContext, bool, String, String),
    ListStart(crate::visitor::NodeContext, bool),
    ListEnd(crate::visitor::NodeContext, bool, String),
    TableStart(crate::visitor::NodeContext),
    TableRow(crate::visitor::NodeContext, Vec<String>, bool),
    TableEnd(crate::visitor::NodeContext, String),
    Blockquote(crate::visitor::NodeContext, String, usize),
    Strong(crate::visitor::NodeContext, String),
    Emphasis(crate::visitor::NodeContext, String),
    Strikethrough(crate::visitor::NodeContext, String),
    Underline(crate::visitor::NodeContext, String),
    Subscript(crate::visitor::NodeContext, String),
    Superscript(crate::visitor::NodeContext, String),
    Mark(crate::visitor::NodeContext, String),
    LineBreak(crate::visitor::NodeContext),
    HorizontalRule(crate::visitor::NodeContext),
    CustomElement(crate::visitor::NodeContext, String, String),
}

#[cfg(feature = "async-visitor")]
impl std::fmt::Debug for AsyncToSyncVisitorBridge {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("AsyncToSyncVisitorBridge")
            .field("async_visitor", &self.async_visitor)
            .finish_non_exhaustive()
    }
}

#[cfg(feature = "async-visitor")]
impl AsyncToSyncVisitorBridge {
    /// Create a new async-to-sync visitor bridge with channel-based communication.
    pub fn new(async_visitor: AsyncVisitorHandle) -> Self {
        // Use tokio::sync::mpsc for async channels (not std::sync::mpsc which blocks)
        let (request_tx, mut request_rx) = tokio::sync::mpsc::unbounded_channel();
        let (response_tx, response_rx) = std::sync::mpsc::channel();
        let response_rx = std::sync::Mutex::new(response_rx);

        // Spawn async task to handle visitor requests
        let visitor_clone = async_visitor.clone();
        tokio::spawn(async move {
            while let Some(request) = request_rx.recv().await {
                let result = match request {
                    VisitorRequest::ElementStart(ctx) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_element_start(&ctx).await
                    }
                    VisitorRequest::ElementEnd(ctx, output) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_element_end(&ctx, &output).await
                    }
                    VisitorRequest::Text(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_text(&ctx, &text).await
                    }
                    VisitorRequest::Link(ctx, href, text, title) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_link(&ctx, &href, &text, title.as_deref()).await
                    }
                    VisitorRequest::Image(ctx, src, alt, title) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_image(&ctx, &src, &alt, title.as_deref()).await
                    }
                    VisitorRequest::Heading(ctx, level, text, id) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_heading(&ctx, level, &text, id.as_deref()).await
                    }
                    VisitorRequest::CodeBlock(ctx, lang, code) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_code_block(&ctx, lang.as_deref(), &code).await
                    }
                    VisitorRequest::CodeInline(ctx, code) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_code_inline(&ctx, &code).await
                    }
                    VisitorRequest::ListItem(ctx, ordered, marker, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_list_item(&ctx, ordered, &marker, &text).await
                    }
                    VisitorRequest::ListStart(ctx, ordered) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_list_start(&ctx, ordered).await
                    }
                    VisitorRequest::ListEnd(ctx, ordered, output) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_list_end(&ctx, ordered, &output).await
                    }
                    VisitorRequest::TableStart(ctx) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_table_start(&ctx).await
                    }
                    VisitorRequest::TableRow(ctx, cells, is_header) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_table_row(&ctx, &cells, is_header).await
                    }
                    VisitorRequest::TableEnd(ctx, output) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_table_end(&ctx, &output).await
                    }
                    VisitorRequest::Blockquote(ctx, content, depth) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_blockquote(&ctx, &content, depth).await
                    }
                    VisitorRequest::Strong(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_strong(&ctx, &text).await
                    }
                    VisitorRequest::Emphasis(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_emphasis(&ctx, &text).await
                    }
                    VisitorRequest::Strikethrough(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_strikethrough(&ctx, &text).await
                    }
                    VisitorRequest::Underline(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_underline(&ctx, &text).await
                    }
                    VisitorRequest::Subscript(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_subscript(&ctx, &text).await
                    }
                    VisitorRequest::Superscript(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_superscript(&ctx, &text).await
                    }
                    VisitorRequest::Mark(ctx, text) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_mark(&ctx, &text).await
                    }
                    VisitorRequest::LineBreak(ctx) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_line_break(&ctx).await
                    }
                    VisitorRequest::HorizontalRule(ctx) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_horizontal_rule(&ctx).await
                    }
                    VisitorRequest::CustomElement(ctx, tag_name, html) => {
                        let mut visitor = visitor_clone.lock().await;
                        visitor.visit_custom_element(&ctx, &tag_name, &html).await
                    }
                };
                let _ = response_tx.send(result);
            }
        });

        Self {
            async_visitor,
            request_tx,
            response_rx,
        }
    }
}

#[cfg(feature = "async-visitor")]
impl crate::visitor::HtmlVisitor for AsyncToSyncVisitorBridge {
    fn visit_element_start(&mut self, ctx: &crate::visitor::NodeContext) -> crate::visitor::VisitResult {
        // Send request through channel
        if self.request_tx.send(VisitorRequest::ElementStart(ctx.clone())).is_err() {
            return crate::visitor::VisitResult::Continue;
        }
        // Wait for response
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_element_end(&mut self, ctx: &crate::visitor::NodeContext, output: &str) -> crate::visitor::VisitResult {
        // Send request through channel
        if self
            .request_tx
            .send(VisitorRequest::ElementEnd(ctx.clone(), output.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        // Wait for response
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_text(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Text(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_link(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        href: &str,
        text: &str,
        title: Option<&str>,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Link(
                ctx.clone(),
                href.to_string(),
                text.to_string(),
                title.map(std::string::ToString::to_string),
            ))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_image(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        src: &str,
        alt: &str,
        title: Option<&str>,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Image(
                ctx.clone(),
                src.to_string(),
                alt.to_string(),
                title.map(std::string::ToString::to_string),
            ))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_heading(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        level: u32,
        text: &str,
        id: Option<&str>,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Heading(
                ctx.clone(),
                level,
                text.to_string(),
                id.map(std::string::ToString::to_string),
            ))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_code_block(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        language: Option<&str>,
        code: &str,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::CodeBlock(
                ctx.clone(),
                language.map(std::string::ToString::to_string),
                code.to_string(),
            ))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_code_inline(&mut self, ctx: &crate::visitor::NodeContext, code: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::CodeInline(ctx.clone(), code.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_list_item(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        ordered: bool,
        marker: &str,
        text: &str,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::ListItem(
                ctx.clone(),
                ordered,
                marker.to_string(),
                text.to_string(),
            ))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_list_start(&mut self, ctx: &crate::visitor::NodeContext, ordered: bool) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::ListStart(ctx.clone(), ordered))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_list_end(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        ordered: bool,
        output: &str,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::ListEnd(ctx.clone(), ordered, output.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_table_start(&mut self, ctx: &crate::visitor::NodeContext) -> crate::visitor::VisitResult {
        if self.request_tx.send(VisitorRequest::TableStart(ctx.clone())).is_err() {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_table_row(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        cells: &[String],
        is_header: bool,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::TableRow(ctx.clone(), cells.to_vec(), is_header))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_table_end(&mut self, ctx: &crate::visitor::NodeContext, output: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::TableEnd(ctx.clone(), output.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_blockquote(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        content: &str,
        depth: usize,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Blockquote(ctx.clone(), content.to_string(), depth))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_strong(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Strong(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_emphasis(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Emphasis(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_strikethrough(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Strikethrough(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_underline(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Underline(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_subscript(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Subscript(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_superscript(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Superscript(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_line_break(&mut self, ctx: &crate::visitor::NodeContext) -> crate::visitor::VisitResult {
        if self.request_tx.send(VisitorRequest::LineBreak(ctx.clone())).is_err() {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_mark(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Mark(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_horizontal_rule(&mut self, ctx: &crate::visitor::NodeContext) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::HorizontalRule(ctx.clone()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_custom_element(
        &mut self,
        ctx: &crate::visitor::NodeContext,
        tag_name: &str,
        html: &str,
    ) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::CustomElement(
                ctx.clone(),
                tag_name.to_string(),
                html.to_string(),
            ))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx
            .lock()
            .unwrap()
            .recv()
            .unwrap_or(crate::visitor::VisitResult::Continue)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_build_node_context() {
        let mut attrs = BTreeMap::new();
        attrs.insert("id".to_string(), "main".to_string());
        attrs.insert("class".to_string(), "container".to_string());

        let ctx = build_node_context(NodeType::Div, "div", &attrs, 2, 3, Some("body"), false);

        assert_eq!(ctx.node_type, NodeType::Div);
        assert_eq!(ctx.tag_name, "div");
        assert_eq!(ctx.depth, 2);
        assert_eq!(ctx.index_in_parent, 3);
        assert_eq!(ctx.parent_tag, Some("body".to_string()));
        assert!(!ctx.is_inline);
        assert_eq!(ctx.attributes.len(), 2);
        assert_eq!(ctx.attributes.get("id"), Some(&"main".to_string()));
    }

    #[test]
    fn test_build_node_context_no_parent() {
        let attrs = BTreeMap::new();

        let ctx = build_node_context(NodeType::Html, "html", &attrs, 0, 0, None, false);

        assert_eq!(ctx.node_type, NodeType::Html);
        assert_eq!(ctx.parent_tag, None);
        assert!(ctx.attributes.is_empty());
    }

    #[test]
    fn test_dispatch_visitor_none() {
        let visitor: Option<Rc<RefCell<dyn HtmlVisitor>>> = None;

        let result = dispatch_visitor(&visitor, |v| {
            let ctx = NodeContext {
                node_type: NodeType::Text,
                tag_name: String::new(),
                attributes: BTreeMap::new(),
                depth: 0,
                index_in_parent: 0,
                parent_tag: None,
                is_inline: true,
            };
            v.visit_text(&ctx, "test")
        })
        .unwrap();

        assert!(result.is_continue());
    }

    #[derive(Debug)]
    struct TestVisitor {
        mode: TestMode,
    }

    #[derive(Debug)]
    enum TestMode {
        Continue,
        Custom,
        Skip,
        PreserveHtml,
        Error,
    }

    impl HtmlVisitor for TestVisitor {
        fn visit_text(&mut self, _ctx: &NodeContext, text: &str) -> VisitResult {
            match self.mode {
                TestMode::Continue => VisitResult::Continue,
                TestMode::Custom => VisitResult::Custom(format!("CUSTOM: {}", text)),
                TestMode::Skip => VisitResult::Skip,
                TestMode::PreserveHtml => VisitResult::PreserveHtml,
                TestMode::Error => VisitResult::Error("test error".to_string()),
            }
        }
    }

    #[test]
    fn test_dispatch_visitor_continue() {
        let visitor: Rc<RefCell<dyn HtmlVisitor>> = Rc::new(RefCell::new(TestVisitor {
            mode: TestMode::Continue,
        }));
        let visitor_opt = Some(visitor);

        let ctx = NodeContext {
            node_type: NodeType::Text,
            tag_name: String::new(),
            attributes: BTreeMap::new(),
            depth: 0,
            index_in_parent: 0,
            parent_tag: None,
            is_inline: true,
        };

        let result = dispatch_visitor(&visitor_opt, |v| v.visit_text(&ctx, "hello")).unwrap();

        assert!(result.is_continue());
    }

    #[test]
    fn test_dispatch_visitor_custom() {
        let visitor: Rc<RefCell<dyn HtmlVisitor>> = Rc::new(RefCell::new(TestVisitor { mode: TestMode::Custom }));
        let visitor_opt = Some(visitor);

        let ctx = NodeContext {
            node_type: NodeType::Text,
            tag_name: String::new(),
            attributes: BTreeMap::new(),
            depth: 0,
            index_in_parent: 0,
            parent_tag: None,
            is_inline: true,
        };

        let result = dispatch_visitor(&visitor_opt, |v| v.visit_text(&ctx, "hello")).unwrap();

        assert!(result.is_custom());
        assert_eq!(result.as_custom(), Some("CUSTOM: hello"));
    }

    #[test]
    fn test_dispatch_visitor_skip() {
        let visitor: Rc<RefCell<dyn HtmlVisitor>> = Rc::new(RefCell::new(TestVisitor { mode: TestMode::Skip }));
        let visitor_opt = Some(visitor);

        let ctx = NodeContext {
            node_type: NodeType::Text,
            tag_name: String::new(),
            attributes: BTreeMap::new(),
            depth: 0,
            index_in_parent: 0,
            parent_tag: None,
            is_inline: true,
        };

        let result = dispatch_visitor(&visitor_opt, |v| v.visit_text(&ctx, "hello")).unwrap();

        assert!(result.is_skip());
    }

    #[test]
    fn test_dispatch_visitor_preserve_html() {
        let visitor: Rc<RefCell<dyn HtmlVisitor>> = Rc::new(RefCell::new(TestVisitor {
            mode: TestMode::PreserveHtml,
        }));
        let visitor_opt = Some(visitor);

        let ctx = NodeContext {
            node_type: NodeType::Text,
            tag_name: String::new(),
            attributes: BTreeMap::new(),
            depth: 0,
            index_in_parent: 0,
            parent_tag: None,
            is_inline: true,
        };

        let result = dispatch_visitor(&visitor_opt, |v| v.visit_text(&ctx, "hello")).unwrap();

        assert!(result.is_preserve_html());
    }

    #[test]
    fn test_dispatch_visitor_error() {
        let visitor: Rc<RefCell<dyn HtmlVisitor>> = Rc::new(RefCell::new(TestVisitor { mode: TestMode::Error }));
        let visitor_opt = Some(visitor);

        let ctx = NodeContext {
            node_type: NodeType::Text,
            tag_name: String::new(),
            attributes: BTreeMap::new(),
            depth: 0,
            index_in_parent: 0,
            parent_tag: None,
            is_inline: true,
        };

        let result = dispatch_visitor(&visitor_opt, |v| v.visit_text(&ctx, "hello"));

        assert!(result.is_err());
        if let Err(ConversionError::Visitor(msg)) = result {
            assert_eq!(msg, "test error");
        } else {
            panic!("Expected Visitor error");
        }
    }

    #[test]
    fn test_visitor_dispatch_predicates() {
        let continue_dispatch = VisitorDispatch::Continue;
        assert!(continue_dispatch.is_continue());
        assert!(!continue_dispatch.is_custom());
        assert!(!continue_dispatch.is_skip());

        let custom_dispatch = VisitorDispatch::Custom("output".to_string());
        assert!(!custom_dispatch.is_continue());
        assert!(custom_dispatch.is_custom());
        assert!(!custom_dispatch.is_skip());

        let skip_dispatch = VisitorDispatch::Skip;
        assert!(!skip_dispatch.is_continue());
        assert!(!skip_dispatch.is_custom());
        assert!(skip_dispatch.is_skip());

        let preserve_dispatch = VisitorDispatch::PreserveHtml;
        assert!(!preserve_dispatch.is_continue());
        assert!(preserve_dispatch.is_preserve_html());
    }

    #[test]
    fn test_visitor_dispatch_into_custom() {
        let custom = VisitorDispatch::Custom("test".to_string());
        assert_eq!(custom.into_custom(), Some("test".to_string()));

        let continue_dispatch = VisitorDispatch::Continue;
        assert_eq!(continue_dispatch.into_custom(), None);
    }

    #[test]
    fn test_visitor_dispatch_as_custom() {
        let custom = VisitorDispatch::Custom("test".to_string());
        assert_eq!(custom.as_custom(), Some("test"));

        let skip = VisitorDispatch::Skip;
        assert_eq!(skip.as_custom(), None);
    }
}
