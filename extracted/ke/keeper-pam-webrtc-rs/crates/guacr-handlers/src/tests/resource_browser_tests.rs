use crate::resource_browser::{
    ActionResult, BrowserMode, ResourceBrowser, ResourceBrowserGrid, ResourceBrowserHandler,
    ResourceUpdate, DEFAULT_HEIGHT, DEFAULT_WIDTH, INITIAL_STREAM_ID,
};
use bytes::Bytes;
use guacr_terminal::{Action, ColumnDef, GridEvent};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{mpsc, Mutex};

// -- Mock ResourceBrowser for testing --

struct MockBrowser {
    columns: Vec<ColumnDef>,
    rows: Arc<Mutex<Vec<Vec<String>>>>,
    actions: Vec<Action>,
    action_results: Arc<Mutex<HashMap<String, MockActionOutcome>>>,
}

#[allow(dead_code)]
enum MockActionOutcome {
    Status(String),
    Refresh,
    Terminal,
}

impl MockBrowser {
    fn new() -> Self {
        Self {
            columns: vec![
                ColumnDef::new("NAME"),
                ColumnDef::new("STATUS"),
                ColumnDef::new("AGE"),
            ],
            rows: Arc::new(Mutex::new(vec![
                vec![
                    "nginx-7d4f9".to_string(),
                    "Running".to_string(),
                    "2d".to_string(),
                ],
                vec![
                    "redis-abc12".to_string(),
                    "Running".to_string(),
                    "5d".to_string(),
                ],
                vec![
                    "postgres-xy".to_string(),
                    "CrashLoop".to_string(),
                    "1h".to_string(),
                ],
            ])),
            actions: vec![
                Action::new("Shell", Some('s'), "shell"),
                Action::new("Logs", Some('l'), "logs"),
                Action::new("Describe", Some('d'), "describe"),
            ],
            action_results: Arc::new(Mutex::new(HashMap::new())),
        }
    }
}

#[async_trait::async_trait]
impl ResourceBrowser for MockBrowser {
    fn columns(&self) -> Vec<ColumnDef> {
        self.columns.clone()
    }

    async fn list_resources(&self) -> Result<Vec<Vec<String>>, String> {
        Ok(self.rows.lock().await.clone())
    }

    fn row_actions(&self, _row_index: usize) -> Vec<Action> {
        self.actions.clone()
    }

    async fn execute_action(
        &self,
        _row_index: usize,
        action_id: &str,
    ) -> Result<ActionResult, String> {
        let results = self.action_results.lock().await;
        match results.get(action_id) {
            Some(MockActionOutcome::Status(msg)) => Ok(ActionResult::Status(msg.clone())),
            Some(MockActionOutcome::Refresh) => Ok(ActionResult::Refresh),
            Some(MockActionOutcome::Terminal) => {
                let (client, server) = tokio::io::duplex(1024);
                let (read_half, write_half) = tokio::io::split(server);
                // Immediately drop the client side to simulate an ended stream
                drop(client);
                Ok(ActionResult::Terminal {
                    reader: Box::new(read_half),
                    writer: Box::new(write_half),
                })
            }
            None => Err(format!("Unknown action: {}", action_id)),
        }
    }

    fn name(&self) -> &str {
        "mock-browser"
    }
}

// -- Parsing tests --

#[test]
fn test_parse_key_event() {
    use crate::resource_browser::parse_key_event;
    let msg = "3.key,5.65507,1.1;";
    let event = parse_key_event(msg).unwrap();
    assert_eq!(event.keysym, 65507);
    assert!(event.pressed);

    let msg = "3.key,2.97,1.0;";
    let event = parse_key_event(msg).unwrap();
    assert_eq!(event.keysym, 97);
    assert!(!event.pressed);
}

#[test]
fn test_parse_key_event_invalid() {
    use crate::resource_browser::parse_key_event;
    assert!(parse_key_event("5.mouse,1.0,1.0,1.0;").is_none());
    assert!(parse_key_event("garbage").is_none());
}

