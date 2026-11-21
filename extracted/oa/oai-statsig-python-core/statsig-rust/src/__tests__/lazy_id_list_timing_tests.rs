use super::*;
use crate::id_lists_adapter::id_list_load_timing::collection_enabled;
use crate::observability::ops_stats::OpsStatsEvent;
use rusty_fork::rusty_fork_test;

#[tokio::test]
async fn lazy_load_timing_distinguishes_caller_timeout_from_background_completion() {
    let observer = crate::__tests__::mock_observability_client::observer();
    let (mut statsig, _provider) = tests::setup_lazy_config_test_with_observer(
        Duration::from_millis(100),
        Some(Arc::downgrade(&observer)),
    )
    .await;
    statsig.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut events = statsig.ops_stats.subscribe_for_test();
    let user = StatsigUser::with_user_id("lazy-member");
    assert!(
        statsig
            .get_dynamic_config(&user, "lazy-config")
            .details
            .reason
            .contains("IdListLoadTimeout")
    );
    let mut waits = 0;
    tokio::time::timeout(Duration::from_secs(3), async {
        loop {
            if let OpsStatsEvent::Observability(event) = events.recv().await.unwrap() {
                match event.metric_name.as_str() {
                    "lazy_id_list_load.wait_ms" => {
                        assert_eq!(event.tags.unwrap()["outcome"], "timeout");
                        assert!(event.value >= 20.0);
                        waits += 1;
                    }
                    "lazy_id_list_load.batch_ms" => {
                        assert_eq!(event.tags.unwrap()["outcome"], "success");
                        assert!(event.value >= 100.0);
                        break;
                    }
                    _ => {}
                }
            }
        }
    })
    .await
    .unwrap();
    assert_eq!(waits, 1);
    assert_eq!(
        statsig
            .get_dynamic_config(&user, "lazy-config")
            .get_opt::<bool>("loaded"),
        Some(true)
    );
    while let Ok(event) = events.try_recv() {
        let OpsStatsEvent::Observability(event) = event else {
            continue;
        };
        assert_ne!(
            event.metric_name, "lazy_id_list_load.wait_ms",
            "warm evaluations do not wait for a load"
        );
    }
}

#[tokio::test]
#[cfg(feature = "ffi-support")]
async fn lazy_load_timing_covers_raw_bindings() {
    let observer = crate::__tests__::mock_observability_client::observer();
    let (mut statsig, _provider) = tests::setup_lazy_config_test_with_observer(
        Duration::ZERO,
        Some(Arc::downgrade(&observer)),
    )
    .await;
    statsig.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut events = statsig.ops_stats.subscribe_for_test();
    let user = StatsigUser::with_user_id("lazy-member");
    statsig.use_raw_dynamic_config_with_options(&user, "lazy-config", Default::default(), |_| {});
    let mut waits = 0;
    tokio::time::timeout(Duration::from_secs(3), async {
        loop {
            if let OpsStatsEvent::Observability(event) = events.recv().await.unwrap() {
                if event.metric_name == "lazy_id_list_load.wait_ms" {
                    waits += 1;
                }
                if event.metric_name == "lazy_id_list_load.batch_ms" {
                    assert_eq!(event.tags.unwrap()["outcome"], "success");
                    break;
                }
            }
        }
    })
    .await
    .unwrap();
    // Completion and caller-wait metrics may arrive in either order.
    while let Ok(event) = events.try_recv() {
        if let OpsStatsEvent::Observability(event) = event {
            waits += usize::from(event.metric_name == "lazy_id_list_load.wait_ms");
        }
    }
    assert_eq!(waits, 1);
    statsig.use_raw_dynamic_config_with_options(&user, "lazy-config", Default::default(), |_| {});
    while let Ok(event) = events.try_recv() {
        if let OpsStatsEvent::Observability(event) = event {
            assert_ne!(event.metric_name, "lazy_id_list_load.wait_ms");
        }
    }
}

