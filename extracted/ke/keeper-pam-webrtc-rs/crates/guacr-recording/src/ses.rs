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
use crate::helpers::{
    extract_opcode, is_binary_frame, is_binary_output_frame, is_drawing_instruction,
};
use crate::writer_thread::{OffloadSink, RecordingWriter, SinkId, SinkTarget};

/// Which payload a `.ses` carries.
///
/// `.ses` is a container with more than one payload shape, and a player has to pick a
/// renderer before it decodes anything. RDP writes fMP4 into the slot, identified by the
/// `ftyp` box at bytes 4..8. The terminal family writes binary opcode frames interleaved
/// with text instructions, which cannot be told from a guacd recording by sniffing —
/// either may open with an ASCII digit — so it declares itself with a marker instruction.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum SesPayload {
    /// Text Guacamole instructions only, byte-for-byte guacd-shaped. Plays in
    /// `GuacamolePlayer`, `guacenc` and `guaclog` with no marker to skip.
    #[default]
    Guacamole,
    /// Binary `TerminalData` frames plus text instructions, replayed as ANSI.
    Terminal,
}

/// The instruction a terminal `.ses` opens with, at offset 0.
///
/// Args are the payload name and a format version, so the player can evolve without a
/// second sniff. Well-formed Guacamole (`LENGTH.OPCODE,...;`, lengths in codepoints), so
/// `guacenc` and `guaclog` skip it as an unknown opcode rather than failing the parse —
/// both end their dispatch with `/* Ignore any unknown instructions */`
/// (`guacamole-server/src/guacenc/instructions.c:73`, `src/guaclog/instructions.c:57`).
///
/// The opcode is namespaced under `guacr` so upstream Guacamole can never collide with it.
pub const TERMINAL_SES_MARKER: &str = "5.guacr,8.terminal,1.1;";

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

    #[error("ZMQ recording error: {0}")]
    Zmq(String),

    /// The producer can never yield a valid recording — for example an H.264 stream
    /// that never delivered the parameter sets the container header is built from.
    /// Distinct from `Io` because no retry can help: the session itself has to end,
    /// or it runs to completion and uploads an empty file.
    #[error("Recording cannot be produced: {0}")]
    Unrecordable(String),
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
    pub(crate) writer: std::io::BufWriter<OffloadSink>,
    /// Set when this recorder spawned the writer thread itself. `None` when the sink was
    /// handed in by [`crate::MultiFormatRecorder`], which owns one thread for all of its
    /// files and shuts it down itself.
    owned_writer: Option<RecordingWriter>,
    start_time: Instant,
    config: RecordingConfig,
    payload: SesPayload,
    terminal_size: Option<(u16, u16)>,
    last_sync_ms: u64,
    /// Last sync timestamp acknowledged by the client, in Guacamole-encoded form
    /// (e.g. "13.1775238357469"). Written as the second arg of server sync instructions
    /// to match guacd recording format. Defaults to "1.0" (value "0") before any
    /// client ack is received.
    last_client_sync_encoded: String,
}

/// Open the `.ses` destination, honouring the directory-creation and overwrite policy.
///
/// Stays on the calling thread: when the path is a FIFO, `File::create` blocks until the
/// gateway's reader opens the other end, and that rendezvous is what tells the caller the
/// recording is live. Only the writes are offloaded.
pub(crate) fn open_ses_file(
    path: &std::path::Path,
    config: &RecordingConfig,
) -> Result<std::fs::File, RecordingError> {
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

    Ok(std::fs::File::create(&actual_path)?)
}

impl GuacamoleSesRecorder {
    /// Create a new .ses recorder carrying text Guacamole instructions.
    pub fn new(path: &std::path::Path, config: &RecordingConfig) -> Result<Self, RecordingError> {
        Self::new_with_payload(path, config, SesPayload::Guacamole)
    }

    /// Create a new .ses recorder for a given payload shape.
    ///
    /// A [`SesPayload::Terminal`] recording opens with [`TERMINAL_SES_MARKER`] so a player
    /// can route on a fixed prefix.
    pub fn new_with_payload(
        path: &std::path::Path,
        config: &RecordingConfig,
        payload: SesPayload,
    ) -> Result<Self, RecordingError> {
        let file = open_ses_file(path, config)?;
        let writer_thread =
            RecordingWriter::spawn([Some(SinkTarget::File(file)), None, None, None]);
        let sink = writer_thread.sink(SinkId::Ses);

        let mut recorder = Self::with_sink(sink, config, payload)?;
        recorder.owned_writer = Some(writer_thread);
        Ok(recorder)
    }

