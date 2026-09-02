use crate::ratatui_db_ui::{AppFocus, DatabaseRatatuiApp, TAB_TERMINAL_COLS};

use crate::{DatabaseError, Result};
use bytes::Bytes;
use guacr_handlers::{send_name, send_ready, CursorManager, HandlerError, StandardCursor};
use guacr_protocol::{format_terminal_data_binary, GuacamoleParser};
use guacr_terminal::{
    buffer_to_ansi, format_clear_selection_instructions, format_clipboard_instructions,
    parse_mouse_instruction, QueryResult, RatatuiRenderer, SelectionResult, TerminalInputHandler,
    TerminalRenderer, CHAR_HEIGHT, CHAR_WIDTH,
};
use std::time::Instant;
use tokio::sync::mpsc;

pub use guacr_terminal::QueryResult as QueryResultData;

use crate::ratatui_db_ui::ViewMode;

/// Map a click's y pixel to the index of the data row it landed on, counted from the
/// top of the rendered viewport. Returns `None` for a click outside the data band.
///
/// The Grid layout is tab bar (1 row) + results panel (`total_rows - 4`) + query input
/// (3 rows). Inside the panel, from the top: top border, header, the data rows, bottom
/// border, and the status bar on the panel's final row. Only the data rows are
/// selectable, so the band is `[3 rows, total_rows - 5 rows)`.
///
/// The returned index is viewport-relative: callers must add `TableState::offset()` to
/// get an index into the result set.
pub(crate) fn grid_clicked_data_row(y_px: u32, total_rows: u16) -> Option<usize> {
    let data_start_px = 3 * CHAR_HEIGHT;
    let data_end_px = (total_rows as u32).saturating_sub(5) * CHAR_HEIGHT;

    if y_px < data_start_px || y_px >= data_end_px {
        return None;
    }
    Some(((y_px - data_start_px) / CHAR_HEIGHT) as usize)
}

/// Database query executor
///
/// Handles keyboard input processing, query buffering, and result rendering.
/// Used by all database handlers for consistent SQL CLI experience.
///
/// Rendering pipeline: ratatui TestBackend (layout engine) -> ANSI escape codes -> terminal-data
pub struct QueryExecutor {
    pub ratatui: RatatuiRenderer,
    pub app: DatabaseRatatuiApp,
    stream_id: u32,
    db_type: String,

    pub(crate) in_continuation: bool,
    pub(crate) current_database: Option<String>,
    prompt_template: String,

    input_handler: TerminalInputHandler,

    // Dirty flag: true when content changed since last render_screen call.
    dirty: bool,

    // Last query result, stored for CSV export.
    last_result: Option<QueryResult>,
}

impl QueryExecutor {
    pub fn new(prompt: &str, db_type: &str) -> Result<Self> {
        Self::new_with_size(prompt, db_type, 24, 80)
    }

    pub fn new_with_size(prompt: &str, db_type: &str, rows: u16, cols: u16) -> Result<Self> {
        let continuation_prompt = match db_type {
            "mysql" | "mariadb" => "    -> ".to_string(),
            "postgresql" => "    -> ".to_string(),
            "mongodb" => "... ".to_string(),
            "redis" => "... ".to_string(),
            _ => "    -> ".to_string(),
        };

        let grid_view_enabled = std::env::var("GUACR_DB_GRID_VIEW")
            .map(|v| matches!(v.to_ascii_lowercase().as_str(), "1" | "true" | "yes"))
            .unwrap_or(false);

        Ok(Self {
            ratatui: RatatuiRenderer::new(cols, rows, CHAR_WIDTH, CHAR_HEIGHT)?,
            app: DatabaseRatatuiApp::new(prompt, &continuation_prompt, grid_view_enabled),
            stream_id: 1,
            db_type: db_type.to_string(),
            in_continuation: false,
            current_database: None,
            prompt_template: prompt.to_string(),
            input_handler: TerminalInputHandler::new_with_scrollback(rows, cols, 1000),
            dirty: true,
            last_result: None,
        })
    }

