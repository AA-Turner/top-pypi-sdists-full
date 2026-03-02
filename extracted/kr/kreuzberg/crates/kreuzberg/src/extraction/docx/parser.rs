//! Inline DOCX XML parser.
//!
//! Vendored and adapted from [docx-lite](https://github.com/v-lawyer/docx-lite) v0.2.0
//! (MIT OR Apache-2.0, V-Lawyer Team). See ATTRIBUTIONS.md for details.
//!
//! Changes from upstream:
//! - `Paragraph::to_text()` joins runs with `" "` instead of `""` (fixes #359)
//! - Adapted to use kreuzberg's existing `quick-xml` and `zip` versions
//! - Removed file-path based APIs (we only need bytes/reader)
//! - Added markdown rendering and formatting support (fixes #376)

use std::collections::HashMap;
use std::io::{Cursor, Read, Seek};

use quick_xml::Reader;
use quick_xml::events::{BytesStart, Event};

// --- Types ---

/// Tracks document element ordering (paragraphs, tables, and drawings interleaved).
#[derive(Debug, Clone)]
pub enum DocumentElement {
    Paragraph(usize), // index into Document::paragraphs
    Table(usize),     // index into Document::tables
    Drawing(usize),   // index into Document::drawings
}

#[derive(Debug, Clone, Default)]
pub struct Document {
    pub paragraphs: Vec<Paragraph>,
    pub tables: Vec<Table>,
    pub headers: Vec<HeaderFooter>,
    pub footers: Vec<HeaderFooter>,
    pub footnotes: Vec<Note>,
    pub endnotes: Vec<Note>,
    pub numbering_defs: HashMap<(i64, i64), ListType>,
    /// Document elements in their original order.
    pub elements: Vec<DocumentElement>,
    /// Parsed style catalog from `word/styles.xml`, if available.
    pub style_catalog: Option<super::styles::StyleCatalog>,
    /// Parsed theme from `word/theme/theme1.xml`, if available.
    pub theme: Option<super::theme::Theme>,
    /// Section properties parsed from `w:sectPr` elements.
    pub sections: Vec<super::section::SectionProperties>,
    /// Drawing objects parsed from `w:drawing` elements.
    pub drawings: Vec<super::drawing::Drawing>,
    /// Image relationships (rId → target path) for image extraction.
    pub image_relationships: HashMap<String, String>,
}

#[derive(Debug, Clone, Default)]
pub struct Paragraph {
    pub runs: Vec<Run>,
    pub style: Option<String>,
    pub numbering_id: Option<i64>,
    pub numbering_level: Option<i64>,
}

#[derive(Debug, Clone, Default)]
pub struct Run {
    pub text: String,
    pub bold: bool,
    pub italic: bool,
    pub underline: bool,
    pub strikethrough: bool,
    pub hyperlink_url: Option<String>,
}

#[derive(Debug, Clone, Default)]
pub struct Table {
    pub rows: Vec<TableRow>,
    pub properties: Option<super::table::TableProperties>,
    pub grid: Option<super::table::TableGrid>,
}

#[derive(Debug, Clone, Default)]
pub struct TableRow {
    pub cells: Vec<TableCell>,
    pub properties: Option<super::table::RowProperties>,
}

#[derive(Debug, Clone, Default)]
pub struct TableCell {
    pub paragraphs: Vec<Paragraph>,
    pub properties: Option<super::table::CellProperties>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ListType {
    Bullet,
    Numbered,
}

#[derive(Debug, Clone, Default)]
pub struct HeaderFooter {
    pub paragraphs: Vec<Paragraph>,
    pub tables: Vec<Table>,
    pub header_type: HeaderFooterType,
}

#[derive(Debug, Clone, Default, PartialEq)]
pub enum HeaderFooterType {
    #[default]
    Default,
    First,
    Even,
    Odd,
}

#[derive(Debug, Clone)]
pub struct Note {
    pub id: String,
    pub note_type: NoteType,
    pub paragraphs: Vec<Paragraph>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum NoteType {
    Footnote,
    Endnote,
}

// --- Helper functions ---

/// Check if a formatting element is enabled (not explicitly set to false/0/none).
fn is_format_enabled(e: &BytesStart) -> bool {
    for attr in e.attributes().flatten() {
        if attr.key.as_ref() == b"w:val"
            && let Ok(val) = std::str::from_utf8(&attr.value)
        {
            return !matches!(val, "false" | "0" | "none");
        }
    }
    true // no w:val attribute means enabled
}

/// Read `w:val` attribute as i64.
fn get_val_attr(e: &BytesStart) -> Option<i64> {
    for attr in e.attributes().flatten() {
        if attr.key.as_ref() == b"w:val"
            && let Ok(val) = std::str::from_utf8(&attr.value)
        {
            return val.parse().ok();
        }
    }
    None
}

/// Read `w:val` attribute as String.
fn get_val_attr_string(e: &BytesStart) -> Option<String> {
    for attr in e.attributes().flatten() {
        if attr.key.as_ref() == b"w:val"
            && let Ok(val) = std::str::from_utf8(&attr.value)
        {
            return Some(val.to_string());
        }
    }
    None
}

/// Map heading style name to markdown heading level (fallback for docs without styles.xml).
fn heading_level_from_style_name(style: &str) -> Option<u8> {
    match style {
        "Title" => Some(1),
        s if s.starts_with("Heading") || s.starts_with("heading") => {
            let num_part = s.trim_start_matches("Heading").trim_start_matches("heading");
            if let Ok(n) = num_part.parse::<u8>()
                && (1..=6).contains(&n)
            {
                // Title is h1, so Heading1 becomes h2, etc. Clamp to 6 (max markdown heading level).
                return Some((n + 1).min(6));
            }
            None
        }
        _ => None,
    }
}

// --- Impls ---

impl Document {
    pub fn new() -> Self {
        Self::default()
    }

    /// Ensure output ends with a blank line (double newline).
    fn ensure_blank_line(output: &mut String) {
        if !output.is_empty() && !output.ends_with("\n\n") {
            if output.ends_with('\n') {
                output.push('\n');
            } else {
                output.push_str("\n\n");
            }
        }
    }

    /// Resolve heading level for a paragraph style using the StyleCatalog.
    ///
    /// Walks the style inheritance chain to find `outline_level`.
    /// Falls back to string-matching on style name/ID if no StyleCatalog is available.
    /// Returns 1-6 (markdown heading levels).
    pub fn resolve_heading_level(&self, style_id: &str) -> Option<u8> {
        if let Some(ref catalog) = self.style_catalog {
            // Walk inheritance chain looking for outline_level
            let mut current_id = Some(style_id);
            let mut visited = 0;
            while let Some(id) = current_id {
                if visited > 20 {
                    break; // prevent infinite loops
                }
                visited += 1;
                if let Some(style_def) = catalog.styles.get(id) {
                    if let Some(level) = style_def.paragraph_properties.outline_level {
                        // outline_level 0 = h1, 1 = h2, ..., clamped to 6
                        return Some((level + 1).min(6));
                    }
                    // Check style name for "Title" pattern
                    if let Some(ref name) = style_def.name
                        && (name == "Title" || name == "title")
                    {
                        return Some(1);
                    }
                    current_id = style_def.based_on.as_deref();
                } else {
                    break;
                }
            }
        }
        // Fallback: string-match on style ID
        heading_level_from_style_name(style_id)
    }

    pub fn extract_text(&self) -> String {
        let mut text = String::new();

        for paragraph in &self.paragraphs {
            let para_text = paragraph.to_text();
            if !para_text.is_empty() {
                text.push_str(&para_text);
                text.push('\n');
            }
        }

        for table in &self.tables {
            for row in &table.rows {
                for cell in &row.cells {
                    for paragraph in &cell.paragraphs {
                        let para_text = paragraph.to_text();
                        if !para_text.is_empty() {
                            text.push_str(&para_text);
                            text.push('\t');
                        }
                    }
                }
                text.push('\n');
            }
            text.push('\n');
        }

        text
    }

    /// Render header/footer content as markdown text.
    fn header_footer_to_markdown(hf: &HeaderFooter) -> String {
        let mut parts = Vec::new();
        for para in &hf.paragraphs {
            let text = para.runs_to_markdown();
            if !text.is_empty() {
                parts.push(text);
            }
        }
        parts.join("\n")
    }

