// Shared data types for database and resource-browser UIs.
//
// DatabaseTerminal and SpreadsheetRenderer previously lived here; both have
// been replaced by ratatui-based implementations (DatabaseRatatuiApp and
// ResourceBrowserGrid respectively) and removed.

/// Query result returned by all database handlers.
#[derive(Debug, Clone, Default)]
pub struct QueryResult {
    pub columns: Vec<String>,
    pub rows: Vec<Vec<String>>,
    pub affected_rows: Option<u64>,
    pub execution_time_ms: Option<u64>,
}

impl QueryResult {
    pub fn new(columns: Vec<String>) -> Self {
        Self {
            columns,
            rows: Vec::new(),
            affected_rows: None,
            execution_time_ms: None,
        }
    }

    pub fn add_row(&mut self, row: Vec<String>) {
        self.rows.push(row);
    }

    pub fn is_empty(&self) -> bool {
        self.rows.is_empty()
    }

    pub fn row_count(&self) -> usize {
        self.rows.len()
    }
}

/// Column alignment for resource-browser grids.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Alignment {
    Left,
    Right,
    Center,
}

/// Column definition for resource-browser grids.
#[derive(Debug, Clone)]
pub struct ColumnDef {
    pub name: String,
    /// Width in characters (0 = auto).
    pub width_chars: usize,
    pub alignment: Alignment,
}

impl ColumnDef {
    /// Left-aligned column with auto width.
    pub fn new(name: &str) -> Self {
        Self {
            name: name.to_string(),
            width_chars: 0,
            alignment: Alignment::Left,
        }
    }

    /// Column with explicit width and alignment.
    pub fn with_width(name: &str, width_chars: usize, alignment: Alignment) -> Self {
        Self {
            name: name.to_string(),
            width_chars,
            alignment,
        }
    }
}

/// Per-row action shown in the resource-browser action bar.
#[derive(Debug, Clone)]
pub struct Action {
    pub label: String,
    pub shortcut: Option<char>,
    pub id: String,
}

impl Action {
    pub fn new(label: &str, shortcut: Option<char>, id: &str) -> Self {
        Self {
            label: label.to_string(),
            shortcut,
            id: id.to_string(),
        }
    }
}

/// Interaction mode for resource-browser keyboard state machine.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GridMode {
    /// Arrow keys navigate rows.
    Browse,
    /// Tab cycles through action buttons.
    ActionBar,
}

/// Events produced by resource-browser input handling.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GridEvent {
    /// No visual change needed.
    None,
    /// Grid content changed, needs re-render.
    Redraw,
    /// User triggered an action on a row.
    ActionTriggered { row: usize, action_id: String },
    /// User selected a specific cell.
    CellSelected {
        row: usize,
        col: usize,
        value: String,
    },
}
