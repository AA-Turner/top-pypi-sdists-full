mod utils;

use crate::utils::mock_observability_client::MockObservabilityClient;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use async_trait::async_trait;
use more_asserts::assert_gt;
use serial_test::serial;
use statsig_rust::log_event_payload::LogEventRequest;
use statsig_rust::networking::NetworkError;
use statsig_rust::output_logger::LogLevel;
use statsig_rust::{EventLoggingAdapter, StatsigRuntime};
use statsig_rust::{ObservabilityClient, Statsig, StatsigErr, StatsigOptions, StatsigUser};
use std::sync::{Arc, atomic::Ordering};
use std::sync::{Mutex, atomic::AtomicBool};
use std::time::Duration;
use tokio::sync::Notify;
use utils::mock_event_logging_adapter::MockEventLoggingAdapter;

async fn setup(
    options: StatsigOptions,
) -> (
    Statsig,
    Arc<MockEventLoggingAdapter>,
    Arc<MockObservabilityClient>,
) {
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    setup_with_logging_adapter(options, logging_adapter).await
}

async fn setup_with_logging_adapter(
    options: StatsigOptions,
    logging_adapter: Arc<MockEventLoggingAdapter>,
) -> (
    Statsig,
    Arc<MockEventLoggingAdapter>,
    Arc<MockObservabilityClient>,
) {
    let specs_adapter = Arc::new(MockSpecsAdapter::with_data("tests/data/eval_proj_dcs.json"));

    let obs_client = Arc::new(MockObservabilityClient::new());
    let obs_client_dyn: Arc<dyn ObservabilityClient> = obs_client.clone();

    let mut options = options;
    options.specs_adapter = Some(specs_adapter);
    options.event_logging_adapter = Some(logging_adapter.clone());
    options.disable_country_lookup = Some(true);
    options.output_log_level = Some(LogLevel::Debug);
    options.observability_client = Some(Arc::downgrade(&obs_client_dyn));

    let uuid = uuid::Uuid::new_v4();
    let statsig = Statsig::new(&format!("secret-{uuid}"), Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    (statsig, logging_adapter, obs_client)
}

async fn teardown(statsig: Option<Statsig>) {
    std::env::remove_var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS");
    std::env::remove_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS");
    std::env::remove_var("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS");
    std::env::remove_var("STATSIG_TEST_OVERRIDE_MAX_LOG_EVENT_RETRIES");

    if let Some(statsig) = statsig {
        let _ = statsig.shutdown().await;
    }
}

#[tokio::test]
#[serial]
async fn test_limit_flushing() {
    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(10);
    options.event_logging_max_pending_batch_queue_size = Some(60);

    let (statsig, logging_adapter, _) = setup(options).await;

    log_some_events(&statsig, 456);

    assert_eventually!(|| {
        let count = logging_adapter.logged_event_count.load(Ordering::SeqCst);
        count > 0 && count < 456 // logged some but not all
    });

    statsig.shutdown().await.unwrap();

    // logged all events
    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        456
    );

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_disables_background_flush_when_adapter_opts_out() {
    std::env::set_var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS", "1");

    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(10);
    options.event_logging_max_pending_batch_queue_size = Some(20);

    let logging_adapter = Arc::new(MockEventLoggingAdapter::new_with_background_flush(false));
    let (statsig, logging_adapter, _) = setup_with_logging_adapter(options, logging_adapter).await;

    log_some_events(&statsig, 20);

    assert!(
        tokio::time::timeout(
            Duration::from_millis(100),
            logging_adapter.on_log_notify.notified()
        )
        .await
        .is_err()
    );
    assert_eq!(logging_adapter.times_called.load(Ordering::SeqCst), 0);

    statsig.shutdown().await.unwrap();

    assert_eq!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        20
    );

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_scheduled_flush_batch_size() {
    const MAX_EVENTS: usize = 5;

    std::env::set_var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "1");

    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(MAX_EVENTS as u32);
    options.event_logging_max_pending_batch_queue_size = Some(2);

    let (statsig, logging_adapter, _) = setup(options).await;

    // trigger failure backoff
    *logging_adapter.mocked_log_events_result.lock().unwrap() =
        Err(StatsigErr::CustomError("test error".into()));

    log_some_events(&statsig, MAX_EVENTS);

    // begin accepting events
    logging_adapter.on_log_notify.notified().await;
    *logging_adapter.mocked_log_events_result.lock().unwrap() = Ok(true);

    assert_eventually_eq!(
        || logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        MAX_EVENTS as u64
    );

    let req = logging_adapter.logged_payloads.lock().unwrap().remove(0);
    assert_eq!(
        req.statsig_metadata
            .get("flushType")
            .and_then(|v| v.as_str()),
        Some("scheduled:full_batch")
    );

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_scheduled_flush_max_time() {
    std::env::set_var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS", "1");

    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(10);
    options.event_logging_max_pending_batch_queue_size = Some(2);

    let (statsig, logging_adapter, _) = setup(options).await;

    // trigger failure backoff
    *logging_adapter.mocked_log_events_result.lock().unwrap() =
        Err(StatsigErr::CustomError("test error".into()));

    let user = StatsigUser::with_user_id("user_1");
    for _ in 0..5 {
        statsig.log_event(&user, "test_event", None, None);
    }

    // begin accepting events
    wait_for_log_notify(&logging_adapter).await;
    *logging_adapter.mocked_log_events_result.lock().unwrap() = Ok(true);

    assert_eventually_eq!(
        || logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        5
    );

    let req = logging_adapter.logged_payloads.lock().unwrap().remove(0);
    assert_eq!(
        req.statsig_metadata
            .get("flushType")
            .and_then(|v| v.as_str()),
        Some("scheduled:max_time")
    );

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_scheduled_flush_failures() {
    std::env::set_var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MAX_LOG_EVENT_RETRIES", "2");

    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(10);

    let (statsig, logging_adapter, obs_client) = setup(options).await;

    // get into failure backoff
    *logging_adapter.mocked_log_events_result.lock().unwrap() =
        Err(StatsigErr::CustomError("test error".into()));

    let user = StatsigUser::with_user_id("user_1");
    statsig.log_event(&user, "test_event", None, None);

    wait_for_log_notify(&logging_adapter).await; // first attempt
    wait_for_log_notify(&logging_adapter).await; // second attempt
    assert_eq!(logging_adapter.logged_event_count.load(Ordering::SeqCst), 0);

    assert_eventually!(|| {
        let count = obs_client.error_calls.lock().ok().map(|c| c.len());
        count.is_some() && count.unwrap() >= 1
    });

    let error = obs_client.error_calls.lock().unwrap().remove(0);
    assert_eq!(error.0, "statsig::log_event_failed");

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_requeue_dropped_events() {
    std::env::set_var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS", "1");

    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(5);
    options.event_logging_max_pending_batch_queue_size = Some(1);

    let (statsig, logging_adapter, obs_client) = setup(options).await;

    // get into failure backoff
    *logging_adapter.mocked_log_events_result.lock().unwrap() =
        Err(StatsigErr::CustomError("test error".into()));

    let user = StatsigUser::with_user_id("user_1");
    statsig.log_event(&user, "test_event", None, None);

    wait_for_log_notify(&logging_adapter).await;
    assert_eq!(logging_adapter.logged_event_count.load(Ordering::SeqCst), 0);
    assert_eq!(obs_client.error_calls.lock().unwrap().len(), 0);

    for _ in 0..50 {
        statsig.log_event(&user, "test_event", None, None);
    }

    assert_eventually!(|| {
        let count = obs_client.error_calls.lock().ok().map(|c| c.len());
        count.is_some() && count.unwrap() > 1
    });

    let error = obs_client.error_calls.lock().unwrap().remove(0);
    assert_eq!(error.0, "statsig::log_event_dropped_event_count");

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_high_qps_dropped_events() {
    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(10);
    options.event_logging_max_pending_batch_queue_size = Some(2);

    let (statsig, logging_adapter, obs_client) = setup(options).await;

    for i in 0..1000 {
        let user = StatsigUser::with_user_id(format!("user_{i}"));
        let _ = statsig.check_gate(&user, &format!("a_gate_{i}"));
    }

    statsig.flush_events().await;

    assert_gt!(
        logging_adapter
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        0
    );

    assert_eventually_eq!(
        || {
            let mut calls = match obs_client.error_calls.lock() {
                Ok(calls) => calls,
                Err(_) => return None,
            };

            if calls.is_empty() {
                return None;
            }

            let error = calls.remove(0);
            Some(error.0)
        },
        Some("statsig::log_event_dropped_event_count".to_string())
    );

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_non_retryable_failure_drops_events() {
    std::env::set_var("STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS", "1");
    std::env::set_var("STATSIG_TEST_OVERRIDE_MAX_LOG_EVENT_RETRIES", "9999"); // retry forever

    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(5);
    options.event_logging_max_pending_batch_queue_size = Some(2);

    let (statsig, logging_adapter, obs_client) = setup(options).await;

    // get into failure backoff
    *logging_adapter.mocked_log_events_result.lock().unwrap() =
        Err(StatsigErr::NetworkError(NetworkError::RequestNotRetryable(
            "test_url".to_string(),
            Some(0),
            "test error".to_string(),
        )));

    let user = StatsigUser::with_user_id("user_1");
    statsig.log_event(&user, "test_event", None, None);

    wait_for_log_notify(&logging_adapter).await;
    assert_eq!(logging_adapter.logged_event_count.load(Ordering::SeqCst), 0);

    assert_eventually!(|| {
        let count = obs_client.error_calls.lock().ok().map(|c| c.len());
        count.is_some() && count.unwrap() >= 1
    });
    assert_eq!(logging_adapter.times_called.load(Ordering::SeqCst), 1);

    let error = match obs_client.error_calls.lock() {
        Ok(calls) => calls
            .iter()
            .find(|(e, _)| e == "statsig::log_event_failed")
            .cloned(),
        Err(_) => None,
    };
    assert!(error.is_some());

    teardown(Some(statsig)).await;
}

#[tokio::test]
#[serial]
async fn test_logging_behavior_when_network_is_disabled() {
    let mut options = StatsigOptions::new();
    options.event_logging_max_queue_size = Some(5);
    options.disable_network = Some(true);
    options.event_logging_max_pending_batch_queue_size = Some(2);
    let (statsig, logging_adapter, obs_client) = setup(options).await;
    let user = StatsigUser::with_user_id("user_1");
    statsig.log_event(&user, "test_event", None, None);
    statsig.flush_events().await;
    assert!(
        logging_adapter
            .times_called
            .fetch_or(u64::MAX, Ordering::SeqCst)
            == 1
    );
    // Verify observability client is not called
    assert!(obs_client.error_calls.lock().unwrap().is_empty())
}

async fn wait_for_log_notify(logging_adapter: &MockEventLoggingAdapter) {
    tokio::select! {
        _ = logging_adapter.on_log_notify.notified() => {
            // done waiting
        }
        _ = tokio::time::sleep(Duration::from_millis(1000)) => {
            panic!("Timeout waiting for log notify");
        }
    }
}

fn log_some_events(statsig: &Statsig, count: usize) {
    let user = StatsigUser::with_user_id("user_1");
    for _ in 0..count {
        statsig.log_event(&user, "test_event", None, None);
    }
}

// Block only the first export after it has taken ownership of a batch. Later
// shutdown exports can succeed independently, exposing an empty-queue race.
struct BlockingLoggingAdapter {
    inner: MockEventLoggingAdapter,
    first: AtomicBool,
    entered: Notify,
    release: Notify,
    finished: Notify,
    first_flush_type: Mutex<Option<String>>,
    fail_first: bool,
}

struct ExportFinished<'a>(&'a Notify);

impl Drop for ExportFinished<'_> {
    fn drop(&mut self) {
        self.0.notify_one();
    }
}

#[async_trait]
impl EventLoggingAdapter for BlockingLoggingAdapter {
    async fn start(&self, _: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        Ok(())
    }

    async fn log_events(&self, request: LogEventRequest) -> Result<bool, StatsigErr> {
        if self.first.swap(false, Ordering::SeqCst) {
            let _finished = ExportFinished(&self.finished);
            *self.first_flush_type.lock().unwrap() = request
                .payload
                .statsig_metadata
                .get("flushType")
                .and_then(|v| v.as_str())
                .map(str::to_owned);
            self.entered.notify_one();
            self.release.notified().await;
            if self.fail_first {
                return Err(StatsigErr::CustomError("retry held batch".into()));
            }
        }
        self.inner.log_events(request).await
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        Ok(())
    }

    fn should_schedule_background_flush(&self) -> bool {
        true
    }
}

async fn setup_blocked_export(
    scheduled: bool,
    fail_first: bool,
) -> (Statsig, Arc<BlockingLoggingAdapter>) {
    // Keep limit flushing deterministic; the scheduled case uses a partial batch.
    std::env::set_var(
        "STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS",
        if scheduled { "1" } else { "60000" },
    );
    std::env::set_var("STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS", "1");
    std::env::set_var(
        "STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS",
        if scheduled { "1" } else { "60000" },
    );
    let adapter = Arc::new(BlockingLoggingAdapter {
        inner: MockEventLoggingAdapter::new(),
        first: AtomicBool::new(true),
        entered: Notify::new(),
        release: Notify::new(),
        finished: Notify::new(),
        first_flush_type: Mutex::new(None),
        fail_first,
    });
    let options = StatsigOptions {
        specs_adapter: Some(Arc::new(MockSpecsAdapter::with_data(
            "tests/data/eval_proj_dcs.json",
        ))),
        event_logging_adapter: Some(adapter.clone()),
        event_logging_max_queue_size: Some(if scheduled { 2000 } else { 10 }),
        disable_country_lookup: Some(true),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(
        &format!("secret-{}", uuid::Uuid::new_v4()),
        Some(Arc::new(options)),
    );
    statsig.initialize().await.unwrap();
    log_some_events(&statsig, 10);
    tokio::time::timeout(Duration::from_secs(5), adapter.entered.notified())
        .await
        .unwrap();
    assert_eq!(
        adapter.first_flush_type.lock().unwrap().as_deref(),
        Some(if scheduled {
            "scheduled:max_time"
        } else {
            "limit"
        })
    );
    (statsig, adapter)
}

async fn assert_shutdown_waits_for_export(scheduled: bool, fail_first: bool) {
    let (statsig, adapter) = setup_blocked_export(scheduled, fail_first).await;
    let shutdown = statsig.shutdown_with_timeout(Duration::from_secs(5));
    tokio::pin!(shutdown);
    // Poll shutdown while the only export is held. No sleep is a flush barrier.
    assert!(
        futures::poll!(&mut shutdown).is_pending(),
        "shutdown completed with an export still in flight"
    );
    assert_eq!(
        adapter
            .inner
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        0
    );
    adapter.release.notify_one();
    shutdown.await.unwrap();
    assert_eq!(
        adapter
            .inner
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        10
    );
    if fail_first {
        let payloads = adapter.inner.logged_payloads.lock().unwrap();
        assert!(payloads.iter().any(
            |p| p.statsig_metadata.get("flushType").and_then(|v| v.as_str()) == Some("shutdown")
        ));
    }
    teardown(None).await;
}

#[tokio::test]
#[serial]
async fn test_shutdown_waits_for_in_flight_limit_export() {
    assert_shutdown_waits_for_export(false, false).await;
}

#[tokio::test]
#[serial]
async fn test_shutdown_waits_for_in_flight_scheduled_export() {
    assert_shutdown_waits_for_export(true, false).await;
}

#[tokio::test]
#[serial]
async fn test_shutdown_retries_failed_in_flight_export() {
    assert_shutdown_waits_for_export(false, true).await;
}

#[tokio::test]
#[serial]
async fn test_shutdown_times_out_and_cancels_in_flight_export() {
    let (statsig, adapter) = setup_blocked_export(false, false).await;
    let result = tokio::time::timeout(
        Duration::from_secs(5),
        statsig.shutdown_with_timeout(Duration::from_millis(20)),
    )
    .await
    .unwrap();
    assert!(
        matches!(result, Err(StatsigErr::ShutdownFailure(_))),
        "held export must prevent successful shutdown: {result:?}"
    );
    // Runtime ownership must survive the deadline wait so cancellation really
    // drops the blocked request rather than detaching it.
    tokio::time::timeout(Duration::from_secs(5), adapter.finished.notified())
        .await
        .unwrap();
    assert_eq!(
        adapter
            .inner
            .no_diagnostics_logged_event_count
            .load(Ordering::SeqCst),
        0
    );
    teardown(None).await;
}
