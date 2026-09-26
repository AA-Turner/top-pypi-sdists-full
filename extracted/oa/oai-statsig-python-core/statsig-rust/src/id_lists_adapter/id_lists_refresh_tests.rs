use super::*;
use crate::networking::{HttpMethod, NetworkProvider};
use parking_lot::Mutex;
use serial_test::serial;
use std::collections::VecDeque;
use std::io::{self, Read, Seek, SeekFrom};
use std::sync::atomic::{AtomicUsize, Ordering};
use tokio::sync::Semaphore;

#[derive(Clone)]
enum Outcome {
    Body(Vec<u8>),
    Status(u16),
    Timeout,
    BodyError,
    MissingBody,
    ReadError,
}

#[derive(Debug)]
struct BrokenStream;
impl Read for BrokenStream {
    fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
        Err(io::Error::new(
            io::ErrorKind::ConnectionReset,
            "interrupted body",
        ))
    }
}
impl Seek for BrokenStream {
    fn seek(&mut self, _: SeekFrom) -> io::Result<u64> {
        Ok(0)
    }
}

impl Outcome {
    fn response(self) -> Response {
        let (status_code, data, error) = match self {
            Self::Body(bytes) => (Some(200), Some(ResponseData::from_bytes(bytes)), None),
            Self::Status(status) => (Some(status), None, Some("HTTP failure".into())),
            Self::Timeout => (None, None, Some("request timed out".into())),
            Self::BodyError => (
                Some(200),
                Some(ResponseData::from_bytes(b"partial".to_vec())),
                Some("body transfer failed".into()),
            ),
            Self::MissingBody => (Some(200), None, None),
            Self::ReadError => (
                Some(200),
                Some(ResponseData::from_stream(Box::new(BrokenStream))),
                None,
            ),
        };
        Response {
            status_code,
            data,
            error,
        }
    }
}

struct Provider {
    manifest: Mutex<IdListsResponse>,
    outcomes: Mutex<HashMap<String, VecDeque<Outcome>>>,
    requests: Mutex<Vec<RequestArgs>>,
    gates: Mutex<HashMap<String, Arc<Semaphore>>>,
    active: AtomicUsize,
    peak: AtomicUsize,
}

struct ActiveRequest<'a>(&'a AtomicUsize);
impl Drop for ActiveRequest<'_> {
    fn drop(&mut self) {
        self.0.fetch_sub(1, Ordering::SeqCst);
    }
}

#[async_trait]
impl NetworkProvider for Provider {
    async fn send(&self, _: &HttpMethod, args: &RequestArgs) -> Response {
        self.requests.lock().push(args.clone());
        let count = self.active.fetch_add(1, Ordering::SeqCst) + 1;
        self.peak.fetch_max(count, Ordering::SeqCst);
        let _active = ActiveRequest(&self.active);
        let gate = self.gates.lock().get(&args.url).cloned();
        if let Some(gate) = gate {
            gate.acquire().await.unwrap().forget();
        }
        if args.url == "https://manifest.test/lists" {
            return Outcome::Body(serde_json::to_vec(&*self.manifest.lock()).unwrap()).response();
        }
        let mut outcomes = self.outcomes.lock();
        let queue = outcomes.get_mut(&args.url).expect("unexpected file URL");
        let outcome = if queue.len() > 1 {
            queue.pop_front().unwrap()
        } else {
            queue.front().unwrap().clone()
        };
        outcome.response()
    }
}

impl Provider {
    fn set(&self, name: &str, outcomes: Vec<Outcome>) {
        self.outcomes
            .lock()
            .insert(format!("https://files.test/{name}"), outcomes.into());
    }
    fn gate(&self, url: &str) -> Arc<Semaphore> {
        let gate = Arc::new(Semaphore::new(0));
        self.gates.lock().insert(url.into(), gate.clone());
        gate
    }
    fn attempts(&self, name: &str) -> usize {
        self.requests
            .lock()
            .iter()
            .filter(|r| r.url == format!("https://files.test/{name}"))
            .count()
    }
    fn manifest_attempts(&self) -> usize {
        self.requests
            .lock()
            .iter()
            .filter(|r| r.url == "https://manifest.test/lists")
            .count()
    }
}

