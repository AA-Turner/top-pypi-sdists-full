//! Definition list handling (dl, dt, dd elements).
//!
//! Processes definition lists with:
//! - Definition terms (dt)
//! - Definition descriptions (dd)
//! - Plain block formatting (no Pandoc colon syntax)

use crate::options::ConversionOptions;
use tl;

// Type aliases for Context and DomContext to avoid circular imports
type Context = crate::converter::Context;
type DomContext = crate::converter::DomContext;

/// Handle definition list element (<dl>).
///
/// Groups dt/dd pairs and formats them with proper Markdown separation.
pub(crate) fn handle_dl(
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    depth: usize,
    dom_ctx: &DomContext,
) {
    let tag = match node_handle.get(parser) {
        Some(tl::Node::Tag(t)) => t,
        _ => return,
    };

    if ctx.convert_as_inline {
        let children = tag.children();
        {
            for child_handle in children.top().iter() {
                use crate::converter::walk_node;
                walk_node(child_handle, parser, output, options, ctx, depth, dom_ctx);
            }
        }
        return;
    }

    let mut content = String::new();
    let children = tag.children();
    {
        for child_handle in children.top().iter() {
            crate::converter::walk_node(child_handle, parser, &mut content, options, ctx, depth, dom_ctx);
        }
    }

    let trimmed = content.trim();
    if !trimmed.is_empty() {
        if !output.is_empty() && !output.ends_with("\n\n") {
            output.push_str("\n\n");
        }
        output.push_str(trimmed);
        output.push_str("\n\n");
    }
}

/// Handle definition term element (<dt>).
///
/// Outputs the term text followed by a newline.
pub(crate) fn handle_dt(
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    depth: usize,
    dom_ctx: &DomContext,
) {
    let tag = match node_handle.get(parser) {
        Some(tl::Node::Tag(t)) => t,
        _ => return,
    };

    let mut content = String::with_capacity(64);
    let children = tag.children();
    {
        for child_handle in children.top().iter() {
            crate::converter::walk_node(child_handle, parser, &mut content, options, ctx, depth + 1, dom_ctx);
        }
    }
    let trimmed = content.trim();
    if !trimmed.is_empty() {
        if ctx.convert_as_inline {
            output.push_str(trimmed);
        } else {
            output.push_str(trimmed);
            output.push('\n');
        }
    }
}

/// Handle definition description element (<dd>).
///
/// Outputs the description as a plain block.
pub(crate) fn handle_dd(
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    depth: usize,
    dom_ctx: &DomContext,
) {
    let tag = match node_handle.get(parser) {
        Some(tl::Node::Tag(t)) => t,
        _ => return,
    };

    let mut content = String::with_capacity(128);
    let children = tag.children();
    {
        for child_handle in children.top().iter() {
            crate::converter::walk_node(child_handle, parser, &mut content, options, ctx, depth + 1, dom_ctx);
        }
    }

    let trimmed = content.trim();

    if ctx.convert_as_inline {
        if !trimmed.is_empty() {
            output.push_str(trimmed);
        }
    } else if !trimmed.is_empty() {
        output.push_str(trimmed);
        output.push_str("\n\n");
    }
}
