use super::*;
use crate::{StatsigOptions, StatsigRuntime};
use mockito::{Mock, Server, ServerGuard};
use parking_lot::Mutex;
use serial_test::serial;
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Condvar};
use std::time::Duration;

#[derive(Default)]
struct Listener {
    lists: Mutex<HashMap<String, IdList>>,
    propagation: Mutex<HashMap<String, IdListPropagationUpdate>>,
    after_snapshot: Mutex<Option<Arc<dyn Fn() + Send + Sync>>>,
    reject_next_snapshot: AtomicBool,
    installs: AtomicUsize,
}

impl IdListsUpdateListener for Listener {
    fn get_current_id_list_metadata(&self) -> HashMap<String, IdListMetadata> {
        self.lists
            .lock()
            .iter()
            .map(|(name, list)| (name.clone(), list.metadata.clone()))
            .collect()
    }
    fn did_receive_id_list_updates(&self, updates: HashMap<String, IdListUpdate>) {
        let mut lists = self.lists.lock();
        lists.retain(|name, _| updates.contains_key(name));
        for (name, update) in updates {
            lists
                .entry(name)
                .or_insert_with(|| IdList::new(update.new_metadata.clone()))
                .apply_update(update);
        }
    }
    fn supports_id_list_snapshots(&self) -> bool {
        true
    }
    fn did_receive_id_list_snapshot(
        &self,
        lists: HashMap<String, IdList>,
        propagation: HashMap<String, IdListPropagationUpdate>,
    ) -> Result<(), crate::StatsigErr> {
        if self.reject_next_snapshot.swap(false, Ordering::Relaxed) {
            return Err(crate::StatsigErr::LockFailure(
                "test snapshot lock busy".into(),
            ));
        }
        self.installs.fetch_add(1, Ordering::Relaxed);
        *self.lists.lock() = lists;
        *self.propagation.lock() = propagation;
        let callback = self.after_snapshot.lock().clone();
        if let Some(callback) = callback {
            callback();
        }
        Ok(())
    }
}

struct Fixture {
    server: ServerGuard,
}
impl Fixture {
    async fn new() -> Self {
        Self {
            server: Server::new_async().await,
        }
    }
    fn options(&self, directory: &std::path::Path, service: &str) -> StatsigOptions {
        StatsigOptions {
            id_lists_url: Some(format!("{}/lists", self.server.url())),
            shared_id_lists_dir: Some(directory.to_str().unwrap().to_string()),
            id_lists_sync_interval_ms: Some(50),
            service_name: Some(service.to_string()),
            state_read_primary_attempts: Some(1),
            disable_all_logging: Some(true),
            ..StatsigOptions::default()
        }
    }
    fn manifest(&mut self, size: u64, creation: i64, timestamp: u64, requests: usize) -> Mock {
        self.server.reset();
        self.server
            .mock("POST", "/lists")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(
                serde_json::json!({
                    "members": {
                        "name": "members", "fileID": "file-1", "creationTime": creation, "size": size,
                        "url": format!("{}/members", self.server.url()), "ts": timestamp
                    }
                })
                .to_string(),
            )
            .expect(requests)
            .create()
    }
    fn heartbeat(&mut self, size: u64, timestamp: u64) -> (Mock, Mock) {
        let manifest = self.manifest(size, 1, timestamp, 1);
        let no_download = self.server.mock("GET", "/members").expect(0).create();
        (manifest, no_download)
    }
    fn response(
        &mut self,
        size: u64,
        creation: i64,
        body: Option<(&str, u64)>,
        requests: usize,
        valid_range: bool,
    ) -> (Mock, Option<Mock>) {
        let timestamp = chrono::Utc::now().timestamp_millis().max(1) as u64;
        let manifest = self.manifest(size, creation, timestamp, requests);
        let file = body.map(|(body, start)| {
            let mut mock = self
                .server
                .mock("GET", "/members")
                .match_header("range", format!("bytes={start}-").as_str())
                .with_status(206)
                .with_body(body)
                .expect(requests);
            if valid_range {
                mock = mock.with_header(
                    "content-range",
                    format!("bytes {start}-{}/{size}", start + body.len() as u64 - 1).as_str(),
                );
            }
            mock.create()
        });
        (manifest, file)
    }
}

async fn start(
    fixture: &Fixture,
    directory: &std::path::Path,
    service: &str,
) -> (Arc<StatsigSharedIdListsAdapter>, Arc<Listener>) {
    let adapter = Arc::new(StatsigSharedIdListsAdapter::new(
        "secret-shared-fixture",
        &fixture.options(directory, service),
    ));
    let listener = Arc::new(Listener::default());
    adapter
        .clone()
        .start(&StatsigRuntime::get_runtime(), listener.clone())
        .await
        .unwrap();
    (adapter, listener)
}
fn verify(mock: &(Mock, Option<Mock>)) {
    mock.0.assert();
    if let Some(file) = &mock.1 {
        file.assert();
    }
}

#[tokio::test]
#[serial]
async fn shared_adapter_preserves_local_metrics_with_remote_telemetry_disabled() {
    use crate::observability::ops_stats::{OPS_STATS, OpsStatsEvent};

    for disabled in [Some(true), Some(false), None] {
        let directory = tempfile::tempdir().unwrap();
        let mut fixture = Fixture::new().await;
        let response = fixture.response(10, 1, Some(("+AAAAAAAA\n", 0)), 1, true);
        let mut options = fixture.options(directory.path(), "remote-telemetry");
        options.disable_remote_telemetry = disabled;
        let key = "secret-shared-remote-telemetry";
        let local = OPS_STATS.get_for_instance_with_options(key, Some(&options));
        let mut events = local.subscribe_for_test();
        let legacy = OPS_STATS.get_for_instance(key);
        let mut legacy_events = legacy.subscribe_for_test();
        let adapter = Arc::new(StatsigSharedIdListsAdapter::new(key, &options));
        let listener = Arc::new(Listener::default());
        adapter
            .clone()
            .start(&StatsigRuntime::get_runtime(), listener.clone())
            .await
            .unwrap();
        verify(&response);
        assert!(listener.lists.lock()["members"].ids.contains("AAAAAAAA"));

        let mut metrics = Vec::new();
        let mut diagnostics = 0;
        while let Ok(event) = events.try_recv() {
            match event {
                OpsStatsEvent::Observability(event) => metrics.push(event.metric_name),
                OpsStatsEvent::Diagnostics(_) => diagnostics += 1,
                _ => {}
            }
        }
        for name in ["shared_id_lists.role", "shared_id_lists.publish"] {
            assert!(
                metrics.iter().any(|metric| metric == name),
                "missing {name}"
            );
        }
        assert_eq!(diagnostics > 0, disabled != Some(true));
        assert_eq!(legacy_events.try_recv().is_ok(), disabled != Some(true));
        adapter.force_shutdown();
    }
}

