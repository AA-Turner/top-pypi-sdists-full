//! Content parity debug test.
//!
//! Compares async `extract_file` vs sync `extract_file_sync` on files that
//! return empty content in CI benchmark FFI bindings but succeed in native Rust.
//! Run with `--nocapture` to see diagnostic output.
//!
//! Usage:
//!   cargo test --test content_parity_debug -p kreuzberg --features pdf,office,email -- --nocapture

use kreuzberg::core::config::ExtractionConfig;
use kreuzberg::core::extractor::extract_file;
#[cfg(feature = "tokio-runtime")]
use kreuzberg::core::extractor::extract_file_sync;
use std::path::PathBuf;

mod helpers;

fn workspace_root() -> PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .to_path_buf()
}

fn test_doc(rel: &str) -> PathBuf {
    workspace_root().join(rel)
}

fn print_result_summary(
    label: &str,
    file: &str,
    result: &Result<kreuzberg::ExtractionResult, kreuzberg::KreuzbergError>,
) {
    match result {
        Ok(r) => {
            let content_len = r.content.len();
            let trimmed_len = r.content.trim().len();
            let preview: String = r.content.chars().take(200).collect();
            eprintln!("[{label}] {file}:");
            eprintln!(
                "  content_len={content_len}, trimmed_len={trimmed_len}, mime={}",
                r.mime_type
            );
            eprintln!("  preview: {:?}", preview);
            eprintln!();
        }
        Err(e) => {
            eprintln!("[{label}] {file}: ERROR: {e}");
            eprintln!();
        }
    }
}

/// Test annotation PDF - reported as empty_content in FFI benchmarks
#[cfg(feature = "pdf")]
#[tokio::test]
async fn parity_annotation_pdf() {
    let path = test_doc("test_documents/vendored/pdfplumber/pdf/annotations.pdf");
    if !path.exists() {
        eprintln!("SKIP: {:?} not found", path);
        return;
    }

    let config = ExtractionConfig::default();

    let async_result = extract_file(&path, None, &config).await;
    print_result_summary("ASYNC", "annotations.pdf", &async_result);

    // Run sync in a blocking thread to avoid nested runtime panic
    let sync_path = path.clone();
    let sync_config = config.clone();
    let sync_result = tokio::task::spawn_blocking(move || extract_file_sync(&sync_path, None, &sync_config))
        .await
        .unwrap();
    print_result_summary("SYNC ", "annotations.pdf", &sync_result);

    match (&async_result, &sync_result) {
        (Ok(a), Ok(s)) => {
            assert_eq!(
                a.content, s.content,
                "Content mismatch between async and sync for annotations.pdf"
            );
            if a.content.trim().is_empty() {
                eprintln!("WARNING: Both async and sync return empty content for annotations.pdf");
                eprintln!("  This means the PDF has no extractable page text (only annotations).");
            }
        }
        (Err(ae), Err(se)) => {
            eprintln!("Both failed: async={ae}, sync={se}");
        }
        _ => {
            panic!(
                "Parity mismatch: async={:?}, sync={:?}",
                async_result.is_ok(),
                sync_result.is_ok()
            );
        }
    }
}

/// Test ODT with text content
#[cfg(feature = "office")]
#[tokio::test]
async fn parity_odt_simple() {
    let path = test_doc("test_documents/odt/simple.odt");
    if !path.exists() {
        eprintln!("SKIP: {:?} not found", path);
        return;
    }

    let config = ExtractionConfig::default();

    let async_result = extract_file(&path, None, &config).await;
    print_result_summary("ASYNC", "simple.odt", &async_result);

    let sync_path = path.clone();
    let sync_config = config.clone();
    let sync_result = tokio::task::spawn_blocking(move || extract_file_sync(&sync_path, None, &sync_config))
        .await
        .unwrap();
    print_result_summary("SYNC ", "simple.odt", &sync_result);

    match (&async_result, &sync_result) {
        (Ok(a), Ok(s)) => {
            assert_eq!(
                a.content, s.content,
                "Content mismatch between async and sync for simple.odt"
            );
            assert!(!a.content.trim().is_empty(), "simple.odt should have content");
        }
        _ => {
            panic!(
                "Extraction failed: async={:?}, sync={:?}",
                async_result.as_ref().err(),
                sync_result.as_ref().err()
            );
        }
    }
}

