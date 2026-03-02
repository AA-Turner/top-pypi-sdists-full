#![cfg(feature = "pdf")]

mod helpers;

use helpers::*;
use kreuzberg::core::config::{ExtractionConfig, OutputFormat};
use kreuzberg::extract_file_sync;

#[test]
#[ignore]
fn debug_table_cells_gmft() {
    let pdfs = ["pdf/tiny.pdf", "pdf/google_doc_document.pdf"];

    for pdf_path in &pdfs {
        if skip_if_missing(pdf_path) {
            continue;
        }

        let path = get_test_file_path(pdf_path);
        let config = ExtractionConfig {
            output_format: OutputFormat::Markdown,
            ..Default::default()
        };

        let result = extract_file_sync(&path, None, &config).expect("extraction should succeed");

        eprintln!("\n=== {} ===", pdf_path);
        eprintln!("Tables: {}", result.tables.len());
        eprintln!("Content ({} chars):", result.content.len());
        eprintln!("{}", &result.content[..result.content.len().min(2000)]);

        for (i, table) in result.tables.iter().enumerate() {
            eprintln!(
                "\n  Table {} ({}x{}, page {}):",
                i + 1,
                table.cells.len(),
                table.cells.first().map_or(0, |r| r.len()),
                table.page_number
            );
            for (r, row) in table.cells.iter().enumerate() {
                let cells: Vec<String> = row
                    .iter()
                    .map(|c| {
                        let s = c.trim();
                        if s.len() > 50 {
                            format!("{}...", &s[..50])
                        } else {
                            s.to_string()
                        }
                    })
                    .collect();
                eprintln!("    Row {}: {:?}", r, cells);
            }
        }
    }
}
