//! HtmlVisitor trait implementation for AsyncToSyncVisitorBridge.
//!
//! This module implements the sync `HtmlVisitor` trait for the async-to-sync bridge,
//! translating each method call into a channel request/response pair.

#[cfg(feature = "async-visitor")]
use super::bridge::{AsyncToSyncVisitorBridge, VisitorRequest};

#[cfg(feature = "async-visitor")]
impl crate::visitor::HtmlVisitor for AsyncToSyncVisitorBridge {
    fn visit_element_start(&mut self, ctx: &crate::visitor::NodeContext) -> crate::visitor::VisitResult {
        if self.request_tx.send(VisitorRequest::ElementStart(ctx.clone())).is_err() {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_element_end(&mut self, ctx: &crate::visitor::NodeContext, output: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::ElementEnd(ctx.clone(), output.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_text(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Text(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_code_inline(&mut self, ctx: &crate::visitor::NodeContext, code: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::CodeInline(ctx.clone(), code.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_list_start(&mut self, ctx: &crate::visitor::NodeContext, ordered: bool) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::ListStart(ctx.clone(), ordered))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_table_start(&mut self, ctx: &crate::visitor::NodeContext) -> crate::visitor::VisitResult {
        if self.request_tx.send(VisitorRequest::TableStart(ctx.clone())).is_err() {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_table_end(&mut self, ctx: &crate::visitor::NodeContext, output: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::TableEnd(ctx.clone(), output.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_strong(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Strong(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_emphasis(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Emphasis(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_strikethrough(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Strikethrough(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_underline(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Underline(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_subscript(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Subscript(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_superscript(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Superscript(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_mark(&mut self, ctx: &crate::visitor::NodeContext, text: &str) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::Mark(ctx.clone(), text.to_string()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }

    fn visit_horizontal_rule(&mut self, ctx: &crate::visitor::NodeContext) -> crate::visitor::VisitResult {
        if self
            .request_tx
            .send(VisitorRequest::HorizontalRule(ctx.clone()))
            .is_err()
        {
            return crate::visitor::VisitResult::Continue;
        }
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
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
        self.response_rx.recv().unwrap_or(crate::visitor::VisitResult::Continue)
    }
}
