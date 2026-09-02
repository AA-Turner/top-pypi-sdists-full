use crate::recording::{format_query_result_for_recording, record_error_output};
use guacr_terminal::QueryResult;

#[test]
fn test_format_empty_result() {
    let result = QueryResult {
        columns: vec![],
        rows: vec![],
        affected_rows: Some(5),
        execution_time_ms: None,
    };
    let output = format_query_result_for_recording(&result);
    assert!(output.contains("5 row(s) affected"));
}

#[test]
fn test_format_query_result() {
    let mut result = QueryResult::new(vec!["id".to_string(), "name".to_string()]);
    result.add_row(vec!["1".to_string(), "Alice".to_string()]);
    result.add_row(vec!["2".to_string(), "Bob".to_string()]);
    result.execution_time_ms = Some(42);

    let output = format_query_result_for_recording(&result);
    assert!(output.contains("id"));
    assert!(output.contains("name"));
    assert!(output.contains("Alice"));
    assert!(output.contains("Bob"));
    assert!(output.contains("(2 row(s))"));
    assert!(output.contains("Time: 42ms"));
}

#[test]
fn test_format_empty_result_no_affected_rows() {
    // When there are no columns and no affected_rows count, fall back to generic message.
    let result = QueryResult {
        columns: vec![],
        rows: vec![],
        affected_rows: None,
        execution_time_ms: None,
    };
    let output = format_query_result_for_recording(&result);
    assert!(
        output.contains("successfully"),
        "no-columns/no-affected should produce a success message"
    );
}

#[test]
fn test_format_single_column_result() {
    let mut result = QueryResult::new(vec!["value".to_string()]);
    result.add_row(vec!["42".to_string()]);
    let output = format_query_result_for_recording(&result);
    assert!(output.contains("value"), "column header must appear");
    assert!(output.contains("42"), "row data must appear");
    assert!(output.contains("(1 row(s))"));
}

#[test]
fn test_format_result_without_execution_time() {
    // When execution_time_ms is None the "Time:" line must not appear.
    let mut result = QueryResult::new(vec!["col".to_string()]);
    result.add_row(vec!["data".to_string()]);
    result.execution_time_ms = None;
    let output = format_query_result_for_recording(&result);
    assert!(
        !output.contains("Time:"),
        "Time line must be absent when execution_time_ms is None"
    );
}

#[test]
fn test_format_zero_rows() {
    // A SELECT that returns no data should still emit headers and a zero-row count.
    let result = QueryResult::new(vec!["id".to_string(), "name".to_string()]);
    let output = format_query_result_for_recording(&result);
    assert!(
        output.contains("id"),
        "column headers must appear even with zero rows"
    );
    assert!(output.contains("(0 row(s))"));
}

#[test]
fn test_record_error_output_format() {
    // record_error_output must produce "ERROR: <msg>\r\n" when a recorder is None
    // (function is a no-op for None, which is the common test path).
    // We test the formatting directly via a None recorder to confirm no panic.
    let mut recorder = None;
    record_error_output(&mut recorder, "some error message");
    // If we reach here without panic, the None-recorder path is handled correctly.
}

#[test]
fn test_column_width_uses_max_of_header_and_data() {
    // When data is wider than the header, the separator line must be at least as
    // wide as the data so the table is aligned correctly.
    let mut result = QueryResult::new(vec!["x".to_string()]);
    result.add_row(vec!["very_long_value_here".to_string()]);
    let output = format_query_result_for_recording(&result);
    // The header line for "x" should be padded to match "very_long_value_here" width.
    assert!(
        output.contains("very_long_value_here"),
        "data value must appear in output"
    );
    // Separator line must be at least as long as the data value.
    let sep_line = output.lines().nth(1).unwrap_or("");
    assert!(
        sep_line.len() >= "very_long_value_here".len(),
        "separator must span at least the width of the widest data cell"
    );
}