#[derive(Default)]
struct Listener {
    metadata: Mutex<IdListsResponse>,
    publications: Mutex<Vec<HashMap<String, IdListUpdate>>>,
}
impl IdListsUpdateListener for Listener {
    fn get_current_id_list_metadata(&self) -> IdListsResponse {
        self.metadata.lock().clone()
    }
    fn did_receive_id_list_updates(&self, updates: HashMap<String, IdListUpdate>) {
        *self.metadata.lock() = updates
            .iter()
            .map(|(name, update)| (name.clone(), update.new_metadata.clone()))
            .collect();
        self.publications.lock().push(updates);
    }
}

fn metadata(name: &str, size: u64, generation: i64) -> IdListMetadata {
    IdListMetadata {
        name: name.into(),
        url: format!("https://files.test/{name}"),
        file_id: Some(format!("generation-{generation}")),
        size,
        creation_time: generation,
    }
}
fn setup(names: &[&str]) -> (Arc<Provider>, Arc<StatsigHttpIdListsAdapter>, Arc<Listener>) {
    let provider = Arc::new(Provider {
        manifest: Mutex::new(
            names
                .iter()
                .map(|name| (name.to_string(), metadata(name, 3, 1)))
                .collect(),
        ),
        outcomes: Mutex::new(HashMap::new()),
        requests: Mutex::new(Vec::new()),
        gates: Mutex::new(HashMap::new()),
        active: AtomicUsize::new(0),
        peak: AtomicUsize::new(0),
    });
    for name in names {
        provider.set(name, vec![Outcome::Body(b"+a\n".to_vec())]);
    }
    let dynamic: Arc<dyn NetworkProvider> = provider.clone();
    let mut adapter = StatsigHttpIdListsAdapter::new(
        "secret-tests",
        &StatsigOptions {
            id_lists_url: Some("https://manifest.test/lists".into()),
            ..StatsigOptions::default()
        },
    );
    adapter
        .network
        .set_network_provider_for_test(Arc::downgrade(&dynamic));
    let adapter = Arc::new(adapter);
    let listener = Arc::new(Listener::default());
    adapter.set_listener(listener.clone());
    (provider, adapter, listener)
}
async fn until(condition: impl Fn() -> bool) {
    tokio::time::timeout(Duration::from_secs(3), async {
        while !condition() {
            sleep(Duration::from_millis(1)).await;
        }
    })
    .await
    .expect("condition did not become true");
}
fn start(
    adapter: Arc<StatsigHttpIdListsAdapter>,
) -> tokio::task::JoinHandle<Result<(), StatsigErr>> {
    tokio::spawn(async move { adapter.sync_id_lists().await })
}

#[tokio::test]
#[serial]
async fn bounded_concurrency_reuses_successful_downloads() {
    let (provider, adapter, listener) = setup(&["a", "b", "c"]);
    let a = provider.gate("https://files.test/a");
    let b = provider.gate("https://files.test/b");
    provider.set(
        "a",
        vec![Outcome::Status(503), Outcome::Body(b"+a\n".to_vec())],
    );
    let task = start(adapter);
    until(|| provider.attempts("a") == 1 && provider.attempts("b") == 1).await;
    assert_eq!(provider.attempts("c"), 1);
    assert!(listener.publications.lock().is_empty());
    b.add_permits(1);
    until(|| provider.attempts("c") == 1).await;
    assert!(listener.publications.lock().is_empty());
    a.add_permits(2);
    task.await.unwrap().unwrap();
    assert!(provider.peak.load(Ordering::SeqCst) <= 4);
    assert_eq!(provider.attempts("a"), 2);
    assert_eq!(provider.attempts("b"), 1);
    assert_eq!(provider.attempts("c"), 1);
    assert_eq!(listener.publications.lock().len(), 1);
    assert_eq!(listener.publications.lock()[0].len(), 3);
    assert!(provider.requests.lock().iter().all(|r| r.retries == 0));
}

#[tokio::test]
#[serial]
async fn exhaustion_drains_other_jobs_and_preserves_committed_lists() {
    let (provider, adapter, listener) = setup(&["a", "b", "c"]);
    listener
        .metadata
        .lock()
        .insert("retained".into(), metadata("retained", 3, 1));
    provider.set("a", vec![Outcome::Status(401)]);
    provider.set("b", vec![Outcome::Status(500)]);
    provider.set("c", vec![Outcome::Timeout, Outcome::Body(b"+c\n".to_vec())]);
    assert!(adapter.sync_id_lists().await.is_err());
    assert_eq!(provider.attempts("a"), 1);
    assert_eq!(provider.attempts("b"), 3);
    assert_eq!(provider.attempts("c"), 2);
    assert!(listener.publications.lock().is_empty());
    assert!(listener.metadata.lock().contains_key("retained"));
}

