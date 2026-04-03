// Guacamole .ses format recorder
//
// Records Guacamole protocol instructions in the native format compatible with
// guacenc (video encoding) and guaclog (text logging) utilities.
//
// Format: Raw Guacamole protocol instructions written sequentially, one per line.
// Each instruction is in standard Guacamole protocol format:
// `LENGTH.OPCODE,LENGTH.ARG1,LENGTH.ARG2,...;`
//
// There is NO timestamp prefix. The Apache Guacamole recording format is simply
// the raw protocol stream. Client-to-server instructions (mouse, key) can
// optionally be recorded with their timestamp parameter for playback.

use async_trait::async_trait;
use bytes::Bytes;
use std::io::Write;
use std::time::Instant;

use crate::config::{find_unique_path, RecordingConfig};
use crate::helpers::{extract_opcode, inject_timestamp, is_drawing_instruction};

/// Recording direction (for .ses format)
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum RecordingDirection {
    /// Server to client (output)
    ServerToClient = 0,
    /// Client to server (input)
    ClientToServer = 1,
}

/// Recording error
#[derive(Debug, thiserror::Error)]
pub enum RecordingError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Path creation failed: {0}")]
    PathCreation(String),

    #[error("File exists and overwrite not allowed: {0}")]
    FileExists(String),

    #[error("Recording disabled")]
    Disabled,
}

/// Session recorder trait for all formats
///
/// Implemented by protocol handlers to record session data.
#[async_trait]
pub trait SessionRecorder: Send + Sync {
    /// Record a Guacamole protocol instruction
    fn record_instruction(
        &mut self,
        direction: RecordingDirection,
        instruction: &Bytes,
    ) -> Result<(), RecordingError>;

    /// Record terminal output (for asciicast/typescript)
    fn record_output(&mut self, data: &[u8]) -> Result<(), RecordingError>;

    /// Record keyboard input (if recording_include_keys is true)
    fn record_input(&mut self, data: &[u8]) -> Result<(), RecordingError>;

    /// Record terminal resize
    fn record_resize(&mut self, cols: u16, rows: u16) -> Result<(), RecordingError>;

    /// Flush all buffers
    fn flush(&mut self) -> Result<(), RecordingError>;

    /// Finalize recording (close files, upload, etc.)
    async fn finalize(self: Box<Self>) -> Result<(), RecordingError>;
}

/// Guacamole .ses format recorder
///
/// Records Guacamole protocol instructions in the native format
/// compatible with guacenc (video encoding) and guaclog (text logging) utilities.
///
/// **Format**: Raw Guacamole protocol instructions written sequentially.
/// Each instruction is in standard Guacamole protocol format:
/// `LENGTH.OPCODE,LENGTH.ARG1,LENGTH.ARG2,...;`
///
/// Timing information is embedded via `sync` instructions in the stream.
/// The recording is essentially a replay of all server-to-client instructions.
///
/// **Note**: Unlike some documentation suggests, there is NO timestamp prefix.
/// The Apache Guacamole recording format is simply the raw protocol stream.
/// Client-to-server instructions (mouse, key) can optionally be recorded with
/// their timestamp parameter for playback.
pub struct GuacamoleSesRecorder {
    pub(crate) writer: std::io::BufWriter<std::fs::File>,
    start_time: Instant,
    config: RecordingConfig,
    last_sync_ms: u64,
}

impl GuacamoleSesRecorder {
    /// Create a new .ses recorder
    pub fn new(path: &std::path::Path, config: &RecordingConfig) -> Result<Self, RecordingError> {
        // Check if directory exists, create if allowed
        if let Some(parent) = path.parent() {
            if !parent.exists() {
                if config.create_recording_path {
                    std::fs::create_dir_all(parent)?;
                } else {
                    return Err(RecordingError::PathCreation(format!(
                        "Directory does not exist: {:?}",
                        parent
                    )));
                }
            }
        }

        // Resolve to a unique path if the file exists and overwrite is not allowed
        let actual_path = if path.exists() && !config.recording_write_existing {
            find_unique_path(path, 255).ok_or_else(|| {
                RecordingError::FileExists(format!("All candidate paths exhausted for: {:?}", path))
            })?
        } else {
            path.to_path_buf()
        };

        let file = std::fs::File::create(&actual_path)?;
        let writer = std::io::BufWriter::new(file);

        Ok(Self {
            writer,
            start_time: Instant::now(),
            config: config.clone(),
            last_sync_ms: 0,
        })
    }

    /// Record an instruction to the .ses file
    ///
    /// Instructions are written in raw Guacamole protocol format.
    /// For server-to-client, instructions are written as-is.
    /// For client-to-server (mouse, key), a timestamp argument is appended
    /// so that guacenc knows when input events occurred.
    pub fn record(
        &mut self,
        direction: RecordingDirection,
        instruction: &Bytes,
    ) -> Result<(), RecordingError> {
        let instr_str = String::from_utf8_lossy(instruction);

        // Check exclusion filters
        if self.config.recording_exclude_output && direction == RecordingDirection::ServerToClient {
            // Filter all drawing instructions but keep sync (timing) and size (dimensions)
            let opcode = extract_opcode(&instr_str);
            if is_drawing_instruction(&instr_str) && opcode != "sync" && opcode != "size" {
                return Ok(());
            }
        }

        if self.config.recording_exclude_mouse
            && direction == RecordingDirection::ClientToServer
            && instr_str.starts_with("5.mouse,")
        {
            return Ok(()); // Skip mouse events
        }

        if !self.config.recording_include_keys
            && direction == RecordingDirection::ClientToServer
            && instr_str.starts_with("3.key,")
        {
            return Ok(()); // Skip key events unless explicitly enabled
        }

        // For client-to-server mouse/key, inject a timestamp argument
        // so guacenc can replay input events with correct timing.
        if direction == RecordingDirection::ClientToServer {
            let opcode = extract_opcode(&instr_str);
            if opcode == "mouse" || opcode == "key" {
                let timestamped = inject_timestamp(&instr_str);
                self.writer.write_all(timestamped.as_bytes())?;
                if !timestamped.ends_with('\n') {
                    self.writer.write_all(b"\n")?;
                }
                return self.maybe_flush();
            }
        }

        // Write the raw instruction (Guacamole protocol format)
        self.writer.write_all(instruction)?;

        // Ensure newline for readability (matches guacd behavior)
        if !instruction.ends_with(b"\n") {
            self.writer.write_all(b"\n")?;
        }

        self.maybe_flush()
    }

    /// Flush writer periodically (~every 5 seconds)
    fn maybe_flush(&mut self) -> Result<(), RecordingError> {
        let timestamp_ms = self.start_time.elapsed().as_millis() as u64;
        if timestamp_ms - self.last_sync_ms > 5000 {
            self.writer.flush()?;
            self.last_sync_ms = timestamp_ms;
        }
        Ok(())
    }

    /// Flush and close the recording
    ///
    /// This method should be called explicitly when the session ends normally.
    /// The `Drop` implementation provides a safety net for abnormal termination.
    pub fn finalize(mut self) -> Result<(), RecordingError> {
        self.flush_internal()
    }

    /// Internal flush logic
    fn flush_internal(&mut self) -> Result<(), RecordingError> {
        self.writer.flush()?;
        Ok(())
    }
}

/// RAII: Ensure recording file is flushed even on early return or panic
impl Drop for GuacamoleSesRecorder {
    fn drop(&mut self) {
        // Attempt to flush any remaining buffered data
        if let Err(e) = self.writer.flush() {
            log::warn!("Failed to flush .ses recording during drop: {}", e);
        }
    }
}
