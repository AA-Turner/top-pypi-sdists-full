// Resource browser infrastructure for infrastructure management UIs.
//
// Provides a shared dual-mode handler framework used by Kubernetes, Docker,
// and vSphere handlers. The two modes are:
//
//   1. **List mode** - Renders a resource list using ResourceBrowserGrid
//      (interactive grid with row selection, keyboard/mouse navigation, and
//      configurable per-row actions).
//
//   2. **Terminal mode** - Switches to a TerminalEmulator for interactive
//      shell/logs sessions (bidirectional byte stream forwarding).
//
// The ResourceBrowser trait defines the data provider contract.
// ResourceBrowserHandler implements the Guacamole protocol event loop,
// managing mode transitions and rendering.

use async_trait::async_trait;
use bytes::Bytes;
use guacr_protocol::{format_chunked_blobs, format_end, format_img, format_instruction};
use guacr_terminal::{
    Action, ColumnDef, GridEvent, GridMode, RatatuiRenderer, TerminalEmulator, TerminalRenderer,
    CHAR_HEIGHT, CHAR_WIDTH, JPEG_QUALITY,
};
use log::{debug, error, info, warn};
use std::collections::HashMap;
use std::pin::Pin;
use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};
use tokio::sync::mpsc;

use crate::error::HandlerError;
use crate::session::{send_disconnect, send_name, send_ready};

// -- Keysym constants for Ctrl+D detection in terminal mode --
const KEYSYM_CTRL_L: u32 = 0xFFE3;
const KEYSYM_D_LOWER: u32 = 0x0064;

// -- Stream ID starts at 1 (stream 0 is reserved in Guacamole protocol) --
pub(crate) const INITIAL_STREAM_ID: u32 = 1;

// -- Default display dimensions --
pub(crate) const DEFAULT_WIDTH: u32 = 1024;
pub(crate) const DEFAULT_HEIGHT: u32 = 768;

/// Result of executing an action on a resource row.
pub enum ActionResult {
    /// Opens terminal mode with bidirectional stream.
    ///
    /// The reader provides output from the remote process (shell stdout, log
    /// stream, console output). The writer accepts input to the remote process
    /// (shell stdin, etc.).
    Terminal {
        reader: Box<dyn AsyncRead + Send + Unpin>,
        writer: Box<dyn AsyncWrite + Send + Unpin>,
    },

    /// One-shot result displayed as a status message in the grid's status area.
    /// The handler will briefly show this message and then return to list mode.
    Status(String),

    /// Refresh the list view by re-fetching resources.
    Refresh,
}

/// Streaming updates for the resource list (used by watch/event APIs).
#[derive(Debug, Clone)]
pub enum ResourceUpdate {
    /// Full replacement of all rows.
    FullUpdate(Vec<Vec<String>>),

    /// Single row changed at the given index.
    RowUpdated { index: usize, row: Vec<String> },

    /// Row added at the end of the list.
    RowAdded(Vec<String>),

    /// Row removed at the given index.
    RowRemoved(usize),
}

/// Data provider trait for infrastructure resource browsers.
///
/// Implementors provide column definitions, resource listing, per-row actions,
/// and optional streaming updates. The ResourceBrowserHandler drives the UI
/// loop and calls these methods as needed.
#[async_trait]
pub trait ResourceBrowser: Send + Sync {
    /// Column definitions for the spreadsheet header.
    fn columns(&self) -> Vec<ColumnDef>;

    /// Fetch the current resource list.
    ///
    /// Each inner `Vec<String>` is a row of cell values matching the columns.
    async fn list_resources(&self) -> Result<Vec<Vec<String>>, String>;

    /// Available actions for the given row index.
    ///
    /// Called whenever the user selects a row to determine what actions
    /// to display in the action bar (e.g., Shell, Logs, Describe, Delete).
    fn row_actions(&self, row_index: usize) -> Vec<Action>;

    /// Execute an action on a specific row.
    ///
    /// The `action_id` matches the `Action::id` field returned by `row_actions`.
    async fn execute_action(
        &self,
        row_index: usize,
        action_id: &str,
    ) -> Result<ActionResult, String>;

    /// Optional: stream resource updates for real-time refresh.
    ///
    /// If the underlying API supports watch/event streaming (e.g., Kubernetes
    /// watch API, Docker events), return a pinned Stream of ResourceUpdate.
    /// The handler will apply updates incrementally to the grid.
    ///
    /// Default implementation returns None (polling only via manual refresh).
    async fn watch_resources(
        &self,
    ) -> Option<Pin<Box<dyn futures_core::Stream<Item = ResourceUpdate> + Send>>> {
        None
    }

