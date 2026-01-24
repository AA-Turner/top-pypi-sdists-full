//! Cell and row handling for Markdown conversion.
//!
//! Provides functionality for processing table cells and rows, including:
//! - Row conversion to Markdown format
//! - Cell layout handling with colspan/rowspan support
//! - Layout table row conversion to list items

use std::borrow::Cow;

use super::cell::{collect_table_cells, convert_table_cell, get_colspan_rowspan};

/// Maximum allowed table columns to prevent unbounded memory usage.
const MAX_TABLE_COLS: usize = 1000;

/// Append a layout table row as a list item.
///
/// For tables used for visual layout, converts rows to list items
/// instead of table format for better readability.
///
/// # Arguments
/// * `row_handle` - Handle to the row element
/// * `parser` - HTML parser instance
/// * `output` - Mutable string to append content
/// * `options` - Conversion options
/// * `ctx` - Conversion context
/// * `dom_ctx` - DOM context
#[allow(clippy::trivially_copy_pass_by_ref)]
pub fn append_layout_row(
    row_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    output: &mut String,
    options: &crate::options::ConversionOptions,
    ctx: &super::super::super::Context,
    dom_ctx: &super::super::super::DomContext,
) {
    if let Some(tl::Node::Tag(row_tag)) = row_handle.get(parser) {
        let mut row_text = String::new();
        let row_children = row_tag.children();
        for cell_handle in row_children.top().iter() {
            if let Some(tl::Node::Tag(cell_tag)) = cell_handle.get(parser) {
                let cell_name: Cow<'_, str> = dom_ctx.tag_info(cell_handle.get_inner(), parser).map_or_else(
                    || normalized_tag_name(cell_tag.name().as_utf8_str()).into_owned().into(),
                    |info| Cow::Borrowed(info.name.as_str()),
                );
                if matches!(cell_name.as_ref(), "td" | "th" | "cell") {
                    let mut cell_text = String::new();
                    let cell_ctx = super::super::super::Context {
                        convert_as_inline: true,
                        ..ctx.clone()
                    };
                    let cell_children = cell_tag.children();
                    for cell_child in cell_children.top().iter() {
                        super::super::super::walk_node(
                            cell_child,
                            parser,
                            &mut cell_text,
                            options,
                            &cell_ctx,
                            0,
                            dom_ctx,
                        );
                    }
                    let cell_content = crate::text::normalize_whitespace_cow(&cell_text);
                    if !cell_content.trim().is_empty() {
                        if !row_text.is_empty() {
                            row_text.push(' ');
                        }
                        row_text.push_str(cell_content.trim());
                    }
                }
            }
        }

        let trimmed = row_text.trim();
        if !trimmed.is_empty() {
            if !output.is_empty() && !output.ends_with('\n') {
                output.push('\n');
            }
            let formatted = trimmed.strip_prefix("- ").unwrap_or(trimmed).trim_start();
            output.push_str("- ");
            output.push_str(formatted);
            output.push('\n');
        }
    }
}

