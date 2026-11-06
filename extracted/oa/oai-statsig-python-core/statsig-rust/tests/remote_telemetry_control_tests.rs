#![cfg(feature = "testing")]

mod utils;

use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};
use statsig_rust::console_capture::{
    console_capture_instances::CONSOLE_CAPTURE_REGISTRY,
    console_capture_options::ConsoleCaptureOptions,
};
use statsig_rust::{
    EvaluationClient, ObservabilityClient, Statsig, StatsigOptions, StatsigUser,
    global_configs::GlobalConfigs, output_logger::LogLevel,
};
use std::{
    collections::HashMap,
    future::Future,
    sync::{Arc, Weak, atomic::Ordering},
    time::{Duration, Instant},
};
use utils::{
    helpers::load_contents,
    mock_event_logging_adapter::MockEventLoggingAdapter,
    mock_log_provider::{MockLogProvider, RecordedLog},
    mock_observability_client::MockObservabilityClient,
    mock_scrapi::{Endpoint, EndpointStub, Method, MockScrapi, StubData},
};

const IDENTITY: &str = "shared-telemetry-instance";
const DIAGNOSTICS: &str = "statsig::diagnostics";

// Fork because the test-only exception endpoint is configured through the environment.
// The production telemetry control is per instance, including within each mixed case.
rusty_fork_test! {
    #[test]
    fn evaluation_client_preloads_preserve_local_observability() {
        run(async {
            for disabled in [Some(true), Some(false), None] {
                run_preload_case(disabled).await;
            }
        });
    }
    #[test]
    fn explicit_true_suppresses_remote_telemetry() {
        run(run_case(Some(true)));
    }
    #[test]
    fn explicit_false_preserves_remote_telemetry() {
        run(run_case(Some(false)));
    }
    #[test]
    fn unset_preserves_remote_telemetry() {
        run(run_case(None));
    }
    #[test]
    fn suppressed_without_observability_does_not_warn_about_unused_metrics() {
        run(run_without_observability());
    }
    #[test]
    fn suppressed_then_legacy_instances_with_shared_identity_are_isolated() {
        run(run_mixed_case(true));
    }
    #[test]
    fn legacy_then_suppressed_instances_with_shared_identity_are_isolated() {
        run(run_mixed_case(false));
    }
}

fn run(scenario: impl Future<Output = ()>) {
    tokio::runtime::Builder::new_multi_thread()
        .worker_threads(2)
        .enable_all()
        .build()
        .unwrap()
        .block_on(scenario);
}

struct Fixture {
    statsig: Statsig,
    server: MockScrapi,
    events: Arc<MockEventLoggingAdapter>,
    metrics: Arc<MockObservabilityClient>,
    logs: Arc<MockLogProvider>,
}

impl Fixture {
    async fn new(disabled: Option<bool>, observe: bool, config_status: u16) -> Self {
        let server = MockScrapi::new().await;
        let mut specs: Value = serde_json::from_str(&load_contents("eval_proj_dcs.json")).unwrap();
        specs.as_object_mut().unwrap().remove("checksum");
        // Full server sampling cannot override suppression and makes legacy assertions deterministic.
        for rate in specs["diagnostics"].as_object_mut().unwrap().values_mut() {
            *rate = json!(10000);
        }
        let list = load_contents("company_id_list");
        let manifest = json!({"company_id_list": {
            "name": "company_id_list", "size": list.len(),
            "url": server.url_for_endpoint(Endpoint::DownloadIdListFile),
            "creationTime": 1721417546000_u64, "fileID": "fixture"
        }});
        let config_body = if config_status == 200 {
            specs.to_string()
        } else {
            "{}".into()
        };
        for (endpoint, method, status, body) in [
            (
                Endpoint::DownloadConfigSpecs,
                Method::GET,
                config_status,
                config_body,
            ),
            (
                Endpoint::GetIdLists,
                Method::POST,
                200,
                manifest.to_string(),
            ),
            (Endpoint::DownloadIdListFile, Method::GET, 200, list),
            (Endpoint::SdkException, Method::POST, 200, "{}".into()),
        ] {
            server
                .stub(EndpointStub {
                    method,
                    status,
                    response: StubData::String(body),
                    ..EndpointStub::with_endpoint(endpoint)
                })
                .await;
        }
        // Each exception observer captures its endpoint before the next SDK is constructed.
        std::env::set_var(
            "STATSIG_SDK_EXCEPTION_URL",
            server.url_for_endpoint(Endpoint::SdkException),
        );
        let events = Arc::new(MockEventLoggingAdapter::new_with_background_flush(false));
        let metrics = Arc::new(MockObservabilityClient::new());
        let logs = Arc::new(MockLogProvider::new());
        let statsig = Statsig::new(
            "secret-shared-telemetry-key",
            Some(Arc::new(StatsigOptions {
                sdk_instance_id: Some(IDENTITY.into()),
                disable_remote_telemetry: disabled,
                specs_url: Some(server.url_for_endpoint(Endpoint::DownloadConfigSpecs)),
                specs_sync_interval_ms: Some(1000),
                enable_id_lists: Some(config_status == 200),
                id_lists_url: Some(server.url_for_endpoint(Endpoint::GetIdLists)),
                id_lists_sync_interval_ms: Some(1000),
                event_logging_adapter: Some(events.clone()),
                observability_client: observe
                    .then(|| Arc::downgrade(&metrics) as Weak<dyn ObservabilityClient>),
                output_logger_provider: Some(logs.clone()),
                output_log_level: Some(LogLevel::Debug),
                console_capture_options: Some(ConsoleCaptureOptions {
                    enabled: true,
                    ..Default::default()
                }),
                disable_country_lookup: Some(true),
                fallback_to_statsig_api: Some(false),
                ..Default::default()
            })),
        );
        Self {
            statsig,
            server,
            events,
            metrics,
            logs,
        }
    }

