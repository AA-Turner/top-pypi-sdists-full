// CSV Export for Database Handlers
//
// Implements file download of query results as CSV via the Guacamole protocol.
// Supports cancellation via Ctrl+C and streaming for large result sets.
//
// Based on the KCM libguac-client-db export implementation.

use bytes::Bytes;
use guacr_terminal::QueryResult;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use tokio::sync::mpsc;

/// CSV exporter for streaming query results to the client as a file download
pub struct CsvExporter {
    /// Unique stream index for this export
    stream_index: i32,

    /// Buffer for accumulating CSV data before sending
    pub(crate) buffer: Vec<u8>,

    /// Maximum blob size for Guacamole protocol (6KB)
    max_blob_size: usize,

    /// Flag to signal cancellation
    cancelled: Arc<AtomicBool>,
}

impl CsvExporter {
    /// Create a new CSV exporter
    ///
    /// # Arguments
    /// * `stream_index` - Unique stream identifier (should be unique per connection)
    pub fn new(stream_index: i32) -> Self {
        Self {
            stream_index,
            buffer: Vec::with_capacity(6144),
            max_blob_size: 6144, // GUAC_PROTOCOL_BLOB_MAX_LENGTH
            cancelled: Arc::new(AtomicBool::new(false)),
        }
    }

    /// Get a cancellation handle that can be used to cancel the export
    pub fn cancellation_handle(&self) -> Arc<AtomicBool> {
        Arc::clone(&self.cancelled)
    }

    /// Check if the export has been cancelled
    pub fn is_cancelled(&self) -> bool {
        self.cancelled.load(Ordering::SeqCst)
    }

    /// Cancel the export
    pub fn cancel(&self) {
        self.cancelled.store(true, Ordering::SeqCst);
    }

    /// Start a file download by sending the Guacamole "file" instruction
    ///
    /// Returns the instruction to send to the client.
    ///
    /// Guacamole LENGTH fields count Unicode codepoints, not UTF-8 bytes.
    /// Using `.len()` (bytes) produces wrong length prefixes for filenames that
    /// contain non-ASCII characters. Use `.chars().count()` for all LENGTH fields.
    pub fn start_download(&self, filename: &str) -> Bytes {
        // 4.file,<stream-len>.<stream>,<mime-len>.<mime>,<name-len>.<name>;
        let stream = self.stream_index.to_string();
        let mimetype = "text/csv";
        Bytes::from(format!(
            "4.file,{}.{},{}.{},{}.{};",
            stream.chars().count(),
            stream,
            mimetype.chars().count(),
            mimetype,
            filename.chars().count(),
            filename,
        ))
    }

    /// Export query results as CSV, yielding Guacamole blob instructions
    ///
    /// This streams the CSV data in chunks suitable for the Guacamole protocol.
    pub async fn export_query_result(
        &mut self,
        result: &QueryResult,
        to_client: &mpsc::Sender<Bytes>,
    ) -> Result<(), String> {
        if self.is_cancelled() {
            return Err("Export cancelled".to_string());
        }

        // Write header row
        self.write_csv_row(&result.columns)?;

        // Flush if buffer is getting full
        self.maybe_flush(to_client).await?;

        // Write data rows
        for row in &result.rows {
            if self.is_cancelled() {
                return Err("Export cancelled".to_string());
            }

            self.write_csv_row(row)?;
            self.maybe_flush(to_client).await?;
        }

        // Final flush
        self.flush(to_client).await?;

        // Send end instruction
        self.send_end(to_client).await?;

        Ok(())
    }

    /// Write a row of CSV data to the internal buffer
    fn write_csv_row(&mut self, fields: &[String]) -> Result<(), String> {
        for (i, field) in fields.iter().enumerate() {
            self.write_csv_field(field);
            if i < fields.len() - 1 {
                self.buffer.push(b',');
            }
        }
        self.buffer.extend_from_slice(b"\r\n");
        Ok(())
    }

    /// Write a single CSV field, escaping as needed
    pub(crate) fn write_csv_field(&mut self, field: &str) {
        write_csv_field_to_buf(&mut self.buffer, field);
    }

    /// Flush buffer if it exceeds the max blob size
    async fn maybe_flush(&mut self, to_client: &mpsc::Sender<Bytes>) -> Result<(), String> {
        if self.buffer.len() >= self.max_blob_size {
            self.flush(to_client).await?;
        }
        Ok(())
    }