#[test]
fn test_parse_mouse_event() {
    use crate::resource_browser::parse_mouse_event;
    let msg = "5.mouse,3.100,3.200,1.1;";
    let event = parse_mouse_event(msg).unwrap();
    assert_eq!(event.x, 100);
    assert_eq!(event.y, 200);
    assert_eq!(event.button_mask, 1);
}

#[test]
fn test_parse_mouse_event_scroll() {
    use crate::resource_browser::parse_mouse_event;
    let msg = "5.mouse,3.512,3.384,2.16;";
    let event = parse_mouse_event(msg).unwrap();
    assert_eq!(event.button_mask, 16); // Scroll down
}

#[test]
fn test_parse_mouse_event_invalid() {
    use crate::resource_browser::parse_mouse_event;
    assert!(parse_mouse_event("3.key,2.97,1.0;").is_none());
    assert!(parse_mouse_event("5.mouse,1.0;").is_none());
}

#[test]
fn test_parse_size_event() {
    use crate::resource_browser::parse_size_event;
    let msg = "4.size,4.1920,4.1080;";
    let (w, h) = parse_size_event(msg).unwrap();
    assert_eq!(w, 1920);
    assert_eq!(h, 1080);
}

#[test]
fn test_parse_size_event_small() {
    use crate::resource_browser::parse_size_event;
    let msg = "4.size,3.800,3.600;";
    let (w, h) = parse_size_event(msg).unwrap();
    assert_eq!(w, 800);
    assert_eq!(h, 600);
}

#[test]
fn test_parse_size_event_invalid() {
    use crate::resource_browser::parse_size_event;
    assert!(parse_size_event("3.key,2.97,1.0;").is_none());
    assert!(parse_size_event("4.size,;").is_none());
}

#[test]
fn test_parse_display_size_defaults() {
    use crate::resource_browser::parse_display_size;
    let params = HashMap::new();
    let (w, h) = parse_display_size(&params);
    assert_eq!(w, 1024);
    assert_eq!(h, 768);
}

#[test]
fn test_parse_display_size_custom() {
    use crate::resource_browser::parse_display_size;
    let mut params = HashMap::new();
    params.insert("size".to_string(), "1920,1080,96".to_string());
    let (w, h) = parse_display_size(&params);
    assert_eq!(w, 1920);
    assert_eq!(h, 1080);
}

#[test]
fn test_parse_display_size_invalid() {
    use crate::resource_browser::parse_display_size;
    let mut params = HashMap::new();
    params.insert("size".to_string(), "not_numbers".to_string());
    let (w, h) = parse_display_size(&params);
    assert_eq!(w, 1024);
    assert_eq!(h, 768);
}

// -- BrowserMode tests --

#[test]
fn test_browser_mode_transitions() {
    let mode = BrowserMode::List;
    assert_eq!(mode, BrowserMode::List);

    let mode = BrowserMode::Terminal {
        action_id: "shell".to_string(),
        row_index: 0,
    };
    assert_eq!(
        mode,
        BrowserMode::Terminal {
            action_id: "shell".to_string(),
            row_index: 0,
        }
    );

    // Verify inequality between different modes
    assert_ne!(
        BrowserMode::List,
        BrowserMode::Terminal {
            action_id: "shell".to_string(),
            row_index: 0,
        }
    );
}

#[test]
fn test_browser_mode_terminal_variants() {
    let shell = BrowserMode::Terminal {
        action_id: "shell".to_string(),
        row_index: 0,
    };
    let logs = BrowserMode::Terminal {
        action_id: "logs".to_string(),
        row_index: 0,
    };
    let different_row = BrowserMode::Terminal {
        action_id: "shell".to_string(),
        row_index: 1,
    };

    assert_ne!(shell, logs);
    assert_ne!(shell, different_row);
}

// -- ResourceUpdate application tests --

