use super::*;
use crate::networking::{NetworkProvider, Response};
use parking_lot::Mutex;
use std::io::{self, Read, Seek, SeekFrom};
use std::sync::atomic::{AtomicU16, AtomicUsize};

#[derive(Debug)]
struct BrokenReader;
impl Read for BrokenReader {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        Err(io::Error::new(
            io::ErrorKind::ConnectionReset,
            "body reader reset",
        ))
    }
}
impl Seek for BrokenReader {
    fn seek(&mut self, _: SeekFrom) -> io::Result<u64> {
        Ok(0)
    }
}

struct ReaderProvider {
    specs: AtomicUsize,
    blobs: AtomicUsize,
    encoding: Option<&'static str>,
    body: Vec<u8>,
    failed_specs_attempts: usize,
    transport_failures: usize,
    transport_body_error: bool,
}
#[async_trait]
impl NetworkProvider for ReaderProvider {
    async fn send(&self, _: &HttpMethod, args: &RequestArgs) -> Response {
        assert_eq!(args.retries, 0);
        let blob = args.url.contains("dynamic_config_value");
        let fail = if blob {
            self.blobs.fetch_add(1, Ordering::SeqCst);
            true
        } else {
            let index = self.specs.fetch_add(1, Ordering::SeqCst);
            if index < self.transport_failures {
                return Response {
                    status_code: Some(503),
                    data: None,
                    error: Some("unavailable".into()),
                };
            }
            index < self.failed_specs_attempts
        };
        if fail && self.transport_body_error {
            return Response {
                status_code: Some(200),
                data: None,
                error: Some("body reader reset".into()),
            };
        }
        let mut headers = HashMap::from([("content-type".into(), "application/json".into())]);
        if let Some(encoding) = self.encoding {
            headers.insert("content-type".into(), "application/octet-stream".into());
            headers.insert("content-encoding".into(), encoding.into());
        }
        let data = if fail {
            ResponseData::from_stream_with_headers(Box::new(BrokenReader), Some(headers))
        } else {
            ResponseData::from_bytes_with_headers(self.body.clone(), Some(headers))
        };
        Response {
            status_code: Some(200),
            data: Some(data),
            error: None,
        }
    }
    async fn send_with_response_limit(
        &self,
        method: &HttpMethod,
        args: &RequestArgs,
        _: u64,
    ) -> crate::networking::ResponseLimitOutcome {
        crate::networking::ResponseLimitOutcome::Response(self.send(method, args).await)
    }
}

fn real_store_adapter(provider: &Arc<ReaderProvider>) -> StatsigHttpSpecsAdapter {
    let (mut adapter, _, _) = setup(false);
    let sdk_key = format!("secret-reader-{:p}", Arc::as_ptr(provider));
    adapter.ops_stats = OPS_STATS.get_for_instance(&sdk_key);
    let mut network = NetworkClient::new(&sdk_key, None, None);
    let net_provider: Arc<dyn NetworkProvider> = provider.clone();
    network.set_network_provider_for_test(Arc::downgrade(&net_provider));
    adapter.network = Arc::new(network);
    adapter.remote_config_value_hydrator = Arc::new(RemoteConfigValueHydrator::new_with_ops_stats(
        adapter.network.clone(),
        adapter.ops_stats.clone(),
    ));
    adapter.initialize(Arc::new(crate::spec_store::SpecStore::new(
        "secret-reader",
        "reader-test".into(),
        StatsigRuntime::get_runtime(),
        Arc::new(crate::sdk_event_emitter::SdkEventEmitter::default()),
        None,
    )));
    adapter
}

#[tokio::test(start_paused = true)]
async fn exhausted_hydration_reader_does_not_restart_specs_budget() {
    let sha = "0".repeat(64);
    let body = serde_json::to_vec(&serde_json::json!({"has_updates":true,"time":1,"dynamic_configs":{"remote": {
        "defaultValue": format!("https://proxy.test/v1/dynamic_config_value/{sha}"),
        "remoteConfigMetadata": {"sha256":sha,"byteLength":2,"contentType":"application/json","compression":"none"}, "rules":[]
    }}})).unwrap();
    let provider = Arc::new(ReaderProvider {
        specs: AtomicUsize::new(0),
        blobs: AtomicUsize::new(0),
        encoding: None,
        body,
        failed_specs_attempts: 0,
        transport_failures: 0,
        transport_body_error: false,
    });
    let adapter = real_store_adapter(&provider);
    let error = adapter
        .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
        .await
        .unwrap_err();
    assert!(error.to_string().contains("body_read_failed"), "{error}");
    assert_eq!(provider.specs.load(Ordering::SeqCst), 1);
    assert_eq!(provider.blobs.load(Ordering::SeqCst), 3);
}