/// Test ODT with unordered list - reported as empty in FFI benchmarks
#[cfg(feature = "office")]
#[tokio::test]
async fn parity_odt_unordered_list() {
    let path = test_doc("test_documents/odt/unorderedList.odt");
    if !path.exists() {
        eprintln!("SKIP: {:?} not found", path);
        return;
    }

    let config = ExtractionConfig::default();

    let async_result = extract_file(&path, None, &config).await;
    print_result_summary("ASYNC", "unorderedList.odt", &async_result);

    let sync_path = path.clone();
    let sync_config = config.clone();
    let sync_result = tokio::task::spawn_blocking(move || extract_file_sync(&sync_path, None, &sync_config))
        .await
        .unwrap();
    print_result_summary("SYNC ", "unorderedList.odt", &sync_result);

    match (&async_result, &sync_result) {
        (Ok(a), Ok(s)) => {
            assert_eq!(a.content, s.content, "Content mismatch for unorderedList.odt");
            assert!(!a.content.trim().is_empty(), "unorderedList.odt should have content");
        }
        _ => {
            panic!(
                "Extraction failed: async={:?}, sync={:?}",
                async_result.as_ref().err(),
                sync_result.as_ref().err()
            );
        }
    }
}

/// Test UTF-16 EML files - reported as empty across ALL bindings including WASM
#[cfg(feature = "email")]
#[tokio::test]
async fn parity_utf16_eml() {
    let files = [
        "test_documents/vendored/unstructured/eml/fake-email-utf-16.eml",
        "test_documents/vendored/unstructured/eml/fake-email-utf-16-le.eml",
        "test_documents/vendored/unstructured/eml/fake-email-utf-16-be.eml",
    ];

    let config = ExtractionConfig::default();

    for rel_path in &files {
        let path = test_doc(rel_path);
        if !path.exists() {
            eprintln!("SKIP: {:?} not found", path);
            continue;
        }

        let filename = path.file_name().unwrap().to_str().unwrap().to_string();

        let async_result = extract_file(&path, None, &config).await;
        print_result_summary("ASYNC", &filename, &async_result);

        let sync_path = path.clone();
        let sync_config = config.clone();
        let sync_result = tokio::task::spawn_blocking(move || extract_file_sync(&sync_path, None, &sync_config))
            .await
            .unwrap();
        print_result_summary("SYNC ", &filename, &sync_result);

        match (&async_result, &sync_result) {
            (Ok(a), Ok(s)) => {
                assert_eq!(a.content, s.content, "Content mismatch for {filename}");
                if a.content.trim().is_empty() {
                    eprintln!("BUG CONFIRMED: {filename} returns empty content in both async and sync");
                    eprintln!("  This is the UTF-16 EML parsing bug - mail_parser cannot handle UTF-16 encoding");
                }
            }
            (Err(ae), Err(se)) => {
                eprintln!("BUG CONFIRMED: {filename} fails in both: async={ae}, sync={se}");
            }
            _ => {
                eprintln!(
                    "Parity mismatch for {filename}: async={:?}, sync={:?}",
                    async_result.is_ok(),
                    sync_result.is_ok()
                );
            }
        }
    }
}

/// Test annotation PDF rotated variants
#[cfg(feature = "pdf")]
#[tokio::test]
async fn parity_annotation_pdf_rotated() {
    let files = [
        "test_documents/vendored/pdfplumber/pdf/annotations-rotated-90.pdf",
        "test_documents/vendored/pdfplumber/pdf/annotations-rotated-180.pdf",
        "test_documents/vendored/pdfplumber/pdf/annotations-rotated-270.pdf",
    ];

    let config = ExtractionConfig::default();

    for rel_path in &files {
        let path = test_doc(rel_path);
        if !path.exists() {
            eprintln!("SKIP: {:?} not found", path);
            continue;
        }

        let filename = path.file_name().unwrap().to_str().unwrap().to_string();

        let async_result = extract_file(&path, None, &config).await;
        print_result_summary("ASYNC", &filename, &async_result);

        let sync_path = path.clone();
        let sync_config = config.clone();
        let sync_result = tokio::task::spawn_blocking(move || extract_file_sync(&sync_path, None, &sync_config))
            .await
            .unwrap();
        print_result_summary("SYNC ", &filename, &sync_result);

        match (&async_result, &sync_result) {
            (Ok(a), Ok(s)) => {
                assert_eq!(a.content, s.content, "Content mismatch for {filename}");
                if a.content.trim().is_empty() {
                    eprintln!("INFO: {filename} returns empty content - PDF has only annotations, no page text");
                }
            }
            _ => {
                eprintln!(
                    "Error for {filename}: async={:?}, sync={:?}",
                    async_result.as_ref().err(),
                    sync_result.as_ref().err()
                );
            }
        }
    }
}
