//! Helper functions for HTML to Markdown conversion.
//!
//! This module contains utility functions used by the main conversion pipeline,
//! including preprocessing helpers, HTML repair, and metadata formatting.

use std::collections::BTreeMap;

use crate::options::ConversionOptions;

/// Compare two tag names case-insensitively.
pub fn tag_name_eq(a: impl AsRef<str>, b: &str) -> bool {
    a.as_ref().eq_ignore_ascii_case(b)
}

/// Remove trailing spaces and tabs from a string.
pub fn trim_trailing_whitespace(output: &mut String) {
    while output.ends_with(' ') || output.ends_with('\t') {
        output.pop();
    }
}

/// Remove trailing spaces/tabs from every line while preserving newlines.
pub fn trim_line_end_whitespace(output: &mut String) {
    if output.is_empty() {
        return;
    }

    let mut cleaned = String::with_capacity(output.len());
    for (idx, line) in output.split('\n').enumerate() {
        if idx > 0 {
            cleaned.push('\n');
        }

        let has_soft_break = line.ends_with("  ");
        let trimmed = line.trim_end_matches([' ', '\t']);

        cleaned.push_str(trimmed);
        if has_soft_break {
            cleaned.push_str("  ");
        }
    }

    cleaned.push('\n');
    *output = cleaned;
}

// has_inline_block_misnest and should_drop_for_preprocessing moved back to main.rs
// due to DomContext circular dependency

/// Check if HTML contains custom element tags.
pub fn has_custom_element_tags(html: &str) -> bool {
    // Custom elements must have a hyphen in their TAG NAME, not in attributes
    // Look for patterns like <foo-bar> or </foo-bar>
    let bytes = html.as_bytes();
    let len = bytes.len();
    let mut i = 0;

    while i < len {
        if bytes[i] == b'<' {
            i += 1;
            if i >= len {
                break;
            }

            // Skip closing tag marker
            if bytes[i] == b'/' {
                i += 1;
                if i >= len {
                    break;
                }
            }

            // Skip whitespace
            while i < len && bytes[i].is_ascii_whitespace() {
                i += 1;
            }

            // Now we're at the start of a tag name - check if it contains a hyphen
            let tag_start = i;
            while i < len {
                let ch = bytes[i];
                if ch == b'>' || ch == b'/' || ch.is_ascii_whitespace() {
                    // End of tag name
                    let tag_name = &bytes[tag_start..i];
                    if tag_name.contains(&b'-') {
                        return true;
                    }
                    break;
                }
                i += 1;
            }
        } else {
            i += 1;
        }
    }

    false
}

/// Try to repair HTML using html5ever parser.
///
/// Returns Some(repaired_html) if repair was successful, None otherwise.
pub fn repair_with_html5ever(input: &str) -> Option<String> {
    use html5ever::serialize::{SerializeOpts, serialize};
    use html5ever::tendril::TendrilSink;
    use markup5ever_rcdom::{RcDom, SerializableHandle};

    let dom = html5ever::parse_document(RcDom::default(), Default::default())
        .from_utf8()
        .read_from(&mut input.as_bytes())
        .ok()?;

    let mut buf = Vec::with_capacity(input.len());
    let handle = SerializableHandle::from(dom.document);
    serialize(&mut buf, &handle, SerializeOpts::default()).ok()?;
    String::from_utf8(buf).ok()
}

/// Format metadata as YAML frontmatter.
pub fn format_metadata_frontmatter(metadata: &BTreeMap<String, String>) -> String {
    let mut result = String::from("---\n");
    for (key, value) in metadata {
        use std::fmt::Write as _;
        let _ = writeln!(&mut result, "{}: {}", key, value);
    }
    result.push_str("---\n");
    result
}

// should_drop_for_preprocessing moved back to main.rs due to DomContext dependency

