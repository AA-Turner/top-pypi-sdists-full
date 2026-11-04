use super::*;
use crate::SpecStore;
use crate::networking::{HttpMethod, NetworkProvider, Response};
use crate::sdk_event_emitter::SdkEventEmitter;
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
    let (provider, adapter, store) = setup(None);

    adapter.sync_id_lists().await.unwrap();

    assert_eq!(provider.file_attempts("default"), 1);
    assert_eq!(provider.file_attempts("selected"), 1);
    assert_eq!(provider.file_attempts("lazy"), 1);
    assert_eq!(store.load_data().id_lists.len(), 3);
}

#[tokio::test]
async fn lazy_initialization_downloads_no_list_bodies() {
    let (provider, adapter, store) = setup(Some(true));

    adapter.sync_id_lists().await.unwrap();

    assert_eq!(provider.file_attempts("default"), 0);
    assert_eq!(provider.file_attempts("selected"), 0);
    assert_eq!(provider.file_attempts("lazy"), 0);
    assert!(store.load_data().id_lists.is_empty());
}

#[tokio::test]
async fn on_demand_load_uses_latest_polled_manifest_and_stays_refreshed() {
    let (provider, adapter, store) = setup(Some(true));
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
    let (provider, adapter, _) = setup(Some(true));
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
    let (provider, adapter, _) = setup(Some(true));
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
    let mut tasks = Vec::new();
    for index in 0..8 {
        let adapter = adapter.clone();
        tasks.push(tokio::spawn(async move {
            adapter.process_id_list(&format!("lazy-{index}")).await
        }));
    }

    tokio::time::timeout(Duration::from_secs(3), async {
        loop {
            let attempts = (0..8)
                .map(|index| provider.file_attempts(&format!("lazy-{index}")))
                .sum::<usize>();
            if attempts == ID_LIST_DOWNLOAD_CONCURRENCY {
                break;
            }
            tokio::task::yield_now().await;
        }
    })
    .await
    .unwrap();
    tokio::time::sleep(Duration::from_millis(25)).await;
    let attempts = (0..8)
        .map(|index| provider.file_attempts(&format!("lazy-{index}")))
        .sum::<usize>();
    assert_eq!(attempts, ID_LIST_DOWNLOAD_CONCURRENCY);

    gate.add_permits(8);
    for task in tasks {
        task.await.unwrap().unwrap();
    }
}

#[tokio::test]
async fn stalled_manifest_poll_does_not_block_unrelated_cold_load() {
    let (provider, adapter, store) = setup(Some(true));
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
    let (provider, adapter, old_store) = setup(Some(true));
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

    let (_, _, replacement) = setup(Some(true));
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
