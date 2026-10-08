use log::{Level, debug, error, info, warn};
use parking_lot::RwLock;
use std::collections::VecDeque;
use std::sync::Arc;
use std::time::Duration;

use crate::logging_utils::sanitize_secret_key;
const MAX_CHARS: usize = 400;
const TRUNCATED_SUFFIX: &str = "...[TRUNCATED]";

const DEFAULT_LOG_LEVEL: LogLevel = LogLevel::Warn;

lazy_static::lazy_static! {
    static ref LOGGER_STATE: RwLock<LoggerState> = RwLock::new(LoggerState {
        level: DEFAULT_LOG_LEVEL,
        initialized: false,
        provider: None,
        active_calls: 0,
        lifecycle_running: false,
        shutting_down: false,
        pending: VecDeque::new(),
    });
}

struct LoggerState {
    level: LogLevel,
    initialized: bool,
    provider: Option<Arc<dyn OutputLogProvider>>,
    active_calls: usize,
    lifecycle_running: bool,
    shutting_down: bool,
    pending: VecDeque<Lifecycle>,
}

enum Lifecycle {
    Initialize(LogLevel, Option<Arc<dyn OutputLogProvider>>),
    Shutdown,
}

impl LoggerState {
    fn begin_call(&mut self) -> Option<ProviderCall> {
        if self.lifecycle_running || !self.pending.is_empty() {
            return None;
        }
        let provider = self.provider.clone()?;
        self.active_calls += 1;
        Some(ProviderCall(provider))
    }
}

struct ProviderCall(Arc<dyn OutputLogProvider>);

impl Drop for ProviderCall {
    fn drop(&mut self) {
        LOGGER_STATE.write().active_calls -= 1;
        run_pending_lifecycle();
    }
}

struct LifecycleCall;

impl Drop for LifecycleCall {
    fn drop(&mut self) {
        let mut state = LOGGER_STATE.write();
        state.lifecycle_running = false;
        state.shutting_down = false;
    }
}

// Preserve process-wide lifecycle ordering, even when bindings reuse or wrap
// the same provider. Only bookkeeping is locked: callbacks and provider releases
// can reenter the logger and must run outside LOGGER_STATE.
fn run_pending_lifecycle() {
    loop {
        let (action, selected, previous) = {
            let mut state = LOGGER_STATE.write();
            if state.active_calls != 0 || state.lifecycle_running {
                return;
            }
            let Some(action) = state.pending.pop_front() else {
                return;
            };
            state.lifecycle_running = true;
            state.shutting_down = matches!(action, Lifecycle::Shutdown);
            let previous = match &action {
                Lifecycle::Initialize(level, provider) => {
                    state.level = level.clone();
                    provider
                        .as_ref()
                        .and_then(|p| state.provider.replace(p.clone()))
                }
                Lifecycle::Shutdown => None,
            };
            (action, state.provider.clone(), previous)
        };
        let call = LifecycleCall;
        drop(previous);
        match action {
            Lifecycle::Initialize(_, Some(provider)) => provider.initialize(),
            Lifecycle::Initialize(level, None) => {
                if let Some(level) = level.to_third_party_level() {
                    if simple_logger::init_with_level(level).is_err() {
                        log::set_max_level(level.to_level_filter());
                    }
                }
            }
            Lifecycle::Shutdown => {
                if let Some(provider) = selected {
                    provider.shutdown();
                }
            }
        }
        drop(call);
    }
}

#[derive(Clone, Debug)]
pub enum LogLevel {
    None,
    Debug,
    Info,
    Warn,
    Error,
}

impl From<&str> for LogLevel {
    fn from(level: &str) -> Self {
        match level.to_lowercase().as_str() {
            "debug" => LogLevel::Debug,
            "info" => LogLevel::Info,
            "warn" => LogLevel::Warn,
            "error" => LogLevel::Error,
            "none" => LogLevel::None,
            _ => DEFAULT_LOG_LEVEL,
        }
    }
}

impl From<u32> for LogLevel {
    fn from(level: u32) -> Self {
        match level {
            0 => LogLevel::None,
            1 => LogLevel::Error,
            2 => LogLevel::Warn,
            3 => LogLevel::Info,
            4 => LogLevel::Debug,
            _ => DEFAULT_LOG_LEVEL,
        }
    }
}

