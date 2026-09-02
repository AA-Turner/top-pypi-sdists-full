//! 3270 Screen Buffer Model.
//!
//! Implements the 24x80 (or alternate size) character grid used by IBM 3270
//! terminals. The screen is a linear buffer of cells, each containing an
//! EBCDIC character and display attributes. Fields are defined by Start Field
//! (SF) orders and span from one field attribute to the next.
//!
//! The buffer address wraps around: after the last position, it continues
//! from position 0.

use crate::datastream::{
    Aid, Color3270, DataStream, DataStreamItem, ExtendedAttribute, FieldAttribute, Highlighting,
    Intensity, Order, Wcc, WriteCommand,
};
use crate::ebcdic::{self, CodePage, EBCDIC_SPACE};

/// Display attributes for a single cell, including extended color and
/// highlighting information.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CellAttribute {
    /// Foreground color (from SA or SFE orders).
    pub foreground: Color3270,
    /// Background color (from SA or SFE orders).
    pub background: Color3270,
    /// Extended highlighting mode.
    pub highlight: Highlight3270,
    /// If this cell is a field attribute position, the field attribute byte.
    /// Field attribute positions display as blanks on a real 3270 terminal.
    pub field_attribute: Option<FieldAttribute>,
}

/// Highlight modes for screen cells (mirrors the extended highlighting attribute).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Highlight3270 {
    Normal,
    Blink,
    ReverseVideo,
    Underscore,
    Intensified,
}

impl Default for CellAttribute {
    fn default() -> Self {
        CellAttribute {
            foreground: Color3270::Default,
            background: Color3270::Default,
            highlight: Highlight3270::Normal,
            field_attribute: None,
        }
    }
}

impl From<Highlighting> for Highlight3270 {
    fn from(h: Highlighting) -> Self {
        match h {
            Highlighting::Default => Highlight3270::Normal,
            Highlighting::Blink => Highlight3270::Blink,
            Highlighting::ReverseVideo => Highlight3270::ReverseVideo,
            Highlighting::Underscore => Highlight3270::Underscore,
            Highlighting::Intensified => Highlight3270::Intensified,
        }
    }
}

/// A single cell in the 3270 screen buffer.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Cell {
    /// The Unicode character displayed in this cell.
    pub character: char,
    /// Display attributes for this cell.
    pub attribute: CellAttribute,
}

impl Default for Cell {
    fn default() -> Self {
        Cell {
            character: ' ',
            attribute: CellAttribute::default(),
        }
    }
}

/// A field on the 3270 screen, defined by a Start Field (SF) order.
///
/// Fields span from the position after a field attribute to just before
/// the next field attribute (or wrapping around the buffer).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Field {
    /// Buffer position of the field attribute byte.
    pub start: u16,
    /// Buffer position of the last data cell in this field (inclusive).
    /// If the field wraps, end < start.
    pub end: u16,
    /// The field attribute.
    pub attribute: FieldAttribute,
    /// Whether this field has been modified by the user since the last
    /// reset-MDT command.
    pub modified: bool,
}

/// The 3270 screen buffer.
///
/// Models the full terminal display as a linear array of cells. Standard
/// screen sizes are 24x80 (Model 2), 32x80 (Model 3), 43x80 (Model 4),
/// and 27x132 (Model 5).
pub struct ScreenBuffer {
    /// Number of rows.
    rows: u16,
    /// Number of columns.
    cols: u16,
    /// Linear buffer of cells (rows * cols entries).
    pub(crate) buffer: Vec<Cell>,
    /// Write address used during data stream processing (advances with each written character).
    /// Do NOT use this for interactive cursor operations — use `display_cursor` instead.
    pub(crate) cursor_position: u16,
    /// Interactive cursor position — the cell shown to the user and used for keyboard input.
    /// Set by the IC (Insert Cursor) order in a data stream; updated by arrow keys / Tab.
    pub(crate) display_cursor: u16,
    /// The code page used for EBCDIC decoding.
    code_page: CodePage,
    /// Current Set Attribute (SA) state - foreground color.
    current_fg: Color3270,
    /// Current Set Attribute (SA) state - background color.
    current_bg: Color3270,
    /// Current Set Attribute (SA) state - highlighting.
    current_highlight: Highlight3270,
}

/// Maximum value for rows or cols. 255 * 255 = 65025, which fits in u16.
/// 256 * 256 = 65536 wraps to 0 as u16, causing divide-by-zero panics in
/// any code that uses `% size()`. Cap both dimensions to prevent overflow.
const MAX_SCREEN_DIM: u16 = 255;

