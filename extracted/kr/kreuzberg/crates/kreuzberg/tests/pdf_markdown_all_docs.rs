//! Comprehensive PDF markdown extraction test across ALL test documents.
//!
//! Run with:
//!   cargo test -p kreuzberg --features "pdf,bundled-pdfium" --test pdf_markdown_all_docs -- --ignored --show-output
//!
//! This test extracts every PDF in test_documents/pdf/ as both Markdown and Plain,
//! prints the first 500 chars of each, and reports comparative statistics.

#![cfg(feature = "pdf")]

mod helpers;

use helpers::*;
use kreuzberg::core::config::{ExtractionConfig, OutputFormat};
use kreuzberg::extract_file_sync;

/// All PDF filenames in test_documents/pdf/.
const ALL_PDFS: &[&str] = &[
    "100_g_networking_technology_overview_slides_toronto_august_2016.pdf",
    "5_level_paging_and_5_level_ept_intel_revision_1_1_may_2017.pdf",
    "a_brief_introduction_to_neural_networks_neuronalenetze_en_zeta2_2col_dkrieselcom.pdf",
    "a_brief_introduction_to_the_standard_annotation_language_sal_2006.pdf",
    "a_catalogue_of_optimizing_transformations_1971_allen_catalog.pdf",
    "a_comparison_of_programming_languages_in_economics_16_jun_2014.pdf",
    "a_comprehensive_study_of_convergent_and_commutative_replicated_data_types.pdf",
    "a_comprehensive_study_of_main_memory_partitioning_and_its_application_to_large_scale_comparison_and_radix_sort_sigmod14_i.pdf",
    "a_course_in_machine_learning_ciml_v0_9_all.pdf",
    "algebra_topology_differential_calculus_and_optimization_theory_for_computer_science_and_machine_learning_2019_math_deep.pdf",
    "an_introduction_to_statistical_learning_with_applications_in_r_islr_sixth_printing.pdf",
    "assembly_language_for_beginners_al4_b_en.pdf",
    "bayesian_data_analysis_third_edition_13th_feb_2020.pdf",
    "code_and_formula.pdf",
    "copy_protected.pdf",
    "embedded_images_tables.pdf",
    "fake_memo.pdf",
    "fundamentals_of_deep_learning_2014.pdf",
    "google_doc_document.pdf",
    "image_only_german_pdf.pdf",
    "intel_64_and_ia_32_architectures_software_developer_s_manual_combined_volumes_1_4_june_2021_325462_sdm_vol_1_2abcd_3abcd.pdf",
    "large.pdf",
    "medium.pdf",
    "multi_page_tables.pdf",
    "multi_page.pdf",
    "non_ascii_text.pdf",
    "non_searchable.pdf",
    "ocr_test_rotated_180.pdf",
    "ocr_test_rotated_270.pdf",
    "ocr_test_rotated_90.pdf",
    "ocr_test.pdf",
    "password_protected.pdf",
    "perfect_hash_functions_slides.pdf",
    "program_design_in_the_unix_environment.pdf",
    "proof_of_concept_or_gtfo_v13_october_18th_2016.pdf",
    "right_to_left_01.pdf",
    "sample_contract.pdf",
    "scanned.pdf",
    "searchable.pdf",
    "sharable_web_guide.pdf",
    "simple.pdf",
    "table_document.pdf",
    "tatr.pdf",
    "test_article.pdf",
    "the_hideous_name_1985_pike85hideous.pdf",
    "tiny.pdf",
    "with_images.pdf",
    "xerox_alta_link_series_mfp_sag_en_us_2.pdf",
];

fn count_headings(content: &str) -> usize {
    content
        .lines()
        .filter(|line| {
            let trimmed = line.trim();
            trimmed.starts_with("# ")
                || trimmed.starts_with("## ")
                || trimmed.starts_with("### ")
                || trimmed.starts_with("#### ")
                || trimmed.starts_with("##### ")
                || trimmed.starts_with("###### ")
        })
        .count()
}

fn count_bold_markers(content: &str) -> usize {
    content.matches("**").count() / 2
}

fn count_italic_markers(content: &str) -> usize {
    let mut count = 0usize;
    let chars: Vec<char> = content.chars().collect();
    let len = chars.len();
    let mut i = 0;
    while i < len {
        if chars[i] == '*' {
            if i + 1 < len && chars[i + 1] == '*' {
                i += 2;
                continue;
            }
            count += 1;
        }
        i += 1;
    }
    count / 2
}

fn count_paragraph_breaks(content: &str) -> usize {
    content.matches("\n\n").count()
}

fn first_n_chars(content: &str, n: usize) -> &str {
    let end = content
        .char_indices()
        .nth(n)
        .map(|(idx, _)| idx)
        .unwrap_or(content.len());
    &content[..end]
}

fn extract_heading_lines(content: &str) -> Vec<String> {
    content
        .lines()
        .filter(|line| line.trim().starts_with('#'))
        .map(|s| s.to_string())
        .collect()
}

