use crate::csv_import::{
    base64_decode, escape_sql_value, parse_blob_instruction, parse_csv, parse_csv_line,
    parse_file_instruction, CsvData, CsvImporter,
};
use std::sync::atomic::Ordering;

#[test]
fn test_parse_csv_line_simple() {
    let result = parse_csv_line("a,b,c");
    assert_eq!(result, vec!["a", "b", "c"]);
}

#[test]
fn test_parse_csv_line_quoted() {
    let result = parse_csv_line("\"hello, world\",b,c");
    assert_eq!(result, vec!["hello, world", "b", "c"]);
}

#[test]
fn test_parse_csv_line_escaped_quotes() {
    let result = parse_csv_line("\"say \"\"hello\"\"\",b");
    assert_eq!(result, vec!["say \"hello\"", "b"]);
}

#[test]
fn test_parse_csv() {
    let csv = "name,age,city\nAlice,30,NYC\nBob,25,LA";
    let data = parse_csv(csv).unwrap();

    assert_eq!(data.headers, vec!["name", "age", "city"]);
    assert_eq!(data.rows.len(), 2);
    assert_eq!(data.rows[0], vec!["Alice", "30", "NYC"]);
    assert_eq!(data.rows[1], vec!["Bob", "25", "LA"]);
}

#[test]
fn test_escape_sql_value() {
    assert_eq!(escape_sql_value("hello"), "'hello'");
    assert_eq!(escape_sql_value("it's"), "'it''s'");
    assert_eq!(escape_sql_value("NULL"), "NULL");
    assert_eq!(escape_sql_value(""), "NULL");
    assert_eq!(escape_sql_value("123"), "123");
    assert_eq!(escape_sql_value("45.67"), "45.67");
}

#[test]
fn test_generate_mysql_inserts() {
    let mut importer = CsvImporter::new(1);
    importer.parsed_data = Some(CsvData {
        headers: vec!["name".to_string(), "age".to_string()],
        rows: vec![
            vec!["Alice".to_string(), "30".to_string()],
            vec!["Bob".to_string(), "25".to_string()],
        ],
    });

    let inserts = importer.generate_mysql_inserts("users").unwrap();
    assert_eq!(inserts.len(), 2);
    assert!(
        inserts[0].contains("INSERT INTO `users`"),
        "got: {}",
        inserts[0]
    );
    assert!(
        inserts[0].contains("`name`"),
        "columns must be quoted; got: {}",
        inserts[0]
    );
    assert!(inserts[0].contains("'Alice'"));
    assert!(inserts[0].contains("30"));
}

/// A table name containing a backtick must be escaped so it cannot break
/// out of the identifier quoting and inject SQL.
/// Correct escaping doubles the backtick inside the identifier, keeping the
/// Table names containing SQL meta-characters must be rejected outright.
/// Identifier quoting alone is not sufficient — validate first.
#[test]
fn test_generate_mysql_inserts_table_name_injection() {
    let mut importer = CsvImporter::new(1);
    importer.parsed_data = Some(CsvData {
        headers: vec!["id".to_string()],
        rows: vec![vec!["1".to_string()]],
    });
    // Backtick + SQL injection in table name must be rejected, not quoted.
    let malicious = "users` WHERE 1=1; DROP TABLE users; --";
    let result = importer.generate_mysql_inserts(malicious);
    assert!(
        result.is_err(),
        "Malicious table name must be rejected, not quoted; got: {:?}",
        result
    );
}

#[test]
fn test_generate_postgres_inserts_table_name_injection() {
    let mut importer = CsvImporter::new(1);
    importer.parsed_data = Some(CsvData {
        headers: vec!["id".to_string()],
        rows: vec![vec!["1".to_string()]],
    });
    // Double-quote + SQL injection in table name must be rejected, not quoted.
    let malicious = r#"users"; DROP TABLE users; --"#;
    let result = importer.generate_postgres_inserts(malicious);
    assert!(
        result.is_err(),
        "Malicious table name must be rejected, not quoted; got: {:?}",
        result
    );
}

#[test]
fn test_base64_decode() {
    let decoded = base64_decode(b"SGVsbG8=").unwrap();
    assert_eq!(decoded, b"Hello");

    let decoded = base64_decode(b"SGVsbG8sIFdvcmxkIQ==").unwrap();
    assert_eq!(decoded, b"Hello, World!");
}

#[test]
fn test_cancellation() {
    let importer = CsvImporter::new(1);
    let handle = importer.cancellation_handle();

    assert!(!importer.is_cancelled());
    handle.store(true, Ordering::SeqCst);
    assert!(importer.is_cancelled());
}

// ---------------------------------------------------------------------------
// Mock CSV stream tests — simulate Guacamole blob protocol feeding the importer
// ---------------------------------------------------------------------------