#[tokio::test]
#[serial]
async fn coexisting_shared_adapters_elect_one_writer_per_instance_format() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+AAAAAAAA\n", 0)), 2, true);
    let mut adapters = Vec::new();
    for (flag, role) in [
        (None, "leader"),
        (Some(true), "leader"),
        (Some(false), "follower"),
    ] {
        let mut options = fixture.options(directory.path(), "same-source");
        options.enable_id_list_elias_fano = flag;
        let adapter = Arc::new(StatsigSharedIdListsAdapter::new(
            "secret-shared-fixture",
            &options,
        ));
        let listener = Arc::new(Listener::default());
        adapter
            .clone()
            .start(&StatsigRuntime::get_runtime(), listener.clone())
            .await
            .unwrap();
        assert_eq!(adapter.role_for_test().await, role);
        let lists = listener.lists.lock();
        let ids = &lists["members"].ids;
        assert!(ids.is_mapped() && ids.contains("AAAAAAAA"));
        assert_eq!(ids.has_compact_base(), flag.unwrap_or(false));
        adapters.push(adapter);
    }
    verify(&initial);
    for adapter in adapters {
        adapter.force_shutdown();
    }
}

#[tokio::test]
#[serial]
async fn elected_catalog_updates_followers_and_keeps_old_snapshots() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(20, 1, Some(("+aaaaaaaa\n+cccccccc\n", 0)), 1, true);
    let (leader, leader_view) = start(&fixture, directory.path(), "leader").await;
    let (follower, follower_view) = start(&fixture, directory.path(), "follower").await;
    verify(&initial);
    assert_eq!(leader.role_for_test().await, "leader");
    assert_eq!(follower.role_for_test().await, "follower");
    assert!(leader_view.lists.lock()["members"].ids.is_mapped());
    assert!(follower_view.lists.lock()["members"].ids.is_mapped());
    let old = follower_view.lists.lock().clone();
    let update = fixture.response(40, 1, Some(("-aaaaaaaa\n+bbbbbbbb\n", 20)), 1, true);
    leader.poll_for_test().await.unwrap();
    follower.poll_for_test().await.unwrap();
    verify(&update);
    let current = follower_view.lists.lock();
    assert!(!current["members"].ids.contains("aaaaaaaa"));
    assert!(current["members"].ids.contains("bbbbbbbb"));
    assert!(old["members"].ids.contains("aaaaaaaa"));
    assert!(!old["members"].ids.contains("bbbbbbbb"));
    assert_eq!(current["members"].metadata.size, 40);
    assert_eq!(old["members"].metadata.size, 20);
    assert_eq!(
        follower_view.propagation.lock()["members"].applied_range,
        Some(0..40)
    );
    drop(current);
    leader.force_shutdown();
    follower.force_shutdown();
}

#[tokio::test]
async fn heartbeat_skips_installs_but_new_propagation_and_members_reach_both_readers() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (leader, owner) = start(&fixture, directory.path(), "leader").await;
    let (follower, reader) = start(&fixture, directory.path(), "follower").await;
    verify(&initial);
    let ts = owner.propagation.lock()["members"].ts.unwrap();
    for (timestamp, expected_installs) in [(ts, 1), (ts + 1, 2)] {
        let (manifest, no_download) = fixture.heartbeat(10, timestamp);
        leader.poll_for_test().await.unwrap();
        follower.poll_for_test().await.unwrap();
        manifest.assert();
        no_download.assert();
        for view in [&owner, &reader] {
            assert_eq!(view.installs.load(Ordering::Relaxed), expected_installs);
            assert_eq!(view.propagation.lock()["members"].ts, Some(timestamp));
        }
    }

    let tail = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 1, true);
    leader.poll_for_test().await.unwrap();
    follower.poll_for_test().await.unwrap();
    verify(&tail);
    for view in [&owner, &reader] {
        assert_eq!(view.installs.load(Ordering::Relaxed), 3);
        assert!(view.lists.lock()["members"].ids.contains("bbbbbbbb"));
        assert_eq!(view.lists.lock()["members"].metadata.size, 20);
    }
    leader.force_shutdown();
    follower.force_shutdown();

    // A newly elected reader skips expired recovery. When HTTP confirms the
    // identical content, it must still install the catalog for the first time.
    let store = leader.store_for_test();
    let catalog = store.load().unwrap().unwrap();
    let lease = store.try_acquire_lease().unwrap().unwrap();
    store
        .publish(&lease, &catalog.lists, &catalog.propagation, 1)
        .unwrap();
    drop(lease);
    let (manifest, no_download) = fixture.heartbeat(20, catalog.propagation["members"].ts.unwrap());
    let (successor, view) = start(&fixture, directory.path(), "successor").await;
    assert_eq!(successor.role_for_test().await, "leader");
    assert_eq!(view.installs.load(Ordering::Relaxed), 1);
    assert!(view.lists.lock()["members"].ids.contains("bbbbbbbb"));
    assert_eq!(
        store.load().unwrap().unwrap().content_digest,
        catalog.content_digest
    );
    manifest.assert();
    no_download.assert();
    successor.force_shutdown();
}

#[tokio::test]
#[serial]
async fn follower_takes_released_lease_and_resumes_the_committed_cursor() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (leader, _) = start(&fixture, directory.path(), "first").await;
    let (successor, view) = start(&fixture, directory.path(), "second").await;
    verify(&initial);
    leader.shutdown(Duration::from_secs(1)).await.unwrap();
    let tail = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 1, true);
    successor.poll_for_test().await.unwrap();
    verify(&tail);
    assert_eq!(successor.role_for_test().await, "leader");
    assert!(view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    assert!(view.lists.lock()["members"].ids.contains("bbbbbbbb"));
    assert_eq!(view.lists.lock()["members"].metadata.size, 20);
    successor.force_shutdown();
}