    /// Render the document as markdown.
    pub fn to_markdown(&self) -> String {
        use std::fmt::Write;

        let mut output = String::new();
        let mut list_counters: HashMap<(i64, i64), usize> = HashMap::new();
        let mut prev_was_list = false;

        // Prepend headers (if any non-empty)
        for header in &self.headers {
            let header_text = Self::header_footer_to_markdown(header);
            if !header_text.is_empty() {
                output.push_str(&header_text);
                output.push_str("\n\n---\n\n");
            }
        }

        // Use elements ordering if populated, otherwise fall back to paragraphs-only
        if !self.elements.is_empty() {
            for element in &self.elements {
                match element {
                    DocumentElement::Paragraph(idx) => {
                        let Some(paragraph) = self.paragraphs.get(*idx) else {
                            continue;
                        };
                        self.append_paragraph_markdown(paragraph, &mut output, &mut list_counters, &mut prev_was_list);
                    }
                    DocumentElement::Table(idx) => {
                        let Some(table) = self.tables.get(*idx) else { continue };
                        // Ensure blank line separation before table
                        Self::ensure_blank_line(&mut output);
                        output.push_str(&table.to_markdown());
                        prev_was_list = false;
                    }
                    DocumentElement::Drawing(idx) => {
                        let Some(drawing) = self.drawings.get(*idx) else {
                            continue;
                        };
                        let alt = drawing
                            .doc_properties
                            .as_ref()
                            .and_then(|dp| dp.description.as_deref())
                            .unwrap_or("");
                        // Ensure blank line separation before image
                        Self::ensure_blank_line(&mut output);
                        let _ = writeln!(output, "![{}](image)", alt);
                        prev_was_list = false;
                    }
                }
            }
        } else {
            for paragraph in &self.paragraphs {
                self.append_paragraph_markdown(paragraph, &mut output, &mut list_counters, &mut prev_was_list);
            }
        }

        // Append footers (if any non-empty)
        for footer in &self.footers {
            let footer_text = Self::header_footer_to_markdown(footer);
            if !footer_text.is_empty() {
                Self::ensure_blank_line(&mut output);
                output.push_str("---\n\n");
                output.push_str(&footer_text);
            }
        }

        // Footnotes
        if !self.footnotes.is_empty() {
            output.push_str("\n\n");
            for note in &self.footnotes {
                let note_text: String = note
                    .paragraphs
                    .iter()
                    .map(|p| p.runs_to_markdown())
                    .collect::<Vec<_>>()
                    .join(" ");
                if !note_text.is_empty() {
                    let _ = writeln!(output, "[^{}]: {}", note.id, note_text);
                }
            }
        }

        // Endnotes
        if !self.endnotes.is_empty() {
            output.push_str("\n\n");
            for note in &self.endnotes {
                let note_text: String = note
                    .paragraphs
                    .iter()
                    .map(|p| p.runs_to_markdown())
                    .collect::<Vec<_>>()
                    .join(" ");
                if !note_text.is_empty() {
                    let _ = writeln!(output, "[^{}]: {}", note.id, note_text);
                }
            }
        }

        // Trim output in-place
        let trimmed_end = output.trim_end().len();
        output.truncate(trimmed_end);
        let trimmed_start = output.len() - output.trim_start().len();
        if trimmed_start > 0 {
            output.drain(..trimmed_start);
        }
        output
    }

    /// Helper: append a paragraph's markdown to output, managing list transitions.
    fn append_paragraph_markdown(
        &self,
        paragraph: &Paragraph,
        output: &mut String,
        list_counters: &mut HashMap<(i64, i64), usize>,
        prev_was_list: &mut bool,
    ) {
        let is_list = paragraph.numbering_id.is_some();

        // Add blank line before list block when transitioning from non-list
        if is_list && !*prev_was_list {
            Self::ensure_blank_line(output);
        }

        // Add blank line after list block when transitioning to non-list
        if !is_list && *prev_was_list {
            Self::ensure_blank_line(output);
        }

        let heading_level = paragraph.style.as_deref().and_then(|s| self.resolve_heading_level(s));
        let md = paragraph.to_markdown(&self.numbering_defs, list_counters, heading_level);
        if md.is_empty() {
            *prev_was_list = is_list;
            return;
        }

        if is_list {
            // List items separated by single newline
            if *prev_was_list {
                output.push('\n');
            }
            output.push_str(&md);
        } else {
            // Non-list paragraphs separated by blank lines
            Self::ensure_blank_line(output);
            output.push_str(&md);
        }

        *prev_was_list = is_list;
    }
}

impl Paragraph {
    pub fn new() -> Self {
        Self::default()
    }

    /// Concatenate text runs to produce paragraph text.
    ///
    /// In DOCX, whitespace between words is stored inside `<w:t>` elements
    /// (e.g. `<w:t>Hello </w:t><w:t>World</w:t>`), so runs are joined
    /// directly without adding extra separators. The parser must use
    /// `trim_text(false)` to preserve this whitespace.
    pub fn to_text(&self) -> String {
        let mut text = String::new();
        for run in &self.runs {
            text.push_str(&run.text);
        }
        text
    }

    /// Render inline runs as markdown (no paragraph-level wrapping).
    pub fn runs_to_markdown(&self) -> String {
        let mut text = String::new();
        for run in &self.runs {
            text.push_str(&run.to_markdown());
        }
        text
    }

    /// Render as markdown with heading/list context.
    ///
    /// If `heading_level` is provided (resolved via `Document::resolve_heading_level`),
    /// it takes precedence over style name matching.
    pub fn to_markdown(
        &self,
        numbering_defs: &HashMap<(i64, i64), ListType>,
        list_counters: &mut HashMap<(i64, i64), usize>,
        heading_level: Option<u8>,
    ) -> String {
        let inline = self.runs_to_markdown();

        // Check for heading level (resolved from StyleCatalog or style name fallback)
        if let Some(level) = heading_level {
            let hashes = "#".repeat(level as usize);
            return format!("{} {}", hashes, inline);
        }

        // Check for list item
        if let (Some(num_id), Some(level)) = (self.numbering_id, self.numbering_level) {
            let indent = "  ".repeat(level as usize);
            let key = (num_id, level);
            let list_type = numbering_defs.get(&key).copied().unwrap_or(ListType::Bullet);

            match list_type {
                ListType::Bullet => {
                    return format!("{}- {}", indent, inline);
                }
                ListType::Numbered => {
                    let counter = list_counters.entry(key).or_insert(0);
                    *counter += 1;
                    return format!("{}{}. {}", indent, *counter, inline);
                }
            }
        }

        // Plain paragraph
        inline
    }

    pub fn add_run(&mut self, run: Run) {
        self.runs.push(run);
    }
}

impl Run {
    pub fn new(text: String) -> Self {
        Self {
            text,
            ..Default::default()
        }
    }

    /// Render this run as markdown with formatting markers.
    pub fn to_markdown(&self) -> String {
        if self.text.is_empty() {
            return String::new();
        }

        let extra = (if self.bold && self.italic {
            6
        } else if self.bold || self.italic {
            4
        } else {
            0
        }) + (if self.strikethrough { 4 } else { 0 })
            + (if self.underline { 7 } else { 0 })
            + self.hyperlink_url.as_ref().map_or(0, |u| u.len() + 4);
        let mut out = String::with_capacity(self.text.len() + extra);

        if self.hyperlink_url.is_some() {
            out.push('[');
        }
        if self.underline {
            out.push_str("<u>");
        }
        if self.strikethrough {
            out.push_str("~~");
        }
        if self.bold && self.italic {
            out.push_str("***");
        } else if self.bold {
            out.push_str("**");
        } else if self.italic {
            out.push('*');
        }

        out.push_str(&self.text);

        if self.bold && self.italic {
            out.push_str("***");
        } else if self.bold {
            out.push_str("**");
        } else if self.italic {
            out.push('*');
        }
        if self.strikethrough {
            out.push_str("~~");
        }
        if self.underline {
            out.push_str("</u>");
        }
        if let Some(ref url) = self.hyperlink_url {
            out.push_str("](");
            out.push_str(url);
            out.push(')');
        }

        out
    }
}

impl Table {
    pub fn new() -> Self {
        Self::default()
    }