    /// Handler name for display in the connection title bar.
    fn name(&self) -> &str;
}

/// UI mode state machine for the resource browser.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BrowserMode {
    /// List view showing resources in ResourceBrowserGrid.
    List,

    /// Terminal mode (shell exec, logs, console).
    /// Stores which action/row initiated this mode for display purposes.
    Terminal { action_id: String, row_index: usize },
}

// -- ResourceBrowserGrid: ratatui-based replacement for ResourceBrowserGrid --

pub(crate) struct ResourceBrowserGrid {
    pub(crate) renderer: RatatuiRenderer,
    pub(crate) columns: Vec<ColumnDef>,
    pub(crate) rows: Vec<Vec<String>>,
    pub(crate) actions: Vec<Action>,
    pub(crate) table_state: ratatui::widgets::TableState,
    pub(crate) focused_action: usize,
    pub(crate) mode: GridMode,
    pub(crate) dirty: bool,
}

impl ResourceBrowserGrid {
    pub(crate) fn new(pixel_width: u32, pixel_height: u32) -> Self {
        let cols = (pixel_width / CHAR_WIDTH).max(80) as u16;
        let rows = (pixel_height / CHAR_HEIGHT).max(24) as u16;
        Self {
            renderer: RatatuiRenderer::new(cols, rows, CHAR_WIDTH, CHAR_HEIGHT)
                .expect("embedded fonts must load"),
            columns: Vec::new(),
            rows: Vec::new(),
            actions: Vec::new(),
            table_state: ratatui::widgets::TableState::default(),
            focused_action: 0,
            mode: GridMode::Browse,
            dirty: true,
        }
    }

    pub(crate) fn set_data(&mut self, columns: Vec<ColumnDef>, rows: Vec<Vec<String>>) {
        self.columns = columns;
        self.rows = rows;
        self.table_state = ratatui::widgets::TableState::default();
        self.dirty = true;
    }

    pub(crate) fn update_rows(&mut self, rows: Vec<Vec<String>>) {
        self.rows = rows;
        self.dirty = true;
    }

    pub(crate) fn set_actions(&mut self, actions: Vec<Action>) {
        self.actions = actions;
        self.focused_action = 0;
        self.dirty = true;
    }

    pub(crate) fn selected_row(&self) -> Option<usize> {
        self.table_state.selected()
    }

    pub(crate) fn is_dirty(&self) -> bool {
        self.dirty
    }

    pub(crate) fn clear_dirty(&mut self) {
        self.dirty = false;
    }

    pub(crate) fn resize(&mut self, pixel_width: u32, pixel_height: u32) {
        let cols = (pixel_width / CHAR_WIDTH).max(80) as u16;
        let rows = (pixel_height / CHAR_HEIGHT).max(24) as u16;
        let _ = self.renderer.resize(cols, rows);
        self.dirty = true;
    }

    fn handle_key(&mut self, keysym: u32, pressed: bool) -> GridEvent {
        if !pressed {
            return GridEvent::None;
        }

        // Shortcut key: check if any action has a matching shortcut
        if let Some(c) = char::from_u32(keysym) {
            let c_lower = c.to_lowercase().next().unwrap_or(c);
            for action in &self.actions {
                if action.shortcut.map(|s| s == c_lower) == Some(true) {
                    if let Some(row) = self.table_state.selected() {
                        let action_id = action.id.clone();
                        self.mode = GridMode::Browse;
                        return GridEvent::ActionTriggered { row, action_id };
                    }
                }
            }
        }

        match self.mode {
            GridMode::Browse => match keysym {
                0xFF52 => {
                    self.move_selection(-1);
                    GridEvent::Redraw
                }
                0xFF54 => {
                    self.move_selection(1);
                    GridEvent::Redraw
                }
                0xFF55 => {
                    self.move_selection(-10);
                    GridEvent::Redraw
                }
                0xFF56 => {
                    self.move_selection(10);
                    GridEvent::Redraw
                }
                0xFF50 => {
                    self.select_first();
                    GridEvent::Redraw
                }
                0xFF57 => {
                    self.select_last();
                    GridEvent::Redraw
                }
                0xFF09 if !self.actions.is_empty() => {
                    self.mode = GridMode::ActionBar;
                    self.focused_action = 0;
                    GridEvent::Redraw
                }
                0xFF0D if !self.actions.is_empty() => {
                    // Enter with actions available: open action bar
                    self.mode = GridMode::ActionBar;
                    self.focused_action = 0;
                    GridEvent::Redraw
                }
                _ => GridEvent::None,
            },
            GridMode::ActionBar => match keysym {
                0xFF1B => {
                    self.mode = GridMode::Browse;
                    GridEvent::Redraw
                }
                0xFF09 => {
                    self.focused_action = (self.focused_action + 1) % self.actions.len().max(1);
                    GridEvent::Redraw
                }
                0xFF0D => {
                    if let (Some(row), Some(action)) = (
                        self.table_state.selected(),
                        self.actions.get(self.focused_action),
                    ) {
                        let action_id = action.id.clone();
                        self.mode = GridMode::Browse;
                        GridEvent::ActionTriggered { row, action_id }
                    } else {
                        GridEvent::None
                    }
                }
                _ => GridEvent::None,
            },
        }
    }

