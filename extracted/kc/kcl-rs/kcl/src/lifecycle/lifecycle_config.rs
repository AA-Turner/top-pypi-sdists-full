//! Port of `software.amazon.kinesis.lifecycle.LifecycleConfig`.

use std::sync::Arc;

use crate::lifecycle::{NoOpTaskExecutionListener, TaskExecutionListener};
use crate::retrieval::AggregatorUtil;

/// Number of consecutive `ReadTimeout`s to ignore before logging a warning
/// (Java `DEFAULT_READ_TIMEOUTS_TO_IGNORE`).
pub const DEFAULT_READ_TIMEOUTS_TO_IGNORE: i32 = 0;

/// Used by the KCL to configure the lifecycle subsystem.
///
/// Port of the Lombok `@Data @Accessors(fluent=true)` config bean. Uses field
/// defaults + fluent chainable setters (matching the `@Data`-generated
/// `this`-returning setters). Fields:
///
/// * `log_warning_for_task_after_millis`: `Option<i64>` (default `None` — "no
///   warning", not `0`).
/// * `task_backoff_time_millis`: `i64` (default `500`).
/// * `aggregator_util`: shared [`AggregatorUtil`] (default `new AggregatorUtil()`).
/// * `task_execution_listener`: [`TaskExecutionListener`] (default
///   [`NoOpTaskExecutionListener`]).
/// * `read_timeouts_to_ignore_before_warning`: `i32` (default `0`).
#[derive(Clone)]
pub struct LifecycleConfig {
    log_warning_for_task_after_millis: Option<i64>,
    task_backoff_time_millis: i64,
    aggregator_util: Arc<AggregatorUtil>,
    task_execution_listener: Arc<dyn TaskExecutionListener>,
    read_timeouts_to_ignore_before_warning: i32,
}

impl Default for LifecycleConfig {
    fn default() -> Self {
        Self {
            log_warning_for_task_after_millis: None,
            task_backoff_time_millis: 500,
            aggregator_util: Arc::new(AggregatorUtil),
            task_execution_listener: Arc::new(NoOpTaskExecutionListener),
            read_timeouts_to_ignore_before_warning: DEFAULT_READ_TIMEOUTS_TO_IGNORE,
        }
    }
}

impl LifecycleConfig {
    /// A new config with all defaults.
    pub fn new() -> Self {
        Self::default()
    }

    // ---- fluent getters (Java `@Accessors(fluent = true)`) ----

    /// Warn if a task is held for more than this many millis (`None` = never).
    pub fn log_warning_for_task_after_millis(&self) -> Option<i64> {
        self.log_warning_for_task_after_millis
    }
    /// Backoff time (millis) for KCL tasks on failure.
    pub fn task_backoff_time_millis(&self) -> i64 {
        self.task_backoff_time_millis
    }
    /// The KPL de-aggregation utility.
    pub fn aggregator_util(&self) -> &Arc<AggregatorUtil> {
        &self.aggregator_util
    }
    /// The task-execution listener.
    pub fn task_execution_listener(&self) -> &Arc<dyn TaskExecutionListener> {
        &self.task_execution_listener
    }
    /// Number of consecutive `ReadTimeout`s to ignore before warning.
    pub fn read_timeouts_to_ignore_before_warning(&self) -> i32 {
        self.read_timeouts_to_ignore_before_warning
    }

    // ---- fluent chainable setters (Java `@Data` `this`-returning setters) ----

    /// Set `log_warning_for_task_after_millis`.
    pub fn set_log_warning_for_task_after_millis(mut self, v: Option<i64>) -> Self {
        self.log_warning_for_task_after_millis = v;
        self
    }
    /// Set `task_backoff_time_millis`.
    pub fn set_task_backoff_time_millis(mut self, v: i64) -> Self {
        self.task_backoff_time_millis = v;
        self
    }
    /// Set `aggregator_util`.
    pub fn set_aggregator_util(mut self, v: Arc<AggregatorUtil>) -> Self {
        self.aggregator_util = v;
        self
    }
    /// Set `task_execution_listener`.
    pub fn set_task_execution_listener(mut self, v: Arc<dyn TaskExecutionListener>) -> Self {
        self.task_execution_listener = v;
        self
    }
    /// Set `read_timeouts_to_ignore_before_warning`.
    pub fn set_read_timeouts_to_ignore_before_warning(mut self, v: i32) -> Self {
        self.read_timeouts_to_ignore_before_warning = v;
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn defaults_match_java() {
        let config = LifecycleConfig::new();
        assert_eq!(config.log_warning_for_task_after_millis(), None);
        assert_eq!(config.task_backoff_time_millis(), 500);
        assert_eq!(config.read_timeouts_to_ignore_before_warning(), 0);
    }

    #[test]
    fn fluent_setters_chain() {
        let config = LifecycleConfig::new()
            .set_task_backoff_time_millis(1000)
            .set_read_timeouts_to_ignore_before_warning(3)
            .set_log_warning_for_task_after_millis(Some(60_000));
        assert_eq!(config.task_backoff_time_millis(), 1000);
        assert_eq!(config.read_timeouts_to_ignore_before_warning(), 3);
        assert_eq!(config.log_warning_for_task_after_millis(), Some(60_000));
    }
}
