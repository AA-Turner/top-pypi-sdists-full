//! PDF extraction regression tests using ground truth.
//!
//! These tests ensure extraction quality does not regress across all output formats
//! (Markdown, Djot, Plain) by comparing extracted text against ground truth files
//! using word-level F1 scoring.
//!
//! Two extraction routes are tested:
//! - **PDFium (native)**: Direct text extraction from searchable PDFs
//! - **OCR**: Image rendering → Tesseract OCR → plain text
//!
//! Usage:
//!   # All quality gates (Markdown, Djot, Plain):
//!   cargo test -p kreuzberg --features "pdf,bundled-pdfium" --test pdf_markdown_regression -- --nocapture
//!
//!   # Include OCR path tests (slow, needs tesseract):
//!   cargo test -p kreuzberg --features "pdf,ocr,bundled-pdfium" --test pdf_markdown_regression -- --ignored --nocapture

#![cfg(feature = "pdf")]

mod helpers;

use helpers::*;
use kreuzberg::core::config::{ExtractionConfig, OutputFormat};
use kreuzberg::extract_file_sync;
use std::collections::HashMap;
use std::path::PathBuf;

// ═══════════════════════════════════════════════════════════════════
// Scoring utilities
// ═══════════════════════════════════════════════════════════════════

/// Tokenize text into normalized lowercase words for comparison.
fn tokenize(text: &str) -> Vec<String> {
    text.split_whitespace()
        .map(|w| w.trim_matches(|c: char| c.is_ascii_punctuation()).to_lowercase())
        .filter(|w| !w.is_empty())
        .collect()
}

/// Compute word-level bag-of-words precision, recall, and F1 between extracted and ground truth.
fn word_f1(extracted: &str, ground_truth: &str) -> (f64, f64, f64) {
    let ext_tokens = tokenize(extracted);
    let gt_tokens = tokenize(ground_truth);

    if gt_tokens.is_empty() && ext_tokens.is_empty() {
        return (1.0, 1.0, 1.0);
    }
    if gt_tokens.is_empty() || ext_tokens.is_empty() {
        return (0.0, 0.0, 0.0);
    }

    let mut gt_bag: HashMap<&str, usize> = HashMap::new();
    for t in &gt_tokens {
        *gt_bag.entry(t.as_str()).or_insert(0) += 1;
    }

    let mut ext_bag: HashMap<&str, usize> = HashMap::new();
    for t in &ext_tokens {
        *ext_bag.entry(t.as_str()).or_insert(0) += 1;
    }

    let mut matching = 0usize;
    for (word, &ext_count) in &ext_bag {
        if let Some(&gt_count) = gt_bag.get(word) {
            matching += ext_count.min(gt_count);
        }
    }

    let precision = matching as f64 / ext_tokens.len() as f64;
    let recall = matching as f64 / gt_tokens.len() as f64;
    let f1 = if precision + recall > 0.0 {
        2.0 * precision * recall / (precision + recall)
    } else {
        0.0
    };

    (precision, recall, f1)
}

// ═══════════════════════════════════════════════════════════════════
// PDF path resolution
// ═══════════════════════════════════════════════════════════════════

/// Resolve a ground truth name to its actual PDF file path.
fn resolve_pdf_path(gt_name: &str) -> Option<PathBuf> {
    let base = get_test_documents_dir();

    let candidates = [
        base.join(format!("pdf/{}.pdf", gt_name)),
        base.join(format!("vendored/docling/pdf/{}.pdf", gt_name)),
        base.join(format!("vendored/pdfplumber/pdf/{}.pdf", gt_name)),
        base.join(format!("vendored/pdfplumber/pdf/from-oss-fuzz/load/{}.pdf", gt_name)),
        base.join(format!("vendored/markitdown/pdf/{}.pdf", gt_name)),
        base.join(format!("vendored/markitdown/{}.pdf", gt_name)),
        base.join(format!("vendored/pdfium-render/{}.pdf", gt_name)),
    ];

    candidates.into_iter().find(|p| p.exists())
}

/// Load ground truth text for a given name.
fn load_ground_truth(gt_name: &str) -> Option<String> {
    let gt_path = get_test_file_path(&format!("ground_truth/pdf/{}.txt", gt_name));
    if gt_path.exists() {
        std::fs::read_to_string(&gt_path).ok()
    } else {
        None
    }
}