/// Extract metadata from the head element.
pub fn extract_head_metadata(
    node_handle: &tl::NodeHandle,
    parser: &tl::Parser,
    options: &ConversionOptions,
) -> BTreeMap<String, String> {
    let mut metadata = BTreeMap::new();

    if let Some(tl::Node::Tag(tag)) = node_handle.get(parser) {
        // Check if this is a head tag
        if tag.name().as_utf8_str().eq_ignore_ascii_case("head") {
            let children = tag.children();
            for child_handle in children.top().iter() {
                if let Some(tl::Node::Tag(child_tag)) = child_handle.get(parser) {
                    // Look for meta tags
                    if child_tag.name().as_utf8_str().eq_ignore_ascii_case("meta")
                        && !options.strip_tags.contains(&"meta".to_string())
                        && !options.preserve_tags.contains(&"meta".to_string())
                    {
                        if let (Some(name), Some(content)) = (
                            child_tag.attributes().get("name").flatten(),
                            child_tag.attributes().get("content").flatten(),
                        ) {
                            let name_str = name.as_utf8_str();
                            let content_str = content.as_utf8_str();
                            metadata.insert(format!("meta-{}", name_str), content_str.to_string());
                        }
                        // Also check for property attribute (Open Graph, etc.)
                        if let (Some(property), Some(content)) = (
                            child_tag.attributes().get("property").flatten(),
                            child_tag.attributes().get("content").flatten(),
                        ) {
                            let property_str = property.as_utf8_str();
                            let content_str = content.as_utf8_str();
                            metadata.insert(format!("meta-{}", property_str), content_str.to_string());
                        }
                    }
                    // Look for title tag
                    if child_tag.name().as_utf8_str().eq_ignore_ascii_case("title")
                        && !options.strip_tags.contains(&"title".to_string())
                        && !options.preserve_tags.contains(&"title".to_string())
                    {
                        // Extract text content from title tag
                        let mut title_content = String::new();
                        let title_children = child_tag.children();
                        for title_child in title_children.top().iter() {
                            if let Some(tl::Node::Raw(raw)) = title_child.get(parser) {
                                title_content.push_str(raw.as_utf8_str().as_ref());
                            }
                        }
                        title_content = title_content.trim().to_string();
                        if !title_content.is_empty() {
                            metadata.insert("title".to_string(), title_content);
                        }
                    }
                    // Look for link tags with rel attribute (e.g., canonical)
                    if child_tag.name().as_utf8_str().eq_ignore_ascii_case("link") {
                        if let Some(rel_attr) = child_tag.attributes().get("rel").flatten() {
                            let rel_str = rel_attr.as_utf8_str();
                            // Check for canonical link
                            if rel_str.contains("canonical") {
                                if let Some(href_attr) = child_tag.attributes().get("href").flatten() {
                                    let href_str = href_attr.as_utf8_str();
                                    metadata.insert("canonical".to_string(), href_str.to_string());
                                }
                            }
                        }
                    }
                    // Look for base tag with href attribute
                    if child_tag.name().as_utf8_str().eq_ignore_ascii_case("base") {
                        if let Some(href_attr) = child_tag.attributes().get("href").flatten() {
                            let href_str = href_attr.as_utf8_str();
                            // Store as "base" which will be mapped to base_href in extract_document_metadata
                            metadata.insert("base".to_string(), href_str.to_string());
                        }
                    }
                }
            }
        } else {
            // If this is not a head tag, recursively search children for head tag
            let children = tag.children();
            for child_handle in children.top().iter() {
                let child_metadata = extract_head_metadata(child_handle, parser, options);
                if !child_metadata.is_empty() {
                    metadata.extend(child_metadata);
                    break; // Only process first head tag found
                }
            }
        }
    }

    metadata
}

/// Check if text has more than one character.
pub fn has_more_than_one_char(text: &str) -> bool {
    let mut chars = text.chars();
    chars.next().is_some() && chars.next().is_some()
}

/// Check if an element is inline (not block-level).
pub fn is_inline_element(tag_name: &str) -> bool {
    matches!(
        tag_name,
        "a" | "abbr"
            | "b"
            | "bdi"
            | "bdo"
            | "br"
            | "cite"
            | "code"
            | "data"
            | "dfn"
            | "em"
            | "i"
            | "kbd"
            | "mark"
            | "q"
            | "rp"
            | "rt"
            | "ruby"
            | "s"
            | "samp"
            | "small"
            | "span"
            | "strong"
            | "sub"
            | "sup"
            | "time"
            | "u"
            | "var"
            | "wbr"
            | "del"
            | "ins"
            | "img"
            | "map"
            | "area"
            | "audio"
            | "video"
            | "picture"
            | "source"
            | "track"
            | "embed"
            | "object"
            | "param"
            | "input"
            | "label"
            | "button"
            | "select"
            | "textarea"
            | "output"
            | "progress"
            | "meter"
    )
}

/// Handle hOCR document conversion, returning true if handled, false if not hOCR.
pub fn handle_hocr_document(
    dom: &tl::VDom<'_>,
    parser: &tl::Parser<'_>,
    options: &ConversionOptions,
    output: &mut String,
) -> bool {
    use crate::converter::utility::attributes::{is_hocr_document, may_be_hocr};
    use crate::hocr::{convert_to_markdown_with_options as convert_hocr_to_markdown, extract_hocr_document};

    let preprocessed = dom.outer_html();
    if !may_be_hocr(preprocessed.as_ref()) {
        return false;
    }

    let mut is_hocr = false;
    for child_handle in dom.children() {
        if is_hocr_document(*child_handle, parser) {
            is_hocr = true;
            break;
        }
    }

    if !is_hocr {
        return false;
    }

    let (elements, metadata) = extract_hocr_document(dom);

    if options.extract_metadata && !options.convert_as_inline {
        let mut metadata_map = BTreeMap::new();
        if let Some(system) = metadata.ocr_system {
            metadata_map.insert("ocr-system".to_string(), system);
        }
        if !metadata.ocr_capabilities.is_empty() {
            metadata_map.insert("ocr-capabilities".to_string(), metadata.ocr_capabilities.join(", "));
        }
        if let Some(pages) = metadata.ocr_number_of_pages {
            metadata_map.insert("ocr-number-of-pages".to_string(), pages.to_string());
        }
        if !metadata.ocr_langs.is_empty() {
            metadata_map.insert("ocr-langs".to_string(), metadata.ocr_langs.join(", "));
        }
        if !metadata.ocr_scripts.is_empty() {
            metadata_map.insert("ocr-scripts".to_string(), metadata.ocr_scripts.join(", "));
        }

        if !metadata_map.is_empty() {
            output.push_str(&format_metadata_frontmatter(&metadata_map));
        }
    }

    let mut markdown = convert_hocr_to_markdown(&elements, true, options.hocr_spatial_tables);

    if !markdown.trim().is_empty() {
        markdown.truncate(markdown.trim_end().len());
        output.push_str(&markdown);
        output.push('\n');
    }

    true
}
