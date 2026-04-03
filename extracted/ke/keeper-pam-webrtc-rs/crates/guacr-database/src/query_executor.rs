// Database query executor with ratatui-based result rendering
// Unified executor for all database handlers

const CHAR_WIDTH: u32 = 9;
const CHAR_HEIGHT: u32 = 18;

use crate::ratatui_db_ui::{AppFocus, DatabaseRatatuiApp};
use crate::{DatabaseError, Result};
use bytes::Bytes;
use guacr_handlers::{send_name, send_ready, CursorManager, HandlerError, StandardCursor};
use guacr_protocol::{format_chunked_blobs, GuacamoleParser, TextProtocolEncoder};
use guacr_terminal::{
    format_clear_selection_instructions, format_clipboard_instructions, parse_mouse_instruction,
    QueryResult, RatatuiRenderer, SelectionResult, TerminalInputHandler, TerminalRenderer,
};
use std::time::Instant;
use tokio::sync::mpsc;

// Re-export QueryResult for convenience
pub use guacr_terminal::QueryResult as QueryResultData;

/// Database query executor
///
/// Handles keyboard input processing, query buffering, and result rendering.
/// Used by all database handlers for consistent SQL CLI experience.
///
/// Rendering pipeline: ratatui TestBackend (layout engine) -> fontdue pixel renderer -> JPEG
pub struct QueryExecutor {
    pub ratatui: RatatuiRenderer,
    pub app: DatabaseRatatuiApp,
    stream_id: u32,
    db_type: String,

    // Multi-line continuation
    pub(crate) in_continuation: bool,

    // Current database context (for dynamic prompts)
    pub(crate) current_database: Option<String>,
    prompt_template: String,

    // Clipboard parsing (mouse selection removed in this refactor)
    input_handler: TerminalInputHandler,

    // Zero-allocation protocol encoder (shared scratch buffer)
    protocol_encoder: TextProtocolEncoder,

    // Dirty flag: true when content changed since last render_screen call.
    // Prevents the 60fps debounce from re-encoding identical frames.
    dirty: bool,
}

impl QueryExecutor {
    /// Create a new query executor for a specific database type with default size
    pub fn new(prompt: &str, db_type: &str) -> Result<Self> {
        Self::new_with_size(prompt, db_type, 24, 80)
    }

    /// Create a new query executor with custom terminal dimensions
    pub fn new_with_size(prompt: &str, db_type: &str, rows: u16, cols: u16) -> Result<Self> {
        let continuation_prompt = match db_type {
            "mysql" | "mariadb" => "    -> ".to_string(),
            "postgresql" => "    -> ".to_string(),
            "mongodb" => "... ".to_string(),
            "redis" => "... ".to_string(),
            _ => "    -> ".to_string(),
        };

        Ok(Self {
            ratatui: RatatuiRenderer::new(cols, rows, CHAR_WIDTH, CHAR_HEIGHT)?,
            app: DatabaseRatatuiApp::new(prompt, &continuation_prompt),
            stream_id: 1,
            db_type: db_type.to_string(),
            in_continuation: false,
            current_database: None,
            prompt_template: prompt.to_string(),
            input_handler: TerminalInputHandler::new_with_scrollback(rows, cols, 1000),
            protocol_encoder: TextProtocolEncoder::new(),
            dirty: true, // render on first tick
        })
    }

    /// Get the database type
    pub fn db_type(&self) -> &str {
        &self.db_type
    }

