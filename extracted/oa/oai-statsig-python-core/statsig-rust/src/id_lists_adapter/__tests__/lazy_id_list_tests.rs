use super::*;
use crate::SpecStore;
use crate::networking::{HttpMethod, NetworkProvider, Response};
use crate::sdk_event_emitter::SdkEventEmitter;
use futures::FutureExt;
use parking_lot::Mutex;
use rusty_fork::rusty_fork_test;
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
    setup_with_options(StatsigOptions {
        lazy_load_id_lists,
        enable_id_list_elias_fano: Some(private_elias_fano),
        ..StatsigOptions::default()
    })
}

fn setup_parallel(
    private_elias_fano: bool,
) -> (
    Arc<Provider>,
    Arc<StatsigHttpIdListsAdapter>,
    Arc<SpecStore>,
) {
    setup_with_options(StatsigOptions {
        lazy_load_id_lists: Some(true),
        experimental_flags: Some(["parallel_lazy_id_list_builds".to_owned()].into()),
        enable_id_list_elias_fano: Some(private_elias_fano),
        ..StatsigOptions::default()
    })
}

fn setup_with_options(
    options: StatsigOptions,
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
        ..options
    };
    let store = Arc::new(SpecStore::new(
        "secret-lazy-list-test",
        "lazy-list-test".into(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    ));
    let mut adapter =
        StatsigHttpIdListsAdapter::new_with_store("secret-lazy-list-test", &options, store.clone());
    let network: Arc<dyn NetworkProvider> = provider.clone();
    adapter
        .network
        .set_network_provider_for_test(Arc::downgrade(&network));
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
    let (provider, adapter, old_store) = setup_parallel(true);
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
    let old_store = Arc::into_inner(old_store).expect("adapter retained the replaced store");
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
fn parallel_lazy_builds_require_explicit_opt_in() {
    for flag in [false, true] {
        let options = StatsigOptions {
            experimental_flags: flag.then(|| ["parallel_lazy_id_list_builds".to_owned()].into()),
            ..StatsigOptions::default()
        };
        for (env, expected) in [
            (None, flag),
            (Some("true"), true),
            (Some("false"), false),
            (Some("TRUE"), false),
            (Some(""), false),
            (Some("1"), false),
        ] {
            assert_eq!(
                parallel_lazy_builds_enabled(&options, env.map(std::ffi::OsStr::new)),
                expected,
                "flag={flag}, env={env:?}"
            );
        }
    }
}

rusty_fork_test! {
    #[test]
    fn process_opt_out_keeps_flagged_lazy_instances_on_serial_publication() {
        // This test runs in its own child process, before starting the SDK runtime.
        unsafe { std::env::set_var("STATSIG_PARALLEL_LAZY_ID_LIST_BUILDS", "false"); }
        let (provider, adapter, store) = setup_parallel(false);
        assert!(adapter.lazy_id_lists.as_ref().unwrap().build_permits.is_none());
        tokio::runtime::Builder::new_current_thread().enable_all().build().unwrap().block_on(async {
            adapter.sync_id_lists().await.unwrap();
            assert_eq!(provider.file_attempts("lazy"), 0);
            adapter.process_id_list("lazy").await.unwrap();
            assert!(store.load_data().id_lists["lazy"].ids.contains("a"));
        });
    }

    #[test]
    fn process_opt_in_applies_only_to_private_lazy_adapters() {
        unsafe { std::env::set_var("STATSIG_PARALLEL_LAZY_ID_LIST_BUILDS", "true"); }
        let (_, lazy, _) = setup(Some(true), false);
        let (_, eager, _) = setup(None, false);
        let standalone = StatsigHttpIdListsAdapter::new("standalone", &StatsigOptions {
            lazy_load_id_lists: Some(true), ..Default::default()
        });
        assert!(lazy.lazy_id_lists.as_ref().unwrap().build_permits.is_some());
        assert!(eager.lazy_id_lists.is_none());
        assert!(standalone.lazy_id_lists.as_ref().unwrap().build_permits.is_none());
    }
}

#[tokio::test]
async fn cancelling_the_only_caller_before_build_releases_its_download() {
    let (provider, adapter, store) = setup_parallel(false);
    adapter.sync_id_lists().await.unwrap();
    let gate = Arc::new(Semaphore::new(0));
    *provider.file_gate.lock() = Some(gate.clone());

    let mut first = Box::pin(adapter.process_id_list("lazy"));
    assert!(futures::poll!(&mut first).is_pending());
    assert_eq!(provider.file_attempts("lazy"), 1);
    drop(first);

    let mut retry = Box::pin(adapter.process_id_list("lazy"));
    assert!(futures::poll!(&mut retry).is_pending());
    assert_eq!(provider.file_attempts("lazy"), 2);
    gate.add_permits(1);
    tokio::time::timeout(Duration::from_secs(3), retry)
        .await
        .unwrap()
        .unwrap();
    assert!(store.load_data().id_lists["lazy"].ids.contains("a"));
}

#[test]
fn hash_publication_timeout_is_reported_only_on_the_opted_in_path_and_retry_installs() {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();
    for parallel in [false, true] {
        let (provider, adapter, store) = if parallel {
            setup_parallel(false)
        } else {
            setup(Some(true), false)
        };
        runtime.block_on(adapter.sync_id_lists()).unwrap();
        assert_eq!(
            adapter
                .lazy_id_lists
                .as_ref()
                .unwrap()
                .build_permits
                .is_some(),
            parallel
        );
        let result = store.with_id_list_mutation_locked_for_test(|| {
            runtime.block_on(adapter.process_id_list("lazy"))
        });
        if parallel {
            assert!(matches!(result, Err(StatsigErr::LockFailure(_))));
        } else {
            result.expect("legacy hash publication treats lock timeout as a skipped update");
        }
        assert!(store.load_data().id_lists.is_empty());
        runtime.block_on(adapter.process_id_list("lazy")).unwrap();
        assert_eq!(provider.file_attempts("lazy"), 2);
        assert!(store.load_data().id_lists["lazy"].ids.contains("a"));
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
        let (provider, adapter, store) = setup_parallel(true);
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
            // Cancellation need not happen on a Tokio thread.
            std::thread::scope(|scope| scope.spawn(move || drop(first)).join().unwrap());
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

fn on_index_build(
    adapter: &mut Arc<StatsigHttpIdListsAdapter>,
    hook: impl Fn(&str) + Send + Sync + 'static,
) {
    let adapter = Arc::get_mut(adapter).unwrap();
    adapter.lazy_id_lists.as_mut().unwrap().before_build = Some(Arc::new(hook));
}

/// Pause the first build of "lazy". Dropping the release sender also unblocks the worker.
fn pause_lazy_build(
    adapter: &mut Arc<StatsigHttpIdListsAdapter>,
) -> (impl Future<Output = ()>, std::sync::mpsc::Sender<()>) {
    let (started, ready) = tokio::sync::oneshot::channel();
    let (release, resume) = std::sync::mpsc::channel();
    let channels = Mutex::new(Some((started, resume)));
    on_index_build(adapter, move |name| {
        if name == "lazy" {
            let first = channels.lock().take();
            if let Some((started, resume)) = first {
                started.send(()).unwrap();
                let _ = resume.recv_timeout(Duration::from_secs(10));
            }
        }
    });
    let wait_for_start = async move {
        tokio::time::timeout(Duration::from_secs(3), ready)
            .await
            .expect("lazy index build did not start")
            .unwrap();
    };
    (wait_for_start, release)
}

#[tokio::test]
async fn another_cold_list_is_usable_while_one_index_is_building() {
    for elias_fano in [false, true] {
        let (provider, mut adapter, store) = setup_parallel(elias_fano);
        let (ready, release) = pause_lazy_build(&mut adapter);
        for name in ["lazy", "selected"] {
            provider.manifest.lock()[name] = manifest_entry(name, 10);
            provider
                .bodies
                .lock()
                .insert(file_url(name), "+AAAAAAAA\n".into());
        }
        adapter
            .clone()
            .start(&StatsigRuntime::get_runtime(), store.clone())
            .await
            .unwrap();
        let first = tokio::spawn({
            let adapter = adapter.clone();
            async move { adapter.process_id_list("lazy").await }
        });
        ready.await;
        tokio::time::timeout(Duration::from_secs(3), adapter.process_id_list("selected"))
            .await
            .expect("unrelated index waited for lazy")
            .unwrap();
        let during = store.load_data();
        assert!(during.id_lists["selected"].ids.contains("AAAAAAAA"));
        assert!(!during.id_lists.contains_key("lazy"));
        release.send(()).unwrap();
        first.await.unwrap().unwrap();
        let after = store.load_data();
        assert!(after.id_lists["lazy"].ids.contains("AAAAAAAA"));
        assert!(after.id_lists["selected"].ids.contains("AAAAAAAA"));
        assert_eq!(provider.file_attempts("selected"), 1);
        assert_eq!(provider.file_attempts("lazy"), 1);
    }
}

#[tokio::test]
async fn manifest_can_remove_or_replace_a_list_during_its_build() {
    for removed in [true, false] {
        let (provider, mut adapter, store) = setup_parallel(true);
        let (ready, release) = pause_lazy_build(&mut adapter);
        adapter.sync_id_lists().await.unwrap();
        let load = tokio::spawn({
            let adapter = adapter.clone();
            async move { adapter.process_id_list("lazy").await }
        });
        ready.await;
        if removed {
            provider
                .manifest
                .lock()
                .as_object_mut()
                .unwrap()
                .remove("lazy");
        } else {
            provider.manifest.lock()["lazy"]["fileID"] = json!("generation-2");
            provider.manifest.lock()["lazy"]["creationTime"] = json!(2);
            provider
                .bodies
                .lock()
                .insert(file_url("lazy"), "+b\n".into());
        }
        tokio::time::timeout(Duration::from_secs(3), adapter.sync_id_lists())
            .await
            .unwrap()
            .unwrap();
        release.send(()).unwrap();
        let result = load.await.unwrap();
        let snapshot = store.load_data();
        if removed {
            assert!(result.is_err());
            assert!(!snapshot.id_lists.contains_key("lazy"));
            assert_eq!(provider.file_attempts("lazy"), 1);
        } else {
            result.unwrap();
            let list = &snapshot.id_lists["lazy"];
            assert_eq!(list.metadata.file_id.as_deref(), Some("generation-2"));
            assert!(list.ids.contains("b"));
            assert!(!list.ids.contains("a"));
            assert_eq!(provider.file_attempts("lazy"), 2);
        }
    }
}

#[test]
fn a_queued_poll_and_a_cold_build_can_share_one_blocking_worker() {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .max_blocking_threads(1)
        .enable_all()
        .build()
        .unwrap();
    let result = runtime.block_on(async {
        let (_provider, mut adapter, store) = setup_parallel(true);
        let (ready, release) = pause_lazy_build(&mut adapter);
        adapter.sync_id_lists().await.unwrap();
        let mut cold = std::pin::pin!(adapter.process_id_list("lazy"));
        assert!(futures::poll!(&mut cold).is_pending());
        ready.await;

        // The poll owns the manifest while its publication waits for the occupied worker.
        let mut poll = std::pin::pin!(adapter.sync_id_lists());
        assert!(futures::poll!(&mut poll).is_pending());
        assert!(
            adapter
                .lazy_id_lists
                .as_ref()
                .unwrap()
                .manifest
                .try_read()
                .is_err()
        );
        release.send(()).unwrap();
        tokio::time::timeout(Duration::from_secs(3), async {
            futures::try_join!(cold, poll).unwrap();
            assert!(store.load_data().id_lists["lazy"].ids.contains("a"));
        })
        .await
    });
    runtime.shutdown_background();
    result.expect("private build must release the worker before waiting for the manifest");
}

#[test]
fn only_two_private_index_builds_run_at_once() {
    // The third blocking thread runs the witness below once all submitted builds
    // have started. With three builds stalled, that witness could never run.
    let runtime = tokio::runtime::Builder::new_current_thread()
        .max_blocking_threads(3)
        .enable_all()
        .build()
        .unwrap();
    runtime.block_on(async {
        let (_provider, mut adapter, store) = setup_parallel(true);
        let (entered, mut started) = tokio::sync::mpsc::unbounded_channel();
        on_index_build(&mut adapter, move |_| {
            let (release, wait) = std::sync::mpsc::channel::<()>();
            entered.send(release).unwrap();
            let _ = wait.recv_timeout(Duration::from_secs(10));
        });
        adapter.sync_id_lists().await.unwrap();
        let names = ["lazy", "default", "selected"];
        let requests = names.map(|name| adapter.process_id_list(name));
        let mut loads = futures::future::try_join_all(requests).boxed();
        assert!(futures::poll!(&mut loads).is_pending());
        let (first, second) = tokio::time::timeout(Duration::from_secs(3), async {
            (started.recv().await.unwrap(), started.recv().await.unwrap())
        })
        .await
        .expect("two independent builds should start");

        tokio::time::timeout(Duration::from_secs(3), tokio::task::spawn_blocking(|| ()))
            .await
            .expect("three builds are occupying the pool")
            .unwrap();
        assert!(started.try_recv().is_err());
        first.send(()).unwrap();
        tokio::time::timeout(Duration::from_secs(3), async {
            let third = tokio::select! {
                result = &mut loads => panic!("loads returned while a build was paused: {result:?}"),
                next = started.recv() => next.unwrap(),
            };
            third.send(()).unwrap();
            second.send(()).unwrap();
            loads.await.unwrap();
        })
        .await
        .expect("the queued build and all requests should finish once slots are released");
        for name in names {
            assert!(store.load_data().id_lists[name].ids.contains("a"));
        }
    });
}

#[tokio::test]
async fn same_cursor_with_replaced_membership_rebuilds_the_delta() {
    let (provider, mut adapter, store) = setup_parallel(true);
    let (ready, release) = pause_lazy_build(&mut adapter);
    provider.manifest.lock()["lazy"] = manifest_entry("lazy", 6);
    provider
        .bodies
        .lock()
        .insert(file_url("lazy"), "+a\n+b\n".into());
    adapter.sync_id_lists().await.unwrap();

    // A snapshot install can replace membership without changing its file ID or cursor.
    let install_snapshot = |body: &str| {
        let metadata: IdListMetadata = serde_json::from_value(manifest_entry("lazy", 3)).unwrap();
        let mut list = IdList::new(metadata.clone());
        list.apply_update(IdListUpdate {
            raw_changeset: Some(body.into()),
            new_metadata: metadata,
        });
        store
            .did_receive_id_list_snapshot(HashMap::from([("lazy".into(), list)]), HashMap::new())
            .unwrap();
    };
    install_snapshot("+a\n");
    let load = tokio::spawn({
        let adapter = adapter.clone();
        async move { adapter.process_id_list("lazy").await }
    });
    ready.await;
    install_snapshot("+z\n");
    release.send(()).unwrap();
    load.await.unwrap().unwrap();
    let snapshot = store.load_data();
    let list = &snapshot.id_lists["lazy"];
    assert_eq!(list.metadata.size, 6);
    assert!(list.ids.contains("z") && list.ids.contains("b"));
    assert!(!list.ids.contains("a"));
}

#[test]
fn shutdown_drains_an_active_build_and_skips_the_next_queued_build() {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .max_blocking_threads(1)
        .enable_all()
        .build()
        .unwrap();
    runtime.block_on(async {
        let (provider, mut adapter, store) = setup_parallel(true);
        let (entered, mut started) = tokio::sync::mpsc::unbounded_channel();
        let (release, wait) = std::sync::mpsc::channel::<()>();
        let wait = Mutex::new(wait);
        on_index_build(&mut adapter, move |name| {
            entered.send(name.to_owned()).unwrap();
            if name == "lazy" {
                let _ = wait.lock().recv_timeout(Duration::from_secs(10));
            }
        });
        adapter.sync_id_lists().await.unwrap();
        let mut first = adapter.process_id_list("lazy").boxed();
        assert!(futures::poll!(&mut first).is_pending());
        let first_build = tokio::time::timeout(Duration::from_secs(3), started.recv())
            .await
            .expect("first build did not start");
        assert_eq!(first_build.as_deref(), Some("lazy"));
        let mut next = adapter.process_id_list("selected").boxed();
        assert!(futures::poll!(&mut next).is_pending());
        assert_eq!(provider.file_attempts("selected"), 1);

        let mut shutdown = adapter.shutdown(Duration::from_secs(5));
        assert!(futures::poll!(&mut shutdown).is_pending());
        assert!(first.await.is_err());
        assert!(next.await.is_err());
        release.send(()).unwrap();
        shutdown.await.unwrap();
        assert!(started.try_recv().is_err());
        assert!(store.load_data().id_lists.is_empty());
    });
}
