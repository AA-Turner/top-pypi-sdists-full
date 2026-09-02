use crate::ratatui_db_ui::{AppFocus, DatabaseRatatuiApp, ViewMode};
use ratatui::widgets::TableState;

#[test]
fn test_focus_starts_as_input() {
    let app = DatabaseRatatuiApp::new("test> ", "->", true);
    assert_eq!(app.focus, AppFocus::Input);
}

#[test]
fn test_default_view_mode_is_terminal() {
    let app = DatabaseRatatuiApp::new("test> ", "->", true);
    assert_eq!(app.view_mode, ViewMode::Terminal);
}

#[test]
fn test_tab_in_terminal_mode_switches_to_grid() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    assert_eq!(app.view_mode, ViewMode::Terminal);
    app.handle_key(0xFF09, true); // Tab
    assert_eq!(app.view_mode, ViewMode::Grid);
}

#[test]
fn test_f5_toggles_view_mode() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    assert_eq!(app.view_mode, ViewMode::Terminal);
    app.handle_key(0x0007, true); // Ctrl+G
    assert_eq!(app.view_mode, ViewMode::Grid);
    app.handle_key(0x0007, true); // Ctrl+G again
    assert_eq!(app.view_mode, ViewMode::Terminal);
}

#[test]
fn test_tab_in_grid_mode_toggles_focus() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    app.view_mode = ViewMode::Grid;
    app.results = vec![vec!["a".into()]];
    app.table_state = TableState::default();
    app.handle_key(0xFF09, true); // Tab in Grid mode
    assert_eq!(app.focus, AppFocus::Results);
    assert_eq!(app.table_state.selected(), Some(0));
}

#[test]
fn test_tab_back_to_input_in_grid_mode() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    app.view_mode = ViewMode::Grid;
    app.results = vec![vec!["a".into()]];
    app.focus = AppFocus::Results;
    app.handle_key(0xFF09, true); // Tab again in Grid mode
    assert_eq!(app.focus, AppFocus::Input);
}

#[test]
fn test_arrow_down_navigates_results_when_focused_in_grid() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    app.view_mode = ViewMode::Grid;
    app.results = vec![
        vec!["row1".into()],
        vec!["row2".into()],
        vec!["row3".into()],
    ];
    app.focus = AppFocus::Results;
    app.table_state.select(Some(0));
    app.handle_key(0xFF54, true); // Down
    assert_eq!(app.table_state.selected(), Some(1));
}

#[test]
fn test_arrow_down_no_op_in_input_focus() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    app.add_to_history("select 1");
    app.handle_key(0xFF52, true); // Up -- go to history entry
    let history_idx_before = app.history_idx;
    let table_sel_before = app.table_state.selected();
    assert_eq!(app.focus, AppFocus::Input);
    app.handle_key(0xFF54, true); // Down -- should navigate history, not table
    assert_ne!(app.history_idx, history_idx_before);
    assert_eq!(app.table_state.selected(), table_sel_before);
}

#[test]
fn test_printable_key_returns_focus_to_input() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    app.focus = AppFocus::Results;
    app.handle_key(0x61, true); // 'a'
    assert_eq!(app.focus, AppFocus::Input);
    assert_eq!(app.input_buffer, "a");
}

#[test]
fn test_tab_in_grid_with_empty_results_returns_to_terminal() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->", true);
    app.view_mode = ViewMode::Grid;
    app.focus = AppFocus::Input;
    app.handle_key(0xFF09, true); // Tab with no results — wraps back to Terminal
    assert_eq!(app.view_mode, ViewMode::Terminal);
}

#[test]
fn test_scrollback_command_echo() {
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", true);
    app.append_scrollback_command("mysql> SELECT 1");
    assert_eq!(app.scrollback.len(), 1);
    assert_eq!(app.scroll_offset, 0);
}

#[test]
fn test_scrollback_snaps_to_bottom_on_result() {
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", true);
    app.scroll_offset = 5;
    let result = guacr_terminal::QueryResult {
        columns: vec!["id".to_string()],
        rows: vec![vec!["1".to_string()]],
        affected_rows: None,
        execution_time_ms: None,
    };
    app.append_result_to_scrollback(&result);
    assert_eq!(app.scroll_offset, 0);
}

