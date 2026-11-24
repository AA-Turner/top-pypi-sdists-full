//! Unified logging for SCAI processes.
//!
//! Provides a thread-safe file logger that writes to
//! `~/.snowflake/scai/logs/scai{YYYYMMDD}.log`.
//! All SCAI processes (CLI, deterministic engine, DMVF, testing
//! orchestration, CUR, plugin) share the same log location.
//! Each entry is tagged with `ps={process}` and optionally
//! `pr={projectId}` and `sn={sessionId}` for filtering.
//!
//! The minimum log level defaults to `Info` and can be overridden
//! by setting the `SCAI_LOG_LEVEL` environment variable to one of
//! `debug`, `info`, `warn`, or `error`.
//!
//! The file follows the UTC day: a long-lived logger moves to the new
//! day's file at the first line after midnight UTC. Each day's file stops at
//! [`MAX_LOG_BYTES`]; the one entry that would cross it is cut to fit, a
//! single notice line says the file is full, and later lines that day are
//! dropped. Every `ScaiLogger`, in any process and binding, takes a shared
//! lock file in the log directory around its size check and write, so
//! concurrent writers cannot all spend the same room. Writers that append to
//! the file without `scai-log` (e.g. a Serilog sink) do not take the lock.
//!
//! For consumer-facing integration patterns (C# / Python wrappers,
//! exception logging, tag-vs-context guidance), see
//! [`docs/logging.md`](https://github.com/snowflake-eng/migrations-code-unit-registry/blob/main/docs/logging.md).

use std::borrow::Cow;
use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::str::FromStr;
use std::sync::{Mutex, MutexGuard};

use chrono::Utc;
use fs2::FileExt;
use serde::{Deserialize, Serialize};

#[cfg(test)]
mod tests;

// ── Error ────────────────────────────────────────────────────────────────

/// Errors that can occur during logger initialisation or level parsing.
#[derive(Debug)]
pub enum Error {
    /// A filesystem operation failed.
    Io {
        op: &'static str,
        path: String,
        source: std::io::Error,
    },
    /// An invalid log level string was provided.
    InvalidLogLevel(String),
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Io { op, path, source } => {
                write!(f, "Failed to {op} '{path}': {source}")
            }
            Error::InvalidLogLevel(msg) => f.write_str(msg),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Io { source, .. } => Some(source),
            Error::InvalidLogLevel(_) => None,
        }
    }
}

pub type Result<T> = std::result::Result<T, Error>;

// ── LogLevel ─────────────────────────────────────────────────────────────

/// Log severity levels, ordered by increasing severity.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum LogLevel {
    Debug = 0,
    Info = 1,
    Warn = 2,
    Error = 3,
}

impl fmt::Display for LogLevel {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LogLevel::Debug => write!(f, "DBG"),
            LogLevel::Info => write!(f, "INF"),
            LogLevel::Warn => write!(f, "WRN"),
            LogLevel::Error => write!(f, "ERR"),
        }
    }
}

impl FromStr for LogLevel {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self> {
        match s.to_lowercase().as_str() {
            "debug" => Ok(LogLevel::Debug),
            "info" => Ok(LogLevel::Info),
            "warn" | "warning" => Ok(LogLevel::Warn),
            "error" => Ok(LogLevel::Error),
            _ => Err(Error::InvalidLogLevel(format!(
                "Invalid log level '{s}': expected one of debug, info, warn, error"
            ))),
        }
    }
}

// ── ScaiLogger ───────────────────────────────────────────────────────────

const DEFAULT_MIN_LEVEL: LogLevel = LogLevel::Info;

/// Size cap of one day's log file. Serilog's default `fileSizeLimitBytes`,
/// where the CLI's own sink stops writing to the same file.
pub const MAX_LOG_BYTES: u64 = 1024 * 1024 * 1024;

/// Below this an entry would say nothing useful, so the file counts as full.
const MIN_BODY_BYTES: usize = 128;

/// `… [truncated N bytes]` with N of up to 20 digits, rounded up.
const TRUNCATED_MARK_BYTES: usize = 48;

/// Beside the logs; see the crate docs.
const LOCK_FILE: &str = ".scai-log.lock";

/// Read `SCAI_LOG_LEVEL` env var, falling back to [`DEFAULT_MIN_LEVEL`].
fn resolve_min_level() -> LogLevel {
    std::env::var("SCAI_LOG_LEVEL")
        .ok()
        .and_then(|s| s.parse::<LogLevel>().ok())
        .unwrap_or(DEFAULT_MIN_LEVEL)
}

/// The day the log file is named by.
fn utc_day() -> String {
    Utc::now().format("%Y%m%d").to_string()
}

