#![allow(clippy::cast_precision_loss, clippy::cast_sign_loss, clippy::unused_self)]
//! Markdown table output formatting

/// Convert table to markdown format
#[must_use]
pub fn table_to_markdown(table: &[Vec<String>]) -> String {
    if table.is_empty() {
        return String::new();
    }

    let num_cols = table[0].len();
    if num_cols == 0 {
        return String::new();
    }

    let mut markdown = String::new();

    for (row_idx, row) in table.iter().enumerate() {
        markdown.push('|');
        for cell in row {
            markdown.push(' ');
            markdown.push_str(&cell.replace('|', "\\|"));
            markdown.push_str(" |");
        }
        markdown.push('\n');

        if row_idx == 0 {
            markdown.push('|');
            for _ in 0..num_cols {
                markdown.push_str(" --- |");
            }
            markdown.push('\n');
        }
    }

    markdown
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_table_to_markdown() {
        let table = vec![
            vec!["Header1".to_string(), "Header2".to_string()],
            vec!["Cell1".to_string(), "Cell2".to_string()],
        ];

        let markdown = table_to_markdown(&table);
        assert!(markdown.contains("| Header1 | Header2 |"));
        assert!(markdown.contains("| --- | --- |"));
        assert!(markdown.contains("| Cell1 | Cell2 |"));
    }

    #[test]
    fn test_table_to_markdown_escape_pipes() {
        let table = vec![vec!["A|B".to_string(), "C".to_string()]];

        let markdown = table_to_markdown(&table);
        assert!(markdown.contains("A\\|B"));
    }
}
