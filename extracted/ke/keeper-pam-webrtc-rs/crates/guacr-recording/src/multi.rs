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
#[cfg(unix)]
use crate::fifo_open;
use crate::ses::{GuacamoleSesRecorder, RecordingDirection, RecordingError, SesPayload};
use crate::writer_thread::{OffloadSink, RecordingWriter, SinkId, SinkTarget};
#[cfg(feature = "zmq-transport")]
use crate::zmq_transport::ZmqRecordingSender;

/// Multi-format session recorder
///
/// Records to multiple formats simultaneously:
/// - Guacamole .ses (if recording_path is set)
/// - Asciicast (if asciicast_path is set, or recording_path for terminal protocols)
/// - Typescript (if typescript_path is set)
pub struct MultiFormatRecorder {
    ses_recorder: Option<GuacamoleSesRecorder>,
    asciicast_writer: Option<std::io::BufWriter<OffloadSink>>,
    typescript_writer: Option<std::io::BufWriter<OffloadSink>>,
    typescript_timing_writer: Option<std::io::BufWriter<OffloadSink>>,
    /// Owns the file descriptors and does the blocking writes. Declared after the
    /// writers so it is dropped last: joining the thread while a sink still holds a
    /// queue sender would wait forever.
    file_writer: Option<RecordingWriter>,
    #[cfg(feature = "zmq-transport")]
    zmq_sender: Option<ZmqRecordingSender>,
    start_time: Instant,
    config: RecordingConfig,
    terminal_width: u16,
    terminal_height: u16,
    /// Timestamp of last periodic file flush (ms since session start).
    last_flush_ms: u64,
}

impl MultiFormatRecorder {
    pub async fn new_async(
        config: &RecordingConfig,
        params: &HashMap<String, String>,
        protocol: &str,
        terminal_width: u16,
        terminal_height: u16,
    ) -> Result<Self, RecordingError> {
        Self::new_with_payload_async(
            config,
            params,
            protocol,
            terminal_width,
            terminal_height,
            SesPayload::Guacamole,
        )
        .await
    }

    pub async fn new_with_payload_async(
        config: &RecordingConfig,
        params: &HashMap<String, String>,
        protocol: &str,
        terminal_width: u16,
        terminal_height: u16,
        payload: SesPayload,
    ) -> Result<Self, RecordingError> {
        Self::new_with_payload_async_for(
            config,
            params,
            protocol,
            terminal_width,
            terminal_height,
            payload,
            std::time::Duration::from_secs(30),
        )
        .await
    }

    pub(crate) async fn new_with_payload_async_for(
        config: &RecordingConfig,
        params: &HashMap<String, String>,
        protocol: &str,
        terminal_width: u16,
        terminal_height: u16,
        payload: SesPayload,
        wait: std::time::Duration,
    ) -> Result<Self, RecordingError> {
        #[cfg(unix)]
        {
            let targets = fifo_open::prepare(config, params, protocol, wait)
                .await
                .map_err(|err| Self::classify_open_error(config, err))?;
            Self::open_destinations(
                config,
                params,
                protocol,
                terminal_width,
                terminal_height,
                payload,
                Some(targets),
            )
            .map_err(|err| Self::classify_open_error(config, err))
        }
        #[cfg(not(unix))]
        {
            let config = config.clone();
            let params = params.clone();
            let protocol = protocol.to_owned();
            tokio::task::spawn_blocking(move || {
                Self::new_with_payload(
                    &config,
                    &params,
                    &protocol,
                    terminal_width,
                    terminal_height,
                    payload,
                )
            })
            .await
            .map_err(|err| RecordingError::Unrecordable(err.to_string()))?
        }
    }

    fn classify_open_error(config: &RecordingConfig, err: RecordingError) -> RecordingError {
        if config.allow_unrecorded {
            err
        } else {
            RecordingError::Unrecordable(format!(
                "recording is required but a destination could not be opened: {err}"
            ))
        }
    }

    pub fn has_ses_recorder(&self) -> bool {
        self.ses_recorder.is_some()
    }

    /// Create a new multi-format recorder writing a guacd-shaped `.ses`.
    ///
    /// Correct for the graphical protocols, which send text drawing instructions. The
    /// terminal family sends binary opcode frames and must use
    /// [`MultiFormatRecorder::new_with_payload`] so the recording declares itself.
    pub fn new(
        config: &RecordingConfig,
        params: &HashMap<String, String>,
        protocol: &str,
        terminal_width: u16,
        terminal_height: u16,
    ) -> Result<Self, RecordingError> {
        Self::new_with_payload(
            config,
            params,
            protocol,
            terminal_width,
            terminal_height,
            SesPayload::Guacamole,
        )
    }