    fn handle_mouse(&mut self, _x: u32, y: u32, button_mask: u32) -> GridEvent {
        let left_click = (button_mask & 1) != 0;
        if !left_click {
            return GridEvent::None;
        }

        // Table header: row 0 = top border, row 1 = header.
        // Data rows start at ratatui row 2 → pixel 2 * CHAR_HEIGHT.
        let header_px = 2 * CHAR_HEIGHT;
        if y < header_px {
            return GridEvent::None;
        }

        let data_row = ((y - header_px) / CHAR_HEIGHT) as usize;
        let abs_row = data_row + self.table_state.offset();
        if abs_row < self.rows.len() {
            self.table_state.select(Some(abs_row));
            self.dirty = true;
            return GridEvent::CellSelected {
                row: abs_row,
                col: 0,
                value: String::new(),
            };
        }
        GridEvent::None
    }

    pub(crate) fn render_jpeg(
        &mut self,
        quality: u8,
    ) -> Result<Vec<u8>, guacr_terminal::TerminalError> {
        use ratatui::{
            layout::{Constraint, Direction, Layout},
            style::{Color, Modifier, Style},
            text::{Line, Span},
            widgets::{Block, Borders, Cell, Paragraph, Row, Table},
        };

        let columns = &self.columns;
        let rows = &self.rows;
        let actions = &self.actions;
        let mode = self.mode;
        let focused_action = self.focused_action;
        let mut table_state = self.table_state.clone();

        self.renderer
            .terminal
            .draw(|f| {
                let area = f.area();

                let (table_area, action_area) = if actions.is_empty() {
                    (area, None)
                } else {
                    let chunks = Layout::default()
                        .direction(Direction::Vertical)
                        .constraints([Constraint::Min(3), Constraint::Length(3)])
                        .split(area);
                    (chunks[0], Some(chunks[1]))
                };

                // Build header row
                let header = Row::new(
                    columns
                        .iter()
                        .map(|c| {
                            Cell::from(c.name.clone()).style(
                                Style::default()
                                    .fg(Color::LightCyan)
                                    .add_modifier(Modifier::BOLD),
                            )
                        })
                        .collect::<Vec<_>>(),
                )
                .height(1);

                // Build data rows
                let data_rows: Vec<Row> = rows
                    .iter()
                    .map(|row| {
                        Row::new(
                            row.iter()
                                .map(|v| Cell::from(v.clone()))
                                .collect::<Vec<_>>(),
                        )
                        .height(1)
                    })
                    .collect();

                // Column constraints: explicit width if provided, else equal share
                let col_count = columns.len().max(1) as u32;
                let col_constraints: Vec<Constraint> = columns
                    .iter()
                    .map(|c| {
                        if c.width_chars > 0 {
                            Constraint::Length(c.width_chars as u16)
                        } else {
                            Constraint::Ratio(1, col_count)
                        }
                    })
                    .collect();

                let table = Table::new(data_rows, col_constraints)
                    .header(header)
                    .block(Block::default().borders(Borders::ALL).title("Resources"))
                    .row_highlight_style(Style::default().add_modifier(Modifier::REVERSED));

                f.render_stateful_widget(table, table_area, &mut table_state);

                // Action bar
                if let Some(action_area) = action_area {
                    let spans: Vec<Span> = actions
                        .iter()
                        .enumerate()
                        .map(|(i, a)| {
                            let label = if let Some(sc) = a.shortcut {
                                format!(" [{}]{} ", sc.to_uppercase().next().unwrap_or(sc), a.label)
                            } else {
                                format!(" {} ", a.label)
                            };
                            let style = if mode == GridMode::ActionBar && i == focused_action {
                                Style::default().add_modifier(Modifier::REVERSED)
                            } else {
                                Style::default().fg(Color::Yellow)
                            };
                            Span::styled(label, style)
                        })
                        .collect();

                    let para = Paragraph::new(Line::from(spans))
                        .block(Block::default().borders(Borders::ALL).title("Actions"));
                    f.render_widget(para, action_area);
                }
            })
            .map_err(|e| guacr_terminal::TerminalError::RenderError(e.to_string()))?;

        self.table_state = table_state;
        self.renderer.render_to_jpeg(quality)
    }