    fn event_names(&self) -> Vec<String> {
        // Inspect all payloads: the usual test helpers filter diagnostics.
        let mut names: Vec<_> = self
            .events
            .logged_payloads
            .lock()
            .unwrap()
            .iter()
            .flat_map(|payload| payload.events.as_array().unwrap())
            .map(|event| event["eventName"].as_str().unwrap().to_owned())
            .collect();
        names.sort();
        names
    }

    async fn await_event(&self, name: &str) {
        let deadline = Instant::now() + Duration::from_secs(5);
        loop {
            self.statsig.flush_events().await;
            if self.event_names().iter().any(|event| event == name) {
                return;
            }
            assert!(
                Instant::now() < deadline,
                "Expected event was not emitted: {name}"
            );
            tokio::time::sleep(Duration::from_millis(10)).await;
        }
    }

    fn network_errors(&self) -> Vec<String> {
        self.metrics
            .error_calls
            .lock()
            .unwrap()
            .iter()
            .filter(|(tag, _)| tag == "NetworkClient")
            .map(|(_, error)| error.clone())
            .collect()
    }

    fn exception_posts(&self) -> Vec<Value> {
        self.server
            .get_requests_for_endpoint(Endpoint::SdkException)
            .iter()
            .map(|request| serde_json::from_slice(&request.body).unwrap())
            .collect()
    }

    fn log_event(&self, name: &str) {
        self.statsig
            .log_event(&StatsigUser::with_user_id("test-user"), name, None, None);
    }
}

async fn run_case(disabled: Option<bool>) {
    let client = Fixture::new(disabled, true, 200).await;
    let suppressed = disabled == Some(true);
    let statsig = &client.statsig;
    let server = &client.server;
    statsig.initialize().await.unwrap();
    // Completed background operations prove local observability remains active.
    assert_eventually!(|| {
        let calls = client.metrics.dist_calls.lock().unwrap();
        let count = |metric| calls.iter().filter(|(name, _, _)| name == metric).count();
        count("statsig.sdk.config_sync_overall.latency") >= 1
            && count("statsig.sdk.id_lists_sync_overall.latency") >= 2
    });
    assert!(server.times_called_for_endpoint(Endpoint::DownloadConfigSpecs) >= 2);
    assert!(server.times_called_for_endpoint(Endpoint::DownloadIdListFile) >= 1);
    assert_eq!(client.metrics.init_called_times.load(Ordering::SeqCst), 1);
    let observers = statsig
        .statsig_runtime
        .get_running_task_ids()
        .iter()
        .filter(|(tag, _)| tag == "opts_stats_listen_for")
        .count();
    // Console capture and local observability remain; remote observers are skipped.
    assert_eq!(observers, if suppressed { 2 } else { 4 });
    if !suppressed {
        client.await_event(DIAGNOSTICS).await;
    }
    assert!(statsig.check_gate(&StatsigUser::with_user_id("test-user"), "test_public"));
    client.log_event("custom-event");
    statsig.shutdown().await.unwrap();
    let mut names = client.event_names();
    assert_eq!(names.iter().any(|name| name == DIAGNOSTICS), !suppressed);
    names.retain(|name| name != DIAGNOSTICS);
    assert_eq!(names, ["custom-event", "statsig::gate_exposure"]);
    let logs = client.logs.logs.lock();
    assert!(
        logs.iter()
            .any(|log| matches!(log, RecordedLog::Debug(_, _)))
    );
}