#[tokio::test]
async fn leader_retries_a_rejected_disk_commit_before_private_fallback() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let view = Arc::new(Listener::default());
    let leader = Arc::new(
        StatsigSharedIdListsAdapter::new(
            "partial-rejected",
            &fixture.options(directory.path(), "leader"),
        )
        .with_listener(view.clone()),
    );
    // No prior successful refresh time. A fallback from this state would use
    // the owner's empty map even though the writer has committed the file.
    fixture
        .server
        .mock("POST", "/lists")
        .with_status(403)
        .create();
    assert!(leader.poll_for_test().await.is_err());
    let full = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    view.reject_next_snapshot.store(true, Ordering::Relaxed);
    assert!(leader.poll_for_test().await.is_err());
    verify(&full);
    assert_eq!(leader.role_for_test().await, "leader");
    assert!(view.lists.lock().is_empty());
    // The owner must install the disk commit even when the next HTTP request fails.
    fixture.server.reset();
    let unavailable = fixture
        .server
        .mock("POST", "/lists")
        .with_status(403)
        .create();
    assert!(leader.poll_for_test().await.is_err());
    unavailable.assert();
    assert!(view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    let unchanged = fixture.response(10, 1, None, 1, true);
    let never = fixture.server.mock("GET", "/members").expect(0).create();
    leader.poll_for_test().await.unwrap();
    verify(&unchanged);
    never.assert();
    assert!(view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    leader.force_shutdown();
}

#[tokio::test]
#[serial]
async fn follower_retries_the_same_manifest_without_blocking_the_runtime() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (leader, _) = start(&fixture, directory.path(), "leader").await;
    let (follower, view) = start(&fixture, directory.path(), "follower").await;
    verify(&initial);

    let tail = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 1, true);
    leader.poll_for_test().await.unwrap();
    view.reject_next_snapshot.store(true, Ordering::Relaxed);
    assert!(matches!(
        follower.poll_for_test().await,
        Err(crate::StatsigErr::LockFailure(_))
    ));
    assert_eq!(view.lists.lock()["members"].metadata.size, 10);

    let runtime = tokio::runtime::Handle::current();
    *view.after_snapshot.lock() = Some(Arc::new(move || {
        let (canary, ran) = std::sync::mpsc::channel();
        runtime.spawn(async move {
            let _ = canary.send(());
        });
        ran.recv_timeout(Duration::from_secs(2))
            .expect("follower install blocked the runtime");
    }));
    follower.poll_for_test().await.unwrap();
    assert!(view.lists.lock()["members"].ids.contains("bbbbbbbb"));
    assert_eq!(view.lists.lock()["members"].metadata.size, 20);
    verify(&tail);
    leader.force_shutdown();
    follower.force_shutdown();
}

#[test]
fn restored_catalog_reuses_its_mapping_after_a_rejected_or_cancelled_removal() {
    tokio::runtime::Builder::new_current_thread()
        .max_blocking_threads(1)
        .enable_all()
        .build()
        .unwrap()
        .block_on(async {
            let directory = tempfile::tempdir().unwrap();
            let mut fixture = Fixture::new().await;
            let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
            let (leader, _) = start(&fixture, directory.path(), "leader").await;
            let (follower, view) = start(&fixture, directory.path(), "follower").await;
            verify(&initial);
            leader.force_shutdown();

            let writer = leader.store_for_test();
            let lease = writer.try_acquire_lease().unwrap().unwrap();
            let first = writer.load().unwrap().unwrap();
            let now = chrono::Utc::now().timestamp_millis() as u64;
            for cancel in [false, true] {
                let installs_before_removal = view.installs.load(Ordering::Relaxed);
                writer
                    .publish(&lease, &HashMap::new(), &HashMap::new(), now)
                    .unwrap();
                if cancel {
                    // Queue the read behind the only worker. Let it finish without
                    // polling its caller again, so the listener never sees the removal.
                    let (release, wait) = std::sync::mpsc::channel();
                    let blocker = tokio::task::spawn_blocking(move || {
                        wait.recv_timeout(Duration::from_secs(5)).unwrap()
                    });
                    let mut poll = Box::pin(follower.poll_for_test());
                    assert!(futures::poll!(&mut poll).is_pending());
                    release.send(()).unwrap();
                    blocker.await.unwrap();
                    tokio::task::spawn_blocking(|| ()).await.unwrap();
                    drop(poll);
                } else {
                    view.reject_next_snapshot.store(true, Ordering::Relaxed);
                    assert!(matches!(
                        follower.poll_for_test().await,
                        Err(crate::StatsigErr::LockFailure(_))
                    ));
                }

                writer
                    .publish(&lease, &first.lists, &first.propagation, now)
                    .unwrap();
                follower.poll_for_test().await.unwrap();
                assert_eq!(
                    view.installs.load(Ordering::Relaxed),
                    installs_before_removal + 1
                );
                writer
                    .publish(&lease, &first.lists, &first.propagation, now + 1)
                    .unwrap();
                follower.poll_for_test().await.unwrap();
                assert_eq!(
                    view.installs.load(Ordering::Relaxed),
                    installs_before_removal + 1
                );
                let loaded = follower.store_for_test().load().unwrap().unwrap();
                assert!(Arc::ptr_eq(
                    &loaded.lists["members"].ids,
                    &view.lists.lock()["members"].ids
                ));
            }
            follower.force_shutdown();
        });
}