    pub fn db_type(&self) -> &str {
        &self.db_type
    }

    pub async fn send_display_init(
        to_client: &mpsc::Sender<Bytes>,
        width: u32,
        height: u32,
    ) -> std::result::Result<(), HandlerError> {
        send_ready(to_client, "database").await?;
        send_name(to_client, "Database").await?;

        let mut cursor_manager = CursorManager::new(false, false, 85);
        let cursor_instrs = cursor_manager
            .send_standard_cursor(StandardCursor::IBeam)
            .map_err(|e| HandlerError::ProtocolError(format!("Cursor error: {}", e)))?;
        for instr in cursor_instrs {
            to_client
                .send(Bytes::from(instr))
                .await
                .map_err(|e| HandlerError::ChannelError(e.to_string()))?;
        }

        let size = Bytes::from(TerminalRenderer::format_size_instruction(0, width, height));
        to_client
            .send(size)
            .await
            .map_err(|e| HandlerError::ChannelError(e.to_string()))?;

        Ok(())
    }

    pub fn size(&self) -> (u16, u16) {
        let area = self.ratatui.terminal.backend().buffer().area;
        (area.height, area.width)
    }

    async fn handle_mouse_input(
        &mut self,
        instruction: &str,
    ) -> Result<(bool, Vec<Bytes>, Option<String>)> {
        let Some(mouse_event) = parse_mouse_instruction(instruction) else {
            return Ok((false, vec![], None));
        };

        // Tab bar click (top 1 row = y < CHAR_HEIGHT): switch view mode
        if self.app.grid_view_enabled
            && mouse_event.button_mask & 0x01 != 0
            && mouse_event.y_px < CHAR_HEIGHT
        {
            let new_mode = if mouse_event.x_px < TAB_TERMINAL_COLS * CHAR_WIDTH {
                ViewMode::Terminal
            } else {
                ViewMode::Grid
            };
            if new_mode != self.app.view_mode {
                self.app.view_mode = new_mode;
                let (_, instructions) = self.render_screen().await?;
                return Ok((true, instructions, None));
            }
            return Ok((false, vec![], None));
        }

        // Mouse scroll: wheel up = bit 3, wheel down = bit 4
        // The tab bar is row 0 (1 row), so content starts at y >= CHAR_HEIGHT.
        // Grid view table data starts at CHAR_HEIGHT + 2*CHAR_HEIGHT (tab + border + header).
        const SCROLL_LINES: usize = 3;

        if mouse_event.button_mask & 0x08 != 0 {
            match self.app.view_mode {
                ViewMode::Terminal => {
                    let max_offset = self.app.scrollback.len();
                    self.app.scroll_offset =
                        (self.app.scroll_offset + SCROLL_LINES).min(max_offset);
                    let (_, instructions) = self.render_screen().await?;
                    return Ok((true, instructions, None));
                }
                ViewMode::Grid => {
                    if !self.app.results.is_empty() {
                        let sel = self.app.table_state.selected().unwrap_or(0);
                        self.app
                            .table_state
                            .select(Some(sel.saturating_sub(SCROLL_LINES)));
                        let (_, instructions) = self.render_screen().await?;
                        return Ok((true, instructions, None));
                    }
                }
            }
        }

        if mouse_event.button_mask & 0x10 != 0 {
            match self.app.view_mode {
                ViewMode::Terminal => {
                    self.app.scroll_offset = self.app.scroll_offset.saturating_sub(SCROLL_LINES);
                    let (_, instructions) = self.render_screen().await?;
                    return Ok((true, instructions, None));
                }
                ViewMode::Grid => {
                    if !self.app.results.is_empty() {
                        let sel = self.app.table_state.selected().unwrap_or(0);
                        let new_sel =
                            (sel + SCROLL_LINES).min(self.app.results.len().saturating_sub(1));
                        self.app.table_state.select(Some(new_sel));
                        let (_, instructions) = self.render_screen().await?;
                        return Ok((true, instructions, None));
                    }
                }
            }
        }

        // Left-click in Grid view results area
        if mouse_event.button_mask & 0x01 != 0
            && self.app.view_mode == ViewMode::Grid
            && !self.app.results.is_empty()
        {
            let (total_rows, _) = self.size();
            if let Some(visible_row) = grid_clicked_data_row(mouse_event.y_px, total_rows) {
                // The click lands on a rendered row, which is `offset` rows into the
                // result set once the table has been scrolled.
                let clicked_row = self.app.table_state.offset() + visible_row;
                if clicked_row < self.app.results.len() {
                    self.app.table_state.select(Some(clicked_row));
                    self.app.focus = AppFocus::Results;
                    let (_, instructions) = self.render_screen().await?;
                    return Ok((true, instructions, None));
                }
            }
        }

        // Text selection (only in Terminal view; Grid view selection not meaningful)
        let buffer = self.ratatui.terminal.backend().buffer();
        let result = self.input_handler.handle_mouse_event_ratatui(
            mouse_event,
            buffer,
            CHAR_WIDTH,
            CHAR_HEIGHT,
        );

        match result {
            SelectionResult::InProgress(overlay_instrs) => {
                let instructions = overlay_instrs.into_iter().map(Bytes::from).collect();
                Ok((true, instructions, None))
            }
            SelectionResult::Complete {
                text,
                clear_instructions,
            } => {
                let clipboard_instrs = format_clipboard_instructions(&text, self.stream_id);
                let instructions: Vec<Bytes> = clear_instructions
                    .into_iter()
                    .chain(clipboard_instrs)
                    .map(Bytes::from)
                    .collect();
                Ok((true, instructions, None))
            }
            SelectionResult::None => Ok((false, vec![], None)),
        }
    }

