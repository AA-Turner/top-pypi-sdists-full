//! Core conversion logic for hOCR to Markdown

use super::elements::convert_element;
use super::output::{ConvertContext, collapse_extra_newlines};
use crate::hocr::types::HocrElement;

/// Convert hOCR elements to Markdown with semantic formatting
///
/// Transforms hOCR document structure into clean, readable Markdown while preserving
/// document hierarchy and semantic meaning.
///
/// # Arguments
///
/// * `elements` - hOCR elements to convert (typically from `extract_hocr_document`)
/// * `preserve_structure` - If `true`, sorts elements by their `order` property to respect reading order
///
/// # Returns
///
/// A `String` containing the formatted Markdown output
///
/// # Semantic Conversion
///
/// All 40 hOCR 1.2 element types are converted with appropriate markdown formatting:
///
/// | hOCR Element | Markdown Output |
/// |--------------|-----------------|
/// | `ocr_title`, `ocr_chapter` | `# Heading` |
/// | `ocr_section` | `## Heading` |
/// | `ocr_subsection` | `### Heading` |
/// | `ocr_par` | Paragraph with blank lines |
/// | `ocr_blockquote` | `> Quote` |
/// | `ocr_abstract` | `**Abstract**` header |
/// | `ocr_author` | `*Author*` (italic) |
/// | `ocr_image`, `ocr_photo` | `![alt](path)` |
/// | `ocr_math`, `ocr_chem` | `` `formula` `` (inline code) |
/// | `ocr_display` | ` ```equation``` ` (code block) |
/// | `ocr_separator` | `---` (horizontal rule) |
/// | `ocr_dropcap` | `**Letter**` (bold) |
/// | `ocrx_word` | Word with markdown escaping |
///
/// # Example
///
/// ```rust
/// use html_to_markdown_rs::hocr::{extract_hocr_document, convert_to_markdown};
///
/// let html = r#"<div class="ocr_page">
///     <h1 class="ocr_title">Document Title</h1>
///     <p class="ocr_par" title="order 1">
///         <span class="ocrx_word" title="bbox 10 10 50 30; x_wconf 95">Hello</span>
///         <span class="ocrx_word" title="bbox 60 10 100 30; x_wconf 92">World</span>
///     </p>
/// </div>"#;
///
/// let dom = tl::parse(html, tl::ParserOptions::default()).unwrap();
/// let (elements, _) = extract_hocr_document(&dom);
/// let markdown = convert_to_markdown(&elements, true);
/// // Output: "# Document Title\n\nHello World"
/// ```
#[must_use]
pub fn convert_to_markdown(elements: &[HocrElement], preserve_structure: bool) -> String {
    convert_to_markdown_with_options(elements, preserve_structure, true)
}

/// Convert hOCR elements to Markdown with advanced options.
///
/// Transforms hOCR document structure into clean, readable Markdown with fine-grained
/// control over structure preservation and spatial table reconstruction behavior.
///
/// # Arguments
///
/// * `elements` - hOCR elements to convert (typically from `extract_hocr_document`)
/// * `preserve_structure` - If `true`, sorts elements by their `order` property to respect reading order.
///   If `false`, elements are processed in their original tree order.
/// * `enable_spatial_tables` - If `true`, attempts to reconstruct table structure from spatial
///   positioning of words. If `false`, word positions are ignored and only text content is used.
///
/// # Returns
///
/// A `String` containing the formatted Markdown output
///
/// # Performance
///
/// - Spatial table reconstruction is more computationally expensive but produces better table formatting
/// - For documents without tables, setting `enable_spatial_tables` to `false` improves performance
/// - Structure preservation requires sorting which adds O(n log n) complexity; disable if not needed
#[must_use]
pub fn convert_to_markdown_with_options(
    elements: &[HocrElement],
    preserve_structure: bool,
    enable_spatial_tables: bool,
) -> String {
    let mut output = String::new();
    let mut ctx = ConvertContext::default();

    if preserve_structure && should_sort_children(elements) {
        let mut sorted_elements: Vec<&HocrElement> = elements.iter().collect();
        sorted_elements.sort_by_key(|e| e.properties.order.unwrap_or(u32::MAX));
        for element in sorted_elements {
            convert_element(
                element,
                &mut output,
                0,
                preserve_structure,
                enable_spatial_tables,
                &mut ctx,
            );
        }
    } else {
        for element in elements {
            convert_element(
                element,
                &mut output,
                0,
                preserve_structure,
                enable_spatial_tables,
                &mut ctx,
            );
        }
    }

    collapse_extra_newlines(&mut output);
    output.trim().to_string()
}

