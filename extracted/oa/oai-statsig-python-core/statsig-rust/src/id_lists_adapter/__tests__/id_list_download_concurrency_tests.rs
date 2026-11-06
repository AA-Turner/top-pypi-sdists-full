use super::*;
use crate::SpecStore;
use crate::networking::Response;
use crate::networking::{HttpMethod, NetworkProvider};
use crate::sdk_event_emitter::SdkEventEmitter;
use parking_lot::Mutex;
use std::sync::atomic::{AtomicUsize, Ordering};
use tokio::sync::Semaphore;

const MANIFEST_URL: &str = "https://manifest.test/lists";

#[derive(Clone)]
enum Outcome {
    Body(Vec<u8>),
    MissingBody,
}

impl Outcome {
    fn response(self) -> Response {
        let (status_code, data) = match self {
            Self::Body(bytes) => (200, Some(ResponseData::from_bytes(bytes))),
            Self::MissingBody => (200, None),
        };
        Response {
            status_code: Some(status_code),
            data,
            error: None,
        }
    }
}

#[derive(Default)]
struct Provider {
    manifest: Mutex<IdListsResponse>,
    outcomes: Mutex<HashMap<String, Outcome>>,
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
        if let Some(outcome) = self.outcomes.lock().get(&args.url).cloned() {
            return outcome.response();
        }
        assert_eq!(args.url, MANIFEST_URL, "unexpected request URL");
        Outcome::Body(serde_json::to_vec(&*self.manifest.lock()).unwrap()).response()
    }
}

impl Provider {
    fn set(&self, name: &str, outcome: Outcome) {
        self.outcomes.lock().insert(file_url(name), outcome);
    }

    fn gate(&self, url: &str) -> Arc<Semaphore> {
        let gate = Arc::new(Semaphore::new(0));
        self.gates.lock().insert(url.into(), gate.clone());
        gate
    }

    fn gate_all_files(&self) {
        for entry in self.manifest.lock().values() {
            self.gate(&entry.url);
        }
    }

    fn release(&self, name: &str) {
        self.gates.lock()[&file_url(name)].add_permits(1);
    }

    fn release_all(&self) {
        for gate in self.gates.lock().values() {
            gate.add_permits(16);
        }
    }

    fn file_requests(&self) -> Vec<RequestArgs> {
        self.requests
            .lock()
            .iter()
            .filter(|request| request.url != MANIFEST_URL)
            .cloned()
            .collect()
    }

    fn started_names(&self) -> Vec<String> {
        self.file_requests()
            .iter()
            .map(|request| request.url.rsplit('/').next().unwrap().to_owned())
            .collect()
    }

    fn attempts(&self, name: &str) -> usize {
        self.file_requests()
            .iter()
            .filter(|request| request.url == file_url(name))
            .count()
    }
}

fn file_url(name: &str) -> String {
    format!("https://files.test/{name}")
}

fn metadata(name: &str, size: u64, generation: i64) -> IdListMetadata {
    IdListMetadata {
        name: name.into(),
        url: file_url(name),
        file_id: Some(format!("generation-{generation}")),
        size,
        creation_time: generation,
    }
}

fn setup(
    names: &[&str],
) -> (
    Arc<Provider>,
    Arc<StatsigHttpIdListsAdapter>,
    Arc<SpecStore>,
) {
    setup_with_options(names, StatsigOptions::default(), None)
}

