// Database query executor with ratatui-based result rendering
// Unified executor for all database handlers

use crate::ratatui_db_ui::DatabaseRatatuiApp;
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
    in_continuation: bool,

    // Current database context (for dynamic prompts)
    current_database: Option<String>,
    prompt_template: String,

    // Clipboard parsing (mouse selection removed in this refactor)
    input_handler: TerminalInputHandler,

    // Zero-allocation protocol encoder (shared scratch buffer)
    protocol_encoder: TextProtocolEncoder,
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

        const CHAR_WIDTH: u32 = 9;
        const CHAR_HEIGHT: u32 = 18;

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

    /// Handle mouse input for text selection
    async fn handle_mouse_input(
        &mut self,
        instruction: &str,
    ) -> Result<(bool, Vec<Bytes>, Option<String>)> {
        let Some(mouse_event) = parse_mouse_instruction(instruction) else {
            return Ok((false, vec![], None));
        };

        const CHAR_WIDTH: u32 = 9;
        const CHAR_HEIGHT: u32 = 18;

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

            const CHAR_WIDTH: u32 = 9;
            const CHAR_HEIGHT: u32 = 18;
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
        let (_, render_instructions) = self.render_screen().await?;

        let instructions = if had_selection {
            // Prepend dispose(1) so the selection overlay disappears before the new frame
            let mut all: Vec<Bytes> = format_clear_selection_instructions()
                .into_iter()
                .map(Bytes::from)
                .collect();
            all.extend(render_instructions);
            all
        } else {
            render_instructions
        };

        Ok((true, instructions, pending_query))
    }

    /// Write query result to the results panel
    pub fn write_result(&mut self, result: &QueryResult) -> Result<()> {
        self.app.set_results(result);
        Ok(())
    }

    /// Write error message to the results panel
    pub fn write_error(&mut self, error: &str) -> Result<()> {
        self.app.set_error(error);
        Ok(())
    }

    /// Write a status/info message to the results panel
    ///
    /// Used by handlers for connection messages, warnings, etc.
    pub fn write_status(&mut self, msg: &str) {
        self.app.set_status(msg.to_string(), None);
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

    /// Always returns true — ratatui renders the full screen on every call
    pub fn is_dirty(&self) -> bool {
        true
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

#[cfg(test)]
mod tests {
    use super::*;

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

        std::fs::write("/tmp/db_render_test.jpg", &jpeg).unwrap();
        println!("Saved {} bytes to /tmp/db_render_test.jpg", jpeg.len());
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
        std::fs::write("/tmp/db_input_test.jpg", &jpeg).unwrap();
        println!("Saved {} bytes to /tmp/db_input_test.jpg", jpeg.len());
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
}