// ═══════════════════════════════════════════════════════════════════
// Ground truth entries with calibrated thresholds
//
// Thresholds are set ~7% below measured F1 to catch regressions
// while allowing minor fluctuations. Documents with placeholder/
// invalid GTs have threshold 0.0 (extraction-must-not-crash only).
// ═══════════════════════════════════════════════════════════════════

const PDFIUM_GROUND_TRUTH: &[(&str, f64)] = &[
    // ── Docling vendored PDFs ──
    ("2203.01017v2", 0.62),           // measured ~0.69
    ("2206.01062", 0.54),             // measured ~0.61
    ("2305.03393v1", 0.55),           // measured ~0.63
    ("2305.03393v1-pg9", 0.67),       // measured ~0.74
    ("amt_handbook_sample", 0.74),    // measured ~0.81
    ("code_and_formula", 0.83),       // measured ~0.90
    ("multi_page", 0.93),             // measured ~1.00
    ("picture_classification", 0.70), // measured ~0.77–0.88 (varies by format)
    ("redp5110_sampled", 0.80),       // measured ~0.87
    ("right_to_left_01", 0.50),       // measured ~0.56
    ("right_to_left_02", 0.66),       // measured ~0.73
    ("right_to_left_03", 0.57),       // measured ~0.64
    // ── pdfplumber vendored PDFs ──
    ("150109DSP-Milw-505-90D", 0.88),                 // measured ~0.95
    ("2023-06-20-PV", 0.80),                          // measured ~0.87
    ("annotations", 0.0),                             // placeholder GT
    ("annotations-rotated-180", 0.20),                // measured ~0.33
    ("annotations-rotated-270", 0.15),                // measured ~0.29
    ("annotations-rotated-90", 0.15),                 // measured ~0.29
    ("annotations-unicode-issues", 0.63),             // measured ~0.71
    ("chelsea_pdta", 0.78),                           // measured ~0.85
    ("cupertino_usd_4-6-16", 0.90),                   // measured ~0.96
    ("extra-attrs-example", 0.0),                     // placeholder GT
    ("federal-register-2020-17221", 0.83),            // measured ~0.90
    ("figure_structure", 0.93),                       // measured ~1.00
    ("hello_structure", 0.82),                        // measured ~0.89
    ("image_structure", 0.30),                        // measured ~0.43
    ("issue-1054-example", 0.0),                      // sparse GT
    ("issue-1114-dedupe-chars", 0.93),                // measured ~1.00
    ("issue-1147-example", 0.48),                     // measured ~0.54
    ("issue-1181", 0.55),                             // measured ~0.60–0.75 (varies by format)
    ("issue-1279-example", 0.15),                     // measured ~0.24
    ("issue-13-151201DSP-Fond-581-90D", 0.85),        // measured ~0.91
    ("issue-140-example", 0.0),                       // image-only
    ("issue-192-example", 0.50),                      // measured ~0.57
    ("issue-316-example", 0.84),                      // measured ~0.90
    ("issue-33-lorem-ipsum", 0.63),                   // measured ~0.70
    ("issue-336-example", 0.46),                      // measured ~0.53
    ("issue-461-example", 0.0),                       // CJK medical report
    ("issue-463-example", 0.86),                      // measured ~0.92
    ("issue-466-example", 0.91),                      // measured ~0.98
    ("issue-53-example", 0.90),                       // measured ~0.96
    ("issue-598-example", 0.84),                      // measured ~0.90
    ("issue-67-example", 0.52),                       // measured ~0.58
    ("issue-71-duplicate-chars", 0.15),               // measured ~0.24
    ("issue-71-duplicate-chars-2", 0.74),             // measured ~0.80
    ("issue-842-example", 0.57),                      // measured ~0.64
    ("issue-848", 0.15),                              // measured ~0.24
    ("issue-90-example", 0.57),                       // measured ~0.64
    ("issue-905", 0.0),                               // placeholder GT
    ("issue-912", 0.61),                              // measured ~0.68
    ("issue-982-example", 0.62),                      // measured ~0.69
    ("issue-987-test", 0.59),                         // measured ~0.67
    ("la-precinct-bulletin-2014-p1", 0.91),           // measured ~0.97
    ("line-char-render-example", 0.30),               // measured ~0.40 (3-word GT, volatile F1)
    ("malformed-from-issue-932", 0.20),               // measured ~0.35
    ("mcid_example", 0.93),                           // measured ~1.00
    ("nics-background-checks-2015-11", 0.93),         // measured ~1.00
    ("nics-background-checks-2015-11-rotated", 0.73), // measured ~0.80
    ("page-boxes-example", 0.93),                     // measured ~1.00
    ("pdf_structure", 0.87),                          // measured ~0.93
    ("pdffill-demo", 0.57),                           // measured ~0.65
    ("pr-136-example", 0.10),                         // measured ~0.19
    ("pr-138-example", 0.59),                         // measured ~0.66
    ("pr-88-example", 0.52),                          // measured ~0.58
    ("scotus-transcript-p1", 0.77),                   // measured ~0.83
    ("senate-expenditures", 0.0),                     // complex tabular
    ("table-curves-example", 0.87),                   // measured ~0.93
    ("test-punkt", 0.59),                             // measured ~0.67
    ("WARN-Report-for-7-1-2015-to-03-25-2016", 0.93), // measured ~0.99
    ("word365_structure", 0.89),                      // measured ~0.96
    // ── markitdown vendored PDFs ──
    ("masterformat_partial_numbering", 0.90),         // measured ~0.96
    ("RECEIPT-2024-TXN-98765_retail_purchase", 0.89), // measured ~0.95
    ("REPAIR-2022-INV-001_multipage", 0.87),          // measured ~0.94
    ("SPARSE-2024-INV-1234_borderless_table", 0.87),  // measured ~0.94
    ("test", 0.86),                                   // measured ~0.92
];

