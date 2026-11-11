use super::{
    ConfigResponseType, ConfigSyncCursor, DELTAS_USED_HEADER, SpecDecodeStats, SpecStore,
    SpecStoreData, build_live_overlay_target_app_index,
};
use crate::data_store_interface::{DataStoreResponse, DataStoreTrait, RequestPath};
use crate::hashing::HashUtil;
use crate::networking::ResponseData;
use crate::sdk_event_emitter::SdkEventEmitter;
use crate::snapshot_evaluation_session::SnapshotEvaluationSession;
use crate::specs_response::spec_types::SpecsResponseFull;
use crate::statsig_options::SnapshotEvaluationSessionInitOptions;
use crate::statsig_runtime::StatsigRuntime;
use crate::{SpecsSource, SpecsUpdate, StatsigErr, StatsigOptions};
use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::{Arc, OnceLock};
use std::time::{Duration, Instant};

struct CacheCapabilityDataStore(bool, bool);

#[async_trait]
impl DataStoreTrait for CacheCapabilityDataStore {
    fn is_read_only(&self) -> bool {
        self.0
    }

    fn write_once(&self) -> bool {
        self.1
    }

    async fn initialize(&self) -> Result<(), StatsigErr> {
        unreachable!()
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        unreachable!()
    }

    async fn get(&self, _key: &str) -> Result<DataStoreResponse, StatsigErr> {
        unreachable!()
    }

    async fn set(&self, _key: &str, _value: &str, _time: Option<u64>) -> Result<(), StatsigErr> {
        unreachable!()
    }

    async fn support_polling_updates_for(&self, _path: RequestPath) -> bool {
        unreachable!()
    }
}

#[test]
fn cache_capture_and_writes_require_a_writable_network_full_response() {
    let full_data = ResponseData::from_bytes(Vec::new());
    let delta_data = ResponseData::from_bytes_with_headers(
        Vec::new(),
        Some(HashMap::from([(
            DELTAS_USED_HEADER.to_string(),
            "true".to_string(),
        )])),
    );
    for (read_only, write_once) in [
        (None, false),
        (Some(false), false),
        (Some(true), false),
        (Some(false), true),
        (Some(true), true),
    ] {
        let options = StatsigOptions {
            data_store: read_only.map(|read_only| {
                Arc::new(CacheCapabilityDataStore(read_only, write_once)) as Arc<dyn DataStoreTrait>
            }),
            ..StatsigOptions::default()
        };
        let store = SpecStore::new(
            "cache-capability",
            "cache-capability".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            Some(&options),
        );
        // The hydration parser's capture flag and the eventual write share
        // this predicate, so read-only stores never construct an encoder.
        assert_eq!(
            store
                .writable_data_store_for_update(&SpecsSource::Network, &full_data)
                .is_some(),
            read_only == Some(false)
        );
        assert!(
            store
                .writable_data_store_for_update(&SpecsSource::Network, &delta_data)
                .is_none()
        );
        assert!(
            store
                .writable_data_store_for_update(
                    &SpecsSource::Adapter("DataStore".to_string()),
                    &full_data
                )
                .is_none()
        );
        store
            .data_store_write_claimed
            .store(true, std::sync::atomic::Ordering::Release);
        assert_eq!(
            store
                .writable_data_store_for_update(&SpecsSource::Network, &full_data)
                .is_some(),
            read_only == Some(false) && !write_once,
            "an in-flight publication must disable capture and writes only for opted-in stores",
        );
        store
            .data_store_write_claimed
            .store(false, std::sync::atomic::Ordering::Release);
        assert_eq!(
            store
                .writable_data_store_for_update(&SpecsSource::Network, &full_data)
                .is_some(),
            read_only == Some(false),
            "abandoning publication must leave writes available",
        );
    }
}