async fn run_without_observability() {
    let client = Fixture::new(Some(true), false, 200).await;
    client.statsig.initialize().await.unwrap();
    client.log_event("custom-event");
    client.statsig.flush_events().await;
    client.statsig.shutdown().await.unwrap();
    assert_eq!(client.event_names(), ["custom-event"]);
    let logs = client.logs.logs.lock();
    assert!(
        logs.iter()
            .any(|log| matches!(log, RecordedLog::Debug(_, _)))
    );
    assert!(!logs.iter().any(|log| matches!(log,
        RecordedLog::Warn(_, message) if message.contains("Dropping ops stats event")
    )));
}

async fn run_mixed_case(suppressed_first: bool) {
    // Failed initialization never receives remote sampling; configure its shared identity directly.
    let config = GlobalConfigs::get_instance(IDENTITY);
    config.set_diagnostics_sampling_rates(HashMap::from([("initialize".into(), 10000.0)]));
    let first = Fixture::new(Some(suppressed_first), true, 500).await;
    let second = Fixture::new(Some(!suppressed_first), true, 500).await;
    let (suppressed, legacy) = if suppressed_first {
        (&first, &second)
    } else {
        (&second, &first)
    };
    // Both SDKs exist before the suppressed failure: a shared queue must not upload its
    // error first and then hide the legacy error behind the uploader's deduplication.
    assert!(suppressed.statsig.initialize().await.is_err());
    assert_eventually!(|| !suppressed.network_errors().is_empty());
    assert!(legacy.statsig.initialize().await.is_err());
    assert_eventually!(|| !legacy.network_errors().is_empty());
    let legacy_url = legacy
        .server
        .url_for_endpoint(Endpoint::DownloadConfigSpecs);
    let suppressed_url = suppressed
        .server
        .url_for_endpoint(Endpoint::DownloadConfigSpecs);
    assert_eventually!(|| legacy.exception_posts().iter().any(|body| {
        body["tag"] == "NetworkClient"
            && body["info"]
                .as_str()
                .is_some_and(|info| info.contains(&legacy_url))
    }));
    legacy.await_event(DIAGNOSTICS).await;
    // Console capture deliberately retains the shared identity bus across both modes.
    CONSOLE_CAPTURE_REGISTRY.enqueue_console_capture_event(
        IDENTITY,
        "warn".into(),
        vec!["console capture remains active".into()],
        123,
        None,
    );
    for client in [suppressed, legacy] {
        client.await_event("statsig::log_line").await;
    }
    suppressed.log_event("suppressed-client-event");
    legacy.log_event("legacy-client-event");
    suppressed.statsig.shutdown().await.unwrap();
    legacy.statsig.shutdown().await.unwrap();
    assert_eq!(
        suppressed.event_names(),
        ["statsig::log_line", "suppressed-client-event"]
    );
    let legacy_events: Vec<_> = legacy
        .event_names()
        .into_iter()
        .filter(|name| name != DIAGNOSTICS)
        .collect();
    assert_eq!(legacy_events, ["legacy-client-event", "statsig::log_line"]);
    assert!(suppressed.exception_posts().is_empty());
    for client in [suppressed, legacy] {
        let own_url = client
            .server
            .url_for_endpoint(Endpoint::DownloadConfigSpecs);
        let errors = client.network_errors();
        assert!(errors.iter().all(|error| error.contains(&own_url)));
        assert_eq!(client.metrics.init_called_times.load(Ordering::SeqCst), 1);
        let counts = client.metrics.increment_calls.lock().unwrap();
        assert!(
            counts.iter().any(
                |(name, value, _)| name == "statsig.sdk.sdk_exceptions_count" && *value == 1.0
            )
        );
    }
    for body in legacy.exception_posts() {
        if body["tag"] == "NetworkClient" {
            let info = body["info"].as_str().unwrap();
            assert!(info.contains(&legacy_url));
            assert!(!info.contains(&suppressed_url));
        }
    }
}