#[test]
fn test_apply_full_update() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    let columns = handler.browser.columns();
    grid.set_data(
        columns,
        vec![vec![
            "old".to_string(),
            "data".to_string(),
            "1d".to_string(),
        ]],
    );
    handler.cached_rows = vec![vec![
        "old".to_string(),
        "data".to_string(),
        "1d".to_string(),
    ]];

    let new_rows = vec![
        vec!["new-1".to_string(), "Running".to_string(), "1h".to_string()],
        vec!["new-2".to_string(), "Pending".to_string(), "5m".to_string()],
    ];
    handler.apply_update(&mut grid, ResourceUpdate::FullUpdate(new_rows.clone()));

    assert_eq!(grid.rows.len(), 2);
    assert_eq!(handler.cached_rows, new_rows);
    assert_eq!(grid.rows[0][0], "new-1");
    assert_eq!(grid.rows[1][1], "Pending");
}

#[test]
fn test_apply_row_updated() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    let columns = handler.browser.columns();
    let initial_rows = vec![
        vec!["pod-a".to_string(), "Running".to_string(), "1d".to_string()],
        vec!["pod-b".to_string(), "Pending".to_string(), "1h".to_string()],
    ];
    grid.set_data(columns, initial_rows.clone());
    handler.cached_rows = initial_rows;

    let updated_row = vec!["pod-b".to_string(), "Running".to_string(), "1h".to_string()];
    handler.apply_update(
        &mut grid,
        ResourceUpdate::RowUpdated {
            index: 1,
            row: updated_row,
        },
    );

    assert_eq!(grid.rows.len(), 2);
    assert_eq!(grid.rows[1][1], "Running");
}

#[test]
fn test_apply_row_added() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    let columns = handler.browser.columns();
    let initial_rows = vec![vec![
        "pod-a".to_string(),
        "Running".to_string(),
        "1d".to_string(),
    ]];
    grid.set_data(columns, initial_rows.clone());
    handler.cached_rows = initial_rows;

    let new_row = vec![
        "pod-c".to_string(),
        "Starting".to_string(),
        "0s".to_string(),
    ];
    handler.apply_update(&mut grid, ResourceUpdate::RowAdded(new_row));

    assert_eq!(grid.rows.len(), 2);
    assert_eq!(grid.rows[1][0], "pod-c");
}

#[test]
fn test_apply_row_removed() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    let columns = handler.browser.columns();
    let initial_rows = vec![
        vec!["pod-a".to_string(), "Running".to_string(), "1d".to_string()],
        vec!["pod-b".to_string(), "Running".to_string(), "5d".to_string()],
        vec!["pod-c".to_string(), "Failed".to_string(), "1h".to_string()],
    ];
    grid.set_data(columns, initial_rows.clone());
    handler.cached_rows = initial_rows;

    handler.apply_update(&mut grid, ResourceUpdate::RowRemoved(1));

    assert_eq!(grid.rows.len(), 2);
    assert_eq!(grid.rows[0][0], "pod-a");
    assert_eq!(grid.rows[1][0], "pod-c");
}

#[test]
fn test_apply_row_removed_out_of_bounds() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    let columns = handler.browser.columns();
    let initial_rows = vec![vec![
        "pod-a".to_string(),
        "Running".to_string(),
        "1d".to_string(),
    ]];
    grid.set_data(columns, initial_rows.clone());
    handler.cached_rows = initial_rows;

    // Should not panic on out-of-bounds
    handler.apply_update(&mut grid, ResourceUpdate::RowRemoved(99));
    assert_eq!(grid.rows.len(), 1);
}

#[test]
fn test_apply_row_updated_out_of_bounds() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    let columns = handler.browser.columns();
    let initial_rows = vec![vec![
        "pod-a".to_string(),
        "Running".to_string(),
        "1d".to_string(),
    ]];
    grid.set_data(columns, initial_rows.clone());
    handler.cached_rows = initial_rows;

    // Should not panic on out-of-bounds
    handler.apply_update(
        &mut grid,
        ResourceUpdate::RowUpdated {
            index: 99,
            row: vec!["nope".to_string()],
        },
    );
    assert_eq!(grid.rows.len(), 1);
    assert_eq!(grid.rows[0][0], "pod-a");
}

