//! Table element handler for HTML to Markdown conversion.
//!
//! This module provides specialized handling for table elements including:
//! - Table structure detection and scanning (TableScan)
//! - Row and cell conversion to Markdown table format
//! - Cell content processing with colspan/rowspan support
//! - Layout table detection (tables used for visual layout)
//! - Integration with the visitor pattern for custom table handling
//!
//! Tables are converted to Markdown pipe-delimited format with header separators.
//! Layout tables (tables without proper semantic headers) may be converted to lists
//! instead of tables for better readability.

pub mod builder;
pub mod caption;
pub mod cell;
pub mod cells;
pub mod layout;
pub mod scanner;
pub(super) mod utils;

// Re-export types from parent module for submodule access
pub use super::super::{Context, DomContext};

// Re-export for use in converter.rs
pub(crate) use builder::handle_table;
pub(crate) use caption::handle_caption;

/// Dispatches table element handling to the main convert_table function.
///
/// # Usage in converter.rs
/// ```ignore
/// if "table" == tag_name {
///     crate::converter::block::table::handle_table(
///         node_handle,
///         parser,
///         output,
///         options,
///         ctx,
///         dom_ctx,
///         depth,
///     );
///     return;
/// }
/// ```
pub fn dispatch_table_handler(
    tag_name: &str,
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    output: &mut String,
    options: &crate::options::ConversionOptions,
    ctx: &super::super::Context,
    depth: usize,
    dom_ctx: &super::super::DomContext,
) -> bool {
    match tag_name {
        "table" => {
            builder::handle_table(node_handle, parser, output, options, ctx, dom_ctx, depth);
            true
        }
        _ => false,
    }
}

/// Handles table output with context-aware formatting.
///
/// This function wraps `handle_table` with list indentation and whitespace management logic.
/// It handles two distinct contexts:
///
/// 1. **List Context** (`ctx.in_list_item = true`):
///    - Indents table content using `indent_table_for_list` for proper nesting
///    - Preserves special caption formatting (lines starting with `*`)
///    - Adds newlines for proper list item separation
///
/// 2. **Normal Context**:
///    - Ensures proper spacing with double newlines around tables
///    - Handles various output state scenarios (empty, ends with newline, etc.)
///
/// # Arguments
/// * `node_handle` - The table node handle
/// * `parser` - The HTML parser instance
/// * `output` - The output string being built
/// * `options` - Conversion options (includes list indent type)
/// * `ctx` - Conversion context (includes list state)
/// * `dom_ctx` - DOM context for tree structure info
/// * `depth` - Current nesting depth
pub(crate) fn handle_table_with_context(
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    output: &mut String,
    options: &crate::options::ConversionOptions,
    ctx: &super::super::Context,
    dom_ctx: &super::super::DomContext,
    depth: usize,
) {
    let mut table_output = String::new();
    builder::handle_table(node_handle, parser, &mut table_output, options, ctx, dom_ctx, depth);

    if ctx.in_list_item {
        let has_caption = table_output.starts_with('*');

        if !has_caption {
            use crate::converter::main_helpers::trim_trailing_whitespace;
            trim_trailing_whitespace(output);
            if !output.is_empty() && !output.ends_with('\n') {
                output.push('\n');
            }
        }

        let indented = layout::indent_table_for_list(&table_output, ctx.list_depth, options);
        output.push_str(&indented);
    } else {
        if !output.ends_with("\n\n") {
            if output.is_empty() || !output.ends_with('\n') {
                output.push_str("\n\n");
            } else {
                output.push('\n');
            }
        }
        output.push_str(&table_output);
    }

    if !output.ends_with('\n') {
        output.push('\n');
    }
}