#[tokio::test]
#[serial]
async fn exhausted_refresh_discards_successful_bodies_before_the_next_refresh() {
    let (provider, adapter, listener) = setup(&["a", "b"]);
    provider.set("b", vec![Outcome::Status(503)]);
    assert!(adapter.sync_id_lists().await.is_err());
    assert_eq!(provider.attempts("a"), 1);
    assert_eq!(provider.attempts("b"), 3);
    assert!(listener.publications.lock().is_empty());

    // Even an unchanged manifest must start with fresh bodies after exhaustion.
    provider.set("a", vec![Outcome::Body(b"+z\n".to_vec())]);
    provider.set("b", vec![Outcome::Body(b"+b\n".to_vec())]);
    adapter.sync_id_lists().await.unwrap();
    assert_eq!(provider.manifest_attempts(), 2);
    assert_eq!(provider.attempts("a"), 2);
    assert_eq!(provider.attempts("b"), 4);
    let publications = listener.publications.lock();
    assert_eq!(publications.len(), 1);
    assert_eq!(publications[0]["a"].raw_changeset.as_deref(), Some("+z\n"));
}

#[tokio::test]
#[serial]
async fn retries_transport_and_body_failures_but_rejects_terminal_errors() {
    for outcome in [
        Outcome::Status(503),
        Outcome::Timeout,
        Outcome::BodyError,
        Outcome::MissingBody,
        Outcome::ReadError,
    ] {
        let (provider, adapter, listener) = setup(&["a"]);
        provider.set("a", vec![outcome, Outcome::Body(b"+a\n".to_vec())]);
        adapter.sync_id_lists().await.unwrap();
        assert_eq!(provider.attempts("a"), 2);
        assert_eq!(listener.publications.lock().len(), 1);
    }
    for outcome in [
        Outcome::Status(400),
        Outcome::Status(401),
        Outcome::Status(403),
        Outcome::Status(405),
        Outcome::Status(413),
        Outcome::Status(429),
        Outcome::Status(501),
        Outcome::Body(vec![0xff]),
    ] {
        let (provider, adapter, listener) = setup(&["a"]);
        provider.set("a", vec![outcome]);
        assert!(adapter.sync_id_lists().await.is_err());
        assert_eq!(provider.attempts("a"), 1);
        assert!(listener.publications.lock().is_empty());
    }
}

#[tokio::test]
#[serial]
async fn exhaustion_reports_actual_attempts() {
    let (provider, adapter, _) = setup(&["a"]);
    provider.set("a", vec![Outcome::BodyError]);
    let error = adapter.sync_id_lists().await.unwrap_err();
    assert!(matches!(
        error,
        StatsigErr::NetworkError(NetworkError::RetriesExhausted(_, Some(200), 3, _))
    ));
    assert_eq!(provider.attempts("a"), 3);
}

#[tokio::test]
#[serial]
async fn terminal_failure_reports_previous_attempts() {
    let (provider, adapter, listener) = setup(&["a"]);
    provider.set("a", vec![Outcome::Status(503), Outcome::Status(401)]);
    let error = adapter.sync_id_lists().await.unwrap_err();
    assert!(matches!(
        error,
        StatsigErr::NetworkError(NetworkError::RetriesExhausted(_, Some(401), 2, _))
    ));
    assert_eq!(provider.attempts("a"), 2);
    assert!(listener.publications.lock().is_empty());
}

#[tokio::test]
#[serial]
async fn frozen_retries_and_next_refresh_use_distinct_generations() {
    let (provider, adapter, listener) = setup(&["a"]);
    listener
        .metadata
        .lock()
        .insert("a".into(), metadata("a", 1, 1));
    provider.set(
        "a",
        vec![Outcome::Status(503), Outcome::Body(b"+a\n".to_vec())],
    );
    let gate = provider.gate("https://files.test/a");
    let task = start(adapter.clone());
    until(|| provider.attempts("a") == 1).await;
    provider
        .manifest
        .lock()
        .insert("a".into(), metadata("a", 9, 2));
    gate.add_permits(2);
    task.await.unwrap().unwrap();
    {
        let requests = provider.requests.lock();
        let files: Vec<_> = requests.iter().filter(|r| r.url.ends_with("/a")).collect();
        assert_eq!(files.len(), 2);
        for request in files {
            assert_eq!(request.id_list_file_id.as_deref(), Some("generation-1"));
            assert_eq!(
                request.headers.as_ref().unwrap().get("Range").unwrap(),
                "bytes=1-"
            );
            assert_eq!(
                request
                    .headers
                    .as_ref()
                    .unwrap()
                    .get("statsig-id-list-file-size")
                    .unwrap(),
                "3"
            );
        }
    }
    gate.add_permits(1);
    adapter.sync_id_lists().await.unwrap();
    let requests = provider.requests.lock();
    let last = requests.last().unwrap();
    assert_eq!(last.id_list_file_id.as_deref(), Some("generation-2"));
    assert_eq!(
        last.headers.as_ref().unwrap().get("Range").unwrap(),
        "bytes=0-"
    );
    assert_eq!(listener.publications.lock().len(), 2);
}