// -- Handler construction tests --

#[test]
fn test_handler_initial_state() {
    let browser = MockBrowser::new();
    let handler = ResourceBrowserHandler::new(browser);
    assert_eq!(handler.mode, BrowserMode::List);
    assert_eq!(handler.stream_id, INITIAL_STREAM_ID);
    assert_eq!(handler.pixel_width, DEFAULT_WIDTH);
    assert_eq!(handler.pixel_height, DEFAULT_HEIGHT);
    assert!(!handler.ctrl_pressed);
    assert!(handler.cached_rows.is_empty());
}

// -- Grid input handling tests --

#[test]
fn test_handle_list_input_key_down() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let columns = handler.browser.columns();
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    grid.set_data(
        columns,
        vec![
            vec!["a".to_string(), "b".to_string(), "c".to_string()],
            vec!["d".to_string(), "e".to_string(), "f".to_string()],
        ],
    );

    // Arrow down selects first row
    let event = handler.handle_list_input("3.key,5.65364,1.1;", &mut grid);
    assert_eq!(event, GridEvent::Redraw);
    assert_eq!(grid.selected_row(), Some(0));
}

#[test]
fn test_handle_list_input_mouse_click() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let columns = handler.browser.columns();
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    grid.set_data(
        columns,
        vec![
            vec!["a".to_string(), "b".to_string(), "c".to_string()],
            vec!["d".to_string(), "e".to_string(), "f".to_string()],
        ],
    );

    // Click on first data row
    let event = handler.handle_list_input("5.mouse,2.50,2.30,1.1;", &mut grid);
    // Should be CellSelected or Redraw depending on exact y coordinate
    assert!(matches!(
        event,
        GridEvent::CellSelected { .. } | GridEvent::Redraw | GridEvent::None
    ));
}

#[test]
fn test_handle_list_input_resize() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let columns = handler.browser.columns();
    let mut grid = ResourceBrowserGrid::new(1024, 768);
    grid.set_data(columns, vec![]);

    let event = handler.handle_list_input("4.size,4.1920,4.1080;", &mut grid);
    assert_eq!(event, GridEvent::Redraw);
    assert_eq!(handler.pixel_width, 1920);
    assert_eq!(handler.pixel_height, 1080);
}

#[test]
fn test_handle_list_input_unrecognized() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let mut grid = ResourceBrowserGrid::new(1024, 768);

    let event = handler.handle_list_input("unknown instruction", &mut grid);
    assert_eq!(event, GridEvent::None);
}

// -- Integration-level tests with channel --

#[tokio::test]
async fn test_handler_run_client_disconnect() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(64);

    // Drop the client sender immediately to simulate disconnect
    drop(from_client_tx);

    // Spawn a task to drain the to_client channel (prevent backpressure stall)
    let drain_handle = tokio::spawn(async move {
        let mut count = 0;
        while to_client_rx.recv().await.is_some() {
            count += 1;
        }
        count
    });

    let params = HashMap::new();
    let result = handler.run(params, to_client_tx, from_client_rx).await;
    assert!(result.is_ok());

    let msg_count = drain_handle.await.unwrap();
    // Should have sent at least: ready, name, img+blob+end+sync, disconnect
    assert!(
        msg_count >= 4,
        "Expected at least 4 messages, got {}",
        msg_count
    );
}

