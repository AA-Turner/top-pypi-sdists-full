use std::collections::VecDeque;

use guacr_terminal::QueryResult;
use ratatui::{
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{
        Block, Borders, Cell, Paragraph, Row, Scrollbar, ScrollbarOrientation, ScrollbarState,
        Table, TableState,
    },
    Frame,
};

pub struct DatabaseRatatuiApp {
    // Query results
    pub results: Vec<Vec<String>>,
    pub columns: Vec<String>,
    pub table_state: TableState,
    pub scroll_state: ScrollbarState,

    // Input line
    pub input_buffer: String,
    pub cursor_pos: usize,

    // History
    pub history: VecDeque<String>,
    pub history_idx: Option<usize>,
    pub temp_buffer: String,
    pub history_max_size: usize,

    // Status / prompt
    pub status_msg: String,
    pub query_time_ms: Option<u64>,
    pub prompt: String,
    pub in_continuation: bool,
    pub continuation_prompt: String,
}

impl DatabaseRatatuiApp {
    pub fn new(prompt: &str, continuation_prompt: &str) -> Self {
        Self {
            results: Vec::new(),
            columns: Vec::new(),
            table_state: TableState::default(),
            scroll_state: ScrollbarState::default(),
            input_buffer: String::new(),
            cursor_pos: 0,
            history: VecDeque::new(),
            history_idx: None,
            temp_buffer: String::new(),
            history_max_size: 250,
            status_msg: String::new(),
            query_time_ms: None,
            prompt: prompt.to_string(),
            in_continuation: false,
            continuation_prompt: continuation_prompt.to_string(),
        }
    }

    pub fn set_prompt(&mut self, prompt: &str) {
        self.prompt = prompt.to_string();
    }

    pub fn set_results(&mut self, result: &QueryResult) {
        self.columns = result.columns.clone();
        self.results = result.rows.clone();
        self.table_state = TableState::default();
        let row_count = self.results.len();
        self.scroll_state = ScrollbarState::new(row_count);

        let summary = if result.rows.is_empty() {
            if let Some(affected) = result.affected_rows {
                format!("Query OK, {} row(s) affected", affected)
            } else {
                "Query executed successfully".to_string()
            }
        } else {
            format!("{} row(s)", result.rows.len())
        };

        self.status_msg = if let Some(ms) = result.execution_time_ms {
            format!("{} ({}ms)", summary, ms)
        } else {
            summary
        };
        self.query_time_ms = result.execution_time_ms;
    }

    pub fn set_error(&mut self, error: &str) {
        self.status_msg = format!("ERROR: {}", error);
        self.columns.clear();
        self.results.clear();
    }

    pub fn set_status(&mut self, msg: String, time_ms: Option<u64>) {
        self.status_msg = msg;
        self.query_time_ms = time_ms;
    }

    pub fn insert_clipboard_text(&mut self, text: &str) {
        self.input_buffer.insert_str(self.cursor_pos, text);
        self.cursor_pos += text.len();
    }

    /// Render the full UI into the given frame
    pub fn render(&mut self, frame: &mut Frame) {
        let area = frame.area();

        // Split vertically: results on top (flexible), input at bottom (3 rows)
        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .constraints([Constraint::Min(3), Constraint::Length(3)])
            .split(area);

        self.render_results(frame, chunks[0]);
        self.render_input(frame, chunks[1]);
    }