/// The CsvImporter stream API accepts base64-encoded blobs and assembles them
/// into parseable CSV. This tests the full pipeline: base64 → buffer → parse.
///
/// This is the path that would be exercised when real file upload is wired.
#[test]
fn test_mock_csv_stream_single_blob() {
    // Encode a CSV document as base64 (as the Guacamole protocol delivers it)
    let csv = "name,age,city\nAlice,30,NYC\nBob,25,LA\n";
    let b64 = base64::engine::general_purpose::STANDARD.encode(csv);

    let mut importer = CsvImporter::new(1);
    importer.receive_blob(b64.as_bytes()).unwrap();
    let data = importer.finish_receive().unwrap();

    assert_eq!(data.headers, vec!["name", "age", "city"]);
    assert_eq!(data.row_count(), 2);
    assert_eq!(data.rows[0], vec!["Alice", "30", "NYC"]);
    assert_eq!(data.rows[1], vec!["Bob", "25", "LA"]);
}

/// Multiple blob chunks arrive and must be assembled in order.
#[test]
fn test_mock_csv_stream_multiple_blobs() {
    let csv_part1 = "id,value\n1,foo\n";
    let csv_part2 = "2,bar\n3,baz\n";

    let b64_1 = base64::engine::general_purpose::STANDARD.encode(csv_part1);
    let b64_2 = base64::engine::general_purpose::STANDARD.encode(csv_part2);

    let mut importer = CsvImporter::new(2);
    importer.receive_blob(b64_1.as_bytes()).unwrap();
    importer.receive_blob(b64_2.as_bytes()).unwrap();
    let data = importer.finish_receive().unwrap();

    assert_eq!(data.headers, vec!["id", "value"]);
    assert_eq!(data.row_count(), 3);
    assert_eq!(data.rows[0], vec!["1", "foo"]);
    assert_eq!(data.rows[1], vec!["2", "bar"]);
    assert_eq!(data.rows[2], vec!["3", "baz"]);
}

/// Cancelled importer must reject further blobs and refuse to parse.
#[test]
fn test_mock_csv_stream_cancelled_rejects_blob() {
    let csv = "k,v\na,1\n";
    let b64 = base64::engine::general_purpose::STANDARD.encode(csv);

    let mut importer = CsvImporter::new(3);
    importer.cancel();
    let result = importer.receive_blob(b64.as_bytes());
    assert!(result.is_err(), "cancelled importer must reject blobs");
}

/// A blob containing non-base64 data must return an error, not panic or silently corrupt.
#[test]
fn test_mock_csv_stream_invalid_base64_returns_error() {
    let garbage = b"\xff\xfe not base64 \x00";
    let mut importer = CsvImporter::new(4);
    let result = importer.receive_blob(garbage);
    assert!(result.is_err(), "invalid base64 must return an error");
}

// ---------------------------------------------------------------------------
// parse_file_instruction tests
// ---------------------------------------------------------------------------

/// A well-formed Guacamole "file" instruction must parse to stream index,
/// mimetype, and filename.
#[test]
fn test_parse_file_instruction_valid() {
    // Guacamole wire format: 4.file,1.1,9.text/csv,8.data.csv;
    let instruction = b"4.file,1.1,9.text/csv,8.data.csv;";
    let result = parse_file_instruction(instruction);
    assert!(result.is_some(), "valid file instruction must parse");
    let (stream_idx, mimetype, filename) = result.unwrap();
    assert_eq!(stream_idx, 1);
    assert_eq!(mimetype, "text/csv");
    assert_eq!(filename, "data.csv");
}

/// An instruction that does not start with "4.file," must return None.
#[test]
fn test_parse_file_instruction_wrong_opcode() {
    let instruction = b"4.blob,1.1,4.dGVzdA==;";
    let result = parse_file_instruction(instruction);
    assert!(result.is_none(), "non-file instruction must return None");
}

/// An empty slice must return None without panicking.
#[test]
fn test_parse_file_instruction_empty() {
    assert!(parse_file_instruction(b"").is_none());
}

// ---------------------------------------------------------------------------
// parse_blob_instruction tests
// ---------------------------------------------------------------------------

/// A well-formed Guacamole "blob" instruction must parse to stream index and
/// decoded bytes.
#[test]
fn test_parse_blob_instruction_valid() {
    // "hello" base64-encoded is "aGVsbG8="
    // Guacamole wire format: 4.blob,1.1,12.aGVsbG8=;
    let b64 = base64::engine::general_purpose::STANDARD.encode("hello");
    let instruction = format!("4.blob,1.1,{}.{};", b64.len(), b64);
    let result = parse_blob_instruction(instruction.as_bytes());
    assert!(result.is_some(), "valid blob instruction must parse");
    let (stream_idx, data) = result.unwrap();
    assert_eq!(stream_idx, 1);
    assert_eq!(data, b"hello");
}

/// An instruction that does not start with "4.blob," must return None.
#[test]
fn test_parse_blob_instruction_wrong_opcode() {
    let instruction = b"4.file,1.1,9.text/csv,8.data.csv;";
    let result = parse_blob_instruction(instruction);
    assert!(result.is_none(), "non-blob instruction must return None");
}

/// An empty slice must return None without panicking.
#[test]
fn test_parse_blob_instruction_empty() {
    assert!(parse_blob_instruction(b"").is_none());
}

// Needed for base64 encoding in the mock stream tests
use base64::Engine;
