//! Link element handler for HTML to Markdown conversion.
//!
//! Handles `<a>` elements including:
//! - Basic link markdown output `[text](href "title")`
//! - Autolinks when text matches href
//! - Links containing heading elements
//! - Complex link content with mixed block/inline elements
//! - Visitor callback integration
//! - Link metadata collection

use std::collections::BTreeMap;

use crate::converter::Context;
use crate::converter::block::heading::{find_single_heading_child, heading_allows_inline_images, push_heading};
use crate::converter::dom_context::DomContext;
use crate::converter::inline::link::append_markdown_link;
use crate::converter::main::walk_node;
use crate::converter::utility::content::{
    collect_link_label_text, escape_link_label, get_text_content, normalize_link_label, normalized_tag_name,
    truncate_at_char_boundary,
};
use crate::options::ConversionOptions;
use crate::text;

#[cfg(feature = "visitor")]
use crate::converter::utility::serialization::serialize_node;

/// Handle an `<a>` (link) element and convert to Markdown.
///
/// This handler processes link elements including:
/// - Extracting href and title attributes
/// - Detecting autolinks (where text equals href)
/// - Handling links that contain heading elements
/// - Processing complex link content (mixed block/inline)
/// - Invoking visitor callbacks when the visitor feature is enabled
/// - Collecting link metadata when the metadata feature is enabled
/// - Generating appropriate markdown link output
#[allow(clippy::too_many_arguments)]
#[allow(clippy::too_many_lines)]
#[cfg_attr(not(feature = "visitor"), allow(unused_variables))]
pub fn handle_link(
    node_handle: &tl::NodeHandle,
    tag: &tl::HTMLTag,
    parser: &tl::Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    depth: usize,
    dom_ctx: &DomContext,
) {
    const MAX_LINK_LABEL_LEN: usize = 512;

    let href_attr = tag
        .attributes()
        .get("href")
        .flatten()
        .map(|v| text::decode_html_entities(&v.as_utf8_str()));
    let title = tag
        .attributes()
        .get("title")
        .flatten()
        .map(|v| v.as_utf8_str().to_string());

    if let Some(href) = href_attr {
        let raw_text = text::normalize_whitespace(&get_text_content(node_handle, parser, dom_ctx))
            .trim()
            .to_string();

        let is_autolink = options.autolinks
            && !options.default_title
            && !href.is_empty()
            && (raw_text == href || (href.starts_with("mailto:") && raw_text == href[7..]));

        if is_autolink {
            output.push('<');
            if href.starts_with("mailto:") && raw_text == href[7..] {
                output.push_str(&raw_text);
            } else {
                output.push_str(&href);
            }
            output.push('>');
            return;
        }

        if let Some((heading_level, heading_handle)) = find_single_heading_child(*node_handle, parser) {
            if let Some(heading_node) = heading_handle.get(parser) {
                if let tl::Node::Tag(heading_tag) = heading_node {
                    let heading_name = normalized_tag_name(heading_tag.name().as_utf8_str()).into_owned();
                    let mut heading_text = String::new();
                    let heading_ctx = Context {
                        in_heading: true,
                        convert_as_inline: true,
                        heading_allow_inline_images: heading_allows_inline_images(
                            &heading_name,
                            &ctx.keep_inline_images_in,
                        ),
                        ..ctx.clone()
                    };
                    walk_node(
                        &heading_handle,
                        parser,
                        &mut heading_text,
                        options,
                        &heading_ctx,
                        depth + 1,
                        dom_ctx,
                    );
                    let trimmed_heading = heading_text.trim();
                    if !trimmed_heading.is_empty() {
                        let escaped_label = escape_link_label(trimmed_heading);
                        let mut link_buffer = String::new();
                        append_markdown_link(
                            &mut link_buffer,
                            &escaped_label,
                            href.as_str(),
                            title.as_deref(),
                            raw_text.as_str(),
                            options,
                        );
                        push_heading(output, ctx, options, heading_level, link_buffer.as_str());
                        return;
                    }
                }
            }
        }

        let children: Vec<_> = tag.children().top().iter().copied().collect();
        let (inline_label, _block_nodes, saw_block) = collect_link_label_text(&children, parser, dom_ctx);
        let mut label = if saw_block {
            let mut content = String::new();
            let link_ctx = Context {
                inline_depth: ctx.inline_depth + 1,
                convert_as_inline: true,
                ..ctx.clone()
            };
            for child_handle in &children {
                let mut child_buf = String::new();
                walk_node(
                    child_handle,
                    parser,
                    &mut child_buf,
                    options,
                    &link_ctx,
                    depth + 1,
                    dom_ctx,
                );
                if !child_buf.trim().is_empty()
                    && !content.is_empty()
                    && !content.chars().last().is_none_or(char::is_whitespace)
                    && !child_buf.chars().next().is_none_or(char::is_whitespace)
                {
                    content.push(' ');
                }
                content.push_str(&child_buf);
            }
            if content.trim().is_empty() {
                normalize_link_label(&inline_label)
            } else {
                normalize_link_label(&content)
            }
        } else {
            let mut content = String::new();
            let link_ctx = Context {
                inline_depth: ctx.inline_depth + 1,
                ..ctx.clone()
            };
            for child_handle in &children {
                walk_node(
                    child_handle,
                    parser,
                    &mut content,
                    options,
                    &link_ctx,
                    depth + 1,
                    dom_ctx,
                );
            }
            normalize_link_label(&content)
        };

        if label.is_empty() && saw_block {
            let fallback = text::normalize_whitespace(&get_text_content(node_handle, parser, dom_ctx));
            label = normalize_link_label(&fallback);
        }

        if label.is_empty() && !raw_text.is_empty() {
            label = normalize_link_label(&raw_text);
        }

        if label.is_empty() && !href.is_empty() && !children.is_empty() {
            label = href.clone();
        }

        if label.len() > MAX_LINK_LABEL_LEN {
            truncate_at_char_boundary(&mut label, MAX_LINK_LABEL_LEN);
            label.push('…');
        }

        let escaped_label = escape_link_label(&label);

        #[cfg(feature = "visitor")]
        let link_output = if let Some(ref visitor_handle) = ctx.visitor {
            use crate::visitor::{NodeContext, NodeType, VisitResult};

            let attributes: BTreeMap<String, String> = tag
                .attributes()
                .iter()
                .filter_map(|(k, v)| v.as_ref().map(|val| (k.to_string(), val.to_string())))
                .collect();

            let node_id = node_handle.get_inner();
            let parent_tag = dom_ctx.parent_tag_name(node_id, parser);
            let index_in_parent = dom_ctx.get_sibling_index(node_id).unwrap_or(0);

            let node_ctx = NodeContext {
                node_type: NodeType::Link,
                tag_name: "a".to_string(),
                attributes,
                depth,
                index_in_parent,
                parent_tag,
                is_inline: true,
            };

            let visit_result = {
                let mut visitor = visitor_handle.borrow_mut();
                visitor.visit_link(&node_ctx, &href, &label, title.as_deref())
            };
            match visit_result {
                VisitResult::Continue => {
                    let mut buf = String::new();
                    append_markdown_link(
                        &mut buf,
                        &escaped_label,
                        href.as_str(),
                        title.as_deref(),
                        label.as_str(),
                        options,
                    );
                    Some(buf)
                }
                VisitResult::Custom(custom) => Some(custom),
                VisitResult::Skip => None,
                VisitResult::Error(err) => {
                    if ctx.visitor_error.borrow().is_none() {
                        *ctx.visitor_error.borrow_mut() = Some(err);
                    }
                    None
                }
                VisitResult::PreserveHtml => Some(serialize_node(node_handle, parser)),
            }
        } else {
            let mut buf = String::new();
            append_markdown_link(
                &mut buf,
                &escaped_label,
                href.as_str(),
                title.as_deref(),
                label.as_str(),
                options,
            );
            Some(buf)
        };

        #[cfg(not(feature = "visitor"))]
        let link_output = {
            let mut buf = String::new();
            append_markdown_link(
                &mut buf,
                &escaped_label,
                href.as_str(),
                title.as_deref(),
                label.as_str(),
                options,
            );
            Some(buf)
        };

        if let Some(link_text) = link_output {
            output.push_str(&link_text);
        }

        #[cfg(feature = "metadata")]
        if ctx.metadata_wants_links {
            if let Some(ref collector) = ctx.metadata_collector {
                let rel_attr = tag
                    .attributes()
                    .get("rel")
                    .flatten()
                    .map(|v| v.as_utf8_str().to_string());
                let mut attributes_map = BTreeMap::new();
                for (key, value_opt) in tag.attributes().iter() {
                    let key_str = key.to_string();
                    if key_str == "href" {
                        continue;
                    }

                    let value = value_opt.map(|v| v.to_string()).unwrap_or_default();
                    attributes_map.insert(key_str, value);
                }
                collector
                    .borrow_mut()
                    .add_link(href.clone(), label.clone(), title.clone(), rel_attr, attributes_map);
            }
        }
    } else {
        let children = tag.children();
        {
            for child_handle in children.top().iter() {
                walk_node(child_handle, parser, output, options, ctx, depth + 1, dom_ctx);
            }
        }
    }
}