#[test]
fn shared_id_list_snapshots_never_wait_for_config_updates() {
    let runtime = StatsigRuntime::get_runtime();
    let emitter = Arc::new(SdkEventEmitter::default());
    let owner = SpecStore::new(
        "secret-shared-owner",
        "shared-owner".to_string(),
        Arc::clone(&runtime),
        Arc::clone(&emitter),
        None,
    );
    let scoped = SpecStore::new(
        "client-shared-scope",
        "shared-scope".to_string(),
        runtime,
        emitter,
        None,
    );

    let update_guard = scoped.update_lock.lock();
    let started = Instant::now();
    let contended = scoped.load_data_with_shared_id_lists(&owner);
    assert!(started.elapsed() < Duration::from_secs(1));
    assert!(Arc::ptr_eq(
        &contended.id_lists,
        &owner.load_data().id_lists
    ));
    assert!(!Arc::ptr_eq(
        &contended.id_lists,
        &scoped.load_data().id_lists
    ));
    drop(update_guard);

    let published = scoped.load_data_with_shared_id_lists(&owner);
    assert!(Arc::ptr_eq(
        &published.id_lists,
        &owner.load_data().id_lists
    ));
    assert!(Arc::ptr_eq(&published, &scoped.load_data()));
    assert!(Arc::ptr_eq(
        &published,
        &scoped.load_data_with_shared_id_lists(&owner)
    ));
}

#[test]
fn applied_response_type_uses_delta_header() {
    let delta_data = ResponseData::from_bytes_with_headers(
        Vec::new(),
        Some(HashMap::from([(
            DELTAS_USED_HEADER.to_string(),
            "true".to_string(),
        )])),
    );
    let full_data = ResponseData::from_bytes(Vec::new());

    assert_eq!(
        ConfigResponseType::from_applied_response_data(&delta_data).as_str(),
        "delta"
    );
    assert_eq!(
        ConfigResponseType::from_applied_response_data(&full_data).as_str(),
        "full"
    );
}

#[test]
fn config_only_snapshots_skip_process_wide_heap_trimming() {
    let runtime = StatsigRuntime::get_runtime();
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let standard = SpecStore::new(
        "standard-snapshot-trim",
        "standard".to_string(),
        runtime.clone(),
        event_emitter.clone(),
        None,
    );
    let config_only = SpecStore::new_with_snapshot_evaluation_session_options(
        "config-only-snapshot-trim",
        "config-only".to_string(),
        runtime,
        event_emitter,
        None,
        &SnapshotEvaluationSessionInitOptions {
            config_only_mode: true,
            ..SnapshotEvaluationSessionInitOptions::default()
        },
    );

    assert!(standard.release_unused_heap_memory_after_update);
    assert!(!config_only.release_unused_heap_memory_after_update);
    assert!(standard.internal_observability_enabled);
    assert!(!config_only.internal_observability_enabled);
}

