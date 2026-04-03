// Multi-format session recorder
//
// Records to multiple formats simultaneously:
// - Guacamole .ses (if recording_path is set)
// - Asciicast (if asciicast_path is set, or recording_path for terminal protocols)
// - Typescript (if typescript_path is set)
// - Typescript timing file (companion .timing alongside typescript)

use bytes::Bytes;
use std::collections::HashMap;
use std::io::Write;
use std::time::{Instant, SystemTime, UNIX_EPOCH};

use crate::config::RecordingConfig;
use crate::ses::{GuacamoleSesRecorder, RecordingDirection, RecordingError};

/// Multi-format session recorder
///
/// Records to multiple formats simultaneously:
/// - Guacamole .ses (if recording_path is set)
/// - Asciicast (if asciicast_path is set, or recording_path for terminal protocols)
/// - Typescript (if typescript_path is set)
pub struct MultiFormatRecorder {
    ses_recorder: Option<GuacamoleSesRecorder>,
    asciicast_writer: Option<std::io::BufWriter<std::fs::File>>,
    typescript_writer: Option<std::io::BufWriter<std::fs::File>>,
    typescript_timing_writer: Option<std::io::BufWriter<std::fs::File>>,
    start_time: Instant,
    config: RecordingConfig,
    terminal_width: u16,
    terminal_height: u16,
}

impl MultiFormatRecorder {
    /// Create a new multi-format recorder
    pub fn new(
        config: &RecordingConfig,
        params: &HashMap<String, String>,
        protocol: &str,
        terminal_width: u16,
        terminal_height: u16,
    ) -> Result<Self, RecordingError> {
        let ses_recorder = if let Some(path) = config.get_ses_path(params, protocol) {
            Some(GuacamoleSesRecorder::new(&path, config)?)
        } else {
            None
        };

        let asciicast_writer = if let Some(path) = config.get_asciicast_path(params, protocol) {
            // Create directory if needed
            if let Some(parent) = path.parent() {
                if !parent.exists() && config.create_recording_path {
                    std::fs::create_dir_all(parent)?;
                }
            }

            // Check file exists
            if path.exists() && !config.recording_write_existing {
                return Err(RecordingError::FileExists(format!(
                    "File exists: {:?}",
                    path
                )));
            }

            let file = std::fs::File::create(&path)?;
            let mut writer = std::io::BufWriter::new(file);

            // Write asciicast v2 header
            let timestamp = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs();
            let header = format!(
                r#"{{"version":2,"width":{},"height":{},"timestamp":{}}}"#,
                terminal_width, terminal_height, timestamp
            );
            writeln!(writer, "{}", header)?;
            writer.flush()?;

            Some(writer)
        } else {
            None
        };

        let (typescript_writer, typescript_timing_writer) =
            if let Some(path) = config.get_typescript_path(params, protocol) {
                // Create directory if needed
                if let Some(parent) = path.parent() {
                    if !parent.exists() && config.create_typescript_path {
                        std::fs::create_dir_all(parent)?;
                    }
                }

                // Check file exists
                if path.exists() && !config.typescript_write_existing {
                    return Err(RecordingError::FileExists(format!(
                        "File exists: {:?}",
                        path
                    )));
                }

                let file = std::fs::File::create(&path)?;
                let mut writer = std::io::BufWriter::new(file);

                // Write typescript header
                let now = chrono::Utc::now();
                writeln!(writer, "Script started on {}", now.format("%c"))?;
                writer.flush()?;

                // Create companion .timing file for scriptreplay
                let timing_path = path.with_extension("timing");
                let timing_file = std::fs::File::create(&timing_path)?;
                let timing_writer = std::io::BufWriter::new(timing_file);

                (Some(writer), Some(timing_writer))
            } else {
                (None, None)
            };

        Ok(Self {
            ses_recorder,
            asciicast_writer,
            typescript_writer,
            typescript_timing_writer,
            start_time: Instant::now(),
            config: config.clone(),
            terminal_width,
            terminal_height,
        })
    }

    /// Check if any recording is active
    pub fn is_active(&self) -> bool {
        self.ses_recorder.is_some()
            || self.asciicast_writer.is_some()
            || self.typescript_writer.is_some()
    }

    /// Record a Guacamole protocol instruction (.ses format)
    pub fn record_instruction(
        &mut self,
        direction: RecordingDirection,
        instruction: &Bytes,
    ) -> Result<(), RecordingError> {
        if let Some(ref mut recorder) = self.ses_recorder {
            recorder.record(direction, instruction)?;
        }
        Ok(())
    }