    /// Create a new multi-format recorder for a given `.ses` payload shape.
    ///
    /// When `allow_unrecorded` is false the caller has been told no recording means no
    /// session, so a destination that cannot be opened is reported as
    /// [`RecordingError::Unrecordable`] rather than the underlying I/O error. Handlers
    /// treat an ordinary open failure as advisory and continue; `Unrecordable` is the
    /// signal that continuing is not allowed.
    pub fn new_with_payload(
        config: &RecordingConfig,
        params: &HashMap<String, String>,
        protocol: &str,
        terminal_width: u16,
        terminal_height: u16,
        payload: SesPayload,
    ) -> Result<Self, RecordingError> {
        Self::open_destinations(
            config,
            params,
            protocol,
            terminal_width,
            terminal_height,
            payload,
            None,
        )
        .map_err(|err| {
            if config.allow_unrecorded {
                err
            } else {
                RecordingError::Unrecordable(format!(
                    "recording is required (recording-allow-unrecorded=false) but no \
                     destination could be opened: {err}"
                ))
            }
        })
    }

    fn open_destinations(
        config: &RecordingConfig,
        params: &HashMap<String, String>,
        protocol: &str,
        terminal_width: u16,
        terminal_height: u16,
        payload: SesPayload,
        prepared: Option<[Option<SinkTarget>; 4]>,
    ) -> Result<Self, RecordingError> {
        // Every destination is opened on this thread — a FIFO's `create` blocks until the
        // gateway's reader arrives, and that rendezvous is what makes the recording live.
        // Only the writes move to the writer thread, below.
        //
        // The endpoint wins when both are somehow present: `from_params` never sets both
        // (config.rs), so a caller that built the config by hand asked for the socket
        // explicitly.
        let [ses_file, asciicast_file, typescript_file, typescript_timing_file] =
            if let Some(mut prepared) = prepared {
                if let Some(addr) = &config.ses_zmq_addr {
                    prepared[0] = Some(open_ses_zmq(addr, config)?);
                }
                prepared
            } else {
                let ses_file = match (&config.ses_zmq_addr, config.get_ses_path(params, protocol)) {
                    (Some(addr), _) => Some(open_ses_zmq(addr, config)?),
                    (None, Some(path)) => {
                        Some(SinkTarget::File(crate::ses::open_ses_file(&path, config)?))
                    }
                    (None, None) => None,
                };

                let asciicast_file = if let Some(path) = config.get_asciicast_path(params, protocol)
                {
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

                    Some(SinkTarget::File(std::fs::File::create(&path)?))
                } else {
                    None
                };

                let (typescript_file, typescript_timing_file) =
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

                        // Companion timing file: the typescript filename with ".timing"
                        // appended, never substituted for an existing extension. guacd builds
                        // it the same way (`"%s.%s"`, src/terminal/typescript.c:133), and the
                        // gateway mkfifos exactly that name — a typescript called
                        // "<stamp>.tys" pairs with "<stamp>.tys.timing". Replacing the
                        // extension instead yields "<stamp>.timing.txt", a file nothing reads,
                        // while the gateway waits forever on a FIFO with no writer.
                        let mut timing_name = path.file_name().unwrap_or_default().to_os_string();
                        timing_name.push(".timing");
                        let timing_path = path.with_file_name(timing_name);
                        let timing_file = std::fs::File::create(&timing_path)?;

                        (
                            Some(SinkTarget::File(file)),
                            Some(SinkTarget::File(timing_file)),
                        )
                    } else {
                        (None, None)
                    };

                [
                    ses_file,
                    asciicast_file,
                    typescript_file,
                    typescript_timing_file,
                ]
            };

        // One writer thread for all of this recorder's destinations, including a `.ses`
        // socket: the `.ses` stream is written through a `BufWriter` by
        // `GuacamoleSesRecorder`, so it needs the same offload seam a file does. Skipped
        // entirely when only the asciicast `zmq_addr` stream is configured, which has its
        // own non-blocking sender.
        let has_ses = ses_file.is_some();
        let has_asciicast = asciicast_file.is_some();
        let has_typescript = typescript_file.is_some();
        let has_timing = typescript_timing_file.is_some();
        let file_writer = if has_ses || has_asciicast || has_typescript {
            Some(RecordingWriter::spawn([
                ses_file,
                asciicast_file,
                typescript_file,
                typescript_timing_file,
            ]))
        } else {
            None
        };

        let ses_recorder = match (&file_writer, has_ses) {
            (Some(writer), true) => Some(GuacamoleSesRecorder::with_sink(
                writer.sink(SinkId::Ses),
                config,
                payload,
            )?),
            _ => None,
        };