    fn move_selection(&mut self, delta: i32) {
        if self.rows.is_empty() {
            return;
        }
        let next = if let Some(current) = self.table_state.selected() {
            (current as i32 + delta).clamp(0, self.rows.len() as i32 - 1) as usize
        } else {
            // Nothing selected: Down → first row, Up → last row
            if delta > 0 {
                0
            } else {
                self.rows.len() - 1
            }
        };
        self.table_state.select(Some(next));
        self.dirty = true;
    }

    fn select_first(&mut self) {
        if !self.rows.is_empty() {
            self.table_state.select(Some(0));
            self.dirty = true;
        }
    }

    fn select_last(&mut self) {
        if !self.rows.is_empty() {
            self.table_state.select(Some(self.rows.len() - 1));
            self.dirty = true;
        }
    }
}

/// Shared handler loop for infrastructure management UIs.
///
/// Wraps a ResourceBrowser implementation and drives the dual-mode Guacamole
/// protocol event loop. This is called from a ProtocolHandler::connect()
/// implementation.
///
/// # Usage
///
/// ```ignore
/// use guacr_handlers::resource_browser::{ResourceBrowserHandler, ResourceBrowser};
///
/// struct K8sHandler { /* ... */ }
///
/// #[async_trait]
/// impl ProtocolHandler for K8sHandler {
///     fn name(&self) -> &str { "kubernetes" }
///
///     async fn connect(
///         &self,
///         params: HashMap<String, String>,
///         to_client: mpsc::Sender<Bytes>,
///         from_client: mpsc::Receiver<Bytes>,
///     ) -> Result<()> {
///         let browser = K8sBrowser::new(&params)?;
///         let mut handler = ResourceBrowserHandler::new(browser);
///         handler.run(params, to_client, from_client).await
///     }
/// }
/// ```
pub struct ResourceBrowserHandler<B: ResourceBrowser> {
    pub(crate) browser: B,
    pub(crate) mode: BrowserMode,
    pub(crate) stream_id: u32,
    pub(crate) pixel_width: u32,
    pub(crate) pixel_height: u32,
    pub(crate) ctrl_pressed: bool,
    pub(crate) cached_rows: Vec<Vec<String>>,
}

impl<B: ResourceBrowser> ResourceBrowserHandler<B> {
    /// Create a new ResourceBrowserHandler wrapping the given browser.
    pub fn new(browser: B) -> Self {
        Self {
            browser,
            mode: BrowserMode::List,
            stream_id: INITIAL_STREAM_ID,
            pixel_width: DEFAULT_WIDTH,
            pixel_height: DEFAULT_HEIGHT,
            ctrl_pressed: false,
            cached_rows: Vec::new(),
        }
    }

