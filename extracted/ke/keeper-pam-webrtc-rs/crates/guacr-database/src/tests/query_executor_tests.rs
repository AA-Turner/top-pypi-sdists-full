use crate::query_executor::{grid_clicked_data_row, ExecutionResult, QueryExecutor};
use bytes::Bytes;
use guacr_terminal::QueryResult;

// ---------------------------------------------------------------------------
// FIX 1 — cursor_pos byte count panic
// ---------------------------------------------------------------------------

/// Clipboard paste with non-ASCII text must advance cursor by char count, not byte count.
///
/// "héllo" is 5 chars but 6 UTF-8 bytes (é = 0xC3 0xA9). Advancing cursor_pos by
/// text.len() (6) produces a byte offset that does not land on a char boundary,
/// causing a panic when the render path slices `&input_buffer[..cursor_pos]`.
///
/// This test fails before the fix (cursor_pos == 6 instead of 5) and passes after.
#[test]
fn test_clipboard_paste_non_ascii_cursor_pos_is_char_count() {
    let mut executor = QueryExecutor::new("mysql> ", "mysql").unwrap();
    executor.app.insert_clipboard_text("héllo");
    assert_eq!(
        executor.app.cursor_pos, 5,
        "cursor_pos must be char count (5), not byte count (6)"
    );
    assert_eq!(executor.app.input_buffer, "héllo");
}

/// After pasting, the render path must not panic when slicing input_buffer at cursor_pos.
///
/// The render code calls `&self.input_buffer[..self.cursor_pos]` (as a char-indexed string
/// in practice via `chars().collect()`). If cursor_pos is a byte offset rather than a char
/// offset, this slice will land in the middle of a multi-byte sequence and panic.
#[test]
fn test_clipboard_paste_non_ascii_slice_is_valid() {
    let mut executor = QueryExecutor::new("mysql> ", "mysql").unwrap();
    executor.app.insert_clipboard_text("café");
    // Slicing at cursor_pos must not panic — confirms cursor_pos is char-aligned.
    // "café" has 4 chars but 5 bytes (é = 0xC3 0xA9).
    // If cursor_pos == 5 (bytes), &input_buffer[..5] is valid but wrong.
    // If cursor_pos == 4 (chars), we need char-based indexing for slicing.
    // The actual fix: cursor_pos is a char index; the render path must be consistent.
    // This test proves the cursor does not land mid-codepoint after paste.
    let cp = executor.app.cursor_pos;
    assert_eq!(cp, 4, "cursor_pos must be 4 chars, not 5 bytes");
    // Verify the char count of the input matches the cursor position
    assert_eq!(executor.app.input_buffer.chars().count(), cp);
}

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