fn setup_with_options(
    names: &[&str],
    options: StatsigOptions,
    before_build: Option<Arc<dyn Fn() + Send + Sync>>,
) -> (
    Arc<Provider>,
    Arc<StatsigHttpIdListsAdapter>,
    Arc<SpecStore>,
) {
    let provider = Arc::new(Provider::default());
    for name in names {
        provider
            .manifest
            .lock()
            .insert((*name).into(), metadata(name, 3, 1));
        provider.set(name, Outcome::Body(b"+a\n".to_vec()));
    }
    let sdk_key = format!("secret-id-lists-{}", uuid::Uuid::new_v4());
    let options = StatsigOptions {
        id_lists_url: Some(MANIFEST_URL.into()),
        ..options
    };
    let mut store = SpecStore::new(
        &sdk_key,
        "id-lists-test".into(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );
    store.before_id_list_build = before_build;
    let store = Arc::new(store);
    let mut adapter = StatsigHttpIdListsAdapter::new(&sdk_key, &options);
    let dynamic: Arc<dyn NetworkProvider> = provider.clone();
    adapter
        .network
        .set_network_provider_for_test(Arc::downgrade(&dynamic));
    adapter.set_listener(store.clone());
    (provider, Arc::new(adapter), store)
}

fn seed(store: &SpecStore, entries: &[(&str, &str, i64)]) {
    store.did_receive_id_list_updates(
        entries
            .iter()
            .map(|(name, body, generation)| {
                (
                    (*name).into(),
                    IdListUpdate {
                        raw_changeset: Some((*body).into()),
                        new_metadata: metadata(name, body.len() as u64, *generation),
                    },
                )
            })
            .collect(),
    );
}

async fn until(condition: impl Fn() -> bool) {
    tokio::time::timeout(Duration::from_secs(3), async {
        while !condition() {
            tokio::task::yield_now().await;
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
async fn id_list_concurrency_is_bounded_to_four_and_refills_slots() {
    let names = ["a", "b", "c", "d", "e", "f"];
    let (provider, adapter, store) = setup(&names);
    provider.gate_all_files();
    let before = store.load_data();
    let task = start(adapter);
    until(|| provider.active.load(Ordering::SeqCst) == 4).await;
    assert_eq!(provider.file_requests().len(), 4);
    assert!(Arc::ptr_eq(&before.id_lists, &store.load_data().id_lists));

    provider.release(&provider.started_names()[0]);
    until(|| provider.file_requests().len() == 5).await;
    assert_eq!(provider.active.load(Ordering::SeqCst), 4);
    assert!(Arc::ptr_eq(&before.id_lists, &store.load_data().id_lists));

    provider.release_all();
    task.await.unwrap().unwrap();
    assert_eq!(provider.peak.load(Ordering::SeqCst), 4);
    assert_eq!(provider.file_requests().len(), names.len());
    assert_eq!(store.load_data().id_lists.len(), names.len());
    assert!(
        store
            .load_data()
            .id_lists
            .values()
            .all(|list| list.ids.contains("a"))
    );
    assert!(
        before.id_lists.is_empty(),
        "old snapshots must remain immutable"
    );
    assert!(
        provider
            .requests
            .lock()
            .iter()
            .all(|request| request.retries == 0)
    );
}

#[tokio::test]
async fn id_list_concurrency_failure_drains_jobs_and_preserves_published_store() {
    let names = ["a", "b", "c", "d", "e", "f"];
    let (provider, adapter, store) = setup(&names);
    seed(&store, &[("retained", "+old\n", 1)]);
    let before = store.load_data();
    provider.gate_all_files();
    let task = start(adapter.clone());
    until(|| provider.active.load(Ordering::SeqCst) == 4).await;
    let first = provider.started_names();
    provider.release(&first[0]);
    until(|| provider.file_requests().len() == 5).await;
    provider.set(&first[1], Outcome::MissingBody);
    provider.release(&first[1]);
    // A failed file must not cancel active or queued independent downloads.
    provider.release_all();
    assert!(task.await.unwrap().is_err());
    assert_eq!(provider.active.load(Ordering::SeqCst), 0);
    assert_eq!(provider.file_requests().len(), names.len() + 1);
    assert_eq!(provider.attempts(&first[1]), 2);
    assert!(Arc::ptr_eq(&before.id_lists, &store.load_data().id_lists));

    provider.gates.lock().clear();
    for name in names {
        provider.set(name, Outcome::Body(b"+z\n".to_vec()));
    }
    adapter.sync_id_lists().await.unwrap();
    for name in names {
        assert_eq!(
            provider.attempts(name),
            if name == first[1] { 3 } else { 2 }
        );
        assert!(store.load_data().id_lists[name].ids.contains("z"));
        assert!(!store.load_data().id_lists[name].ids.contains("a"));
    }
    assert!(!store.load_data().id_lists.contains_key("retained"));
    assert!(before.id_lists["retained"].ids.contains("old"));
}

#[tokio::test]
async fn id_list_concurrency_preserves_ranges_generations_unchanged_and_removal() {
    let (provider, adapter, store) = setup(&["same", "shrink", "grow", "replace"]);
    seed(
        &store,
        &[
            ("same", "+a\n", 1),
            ("shrink", "+a\n+b\n", 1),
            ("grow", "+a\n", 1),
            ("replace", "+a\n", 0),
            ("remove", "+a\n", 1),
        ],
    );
    provider.manifest.lock().get_mut("grow").unwrap().size = 6;
    provider.set("grow", Outcome::Body(b"+a\n+b\n".to_vec()));
    provider.set("replace", Outcome::Body(b"+b\n".to_vec()));
    let before = store.load_data();
    adapter.sync_id_lists().await.unwrap();
    assert_eq!(provider.attempts("same"), 0);
    assert_eq!(provider.attempts("shrink"), 0);
    assert_eq!(provider.attempts("grow"), 1);
    assert_eq!(provider.attempts("replace"), 1);
    for request in provider.file_requests() {
        let expected_range = if request.url == file_url("grow") {
            "bytes=3-"
        } else {
            "bytes=0-"
        };
        assert_eq!(request.headers.as_ref().unwrap()["Range"], expected_range);
        assert_eq!(request.id_list_file_id.as_deref(), Some("generation-1"));
    }
    let published = store.load_data();
    assert_eq!(published.id_lists.len(), 4);
    assert!(!published.id_lists.contains_key("remove"));
    assert!(Arc::ptr_eq(
        &before.id_lists["same"].ids,
        &published.id_lists["same"].ids
    ));
    assert!(Arc::ptr_eq(
        &before.id_lists["shrink"].ids,
        &published.id_lists["shrink"].ids
    ));
    assert!(
        published.id_lists["grow"].ids.contains("a")
            && published.id_lists["grow"].ids.contains("b")
    );
    assert!(!published.id_lists["replace"].ids.contains("a"));
    assert!(published.id_lists["replace"].ids.contains("b"));
    assert!(!before.id_lists["grow"].ids.contains("b"));
}

#[tokio::test]
async fn id_list_concurrency_freezes_manifest_until_the_next_refresh() {
    let (provider, adapter, store) = setup(&["a"]);
    seed(&store, &[("a", "+old\n", 1)]);
    provider
        .manifest
        .lock()
        .insert("a".into(), metadata("a", 8, 1));
    provider.set("a", Outcome::Body(b"+old\n+a\n".to_vec()));
    let gate = provider.gate(&file_url("a"));
    let task = start(adapter.clone());
    until(|| provider.attempts("a") == 1).await;
    provider
        .manifest
        .lock()
        .insert("a".into(), metadata("a", 3, 2));
    gate.add_permits(1);
    task.await.unwrap().unwrap();
    let first = provider.file_requests()[0].clone();
    assert_eq!(first.id_list_file_id.as_deref(), Some("generation-1"));
    assert_eq!(first.headers.as_ref().unwrap()["Range"], "bytes=5-");
    assert_eq!(
        first.headers.as_ref().unwrap()["statsig-id-list-file-size"],
        "8"
    );
    assert!(store.load_data().id_lists["a"].ids.contains("old"));

    provider.set("a", Outcome::Body(b"+a\n".to_vec()));
    gate.add_permits(1);
    adapter.sync_id_lists().await.unwrap();
    let second = provider.file_requests()[1].clone();
    assert_eq!(second.id_list_file_id.as_deref(), Some("generation-2"));
    assert_eq!(second.headers.as_ref().unwrap()["Range"], "bytes=0-");
    assert!(!store.load_data().id_lists["a"].ids.contains("old"));
}

#[tokio::test]
async fn id_list_concurrency_empty_manifest_publishes_all_removals() {
    let (provider, adapter, store) = setup(&[]);
    seed(&store, &[("removed", "+old\n", 1)]);
    adapter.sync_id_lists().await.unwrap();
    assert_eq!(provider.requests.lock().len(), 1);
    assert!(provider.file_requests().is_empty());
    assert!(store.load_data().id_lists.is_empty());
}

#[tokio::test]
async fn id_list_concurrency_cancellation_drops_active_and_queued_downloads() {
    let (provider, adapter, store) = setup(&["a", "b", "c", "d", "e", "f"]);
    provider.gate_all_files();
    let before = store.load_data();
    let task = {
        let adapter = adapter.clone();
        let store = store.clone();
        tokio::spawn(async move { adapter.start(&StatsigRuntime::get_runtime(), store).await })
    };
    until(|| provider.active.load(Ordering::SeqCst) == 4).await;
    provider.release(&provider.started_names()[0]);
    until(|| provider.file_requests().len() == 5).await;
    task.abort();
    assert!(task.await.unwrap_err().is_cancelled());
    assert_eq!(provider.active.load(Ordering::SeqCst), 0);
    assert_eq!(provider.file_requests().len(), 5);
    provider.release_all();
    tokio::task::yield_now().await;
    assert_eq!(provider.file_requests().len(), 5);
    assert!(Arc::ptr_eq(&before.id_lists, &store.load_data().id_lists));
}

#[tokio::test]
async fn eager_init_publishes_only_to_the_listener_passed_to_start() {
    let (_provider, adapter, original) = setup(&["a", "b"]);
    let runtime = StatsigRuntime::get_runtime();
    let mut replacement = SpecStore::new(
        "secret-replacement",
        "replacement".into(),
        runtime.clone(),
        Arc::new(SdkEventEmitter::default()),
        Some(&StatsigOptions {
            id_list_init_build_concurrency: Some(2),
            ..Default::default()
        }),
    );
    let startup_thread = std::thread::current().id();
    replacement.before_id_list_build = Some(Arc::new(move || {
        assert_ne!(std::thread::current().id(), startup_thread);
    }));
    let replacement = Arc::new(replacement);

    adapter.start(&runtime, replacement.clone()).await.unwrap();
    assert!(original.load_data().id_lists.is_empty());
    let snapshot = replacement.load_data();
    for name in ["a", "b"] {
        assert!(snapshot.id_lists[name].ids.contains("a"));
    }
}

#[test]
fn eager_init_builds_use_the_configured_workers_and_publish_together() {
    use std::sync::mpsc;
    use std::thread;

    for (limit, trigger, elias_fano, expected) in [
        (None, RefreshTrigger::PrivateInitialize, true, 1),
        (Some(1), RefreshTrigger::PrivateInitialize, true, 1),
        (Some(0), RefreshTrigger::PrivateInitialize, true, 1),
        (Some(33), RefreshTrigger::PrivateInitialize, true, 1),
        (Some(2), RefreshTrigger::PrivateInitialize, true, 2),
        (Some(32), RefreshTrigger::PrivateInitialize, true, 4),
        (Some(4), RefreshTrigger::Background, true, 1),
        (Some(4), RefreshTrigger::SharedInitialize, true, 1),
        (Some(2), RefreshTrigger::PrivateInitialize, false, 2),
    ] {
        let (entered, builds) = mpsc::channel();
        let before_build = Arc::new(move || {
            let (release, wait) = mpsc::channel();
            entered.send((thread::current().id(), release)).unwrap();
            wait.recv_timeout(Duration::from_secs(5))
                .expect("test did not release build");
        });
        let names = ["a", "b", "c", "d"];
        let (_provider, adapter, store) = setup_with_options(
            &names,
            StatsigOptions {
                id_list_init_build_concurrency: limit,
                enable_id_list_elias_fano: Some(elias_fano),
                ..Default::default()
            },
            Some(before_build),
        );
        let (finished, completion) = mpsc::channel();
        // A timeout must be able to fail this test even if publication deadlocks.
        let init = thread::spawn(move || {
            let runtime = tokio::runtime::Builder::new_current_thread()
                .max_blocking_threads(1)
                .enable_all()
                .build()
                .unwrap();
            let result = runtime.block_on(adapter.refresh(trigger));
            runtime.shutdown_background();
            let _ = finished.send(result);
        });
        let mut threads = std::collections::HashSet::new();
        let mut paused = Vec::new();
        for i in 0..names.len() {
            let (id, release) = builds
                .recv_timeout(Duration::from_secs(3))
                .expect("an index build should make progress with one Tokio blocking worker");
            threads.insert(id);
            paused.push(release);
            if i + 1 >= expected {
                assert!(
                    store.load_data().id_lists.is_empty(),
                    "a partially built catalog became visible"
                );
                paused.pop().unwrap().send(()).unwrap();
            }
        }
        for release in paused {
            release.send(()).unwrap();
        }
        completion
            .recv_timeout(Duration::from_secs(3))
            .expect("eager publication stalled")
            .unwrap();
        init.join().unwrap();
        assert_eq!(threads.len(), expected, "limit {limit:?}");
        let snapshot = store.load_data();
        assert!(
            names
                .iter()
                .all(|name| snapshot.id_lists[*name].ids.contains("a"))
        );
    }
}

#[tokio::test]
async fn eager_hash_build_yields_to_the_runtime_and_fences_force_shutdown() {
    let (entered, started) = tokio::sync::oneshot::channel();
    let (release, wait) = std::sync::mpsc::channel::<()>();
    let gate = Mutex::new(Some((entered, wait)));
    let (_provider, adapter, store) = setup_with_options(
        &["members"],
        StatsigOptions::builder()
            .id_list_init_build_concurrency(Some(4))
            .build(),
        Some(Arc::new(move || {
            let (entered, wait) = gate.lock().take().unwrap();
            entered.send(()).unwrap();
            wait.recv_timeout(Duration::from_secs(3))
                .expect("hash build blocked the Tokio thread that releases it");
        })),
    );
    let loading = tokio::spawn({
        let adapter = adapter.clone();
        async move { adapter.refresh(RefreshTrigger::PrivateInitialize).await }
    });
    tokio::time::timeout(Duration::from_secs(3), started)
        .await
        .unwrap()
        .unwrap();
    // This runs on the sole async thread while the hash build is still paused.
    let mut stopping = tokio::task::spawn_blocking({
        let adapter = adapter.clone();
        move || adapter.force_shutdown()
    });
    until(|| adapter.network.shutdown_flag().load(Ordering::SeqCst)).await;
    assert!(
        tokio::time::timeout(Duration::from_millis(20), &mut stopping)
            .await
            .is_err(),
        "force_shutdown returned during an entered hash publication"
    );
    release.send(()).unwrap();
    stopping.await.unwrap();
    assert!(store.load_data().id_lists["members"].ids.contains("a"));
    loading.await.unwrap().unwrap();
}