#[tokio::test]
#[serial]
async fn unchanged_shrinking_lists_and_removals_preserve_existing_rules() {
    let (provider, adapter, listener) = setup(&["same", "shrink", "grow", "replace"]);
    for (name, size, generation) in [
        ("same", 3, 1),
        ("shrink", 8, 1),
        ("grow", 1, 1),
        ("replace", 3, 0),
        ("remove", 3, 1),
    ] {
        listener
            .metadata
            .lock()
            .insert(name.into(), metadata(name, size, generation));
    }
    adapter.sync_id_lists().await.unwrap();
    assert_eq!(provider.attempts("same"), 0);
    assert_eq!(provider.attempts("shrink"), 0);
    assert_eq!(provider.attempts("grow"), 1);
    assert_eq!(provider.attempts("replace"), 1);
    let updates = listener.publications.lock();
    assert_eq!(updates[0].len(), 4);
    assert!(updates[0]["same"].raw_changeset.is_none());
    assert!(updates[0]["shrink"].raw_changeset.is_none());
    assert!(!updates[0].contains_key("remove"));
}

#[tokio::test]
#[serial]
async fn empty_manifest_publishes_removal_of_all_lists_without_file_downloads() {
    let (provider, adapter, listener) = setup(&[]);
    listener
        .metadata
        .lock()
        .insert("removed".into(), metadata("removed", 3, 1));

    adapter.sync_id_lists().await.unwrap();
    assert_eq!(provider.manifest_attempts(), 1);
    assert_eq!(provider.requests.lock().len(), 1);
    assert!(listener.metadata.lock().is_empty());
    let publications = listener.publications.lock();
    assert_eq!(publications.len(), 1);
    assert!(publications[0].is_empty());
}

#[tokio::test]
#[serial]
async fn cdn_download_uses_query_range_and_accepts_http_200() {
    let (provider, adapter, listener) = setup(&["a"]);
    let url = "https://statsigcdn.openai.com/v1/download_id_list_file/a";
    provider.manifest.lock().get_mut("a").unwrap().url = url.into();
    listener
        .metadata
        .lock()
        .insert("a".into(), metadata("a", 1, 1));
    provider
        .outcomes
        .lock()
        .insert(url.into(), vec![Outcome::Body(b"+a\n".to_vec())].into());
    adapter.sync_id_lists().await.unwrap();
    let requests = provider.requests.lock();
    let request = requests.last().unwrap();
    assert_eq!(
        request
            .query_params
            .as_ref()
            .unwrap()
            .get("range")
            .map(String::as_str),
        Some("1-")
    );
    assert!(!request.headers.as_ref().unwrap().contains_key("Range"));
    assert!(
        !request
            .headers
            .as_ref()
            .unwrap()
            .contains_key("statsig-id-list-file-size")
    );
    assert_eq!(listener.publications.lock().len(), 1);
}

