use super::*;
use crate::sdk_event_emitter::SdkEventEmitter;
use std::io::{self, Cursor, Read, Seek, SeekFrom};
use std::sync::atomic::AtomicUsize;

#[derive(Debug)]
struct CountedReader {
    cursor: Cursor<Vec<u8>>,
    bytes: Arc<AtomicUsize>,
}

impl Read for CountedReader {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        let count = self.cursor.read(buf)?;
        self.bytes.fetch_add(count, Ordering::Relaxed);
        Ok(count)
    }
}

impl Seek for CountedReader {
    fn seek(&mut self, position: SeekFrom) -> io::Result<u64> {
        self.cursor.seek(position)
    }
}

fn full(has_updates: bool, time: u64) -> Vec<u8> {
    format!(
        r#"{{"feature_gates":{{}},"dynamic_configs":{{}},"layer_configs":{{}},"condition_map":{{}},"experiment_to_layer":{{}},"has_updates":{has_updates},"time":{time}}}"#
    )
    .into_bytes()
}

fn store() -> Arc<SpecStore> {
    Arc::new(SpecStore::new(
        "response-metrics-reuse",
        "response-metrics-reuse".to_owned(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    ))
}

fn update(data: ResponseData) -> SpecsUpdate {
    SpecsUpdate {
        data,
        source: SpecsSource::Network,
        received_at: 0,
        source_api: None,
        has_updates: None,
    }
}

async fn process(
    body: &[u8],
    headers: HashMap<String, String>,
    native: bool,
    prior_time: Option<u64>,
) -> (Result<(), StatsigErr>, &'static str, usize, u64) {
    let store = store();
    if let Some(time) = prior_time {
        store
            .set_values(update(ResponseData::from_bytes(full(true, time))))
            .unwrap();
    }
    let adapter = StatsigHttpSpecsAdapter::new("response-metrics-reuse", None, None);
    if native {
        adapter.initialize_spec_store(store.clone());
    } else {
        adapter.initialize(store.clone());
    }
    let bytes = Arc::new(AtomicUsize::new(0));
    let data = ResponseData::from_stream_with_headers(
        Box::new(CountedReader {
            cursor: Cursor::new(body.to_vec()),
            bytes: bytes.clone(),
        }),
        Some(headers),
    );
    let metrics = parking_lot::Mutex::new(Some(ConfigSyncMetrics::from_response_headers(
        &data, "test", false,
    )));
    assert_eq!(bytes.load(Ordering::Relaxed), 0);
    let result = adapter
        .process_spec_data_with_metrics(
            SpecsSyncTrigger::Initial,
            Ok(NetworkResponse {
                data,
                loggable_api: "test".to_owned(),
                requested_deltas: false,
                request_url: "https://api.statsig.com/v1/download_config_specs/test.json"
                    .to_owned(),
            }),
            Some(&metrics),
        )
        .await;
    (
        result,
        metrics.into_inner().unwrap().response_type.as_str(),
        bytes.load(Ordering::Relaxed),
        store.get_current_specs_info().lcut.unwrap_or(0),
    )
}

#[tokio::test]
async fn native_full_response_avoids_one_body_scan() {
    let mut body = full(true, 2);
    body.pop();
    body.extend_from_slice(format!(",\"unknown\":\"{}\"}}", "a".repeat(16_384)).as_bytes());
    for prior_time in [None, Some(3)] {
        let legacy = process(&body, HashMap::new(), false, prior_time).await;
        let native = process(&body, HashMap::new(), true, prior_time).await;
        assert!(legacy.0.is_ok());
        assert!(native.0.is_ok());
        assert_eq!(native.1, "full");
        assert_eq!(native.1, legacy.1);
        assert_eq!(native.3, legacy.3);
        assert_eq!(legacy.2 - native.2, body.len());
    }
}

#[tokio::test]
async fn native_no_update_and_malformed_classification_matches_legacy() {
    let mut trailing_true = full(true, 1);
    trailing_true.extend_from_slice(b" trailing");
    let mut trailing_false = full(false, 1);
    trailing_false.extend_from_slice(b" trailing");
    let cases = [
        (b"{\"has_updates\":false}".to_vec(), "no_update"),
        (
            b"{\"has_updates\":false,\"time\":\"bad\"}".to_vec(),
            "no_update",
        ),
        (b"{\"has_updates\":true}".to_vec(), "full"),
        (
            b"{\"has_updates\":false,\"has_updates\":true}".to_vec(),
            "full",
        ),
        (b"{\"has_updates\":false} trailing".to_vec(), "full"),
        (b"{\"has_updates\":false,\"unknown\":[}".to_vec(), "full"),
        (b"{\"has_updates\":\"false\"}".to_vec(), "full"),
        (vec![0xff], "full"),
        (full(false, 1), "no_update"),
        (trailing_true, "full"),
        (trailing_false, "full"),
    ];
    for (body, expected) in cases {
        for prior_time in [None, Some(2)] {
            let legacy = process(&body, HashMap::new(), false, prior_time).await;
            let native = process(&body, HashMap::new(), true, prior_time).await;
            assert_eq!(native.1, expected, "{body:?}, {prior_time:?}");
            assert_eq!(native.1, legacy.1);
            assert_eq!(native.0.is_ok(), legacy.0.is_ok(), "{body:?}");
            assert_eq!(
                native.0.err().map(|e| e.to_string()),
                legacy.0.err().map(|e| e.to_string())
            );
            assert_eq!(native.3, legacy.3);
        }
    }
}

#[tokio::test]
async fn native_no_update_reuses_existing_strict_fallback() {
    let body = b"{\"has_updates\":false}";
    let legacy = process(body, HashMap::new(), false, None).await;
    let native = process(body, HashMap::new(), true, None).await;
    assert!(native.0.is_ok());
    assert_eq!(native.1, "no_update");
    assert_eq!(legacy.2 - native.2, body.len());
}

#[tokio::test]
async fn header_classification_keeps_precedence_and_does_not_add_reads() {
    for (headers, expected) in [
        (
            HashMap::from([("x-deltas-used".to_owned(), "false".to_owned())]),
            "delta",
        ),
        (
            HashMap::from([
                ("x-cache-hit".to_owned(), "TrUe".to_owned()),
                ("x-deltas-used".to_owned(), "true".to_owned()),
            ]),
            "no_update",
        ),
    ] {
        let body = full(true, 1);
        let legacy = process(&body, headers.clone(), false, None).await;
        let native = process(&body, headers, true, None).await;
        assert!(native.0.is_ok());
        assert_eq!(native.1, expected);
        assert_eq!(native.1, legacy.1);
        assert_eq!(native.2, legacy.2);
    }
}

struct RetainingListener(parking_lot::Mutex<Option<SpecsUpdate>>);

#[async_trait]
impl SpecsUpdateListener for RetainingListener {
    fn did_receive_specs_update(&self, _: SpecsUpdate) -> Result<(), StatsigErr> {
        unreachable!()
    }

    async fn did_receive_specs_update_async(
        &self,
        update: SpecsUpdate,
        _: Option<SpecsUpdateHydration>,
    ) -> Result<(), StatsigErr> {
        *self.0.lock() = Some(update);
        Err(StatsigErr::InvalidOperation(
            "custom listener error".to_owned(),
        ))
    }

    fn get_current_specs_info(&self) -> SpecsInfo {
        SpecsInfo::empty()
    }
}

#[tokio::test]
async fn custom_async_listener_keeps_original_response_and_error_classification() {
    let listener = Arc::new(RetainingListener(parking_lot::Mutex::new(None)));
    let adapter = StatsigHttpSpecsAdapter::new("custom-metrics-reuse", None, None);
    adapter.initialize(listener.clone());
    let body = b"{\"has_updates\":false}";
    let data = ResponseData::from_bytes(body.to_vec());
    let metrics = parking_lot::Mutex::new(Some(ConfigSyncMetrics::from_response_headers(
        &data, "test", false,
    )));
    let result = adapter
        .process_spec_data_with_metrics(
            SpecsSyncTrigger::Initial,
            Ok(NetworkResponse {
                data,
                loggable_api: "test".to_owned(),
                requested_deltas: false,
                request_url: "https://api.statsig.com/v1/download_config_specs/test.json"
                    .to_owned(),
            }),
            Some(&metrics),
        )
        .await;
    assert!(matches!(result, Err(StatsigErr::InvalidOperation(_))));
    assert_eq!(
        metrics.into_inner().unwrap().response_type.as_str(),
        "no_update"
    );
    let mut retained = listener.0.lock().take().unwrap();
    let mut received = Vec::new();
    retained
        .data
        .get_stream_mut()
        .read_to_end(&mut received)
        .unwrap();
    assert_eq!(received, body);
}

struct EmptyReadOnlyDataStore;

#[async_trait]
impl crate::data_store_interface::DataStoreTrait for EmptyReadOnlyDataStore {
    fn is_read_only(&self) -> bool {
        true
    }
    async fn initialize(&self) -> Result<(), StatsigErr> {
        Ok(())
    }
    async fn shutdown(&self) -> Result<(), StatsigErr> {
        Ok(())
    }
    async fn get(
        &self,
        _: &str,
    ) -> Result<crate::data_store_interface::DataStoreResponse, StatsigErr> {
        Ok(crate::data_store_interface::DataStoreResponse {
            result: None,
            time: None,
            checksum: None,
            has_updates: None,
        })
    }
    async fn set(&self, _: &str, _: &str, _: Option<u64>) -> Result<(), StatsigErr> {
        panic!("read-only datastore must not receive writes")
    }
    async fn support_polling_updates_for(
        &self,
        _: crate::data_store_interface::RequestPath,
    ) -> bool {
        false
    }
}

#[tokio::test]
async fn sdk_initialization_reuses_decode_for_owned_http_compositions() {
    for (configured, data_store) in [(false, false), (true, false), (false, true), (true, true)] {
        let mut server = mockito::Server::new_async().await;
        let mut failing = mockito::Server::new_async().await;
        let success = server
            .mock("GET", mockito::Matcher::Any)
            .with_status(200)
            .with_body(full(true, 1))
            .expect(1)
            .create_async()
            .await;
        let failed = failing
            .mock("GET", mockito::Matcher::Any)
            .with_status(503)
            .expect(if configured { 2 } else { 0 })
            .create_async()
            .await;
        let options = StatsigOptions {
            specs_url: Some(server.url()),
            disable_all_logging: Some(true),
            fallback_to_statsig_api: Some(false),
            data_store: data_store.then(|| {
                Arc::new(EmptyReadOnlyDataStore)
                    as Arc<dyn crate::data_store_interface::DataStoreTrait>
            }),
            spec_adapters_config: configured.then(|| {
                [failing.url(), server.url()]
                    .into_iter()
                    .map(|url| crate::SpecAdapterConfig {
                        adapter_type: crate::SpecsAdapterType::NetworkHttp,
                        init_timeout_ms: 3000,
                        specs_url: Some(url),
                        authentication_mode: None,
                        ca_cert_path: None,
                        client_cert_path: None,
                        client_key_path: None,
                        domain_name: None,
                    })
                    .collect()
            }),
            ..StatsigOptions::default()
        };
        let statsig = crate::Statsig::new("secret-metrics-composition", Some(Arc::new(options)));
        statsig.initialize().await.unwrap();
        success.assert_async().await;
        failed.assert_async().await;
        statsig.shutdown().await.unwrap();
    }
}

struct PendingListener;

#[async_trait]
impl SpecsUpdateListener for PendingListener {
    fn did_receive_specs_update(&self, _: SpecsUpdate) -> Result<(), StatsigErr> {
        unreachable!()
    }
    async fn did_receive_specs_update_async(
        &self,
        _: SpecsUpdate,
        _: Option<SpecsUpdateHydration>,
    ) -> Result<(), StatsigErr> {
        std::future::pending().await
    }
    fn get_current_specs_info(&self) -> SpecsInfo {
        SpecsInfo::empty()
    }
}

#[tokio::test(start_paused = true)]
async fn cancelled_custom_listener_keeps_response_classification() {
    let adapter = StatsigHttpSpecsAdapter::new("cancelled-custom-metrics", None, None);
    adapter.initialize(Arc::new(PendingListener));
    let data = ResponseData::from_bytes(b"{\"has_updates\":false}".to_vec());
    let metrics = parking_lot::Mutex::new(Some(ConfigSyncMetrics::from_response_headers(
        &data, "test", false,
    )));
    assert!(
        tokio::time::timeout(
            Duration::from_millis(1),
            adapter.process_spec_data_with_metrics(
                SpecsSyncTrigger::Initial,
                Ok(NetworkResponse {
                    data,
                    loggable_api: "test".to_owned(),
                    requested_deltas: false,
                    request_url: "https://api.statsig.com/v1/download_config_specs/test.json"
                        .to_owned(),
                }),
                Some(&metrics)
            )
        )
        .await
        .is_err()
    );
    assert_eq!(
        metrics.into_inner().unwrap().response_type.as_str(),
        "no_update"
    );
}

struct PendingDownload(AtomicBool);

#[async_trait]
impl crate::networking::NetworkProvider for PendingDownload {
    async fn send(&self, _: &HttpMethod, _: &RequestArgs) -> crate::networking::Response {
        unreachable!()
    }
    async fn send_with_response_limit(
        &self,
        _: &HttpMethod,
        _: &RequestArgs,
        _: u64,
    ) -> crate::networking::ResponseLimitOutcome {
        self.0.store(true, Ordering::Relaxed);
        std::future::pending().await
    }
}

#[tokio::test(start_paused = true)]
async fn cancelled_remote_download_keeps_original_no_update_and_duplicate_metrics() {
    for duplicate in [false, true] {
        for native in [false, true] {
            let options = StatsigOptions {
                specs_url: Some("https://proxy.test".to_owned()),
                ..StatsigOptions::default()
            };
            let mut adapter =
                StatsigHttpSpecsAdapter::new("cancelled-remote-metrics", Some(&options), None);
            let provider = Arc::new(PendingDownload(AtomicBool::new(false)));
            let net_provider: Arc<dyn crate::networking::NetworkProvider> = provider.clone();
            let mut network = NetworkClient::new("cancelled-remote-metrics", None, Some(&options));
            network.set_network_provider_for_test(Arc::downgrade(&net_provider));
            adapter.network = Arc::new(network);
            adapter.remote_config_value_hydrator =
                Arc::new(RemoteConfigValueHydrator::new_with_ops_stats(
                    adapter.network.clone(),
                    adapter.ops_stats.clone(),
                ));
            if native {
                adapter.initialize_spec_store(store());
            } else {
                adapter.initialize(store());
            }
            let sha = "0".repeat(64);
            let remote = serde_json::json!({"remote": {
                "defaultValue": format!("https://proxy.test/v1/dynamic_config_value/{sha}"),
                "remoteConfigMetadata": {"sha256": sha, "byteLength": 2, "contentType": "application/json", "compression": "none"},
                "rules": []
            }});
            let mut body = String::from_utf8(full(false, 1)).unwrap().replace(
                "\"dynamic_configs\":{}",
                &format!("\"dynamic_configs\":{remote}"),
            );
            if duplicate {
                body.pop();
                body.push_str(",\"has_updates\":false}");
            }
            let data = ResponseData::from_bytes(body.into_bytes());
            let metrics = parking_lot::Mutex::new(Some(ConfigSyncMetrics::from_response_headers(
                &data, "test", false,
            )));
            assert!(
                tokio::time::timeout(
                    Duration::from_millis(1),
                    adapter.process_spec_data_with_metrics(
                        SpecsSyncTrigger::Initial,
                        Ok(NetworkResponse {
                            data,
                            loggable_api: "test".to_owned(),
                            requested_deltas: false,
                            request_url: "https://proxy.test/v1/download_config_specs/test.json"
                                .to_owned(),
                        }),
                        Some(&metrics)
                    )
                )
                .await
                .is_err()
            );
            assert!(provider.0.load(Ordering::Relaxed));
            assert_eq!(
                metrics.into_inner().unwrap().response_type.as_str(),
                if duplicate { "full" } else { "no_update" }
            );
        }
    }
}
