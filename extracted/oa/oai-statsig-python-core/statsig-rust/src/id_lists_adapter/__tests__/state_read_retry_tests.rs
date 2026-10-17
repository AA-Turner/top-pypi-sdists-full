use super::*;
use crate::networking::{NetworkProvider, Response};
use parking_lot::Mutex;
use std::sync::atomic::{AtomicBool, AtomicU16, Ordering};

struct Provider {
    calls: Mutex<Vec<String>>,
    requests: Mutex<Vec<RequestArgs>>,
    file_status: AtomicU16,
    manifest_status: AtomicU16,
    skip_files: AtomicBool,
}

#[async_trait]
impl NetworkProvider for Provider {
    async fn send(&self, _: &HttpMethod, args: &RequestArgs) -> Response {
        self.calls.lock().push(args.url.clone());
        self.requests.lock().push(args.clone());
        let manifest = args.url.contains("manifest");
        let primary = args.url.starts_with("https://proxy.test");
        let status = if primary {
            if manifest {
                self.manifest_status.load(Ordering::SeqCst)
            } else {
                self.file_status.load(Ordering::SeqCst)
            }
        } else {
            200
        };
        let body = if manifest {
            let lists: HashMap<_, _> = (0..12)
                .map(|n| {
                    let name = format!("list{n}");
                    (
                        name.clone(),
                        IdListMetadata {
                            name,
                            url: format!("https://statsigcdn.openai.com/file{n}"),
                            size: 3,
                            file_id: Some("generation1".into()),
                            creation_time: 1,
                        },
                    )
                })
                .collect();
            if self.skip_files.load(Ordering::SeqCst) {
                b"{}".to_vec()
            } else {
                serde_json::to_vec(&lists).unwrap()
            }
        } else {
            b"+a\n".to_vec()
        };
        Response {
            status_code: Some(status),
            data: Some(ResponseData::from_bytes(body)),
            error: None,
        }
    }
    async fn send_without_redirects(&self, method: &HttpMethod, args: &RequestArgs) -> Response {
        self.send(method, args).await
    }
}

#[derive(Default)]
struct Listener(AtomicU16);
impl IdListsUpdateListener for Listener {
    fn get_current_id_list_metadata(&self) -> IdListsResponse {
        HashMap::new()
    }
    fn did_receive_id_list_updates(&self, _: HashMap<String, IdListUpdate>) {
        self.0.fetch_add(1, Ordering::SeqCst);
    }
}

#[tokio::test(start_paused = true)]
async fn files_count_once_per_refresh_and_manifest_success_does_not_reset_them() {
    let provider = Arc::new(Provider {
        calls: Mutex::new(Vec::new()),
        requests: Mutex::new(Vec::new()),
        file_status: AtomicU16::new(503),
        manifest_status: AtomicU16::new(200),
        skip_files: AtomicBool::new(false),
    });
    let listener = Arc::new(Listener::default());
    let mut adapter = StatsigHttpIdListsAdapter::new(
        "secret-test",
        &StatsigOptions {
            id_lists_url: Some("https://proxy.test/manifest".into()),
            download_id_list_file_api: Some("https://proxy.test".into()),
            fallback_to_statsig_api: Some(true),
            ..Default::default()
        },
    );
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    adapter
        .network
        .set_network_provider_for_test(Arc::downgrade(&network_provider));
    adapter.set_listener(listener.clone());
    for refresh in 1..=10 {
        provider.calls.lock().clear();
        assert_eq!(
            adapter.sync_id_lists_with_trigger(true).await.is_ok(),
            refresh % 5 == 0
        );
        let calls = provider.calls.lock();
        assert_eq!(
            calls
                .iter()
                .filter(|url| url.starts_with("https://proxy.test/file"))
                .count(),
            24
        );
        assert_eq!(
            calls
                .iter()
                .filter(|url| url.starts_with("https://statsigcdn.openai.com/file"))
                .count(),
            if refresh % 5 == 0 { 12 } else { 0 }
        );
        assert_eq!(listener.0.load(Ordering::SeqCst), refresh / 5);
    }
    // Foreground success does not change the background streak; skipped files do not either.
    for _ in 0..4 {
        assert!(adapter.sync_id_lists_with_trigger(true).await.is_err());
    }
    assert!(adapter.sync_id_lists().await.is_ok());
    provider.skip_files.store(true, Ordering::SeqCst);
    assert!(adapter.sync_id_lists_with_trigger(true).await.is_ok());
    provider.skip_files.store(false, Ordering::SeqCst);
    assert!(adapter.sync_id_lists_with_trigger(true).await.is_ok());
    // A terminal file failure breaks the eligible streak and never contacts the CDN.
    for _ in 0..4 {
        assert!(adapter.sync_id_lists_with_trigger(true).await.is_err());
    }
    provider.file_status.store(401, Ordering::SeqCst);
    provider.calls.lock().clear();
    assert!(adapter.sync_id_lists_with_trigger(true).await.is_err());
    assert_eq!(provider.calls.lock().len(), 13);
    provider.file_status.store(503, Ordering::SeqCst);
    assert!(adapter.sync_id_lists_with_trigger(true).await.is_err());
    provider.file_status.store(200, Ordering::SeqCst);
    assert!(adapter.sync_id_lists_with_trigger(true).await.is_ok());
    provider.file_status.store(503, Ordering::SeqCst);
    assert!(adapter.sync_id_lists_with_trigger(true).await.is_err());
}

