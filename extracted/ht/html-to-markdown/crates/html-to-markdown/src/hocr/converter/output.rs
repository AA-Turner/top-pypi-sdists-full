//! Output formatting utilities for hOCR to Markdown conversion

use crate::hocr::types::{HocrElement, HocrElementType};

#[derive(Default)]
pub struct ConvertContext {
    pub last_heading: Option<String>,
}

pub fn ensure_trailing_blank_line(output: &mut String) {
    while output.ends_with("\n\n\n") {
        output.pop();
    }
    if output.ends_with("\n\n") {
        return;
    }
    if output.ends_with('\n') {
        output.push('\n');
    } else {
        output.push_str("\n\n");
    }
}

pub fn collapse_extra_newlines(output: &mut String) {
    let mut collapsed = String::with_capacity(output.len());
    let mut newline_count = 0;

    for ch in output.chars() {
        if ch == '\n' {
            newline_count += 1;
            if newline_count <= 2 {
                collapsed.push('\n');
            }
        } else {
            newline_count = 0;
            collapsed.push(ch);
        }
    }

    if collapsed.len() != output.len() {
        *output = collapsed;
    }
}

pub fn element_text_content(element: &HocrElement) -> String {
    let mut output = String::new();
    collect_text_tokens(element, &mut output);
    output
}

fn collect_text_tokens(element: &HocrElement, output: &mut String) {
    if element.element_type == HocrElementType::OcrxWord {
        let trimmed = element.text.trim();
        if !trimmed.is_empty() {
            if !output.is_empty() {
                output.push(' ');
            }
            output.push_str(trimmed);
        }
    }

    for child in &element.children {
        collect_text_tokens(child, output);
    }
}

pub fn collect_line_words(element: &HocrElement, words: &mut Vec<String>) {
    if element.element_type == HocrElementType::OcrxWord {
        let trimmed = element.text.trim();
        if !trimmed.is_empty() {
            words.push(trimmed.to_string());
        }
    }

    for child in &element.children {
        collect_line_words(child, words);
    }
}