    /// Send display initialization instructions (ready, name, cursor, size)
    pub async fn send_display_init(
        to_client: &mpsc::Sender<Bytes>,
        width: u32,
        height: u32,
    ) -> std::result::Result<(), HandlerError> {
        send_ready(to_client, "database").await?;
        send_name(to_client, "Database").await?;

        // Send I-beam cursor bitmap (standard text cursor for terminals)
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

    /// Get terminal size (rows, cols)
    pub fn size(&self) -> (u16, u16) {
        let area = self.ratatui.terminal.backend().buffer().area;
        (area.height, area.width)
    }

    /// Handle clipboard paste from client
    async fn handle_clipboard_input(
        &mut self,
        instruction: &str,
    ) -> Result<(bool, Vec<Bytes>, Option<String>)> {
        if let Some(clipboard_text) = self.input_handler.parse_clipboard_instruction(instruction) {
            self.app.insert_clipboard_text(&clipboard_text);
            let (_, instructions) = self.render_screen().await?;
            Ok((true, instructions, None))
        } else {
            Ok((false, vec![], None))
        }
    }

    /// Handle mouse input for text selection and results table row clicks
    async fn handle_mouse_input(
        &mut self,
        instruction: &str,
    ) -> Result<(bool, Vec<Bytes>, Option<String>)> {
        let Some(mouse_event) = parse_mouse_instruction(instruction) else {
            return Ok((false, vec![], None));
        };

        // Scroll wheel (bits 3=up, 4=down): scroll the results table.
        const SCROLL_LINES: usize = 3;
        if mouse_event.button_mask & 0x08 != 0 && !self.app.results.is_empty() {
            let sel = self.app.table_state.selected().unwrap_or(0);
            self.app
                .table_state
                .select(Some(sel.saturating_sub(SCROLL_LINES)));
            let (_, instructions) = self.render_screen().await?;
            return Ok((true, instructions, None));
        }
        if mouse_event.button_mask & 0x10 != 0 && !self.app.results.is_empty() {
            let sel = self.app.table_state.selected().unwrap_or(0);
            let new_sel = (sel + SCROLL_LINES).min(self.app.results.len().saturating_sub(1));
            self.app.table_state.select(Some(new_sel));
            let (_, instructions) = self.render_screen().await?;
            return Ok((true, instructions, None));
        }

        // Left-click (button_mask bit 0): check if it lands in the results table data area.
        // Layout: results panel fills top, input panel is 3 rows at the bottom.
        // Within the results panel: 1-row block border + 1-row header = 2 rows before data.
        // So data rows start at pixel y = 2 * CHAR_HEIGHT = 36.
        // The results panel ends at pixel y = (total_rows - 3) * CHAR_HEIGHT.
        if mouse_event.button_mask & 0x01 != 0 && !self.app.results.is_empty() {
            let (total_rows, _) = self.size();
            let results_panel_height_px = (total_rows as u32).saturating_sub(3) * CHAR_HEIGHT;
            const DATA_ROW_PIXEL_START: u32 = 2 * CHAR_HEIGHT; // border + header

            if mouse_event.y_px >= DATA_ROW_PIXEL_START
                && mouse_event.y_px < results_panel_height_px
            {
                let clicked_row =
                    ((mouse_event.y_px - DATA_ROW_PIXEL_START) / CHAR_HEIGHT) as usize;
                if clicked_row < self.app.results.len() {
                    self.app.table_state.select(Some(clicked_row));
                    self.app.focus = AppFocus::Results;
                    let (_, instructions) = self.render_screen().await?;
                    return Ok((true, instructions, None));
                }
            }
        }

        // buffer borrows from self.ratatui; mouse_selection mutation is in self.input_handler —
        // disjoint fields allow simultaneous borrows.
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

    /// Handle terminal resize
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

    /// Process keyboard input and return query if Enter was pressed
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
                return self
                    .handle_clipboard_input(&String::from_utf8_lossy(instruction))
                    .await
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

        // Clear any active selection overlay when a non-release key event arrives
        let had_selection = pressed && self.input_handler.has_selection();
        if had_selection {
            self.input_handler.clear_selection();
        }

        let pending_query = self.app.handle_key(keysym, pressed);

        // Mark dirty so the debounce timer renders within ~16ms.
        // Calling render_screen() here (per keystroke) is the source of typing lag.
        self.dirty = true;

        // If a selection was just cleared, dispose the overlay immediately so it
        // disappears without waiting for the debounce tick.
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

    /// Write query result to the results panel
    pub fn write_result(&mut self, result: &QueryResult) -> Result<()> {
        self.app.set_results(result);
        self.app.focus = AppFocus::Input;
        self.dirty = true;
        Ok(())
    }

    /// Write error message to the results panel
    pub fn write_error(&mut self, error: &str) -> Result<()> {
        self.app.set_error(error);
        self.app.focus = AppFocus::Input;
        self.dirty = true;
        Ok(())
    }

    /// Write a status/info message to the results panel
    pub fn write_status(&mut self, msg: &str) {
        self.app.set_status(msg.to_string(), None);
        self.dirty = true;
    }

    /// Append a line to the status message (for multi-line banners)
    pub fn write_line(&mut self, line: &str) -> Result<()> {
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

    /// Write a success message (same as write_line in the ratatui path)
    pub fn write_success(&mut self, msg: &str) -> Result<()> {
        self.write_line(msg)
    }

    /// No-op: prompt is always visible in the ratatui input widget
    pub fn write_prompt(&mut self) -> Result<()> {
        Ok(())
    }

    pub fn is_dirty(&self) -> bool {
        self.dirty
    }

    /// Render terminal screen and return Guacamole instructions
    pub async fn render_screen(&mut self) -> Result<(bool, Vec<Bytes>)> {
        // Sync continuation state to app before rendering
        self.app.in_continuation = self.in_continuation;

        let app = &mut self.app;
        self.ratatui
            .terminal
            .draw(|f| app.render(f))
            .map_err(|e| DatabaseError::QueryError(format!("Render error: {}", e)))?;

        let jpeg = self
            .ratatui
            .render_to_jpeg(85)
            .map_err(|e| DatabaseError::QueryError(format!("JPEG error: {}", e)))?;

        let base64_data = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, &jpeg);

        let img_instr =
            self.protocol_encoder
                .format_img_instruction(self.stream_id, 0, 0, 0, "image/jpeg");
        let blob_instructions = format_chunked_blobs(self.stream_id, &base64_data, None);

        let mut instructions = Vec::with_capacity(1 + blob_instructions.len() + 1);
        instructions.push(img_instr.freeze());
        instructions.extend(blob_instructions.into_iter().map(Bytes::from));

        let timestamp_ms = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_millis() as u64;
        let sync_instr = self
            .ratatui
            .font_renderer
            .format_sync_instruction(timestamp_ms);
        instructions.push(Bytes::from(sync_instr));

        self.dirty = false;
        Ok((true, instructions))
    }

    /// Get current input buffer contents
    pub fn current_input(&self) -> &str {
        &self.app.input_buffer
    }

    /// Set the current database context (for dynamic prompts)
    pub fn set_current_database(&mut self, database: Option<String>) {
        self.current_database = database;
        self.update_prompt();
        self.dirty = true;
    }

    /// Update the prompt based on current context
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

    /// Set continuation mode
    pub fn set_continuation(&mut self, in_continuation: bool) {
        self.in_continuation = in_continuation;
        self.dirty = true;
    }
}

/// Query execution result with timing
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

/// Helper trait for database query execution
#[async_trait::async_trait]
#[allow(dead_code)]
pub trait DatabaseQueryExecutor: Send + Sync {
    /// Execute a query and return results
    async fn execute(&self, query: &str) -> std::result::Result<QueryResult, String>;

    /// Test connection
    async fn test_connection(&self) -> std::result::Result<(), String>;
}

/// Measure query execution time
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