#[tokio::test]
async fn cancelled_follower_install_tracks_the_snapshot_accepted_by_the_listener() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (leader, _) = start(&fixture, directory.path(), "leader").await;
    let (follower, view) = start(&fixture, directory.path(), "follower").await;
    verify(&initial);
    leader.force_shutdown();
    let store = leader.store_for_test();
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let first = store.load().unwrap().unwrap();
    let now_ms = || chrono::Utc::now().timestamp_millis() as u64;
    store
        .publish(&lease, &HashMap::new(), &HashMap::new(), now_ms())
        .unwrap();

    let entered = Arc::new(tokio::sync::Notify::new());
    let (release, resume) = std::sync::mpsc::channel();
    *view.after_snapshot.lock() = Some(Arc::new({
        let entered = entered.clone();
        let resume = Mutex::new(resume);
        move || {
            entered.notify_one();
            resume.lock().recv_timeout(Duration::from_secs(5)).unwrap();
        }
    }));
    let polling = follower.clone();
    let task = tokio::spawn(async move { polling.poll_for_test().await });
    tokio::time::timeout(Duration::from_secs(5), entered.notified())
        .await
        .unwrap();
    task.abort();
    assert!(task.await.unwrap_err().is_cancelled());
    assert!(view.lists.lock().is_empty());
    let restored = store
        .publish(&lease, &first.lists, &first.propagation, now_ms())
        .unwrap();
    *view.after_snapshot.lock() = None;
    release.send(()).unwrap();

    follower.poll_for_test().await.unwrap();
    assert!(view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    assert_eq!(view.installs.load(Ordering::Relaxed), 3);
    // An older follower may still have the first wire generation recorded after
    // cancellation. It must see restored A as a new publication.
    assert_ne!(first.generation, restored.generation);
    follower.force_shutdown();
}

#[tokio::test]
#[serial]
async fn shared_http_uses_the_callers_fallback_cadence_and_diagnostics() {
    use super::statsig_http_id_lists_adapter::TEST_CDN_MANIFEST_URL;
    use crate::observability::ops_stats::{OPS_STATS, OpsStatsEvent};
    use crate::sdk_diagnostics::{diagnostics::ContextType, marker::KeyType};

    for shared in [true, false] {
        let directory = tempfile::tempdir().unwrap();
        let mut fixture = Fixture::new().await;
        let mut options = fixture.options(directory.path(), "retry-cadence");
        options.fallback_to_statsig_api = Some(true);
        options.id_lists_sync_interval_ms = Some(3_600_000);
        if !shared {
            options.shared_id_lists_dir = None;
        }
        let key = "secret-shared-cadence";
        let view = Arc::new(Listener::default());
        let adapter =
            Arc::new(StatsigSharedIdListsAdapter::new(key, &options).with_listener(view.clone()));
        let mut events = OPS_STATS.get_for_instance(key).subscribe_for_test();
        let mut check_enqueues = |expected| {
            let mut enqueues = 0;
            while let Ok(event) = events.try_recv() {
                if let OpsStatsEvent::Diagnostics(event) = event {
                    if event.should_enqueue {
                        assert_eq!(event.key, Some(KeyType::GetIDListSources));
                        assert_eq!(event.context, Some(ContextType::ConfigSync));
                        enqueues += 1;
                    }
                }
            }
            assert_eq!(enqueues, expected);
        };
        if shared {
            let store = adapter.store_for_test();
            let lease = store.try_acquire_lease().unwrap().unwrap();
            store
                .publish(
                    &lease,
                    &HashMap::new(),
                    &HashMap::new(),
                    chrono::Utc::now().timestamp_millis() as u64,
                )
                .unwrap();
            adapter.poll_for_test().await.unwrap();
            check_enqueues(0);
            drop(lease);
        }
        let primary = fixture
            .server
            .mock("POST", "/lists")
            .with_status(503)
            .expect(6)
            .create();
        let cdn = fixture
            .server
            .mock("GET", "/cdn")
            .with_body("{}")
            .expect(2)
            .create();
        TEST_CDN_MANIFEST_URL
            .scope(format!("{}/cdn", fixture.server.url()), async {
                // Listener registration on election or entry to private fallback is background work.
                assert!(adapter.poll_for_test().await.is_err());
                check_enqueues(1);
                assert_eq!(
                    adapter.role_for_test().await,
                    if shared { "leader" } else { "http_fallback" }
                );

                adapter
                    .clone()
                    .start(&StatsigRuntime::get_runtime(), view)
                    .await
                    .unwrap();
                check_enqueues(0);
                for attempt in 2..=5 {
                    assert_eq!(adapter.poll_for_test().await.is_ok(), attempt == 5);
                    check_enqueues(1);
                }
            })
            .await;
        primary.assert();
        cdn.assert();
        adapter.force_shutdown();
    }
}

#[tokio::test]
#[serial]
async fn same_file_full_replay_resets_cursor_then_noop_does_not_download() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let first = fixture.response(20, 1, Some(("+aaaaaaaa\n+bbbbbbbb\n", 0)), 1, true);
    let (adapter, view) = start(&fixture, directory.path(), "same-file").await;
    verify(&first);
    let replay = fixture.response(10, 2, Some(("+cccccccc\n", 0)), 1, true);
    adapter.poll_for_test().await.unwrap();
    verify(&replay);
    assert_eq!(view.lists.lock()["members"].metadata.size, 10);
    assert_eq!(view.lists.lock()["members"].metadata.creation_time, 2);
    assert!(!view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    assert!(view.lists.lock()["members"].ids.contains("cccccccc"));
    assert_eq!(
        view.propagation.lock()["members"].applied_range,
        Some(0..10)
    );
    let noop = fixture.response(10, 2, None, 1, true);
    adapter.poll_for_test().await.unwrap();
    verify(&noop);
    assert_eq!(view.lists.lock()["members"].metadata.size, 10);
    adapter.force_shutdown();
}

