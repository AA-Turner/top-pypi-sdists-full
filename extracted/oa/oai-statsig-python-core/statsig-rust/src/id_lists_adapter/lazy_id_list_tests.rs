use super::*;
use crate::SpecStore;
use crate::networking::{HttpMethod, NetworkProvider, Response};
use crate::sdk_event_emitter::SdkEventEmitter;
use futures::FutureExt;
use parking_lot::Mutex;
use serde_json::{Value, json};
use tokio::sync::Semaphore;

const MANIFEST_URL: &str = "https://manifest.test/lists";

struct Provider {
    manifest: Mutex<Value>,
    bodies: Mutex<HashMap<String, String>>,
    requests: Mutex<Vec<RequestArgs>>,
    file_gate: Mutex<Option<Arc<Semaphore>>>,
    manifest_gate: Mutex<Option<Arc<Semaphore>>>,
}

#[async_trait]
impl NetworkProvider for Provider {
    async fn send(&self, _: &HttpMethod, args: &RequestArgs) -> Response {
        self.requests.lock().push(args.clone());
        if args.url == MANIFEST_URL {
            let gate = self.manifest_gate.lock().clone();
            if let Some(gate) = gate {
                gate.acquire().await.unwrap().forget();
            }
            return Response {
                status_code: Some(200),
                data: Some(ResponseData::from_bytes(
                    serde_json::to_vec(&*self.manifest.lock()).unwrap(),
                )),
                error: None,
            };
        }
        let gate = self.file_gate.lock().clone();
        if let Some(gate) = gate {
            gate.acquire().await.unwrap().forget();
        }
        let body = self
            .bodies
            .lock()
            .get(&args.url)
            .cloned()
            .expect("unexpected ID-list URL");
        Response {
            status_code: Some(200),
            data: Some(ResponseData::from_bytes(body.into_bytes())),
            error: None,
        }
    }
}

impl Provider {
    fn manifest_attempts(&self) -> usize {
        self.requests
            .lock()
            .iter()
            .filter(|request| request.url == MANIFEST_URL)
            .count()
    }

    fn file_attempts(&self, name: &str) -> usize {
        let url = file_url(name);
        self.requests
            .lock()
            .iter()
            .filter(|request| request.url == url)
            .count()
    }
}

fn file_url(name: &str) -> String {
    format!("https://files.test/{name}")
}

fn manifest_entry(name: &str, size: u64) -> Value {
    json!({
        "name": name,
        "url": file_url(name),
        "fileID": "generation-1",
        "size": size,
        "creationTime": 1,
    })
}

