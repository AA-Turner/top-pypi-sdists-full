//! Async-to-sync visitor bridge for integrating async visitors with synchronous converters.
//!
//! This module provides the `AsyncToSyncVisitorBridge` struct that wraps an async visitor
//! and implements the sync `HtmlVisitor` trait using channel-based communication.

#[cfg(feature = "async-visitor")]
use super::AsyncVisitorHandle;

/// Request types for visitor method calls over the channel.
#[cfg(feature = "async-visitor")]
pub(super) enum VisitorRequest {
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

/// Bridge that wraps an async visitor and implements the sync `HtmlVisitor` trait.
///
/// This bridge uses a channel-based approach to avoid blocking:
/// 1. Sync converter sends visitor call request through channel
/// 2. Async runtime receives request and awaits JS callback
/// 3. Result sent back through response channel
/// 4. Sync converter receives result and continues
///
/// This approach avoids deadlock by never blocking on async operations.
#[cfg(feature = "async-visitor")]
pub struct AsyncToSyncVisitorBridge {
    #[allow(dead_code)]
    pub(super) async_visitor: AsyncVisitorHandle,
    pub(super) request_tx: tokio::sync::mpsc::UnboundedSender<VisitorRequest>,
    pub(super) response_rx: std::sync::mpsc::Receiver<crate::visitor::VisitResult>,
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
