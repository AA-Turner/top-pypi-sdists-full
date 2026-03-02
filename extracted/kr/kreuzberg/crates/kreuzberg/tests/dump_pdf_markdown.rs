//! Dump PDF markdown output for manual inspection.
//! Run with: cargo test --all-features --test dump_pdf_markdown -- --ignored --show-output

#![cfg(feature = "pdf")]

mod helpers;

use helpers::*;
use kreuzberg::core::config::{ExtractionConfig, OutputFormat};
use kreuzberg::extract_file_sync;

#[test]
#[ignore] // Only run manually for inspection
fn dump_fake_memo_markdown() {
    if skip_if_missing("pdf/fake_memo.pdf") {
        eprintln!("SKIP: fake_memo.pdf not found");
        return;
    }

    let path = get_test_file_path("pdf/fake_memo.pdf");

    let md_config = ExtractionConfig {
        output_format: OutputFormat::Markdown,
        ..Default::default()
    };
    let md_result = extract_file_sync(&path, None, &md_config).expect("Markdown extraction failed");

    let plain_config = ExtractionConfig::default();
    let plain_result = extract_file_sync(&path, None, &plain_config).expect("Plain extraction failed");

    // Write to /tmp for inspection
    std::fs::write("/tmp/fake_memo_markdown.md", &md_result.content).expect("write failed");
    std::fs::write("/tmp/fake_memo_plain.txt", &plain_result.content).expect("write failed");

    eprintln!("=== PLAIN (first 800 chars) ===");
    eprintln!("{}", &plain_result.content[..plain_result.content.len().min(800)]);
    eprintln!("\n=== MARKDOWN (first 800 chars) ===");
    eprintln!("{}", &md_result.content[..md_result.content.len().min(800)]);
    eprintln!("\n=== STATS ===");
    eprintln!(
        "Plain: {} chars, mime={}",
        plain_result.content.len(),
        plain_result.mime_type
    );
    eprintln!(
        "Markdown: {} chars, mime={}",
        md_result.content.len(),
        md_result.mime_type
    );
    eprintln!("Has '# ' heading: {}", md_result.content.contains("# "));
    eprintln!("Paragraph breaks: {}", md_result.content.matches("\n\n").count());
    eprintln!("\nFiles written to /tmp/fake_memo_markdown.md and /tmp/fake_memo_plain.txt");
}

#[test]
#[ignore]
fn dump_google_doc_markdown() {
    if skip_if_missing("pdf/google_doc_document.pdf") {
        eprintln!("SKIP: google_doc_document.pdf not found");
        return;
    }

    let path = get_test_file_path("pdf/google_doc_document.pdf");

    let md_config = ExtractionConfig {
        output_format: OutputFormat::Markdown,
        ..Default::default()
    };
    let md_result = extract_file_sync(&path, None, &md_config).expect("Markdown extraction failed");

    std::fs::write("/tmp/google_doc_markdown.md", &md_result.content).expect("write failed");

    eprintln!("=== MARKDOWN (first 1000 chars) ===");
    eprintln!("{}", &md_result.content[..md_result.content.len().min(1000)]);
    eprintln!("\n=== STATS ===");
    eprintln!(
        "Markdown: {} chars, mime={}",
        md_result.content.len(),
        md_result.mime_type
    );
    eprintln!("Has '# ' heading: {}", md_result.content.contains("# "));
    eprintln!("Paragraph breaks: {}", md_result.content.matches("\n\n").count());
}

#[test]
#[ignore]
fn dump_redp5110_markdown() {
    if skip_if_missing("vendored/docling/pdf/redp5110_sampled.pdf") {
        eprintln!("SKIP: redp5110_sampled.pdf not found");
        return;
    }

    let path = get_test_file_path("vendored/docling/pdf/redp5110_sampled.pdf");

    let md_config = ExtractionConfig {
        output_format: OutputFormat::Markdown,
        ..Default::default()
    };
    let md_result = extract_file_sync(&path, None, &md_config).expect("Markdown extraction failed");

    let plain_config = ExtractionConfig::default();
    let plain_result = extract_file_sync(&path, None, &plain_config).expect("Plain extraction failed");

    eprintln!(
        "=== PLAIN: {} words ===",
        plain_result.content.split_whitespace().count()
    );
    eprintln!(
        "=== MARKDOWN: {} words ===",
        md_result.content.split_whitespace().count()
    );
    eprintln!(
        "Markdown first 500 chars: {}",
        &md_result.content[..md_result.content.len().min(500)]
    );
}
