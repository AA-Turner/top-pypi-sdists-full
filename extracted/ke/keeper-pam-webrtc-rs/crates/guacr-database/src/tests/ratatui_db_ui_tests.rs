use crate::ratatui_db_ui::{AppFocus, DatabaseRatatuiApp};
use ratatui::widgets::TableState;

#[test]
fn test_focus_starts_as_input() {
    let app = DatabaseRatatuiApp::new("test> ", "->");
    assert_eq!(app.focus, AppFocus::Input);
}

#[test]
fn test_tab_toggles_focus() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->");
    app.results = vec![vec!["a".into()]];
    app.table_state = TableState::default();
    app.handle_key(0xFF09, true); // Tab
    assert_eq!(app.focus, AppFocus::Results);
    assert_eq!(app.table_state.selected(), Some(0));
}

#[test]
fn test_tab_back_to_input() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->");
    app.results = vec![vec!["a".into()]];
    app.focus = AppFocus::Results;
    app.handle_key(0xFF09, true); // Tab again
    assert_eq!(app.focus, AppFocus::Input);
}

#[test]
fn test_arrow_down_navigates_results_when_focused() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->");
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
    let mut app = DatabaseRatatuiApp::new("test> ", "->");
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
    let mut app = DatabaseRatatuiApp::new("test> ", "->");
    app.focus = AppFocus::Results;
    app.handle_key(0x61, true); // 'a'
    assert_eq!(app.focus, AppFocus::Input);
    assert_eq!(app.input_buffer, "a");
}

#[test]
fn test_tab_with_empty_results_stays_results() {
    let mut app = DatabaseRatatuiApp::new("test> ", "->");
    app.handle_key(0xFF09, true); // Tab with no results
    assert_eq!(app.focus, AppFocus::Results);
    assert_eq!(app.table_state.selected(), None);
}
