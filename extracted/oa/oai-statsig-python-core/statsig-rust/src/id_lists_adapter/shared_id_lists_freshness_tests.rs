use super::{
    IdList, IdListIds, IdListMetadata, IdListUpdate, IdListsAdapter, IdListsUpdateListener,
    SharedIdListLease, SharedIdListStore, StatsigSharedIdListsAdapter,
};
use crate::{StatsigOptions, StatsigRuntime};
use mockito::{Mock, Server, ServerGuard};
use parking_lot::Mutex;
use serial_test::serial;
use std::collections::HashMap;
use std::sync::{Arc, mpsc};
use std::time::Duration;

fn now_ms() -> u64 {
    chrono::Utc::now().timestamp_millis() as u64
}

#[derive(Default)]
struct View(Mutex<HashMap<String, IdList>>);
impl IdListsUpdateListener for View {
    fn get_current_id_list_metadata(&self) -> HashMap<String, IdListMetadata> {
        self.0
            .lock()
            .iter()
            .map(|(name, list)| (name.clone(), list.metadata.clone()))
            .collect()
    }
    fn did_receive_id_list_updates(&self, updates: HashMap<String, IdListUpdate>) {
        let mut lists = self.0.lock();
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
        _propagation: HashMap<String, super::IdListPropagationUpdate>,
    ) -> Result<(), crate::StatsigErr> {
        *self.0.lock() = lists;
        Ok(())
    }
}

struct Fixture {
    _directory: tempfile::TempDir,
    server: ServerGuard,
    adapter: Arc<StatsigSharedIdListsAdapter>,
    view: Arc<View>,
    store: Arc<SharedIdListStore>,
    lease: Arc<SharedIdListLease>,
    initial: HashMap<String, IdList>,
}
impl Fixture {
    async fn unstarted(partial_refresh: bool) -> Self {
        let directory = tempfile::tempdir().unwrap();
        let server = Server::new_async().await;
        let options = StatsigOptions {
            id_lists_url: Some(format!("{}/lists", server.url())),
            shared_id_lists_dir: Some(directory.path().to_str().unwrap().to_owned()),
            id_lists_sync_interval_ms: Some(1_000),
            disable_all_logging: Some(true),
            experimental_flags: partial_refresh
                .then(|| ["partial_id_list_refresh".to_owned()].into()),
            ..StatsigOptions::default()
        };
        let adapter = Arc::new(StatsigSharedIdListsAdapter::new(
            "secret-freshness",
            &options,
        ));
        let store = adapter.store_for_test();
        let lease = Arc::new(store.try_acquire_lease().unwrap().unwrap());
        let initial = HashMap::from([(
            "members".to_owned(),
            IdList {
                metadata: IdListMetadata {
                    name: "members".to_owned(),
                    url: format!("{}/members", server.url()),
                    file_id: Some("file-1".to_owned()),
                    size: 10,
                    creation_time: 1,
                },
                ids: Arc::new(IdListIds::from(["aaaaaaaa".to_owned()])),
            },
        )]);
        let view = Arc::new(View::default());
        Self {
            _directory: directory,
            server,
            adapter,
            view,
            store,
            lease,
            initial,
        }
    }
    async fn new() -> Self {
        let fixture = Self::unstarted(false).await;
        fixture
            .store
            .publish(&fixture.lease, &fixture.initial, &HashMap::new(), now_ms())
            .unwrap();
        fixture
            .adapter
            .clone()
            .start(&StatsigRuntime::get_runtime(), fixture.view.clone())
            .await
            .unwrap();
        assert_eq!(fixture.adapter.role_for_test().await, "follower");
        fixture
    }
    fn updated(&self) -> HashMap<String, IdList> {
        let mut lists = self.initial.clone();
        let list = lists.get_mut("members").unwrap();
        Arc::make_mut(&mut list.ids).insert_str("bbbbbbbb");
        list.metadata.size = 20;
        lists
    }
    fn expect_private_delta(&mut self) -> (Mock, Mock) {
        let manifest = self
            .server
            .mock("POST", "/lists")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(
                serde_json::json!({"members":{
                    "name":"members", "url":format!("{}/members", self.server.url()),
                    "fileID":"file-1", "size":20, "creationTime":1,
                }})
                .to_string(),
            )
            .expect(1)
            .create();
        let body = self
            .server
            .mock("GET", "/members")
            .match_header("range", "bytes=10-")
            .with_status(206)
            .with_header("content-range", "bytes 10-19/20")
            .with_body("+bbbbbbbb\n")
            .expect(1)
            .create();
        (manifest, body)
    }
}

