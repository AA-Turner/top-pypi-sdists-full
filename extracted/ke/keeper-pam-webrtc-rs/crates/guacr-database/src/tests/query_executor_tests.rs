use crate::query_executor::{ExecutionResult, QueryExecutor};
use guacr_terminal::QueryResult;

#[test]
fn test_query_executor_new() {
    let executor = QueryExecutor::new("mysql> ", "mysql");
    assert!(executor.is_ok());
    assert_eq!(executor.unwrap().db_type(), "mysql");
}

#[test]
fn test_execution_result() {
    let result = QueryResult::new(vec!["id".to_string()]);
    let exec_result = ExecutionResult::new(result, std::time::Duration::from_millis(100));
    let query_result = exec_result.into_query_result();
    assert_eq!(query_result.execution_time_ms, Some(100));
}

#[test]
fn test_command_history() {
    let mut executor = QueryExecutor::new("test> ", "test").unwrap();

    executor.app.add_to_history("SELECT 1");
    executor.app.add_to_history("SELECT 2");
    executor.app.add_to_history("SELECT 3");

    assert_eq!(executor.app.history.len(), 3);

    // Navigate up (keysym 0xFF52 = Up arrow)
    executor.app.handle_key(0xFF52, true);
    assert_eq!(executor.app.input_buffer, "SELECT 3");

    executor.app.handle_key(0xFF52, true);
    assert_eq!(executor.app.input_buffer, "SELECT 2");

    executor.app.handle_key(0xFF52, true);
    assert_eq!(executor.app.input_buffer, "SELECT 1");

    // Can't go further back
    executor.app.handle_key(0xFF52, true);
    assert_eq!(executor.app.input_buffer, "SELECT 1");

    // Navigate down (keysym 0xFF54 = Down arrow)
    executor.app.handle_key(0xFF54, true);
    assert_eq!(executor.app.input_buffer, "SELECT 2");

    executor.app.handle_key(0xFF54, true);
    assert_eq!(executor.app.input_buffer, "SELECT 3");
}

#[test]
fn test_history_deduplication() {
    let mut executor = QueryExecutor::new("test> ", "test").unwrap();

    executor.app.add_to_history("SELECT 1");
    executor.app.add_to_history("SELECT 1"); // Duplicate
    executor.app.add_to_history("SELECT 2");

    assert_eq!(executor.app.history.len(), 2);
}

#[test]
fn test_history_max_size() {
    let mut executor = QueryExecutor::new("test> ", "test").unwrap();
    executor.app.history_max_size = 3;

    executor.app.add_to_history("SELECT 1");
    executor.app.add_to_history("SELECT 2");
    executor.app.add_to_history("SELECT 3");
    executor.app.add_to_history("SELECT 4");

    assert_eq!(executor.app.history.len(), 3);
    assert_eq!(executor.app.history[0], "SELECT 2");
    assert_eq!(executor.app.history[2], "SELECT 4");
}

#[test]
fn test_cursor_movement() {
    let mut executor = QueryExecutor::new("test> ", "test").unwrap();

    executor.app.input_buffer = "SELECT * FROM users".to_string();
    executor.app.cursor_pos = 19;

    // Move left (0xFF51)
    executor.app.handle_key(0xFF51, true);
    assert_eq!(executor.app.cursor_pos, 18);

    // Move right (0xFF53)
    executor.app.handle_key(0xFF53, true);
    assert_eq!(executor.app.cursor_pos, 19);

    // Can't move right past end
    executor.app.handle_key(0xFF53, true);
    assert_eq!(executor.app.cursor_pos, 19);

    // Home (0xFF50)
    executor.app.handle_key(0xFF50, true);
    assert_eq!(executor.app.cursor_pos, 0);

    // Can't move left past beginning
    executor.app.handle_key(0xFF51, true);
    assert_eq!(executor.app.cursor_pos, 0);

    // End (0xFF57)
    executor.app.handle_key(0xFF57, true);
    assert_eq!(executor.app.cursor_pos, 19);
}

#[test]
fn test_insert_char() {
    let mut executor = QueryExecutor::new("test> ", "test").unwrap();

    executor.app.input_buffer = "SELECT FROM users".to_string();
    executor.app.cursor_pos = 7;

    // Insert '*' (keysym = 0x2A = 42)
    executor.app.handle_key(0x2A, true);
    executor.app.handle_key(0x20, true); // space

    assert_eq!(executor.app.input_buffer, "SELECT * FROM users");
    assert_eq!(executor.app.cursor_pos, 9);
}

#[test]
fn test_delete_operations() {
    let mut executor = QueryExecutor::new("test> ", "test").unwrap();

    executor.app.input_buffer = "SELECT * FROM users".to_string();
    executor.app.cursor_pos = 9;

    // Backspace (0xFF08)
    executor.app.handle_key(0xFF08, true);
    assert_eq!(executor.app.input_buffer, "SELECT *FROM users");
    assert_eq!(executor.app.cursor_pos, 8);

    // Delete at cursor (0xFFFF)
    executor.app.handle_key(0xFFFF, true);
    assert_eq!(executor.app.input_buffer, "SELECT *ROM users");
    assert_eq!(executor.app.cursor_pos, 8);
}

