use std::collections::VecDeque;

use guacr_terminal::QueryResult;
use ratatui::{
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span, Text},
    widgets::{
        Block, BorderType, Borders, Cell, Paragraph, Row, Scrollbar, ScrollbarOrientation,
        ScrollbarState, Table, TableState, Wrap,
    },
    Frame,
};

// Tab bar character widths for click detection (must match render_tab_bar spans)
// " Terminal " = 10 chars; " " separator = 1; " Grid View " starts at col 11
pub const TAB_TERMINAL_COLS: u32 = 11;

const SCROLLBACK_MAX: usize = 10_000;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ViewMode {
    Terminal,
    Grid,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AppFocus {
    Input,
    Results,
}

#[derive(Clone)]
pub enum ScrollbackLine {
    Command(String),
    Output(String),
    Error(String),
    Info(String),
}

pub struct DatabaseRatatuiApp {
    // Query results (Grid view state)
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

    // Focus state (Grid view)
    pub focus: AppFocus,

    // View mode + terminal scrollback
    pub view_mode: ViewMode,
    pub scrollback: VecDeque<ScrollbackLine>,
    pub scroll_offset: usize,

    // Feature flag: when false, tab bar is hidden and only Terminal view is available
    pub grid_view_enabled: bool,

    // Modifier key state — Guacamole sends Ctrl as a separate key event (0xFFE3/0xFFE4)
    // before the character key, not as a combined keysym. We track it to apply the
    // ctrl modifier ourselves.
    ctrl_pressed: bool,
}

impl DatabaseRatatuiApp {
    pub fn new(prompt: &str, continuation_prompt: &str, grid_view_enabled: bool) -> Self {
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
            focus: AppFocus::Input,
            view_mode: ViewMode::Terminal,
            scrollback: VecDeque::new(),
            scroll_offset: 0,
            grid_view_enabled,
            ctrl_pressed: false,
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

    /// Convert a char-index cursor position to a byte offset in `input_buffer`.
    ///
    /// cursor_pos is always a char count (number of Unicode codepoints from the
    /// start of the buffer). All string mutation methods require a byte offset,
    /// so this conversion is called at every insertion/deletion/slice site.
    fn cursor_byte_offset(&self) -> usize {
        self.input_buffer
            .char_indices()
            .nth(self.cursor_pos)
            .map(|(byte_idx, _)| byte_idx)
            .unwrap_or(self.input_buffer.len())
    }

    pub fn insert_clipboard_text(&mut self, text: &str) {
        let byte_offset = self.cursor_byte_offset();
        self.input_buffer.insert_str(byte_offset, text);
        self.cursor_pos += text.chars().count();
    }

    // --- Scrollback management ---

    fn push_scrollback(&mut self, line: ScrollbackLine) {
        self.scrollback.push_back(line);
        if self.scrollback.len() > SCROLLBACK_MAX {
            self.scrollback.pop_front();
        }
    }

    pub fn append_scrollback_command(&mut self, text: &str) {
        self.push_scrollback(ScrollbackLine::Command(text.to_string()));
        self.scroll_offset = 0;
    }

    pub fn append_scrollback_output(&mut self, text: &str) {
        self.push_scrollback(ScrollbackLine::Output(text.to_string()));
    }

    pub fn append_scrollback_error(&mut self, text: &str) {
        self.push_scrollback(ScrollbackLine::Error(text.to_string()));
        self.scroll_offset = 0;
    }

    pub fn append_scrollback_info(&mut self, text: &str) {
        self.push_scrollback(ScrollbackLine::Info(text.to_string()));
    }

    /// Format a QueryResult as ASCII table lines and append to scrollback.
    pub fn append_result_to_scrollback(&mut self, result: &QueryResult) {
        if result.columns.is_empty() {
            let msg = if let Some(n) = result.affected_rows {
                format!("Query OK, {} row(s) affected", n)
            } else {
                "Query executed successfully".to_string()
            };
            self.push_scrollback(ScrollbackLine::Info(msg));
        } else {
            let col_widths: Vec<usize> = result
                .columns
                .iter()
                .enumerate()
                .map(|(i, col)| {
                    let max_data = result
                        .rows
                        .iter()
                        .filter_map(|row| row.get(i))
                        .map(|v| v.len())
                        .max()
                        .unwrap_or(0);
                    col.len().max(max_data).min(40)
                })
                .collect();

            let sep: String = col_widths
                .iter()
                .map(|&w| format!("+{}", "-".repeat(w + 2)))
                .collect::<String>()
                + "+";

            let header: String = result
                .columns
                .iter()
                .enumerate()
                .map(|(i, col)| format!("| {:<width$} ", col, width = col_widths[i]))
                .collect::<String>()
                + "|";

            self.push_scrollback(ScrollbackLine::Output(sep.clone()));
            self.push_scrollback(ScrollbackLine::Output(header));
            self.push_scrollback(ScrollbackLine::Output(sep.clone()));

            for row in &result.rows {
                let row_line: String = row
                    .iter()
                    .enumerate()
                    .map(|(i, val)| {
                        let w = col_widths.get(i).copied().unwrap_or(10);
                        let display = if val.len() > w {
                            format!("{}...", &val[..w.saturating_sub(3)])
                        } else {
                            val.clone()
                        };
                        format!("| {:<width$} ", display, width = w)
                    })
                    .collect::<String>()
                    + "|";
                self.push_scrollback(ScrollbackLine::Output(row_line));
            }

            self.push_scrollback(ScrollbackLine::Output(sep));

            let row_label = if result.rows.len() == 1 {
                "1 row in set".to_string()
            } else {
                format!("{} rows in set", result.rows.len())
            };
            let row_label = if let Some(ms) = result.execution_time_ms {
                format!("{} ({:.2} sec)", row_label, ms as f64 / 1000.0)
            } else {
                row_label
            };
            self.push_scrollback(ScrollbackLine::Info(row_label));
        }
        self.scroll_offset = 0;
    }

    // --- Rendering ---

    /// Render the full UI into the given frame
    pub fn render(&mut self, frame: &mut Frame) {
        let area = frame.area();

        let in_terminal_mode = self.view_mode == ViewMode::Terminal || !self.grid_view_enabled;

        if in_terminal_mode {
            if self.grid_view_enabled {
                // Tab bar (1 row) + full-height terminal area with inline prompt
                let chunks = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([Constraint::Length(1), Constraint::Min(0)])
                    .split(area);
                self.render_tab_bar(frame, chunks[0]);
                self.render_terminal(frame, chunks[1]);
            } else {
                // No tab bar — plain terminal fills everything
                self.render_terminal(frame, area);
            }
        } else {
            // Grid view: tab bar + results table + query input box
            let content_rows = area.height.saturating_sub(4);
            let chunks = Layout::default()
                .direction(Direction::Vertical)
                .constraints([
                    Constraint::Length(1),
                    Constraint::Length(content_rows),
                    Constraint::Length(3),
                ])
                .split(area);
            self.render_tab_bar(frame, chunks[0]);
            self.render_results(frame, chunks[1]);
            self.render_input(frame, chunks[2]);
        }
    }

    fn render_tab_bar(&self, frame: &mut Frame, area: Rect) {
        let active = Style::default()
            .fg(Color::Black)
            .bg(Color::Cyan)
            .add_modifier(Modifier::BOLD);
        let inactive = Style::default().fg(Color::DarkGray);

        let (term_style, grid_style) = match self.view_mode {
            ViewMode::Terminal => (active, inactive),
            ViewMode::Grid => (inactive, active),
        };

        let line = Line::from(vec![
            Span::styled(" Terminal ", term_style),
            Span::raw(" "),
            Span::styled(" Grid View ", grid_style),
        ]);
        frame.render_widget(Paragraph::new(line), area);
    }

    fn render_terminal(&mut self, frame: &mut Frame, area: Rect) {
        let content_height = area.height as usize;
        let term_width = (area.width as usize).max(1);
        let n = self.scrollback.len();
        // Clamp stored scroll_offset to the actual scrollable range so that
        // Page Down always produces a visible change without needing to first
        // "burn through" excess offset accumulated by Page Up.
        let max_scroll = n.saturating_sub(content_height.saturating_sub(1));
        self.scroll_offset = self.scroll_offset.min(max_scroll);
        let show_prompt = self.scroll_offset == 0;

        // Helper: visual row count for one scrollback entry with wrapping.
        let visual_rows = |s: &str| -> usize {
            let len = s.chars().count();
            if len == 0 {
                1
            } else {
                len.div_ceil(term_width)
            }
        };

        let (start, end) = if show_prompt {
            // At the bottom: work backwards, fitting as many scrollback entries
            // as possible into (content_height - 1) rows, reserving 1 for prompt.
            let budget = content_height.saturating_sub(1);
            let mut used = 0usize;
            let mut start = n;
            for i in (0..n).rev() {
                let rows = match &self.scrollback[i] {
                    ScrollbackLine::Command(s)
                    | ScrollbackLine::Output(s)
                    | ScrollbackLine::Error(s)
                    | ScrollbackLine::Info(s) => visual_rows(s),
                };
                if used + rows > budget {
                    break;
                }
                used += rows;
                start = i;
            }
            (start, n)
        } else {
            // Scrolled into history: use line-count-based window.
            let rows = content_height;
            let max_scroll = n.saturating_sub(rows);
            let off = self.scroll_offset.min(max_scroll);
            let end = n.saturating_sub(off);
            (end.saturating_sub(rows), end)
        };

        let to_line = |sl: &ScrollbackLine| -> Line {
            match sl {
                ScrollbackLine::Command(s) => {
                    Line::from(Span::styled(s.clone(), Style::default().fg(Color::Green)))
                }
                ScrollbackLine::Output(s) => Line::from(Span::raw(s.clone())),
                ScrollbackLine::Error(s) => {
                    Line::from(Span::styled(s.clone(), Style::default().fg(Color::Red)))
                }
                ScrollbackLine::Info(s) => {
                    Line::from(Span::styled(s.clone(), Style::default().fg(Color::Gray)))
                }
            }
        };

        let mut lines: Vec<Line> = self
            .scrollback
            .iter()
            .skip(start)
            .take(end - start)
            .map(to_line)
            .collect();

        if !show_prompt {
            frame.render_widget(
                Paragraph::new(Text::from(lines)).wrap(Wrap { trim: false }),
                area,
            );
            return;
        }

        let prompt_str = if self.in_continuation {
            self.continuation_prompt.as_str()
        } else {
            self.prompt.as_str()
        };
        let byte_off = self.cursor_byte_offset();
        let before = &self.input_buffer[..byte_off];
        let after = &self.input_buffer[byte_off..];
        lines.push(Line::from(vec![
            Span::styled(prompt_str.to_string(), Style::default().fg(Color::Green)),
            Span::raw(before.to_string()),
            Span::styled(
                "_",
                Style::default()
                    .add_modifier(Modifier::SLOW_BLINK)
                    .fg(Color::White),
            ),
            Span::raw(after.to_string()),
        ]));

        frame.render_widget(
            Paragraph::new(Text::from(lines)).wrap(Wrap { trim: false }),
            area,
        );
    }

    fn render_results(&mut self, frame: &mut Frame, area: Rect) {
        let results_focused = self.focus == AppFocus::Results;

        // Reserve the panel's final row for the "Row X / Y" status bar.
        // `grid_clicked_data_row` in query_executor.rs derives the clickable band from the same
        // layout — change one and the other must follow.
        let table_area = Rect {
            height: area.height.saturating_sub(1),
            ..area
        };
        let status_area = Rect {
            y: area.y + table_area.height,
            height: 1,
            ..area
        };

        if self.columns.is_empty() {
            // No result set: nothing to count, so the panel keeps its full height.
            let block = if results_focused {
                Block::default()
                    .borders(Borders::ALL)
                    .border_type(BorderType::Double)
                    .border_style(Style::default().fg(Color::Cyan))
                    .title("Results [focused]")
            } else {
                Block::default().borders(Borders::ALL).title("Results")
            };
            let para = Paragraph::new(self.status_msg.clone())
                .block(block)
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
                let cells: Vec<Cell> = row
                    .iter()
                    .map(|val| {
                        let style = match val.as_str() {
                            "NULL" => Style::default()
                                .fg(Color::DarkGray)
                                .add_modifier(Modifier::ITALIC),
                            "true" => Style::default().fg(Color::Green),
                            "false" => Style::default().fg(Color::Red),
                            _ => Style::default(),
                        };
                        Cell::from(val.clone()).style(style)
                    })
                    .collect();
                Row::new(cells).height(1)
            })
            .collect();

        let col_count = self.columns.len().max(1);
        let constraints: Vec<Constraint> = (0..col_count)
            .map(|i| {
                let header_w = self.columns.get(i).map(|c| c.len()).unwrap_or(4);
                let data_w = self
                    .results
                    .iter()
                    .filter_map(|row| row.get(i))
                    .map(|v| v.len())
                    .max()
                    .unwrap_or(0);
                let natural = (header_w.max(data_w) + 2).clamp(6, 40) as u16;
                Constraint::Min(natural)
            })
            .collect();

        let base_title = if self.status_msg.is_empty() {
            "Results".to_string()
        } else {
            format!("Results - {}", self.status_msg)
        };
        let title = if results_focused {
            format!("{} [focused]", base_title)
        } else {
            base_title
        };

        let results_block = if results_focused {
            Block::default()
                .borders(Borders::ALL)
                .border_type(BorderType::Double)
                .border_style(Style::default().fg(Color::Cyan))
                .title(title)
        } else {
            Block::default().borders(Borders::ALL).title(title)
        };

        let table = Table::new(rows, constraints)
            .header(header)
            .block(results_block)
            .row_highlight_style(Style::default().add_modifier(Modifier::REVERSED))
            .style(Style::default().fg(Color::White));

        let table_render_area = Rect {
            width: table_area.width.saturating_sub(1),
            ..table_area
        };
        let scroll_area = Rect {
            x: table_area.x + table_area.width.saturating_sub(1),
            y: table_area.y,
            width: 1,
            height: table_area.height,
        };

        frame.render_stateful_widget(table, table_render_area, &mut self.table_state);

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

        // Render status bar
        let selected = self.table_state.selected().map(|s| s + 1).unwrap_or(0);
        let status_text = format!("Row {} / {}", selected, row_count);
        let status = Paragraph::new(status_text).style(Style::default().fg(Color::DarkGray));
        frame.render_widget(status, status_area);
    }

    fn render_input(&mut self, frame: &mut Frame, area: Rect) {
        let prompt_str = if self.in_continuation {
            &self.continuation_prompt
        } else {
            &self.prompt
        };

        let byte_off = self.cursor_byte_offset();
        let before_cursor = &self.input_buffer[..byte_off];
        let after_cursor = &self.input_buffer[byte_off..];

        let line = Line::from(vec![
            Span::styled(prompt_str.clone(), Style::default().fg(Color::Green)),
            Span::raw(before_cursor.to_string()),
            Span::styled(
                "_",
                Style::default()
                    .add_modifier(Modifier::SLOW_BLINK)
                    .fg(Color::White),
            ),
            Span::raw(after_cursor.to_string()),
        ]);

        let para = Paragraph::new(line)
            .block(Block::default().borders(Borders::ALL).title("Query"))
            .wrap(Wrap { trim: false });
        frame.render_widget(para, area);
    }

    /// Handle a key event. Returns Some(query) when Enter is pressed with non-empty input.
    pub fn handle_key(&mut self, keysym: u32, pressed: bool) -> Option<String> {
        // Modifier key tracking must happen before the !pressed early-return so
        // Ctrl-release (pressed=false) correctly clears ctrl_pressed.
        if matches!(keysym, 0xFFE3 | 0xFFE4) {
            self.ctrl_pressed = pressed;
            return None;
        }

        if !pressed {
            return None;
        }

        // Any key other than Page Up/Down snaps the view back to the bottom so the
        // user can see their input. Page Up/Down are the only intentional scroll keys.
        if !matches!(keysym, 0xFF55 | 0xFF56) {
            self.scroll_offset = 0;
        }

        match keysym {
            // Ctrl+G - toggle view mode (F5 is captured by browsers for page refresh)
            0x0007 => {
                if self.grid_view_enabled {
                    self.view_mode = match self.view_mode {
                        ViewMode::Terminal => ViewMode::Grid,
                        ViewMode::Grid => ViewMode::Terminal,
                    };
                }
                None
            }
            // Tab: Terminal → Grid/Input → Grid/Results → Terminal
            0xFF09 => match self.view_mode {
                ViewMode::Terminal => {
                    if self.grid_view_enabled {
                        self.view_mode = ViewMode::Grid;
                        self.focus = AppFocus::Input;
                    }
                    None
                }
                ViewMode::Grid => {
                    match self.focus {
                        AppFocus::Input => {
                            if !self.results.is_empty() {
                                self.focus = AppFocus::Results;
                                if self.table_state.selected().is_none() {
                                    self.table_state.select(Some(0));
                                }
                            } else {
                                // No results to tab into — go back to Terminal
                                self.view_mode = ViewMode::Terminal;
                            }
                        }
                        AppFocus::Results => {
                            // Wrap back to Terminal
                            self.view_mode = ViewMode::Terminal;
                            self.focus = AppFocus::Input;
                        }
                    }
                    None
                }
            },
            // Enter
            0xFF0D => {
                if self.view_mode == ViewMode::Grid && self.focus == AppFocus::Results {
                    self.focus = AppFocus::Input;
                    return None;
                }
                let query = self.input_buffer.trim().to_string();
                self.input_buffer.clear();
                self.cursor_pos = 0;
                // Always reset history navigation so Up always starts from the end,
                // even when add_to_history skips a duplicate and leaves history_idx set.
                self.history_idx = None;
                self.temp_buffer.clear();
                if !query.is_empty() {
                    self.add_to_history(&query);
                    return Some(query);
                }
                None
            }
            // Backspace
            0xFF08 => {
                if self.view_mode == ViewMode::Grid && self.focus == AppFocus::Results {
                    self.focus = AppFocus::Input;
                    return None;
                }
                self.delete_char_before_cursor();
                None
            }
            // Escape
            0xFF1B => {
                if self.view_mode == ViewMode::Grid && self.focus == AppFocus::Results {
                    self.focus = AppFocus::Input;
                    return None;
                }
                self.input_buffer.clear();
                self.cursor_pos = 0;
                None
            }
            // Up arrow
            0xFF52 => {
                if self.view_mode == ViewMode::Grid && self.focus == AppFocus::Results {
                    if !self.results.is_empty() {
                        let sel = self.table_state.selected().unwrap_or(0);
                        self.table_state.select(Some(sel.saturating_sub(1)));
                    }
                } else {
                    self.history_previous();
                }
                None
            }
            // Down arrow
            0xFF54 => {
                if self.view_mode == ViewMode::Grid && self.focus == AppFocus::Results {
                    if !self.results.is_empty() {
                        let sel = self.table_state.selected().unwrap_or(0);
                        let new_sel = (sel + 1).min(self.results.len().saturating_sub(1));
                        self.table_state.select(Some(new_sel));
                    }
                } else {
                    self.history_next();
                }
                None
            }
            // Left arrow
            0xFF51 => {
                if self.focus == AppFocus::Input && self.cursor_pos > 0 {
                    self.cursor_pos -= 1;
                }
                None
            }
            // Right arrow
            0xFF53 => {
                if self.focus == AppFocus::Input
                    && self.cursor_pos < self.input_buffer.chars().count()
                {
                    self.cursor_pos += 1;
                }
                None
            }
            // Home / Ctrl+A
            0xFF50 | 0x0001 => {
                if self.focus == AppFocus::Input {
                    self.cursor_pos = 0;
                }
                None
            }
            // End / Ctrl+E
            0xFF57 | 0x0005 => {
                if self.focus == AppFocus::Input {
                    self.cursor_pos = self.input_buffer.chars().count();
                }
                None
            }
            // Delete
            0xFFFF => {
                if self.view_mode == ViewMode::Grid && self.focus == AppFocus::Results {
                    self.focus = AppFocus::Input;
                    return None;
                }
                self.delete_char_at_cursor();
                None
            }
            // Ctrl+K - kill to end
            0x000B => {
                if self.focus == AppFocus::Input {
                    let byte_off = self.cursor_byte_offset();
                    self.input_buffer.truncate(byte_off);
                }
                None
            }
            // Ctrl+U - kill line
            0x0015 => {
                if self.focus == AppFocus::Input {
                    self.input_buffer.clear();
                    self.cursor_pos = 0;
                }
                None
            }
            // Ctrl+W - kill word
            0x0017 => {
                if self.focus == AppFocus::Input {
                    self.kill_word();
                }
                None
            }
            // Ctrl+C — cancel current input
            0x0003 => {
                if self.view_mode == ViewMode::Grid && self.focus == AppFocus::Results {
                    self.focus = AppFocus::Input;
                    return None;
                }
                self.input_buffer.clear();
                self.cursor_pos = 0;
                None
            }
            // Ctrl+D — quit (EOF, like real DB CLIs)
            0x0004 => {
                if pressed {
                    return Some("quit".to_string());
                }
                None
            }
            // Ctrl+L — clear screen / scroll to bottom
            0x000C => {
                if pressed {
                    self.scroll_offset = 0;
                }
                None
            }
            // Ctrl+V — paste is handled via clipboard instruction; absorb the keysym
            // so it doesn't fall through to the printable-char handler.
            0x0016 => None,
            // Page Up - scroll terminal up OR scroll grid table
            0xFF55 => {
                match self.view_mode {
                    ViewMode::Terminal => {
                        let max_offset = self.scrollback.len();
                        self.scroll_offset = (self.scroll_offset + 10).min(max_offset);
                    }
                    ViewMode::Grid => {
                        if !self.results.is_empty() {
                            let sel = self.table_state.selected().unwrap_or(0);
                            self.table_state.select(Some(sel.saturating_sub(10)));
                        }
                    }
                }
                None
            }
            // Page Down - scroll terminal down OR scroll grid table
            0xFF56 => {
                match self.view_mode {
                    ViewMode::Terminal => {
                        self.scroll_offset = self.scroll_offset.saturating_sub(10);
                    }
                    ViewMode::Grid => {
                        if !self.results.is_empty() {
                            let sel = self.table_state.selected().unwrap_or(0);
                            let new_sel = (sel + 10).min(self.results.len().saturating_sub(1));
                            self.table_state.select(Some(new_sel));
                        }
                    }
                }
                None
            }
            // Regular printable character — or ctrl+letter when ctrl_pressed is set.
            // Guacamole sends Ctrl as a separate key event (0xFFE3/0xFFE4), then the
            // character key. When ctrl_pressed is true, transform the character into
            // its control-character equivalent and re-dispatch.
            _ => {
                if self.ctrl_pressed && pressed {
                    // Apply Ctrl modifier: 'a'-'z' (0x61-0x7A) and 'A'-'Z' (0x41-0x5A)
                    // map to control chars 0x01-0x1A via keysym & 0x1F.
                    if (0x41..=0x5A).contains(&keysym) || (0x61..=0x7A).contains(&keysym) {
                        let ctrl_keysym = keysym & 0x1F;
                        return self.handle_key(ctrl_keysym, true);
                    }
                }
                if pressed {
                    if let Some(c) = char::from_u32(keysym) {
                        if c.is_ascii() && !c.is_control() {
                            self.focus = AppFocus::Input;
                            let byte_off = self.cursor_byte_offset();
                            self.input_buffer.insert(byte_off, c);
                            self.cursor_pos += 1;
                        }
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
            self.cursor_pos = self.input_buffer.chars().count();
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
            self.cursor_pos = self.input_buffer.chars().count();
        }
    }

    // --- Editing ---

    fn delete_char_before_cursor(&mut self) {
        if self.cursor_pos > 0 {
            // Convert the char index one position before cursor to a byte offset.
            let byte_off = self
                .input_buffer
                .char_indices()
                .nth(self.cursor_pos - 1)
                .map(|(b, _)| b)
                .unwrap_or(0);
            self.input_buffer.remove(byte_off);
            self.cursor_pos -= 1;
        }
    }

    fn delete_char_at_cursor(&mut self) {
        if self.cursor_pos < self.input_buffer.chars().count() {
            let byte_off = self.cursor_byte_offset();
            self.input_buffer.remove(byte_off);
        }
    }

    fn kill_word(&mut self) {
        if self.cursor_pos > 0 {
            // Work in char space (cursor_pos is a char count).
            let chars: Vec<char> = self.input_buffer.chars().collect();
            let mut pos = self.cursor_pos - 1;
            while pos > 0 && chars[pos].is_whitespace() {
                pos -= 1;
            }
            while pos > 0 && !chars[pos - 1].is_whitespace() {
                pos -= 1;
            }
            // Convert char positions to byte offsets for drain.
            let byte_start = self
                .input_buffer
                .char_indices()
                .nth(pos)
                .map(|(b, _)| b)
                .unwrap_or(0);
            let byte_end = self.cursor_byte_offset();
            self.input_buffer.drain(byte_start..byte_end);
            self.cursor_pos = pos;
        }
    }
}