    /// Run the handler loop.
    ///
    /// This is called from ProtocolHandler::connect(). It manages the full
    /// lifecycle: initial render, event loop, mode transitions, and cleanup.
    pub async fn run(
        &mut self,
        params: HashMap<String, String>,
        to_client: mpsc::Sender<Bytes>,
        mut from_client: mpsc::Receiver<Bytes>,
    ) -> Result<(), HandlerError> {
        // Parse display dimensions from connection params
        let (width, height) = parse_display_size(&params);
        self.pixel_width = width;
        self.pixel_height = height;

        // Send session startup instructions
        let connection_id = format!("{}-browser", self.browser.name());
        send_ready(&to_client, &connection_id).await?;
        send_name(&to_client, self.browser.name()).await?;

        // Initialize ResourceBrowserGrid
        let mut grid = ResourceBrowserGrid::new(self.pixel_width, self.pixel_height);
        let columns = self.browser.columns();

        // Fetch initial resource list
        let rows = self.browser.list_resources().await.map_err(|e| {
            HandlerError::ConnectionFailed(format!("Failed to list resources: {}", e))
        })?;
        self.cached_rows = rows.clone();

        grid.set_data(columns, rows);

        // Set initial actions (empty until a row is selected)
        // Actions will be set when the user selects a row.

        // Initial render
        self.render_grid(&mut grid, &to_client).await?;
        grid.clear_dirty();

        // Spawn optional watch task
        let (watch_tx, mut watch_rx) = mpsc::channel::<ResourceUpdate>(64);
        let watch_handle = self.spawn_watch_task(watch_tx).await;

        // Event loop
        loop {
            match &self.mode {
                BrowserMode::List => {
                    tokio::select! {
                        msg = from_client.recv() => {
                            let Some(msg) = msg else {
                                debug!("{}: Client disconnected", self.browser.name());
                                break;
                            };

                            let msg_str = match std::str::from_utf8(&msg) {
                                Ok(s) => s,
                                Err(_) => continue,
                            };

                            let event = self.handle_list_input(msg_str, &mut grid);

                            match event {
                                GridEvent::ActionTriggered { row, action_id } => {
                                    info!(
                                        "{}: Action '{}' triggered on row {}",
                                        self.browser.name(), action_id, row
                                    );

                                    match self.browser.execute_action(row, &action_id).await {
                                        Ok(ActionResult::Terminal { reader, writer }) => {
                                            self.mode = BrowserMode::Terminal {
                                                action_id: action_id.clone(),
                                                row_index: row,
                                            };

                                            // Run terminal mode inline (it will
                                            // return when the user exits with Ctrl+D
                                            // or the stream ends)
                                            self.run_terminal_mode(
                                                reader,
                                                writer,
                                                &to_client,
                                                &mut from_client,
                                            )
                                            .await?;

                                            // Back to list mode: refresh data
                                            self.mode = BrowserMode::List;
                                            self.refresh_list(&mut grid).await?;
                                            self.render_grid(&mut grid, &to_client).await?;
                                            grid.clear_dirty();
                                        }
                                        Ok(ActionResult::Status(message)) => {
                                            info!("{}: Status: {}", self.browser.name(), message);
                                            // Re-render with updated status (the grid
                                            // will show status in the status line area)
                                            self.render_grid(&mut grid, &to_client).await?;
                                            grid.clear_dirty();
                                        }
                                        Ok(ActionResult::Refresh) => {
                                            self.refresh_list(&mut grid).await?;
                                            self.render_grid(&mut grid, &to_client).await?;
                                            grid.clear_dirty();
                                        }
                                        Err(e) => {
                                            warn!(
                                                "{}: Action '{}' failed: {}",
                                                self.browser.name(), action_id, e
                                            );
                                            // Stay in list mode, re-render
                                            self.render_grid(&mut grid, &to_client).await?;
                                            grid.clear_dirty();
                                        }
                                    }
                                }
                                GridEvent::Redraw => {
                                    // Update actions based on current selection
                                    if let Some(sel) = grid.selected_row() {
                                        let actions = self.browser.row_actions(sel);
                                        grid.set_actions(actions);
                                    }
                                    self.render_grid(&mut grid, &to_client).await?;
                                    grid.clear_dirty();
                                }
                                GridEvent::CellSelected { row, .. } => {
                                    // Update actions for newly selected row
                                    let actions = self.browser.row_actions(row);
                                    grid.set_actions(actions);
                                    self.render_grid(&mut grid, &to_client).await?;
                                    grid.clear_dirty();
                                }
                                GridEvent::None => {
                                    // No visual change needed
                                }
                            }
                        }

                        update = watch_rx.recv() => {
                            if let Some(update) = update {
                                self.apply_update(&mut grid, update);
                                if grid.is_dirty() {
                                    self.render_grid(&mut grid, &to_client).await?;
                                    grid.clear_dirty();
                                }
                            }
                        }
                    }
                }
                BrowserMode::Terminal { .. } => {
                    // Terminal mode is handled inline in the ActionTriggered
                    // branch above. If we somehow reach here, break.
                    error!(
                        "{}: Unexpected terminal mode in main loop",
                        self.browser.name()
                    );
                    break;
                }
            }
        }

        // Cleanup
        if let Some(handle) = watch_handle {
            handle.abort();
        }
        send_disconnect(&to_client).await;
        Ok(())
    }

    /// Handle a Guacamole instruction in list mode, returning the grid event.
    pub(crate) fn handle_list_input(
        &mut self,
        msg_str: &str,
        grid: &mut ResourceBrowserGrid,
    ) -> GridEvent {
        // Handle key instruction
        if msg_str.contains(".key,") {
            if let Some(key) = parse_key_event(msg_str) {
                return grid.handle_key(key.keysym, key.pressed);
            }
        }

        // Handle mouse instruction
        if msg_str.contains(".mouse,") {
            if let Some(mouse) = parse_mouse_event(msg_str) {
                return grid.handle_mouse(mouse.x, mouse.y, mouse.button_mask);
            }
        }

        // Handle size instruction (resize)
        if msg_str.contains(".size,") {
            if let Some((w, h)) = parse_size_event(msg_str) {
                if w > 0 && h > 0 {
                    self.pixel_width = w;
                    self.pixel_height = h;
                    grid.resize(w, h);
                    return GridEvent::Redraw;
                }
            }
        }

        GridEvent::None
    }

