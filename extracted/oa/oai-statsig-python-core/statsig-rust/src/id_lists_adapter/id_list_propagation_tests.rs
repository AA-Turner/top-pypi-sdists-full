use super::*;
use crate::SpecStore;
use crate::networking::{HttpMethod, NetworkProvider};
use crate::observability::ops_stats::OpsStatsEvent;
use crate::sdk_event_emitter::SdkEventEmitter;
use crate::statsig_options::SnapshotEvaluationSessionInitOptions;
use parking_lot::Mutex;
use serde_json::{Value, json};
use tokio::sync::broadcast::Receiver;

const MANIFEST_URL: &str = "https://manifest.test/lists";

#[derive(Clone)]
struct FileResponse {
    body: Option<String>,
    content_range: Option<String>,
}

#[derive(Default)]
struct Provider {
    manifest: Mutex<serde_json::Map<String, Value>>,
    files: Mutex<HashMap<String, FileResponse>>,
    requests: Mutex<Vec<RequestArgs>>,
}

#[async_trait]
impl NetworkProvider for Provider {
    async fn send(&self, _: &HttpMethod, args: &RequestArgs) -> Response {
        self.requests.lock().push(args.clone());
        let data = if args.url == MANIFEST_URL {
            Some(ResponseData::from_bytes(
                serde_json::to_vec(&*self.manifest.lock()).unwrap(),
            ))
        } else {
            let file = self.files.lock()[&args.url].clone();
            file.body.map(|body| {
                ResponseData::from_bytes_with_headers(
                    body.into_bytes(),
                    file.content_range
                        .map(|range| HashMap::from([("content-range".into(), range)])),
                )
            })
        };
        Response {
            status_code: Some(200),
            data,
            error: None,
        }
    }
}

struct Fixture {
    provider: Arc<Provider>,
    adapter: StatsigHttpIdListsAdapter,
    store: Arc<SpecStore>,
    events: Receiver<OpsStatsEvent>,
}

impl Fixture {
    fn new() -> Self {
        Self::with_config_only_mode(false)
    }

    fn with_config_only_mode(config_only_mode: bool) -> Self {
        Self::with_observability(config_only_mode, false, false)
    }