#[tokio::test]
#[serial]
async fn cold_leader_does_not_install_expired_recovery_after_http_failure() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (writer, _) = start(&fixture, directory.path(), "first").await;
    verify(&initial);
    writer.force_shutdown();
    let store = writer.store_for_test();
    let catalog = store.load().unwrap().unwrap();
    {
        let lease = store.try_acquire_lease().unwrap().unwrap();
        store
            .publish(&lease, &catalog.lists, &catalog.propagation, 1)
            .unwrap();
    }

    fixture.server.reset();
    let unavailable = fixture
        .server
        .mock("POST", "/lists")
        .with_status(403)
        .expect(2)
        .create();
    let adapter = Arc::new(StatsigSharedIdListsAdapter::new(
        "secret-shared-fixture",
        &fixture.options(directory.path(), "cold"),
    ));
    let view = Arc::new(Listener::default());
    assert!(
        adapter
            .clone()
            .start(&StatsigRuntime::get_runtime(), view.clone())
            .await
            .is_err()
    );
    unavailable.assert();
    assert_eq!(adapter.role_for_test().await, "http_fallback");
    assert!(view.lists.lock().is_empty());

    let fresh = fixture.response(10, 2, Some(("+bbbbbbbb\n", 0)), 1, true);
    adapter
        .clone()
        .start(&StatsigRuntime::get_runtime(), view.clone())
        .await
        .unwrap();
    verify(&fresh);
    assert_eq!(adapter.role_for_test().await, "http_fallback");
    assert!(view.lists.lock()["members"].ids.contains("bbbbbbbb"));
    assert!(!view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    adapter.force_shutdown();
}

#[tokio::test]
#[serial]
async fn queued_initialize_retries_each_observe_their_own_fallback_refresh() {
    use futures::poll;

    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let mut options = fixture.options(directory.path(), "readiness");
    options.shared_id_lists_dir = None; // Enter private fallback on the first start.
    options.id_lists_sync_interval_ms = Some(3_600_000);
    let adapter = Arc::new(StatsigSharedIdListsAdapter::new(
        "secret-shared-fixture",
        &options,
    ));
    let view = Arc::new(Listener::default());
    let runtime = StatsigRuntime::get_runtime();
    let rejected = fixture
        .server
        .mock("POST", "/lists")
        .with_status(403)
        .expect(3)
        .create();
    assert!(adapter.clone().start(&runtime, view.clone()).await.is_err());
    assert_eq!(adapter.role_for_test().await, "http_fallback");

    // Tokio's FIFO mutex puts the second caller ahead of the first one's
    // next lock acquisition. No timing or scheduler assumptions are needed.
    let pause = adapter.pause_ticks_for_test().await;
    let mut first = Box::pin(adapter.clone().start(&runtime, view.clone()));
    let mut second = Box::pin(adapter.clone().start(&runtime, view.clone()));
    assert!(poll!(first.as_mut()).is_pending());
    assert!(poll!(second.as_mut()).is_pending());
    drop(pause);
    let (a, b) = tokio::join!(first, second);
    assert!(
        a.is_err() && b.is_err(),
        "a skipped refresh is not readiness: {a:?}, {b:?}"
    );
    rejected.assert();
    assert!(view.lists.lock().is_empty());
    adapter.force_shutdown();
}

#[tokio::test]
#[serial]
async fn failed_publication_falls_back_from_the_committed_members_and_cursor() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (adapter, view) = start(&fixture, directory.path(), "publish-failure").await;
    verify(&initial);
    let store = adapter.store_for_test();
    let manifest = store.directory().join("manifest.json");
    let backup = store.directory().join("old-manifest-test.json");
    std::fs::rename(&manifest, &backup).unwrap();
    std::fs::create_dir(&manifest).unwrap();
    let tail = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 2, true);
    adapter.poll_for_test().await.unwrap();
    verify(&tail);
    assert_eq!(adapter.role_for_test().await, "http_fallback");
    let lists = view.lists.lock();
    assert_eq!(lists["members"].metadata.size, 20);
    assert!(lists["members"].ids.contains("aaaaaaaa"));
    assert!(lists["members"].ids.contains("bbbbbbbb"));
    assert!(!lists["members"].ids.is_mapped());
    drop(lists);
    assert!(store.try_acquire_lease().unwrap().is_some());
    adapter.force_shutdown();
}

#[tokio::test]
#[serial]
async fn successor_can_acquire_the_lease_during_private_fallback() {
    for established in [false, true] {
        let directory = tempfile::tempdir().unwrap();
        let mut fixture = Fixture::new().await;
        let listener = Arc::new(Listener::default());
        let adapter = Arc::new(
            StatsigSharedIdListsAdapter::new(
                "secret-handoff",
                &fixture.options(directory.path(), "handoff"),
            )
            .with_listener(listener),
        );
        if established {
            let initial = fixture
                .server
                .mock("POST", "/lists")
                .with_body("{}")
                .create();
            adapter.poll_for_test().await.unwrap();
            initial.assert();
            fixture.server.reset();
        }

        let store = adapter.store_for_test();
        let manifest = store.directory().join("manifest.json");
        // Fail the commit after election/recovery, even for a newly elected leader.
        let shared = fixture
            .server
            .mock("POST", "/lists")
            .with_body_from_request(move |_| {
                if established {
                    std::fs::remove_file(&manifest).unwrap();
                }
                std::fs::create_dir(&manifest).unwrap();
                b"{}".to_vec()
            })
            .expect(1)
            .create();
        let (send_lease, lease) = std::sync::mpsc::channel();
        let private = fixture
            .server
            .mock("POST", "/lists")
            .with_body_from_request(move |_| {
                send_lease.send(store.try_acquire_lease().unwrap()).unwrap();
                b"{}".to_vec()
            })
            .expect(1)
            .create();

        adapter.poll_for_test().await.unwrap();
        assert!(
            lease.try_recv().unwrap().is_some(),
            "lease still held during private HTTP"
        );
        shared.assert();
        private.assert();
        assert_eq!(adapter.role_for_test().await, "http_fallback");
        adapter.force_shutdown();
    }
}

#[tokio::test]
#[serial]
async fn missing_range_proof_is_not_replaced_with_advertised_size() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (adapter, view) = start(&fixture, directory.path(), "range-proof").await;
    verify(&initial);
    let tail = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 1, false);
    assert!(adapter.poll_for_test().await.is_err());
    verify(&tail);
    assert!(!view.lists.lock()["members"].ids.contains("bbbbbbbb"));
    assert_eq!(view.lists.lock()["members"].metadata.size, 10);
    assert_eq!(
        view.propagation.lock()["members"].applied_range,
        Some(0..10)
    );
    adapter.force_shutdown();
}