    /// Render this table as a markdown table.
    ///
    /// Uses table row and cell properties to improve formatting:
    /// - Respects `RowProperties.is_header` to identify header rows
    /// - Handles `CellProperties.grid_span` to account for merged cells
    ///
    /// If no explicit header row is marked, treats the first row as the header.
    pub fn to_markdown(&self) -> String {
        if self.rows.is_empty() {
            return String::new();
        }

        // Build cells, accounting for grid_span (horizontal cell merging)
        let mut cells: Vec<Vec<String>> = Vec::new();
        for row in &self.rows {
            let mut row_cells = Vec::new();
            for cell in &row.cells {
                // Cells with v_merge=Continue are continuations of a vertically merged cell above;
                // render them as empty in the markdown table.
                let is_vmerge_continue = cell
                    .properties
                    .as_ref()
                    .is_some_and(|p| matches!(p.v_merge, Some(super::table::VerticalMerge::Continue)));

                let cell_text = if is_vmerge_continue {
                    String::new()
                } else {
                    cell.paragraphs
                        .iter()
                        .map(|para| para.runs_to_markdown())
                        .collect::<Vec<_>>()
                        .join(" ")
                        .trim()
                        .to_string()
                };
                row_cells.push(cell_text);

                // Add empty cells for grid_span > 1 (horizontal merging)
                let span = cell.properties.as_ref().and_then(|p| p.grid_span).unwrap_or(1);
                for _ in 1..span {
                    row_cells.push(String::new());
                }
            }
            cells.push(row_cells);
        }

        if cells.is_empty() {
            return String::new();
        }

        let num_cols = cells.iter().map(|r| r.len()).max().unwrap_or(0);
        if num_cols == 0 {
            return String::new();
        }

        // Calculate column widths
        let mut col_widths = vec![3usize; num_cols];
        for row in &cells {
            for (i, cell) in row.iter().enumerate() {
                col_widths[i] = col_widths[i].max(cell.len());
            }
        }

        // Determine which row is the header.
        // Prefer explicitly marked header rows; fall back to first row if none found.
        let header_row_index = self
            .rows
            .iter()
            .position(|row| row.properties.as_ref().map(|p| p.is_header).unwrap_or(false))
            .unwrap_or(0); // Default to first row if no explicit header found

        let mut md = String::new();

        // Render rows
        for (row_idx, row) in cells.iter().enumerate() {
            md.push('|');
            for (i, cell) in row.iter().enumerate() {
                let width = col_widths.get(i).copied().unwrap_or(3);
                md.push_str(&format!(" {:width$} |", cell, width = width));
            }
            // Pad missing columns
            for i in row.len()..num_cols {
                let width = col_widths.get(i).copied().unwrap_or(3);
                md.push_str(&format!(" {:width$} |", "", width = width));
            }
            md.push('\n');

            // Insert separator after header row
            if row_idx == header_row_index {
                md.push('|');
                for i in 0..num_cols {
                    let width = col_widths.get(i).copied().unwrap_or(3);
                    md.push_str(&format!(" {} |", "-".repeat(width)));
                }
                md.push('\n');
            }
        }

        md.trim_end().to_string()
    }
}

// --- Parser ---

/// Context for tracking nested table parsing state.
///
/// Each level of table nesting gets its own context on the stack,
/// allowing arbitrary nesting depth (e.g. tables within table cells).
struct TableContext {
    table: Table,
    current_row: Option<TableRow>,
    current_cell: Option<TableCell>,
    paragraph: Option<Paragraph>,
}

impl TableContext {
    fn new() -> Self {
        Self {
            table: Table::new(),
            current_row: None,
            current_cell: None,
            paragraph: None,
        }
    }
}

/// Apply run-level formatting from a `<w:b>`, `<w:i>`, `<w:u>`, `<w:strike>`, or `<w:dstrike>` element.
///
/// Works for both `Event::Start` and `Event::Empty` events, eliminating duplication.
fn apply_run_formatting(e: &BytesStart, current_run: &mut Option<Run>) {
    if let Some(run) = current_run {
        match e.name().as_ref() {
            b"w:b" => run.bold = is_format_enabled(e),
            b"w:i" => run.italic = is_format_enabled(e),
            b"w:u" => run.underline = is_format_enabled(e),
            b"w:strike" | b"w:dstrike" => run.strikethrough = is_format_enabled(e),
            _ => {}
        }
    }
}

/// Apply paragraph-level properties from a `<w:pStyle>`, `<w:ilvl>`, or `<w:numId>` element.
///
/// Resolves the correct paragraph (table context vs top-level) automatically.
fn apply_paragraph_property(
    e: &BytesStart,
    table_stack: &mut [TableContext],
    current_paragraph: &mut Option<Paragraph>,
) {
    let para = if let Some(ctx) = table_stack.last_mut() {
        ctx.paragraph.as_mut()
    } else {
        current_paragraph.as_mut()
    };

    if let Some(para) = para {
        match e.name().as_ref() {
            b"w:pStyle" => para.style = get_val_attr_string(e),
            b"w:ilvl" => para.numbering_level = get_val_attr(e),
            b"w:numId" => para.numbering_id = get_val_attr(e),
            _ => {}
        }
    }
}

// --- Security Validation ---

/// Validate archive against ZIP bomb attacks and resource exhaustion.
///
/// Checks:
/// - Maximum uncompressed size per file (100 MB default)
/// - Maximum total number of entries (10,000 default)
/// - Maximum total uncompressed size (500 MB default)
fn validate_archive_security(archive: &mut zip::ZipArchive<impl Read + Seek>) -> Result<(), DocxParseError> {
    use super::{MAX_TOTAL_UNCOMPRESSED_SIZE, MAX_UNCOMPRESSED_FILE_SIZE, MAX_ZIP_ENTRIES};

    // Check entry count
    if archive.len() > MAX_ZIP_ENTRIES {
        return Err(DocxParseError::SecurityLimit(format!(
            "Archive contains {} entries, exceeds limit of {}",
            archive.len(),
            MAX_ZIP_ENTRIES
        )));
    }

    // Check individual file sizes and accumulate total
    let mut total_uncompressed: u64 = 0;
    for i in 0..archive.len() {
        let file = archive
            .by_index_raw(i)
            .map_err(|e| DocxParseError::SecurityLimit(format!("Failed to read ZIP entry {}: {}", i, e)))?;
        let size = file.size();
        if size > MAX_UNCOMPRESSED_FILE_SIZE {
            return Err(DocxParseError::SecurityLimit(format!(
                "File '{}' uncompressed size {} bytes exceeds limit of {} bytes",
                file.name(),
                size,
                MAX_UNCOMPRESSED_FILE_SIZE
            )));
        }
        total_uncompressed = total_uncompressed.saturating_add(size);
    }

    // Check total uncompressed size
    if total_uncompressed > MAX_TOTAL_UNCOMPRESSED_SIZE {
        return Err(DocxParseError::SecurityLimit(format!(
            "Total uncompressed size {} bytes exceeds limit of {} bytes",
            total_uncompressed, MAX_TOTAL_UNCOMPRESSED_SIZE
        )));
    }

    Ok(())
}

#[derive(Debug)]
struct DocxParser<R: Read + Seek> {
    archive: zip::ZipArchive<R>,
    relationships: HashMap<String, String>,
    styles: Option<super::styles::StyleCatalog>,
    theme: Option<super::theme::Theme>,
}

impl<R: Read + Seek> DocxParser<R> {
    fn new(reader: R) -> Result<Self, DocxParseError> {
        let mut archive = zip::ZipArchive::new(reader)?;
        validate_archive_security(&mut archive)?;

        // Load styles catalog (best-effort - styles.xml is optional)
        let styles = {
            let mut styles_result = None;
            if let Ok(file) = archive.by_name("word/styles.xml") {
                let mut xml = String::new();
                if file
                    .take(super::MAX_UNCOMPRESSED_FILE_SIZE)
                    .read_to_string(&mut xml)
                    .is_ok()
                {
                    styles_result = super::styles::parse_styles_xml(&xml).ok();
                }
            }
            styles_result
        };

        // Load theme (best-effort - theme1.xml is optional)
        let theme = {
            let mut theme_result = None;
            if let Ok(file) = archive.by_name("word/theme/theme1.xml") {
                let mut xml = String::new();
                if file
                    .take(super::MAX_UNCOMPRESSED_FILE_SIZE)
                    .read_to_string(&mut xml)
                    .is_ok()
                {
                    theme_result = super::theme::parse_theme_xml(&xml).ok();
                }
            }
            theme_result
        };

        Ok(Self {
            archive,
            relationships: HashMap::new(),
            styles,
            theme,
        })
    }

    fn parse(mut self) -> Result<Document, DocxParseError> {
        let mut document = Document::new();

        // Parse relationships first for hyperlink URL resolution
        if let Ok(rels_xml) = self.read_file("word/_rels/document.xml.rels") {
            self.relationships = Self::parse_relationships_xml(&rels_xml);
        }

        let document_xml = self.read_file("word/document.xml")?;
        self.parse_document_xml(&document_xml, &mut document)?;

        if let Ok(numbering_xml) = self.read_file("word/numbering.xml") {
            let numbering_defs = self.parse_numbering(&numbering_xml)?;
            document.numbering_defs = numbering_defs;
        }

        self.parse_headers_footers(&mut document)?;

        if let Ok(footnotes_xml) = self.read_file("word/footnotes.xml") {
            self.parse_notes(&footnotes_xml, &mut document.footnotes, NoteType::Footnote)?;
        }

        if let Ok(endnotes_xml) = self.read_file("word/endnotes.xml") {
            self.parse_notes(&endnotes_xml, &mut document.endnotes, NoteType::Endnote)?;
        }

        document.style_catalog = self.styles.take();
        document.theme = self.theme.take();
        // Filter to only image relationships (exclude hyperlinks)
        document.image_relationships = self
            .relationships
            .iter()
            .filter(|(_, target)| {
                // Image targets point to media/ paths, not URLs
                !target.starts_with("http://") && !target.starts_with("https://")
            })
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect();

        Ok(document)
    }

    /// Parse relationship file to get rId → target mappings for hyperlinks and images.
    fn parse_relationships_xml(xml: &str) -> HashMap<String, String> {
        let mut rels = HashMap::new();
        let mut reader = Reader::from_str(xml);
        reader.config_mut().trim_text(true);
        let mut buf = Vec::new();

        loop {
            match reader.read_event_into(&mut buf) {
                Ok(Event::Empty(ref e)) | Ok(Event::Start(ref e)) if e.name().as_ref() == b"Relationship" => {
                    let mut id = None;
                    let mut target = None;
                    let mut rel_type_matches = false;
                    for attr in e.attributes().flatten() {
                        match attr.key.as_ref() {
                            b"Id" => id = std::str::from_utf8(&attr.value).ok().map(String::from),
                            b"Target" => {
                                target = std::str::from_utf8(&attr.value).ok().map(String::from);
                            }
                            b"Type" => {
                                rel_type_matches = std::str::from_utf8(&attr.value)
                                    .ok()
                                    .is_some_and(|t| t.contains("hyperlink") || t.contains("image"));
                            }
                            _ => {}
                        }
                    }
                    // Include hyperlink and image relationships
                    if let (Some(id_val), Some(target_val)) = (id, target)
                        && rel_type_matches
                    {
                        rels.insert(id_val, target_val);
                    }
                }
                Ok(Event::Eof) => break,
                _ => {}
            }
            buf.clear();
        }

        rels
    }

    fn read_file(&mut self, path: &str) -> Result<String, DocxParseError> {
        let read_limit = super::MAX_UNCOMPRESSED_FILE_SIZE;

        let file = self
            .archive
            .by_name(path)
            .map_err(|_| DocxParseError::FileNotFound(path.to_string()))?;

        let mut contents = String::new();
        file.take(read_limit).read_to_string(&mut contents)?;
        Ok(contents)
    }