    async fn handle_resize_input(
        &mut self,
        args: &[&str],
    ) -> Result<(bool, Vec<Bytes>, Option<String>)> {
        if args.len() >= 2 {
            let width: u32 = args[0].parse().unwrap_or(1024);
            let height: u32 = args[1].parse().unwrap_or(768);

            let cols = (width / CHAR_WIDTH).max(80) as u16;
            let rows = (height / CHAR_HEIGHT).max(24) as u16;

            self.ratatui
                .resize(cols, rows)
                .map_err(|e| DatabaseError::QueryError(format!("Resize error: {}", e)))?;

            self.input_handler.clear_selection();

            let (_, instructions) = self.render_screen().await?;
            Ok((true, instructions, None))
        } else {
            Ok((false, vec![], None))
        }
    }

    /// Process keyboard/mouse input and return query if Enter was pressed.
    ///
    /// Returns (needs_render, instructions, pending_query)
    pub async fn process_input(
        &mut self,
        instruction: &Bytes,
    ) -> Result<(bool, Vec<Bytes>, Option<String>)> {
        let instr = GuacamoleParser::parse_instruction(instruction)
            .map_err(|e| DatabaseError::QueryError(format!("Parse error: {}", e)))?;

        match instr.opcode {
            "mouse" => {
                return self
                    .handle_mouse_input(&String::from_utf8_lossy(instruction))
                    .await;
            }
            "clipboard" => {
                // Direct clipboard instruction: args = [mime_type, text]
                if instr.args.len() >= 2 && !instr.args[1].is_empty() {
                    self.app.insert_clipboard_text(instr.args[1]);
                    self.dirty = true;
                }
                return Ok((true, vec![], None));
            }
            "blob" => {
                // Guacamole streaming clipboard protocol (same path as SSH).
                // Vault sends via createClipboardStream → StringWriter → blob instruction.
                if let Some(text) =
                    guacr_protocol::parse_clipboard_blob(&String::from_utf8_lossy(instruction))
                {
                    self.app.insert_clipboard_text(&text);
                    self.dirty = true;
                }
                return Ok((true, vec![], None));
            }
            "export-csv" => {
                return self.handle_export_csv().await;
            }
            "size" => return self.handle_resize_input(&instr.args).await,
            "key" => {}
            _ => return Ok((false, vec![], None)),
        }

        if instr.args.len() < 2 {
            return Ok((false, vec![], None));
        }

        let keysym: u32 = instr.args[0]
            .parse()
            .map_err(|_| DatabaseError::QueryError("Invalid keysym".to_string()))?;
        let pressed = instr.args[1] == "1";

        let had_selection = pressed && self.input_handler.has_selection();
        if had_selection {
            self.input_handler.clear_selection();
        }

        // Modifier-only keys (Ctrl left/right = 0xFFE3/0xFFE4) change no visible
        // state — skip dirty-flag to avoid triggering a needless re-render.
        let is_modifier_only = matches!(keysym, 0xFFE3 | 0xFFE4);

        let pending_query = self.app.handle_key(keysym, pressed);

        // Echo submitted command to scrollback so terminal view shows history
        if let Some(ref q) = pending_query {
            let prompt = if self.app.in_continuation {
                self.app.continuation_prompt.clone()
            } else {
                self.app.prompt.clone()
            };
            self.app
                .append_scrollback_command(&format!("{}{}", prompt, q));
        }

        if !is_modifier_only {
            self.dirty = true;
        }

        let instructions = if had_selection {
            format_clear_selection_instructions()
                .into_iter()
                .map(Bytes::from)
                .collect()
        } else {
            vec![]
        };

        Ok((true, instructions, pending_query))
    }