#[tokio::test(start_paused = true)]
async fn real_store_retries_body_io_but_not_invalid_compression() {
    for encoding in [None, Some("statsig-br"), Some("statsig-zstd")] {
        let body = match encoding {
            None => include_bytes!("../../../tests/data/eval_proj_dcs.json").to_vec(),
            Some("statsig-br") => {
                include_bytes!("../../../tests/data/eval_proj_dcs.pb.br").to_vec()
            }
            Some(_) => {
                let mut decoded = Vec::new();
                brotli::Decompressor::new(
                    include_bytes!("../../../tests/data/eval_proj_dcs.pb.br").as_slice(),
                    4096,
                )
                .read_to_end(&mut decoded)
                .unwrap();
                zstd::stream::encode_all(decoded.as_slice(), 3).unwrap()
            }
        };
        let provider = Arc::new(ReaderProvider {
            specs: AtomicUsize::new(0),
            blobs: AtomicUsize::new(0),
            encoding,
            body,
            failed_specs_attempts: 1,
            transport_failures: 0,
            transport_body_error: false,
        });
        let adapter = real_store_adapter(&provider);
        adapter
            .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
            .await
            .unwrap();
        assert_eq!(provider.specs.load(Ordering::SeqCst), 2, "{encoding:?}");
        let malformed = Arc::new(ReaderProvider {
            specs: AtomicUsize::new(0),
            blobs: AtomicUsize::new(0),
            encoding,
            body: b"invalid".to_vec(),
            failed_specs_attempts: 0,
            transport_failures: 0,
            transport_body_error: false,
        });
        let adapter = real_store_adapter(&malformed);
        assert!(
            adapter
                .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
                .await
                .is_err()
        );
        assert_eq!(malformed.specs.load(Ordering::SeqCst), 1);
    }
}

struct Provider {
    calls: Mutex<Vec<RequestArgs>>,
    status: AtomicU16,
    body: Mutex<Vec<u8>>,
}
#[async_trait]
impl NetworkProvider for Provider {
    async fn send(&self, _: &HttpMethod, args: &RequestArgs) -> Response {
        self.calls.lock().push(args.clone());
        Response {
            status_code: Some(if args.url.contains("proxy.test") {
                self.status.load(Ordering::SeqCst)
            } else {
                200
            }),
            data: Some(ResponseData::from_bytes(self.body.lock().clone())),
            error: None,
        }
    }
}

struct Listener {
    updates: AtomicUsize,
    fail_checksum_once: AtomicBool,
}
impl SpecsUpdateListener for Listener {
    fn did_receive_specs_update(&self, mut update: SpecsUpdate) -> Result<(), StatsigErr> {
        update.data.deserialize_into::<serde_json::Value>()?;
        self.updates.fetch_add(1, Ordering::SeqCst);
        if self.fail_checksum_once.swap(false, Ordering::SeqCst) {
            Err(StatsigErr::ChecksumFailure("bad delta".into()))
        } else {
            Ok(())
        }
    }
    fn get_current_specs_info(&self) -> SpecsInfo {
        SpecsInfo::empty()
    }
}

fn setup(deltas: bool) -> (StatsigHttpSpecsAdapter, Arc<Provider>, Arc<Listener>) {
    setup_with_attempts(deltas, None)
}