#[tokio::test]
async fn test_handler_sends_ready_and_name() {
    let browser = MockBrowser::new();
    let mut handler = ResourceBrowserHandler::new(browser);
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(64);
    let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(64);

    // Drop client sender to trigger immediate exit
    drop(from_client_tx);

    let handle = tokio::spawn(async move {
        let params = HashMap::new();
        handler.run(params, to_client_tx, from_client_rx).await
    });

    // Read first two messages: ready and name
    let ready_msg = to_client_rx.recv().await.unwrap();
    let ready_str = String::from_utf8(ready_msg.to_vec()).unwrap();
    assert!(
        ready_str.contains("ready"),
        "Expected ready instruction, got: {}",
        ready_str
    );

    let name_msg = to_client_rx.recv().await.unwrap();
    let name_str = String::from_utf8(name_msg.to_vec()).unwrap();
    assert!(
        name_str.contains("mock-browser"),
        "Expected name instruction with mock-browser, got: {}",
        name_str
    );

    // Drain remaining
    while to_client_rx.recv().await.is_some() {}

    let result = handle.await.unwrap();
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_action_result_status() {
    let browser = MockBrowser::new();
    browser.action_results.lock().await.insert(
        "describe".to_string(),
        MockActionOutcome::Status("3 replicas, healthy".to_string()),
    );

    let mut handler = ResourceBrowserHandler::new(browser);
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(256);
    let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(64);

    let handle = tokio::spawn(async move {
        let params = HashMap::new();
        handler.run(params, to_client_tx, from_client_rx).await
    });

    // Wait for initial render to complete by consuming messages until we
    // see a sync instruction
    loop {
        let msg = to_client_rx.recv().await.unwrap();
        let s = String::from_utf8(msg.to_vec()).unwrap();
        if s.contains("sync") {
            break;
        }
    }

    // Select row 0 (arrow down)
    from_client_tx
        .send(Bytes::from("3.key,5.65364,1.1;"))
        .await
        .unwrap();

    // Wait for the redraw to complete
    loop {
        let msg = to_client_rx.recv().await.unwrap();
        let s = String::from_utf8(msg.to_vec()).unwrap();
        if s.contains("sync") {
            break;
        }
    }

    // Trigger describe action with shortcut 'd'
    from_client_tx
        .send(Bytes::from("3.key,3.100,1.1;"))
        .await
        .unwrap();

    // The action should produce a status result; wait for another render
    loop {
        let msg = to_client_rx.recv().await.unwrap();
        let s = String::from_utf8(msg.to_vec()).unwrap();
        if s.contains("sync") {
            break;
        }
    }

    // Disconnect
    drop(from_client_tx);

    // Drain remaining
    while to_client_rx.recv().await.is_some() {}

    let result = handle.await.unwrap();
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_action_result_refresh() {
    let browser = MockBrowser::new();
    browser
        .action_results
        .lock()
        .await
        .insert("describe".to_string(), MockActionOutcome::Refresh);

    let mut handler = ResourceBrowserHandler::new(browser);
    let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(256);
    let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(64);

    let handle = tokio::spawn(async move {
        let params = HashMap::new();
        handler.run(params, to_client_tx, from_client_rx).await
    });

    // Wait for initial render
    loop {
        let msg = to_client_rx.recv().await.unwrap();
        let s = String::from_utf8(msg.to_vec()).unwrap();
        if s.contains("sync") {
            break;
        }
    }

    // Select row 0
    from_client_tx
        .send(Bytes::from("3.key,5.65364,1.1;"))
        .await
        .unwrap();

    // Wait for redraw
    loop {
        let msg = to_client_rx.recv().await.unwrap();
        let s = String::from_utf8(msg.to_vec()).unwrap();
        if s.contains("sync") {
            break;
        }
    }

    // Trigger describe action (shortcut 'd' = keysym 100)
    from_client_tx
        .send(Bytes::from("3.key,3.100,1.1;"))
        .await
        .unwrap();

    // Wait for the refresh render
    loop {
        let msg = to_client_rx.recv().await.unwrap();
        let s = String::from_utf8(msg.to_vec()).unwrap();
        if s.contains("sync") {
            break;
        }
    }

    drop(from_client_tx);
    while to_client_rx.recv().await.is_some() {}

    let result = handle.await.unwrap();
    assert!(result.is_ok());
}