// ═══════════════════════════════════════════════════════════════════
// Shared quality gate runner
// ═══════════════════════════════════════════════════════════════════

/// Extract a PDF with the given output format.
fn extract_with_format(pdf_path: &std::path::Path, format: OutputFormat) -> Option<kreuzberg::types::ExtractionResult> {
    let config = ExtractionConfig {
        output_format: format,
        ..Default::default()
    };
    extract_file_sync(pdf_path, None, &config).ok()
}

/// Result of running the quality gate across all documents.
#[allow(dead_code)]
struct QualityGateResult {
    tested: usize,
    passed: usize,
    failed: usize,
    skipped: usize,
    avg_f1: f64,
    failures: Vec<String>,
}

/// Run the quality gate for a given output format with per-document F1 thresholds.
///
/// `threshold_scale` scales the base thresholds (e.g. 0.9 for plain text which may
/// score slightly lower due to missing formatting structure in the ground truth).
fn run_quality_gate(
    format: OutputFormat,
    ground_truth: &[(&str, f64)],
    label: &str,
    threshold_scale: f64,
) -> QualityGateResult {
    let mut tested = 0usize;
    let mut skipped = 0usize;
    let mut passed = 0usize;
    let mut failed = 0usize;
    let mut f1_sum = 0.0f64;
    let mut failures: Vec<String> = Vec::new();

    println!("\n{}", "=".repeat(100));
    println!("{} — Ground Truth Quality Gate", label);
    println!("{}", "=".repeat(100));
    println!(
        "{:<50} {:>8} {:>8} {:>8} {:>6} {:>8}",
        "Document", "Prec", "Recall", "F1", "Thresh", "Status"
    );
    println!("{}", "-".repeat(100));

    for &(gt_name, base_min_f1) in ground_truth {
        let gt = match load_ground_truth(gt_name) {
            Some(gt) => gt,
            None => {
                skipped += 1;
                continue;
            }
        };

        let pdf_path = match resolve_pdf_path(gt_name) {
            Some(p) => p,
            None => {
                skipped += 1;
                continue;
            }
        };

        let result = match extract_with_format(&pdf_path, format) {
            Some(r) => r,
            None => {
                println!(
                    "{:<50} {:>8} {:>8} {:>8} {:>6} {:>8}",
                    gt_name, "-", "-", "-", "-", "ERR"
                );
                failed += 1;
                failures.push(format!("{}: extraction failed", gt_name));
                continue;
            }
        };

        let min_f1 = base_min_f1 * threshold_scale;
        let (precision, recall, f1) = word_f1(&result.content, &gt);
        tested += 1;
        f1_sum += f1;

        let status = if f1 >= min_f1 { "PASS" } else { "FAIL" };
        if f1 < min_f1 {
            failed += 1;
            failures.push(format!("{}: F1={:.3} < threshold {:.2}", gt_name, f1, min_f1));
        } else {
            passed += 1;
        }

        println!(
            "{:<50} {:>7.1}% {:>7.1}% {:>7.1}% {:>5.0}% {:>8}",
            gt_name,
            precision * 100.0,
            recall * 100.0,
            f1 * 100.0,
            min_f1 * 100.0,
            status
        );
    }

    let avg_f1 = if tested > 0 { f1_sum / tested as f64 } else { 0.0 };

    println!("{}", "-".repeat(100));
    println!(
        "Summary: {} tested, {} passed, {} failed, {} skipped, avg F1={:.1}%",
        tested,
        passed,
        failed,
        skipped,
        avg_f1 * 100.0
    );

    if !failures.is_empty() {
        println!("\nFailures:");
        for f in &failures {
            println!("  - {}", f);
        }
    }

    QualityGateResult {
        tested,
        passed,
        failed,
        skipped,
        avg_f1,
        failures,
    }
}