fn setup_with_attempts(
    deltas: bool,
    attempts: Option<i64>,
) -> (StatsigHttpSpecsAdapter, Arc<Provider>, Arc<Listener>) {
    static NEXT_KEY: AtomicUsize = AtomicUsize::new(0);
    let sdk_key = format!(
        "secret-retry-test-{}",
        NEXT_KEY.fetch_add(1, Ordering::SeqCst)
    );
    let provider = Arc::new(Provider {
        calls: Mutex::new(Vec::new()),
        status: AtomicU16::new(503),
        body: Mutex::new(br#"{"has_updates":false}"#.to_vec()),
    });
    let mut adapter = StatsigHttpSpecsAdapter::new(
        &sdk_key,
        Some(&StatsigOptions {
            specs_url: Some("https://proxy.test".into()),
            fallback_to_statsig_api: Some(true),
            enable_dcs_deltas: Some(deltas),
            state_read_primary_attempts: attempts,
            ..Default::default()
        }),
        None,
    );
    // Replace both network owners so hydration uses the same deterministic provider.
    let mut network = NetworkClient::new(&sdk_key, None, None);
    let net_provider: Arc<dyn NetworkProvider> = provider.clone();
    network.set_network_provider_for_test(Arc::downgrade(&net_provider));
    adapter.network = Arc::new(network);
    adapter.remote_config_value_hydrator = Arc::new(RemoteConfigValueHydrator::new_with_ops_stats(
        adapter.network.clone(),
        adapter.ops_stats.clone(),
    ));
    let listener = Arc::new(Listener {
        updates: AtomicUsize::new(0),
        fail_checksum_once: AtomicBool::new(false),
    });
    adapter.initialize(listener.clone());
    (adapter, provider, listener)
}

#[tokio::test(start_paused = true)]
async fn specs_cadence_starts_each_refresh_at_primary_and_fallback_does_not_reset() {
    let (adapter, provider, listener) = setup(false);
    for n in 1..=10 {
        provider.calls.lock().clear();
        assert_eq!(
            adapter
                .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Background)
                .await
                .is_ok(),
            n % 5 == 0
        );
        let calls = provider.calls.lock();
        assert_eq!(calls.len(), if n % 5 == 0 { 5 } else { 4 });
        assert!(
            calls[..4]
                .iter()
                .all(|r| r.url.contains("proxy.test") && r.retries == 0)
        );
        if n % 5 == 0 {
            assert!(!calls[4].url.contains("proxy.test"));
        }
    }
    assert_eq!(listener.updates.load(Ordering::SeqCst), 2);
    for status in [400, 401, 403, 405, 413, 429, 501] {
        provider.status.store(status, Ordering::SeqCst);
        provider.calls.lock().clear();
        assert!(
            adapter
                .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
                .await
                .is_err()
        );
        assert_eq!(provider.calls.lock().len(), 1);
    }
}

#[tokio::test(start_paused = true)]
async fn checksum_recovery_spends_remaining_budget_at_primary() {
    let (adapter, provider, listener) = setup(true);
    provider.status.store(200, Ordering::SeqCst);
    listener.fail_checksum_once.store(true, Ordering::SeqCst);
    adapter
        .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
        .await
        .unwrap();
    let calls = provider.calls.lock();
    assert_eq!(calls.len(), 2);
    assert!(calls[0].deltas_enabled);
    assert!(!calls[1].deltas_enabled);
    assert!(calls.iter().all(|r| r.url.contains("proxy.test")));
}

#[tokio::test(start_paused = true)]
async fn invalid_payload_is_terminal_and_manual_fetch_has_no_publication_or_fallback() {
    let (adapter, provider, listener) = setup(false);
    provider.status.store(200, Ordering::SeqCst);
    *provider.body.lock() = b"invalid".to_vec();
    assert!(
        adapter
            .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
            .await
            .is_err()
    );
    assert_eq!(provider.calls.lock().len(), 1);
    assert_eq!(listener.updates.load(Ordering::SeqCst), 0);
    provider.status.store(503, Ordering::SeqCst);
    provider.calls.lock().clear();
    assert!(
        adapter
            .fetch_specs_from_network(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
            .await
            .is_err()
    );
    assert_eq!(provider.calls.lock().len(), 2);
    assert_eq!(listener.updates.load(Ordering::SeqCst), 0);
}

fn assert_failed_sync_delta_metric(
    receiver: &mut tokio::sync::broadcast::Receiver<crate::observability::ops_stats::OpsStatsEvent>,
    requested_deltas: bool,
) {
    use crate::observability::ops_stats::OpsStatsEvent;

    while let Ok(event) = receiver.try_recv() {
        let OpsStatsEvent::Observability(event) = event else {
            continue;
        };
        if event.metric_name == "config_sync_overall.latency" {
            let tags = event.tags.unwrap();
            assert_eq!(tags["deltas_used"], requested_deltas.to_string());
            assert_eq!(tags["network_success"], "false");
            assert_eq!(tags["process_success"], "false");
            assert_eq!(
                tags["source_api"],
                api_from_url(&config_specs_url("https://proxy.test"))
            );
            return;
        }
    }
    panic!("missing config_sync_overall.latency metric");
}

#[tokio::test(start_paused = true)]
async fn failed_sync_metrics_preserve_requested_deltas() {
    for requested_deltas in [true, false] {
        let (mut adapter, provider, _) = setup(requested_deltas);
        adapter.ops_stats = Arc::new(OpsStatsForInstance::new());
        let mut receiver = adapter.ops_stats.subscribe_for_test();
        assert!(
            adapter
                .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Background)
                .await
                .is_err()
        );
        let calls = provider.calls.lock();
        assert_eq!(calls.len(), 4);
        assert!(
            calls
                .iter()
                .all(|args| args.deltas_enabled == requested_deltas)
        );
        assert_failed_sync_delta_metric(&mut receiver, requested_deltas);
    }
}