impl LogLevel {
    fn to_third_party_level(&self) -> Option<Level> {
        match self {
            LogLevel::Debug => Some(Level::Debug),
            LogLevel::Info => Some(Level::Info),
            LogLevel::Warn => Some(Level::Warn),
            LogLevel::Error => Some(Level::Error),
            LogLevel::None => None,
        }
    }

    fn to_number(&self) -> u32 {
        match self {
            LogLevel::Debug => 4,
            LogLevel::Info => 3,
            LogLevel::Warn => 2,
            LogLevel::Error => 1,
            LogLevel::None => 0,
        }
    }
}

pub trait OutputLogProvider: Send + Sync {
    fn initialize(&self);
    fn debug(&self, tag: &str, msg: String);
    fn info(&self, tag: &str, msg: String);
    fn warn(&self, tag: &str, msg: String);
    fn error(&self, tag: &str, msg: String);
    fn shutdown(&self);
}

/// Queue initialization after earlier callbacks and shutdowns. Reentrant callers
/// must not wait for the callback they are currently executing.
pub fn initialize_output_logger(
    level: &Option<LogLevel>,
    provider: Option<Arc<dyn OutputLogProvider>>,
) {
    if crate::output_policy::OutputPolicy::current().is_silent() {
        return;
    }
    let mut state = match LOGGER_STATE.try_write_for(Duration::from_secs(5)) {
        Some(state) => state,
        None => {
            eprintln!(
                "[Statsig] Failed to acquire write lock for initialize_output_logger: Failed to lock LOGGER_STATE"
            );
            return;
        }
    };
    if state.initialized {
        return;
    }
    state.initialized = true;
    let level = level.as_ref().unwrap_or(&DEFAULT_LOG_LEVEL).clone();
    state
        .pending
        .push_back(Lifecycle::Initialize(level, provider));
    drop(state);
    run_pending_lifecycle();
}

/// Defer provider shutdown until active callbacks finish, including when called
/// from a callback. Keep the legacy behavior of retaining the selected provider
/// for later messages until another initialization replaces it.
pub fn shutdown_output_logger() {
    if crate::output_policy::OutputPolicy::current().is_silent() {
        return;
    }
    let mut state = match LOGGER_STATE.try_write_for(Duration::from_secs(5)) {
        Some(state) => state,
        None => {
            eprintln!(
                "[Statsig] Failed to acquire write lock for shutdown_output_logger: Failed to lock LOGGER_STATE"
            );
            return;
        }
    };

    // Coalesce adjacent shutdowns, including shutdown reentered by the provider.
    // A queued initialization is a boundary: its later shutdown must stay later.
    if matches!(state.pending.back(), Some(Lifecycle::Shutdown))
        || (state.shutting_down && state.pending.is_empty())
    {
        return;
    }
    state.initialized = false;
    state.pending.push_back(Lifecycle::Shutdown);
    drop(state);
    run_pending_lifecycle();
}

pub fn log_message(tag: &str, level: LogLevel, msg: String) {
    if crate::output_policy::OutputPolicy::current().is_silent() {
        return;
    }
    let truncated_msg = if msg.chars().count() > MAX_CHARS {
        let visible_chars = MAX_CHARS.saturating_sub(TRUNCATED_SUFFIX.len());
        format!(
            "{}{}",
            msg.chars().take(visible_chars).collect::<String>(),
            TRUNCATED_SUFFIX
        )
    } else {
        msg
    };

    let sanitized_msg = sanitize_secret_key(&truncated_msg);

    let provider = if let Some(mut state) = LOGGER_STATE.try_write_for(Duration::from_secs(5)) {
        state.begin_call()
    } else {
        eprintln!("[Statsig] Failed to acquire write lock for logger: Failed to lock LOGGER_STATE");
        None
    };
    if let Some(call) = provider {
        let provider = &call.0;
        match level {
            LogLevel::Debug => provider.debug(tag, sanitized_msg),
            LogLevel::Info => provider.info(tag, sanitized_msg),
            LogLevel::Warn => provider.warn(tag, sanitized_msg),
            LogLevel::Error => provider.error(tag, sanitized_msg),
            _ => {}
        }
        return;
    }

    if let Some(level) = level.to_third_party_level() {
        let mut target = String::from("Statsig::");
        target += tag;

        match level {
            Level::Debug => debug!(target: target.as_str(), "{}", sanitized_msg),
            Level::Info => info!(target: target.as_str(), "{}", sanitized_msg),
            Level::Warn => warn!(target: target.as_str(), "{}", sanitized_msg),
            Level::Error => error!(target: target.as_str(), "{}", sanitized_msg),
            _ => {}
        };
    }
}