    /// Run terminal mode: forward I/O between the Guacamole client and a
    /// bidirectional byte stream (shell, log tail, etc.).
    ///
    /// Returns when the stream ends or the user presses Ctrl+D.
    async fn run_terminal_mode(
        &mut self,
        mut reader: Box<dyn AsyncRead + Send + Unpin>,
        mut writer: Box<dyn AsyncWrite + Send + Unpin>,
        to_client: &mpsc::Sender<Bytes>,
        from_client: &mut mpsc::Receiver<Bytes>,
    ) -> Result<(), HandlerError> {
        // Set up terminal emulator for rendering shell output
        let cols = (self.pixel_width / CHAR_WIDTH).max(80) as u16;
        let rows = (self.pixel_height / CHAR_HEIGHT).max(24) as u16;
        let mut terminal = TerminalEmulator::new(rows, cols);
        let renderer = TerminalRenderer::new()
            .map_err(|e| HandlerError::ProtocolError(format!("Terminal renderer init: {}", e)))?;

        // Show initial empty terminal
        let jpeg = renderer
            .render_screen(terminal.screen(), rows, cols)
            .map_err(|e| HandlerError::ProtocolError(format!("Render error: {}", e)))?;
        self.send_jpeg_frame(&jpeg, 0, 0, to_client).await?;
        self.send_sync(to_client).await?;

        self.ctrl_pressed = false;
        let mut read_buf = [0u8; 4096];

        loop {
            tokio::select! {
                // Data from the remote process (stdout/logs)
                n = reader.read(&mut read_buf) => {
                    match n {
                        Ok(0) => {
                            debug!("{}: Terminal stream ended (EOF)", self.browser.name());
                            break;
                        }
                        Ok(n) => {
                            terminal.process(&read_buf[..n]).map_err(|e| {
                                HandlerError::ProtocolError(format!("Terminal process: {}", e))
                            })?;

                            let jpeg = renderer
                                .render_screen(terminal.screen(), rows, cols)
                                .map_err(|e| {
                                    HandlerError::ProtocolError(format!("Render error: {}", e))
                                })?;
                            self.send_jpeg_frame(&jpeg, 0, 0, to_client).await?;
                            self.send_sync(to_client).await?;
                        }
                        Err(e) => {
                            warn!("{}: Terminal read error: {}", self.browser.name(), e);
                            break;
                        }
                    }
                }

                // Input from the Guacamole client (keyboard/mouse)
                msg = from_client.recv() => {
                    let Some(msg) = msg else {
                        debug!("{}: Client disconnected during terminal mode", self.browser.name());
                        break;
                    };

                    let msg_str = match std::str::from_utf8(&msg) {
                        Ok(s) => s,
                        Err(_) => continue,
                    };

                    // Check for Ctrl+D to exit terminal mode
                    if msg_str.contains(".key,") {
                        if let Some(key) = parse_key_event(msg_str) {
                            // Track Ctrl state
                            if key.keysym == KEYSYM_CTRL_L {
                                self.ctrl_pressed = key.pressed;
                                continue;
                            }

                            // Ctrl+D on key-down exits terminal mode
                            if key.pressed && key.keysym == KEYSYM_D_LOWER && self.ctrl_pressed {
                                info!("{}: Ctrl+D detected, exiting terminal mode", self.browser.name());
                                break;
                            }

                            // Forward key press as terminal input
                            if key.pressed {
                                let bytes = guacr_terminal::x11_keysym_to_bytes(key.keysym, true, None);
                                if !bytes.is_empty() {
                                    if let Err(e) = writer.write_all(&bytes).await {
                                        warn!("{}: Terminal write error: {}", self.browser.name(), e);
                                        break;
                                    }
                                }
                            }
                        }
                    }

                    // Handle size changes in terminal mode
                    if msg_str.contains(".size,") {
                        if let Some((w, h)) = parse_size_event(msg_str) {
                            if w > 0 && h > 0 {
                                self.pixel_width = w;
                                self.pixel_height = h;
                                let new_cols = (w / CHAR_WIDTH).max(80) as u16;
                                let new_rows = (h / CHAR_HEIGHT).max(24) as u16;
                                terminal.resize(new_rows, new_cols);

                                let jpeg = renderer
                                    .render_screen(terminal.screen(), new_rows, new_cols)
                                    .map_err(|e| {
                                        HandlerError::ProtocolError(format!("Render error: {}", e))
                                    })?;
                                self.send_jpeg_frame(&jpeg, 0, 0, to_client).await?;
                                self.send_sync(to_client).await?;
                            }
                        }
                    }
                }
            }
        }

        // Attempt graceful shutdown of the writer side
        let _ = writer.shutdown().await;

        Ok(())
    }