#[tokio::test(flavor = "multi_thread", worker_threads = 1)]
#[serial]
async fn shutdown_does_not_release_the_lease_during_an_entered_publication() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (adapter, view) = start(&fixture, directory.path(), "blocked-callback").await;
    verify(&initial);
    let entered = Arc::new(AtomicBool::new(false));
    let release = Arc::new((std::sync::Mutex::new(false), Condvar::new()));
    *view.after_snapshot.lock() = Some(Arc::new({
        let entered = entered.clone();
        let release = release.clone();
        move || {
            entered.store(true, Ordering::Release);
            let (lock, signal) = &*release;
            let mut released = lock.lock().unwrap();
            while !*released {
                released = signal.wait(released).unwrap();
            }
        }
    }));
    // A synchronous installation can block. The lone runtime worker must
    // remain available, and the lease must outlive cancellation.
    let runtime = tokio::runtime::Handle::current();
    let coordinator = std::thread::spawn({
        let adapter = adapter.clone();
        let release = release.clone();
        move || {
            struct Release(Arc<(std::sync::Mutex<bool>, Condvar)>);
            impl Drop for Release {
                fn drop(&mut self) {
                    let (lock, signal) = &*self.0;
                    *lock.lock().unwrap() = true;
                    signal.notify_all();
                }
            }
            let release_guard = Release(release);
            let deadline = std::time::Instant::now() + Duration::from_secs(3);
            while !entered.load(Ordering::Acquire) {
                assert!(
                    std::time::Instant::now() < deadline,
                    "publication did not enter"
                );
                std::thread::sleep(Duration::from_millis(1));
            }
            let (canary, ran) = std::sync::mpsc::channel();
            runtime.spawn(async move { canary.send(()).unwrap() });
            ran.recv_timeout(Duration::from_secs(2))
                .expect("runtime worker blocked by publication");
            let stopping = std::thread::spawn({
                let adapter = adapter.clone();
                move || {
                    runtime
                        .block_on(adapter.shutdown(Duration::from_secs(3)))
                        .unwrap()
                }
            });
            while !adapter.stopped_for_test() {
                assert!(
                    std::time::Instant::now() < deadline,
                    "shutdown did not start"
                );
                std::thread::sleep(Duration::from_millis(1));
            }
            let still_running = !stopping.is_finished();
            let still_locked = adapter
                .store_for_test()
                .try_acquire_lease()
                .unwrap()
                .is_none();
            drop(release_guard);
            stopping.join().unwrap();
            assert!(still_running, "shutdown escaped an entered callback");
            assert!(still_locked, "lease released before callback completed");
        }
    });
    let tail = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 1, true);
    let polling = adapter.clone();
    let _ = tokio::spawn(async move { polling.poll_for_test().await })
        .await
        .unwrap();
    coordinator.join().unwrap();
    verify(&tail);
    assert!(
        adapter
            .store_for_test()
            .try_acquire_lease()
            .unwrap()
            .is_some()
    );
}

#[tokio::test]
#[serial]
async fn publication_callback_can_request_shutdown_without_deadlock() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (adapter, view) = start(&fixture, directory.path(), "reentrant-stop").await;
    verify(&initial);
    let weak = Arc::downgrade(&adapter);
    *view.after_snapshot.lock() = Some(Arc::new(move || weak.upgrade().unwrap().force_shutdown()));
    let tail = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 1, true);
    let _ = tokio::time::timeout(Duration::from_secs(3), adapter.poll_for_test())
        .await
        .unwrap();
    verify(&tail);
    // The cancelled poll can return while the blocking callback still owns the lease.
    let store = adapter.store_for_test();
    tokio::time::timeout(Duration::from_secs(3), async {
        while store.try_acquire_lease().unwrap().is_none() {
            tokio::time::sleep(Duration::from_millis(1)).await;
        }
    })
    .await
    .expect("publication callback did not release its lease after shutdown");
}

#[tokio::test]
#[serial]
async fn stale_follower_falls_back_with_a_complete_mapped_baseline_and_stays_private() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (leader, _) = start(&fixture, directory.path(), "stale-leader").await;
    let (follower, view) = start(&fixture, directory.path(), "stale-follower").await;
    verify(&initial);
    leader.force_shutdown();
    let store = follower.store_for_test();
    let lease = store.try_acquire_lease().unwrap().unwrap();
    let catalog = store.load().unwrap().unwrap();
    store
        .publish(
            &lease,
            &catalog.lists,
            &catalog.propagation,
            (chrono::Utc::now().timestamp_millis() - 181_000) as u64,
        )
        .unwrap();
    let unchanged = fixture.response(10, 1, None, 2, true);
    follower.poll_for_test().await.unwrap();
    assert_eq!(follower.role_for_test().await, "http_fallback");
    assert_eq!(view.lists.lock()["members"].metadata.size, 10);
    assert!(view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    // An unchanged HTTP refresh may retain a valid mapping; private fallback
    // describes the source controller, not a forced copy of unchanged sets.
    assert!(view.lists.lock()["members"].ids.is_mapped());
    drop(lease);
    follower.poll_for_test().await.unwrap();
    assert_eq!(follower.role_for_test().await, "http_fallback");
    assert!(store.try_acquire_lease().unwrap().is_some());
    verify(&unchanged);
    follower.force_shutdown();
}

#[tokio::test]
#[serial]
async fn rejected_older_generation_preserves_members_cursor_and_delivery_proof() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let initial = fixture.response(10, 2, Some(("+aaaaaaaa\n", 0)), 1, true);
    let (adapter, view) = start(&fixture, directory.path(), "older-generation").await;
    verify(&initial);
    let original = view.propagation.lock()["members"].clone();
    let older = fixture.response(20, 1, Some(("+bbbbbbbb\n", 10)), 1, true);
    adapter.poll_for_test().await.unwrap();
    verify(&older);
    assert_eq!(view.lists.lock()["members"].metadata.size, 10);
    assert!(view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    assert!(!view.lists.lock()["members"].ids.contains("bbbbbbbb"));
    let proof = view.propagation.lock();
    assert_eq!(proof["members"].applied_range, original.applied_range);
    assert_eq!(proof["members"].ts, original.ts);
    adapter.force_shutdown();
}