impl ScreenBuffer {
    /// Create a new screen buffer with the given dimensions.
    ///
    /// Common sizes: 24x80 (standard), 32x80, 43x80, 27x132.
    ///
    /// Rows and cols are each capped at 255 to prevent u16 overflow in `size()`.
    pub fn new(rows: u16, cols: u16) -> Self {
        let rows = rows.min(MAX_SCREEN_DIM);
        let cols = cols.min(MAX_SCREEN_DIM);
        let size = rows as usize * cols as usize;
        ScreenBuffer {
            rows,
            cols,
            buffer: vec![Cell::default(); size],
            cursor_position: 0,
            display_cursor: 0,
            code_page: CodePage::Cp037,
            current_fg: Color3270::Default,
            current_bg: Color3270::Default,
            current_highlight: Highlight3270::Normal,
        }
    }

    /// Create a new screen buffer with a specified code page.
    pub fn with_code_page(rows: u16, cols: u16, code_page: CodePage) -> Self {
        let mut screen = Self::new(rows, cols);
        screen.code_page = code_page;
        screen
    }

    /// Total number of buffer positions.
    pub fn size(&self) -> u16 {
        self.rows * self.cols
    }

    /// Number of rows.
    pub fn rows(&self) -> u16 {
        self.rows
    }

    /// Number of columns.
    pub fn cols(&self) -> u16 {
        self.cols
    }

    /// Get the interactive cursor position (set by IC order, updated by keyboard input).
    pub fn cursor_pos(&self) -> u16 {
        self.display_cursor
    }

    /// Get the current write address used during data stream processing.
    /// Only needed for tests that verify data stream write positioning.
    #[cfg(test)]
    pub(crate) fn write_pos(&self) -> u16 {
        self.cursor_position
    }

    /// Get the cursor position as (row, col).
    pub fn cursor_row_col(&self) -> (u16, u16) {
        (
            self.display_cursor / self.cols,
            self.display_cursor % self.cols,
        )
    }

    /// Get a reference to the cell at the given (row, col).
    ///
    /// Returns None if row or col is out of range.
    pub fn get_cell(&self, row: u16, col: u16) -> Option<&Cell> {
        if row < self.rows && col < self.cols {
            let idx = (row as usize) * (self.cols as usize) + (col as usize);
            Some(&self.buffer[idx])
        } else {
            None
        }
    }

    /// Get a reference to the cell at a linear buffer address.
    pub fn get_cell_at(&self, pos: u16) -> &Cell {
        &self.buffer[pos as usize % self.buffer.len()]
    }

    /// Clear the entire screen buffer to spaces with default attributes.
    pub fn clear(&mut self) {
        for cell in &mut self.buffer {
            *cell = Cell::default();
        }
        self.cursor_position = 0;
        self.display_cursor = 0;
        self.reset_sa_state();
    }

    /// Reset the current SA (Set Attribute) state to defaults.
    fn reset_sa_state(&mut self) {
        self.current_fg = Color3270::Default;
        self.current_bg = Color3270::Default;
        self.current_highlight = Highlight3270::Normal;
    }

    /// Advance the buffer address by one position, wrapping at the end.
    pub(crate) fn advance(&mut self) {
        self.cursor_position = (self.cursor_position + 1) % self.size();
    }

    /// Write a character at the current buffer position and advance.
    fn write_char(&mut self, ebcdic_byte: u8) {
        let ch = ebcdic::ebcdic_to_unicode(ebcdic_byte, self.code_page);
        let pos = self.cursor_position as usize;
        self.buffer[pos].character = ch;
        self.buffer[pos].attribute.foreground = self.current_fg;
        self.buffer[pos].attribute.background = self.current_bg;
        self.buffer[pos].attribute.highlight = self.current_highlight;
        // Preserve field_attribute if this position has one
        self.advance();
    }

    /// Process a WCC (Write Control Character).
    fn apply_wcc(&mut self, wcc: &Wcc) {
        if wcc.reset_mdt {
            // Reset the MDT bit on all field attribute positions
            for cell in &mut self.buffer {
                if let Some(ref mut fa) = cell.attribute.field_attribute {
                    fa.modified = false;
                }
            }
        }
        // restore_keyboard and alarm are handled by the caller (UI layer)
    }

