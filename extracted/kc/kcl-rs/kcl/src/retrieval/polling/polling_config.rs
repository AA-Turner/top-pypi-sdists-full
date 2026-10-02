//! Port of `software.amazon.kinesis.retrieval.polling.PollingConfig`.

use std::sync::{Arc, Mutex};
use std::time::Duration;

use crate::retrieval::polling::simple_records_fetcher_factory::SimpleRecordsFetcherFactory;
use crate::retrieval::polling::sleep_time_controller::{
    KinesisSleepTimeController, SleepTimeController,
};
use crate::retrieval::polling::synchronous_blocking_retrieval_factory::SynchronousBlockingRetrievalFactory;
use crate::retrieval::records_fetcher_factory::RecordsFetcherFactory;
use crate::retrieval::retrieval_factory::RetrievalFactory;
use crate::retrieval::retrieval_specific_config::RetrievalSpecificConfig;

/// Default `GetRecords` request timeout (Java `DEFAULT_REQUEST_TIMEOUT`, 30s).
pub const DEFAULT_REQUEST_TIMEOUT: Duration = Duration::from_secs(30);
/// Default max records per `GetRecords` call (Java `DEFAULT_MAX_RECORDS`, 10000).
pub const DEFAULT_MAX_RECORDS: i32 = 10_000;
/// Hard cap on `maxPendingProcessRecordsInput` (Java visible-for-testing limit, 5).
pub const DEFAULT_MAX_PENDING_PROCESS_RECORDS_INPUT_LIMIT: i32 = 5;
/// Default `maxPendingProcessRecordsInput` (Java default, 4).
pub const DEFAULT_MAX_PENDING_PROCESS_RECORDS_INPUT: i32 = 4;
/// Minimum idle time between reads (Java `MIN_IDLE_MILLIS_BETWEEN_READS`, 200ms).
pub const MIN_IDLE_MILLIS_BETWEEN_READS: i64 = 200;
/// Default reduced-TPS threshold (Java default, 0 = disabled).
pub const DEFAULT_MILLIS_BEHIND_LATEST_THRESHOLD_FOR_REDUCED_TPS: i64 = 0;

/// User-facing configuration for classic polling-based (`GetRecords`) retrieval.
///
/// Port of the Java `@Accessors(fluent=true) @Getter @Setter` class implementing
/// [`RetrievalSpecificConfig`]. Fluent setters return `Self` (chainable, matching
/// Java's `this`-return for the validated setters); validation-at-set-time is
/// preserved (`maxRecords`/`maxPendingProcessRecordsInput` panic on overflow,
/// `idleTimeBetweenReadsInMillis` clamps to the 200ms floor + flips
/// `usePollingConfigIdleTimeValue`).
pub struct PollingConfig {
    kinesis_client: aws_sdk_kinesis::Client,
    stream_name: Option<String>,
    use_polling_config_idle_time_value: bool,
    millis_behind_latest_threshold_for_reduced_tps: i64,
    max_records: i32,
    idle_time_between_reads_in_millis: i64,
    records_fetcher_factory: Mutex<Box<dyn RecordsFetcherFactory>>,
    sleep_time_controller: Arc<dyn SleepTimeController>,
    max_pending_process_records_input: i32,
    kinesis_request_timeout: Duration,
}

impl PollingConfig {
    /// Construct from a Kinesis client (Java `PollingConfig(KinesisAsyncClient)`).
    pub fn new(kinesis_client: aws_sdk_kinesis::Client) -> Self {
        Self {
            kinesis_client,
            stream_name: None,
            use_polling_config_idle_time_value: false,
            millis_behind_latest_threshold_for_reduced_tps:
                DEFAULT_MILLIS_BEHIND_LATEST_THRESHOLD_FOR_REDUCED_TPS,
            max_records: DEFAULT_MAX_RECORDS,
            idle_time_between_reads_in_millis: 1500,
            records_fetcher_factory: Mutex::new(Box::new(SimpleRecordsFetcherFactory::new())),
            sleep_time_controller: Arc::new(KinesisSleepTimeController),
            max_pending_process_records_input: DEFAULT_MAX_PENDING_PROCESS_RECORDS_INPUT,
            kinesis_request_timeout: DEFAULT_REQUEST_TIMEOUT,
        }
    }