    /// Create a recorder writing to a sink owned by someone else's writer thread.
    ///
    /// The caller keeps the [`RecordingWriter`] and is responsible for shutting it down;
    /// this recorder only closes its own sink.
    pub(crate) fn with_sink(
        sink: OffloadSink,
        config: &RecordingConfig,
        payload: SesPayload,
    ) -> Result<Self, RecordingError> {
        let mut writer = std::io::BufWriter::new(sink);

        // Must be the first bytes in the file: the player tests a fixed prefix rather
        // than parsing, so anything written ahead of it defeats the check.
        if payload == SesPayload::Terminal {
            writer.write_all(TERMINAL_SES_MARKER.as_bytes())?;
        }

        Ok(Self {
            writer,
            owned_writer: None,
            start_time: Instant::now(),
            config: config.clone(),
            payload,
            terminal_size: None,
            last_sync_ms: 0,
            last_client_sync_encoded: "1.0".to_string(),
        })
    }

    /// Recording-only terminal cell geometry, timed on the same clock as frame syncs.
    pub(crate) fn record_resize(&mut self, cols: u16, rows: u16) -> Result<(), RecordingError> {
        if self.payload != SesPayload::Terminal || self.terminal_size == Some((cols, rows)) {
            return Ok(());
        }
        let time_ms = if self.terminal_size.is_none() {
            0
        } else {
            self.start_time.elapsed().as_millis() as u64
        };
        // All values are ASCII decimal: byte and codepoint lengths are identical.
        write!(
            self.writer,
            "5.guacr,13.terminal-size,{}.{},{}.{},{}.{};",
            cols.checked_ilog10().unwrap_or(0) + 1,
            cols,
            rows.checked_ilog10().unwrap_or(0) + 1,
            rows,
            time_ms.checked_ilog10().unwrap_or(0) + 1,
            time_ms,
        )?;
        self.terminal_size = Some((cols, rows));
        self.maybe_flush()
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
            // Binary opcode frames (the terminal family) carry their type in byte 0, and
            // a lossy UTF-8 view of one has no length prefix for the text classifier to
            // read — so they have to be classified before it, not by it.
            //
            // The frame's timing sync goes with it. Emitting one per excluded frame would
            // publish the cadence of every keystroke and every line of output into a
            // recording whose purpose is to hold no session content.
            if is_binary_frame(instruction) {
                if is_binary_output_frame(instruction) {
                    return Ok(());
                }
            } else {
                // Filter all drawing instructions but keep sync (timing) and size (dimensions)
                let opcode = extract_opcode(&instr_str).to_ascii_lowercase();
                if is_drawing_instruction(&instr_str) && opcode != "sync" && opcode != "size" {
                    return Ok(());
                }
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

        // Client-to-server instructions
        if direction == RecordingDirection::ClientToServer {
            let opcode = extract_opcode(&instr_str);

            // Capture client sync ack — store as a session-relative timestamp
            // so it matches the relative server timestamps written to the file.
            if opcode == "sync" {
                let relative_ts = self.start_time.elapsed().as_millis() as u64;
                let ts_str = relative_ts.to_string();
                self.last_client_sync_encoded = format!("{}.{}", ts_str.len(), ts_str);
                // Client sync instructions are not written to the recording.
                return Ok(());
            }

            // A recording replays as a stream of server instructions, and the two
            // directions do not agree on `size`: the client sends `size,<width>,<height>`
            // while the server sends `size,<layer>,<width>,<height>`. Copied through
            // verbatim, a player reads the client's width as a layer index — sizing an
            // off-screen buffer nothing draws to and leaving layer 0 at 0x0, which renders
            // as a blank screen for the whole recording. The server emits its own `size`,
            // so nothing is lost by dropping this one, same as client `sync`.
            if opcode == "size" {
                return Ok(());
            }

            // For mouse/key, inject a session-relative timestamp so guacenc can
            // replay with correct timing. Must use the same session-relative scale
            // as sync timestamps (self.start_time.elapsed()), NOT Unix epoch time.
            // Mixing absolute epoch timestamps with session-relative sync timestamps
            // causes the player to see billion-millisecond deltas and loop.
            if opcode == "mouse" || opcode == "key" {
                let relative_ts = self.start_time.elapsed().as_millis() as u64;
                let ts_str = relative_ts.to_string();
                // Write original bytes up to (not including) the trailing ';', then
                // append the timestamp argument and close — avoids copying the whole
                // instruction into a new String.
                let raw = instruction.as_ref();
                let body = raw.strip_suffix(b";").unwrap_or(raw);
                self.writer.write_all(body)?;
                let suffix = format!(",{}.{};", ts_str.len(), ts_str);
                self.writer.write_all(suffix.as_bytes())?;
                return self.maybe_flush();
            }
        }

        // Server-to-client sync: rewrite the timestamp to be session-relative.
        if extract_opcode(&instr_str) == "sync" && direction == RecordingDirection::ServerToClient {
            self.write_relative_sync()?;
            return self.maybe_flush();
        }

        // Terminal-family handlers (SSH, telnet, database, mainframe, SFTP) record
        // binary opcode frames rather than text instructions:
        //   [opcode][flags][reserved u16][payload len u32][payload]
        // A text instruction always opens with an ASCII digit — its length prefix — so
        // the first byte tells the two apart.
        //
        // Those handlers emit `sync` only on the 5s keepalive and the 64 KiB
        // flow-control threshold, neither of which is a frame clock, so the recording
        // would carry at most one timestamp every five seconds and a player replaying by
        // sync deltas would dump whole seconds of output at once. Give every frame its
        // own marker. It goes to the recording and never to the client, so it costs one
        // local write and nothing on the wire.
        if direction == RecordingDirection::ServerToClient && is_binary_frame(instruction) {
            self.writer.write_all(instruction)?;
            self.write_relative_sync()?;
            return self.maybe_flush();
        }

        // Write the raw instruction (Guacamole protocol format). Nothing separates
        // instructions: a reader finds the boundaries from the declared element
        // lengths, so any byte added between them is read as part of the next
        // instruction's length prefix.
        self.writer.write_all(instruction)?;

        self.maybe_flush()
    }

    /// Write a `sync` carrying the session-relative time in milliseconds, with the last
    /// client ack as the second argument — the shape guacd's recordings use:
    /// `4.sync,<relative_server_ts>,<relative_client_ts>;`
    ///
    /// The scale has to stay session-relative. Absolute Unix-epoch values make a player
    /// that replays on timestamp deltas see the session as thousands of seconds long.
    fn write_relative_sync(&mut self) -> Result<(), RecordingError> {
        let relative_ts = self.start_time.elapsed().as_millis() as u64;
        let ts_str = relative_ts.to_string();
        let sync = format!(
            "4.sync,{}.{},{};",
            ts_str.len(),
            ts_str,
            self.last_client_sync_encoded
        );
        self.writer.write_all(sync.as_bytes())?;
        Ok(())
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
    /// Waits for the writer thread to drain, so the file is complete and closed when this
    /// returns — the gateway's reader sees EOF and can upload.
    pub fn finalize(mut self) -> Result<(), RecordingError> {
        let flushed = self.flush_internal();

        // Order matters: the sink holds a queue sender, and the writer thread exits when
        // the last sender drops. Joining before releasing it would wait forever.
        self.writer.get_mut().close();
        let drained = match self.owned_writer.take() {
            Some(mut writer_thread) => writer_thread.shutdown().map_err(RecordingError::from),
            None => Ok(()),
        };

        flushed.and(drained).map_err(|err| {
            if self.config.allow_unrecorded || matches!(err, RecordingError::Unrecordable(_)) {
                err
            } else {
                RecordingError::Unrecordable(format!(
                    "recording is required (recording-allow-unrecorded=false) but a .ses write failed, so the recording is incomplete: {err}"
                ))
            }
        })
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
        // Release the queue sender. `RecordingWriter::drop` then drains and joins.
        self.writer.get_mut().close();
    }
}