    /// Apply a complete data stream to the screen buffer.
    ///
    /// Processes the write command, WCC, and all orders/characters in sequence.
    pub fn apply_data_stream(&mut self, stream: &DataStream) {
        // Handle erase commands
        match stream.command {
            WriteCommand::EraseWrite | WriteCommand::EraseWriteAlternate => {
                self.clear();
            }
            WriteCommand::Write => {
                // No erase, write to current buffer content
            }
            WriteCommand::WriteStructuredField => {
                // WSF data is handled differently (structured fields)
                // For now, store raw data as characters (basic support)
            }
        }

        // Apply WCC
        self.apply_wcc(&stream.wcc);

        // Reset SA state at the start of a data stream
        self.reset_sa_state();

        // Track whether the data stream explicitly positioned the display cursor
        // via an IC (Insert Cursor) order. If not, we'll default to the first
        // unprotected field after processing.
        let cursor_before = self.display_cursor;

        // Process each item in the data stream
        for item in &stream.orders {
            match item {
                DataStreamItem::Order(order) => self.apply_order(order),
                DataStreamItem::Character(byte) => self.write_char(*byte),
            }
        }

        // If no IC order moved the display cursor, tab forward to the first
        // unprotected input field. Many legacy 3270 screens omit IC (e.g. Hercules
        // TK4- VTAM messages), leaving display_cursor at 0 which is almost always
        // a protected field attribute byte.
        if self.display_cursor == cursor_before {
            self.tab_forward();
        }
    }

    /// Apply a single order to the screen buffer.
    fn apply_order(&mut self, order: &Order) {
        match order {
            Order::Sba(addr) => {
                self.cursor_position = *addr % self.size();
            }
            Order::Sf(attr) => {
                // Place the field attribute at the current position.
                // The field attribute position displays as a blank.
                let pos = self.cursor_position as usize;
                self.buffer[pos].character = ' ';
                self.buffer[pos].attribute.field_attribute = Some(*attr);
                self.buffer[pos].attribute.foreground = Color3270::Default;
                self.buffer[pos].attribute.background = Color3270::Default;
                self.buffer[pos].attribute.highlight = Highlight3270::Normal;
                self.advance();
            }
            Order::Sfe(attrs) => {
                // Start Field Extended: set field attribute with extended attrs
                let pos = self.cursor_position as usize;
                self.buffer[pos].character = ' ';
                let mut fa = FieldAttribute {
                    protected: false,
                    numeric: false,
                    intensity: Intensity::Normal,
                    modified: false,
                };
                for ea in attrs {
                    match ea {
                        ExtendedAttribute::FieldAttribute(a) => fa = *a,
                        ExtendedAttribute::ForegroundColor(c) => {
                            self.buffer[pos].attribute.foreground = *c;
                        }
                        ExtendedAttribute::BackgroundColor(c) => {
                            self.buffer[pos].attribute.background = *c;
                        }
                        ExtendedAttribute::Highlighting(h) => {
                            self.buffer[pos].attribute.highlight = (*h).into();
                        }
                        _ => {}
                    }
                }
                self.buffer[pos].attribute.field_attribute = Some(fa);
                self.advance();
            }
            Order::Sa(attr) => {
                // Set Attribute: change the current character attribute state
                // (does not create a field, does not occupy a buffer position)
                match attr {
                    ExtendedAttribute::ForegroundColor(c) => self.current_fg = *c,
                    ExtendedAttribute::BackgroundColor(c) => self.current_bg = *c,
                    ExtendedAttribute::Highlighting(h) => {
                        self.current_highlight = (*h).into();
                    }
                    _ => {}
                }
            }
            Order::Ic => {
                // Insert Cursor: mark the current write address as the display cursor.
                // cursor_position tracks the write address; display_cursor tracks where
                // the user's interactive cursor should appear and keyboard input lands.
                self.display_cursor = self.cursor_position;
            }
            Order::Pt => {
                // Program Tab: advance to the next unprotected field.
                self.tab_forward();
            }
            Order::Ra(addr, ch) => {
                // Repeat to Address: fill from current position to addr with ch
                let target = *addr % self.size();
                loop {
                    if self.cursor_position == target {
                        break;
                    }
                    self.write_char(*ch);
                }
            }
            Order::Eua(addr) => {
                // Erase Unprotected to Address: clear unprotected cells to addr
                let target = *addr % self.size();
                loop {
                    if self.cursor_position == target {
                        break;
                    }
                    let pos = self.cursor_position as usize;
                    // Only clear if the cell is in an unprotected field
                    if !self.is_protected(self.cursor_position) {
                        self.buffer[pos].character = ' ';
                    }
                    self.advance();
                }
            }
            Order::Mf(attrs) => {
                // Modify Field: modify attributes of the field at current position
                let pos = self.cursor_position as usize;
                for ea in attrs {
                    match ea {
                        ExtendedAttribute::FieldAttribute(a) => {
                            self.buffer[pos].attribute.field_attribute = Some(*a);
                        }
                        ExtendedAttribute::ForegroundColor(c) => {
                            self.buffer[pos].attribute.foreground = *c;
                        }
                        ExtendedAttribute::BackgroundColor(c) => {
                            self.buffer[pos].attribute.background = *c;
                        }
                        ExtendedAttribute::Highlighting(h) => {
                            self.buffer[pos].attribute.highlight = (*h).into();
                        }
                        _ => {}
                    }
                }
            }
        }
    }