#[test]
fn lazy_load_timing_requires_a_live_configured_observer() {
    let observer = crate::__tests__::mock_observability_client::observer();
    assert!(!collection_enabled(None));
    let mut options = StatsigOptions::default();
    assert!(!collection_enabled(Some(&options)));
    options.observability_client = Some(Arc::downgrade(&observer));
    assert!(collection_enabled(Some(&options)));
    // An unrelated experimental flag does not control metrics.
    options.experimental_flags = Some(["parallel_lazy_id_list_builds".into()].into());
    assert!(collection_enabled(Some(&options)));
    options = options.suppress_diagnostic_output(true);
    assert!(!collection_enabled(Some(&options)));
    options = options.suppress_diagnostic_output(false);
    assert!(collection_enabled(Some(&options)));
    drop(observer);
    assert!(!collection_enabled(Some(&options)));
    assert!(!collection_enabled(None));
}

#[tokio::test]
async fn lazy_load_silent_observer_skips_collection_and_export() {
    use crate::id_lists_adapter::id_list_load_timing::{start_phase, time_list_load};
    let observer = crate::__tests__::mock_observability_client::observer();
    let (statsig, _provider) = tests::setup_lazy_config_test_with_options(
        StatsigOptions {
            observability_client: Some(Arc::downgrade(&observer)),
            ..Default::default()
        }
        .suppress_diagnostic_output(true),
    )
    .await;
    let LocalIdLists::Worker(adapter) = &statsig.id_lists_adapter else {
        panic!("expected worker adapter")
    };
    let enabled = adapter.load_timings_enabled;
    assert!(!enabled);
    let ops = OpsStatsForInstance::new();
    let mut events = ops.subscribe_for_test();
    time_list_load(&ops, "members", enabled, async {
        assert!(start_phase().is_none());
        Ok(true)
    })
    .await
    .unwrap();
    assert!(events.try_recv().is_err());
    assert!(statsig.ops_stats.is_disabled_for_test());
    let user = StatsigUser::with_user_id("lazy-member");
    let deadline = Instant::now() + Duration::from_secs(3);
    while statsig
        .get_dynamic_config(&user, "lazy-config")
        .get_opt::<bool>("loaded")
        != Some(true)
    {
        assert!(Instant::now() < deadline);
        tokio::time::sleep(Duration::from_millis(5)).await;
    }
}

#[tokio::test]
async fn lazy_load_without_observer_skips_collection_and_export() {
    use crate::id_lists_adapter::id_list_load_timing::{start_phase, time_list_load};
    let ops = OpsStatsForInstance::new();
    let mut events = ops.subscribe_for_test();
    time_list_load(&ops, "members", collection_enabled(None), async {
        assert!(
            start_phase().is_none(),
            "disabled load installed a timing context"
        );
        Ok(true)
    })
    .await
    .unwrap();
    assert!(events.try_recv().is_err());

    let (mut statsig, _provider) = tests::setup_lazy_config_test(Duration::ZERO).await;
    // Keep the queue observable even though this SDK has no observer installed.
    statsig.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut events = statsig.ops_stats.subscribe_for_test();
    let user = StatsigUser::with_user_id("lazy-member");
    let deadline = Instant::now() + Duration::from_secs(3);
    while statsig
        .get_dynamic_config(&user, "lazy-config")
        .get_opt::<bool>("loaded")
        != Some(true)
    {
        assert!(Instant::now() < deadline);
        tokio::time::sleep(Duration::from_millis(5)).await;
    }
    while let Ok(event) = events.try_recv() {
        for event in crate::id_lists_adapter::id_list_load_timing::metrics_for_test(event) {
            assert!(!event.metric_name.starts_with("lazy_id_list_load."));
        }
    }
}

