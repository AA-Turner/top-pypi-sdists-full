use log::{Level, Metadata, Record};
use pyo3::exceptions::PyRuntimeError;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::{MutexExt, PyOnceLock};
use pyo3::types::PyFunction;
use std::sync::{Mutex, OnceLock};
use tokio::sync::mpsc::{Receiver, Sender, channel};

struct LogEntry {
    level: Level,
    target: String,
    message: String,
}

struct Channel {
    sender: Sender<LogEntry>,
    receiver: Mutex<Receiver<LogEntry>>,
}

const CHANNEL_BUFFER_SIZE: usize = 10000;
static CHANNEL: OnceLock<Channel> = OnceLock::new();

struct GlobalLogger;
impl log::Log for GlobalLogger {
    fn enabled(&self, _metadata: &Metadata) -> bool {
        true
    }

    fn log(&self, record: &Record) {
        let Some(channel) = CHANNEL.get() else {
            return; // Logging not initialized yet
        };

        let entry = LogEntry {
            level: record.level(),
            target: record.target().to_string(),
            message: format!("{}", record.args()),
        };
        let _ = channel.sender.try_send(entry);
    }

    fn flush(&self) {}
}

static LOGGER: GlobalLogger = GlobalLogger;

fn py_log(py: Python, entry: LogEntry) -> PyResult<()> {
    static PY_LOGGER: PyOnceLock<Py<PyFunction>> = PyOnceLock::new();
    let logger = PY_LOGGER.import(py, "logging", "getLogger")?;

    let py_level = match entry.level {
        Level::Error => 40, // Corresponds to logging.ERROR, etc.
        Level::Warn => 30,
        Level::Info => 20,
        Level::Debug | Level::Trace => 10,
    };

    logger
        .call1((entry.target,))?
        .call_method1(intern!(py, "log"), (py_level, entry.message))?;
    Ok(())
}

fn pop_entries(py: Option<Python>, count: Option<usize>) -> Option<Vec<LogEntry>> {
    let Some(channel) = CHANNEL.get() else {
        return None; // Logging not initialized yet
    };

    let receiver_lock = if let Some(py) = py {
        channel.receiver.lock_py_attached(py).ok()
    } else {
        channel.receiver.lock().ok()
    };
    let Some(mut receiver) = receiver_lock else {
        return None; // Just skip on poisoned lock
    };

    let mut entries = Vec::with_capacity(receiver.len().min(count.unwrap_or(usize::MAX)));
    while let Ok(entry) = receiver.try_recv() {
        entries.push(entry);
        if let Some(max_count) = count
            && entries.len() >= max_count
        {
            break;
        }
    }
    if entries.is_empty() { None } else { Some(entries) }
}

pub fn init_verbose_logging() -> PyResult<()> {
    if CHANNEL.get().is_some() {
        return Ok(()); // Already initialized (fast path without init)
    }
    let (tx, rx) = channel(CHANNEL_BUFFER_SIZE);
    let channel = Channel {
        sender: tx,
        receiver: Mutex::new(rx),
    };
    if CHANNEL.set(channel).is_err() {
        return Ok(()); // Already initialized
    }

    log::set_logger(&LOGGER).map_err(|e| PyRuntimeError::new_err(e.to_string()))?;
    log::set_max_level(log::LevelFilter::Trace);
    Ok(())
}

pub fn flush_logs_no_gil() -> PyResult<()> {
    // Process in batches to avoid holding GIL too long
    while let Some(entries) = pop_entries(None, Some(1000)) {
        Python::attach(|py| entries.into_iter().try_for_each(|log| py_log(py, log)))?;
    }
    Ok(())
}

#[pyfunction]
pub fn flush_logs(py: Python) -> PyResult<()> {
    if let Some(entries) = pop_entries(Some(py), None) {
        entries.into_iter().try_for_each(|log| py_log(py, log))?;
    }
    Ok(())
}