#[tokio::test]
#[serial]
async fn successful_and_failed_refreshes_close_diagnostics_and_count_files_once() {
    use crate::observability::ops_stats::OpsStatsEvent;
    for succeed in [false, true] {
        let (provider, adapter, _) = setup(&["a", "b"]);
        let mut events = adapter.ops_stats.subscribe_for_test();
        provider.set(
            "a",
            if succeed {
                vec![Outcome::Status(503), Outcome::Body(b"+a\n".to_vec())]
            } else {
                vec![Outcome::Status(403)]
            },
        );
        assert_eq!(adapter.sync_id_lists().await.is_ok(), succeed);
        let mut balance: HashMap<String, i32> = HashMap::new();
        let mut saw_sync = false;
        while let Ok(event) = events.try_recv() {
            match event {
                OpsStatsEvent::Diagnostics(event) => {
                    if let Some(marker) = event.marker {
                        let marker = serde_json::to_value(marker).unwrap();
                        let key = format!("{}:{}:{}", marker["key"], marker["step"], marker["url"]);
                        *balance.entry(key).or_default() +=
                            if marker["action"] == "start" { 1 } else { -1 };
                    }
                }
                OpsStatsEvent::Observability(event)
                    if event.metric_name == ID_LISTS_SYNC_OVERALL_LATENCY_METRIC =>
                {
                    let tags = event.tags.as_ref().unwrap();
                    assert_eq!(tags["id_lists_sync_success"], succeed.to_string());
                    assert_eq!(tags["id_list_manifest_success"], "true");
                    assert_eq!(
                        tags["succeed_single_id_list_number"],
                        if succeed { "2" } else { "1" }
                    );
                    saw_sync = true;
                }
                _ => {}
            }
        }
        assert!(saw_sync);
        assert!(!balance.is_empty());
        assert!(
            balance.values().all(|value| *value == 0),
            "unclosed markers: {balance:?}"
        );
    }
}

#[tokio::test]
#[serial]
async fn manifest_and_file_failure_diagnostics_preserve_region_and_transport_error() {
    use crate::observability::ops_stats::OpsStatsEvent;

    struct ManifestFailureProvider {
        connection_error: bool,
    }
    #[async_trait]
    impl NetworkProvider for ManifestFailureProvider {
        async fn send(&self, _: &HttpMethod, _: &RequestArgs) -> Response {
            if self.connection_error {
                return Response {
                    status_code: None,
                    data: None,
                    error: Some("connection reset".into()),
                };
            }
            Response {
                status_code: Some(500),
                data: Some(ResponseData::from_bytes_with_headers(
                    b"unavailable".to_vec(),
                    Some(HashMap::from([
                        ("x-statsig-region".into(), "az-westus-2".into()),
                        ("content-type".into(), "text/plain".into()),
                    ])),
                )),
                error: None,
            }
        }
    }

    for (use_get, is_file) in [(false, false), (true, false), (true, true)] {
        for connection_error in [false, true] {
            let provider: Arc<dyn NetworkProvider> =
                Arc::new(ManifestFailureProvider { connection_error });
            let mut adapter = StatsigHttpIdListsAdapter::new(
                "secret-tests",
                &StatsigOptions {
                    id_lists_url: if use_get {
                        None
                    } else {
                        Some("https://manifest.test/lists".into())
                    },
                    ..StatsigOptions::default()
                },
            );
            adapter
                .network
                .set_network_provider_for_test(Arc::downgrade(&provider));
            let mut events = adapter.ops_stats.subscribe_for_test();
            adapter.download_retry_count = 0;
            let result = if is_file {
                adapter
                    .download_id_list(&IdListDownloadJob {
                        name: "a".into(),
                        url: "https://files.test/a".into(),
                        metadata: metadata("a", 3, 1),
                        range_start: 0,
                    })
                    .await
                    .map(|_| ())
            } else {
                adapter
                    .fetch_id_list_manifests_from_network()
                    .await
                    .map(|_| ())
            };
            assert!(result.is_err());
            let mut markers = Vec::new();
            while let Ok(event) = events.try_recv() {
                if let OpsStatsEvent::Diagnostics(event) = event {
                    if let Some(marker) = event.marker {
                        let marker = serde_json::to_value(marker).unwrap();
                        if marker["step"] == "network_request" {
                            markers.push(marker);
                        }
                    }
                }
            }
            assert_eq!(markers.len(), 2, "one start/end pair per request");
            assert_eq!(markers[0]["action"], "start");
            let end = &markers[1];
            assert_eq!(
                end["key"],
                if is_file {
                    "get_id_list"
                } else {
                    "get_id_list_sources"
                }
            );
            assert_eq!(end["step"], "network_request");
            assert_eq!(end["action"], "end");
            assert_eq!(end["success"], false);
            if connection_error {
                assert_eq!(end["error"]["name"], "NetworkError");
                assert_eq!(end["error"]["message"], "connection reset");
                assert_eq!(end["error"]["code"], "None");
            } else {
                assert_eq!(end["statusCode"], 500);
                assert_eq!(end["sdkRegion"], "az-westus-2");
                assert_eq!(end["contentType"], "text/plain");
            }
        }
    }
}
