#![allow(clippy::cast_precision_loss, clippy::cast_sign_loss, clippy::unused_self)]
//! Word extraction and DOM processing for hOCR documents

use crate::hocr::spatial::coords::{HocrWord, parse_bbox, parse_confidence};

/// Extract text content from a node
#[allow(clippy::trivially_copy_pass_by_ref)]
fn get_text_content(node_handle: &tl::NodeHandle, parser: &tl::Parser) -> String {
    let mut text = String::new();

    if let Some(node) = node_handle.get(parser) {
        match node {
            tl::Node::Raw(bytes) => {
                text.push_str(&bytes.as_utf8_str());
            }
            tl::Node::Tag(tag) => {
                let children = tag.children();
                for child_handle in children.top().iter() {
                    text.push_str(&get_text_content(child_handle, parser));
                }
            }
            tl::Node::Comment(_) => {}
        }
    }

    text
}

/// Extract hOCR words from a DOM tree
///
/// Walks the DOM and extracts all elements with `ocrx_word` class,
/// parsing their bbox and confidence information.
#[must_use]
#[allow(clippy::trivially_copy_pass_by_ref)]
pub fn extract_hocr_words(node_handle: &tl::NodeHandle, parser: &tl::Parser, min_confidence: f64) -> Vec<HocrWord> {
    let mut words = Vec::new();

    if let Some(tl::Node::Tag(tag)) = node_handle.get(parser) {
        let tag_name = tag.name().as_utf8_str();
        let attrs = tag.attributes();

        let class_attr = attrs.get("class").flatten().map(|v| v.as_utf8_str().to_string());

        // hOCR class validation removed for performance

        if tag_name == "span" {
            let is_word = class_attr.as_ref().is_some_and(|c| c.contains("ocrx_word"));
            let title = attrs.get("title").flatten().map(|v| v.as_utf8_str());

            if is_word {
                let title_str = title.as_deref().unwrap_or("");
                if let Some((left, top, width, height)) = parse_bbox(title_str) {
                    let confidence = parse_confidence(title_str);

                    if confidence >= min_confidence {
                        let text = get_text_content(node_handle, parser).trim().to_string();

                        if !text.is_empty() {
                            words.push(HocrWord {
                                text,
                                left,
                                top,
                                width,
                                height,
                                confidence,
                            });
                        }
                    }
                }
            }
        }

        let children = tag.children();
        for child_handle in children.top().iter() {
            words.extend(extract_hocr_words(child_handle, parser, min_confidence));
        }
    }

    words
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_hocr_words() {
        let hocr = r#"
            <div class="ocr_page">
                <span class="ocrx_word" title="bbox 100 50 150 80; x_wconf 95">Hello</span>
                <span class="ocrx_word" title="bbox 160 50 210 80; x_wconf 92">World</span>
            </div>
        "#;

        let dom = tl::parse(hocr, tl::ParserOptions::default()).unwrap();
        let parser = dom.parser();

        let mut words = Vec::new();
        for child_handle in dom.children().iter() {
            words.extend(extract_hocr_words(child_handle, parser, 0.0));
        }

        assert_eq!(words.len(), 2);
        assert_eq!(words[0].text, "Hello");
        assert_eq!(words[0].left, 100);
        assert_eq!(words[0].confidence, 95.0);

        assert_eq!(words[1].text, "World");
        assert_eq!(words[1].left, 160);
        assert_eq!(words[1].confidence, 92.0);
    }

    #[test]
    fn test_extract_hocr_words_confidence_filter() {
        let hocr = r#"
            <div class="ocr_page">
                <span class="ocrx_word" title="bbox 100 50 150 80; x_wconf 95">HighConf</span>
                <span class="ocrx_word" title="bbox 160 50 210 80; x_wconf 50">LowConf</span>
                <span class="ocrx_word" title="bbox 220 50 270 80; x_wconf 98">VeryHigh</span>
            </div>
        "#;

        let dom = tl::parse(hocr, tl::ParserOptions::default()).unwrap();
        let parser = dom.parser();

        let mut words = Vec::new();
        for child_handle in dom.children().iter() {
            words.extend(extract_hocr_words(child_handle, parser, 90.0));
        }

        assert_eq!(words.len(), 2);
        assert_eq!(words[0].text, "HighConf");
        assert_eq!(words[1].text, "VeryHigh");
    }

    #[test]
    fn test_end_to_end_hocr_table_extraction() {
        let hocr = r#"
            <div class="ocr_page">
                <span class="ocrx_word" title="bbox 100 50 140 70; x_wconf 95">Product</span>
                <span class="ocrx_word" title="bbox 200 50 240 70; x_wconf 95">Price</span>
                <span class="ocrx_word" title="bbox 100 100 140 120; x_wconf 95">Apple</span>
                <span class="ocrx_word" title="bbox 200 100 240 120; x_wconf 95">$1.50</span>
                <span class="ocrx_word" title="bbox 100 150 140 170; x_wconf 95">Orange</span>
                <span class="ocrx_word" title="bbox 200 150 240 170; x_wconf 95">$2.00</span>
            </div>
        "#;

        let dom = tl::parse(hocr, tl::ParserOptions::default()).unwrap();
        let parser = dom.parser();

        let mut words = Vec::new();
        for child_handle in dom.children().iter() {
            words.extend(extract_hocr_words(child_handle, parser, 0.0));
        }

        assert_eq!(words.len(), 6);
        assert_eq!(words[0].text, "Product");
        assert_eq!(words[1].text, "Price");
        assert_eq!(words[2].text, "Apple");
        assert_eq!(words[3].text, "$1.50");
        assert_eq!(words[4].text, "Orange");
        assert_eq!(words[5].text, "$2.00");
    }
}