    /// Record terminal output (asciicast + typescript)
    pub fn record_output(&mut self, data: &[u8]) -> Result<(), RecordingError> {
        let elapsed = self.start_time.elapsed().as_secs_f64();

        // Asciicast format: [time, "o", "data"]
        if let Some(ref mut writer) = self.asciicast_writer {
            let data_str = String::from_utf8_lossy(data);
            // Escape JSON string
            let escaped = data_str
                .replace('\\', "\\\\")
                .replace('"', "\\\"")
                .replace('\n', "\\n")
                .replace('\r', "\\r")
                .replace('\t', "\\t");
            writeln!(writer, r#"[{:.6},"o","{}"]"#, elapsed, escaped)?;
        }

        // Typescript format: raw output
        if let Some(ref mut writer) = self.typescript_writer {
            writer.write_all(data)?;
        }

        // Typescript timing: elapsed_seconds byte_count
        if let Some(ref mut timing_writer) = self.typescript_timing_writer {
            writeln!(timing_writer, "{:.6} {}", elapsed, data.len())?;
        }

        Ok(())
    }

    /// Record keyboard input (asciicast, if recording_include_keys)
    pub fn record_input(&mut self, data: &[u8]) -> Result<(), RecordingError> {
        if !self.config.recording_include_keys {
            return Ok(());
        }

        let elapsed = self.start_time.elapsed().as_secs_f64();

        // Asciicast format: [time, "i", "data"]
        if let Some(ref mut writer) = self.asciicast_writer {
            let data_str = String::from_utf8_lossy(data);
            let escaped = data_str
                .replace('\\', "\\\\")
                .replace('"', "\\\"")
                .replace('\n', "\\n")
                .replace('\r', "\\r")
                .replace('\t', "\\t");
            writeln!(writer, r#"[{:.6},"i","{}"]"#, elapsed, escaped)?;
        }

        Ok(())
    }

    /// Record terminal resize
    pub fn record_resize(&mut self, cols: u16, rows: u16) -> Result<(), RecordingError> {
        self.terminal_width = cols;
        self.terminal_height = rows;

        let elapsed = self.start_time.elapsed().as_secs_f64();

        // Asciicast format: [time, "r", "COLSxROWS"]
        if let Some(ref mut writer) = self.asciicast_writer {
            writeln!(writer, r#"[{:.6},"r","{}x{}"]"#, elapsed, cols, rows)?;
        }

        Ok(())
    }

    /// Flush all writers
    pub fn flush(&mut self) -> Result<(), RecordingError> {
        if let Some(ref mut recorder) = self.ses_recorder {
            recorder.writer.flush()?;
        }
        if let Some(ref mut writer) = self.asciicast_writer {
            writer.flush()?;
        }
        if let Some(ref mut writer) = self.typescript_writer {
            writer.flush()?;
        }
        if let Some(ref mut writer) = self.typescript_timing_writer {
            writer.flush()?;
        }
        Ok(())
    }

    /// Finalize all recordings
    ///
    /// This method should be called explicitly when the session ends normally.
    /// The `Drop` implementation provides a safety net for abnormal termination.
    pub fn finalize(mut self) -> Result<(), RecordingError> {
        self.finalize_internal()
    }

    /// Internal finalization logic (used by both finalize and Drop)
    fn finalize_internal(&mut self) -> Result<(), RecordingError> {
        // Finalize .ses
        if let Some(recorder) = self.ses_recorder.take() {
            recorder.finalize()?;
        }

        // Finalize asciicast (no footer needed)
        if let Some(mut writer) = self.asciicast_writer.take() {
            writer.flush()?;
        }

        // Finalize typescript
        if let Some(mut writer) = self.typescript_writer.take() {
            let now = chrono::Utc::now();
            writeln!(writer, "\nScript done on {}", now.format("%c"))?;
            writer.flush()?;
        }

        // Finalize typescript timing
        if let Some(mut writer) = self.typescript_timing_writer.take() {
            writer.flush()?;
        }

        Ok(())
    }
}

/// RAII: Ensure recording files are flushed even on early return or panic
impl Drop for MultiFormatRecorder {
    fn drop(&mut self) {
        // Only finalize if not already done (writers still present)
        if self.ses_recorder.is_some()
            || self.asciicast_writer.is_some()
            || self.typescript_writer.is_some()
        {
            if let Err(e) = self.finalize_internal() {
                // Can't propagate error from Drop, just log it
                log::warn!("Recording finalization failed during drop: {}", e);
            }
        }
    }
}
