//! Handler for line break elements (br).
//!
//! Converts HTML line break tags to Markdown line breaks using the configured
//! newline style (spaces, backslash, or plain newline).

use crate::converter::main_helpers::trim_trailing_whitespace;
use crate::options::{ConversionOptions, NewlineStyle};
use tl::{NodeHandle, Parser};

// Type aliases for Context and DomContext to avoid circular imports
type Context = crate::converter::Context;
type DomContext = crate::converter::DomContext;

/// Handle line break elements (br).
///
/// Converts to appropriate Markdown line break syntax based on the configured
/// newline style and current context (e.g., in headings).
pub(crate) fn handle(
    _node_handle: &NodeHandle,
    _parser: &Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    _depth: usize,
    _dom_ctx: &DomContext,
) {
    if ctx.in_heading {
        trim_trailing_whitespace(output);
        output.push_str("  ");
    } else {
        if output.is_empty() || output.ends_with('\n') {
            output.push('\n');
        } else {
            match options.newline_style {
                NewlineStyle::Spaces => output.push_str("  \n"),
                NewlineStyle::Backslash => output.push_str("\\\n"),
            }
        }
    }
}
