mod utils;

use parking_lot::Mutex;
use serial_test::serial;
use statsig_rust::output_logger::{LogLevel, initialize_output_logger, shutdown_output_logger};
use statsig_rust::{SpecsUpdateListener, Statsig, StatsigOptions, log_d, log_e, log_i, log_w};
use std::sync::Arc;
use std::time::Duration;
use utils::mock_log_provider::{MockLogProvider, RecordedLog};

use crate::utils::mock_scrapi::{Endpoint, MockScrapi};

fn nested_decode_failure(marker: &str, time: u64) -> statsig_rust::SpecsUpdate {
    statsig_rust::SpecsUpdate {
        data: statsig_rust::networking::ResponseData::from_bytes(
            serde_json::to_vec(&serde_json::json!({
                "has_updates": true, "time": time, "checksum": time.to_string(),
                "feature_gates": {"fake": {"enabled": marker}},
                "dynamic_configs": {}, "layer_configs": {},
                "experiment_to_layer": {}, "condition_map": {}
            }))
            .unwrap(),
        ),
        source: statsig_rust::SpecsSource::Network,
        received_at: time,
        source_api: Some("local-fixture".into()),
        has_updates: None,
    }
}

#[tokio::test]
#[serial]
async fn silent_client_isolated_for_both_orders_and_shared_instance_ids() {
    for construction_order in ["ordinary_first", "silent_first", "concurrent"] {
        for same_id in [false, true] {
            shutdown_output_logger();
            let ordinary_provider = Arc::new(MockLogProvider::new());
            let silent_provider = Arc::new(MockLogProvider::new());
            let make = |silent: bool, provider: Arc<MockLogProvider>| {
                let mut options = StatsigOptions {
                    sdk_instance_id: Some(
                        if same_id || !silent {
                            "shared"
                        } else {
                            "separate"
                        }
                        .into(),
                    ),
                    disable_all_logging: Some(true),
                    disable_network: Some(true),
                    disable_disk_access: Some(true),
                    output_log_level: Some(LogLevel::Debug),
                    output_logger_provider: Some(provider),
                    ..StatsigOptions::default()
                }
                .suppress_diagnostic_output(silent);
                // The real caller constructs its HTTP adapter before Statsig::new.
                options.specs_adapter = Some(Arc::new(statsig_rust::StatsigHttpSpecsAdapter::new(
                    "secret-SILENT_TEST_ONLY",
                    Some(&options),
                    None,
                )));
                Statsig::new("secret-SILENT_TEST_ONLY", Some(Arc::new(options)))
            };
            let (ordinary, silent) = if construction_order == "concurrent" {
                let start = std::sync::Barrier::new(2);
                std::thread::scope(|scope| {
                    let ordinary = scope.spawn(|| {
                        start.wait();
                        make(false, ordinary_provider.clone())
                    });
                    start.wait();
                    let silent = make(true, silent_provider.clone());
                    (ordinary.join().unwrap(), silent)
                })
            } else if construction_order == "silent_first" {
                let silent = make(true, silent_provider.clone());
                (make(false, ordinary_provider.clone()), silent)
            } else {
                (
                    make(false, ordinary_provider.clone()),
                    make(true, silent_provider.clone()),
                )
            };
            assert!(silent_provider.logs.lock().is_empty());
            ordinary_provider.clear();

            let ordinary_store = ordinary.get_context().spec_store;
            let silent_store = silent.get_context().spec_store;
            let barrier = Arc::new(std::sync::Barrier::new(2));
            std::thread::scope(|scope| {
                let ordinary_barrier = barrier.clone();
                let ordinary_store = &ordinary_store;
                scope.spawn(move || {
                    ordinary_barrier.wait();
                    ordinary_store
                        .set_values(nested_decode_failure("secret-LOUDX_TEST_ONLY", 1))
                        .unwrap();
                });
                barrier.wait();
                // Tolerant decoding still succeeds; it must not print the rejected item's value.
                silent_store
                    .set_values(nested_decode_failure("secret-QUIET_TEST_ONLY", 1))
                    .unwrap();
            });
            let recorded = format!("{:?}", ordinary_provider.logs.lock());
            assert!(recorded.contains("secret-LOUDX"));
            assert!(!recorded.contains("secret-QUIET"));
            assert_eq!(silent_store.get_current_specs_info().lcut, Some(1));

            let callback_store = ordinary_store.clone();
            silent.subscribe(
                statsig_rust::sdk_event_emitter::SdkEvent::SPECS_UPDATED,
                move |_| {
                    callback_store
                        .set_values(nested_decode_failure("secret-REENT_TEST_ONLY", 2))
                        .unwrap();
                },
            );
            ordinary_provider.clear();
            silent_store
                .set_values(nested_decode_failure("secret-QUIET_TEST_ONLY", 2))
                .unwrap();
            let recorded = format!("{:?}", ordinary_provider.logs.lock());
            assert!(
                recorded.contains("secret-REENT"),
                "ordinary client keeps diagnostics in a reentrant callback"
            );
            assert!(!recorded.contains("secret-QUIET"));

            ordinary_provider.clear();
            let shutdown_barrier = Arc::new(std::sync::Barrier::new(2));
            let concurrent_barrier = shutdown_barrier.clone();
            let concurrent_store = ordinary_store.clone();
            let ordinary_work = std::thread::spawn(move || {
                concurrent_barrier.wait();
                concurrent_store
                    .set_values(nested_decode_failure("secret-ACTIVE_TEST_ONLY", 3))
                    .unwrap();
            });
            shutdown_barrier.wait();
            let _ = silent.initialize().await;
            let _ = silent.shutdown().await;
            drop(silent);
            ordinary_work.join().unwrap();
            let recorded = format!("{:?}", ordinary_provider.logs.lock());
            assert!(recorded.contains("secret-ACTIV"));
            assert!(!recorded.contains("secret-SILEN"));
            {
                let logs = ordinary_provider.logs.lock();
                assert!(
                    !logs.contains(&RecordedLog::Init) && !logs.contains(&RecordedLog::Shutdown),
                    "silent initialization/shutdown/drop must not reset the ordinary logger"
                );
            }
            assert!(silent_provider.logs.lock().is_empty());
            ordinary_provider.clear();
            log_w!("ordinary-still-running", "ordinary diagnostic survives");
            assert_eq!(ordinary_provider.logs.lock().len(), 1);

            drop(ordinary);
            let replacement = Arc::new(MockLogProvider::new());
            initialize_output_logger(&Some(LogLevel::Warn), Some(replacement.clone()));
            log_w!("replacement", "legacy reinitialization still works");
            assert_eq!(replacement.logs.lock().len(), 2);
            shutdown_output_logger();
        }
    }
}