/// Normalize HTML tag names to lowercase.
///
/// Converts tag names to a consistent lowercase form for comparison.
fn normalized_tag_name(raw: Cow<'_, str>) -> Cow<'_, str> {
    let lowercased = raw.to_lowercase();
    if lowercased.as_str() == raw.as_ref() {
        raw
    } else {
        Cow::Owned(lowercased)
    }
}

/// Convert a table row (tr) to Markdown format.
///
/// Processes all cells in a row, handling colspan and rowspan for proper
/// column alignment. Renders header separator row after the first row.
/// Integrates with visitor pattern for custom row handling.
///
/// # Arguments
/// * `node_handle` - Handle to the row element
/// * `parser` - HTML parser instance
/// * `output` - Mutable string to append row content
/// * `options` - Conversion options
/// * `ctx` - Conversion context (visitor, etc)
/// * `row_index` - Index of this row in the table
/// * `has_span` - Whether table has colspan/rowspan
/// * `rowspan_tracker` - Mutable array tracking rowspan remainder for each column
/// * `total_cols` - Total columns in the table
/// * `header_cols` - Columns to render in separator row
/// * `dom_ctx` - DOM context
/// * `depth` - Nesting depth
/// * `is_header` - Whether this is a header row
#[allow(clippy::too_many_arguments)]
#[cfg_attr(not(feature = "visitor"), allow(unused_variables))]
#[allow(clippy::trivially_copy_pass_by_ref)]
pub fn convert_table_row(
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    output: &mut String,
    options: &crate::options::ConversionOptions,
    ctx: &super::super::super::Context,
    row_index: usize,
    has_span: bool,
    rowspan_tracker: &mut [Option<usize>],
    total_cols: usize,
    header_cols: usize,
    dom_ctx: &super::super::super::DomContext,
    depth: usize,
    is_header: bool,
) {
    let mut row_text = String::with_capacity(256);
    let mut cells = Vec::new();

    collect_table_cells(node_handle, parser, dom_ctx, &mut cells);

    #[cfg(feature = "visitor")]
    let cell_contents: Vec<String> = if ctx.visitor.is_some() {
        cells
            .iter()
            .map(|cell_handle| {
                let mut text = String::new();
                let cell_ctx = super::super::super::Context {
                    in_table_cell: true,
                    ..ctx.clone()
                };
                if let Some(tl::Node::Tag(tag)) = cell_handle.get(parser) {
                    for child_handle in tag.children().top().iter() {
                        super::super::super::walk_node(child_handle, parser, &mut text, options, &cell_ctx, 0, dom_ctx);
                    }
                }
                crate::text::normalize_whitespace_cow(&text).trim().to_string()
            })
            .collect()
    } else {
        Vec::new()
    };

    #[cfg(feature = "visitor")]
    if let Some(ref visitor_handle) = ctx.visitor {
        use crate::visitor::{NodeContext, NodeType, VisitResult};
        use std::collections::BTreeMap;

        if let Some(tl::Node::Tag(tag)) = node_handle.get(parser) {
            let attributes: BTreeMap<String, String> = tag
                .attributes()
                .iter()
                .filter_map(|(k, v)| v.as_ref().map(|val| (k.to_string(), val.to_string())))
                .collect();

            let node_ctx = NodeContext {
                node_type: NodeType::TableRow,
                tag_name: "tr".to_string(),
                attributes,
                depth,
                index_in_parent: row_index,
                parent_tag: Some("table".to_string()),
                is_inline: false,
            };

            let visit_result = {
                let mut visitor = visitor_handle.borrow_mut();
                visitor.visit_table_row(&node_ctx, &cell_contents, is_header)
            };
            match visit_result {
                VisitResult::Continue => {}
                VisitResult::Skip => return,
                VisitResult::Custom(custom) => {
                    output.push_str(&custom);
                    return;
                }
                VisitResult::Error(err) => {
                    if ctx.visitor_error.borrow().is_none() {
                        *ctx.visitor_error.borrow_mut() = Some(err);
                    }
                    return;
                }
                VisitResult::PreserveHtml => {
                    output.push_str(&super::super::super::serialize_node(node_handle, parser));
                    return;
                }
            }
        }
    }

    if has_span {
        let mut col_index = 0;
        let mut cell_iter = cells.iter();

        loop {
            if col_index < total_cols {
                if let Some(Some(remaining_rows)) = rowspan_tracker.get_mut(col_index) {
                    if *remaining_rows > 0 {
                        row_text.push(' ');
                        row_text.push_str(" |");
                        *remaining_rows -= 1;
                        if *remaining_rows == 0 {
                            rowspan_tracker[col_index] = None;
                        }
                        col_index += 1;
                        continue;
                    }
                }
            }

            if let Some(cell_handle) = cell_iter.next() {
                convert_table_cell(cell_handle, parser, &mut row_text, options, ctx, "", dom_ctx);

                let (colspan, rowspan) = get_colspan_rowspan(cell_handle, parser);

                if rowspan > 1 && col_index < total_cols {
                    rowspan_tracker[col_index] = Some(rowspan - 1);
                }

                col_index = col_index.saturating_add(colspan);
            } else {
                break;
            }
        }
    } else {
        for cell_handle in &cells {
            convert_table_cell(cell_handle, parser, &mut row_text, options, ctx, "", dom_ctx);
        }
    }

    output.push('|');
    output.push_str(&row_text);
    output.push('\n');

    let is_first_row = row_index == 0;
    if is_first_row {
        let total_cols = header_cols.clamp(1, MAX_TABLE_COLS);
        output.push_str("| ");
        for i in 0..total_cols {
            if i > 0 {
                output.push_str(" | ");
            }
            output.push_str("---");
        }
        output.push_str(" |\n");
    }
}