    /// Refresh the resource list and update the grid.
    async fn refresh_list(&mut self, grid: &mut ResourceBrowserGrid) -> Result<(), HandlerError> {
        match self.browser.list_resources().await {
            Ok(rows) => {
                self.cached_rows = rows.clone();
                grid.update_rows(rows);

                // Refresh actions for the current selection
                if let Some(sel) = grid.selected_row() {
                    let actions = self.browser.row_actions(sel);
                    grid.set_actions(actions);
                }

                Ok(())
            }
            Err(e) => {
                warn!(
                    "{}: Failed to refresh resources: {}",
                    self.browser.name(),
                    e
                );
                // Keep existing data, just log the error
                Ok(())
            }
        }
    }

    /// Apply a streaming ResourceUpdate to the grid.
    pub(crate) fn apply_update(&mut self, grid: &mut ResourceBrowserGrid, update: ResourceUpdate) {
        match update {
            ResourceUpdate::FullUpdate(rows) => {
                self.cached_rows = rows.clone();
                grid.update_rows(rows);
            }
            ResourceUpdate::RowUpdated { index, row } => {
                if index < self.cached_rows.len() {
                    self.cached_rows[index] = row;
                    grid.update_rows(self.cached_rows.clone());
                }
            }
            ResourceUpdate::RowAdded(row) => {
                self.cached_rows.push(row);
                grid.update_rows(self.cached_rows.clone());
            }
            ResourceUpdate::RowRemoved(index) => {
                if index < self.cached_rows.len() {
                    self.cached_rows.remove(index);
                    grid.update_rows(self.cached_rows.clone());
                }
            }
        }

        // Refresh actions for the current selection after update
        if let Some(sel) = grid.selected_row() {
            if sel < self.cached_rows.len() {
                let actions = self.browser.row_actions(sel);
                grid.set_actions(actions);
            }
        }
    }

    /// Spawn an optional background task that receives watch updates.
    ///
    /// If the browser supports watch_resources(), spawn a task that forwards
    /// updates into the given channel. Returns the JoinHandle for cleanup.
    async fn spawn_watch_task(
        &self,
        watch_tx: mpsc::Sender<ResourceUpdate>,
    ) -> Option<tokio::task::JoinHandle<()>> {
        use futures_core::Stream;
        use std::task::Context;

        let stream_opt = self.browser.watch_resources().await;
        let mut stream = stream_opt?;

        let name = self.browser.name().to_string();
        Some(tokio::spawn(async move {
            // Poll the stream manually using a simple loop.
            // We wrap in a poll_fn to drive the pinned stream.
            loop {
                // Use poll_fn to drive the stream
                let next = std::future::poll_fn(|cx: &mut Context<'_>| {
                    Pin::new(&mut stream).poll_next(cx)
                })
                .await;

                match next {
                    Some(update) => {
                        if watch_tx.send(update).await.is_err() {
                            debug!("{}: Watch channel closed, stopping watcher", name);
                            break;
                        }
                    }
                    None => {
                        debug!("{}: Watch stream ended", name);
                        break;
                    }
                }
            }
        }))
    }

    /// Render the ResourceBrowserGrid grid and send as a Guacamole image frame.
    ///
    /// Takes `&mut ResourceBrowserGrid` (not `&`) so the future remains Send.
    /// ResourceBrowserGrid internally uses RefCell for its glyph cache, which
    /// makes &ResourceBrowserGrid !Send. Using &mut avoids this issue.
    async fn render_grid(
        &mut self,
        grid: &mut ResourceBrowserGrid,
        to_client: &mpsc::Sender<Bytes>,
    ) -> Result<(), HandlerError> {
        let jpeg_data = grid
            .render_jpeg(JPEG_QUALITY)
            .map_err(|e| HandlerError::ProtocolError(format!("Grid render error: {}", e)))?;

        self.send_jpeg_frame(&jpeg_data, 0, 0, to_client).await?;
        self.send_sync(to_client).await?;
        Ok(())
    }

    /// Send a JPEG image frame via the modern img + blob + end protocol.
    async fn send_jpeg_frame(
        &mut self,
        jpeg_data: &[u8],
        x: i32,
        y: i32,
        to_client: &mpsc::Sender<Bytes>,
    ) -> Result<(), HandlerError> {
        let base64_data =
            base64::Engine::encode(&base64::engine::general_purpose::STANDARD, jpeg_data);

        // img instruction: start image stream
        let img_instr = format_img(self.stream_id, 14, 0, "image/jpeg", x, y);
        to_client
            .send(Bytes::from(img_instr))
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;

        // blob instructions: chunked base64 data
        let blob_instructions = format_chunked_blobs(self.stream_id, &base64_data, None);
        for blob_instr in blob_instructions {
            to_client
                .send(Bytes::from(blob_instr))
                .await
                .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
        }

        // end instruction: close the stream
        let end_instr = format_end(self.stream_id);
        to_client
            .send(Bytes::from(end_instr))
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;

        // Increment stream ID for next frame (stream 0 is reserved)
        self.stream_id += 1;

        Ok(())
    }

    /// Send a sync instruction to signal frame completion.
    async fn send_sync(&self, to_client: &mpsc::Sender<Bytes>) -> Result<(), HandlerError> {
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis();
        let timestamp_str = timestamp.to_string();
        let sync_instr = format_instruction("sync", &[&timestamp_str]);
        to_client
            .send(Bytes::from(sync_instr))
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))
    }
}