#[test]
#[serial]
fn disabling_silent_option_restores_legacy_without_changing_other_flags() {
    let provider = Arc::new(MockLogProvider::new());
    shutdown_output_logger();
    let options = StatsigOptions {
        output_logger_provider: Some(provider.clone()),
        disable_network: Some(true),
        disable_disk_access: Some(true),
        disable_all_logging: Some(true),
        experimental_flags: Some(["unrelated".into()].into()),
        ..StatsigOptions::default()
    }
    .suppress_diagnostic_output(true)
    .suppress_diagnostic_output(false);
    assert_eq!(options.experimental_flags.as_ref().unwrap().len(), 1);
    assert_eq!(options.disable_all_logging, Some(true));
    let client = Statsig::new("secret-FAKE_ONLY", Some(Arc::new(options)));
    assert!(provider.logs.lock().contains(&RecordedLog::Init));
    drop(client);
    assert!(provider.logs.lock().contains(&RecordedLog::Shutdown));
}

#[tokio::test]
#[serial]
async fn preconstructed_http_adapter_suppresses_real_spawned_background_failure() {
    shutdown_output_logger();
    let provider = Arc::new(MockLogProvider::new());
    initialize_output_logger(&Some(LogLevel::Debug), Some(provider.clone()));
    let runtime = statsig_rust::StatsigRuntime::get_runtime();
    for silent in [true, false] {
        let options = StatsigOptions {
            disable_network: Some(true),
            disable_disk_access: Some(true),
            specs_url: Some("https://example.invalid/secret-BACKGROUND_ONLY".into()),
            ..StatsigOptions::default()
        }
        .suppress_diagnostic_output(silent);
        let adapter = Arc::new(statsig_rust::StatsigHttpSpecsAdapter::new(
            "secret-BACKGROUND_ONLY",
            Some(&options),
            None,
        ));
        provider.clear();
        // A genuine spawned task, but no sockets, elapsed-time sleeps or live credentials.
        let (sender, receiver) = tokio::sync::oneshot::channel();
        runtime
            .spawn("background-output-test", move |_| async move {
                adapter.run_background_sync().await;
                sender.send(()).unwrap();
            })
            .unwrap();
        receiver.await.unwrap();
        runtime.await_tasks_with_tag("background-output-test").await;
        let errors = provider.get_error_logs();
        assert_eq!(
            errors.is_empty(),
            silent,
            "only the ordinary adapter reports its failure"
        );
        if silent {
            assert!(!format!("{:?}", provider.logs.lock()).contains("secret-BACKG"));
        }
    }
    runtime.shutdown();
    shutdown_output_logger();
}

#[test]
#[serial]
fn test_custom_log_provider() {
    let provider = Arc::new(MockLogProvider {
        logs: Mutex::new(Vec::new()),
    });

    initialize_output_logger(&Some(LogLevel::Debug), Some(provider.clone()));

    let test_tag = "test_tag";

    log_d!(test_tag, "debug message");
    log_i!(test_tag, "info message");
    log_w!(test_tag, "warn message");
    log_e!(test_tag, "error message");

    shutdown_output_logger();

    let logs = provider.logs.try_lock_for(Duration::from_secs(5)).unwrap();
    assert_eq!(logs.len(), 6);

    assert_eq!(logs[0], RecordedLog::Init);
    assert_eq!(
        logs[1],
        RecordedLog::Debug(test_tag.to_string(), "debug message".to_string())
    );
    assert_eq!(
        logs[2],
        RecordedLog::Info(test_tag.to_string(), "info message".to_string())
    );
    assert_eq!(
        logs[3],
        RecordedLog::Warn(test_tag.to_string(), "warn message".to_string())
    );
    assert_eq!(
        logs[4],
        RecordedLog::Error(test_tag.to_string(), "error message".to_string())
    );
    assert_eq!(logs[5], RecordedLog::Shutdown);
}

