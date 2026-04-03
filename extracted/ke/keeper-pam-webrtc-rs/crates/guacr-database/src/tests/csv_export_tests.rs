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