#[test]
fn scoped_checksum_mismatch_never_publishes_or_advances_the_snapshot() {
    let store = SpecStore::new_with_snapshot_evaluation_session_options(
        "scoped-checksum-guard",
        "scoped-checksum-guard".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
        &SnapshotEvaluationSessionInitOptions {
            config_only_mode: true,
            ..SnapshotEvaluationSessionInitOptions::default()
        },
    );
    let mut specs: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
    specs["time"] = serde_json::json!(100);
    specs["checksum"] = serde_json::json!("initial-checksum");
    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
            source: SpecsSource::Network,
            received_at: 1,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    let original = store.load_data();

    specs["time"] = serde_json::json!(200);
    specs["checksum"] = serde_json::json!("incorrect-payload-checksum");
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
    data.set_scoped_expected_checksum("expected-metadata-checksum");
    let result = store.set_values(SpecsUpdate {
        data,
        source: SpecsSource::Adapter("ScopedConfigSource".to_string()),
        received_at: 2,
        source_api: Some("ScopedConfigSource".to_string()),
        has_updates: None,
    });

    assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
    let unchanged = store.load_data();
    assert!(Arc::ptr_eq(&original, &unchanged));
    assert_eq!(unchanged.lcut(), 100);
    assert_eq!(unchanged.checksum(), Some("initial-checksum"));

    let mut future_lcut_data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
    future_lcut_data.set_scoped_expected_checksum("incorrect-payload-checksum");
    future_lcut_data.set_scoped_expected_lcut(150);
    let result = store.set_values(SpecsUpdate {
        data: future_lcut_data,
        source: SpecsSource::Adapter("ScopedConfigSource".to_string()),
        received_at: 3,
        source_api: Some("ScopedConfigSource".to_string()),
        has_updates: None,
    });

    assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
    let unchanged = store.load_data();
    assert!(Arc::ptr_eq(&original, &unchanged));
    assert_eq!(unchanged.lcut(), 100);
    assert_eq!(unchanged.checksum(), Some("initial-checksum"));

    let mut network_data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
    network_data.set_scoped_expected_checksum("irrelevant-scoped-header");
    network_data.set_scoped_expected_lcut(50);
    store
        .set_values(SpecsUpdate {
            data: network_data,
            source: SpecsSource::Network,
            received_at: 4,
            source_api: None,
            has_updates: None,
        })
        .expect("scoped metadata must never constrain ordinary network updates");
    assert_eq!(
        store.load_data().checksum(),
        Some("incorrect-payload-checksum")
    );

    specs["time"] = serde_json::json!(250);
    specs["checksum"] = serde_json::json!("older-than-metadata-checksum");
    let mut older_lcut_data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
    older_lcut_data.set_scoped_expected_checksum("older-than-metadata-checksum");
    older_lcut_data.set_scoped_expected_lcut(300);
    store
        .set_values(SpecsUpdate {
            data: older_lcut_data,
            source: SpecsSource::Adapter("ScopedConfigSource".to_string()),
            received_at: 5,
            source_api: Some("ScopedConfigSource".to_string()),
            has_updates: None,
        })
        .expect("older payloads must remain eligible for metadata cursor catch-up");
    assert_eq!(store.load_data().lcut(), 250);
}

#[test]
fn config_only_snapshots_preserve_sdk_configs_without_projecting_global_state() {
    let runtime = StatsigRuntime::get_runtime();
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let standard = SpecStore::new(
        "standard-global-projection",
        "standard-global-projection".to_string(),
        runtime.clone(),
        event_emitter.clone(),
        None,
    );
    let config_only = SpecStore::new_with_snapshot_evaluation_session_options(
        "config-only-global-projection",
        "config-only-global-projection".to_string(),
        runtime,
        event_emitter,
        None,
        &SnapshotEvaluationSessionInitOptions {
            config_only_mode: true,
            ..SnapshotEvaluationSessionInitOptions::default()
        },
    );
    let mut specs: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
    specs["sdk_configs"] = serde_json::json!({ "snapshot_config": "preserved" });
    specs["sdk_flags"] = serde_json::json!({ "snapshot_flag": true });
    specs["diagnostics"] = serde_json::json!({ "initialize": 7.0 });
    let payload = serde_json::to_vec(&specs).unwrap();

    for store in [&standard, &config_only] {
        store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(payload.clone()),
                source: SpecsSource::Network,
                received_at: 1,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
    }

    let standard_globals = standard.global_configs.as_ref().unwrap();
    assert!(standard_globals.get_sdk_flag_value("snapshot_flag"));
    standard_globals.use_sdk_config_value("snapshot_config", |value| {
        assert_eq!(
            value.map(|value| &value.json_value),
            Some(&serde_json::json!("preserved"))
        );
    });
    assert!(config_only.global_configs.is_none());
    assert_eq!(
        config_only
            .load_data()
            .snapshot
            .sdk_configs
            .as_ref()
            .and_then(|configs| configs.get("snapshot_config"))
            .map(|value| &value.json_value),
        Some(&serde_json::json!("preserved"))
    );
    assert_eq!(
        config_only
            .load_data()
            .snapshot
            .sdk_flags
            .as_ref()
            .and_then(|flags| flags.get("snapshot_flag")),
        Some(&true)
    );
}

