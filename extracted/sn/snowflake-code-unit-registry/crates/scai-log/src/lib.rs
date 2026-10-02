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
//! For consumer-facing integration patterns (C# / Python wrappers,
//! exception logging, tag-vs-context guidance), see
//! [`docs/logging.md`](https://github.com/snowflake-eng/migrations-code-unit-registry/blob/main/docs/logging.md).

use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::str::FromStr;
use std::sync::Mutex;

use chrono::Utc;
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

/// Read `SCAI_LOG_LEVEL` env var, falling back to [`DEFAULT_MIN_LEVEL`].
fn resolve_min_level() -> LogLevel {
    std::env::var("SCAI_LOG_LEVEL")
        .ok()
        .and_then(|s| s.parse::<LogLevel>().ok())
        .unwrap_or(DEFAULT_MIN_LEVEL)
}

/// Thread-safe file logger that appends structured log entries to disk.
///
/// All logs are written to `~/.snowflake/scai/logs/scai{YYYYMMDD}.log`.
/// The location is fixed so every SCAI process shares the same log directory.
///
/// The minimum level defaults to `Info` and can be overridden via the
/// `SCAI_LOG_LEVEL` environment variable (read once at init time).
///
/// Each write is flushed immediately — no explicit flush needed.
/// Individual `log`/`debug`/`info`/`warn`/`error` calls never fail;
/// write errors are silently swallowed to ensure logging cannot crash
/// the calling process.
pub struct ScaiLogger {
    writer: Mutex<File>,
    min_level: LogLevel,
    process: String,
    project_id: Option<String>,
    session_id: Option<String>,
    log_path: PathBuf,
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
        fs::create_dir_all(&log_dir).map_err(|source| Error::Io {
            op: "create_dir_all",
            path: log_dir.display().to_string(),
            source,
        })?;

        let date = Utc::now().format("%Y%m%d");
        let log_path = log_dir.join(format!("scai{date}.log"));

        let file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&log_path)
            .map_err(|source| Error::Io {
                op: "open",
                path: log_path.display().to_string(),
                source,
            })?;

        Ok(Self {
            writer: Mutex::new(file),
            min_level: resolve_min_level(),
            process: process.to_string(),
            project_id: project_id.map(|s| s.to_string()),
            session_id: None,
            log_path,
        })
    }

    /// Returns `true` if a message at the given level would be logged.
    pub fn is_enabled(&self, level: LogLevel) -> bool {
        level >= self.min_level
    }

    /// Log a message at the given level with optional structured JSON context.
    ///
    /// Messages below the minimum level are dropped.
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

    /// Returns the path of the current log file.
    pub fn log_path(&self) -> &Path {
        &self.log_path
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

    fn write_entry(
        &self,
        timestamp: impl fmt::Display,
        level: LogLevel,
        message: &str,
        context: Option<&str>,
    ) -> std::io::Result<()> {
        let mut guard = self
            .writer
            .lock()
            .map_err(|_| std::io::Error::other("lock poisoned"))?;
        let tag = self.tag();
        match context {
            Some(ctx) => writeln!(guard, "{timestamp} [{level}] {tag}: {message} | {ctx}"),
            None => writeln!(guard, "{timestamp} [{level}] {tag}: {message}"),
        }
    }
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
