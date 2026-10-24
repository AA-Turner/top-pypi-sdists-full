// Shared data types for database and resource-browser UIs.
//
// DatabaseTerminal and SpreadsheetRenderer previously lived here; both have
// been replaced by ratatui-based implementations (DatabaseRatatuiApp and
// ResourceBrowserGrid respectively) and removed.

use std::borrow::Cow;
use std::cmp::Ordering;
use std::fmt;

/// Database column metadata, retained independently of its rendered header.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize)]
pub struct QueryColumn {
    pub name: String,
    pub data_type: String,
    pub nullable: bool,
    pub is_primary_key: bool,
}

impl From<String> for QueryColumn {
    fn from(name: String) -> Self {
        Self {
            name,
            data_type: String::new(),
            nullable: true,
            is_primary_key: false,
        }
    }
}

impl From<&str> for QueryColumn {
    fn from(name: &str) -> Self {
        name.to_owned().into()
    }
}

impl fmt::Display for QueryColumn {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.name)
    }
}

/// Native database values. Text is never interpreted as another variant.
#[derive(Debug, Clone, PartialEq, serde::Serialize)]
pub enum QueryCell {
    Null,
    Bool(bool),
    Int(i64),
    Float(f64),
    Text(String),
    Json(serde_json::Value),
    Blob(Vec<u8>),
}

impl From<String> for QueryCell {
    fn from(value: String) -> Self {
        Self::Text(value)
    }
}

impl From<&str> for QueryCell {
    fn from(value: &str) -> Self {
        Self::Text(value.to_owned())
    }
}

impl QueryCell {
    /// Full, lossless display text; text cells borrow their stored payload.
    pub fn display_text(&self) -> Cow<'_, str> {
        match self {
            Self::Null => Cow::Borrowed("NULL"),
            Self::Text(text) => Cow::Borrowed(text),
            _ => Cow::Owned(self.to_string()),
        }
    }

    /// Loaded-result ordering: NULL first, then booleans, numbers, text, JSON, blobs.
    /// Integers and floats share mathematical ordering without rounding integers.
    pub fn compare(&self, other: &Self) -> Ordering {
        fn rank(cell: &QueryCell) -> u8 {
            match cell {
                QueryCell::Null => 0,
                QueryCell::Bool(_) => 1,
                QueryCell::Int(_) | QueryCell::Float(_) => 2,
                QueryCell::Text(_) => 3,
                QueryCell::Json(_) => 4,
                QueryCell::Blob(_) => 5,
            }
        }
        fn int_float(integer: i64, float: f64) -> Ordering {
            if float.is_nan() {
                return if float.is_sign_negative() {
                    Ordering::Greater
                } else {
                    Ordering::Less
                };
            }
            if float >= 9_223_372_036_854_775_808.0 {
                return Ordering::Less;
            }
            if float < -9_223_372_036_854_775_808.0 {
                return Ordering::Greater;
            }
            match integer.cmp(&(float as i64)) {
                Ordering::Equal => (integer as f64).partial_cmp(&float).unwrap(),
                order => order,
            }
        }
        match (self, other) {
            (Self::Null, Self::Null) => Ordering::Equal,
            (Self::Bool(a), Self::Bool(b)) => a.cmp(b),
            (Self::Int(a), Self::Int(b)) => a.cmp(b),
            (Self::Float(a), Self::Float(b)) => {
                if a == b {
                    Ordering::Equal
                } else {
                    a.total_cmp(b)
                }
            }
            (Self::Int(a), Self::Float(b)) => int_float(*a, *b),
            (Self::Float(a), Self::Int(b)) => int_float(*b, *a).reverse(),
            (Self::Text(a), Self::Text(b)) => a.cmp(b),
            (Self::Json(a), Self::Json(b)) => a.to_string().cmp(&b.to_string()),
            (Self::Blob(a), Self::Blob(b)) => a.cmp(b),
            _ => rank(self).cmp(&rank(other)),
        }
    }
}

impl fmt::Display for QueryCell {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Null => f.write_str("NULL"),
            Self::Bool(value) => write!(f, "{value}"),
            Self::Int(value) => write!(f, "{value}"),
            Self::Float(value) => write!(f, "{value}"),
            Self::Text(value) => f.write_str(value),
            Self::Json(value) => write!(f, "{value}"),
            Self::Blob(bytes) => {
                f.write_str("0x")?;
                for byte in bytes {
                    write!(f, "{byte:02x}")?;
                }
                Ok(())
            }
        }
    }
}

/// Query result returned by all database handlers.
#[derive(Debug, Clone, Default, PartialEq)]
pub struct QueryResult {
    pub columns: Vec<QueryColumn>,
    pub rows: Vec<Vec<QueryCell>>,
    pub affected_rows: Option<u64>,
    pub execution_time_ms: Option<u64>,
    /// Total server-side rows, when reported; distinct from loaded row count.
    pub total_rows: Option<u64>,
    /// True when the server or a client limit omitted rows.
    pub truncated: bool,
}

impl QueryResult {
    pub fn new(columns: Vec<QueryColumn>) -> Self {
        Self {
            columns,
            ..Self::default()
        }
    }

    /// Explicit conversion for external APIs exposing only textual values.
    pub fn text(columns: Vec<String>, rows: Vec<Vec<String>>) -> Self {
        Self {
            columns: columns.into_iter().map(QueryColumn::from).collect(),
            rows: rows
                .into_iter()
                .map(|row| row.into_iter().map(QueryCell::Text).collect())
                .collect(),
            ..Self::default()
        }
    }

    pub fn add_row(&mut self, row: Vec<QueryCell>) {
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