    fn with_observability(config_only_mode: bool, disabled: bool, silent: bool) -> Self {
        let provider = Arc::new(Provider::default());
        let sdk_key = format!("secret-id-list-propagation-{}", uuid::Uuid::new_v4());
        let ordinary_ops = OPS_STATS.get_for_instance(&sdk_key);
        let events = ordinary_ops.subscribe_for_test();
        let _scope = disabled.then(|| {
            OPS_STATS
                .enter_instance_scope(&sdk_key, Some(Arc::new(OpsStatsForInstance::disabled())))
        });
        let options = StatsigOptions {
            id_lists_url: Some(MANIFEST_URL.into()),
            ..StatsigOptions::default()
        }
        .suppress_diagnostic_output(silent);
        let mut adapter = StatsigHttpIdListsAdapter::new(&sdk_key, &options);
        let dynamic: Arc<dyn NetworkProvider> = provider.clone();
        adapter
            .network
            .set_network_provider_for_test(Arc::downgrade(&dynamic));
        let store = Arc::new(SpecStore::new_with_snapshot_evaluation_session_options(
            &sdk_key,
            "id-list-propagation-test".into(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            Some(&options),
            &SnapshotEvaluationSessionInitOptions {
                config_only_mode,
                ..SnapshotEvaluationSessionInitOptions::default()
            },
        ));
        adapter.set_listener(store.clone());
        assert_eq!(adapter.ops_stats.is_disabled_for_test(), disabled || silent);
        Self {
            provider,
            adapter,
            store,
            events,
        }
    }

    fn set(&self, name: &str, file: &str, creation: i64, start: u64, body: &str, ts: Option<u64>) {
        let size = start + body.len() as u64;
        let mut metadata = json!({
            "name": name, "url": format!("https://files.test/{name}"),
            "fileID": file, "creationTime": creation, "size": size,
        });
        if let Some(ts) = ts {
            metadata["ts"] = json!(ts);
        }
        self.provider.manifest.lock().insert(name.into(), metadata);
        self.provider.files.lock().insert(
            format!("https://files.test/{name}"),
            FileResponse {
                body: Some(body.into()),
                content_range: size
                    .checked_sub(1)
                    .map(|end| format!("bytes {start}-{end}/{size}")),
            },
        );
    }

    fn metrics(&mut self) -> Vec<ObservabilityEvent> {
        let mut metrics = Vec::new();
        while let Ok(event) = self.events.try_recv() {
            if let OpsStatsEvent::Observability(event) = event {
                if event.metric_name == "id_list_propagation_diff" {
                    metrics.push(event);
                }
            }
        }
        metrics
    }

    fn set_signed_url(&self, name: &str, signature: &str) {
        let base_url = format!("https://files.test/{name}");
        let signed_url = format!("{base_url}?sig={signature}");
        let file = self.provider.files.lock().remove(&base_url).unwrap();
        self.provider.files.lock().insert(signed_url.clone(), file);
        self.provider.manifest.lock()[name]["url"] = json!(signed_url);
    }

    fn ranges(&self) -> Vec<String> {
        self.provider
            .requests
            .lock()
            .iter()
            .filter(|request| request.url != MANIFEST_URL)
            .map(|request| request.headers.as_ref().unwrap()["Range"].clone())
            .collect()
    }
}

fn source_times() -> (u64, u64) {
    let now = Utc::now().timestamp_millis() as u64;
    (now - 120_000, now - 60_000)
}

#[tokio::test]
async fn id_list_propagation_shared_owner_config_only_store_emits_after_install() {
    let mut fixture = Fixture::with_config_only_mode(true);
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    fixture.set("users", "A", 1, 3, "+p\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert_eq!(fixture.metrics().len(), 1);
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
}

#[tokio::test]
async fn id_list_propagation_respects_disabled_and_silent_observability() {
    for (disabled, silent) in [(true, false), (false, true)] {
        let mut fixture = Fixture::with_observability(true, disabled, silent);
        let (old, new) = source_times();
        fixture.set("users", "A", 1, 0, "+a\n", Some(old));
        fixture.adapter.sync_id_lists().await.unwrap();
        fixture.set("users", "A", 1, 3, "+p\n", Some(new));
        fixture.adapter.sync_id_lists().await.unwrap();
        assert!(fixture.metrics().is_empty());
        assert!(
            fixture.store.load_data().id_lists["users"]
                .ids
                .contains("p")
        );
    }
}

#[tokio::test]
async fn id_list_propagation_measures_installed_append_without_evaluation() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(
        fixture.metrics().is_empty(),
        "initial hydration is not propagation"
    );
    let before = fixture.store.load_data();

    fixture.set("users", "A", 1, 3, "+p\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    let metrics = fixture.metrics();
    assert_eq!(metrics.len(), 1);
    assert!(matches!(metrics[0].metric_type, MetricType::Dist));
    assert!((60_000.0..120_000.0).contains(&metrics[0].value));
    let tags = metrics[0].tags.as_ref().unwrap();
    assert_eq!(tags["id_list_name"], "users");
    assert_eq!(tags["source"], "Network");
    assert_eq!(tags["lcut"], new.to_string());
    assert_eq!(tags["prev_lcut"], old.to_string());
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
    assert!(!before.id_lists["users"].ids.contains("p"));

    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=3-"]);

    let added = fixture.store.load_data();
    fixture.set("users", "A", 1, 6, "-p\n", Some(new + 1));
    fixture.adapter.sync_id_lists().await.unwrap();
    let metrics = fixture.metrics();
    assert_eq!(metrics.len(), 1);
    assert_eq!(
        metrics[0].tags.as_ref().unwrap()["lcut"],
        (new + 1).to_string()
    );
    assert!(
        !fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
    assert!(added.id_lists["users"].ids.contains("p"));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=3-", "bytes=6-"]);
}

#[tokio::test]
async fn id_list_propagation_first_timestamp_on_existing_list_is_measured() {
    let mut fixture = Fixture::new();
    fixture.set("users", "A", 1, 0, "+a\n", None);
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());

    let (_, ts) = source_times();
    fixture.set("users", "A", 1, 3, "+p\n", Some(ts));
    fixture.adapter.sync_id_lists().await.unwrap();
    let metrics = fixture.metrics();
    assert_eq!(metrics.len(), 1);
    assert_eq!(metrics[0].tags.as_ref().unwrap()["lcut"], ts.to_string());
    assert_eq!(metrics[0].tags.as_ref().unwrap()["prev_lcut"], "0");
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
}

#[tokio::test]
async fn id_list_propagation_smaller_replacement_counts_source_once() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n+p\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());

