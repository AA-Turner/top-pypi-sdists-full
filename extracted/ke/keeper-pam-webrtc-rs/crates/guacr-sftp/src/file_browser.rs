// File browser UI renderer for SFTP
//
// Uses ratatui TestBackend as a layout engine and fontdue (via RatatuiRenderer)
// to produce a JPEG with real text — the same pipeline as the database handler.

use guacr_terminal::{RatatuiRenderer, TerminalError};
use ratatui::{
    layout::{Constraint, Direction, Layout},
    style::{Color, Modifier, Style},
    widgets::{
        Block, Borders, Cell, Paragraph, Row, Scrollbar, ScrollbarOrientation, ScrollbarState,
        Table, TableState,
    },
};

const CHAR_WIDTH: u32 = 9;
pub(crate) const CHAR_HEIGHT: u32 = 18;

// Ratatui layout (rows from top):
//   0-2  : path bar block (Constraint::Length(3))
//   3    : top border of file list block
//   4    : header row
//   5+   : data rows (one per file entry)
//   last : bottom border of file list block
//
// In pixels (CHAR_HEIGHT = 18):
//   0-53   : path bar
//   54-71  : top border of file list
//   72-89  : header row
//   90+    : data rows; data_row_n starts at pixel 90 + n*18
pub(crate) const DATA_ROW_PIXEL_START: u32 = 90; // first data row starts at this pixel Y

pub struct FileEntry {
    pub name: String,
    pub size: u64,
    pub is_directory: bool,
    pub permissions: String,
    pub modified: String,
}

pub struct FileBrowser {
    pub(crate) current_path: String,
    pub(crate) entries: Vec<FileEntry>,
    pub(crate) selected_index: Option<usize>,
    scroll_offset: usize,
}

impl FileBrowser {
    pub fn new(path: String, entries: Vec<FileEntry>) -> Self {
        Self {
            current_path: path,
            entries,
            selected_index: None,
            scroll_offset: 0,
        }
    }

    /// Render the file browser to a JPEG using ratatui + fontdue.
    ///
    /// Width and height are in pixels. Character cell size is fixed at 9x18.
    pub fn render_to_jpeg(&self, width: u32, height: u32) -> Result<Vec<u8>, TerminalError> {
        let cols = (width / CHAR_WIDTH).max(80) as u16;
        let rows = (height / CHAR_HEIGHT).max(24) as u16;

        let mut renderer = RatatuiRenderer::new(cols, rows, CHAR_WIDTH, CHAR_HEIGHT)?;

        // Build TableState for selection highlight (relative to scroll window)
        let mut table_state = TableState::default();
        if let Some(idx) = self.selected_index {
            if idx >= self.scroll_offset {
                table_state.select(Some(idx - self.scroll_offset));
            }
        }

        let current_path = &self.current_path;
        let entries = &self.entries;
        let scroll_offset = self.scroll_offset;

        renderer
            .terminal
            .draw(|f| {
                let area = f.area();

                let chunks = Layout::default()
                    .direction(Direction::Vertical)
                    .constraints([Constraint::Length(3), Constraint::Min(1)])
                    .split(area);

                // Path bar
                let path_para = Paragraph::new(current_path.as_str())
                    .block(Block::default().borders(Borders::ALL).title("Path"))
                    .style(Style::default().fg(Color::LightCyan));
                f.render_widget(path_para, chunks[0]);

                // Header row
                let header = Row::new(vec![
                    Cell::from("Type").style(
                        Style::default()
                            .fg(Color::LightCyan)
                            .add_modifier(Modifier::BOLD),
                    ),
                    Cell::from("Name").style(
                        Style::default()
                            .fg(Color::LightCyan)
                            .add_modifier(Modifier::BOLD),
                    ),
                    Cell::from("Size").style(
                        Style::default()
                            .fg(Color::LightCyan)
                            .add_modifier(Modifier::BOLD),
                    ),
                    Cell::from("Permissions").style(
                        Style::default()
                            .fg(Color::LightCyan)
                            .add_modifier(Modifier::BOLD),
                    ),
                    Cell::from("Modified").style(
                        Style::default()
                            .fg(Color::LightCyan)
                            .add_modifier(Modifier::BOLD),
                    ),
                ])
                .height(1);

                let rows: Vec<Row> = entries
                    .iter()
                    .skip(scroll_offset)
                    .map(|entry| {
                        let type_str = if entry.is_directory { "DIR" } else { "   " };
                        let size_str = if entry.is_directory {
                            "-".to_string()
                        } else {
                            format_size(entry.size)
                        };
                        let style = if entry.is_directory {
                            Style::default().fg(Color::LightBlue)
                        } else {
                            Style::default().fg(Color::White)
                        };
                        Row::new(vec![
                            Cell::from(type_str),
                            Cell::from(entry.name.clone()),
                            Cell::from(size_str),
                            Cell::from(entry.permissions.clone()),
                            Cell::from(entry.modified.clone()),
                        ])
                        .style(style)
                        .height(1)
                    })
                    .collect();

                let constraints = [
                    Constraint::Length(4),  // Type
                    Constraint::Min(20),    // Name
                    Constraint::Length(10), // Size
                    Constraint::Length(12), // Permissions
                    Constraint::Length(20), // Modified
                ];

                let table = Table::new(rows, constraints)
                    .header(header)
                    .block(Block::default().borders(Borders::ALL).title("Files"))
                    .row_highlight_style(
                        Style::default()
                            .bg(Color::DarkGray)
                            .add_modifier(Modifier::BOLD),
                    );

                // Leave one column for scrollbar
                let table_area = ratatui::layout::Rect {
                    width: chunks[1].width.saturating_sub(1),
                    ..chunks[1]
                };
                let scroll_area = ratatui::layout::Rect {
                    x: chunks[1].x + chunks[1].width.saturating_sub(1),
                    width: 1,
                    ..chunks[1]
                };

                f.render_stateful_widget(table, table_area, &mut table_state);

                let row_count = entries.len().saturating_sub(scroll_offset);
                let scroll_pos = self
                    .selected_index
                    .and_then(|i| i.checked_sub(scroll_offset))
                    .unwrap_or(0);
                let mut scroll_state = ScrollbarState::new(row_count).position(scroll_pos);
                f.render_stateful_widget(
                    Scrollbar::new(ScrollbarOrientation::VerticalRight),
                    scroll_area,
                    &mut scroll_state,
                );
            })
            .map_err(|e| TerminalError::RenderError(e.to_string()))?;

        renderer.render_to_jpeg(85)
    }

    /// Map a mouse click at pixel Y to a file entry and update selection.
    pub fn handle_click(&mut self, y: u32) {
        if y < DATA_ROW_PIXEL_START {
            return;
        }
        let data_row = ((y - DATA_ROW_PIXEL_START) / CHAR_HEIGHT) as usize;
        let index = data_row + self.scroll_offset;
        if index < self.entries.len() {
            self.selected_index = Some(index);
        }
    }

    pub fn get_selected(&self) -> Option<&FileEntry> {
        self.selected_index.and_then(|i| self.entries.get(i))
    }
}

pub(crate) fn format_size(bytes: u64) -> String {
    if bytes < 1024 {
        format!("{} B", bytes)
    } else if bytes < 1024 * 1024 {
        format!("{:.1} KB", bytes as f64 / 1024.0)
    } else if bytes < 1024 * 1024 * 1024 {
        format!("{:.1} MB", bytes as f64 / (1024.0 * 1024.0))
    } else {
        format!("{:.1} GB", bytes as f64 / (1024.0 * 1024.0 * 1024.0))
    }
}
