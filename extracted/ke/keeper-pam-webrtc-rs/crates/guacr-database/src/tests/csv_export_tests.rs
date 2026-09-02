use crate::csv_export::{base64_encode, extract_table_name, generate_csv_filename, CsvExporter};
use std::sync::atomic::Ordering;

#[test]
fn test_base64_encode() {
    assert_eq!(base64_encode(b"Hello"), "SGVsbG8=");
    assert_eq!(base64_encode(b"Hello, World!"), "SGVsbG8sIFdvcmxkIQ==");
    assert_eq!(base64_encode(b""), "");
    assert_eq!(base64_encode(b"a"), "YQ==");
    assert_eq!(base64_encode(b"ab"), "YWI=");
    assert_eq!(base64_encode(b"abc"), "YWJj");
}

#[test]
fn test_csv_field_escaping() {
    let mut exporter = CsvExporter::new(1);

    // Simple field
    exporter.write_csv_field("hello");
    assert_eq!(String::from_utf8_lossy(&exporter.buffer), "hello");
    exporter.buffer.clear();

    // Field with comma
    exporter.write_csv_field("hello,world");
    assert_eq!(String::from_utf8_lossy(&exporter.buffer), "\"hello,world\"");
    exporter.buffer.clear();

    // Field with quote
    exporter.write_csv_field("say \"hello\"");
    assert_eq!(
        String::from_utf8_lossy(&exporter.buffer),
        "\"say \"\"hello\"\"\""
    );
    exporter.buffer.clear();

    // Field with newline
    exporter.write_csv_field("line1\nline2");
    assert_eq!(
        String::from_utf8_lossy(&exporter.buffer),
        "\"line1\nline2\""
    );
}

#[test]
fn test_extract_table_name() {
    assert_eq!(extract_table_name("SELECT * FROM users"), Some("users"));
    assert_eq!(
        extract_table_name("SELECT id, name FROM products WHERE id > 5"),
        Some("products")
    );
    assert_eq!(extract_table_name("select * from ORDERS;"), Some("ORDERS"));
    assert_eq!(extract_table_name("INSERT INTO users"), None);
}

#[test]
fn test_generate_filename() {
    let filename = generate_csv_filename("SELECT * FROM users", "mysql");
    assert!(filename.starts_with("mysql_users_export_"));
    assert!(filename.ends_with(".csv"));
}

#[test]
fn test_start_download_instruction() {
    let exporter = CsvExporter::new(5);
    let instruction = exporter.start_download("test.csv");
    let s = String::from_utf8_lossy(&instruction);
    assert!(s.contains("file"));
    assert!(s.contains("text/csv"));
    assert!(s.contains("test.csv"));
}

#[test]
fn test_cancellation() {
    let exporter = CsvExporter::new(1);
    let handle = exporter.cancellation_handle();

    assert!(!exporter.is_cancelled());

    handle.store(true, Ordering::SeqCst);
    assert!(exporter.is_cancelled());
}

/// CSV fields starting with formula prefixes (=, +, -, @) must have those characters
/// escaped to prevent spreadsheet formula injection when the CSV is opened in Excel/LibreOffice.
/// The standard defense is to prefix the cell with a tab so the spreadsheet app
/// treats it as a text value rather than a formula.
#[test]
fn test_csv_write_field_formula_injection_escaped() {
    use crate::csv_export::write_csv_field_to_buf;

    for prefix in ["=", "+", "-", "@"] {
        let field = format!("{prefix}EVIL(A1:B2)");
        let mut buf: Vec<u8> = Vec::new();
        write_csv_field_to_buf(&mut buf, &field);
        let out = String::from_utf8(buf).unwrap();
        assert!(
            !out.contains(prefix) || out.starts_with('\t') || out.starts_with("\""),
            "formula prefix '{prefix}' must be neutralized; got: {out:?}"
        );
        assert!(
            !out.trim_matches('"').starts_with(prefix),
            "formula prefix '{prefix}' must not appear at start of unquoted value; got: {out:?}"
        );
    }
}

#[test]
fn test_csv_write_field_normal_values_unchanged() {
    use crate::csv_export::write_csv_field_to_buf;

    for val in ["hello", "123", "2026-05-13", "normal text"] {
        let mut buf: Vec<u8> = Vec::new();
        write_csv_field_to_buf(&mut buf, val);
        let out = String::from_utf8(buf).unwrap();
        assert_eq!(out, val, "normal value must not be altered");
    }
}

/// start_download must use codepoint counts, not byte counts, for Guacamole LENGTH fields.
/// A non-ASCII filename such as "résultats.csv" has more bytes than codepoints.
/// Using .len() (bytes) produces a wrong LENGTH prefix that breaks the protocol.
#[test]
fn test_start_download_codepoint_length_ascii() {
    let exporter = CsvExporter::new(1);
    let instr = exporter.start_download("export.csv");
    let s = String::from_utf8(instr.to_vec()).unwrap();
    // Guacamole instruction: 4.file,<stream-len>.<stream>,<mime-len>.<mime>,<name-len>.<name>;
    // stream "1" -> len 1, "text/csv" -> len 8, "export.csv" -> len 10
    assert!(
        s.starts_with("4.file,1.1,8.text/csv,10.export.csv;"),
        "got: {s}"
    );
}

#[test]
fn test_start_download_codepoint_length_unicode_filename() {
    let exporter = CsvExporter::new(42);
    // "résultats.csv" = 13 Unicode codepoints, but 14 UTF-8 bytes (é = 2 bytes)
    let filename = "r\u{00e9}sultats.csv";
    let codepoints = filename.chars().count(); // 13
    assert_eq!(codepoints, 13, "sanity: 13 codepoints");
    let instr = exporter.start_download(filename);
    let s = String::from_utf8(instr.to_vec()).unwrap();
    // stream "42" -> len 2, "text/csv" -> len 8, filename -> len 13
    let expected_prefix = format!("4.file,2.42,8.text/csv,{}.{};", codepoints, filename);
    assert_eq!(s, expected_prefix, "got: {s}");
}