/// Thread-safe file logger that appends structured log entries to disk.
///
/// All logs are written to `~/.snowflake/scai/logs/scai{YYYYMMDD}.log`.
/// The location is fixed so every SCAI process shares the same log directory.
/// The file follows the UTC day and stops at [`MAX_LOG_BYTES`]; see the crate
/// docs.
///
/// The minimum level defaults to `Info` and can be overridden via the
/// `SCAI_LOG_LEVEL` environment variable (read once at init time).
///
/// Each write is flushed immediately — no explicit flush needed.
/// Individual `log`/`debug`/`info`/`warn`/`error` calls never fail;
/// write errors are silently swallowed to ensure logging cannot crash
/// the calling process.
pub struct ScaiLogger {
    state: Mutex<State>,
    min_level: LogLevel,
    process: String,
    project_id: Option<String>,
    session_id: Option<String>,
    log_dir: PathBuf,
    max_bytes: u64,
    day: fn() -> String,
}

struct State {
    file: File,
    log_path: PathBuf,
    day: String,
    /// The day's file reached the cap; nothing is written until the day turns.
    full: bool,
    /// `None` until it opens; entries are dropped while it cannot be had.
    lock_file: Option<File>,
}

impl ScaiLogger {
    /// Initialize the logger, creating the log directory and file if needed.
    ///
    /// Log path: `~/.snowflake/scai/logs/scai{YYYYMMDD}.log`
    pub fn init(process: &str) -> Result<Self> {
        Self::create(process, None, log_dir())
    }

    /// Initialize the logger with an associated project ID.
    pub fn init_with_project_id(process: &str, project_id: &str) -> Result<Self> {
        Self::create(process, Some(project_id), log_dir())
    }

    /// Constructor that accepts an explicit directory instead of the
    /// default `~/.snowflake/scai/logs/`. Exposed for binding-level
    /// tests that need to redirect output to a temporary directory.
    /// Not re-exported by the managed Python/C#/Node wrappers.
    pub fn init_in_dir(process: &str, log_dir: PathBuf) -> Result<Self> {
        Self::create(process, None, log_dir)
    }

    /// Like [`Self::init_in_dir`] but also sets the project ID tag.
    pub fn init_in_dir_with_project_id(
        process: &str,
        project_id: &str,
        log_dir: PathBuf,
    ) -> Result<Self> {
        Self::create(process, Some(project_id), log_dir)
    }

    /// Attach a session ID to the logger (appears as `sn={id}` in log entries).
    pub fn with_session_id(mut self, session_id: &str) -> Self {
        self.session_id = Some(session_id.to_string());
        self
    }

    fn create(process: &str, project_id: Option<&str>, log_dir: PathBuf) -> Result<Self> {
        Self::create_with(process, project_id, log_dir, MAX_LOG_BYTES, utc_day)
    }

    fn create_with(
        process: &str,
        project_id: Option<&str>,
        log_dir: PathBuf,
        max_bytes: u64,
        day: fn() -> String,
    ) -> Result<Self> {
        fs::create_dir_all(&log_dir).map_err(|source| Error::Io {
            op: "create_dir_all",
            path: log_dir.display().to_string(),
            source,
        })?;
        let today = day();
        let (file, log_path) = open_log_file(&log_dir, &today)?;

        Ok(Self {
            state: Mutex::new(State {
                file,
                log_path,
                day: today,
                full: false,
                lock_file: None,
            }),
            min_level: resolve_min_level(),
            process: process.to_string(),
            project_id: project_id.map(|s| s.to_string()),
            session_id: None,
            log_dir,
            max_bytes,
            day,
        })
    }

    /// Returns `true` if a message at the given level would be logged.
    pub fn is_enabled(&self, level: LogLevel) -> bool {
        level >= self.min_level
    }

    /// Log a message at the given level with optional structured JSON context.
    ///
    /// Messages below the minimum level are dropped, and so is every message
    /// once the day's file is full.
    /// Write errors are silently swallowed.
    pub fn log(&self, level: LogLevel, message: &str, context: Option<&str>) {
        if level < self.min_level {
            return;
        }
        let timestamp = chrono::Local::now().format("%Y-%m-%d %H:%M:%S%.3f %:z");
        let _ = self.write_entry(timestamp, level, message, context);
    }

    pub fn debug(&self, message: &str) {
        self.log(LogLevel::Debug, message, None);
    }

    pub fn info(&self, message: &str) {
        self.log(LogLevel::Info, message, None);
    }

    pub fn warn(&self, message: &str) {
        self.log(LogLevel::Warn, message, None);
    }

    pub fn error(&self, message: &str) {
        self.log(LogLevel::Error, message, None);
    }

    /// Returns the path of the file entries go to today.
    pub fn log_path(&self) -> PathBuf {
        self.lock().log_path.clone()
    }

    fn tag(&self) -> String {
        let mut tag = format!("ps={}", self.process);
        if let Some(pr) = &self.project_id {
            tag.push_str(&format!(" pr={pr}"));
        }
        if let Some(sn) = &self.session_id {
            tag.push_str(&format!(" sn={sn}"));
        }
        tag
    }