fn should_sort_children(children: &[HocrElement]) -> bool {
    let mut last = 0u32;
    let mut saw_any = false;

    for child in children {
        let order = child.properties.order.unwrap_or(u32::MAX);
        if saw_any && order < last {
            return true;
        }
        last = order;
        saw_any = true;
    }

    false
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::hocr::types::{BBox, HocrElement, HocrElementType, HocrProperties};

    #[test]
    fn test_convert_title() {
        let element = HocrElement {
            element_type: HocrElementType::OcrTitle,
            properties: HocrProperties::default(),
            text: "Document Title".to_string(),
            children: vec![],
        };

        let markdown = convert_to_markdown(&[element], true);
        assert_eq!(markdown, "# Document Title");
    }

    #[test]
    fn test_spatial_table_reconstruction_can_be_disabled() {
        fn word(text: &str, x1: u32, y1: u32) -> HocrElement {
            HocrElement {
                element_type: HocrElementType::OcrxWord,
                properties: HocrProperties {
                    bbox: Some(BBox {
                        x1,
                        y1,
                        x2: x1 + 40,
                        y2: y1 + 20,
                    }),
                    x_wconf: Some(95.0),
                    ..HocrProperties::default()
                },
                text: text.to_string(),
                children: vec![],
            }
        }

        let paragraph = HocrElement {
            element_type: HocrElementType::OcrPar,
            properties: HocrProperties::default(),
            text: String::new(),
            children: vec![
                word("A", 10, 10),
                word("B", 120, 10),
                word("C", 230, 10),
                word("D", 12, 60),
                word("E", 122, 60),
                word("F", 232, 60),
            ],
        };

        let markdown_with_tables = convert_to_markdown_with_options(std::slice::from_ref(&paragraph), true, true);
        assert!(
            markdown_with_tables.contains("| --- |"),
            "Expected spatial table reconstruction to produce a markdown table"
        );

        let markdown_without_tables = convert_to_markdown_with_options(std::slice::from_ref(&paragraph), true, false);
        assert!(
            !markdown_without_tables.contains('|'),
            "Table reconstruction should be disabled when the flag is false"
        );
        assert!(
            markdown_without_tables.contains("A B C"),
            "Plain text output should retain original word order"
        );
    }

    #[test]
    fn test_convert_paragraph_with_words() {
        let par = HocrElement {
            element_type: HocrElementType::OcrPar,
            properties: HocrProperties::default(),
            text: String::new(),
            children: vec![
                HocrElement {
                    element_type: HocrElementType::OcrxWord,
                    properties: HocrProperties::default(),
                    text: "Hello".to_string(),
                    children: vec![],
                },
                HocrElement {
                    element_type: HocrElementType::OcrxWord,
                    properties: HocrProperties::default(),
                    text: "World".to_string(),
                    children: vec![],
                },
            ],
        };

        let markdown = convert_to_markdown(&[par], true);
        assert!(markdown.contains("Hello"));
        assert!(markdown.contains("World"));
    }

    #[test]
    fn test_convert_blockquote() {
        let quote = HocrElement {
            element_type: HocrElementType::OcrBlockquote,
            properties: HocrProperties::default(),
            text: "This is a quote".to_string(),
            children: vec![],
        };

        let markdown = convert_to_markdown(&[quote], true);
        assert!(markdown.starts_with("> "));
    }
}