    fn render_results(&mut self, frame: &mut Frame, area: Rect) {
        if self.columns.is_empty() {
            let para = Paragraph::new(self.status_msg.clone())
                .block(Block::default().borders(Borders::ALL).title("Results"))
                .style(Style::default().fg(Color::Gray));
            frame.render_widget(para, area);
            return;
        }

        let header_cells: Vec<Cell> = self
            .columns
            .iter()
            .map(|c| {
                Cell::from(c.clone()).style(
                    Style::default()
                        .fg(Color::LightCyan)
                        .add_modifier(Modifier::BOLD),
                )
            })
            .collect();
        let header = Row::new(header_cells).height(1);

        let rows: Vec<Row> = self
            .results
            .iter()
            .map(|row| {
                let cells: Vec<Cell> = row.iter().map(|val| Cell::from(val.clone())).collect();
                Row::new(cells).height(1)
            })
            .collect();

        let col_count = self.columns.len().max(1);
        let constraints: Vec<Constraint> = (0..col_count)
            .map(|_| Constraint::Ratio(1, col_count as u32))
            .collect();

        let title = if self.status_msg.is_empty() {
            "Results".to_string()
        } else {
            format!("Results - {}", self.status_msg)
        };

        let table = Table::new(rows, constraints)
            .header(header)
            .block(Block::default().borders(Borders::ALL).title(title))
            .row_highlight_style(Style::default().add_modifier(Modifier::REVERSED))
            .style(Style::default().fg(Color::White));

        // Leave 1 column for the scrollbar
        let table_area = Rect {
            width: area.width.saturating_sub(1),
            ..area
        };
        let scroll_area = Rect {
            x: area.x + area.width.saturating_sub(1),
            width: 1,
            ..area
        };

        frame.render_stateful_widget(table, table_area, &mut self.table_state);

        let row_count = self.results.len();
        self.scroll_state = self.scroll_state.content_length(row_count);
        if let Some(sel) = self.table_state.selected() {
            self.scroll_state = self.scroll_state.position(sel);
        }
        frame.render_stateful_widget(
            Scrollbar::new(ScrollbarOrientation::VerticalRight),
            scroll_area,
            &mut self.scroll_state,
        );
    }

    fn render_input(&mut self, frame: &mut Frame, area: Rect) {
        let prompt_str = if self.in_continuation {
            &self.continuation_prompt
        } else {
            &self.prompt
        };

        let before_cursor = &self.input_buffer[..self.cursor_pos];
        let after_cursor = &self.input_buffer[self.cursor_pos..];

        let line = Line::from(vec![
            Span::styled(prompt_str.clone(), Style::default().fg(Color::Green)),
            Span::raw(before_cursor.to_string()),
            Span::styled(
                "_",
                Style::default()
                    .add_modifier(Modifier::RAPID_BLINK)
                    .fg(Color::White),
            ),
            Span::raw(after_cursor.to_string()),
        ]);

        let para =
            Paragraph::new(line).block(Block::default().borders(Borders::ALL).title("Query"));
        frame.render_widget(para, area);
    }