#[test]
fn only_config_only_snapshots_prepare_evaluation_metadata() {
    let runtime = StatsigRuntime::get_runtime();
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let standard = SpecStore::new(
        "standard-snapshot-preparation",
        "standard-snapshot-preparation".to_string(),
        runtime.clone(),
        event_emitter.clone(),
        None,
    );
    let config_only = SpecStore::new_with_snapshot_evaluation_session_options(
        "config-only-snapshot-preparation",
        "config-only-snapshot-preparation".to_string(),
        runtime,
        event_emitter,
        None,
        &SnapshotEvaluationSessionInitOptions {
            config_only_mode: true,
            preserve_dcs_session_update_mode: true,
            ..SnapshotEvaluationSessionInitOptions::default()
        },
    );
    let mut specs: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
    specs["auto_capture_settings"] = serde_json::json!({
        "disabled_events": { "click": true }
    });
    specs["condition_map"]["snapshot-id-list"] = serde_json::json!({
        "type": "unit_id",
        "targetValue": "beta_users",
        "operator": "in_segment_list",
        "idType": "userID"
    });
    specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = serde_json::json!("live");
    specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
        serde_json::json!(["prepared-app"]);
    let payload = serde_json::to_vec(&specs).unwrap();

    for store in [&standard, &config_only] {
        store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(payload.clone()),
                source: SpecsSource::Network,
                received_at: 1,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
    }

    let standard_data = standard.load_data();
    assert!(!standard_data.has_id_list_conditions);
    assert!(standard_data.auto_capture_settings_value.is_none());
    assert_eq!(standard_data.auto_capture_settings_hash, 0);
    assert!(standard_data.live_overlay_target_app_index.get().is_none());

    let config_only_data = config_only.load_data();
    assert!(config_only_data.has_id_list_conditions);
    assert!(
        config_only_data
            .id_list_lookup_conditions()
            .iter()
            .any(|condition| condition.name == "beta_users")
    );
    assert!(config_only_data.auto_capture_settings_value.is_some());
    assert_ne!(config_only_data.auto_capture_settings_hash, 0);
    let index = config_only_data
        .live_overlay_target_app_index
        .get()
        .expect("config-only snapshots should prepare live target app metadata");
    assert!(index.has_live_entities);
    assert!(index.target_app_ids.contains("prepared-app"));
}

#[test]
fn spec_store_data_reuses_gcir_evaluation_plan_cache_across_clones() {
    let data = SpecStoreData {
        source: SpecsSource::Network,
        source_api: Some("/v2/download_config_specs".to_string()),
        time_received_at: Some(1),
        snapshot: Arc::new(SpecsResponseFull::default()),
        id_lists: Arc::new(HashMap::new()),
        has_id_list_conditions: false,
        may_have_time_dependent_evaluations: true,
        id_list_lookup_conditions: Arc::new(OnceLock::new()),
        id_list_dependencies: Arc::new(Default::default()),
        auto_capture_settings_value: None,
        auto_capture_settings_hash: 0,
        live_overlay_target_app_index: Arc::new(Default::default()),
        gcir_evaluation_plan: Arc::new(OnceLock::new()),
        sync_cursor: ConfigSyncCursor::default(),
        spec_decode_stats: SpecDecodeStats::default(),
        field_checksums: Default::default(),
        verified_remote_values: Arc::new(Default::default()),
    };
    let hashing = HashUtil::new();

    let first = data.gcir_evaluation_plan(&hashing);
    let cloned = data.clone();
    let second = cloned.gcir_evaluation_plan(&hashing);

    assert!(std::ptr::eq(first, second));
    assert!(Arc::ptr_eq(
        &data.live_overlay_target_app_index,
        &cloned.live_overlay_target_app_index
    ));
    assert!(Arc::ptr_eq(
        &data.id_list_lookup_conditions,
        &cloned.id_list_lookup_conditions
    ));
}

