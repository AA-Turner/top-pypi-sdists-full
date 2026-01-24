//! Embedded media element handling (iframe, video, audio, source).
//!
//! Converts various embedded media elements:
//! - **iframe**: Embedded content frames, outputs src as a link
//! - **video**: Video elements with src or nested source elements
//! - **audio**: Audio elements with src or nested source elements
//! - **source**: Media source elements (handled within parent elements)
//! - **picture**: Picture elements with responsive image sources

use std::borrow::Cow;
use tl::{HTMLTag, NodeHandle, Parser};

use crate::converter::Context;
use crate::converter::dom_context::DomContext;
use crate::options::ConversionOptions;

/// Extract src attribute from media element (audio, video, iframe).
pub(crate) fn extract_media_src<'a>(tag: &'a HTMLTag<'a>) -> Cow<'a, str> {
    tag.attributes()
        .get("src")
        .flatten()
        .map(|v| v.as_utf8_str())
        .unwrap_or_else(|| Cow::Borrowed(""))
}

/// Try to find source src from nested source element.
///
/// Used by audio and video elements to extract src from child <source> elements
/// when the parent doesn't have a src attribute.
pub(crate) fn find_source_src<'a, T>(children: T, parser: &'a Parser) -> Option<Cow<'a, str>>
where
    T: IntoIterator<Item = &'a NodeHandle>,
{
    for child_handle in children {
        if let Some(tl::Node::Tag(child_tag)) = child_handle.get(parser) {
            if tag_name_eq(child_tag.name().as_utf8_str(), "source") {
                return child_tag.attributes().get("src").flatten().map(|v| v.as_utf8_str());
            }
        }
    }
    None
}

/// Check if tag is a source element.
pub(crate) fn is_source_element(tag: &HTMLTag) -> bool {
    tag_name_eq(tag.name().as_utf8_str(), "source")
}

/// Compare tag name with needle (case-insensitive).
fn tag_name_eq<'a>(name: impl AsRef<str>, needle: &str) -> bool {
    name.as_ref().eq_ignore_ascii_case(needle)
}

/// Determine if media should output source link in markdown.
///
/// Returns true if src is non-empty.
pub(crate) fn should_output_media_link(src: &str) -> bool {
    !src.is_empty()
}

/// Handle audio element conversion to Markdown.
///
/// Extracts src from audio tag or nested source elements, outputs as a link,
/// and processes fallback content (e.g., browser compatibility text).
pub(crate) fn handle_audio(
    _node_handle: &NodeHandle,
    tag: &HTMLTag,
    parser: &Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    depth: usize,
    dom_ctx: &DomContext,
) {
    use crate::converter::main::walk_node;

    let children = tag.children();
    let src = if extract_media_src(tag).is_empty() {
        find_source_src(children.top().iter(), parser).unwrap_or(Cow::Borrowed(""))
    } else {
        extract_media_src(tag)
    };

    if should_output_media_link(&src) {
        output.push('[');
        output.push_str(&src);
        output.push_str("](");
        output.push_str(&src);
        output.push(')');
        if !ctx.in_paragraph && !ctx.convert_as_inline {
            output.push_str("\n\n");
        }
    }

    let mut fallback = String::new();
    for child_handle in tag.children().top().iter() {
        let is_source = if let Some(tl::Node::Tag(child_tag)) = child_handle.get(parser) {
            is_source_element(child_tag)
        } else {
            false
        };

        if !is_source {
            walk_node(child_handle, parser, &mut fallback, options, ctx, depth + 1, dom_ctx);
        }
    }
    if !fallback.is_empty() {
        output.push_str(fallback.trim());
        if !ctx.in_paragraph && !ctx.convert_as_inline {
            output.push_str("\n\n");
        }
    }
}

/// Handle video element conversion to Markdown.
///
/// Extracts src from video tag or nested source elements, outputs as a link,
/// and processes fallback content (e.g., browser compatibility text).
pub(crate) fn handle_video(
    _node_handle: &NodeHandle,
    tag: &HTMLTag,
    parser: &Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    depth: usize,
    dom_ctx: &DomContext,
) {
    use crate::converter::main::walk_node;

    let children = tag.children();
    let src = if extract_media_src(tag).is_empty() {
        find_source_src(children.top().iter(), parser).unwrap_or(Cow::Borrowed(""))
    } else {
        extract_media_src(tag)
    };

    if should_output_media_link(&src) {
        output.push('[');
        output.push_str(&src);
        output.push_str("](");
        output.push_str(&src);
        output.push(')');
        if !ctx.in_paragraph && !ctx.convert_as_inline {
            output.push_str("\n\n");
        }
    }

    let mut fallback = String::new();
    for child_handle in tag.children().top().iter() {
        let is_source = if let Some(tl::Node::Tag(child_tag)) = child_handle.get(parser) {
            is_source_element(child_tag)
        } else {
            false
        };

        if !is_source {
            walk_node(child_handle, parser, &mut fallback, options, ctx, depth + 1, dom_ctx);
        }
    }
    if !fallback.is_empty() {
        output.push_str(fallback.trim());
        if !ctx.in_paragraph && !ctx.convert_as_inline {
            output.push_str("\n\n");
        }
    }
}

/// Handle picture element conversion to Markdown.
///
/// Finds and processes the first child img element, skipping source elements.
pub(crate) fn handle_picture(
    _node_handle: &NodeHandle,
    tag: &HTMLTag,
    parser: &Parser,
    output: &mut String,
    options: &ConversionOptions,
    ctx: &Context,
    depth: usize,
    dom_ctx: &DomContext,
) {
    use crate::converter::main::walk_node;

    for child_handle in tag.children().top().iter() {
        if let Some(tl::Node::Tag(child_tag)) = child_handle.get(parser) {
            if tag_name_eq(child_tag.name().as_utf8_str(), "img") {
                walk_node(child_handle, parser, output, options, ctx, depth, dom_ctx);
                break;
            }
        }
    }
}

/// Handle iframe element conversion to Markdown.
///
/// Extracts src attribute from iframe and outputs as a markdown link.
/// iframes cannot be embedded in markdown, so we just provide a link to the source.
pub(crate) fn handle_iframe(tag: &HTMLTag, output: &mut String, ctx: &Context) {
    let src = tag
        .attributes()
        .get("src")
        .flatten()
        .map_or(Cow::Borrowed(""), |v| v.as_utf8_str());

    if !src.is_empty() {
        output.push('[');
        output.push_str(&src);
        output.push_str("](");
        output.push_str(&src);
        output.push(')');
        if !ctx.in_paragraph && !ctx.convert_as_inline {
            output.push_str("\n\n");
        }
    }
}
