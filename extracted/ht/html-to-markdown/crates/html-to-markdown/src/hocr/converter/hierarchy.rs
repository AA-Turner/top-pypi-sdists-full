#![allow(clippy::cast_possible_truncation)]
//! Document hierarchy and code block detection for hOCR conversion

use super::code_analysis::{is_bullet_like, is_code_paragraph, is_confident_code_block};
use super::keywords::detect_code_language;
use super::output::{ConvertContext, collect_line_words, element_text_content};
use crate::hocr::types::{HocrElement, HocrElementType};

pub fn append_text_and_children(
    element: &HocrElement,
    output: &mut String,
    depth: usize,
    preserve_structure: bool,
    enable_spatial_tables: bool,
    ctx: &mut ConvertContext,
) {
    use super::elements::convert_element;

    if !element.text.is_empty() {
        output.push_str(&element.text);
        if !element.children.is_empty() {
            output.push(' ');
        }
    }

    if preserve_structure && should_sort_children(&element.children) {
        let mut sorted_children: Vec<&HocrElement> = element.children.iter().collect();
        sorted_children.sort_by_key(|e| e.properties.order.unwrap_or(u32::MAX));
        for child in sorted_children {
            convert_element(child, output, depth + 1, preserve_structure, enable_spatial_tables, ctx);
        }
    } else {
        for child in &element.children {
            convert_element(child, output, depth + 1, preserve_structure, enable_spatial_tables, ctx);
        }
    }
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

pub fn detect_heading_paragraph(element: &HocrElement, text: &str) -> Option<String> {
    if element.element_type != HocrElementType::OcrPar {
        return None;
    }

    let line_count = element
        .children
        .iter()
        .filter(|child| matches!(child.element_type, HocrElementType::OcrLine | HocrElementType::OcrxLine))
        .count();

    if line_count != 1 {
        return None;
    }

    if text.is_empty() || text.len() > 60 || text.contains(':') || text.contains('\n') {
        return None;
    }

    let mut word_count = 0usize;
    let mut uppercase_initial = 0usize;
    for word in text.split_whitespace() {
        word_count += 1;
        if word.chars().next().is_some_and(char::is_uppercase) {
            uppercase_initial += 1;
        }
        if word_count > 8 {
            return None;
        }
    }

    if word_count < 2 {
        return None;
    }

    if uppercase_initial < word_count.saturating_sub(1) {
        return None;
    }

    if text.ends_with('.') {
        return None;
    }

    Some(text.to_string())
}

pub fn find_previous_heading(children: &[&HocrElement], idx: usize) -> Option<String> {
    if idx == 0 {
        return None;
    }

    for candidate in children[..idx].iter().rev() {
        let text_snapshot = element_text_content(candidate);
        if let Some(text) = detect_heading_paragraph(candidate, &text_snapshot) {
            return Some(text);
        }
    }

    None
}

pub fn ensure_heading_prefix(output: &mut String, heading: &str) {
    let snippet = format!("# {heading}\n\n");
    if output.ends_with(&snippet) {
        return;
    }

    if !output.is_empty() && !output.ends_with("\n\n") {
        if output.ends_with('\n') {
            output.push('\n');
        } else {
            output.push_str("\n\n");
        }
    }

    output.push_str(&snippet);
}

#[derive(Clone)]
pub struct CodeLineInfo {
    pub text: String,
    pub x1: u32,
}

pub fn collect_code_block(children: &[&HocrElement]) -> Option<(Vec<String>, usize, Option<&'static str>)> {
    let mut collected: Vec<CodeLineInfo> = Vec::new();
    let mut consumed = 0;
    let mut paragraph_count = 0;

    while consumed < children.len() {
        let child = children[consumed];
        if child.element_type != HocrElementType::OcrPar {
            break;
        }

        let lines = extract_code_lines(child);
        if lines.is_empty() || !is_code_paragraph(&lines) {
            break;
        }

        if paragraph_count > 0 && !collected.is_empty() && should_insert_code_paragraph_break(&collected, &lines) {
            let gap_x = lines
                .first()
                .map(|info| info.x1)
                .or_else(|| child.properties.bbox.map(|bbox| bbox.x1))
                .unwrap_or(0);
            collected.push(CodeLineInfo {
                text: String::new(),
                x1: gap_x,
            });
        }

        collected.extend(lines);
        consumed += 1;
        paragraph_count += 1;
    }

    if collected.is_empty() {
        return None;
    }

    if !is_confident_code_block(&collected) {
        return None;
    }

    let mut x_values: Vec<u32> = collected
        .iter()
        .filter(|info| !info.text.is_empty())
        .map(|info| info.x1)
        .collect();

    if x_values.is_empty() {
        x_values.push(0);
    }

    let min_x = *x_values.iter().min().unwrap_or(&0);
    let indent_candidates: Vec<u32> = x_values
        .iter()
        .filter_map(|&x| if x > min_x { Some(x - min_x) } else { None })
        .filter(|&delta| delta > 5)
        .collect();

    let mut indent_step = indent_candidates.iter().copied().min().unwrap_or(40);

    if indent_step == 0 {
        indent_step = 40;
    }

    let mut lines: Vec<String> = Vec::new();
    for info in collected {
        if info.text.is_empty() {
            if !lines.is_empty() && !lines.last().unwrap().is_empty() {
                lines.push(String::new());
            }
            continue;
        }

        let indent_level = if info.x1 <= min_x {
            0
        } else {
            let diff = info.x1 - min_x;
            (((diff as f32) / indent_step as f32) + 0.25).floor() as usize
        }
        .min(6);

        let mut normalized = normalize_code_line(&info.text);
        if indent_level > 0 {
            let indent = "  ".repeat(indent_level);
            normalized = format!("{indent}{normalized}");
        }
        lines.push(normalized);
    }

    while matches!(lines.last(), Some(last) if last.is_empty()) {
        lines.pop();
    }

    let meaningful_lines: Vec<&String> = lines.iter().filter(|line| !line.trim().is_empty()).collect();
    let meaningful_count = meaningful_lines.len();
    if meaningful_count < 3 {
        return None;
    }

    let bullet_like = meaningful_lines.iter().filter(|line| is_bullet_like(line)).count();
    if bullet_like * 2 >= meaningful_count {
        return None;
    }

    let language = detect_code_language(&lines);
    Some((lines, consumed, language))
}

fn extract_code_lines(paragraph: &HocrElement) -> Vec<CodeLineInfo> {
    let mut lines = Vec::new();

    for child in &paragraph.children {
        match child.element_type {
            HocrElementType::OcrLine | HocrElementType::OcrxLine => {
                let mut words = Vec::new();
                collect_line_words(child, &mut words);
                if words.is_empty() {
                    continue;
                }
                let text = words.join(" ");
                if text.trim().is_empty() {
                    continue;
                }
                let x1 = child
                    .properties
                    .bbox
                    .map(|bbox| bbox.x1)
                    .or_else(|| paragraph.properties.bbox.map(|bbox| bbox.x1))
                    .unwrap_or(0);
                lines.push(CodeLineInfo {
                    text: text.trim().to_string(),
                    x1,
                });
            }
            _ => {}
        }
    }

    if lines.is_empty() {
        let mut words = Vec::new();
        collect_line_words(paragraph, &mut words);
        if !words.is_empty() {
            let x1 = paragraph.properties.bbox.map_or(0, |bbox| bbox.x1);
            lines.push(CodeLineInfo {
                text: words.join(" ").trim().to_string(),
                x1,
            });
        }
    }

    lines
}

fn should_insert_code_paragraph_break(previous: &[CodeLineInfo], next: &[CodeLineInfo]) -> bool {
    let prev_line = previous.iter().rev().find(|info| !info.text.trim().is_empty());
    let next_line = next.iter().find(|info| !info.text.trim().is_empty());

    match (prev_line, next_line) {
        (Some(prev), Some(next)) => {
            let prev_text = prev.text.trim();
            let next_text = next.text.trim();

            if next_text == "}" {
                return false;
            }

            if prev_text.ends_with('{') && next_text == "}" {
                return false;
            }

            true
        }
        _ => false,
    }
}

fn normalize_code_line(text: &str) -> String {
    let mut normalized = text.trim().to_string();
    let replacements = [("\u{2014}", "-"), ("\u{2013}", "-"), ("\u{2212}", "-")];
    for (from, to) in replacements {
        normalized = normalized.replace(from, to);
    }

    normalized = normalized.replace('+', " + ");

    let mut collapsed = String::new();
    let mut last_space = false;
    for ch in normalized.chars() {
        if ch.is_whitespace() {
            if !last_space {
                collapsed.push(' ');
                last_space = true;
            }
        } else {
            collapsed.push(ch);
            last_space = false;
        }
    }
    let mut cleaned = collapsed.trim().to_string();
    let punctuation_fixes = [(" ,", ","), (" ;", ";"), (" )", ")"), ("( ", "(")];
    for (from, to) in punctuation_fixes {
        cleaned = cleaned.replace(from, to);
    }
    let mut final_line = String::new();
    for ch in cleaned.chars() {
        match ch {
            '{' => {
                if !final_line.ends_with(' ') && !final_line.is_empty() {
                    final_line.push(' ');
                }
                final_line.push('{');
            }
            '}' | ';' => {
                if final_line.ends_with(' ') {
                    final_line.pop();
                }
                final_line.push(ch);
            }
            _ => final_line.push(ch),
        }
    }
    while final_line.contains("  ") {
        final_line = final_line.replace("  ", " ");
    }
    final_line.trim().to_string()
}