#[test]
fn offline_and_proxy_instances_skip_shared_storage_initialization() {
    use crate::networking::proxy_config::ProxyConfig;
    for (offline, proxy) in [(true, false), (false, true), (false, false)] {
        let temp = tempfile::tempdir().unwrap();
        let shared = temp.path().join("shared");
        let options = StatsigOptions {
            enable_id_lists: Some(true),
            disable_network: Some(offline),
            shared_id_lists_dir: Some(shared.to_str().unwrap().to_owned()),
            proxy_config: proxy.then(|| ProxyConfig {
                proxy_host: Some("localhost".to_string()),
                proxy_port: Some(8888),
                proxy_protocol: None,
                proxy_auth: None,
                ca_cert_path: None,
            }),
            ..Default::default()
        };
        let _sdk = crate::Statsig::new("secret-shared-policy", Some(Arc::new(options)));
        assert_eq!(shared.exists(), !offline && !proxy);
    }
}

#[cfg(not(feature = "custom_network_provider"))]
#[tokio::test]
#[serial]
async fn graceful_shutdown_bounds_an_inline_private_fallback() {
    struct InlineListener {
        entered: std::sync::mpsc::Sender<()>,
        release: Mutex<std::sync::mpsc::Receiver<()>>,
    }
    impl IdListsUpdateListener for InlineListener {
        fn get_current_id_list_metadata(&self) -> HashMap<String, IdListMetadata> {
            HashMap::new()
        }
        fn did_receive_id_list_updates(&self, _: HashMap<String, IdListUpdate>) {
            self.entered.send(()).unwrap();
            self.release
                .lock()
                .recv_timeout(Duration::from_secs(3))
                .unwrap();
        }
    }

    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let manifest = fixture
        .server
        .mock("POST", "/lists")
        .with_body("{}")
        .expect(1)
        .create();
    let adapter = Arc::new(StatsigSharedIdListsAdapter::new(
        "fallback-test",
        &fixture.options(directory.path(), "fallback-stop"),
    ));
    let (release, rx) = std::sync::mpsc::channel();
    let (entered, ready) = std::sync::mpsc::channel();
    let listener = Arc::new(InlineListener {
        entered,
        release: Mutex::new(rx),
    });
    // The callback occupies its runtime thread. Drive the shutdown deadline independently.
    let stopping = std::thread::spawn({
        let adapter = adapter.clone();
        move || {
            ready.recv_timeout(Duration::from_secs(3)).unwrap();
            let shutdown_runtime = tokio::runtime::Builder::new_current_thread()
                .enable_time()
                .build()
                .unwrap();
            let result = shutdown_runtime.block_on(adapter.shutdown(Duration::from_millis(20)));
            assert!(
                matches!(result, Err(crate::StatsigErr::ShutdownFailure(_))),
                "{result:?}"
            );
            release.send(()).unwrap();
        }
    });
    // A listener without snapshot support takes the controller's HTTP fallback.
    let _ = adapter
        .clone()
        .start(&StatsigRuntime::get_runtime(), listener)
        .await;
    stopping.join().unwrap();
    adapter.shutdown(Duration::from_secs(2)).await.unwrap();
    manifest.assert();
}

#[tokio::test]
async fn shutdown_during_listener_check_prevents_http_fallback() {
    struct StopOnFallback(Arc<StatsigSharedIdListsAdapter>);
    impl IdListsUpdateListener for StopOnFallback {
        fn supports_id_list_snapshots(&self) -> bool {
            self.0.force_shutdown();
            false
        }
        fn get_current_id_list_metadata(&self) -> HashMap<String, IdListMetadata> {
            panic!("read cursor after shutdown")
        }
        fn did_receive_id_list_updates(&self, _: HashMap<String, IdListUpdate>) {
            panic!("published after shutdown")
        }
    }

    let adapter = Arc::new(StatsigSharedIdListsAdapter::new(
        "stop-before-fallback",
        &StatsigOptions {
            disable_network: Some(true),
            ..Default::default()
        },
    ));
    // A fallback request would return DisableNetworkOn instead of observing shutdown.
    let result = adapter
        .clone()
        .start(
            &StatsigRuntime::get_runtime(),
            Arc::new(StopOnFallback(adapter)),
        )
        .await;
    assert!(
        matches!(result, Err(crate::StatsigErr::ShutdownFailure(_))),
        "{result:?}"
    );
}