/// A full round-trip: export_query_result → collect blobs → decode base64 → check CSV content.
#[tokio::test]
async fn test_csv_export_round_trip() {
    use guacr_terminal::QueryResult;
    use tokio::sync::mpsc;

    let mut result = QueryResult::new(vec!["id".to_string(), "name".to_string()]);
    result.add_row(vec!["1".to_string(), "Alice".to_string()]);
    result.add_row(vec!["2".to_string(), "Bob".to_string()]);

    let mut exporter = CsvExporter::new(1000);
    let (tx, mut rx) = mpsc::channel::<bytes::Bytes>(64);

    let file_instr = exporter.start_download("test.csv");
    let file_str = String::from_utf8(file_instr.to_vec()).unwrap();
    assert!(
        file_str.starts_with("4.file,"),
        "file instruction malformed: {file_str}"
    );
    assert!(
        file_str.contains("text/csv"),
        "missing mimetype: {file_str}"
    );
    assert!(
        file_str.contains("test.csv"),
        "missing filename: {file_str}"
    );

    let export_result = exporter.export_query_result(&result, &tx).await;
    drop(tx);
    assert!(
        export_result.is_ok(),
        "export failed: {:?}",
        export_result.err()
    );

    // Collect blob and end instructions
    let mut blobs: Vec<bytes::Bytes> = Vec::new();
    let mut end_count = 0usize;
    while let Some(msg) = rx.recv().await {
        let s = String::from_utf8(msg.to_vec()).unwrap();
        if s.starts_with("4.blob,") {
            blobs.push(bytes::Bytes::from(s));
        } else if s.starts_with("3.end,") {
            end_count += 1;
        }
    }

    assert!(
        end_count == 1,
        "expected exactly 1 end instruction, got {end_count}"
    );
    assert!(!blobs.is_empty(), "expected at least one blob instruction");

    // Decode each blob and concatenate CSV content
    let mut csv_content = String::new();
    for blob in &blobs {
        let s = String::from_utf8(blob.to_vec()).unwrap();
        // Format: "4.blob,<stream-len>.<stream>,<data-len>.<base64>;"
        let content = s.trim_start_matches("4.blob,").trim_end_matches(';');
        let parts: Vec<&str> = content.splitn(3, ',').collect();
        assert_eq!(parts.len(), 2, "blob instruction must have 2 args");
        let b64 = parts[1]
            .split_once('.')
            .map(|x| x.1)
            .expect("blob data missing");
        let decoded = crate::csv_import::base64_decode(b64.as_bytes()).expect("decode failed");
        csv_content.push_str(&String::from_utf8(decoded).expect("UTF-8"));
    }

    // Header row
    assert!(
        csv_content.contains("id,name"),
        "header row missing: {csv_content}"
    );
    // Data rows
    assert!(
        csv_content.contains("1,Alice"),
        "row 1 missing: {csv_content}"
    );
    assert!(
        csv_content.contains("2,Bob"),
        "row 2 missing: {csv_content}"
    );
}

/// When there are no results the QueryExecutor should return an error, not a file instruction.
/// This is tested via handle_export_csv indirectly: the last_result field starts as None,
/// and calling handle_export_csv on a fresh executor must NOT produce a file instruction.
#[tokio::test]
async fn test_export_csv_no_results_returns_error_render() {
    use crate::query_executor::QueryExecutor;

    let mut executor = QueryExecutor::new("mysql> ", "mysql").unwrap();
    // last_result starts as None — calling handle_export_csv should not crash
    // and must mark the executor dirty (error message shown) but return no file instructions.
    let instr = bytes::Bytes::from("10.export-csv;");
    let result = executor.process_input(&instr).await;
    assert!(
        result.is_ok(),
        "export-csv on empty executor must not return Err"
    );
    let (needs_render, instructions, pending_query) = result.unwrap();
    assert!(needs_render, "should signal render needed after error");
    assert!(
        instructions.is_empty(),
        "no file/blob/end instructions when no results"
    );
    assert!(pending_query.is_none(), "no pending query");
}

/// Storing a result and then exporting must produce a file instruction followed by blobs.
#[tokio::test]
async fn test_export_csv_with_results_produces_file_instruction() {
    use crate::query_executor::QueryExecutor;
    use guacr_terminal::QueryResult;

    let mut executor = QueryExecutor::new("mysql> ", "mysql").unwrap();
    let mut result = QueryResult::new(vec!["col".to_string()]);
    result.add_row(vec!["val".to_string()]);
    executor.write_result(&result).unwrap();

    let instr = bytes::Bytes::from("10.export-csv;");
    let out = executor.process_input(&instr).await;
    assert!(out.is_ok(), "export-csv with results must succeed");
    let (needs_render, instructions, _) = out.unwrap();
    // needs_render is false when export is successful (no error message shown)
    assert!(!needs_render, "no error render when export succeeds");
    assert!(
        !instructions.is_empty(),
        "must produce at least file + blob + end"
    );

    let first = String::from_utf8(instructions[0].to_vec()).unwrap();
    assert!(
        first.starts_with("4.file,"),
        "first instruction must be file: {first}"
    );

    let last = String::from_utf8(instructions.last().unwrap().to_vec()).unwrap();
    assert!(
        last.starts_with("3.end,"),
        "last instruction must be end: {last}"
    );
}