// Isolate the process-global SDK runtime so the worker count cannot be inherited
// from another test. Register through options, exactly as an application does.
rusty_fork_test! {
    #[test]
    fn id_list_callbacks_do_not_block_other_lists_on_a_single_sdk_worker() {
        let runtime = tokio::runtime::Builder::new_current_thread().enable_all().build().unwrap();
        runtime.block_on(async {
            for metric in [
                "lazy_id_list_load.list_phase_ms",
                "lazy_id_list_load.wait_ms",
                "lazy_id_list_load.batch_ms",
                "id_list_membership_lookup",
                "id_list_membership_rpc_latency_ms",
            ] {
                let (entered_tx, entered_rx) = std::sync::mpsc::channel();
                let (release_tx, release_rx) = std::sync::mpsc::channel();
                let observer: Arc<dyn crate::ObservabilityClient> = Arc::new(BlockingObserver {
                    metric: format!("statsig.sdk.{metric}"),
                    entered: parking_lot::Mutex::new(Some(entered_tx)),
                    release: parking_lot::Mutex::new(release_rx),
                });
                let (statsig, _provider) = tests::setup_lazy_config_test_with_options(StatsigOptions {
                    sdk_runtime_thread_count: Some(1),
                    observability_client: Some(Arc::downgrade(&observer)),
                    ..Default::default()
                }).await;
                assert_eq!(statsig.statsig_runtime.get_handle().unwrap().metrics().num_workers(), 1);
                let _release_on_failure = scopeguard::guard(release_tx, |tx| { let _ = tx.send(()); });
                let user = StatsigUser::with_user_id("lazy-member");
                statsig.get_dynamic_config(&user, "lazy-config");
                let metrics = remote_id_list_metrics::RemoteIdListMetrics::new(
                    &statsig.options, &statsig.ops_stats,
                );
                metrics.record_cache_hit("members", Some(true), true);
                metrics.record_rpc_latency("members", Some(Duration::ZERO), "answered");
                entered_rx.recv_timeout(Duration::from_secs(3)).unwrap();
                // The observer is blocked. A second cold list must still load on this call.
                let result = statsig.get_dynamic_config(&user, "second-config");
                assert_eq!(result.get_opt::<bool>("loaded"), Some(true), "{metric}: {}", result.details.reason);
                assert!(!result.details.reason.contains("IdListLoadTimeout"));
            }
        });
    }
}

struct BlockingObserver {
    metric: String,
    entered: parking_lot::Mutex<Option<std::sync::mpsc::Sender<()>>>,
    release: parking_lot::Mutex<std::sync::mpsc::Receiver<()>>,
}
impl crate::ObservabilityClient for BlockingObserver {
    fn init(&self) {}
    fn increment(&self, name: String, value: f64, tags: Option<HashMap<String, String>>) {
        self.dist(name, value, tags);
    }
    fn gauge(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
    fn error(&self, _: String, _: String) {}
    fn should_enable_high_cardinality_for_this_tag(&self, _: String) -> Option<bool> {
        Some(false)
    }
    fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn crate::OpsStatsEventObserver> {
        self
    }
    fn dist(&self, name: String, _: f64, _: Option<HashMap<String, String>>) {
        if name == self.metric {
            if let Some(entered) = self.entered.lock().take() {
                entered.send(()).unwrap();
                self.release
                    .lock()
                    .recv_timeout(Duration::from_secs(5))
                    .unwrap();
            }
        }
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn lazy_load_batch_reports_publication_failure() {
    let observer = crate::__tests__::mock_observability_client::observer();
    let (statsig, _provider) = tests::setup_lazy_config_test_with_observer(
        Duration::ZERO,
        Some(Arc::downgrade(&observer)),
    )
    .await;
    let mut events = statsig.ops_stats.subscribe_for_test();
    statsig
        .spec_store
        .with_id_list_mutation_locked_for_test(|| {
            let result = statsig
                .get_dynamic_config(&StatsigUser::with_user_id("lazy-member"), "lazy-config");
            assert!(result.details.reason.contains("IdListLoadTimeout"));
            let mut totals = 0;
            futures::executor::block_on(async {
                loop {
                    let event = tokio::time::timeout(Duration::from_secs(10), events.recv())
                        .await
                        .unwrap()
                        .unwrap();
                    for event in
                        crate::id_lists_adapter::id_list_load_timing::metrics_for_test(event)
                    {
                        let tags = event.tags.unwrap_or_default();
                        if event.metric_name == "lazy_id_list_load.list_phase_ms"
                            && tags["phase"] == "total"
                        {
                            assert_eq!(tags["outcome"], "error");
                            totals += 1;
                        }
                        if event.metric_name == "lazy_id_list_load.batch_ms" {
                            assert_eq!(tags["outcome"], "error");
                            return;
                        }
                    }
                }
            });
            assert_eq!(totals, 1);
            assert!(statsig.spec_store.load_data().id_lists.is_empty());
        });
}