    /// Handle a key event. Returns Some(query) when Enter is pressed with non-empty input.
    pub fn handle_key(&mut self, keysym: u32, pressed: bool) -> Option<String> {
        if !pressed {
            return None;
        }

        match keysym {
            // Enter
            0xFF0D => {
                let query = self.input_buffer.trim().to_string();
                self.input_buffer.clear();
                self.cursor_pos = 0;
                if !query.is_empty() {
                    self.add_to_history(&query);
                    return Some(query);
                }
                None
            }
            // Backspace
            0xFF08 => {
                self.delete_char_before_cursor();
                None
            }
            // Escape
            0xFF1B => {
                self.input_buffer.clear();
                self.cursor_pos = 0;
                None
            }
            // Up arrow - history previous
            0xFF52 => {
                self.history_previous();
                None
            }
            // Down arrow - history next
            0xFF54 => {
                self.history_next();
                None
            }
            // Left arrow
            0xFF51 => {
                if self.cursor_pos > 0 {
                    self.cursor_pos -= 1;
                }
                None
            }
            // Right arrow
            0xFF53 => {
                if self.cursor_pos < self.input_buffer.len() {
                    self.cursor_pos += 1;
                }
                None
            }
            // Home / Ctrl+A
            0xFF50 | 0x0001 => {
                self.cursor_pos = 0;
                None
            }
            // End / Ctrl+E
            0xFF57 | 0x0005 => {
                self.cursor_pos = self.input_buffer.len();
                None
            }
            // Delete
            0xFFFF => {
                self.delete_char_at_cursor();
                None
            }
            // Ctrl+K - kill to end
            0x000B => {
                self.input_buffer.truncate(self.cursor_pos);
                None
            }
            // Ctrl+U - kill line
            0x0015 => {
                self.input_buffer.clear();
                self.cursor_pos = 0;
                None
            }
            // Ctrl+W - kill word
            0x0017 => {
                self.kill_word();
                None
            }
            // Ctrl+C
            0x0003 => {
                self.input_buffer.clear();
                self.cursor_pos = 0;
                None
            }
            // Page Up - scroll table up
            0xFF55 => {
                if !self.results.is_empty() {
                    let sel = self.table_state.selected().unwrap_or(0);
                    let new_sel = sel.saturating_sub(10);
                    self.table_state.select(Some(new_sel));
                }
                None
            }
            // Page Down - scroll table down
            0xFF56 => {
                if !self.results.is_empty() {
                    let sel = self.table_state.selected().unwrap_or(0);
                    let new_sel = (sel + 10).min(self.results.len().saturating_sub(1));
                    self.table_state.select(Some(new_sel));
                }
                None
            }
            // Regular printable character
            _ => {
                if let Some(c) = char::from_u32(keysym) {
                    if c.is_ascii() && !c.is_control() {
                        self.input_buffer.insert(self.cursor_pos, c);
                        self.cursor_pos += 1;
                    }
                }
                None
            }
        }
    }

    // --- History ---

    pub fn add_to_history(&mut self, command: &str) {
        if command.trim().is_empty() {
            return;
        }
        if self.history.back() == Some(&command.to_string()) {
            return;
        }
        self.history.push_back(command.to_string());
        if self.history.len() > self.history_max_size {
            self.history.pop_front();
        }
        self.history_idx = None;
        self.temp_buffer.clear();
    }

    fn history_previous(&mut self) {
        if self.history.is_empty() {
            return;
        }
        if self.history_idx.is_none() {
            self.temp_buffer = self.input_buffer.clone();
            self.history_idx = Some(self.history.len() - 1);
        } else if let Some(idx) = self.history_idx {
            if idx > 0 {
                self.history_idx = Some(idx - 1);
            } else {
                return;
            }
        }
        if let Some(idx) = self.history_idx {
            self.input_buffer = self.history[idx].clone();
            self.cursor_pos = self.input_buffer.len();
        }
    }

    fn history_next(&mut self) {
        if let Some(idx) = self.history_idx {
            if idx < self.history.len() - 1 {
                self.history_idx = Some(idx + 1);
                self.input_buffer = self.history[idx + 1].clone();
            } else {
                self.history_idx = None;
                self.input_buffer = self.temp_buffer.clone();
                self.temp_buffer.clear();
            }
            self.cursor_pos = self.input_buffer.len();
        }
    }

    // --- Editing ---

    fn delete_char_before_cursor(&mut self) {
        if self.cursor_pos > 0 {
            self.input_buffer.remove(self.cursor_pos - 1);
            self.cursor_pos -= 1;
        }
    }

    fn delete_char_at_cursor(&mut self) {
        if self.cursor_pos < self.input_buffer.len() {
            self.input_buffer.remove(self.cursor_pos);
        }
    }

    fn kill_word(&mut self) {
        if self.cursor_pos > 0 {
            let chars: Vec<char> = self.input_buffer.chars().collect();
            let mut pos = self.cursor_pos - 1;
            while pos > 0 && chars[pos].is_whitespace() {
                pos -= 1;
            }
            while pos > 0 && !chars[pos - 1].is_whitespace() {
                pos -= 1;
            }
            self.input_buffer.drain(pos..self.cursor_pos);
            self.cursor_pos = pos;
        }
    }
}