#[test]
fn semantic_snapshot_updates_replace_live_target_app_index_but_cursor_updates_reuse_it() {
    let store = SpecStore::new_with_snapshot_evaluation_session_options(
        "live-overlay-snapshot-index",
        "live-overlay-snapshot-index".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
        &SnapshotEvaluationSessionInitOptions {
            config_only_mode: true,
            preserve_dcs_session_update_mode: true,
            ..SnapshotEvaluationSessionInitOptions::default()
        },
    );
    let mut specs: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
    specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = serde_json::json!("live");
    specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
        serde_json::json!(["first-app"]);

    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
            source: SpecsSource::Network,
            received_at: 1,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    let first = store.load_data();
    assert!(
        first
            .live_overlay_target_app_index
            .get()
            .unwrap()
            .target_app_ids
            .contains("first-app")
    );

    store.specs_cursor_update_apply(
        first.lcut() + 1,
        "cursor-only-checksum".to_string(),
        SpecsSource::Network,
        None,
    );
    let cursor_only = store.load_data();
    assert!(Arc::ptr_eq(&first.snapshot, &cursor_only.snapshot,));
    assert!(Arc::ptr_eq(
        &first.live_overlay_target_app_index,
        &cursor_only.live_overlay_target_app_index,
    ));
    assert!(Arc::ptr_eq(
        &first.id_list_lookup_conditions,
        &cursor_only.id_list_lookup_conditions,
    ));

    specs["time"] = serde_json::json!(cursor_only.lcut() + 1);
    specs["checksum"] = serde_json::json!("semantic-update-checksum");
    specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
        serde_json::json!(["second-app"]);
    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
            source: SpecsSource::Network,
            received_at: 2,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    let refreshed = store.load_data();
    assert!(!Arc::ptr_eq(
        &cursor_only.live_overlay_target_app_index,
        &refreshed.live_overlay_target_app_index,
    ));
    assert!(!Arc::ptr_eq(
        &cursor_only.id_list_lookup_conditions,
        &refreshed.id_list_lookup_conditions,
    ));
    let refreshed_index = refreshed.live_overlay_target_app_index.get().unwrap();
    assert!(refreshed_index.target_app_ids.contains("second-app"));
    assert!(!refreshed_index.target_app_ids.contains("first-app"));
}

#[test]
fn standard_snapshot_sessions_build_live_target_app_index_lazily() {
    let store = SpecStore::new_with_snapshot_evaluation_session_options(
        "standard-live-overlay-index",
        "standard-live-overlay-index".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
        &SnapshotEvaluationSessionInitOptions {
            preserve_dcs_session_update_mode: true,
            ..SnapshotEvaluationSessionInitOptions::default()
        },
    );
    let mut specs: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
    specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = serde_json::json!("live");
    specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] =
        serde_json::json!(["standard-app"]);
    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
            source: SpecsSource::Network,
            received_at: 1,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    let data = store.load_data();
    assert!(data.live_overlay_target_app_index.get().is_none());

    let hashing = HashUtil::new();
    let session = SnapshotEvaluationSession::new(Arc::clone(&data), &hashing, false);
    assert!(session.has_live_overlay_entities_for_target_app(Some("standard-app")));
    assert!(!session.has_live_overlay_entities_for_target_app(Some("other-app")));
    assert!(session.has_live_overlay_entities_for_target_app(None));
    assert!(data.live_overlay_target_app_index.get().is_some());
}

#[test]
fn live_target_app_index_ignores_unscoped_and_non_live_entities() {
    let mut specs: serde_json::Value =
        serde_json::from_slice(include_bytes!("../../tests/data/eval_proj_dcs.json")).unwrap();
    specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = serde_json::json!("live");
    specs["feature_gates"]["test_small_pass_gate"]
        .as_object_mut()
        .unwrap()
        .remove("targetAppIDs");
    specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] =
        serde_json::json!(["non-live-app"]);
    let specs: SpecsResponseFull = serde_json::from_value(specs).unwrap();
    let index = build_live_overlay_target_app_index(&specs);

    assert!(index.has_live_entities);
    assert!(index.target_app_ids.is_empty());
}
