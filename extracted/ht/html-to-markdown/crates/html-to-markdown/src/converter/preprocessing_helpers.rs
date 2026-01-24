//! HTML preprocessing and validation helpers.
//!
//! This module contains helper functions for preprocessing HTML before conversion,
//! including validation and normalization checks.

use crate::converter::dom_context::DomContext;
use crate::converter::main_helpers::is_inline_element;
use crate::converter::utility::attributes::element_has_navigation_hint;
use crate::converter::utility::content::normalized_tag_name;
use crate::options::ConversionOptions;

/// Check if an inline ancestor element is allowed to contain block-level elements.
pub(crate) fn inline_ancestor_allows_block(tag_name: &str) -> bool {
    matches!(tag_name, "a" | "ins" | "del")
}

/// Detect block elements that were incorrectly nested under inline ancestors.
///
/// Excludes elements inside `<pre>` or `<code>` blocks, as they have special
/// whitespace preservation rules and should not be repaired.
pub(crate) fn has_inline_block_misnest(dom_ctx: &DomContext, parser: &tl::Parser) -> bool {
    for handle in dom_ctx.node_map.iter().flatten() {
        if let Some(tl::Node::Tag(_tag)) = handle.get(parser) {
            let is_block = dom_ctx
                .tag_info(handle.get_inner(), parser)
                .map(|info| info.is_block)
                .unwrap_or(false);
            if is_block {
                // Check if this block element or any ancestor is pre/code
                let mut check_parent = Some(handle.get_inner());
                let mut inside_preformatted = false;
                while let Some(node_id) = check_parent {
                    if let Some(info) = dom_ctx.tag_info(node_id, parser) {
                        if matches!(info.name.as_str(), "pre" | "code") {
                            inside_preformatted = true;
                            break;
                        }
                    }
                    check_parent = dom_ctx.parent_of(node_id);
                }

                // Skip misnesting check for elements inside pre/code blocks
                if inside_preformatted {
                    continue;
                }

                let mut current = dom_ctx.parent_of(handle.get_inner());
                while let Some(parent_id) = current {
                    if let Some(parent_info) = dom_ctx.tag_info(parent_id, parser) {
                        if is_inline_element(&parent_info.name) && !inline_ancestor_allows_block(&parent_info.name) {
                            return true;
                        }
                    } else if let Some(parent_handle) = dom_ctx.node_handle(parent_id) {
                        if let Some(tl::Node::Tag(parent_tag)) = parent_handle.get(parser) {
                            let parent_name = normalized_tag_name(parent_tag.name().as_utf8_str());
                            if is_inline_element(&parent_name) && !inline_ancestor_allows_block(&parent_name) {
                                return true;
                            }
                        }
                    }
                    current = dom_ctx.parent_of(parent_id);
                }
            }
        }
    }

    false
}

/// Determine if a node should be dropped during preprocessing.
pub(crate) fn should_drop_for_preprocessing(
    node_handle: &tl::NodeHandle,
    tag_name: &str,
    tag: &tl::HTMLTag,
    parser: &tl::Parser,
    dom_ctx: &DomContext,
    options: &ConversionOptions,
) -> bool {
    // If preprocessing is globally disabled, don't drop any nodes
    if !options.preprocessing.enabled {
        return false;
    }

    if !options.preprocessing.remove_navigation {
        return false;
    }

    let has_nav_hint = element_has_navigation_hint(tag);

    if tag_name == "nav" {
        return true;
    }

    if tag_name == "header" {
        use crate::converter::utility::attributes::has_semantic_content_ancestor;
        let inside_semantic_content = has_semantic_content_ancestor(node_handle, parser, dom_ctx);
        if !inside_semantic_content {
            return true;
        }
        if has_nav_hint {
            return true;
        }
    } else if tag_name == "footer" || tag_name == "aside" {
        if has_nav_hint {
            return true;
        }
    }

    false
}
