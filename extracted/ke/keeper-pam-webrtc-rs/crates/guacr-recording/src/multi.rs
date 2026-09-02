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
use crate::zmq_transport::ZmqRecordingSender;

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
    zmq_sender: Option<ZmqRecordingSender>,
    start_time: Instant,
    config: RecordingConfig,
    terminal_width: u16,
    terminal_height: u16,
    /// Timestamp of last periodic file flush (ms since session start).
    last_flush_ms: u64,
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

                // Write typescript header — matches guacd format expected by Keeper player
                writeln!(writer, "[BEGIN TYPESCRIPT]")?;
                writer.flush()?;

                // Companion timing file: same stem as the typescript file so multiple
                // recordings in the same directory never collide.
                // e.g. "session" → "session.timing", "session.ts" → "session.timing.txt"
                let timing_path = if path.extension().is_some() {
                    path.with_extension("timing.txt")
                } else {
                    path.with_extension("timing")
                };
                let timing_file = std::fs::File::create(&timing_path)?;
                let timing_writer = std::io::BufWriter::new(timing_file);

                (Some(writer), Some(timing_writer))
            } else {
                (None, None)
            };

        let zmq_sender = if let Some(ref addr) = config.zmq_addr {
            match ZmqRecordingSender::connect(addr, config.allow_unrecorded) {
                Ok(s) => {
                    // Send asciicast v2 header line immediately so Python's
                    // RecordingReader sees a valid asciicast stream from the start.
                    let timestamp = SystemTime::now()
                        .duration_since(UNIX_EPOCH)
                        .unwrap()
                        .as_secs();
                    let header = format!(
                        "{}\n",
                        serde_json::json!({
                            "version": 2,
                            "width": terminal_width,
                            "height": terminal_height,
                            "timestamp": timestamp
                        })
                    );
                    if let Err(e) = s.send(header.as_bytes()) {
                        log::warn!("ZMQ: failed to send asciicast header: {}", e);
                    }
                    Some(s)
                }
                Err(e) => {
                    log::warn!("ZMQ recording unavailable ({}): {}", addr, e);
                    None
                }
            }
        } else {
            None
        };

        Ok(Self {
            ses_recorder,
            asciicast_writer,
            typescript_writer,
            typescript_timing_writer,
            zmq_sender,
            start_time: Instant::now(),
            config: config.clone(),
            terminal_width,
            terminal_height,
            last_flush_ms: 0,
        })
    }

    /// Check if any recording is active
    pub fn is_active(&self) -> bool {
        self.ses_recorder.is_some()
            || self.asciicast_writer.is_some()
            || self.typescript_writer.is_some()
            || self.zmq_sender.is_some()
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

    /// Record terminal output (asciicast + typescript + ZMQ)
    pub fn record_output(&mut self, data: &[u8]) -> Result<(), RecordingError> {
        let elapsed = self.start_time.elapsed().as_secs_f64();

        // Asciicast format: [time, "o", "data"]
        let asciicast_line = {
            let data_str = String::from_utf8_lossy(data);
            let escaped = escape_for_json(&data_str);
            format!("[{:.6},\"o\",\"{}\"]\n", elapsed, escaped)
        };

        if let Some(ref mut writer) = self.asciicast_writer {
            writer.write_all(asciicast_line.as_bytes())?;
        }

        // ZMQ: stream asciicast event line to Python for encryption + upload.
        // Non-blocking: try_send avoids blocking the async Tokio runtime when
        // Python is slow to consume. Under load (e.g. cmatrix) dropped events
        // are acceptable when allow_unrecorded=true; strict sessions fail fast.
        if let Some(ref sender) = self.zmq_sender {
            if let Err(e) = sender.try_send(asciicast_line.as_bytes()) {
                if !self.config.allow_unrecorded {
                    return Err(e);
                }
                log::warn!("ZMQ recording send failed (allow-unrecorded=true): {}", e);
            }
        }

        // Typescript format: raw output
        if let Some(ref mut writer) = self.typescript_writer {
            writer.write_all(data)?;
        }

        // Typescript timing: elapsed_seconds byte_count
        if let Some(ref mut timing_writer) = self.typescript_timing_writer {
            writeln!(timing_writer, "{:.6} {}", elapsed, data.len())?;
        }

        // Periodic flush every 5s — ensures data reaches disk if the session
        // ends unexpectedly before finalize() can flush the BufWriter.
        self.maybe_flush_periodic()?;

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
            let escaped = escape_for_json(&data_str);
            writeln!(writer, r#"[{:.6},"i","{}"]"#, elapsed, escaped)?;
        }

        Ok(())
    }

    /// Record terminal resize
    pub fn record_resize(&mut self, cols: u16, rows: u16) -> Result<(), RecordingError> {
        self.terminal_width = cols;
        self.terminal_height = rows;

        let elapsed = self.start_time.elapsed().as_secs_f64();

        let resize_line = format!("[{:.6},\"r\",\"{}x{}\"]\n", elapsed, cols, rows);

        if let Some(ref mut writer) = self.asciicast_writer {
            writer.write_all(resize_line.as_bytes())?;
        }

        if let Some(ref sender) = self.zmq_sender {
            if let Err(e) = sender.try_send(resize_line.as_bytes()) {
                if !self.config.allow_unrecorded {
                    return Err(e);
                }
                log::warn!("ZMQ resize send failed (allow-unrecorded=true): {}", e);
            }
        }

        Ok(())
    }

    /// Flush file writers periodically (~every 5 seconds). Called from record_output
    /// so recent recording data reaches disk even if the session ends abruptly.
    fn maybe_flush_periodic(&mut self) -> Result<(), RecordingError> {
        let now_ms = self.start_time.elapsed().as_millis() as u64;
        if now_ms.saturating_sub(self.last_flush_ms) > 5000 {
            self.last_flush_ms = now_ms;
            if let Some(ref mut writer) = self.asciicast_writer {
                writer.flush()?;
            }
            if let Some(ref mut writer) = self.typescript_writer {
                writer.flush()?;
            }
            if let Some(ref mut writer) = self.typescript_timing_writer {
                writer.flush()?;
            }
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

        // Finalize typescript — matches guacd format expected by Keeper player
        if let Some(mut writer) = self.typescript_writer.take() {
            writeln!(writer, "[END TYPESCRIPT]")?;
            writer.flush()?;
        }

        // Finalize typescript timing
        if let Some(mut writer) = self.typescript_timing_writer.take() {
            writer.flush()?;
        }

        // Close ZMQ sender — signals end-of-recording to Python.
        if let Some(sender) = self.zmq_sender.take() {
            sender.close();
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
            || self.zmq_sender.is_some()
        {
            if let Err(e) = self.finalize_internal() {
                // Can't propagate error from Drop, just log it
                log::warn!("Recording finalization failed during drop: {}", e);
            }
        }
    }
}

/// Escape a string for embedding in a JSON string value.
/// All control characters (U+0000–U+001F) must be escaped per RFC 8259.
/// Named escapes: \\ \" \n \r \t. All others: \uXXXX.
fn escape_for_json(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    for ch in s.chars() {
        match ch {
            '\\' => out.push_str("\\\\"),
            '"' => out.push_str("\\\""),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => {
                // All other control characters must be \uXXXX
                out.push_str(&format!("\\u{:04x}", c as u32));
            }
            c => out.push(c),
        }
    }
    out
}