        let asciicast_writer = match (&file_writer, has_asciicast) {
            (Some(writer), true) => {
                let mut writer = std::io::BufWriter::new(writer.sink(SinkId::Asciicast));

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
            }
            _ => None,
        };

        let typescript_writer = match (&file_writer, has_typescript) {
            (Some(writer), true) => {
                let mut writer = std::io::BufWriter::new(writer.sink(SinkId::Typescript));

                // Write typescript header — matches guacd format expected by Keeper player
                writeln!(writer, "[BEGIN TYPESCRIPT]")?;
                writer.flush()?;

                Some(writer)
            }
            _ => None,
        };

        let typescript_timing_writer = match (&file_writer, has_timing) {
            (Some(writer), true) => Some(std::io::BufWriter::new(
                writer.sink(SinkId::TypescriptTiming),
            )),
            _ => None,
        };

        #[cfg(feature = "zmq-transport")]
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

        // Symmetric with the enabled path: report the dropped address instead of leaving a
        // session that asked for ZMQ recording quietly without it.
        #[cfg(not(feature = "zmq-transport"))]
        if let Some(ref addr) = config.zmq_addr {
            log::warn!(
                "recording-zmq-addr is set ({addr}) but this build has the zmq-transport \
                 feature disabled, the ZMQ recording stream will not be produced"
            );
        }