pub fn has_valid_log_level(level: &LogLevel) -> bool {
    if crate::output_policy::OutputPolicy::current().is_silent() {
        return false;
    }
    let state = match LOGGER_STATE.try_read_for(Duration::from_secs(5)) {
        Some(state) => state,
        None => {
            eprintln!(
                "[Statsig] Failed to acquire read lock for logger: Failed to lock LOGGER_STATE"
            );
            return false;
        }
    };
    let current_level = &state.level;
    level.to_number() <= current_level.to_number()
}

#[doc(hidden)]
pub fn is_diagnostic_output_suppressed() -> bool {
    crate::output_policy::OutputPolicy::current().is_silent()
}

#[macro_export]
macro_rules! log_d {
  ($tag:expr, $($arg:tt)*) => {
        {
            let level = $crate::output_logger::LogLevel::Debug;
            if $crate::output_logger::has_valid_log_level(&level) {
                $crate::output_logger::log_message($tag, level, format!($($arg)*));
            }
        }
    }
}

#[macro_export]
macro_rules! log_i {
  ($tag:expr, $($arg:tt)*) => {
        {
            let level = $crate::output_logger::LogLevel::Info;
            if $crate::output_logger::has_valid_log_level(&level) {
                $crate::output_logger::log_message($tag, level, format!($($arg)*));
            }
        }
    }
}

#[macro_export]
macro_rules! log_w {
  ($tag:expr, $($arg:tt)*) => {
        {
            let level = $crate::output_logger::LogLevel::Warn;
            if $crate::output_logger::has_valid_log_level(&level) {
                $crate::output_logger::log_message($tag, level, format!($($arg)*));
            }
        }
    }
}

#[macro_export]
macro_rules! log_e {
  ($tag:expr, $($arg:tt)*) => {
        {
            let level = $crate::output_logger::LogLevel::Error;
            if $crate::output_logger::has_valid_log_level(&level) {
                $crate::output_logger::log_message($tag, level, format!($($arg)*));
            }
        }
    }
}

#[macro_export]
macro_rules! log_error_to_statsig_and_console {
    ($ops_stats:expr, $tag:expr, $err:expr) => {
        if !$crate::output_logger::is_diagnostic_output_suppressed() {
            let event = ErrorBoundaryEvent {
                bypass_dedupe: false,
                exception: $err.name().to_string(),
                info: serde_json::to_string(&$err).unwrap_or_default(),
                tag: $tag.to_string(),
                extra: None,
                dedupe_key: None,
            };
            $ops_stats.log_error(event);

            $crate::output_logger::log_message(
                &$tag,
                $crate::output_logger::LogLevel::Error,
                $err.to_string(),
            );
        }
    };
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn test_sanitize_url_for_logging() {
        let test_cases = HashMap::from([
            (
                "https://statsigcdn.openai.com/v2/download_config_specs/secret-jadkfjalkjnsdlvcnjsdfaf.json",
                "https://statsigcdn.openai.com/v2/download_config_specs/secret-jadkf*****.json",
            ),
            (
                "https://statsigcdn.openai.com/v1/log_event/",
                "https://statsigcdn.openai.com/v1/log_event/",
            ),
            (
                "https://statsigcdn.openai.com/v2/download_config_specs/secret-jadkfjalkjnsdlvcnjsdfaf.json?sinceTime=1",
                "https://statsigcdn.openai.com/v2/download_config_specs/secret-jadkf*****.json?sinceTime=1",
            ),
        ]);
        for (before, expected) in test_cases {
            let sanitized = sanitize_secret_key(before);
            assert!(sanitized == expected);
        }
    }

    #[test]
    fn test_multiple_secrets() {
        let input = "Multiple secrets: secret-key1 and secret-key2";
        let sanitized = sanitize_secret_key(input);
        assert_eq!(
            sanitized,
            "Multiple secrets: secret-key1***** and secret-key2*****"
        );
    }

    #[test]
    fn test_short_secret() {
        let input = "Short secret: secret-a";
        let sanitized = sanitize_secret_key(input);
        assert_eq!(sanitized, "Short secret: secret-a*****");
    }
}