// -- Guacamole instruction parsing helpers --

/// Parsed key event from Guacamole "key" instruction.
pub(crate) struct KeyEventParsed {
    pub(crate) keysym: u32,
    pub(crate) pressed: bool,
}

/// Parsed mouse event from Guacamole "mouse" instruction.
pub(crate) struct MouseEventParsed {
    pub(crate) x: u32,
    pub(crate) y: u32,
    pub(crate) button_mask: u32,
}

/// Parse a Guacamole key instruction.
///
/// Format: `3.key,{keysym_len}.{keysym},{pressed_len}.{pressed};`
pub(crate) fn parse_key_event(msg: &str) -> Option<KeyEventParsed> {
    let args_part = msg.split_once(".key,")?.1;
    let (first_arg, rest) = args_part.split_once(',')?;
    let (_, keysym_str) = first_arg.split_once('.')?;
    let keysym = keysym_str.parse::<u32>().ok()?;

    let (_, pressed_val) = rest.split_once('.')?;
    let pressed = pressed_val.starts_with('1');

    Some(KeyEventParsed { keysym, pressed })
}

/// Parse a Guacamole mouse instruction.
///
/// Format: `5.mouse,{x_len}.{x},{y_len}.{y},{button_len}.{button};`
pub(crate) fn parse_mouse_event(msg: &str) -> Option<MouseEventParsed> {
    let args_part = msg.split_once(".mouse,")?.1;
    let parts: Vec<&str> = args_part.split(',').collect();
    if parts.len() < 3 {
        return None;
    }

    let (_, x_str) = parts[0].split_once('.')?;
    let (_, y_str) = parts[1].split_once('.')?;
    let button_part = parts[2].trim_end_matches(';');
    let (_, button_str) = button_part.split_once('.')?;

    Some(MouseEventParsed {
        x: x_str.parse().ok()?,
        y: y_str.parse().ok()?,
        button_mask: button_str.parse().ok()?,
    })
}

/// Parse a Guacamole size instruction.
///
/// Format: `4.size,{width_len}.{width},{height_len}.{height};`
pub(crate) fn parse_size_event(msg: &str) -> Option<(u32, u32)> {
    let args_part = msg.split_once(".size,")?.1;
    let parts: Vec<&str> = args_part.split(',').collect();
    if parts.len() < 2 {
        return None;
    }

    let (_, width_str) = parts[0].split_once('.')?;
    let height_part = parts[1].trim_end_matches(';');
    let (_, height_str) = height_part.split_once('.')?;

    Some((width_str.parse().ok()?, height_str.parse().ok()?))
}

/// Parse display size from connection params.
///
/// The "size" parameter is formatted as "width,height,dpi".
/// Returns (pixel_width, pixel_height).
pub(crate) fn parse_display_size(params: &HashMap<String, String>) -> (u32, u32) {
    let size_str = params
        .get("size")
        .map(|s| s.as_str())
        .unwrap_or("1024,768,96");
    let parts: Vec<&str> = size_str.split(',').collect();
    let width = parts
        .first()
        .and_then(|s| s.parse().ok())
        .unwrap_or(DEFAULT_WIDTH);
    let height = parts
        .get(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(DEFAULT_HEIGHT);

    (width, height)
}