#[tokio::test(start_paused = true)]
async fn failed_sync_metrics_use_full_request_after_checksum_recovery() {
    struct ChecksumFailureListener(Arc<Provider>);
    impl SpecsUpdateListener for ChecksumFailureListener {
        fn did_receive_specs_update(&self, _: SpecsUpdate) -> Result<(), StatsigErr> {
            self.0.status.store(503, Ordering::SeqCst);
            Err(StatsigErr::ChecksumFailure("bad delta".into()))
        }
        fn get_current_specs_info(&self) -> SpecsInfo {
            SpecsInfo::empty()
        }
    }

    let (mut adapter, provider, _) = setup(true);
    provider.status.store(200, Ordering::SeqCst);
    adapter.initialize(Arc::new(ChecksumFailureListener(provider.clone())));
    adapter.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut receiver = adapter.ops_stats.subscribe_for_test();
    assert!(
        adapter
            .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Background)
            .await
            .is_err()
    );
    let calls = provider.calls.lock();
    assert_eq!(calls.len(), 4);
    assert!(calls[0].deltas_enabled);
    assert!(calls[1..].iter().all(|args| !args.deltas_enabled));
    assert_failed_sync_delta_metric(&mut receiver, false);
}

#[tokio::test(start_paused = true)]
async fn body_read_failures_get_one_retry_and_keep_background_fallback_cadence() {
    for (transport_body_error, transport_failures) in [(false, 0), (true, 0), (false, 2), (true, 2)]
    {
        let provider = Arc::new(ReaderProvider {
            specs: AtomicUsize::new(0),
            blobs: AtomicUsize::new(0),
            encoding: None,
            body: Vec::new(),
            failed_specs_attempts: usize::MAX,
            transport_body_error,
            transport_failures,
        });
        let adapter = real_store_adapter(&provider);
        let primary = if transport_failures == 0 { 2 } else { 3 };
        for refresh in 1..=5 {
            provider.specs.store(0, Ordering::SeqCst);
            let mut events = adapter.ops_stats.subscribe_for_test();
            let result = adapter
                .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Background)
                .await;
            assert!(result.is_err());
            let count = primary + usize::from(refresh == 5);
            assert_eq!(provider.specs.load(Ordering::SeqCst), count);
            if transport_body_error {
                assert!(
                    matches!(result, Err(StatsigErr::NetworkError(NetworkError::RetriesExhausted(_, Some(200), attempts, _))) if attempts as usize == count)
                );
            }
            let mut indices = Vec::new();
            while let Ok(event) = events.try_recv() {
                if let crate::observability::ops_stats::OpsStatsEvent::Diagnostics(event) = event {
                    if let Some(marker) = event.marker {
                        let marker = serde_json::to_value(marker).unwrap();
                        if marker["step"] == "network_request" && marker["action"] == "start" {
                            indices.push(marker["attempt"].as_u64().unwrap());
                        }
                    }
                }
            }
            assert_eq!(indices, (0..count as u64).collect::<Vec<_>>());
        }
        provider.specs.store(0, Ordering::SeqCst);
        assert!(
            adapter
                .fetch_hydrated_specs_from_network(SpecsInfo::empty(), SpecsSyncTrigger::Background)
                .await
                .is_err()
        );
        assert_eq!(provider.specs.load(Ordering::SeqCst), primary);
        if transport_body_error {
            provider.specs.store(0, Ordering::SeqCst);
            assert!(
                adapter
                    .fetch_specs_from_network(SpecsInfo::empty(), SpecsSyncTrigger::Background)
                    .await
                    .is_err()
            );
            assert_eq!(provider.specs.load(Ordering::SeqCst), primary);
        }
    }
}