    pub fn write_result(&mut self, result: &QueryResult) -> Result<()> {
        self.last_result = Some(result.clone());
        self.app.set_results(result);
        self.app.append_result_to_scrollback(result);
        self.app.focus = AppFocus::Input;
        self.dirty = true;
        Ok(())
    }

    pub fn write_error(&mut self, error: &str) -> Result<()> {
        self.app.set_error(error);
        self.app
            .append_scrollback_error(&format!("ERROR: {}", error));
        self.app.focus = AppFocus::Input;
        self.dirty = true;
        Ok(())
    }

    pub fn write_status(&mut self, msg: &str) {
        self.app.set_status(msg.to_string(), None);
        if !msg.is_empty() {
            self.app.append_scrollback_info(msg);
        }
        self.dirty = true;
    }

    pub fn write_line(&mut self, line: &str) -> Result<()> {
        // Always append to scrollback (even empty lines — they're blank lines in terminal output)
        self.app.append_scrollback_info(line);
        // Only append to status_msg (grid view) if non-empty
        if !line.is_empty() {
            if self.app.status_msg.is_empty() {
                self.app.status_msg = line.to_string();
            } else {
                self.app.status_msg.push('\n');
                self.app.status_msg.push_str(line);
            }
            self.dirty = true;
        }
        Ok(())
    }

    pub fn write_success(&mut self, msg: &str) -> Result<()> {
        self.write_line(msg)
    }

    pub fn write_prompt(&mut self) -> Result<()> {
        Ok(())
    }

    pub fn is_dirty(&self) -> bool {
        self.dirty
    }

    /// Render terminal screen and return protocol instructions.
    pub async fn render_screen(&mut self) -> Result<(bool, Vec<Bytes>)> {
        self.app.in_continuation = self.in_continuation;

        let app = &mut self.app;
        self.ratatui
            .terminal
            .draw(|f| app.render(f))
            .map_err(|e| DatabaseError::QueryError(format!("Render error: {}", e)))?;

        let ansi_bytes = {
            let buffer = self.ratatui.terminal.backend().buffer().clone();
            let mut bytes = buffer_to_ansi(&buffer);
            // Hide the xterm.js hardware cursor — we render our own inline cursor char
            bytes.extend_from_slice(b"\x1b[?25l");
            bytes
        };

        let instr = format_terminal_data_binary(&ansi_bytes);
        self.dirty = false;
        Ok((true, vec![instr]))
    }