        Ok(Self {
            ses_recorder,
            asciicast_writer,
            typescript_writer,
            typescript_timing_writer,
            file_writer,
            #[cfg(feature = "zmq-transport")]
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
            || self.zmq_active()
    }

    /// Whether a ZMQ recording sink is attached.
    ///
    /// Always false when the `zmq-transport` feature is off, so callers do not
    /// need their own `cfg` blocks.
    fn zmq_active(&self) -> bool {
        #[cfg(feature = "zmq-transport")]
        {
            self.zmq_sender.is_some()
        }
        #[cfg(not(feature = "zmq-transport"))]
        {
            false
        }
    }

    /// Reclassify a mid-session write failure according to the session's policy.
    ///
    /// `allow_unrecorded=false` is the operator saying no recording, no session. A write
    /// that fails after the recording started is not an advisory I/O error under that
    /// policy: the destination is closed (`writer_thread.rs:171-181`), the failure is
    /// sticky, and the recording is already incomplete. Handlers treat `Io` as something to
    /// log and carry on, and [`RecordingError::Unrecordable`] as the session's end, so the
    /// policy has to be applied here — the only place that knows it.
    fn classify_write_failure(&self, err: RecordingError) -> RecordingError {
        if self.config.allow_unrecorded || matches!(err, RecordingError::Unrecordable(_)) {
            return err;
        }
        RecordingError::Unrecordable(format!(
            "recording is required (recording-allow-unrecorded=false) but a write failed \
             so the recording is incomplete: {err}"
        ))
    }

    /// Fail now if the writer thread has already given up on a destination.
    ///
    /// Every text writer here buffers (8 KiB `BufWriter`s), so a `record_*` call keeps
    /// returning `Ok` for as long as the buffer takes to fill after the destination died —
    /// and a keystroke is fifteen bytes. Under a strict session that window is time the user
    /// spends working unrecorded, which is the thing `allow_unrecorded=false` forbids, so the
    /// failure slot is consulted on every call rather than waited on.
    fn check_destination_health(&self) -> Result<(), RecordingError> {
        if self.config.allow_unrecorded {
            return Ok(());
        }
        match self.file_writer.as_ref().and_then(|w| w.failure_reason()) {
            Some(reason) => Err(RecordingError::Unrecordable(format!(
                "recording is required (recording-allow-unrecorded=false) but a recording \
                 destination has stopped accepting writes: {reason}"
            ))),
            None => Ok(()),
        }
    }

    /// Record a Guacamole protocol instruction (.ses format)
    pub fn record_instruction(
        &mut self,
        direction: RecordingDirection,
        instruction: &Bytes,
    ) -> Result<(), RecordingError> {
        self.check_destination_health()?;
        let result = match self.ses_recorder {
            Some(ref mut recorder) => recorder.record(direction, instruction),
            None => Ok(()),
        };
        result.map_err(|e| self.classify_write_failure(e))
    }

    /// Record terminal output (asciicast + typescript + ZMQ)
    pub fn record_output(&mut self, data: &[u8]) -> Result<(), RecordingError> {
        self.check_destination_health()?;
        let result = self.record_output_inner(data);
        result.map_err(|e| self.classify_write_failure(e))
    }

    fn record_output_inner(&mut self, data: &[u8]) -> Result<(), RecordingError> {
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
        #[cfg(feature = "zmq-transport")]
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
        self.check_destination_health()?;
        let result = self.record_input_inner(data);
        result.map_err(|e| self.classify_write_failure(e))
    }

    fn record_input_inner(&mut self, data: &[u8]) -> Result<(), RecordingError> {
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
        self.check_destination_health()?;
        let result = self.record_resize_inner(cols, rows);
        result.map_err(|e| self.classify_write_failure(e))
    }

    fn record_resize_inner(&mut self, cols: u16, rows: u16) -> Result<(), RecordingError> {
        self.terminal_width = cols;
        self.terminal_height = rows;

        let elapsed = self.start_time.elapsed().as_secs_f64();

        let resize_line = format!("[{:.6},\"r\",\"{}x{}\"]\n", elapsed, cols, rows);

        if let Some(ref mut writer) = self.asciicast_writer {
            writer.write_all(resize_line.as_bytes())?;
        }

        #[cfg(feature = "zmq-transport")]
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
        let result = self.flush_inner();
        result.map_err(|e| self.classify_write_failure(e))
    }

    fn flush_inner(&mut self) -> Result<(), RecordingError> {
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
    ///
    /// Every sink is dropped before the writer thread is joined — the thread exits on the
    /// queue disconnect, so a surviving sender would hold the join open indefinitely. The
    /// first error is returned, but every writer is still finalized: a failed `.ses` must
    /// not leave the typescript truncated.
    fn finalize_internal(&mut self) -> Result<(), RecordingError> {
        let mut first_error = None;

        // Finalize .ses
        if let Some(recorder) = self.ses_recorder.take() {
            if let Err(e) = recorder.finalize() {
                first_error = Some(e);
            }
        }

        // Finalize asciicast (no footer needed)
        if let Some(mut writer) = self.asciicast_writer.take() {
            if let Err(e) = writer.flush() {
                first_error = first_error.or(Some(e.into()));
            }
        }

        // Finalize typescript — matches guacd format expected by Keeper player
        if let Some(mut writer) = self.typescript_writer.take() {
            let result = writeln!(writer, "[END TYPESCRIPT]").and_then(|()| writer.flush());
            if let Err(e) = result {
                first_error = first_error.or(Some(e.into()));
            }
        }

        // Finalize typescript timing
        if let Some(mut writer) = self.typescript_timing_writer.take() {
            if let Err(e) = writer.flush() {
                first_error = first_error.or(Some(e.into()));
            }
        }

        // All sinks are gone: drain the queue and close the files, so the gateway's
        // readers see EOF on complete recordings rather than mid-instruction.
        if let Some(mut writer) = self.file_writer.take() {
            if let Err(e) = writer.shutdown() {
                first_error = first_error.or(Some(e.into()));
            }
        }

        // Close ZMQ sender: signals end-of-recording to Python.
        #[cfg(feature = "zmq-transport")]
        if let Some(sender) = self.zmq_sender.take() {
            sender.close();
        }

        match first_error {
            Some(e) => Err(self.classify_write_failure(e)),
            None => Ok(()),
        }
    }
}

/// RAII: Ensure recording files are flushed even on early return or panic
impl Drop for MultiFormatRecorder {
    fn drop(&mut self) {
        // Only finalize if not already done (writers still present)
        if self.ses_recorder.is_some()
            || self.asciicast_writer.is_some()
            || self.typescript_writer.is_some()
            || self.file_writer.is_some()
            || self.zmq_active()
        {
            if let Err(e) = self.finalize_internal() {
                // Can't propagate error from Drop, just log it
                log::warn!("Recording finalization failed during drop: {}", e);
            }
        }
    }
}

/// Connect the `.ses` stream to a ZMQ endpoint the gateway has bound.
///
/// Errors rather than degrading: on Windows this is the only `.ses` destination there is,
/// so a build without the transport cannot record at all, and `new_with_payload` turns that
/// into [`RecordingError::Unrecordable`] unless the session allows going unrecorded. The
/// alternative — warn and continue — is the silent-drop behaviour this replaced.
#[cfg(feature = "zmq-transport")]
fn open_ses_zmq(addr: &str, config: &RecordingConfig) -> Result<SinkTarget, RecordingError> {
    Ok(SinkTarget::Zmq(ZmqRecordingSender::connect(
        addr,
        config.allow_unrecorded,
    )?))
}

#[cfg(not(feature = "zmq-transport"))]
fn open_ses_zmq(addr: &str, _config: &RecordingConfig) -> Result<SinkTarget, RecordingError> {
    Err(RecordingError::Zmq(format!(
        "recording-path is a ZMQ endpoint ({addr}) but this build has the zmq-transport \
         feature disabled, so the .ses stream has nowhere to go"
    )))
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