// ═══════════════════════════════════════════════════════════════════
// Section 1: PDFium Path — Quality Gates per Output Format
// ═══════════════════════════════════════════════════════════════════

#[test]
fn test_pdfium_quality_gate() {
    if !test_documents_available() {
        println!("Skipping: test_documents not available");
        return;
    }

    let result = run_quality_gate(
        OutputFormat::Markdown,
        PDFIUM_GROUND_TRUTH,
        "PDFium Markdown Extraction",
        1.0,
    );

    assert!(
        result.failures.is_empty(),
        "{} document(s) fell below their F1 threshold",
        result.failures.len()
    );
    assert!(
        result.avg_f1 >= 0.62,
        "Average F1 ({:.1}%) is below 62% threshold",
        result.avg_f1 * 100.0
    );
}

#[test]
fn test_pdfium_djot_quality_gate() {
    if !test_documents_available() {
        println!("Skipping: test_documents not available");
        return;
    }

    // Djot output uses the same structural pipeline as Markdown,
    // so thresholds should be equivalent.
    let result = run_quality_gate(OutputFormat::Djot, PDFIUM_GROUND_TRUTH, "PDFium Djot Extraction", 1.0);

    assert!(
        result.failures.is_empty(),
        "{} document(s) fell below their Djot F1 threshold",
        result.failures.len()
    );
    assert!(
        result.avg_f1 >= 0.62,
        "Average Djot F1 ({:.1}%) is below 62% threshold",
        result.avg_f1 * 100.0
    );
}

#[test]
fn test_pdfium_plain_quality_gate() {
    if !test_documents_available() {
        println!("Skipping: test_documents not available");
        return;
    }

    // Plain text scores slightly differently — no markdown formatting artifacts
    // but also no structural enhancements. Use 90% of base thresholds.
    let result = run_quality_gate(
        OutputFormat::Plain,
        PDFIUM_GROUND_TRUTH,
        "PDFium Plain Text Extraction",
        0.90,
    );

    assert!(
        result.failures.is_empty(),
        "{} document(s) fell below their Plain F1 threshold",
        result.failures.len()
    );
    assert!(
        result.avg_f1 >= 0.55,
        "Average Plain F1 ({:.1}%) is below 55% threshold",
        result.avg_f1 * 100.0
    );
}

// ═══════════════════════════════════════════════════════════════════
// Section 1b: Docling.pdf Parity Tests — All Formats
// ═══════════════════════════════════════════════════════════════════

/// Run docling.pdf parity check for a given format.
fn run_docling_parity(format: OutputFormat, label: &str, min_f1: f64) {
    let pdf_path = get_test_file_path("pdf/docling.pdf");
    if !pdf_path.exists() {
        println!("Skipping: docling.pdf not found");
        return;
    }

    let gt_path = get_test_file_path("ground_truth/docling-docling.md");
    if !gt_path.exists() {
        println!("Skipping: docling-docling.md ground truth not found");
        return;
    }

    let gt = std::fs::read_to_string(&gt_path).expect("should read docling ground truth");
    let result = extract_with_format(&pdf_path, format).expect("should extract docling.pdf");

    let (precision, recall, f1) = word_f1(&result.content, &gt);

    println!("=== docling.pdf {} parity check ===", label);
    println!(
        "  Precision: {:.1}%  Recall: {:.1}%  F1: {:.1}%",
        precision * 100.0,
        recall * 100.0,
        f1 * 100.0
    );
    println!("  Extracted words: {}", tokenize(&result.content).len());
    println!("  GT words: {}", tokenize(&gt).len());

    assert!(
        f1 >= min_f1,
        "docling.pdf {} F1 ({:.1}%) regressed below {:.0}% threshold",
        label,
        f1 * 100.0,
        min_f1 * 100.0
    );
}