#[test]
fn test_kill_operations() {
    let mut executor = QueryExecutor::new("test> ", "test").unwrap();

    // Kill to end (Ctrl+K = 0x000B)
    executor.app.input_buffer = "SELECT * FROM users".to_string();
    executor.app.cursor_pos = 9;
    executor.app.handle_key(0x000B, true);
    assert_eq!(executor.app.input_buffer, "SELECT * ");

    // Kill entire line (Ctrl+U = 0x0015)
    executor.app.input_buffer = "SELECT * FROM users".to_string();
    executor.app.cursor_pos = 10;
    executor.app.handle_key(0x0015, true);
    assert_eq!(executor.app.input_buffer, "");
    assert_eq!(executor.app.cursor_pos, 0);

    // Kill word (Ctrl+W = 0x0017)
    executor.app.input_buffer = "SELECT * FROM users".to_string();
    executor.app.cursor_pos = 13;
    executor.app.handle_key(0x0017, true);
    assert_eq!(executor.app.input_buffer, "SELECT *  users");
}

#[test]
fn test_set_current_database() {
    let mut executor = QueryExecutor::new("mysql> ", "mysql").unwrap();

    executor.set_current_database(Some("testdb".to_string()));
    assert_eq!(executor.current_database, Some("testdb".to_string()));

    // Prompt should be updated
    assert!(executor.app.prompt.contains("testdb"));
}

#[test]
fn test_continuation_mode() {
    let mut executor = QueryExecutor::new("mysql> ", "mysql").unwrap();

    assert!(!executor.in_continuation);

    executor.set_continuation(true);
    assert!(executor.in_continuation);

    executor.set_continuation(false);
    assert!(!executor.in_continuation);
}

/// Visual smoke test: renders a 150-row result set to JPEG and saves to /tmp.
///
/// Run with: cargo test -p guacr-database test_render_smoke -- --nocapture
/// Then:     open /tmp/db_render_test.jpg
///
/// Verify:
///   - JPEG is not blank/black
///   - Results panel shows table with 150 rows (no 100-row cap)
///   - Title shows "Results - 150 row(s) (42ms)"
///   - Column headers are rendered
///   - Scrollbar is visible on the right
///   - Input panel shows "mysql> _" at the bottom
#[tokio::test]
async fn test_render_smoke() {
    let mut executor = QueryExecutor::new_with_size("mysql> ", "mysql", 40, 120).unwrap();

    let mut result = QueryResult::new(vec![
        "id".to_string(),
        "name".to_string(),
        "email".to_string(),
        "status".to_string(),
    ]);
    for i in 0..150 {
        result.add_row(vec![
            i.to_string(),
            format!("User {}", i),
            format!("user{}@example.com", i),
            if i % 3 == 0 { "active" } else { "inactive" }.to_string(),
        ]);
    }
    result.execution_time_ms = Some(42);
    executor.write_result(&result).unwrap();

    let (_, instructions) = executor.render_screen().await.unwrap();
    assert!(!instructions.is_empty(), "render produced no instructions");

    let jpeg = executor.ratatui.render_to_jpeg(85).unwrap();
    assert!(
        jpeg.len() > 1000,
        "JPEG suspiciously small ({} bytes)",
        jpeg.len()
    );

    let path = std::env::temp_dir().join("db_render_test.jpg");
    std::fs::write(&path, &jpeg).unwrap();
    println!("Saved {} bytes to {}", jpeg.len(), path.display());
}

/// Visual test: types text into the input line and renders to JPEG.
///
/// Run with: cargo test -p guacr-database test_render_input_editing -- --nocapture
/// Then:     open /tmp/db_input_test.jpg
///
/// Verify:
///   - Query panel shows "mysql> SELECT * FROM users_"
///   - Results panel shows "Connected to MySQL"
#[tokio::test]
async fn test_render_input_editing() {
    let mut executor = QueryExecutor::new_with_size("mysql> ", "mysql", 40, 120).unwrap();
    executor.write_status("Connected to MySQL");

    for c in "SELECT * FROM users".chars() {
        executor.app.handle_key(c as u32, true);
    }

    let (_, instructions) = executor.render_screen().await.unwrap();
    assert!(!instructions.is_empty());

    let jpeg = executor.ratatui.render_to_jpeg(85).unwrap();
    let path = std::env::temp_dir().join("db_input_test.jpg");
    std::fs::write(&path, &jpeg).unwrap();
    println!("Saved {} bytes to {}", jpeg.len(), path.display());
}

/// Tests that resize updates the ratatui terminal dimensions.
#[tokio::test]
async fn test_render_resize() {
    let mut executor = QueryExecutor::new_with_size("mysql> ", "mysql", 24, 80).unwrap();

    let (rows, cols) = executor.size();
    assert_eq!(cols, 80);
    assert_eq!(rows, 24);

    let new_cols = (1920u32 / 9) as u16; // 213
    let new_rows = (1080u32 / 18) as u16; // 60
    executor.ratatui.resize(new_cols, new_rows).unwrap();
    // ratatui applies the resize on the next draw
    executor.render_screen().await.unwrap();

    let (rows, cols) = executor.size();
    assert_eq!(cols, 213);
    assert_eq!(rows, 60);
}
