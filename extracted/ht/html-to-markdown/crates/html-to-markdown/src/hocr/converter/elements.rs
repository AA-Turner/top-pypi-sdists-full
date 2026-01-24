#![allow(clippy::branches_sharing_code)]
//! Element-specific conversion logic for hOCR to Markdown

use super::hierarchy::{
    append_text_and_children, collect_code_block, detect_heading_paragraph, ensure_heading_prefix,
    find_previous_heading,
};
use super::layout::{is_bullet_paragraph, try_spatial_table_reconstruction};
use super::output::{ConvertContext, element_text_content, ensure_trailing_blank_line};
use crate::hocr::types::{HocrElement, HocrElementType};

pub fn convert_element(
    element: &HocrElement,
    output: &mut String,
    depth: usize,
    preserve_structure: bool,
    enable_spatial_tables: bool,
    ctx: &mut ConvertContext,
) {
    match element.element_type {
        HocrElementType::OcrTitle | HocrElementType::OcrChapter | HocrElementType::OcrPart => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("# ");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("\n\n");
        }
        HocrElementType::OcrSection => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("## ");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("\n\n");
        }
        HocrElementType::OcrSubsection => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("### ");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("\n\n");
        }
        HocrElementType::OcrSubsubsection => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("#### ");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("\n\n");
        }

        HocrElementType::OcrPar => {
            let text_snapshot = element_text_content(element);
            let bullet_paragraph = is_bullet_paragraph(element, &text_snapshot);
            if !output.is_empty() {
                if bullet_paragraph {
                    if !output.ends_with('\n') {
                        output.push('\n');
                    }
                } else if !output.ends_with("\n\n") {
                    output.push_str("\n\n");
                }
            }

            if let Some(heading) = detect_heading_paragraph(element, &text_snapshot) {
                if !output.is_empty() && !output.ends_with("\n\n") {
                    if output.ends_with('\n') {
                        output.push('\n');
                    } else {
                        output.push_str("\n\n");
                    }
                }
                output.push_str("# ");
                output.push_str(&heading);
                output.push_str("\n\n");
                ctx.last_heading = Some(heading);
                return;
            }

            if enable_spatial_tables {
                if let Some(table_markdown) = try_spatial_table_reconstruction(element) {
                    output.push_str(&table_markdown);
                    ensure_trailing_blank_line(output);
                    return;
                }
            }

            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            if bullet_paragraph {
                if !output.ends_with('\n') {
                    output.push('\n');
                }
            } else {
                output.push_str("\n\n");
            }
        }

        HocrElementType::OcrBlockquote => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            let mut quote_content = String::new();
            append_text_and_children(
                element,
                &mut quote_content,
                depth,
                preserve_structure,
                enable_spatial_tables,
                ctx,
            );
            for line in quote_content.trim().lines() {
                output.push_str("> ");
                output.push_str(line);
                output.push('\n');
            }
            output.push('\n');
        }

        HocrElementType::OcrLine | HocrElementType::OcrxLine => {
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if !output.ends_with(' ') && !output.ends_with('\n') {
                output.push(' ');
            }
        }

        HocrElementType::OcrxWord => {
            if !output.is_empty()
                && !output.ends_with(' ')
                && !output.ends_with('\t')
                && !output.ends_with('\n')
                && !output.ends_with('*')
                && !output.ends_with('`')
                && !output.ends_with('_')
                && !output.ends_with('[')
            {
                output.push(' ');
            }

            if !element.text.is_empty() {
                output.push_str(&element.text);
            }
        }

        HocrElementType::OcrHeader | HocrElementType::OcrFooter => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push('*');
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("*\n\n");
        }

        HocrElementType::OcrCaption => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push('*');
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("*\n\n");
        }

        HocrElementType::OcrPageno => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("---\n");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            output.push_str("\n---\n\n");
        }

        HocrElementType::OcrAbstract => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("**Abstract**\n\n");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("\n\n");
        }

        HocrElementType::OcrAuthor => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push('*');
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("*\n\n");
        }

        HocrElementType::OcrSeparator => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("---\n\n");
        }

        HocrElementType::OcrTable => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }

            if enable_spatial_tables {
                if let Some(table_markdown) = try_spatial_table_reconstruction(element) {
                    output.push_str(&table_markdown);
                    ensure_trailing_blank_line(output);
                } else {
                    let mut sorted_children: Vec<_> = element.children.iter().collect();
                    if preserve_structure {
                        sorted_children.sort_by_key(|e| e.properties.order.unwrap_or(u32::MAX));
                    }
                    for child in sorted_children {
                        convert_element(child, output, depth + 1, preserve_structure, enable_spatial_tables, ctx);
                    }
                    ensure_trailing_blank_line(output);
                }
            } else {
                let mut sorted_children: Vec<_> = element.children.iter().collect();
                if preserve_structure {
                    sorted_children.sort_by_key(|e| e.properties.order.unwrap_or(u32::MAX));
                }
                for child in sorted_children {
                    convert_element(child, output, depth + 1, preserve_structure, enable_spatial_tables, ctx);
                }
                ensure_trailing_blank_line(output);
            }
        }

        HocrElementType::OcrFloat | HocrElementType::OcrTextfloat | HocrElementType::OcrTextimage => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            let mut sorted_children: Vec<_> = element.children.iter().collect();
            if preserve_structure {
                sorted_children.sort_by_key(|e| e.properties.order.unwrap_or(u32::MAX));
            }
            for child in sorted_children {
                convert_element(child, output, depth + 1, preserve_structure, enable_spatial_tables, ctx);
            }
            ensure_trailing_blank_line(output);
        }

        HocrElementType::OcrImage | HocrElementType::OcrPhoto | HocrElementType::OcrLinedrawing => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            if let Some(ref image_path) = element.properties.image {
                output.push_str("![");
                append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
                if output.ends_with(' ') {
                    output.pop();
                }
                output.push_str("](");
                output.push_str(image_path);
                output.push_str(")\n\n");
            } else {
                output.push_str("![Image]\n\n");
            }
        }

        HocrElementType::OcrMath | HocrElementType::OcrChem => {
            output.push('`');
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push('`');
        }

        HocrElementType::OcrDisplay => {
            if !output.is_empty() && !output.ends_with("\n\n") {
                output.push_str("\n\n");
            }
            output.push_str("```\n");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("\n```\n\n");
        }

        HocrElementType::OcrDropcap => {
            output.push_str("**");
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
            if output.ends_with(' ') {
                output.pop();
            }
            output.push_str("**");
        }

        HocrElementType::OcrGlyph | HocrElementType::OcrGlyphs | HocrElementType::OcrCinfo => {
            append_text_and_children(element, output, depth, preserve_structure, enable_spatial_tables, ctx);
        }

        HocrElementType::OcrPage
        | HocrElementType::OcrCarea
        | HocrElementType::OcrDocument
        | HocrElementType::OcrLinear
        | HocrElementType::OcrxBlock
        | HocrElementType::OcrColumn
        | HocrElementType::OcrXycut => {
            let mut sorted_children: Vec<_> = element.children.iter().collect();
            if preserve_structure {
                sorted_children.sort_by_key(|e| e.properties.order.unwrap_or(u32::MAX));
            }

            let mut idx = 0;
            while idx < sorted_children.len() {
                let child = sorted_children[idx];
                if child.element_type == HocrElementType::OcrPar {
                    if let Some((code_lines, consumed, language)) = collect_code_block(&sorted_children[idx..]) {
                        if let Some(heading_text) =
                            find_previous_heading(&sorted_children, idx).or_else(|| ctx.last_heading.clone())
                        {
                            ensure_heading_prefix(output, &heading_text);
                        }
                        emit_code_block(output, &code_lines, language);
                        idx += consumed;
                        continue;
                    }
                }

                convert_element(child, output, depth + 1, preserve_structure, enable_spatial_tables, ctx);
                idx += 1;
            }
        }

        HocrElementType::OcrNoise => {}
    }
}

pub fn emit_code_block(output: &mut String, lines: &[String], language: Option<&str>) {
    if !output.is_empty() {
        if output.ends_with('\n') {
            if !output.ends_with("\n\n") {
                output.push('\n');
            }
        } else {
            output.push_str("\n\n");
        }
    }

    output.push_str("```");
    if let Some(lang) = language {
        output.push_str(lang);
    }
    output.push('\n');

    for line in lines {
        output.push_str(line);
        output.push('\n');
    }

    output.push_str("```\n\n");
}
