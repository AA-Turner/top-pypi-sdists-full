#![allow(clippy::cast_precision_loss, clippy::cast_sign_loss, clippy::unused_self)]
//! Layout analysis and table reconstruction

use crate::hocr::spatial::coords::HocrWord;

/// Detect column positions from word positions
///
/// Groups words by their x-position and returns the median x-position
/// for each detected column.
///
/// Optimized with O(n log n) complexity using sorted insertion.
#[must_use]
pub fn detect_columns(words: &[HocrWord], column_threshold: u32) -> Vec<u32> {
    if words.is_empty() {
        return Vec::new();
    }

    let mut x_positions: Vec<u32> = words.iter().map(|w| w.left).collect();
    x_positions.sort_unstable();

    let mut position_groups: Vec<Vec<u32>> = Vec::new();
    let mut current_group = vec![x_positions[0]];

    for &x_pos in &x_positions[1..] {
        let matches_group = current_group.iter().any(|&pos| x_pos.abs_diff(pos) <= column_threshold);

        if matches_group {
            current_group.push(x_pos);
        } else {
            position_groups.push(std::mem::replace(&mut current_group, vec![x_pos]));
        }
    }

    if !current_group.is_empty() {
        position_groups.push(current_group);
    }

    let mut columns: Vec<u32> = position_groups
        .iter()
        .map(|group| {
            let mid = group.len() / 2;
            group[mid]
        })
        .collect();

    columns.sort_unstable();
    columns
}

/// Detect row positions from word positions
///
/// Groups words by their vertical center position and returns the median
/// y-position for each detected row.
///
/// Optimized with O(n log n) complexity using sorted insertion.
#[must_use]
#[allow(clippy::cast_possible_truncation)]
pub fn detect_rows(words: &[HocrWord], row_threshold_ratio: f64) -> Vec<u32> {
    if words.is_empty() {
        return Vec::new();
    }

    let mut heights: Vec<u32> = words.iter().map(|w| w.height).collect();
    heights.sort_unstable();
    let median_height = heights[heights.len() / 2];
    let row_threshold = f64::from(median_height) * row_threshold_ratio;

    let mut y_centers: Vec<f64> = words.iter().map(HocrWord::y_center).collect();
    y_centers.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));

    let mut position_groups: Vec<Vec<f64>> = Vec::new();
    let mut current_group = vec![y_centers[0]];

    for &y_center in &y_centers[1..] {
        let matches_group = current_group.iter().any(|&pos| (y_center - pos).abs() <= row_threshold);

        if matches_group {
            current_group.push(y_center);
        } else {
            position_groups.push(std::mem::replace(&mut current_group, vec![y_center]));
        }
    }

    if !current_group.is_empty() {
        position_groups.push(current_group);
    }

    let mut rows: Vec<u32> = position_groups
        .iter()
        .map(|group| {
            let mid = group.len() / 2;
            group[mid] as u32
        })
        .collect();

    rows.sort_unstable();
    rows
}

/// Remove empty rows and columns from table
fn remove_empty_rows_and_columns(table: Vec<Vec<String>>) -> Vec<Vec<String>> {
    if table.is_empty() {
        return table;
    }

    let num_cols = table[0].len();
    let mut non_empty_cols: Vec<bool> = vec![false; num_cols];

    for row in &table {
        for (col_idx, cell) in row.iter().enumerate() {
            if !cell.trim().is_empty() {
                non_empty_cols[col_idx] = true;
            }
        }
    }

    table
        .into_iter()
        .filter(|row| row.iter().any(|cell| !cell.trim().is_empty()))
        .map(|row| {
            row.into_iter()
                .enumerate()
                .filter(|(idx, _)| non_empty_cols[*idx])
                .map(|(_, cell)| cell)
                .collect()
        })
        .collect()
}

/// Find which row a word belongs to based on its y-center
#[allow(clippy::cast_possible_truncation)]
fn find_row_index(row_positions: &[u32], word: &HocrWord) -> Option<usize> {
    let y_center = word.y_center() as u32;

    row_positions
        .iter()
        .enumerate()
        .min_by_key(|&(_, row_y)| row_y.abs_diff(y_center))
        .map(|(idx, _)| idx)
}

/// Find which column a word belongs to based on its x-position
fn find_column_index(col_positions: &[u32], word: &HocrWord) -> Option<usize> {
    let x_pos = word.left;

    col_positions
        .iter()
        .enumerate()
        .min_by_key(|&(_, col_x)| col_x.abs_diff(x_pos))
        .map(|(idx, _)| idx)
}