    /// Check if a buffer position is in a protected field.
    fn is_protected(&self, pos: u16) -> bool {
        // Walk backward from pos to find the governing field attribute
        let size = self.size();
        let mut check = pos;
        for _ in 0..size {
            if let Some(fa) = &self.buffer[check as usize].attribute.field_attribute {
                return fa.protected;
            }
            if check == 0 {
                check = size - 1;
            } else {
                check -= 1;
            }
        }
        // No field attributes found: default is unprotected
        false
    }

    /// Get all fields currently defined on the screen.
    ///
    /// Returns fields in screen order. Each field starts at the position
    /// after the field attribute byte and extends to just before the next
    /// field attribute byte.
    pub fn get_fields(&self) -> Vec<Field> {
        let size = self.size();
        let mut fa_positions: Vec<(u16, FieldAttribute)> = Vec::new();

        // Collect all field attribute positions
        for i in 0..size {
            if let Some(fa) = &self.buffer[i as usize].attribute.field_attribute {
                fa_positions.push((i, *fa));
            }
        }

        if fa_positions.is_empty() {
            return Vec::new();
        }

        let mut fields = Vec::with_capacity(fa_positions.len());
        for (idx, &(start_pos, ref attr)) in fa_positions.iter().enumerate() {
            let next_idx = (idx + 1) % fa_positions.len();
            let next_start = fa_positions[next_idx].0;

            // The field's data area starts at start_pos + 1 (after the attribute byte).
            // It ends just before the next field attribute.
            let end = if next_start == 0 {
                size - 1
            } else {
                next_start - 1
            };

            fields.push(Field {
                start: start_pos,
                end,
                attribute: *attr,
                modified: attr.modified,
            });
        }

        fields
    }

    /// Get the field containing the given buffer position, if any.
    pub fn get_field_at(&self, pos: u16) -> Option<Field> {
        let fields = self.get_fields();
        for field in &fields {
            if field.start <= field.end {
                // Non-wrapping field
                if pos >= field.start && pos <= field.end {
                    return Some(field.clone());
                }
            } else {
                // Wrapping field
                if pos >= field.start || pos <= field.end {
                    return Some(field.clone());
                }
            }
        }
        None
    }

    /// Move the cursor to the next unprotected field.
    ///
    /// Scans forward from the current cursor position looking for an
    /// unprotected field. If found, positions the cursor at the first
    /// data position of that field.
    pub fn tab_forward(&mut self) {
        let size = self.size();
        let start = self.display_cursor;
        let mut pos = (start + 1) % size;

        for _ in 0..size {
            if let Some(fa) = &self.buffer[pos as usize].attribute.field_attribute {
                if !fa.protected {
                    self.display_cursor = (pos + 1) % size;
                    return;
                }
            }
            pos = (pos + 1) % size;
        }
    }

    /// Move the cursor to the previous unprotected field.
    ///
    /// Scans backward from the current cursor position.
    pub fn tab_backward(&mut self) {
        let size = self.size();
        let start = self.display_cursor;
        let mut pos = if start == 0 { size - 1 } else { start - 1 };

        for _ in 0..size {
            if let Some(fa) = &self.buffer[pos as usize].attribute.field_attribute {
                if !fa.protected {
                    let data_start = (pos + 1) % size;
                    if data_start != start {
                        self.display_cursor = data_start;
                        return;
                    }
                }
            }
            if pos == 0 {
                pos = size - 1;
            } else {
                pos -= 1;
            }
        }
    }