    fixture.set("users", "B", 2, 0, "+p\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert_eq!(fixture.metrics().len(), 1);
    let data = fixture.store.load_data();
    assert_eq!(
        data.id_lists["users"].metadata.file_id.as_deref(),
        Some("B")
    );
    assert_eq!(data.id_lists["users"].metadata.size, 3);
    assert_eq!(data.id_lists["users"].ids.len(), 1);

    fixture.set("users", "C", 3, 0, "+p\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(
        fixture.metrics().is_empty(),
        "pure regeneration must not repeat source time"
    );
    assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=0-", "bytes=0-"]);
}

#[tokio::test]
async fn id_list_propagation_failed_batch_does_not_consume_source_time() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    for name in ["a", "b"] {
        fixture.set(name, "A", 1, 0, "+old\n", Some(old));
    }
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    let before = fixture.store.load_data();
    for name in ["a", "b"] {
        fixture.set(name, "A", 1, 5, "+new\n", Some(new));
    }
    fixture
        .provider
        .files
        .lock()
        .get_mut("https://files.test/b")
        .unwrap()
        .body = None;
    assert!(fixture.adapter.sync_id_lists().await.is_err());
    assert!(fixture.metrics().is_empty());
    assert!(Arc::ptr_eq(
        &before.id_lists,
        &fixture.store.load_data().id_lists
    ));

    fixture.set("b", "A", 1, 5, "+new\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert_eq!(fixture.metrics().len(), 2);
    for name in ["a", "b"] {
        assert!(fixture.store.load_data().id_lists[name].ids.contains("new"));
        assert!(!before.id_lists[name].ids.contains("new"));
    }
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
}

#[tokio::test]
async fn id_list_propagation_optional_fields_do_not_change_delivery() {
    for fields in [
        json!({}),
        json!({"ts":"bad"}),
        json!({"ts":{}}),
        json!({"ts":-1}),
        json!({"ts":null}),
        json!({"ts":0}),
        json!({"ts":1.5}),
        json!({"ts":u64::MAX}),
    ] {
        let mut fixture = Fixture::new();
        for (start, body) in [(0, "+a\n"), (3, "+p\n")] {
            fixture.set("users", "A", 1, start, body, None);
            fixture.provider.manifest.lock()["users"]
                .as_object_mut()
                .unwrap()
                .extend(fields.as_object().unwrap().clone());
            fixture.adapter.sync_id_lists().await.unwrap();
        }
        assert!(fixture.metrics().is_empty());
        assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=3-"]);
        let data = fixture.store.load_data();
        assert_eq!(data.id_lists["users"].metadata.size, 6);
        assert_eq!(data.id_lists["users"].ids.len(), 2);
        assert!(data.id_lists["users"].ids.contains("p"));
    }
}

#[tokio::test]
async fn id_list_propagation_replay_cannot_invent_contiguous_coverage() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    fixture.set("users", "A", 2, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    // Preserve the existing cursor behavior: replay counts bytes again. Telemetry must not.
    assert_eq!(fixture.store.load_data().id_lists["users"].metadata.size, 6);
    fixture.set("users", "A", 1, 6, "+p\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(
        fixture.metrics().is_empty(),
        "bytes 3..6 were never downloaded"
    );
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
    assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=0-", "bytes=6-"]);
}

#[tokio::test]
async fn id_list_propagation_unproven_response_range_only_skips_metric() {
    for range in ["bytes 3-8/9", "bytes 4-6/7", "invalid"] {
        let mut fixture = Fixture::new();
        let (old, new) = source_times();
        fixture.set("users", "A", 1, 0, "+a\n", Some(old));
        fixture.adapter.sync_id_lists().await.unwrap();
        fixture.set("users", "A", 1, 3, "+p\n", Some(new));
        fixture
            .provider
            .files
            .lock()
            .get_mut("https://files.test/users")
            .unwrap()
            .content_range = Some(range.into());
        fixture.adapter.sync_id_lists().await.unwrap();
        assert!(fixture.metrics().is_empty());
        assert!(
            fixture.store.load_data().id_lists["users"]
                .ids
                .contains("p")
        );
        assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=3-"]);
    }
}

#[tokio::test]
async fn id_list_propagation_late_metadata_does_not_measure_manifest_delay() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    fixture.set("users", "A", 1, 3, "+p\n", None);
    fixture.adapter.sync_id_lists().await.unwrap();
    fixture.set("users", "A", 1, 0, "+a\n+p\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=3-"]);
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
}