#[tokio::test]
async fn cold_partial_catalog_times_out_from_its_first_publication_and_resumes_installed_bytes() {
    for elected in [false, true] {
        let mut fixture = Fixture::unstarted(true).await;
        let store = &fixture.store;
        let lease = &fixture.lease;
        let first = store
            .publish_with_clock(
                lease,
                &fixture.initial,
                &HashMap::new(),
                Some(Default::default()),
                || 1,
            )
            .unwrap();
        let repeated = store
            .publish_with_clock(
                lease,
                &fixture.initial,
                &HashMap::new(),
                Some(first.status),
                now_ms,
            )
            .unwrap();
        assert_eq!(repeated.status.successful_refresh_ms, 0);
        assert_eq!(repeated.status.incomplete_since_ms, Some(1));
        let failed_renewal = elected.then(|| {
            fixture
                .server
                .mock("POST", "/lists")
                .with_status(403)
                .expect(1)
                .create()
        });
        let (manifest, tail) = fixture.expect_private_delta();
        if elected {
            drop(fixture.lease);
        }
        fixture
            .adapter
            .clone()
            .start(&StatsigRuntime::get_runtime(), fixture.view.clone())
            .await
            .unwrap();
        assert_eq!(fixture.adapter.role_for_test().await, "http_fallback");
        assert!(fixture.view.0.lock()["members"].ids.contains("bbbbbbbb"));
        if let Some(renewal) = failed_renewal {
            renewal.assert();
        }
        manifest.assert();
        tail.assert();
        fixture.adapter.force_shutdown();
    }
}

#[tokio::test]
#[serial]
async fn publication_clock_is_sampled_after_files_are_ready() {
    let fixture = Fixture::new().await;
    let next = fixture.updated();
    let catalog = fixture
        .store
        .publish_with_clock(&fixture.lease, &next, &HashMap::new(), None, || {
            let images = std::fs::read_dir(fixture.store.directory())
                .unwrap()
                .filter_map(Result::ok)
                .filter(|entry| entry.path().extension().is_some_and(|value| value == "ids"))
                .count();
            // Both committed old image and newly prepared image exist at this point.
            assert_eq!(images, 2);
            123_456
        })
        .unwrap();
    assert_eq!(catalog.status.successful_refresh_ms, 123_456);
    assert_eq!(
        fixture
            .store
            .load()
            .unwrap()
            .unwrap()
            .status
            .successful_refresh_ms,
        123_456
    );
    assert!(catalog.lists["members"].ids.contains("bbbbbbbb"));
    fixture.adapter.force_shutdown();
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
#[serial]
async fn publication_still_in_flight_past_budget_does_not_get_unbounded_grace() {
    let mut fixture = Fixture::new().await;
    let expected = fixture.expect_private_delta();
    let last_success = now_ms() - 178_000;
    fixture
        .store
        .publish(
            &fixture.lease,
            &fixture.initial,
            &HashMap::new(),
            last_success,
        )
        .unwrap();
    fixture.adapter.poll_for_test().await.unwrap();
    assert_eq!(fixture.adapter.role_for_test().await, "follower");
    assert!(fixture.view.0.lock()["members"].ids.is_mapped());
    let next = fixture.updated();
    let store = fixture.store.clone();
    let lease = fixture.lease.clone();
    let (entered, observed) = mpsc::channel();
    let (release, resumed) = mpsc::channel();
    let publisher = std::thread::spawn(move || {
        store
            .publish_with_clock(&lease, &next, &HashMap::new(), None, || {
                entered.send(()).unwrap();
                resumed.recv_timeout(Duration::from_secs(10)).unwrap();
                now_ms()
            })
            .unwrap()
    });
    observed.recv_timeout(Duration::from_secs(2)).unwrap();
    // The installed manifest stays unchanged while the next publication is blocked.
    tokio::time::sleep(Duration::from_millis(
        (last_success + 180_001).saturating_sub(now_ms()),
    ))
    .await;
    let result = fixture.adapter.poll_for_test().await;
    release.send(()).unwrap();
    let committed = publisher.join().unwrap();
    result.unwrap();
    assert_eq!(fixture.adapter.role_for_test().await, "http_fallback");
    assert!(fixture.view.0.lock()["members"].ids.contains("bbbbbbbb"));
    assert!(!fixture.view.0.lock()["members"].ids.is_mapped());
    assert!(committed.lists["members"].ids.is_mapped());
    expected.0.assert();
    expected.1.assert();
    fixture.adapter.force_shutdown();
}

#[tokio::test]
#[serial]
async fn fast_polling_keeps_sharing_through_a_short_refresh_failure() {
    let fixture = Fixture::new().await;
    fixture
        .store
        .publish(
            &fixture.lease,
            &fixture.initial,
            &HashMap::new(),
            now_ms() - 45_000,
        )
        .unwrap();
    fixture.adapter.poll_for_test().await.unwrap();
    assert_eq!(fixture.adapter.role_for_test().await, "follower");
    assert!(fixture.view.0.lock()["members"].ids.is_mapped());

    let next = fixture.updated();
    fixture
        .store
        .publish(&fixture.lease, &next, &HashMap::new(), now_ms())
        .unwrap();
    fixture.adapter.poll_for_test().await.unwrap();
    assert_eq!(fixture.adapter.role_for_test().await, "follower");
    assert!(fixture.view.0.lock()["members"].ids.contains("bbbbbbbb"));
    fixture.adapter.force_shutdown();
}