    /// Generate a Read Modified response for the current screen state.
    ///
    /// The Read Modified response is sent from the terminal to the host and
    /// contains:
    /// 1. AID byte
    /// 2. Cursor address (2 bytes)
    /// 3. For each modified unprotected field: SBA + field data
    ///
    /// PA keys (PA1-PA3) and Clear send only the AID + cursor address
    /// (short read modified).
    pub fn read_modified_fields(&self, aid: Aid) -> Vec<u8> {
        let mut response = Vec::new();

        // AID byte
        response.push(aid.to_byte());

        // Cursor address uses the interactive cursor, not the write position.
        let (cb1, cb2) = crate::datastream::encode_buffer_address(self.display_cursor);
        response.push(cb1);
        response.push(cb2);

        // PA keys and Clear only send AID + cursor (short read modified)
        match aid {
            Aid::Pa(_) | Aid::Clear => return response,
            _ => {}
        }

        // For each modified field, send SBA + field data
        let size = self.size() as usize;
        let fields = self.get_fields();

        for field in &fields {
            if field.attribute.protected || !field.modified {
                continue;
            }

            // SBA order pointing to the first data position of this field
            let data_start = ((field.start as usize + 1) % size) as u16;
            let (b1, b2) = crate::datastream::encode_buffer_address(data_start);
            response.push(0x11); // SBA order
            response.push(b1);
            response.push(b2);

            // Field data (EBCDIC bytes)
            let mut pos = data_start;
            loop {
                let cell = &self.buffer[pos as usize];
                // Stop if we hit another field attribute
                if pos != data_start && cell.attribute.field_attribute.is_some() {
                    break;
                }
                // Convert character back to EBCDIC
                let ebcdic = ebcdic::unicode_to_ebcdic(cell.character, self.code_page)
                    .unwrap_or(EBCDIC_SPACE);
                response.push(ebcdic);
                pos = ((pos as usize + 1) % size) as u16;
                if pos == data_start {
                    break; // wrapped around
                }
            }
        }

        response
    }

    /// Set a field's MDT (Modified Data Tag) flag.
    ///
    /// Called when the user types into a field.
    pub fn set_field_modified(&mut self, field_attr_pos: u16) {
        if let Some(ref mut fa) = self.buffer[field_attr_pos as usize]
            .attribute
            .field_attribute
        {
            fa.modified = true;
        }
    }

    /// Get the text content of a row as a Unicode string.
    ///
    /// Field attribute positions are rendered as spaces.
    pub fn get_row_text(&self, row: u16) -> String {
        if row >= self.rows {
            return String::new();
        }
        let start = (row as usize) * (self.cols as usize);
        let end = start + self.cols as usize;
        self.buffer[start..end]
            .iter()
            .map(|cell| {
                if cell.attribute.field_attribute.is_some() {
                    ' '
                } else {
                    cell.character
                }
            })
            .collect()
    }

    /// Get the full screen content as a multi-line string.
    pub fn get_screen_text(&self) -> String {
        let mut lines = Vec::with_capacity(self.rows as usize);
        for row in 0..self.rows {
            lines.push(self.get_row_text(row));
        }
        lines.join("\n")
    }

    /// Move the interactive cursor to an absolute linear position.
    ///
    /// Wraps at `size()`. Used by keyboard handlers for arrow-key navigation.
    pub fn set_cursor_position(&mut self, pos: u16) {
        let size = self.size();
        if size > 0 {
            self.display_cursor = pos % size;
        }
    }

    /// Delete (clear) the character at the current cursor position.
    ///
    /// Only clears the cell if it is in an unprotected field; protected cells
    /// are left unchanged. Returns `true` if the cell was cleared.
    pub fn delete_at_cursor(&mut self) -> bool {
        if self.is_protected(self.display_cursor) {
            return false;
        }
        let pos = self.display_cursor as usize;
        self.buffer[pos].character = ' ';
        true
    }

    /// Input a character at the current cursor position.
    ///
    /// Only works if the cursor is in an unprotected field. Returns true
    /// if the character was accepted, false if the field is protected.
    pub fn input_char(&mut self, ch: char) -> bool {
        if self.is_protected(self.display_cursor) {
            return false;
        }

        // Find the governing field attribute and set its MDT
        let size = self.size();
        let mut check = self.display_cursor;
        for _ in 0..size {
            if self.buffer[check as usize]
                .attribute
                .field_attribute
                .is_some()
            {
                self.set_field_modified(check);
                break;
            }
            if check == 0 {
                check = size - 1;
            } else {
                check -= 1;
            }
        }

        let pos = self.display_cursor as usize;
        self.buffer[pos].character = ch;
        self.display_cursor = (self.display_cursor + 1) % self.size();
        true
    }
}