#[tokio::test]
async fn id_list_propagation_sas_rotation_preserves_append_coverage() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.set_signed_url("users", "old");
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());

    fixture.set("users", "A", 1, 3, "+p\n", Some(new));
    fixture.set_signed_url("users", "renewed");
    fixture.adapter.sync_id_lists().await.unwrap();

    let metrics = fixture.metrics();
    assert_eq!(metrics.len(), 1);
    assert_eq!(metrics[0].tags.as_ref().unwrap()["lcut"], new.to_string());
    assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=3-"]);
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
}

#[tokio::test]
async fn id_list_propagation_sas_rotation_does_not_retime_late_checkpoint() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.set_signed_url("users", "old");
    fixture.adapter.sync_id_lists().await.unwrap();
    fixture.set("users", "A", 1, 3, "+p\n", None);
    fixture.set_signed_url("users", "old");
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());

    // The existing creationTime behavior replays the same file, but its bytes
    // were already applied before the checkpoint and renewed SAS arrived.
    fixture.set("users", "A", 2, 0, "+a\n+p\n", Some(new));
    fixture.set_signed_url("users", "renewed");
    fixture.adapter.sync_id_lists().await.unwrap();

    assert!(fixture.metrics().is_empty());
    assert_eq!(fixture.ranges(), ["bytes=0-", "bytes=3-", "bytes=0-"]);
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
}

#[tokio::test]
async fn id_list_propagation_empty_replacement_is_an_applied_change() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    fixture.set("users", "B", 2, 0, "", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert_eq!(fixture.metrics().len(), 1);
    assert!(fixture.store.load_data().id_lists["users"].ids.is_empty());
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
}

#[tokio::test]
async fn id_list_propagation_replica_switch_cannot_reuse_another_prefix() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 1, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    fixture.set("users", "A", 1, 3, "+p\n", Some(new));
    let url = "https://files.test/users?private=true";
    fixture.provider.manifest.lock()["users"]["url"] = json!(url);
    let response = fixture.provider.files.lock()["https://files.test/users"].clone();
    fixture.provider.files.lock().insert(url.into(), response);
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    assert!(
        fixture.store.load_data().id_lists["users"]
            .ids
            .contains("p")
    );
}

#[tokio::test]
async fn id_list_propagation_cdn_query_range_accepts_200_without_content_range() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    let url = "https://statsigcdn.openai.com/file";
    for (start, body, lcut) in [(0, "+a\n", old), (3, "+p\n", new)] {
        fixture.set("users", "A", 1, start, body, Some(lcut));
        fixture.provider.manifest.lock()["users"]["url"] = json!(url);
        fixture.provider.files.lock().insert(
            url.into(),
            FileResponse {
                body: Some(body.into()),
                content_range: None,
            },
        );
        fixture.adapter.sync_id_lists().await.unwrap();
    }
    assert_eq!(fixture.metrics().len(), 1);
    let requests = fixture.provider.requests.lock();
    let request = requests.last().unwrap();
    assert!(
        request
            .headers
            .as_ref()
            .is_none_or(|headers| !headers.contains_key("Range"))
    );
    assert_eq!(request.query_params.as_ref().unwrap()["range"], "3-");
}

#[tokio::test]
async fn id_list_propagation_rejected_older_generation_does_not_emit() {
    let mut fixture = Fixture::new();
    let (old, new) = source_times();
    fixture.set("users", "A", 2, 0, "+a\n", Some(old));
    fixture.adapter.sync_id_lists().await.unwrap();
    fixture.set("users", "B", 1, 0, "+p\n", Some(new));
    fixture.adapter.sync_id_lists().await.unwrap();
    assert!(fixture.metrics().is_empty());
    assert_eq!(
        fixture.store.load_data().id_lists["users"]
            .metadata
            .file_id
            .as_deref(),
        Some("A")
    );
}