#[tokio::test(start_paused = true)]
async fn configured_primary_budget_controls_manual_reads_and_background_fallback() {
    for (attempts, foreground, background) in [
        (None, 2, 4),
        (Some(0), 2, 4),
        (Some(-1), 2, 4),
        (Some(4294967296), 2, 4),
        (Some(1), 1, 1),
        (Some(2), 2, 2),
    ] {
        let (adapter, provider, _) = setup_with_attempts(false, attempts);
        assert!(
            adapter
                .fetch_specs_from_network(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
                .await
                .is_err()
        );
        assert_eq!(provider.calls.lock().len(), foreground);
        for refresh in 1..=10 {
            provider.calls.lock().clear();
            let mut events = adapter.ops_stats.subscribe_for_test();
            let result = adapter
                .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Background)
                .await;
            assert_eq!(result.is_ok(), refresh % 5 == 0);
            let calls = provider.calls.lock();
            assert_eq!(calls.len(), background + usize::from(refresh % 5 == 0));
            assert!(calls.iter().all(|call| call.retries == 0));
            let mut indices = Vec::new();
            while let Ok(event) = events.try_recv() {
                if let crate::observability::ops_stats::OpsStatsEvent::Diagnostics(event) = event {
                    if let Some(marker) = event.marker {
                        let marker = serde_json::to_value(marker).unwrap();
                        if marker["step"] == "network_request" && marker["action"] == "start" {
                            indices.push(marker["attempt"].as_u64().unwrap());
                        }
                    }
                }
            }
            assert_eq!(indices, (0..calls.len() as u64).collect::<Vec<_>>());
        }
    }
}

#[tokio::test(start_paused = true)]
async fn checksum_recovery_cannot_restart_configured_primary_budget() {
    for attempts in [1, 2] {
        let (adapter, provider, listener) = setup_with_attempts(true, Some(attempts));
        provider.status.store(200, Ordering::SeqCst);
        listener.fail_checksum_once.store(true, Ordering::SeqCst);
        let result = adapter
            .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Background)
            .await;
        assert_eq!(result.is_ok(), attempts == 2);
        let calls = provider.calls.lock();
        assert_eq!(calls.len(), attempts as usize);
        assert!(calls[0].deltas_enabled);
        if attempts == 2 {
            assert!(!calls[1].deltas_enabled);
        }
    }
}

#[tokio::test]
async fn maximum_fallback_index_reports_error_without_overflow() {
    let (adapter, _provider, _) = setup(false);
    let error = adapter
        .network
        .request_once(
            HttpMethod::GET,
            RequestArgs {
                url: "https://proxy.test".into(),
                retries: u32::MAX - 1,
                ..RequestArgs::new()
            },
            None,
            false,
            true,
            u32::MAX,
        )
        .await
        .err()
        .unwrap();
    assert!(matches!(
        error,
        NetworkError::RetriesExhausted(_, _, u32::MAX, _)
    ));
}

#[tokio::test(start_paused = true)]
async fn explicit_budget_overrides_specs_body_read_default_ceiling() {
    for transport_body_error in [false, true] {
        let provider = Arc::new(ReaderProvider {
            specs: AtomicUsize::new(0),
            blobs: AtomicUsize::new(0),
            encoding: None,
            body: Vec::new(),
            failed_specs_attempts: usize::MAX,
            transport_failures: 0,
            transport_body_error,
        });
        let mut adapter = real_store_adapter(&provider);
        // Use policies captured by the public-option constructor with this deterministic provider.
        let configured = StatsigHttpSpecsAdapter::new(
            "secret-body-budget",
            Some(&StatsigOptions {
                state_read_primary_attempts: Some(3),
                ..Default::default()
            }),
            None,
        );
        adapter.foreground_retry_policy = configured.foreground_retry_policy;
        adapter.background_retry_policy = configured.background_retry_policy;
        assert!(
            adapter
                .manually_sync_specs(SpecsInfo::empty(), SpecsSyncTrigger::Background)
                .await
                .is_err()
        );
        assert_eq!(provider.specs.load(Ordering::SeqCst), 3);
    }
}