    pub fn current_input(&self) -> &str {
        &self.app.input_buffer
    }

    pub fn set_current_database(&mut self, database: Option<String>) {
        self.current_database = database;
        self.update_prompt();
        self.dirty = true;
    }

    fn update_prompt(&mut self) {
        let prompt = if let Some(ref db) = self.current_database {
            match self.db_type.as_str() {
                "mysql" | "mariadb" => format!("mysql [{}]> ", db),
                "postgresql" => format!("{}=# ", db),
                _ => self.prompt_template.clone(),
            }
        } else {
            self.prompt_template.clone()
        };

        self.app.set_prompt(&prompt);
    }

    pub fn set_continuation(&mut self, in_continuation: bool) {
        self.in_continuation = in_continuation;
        self.dirty = true;
    }

    /// Handle the `export-csv` opcode from the client.
    ///
    /// Formats the last query result as a CSV file and returns the Guacamole
    /// `file` + `blob`... + `end` instructions to stream to the client.
    /// Returns `(needs_render=true, [], None)` when there are no results to export.
    async fn handle_export_csv(&mut self) -> Result<(bool, Vec<Bytes>, Option<String>)> {
        let result = match &self.last_result {
            Some(r) => r.clone(),
            None => {
                self.write_error("No query results to export")?;
                self.dirty = true;
                return Ok((true, vec![], None));
            }
        };

        // Use the last command from scrollback to build a descriptive filename.
        let last_command = self.app.scrollback.iter().rev().find_map(|line| {
            if let crate::ratatui_db_ui::ScrollbackLine::Command(cmd) = line {
                let trimmed = cmd.trim();
                if !trimmed.is_empty() {
                    // Strip the prompt prefix (everything up to and including "> " or "# ")
                    let cmd_text = trimmed
                        .find("> ")
                        .map(|i| trimmed[i + 2..].trim())
                        .or_else(|| trimmed.find("# ").map(|i| trimmed[i + 2..].trim()))
                        .unwrap_or(trimmed);
                    if !cmd_text.is_empty() {
                        return Some(cmd_text.to_string());
                    }
                }
            }
            None
        });

        let filename = crate::csv_export::generate_csv_filename(
            &last_command.unwrap_or_default(),
            &self.db_type,
        );

        let mut exporter = crate::csv_export::CsvExporter::new(1000);
        let mut instructions: Vec<Bytes> = Vec::new();

        // file instruction opens the download on the client side
        instructions.push(exporter.start_download(&filename));

        // Stream CSV data through an in-process channel and collect the blobs synchronously
        let (tx, mut rx) = tokio::sync::mpsc::channel::<Bytes>(64);
        let export_result = exporter.export_query_result(&result, &tx).await;
        drop(tx);
        while let Some(blob) = rx.recv().await {
            instructions.push(blob);
        }

        if let Err(e) = export_result {
            self.write_error(&format!("CSV export failed: {}", e))?;
            self.dirty = true;
            return Ok((true, vec![], None));
        }

        Ok((false, instructions, None))
    }
}

pub struct ExecutionResult {
    pub result: QueryResult,
    pub execution_time: std::time::Duration,
}

impl ExecutionResult {
    pub fn new(result: QueryResult, execution_time: std::time::Duration) -> Self {
        Self {
            result,
            execution_time,
        }
    }

    pub fn into_query_result(self) -> QueryResult {
        let mut result = self.result;
        result.execution_time_ms = Some(self.execution_time.as_millis() as u64);
        result
    }
}

pub async fn execute_with_timing<F, Fut>(
    execute_fn: F,
) -> std::result::Result<ExecutionResult, String>
where
    F: FnOnce() -> Fut,
    Fut: std::future::Future<Output = std::result::Result<QueryResult, String>>,
{
    let start = Instant::now();
    let result = execute_fn().await?;
    let duration = start.elapsed();
    Ok(ExecutionResult::new(result, duration))
}
