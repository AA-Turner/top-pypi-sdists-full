//! Port of `software.amazon.kinesis.coordinator.StreamInfoManager`.
//!
//! Periodically backfills a `StreamInfo` entry for every currently-tracked
//! stream that doesn't already have one, on a fixed-delay schedule; no-ops
//! entirely if `StreamInfoMode` is `Disabled`.
//!
//! # Deviations
//!
//! - Java's `ScheduledExecutorService` (fixed-delay `performBackfill`) becomes a
//!   **tokio interval task** started by [`start`] and stopped by [`stop`]. The
//!   `isRunning` guard is an `AtomicBool`. `stop(is_shutdown)`'s executor
//!   escalation (`shutdown`→`awaitTermination`→`shutdownNow`) collapses into
//!   aborting the task handle (there is no separately-owned executor lifecycle).
//! - The consumers depend on the [`StreamInfoStore`] trait so the manager is
//!   unit-testable (Java tests mock `StreamInfoDAO`).

use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use tokio::task::JoinHandle;

use crate::common::{StreamConfig, StreamIdentifier};
use crate::coordinator::stream_info::{StreamIdOnboardingState, StreamInfoMode, StreamInfoStore};
use crate::leases::exceptions::LeasingError;
use crate::metrics::MetricsFactory;
use crate::utils::panic_util;

/// Periodically backfills `StreamInfo` metadata for tracked streams. Java
/// `StreamInfoManager`.
pub struct StreamInfoManager {
    current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
    stream_info_dao: Arc<dyn StreamInfoStore>,
    #[allow(dead_code)]
    metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
    #[allow(dead_code)]
    is_multi_stream_mode: bool,
    stream_info_backfill_interval_millis: u64,
    stream_info_mode: StreamInfoMode,
    stream_id_onboarding_state: StreamIdOnboardingState,

    is_running: AtomicBool,
    task: Mutex<Option<JoinHandle<()>>>,
}

