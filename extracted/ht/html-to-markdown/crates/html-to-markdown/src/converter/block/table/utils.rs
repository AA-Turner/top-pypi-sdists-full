//! Utility functions for table processing.
//!
//! Provides helper functions for tag name normalization and comparison.

use std::borrow::Cow;

/// Normalize HTML tag names to lowercase.
///
/// Converts tag names to a consistent lowercase form for comparison.
pub(super) fn normalized_tag_name(raw: Cow<'_, str>) -> Cow<'_, str> {
    let lowercased = raw.to_lowercase();
    if lowercased.as_str() == raw.as_ref() {
        raw
    } else {
        Cow::Owned(lowercased)
    }
}

/// Check tag name equality with case-insensitive comparison.
pub(super) fn tag_name_eq(name: Cow<'_, str>, needle: &str) -> bool {
    name.eq_ignore_ascii_case(needle)
}

/// Check if a node has a specific tag name.
///
/// Handles both direct tag matching and DOM context-based tag resolution.
///
/// # Arguments
/// * `node_handle` - Handle to the node
/// * `parser` - HTML parser instance
/// * `dom_ctx` - DOM context for tag name resolution
/// * `name` - Expected tag name
///
/// # Returns
/// True if node has the specified tag name
#[allow(clippy::trivially_copy_pass_by_ref)]
pub(super) fn is_tag_name(
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    dom_ctx: &super::super::super::DomContext,
    name: &str,
) -> bool {
    if let Some(info) = dom_ctx.tag_info(node_handle.get_inner(), parser) {
        return info.name == name;
    }
    matches!(
        node_handle.get(parser),
        Some(tl::Node::Tag(tag)) if tag_name_eq(tag.name().as_utf8_str(), name)
    )
}
