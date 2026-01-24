//! Spatial layout analysis and table reconstruction for hOCR conversion

use crate::hocr::spatial::{self, HocrWord};
use crate::hocr::types::{HocrElement, HocrElementType};

pub fn is_bullet_paragraph(element: &HocrElement, text: &str) -> bool {
    if element.element_type != HocrElementType::OcrPar {
        return false;
    }

    let trimmed = text.trim_start();
    if trimmed.is_empty() {
        return false;
    }

    if matches!(trimmed.chars().next(), Some('•' | '●' | '-' | '+' | '*')) {
        return true;
    }

    let mut chars = trimmed.chars().peekable();
    let mut digit_count = 0;
    while let Some(&ch) = chars.peek() {
        if ch.is_ascii_digit() {
            digit_count += 1;
            chars.next();
        } else {
            break;
        }
    }

    if digit_count > 0 {
        if let Some(&ch) = chars.peek() {
            if (ch == '.' || ch == ')') && chars.clone().nth(1).is_some_and(char::is_whitespace) {
                return true;
            }
        }
    }

    false
}

/// Try to detect and reconstruct a table from an element's word children
///
/// Returns Some(markdown) if table structure detected, None otherwise
pub fn try_spatial_table_reconstruction(element: &HocrElement) -> Option<String> {
    let mut words = Vec::new();
    collect_words(element, &mut words);

    if words.len() < 6 {
        return None;
    }

    let table = spatial::reconstruct_table(&words, 50, 0.5);

    if table.is_empty() || table[0].is_empty() {
        return None;
    }

    if let Some(cleaned_table) = post_process_table(table) {
        let markdown = spatial::table_to_markdown(&cleaned_table);
        if !markdown.is_empty() {
            return Some(markdown);
        }
    }

    None
}

/// Collect all word elements recursively from an element tree
fn collect_words(element: &HocrElement, words: &mut Vec<HocrWord>) {
    if element.element_type == HocrElementType::OcrxWord {
        if let Some(bbox) = element.properties.bbox {
            let confidence = element.properties.x_wconf.unwrap_or(0.0);
            words.push(HocrWord {
                text: element.text.clone(),
                left: bbox.x1,
                top: bbox.y1,
                width: bbox.width(),
                height: bbox.height(),
                confidence,
            });
        }
    }

    for child in &element.children {
        collect_words(child, words);
    }
}

fn post_process_table(mut table: Vec<Vec<String>>) -> Option<Vec<Vec<String>>> {
    table.retain(|row| row.iter().any(|cell| !cell.trim().is_empty()));
    if table.is_empty() {
        return None;
    }

    let mut non_empty = 0;
    let mut long_cells = 0;
    for row in &table {
        for cell in row {
            let trimmed = cell.trim();
            if trimmed.is_empty() {
                continue;
            }
            non_empty += 1;
            if trimmed.chars().count() > 60 {
                long_cells += 1;
            }
        }
    }

    if non_empty > 0 && long_cells * 3 > non_empty * 2 {
        return None;
    }

    let data_start = table
        .iter()
        .enumerate()
        .find_map(|(idx, row)| {
            let digit_cells = row
                .iter()
                .filter(|cell| cell.chars().any(|c| c.is_ascii_digit()))
                .count();
            if digit_cells >= 3 { Some(idx) } else { None }
        })
        .unwrap_or(0);

    let mut header_rows = if data_start > 0 {
        table[..data_start].to_vec()
    } else {
        Vec::new()
    };
    let mut data_rows = table[data_start..].to_vec();

    if header_rows.len() > 2 {
        header_rows = header_rows[header_rows.len() - 2..].to_vec();
    }

    if header_rows.is_empty() {
        if data_rows.len() < 2 {
            return None;
        }
        header_rows.push(data_rows[0].clone());
        data_rows = data_rows[1..].to_vec();
    }

    let column_count = header_rows
        .first()
        .or_else(|| data_rows.first())
        .map_or(0, std::vec::Vec::len);

    if column_count == 0 {
        return None;
    }

    let mut header = vec![String::new(); column_count];
    for row in &header_rows {
        for (idx, cell) in row.iter().enumerate() {
            let trimmed = cell.trim();
            if trimmed.is_empty() {
                continue;
            }
            if !header[idx].is_empty() {
                header[idx].push(' ');
            }
            header[idx].push_str(trimmed);
        }
    }

    let mut processed = Vec::new();
    processed.push(header);
    processed.extend(data_rows);

    if processed.len() <= 1 {
        return None;
    }

    let mut col = 0;
    while col < processed[0].len() {
        let header_text = processed[0][col].trim().to_string();
        let data_empty = processed[1..]
            .iter()
            .all(|row| row.get(col).is_none_or(|cell| cell.trim().is_empty()));

        if data_empty {
            merge_header_only_column(&mut processed, col, header_text);
        } else {
            col += 1;
        }

        if processed.is_empty() || processed[0].is_empty() {
            return None;
        }
    }

    if processed[0].len() < 2 || processed.len() <= 1 {
        return None;
    }

    for cell in &mut processed[0] {
        normalize_header_cell(cell);
    }

    for row in processed.iter_mut().skip(1) {
        for cell in row.iter_mut() {
            normalize_data_cell(cell);
        }
    }

    Some(processed)
}