impl StreamInfoManager {
    /// Java `StreamInfoManager(scheduledExecutorService, currentStreamConfigMap,
    /// streamInfoDAO, metricsFactory, isMultiStreamMode,
    /// streamInfoBackfillIntervalMillis, streamInfoMode, streamIdOnboardingState)`.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        current_stream_config_map: HashMap<StreamIdentifier, StreamConfig>,
        stream_info_dao: Arc<dyn StreamInfoStore>,
        metrics_factory: Arc<dyn MetricsFactory + Send + Sync>,
        is_multi_stream_mode: bool,
        stream_info_backfill_interval_millis: u64,
        stream_info_mode: StreamInfoMode,
        stream_id_onboarding_state: StreamIdOnboardingState,
    ) -> Self {
        Self {
            current_stream_config_map,
            stream_info_dao,
            metrics_factory,
            is_multi_stream_mode,
            stream_info_backfill_interval_millis,
            stream_info_mode,
            stream_id_onboarding_state,
            is_running: AtomicBool::new(false),
            task: Mutex::new(None),
        }
    }

    pub fn is_running(&self) -> bool {
        self.is_running.load(Ordering::SeqCst)
    }

    /// Java `synchronized start()`. No-op if StreamInfo tracking is disabled;
    /// else spawns the fixed-delay backfill task (starting immediately).
    pub fn start(self: &Arc<Self>) {
        if !self.need_stream_info() {
            return;
        }
        if self.is_running.swap(true, Ordering::SeqCst) {
            return; // already running
        }
        let this = Arc::clone(self);
        let interval = Duration::from_millis(self.stream_info_backfill_interval_millis);
        let handle = tokio::spawn(async move {
            // Java scheduleWithFixedDelay(initialDelay=0): run immediately, then
            // wait `interval` between the end of one run and the start of the next.
            loop {
                // Java StreamInfoManager catch(Throwable): a panicking backfill
                // must not kill the fixed-delay loop.
                if let Err(panic_msg) = panic_util::catch_tick(this.perform_backfill()).await {
                    tracing::error!(
                        "Error in backfill task. Will retry in {} ms: {}",
                        interval.as_millis(),
                        panic_msg
                    );
                }
                tokio::time::sleep(interval).await;
            }
        });
        *self.task.lock().unwrap() = Some(handle);
        tracing::info!("Started StreamInfoManager");
    }

    /// Java `synchronized stop(boolean isShutdown)`. Cancels the scheduled task.
    /// (`is_shutdown` in Java also shuts down the executor; here the task handle
    /// is simply aborted.)
    pub fn stop(&self, _is_shutdown: bool) {
        if self.is_running.swap(false, Ordering::SeqCst) {
            if let Some(handle) = self.task.lock().unwrap().take() {
                handle.abort();
                tracing::info!("Cancelled scheduled stream metadata back-fill task");
            }
        }
    }

    /// Java `createStreamInfo(StreamIdentifier)`. No-op if StreamInfo tracking is
    /// disabled.
    pub async fn create_stream_info(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<(), LeasingError> {
        if !self.need_stream_info() {
            return Ok(());
        }
        self.stream_info_dao
            .create_stream_info(stream_identifier)
            .await?;
        Ok(())
    }

    /// Java `deleteStreamInfo(StreamIdentifier)`. No-op if StreamInfo tracking is
    /// disabled. Deletes using the serialized identifier.
    pub async fn delete_stream_info(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<(), LeasingError> {
        if !self.need_stream_info() {
            return Ok(());
        }
        self.stream_info_dao
            .delete_stream_info(&stream_identifier.serialize())
            .await?;
        Ok(())
    }

    /// Java private `performBackfill()` — snapshots the tracked streams, lists
    /// existing `StreamInfo` keys, and creates one for each tracked stream
    /// lacking an entry. Never propagates errors (logs + retries next run).
    pub async fn perform_backfill(&self) {
        let existing: std::collections::HashSet<String> =
            match self.stream_info_dao.list_stream_info().await {
                Ok(list) => list.into_iter().map(|s| s.key().to_string()).collect(),
                Err(e) => {
                    self.log_backfill_error("Caught exception while syncing streamId.", &e);
                    return;
                }
            };

        for (stream_identifier, stream_config) in &self.current_stream_config_map {
            // Java also skips purged streams (null config); our map values are
            // always present, so this mirrors the "config present" path.
            let _ = stream_config;
            if existing.contains(&stream_identifier.serialize()) {
                tracing::debug!(stream = %stream_identifier, "Stream metadata already exists");
                continue;
            }
            if let Err(e) = self
                .stream_info_dao
                .create_stream_info(stream_identifier)
                .await
            {
                self.log_backfill_error(
                    &format!("Caught exception while syncing streamId {stream_identifier}. Will retry in next run"),
                    &e,
                );
            }
        }
    }

    fn log_backfill_error(&self, message: &str, e: &LeasingError) {
        if self.stream_id_onboarding_state == StreamIdOnboardingState::Onboarded {
            tracing::error!(error = %e, "{message}");
        } else {
            tracing::debug!(error = %e, "{message}");
        }
    }

    fn need_stream_info(&self) -> bool {
        self.stream_info_mode != StreamInfoMode::Disabled
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::arn::Arn;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
    use crate::coordinator::stream_info::stream_info_dao::MockStreamInfoStore;
    use crate::coordinator::stream_info::StreamInfo;
    use crate::metrics::NullMetricsFactory;
    use mockall::predicate::eq;

    const BACKFILL_INTERVAL: u64 = 1000;

    fn stream_config(si: StreamIdentifier) -> StreamConfig {
        StreamConfig::new(
            si,
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        )
    }

    fn single_map() -> (StreamIdentifier, HashMap<StreamIdentifier, StreamConfig>) {
        let si = StreamIdentifier::single_stream_instance("test-stream");
        let mut m = HashMap::new();
        m.insert(si.clone(), stream_config(si.clone()));
        (si, m)
    }

    fn multi_map() -> (
        Vec<StreamIdentifier>,
        HashMap<StreamIdentifier, StreamConfig>,
    ) {
        let arn1 =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/stream1").unwrap();
        let s1 = StreamIdentifier::multi_stream_instance_from_arn(arn1, 1234567890);
        let arn2 =
            Arn::from_string("arn:aws:kinesis:us-east-1:123456789012:stream/stream2").unwrap();
        let s2 = StreamIdentifier::multi_stream_instance_from_arn(arn2, 1234567891);
        let mut m = HashMap::new();
        m.insert(s1.clone(), stream_config(s1.clone()));
        m.insert(s2.clone(), stream_config(s2.clone()));
        (vec![s1, s2], m)
    }

    fn manager(
        dao: MockStreamInfoStore,
        map: HashMap<StreamIdentifier, StreamConfig>,
        multi: bool,
        mode: StreamInfoMode,
    ) -> StreamInfoManager {
        StreamInfoManager::new(
            map,
            Arc::new(dao),
            Arc::new(NullMetricsFactory::new()),
            multi,
            BACKFILL_INTERVAL,
            mode,
            StreamIdOnboardingState::NotOnboarded,
        )
    }

    #[tokio::test]
    async fn start_with_disabled_mode_does_not_start() {
        let (_, map) = single_map();
        let mgr = Arc::new(manager(
            MockStreamInfoStore::new(),
            map,
            false,
            StreamInfoMode::Disabled,
        ));
        mgr.start();
        assert!(!mgr.is_running());
    }

    #[tokio::test]
    async fn start_with_track_only_starts() {
        let (_, map) = single_map();
        let mut dao = MockStreamInfoStore::new();
        // The spawned task may call list/create; tolerate any number.
        dao.expect_list_stream_info().returning(|| Ok(Vec::new()));
        dao.expect_create_stream_info().returning(|_| Ok(true));
        let mgr = Arc::new(manager(dao, map, false, StreamInfoMode::TrackOnly));
        mgr.start();
        assert!(mgr.is_running());
        mgr.stop(false);
        assert!(!mgr.is_running());
    }

    #[tokio::test]
    async fn stop_without_shutdown_flag_stops() {
        let (_, map) = single_map();
        let mut dao = MockStreamInfoStore::new();
        dao.expect_list_stream_info().returning(|| Ok(Vec::new()));
        dao.expect_create_stream_info().returning(|_| Ok(true));
        let mgr = Arc::new(manager(dao, map, false, StreamInfoMode::TrackOnly));
        mgr.start();
        mgr.stop(false);
        assert!(!mgr.is_running());
    }

    #[tokio::test]
    async fn create_stream_info_disabled_does_not_call_dao() {
        let (si, map) = single_map();
        let dao = MockStreamInfoStore::new(); // no expectations
        let mgr = manager(dao, map, false, StreamInfoMode::Disabled);
        mgr.create_stream_info(&si).await.unwrap();
        mgr.delete_stream_info(&si).await.unwrap();
    }

    #[tokio::test]
    async fn create_stream_info_track_only_calls_dao() {
        let (si, map) = single_map();
        let mut dao = MockStreamInfoStore::new();
        let si_clone = si.clone();
        dao.expect_create_stream_info()
            .withf(move |s| s.serialize() == si_clone.serialize())
            .times(1)
            .returning(|_| Ok(true));
        let mgr = manager(dao, map, false, StreamInfoMode::TrackOnly);
        mgr.create_stream_info(&si).await.unwrap();
    }

    #[tokio::test]
    async fn create_stream_info_multi_stream_calls_dao() {
        let (ids, map) = multi_map();
        let target = ids[0].clone();
        let mut dao = MockStreamInfoStore::new();
        let target_clone = target.clone();
        dao.expect_create_stream_info()
            .withf(move |s| s.serialize() == target_clone.serialize())
            .times(1)
            .returning(|_| Ok(true));
        let mgr = manager(dao, map, true, StreamInfoMode::TrackOnly);
        mgr.create_stream_info(&target).await.unwrap();
    }

    #[tokio::test]
    async fn perform_backfill_all_exist_does_not_create() {
        let (si, map) = single_map();
        let key = si.serialize();
        let mut dao = MockStreamInfoStore::new();
        dao.expect_list_stream_info()
            .times(1)
            .returning(move || Ok(vec![StreamInfo::new(key.clone(), "stream-id")]));
        dao.expect_create_stream_info().never();
        let mgr = manager(dao, map, false, StreamInfoMode::TrackOnly);
        mgr.perform_backfill().await;
    }

    #[tokio::test]
    async fn perform_backfill_no_streams_exist_creates() {
        let (si, map) = single_map();
        let mut dao = MockStreamInfoStore::new();
        dao.expect_list_stream_info()
            .times(1)
            .returning(|| Ok(Vec::new()));
        let si_clone = si.clone();
        dao.expect_create_stream_info()
            .withf(move |s| s.serialize() == si_clone.serialize())
            .times(1)
            .returning(|_| Ok(true));
        let mgr = manager(dao, map, false, StreamInfoMode::TrackOnly);
        mgr.perform_backfill().await;
    }

    #[tokio::test]
    async fn perform_backfill_mixed_existing_and_new() {
        let s1 = StreamIdentifier::single_stream_instance("test-stream-1");
        let s2 = StreamIdentifier::single_stream_instance("test-stream-2");
        let mut map = HashMap::new();
        map.insert(s1.clone(), stream_config(s1.clone()));
        map.insert(s2.clone(), stream_config(s2.clone()));

        let s1_key = s1.serialize();
        let s2_ser = s2.serialize();
        let mut dao = MockStreamInfoStore::new();
        dao.expect_list_stream_info()
            .times(1)
            .returning(move || Ok(vec![StreamInfo::new(s1_key.clone(), "stream-id-1")]));
        dao.expect_create_stream_info()
            .withf(move |s| s.serialize() == s2_ser)
            .times(1)
            .returning(|_| Ok(true));
        let mgr = manager(dao, map, false, StreamInfoMode::TrackOnly);
        mgr.perform_backfill().await;
    }

    #[tokio::test]
    async fn perform_backfill_multi_stream_creates_both() {
        let (ids, map) = multi_map();
        let s1 = ids[0].serialize();
        let s2 = ids[1].serialize();
        let mut dao = MockStreamInfoStore::new();
        dao.expect_list_stream_info()
            .times(1)
            .returning(|| Ok(Vec::new()));
        dao.expect_create_stream_info()
            .withf(move |s| s.serialize() == s1 || s.serialize() == s2)
            .times(2)
            .returning(|_| Ok(true));
        let mgr = manager(dao, map, true, StreamInfoMode::TrackOnly);
        mgr.perform_backfill().await;
    }

    #[tokio::test]
    async fn perform_backfill_empty_config_map() {
        let mut dao = MockStreamInfoStore::new();
        dao.expect_list_stream_info()
            .times(1)
            .returning(|| Ok(Vec::new()));
        dao.expect_create_stream_info().never();
        let mgr = manager(dao, HashMap::new(), false, StreamInfoMode::TrackOnly);
        mgr.perform_backfill().await;
    }

    #[tokio::test]
    async fn delete_stream_info_with_dao_error_propagates() {
        let (si, map) = single_map();
        let mut dao = MockStreamInfoStore::new();
        dao.expect_delete_stream_info()
            .with(eq(si.serialize()))
            .returning(|_| Err(LeasingError::dependency("Test exception")));
        let mgr = manager(dao, map, false, StreamInfoMode::TrackOnly);
        assert!(mgr.delete_stream_info(&si).await.is_err());
    }
}