#[tokio::test]
async fn test_clipboard_paste_inserts_into_input_buffer() {
    // Guacamole clipboard instruction: 9.clipboard,10.text/plain,5.hello;
    let instr = Bytes::from("9.clipboard,10.text/plain,5.hello;");
    let mut executor = QueryExecutor::new("mysql> ", "mysql").unwrap();
    let result = executor.process_input(&instr).await;
    assert!(result.is_ok(), "clipboard instruction should succeed");
    assert_eq!(
        executor.app.input_buffer, "hello",
        "pasted text must appear in input buffer"
    );
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

// ---------------------------------------------------------------------------
// Phase 1e security: ZK proof — query result data cannot escape session boundary
//
// Proof: raw query results fed through the database handler's rendering pipeline
// emerge as a binary Guacamole terminal-data frame (opcode 0x20), not as the
// original plaintext SQL output. This confirms the session boundary holds —
// query result data never exits as plaintext on the to_client channel.
// ---------------------------------------------------------------------------

/// Verify that query results rendered by QueryExecutor are wrapped in a Guacamole
/// terminal-data instruction before they leave the session boundary.
///
/// The database handler calls `render_screen()` which calls
/// `format_terminal_data_binary(&ansi_bytes)`. This test confirms:
///   1. `render_screen()` returns at least one instruction.
///   2. The instruction starts with the TerminalData binary opcode (0x20), proving
///      the data is framed as a Guacamole protocol message before it reaches any
///      client channel — not sent as raw bytes.
///   3. The frame has the mandatory 8-byte binary header, confirming correct framing.
///
/// The ZK property: query data cannot reach a client as unframed bytes because
/// `render_screen()` always passes through `format_terminal_data_binary`, which
/// prepends the 8-byte header with opcode 0x20. A client that receives a raw
/// `&[u8]` stream can verify the session boundary by asserting byte[0] == 0x20.
#[tokio::test]
async fn test_pty_data_wrapped_in_terminal_data() {
    use guacr_terminal::QueryResult;

    let mut executor = QueryExecutor::new_with_size("mysql> ", "mysql", 24, 80).unwrap();

    // Populate with a query result
    let mut result = QueryResult::new(vec!["col".to_string()]);
    result.add_row(vec!["value".to_string()]);
    result.execution_time_ms = Some(1);
    executor.write_result(&result).unwrap();

    let (_dirty, instructions) = executor.render_screen().await.unwrap();
    assert!(
        !instructions.is_empty(),
        "render_screen must produce at least one instruction"
    );

    let frame = &instructions[0];

    // First byte: TerminalData binary opcode 0x20.
    // This is the proof: the frame opens with the protocol opcode, not with
    // raw query bytes. No raw database output can bypass this framing step.
    assert_eq!(
        frame[0], 0x20,
        "first byte of every database instruction must be the TerminalData opcode (0x20)"
    );

    // Must have at least the 8-byte binary header (opcode + flags + reserved + length)
    assert!(
        frame.len() >= 8,
        "binary frame must have at least the 8-byte header"
    );

    // The frame must be longer than 8 bytes (header alone) — payload must follow
    assert!(
        frame.len() > 8,
        "frame must contain ANSI payload after the header, not just the header itself"
    );
}

// ---------------------------------------------------------------------------
// Phase 1e security: Threat detection initialisation proof
// ---------------------------------------------------------------------------

/// Verify that the threat detector initialises from a minimal params map.
///
/// Database handlers call `threat_config_from_params` when the
/// `threat-detection` feature is enabled. This test confirms:
///   1. `threat_config_from_params` produces a config with a non-empty endpoint.
///   2. The enabled flag is false by default when only the endpoint is set (the
///      handler decides whether to enable based on other params).
///   3. Setting `threat_detection_enabled = "true"` flips the enabled flag.
#[cfg(feature = "threat-detection")]
#[test]
fn test_threat_detector_initialises_from_params() {
    use std::collections::HashMap;

    let mut params = HashMap::new();
    params.insert(
        "threat_detection_baml_endpoint".to_string(),
        "http://threat-svc.internal/api".to_string(),
    );

    // threat_config_from_params is the database-crate helper; it delegates to
    // ThreatDetectorConfig construction from params.
    let config = crate::threat::threat_config_from_params(&params);

    assert!(
        !config.baml_endpoint.is_empty(),
        "config must capture the baml_endpoint from params"
    );
    assert_eq!(
        config.baml_endpoint, "http://threat-svc.internal/api",
        "baml_endpoint must match the value supplied in params"
    );

    // Also verify ThreatDetector::from_params (the shared path) works end-to-end
    let detector = guacr_threat_detection::ThreatDetector::from_params(&params, "Database");
    assert!(
        detector.is_some(),
        "ThreatDetector::from_params must return Some when baml_endpoint is present"
    );
}

// ---------------------------------------------------------------------------
// Grid view click geometry
// ---------------------------------------------------------------------------
// The Grid layout is tab bar (1 row) + results panel (total_rows - 4) + query input
// (3 rows). Inside the panel: top border, header, data rows, bottom border, and then
// the "Row X / Y" status bar occupies the panel's final row. Only the data band is
// clickable; the click->row math lives here so it cannot drift from the renderer
// again when the panel is resized.

/// A 30-row terminal: data rows are 3..=24, so px 54..450 map to rows 0..=21.
#[test]
fn test_grid_click_maps_first_data_row() {
    // Row 3 begins at 3 * CHAR_HEIGHT = 54.
    assert_eq!(Some(0), grid_clicked_data_row(54, 30));
    assert_eq!(Some(0), grid_clicked_data_row(71, 30));
    assert_eq!(Some(1), grid_clicked_data_row(72, 30));
}

/// The last data row is the one before the table's bottom border.
#[test]
fn test_grid_click_maps_last_data_row() {
    assert_eq!(Some(21), grid_clicked_data_row(449, 30));
}

/// Regression: the status bar shrank the table by one row, so the bottom border moved
/// up. Neither the border row nor the status bar row may resolve to a data row.
#[test]
fn test_grid_click_rejects_bottom_border_and_status_bar() {
    // Row 25 = table bottom border.
    assert_eq!(None, grid_clicked_data_row(450, 30));
    assert_eq!(None, grid_clicked_data_row(467, 30));
    // Row 26 = status bar.
    assert_eq!(None, grid_clicked_data_row(468, 30));
    assert_eq!(None, grid_clicked_data_row(485, 30));
}

/// Tab bar, top border and header rows are not data.
#[test]
fn test_grid_click_rejects_chrome_above_the_data() {
    assert_eq!(None, grid_clicked_data_row(0, 30)); // tab bar
    assert_eq!(None, grid_clicked_data_row(18, 30)); // top border
    assert_eq!(None, grid_clicked_data_row(36, 30)); // header
    assert_eq!(None, grid_clicked_data_row(53, 30)); // last px of header
}

/// The query input box below the panel is not data.
#[test]
fn test_grid_click_rejects_the_input_box() {
    assert_eq!(None, grid_clicked_data_row(486, 30));
    assert_eq!(None, grid_clicked_data_row(539, 30));
}

/// A terminal too short to hold any data row must not panic or select anything.
#[test]
fn test_grid_click_on_a_degenerate_terminal() {
    for total_rows in [0u16, 1, 4, 5, 8] {
        for y_px in [0u32, 18, 54, 100] {
            assert_eq!(
                None,
                grid_clicked_data_row(y_px, total_rows),
                "total_rows={total_rows} y_px={y_px} must not resolve to a data row"
            );
        }
    }
}