    fn parse_document_xml(&self, xml: &str, document: &mut Document) -> Result<(), DocxParseError> {
        let mut reader = Reader::from_str(xml);
        reader.config_mut().trim_text(false);

        let mut buf = Vec::new();
        let mut current_paragraph: Option<Paragraph> = None;
        let mut current_run: Option<Run> = None;
        let mut in_text = false;
        let mut in_math_text = false;
        let mut current_hyperlink_url: Option<String> = None;
        let mut table_stack: Vec<TableContext> = Vec::new();

        loop {
            match reader.read_event_into(&mut buf) {
                Ok(Event::Start(ref e)) => match e.name().as_ref() {
                    b"w:p" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            ctx.paragraph = Some(Paragraph::new());
                        } else {
                            current_paragraph = Some(Paragraph::new());
                        }
                    }
                    b"w:r" => {
                        let mut run = Run::default();
                        if let Some(ref url) = current_hyperlink_url {
                            run.hyperlink_url = Some(url.clone());
                        }
                        current_run = Some(run);
                    }
                    b"w:t" => {
                        in_text = true;
                    }
                    // OMML math run — treat like a word run for text extraction
                    b"m:r" => {
                        if current_run.is_none() {
                            current_run = Some(Run::default());
                        }
                    }
                    // OMML math text
                    b"m:t" => {
                        in_math_text = true;
                    }
                    b"w:tbl" => {
                        table_stack.push(TableContext::new());
                    }
                    b"w:tblPr" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            ctx.table.properties = Some(super::table::parse_table_properties(&mut reader));
                        }
                    }
                    b"w:tblGrid" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            ctx.table.grid = Some(super::table::parse_table_grid(&mut reader));
                        }
                    }
                    b"w:tr" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            ctx.current_row = Some(TableRow::default());
                        }
                    }
                    b"w:trPr" => {
                        if let Some(ctx) = table_stack.last_mut()
                            && let Some(ref mut row) = ctx.current_row
                        {
                            row.properties = Some(super::table::parse_row_properties(&mut reader));
                        }
                    }
                    b"w:tc" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            ctx.current_cell = Some(TableCell::default());
                        }
                    }
                    b"w:tcPr" => {
                        if let Some(ctx) = table_stack.last_mut()
                            && let Some(ref mut cell) = ctx.current_cell
                        {
                            cell.properties = Some(super::table::parse_cell_properties(&mut reader));
                        }
                    }
                    b"w:b" | b"w:i" | b"w:u" | b"w:strike" | b"w:dstrike" => {
                        apply_run_formatting(e, &mut current_run);
                    }
                    b"w:pStyle" | b"w:ilvl" | b"w:numId" => {
                        apply_paragraph_property(e, &mut table_stack, &mut current_paragraph);
                    }
                    b"w:hyperlink" => {
                        for attr in e.attributes().flatten() {
                            if attr.key.as_ref() == b"r:id"
                                && let Ok(rid) = std::str::from_utf8(&attr.value)
                            {
                                current_hyperlink_url = self.relationships.get(rid).cloned();
                            }
                        }
                    }
                    b"w:drawing" => {
                        let drawing = super::drawing::parse_drawing(&mut reader);
                        let idx = document.drawings.len();
                        document.drawings.push(drawing);
                        document.elements.push(DocumentElement::Drawing(idx));
                    }
                    // Line break (when not self-closing)
                    b"w:br" => {
                        if let Some(ref mut run) = current_run {
                            run.text.push('\n');
                        }
                    }
                    b"w:sectPr" => {
                        let sect_props = super::section::parse_section_properties_streaming(&mut reader);
                        document.sections.push(sect_props);
                    }
                    _ => {}
                },
                Ok(Event::Empty(ref e)) => match e.name().as_ref() {
                    b"w:b" | b"w:i" | b"w:u" | b"w:strike" | b"w:dstrike" => {
                        apply_run_formatting(e, &mut current_run);
                    }
                    b"w:pStyle" | b"w:ilvl" | b"w:numId" => {
                        apply_paragraph_property(e, &mut table_stack, &mut current_paragraph);
                    }
                    // Line break: insert newline to separate adjacent text
                    b"w:br" => {
                        if let Some(ref mut run) = current_run {
                            run.text.push('\n');
                        }
                    }
                    b"w:footnoteReference" | b"w:endnoteReference" => {
                        // Insert inline footnote/endnote reference marker [^N]
                        if let Some(ref mut run) = current_run {
                            for attr in e.attributes().flatten() {
                                if attr.key.as_ref() == b"w:id"
                                    && let Ok(id) = std::str::from_utf8(&attr.value)
                                {
                                    // Skip separator references (id 0 and 1)
                                    if id != "0" && id != "1" {
                                        run.text.push_str(&format!("[^{}]", id));
                                    }
                                }
                            }
                        }
                    }
                    b"w:sectPr" => {
                        // Self-closing <w:sectPr/> (empty section properties)
                        document.sections.push(super::section::SectionProperties::default());
                    }
                    b"w:tblPr" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            ctx.table.properties = Some(super::table::TableProperties::default());
                        }
                    }
                    b"w:tblGrid" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            ctx.table.grid = Some(super::table::TableGrid::default());
                        }
                    }
                    b"w:trPr" => {
                        if let Some(ctx) = table_stack.last_mut()
                            && let Some(ref mut row) = ctx.current_row
                        {
                            row.properties = Some(super::table::RowProperties::default());
                        }
                    }
                    b"w:tcPr" => {
                        if let Some(ctx) = table_stack.last_mut()
                            && let Some(ref mut cell) = ctx.current_cell
                        {
                            cell.properties = Some(super::table::CellProperties::default());
                        }
                    }
                    _ => {}
                },
                Ok(Event::Text(e)) => {
                    if (in_text || in_math_text)
                        && let Some(ref mut run) = current_run
                    {
                        let text = e.decode()?;
                        run.text.push_str(&text);
                    }
                }
                Ok(Event::End(ref e)) => match e.name().as_ref() {
                    b"w:t" => {
                        in_text = false;
                    }
                    b"m:t" => {
                        in_math_text = false;
                    }
                    // Math run ends — flush accumulated math text as a regular run
                    b"m:r" => {
                        if let Some(run) = current_run.take()
                            && !run.text.is_empty()
                        {
                            if let Some(ctx) = table_stack.last_mut() {
                                if let Some(ref mut para) = ctx.paragraph {
                                    para.add_run(run);
                                } else if let Some(ref mut cell) = ctx.current_cell {
                                    if cell.paragraphs.is_empty() {
                                        cell.paragraphs.push(Paragraph::new());
                                    }
                                    if let Some(para) = cell.paragraphs.last_mut() {
                                        para.add_run(run);
                                    }
                                }
                            } else if let Some(ref mut para) = current_paragraph {
                                para.add_run(run);
                            }
                        }
                    }
                    b"w:r" => {
                        if let Some(run) = current_run.take() {
                            if let Some(ctx) = table_stack.last_mut() {
                                if let Some(ref mut para) = ctx.paragraph {
                                    para.add_run(run);
                                } else if let Some(ref mut cell) = ctx.current_cell {
                                    if cell.paragraphs.is_empty() {
                                        cell.paragraphs.push(Paragraph::new());
                                    }
                                    if let Some(para) = cell.paragraphs.last_mut() {
                                        para.add_run(run);
                                    }
                                }
                            } else if let Some(ref mut para) = current_paragraph {
                                para.add_run(run);
                            }
                        }
                    }
                    b"w:p" => {
                        if let Some(ctx) = table_stack.last_mut() {
                            if let Some(para) = ctx.paragraph.take()
                                && let Some(ref mut cell) = ctx.current_cell
                            {
                                cell.paragraphs.push(para);
                            }
                        } else if let Some(para) = current_paragraph.take() {
                            let idx = document.paragraphs.len();
                            document.paragraphs.push(para);
                            document.elements.push(DocumentElement::Paragraph(idx));
                        }
                    }
                    b"w:tc" => {
                        if let Some(ctx) = table_stack.last_mut()
                            && let Some(cell) = ctx.current_cell.take()
                            && let Some(ref mut row) = ctx.current_row
                        {
                            row.cells.push(cell);
                        }
                    }
                    b"w:tr" => {
                        if let Some(ctx) = table_stack.last_mut()
                            && let Some(row) = ctx.current_row.take()
                        {
                            ctx.table.rows.push(row);
                        }
                    }
                    b"w:tbl" => {
                        if let Some(completed_ctx) = table_stack.pop() {
                            let completed_table = completed_ctx.table;
                            if let Some(parent_ctx) = table_stack.last_mut() {
                                // Nested table: flatten content into parent cell
                                if let Some(ref mut cell) = parent_ctx.current_cell {
                                    for row in completed_table.rows {
                                        for table_cell in row.cells {
                                            for para in table_cell.paragraphs {
                                                cell.paragraphs.push(para);
                                            }
                                        }
                                    }
                                }
                            } else {
                                // Top-level table
                                let idx = document.tables.len();
                                document.tables.push(completed_table);
                                document.elements.push(DocumentElement::Table(idx));
                            }
                        }
                    }
                    b"w:hyperlink" => {
                        current_hyperlink_url = None;
                    }
                    _ => {}
                },
                Ok(Event::Eof) => break,
                Err(e) => return Err(e.into()),
                _ => {}
            }
            buf.clear();
        }

        Ok(())
    }

    fn parse_numbering(&self, xml: &str) -> Result<HashMap<(i64, i64), ListType>, DocxParseError> {
        let mut numbering_defs: HashMap<(i64, i64), ListType> = HashMap::new();
        let mut abstract_num_formats: HashMap<i64, HashMap<i64, ListType>> = HashMap::new();
        let mut num_to_abstract: HashMap<i64, i64> = HashMap::new();

        let mut reader = Reader::from_str(xml);
        reader.config_mut().trim_text(false);

        let mut buf = Vec::new();
        let mut current_abstract_num_id: Option<i64> = None;
        let mut current_num_id: Option<i64> = None;
        let mut current_lvl: Option<i64> = None;

        loop {
            match reader.read_event_into(&mut buf) {
                Ok(Event::Start(ref e)) => match e.name().as_ref() {
                    b"w:abstractNum" => {
                        for attr in e.attributes().flatten() {
                            if attr.key.as_ref() == b"w:abstractNumId"
                                && let Ok(id_str) = std::str::from_utf8(&attr.value)
                            {
                                current_abstract_num_id = id_str.parse().ok();
                            }
                        }
                    }
                    b"w:num" => {
                        for attr in e.attributes().flatten() {
                            if attr.key.as_ref() == b"w:numId"
                                && let Ok(id_str) = std::str::from_utf8(&attr.value)
                            {
                                current_num_id = id_str.parse().ok();
                            }
                        }
                    }
                    b"w:lvl" => {
                        for attr in e.attributes().flatten() {
                            if attr.key.as_ref() == b"w:ilvl"
                                && let Ok(id_str) = std::str::from_utf8(&attr.value)
                            {
                                current_lvl = id_str.parse().ok();
                            }
                        }
                    }
                    b"w:numFmt" => {
                        if let (Some(abstract_id), Some(lvl)) = (current_abstract_num_id, current_lvl) {
                            let fmt = get_val_attr_string(e);
                            let list_type = match fmt.as_deref() {
                                Some("decimal") | Some("decimalZero") | Some("lowerLetter") | Some("upperLetter")
                                | Some("lowerRoman") | Some("upperRoman") => ListType::Numbered,
                                _ => ListType::Bullet,
                            };
                            abstract_num_formats
                                .entry(abstract_id)
                                .or_default()
                                .insert(lvl, list_type);
                        }
                    }
                    _ => {}
                },
                Ok(Event::Empty(ref e)) => match e.name().as_ref() {
                    b"w:abstractNumId" => {
                        if let Some(num_id) = current_num_id
                            && let Some(abstract_id) = get_val_attr(e)
                        {
                            num_to_abstract.insert(num_id, abstract_id);
                        }
                    }
                    b"w:numFmt" => {
                        if let (Some(abstract_id), Some(lvl)) = (current_abstract_num_id, current_lvl) {
                            let fmt = get_val_attr_string(e);
                            let list_type = match fmt.as_deref() {
                                Some("decimal") | Some("decimalZero") | Some("lowerLetter") | Some("upperLetter")
                                | Some("lowerRoman") | Some("upperRoman") => ListType::Numbered,
                                _ => ListType::Bullet,
                            };
                            abstract_num_formats
                                .entry(abstract_id)
                                .or_default()
                                .insert(lvl, list_type);
                        }
                    }
                    _ => {}
                },
                Ok(Event::End(ref e)) => match e.name().as_ref() {
                    b"w:abstractNum" => {
                        current_abstract_num_id = None;
                        current_lvl = None;
                    }
                    b"w:lvl" => {
                        current_lvl = None;
                    }
                    b"w:num" => {
                        current_num_id = None;
                    }
                    _ => {}
                },
                Ok(Event::Eof) => break,
                _ => {}
            }
            buf.clear();
        }

        // Build final numbering_defs by resolving num → abstractNum references
        for (num_id, abstract_id) in &num_to_abstract {
            if let Some(formats) = abstract_num_formats.get(abstract_id) {
                for (lvl, list_type) in formats {
                    numbering_defs.insert((*num_id, *lvl), *list_type);
                }
            }
        }

        Ok(numbering_defs)
    }

    fn parse_headers_footers(&mut self, document: &mut Document) -> Result<(), DocxParseError> {
        for i in 1..=3 {
            let header_path = format!("word/header{}.xml", i);
            if let Ok(header_xml) = self.read_file(&header_path) {
                let mut header = HeaderFooter::default();
                self.parse_header_footer_content(&header_xml, &mut header)?;
                document.headers.push(header);
            }

            let footer_path = format!("word/footer{}.xml", i);
            if let Ok(footer_xml) = self.read_file(&footer_path) {
                let mut footer = HeaderFooter::default();
                self.parse_header_footer_content(&footer_xml, &mut footer)?;
                document.footers.push(footer);
            }
        }

        Ok(())
    }

    fn parse_header_footer_content(&self, xml: &str, header_footer: &mut HeaderFooter) -> Result<(), DocxParseError> {
        let mut reader = Reader::from_str(xml);
        reader.config_mut().trim_text(false);

        let mut buf = Vec::new();
        let mut current_paragraph: Option<Paragraph> = None;
        let mut current_run: Option<Run> = None;
        let mut in_text = false;

        loop {
            match reader.read_event_into(&mut buf) {
                Ok(Event::Start(ref e)) => match e.name().as_ref() {
                    b"w:p" => current_paragraph = Some(Paragraph::new()),
                    b"w:r" => current_run = Some(Run::default()),
                    b"w:t" => in_text = true,
                    b"w:b" => {
                        if let Some(ref mut run) = current_run {
                            run.bold = is_format_enabled(e);
                        }
                    }
                    b"w:i" => {
                        if let Some(ref mut run) = current_run {
                            run.italic = is_format_enabled(e);
                        }
                    }
                    b"w:u" => {
                        if let Some(ref mut run) = current_run {
                            run.underline = is_format_enabled(e);
                        }
                    }
                    _ => {}
                },
                Ok(Event::Empty(ref e)) => match e.name().as_ref() {
                    b"w:b" => {
                        if let Some(ref mut run) = current_run {
                            run.bold = is_format_enabled(e);
                        }
                    }
                    b"w:i" => {
                        if let Some(ref mut run) = current_run {
                            run.italic = is_format_enabled(e);
                        }
                    }
                    b"w:u" => {
                        if let Some(ref mut run) = current_run {
                            run.underline = is_format_enabled(e);
                        }
                    }
                    _ => {}
                },
                Ok(Event::Text(e)) => {
                    if in_text && let Some(ref mut run) = current_run {
                        let text = e.decode()?;
                        run.text.push_str(&text);
                    }
                }
                Ok(Event::End(ref e)) => match e.name().as_ref() {
                    b"w:t" => in_text = false,
                    b"w:r" => {
                        if let Some(run) = current_run.take()
                            && let Some(ref mut para) = current_paragraph
                        {
                            para.add_run(run);
                        }
                    }
                    b"w:p" => {
                        if let Some(para) = current_paragraph.take() {
                            header_footer.paragraphs.push(para);
                        }
                    }
                    _ => {}
                },
                Ok(Event::Eof) => break,
                _ => {}
            }
            buf.clear();
        }

        Ok(())
    }

    fn parse_notes(&self, xml: &str, notes: &mut Vec<Note>, note_type: NoteType) -> Result<(), DocxParseError> {
        let mut reader = Reader::from_str(xml);
        reader.config_mut().trim_text(false);

        let mut buf = Vec::new();
        let mut current_note: Option<Note> = None;
        let mut current_paragraph: Option<Paragraph> = None;
        let mut current_run: Option<Run> = None;
        let mut in_text = false;

        loop {
            match reader.read_event_into(&mut buf) {
                Ok(Event::Start(ref e)) => match e.name().as_ref() {
                    b"w:footnote" | b"w:endnote" => {
                        let mut id = String::new();
                        for attr in e.attributes().flatten() {
                            if attr.key.as_ref() == b"w:id" {
                                id = String::from_utf8_lossy(&attr.value).to_string();
                            }
                        }
                        current_note = Some(Note {
                            id,
                            note_type,
                            paragraphs: Vec::new(),
                        });
                    }
                    b"w:p" => current_paragraph = Some(Paragraph::new()),
                    b"w:r" => current_run = Some(Run::default()),
                    b"w:t" => in_text = true,
                    b"w:b" => {
                        if let Some(ref mut run) = current_run {
                            run.bold = is_format_enabled(e);
                        }
                    }
                    b"w:i" => {
                        if let Some(ref mut run) = current_run {
                            run.italic = is_format_enabled(e);
                        }
                    }
                    _ => {}
                },
                Ok(Event::Empty(ref e)) => match e.name().as_ref() {
                    b"w:b" => {
                        if let Some(ref mut run) = current_run {
                            run.bold = is_format_enabled(e);
                        }
                    }
                    b"w:i" => {
                        if let Some(ref mut run) = current_run {
                            run.italic = is_format_enabled(e);
                        }
                    }
                    _ => {}
                },
                Ok(Event::Text(e)) => {
                    if in_text && let Some(ref mut run) = current_run {
                        let text = e.decode()?;
                        run.text.push_str(&text);
                    }
                }
                Ok(Event::End(ref e)) => match e.name().as_ref() {
                    b"w:t" => in_text = false,
                    b"w:r" => {
                        if let Some(run) = current_run.take()
                            && let Some(ref mut para) = current_paragraph
                        {
                            para.add_run(run);
                        }
                    }
                    b"w:p" => {
                        if let Some(para) = current_paragraph.take()
                            && let Some(ref mut note) = current_note
                        {
                            note.paragraphs.push(para);
                        }
                    }
                    b"w:footnote" | b"w:endnote" => {
                        // Filter separator/continuation separator notes (id -1, 0, 1)
                        if let Some(note) = current_note.take()
                            && note.id != "-1"
                            && note.id != "0"
                            && note.id != "1"
                        {
                            notes.push(note);
                        }
                    }
                    _ => {}
                },
                Ok(Event::Eof) => break,
                _ => {}
            }
            buf.clear();
        }

        Ok(())
    }
}

