const TICK_INTERVAL_MS: u64 = 1000;
const MIN_FLUSH_INTERVAL_MS: u64 = 1000;
const MAX_LOG_EVENT_RETRIES: u8 = 5;
const MAX_FLUSH_INTERVAL_MS: u64 = 60_000;

pub struct EventLoggerConstants;

impl EventLoggerConstants {
    pub fn tick_interval_ms() -> u64 {
        #[cfg(feature = "testing")]
        if let Ok(value) = std::env::var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS") {
            return value.parse().unwrap_or(TICK_INTERVAL_MS);
        }

        TICK_INTERVAL_MS
    }

    pub fn min_flush_interval_ms() -> u64 {
        #[cfg(feature = "testing")]
        if let Ok(value) = std::env::var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS") {
            return value.parse().unwrap_or(MIN_FLUSH_INTERVAL_MS);
        }

        MIN_FLUSH_INTERVAL_MS
    }

    pub fn max_flush_interval_ms() -> u64 {
        #[cfg(feature = "testing")]
        if let Ok(value) = std::env::var("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS") {
            return value.parse().unwrap_or(MAX_FLUSH_INTERVAL_MS);
        }

        MAX_FLUSH_INTERVAL_MS
    }

    pub fn max_log_event_retries() -> u8 {
        #[cfg(feature = "testing")]
        if let Ok(value) = std::env::var("STATSIG_TEST_OVERRIDE_MAX_LOG_EVENT_RETRIES") {
            return value.parse().unwrap_or(MAX_LOG_EVENT_RETRIES);
        }

        MAX_LOG_EVENT_RETRIES
    }
}