    /// Construct from a stream name + client (Java `PollingConfig(String, KinesisAsyncClient)`).
    pub fn from_stream_name(
        stream_name: impl Into<String>,
        kinesis_client: aws_sdk_kinesis::Client,
    ) -> Self {
        let mut cfg = Self::new(kinesis_client);
        cfg.stream_name = Some(stream_name.into());
        cfg
    }

    /// The stream name, if set.
    pub fn stream_name(&self) -> Option<&str> {
        self.stream_name.as_deref()
    }

    /// Set the stream name (Lombok fluent setter).
    pub fn set_stream_name(mut self, stream_name: impl Into<String>) -> Self {
        self.stream_name = Some(stream_name.into());
        self
    }

    /// The max records per call (default 10000).
    pub fn max_records(&self) -> i32 {
        self.max_records
    }

    /// Set the max records per call. Panics (Java `IllegalArgumentException`) if
    /// above [`DEFAULT_MAX_RECORDS`].
    pub fn set_max_records(mut self, max_records: i32) -> Self {
        if max_records > DEFAULT_MAX_RECORDS {
            panic!(
                "maxRecords must be less than or equal to {} but current value is {}",
                DEFAULT_MAX_RECORDS, max_records
            );
        }
        self.max_records = max_records;
        self
    }

    /// The idle time between reads (millis).
    pub fn idle_time_between_reads_in_millis(&self) -> i64 {
        self.idle_time_between_reads_in_millis
    }

    /// Set the idle time between reads. Clamps to the [`MIN_IDLE_MILLIS_BETWEEN_READS`]
    /// floor (with a warning) and flips `usePollingConfigIdleTimeValue`.
    pub fn set_idle_time_between_reads_in_millis(mut self, mut idle: i64) -> Self {
        if idle < MIN_IDLE_MILLIS_BETWEEN_READS {
            tracing::warn!(
                "idleTimeBetweenReadsInMillis must be >= {} but was {}. Defaulting to minimum.",
                MIN_IDLE_MILLIS_BETWEEN_READS,
                idle
            );
            idle = MIN_IDLE_MILLIS_BETWEEN_READS;
        }
        self.use_polling_config_idle_time_value = true;
        self.idle_time_between_reads_in_millis = idle;
        self
    }

    /// The max pending process-records inputs (default 4).
    pub fn max_pending_process_records_input(&self) -> i32 {
        self.max_pending_process_records_input
    }

    /// Set the max pending process-records inputs. Panics (Java
    /// `IllegalArgumentException`) if above [`DEFAULT_MAX_PENDING_PROCESS_RECORDS_INPUT_LIMIT`].
    pub fn set_max_pending_process_records_input(mut self, value: i32) -> Self {
        if value > DEFAULT_MAX_PENDING_PROCESS_RECORDS_INPUT_LIMIT {
            panic!(
                "maxPendingProcessRecordsInput must be less than or equal to {} but current value is {}",
                DEFAULT_MAX_PENDING_PROCESS_RECORDS_INPUT_LIMIT, value
            );
        }
        self.max_pending_process_records_input = value;
        self
    }

    /// The reduced-TPS threshold.
    pub fn millis_behind_latest_threshold_for_reduced_tps(&self) -> i64 {
        self.millis_behind_latest_threshold_for_reduced_tps
    }

    /// Set the reduced-TPS threshold.
    pub fn set_millis_behind_latest_threshold_for_reduced_tps(mut self, value: i64) -> Self {
        self.millis_behind_latest_threshold_for_reduced_tps = value;
        self
    }

    /// The Kinesis request timeout (default 30s).
    pub fn kinesis_request_timeout(&self) -> Duration {
        self.kinesis_request_timeout
    }

    /// Set the Kinesis request timeout.
    pub fn set_kinesis_request_timeout(mut self, value: Duration) -> Self {
        self.kinesis_request_timeout = value;
        self
    }

    /// The Kinesis client.
    pub fn kinesis_client(&self) -> &aws_sdk_kinesis::Client {
        &self.kinesis_client
    }
}