/// Reconstruct table structure from words
///
/// Takes detected words and reconstructs a 2D table by:
/// 1. Detecting column and row positions
/// 2. Assigning words to cells based on position
/// 3. Combining words within the same cell
#[must_use]
pub fn reconstruct_table(words: &[HocrWord], column_threshold: u32, row_threshold_ratio: f64) -> Vec<Vec<String>> {
    if words.is_empty() {
        return Vec::new();
    }

    let col_positions = detect_columns(words, column_threshold);
    let row_positions = detect_rows(words, row_threshold_ratio);

    if col_positions.is_empty() || row_positions.is_empty() {
        return Vec::new();
    }

    let num_rows = row_positions.len();
    let num_cols = col_positions.len();
    let mut table: Vec<Vec<Vec<String>>> = vec![vec![vec![]; num_cols]; num_rows];

    for word in words {
        if let (Some(r), Some(c)) = (
            find_row_index(&row_positions, word),
            find_column_index(&col_positions, word),
        ) {
            if r < num_rows && c < num_cols {
                table[r][c].push(word.text.clone());
            }
        }
    }

    let result: Vec<Vec<String>> = table
        .into_iter()
        .map(|row| {
            row.into_iter()
                .map(|cell_words| {
                    if cell_words.is_empty() {
                        String::new()
                    } else {
                        cell_words.join(" ")
                    }
                })
                .collect()
        })
        .collect();

    remove_empty_rows_and_columns(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_detect_columns() {
        let words = vec![
            HocrWord {
                text: "A".to_string(),
                left: 100,
                top: 50,
                width: 20,
                height: 30,
                confidence: 95.0,
            },
            HocrWord {
                text: "B".to_string(),
                left: 200,
                top: 50,
                width: 20,
                height: 30,
                confidence: 95.0,
            },
            HocrWord {
                text: "C".to_string(),
                left: 105,
                top: 100,
                width: 20,
                height: 30,
                confidence: 95.0,
            },
        ];

        let columns = detect_columns(&words, 50);
        assert_eq!(columns.len(), 2);
        assert!(columns.contains(&100) || columns.contains(&105));
        assert!(columns.contains(&200));
    }

    #[test]
    fn test_reconstruct_simple_table() {
        let words = vec![
            HocrWord {
                text: "Name".to_string(),
                left: 100,
                top: 50,
                width: 50,
                height: 20,
                confidence: 95.0,
            },
            HocrWord {
                text: "Age".to_string(),
                left: 200,
                top: 50,
                width: 50,
                height: 20,
                confidence: 95.0,
            },
            HocrWord {
                text: "Alice".to_string(),
                left: 100,
                top: 100,
                width: 50,
                height: 20,
                confidence: 95.0,
            },
            HocrWord {
                text: "30".to_string(),
                left: 200,
                top: 100,
                width: 50,
                height: 20,
                confidence: 95.0,
            },
        ];

        let table = reconstruct_table(&words, 50, 0.5);

        assert_eq!(table.len(), 2);
        assert_eq!(table[0].len(), 2);
        assert_eq!(table[0][0], "Name");
        assert_eq!(table[0][1], "Age");
        assert_eq!(table[1][0], "Alice");
        assert_eq!(table[1][1], "30");
    }

    #[test]
    fn test_reconstruct_table_with_multi_word_cells() {
        let words = vec![
            HocrWord {
                text: "First".to_string(),
                left: 100,
                top: 50,
                width: 30,
                height: 20,
                confidence: 95.0,
            },
            HocrWord {
                text: "Name".to_string(),
                left: 135,
                top: 50,
                width: 30,
                height: 20,
                confidence: 95.0,
            },
            HocrWord {
                text: "Last".to_string(),
                left: 200,
                top: 50,
                width: 30,
                height: 20,
                confidence: 95.0,
            },
            HocrWord {
                text: "Name".to_string(),
                left: 235,
                top: 50,
                width: 30,
                height: 20,
                confidence: 95.0,
            },
        ];

        let table = reconstruct_table(&words, 50, 0.5);

        assert_eq!(table.len(), 1);
        assert_eq!(table[0].len(), 2);
        assert_eq!(table[0][0], "First Name");
        assert_eq!(table[0][1], "Last Name");
    }
}