    /// Flush the buffer, sending a blob instruction
    async fn flush(&mut self, to_client: &mpsc::Sender<Bytes>) -> Result<(), String> {
        if self.buffer.is_empty() {
            return Ok(());
        }

        if self.is_cancelled() {
            return Err("Export cancelled".to_string());
        }

        // Send blob instruction
        // 4.blob,<stream-index>,<base64-data>;
        let data_base64 = base64_encode(&self.buffer);
        let instruction = format!(
            "4.blob,{}.{},{}.{};",
            self.stream_index.to_string().len(),
            self.stream_index,
            data_base64.len(),
            data_base64
        );

        to_client
            .send(Bytes::from(instruction))
            .await
            .map_err(|e| format!("Failed to send blob: {}", e))?;

        self.buffer.clear();
        Ok(())
    }

    /// Send the end instruction to complete the download
    async fn send_end(&self, to_client: &mpsc::Sender<Bytes>) -> Result<(), String> {
        // 3.end,<stream-index>;
        let instruction = format!(
            "3.end,{}.{};",
            self.stream_index.to_string().len(),
            self.stream_index
        );

        to_client
            .send(Bytes::from(instruction))
            .await
            .map_err(|e| format!("Failed to send end: {}", e))?;

        Ok(())
    }

    /// Send an ack instruction (used for responding to client acks)
    pub fn create_ack_instruction(&self, message: &str, status: u16) -> Bytes {
        // 3.ack,<stream-index>,<message>,<status>;
        let instruction = format!(
            "3.ack,{}.{},{}.{},{}.{};",
            self.stream_index.to_string().len(),
            self.stream_index,
            message.len(),
            message,
            status.to_string().len(),
            status
        );
        Bytes::from(instruction)
    }
}

/// Write a single CSV field value to a byte buffer, applying:
/// - Quote-wrapping when the value contains commas, quotes, or newlines
/// - Formula injection prevention: cells starting with `=`, `+`, `-`, or `@`
///   are prefixed with a tab character so spreadsheet apps treat them as text
pub(crate) fn write_csv_field_to_buf(buf: &mut Vec<u8>, field: &str) {
    // Prepend tab to neutralize spreadsheet formula prefixes.
    // This is the standard defense recommended by OWASP for CSV injection.
    let safe_field: std::borrow::Cow<str> = if field.starts_with(['=', '+', '-', '@']) {
        std::borrow::Cow::Owned(format!("\t{field}"))
    } else {
        std::borrow::Cow::Borrowed(field)
    };

    let needs_quoting = safe_field.contains(',')
        || safe_field.contains('"')
        || safe_field.contains('\n')
        || safe_field.contains('\r')
        || safe_field.contains('\t'); // tab-prefixed values need quoting

    if needs_quoting {
        buf.push(b'"');
        for ch in safe_field.bytes() {
            if ch == b'"' {
                buf.push(b'"'); // double-escape
            }
            buf.push(ch);
        }
        buf.push(b'"');
    } else {
        buf.extend_from_slice(safe_field.as_bytes());
    }
}

/// Simple base64 encoding (without external dependency)
pub(crate) fn base64_encode(data: &[u8]) -> String {
    const ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    let mut result = Vec::with_capacity(data.len().div_ceil(3) * 4);

    for chunk in data.chunks(3) {
        let b0 = chunk[0] as u32;
        let b1 = chunk.get(1).copied().unwrap_or(0) as u32;
        let b2 = chunk.get(2).copied().unwrap_or(0) as u32;

        let n = (b0 << 16) | (b1 << 8) | b2;

        result.push(ALPHABET[((n >> 18) & 0x3F) as usize]);
        result.push(ALPHABET[((n >> 12) & 0x3F) as usize]);

        if chunk.len() > 1 {
            result.push(ALPHABET[((n >> 6) & 0x3F) as usize]);
        } else {
            result.push(b'=');
        }

        if chunk.len() > 2 {
            result.push(ALPHABET[(n & 0x3F) as usize]);
        } else {
            result.push(b'=');
        }
    }

    // Safe because we only used ASCII bytes
    String::from_utf8(result).unwrap()
}

/// Helper to generate a unique filename for CSV export
pub fn generate_csv_filename(query: &str, database_type: &str) -> String {
    use std::time::{SystemTime, UNIX_EPOCH};

    // Get timestamp
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0);

    // Extract table name from query if possible
    let table_name = extract_table_name(query).unwrap_or("query");

    format!("{}_{}_export_{}.csv", database_type, table_name, timestamp)
}

/// Try to extract a table name from a SELECT query
pub(crate) fn extract_table_name(query: &str) -> Option<&str> {
    let query_upper = query.to_uppercase();

    // Look for FROM clause
    if let Some(from_pos) = query_upper.find(" FROM ") {
        let after_from = &query[from_pos + 6..];
        // Get the first word after FROM
        let table = after_from.split_whitespace().next()?;
        // Remove any trailing punctuation
        let table = table.trim_end_matches(|c: char| !c.is_alphanumeric() && c != '_');
        if !table.is_empty() {
            return Some(table);
        }
    }

    None
}