impl RetrievalSpecificConfig for PollingConfig {
    fn retrieval_factory(&self) -> Box<dyn RetrievalFactory> {
        // Mutate the shared records-fetcher factory with the polling config values
        // (Java re-applies these every call), then snapshot it as an Arc for the
        // retrieval factory.
        let fetcher_factory: Arc<dyn RecordsFetcherFactory> = {
            let mut ff = self.records_fetcher_factory.lock().unwrap();
            if self.use_polling_config_idle_time_value {
                ff.set_idle_millis_between_calls(self.idle_time_between_reads_in_millis);
            }
            ff.set_max_pending_process_records_input(self.max_pending_process_records_input);
            ff.set_millis_behind_latest_threshold_for_reduced_tps(
                self.millis_behind_latest_threshold_for_reduced_tps,
            );
            // Snapshot the configured factory. SimpleRecordsFetcherFactory holds
            // only plain config; rebuild a fresh one carrying the same values so
            // the returned Arc is independent of the mutex-guarded original.
            let snapshot = SimpleRecordsFetcherFactory::from_values(
                ff.max_pending_process_records_input(),
                ff.max_byte_size(),
                ff.max_records_count(),
                ff.idle_millis_between_calls(),
                ff.millis_behind_latest_threshold_for_reduced_tps(),
                ff.data_fetching_strategy(),
            );
            Arc::new(snapshot)
        };

        Box::new(SynchronousBlockingRetrievalFactory::new(
            self.stream_name.clone(),
            self.kinesis_client.clone(),
            fetcher_factory,
            self.max_records,
            self.kinesis_request_timeout,
            None,
            Arc::clone(&self.sleep_time_controller),
        ))
    }

    fn validate_state(&self, is_multi_stream: bool) {
        if is_multi_stream && self.stream_name.is_some() {
            panic!("PollingConfig must not have streamName configured in multi-stream mode");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn client() -> aws_sdk_kinesis::Client {
        aws_sdk_kinesis::Client::from_conf(
            aws_sdk_kinesis::Config::builder()
                .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
                .region(aws_sdk_kinesis::config::Region::new("us-east-1"))
                .build(),
        )
    }

    // Port of PollingConfigTest.testValidState.
    #[test]
    fn valid_state() {
        let config = PollingConfig::new(client());
        assert!(config.stream_name().is_none());
        config.validate_state(true);
        config.validate_state(false);
        let config = config.set_stream_name("PollingConfigTest");
        assert_eq!(config.stream_name(), Some("PollingConfigTest"));
        config.validate_state(false);
    }

    // Port of PollingConfigTest.testInvalidStateMultiWithStreamName.
    #[test]
    #[should_panic(
        expected = "PollingConfig must not have streamName configured in multi-stream mode"
    )]
    fn invalid_state_multi_with_stream_name() {
        let config = PollingConfig::new(client()).set_stream_name("PollingConfigTest");
        config.validate_state(true);
    }

    // Port of PollingConfigTest.testInvalidRecordLimit.
    #[test]
    #[should_panic(expected = "maxRecords must be less than or equal to")]
    fn invalid_record_limit() {
        let _ = PollingConfig::new(client()).set_max_records(DEFAULT_MAX_RECORDS + 1);
    }

    // Port of PollingConfigTest.testMaxPendingProcessRecordsInputLimit.
    #[test]
    #[should_panic(expected = "maxPendingProcessRecordsInput must be less than or equal to")]
    fn max_pending_process_records_input_limit() {
        let _ = PollingConfig::new(client()).set_max_pending_process_records_input(
            DEFAULT_MAX_PENDING_PROCESS_RECORDS_INPUT_LIMIT + 1,
        );
    }

    // Port of PollingConfigTest.testMinIdleMillisLimit.
    #[test]
    fn min_idle_millis_limit() {
        let config = PollingConfig::new(client()).set_idle_time_between_reads_in_millis(0);
        assert_eq!(
            config.idle_time_between_reads_in_millis(),
            MIN_IDLE_MILLIS_BETWEEN_READS
        );
    }
}