#[test]
#[ignore]
fn test_all_pdfs_markdown_extraction() {
    println!("\n{}", "=".repeat(80));
    println!("COMPREHENSIVE PDF MARKDOWN EXTRACTION TEST");
    println!("Testing {} PDFs from test_documents/pdf/", ALL_PDFS.len());
    println!("{}\n", "=".repeat(80));

    let mut total_tested = 0usize;
    let mut total_skipped = 0usize;
    let mut total_md_failed = 0usize;
    let mut total_plain_failed = 0usize;
    let mut summary_rows: Vec<String> = Vec::new();

    for (idx, pdf_name) in ALL_PDFS.iter().enumerate() {
        let rel = format!("pdf/{}", pdf_name);

        println!("\n{}", "#".repeat(80));
        println!("## [{}/{}] {}", idx + 1, ALL_PDFS.len(), pdf_name);
        println!("{}", "#".repeat(80));

        if skip_if_missing(&rel) {
            println!("  SKIPPED: file not found");
            total_skipped += 1;
            summary_rows.push(format!("{:<70} SKIPPED", pdf_name));
            continue;
        }

        let path = get_test_file_path(&rel);

        // --- Markdown extraction ---
        let md_config = ExtractionConfig {
            output_format: OutputFormat::Markdown,
            ..Default::default()
        };

        let md_result = match extract_file_sync(&path, None, &md_config) {
            Ok(r) => r,
            Err(e) => {
                println!("  MARKDOWN EXTRACTION FAILED: {}", e);
                total_md_failed += 1;
                summary_rows.push(format!("{:<70} MD_FAIL: {}", pdf_name, e));
                continue;
            }
        };

        // --- Plain extraction ---
        let plain_config = ExtractionConfig::default();
        let plain_result = match extract_file_sync(&path, None, &plain_config) {
            Ok(r) => r,
            Err(e) => {
                println!("  PLAIN EXTRACTION FAILED: {}", e);
                total_plain_failed += 1;
                let headings = count_headings(&md_result.content);
                let para_breaks = count_paragraph_breaks(&md_result.content);
                summary_rows.push(format!(
                    "{:<70} md={:<8} headings={:<4} paras={:<4} PLAIN_FAIL: {}",
                    pdf_name,
                    md_result.content.len(),
                    headings,
                    para_breaks,
                    e
                ));
                continue;
            }
        };

        total_tested += 1;

        // --- Statistics ---
        let md_len = md_result.content.len();
        let plain_len = plain_result.content.len();
        let headings = count_headings(&md_result.content);
        let bold_count = count_bold_markers(&md_result.content);
        let italic_count = count_italic_markers(&md_result.content);
        let md_para_breaks = count_paragraph_breaks(&md_result.content);
        let plain_para_breaks = count_paragraph_breaks(&plain_result.content);
        let heading_lines = extract_heading_lines(&md_result.content);
        let md_mime = md_result.mime_type.to_string();
        let plain_mime = plain_result.mime_type.to_string();
        let content_differs = md_result.content != plain_result.content;

        // --- Print Markdown output (first 500 chars) ---
        println!("\n--- MARKDOWN OUTPUT (first 500 chars) ---");
        println!("{}", first_n_chars(&md_result.content, 500));

        // --- Print Plain output (first 500 chars) ---
        println!("\n--- PLAIN OUTPUT (first 500 chars) ---");
        println!("{}", first_n_chars(&plain_result.content, 500));

        // --- Print detected headings ---
        if !heading_lines.is_empty() {
            println!("\n--- DETECTED HEADINGS ({}) ---", heading_lines.len());
            for (i, h) in heading_lines.iter().enumerate().take(20) {
                println!("  [{}] {}", i + 1, h);
            }
            if heading_lines.len() > 20 {
                println!("  ... and {} more", heading_lines.len() - 20);
            }
        }

        // --- Comparison stats ---
        println!("\n--- COMPARISON STATS ---");
        println!("  Markdown length:        {} chars", md_len);
        println!("  Plain length:           {} chars", plain_len);
        println!(
            "  Length ratio (md/plain): {:.2}",
            if plain_len > 0 {
                md_len as f64 / plain_len as f64
            } else {
                0.00
            }
        );
        println!("  Headings detected:      {}", headings);
        println!("  Bold markers:           {}", bold_count);
        println!("  Italic markers:         {}", italic_count);
        println!("  MD paragraph breaks:    {}", md_para_breaks);
        println!("  Plain paragraph breaks: {}", plain_para_breaks);
        println!("  MD mime type:           {}", md_mime);
        println!("  Plain mime type:        {}", plain_mime);
        println!("  Content differs:        {}", content_differs);

        summary_rows.push(format!(
            "{:<70} md={:<8} plain={:<8} hdg={:<4} bold={:<4} ital={:<4} md_para={:<4} pl_para={:<4} differs={}",
            pdf_name,
            md_len,
            plain_len,
            headings,
            bold_count,
            italic_count,
            md_para_breaks,
            plain_para_breaks,
            content_differs
        ));
    }

    // --- Final summary ---
    println!("\n\n{}", "=".repeat(120));
    println!("SUMMARY TABLE");
    println!("{}", "=".repeat(120));
    println!(
        "{:<70} {:<10} {:<10} {:<6} {:<6} {:<6} {:<8} {:<8} DIFFERS",
        "FILENAME", "MD_LEN", "PLAIN_LEN", "HDGS", "BOLD", "ITAL", "MD_PARA", "PL_PARA"
    );
    println!("{}", "-".repeat(120));
    for row in &summary_rows {
        println!("{}", row);
    }
    println!("{}", "-".repeat(120));
    println!("Total tested:       {}", total_tested);
    println!("Total skipped:      {}", total_skipped);
    println!("Markdown failures:  {}", total_md_failed);
    println!("Plain failures:     {}", total_plain_failed);
    println!("{}", "=".repeat(120));
}
