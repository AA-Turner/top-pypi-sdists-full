use crate::recording::format_query_result_for_recording;
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