#[test]
#[serial]
fn test_log_level_filtering() {
    let provider = Arc::new(MockLogProvider {
        logs: Mutex::new(Vec::new()),
    });

    initialize_output_logger(&Some(LogLevel::Warn), Some(provider.clone()));

    let test_tag = "test_tag";

    log_d!(test_tag, "debug message");
    log_i!(test_tag, "info message");
    log_w!(test_tag, "warn message");
    log_e!(test_tag, "error message");

    shutdown_output_logger();

    let logs = provider.logs.try_lock_for(Duration::from_secs(5)).unwrap();
    assert_eq!(logs.len(), 4); // Init + Warn + Error + Shutdown

    assert_eq!(logs[0], RecordedLog::Init);
    assert_eq!(
        logs[1],
        RecordedLog::Warn(test_tag.to_string(), "warn message".to_string())
    );
    assert_eq!(
        logs[2],
        RecordedLog::Error(test_tag.to_string(), "error message".to_string())
    );
    assert_eq!(logs[3], RecordedLog::Shutdown);
}

#[test]
#[serial]
fn test_message_truncation() {
    let provider = Arc::new(MockLogProvider {
        logs: Mutex::new(Vec::new()),
    });

    initialize_output_logger(&Some(LogLevel::Debug), Some(provider.clone()));

    let test_tag = "test_tag";
    let long_message = "x".repeat(500);
    log_d!(test_tag, "{}", long_message);

    let logs = {
        let mut guard = provider.logs.try_lock_for(Duration::from_secs(5)).unwrap();
        std::mem::take(&mut *guard)
    };
    assert_eq!(logs.len(), 2);

    if let RecordedLog::Debug(_, msg) = &logs[1] {
        assert!(msg.len() <= 400 + 13);
        assert!(msg.ends_with("...[TRUNCATED]"));
    } else {
        panic!("Expected Debug log level");
    }

    shutdown_output_logger();
}

#[test]
#[serial]
fn test_secret_sanitization() {
    let provider = Arc::new(MockLogProvider {
        logs: Mutex::new(Vec::new()),
    });

    initialize_output_logger(&Some(LogLevel::Debug), Some(provider.clone()));

    let test_tag = "test_tag";
    let message = "secret-key12345 and secret-abcde";
    log_d!(test_tag, "{}", message);

    let logs = {
        let mut guard = provider.logs.try_lock_for(Duration::from_secs(5)).unwrap();
        std::mem::take(&mut *guard)
    };
    assert_eq!(logs.len(), 2); // Init + Debug

    if let RecordedLog::Debug(_, msg) = &logs[1] {
        assert_eq!(msg, "secret-key12***** and secret-abcde*****");
    } else {
        panic!("Expected Debug log level");
    }

    shutdown_output_logger();
}

#[tokio::test]
#[serial]
async fn test_default_logger_no_error_on_multiple_instances() {
    let mock_scrapi = MockScrapi::new().await;
    let options = StatsigOptions {
        log_event_url: Some(mock_scrapi.url_for_endpoint(Endpoint::LogEvent)),
        specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
        ..StatsigOptions::new()
    };

    // checking for uncaught panics
    let statsig1 = Statsig::new("secret-key12345", Some(Arc::new(options.clone())));
    let statsig2 = Statsig::new("secret-key67890", Some(Arc::new(options)));

    let _ = statsig1.initialize().await;
    let _ = statsig2.initialize().await;

    let _ = statsig1.shutdown().await;
    let _ = statsig2.shutdown().await;
}

#[tokio::test]
#[serial]
async fn test_custom_logger_no_error_on_multiple_instances() {
    // checking for uncaught panics
    let provider = Arc::new(MockLogProvider {
        logs: Mutex::new(Vec::new()),
    });

    let provider2 = provider.clone();

    let mock_scrapi = MockScrapi::new().await;
    let mut options1 = StatsigOptions {
        log_event_url: Some(mock_scrapi.url_for_endpoint(Endpoint::LogEvent)),
        specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
        ..StatsigOptions::new()
    };
    options1.output_logger_provider = Some(provider.clone());

    let mut options2 = StatsigOptions {
        log_event_url: Some(mock_scrapi.url_for_endpoint(Endpoint::LogEvent)),
        specs_url: Some(mock_scrapi.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
        ..StatsigOptions::new()
    };
    options2.output_logger_provider = Some(provider2.clone());

    let statsig1 = Statsig::new("secret-key12345", Some(Arc::new(options1)));
    let statsig2 = Statsig::new("secret-key67890", Some(Arc::new(options2)));

    let _ = statsig1.initialize().await;
    let _ = statsig2.initialize().await;

    let _ = statsig1.shutdown().await;
    let _ = statsig2.shutdown().await;
}
