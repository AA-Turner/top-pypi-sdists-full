use super::*;
use crate::networking::{HttpMethod, NetworkProvider, Response};
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
    setup_with_options(names, StatsigOptions::default())
}

fn setup_with_options(
    names: &[&str],
    options: StatsigOptions,
) -> (Arc<Provider>, Arc<StatsigHttpIdListsAdapter>, Arc<Listener>) {
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
            ..options
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
    assert_eq!(provider.attempts("b"), 2);
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
    assert_eq!(provider.attempts("b"), 2);
    assert!(listener.publications.lock().is_empty());

    // Even an unchanged manifest must start with fresh bodies after exhaustion.
    provider.set("a", vec![Outcome::Body(b"+z\n".to_vec())]);
    provider.set("b", vec![Outcome::Body(b"+b\n".to_vec())]);
    adapter.sync_id_lists().await.unwrap();
    assert_eq!(provider.manifest_attempts(), 2);
    assert_eq!(provider.attempts("a"), 2);
    assert_eq!(provider.attempts("b"), 3);
    let publications = listener.publications.lock();
    assert_eq!(publications.len(), 1);
    assert_eq!(publications[0]["a"].raw_changeset.as_deref(), Some("+z\n"));
}

#[tokio::test]
#[serial]
async fn partial_eager_refresh_removes_by_name_and_recovers_only_missing_bytes() {
    use crate::{
        observability::ops_stats::OpsStatsEvent, sdk_event_emitter::SdkEventEmitter,
        spec_store::SpecStore,
    };
    for compact in [false, true] {
        let options = StatsigOptions {
            enable_id_list_elias_fano: Some(compact),
            experimental_flags: Some(["partial_id_list_refresh".to_string()].into()),
            ..Default::default()
        };
        let (provider, adapter, _) = setup_with_options(&["a", "b", "removed"], options.clone());
        let store = Arc::new(SpecStore::new(
            "partial",
            "partial".into(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            Some(&options),
        ));
        adapter.set_listener(store.clone());
        adapter.sync_id_lists().await.unwrap();
        {
            let mut manifest = provider.manifest.lock();
            manifest.remove("removed");
            manifest.insert(
                "a".into(),
                IdListMetadata {
                    name: "b".into(),
                    ..metadata("a", 6, 1)
                },
            );
            manifest.insert("b".into(), metadata("b", 3, 2));
            manifest.insert(
                "cold".into(),
                IdListMetadata {
                    name: "removed".into(), // The embedded name must not keep this list alive.
                    ..metadata("cold", 3, 1)
                },
            );
        }
        provider.set("a", vec![Outcome::Body(b"+a\n+z\n".to_vec())]);
        provider.set("b", vec![Outcome::Status(403)]);
        provider.set("cold", vec![Outcome::Status(403)]);
        let mut events = adapter.ops_stats.subscribe_for_test();
        assert!(adapter.sync_id_lists().await.is_err());
        assert!(std::iter::from_fn(|| events.try_recv().ok()).any(|event| matches!(event,
            OpsStatsEvent::Observability(m) if m.metric_name == "id_list_manifest_name_mismatch" && m.value == 2.0
        )));
        let partial = store.load_data();
        assert_eq!(partial.id_lists.len(), 2);
        assert!(partial.id_lists["a"].ids.contains("z"));
        assert_eq!(partial.id_lists["a"].metadata.size, 6);
        assert!(partial.id_lists["b"].ids.contains("a"));
        assert_eq!(
            partial.id_lists["b"].metadata.file_id,
            metadata("b", 3, 1).file_id
        );
        provider.set("b", vec![Outcome::Body(b"+y\n".to_vec())]);
        provider.set("cold", vec![Outcome::Body(b"+c\n".to_vec())]);
        adapter.sync_id_lists().await.unwrap();
        let recovered = store.load_data();
        assert_eq!(provider.attempts("a"), 2); // initial body and one append
        assert!(recovered.id_lists["b"].ids.contains("y"));
        assert!(!recovered.id_lists["b"].ids.contains("a"));
        assert!(recovered.id_lists["cold"].ids.contains("c"));
        assert_eq!(recovered.id_lists["cold"].metadata.name, "cold");
        assert!(!recovered.id_lists.contains_key("removed"));
        assert!(partial.id_lists["b"].ids.contains("a")); // old snapshot stays valid
        assert!(
            provider
                .requests
                .lock()
                .iter()
                .filter(|r| r.url.ends_with("/b"))
                .all(|r| r.headers.as_ref().unwrap()["Range"] == "bytes=0-")
        );
        provider.manifest.lock().clear();
        adapter.sync_id_lists().await.unwrap();
        assert!(store.load_data().id_lists.is_empty());
    }
}

#[tokio::test]
#[serial]
async fn default_refresh_preserves_embedded_names_without_counting_mismatches() {
    use crate::observability::ops_stats::OpsStatsEvent;
    let (provider, adapter, listener) = setup(&["a"]);
    provider.manifest.lock().get_mut("a").unwrap().name = "b".into();
    let mut events = adapter.ops_stats.subscribe_for_test();

    adapter.sync_id_lists().await.unwrap();
    assert_eq!(listener.metadata.lock()["a"].name, "b");
    assert!(
        !std::iter::from_fn(|| events.try_recv().ok()).any(|event| matches!(event,
            OpsStatsEvent::Observability(m) if m.metric_name == "id_list_manifest_name_mismatch"
        ))
    );
}

#[tokio::test]
async fn partial_refresh_does_not_merge_failed_lazy_loads() {
    let (provider, adapter, listener) = setup_with_options(
        &["a"],
        StatsigOptions {
            lazy_load_id_lists: Some(true),
            experimental_flags: Some(["partial_id_list_refresh".to_owned()].into()),
            ..Default::default()
        },
    );
    adapter.sync_id_lists().await.unwrap();
    assert_eq!(provider.attempts("a"), 0);
    provider.set("a", vec![Outcome::Status(403)]);
    let before = listener.publications.lock().len();
    assert!(adapter.process_id_list("a").await.is_err());
    assert_eq!(listener.publications.lock().len(), before);
    assert!(!listener.metadata.lock().contains_key("a"));
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
        StatsigErr::NetworkError(NetworkError::RetriesExhausted(_, Some(200), 2, _))
    ));
    assert_eq!(provider.attempts("a"), 2);
}