fn setup(
    lazy_load_id_lists: Option<bool>,
    private_elias_fano: bool,
) -> (
    Arc<Provider>,
    Arc<StatsigHttpIdListsAdapter>,
    Arc<SpecStore>,
) {
    let provider = Arc::new(Provider {
        manifest: Mutex::new(json!({
            "default": manifest_entry("default", 3),
            "selected": manifest_entry("selected", 3),
            "lazy": manifest_entry("lazy", 3),
        })),
        bodies: Mutex::new(HashMap::from([
            (file_url("default"), "+a\n".into()),
            (file_url("selected"), "+a\n".into()),
            (file_url("lazy"), "+a\n".into()),
        ])),
        requests: Mutex::new(Vec::new()),
        file_gate: Mutex::new(None),
        manifest_gate: Mutex::new(None),
    });
    let options = StatsigOptions {
        id_lists_url: Some(MANIFEST_URL.into()),
        lazy_load_id_lists,
        enable_id_list_elias_fano: Some(private_elias_fano),
        ..StatsigOptions::default()
    };
    let mut adapter = StatsigHttpIdListsAdapter::new("secret-lazy-list-test", &options);
    let network: Arc<dyn NetworkProvider> = provider.clone();
    adapter
        .network
        .set_network_provider_for_test(Arc::downgrade(&network));
    let store = Arc::new(SpecStore::new(
        "secret-lazy-list-test",
        "lazy-list-test".into(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    ));
    adapter.set_listener(store.clone());
    (provider, Arc::new(adapter), store)
}

#[tokio::test]
async fn initialization_remains_eager_by_default() {
    let (provider, adapter, store) = setup(None, false);

    adapter.sync_id_lists().await.unwrap();

    assert_eq!(provider.file_attempts("default"), 1);
    assert_eq!(provider.file_attempts("selected"), 1);
    assert_eq!(provider.file_attempts("lazy"), 1);
    assert_eq!(store.load_data().id_lists.len(), 3);
}

#[tokio::test]
async fn lazy_initialization_downloads_no_list_bodies() {
    let (provider, adapter, store) = setup(Some(true), false);

    adapter.sync_id_lists().await.unwrap();

    assert_eq!(provider.file_attempts("default"), 0);
    assert_eq!(provider.file_attempts("selected"), 0);
    assert_eq!(provider.file_attempts("lazy"), 0);
    assert!(store.load_data().id_lists.is_empty());
}

#[tokio::test]
async fn on_demand_load_uses_latest_polled_manifest_and_stays_refreshed() {
    let (provider, adapter, store) = setup(Some(true), false);
    adapter.sync_id_lists().await.unwrap();

    provider.manifest.lock()["lazy"] = manifest_entry("lazy", 6);
    provider
        .bodies
        .lock()
        .insert(file_url("lazy"), "+a\n+b\n".into());
    adapter.sync_id_lists().await.unwrap();

    assert_eq!(provider.manifest_attempts(), 2);
    assert_eq!(provider.file_attempts("lazy"), 0);
    adapter.process_id_list("lazy").await.unwrap();

    assert_eq!(provider.manifest_attempts(), 2);
    assert_eq!(provider.file_attempts("lazy"), 1);
    assert_eq!(store.load_data().id_lists.len(), 1);
    assert!(store.load_data().id_lists["lazy"].ids.contains("b"));

    provider.manifest.lock()["lazy"] = manifest_entry("lazy", 9);
    provider
        .bodies
        .lock()
        .insert(file_url("lazy"), "+a\n+b\n+c\n".into());
    adapter.sync_id_lists().await.unwrap();

    assert_eq!(provider.file_attempts("lazy"), 2);
    let data = store.load_data();
    let lazy = &data.id_lists["lazy"];
    assert!(lazy.ids.contains("a"));
    assert!(lazy.ids.contains("b"));
    assert!(lazy.ids.contains("c"));
}

#[tokio::test]
async fn concurrent_on_demand_loads_share_one_download() {
    let (provider, adapter, _) = setup(Some(true), false);
    adapter.sync_id_lists().await.unwrap();
    let gate = Arc::new(Semaphore::new(0));
    *provider.file_gate.lock() = Some(gate.clone());

    let mut tasks = Vec::new();
    for _ in 0..16 {
        let adapter = adapter.clone();
        tasks.push(tokio::spawn(async move {
            adapter.process_id_list("lazy").await
        }));
    }
    tokio::time::timeout(Duration::from_secs(3), async {
        while provider.file_attempts("lazy") == 0 {
            tokio::task::yield_now().await;
        }
    })
    .await
    .unwrap();
    assert_eq!(provider.file_attempts("lazy"), 1);

    gate.add_permits(1);
    for task in tasks {
        task.await.unwrap().unwrap();
    }
    assert_eq!(provider.file_attempts("lazy"), 1);
}

#[tokio::test]
async fn concurrent_distinct_on_demand_loads_are_globally_bounded() {
    for private_elias_fano in [false, true] {
        check_distinct_download_limit(private_elias_fano).await;
    }
}

async fn check_distinct_download_limit(private_elias_fano: bool) {
    let (provider, adapter, store) = setup(Some(true), private_elias_fano);
    for index in 0..8 {
        let name = format!("lazy-{index}");
        provider.manifest.lock()[name.as_str()] = manifest_entry(&name, 3);
        provider
            .bodies
            .lock()
            .insert(file_url(&name), "+a\n".into());
    }
    adapter.sync_id_lists().await.unwrap();

    let gate = Arc::new(Semaphore::new(0));
    *provider.file_gate.lock() = Some(gate.clone());
    let loads = (0..8).map(|index| {
        let adapter = &adapter;
        async move { adapter.process_id_list(&format!("lazy-{index}")).await }
    });
    // Poll every caller while the provider holds all body requests open.
    let mut loads = std::pin::pin!(futures::future::try_join_all(loads));
    assert!(futures::poll!(&mut loads).is_pending());
    let active = provider
        .requests
        .lock()
        .iter()
        .filter(|r| r.url != MANIFEST_URL)
        .count();
    assert_eq!(active, ID_LIST_DOWNLOAD_CONCURRENCY);

    gate.add_permits(8);
    loads.await.unwrap();
    assert_eq!(store.load_data().id_lists.len(), 8);
}

#[tokio::test]
async fn stalled_manifest_poll_does_not_block_unrelated_cold_load() {
    let (provider, adapter, store) = setup(Some(true), false);
    adapter.sync_id_lists().await.unwrap();

    let manifest_gate = Arc::new(Semaphore::new(0));
    *provider.manifest_gate.lock() = Some(manifest_gate.clone());
    let polling = {
        let adapter = Arc::clone(&adapter);
        tokio::spawn(async move { adapter.sync_id_lists().await })
    };
    tokio::time::timeout(Duration::from_secs(3), async {
        while provider.manifest_attempts() < 2 {
            tokio::task::yield_now().await;
        }
    })
    .await
    .unwrap();

    tokio::time::timeout(Duration::from_millis(100), adapter.process_id_list("lazy"))
        .await
        .expect("stalled polling should not hold the lazy-load publication barrier")
        .unwrap();
    assert!(store.load_data().id_lists.contains_key("lazy"));

    manifest_gate.add_permits(1);
    polling.await.unwrap().unwrap();
}

#[tokio::test]
async fn cold_load_finishes_on_the_replacement_listener() {
    let (provider, adapter, old_store) = setup(Some(true), true);
    adapter.sync_id_lists().await.unwrap();
    let gate = Arc::new(Semaphore::new(0));
    *provider.file_gate.lock() = Some(gate.clone());
    let load = {
        let adapter = adapter.clone();
        tokio::spawn(async move { adapter.process_id_list("lazy").await })
    };
    tokio::time::timeout(Duration::from_secs(3), async {
        while provider.file_attempts("lazy") == 0 {
            tokio::task::yield_now().await;
        }
    })
    .await
    .unwrap();

    let (_, _, replacement) = setup(Some(true), false);
    adapter
        .clone()
        .start(&StatsigRuntime::get_runtime(), replacement.clone())
        .await
        .unwrap();
    gate.add_permits(2);
    load.await.unwrap().unwrap();
    assert!(!old_store.load_data().id_lists.contains_key("lazy"));
    assert_eq!(replacement.get_current_id_list_metadata()["lazy"].size, 3);
}

#[tokio::test]
async fn polling_a_warm_list_preserves_a_new_cold_lists_partial_cursor() {
    let (provider, adapter, store) = setup(Some(true), true);
    provider.manifest.lock()["lazy"] = manifest_entry("lazy", 9);
    adapter.sync_id_lists().await.unwrap();
    adapter.process_id_list("selected").await.unwrap();

    // Pause the poll's append. The cold list was absent when this poll selected its jobs.
    provider.manifest.lock()["selected"] = manifest_entry("selected", 6);
    provider
        .bodies
        .lock()
        .insert(file_url("selected"), "+a\n+b\n".into());
    let gate = Arc::new(Semaphore::new(0));
    *provider.file_gate.lock() = Some(gate.clone());
    let mut poll = adapter.sync_id_lists().boxed_local();
    assert!(futures::poll!(&mut poll).is_pending());
    assert_eq!(provider.file_attempts("selected"), 2);
    *provider.file_gate.lock() = None;
    adapter.process_id_list("lazy").await.unwrap();
    gate.add_permits(1);
    poll.await.unwrap();

    let installed = store.get_current_id_list_metadata();
    assert_eq!(installed.get("lazy").map(|entry| entry.size), Some(3));
    provider
        .bodies
        .lock()
        .insert(file_url("lazy"), "+a\n+b\n+c\n".into());
    adapter.sync_id_lists().await.unwrap();
    let requests = provider.requests.lock();
    let ranges: Vec<_> = requests
        .iter()
        .filter(|r| r.url == file_url("lazy"))
        .map(|r| r.headers.as_ref().unwrap()["Range"].as_str())
        .collect();
    assert_eq!(ranges, ["bytes=0-", "bytes=3-"]);
    assert!(store.load_data().id_lists["lazy"].ids.contains("c"));
}

#[tokio::test]
async fn overlapping_lazy_poll_and_materialization_resume_from_the_committed_cursor() {
    for poll_first in [true, false] {
        let (provider, adapter, store) = setup(Some(true), true);
        provider.manifest.lock()["lazy"] = manifest_entry("lazy", 9);
        adapter.sync_id_lists().await.unwrap();
        adapter.process_id_list("lazy").await.unwrap();

        // The body is behind the manifest. Both requests start at byte three.
        let gate = Arc::new(Semaphore::new(0));
        *provider.file_gate.lock() = Some(gate.clone());
        provider
            .bodies
            .lock()
            .insert(file_url("lazy"), "+a\n+b\n".into());
        let mut poll = adapter.sync_id_lists().boxed_local();
        let mut load = adapter.process_id_list("lazy").boxed_local();
        assert!(futures::poll!(&mut poll).is_pending());
        assert!(futures::poll!(&mut load).is_pending());
        assert_eq!(provider.file_attempts("lazy"), 3);

        // Wake both requests, but only poll the first caller to completion.
        gate.add_permits(2);
        let (first, second) = if poll_first {
            (poll, load)
        } else {
            (load, poll)
        };
        first.await.unwrap();
        assert_eq!(store.get_current_id_list_metadata()["lazy"].size, 6);
        provider
            .bodies
            .lock()
            .insert(file_url("lazy"), "+a\n+b\n+c\n".into());
        gate.add_permits(1);
        second.await.unwrap();

        let requests = provider.requests.lock();
        let ranges: Vec<_> = requests
            .iter()
            .filter(|r| r.url == file_url("lazy"))
            .map(|r| r.headers.as_ref().unwrap()["Range"].as_str())
            .collect();
        assert_eq!(ranges, ["bytes=0-", "bytes=3-", "bytes=3-", "bytes=6-"]);
        let snapshot = store.load_data();
        assert_eq!(snapshot.id_lists["lazy"].metadata.size, 9);
        assert!(snapshot.id_lists["lazy"].ids.contains("c"));
    }
}

#[test]
fn cancelled_lazy_caller_drains_its_worker_before_same_name_retry() {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .max_blocking_threads(1)
        .enable_all()
        .build()
        .unwrap();
    runtime.block_on(async {
        let (provider, adapter, store) = setup(Some(true), true);
        adapter.sync_id_lists().await.unwrap();

        // Occupy the publication worker so the first caller can be dropped after
        // submitting its callback but before the callback installs the list.
        let (release, wait) = std::sync::mpsc::channel();
        let blocker =
            tokio::task::spawn_blocking(move || wait.recv_timeout(Duration::from_secs(5)).unwrap());
        {
            let mut first = Box::pin(adapter.process_id_list("lazy"));
            assert!(futures::poll!(&mut first).is_pending());
            assert_eq!(provider.file_attempts("lazy"), 1);
        }
        let mut retry = Box::pin(adapter.process_id_list("lazy"));
        assert!(futures::poll!(&mut retry).is_pending());
        assert_eq!(provider.file_attempts("lazy"), 1);
        release.send(()).unwrap();
        blocker.await.unwrap();
        retry.await.unwrap();

        assert_eq!(provider.file_attempts("lazy"), 1);
        assert_eq!(store.get_current_id_list_metadata()["lazy"].size, 3);
    });
}