#[test]
fn test_scrollback_result_formatting() {
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", true);
    let result = guacr_terminal::QueryResult {
        columns: vec!["id".to_string(), "name".to_string()],
        rows: vec![
            vec!["1".to_string(), "Alice".to_string()],
            vec!["2".to_string(), "Bob".to_string()],
        ],
        affected_rows: None,
        execution_time_ms: None,
    };
    app.append_result_to_scrollback(&result);
    // sep + header + sep + 2 rows + sep + row count = 7 lines
    assert_eq!(app.scrollback.len(), 7);
}

#[test]
fn test_history_recalled_command_can_be_recalled_again() {
    // Reproduce: type "show databases;", submit, up recalls it, submit again,
    // up arrow should recall it again — not forget it.
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", true);

    // First submission
    for c in "show databases;".chars() {
        app.handle_key(c as u32, true);
    }
    app.handle_key(0xFF0D, true); // Enter

    // Navigate to it with Up
    app.handle_key(0xFF52, true); // Up
    assert_eq!(app.input_buffer, "show databases;");

    // Submit again (same command)
    app.handle_key(0xFF0D, true); // Enter

    // Up should still recall it
    app.handle_key(0xFF52, true); // Up
    assert_eq!(
        app.input_buffer, "show databases;",
        "should recall after re-submit"
    );
}

#[test]
fn test_page_up_scrolls_terminal_scrollback() {
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", true);
    for i in 0..50 {
        app.append_scrollback_info(&format!("line {}", i));
    }
    assert_eq!(app.scroll_offset, 0);
    app.handle_key(0xFF55, true); // Page Up
    assert_eq!(app.scroll_offset, 10);
    app.handle_key(0xFF56, true); // Page Down
    assert_eq!(app.scroll_offset, 0);
}

// ---------------------------------------------------------------------------
// Affected row count — status message display path
//
// `set_results` builds the status_msg string used both in the Grid view title
// and the terminal scrollback.  The branch `if let Some(affected) =
// result.affected_rows` must show the real count, not a hardcoded zero.
// ---------------------------------------------------------------------------

/// When a DML result reports N affected rows, `set_results` must show
/// "Query OK, N row(s) affected" in status_msg — not 0.
///
/// This is the UI-side counterpart to the `execution_result_to_query_result`
/// fix: even if the driver returns the correct count, a wrong branch in
/// `set_results` could silently display 0 to the user.
#[test]
fn test_set_results_shows_affected_row_count() {
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", false);
    let result = guacr_terminal::QueryResult {
        columns: vec![],
        rows: vec![],
        affected_rows: Some(7),
        execution_time_ms: Some(3),
    };
    app.set_results(&result);
    assert!(
        app.status_msg.contains("7"),
        "status_msg must contain the affected row count 7; got: {:?}",
        app.status_msg
    );
    assert!(
        app.status_msg.contains("affected"),
        "status_msg must say 'affected'; got: {:?}",
        app.status_msg
    );
}

/// When affected_rows is None (e.g. a DDL statement where the driver cannot
/// report a count), the status must fall back to the generic success message.
#[test]
fn test_set_results_no_affected_count_shows_success_message() {
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", false);
    let result = guacr_terminal::QueryResult {
        columns: vec![],
        rows: vec![],
        affected_rows: None,
        execution_time_ms: None,
    };
    app.set_results(&result);
    assert!(
        app.status_msg.contains("successfully") || app.status_msg.contains("OK"),
        "status_msg must contain a success phrase when affected_rows is None; got: {:?}",
        app.status_msg
    );
}

/// The affected row count scrollback message must also show the real count,
/// not 0.  `append_result_to_scrollback` has a parallel branch for the
/// no-columns DML path.
#[test]
fn test_append_result_to_scrollback_shows_affected_row_count() {
    let mut app = DatabaseRatatuiApp::new("mysql> ", "->", false);
    let result = guacr_terminal::QueryResult {
        columns: vec![],
        rows: vec![],
        affected_rows: Some(3),
        execution_time_ms: None,
    };
    app.append_result_to_scrollback(&result);
    let found = app.scrollback.iter().any(|line| {
        let s = match line {
            crate::ratatui_db_ui::ScrollbackLine::Info(s) => s,
            crate::ratatui_db_ui::ScrollbackLine::Output(s) => s,
            _ => return false,
        };
        s.contains("3")
    });
    assert!(
        found,
        "scrollback must contain the affected row count 3; scrollback: {:?}",
        app.scrollback
            .iter()
            .map(|l| match l {
                crate::ratatui_db_ui::ScrollbackLine::Info(s)
                | crate::ratatui_db_ui::ScrollbackLine::Output(s) => s.as_str(),
                _ => "",
            })
            .collect::<Vec<_>>()
    );
}
