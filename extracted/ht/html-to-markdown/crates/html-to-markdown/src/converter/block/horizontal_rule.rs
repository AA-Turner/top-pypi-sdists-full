//! Handler for horizontal rule elements (hr).
//!
//! Converts HTML horizontal rule tags to Markdown horizontal rules (---)
//! with appropriate spacing handling based on context.

use crate::converter::main_helpers::trim_trailing_whitespace;
use crate::converter::utility::siblings::get_previous_sibling_tag;
use tl::{NodeHandle, Parser};

// Type aliases for Context and DomContext to avoid circular imports
type Context = crate::converter::Context;
type DomContext = crate::converter::DomContext;

/// Handle horizontal rule elements (hr).
///
/// Converts to Markdown horizontal rule (---) with appropriate blank line
/// spacing based on context and previous siblings.
pub(crate) fn handle(
    node_handle: &NodeHandle,
    parser: &Parser,
    output: &mut String,
    _options: &crate::options::ConversionOptions,
    ctx: &Context,
    _depth: usize,
    dom_ctx: &DomContext,
) {
    if !output.is_empty() {
        let prev_tag = get_previous_sibling_tag(node_handle, parser, dom_ctx);
        let last_line_is_blockquote = output
            .rsplit('\n')
            .find(|line| !line.trim().is_empty())
            .is_some_and(|line| line.trim_start().starts_with('>'));
        let needs_blank_line = !ctx.in_paragraph && !matches!(prev_tag, Some("blockquote")) && !last_line_is_blockquote;

        // If previous element was a blockquote, it added \n\n; reduce to \n
        if matches!(prev_tag, Some("blockquote")) && output.ends_with("\n\n") {
            output.truncate(output.len() - 1);
        } else if ctx.in_paragraph || !needs_blank_line {
            if !output.ends_with('\n') {
                output.push('\n');
            }
        } else {
            trim_trailing_whitespace(output);
            if output.ends_with('\n') {
                if !output.ends_with("\n\n") {
                    output.push('\n');
                }
            } else {
                output.push_str("\n\n");
            }
        }
    }
    output.push_str("---\n");
}