#[tokio::test]
#[serial]
async fn terminal_failure_reports_previous_attempts() {
    let (provider, adapter, listener) = setup(&["a"]);
    provider.set("a", vec![Outcome::Status(503), Outcome::Status(401)]);
    let error = adapter.sync_id_lists().await.unwrap_err();
    assert!(matches!(
        error,
        StatsigErr::NetworkError(NetworkError::RequestNotRetryable(_, Some(401), _))
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
    provider.set("a", vec![Outcome::Body(b"+a\n+b\n+c\n".to_vec())]);
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
async fn cdn_download_uses_range_header_and_normalizes_http_200() {
    let (provider, adapter, listener) = setup(&["a"]);
    let url = "https://statsigcdn.openai.com/v1/download_id_list_file/a";
    provider.manifest.lock().get_mut("a").unwrap().url = url.into();
    listener
        .metadata
        .lock()
        .insert("a".into(), metadata("a", 3, 1));
    provider.manifest.lock().get_mut("a").unwrap().size = 6;
    provider
        .outcomes
        .lock()
        .insert(url.into(), vec![Outcome::Body(b"+a\n+b\n".to_vec())].into());
    adapter.sync_id_lists().await.unwrap();
    let requests = provider.requests.lock();
    let request = requests.last().unwrap();
    assert!(request.query_params.is_none());
    assert_eq!(request.headers.as_ref().unwrap()["Range"], "bytes=3-");
    assert_eq!(
        request.headers.as_ref().unwrap()["statsig-id-list-file-size"],
        "6"
    );
    assert_eq!(
        request.headers.as_ref().unwrap()["Accept-Encoding"],
        "identity"
    );
    assert_eq!(listener.publications.lock().len(), 1);
    assert_eq!(
        listener.publications.lock()[0]["a"]
            .raw_changeset
            .as_deref(),
        Some("+b\n")
    );
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
            let result = if is_file {
                adapter
                    .download_id_list(
                        &IdListDownloadJob {
                            name: "a".into(),
                            url: "https://files.test/a".into(),
                            metadata: metadata("a", 3, 1),
                            range_start: 0,
                        },
                        false,
                        0,
                    )
                    .await
                    .map(|_| ())
            } else {
                adapter
                    .fetch_id_list_manifests_from_network(false)
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
            assert_eq!(
                markers.len(),
                if is_file { 2 } else { 4 },
                "one start/end pair per attempt"
            );
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

#[tokio::test]
#[serial]
async fn overlapping_refresh_reads_the_new_manifest_and_committed_cursor() {
    let (provider, adapter, _) = setup(&["a"]);
    let gate = provider.gate("https://files.test/a");
    let runtime = StatsigRuntime::get_runtime();
    let store = Arc::new(crate::SpecStore::new(
        "cursor-test",
        "cursor-test".into(),
        runtime.clone(),
        Arc::new(crate::sdk_event_emitter::SdkEventEmitter::default()),
        None,
    ));
    let first = adapter.clone().start(&runtime, store.clone());
    let next = adapter.refresh(RefreshTrigger::Background);
    tokio::pin!(first, next);
    assert!(futures::poll!(&mut first).is_pending());
    assert!(futures::poll!(&mut next).is_pending());
    assert_eq!(provider.manifest_attempts(), 1);
    provider
        .manifest
        .lock()
        .insert("b".into(), metadata("b", 3, 1));
    provider.set("b", vec![Outcome::Body(b"+b\n".to_vec())]);
    gate.add_permits(2);
    let (first, next) = tokio::join!(first, next);
    first.unwrap();
    next.unwrap();
    assert_eq!(provider.manifest_attempts(), 2);
    assert_eq!((provider.attempts("a"), provider.attempts("b")), (1, 1));
    let committed = store.get_current_id_list_metadata();
    assert_eq!((committed["a"].size, committed["b"].size), (3, 3));
}

#[tokio::test]
#[serial]
async fn serialized_starts_cannot_replace_another_refresh_listener() {
    let (provider, adapter, first_listener) = setup(&["a"]);
    let second_listener = Arc::new(Listener::default());
    let manifest = provider.gate("https://manifest.test/lists");
    let runtime = StatsigRuntime::get_runtime();
    let first = adapter.clone().start(&runtime, first_listener.clone());
    let second = adapter.clone().start(&runtime, second_listener.clone());
    tokio::pin!(first, second);
    assert!(futures::poll!(&mut first).is_pending());
    assert!(futures::poll!(&mut second).is_pending());
    assert_eq!(provider.manifest_attempts(), 1);
    manifest.add_permits(2);
    let (first, second) = tokio::join!(first, second);
    first.unwrap();
    second.unwrap();
    assert_eq!(first_listener.publications.lock().len(), 1);
    assert_eq!(second_listener.publications.lock().len(), 1);
}

#[tokio::test]
#[serial]
async fn cancelled_downloads_close_diagnostics_and_shutdown_rejects_queued_work() {
    use crate::observability::ops_stats::OpsStatsEvent;
    for url in ["https://manifest.test/lists", "https://files.test/a"] {
        for shutdown in [false, true] {
            let (provider, adapter, listener) = setup(&["a"]);
            let mut events = adapter.ops_stats.subscribe_for_test();
            provider.gate(url);
            let task = start(adapter.clone());
            until(|| provider.requests.lock().iter().any(|r| r.url == url)).await;
            if shutdown {
                let queued = adapter.sync_id_lists();
                tokio::pin!(queued);
                assert!(futures::poll!(&mut queued).is_pending());
                let (drained, queued) =
                    tokio::join!(adapter.shutdown(Duration::from_secs(2)), queued);
                drained.unwrap();
                assert!(queued.is_err());
                assert!(task.await.unwrap().is_err());
                assert!(adapter.sync_id_lists().await.is_err());
            } else {
                task.abort();
                assert!(task.await.unwrap_err().is_cancelled());
            }
            assert_eq!(provider.manifest_attempts(), 1);
            assert_eq!(provider.active.load(Ordering::SeqCst), 0);
            assert!(listener.publications.lock().is_empty());
            let mut balance = HashMap::<String, i32>::new();
            let mut failed_requests = 0;
            let mut failed_syncs = 0;
            while let Ok(event) = events.try_recv() {
                match event {
                    OpsStatsEvent::Diagnostics(event) => {
                        if let Some(marker) = event.marker {
                            let marker = serde_json::to_value(marker).unwrap();
                            let key =
                                format!("{}:{}:{}", marker["key"], marker["step"], marker["url"]);
                            *balance.entry(key).or_default() +=
                                if marker["action"] == "start" { 1 } else { -1 };
                            if marker["url"] == url
                                && marker["step"] == "network_request"
                                && marker["action"] == "end"
                            {
                                assert_eq!(marker["success"], false);
                                assert_eq!(marker["attempt"], 0);
                                failed_requests += 1;
                            }
                        }
                    }
                    OpsStatsEvent::Observability(event)
                        if event.metric_name == ID_LISTS_SYNC_OVERALL_LATENCY_METRIC =>
                    {
                        assert_eq!(
                            event.tags.as_ref().unwrap()["id_lists_sync_success"],
                            "false"
                        );
                        failed_syncs += 1;
                    }
                    _ => {}
                }
            }
            assert_eq!((failed_requests, failed_syncs), (1, 1));
            assert!(balance.values().all(|v| *v == 0), "{balance:?}");
        }
    }
}

#[tokio::test]
#[serial]
async fn serialized_background_schedules_stop_active_and_future_downloads() {
    let (provider, mut adapter, listener) = setup(&["a"]);
    let config = Arc::get_mut(&mut adapter).unwrap();
    config.sync_interval_duration = Duration::from_millis(1);
    provider.gate("https://files.test/a");
    let runtime = StatsigRuntime::get_runtime();
    for _ in 0..2 {
        adapter
            .clone()
            .schedule_background_sync(&runtime)
            .await
            .unwrap();
    }
    until(|| provider.attempts("a") == 1).await;
    adapter.force_shutdown();
    until(|| runtime.get_num_active_tasks() == 0).await;
    adapter
        .clone()
        .schedule_background_sync(&runtime)
        .await
        .unwrap();
    until(|| runtime.get_num_active_tasks() == 0).await;
    assert_eq!(provider.active.load(Ordering::SeqCst), 0);
    assert_eq!(provider.manifest_attempts(), 1);
    assert!(listener.publications.lock().is_empty());

    let (_, adapter, _) = setup(&["a"]);
    let weak = Arc::downgrade(&adapter);
    adapter.schedule_background_sync(&runtime).await.unwrap();
    assert!(weak.upgrade().is_none());
    until(|| runtime.get_num_active_tasks() == 0).await;
}

#[tokio::test]
#[serial]
async fn serialized_shutdown_bounds_an_entered_blocking_callback() {
    let (provider, adapter, _) = setup(&[]);
    let (release, rx) = std::sync::mpsc::channel();
    let entered = Arc::new(Notify::new());
    let listener = Arc::new(CallbackListener {
        blocking: true,
        callback: {
            let entered = entered.clone();
            let rx = Mutex::new(rx);
            move || {
                entered.notify_one();
                rx.lock().recv_timeout(Duration::from_secs(3)).unwrap();
            }
        },
    });
    let runtime = StatsigRuntime::get_runtime();
    tokio::select! {
        result = adapter.clone().start(&runtime, listener.clone()) => panic!("publication finished early: {result:?}"),
        () = entered.notified() => {}
    }
    let queued = adapter.sync_id_lists();
    tokio::pin!(queued);
    assert!(futures::poll!(&mut queued).is_pending());
    assert!(matches!(
        adapter.shutdown(Duration::ZERO).await,
        Err(StatsigErr::ShutdownFailure(_))
    ));
    assert!(queued.await.is_err());
    assert_eq!(provider.manifest_attempts(), 1);
    release.send(()).unwrap();
    adapter.shutdown(Duration::from_secs(2)).await.unwrap();
}

#[tokio::test]
#[serial]
async fn same_listener_start_fetches_the_manifest_during_a_cold_compact_download() {
    let (provider, adapter, _) = setup_with_options(
        &["cold"],
        StatsigOptions {
            lazy_load_id_lists: Some(true),
            ..Default::default()
        },
    );
    let runtime = StatsigRuntime::get_runtime();
    let listener = Arc::new(CallbackListener {
        blocking: true,
        callback: || {},
    });
    adapter
        .clone()
        .start(&runtime, listener.clone())
        .await
        .unwrap();
    let gate = provider.gate("https://files.test/cold");
    let cold = {
        let adapter = adapter.clone();
        tokio::spawn(async move { adapter.process_id_list("cold").await })
    };
    until(|| provider.attempts("cold") == 1).await;
    let start = adapter.clone().start(&runtime, listener);
    tokio::pin!(start);
    tokio::select! {
        result = &mut start => panic!("refresh finished while compact storage was busy: {result:?}"),
        () = until(|| provider.manifest_attempts() == 2) => {}
    }
    gate.add_permits(1);
    cold.await.unwrap().unwrap();
    start.await.unwrap();
}

#[tokio::test]
#[serial]
async fn shutdown_releases_start_waiting_for_a_detached_cold_publication() {
    let (provider, adapter, _) = setup_with_options(
        &["cold"],
        StatsigOptions {
            lazy_load_id_lists: Some(true),
            ..Default::default()
        },
    );
    let (release, rx) = std::sync::mpsc::channel();
    let entered = Arc::new(Notify::new());
    let runtime = StatsigRuntime::get_runtime();
    let listener = Arc::new(CallbackListener {
        blocking: true,
        callback: {
            let entered = entered.clone();
            let rx = Mutex::new(rx);
            let initial = std::sync::atomic::AtomicBool::new(true);
            move || {
                if !initial.swap(false, Ordering::SeqCst) {
                    entered.notify_one();
                    rx.lock().recv_timeout(Duration::from_secs(3)).unwrap();
                }
            }
        },
    });
    adapter.clone().start(&runtime, listener).await.unwrap();
    tokio::select! {
        result = adapter.process_id_list("cold") => panic!("cold publication finished early: {result:?}"),
        () = entered.notified() => {}
    }
    let start = adapter
        .clone()
        .start(&runtime, Arc::new(Listener::default()));
    tokio::pin!(start);
    assert!(futures::poll!(&mut start).is_pending());
    adapter.force_shutdown();
    assert!(matches!(
        tokio::time::timeout(Duration::from_secs(1), start)
            .await
            .unwrap(),
        Err(StatsigErr::ShutdownFailure(_))
    ));
    assert_eq!(provider.manifest_attempts(), 1);
    assert!(adapter.shutdown(Duration::ZERO).await.is_err());
    release.send(()).unwrap();
    adapter.shutdown(Duration::from_secs(2)).await.unwrap();
}

struct CallbackListener<F> {
    blocking: bool,
    callback: F,
}

impl<F: Fn() + Send + Sync> IdListsUpdateListener for CallbackListener<F> {
    fn requires_blocking_id_list_publication(&self) -> bool {
        self.blocking
    }
    fn get_current_id_list_metadata(&self) -> IdListsResponse {
        HashMap::new()
    }
    fn did_receive_id_list_updates(&self, _: HashMap<String, IdListUpdate>) {
        (self.callback)();
    }
}

#[tokio::test]
#[serial]
async fn forced_stop_fences_inline_publication_and_is_reentrant() {
    let (_provider, adapter, _) = setup(&[]);
    let (release, rx) = std::sync::mpsc::channel();
    let (entered, started) = tokio::sync::oneshot::channel();
    let listener = Arc::new(CallbackListener {
        blocking: false,
        callback: {
            let entered = Mutex::new(Some(entered));
            let rx = Mutex::new(rx);
            let weak = Arc::downgrade(&adapter);
            move || {
                entered.lock().take().unwrap().send(()).unwrap();
                rx.lock().recv_timeout(Duration::from_secs(3)).unwrap();
                weak.upgrade().unwrap().force_shutdown();
            }
        },
    });
    let (done, callback_done) = tokio::sync::oneshot::channel();
    std::thread::spawn({
        let adapter = adapter.clone();
        move || {
            let rt = tokio::runtime::Builder::new_current_thread()
                .enable_all()
                .build()
                .unwrap();
            let result = rt.block_on(async {
                adapter
                    .start(&StatsigRuntime::get_runtime(), listener)
                    .await
            });
            done.send(result).unwrap();
        }
    });
    tokio::time::timeout(Duration::from_secs(3), started)
        .await
        .unwrap()
        .unwrap();
    let (stopped, mut force_done) = tokio::sync::oneshot::channel();
    std::thread::spawn({
        let adapter = adapter.clone();
        move || {
            adapter.force_shutdown();
            stopped.send(()).unwrap();
        }
    });
    until(|| adapter.network.shutdown_flag().load(Ordering::SeqCst)).await;
    assert!(
        tokio::time::timeout(Duration::from_millis(50), &mut force_done)
            .await
            .is_err()
    );
    assert!(matches!(
        adapter.shutdown(Duration::ZERO).await,
        Err(StatsigErr::ShutdownFailure(_))
    ));
    release.send(()).unwrap();
    tokio::time::timeout(Duration::from_secs(3), callback_done)
        .await
        .unwrap()
        .unwrap()
        .unwrap();
    tokio::time::timeout(Duration::from_secs(3), force_done)
        .await
        .unwrap()
        .unwrap();
    assert!(adapter.sync_id_lists().await.is_err());
}

#[test]
#[serial]
fn serialized_refresh_keeps_context_until_background_enqueue() {
    use crate::observability::ops_stats::OpsStatsEvent;

    let rt = tokio::runtime::Builder::new_current_thread()
        .max_blocking_threads(1)
        .enable_all()
        .build()
        .unwrap();
    rt.block_on(async {
        let (provider, adapter, _) = setup(&[]);
        let (release, rx) = std::sync::mpsc::channel();
        let rx = Mutex::new(rx);
        adapter.set_listener(Arc::new(CallbackListener {
            blocking: true,
            callback: move || {
                rx.lock().recv_timeout(Duration::from_secs(3)).unwrap();
            },
        }));
        let mut events = adapter.ops_stats.subscribe_for_test();
        let background = adapter.refresh(RefreshTrigger::Background);
        tokio::pin!(background);
        assert!(futures::poll!(&mut background).is_pending());
        release.send(()).unwrap();
        // The single blocking worker finished publication. Leave its caller unpolled.
        tokio::task::spawn_blocking(|| ()).await.unwrap();
        let runtime = StatsigRuntime::get_runtime();
        let init = adapter
            .clone()
            .start(&runtime, Arc::new(Listener::default()));
        tokio::pin!(init);
        assert!(futures::poll!(&mut init).is_pending());
        assert_eq!(provider.manifest_attempts(), 1);
        background.await.unwrap();
        init.await.unwrap();
        let mut contexts = vec![];
        while let Ok(event) = events.try_recv() {
            if let OpsStatsEvent::Diagnostics(event) = event {
                if let Some(context) = event.context {
                    contexts.push((context, event.should_enqueue));
                }
            }
        }
        assert_eq!(
            contexts,
            [
                (ContextType::ConfigSync, false),
                (ContextType::ConfigSync, true),
                (ContextType::Initialize, false)
            ]
        );
    });
}

#[tokio::test]
#[serial]
async fn aborted_partial_batch_reports_completed_files_and_only_id_list_cancellation() {
    use crate::observability::ops_stats::OpsStatsEvent;
    let (provider, adapter, listener) = setup(&["a", "b"]);
    let mut events = adapter.ops_stats.subscribe_for_test();
    let pending_url = "https://files.test/b";
    provider.gate(pending_url);
    let refresh = start(adapter.clone());
    until(|| {
        provider.attempts("b") == 1
            && provider.attempts("a") == 1
            && provider.active.load(Ordering::SeqCst) == 1
    })
    .await;
    refresh.abort();
    assert!(refresh.await.unwrap_err().is_cancelled());
    assert!(listener.publications.lock().is_empty());
    {
        let request = adapter.network.request_once(
            HttpMethod::GET,
            RequestArgs {
                url: pending_url.to_owned(),
                diagnostics_key: Some(KeyType::DownloadConfigSpecs),
                ..RequestArgs::new()
            },
            None,
            false,
            true,
            0,
        );
        tokio::pin!(request);
        assert!(futures::poll!(&mut request).is_pending());
    }
    let mut id_ends = 0;
    let mut dcs_starts = 0;
    let mut process_ends = 0;
    let mut summaries = 0;
    while let Ok(event) = events.try_recv() {
        match event {
            OpsStatsEvent::Diagnostics(event) => {
                if let Some(marker) = event.marker {
                    let marker = serde_json::to_value(marker).unwrap();
                    if marker["url"] == pending_url && marker["step"] == "network_request" {
                        if marker["key"] == "download_config_specs" {
                            assert_eq!(marker["action"], "start");
                            dcs_starts += 1;
                        } else if marker["action"] == "end" {
                            assert_eq!(marker["success"], false);
                            id_ends += 1;
                        }
                    }
                    if marker["key"] == "get_id_list_sources"
                        && marker["step"] == "process"
                        && marker["action"] == "end"
                    {
                        assert_eq!(marker["success"], false);
                        process_ends += 1;
                    }
                }
            }
            OpsStatsEvent::Observability(event)
                if event.metric_name == ID_LISTS_SYNC_OVERALL_LATENCY_METRIC =>
            {
                let tags = event.tags.as_ref().unwrap();
                assert_eq!(tags["succeed_single_id_list_number"], "1");
                assert_eq!(tags["id_lists_sync_success"], "false");
                summaries += 1;
            }
            _ => {}
        }
    }
    assert_eq!((id_ends, process_ends, summaries, dcs_starts), (1, 1, 1, 1));
}

#[tokio::test(start_paused = true)]
#[serial]
async fn serialized_shutdown_during_file_backoff_does_not_retry() {
    let (provider, adapter, listener) = setup(&["a"]);
    provider.set("a", vec![Outcome::Timeout]);
    let refresh = adapter.sync_id_lists();
    tokio::pin!(refresh);
    assert!(futures::poll!(&mut refresh).is_pending());
    assert_eq!(provider.attempts("a"), 1);
    assert_eq!(provider.active.load(Ordering::SeqCst), 0);
    adapter.force_shutdown();
    tokio::time::advance(Duration::from_secs(2)).await;
    assert!(refresh.await.is_err());
    assert_eq!(provider.attempts("a"), 1);
    assert!(listener.publications.lock().is_empty());
}