#[tokio::test(start_paused = true)]
async fn manifest_has_its_own_cadence_and_terminal_statuses_never_fallback() {
    let provider = Arc::new(Provider {
        calls: Mutex::new(Vec::new()),
        requests: Mutex::new(Vec::new()),
        file_status: AtomicU16::new(200),
        manifest_status: AtomicU16::new(503),
        skip_files: AtomicBool::new(true),
    });
    let mut adapter = StatsigHttpIdListsAdapter::new(
        "secret-test",
        &StatsigOptions {
            id_lists_url: Some("https://proxy.test/manifest".into()),
            fallback_to_statsig_api: Some(true),
            ..Default::default()
        },
    );
    adapter.fallback_url = Some("https://cdn.test/manifest".into());
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    adapter
        .network
        .set_network_provider_for_test(Arc::downgrade(&network_provider));
    for n in 1..=10 {
        provider.calls.lock().clear();
        assert_eq!(
            adapter
                .fetch_id_list_manifests_from_network(true)
                .await
                .is_ok(),
            n % 5 == 0
        );
        assert_eq!(provider.calls.lock().len(), if n % 5 == 0 { 3 } else { 2 });
    }
    for status in [400, 401, 403, 405, 413, 429, 501] {
        provider.manifest_status.store(status, Ordering::SeqCst);
        provider.calls.lock().clear();
        assert!(
            adapter
                .fetch_id_list_manifests_from_network(false)
                .await
                .is_err()
        );
        assert_eq!(provider.calls.lock().len(), 1);
    }
}

#[tokio::test(start_paused = true)]
async fn configured_primary_budget_controls_manifests_and_each_file() {
    for (attempts, manifests, files) in [
        (None, 2, 2),
        (Some(0), 2, 2),
        (Some(-1), 2, 2),
        (Some(4294967296), 2, 2),
        (Some(1), 1, 1),
        (Some(2), 2, 2),
        (Some(3), 3, 3),
    ] {
        let provider = Arc::new(Provider {
            calls: Mutex::new(Vec::new()),
            requests: Mutex::new(Vec::new()),
            file_status: AtomicU16::new(503),
            manifest_status: AtomicU16::new(503),
            skip_files: AtomicBool::new(false),
        });
        let mut adapter = StatsigHttpIdListsAdapter::new(
            &format!("secret-id-budget-{attempts:?}"),
            &StatsigOptions {
                id_lists_url: Some("https://proxy.test/manifest".into()),
                download_id_list_file_api: Some("https://proxy.test".into()),
                state_read_primary_attempts: attempts,
                ..Default::default()
            },
        );
        let network_provider: Arc<dyn NetworkProvider> = provider.clone();
        adapter
            .network
            .set_network_provider_for_test(Arc::downgrade(&network_provider));
        adapter.set_listener(Arc::new(Listener::default()));
        let mut events = adapter.ops_stats.subscribe_for_test();
        assert!(adapter.sync_id_lists_with_trigger(false).await.is_err());
        assert_eq!(provider.calls.lock().len(), manifests);
        let mut manifest_indices = Vec::new();
        while let Ok(event) = events.try_recv() {
            if let crate::observability::ops_stats::OpsStatsEvent::Diagnostics(event) = event {
                if let Some(marker) = event.marker {
                    let marker = serde_json::to_value(marker).unwrap();
                    if marker["key"] == "get_id_list_sources"
                        && marker["step"] == "network_request"
                        && marker["action"] == "start"
                    {
                        manifest_indices.push(marker["attempt"].as_u64().unwrap());
                    }
                }
            }
        }
        assert_eq!(manifest_indices, (0..manifests as u64).collect::<Vec<_>>());
        provider.calls.lock().clear();
        provider.requests.lock().clear();
        provider.manifest_status.store(200, Ordering::SeqCst);
        assert!(adapter.sync_id_lists_with_trigger(false).await.is_err());
        let calls = provider.calls.lock();
        for file in 0..12 {
            assert_eq!(
                calls
                    .iter()
                    .filter(|url| **url == format!("https://proxy.test/file{file}"))
                    .count(),
                files
            );
        }
        assert_eq!(calls.len(), 1 + 12 * files);
        for request in provider
            .requests
            .lock()
            .iter()
            .filter(|request| request.url.contains("/file"))
        {
            assert_eq!(request.headers.as_ref().unwrap()["Range"], "bytes=0-");
            assert_eq!(request.retries, 0);
        }
        let mut file_indices = Vec::new();
        while let Ok(event) = events.try_recv() {
            if let crate::observability::ops_stats::OpsStatsEvent::Diagnostics(event) = event {
                if let Some(marker) = event.marker {
                    let marker = serde_json::to_value(marker).unwrap();
                    if marker["key"] == "get_id_list"
                        && marker["step"] == "network_request"
                        && marker["action"] == "start"
                    {
                        file_indices.push(marker["attempt"].as_u64().unwrap());
                    }
                }
            }
        }
        for index in 0..manifests as u64 {
            assert_eq!(
                file_indices.iter().filter(|value| **value == index).count(),
                12
            );
        }
    }
}