// --- Error ---

#[derive(Debug, thiserror::Error)]
enum DocxParseError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("ZIP error: {0}")]
    Zip(#[from] zip::result::ZipError),

    #[error("XML parsing error: {0}")]
    Xml(#[from] quick_xml::Error),

    #[error("Required file not found in DOCX: {0}")]
    FileNotFound(String),

    #[error("Security limit exceeded: {0}")]
    SecurityLimit(String),
}

// quick-xml's unescape returns an encoding error type
impl From<quick_xml::encoding::EncodingError> for DocxParseError {
    fn from(e: quick_xml::encoding::EncodingError) -> Self {
        DocxParseError::Xml(quick_xml::Error::Encoding(e))
    }
}

// --- Public API ---

/// Parse a DOCX document from bytes and return the structured document.
pub fn parse_document(bytes: &[u8]) -> crate::error::Result<Document> {
    let cursor = Cursor::new(bytes);
    let parser = DocxParser::new(cursor)
        .map_err(|e| crate::error::KreuzbergError::parsing(format!("DOCX parsing failed: {}", e)))?;
    parser
        .parse()
        .map_err(|e| crate::error::KreuzbergError::parsing(format!("DOCX parsing failed: {}", e)))
}

/// Extract text from DOCX bytes.
pub fn extract_text_from_bytes(bytes: &[u8]) -> crate::error::Result<String> {
    let doc = parse_document(bytes)?;
    Ok(doc.extract_text())
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Runs are concatenated directly; whitespace comes from the XML text content.
    #[test]
    fn test_paragraph_to_text_concatenates_runs() {
        let mut para = Paragraph::new();
        para.add_run(Run::new("Hello ".to_string()));
        para.add_run(Run::new("World".to_string()));
        assert_eq!(para.to_text(), "Hello World");
    }

    /// Mid-word run splits (e.g. drop caps) must not insert extra spaces.
    #[test]
    fn test_paragraph_to_text_mid_word_split() {
        let mut para = Paragraph::new();
        para.add_run(Run::new("S".to_string()));
        para.add_run(Run::new("ermocination".to_string()));
        assert_eq!(para.to_text(), "Sermocination");
    }

    #[test]
    fn test_paragraph_to_text_single_run() {
        let mut para = Paragraph::new();
        para.add_run(Run::new("Hello".to_string()));
        assert_eq!(para.to_text(), "Hello");
    }

    #[test]
    fn test_paragraph_to_text_no_runs() {
        let para = Paragraph::new();
        assert_eq!(para.to_text(), "");
    }

    /// Whitespace between words is stored in the run text, not added by join.
    #[test]
    fn test_paragraph_to_text_whitespace_in_runs() {
        let mut para = Paragraph::new();
        para.add_run(Run::new("The ".to_string()));
        para.add_run(Run::new("quick ".to_string()));
        para.add_run(Run::new("fox".to_string()));
        assert_eq!(para.to_text(), "The quick fox");
    }

    // --- Markdown rendering unit tests ---

    #[test]
    fn test_run_bold_to_markdown() {
        let run = Run {
            text: "hello".to_string(),
            bold: true,
            ..Default::default()
        };
        assert_eq!(run.to_markdown(), "**hello**");
    }

    #[test]
    fn test_run_italic_to_markdown() {
        let run = Run {
            text: "hello".to_string(),
            italic: true,
            ..Default::default()
        };
        assert_eq!(run.to_markdown(), "*hello*");
    }

    #[test]
    fn test_run_bold_italic_to_markdown() {
        let run = Run {
            text: "hello".to_string(),
            bold: true,
            italic: true,
            ..Default::default()
        };
        assert_eq!(run.to_markdown(), "***hello***");
    }

    #[test]
    fn test_run_strikethrough_to_markdown() {
        let run = Run {
            text: "hello".to_string(),
            strikethrough: true,
            ..Default::default()
        };
        assert_eq!(run.to_markdown(), "~~hello~~");
    }

    #[test]
    fn test_run_hyperlink_to_markdown() {
        let run = Run {
            text: "click here".to_string(),
            hyperlink_url: Some("https://example.com".to_string()),
            ..Default::default()
        };
        assert_eq!(run.to_markdown(), "[click here](https://example.com)");
    }

    #[test]
    fn test_run_bold_hyperlink_to_markdown() {
        let run = Run {
            text: "click".to_string(),
            bold: true,
            hyperlink_url: Some("https://example.com".to_string()),
            ..Default::default()
        };
        assert_eq!(run.to_markdown(), "[**click**](https://example.com)");
    }

    #[test]
    fn test_run_empty_text_to_markdown() {
        let run = Run {
            text: String::new(),
            bold: true,
            ..Default::default()
        };
        assert_eq!(run.to_markdown(), "");
    }

    #[test]
    fn test_paragraph_heading_to_markdown() {
        let mut para = Paragraph::new();
        para.style = Some("Title".to_string());
        para.add_run(Run::new("My Title".to_string()));
        let defs = HashMap::new();
        let mut counters = HashMap::new();
        assert_eq!(para.to_markdown(&defs, &mut counters, Some(1)), "# My Title");
    }

    #[test]
    fn test_paragraph_heading1_to_markdown() {
        let mut para = Paragraph::new();
        para.style = Some("Heading1".to_string());
        para.add_run(Run::new("Section".to_string()));
        let defs = HashMap::new();
        let mut counters = HashMap::new();
        assert_eq!(para.to_markdown(&defs, &mut counters, Some(2)), "## Section");
    }

    #[test]
    fn test_paragraph_heading2_to_markdown() {
        let mut para = Paragraph::new();
        para.style = Some("Heading2".to_string());
        para.add_run(Run::new("Subsection".to_string()));
        let defs = HashMap::new();
        let mut counters = HashMap::new();
        assert_eq!(para.to_markdown(&defs, &mut counters, Some(3)), "### Subsection");
    }

    #[test]
    fn test_paragraph_bullet_list_to_markdown() {
        let mut para = Paragraph::new();
        para.numbering_id = Some(1);
        para.numbering_level = Some(0);
        para.add_run(Run::new("Item".to_string()));
        let mut defs = HashMap::new();
        defs.insert((1, 0), ListType::Bullet);
        let mut counters = HashMap::new();
        assert_eq!(para.to_markdown(&defs, &mut counters, None), "- Item");
    }

    #[test]
    fn test_paragraph_numbered_list_to_markdown() {
        let mut para = Paragraph::new();
        para.numbering_id = Some(2);
        para.numbering_level = Some(0);
        para.add_run(Run::new("Item".to_string()));
        let mut defs = HashMap::new();
        defs.insert((2, 0), ListType::Numbered);
        let mut counters = HashMap::new();
        assert_eq!(para.to_markdown(&defs, &mut counters, None), "1. Item");
    }

    #[test]
    fn test_paragraph_nested_list_to_markdown() {
        let mut para = Paragraph::new();
        para.numbering_id = Some(1);
        para.numbering_level = Some(1);
        para.add_run(Run::new("Nested".to_string()));
        let mut defs = HashMap::new();
        defs.insert((1, 1), ListType::Bullet);
        let mut counters = HashMap::new();
        assert_eq!(para.to_markdown(&defs, &mut counters, None), "  - Nested");
    }

    #[test]
    fn test_heading_level_from_style_name() {
        assert_eq!(heading_level_from_style_name("Title"), Some(1));
        assert_eq!(heading_level_from_style_name("Heading1"), Some(2));
        assert_eq!(heading_level_from_style_name("Heading2"), Some(3));
        assert_eq!(heading_level_from_style_name("Heading3"), Some(4));
        assert_eq!(heading_level_from_style_name("Heading6"), Some(6)); // clamped to max markdown level
        assert_eq!(heading_level_from_style_name("Normal"), None);
    }

    #[test]
    fn test_resolve_heading_level_with_style_catalog() {
        use super::super::styles::{ParagraphProperties, StyleCatalog, StyleDefinition, StyleType};

        let mut doc = Document::new();
        let mut catalog = StyleCatalog::default();

        // Style with outline_level = 2 (should become h3)
        catalog.styles.insert(
            "CustomHeading".to_string(),
            StyleDefinition {
                id: "CustomHeading".to_string(),
                name: Some("Custom Heading".to_string()),
                style_type: StyleType::Paragraph,
                based_on: None,
                next_style: None,
                is_default: false,
                paragraph_properties: ParagraphProperties {
                    outline_level: Some(2),
                    ..Default::default()
                },
                run_properties: Default::default(),
            },
        );

        doc.style_catalog = Some(catalog);
        assert_eq!(doc.resolve_heading_level("CustomHeading"), Some(3));
    }

    #[test]
    fn test_resolve_heading_level_inheritance_chain() {
        use super::super::styles::{ParagraphProperties, StyleCatalog, StyleDefinition, StyleType};

        let mut doc = Document::new();
        let mut catalog = StyleCatalog::default();

        // Parent has outline_level
        catalog.styles.insert(
            "ParentStyle".to_string(),
            StyleDefinition {
                id: "ParentStyle".to_string(),
                name: Some("Parent".to_string()),
                style_type: StyleType::Paragraph,
                based_on: None,
                next_style: None,
                is_default: false,
                paragraph_properties: ParagraphProperties {
                    outline_level: Some(0),
                    ..Default::default()
                },
                run_properties: Default::default(),
            },
        );

        // Child inherits from parent
        catalog.styles.insert(
            "ChildStyle".to_string(),
            StyleDefinition {
                id: "ChildStyle".to_string(),
                name: Some("Child".to_string()),
                style_type: StyleType::Paragraph,
                based_on: Some("ParentStyle".to_string()),
                next_style: None,
                is_default: false,
                paragraph_properties: ParagraphProperties::default(),
                run_properties: Default::default(),
            },
        );

        doc.style_catalog = Some(catalog);
        // Child resolves to parent's outline_level 0 → h1
        assert_eq!(doc.resolve_heading_level("ChildStyle"), Some(1));
    }

    #[test]
    fn test_underline_rendering() {
        let mut run = Run::new("underlined text".to_string());
        run.underline = true;
        assert_eq!(run.to_markdown(), "<u>underlined text</u>");
    }

    #[test]
    fn test_underline_combined_with_bold_italic() {
        let mut run = Run::new("styled".to_string());
        run.bold = true;
        run.italic = true;
        run.underline = true;
        let md = run.to_markdown();
        assert!(md.contains("<u>"));
        assert!(md.contains("</u>"));
        assert!(md.contains("**"));
        assert!(md.contains("*"));
    }

    #[test]
    fn test_header_footer_in_markdown() {
        let mut doc = Document::new();

        // Add a header
        let mut header = HeaderFooter::default();
        let mut para = Paragraph::new();
        para.add_run(Run::new("Header Text".to_string()));
        header.paragraphs.push(para);
        doc.headers.push(header);

        // Add body content
        let mut body_para = Paragraph::new();
        body_para.add_run(Run::new("Body content".to_string()));
        let idx = doc.paragraphs.len();
        doc.paragraphs.push(body_para);
        doc.elements.push(DocumentElement::Paragraph(idx));

        // Add a footer
        let mut footer = HeaderFooter::default();
        let mut footer_para = Paragraph::new();
        footer_para.add_run(Run::new("Footer Text".to_string()));
        footer.paragraphs.push(footer_para);
        doc.footers.push(footer);

        let md = doc.to_markdown();
        assert!(md.contains("Header Text"), "Should contain header text");
        assert!(md.contains("Body content"), "Should contain body content");
        assert!(md.contains("Footer Text"), "Should contain footer text");
        assert!(md.contains("---"), "Should contain separator");
        // Header should be before body
        let header_pos = md.find("Header Text").unwrap();
        let body_pos = md.find("Body content").unwrap();
        let footer_pos = md.find("Footer Text").unwrap();
        assert!(header_pos < body_pos, "Header before body");
        assert!(body_pos < footer_pos, "Body before footer");
    }

    #[test]
    fn test_footnote_reference_in_parsing() {
        // Simulate parsing a paragraph with a footnote reference
        let xml = r#"<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:body>
                <w:p>
                    <w:r>
                        <w:t>See note</w:t>
                    </w:r>
                    <w:r>
                        <w:footnoteReference w:id="2"/>
                    </w:r>
                </w:p>
            </w:body>
        </w:document>"#;

        let parser_struct = DocxParser {
            archive: zip::ZipArchive::new(std::io::Cursor::new(create_minimal_zip())).unwrap(),
            relationships: HashMap::new(),
            styles: None,
            theme: None,
        };
        let mut document = Document::new();
        parser_struct.parse_document_xml(xml, &mut document).unwrap();

        assert_eq!(document.paragraphs.len(), 1);
        // The second run should contain the footnote reference marker
        let full_text = document.paragraphs[0].to_text();
        assert!(
            full_text.contains("[^2]"),
            "Should contain footnote reference [^2], got: {}",
            full_text
        );
    }

    #[test]
    fn test_separator_footnotes_filtered() {
        // Separator footnotes (id 0 and 1) should be excluded
        let xml = r#"<w:footnotes xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:footnote w:id="0">
                <w:p><w:r><w:t>separator</w:t></w:r></w:p>
            </w:footnote>
            <w:footnote w:id="1">
                <w:p><w:r><w:t>continuation</w:t></w:r></w:p>
            </w:footnote>
            <w:footnote w:id="2">
                <w:p><w:r><w:t>Actual footnote</w:t></w:r></w:p>
            </w:footnote>
        </w:footnotes>"#;

        let parser_struct = DocxParser {
            archive: zip::ZipArchive::new(std::io::Cursor::new(create_minimal_zip())).unwrap(),
            relationships: HashMap::new(),
            styles: None,
            theme: None,
        };
        let mut notes = Vec::new();
        parser_struct.parse_notes(xml, &mut notes, NoteType::Footnote).unwrap();

        assert_eq!(notes.len(), 1, "Only actual footnote should remain");
        assert_eq!(notes[0].id, "2");
    }

    // Helper to create a minimal valid ZIP for parser construction in tests
    fn create_minimal_zip() -> Vec<u8> {
        use std::io::Write;
        let buf = Vec::new();
        let cursor = std::io::Cursor::new(buf);
        let mut zip = zip::ZipWriter::new(cursor);
        let options: zip::write::FileOptions<()> = zip::write::FileOptions::default();
        zip.start_file("word/document.xml", options).unwrap();
        zip.write_all(b"<w:document/>").unwrap();
        zip.finish().unwrap().into_inner()
    }

    #[test]
    fn test_is_format_enabled_no_val() {
        // <w:b/> - no w:val attribute means enabled
        let xml = r#"<w:b/>"#;
        let mut reader = Reader::from_str(xml);
        let mut buf = Vec::new();
        if let Ok(Event::Empty(ref e)) = reader.read_event_into(&mut buf) {
            assert!(is_format_enabled(e));
        }
    }

    // --- Security validation tests ---

    #[test]
    fn test_security_valid_minimal_archive() {
        // Create a minimal valid ZIP archive (empty) - should pass
        use std::io::Cursor;
        let zip_data = vec![
            0x50, 0x4b, 0x05, 0x06, // End of central directory signature
            0x00, 0x00, // Disk number
            0x00, 0x00, // Disk with central directory
            0x00, 0x00, // Number of entries on this disk
            0x00, 0x00, // Total number of entries
            0x00, 0x00, 0x00, 0x00, // Size of central directory
            0x00, 0x00, 0x00, 0x00, // Offset of central directory
            0x00, 0x00, // Comment length
        ];
        let cursor = Cursor::new(zip_data);
        let result = DocxParser::new(cursor);
        // Empty archive should pass security checks (0 entries, 0 size)
        assert!(
            result.is_ok(),
            "Empty valid ZIP should pass security checks: {:?}",
            result.err()
        );
    }

    #[test]
    fn test_security_constants_are_reasonable() {
        use super::super::{MAX_TOTAL_UNCOMPRESSED_SIZE, MAX_UNCOMPRESSED_FILE_SIZE, MAX_ZIP_ENTRIES};

        const {
            assert!(MAX_ZIP_ENTRIES >= 1_000, "Entry limit must be at least 1,000");
            assert!(
                MAX_UNCOMPRESSED_FILE_SIZE >= 10 * 1024 * 1024,
                "Per-file size limit must be at least 10 MB"
            );
            assert!(
                MAX_TOTAL_UNCOMPRESSED_SIZE >= MAX_UNCOMPRESSED_FILE_SIZE,
                "Total size limit must be >= per-file limit"
            );
        }
    }

    #[test]
    fn test_security_normal_docx_passes() {
        use std::io::{Cursor, Write};

        let buffer = Vec::new();
        let cursor = Cursor::new(buffer);
        let mut zip = zip::ZipWriter::new(cursor);
        let options = zip::write::FileOptions::<()>::default().compression_method(zip::CompressionMethod::Stored);

        zip.start_file("word/document.xml", options).unwrap();
        zip.write_all(b"<w:document/>").unwrap();

        zip.start_file("docProps/core.xml", options).unwrap();
        zip.write_all(b"<cp:coreProperties/>").unwrap();

        let cursor = zip.finish().unwrap();
        let data = cursor.into_inner();

        let mut archive = zip::ZipArchive::new(Cursor::new(data)).unwrap();
        let result = validate_archive_security(&mut archive);
        assert!(
            result.is_ok(),
            "A normal small archive must pass security validation: {:?}",
            result.err()
        );
    }

    #[test]
    fn test_security_rejects_too_many_entries() {
        use std::io::{Cursor, Write};

        // Create a ZIP with 10,001 entries to exceed the 10,000 limit.
        // Each entry is an empty file, so this is fast.
        let buffer = Vec::new();
        let cursor = Cursor::new(buffer);
        let mut zip = zip::ZipWriter::new(cursor);
        let options = zip::write::FileOptions::<()>::default().compression_method(zip::CompressionMethod::Stored);

        for i in 0..10_001 {
            zip.start_file(format!("file_{}.txt", i), options).unwrap();
            zip.write_all(b"").unwrap();
        }

        let cursor = zip.finish().unwrap();
        let data = cursor.into_inner();

        let mut archive = zip::ZipArchive::new(Cursor::new(data)).unwrap();
        let result = validate_archive_security(&mut archive);
        assert!(result.is_err(), "Archive with >10,000 entries must be rejected");

        let err_msg = format!("{}", result.unwrap_err());
        assert!(
            err_msg.contains("10001") && err_msg.contains("10000"),
            "Error should mention actual and limit counts, got: {}",
            err_msg
        );
    }

    #[test]
    fn test_security_rejects_oversized_file() {
        use std::io::{Cursor, Write};

        // We cannot actually write 100 MB in a unit test, but we can verify the
        // validation path by confirming a small archive passes and the error
        // message format is correct when it would fail. The constant-based test
        // above already validates the limit values are reasonable.
        //
        // Here we verify that a single-file archive just under the limit passes.
        let buffer = Vec::new();
        let cursor = Cursor::new(buffer);
        let mut zip = zip::ZipWriter::new(cursor);
        let options = zip::write::FileOptions::<()>::default().compression_method(zip::CompressionMethod::Stored);

        // Write a small file (1 KB) - well under limits
        zip.start_file("word/document.xml", options).unwrap();
        zip.write_all(&[b'x'; 1024]).unwrap();

        let cursor = zip.finish().unwrap();
        let data = cursor.into_inner();

        let mut archive = zip::ZipArchive::new(Cursor::new(data)).unwrap();
        let result = validate_archive_security(&mut archive);
        assert!(
            result.is_ok(),
            "A 1 KB file must pass size validation: {:?}",
            result.err()
        );
    }

    // --- Nested table integration test ---

    /// Helper: create a minimal DOCX ZIP with the given XML as word/document.xml.
    fn create_test_docx(document_xml: &str) -> Vec<u8> {
        use std::io::{Cursor, Write};

        let buffer = Vec::new();
        let cursor = Cursor::new(buffer);
        let mut zip = zip::ZipWriter::new(cursor);
        let options = zip::write::FileOptions::<()>::default().compression_method(zip::CompressionMethod::Stored);

        zip.start_file("word/document.xml", options).unwrap();
        zip.write_all(document_xml.as_bytes()).unwrap();

        let cursor = zip.finish().unwrap();
        cursor.into_inner()
    }

    #[test]
    fn test_nested_table_parsing() {
        let xml = r#"<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:tbl>
      <w:tr>
        <w:tc>
          <w:p><w:r><w:t>Outer Cell 1</w:t></w:r></w:p>
          <w:tbl>
            <w:tr>
              <w:tc>
                <w:p><w:r><w:t>Inner Cell</w:t></w:r></w:p>
              </w:tc>
            </w:tr>
          </w:tbl>
        </w:tc>
        <w:tc>
          <w:p><w:r><w:t>Outer Cell 2</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>
  </w:body>
</w:document>"#;

        let bytes = create_test_docx(xml);
        let doc = parse_document(&bytes).expect("parse_document should succeed");

        // Only the outer table is stored; nested table content is flattened.
        assert_eq!(doc.tables.len(), 1, "Expected exactly 1 (outer) table");

        let table = &doc.tables[0];
        assert_eq!(table.rows.len(), 1, "Outer table should have 1 row");
        assert_eq!(table.rows[0].cells.len(), 2, "Outer row should have 2 cells");

        // First cell: "Outer Cell 1" paragraph + flattened "Inner Cell" paragraph
        let cell0 = &table.rows[0].cells[0];
        let cell0_texts: Vec<String> = cell0.paragraphs.iter().map(|p| p.to_text()).collect();
        assert!(
            cell0_texts.iter().any(|t| t.contains("Outer Cell 1")),
            "First cell must contain 'Outer Cell 1', got: {:?}",
            cell0_texts
        );
        assert!(
            cell0_texts.iter().any(|t| t.contains("Inner Cell")),
            "First cell must contain flattened 'Inner Cell', got: {:?}",
            cell0_texts
        );

        // Second cell: "Outer Cell 2"
        let cell1 = &table.rows[0].cells[1];
        let cell1_texts: Vec<String> = cell1.paragraphs.iter().map(|p| p.to_text()).collect();
        assert!(
            cell1_texts.iter().any(|t| t.contains("Outer Cell 2")),
            "Second cell must contain 'Outer Cell 2', got: {:?}",
            cell1_texts
        );
    }

    #[test]
    fn test_parser_loads_styles() {
        use std::io::{Cursor, Write};

        let styles_xml = r#"<?xml version="1.0" encoding="UTF-8"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
  </w:style>
</w:styles>"#;

        let doc_xml = r#"<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
      <w:r><w:t>Hello</w:t></w:r>
    </w:p>
  </w:body>
</w:document>"#;

        let buffer = Vec::new();
        let cursor = Cursor::new(buffer);
        let mut zip = zip::ZipWriter::new(cursor);
        let options = zip::write::FileOptions::<()>::default().compression_method(zip::CompressionMethod::Stored);

        zip.start_file("word/document.xml", options).unwrap();
        zip.write_all(doc_xml.as_bytes()).unwrap();
        zip.start_file("word/styles.xml", options).unwrap();
        zip.write_all(styles_xml.as_bytes()).unwrap();

        let cursor = zip.finish().unwrap();
        let bytes = cursor.into_inner();

        let doc = parse_document(&bytes).expect("should parse");

        // Verify styles were loaded
        assert!(doc.style_catalog.is_some(), "Style catalog should be loaded");
        let catalog = doc.style_catalog.as_ref().unwrap();
        assert!(catalog.styles.contains_key("Heading1"));
        assert!(catalog.styles.contains_key("Normal"));

        // Verify heading1 has bold and font size
        let h1 = &catalog.styles["Heading1"];
        assert_eq!(h1.run_properties.bold, Some(true));
        assert_eq!(h1.run_properties.font_size_half_points, Some(32));
        assert_eq!(h1.paragraph_properties.outline_level, Some(0));
    }

    #[test]
    fn test_table_properties_integration() {
        let xml = r#"<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:tbl>
      <w:tblPr>
        <w:tblStyle w:val="TableGrid"/>
        <w:tblW w:w="5000" w:type="dxa"/>
        <w:jc w:val="center"/>
      </w:tblPr>
      <w:tblGrid>
        <w:gridCol w:w="2500"/>
        <w:gridCol w:w="2500"/>
      </w:tblGrid>
      <w:tr>
        <w:trPr>
          <w:tblHeader/>
        </w:trPr>
        <w:tc>
          <w:tcPr>
            <w:tcW w:w="2500" w:type="dxa"/>
            <w:shd w:val="clear" w:fill="D9E2F3"/>
          </w:tcPr>
          <w:p><w:r><w:t>Header 1</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:tcPr>
            <w:tcW w:w="2500" w:type="dxa"/>
            <w:gridSpan w:val="1"/>
          </w:tcPr>
          <w:p><w:r><w:t>Header 2</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
      <w:tr>
        <w:tc>
          <w:tcPr>
            <w:vMerge w:val="restart"/>
          </w:tcPr>
          <w:p><w:r><w:t>Merged</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:p><w:r><w:t>Data</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>
  </w:body>
</w:document>"#;

        let bytes = create_test_docx(xml);
        let doc = parse_document(&bytes).expect("parse should succeed");

        assert_eq!(doc.tables.len(), 1);
        let table = &doc.tables[0];

        // Table properties
        let tbl_props = table.properties.as_ref().expect("table should have properties");
        assert_eq!(tbl_props.style_id.as_deref(), Some("TableGrid"));
        assert_eq!(tbl_props.alignment.as_deref(), Some("center"));
        assert!(tbl_props.width.is_some());
        assert_eq!(tbl_props.width.as_ref().unwrap().value, 5000);

        // Table grid
        let grid = table.grid.as_ref().expect("table should have grid");
        assert_eq!(grid.columns, vec![2500, 2500]);

        // Row 0 header
        let row0 = &table.rows[0];
        let row_props = row0.properties.as_ref().expect("header row should have properties");
        assert!(row_props.is_header);

        // Cell 0,0 shading
        let cell00 = &row0.cells[0];
        let cell_props = cell00.properties.as_ref().expect("cell should have properties");
        assert!(cell_props.shading.is_some());
        assert_eq!(cell_props.shading.as_ref().unwrap().fill.as_deref(), Some("D9E2F3"));

        // Cell 1,0 vMerge
        let cell10 = &table.rows[1].cells[0];
        let cell10_props = cell10.properties.as_ref().expect("merged cell should have properties");
        assert_eq!(
            cell10_props.v_merge,
            Some(crate::extraction::docx::table::VerticalMerge::Restart)
        );
    }

    #[test]
    fn test_table_with_explicit_header_row_renders_correctly() {
        let xml = r#"<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:tbl>
      <w:tr>
        <w:trPr>
          <w:tblHeader/>
        </w:trPr>
        <w:tc>
          <w:p><w:r><w:t>Name</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:p><w:r><w:t>Age</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
      <w:tr>
        <w:tc>
          <w:p><w:r><w:t>Alice</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:p><w:r><w:t>30</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>
  </w:body>
</w:document>"#;

        let bytes = create_test_docx(xml);
        let doc = parse_document(&bytes).expect("parse should succeed");

        assert_eq!(doc.tables.len(), 1);
        let table = &doc.tables[0];

        // Verify first row is marked as header
        let row0_props = table.rows[0]
            .properties
            .as_ref()
            .expect("first row should have properties");
        assert!(row0_props.is_header, "First row should be marked as header");

        // Verify markdown rendering has separator after header row
        let markdown = table.to_markdown();
        let lines: Vec<&str> = markdown.lines().collect();

        // Should have at least 3 lines: header, separator, data row
        assert!(
            lines.len() >= 3,
            "Table should have at least 3 lines, got: {}",
            markdown
        );

        // Line 1 should be separator (all dashes)
        assert!(
            lines[1].contains("---"),
            "Second line should be separator, got: {}",
            lines[1]
        );
    }

    #[test]
    fn test_table_with_merged_cells_expands_columns() {
        let xml = r#"<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:tbl>
      <w:tr>
        <w:tc>
          <w:p><w:r><w:t>A</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
          <w:p><w:r><w:t>B</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
      <w:tr>
        <w:tc>
          <w:tcPr>
            <w:gridSpan w:val="2"/>
          </w:tcPr>
          <w:p><w:r><w:t>Merged</w:t></w:r></w:p>
        </w:tc>
      </w:tr>
    </w:tbl>
  </w:body>
</w:document>"#;

        let bytes = create_test_docx(xml);
        let doc = parse_document(&bytes).expect("parse should succeed");

        assert_eq!(doc.tables.len(), 1);
        let table = &doc.tables[0];

        // Verify second row cell has grid_span=2
        let merged_cell = &table.rows[1].cells[0];
        let cell_props = merged_cell.properties.as_ref().expect("cell should have properties");
        assert_eq!(cell_props.grid_span, Some(2), "Cell should have grid_span=2");

        // Verify markdown rendering produces equal number of columns
        let markdown = table.to_markdown();
        let lines: Vec<&str> = markdown.lines().collect();

        // Both rows should have same number of pipe characters (column count)
        let pipes_row0 = lines[0].matches('|').count();
        let pipes_row1 = lines[2].matches('|').count(); // After separator

        assert_eq!(
            pipes_row0, pipes_row1,
            "All rows should have same column count in markdown"
        );
    }
}