#[tokio::test]
async fn partial_catalog_is_visible_across_processes_and_recovers_after_writer_exit() {
    const CHILD: &str = "STATSIG_PARTIAL_ID_LIST_READER_TEST";
    let options = |root: &std::path::Path, url: &str| StatsigOptions {
        shared_id_lists_dir: Some(root.to_string_lossy().into_owned()),
        id_lists_url: Some(format!("{url}/lists")),
        state_read_primary_attempts: Some(1),
        experimental_flags: Some(["partial_id_list_refresh".to_string()].into()),
        ..Default::default()
    };
    if let Some(path) = std::env::var_os(CHILD) {
        let url = std::env::var("STATSIG_PARTIAL_ID_LIST_READER_URL").unwrap();
        let reader = Arc::new(StatsigSharedIdListsAdapter::new(
            "partial",
            &options(path.as_ref(), &url),
        ));
        let view = Arc::new(Listener::default());
        assert!(
            reader
                .clone()
                .start(&StatsigRuntime::get_runtime(), view.clone())
                .await
                .is_err()
        );
        assert_eq!(reader.role_for_test().await, "follower");
        let lists = view.lists.lock();
        assert_eq!(lists.len(), 2);
        assert!(lists["a"].ids.contains("new-a"));
        assert!(lists["b"].ids.contains("old-b"));
        return;
    }
    let dir = tempfile::tempdir().unwrap();
    let mut server = Server::new_async().await;
    let url = server.url();
    let opts = options(dir.path(), &url);
    let leader = Arc::new(StatsigSharedIdListsAdapter::new("partial", &opts));
    let store = leader.store_for_test();
    let view = Arc::new(Listener::default());
    let entry = |name: &str, file: &str, size: u64| {
        serde_json::json!({
            "name":name, "fileID":file, "url":format!("{url}/{name}"), "size":size, "creationTime":1
        })
    };
    // Simulate the legacy reader using its original source and lease.
    let legacy = StatsigSharedIdListsAdapter::new(
        "partial",
        &StatsigOptions {
            experimental_flags: None,
            ..opts.clone()
        },
    )
    .store_for_test();
    assert_ne!(store.directory(), legacy.directory());
    let _legacy_writer = legacy.try_acquire_lease().unwrap().unwrap();
    let baseline = serde_json::json!({"b":entry("b","old",7), "removed":entry("removed","r",3)});
    server
        .mock("POST", "/lists")
        .with_body(baseline.to_string())
        .create();
    server.mock("GET", "/b").with_body("+old-b\n").create();
    server.mock("GET", "/removed").with_body("+r\n").create();
    leader
        .clone()
        .start(&StatsigRuntime::get_runtime(), view.clone())
        .await
        .unwrap();
    let last_complete = store.load().unwrap().unwrap().status.successful_refresh_ms;
    assert_ne!(last_complete, 0);

    server.reset();
    let mut target = serde_json::json!({"a":entry("a","a",7), "b":entry("b","new",7)});
    target["a"]["name"] = "b".into(); // Keep the two files distinct through publication and takeover.
    let manifest = server
        .mock("POST", "/lists")
        .with_body(target.to_string())
        .expect(1)
        .create();
    let a = server
        .mock("GET", "/a")
        .with_body("+new-a\n")
        .expect(1)
        .create();
    let b = server
        .mock("GET", "/b")
        .match_header("range", "bytes=0-")
        .with_status(403)
        .expect(1)
        .create();
    assert!(leader.poll_for_test().await.is_err());
    let partial = store.load().unwrap().unwrap();
    assert_eq!(partial.status.successful_refresh_ms, last_complete);
    assert!(partial.status.incomplete_since_ms.is_some());
    assert!(view.lists.lock()["b"].ids.contains("old-b"));
    let child = std::process::Command::new(std::env::current_exe().unwrap())
        .args([
            "--exact",
            concat!(
                module_path!(),
                "::partial_catalog_is_visible_across_processes_and_recovers_after_writer_exit"
            )
            .strip_prefix("statsig_rust::")
            .unwrap(),
            "--nocapture",
        ])
        .env(CHILD, dir.path())
        .env("STATSIG_PARTIAL_ID_LIST_READER_URL", &url)
        .output()
        .unwrap();
    let stdout = String::from_utf8_lossy(&child.stdout);
    assert!(
        child.status.success() && stdout.contains("1 passed"),
        "{stdout}\n{}",
        String::from_utf8_lossy(&child.stderr)
    );
    manifest.assert();
    a.assert();
    b.assert();
    server.reset();
    server.mock("POST", "/lists").with_body("{").create();
    assert!(leader.poll_for_test().await.is_err());
    assert_eq!(
        store.load().unwrap().unwrap().generation,
        partial.generation
    );
    assert!(legacy.load().unwrap().is_none());
    leader.force_shutdown();
    drop(leader);

    server.reset();
    server
        .mock("POST", "/lists")
        .with_body(target.to_string())
        .create();
    let a = server.mock("GET", "/a").expect(0).create();
    let b = server
        .mock("GET", "/b")
        .match_header("range", "bytes=0-")
        .with_body("+new-b\n")
        .expect(1)
        .create();
    let successor = Arc::new(StatsigSharedIdListsAdapter::new("partial", &opts));
    let next = Arc::new(Listener::default());
    successor
        .clone()
        .start(&StatsigRuntime::get_runtime(), next.clone())
        .await
        .unwrap();
    assert!(next.lists.lock()["a"].ids.contains("new-a"));
    assert!(next.lists.lock()["b"].ids.contains("new-b"));
    assert!(!next.lists.lock()["b"].ids.contains("old-b"));
    assert!(
        store
            .load()
            .unwrap()
            .unwrap()
            .status
            .incomplete_since_ms
            .is_none()
    );
    a.assert();
    b.assert();
    successor.force_shutdown();
}

#[tokio::test]
async fn rejected_expired_catalog_releases_the_lease_and_uses_the_owners_cursor() {
    let directory = tempfile::tempdir().unwrap();
    let mut fixture = Fixture::new().await;
    let options = StatsigOptions {
        init_timeout_ms: Some(0), // The first incomplete catalog is immediately stale.
        experimental_flags: Some(["partial_id_list_refresh".to_owned()].into()),
        ..fixture.options(directory.path(), "rejected-expired")
    };
    let adapter = || {
        let view = Arc::new(Listener::default());
        let adapter = StatsigSharedIdListsAdapter::new("rejected-expired", &options)
            .with_listener(view.clone());
        (adapter, view)
    };
    let (leader, owner) = adapter();
    let store = leader.store_for_test();
    let url = fixture.server.url();
    let entry = |name: &str| {
        serde_json::json!({
            "name": name, "url": format!("{url}/{name}"),
            "fileID": "file-1", "size": 10, "creationTime": 1
        })
    };
    fixture
        .server
        .mock("POST", "/lists")
        .with_body(
            serde_json::json!({"members": entry("members"), "unavailable": entry("unavailable")})
                .to_string(),
        )
        .create();
    fixture
        .server
        .mock("GET", "/members")
        .with_body("+aaaaaaaa\n")
        .create();
    fixture
        .server
        .mock("GET", "/unavailable")
        .with_status(403)
        .create();
    owner.reject_next_snapshot.store(true, Ordering::Relaxed);
    assert!(leader.poll_for_test().await.is_err());
    assert!(owner.lists.lock().is_empty());
    assert_eq!(
        store.load().unwrap().unwrap().lists["members"]
            .metadata
            .size,
        10
    );
    assert!(store.try_acquire_lease().unwrap().is_none());

    // None of these owners installed the ten bytes committed to disk.
    let private = fixture.response(10, 1, Some(("+aaaaaaaa\n", 0)), 3, true);
    let controllers = [adapter(), (leader, owner), adapter()]; // follower, leader, successor
    for (controller, view) in &controllers {
        view.reject_next_snapshot.store(true, Ordering::Relaxed);
        controller.poll_for_test().await.unwrap();
        assert_eq!(controller.role_for_test().await, "http_fallback");
        assert!(view.lists.lock()["members"].ids.contains("aaaaaaaa"));
    }
    verify(&private);
    assert!(store.try_acquire_lease().unwrap().is_some());
}