async fn run_preload_case(disabled: Option<bool>) {
    let server = MockScrapi::new().await;
    let metrics = Arc::new(MockObservabilityClient::new());
    let client =
        EvaluationClient::new(tokio::runtime::Handle::current(), Some(metrics.clone())).unwrap();
    // A legacy uploader sharing the identity must not receive suppressed preload errors.
    std::env::set_var(
        "STATSIG_SDK_EXCEPTION_URL",
        server.url_for_endpoint(Endpoint::SdkException),
    );
    let legacy_metrics = Arc::new(MockObservabilityClient::new());
    let legacy = Statsig::new(
        "secret-legacy-preload",
        Some(Arc::new(StatsigOptions {
            sdk_instance_id: Some(client.id_lists_sdk_instance_id().to_string()),
            observability_client: Some(Arc::downgrade(&legacy_metrics) as _),
            event_logging_adapter: Some(Arc::new(
                MockEventLoggingAdapter::new_with_background_flush(false),
            )),
            disable_country_lookup: Some(true),
            ..Default::default()
        })),
    );
    server
        .stub(EndpointStub {
            method: Method::POST,
            response: StubData::String("{}".into()),
            ..EndpointStub::with_endpoint(Endpoint::GetIdLists)
        })
        .await;
    let options = StatsigOptions {
        disable_remote_telemetry: disabled,
        id_lists_url: Some(server.url_for_endpoint(Endpoint::GetIdLists)),
        id_lists_sync_interval_ms: Some(60_000),
        state_read_primary_attempts: Some(1),
        fallback_to_statsig_api: Some(false),
        disable_disk_access: Some(true),
        ..Default::default()
    };
    let first = client
        .preload_shared_id_lists("secret-owner", "tenant", &options)
        .await
        .unwrap();
    let repeated = client
        .preload_shared_id_lists("secret-owner", "tenant", &options)
        .await
        .unwrap();
    assert!(Arc::ptr_eq(&first, &repeated));
    assert_eq!(server.times_called_for_endpoint(Endpoint::GetIdLists), 1);
    let sync_count = || {
        metrics
            .dist_calls
            .lock()
            .unwrap()
            .iter()
            .filter(|(name, _, _)| name == "statsig.sdk.id_lists_sync_overall.latency")
            .count()
    };
    assert_eventually!(|| sync_count() == 1);

    server.clear_stubs().await;
    for (endpoint, status) in [(Endpoint::GetIdLists, 500), (Endpoint::SdkException, 200)] {
        server
            .stub(EndpointStub {
                method: Method::POST,
                status,
                response: StubData::String("{}".into()),
                ..EndpointStub::with_endpoint(endpoint)
            })
            .await;
    }
    for key in ["secret-failed-owner-one", "secret-failed-owner-two"] {
        assert!(
            client
                .preload_shared_id_lists(key, "tenant", &options)
                .await
                .is_err()
        );
    }
    assert_eventually!(|| metrics.error_calls.lock().unwrap().len() >= 2);
    assert_eventually!(|| sync_count() >= 3);
    // Delivery of the final latency event drains preceding error callbacks on this bus.
    assert_eq!(metrics.error_calls.lock().unwrap().len(), 2);
    assert_eq!(
        metrics
            .increment_calls
            .lock()
            .unwrap()
            .iter()
            .filter(|(name, _, _)| { name == "statsig.sdk.sdk_exceptions_count" })
            .count(),
        2
    );
    assert_eq!(sync_count(), 3);
    if disabled == Some(true) {
        assert!(legacy_metrics.error_calls.lock().unwrap().is_empty());
        assert_eq!(server.times_called_for_endpoint(Endpoint::SdkException), 0);
    } else {
        assert_eventually!(|| server.times_called_for_endpoint(Endpoint::SdkException) > 0);
    }
    client.shutdown().await;
    assert!(
        client
            .preload_shared_id_lists(
                "secret-after-shutdown",
                "tenant",
                &StatsigOptions {
                    disable_remote_telemetry: Some(true),
                    ..options
                }
            )
            .await
            .is_err()
    );
    assert_eq!(server.times_called_for_endpoint(Endpoint::GetIdLists), 3);
    legacy.shutdown().await.unwrap();
}
