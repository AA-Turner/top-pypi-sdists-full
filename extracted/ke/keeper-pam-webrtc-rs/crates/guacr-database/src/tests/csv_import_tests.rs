use crate::csv_import::{
    base64_decode, escape_sql_value, parse_csv, parse_csv_line, CsvData, CsvImporter,
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
    assert!(inserts[0].contains("INSERT INTO `users`"));
    assert!(inserts[0].contains("'Alice'"));
    assert!(inserts[0].contains("30"));
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