    fn lock(&self) -> MutexGuard<'_, State> {
        self.state.lock().unwrap_or_else(|p| p.into_inner())
    }

    fn write_entry(
        &self,
        timestamp: impl fmt::Display,
        level: LogLevel,
        message: &str,
        context: Option<&str>,
    ) -> std::io::Result<()> {
        let mut guard = self.lock();
        let state = &mut *guard;
        let today = (self.day)();
        if today != state.day {
            // A failed reopen keeps the old file; the next entry tries again.
            if let Ok((file, log_path)) = open_log_file(&self.log_dir, &today) {
                state.file = file;
                state.log_path = log_path;
                state.day = today;
                state.full = false;
            }
        }
        if state.full {
            return Ok(());
        }
        if state.lock_file.is_none() {
            state.lock_file = open_lock_file(&self.log_dir);
        }
        // Without the shared lock another writer could spend the same room,
        // so the entry is dropped rather than risk the cap. Released at the end.
        let Some(_shared) = state
            .lock_file
            .as_ref()
            .filter(|f| f.lock_exclusive().is_ok())
            .map(Unlock)
        else {
            return Ok(());
        };

        let tag = self.tag();
        let header = format!("{timestamp} [{level}] {tag}: ");
        let notice = format!(
            "{timestamp} [{}] {tag}: log file reached its cap of {} bytes; ps={} writes no more to it until the next UTC day\n",
            LogLevel::Warn,
            self.max_bytes,
            self.process
        );
        let separator = if context.is_some() { " | ".len() } else { 0 };
        // The open handle is sized, not the path: a renamed or deleted log is
        // still the file written to. An unknown size drops the entry.
        let Ok(size) = state.file.metadata().map(|m| m.len()) else {
            return Ok(());
        };
        // Room is kept for the notice, so the file ends at or under the cap.
        let room = self
            .max_bytes
            .saturating_sub(size)
            .saturating_sub(notice.len() as u64);
        let frame = (header.len() + separator + 1) as u64;
        let body = room.saturating_sub(frame) as usize;
        // Only an entry that would cross the cap is cut, so below it a large
        // response keeps its tail, where the error usually is. The frame alone
        // must fit too, or empty entries would grow a full file.
        let wanted = message.len() + context.map_or(0, str::len);
        if room < frame || (wanted > body && body < MIN_BODY_BYTES) {
            state.full = true;
            if size + notice.len() as u64 <= self.max_bytes {
                state.file.write_all(notice.as_bytes())?;
            }
            return Ok(());
        }
        let (message, context) = fit(message, context, body);
        let mut line = match context {
            Some(ctx) => format!("{header}{message} | {ctx}\n"),
            None => format!("{header}{message}\n"),
        };
        // The entry that crosses the cap closes the file with the notice, so
        // it is there even when nothing else is logged that day.
        if wanted > body {
            state.full = true;
            line.push_str(&notice);
        }
        // One write per entry, so appends from other processes never interleave.
        state.file.write_all(line.as_bytes())
    }
}

/// Cuts `message` and `context` to `body` bytes together, the context getting
/// whatever the message leaves, and at least half when both are long.
fn fit<'a>(
    message: &'a str,
    context: Option<&'a str>,
    body: usize,
) -> (Cow<'a, str>, Option<Cow<'a, str>>) {
    let ctx_len = context.map_or(0, str::len);
    if message.len() + ctx_len <= body {
        return (Cow::Borrowed(message), context.map(Cow::Borrowed));
    }
    let Some(context) = context else {
        return (cut(message, body), None);
    };
    let message_cap = (body / 2).max(body.saturating_sub(ctx_len));
    let message = cut(message, message_cap);
    let context = cut(context, body - message.len());
    (message, Some(context))
}

fn cut(text: &str, max: usize) -> Cow<'_, str> {
    if text.len() <= max {
        return Cow::Borrowed(text);
    }
    let mut end = max.saturating_sub(TRUNCATED_MARK_BYTES);
    while !text.is_char_boundary(end) {
        end -= 1;
    }
    Cow::Owned(format!(
        "{}… [truncated {} bytes]",
        &text[..end],
        text.len() - end
    ))
}

struct Unlock<'a>(&'a File);

impl Drop for Unlock<'_> {
    fn drop(&mut self) {
        let _ = FileExt::unlock(self.0);
    }
}

/// A lock needs only a handle, so a lock file left read-only still works.
fn open_lock_file(dir: &Path) -> Option<File> {
    let path = dir.join(LOCK_FILE);
    OpenOptions::new()
        .create(true)
        .truncate(false)
        .write(true)
        .open(&path)
        .or_else(|_| File::open(&path))
        .ok()
        .filter(|f| f.metadata().is_ok_and(|m| m.is_file()))
}

fn open_log_file(log_dir: &Path, day: &str) -> Result<(File, PathBuf)> {
    let log_path = log_dir.join(format!("scai{day}.log"));
    let file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(&log_path)
        .map_err(|source| Error::Io {
            op: "open",
            path: log_path.display().to_string(),
            source,
        })?;
    Ok((file, log_path))
}

/// The fixed log directory: `~/.snowflake/scai/logs/`
fn log_dir() -> PathBuf {
    let home = std::env::var("HOME")
        .or_else(|_| std::env::var("USERPROFILE"))
        .unwrap_or_else(|_| ".".to_string());
    PathBuf::from(home)
        .join(".snowflake")
        .join("scai")
        .join("logs")
}