#[test]
fn test_docling_pdf_parity() {
    run_docling_parity(OutputFormat::Markdown, "Markdown", 0.75);
}

#[test]
fn test_docling_pdf_djot_parity() {
    run_docling_parity(OutputFormat::Djot, "Djot", 0.75);
}

#[test]
fn test_docling_pdf_plain_parity() {
    run_docling_parity(OutputFormat::Plain, "Plain", 0.60);
}

// ═══════════════════════════════════════════════════════════════════
// Section 2: OCR Path — Regression Tests (slow, run with --ignored)
// ═══════════════════════════════════════════════════════════════════

/// Extract text via the OCR (forced) path.
#[cfg(feature = "ocr")]
fn extract_ocr(pdf_path: &std::path::Path) -> Option<kreuzberg::types::ExtractionResult> {
    use kreuzberg::core::config::OcrConfig;

    let config = ExtractionConfig {
        output_format: OutputFormat::Plain,
        ocr: Some(OcrConfig {
            backend: "tesseract".to_string(),
            language: "eng".to_string(),
            ..Default::default()
        }),
        force_ocr: true,
        ..Default::default()
    };

    extract_file_sync(pdf_path, None, &config).ok()
}

/// OCR ground truth entries. Same documents but tested through OCR pipeline.
/// Thresholds are lower because OCR introduces more noise than native extraction.
#[cfg(feature = "ocr")]
const OCR_GROUND_TRUTH: &[(&str, f64)] = &[
    ("hello_structure", 0.30),
    ("multi_page", 0.30),
    ("code_and_formula", 0.20),
    ("2305.03393v1-pg9", 0.20),
    ("amt_handbook_sample", 0.20),
    ("scotus-transcript-p1", 0.30),
    ("federal-register-2020-17221", 0.30),
    ("issue-33-lorem-ipsum", 0.30),
    ("masterformat_partial_numbering", 0.20),
    ("test", 0.20),
];

#[cfg(feature = "ocr")]
#[test]
#[ignore]
fn test_ocr_quality_gate() {
    if !test_documents_available() {
        println!("Skipping: test_documents not available");
        return;
    }

    let mut tested = 0usize;
    let mut skipped = 0usize;
    let mut passed = 0usize;
    let mut failed = 0usize;
    let mut f1_sum = 0.0f64;
    let mut failures: Vec<String> = Vec::new();

    println!("\n{}", "=".repeat(100));
    println!("OCR Extraction — Ground Truth Quality Gate");
    println!("{}", "=".repeat(100));
    println!(
        "{:<50} {:>8} {:>8} {:>8} {:>6} {:>8}",
        "Document", "Prec", "Recall", "F1", "Thresh", "Status"
    );
    println!("{}", "-".repeat(100));

    for &(gt_name, min_f1) in OCR_GROUND_TRUTH {
        let gt = match load_ground_truth(gt_name) {
            Some(gt) => gt,
            None => {
                skipped += 1;
                continue;
            }
        };

        let pdf_path = match resolve_pdf_path(gt_name) {
            Some(p) => p,
            None => {
                skipped += 1;
                continue;
            }
        };

        let result = match extract_ocr(&pdf_path) {
            Some(r) => r,
            None => {
                println!(
                    "{:<50} {:>8} {:>8} {:>8} {:>6} {:>8}",
                    gt_name, "-", "-", "-", "-", "ERR"
                );
                failed += 1;
                failures.push(format!("{}: OCR extraction failed", gt_name));
                continue;
            }
        };

        let (precision, recall, f1) = word_f1(&result.content, &gt);
        tested += 1;
        f1_sum += f1;

        let status = if f1 >= min_f1 { "PASS" } else { "FAIL" };
        if f1 < min_f1 {
            failed += 1;
            failures.push(format!("{}: F1={:.3} < threshold {:.2}", gt_name, f1, min_f1));
        } else {
            passed += 1;
        }

        println!(
            "{:<50} {:>7.1}% {:>7.1}% {:>7.1}% {:>5.0}% {:>8}",
            gt_name,
            precision * 100.0,
            recall * 100.0,
            f1 * 100.0,
            min_f1 * 100.0,
            status
        );
    }

    let avg_f1 = if tested > 0 { f1_sum / tested as f64 } else { 0.0 };

    println!("{}", "-".repeat(100));
    println!(
        "Summary: {} tested, {} passed, {} failed, {} skipped, avg F1={:.1}%",
        tested,
        passed,
        failed,
        skipped,
        avg_f1 * 100.0
    );

    if !failures.is_empty() {
        println!("\nFailures:");
        for f in &failures {
            println!("  - {}", f);
        }
    }

    assert!(
        failures.is_empty(),
        "{} document(s) fell below their OCR F1 threshold",
        failures.len()
    );
}