#[allow(clippy::trivially_copy_pass_by_ref)]
fn merge_header_only_column(table: &mut [Vec<String>], col: usize, header_text: String) {
    if table.is_empty() || table[0].is_empty() {
        return;
    }

    let trimmed = header_text.trim();
    if trimmed.is_empty() && table.len() > 1 {
        for row in table.iter_mut() {
            row.remove(col);
        }
        return;
    }

    if !trimmed.is_empty() {
        if col > 0 {
            let mut target = col - 1;
            while target > 0 && table[0][target].trim().is_empty() {
                target -= 1;
            }
            if !table[0][target].trim().is_empty() || target == 0 {
                if !table[0][target].is_empty() {
                    table[0][target].push(' ');
                }
                table[0][target].push_str(trimmed);
                for row in table.iter_mut() {
                    row.remove(col);
                }
                return;
            }
        }

        if col + 1 < table[0].len() {
            if table[0][col + 1].trim().is_empty() {
                table[0][col + 1] = trimmed.to_string();
            } else {
                let mut updated = trimmed.to_string();
                updated.push(' ');
                updated.push_str(table[0][col + 1].trim());
                table[0][col + 1] = updated;
            }
            for row in table.iter_mut() {
                row.remove(col);
            }
            return;
        }
    }

    for row in table.iter_mut() {
        row.remove(col);
    }
}

fn normalize_header_cell(cell: &mut String) {
    let mut text = cell.trim().replace("  ", " ");
    if text.contains("(Q)") {
        text = text.replace("(Q)", "(Ω)");
    }
    if text.contains("icorr") && text.contains("(A/cm)") && !text.contains("^2") {
        text = text.replace("(A/cm)", "(A/cm^2)");
    }
    if text.eq_ignore_ascii_case("be (V/dec)") {
        text = "bc (V/dec)".to_string();
    }
    if text.starts_with("Polarization resistance") {
        if text.contains("(Ω)") {
            text = text.replace("(Ω) rate", "(Ω)");
        } else {
            text.push_str(" (Ω)");
        }
    }
    if text.starts_with("Corrosion") && text.contains("mm/year") {
        text = "Corrosion rate (mm/year)".to_string();
    }
    *cell = text;
}

fn normalize_data_cell(cell: &mut String) {
    let mut text = cell.trim().to_string();
    if text.is_empty() {
        cell.clear();
        return;
    }

    for ch in ['\u{2014}', '\u{2013}', '\u{2212}'] {
        text = text.replace(ch, "-");
    }

    if text.starts_with("- ") {
        text = format!("-{}", text[2..].trim_start());
    }

    text = text.replace("- ", "-");
    text = text.replace(" -", "-");
    text = text.replace("E-", "e-").replace("E+", "e+");

    if text == "-" {
        text.clear();
    }

    *cell = text;
}