// ═══════════════════════════════════════════════════════════════════
// Section 3: Detailed per-document snapshot (run with --ignored)
// ═══════════════════════════════════════════════════════════════════

#[test]
#[ignore]
fn test_pdfium_detailed_snapshot() {
    if !test_documents_available() {
        println!("Skipping: test_documents not available");
        return;
    }

    println!("\n{}", "=".repeat(120));
    println!("PDFium Markdown — Detailed Snapshot");
    println!("{}", "=".repeat(120));

    for &(gt_name, _) in PDFIUM_GROUND_TRUTH {
        let gt = match load_ground_truth(gt_name) {
            Some(gt) => gt,
            None => continue,
        };
        let pdf_path = match resolve_pdf_path(gt_name) {
            Some(p) => p,
            None => continue,
        };
        let result = match extract_with_format(&pdf_path, OutputFormat::Markdown) {
            Some(r) => r,
            None => continue,
        };

        let (precision, recall, f1) = word_f1(&result.content, &gt);
        let ext_words = tokenize(&result.content).len();
        let gt_words = tokenize(&gt).len();
        let headings: Vec<&str> = result.content.lines().filter(|l| l.trim().starts_with('#')).collect();

        println!("\n--- {} ---", gt_name);
        println!(
            "  P={:.1}% R={:.1}% F1={:.1}%  |  extracted={} words, gt={} words  |  {} headings  |  {} tables",
            precision * 100.0,
            recall * 100.0,
            f1 * 100.0,
            ext_words,
            gt_words,
            headings.len(),
            result.tables.len()
        );

        let preview: String = result.content.chars().take(300).collect();
        println!("  Preview: {}", preview.replace('\n', " \\n "));
    }
}

// ═══════════════════════════════════════════════════════════════════
// Unit tests for scoring utilities
// ═══════════════════════════════════════════════════════════════════

#[cfg(test)]
mod scoring_tests {
    use super::*;

    #[test]
    fn test_word_f1_identical() {
        let (p, r, f1) = word_f1("hello world", "hello world");
        assert!((p - 1.0).abs() < 0.001);
        assert!((r - 1.0).abs() < 0.001);
        assert!((f1 - 1.0).abs() < 0.001);
    }

    #[test]
    fn test_word_f1_no_overlap() {
        let (p, r, f1) = word_f1("hello world", "foo bar");
        assert!(p < 0.001);
        assert!(r < 0.001);
        assert!(f1 < 0.001);
    }

    #[test]
    fn test_word_f1_partial_overlap() {
        let (p, r, f1) = word_f1("hello world foo", "hello world bar");
        assert!(p > 0.5);
        assert!(r > 0.5);
        assert!(f1 > 0.5);
    }

    #[test]
    fn test_word_f1_empty() {
        let (_, _, f1) = word_f1("", "");
        assert!((f1 - 1.0).abs() < 0.001);

        let (_, _, f1) = word_f1("hello", "");
        assert!(f1 < 0.001);

        let (_, _, f1) = word_f1("", "hello");
        assert!(f1 < 0.001);
    }

    #[test]
    fn test_word_f1_case_insensitive() {
        let (_, _, f1) = word_f1("Hello World", "hello world");
        assert!((f1 - 1.0).abs() < 0.001);
    }

    #[test]
    fn test_word_f1_punctuation_stripped() {
        let (_, _, f1) = word_f1("hello, world!", "hello world");
        assert!((f1 - 1.0).abs() < 0.001);
    }

    #[test]
    fn test_resolve_pdf_path_basic() {
        let _ = resolve_pdf_path("nonexistent_document_12345");
    }
}
