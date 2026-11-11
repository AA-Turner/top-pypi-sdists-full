use async_trait::async_trait;
use rusty_fork::rusty_fork_test;
use std::sync::atomic::AtomicUsize;

use super::*;
use crate::{
    SpecsUpdate,
    interned_values::{
        InternedStore,
        interned_store::{preload_mmap_v2_multi_for_test, write_mmap_v2_for_test},
    },
    networking::{HttpMethod, NetworkProvider, RequestArgs, Response, ResponseData},
};

const EVAL_PROJ_JSON: &[u8] = include_bytes!("../../tests/data/eval_proj_dcs.json");

const LAZY_CONFIG_ID_LIST_MANIFEST_URL: &str = "https://lists.test/manifest";
const LAZY_CONFIG_ID_LIST_FILE_URL: &str = "https://lists.test/lazy-members";

#[derive(Default)]
struct CapturingEventLoggingAdapter {
    payloads: Mutex<Vec<crate::log_event_payload::LogEventPayload>>,
}

#[async_trait]
impl EventLoggingAdapter for CapturingEventLoggingAdapter {
    async fn start(&self, _statsig_runtime: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        Ok(())
    }

    async fn log_events(
        &self,
        request: crate::log_event_payload::LogEventRequest,
    ) -> Result<bool, StatsigErr> {
        self.payloads.lock().push(request.payload);
        Ok(true)
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        Ok(())
    }

    fn should_schedule_background_flush(&self) -> bool {
        false
    }
}

struct LazyConfigIdListProvider {
    delay: Duration,
    member_hash: String,
    downloads: AtomicUsize,
    first_body_gate: Mutex<Option<Arc<tokio::sync::Semaphore>>>,
}

impl LazyConfigIdListProvider {
    fn new(delay: Duration, member_hash: String) -> Self {
        Self {
            delay,
            member_hash,
            downloads: AtomicUsize::new(0),
            first_body_gate: Mutex::new(None),
        }
    }
}

#[async_trait]
impl NetworkProvider for LazyConfigIdListProvider {
    async fn send(&self, _method: &HttpMethod, args: &RequestArgs) -> Response {
        if args.url == LAZY_CONFIG_ID_LIST_MANIFEST_URL {
            let body = format!("+{}\n", self.member_hash);
            return Response {
                status_code: Some(200),
                data: Some(ResponseData::from_bytes(
                    serde_json::to_vec(&json!({
                        "lazy-members": {
                            "name": "lazy-members",
                            "url": LAZY_CONFIG_ID_LIST_FILE_URL,
                            "fileID": "generation-1",
                            "size": body.len(),
                            "creationTime": 1,
                        },
                        "replacement-members": {
                            "name": "replacement-members",
                            "url": "https://lists.test/replacement-members",
                            "fileID": "generation-1",
                            "size": body.len(),
                            "creationTime": 1,
                        }
                    }))
                    .unwrap(),
                )),
                error: None,
            };
        }

        self.downloads.fetch_add(1, Ordering::SeqCst);
        if args.url == LAZY_CONFIG_ID_LIST_FILE_URL {
            let gate = self.first_body_gate.lock().clone();
            if let Some(gate) = gate {
                gate.acquire().await.unwrap().forget();
            } else {
                tokio::time::sleep(self.delay).await;
            }
        }
        let body = format!("+{}\n", self.member_hash);
        Response {
            status_code: Some(200),
            data: Some(ResponseData::from_bytes(body.into_bytes())),
            error: None,
        }
    }
}

async fn setup_lazy_config_test(delay: Duration) -> (Statsig, Arc<LazyConfigIdListProvider>) {
    let (statsig, provider, _) = setup_lazy_config_test_with_logging(delay, false).await;
    (statsig, provider)
}

async fn setup_lazy_config_test_with_logging(
    delay: Duration,
    capture_events: bool,
) -> (
    Statsig,
    Arc<LazyConfigIdListProvider>,
    Option<Arc<CapturingEventLoggingAdapter>>,
) {
    setup_lazy_config_test_with_option(delay, capture_events, Some(true)).await
}

async fn setup_lazy_config_test_with_option(
    delay: Duration,
    capture_events: bool,
    lazy_load_id_lists: Option<bool>,
) -> (
    Statsig,
    Arc<LazyConfigIdListProvider>,
    Option<Arc<CapturingEventLoggingAdapter>>,
) {
    let hash = HashUtil::new().sha256("lazy-member");
    let provider = Arc::new(LazyConfigIdListProvider::new(
        delay,
        hash.chars().take(8).collect(),
    ));
    let event_logging_adapter =
        capture_events.then(|| Arc::new(CapturingEventLoggingAdapter::default()));
    let options = Arc::new(StatsigOptions {
        sdk_instance_id: Some(uuid::Uuid::new_v4().to_string()),
        enable_id_lists: Some(true),
        lazy_load_id_lists,
        id_lists_url: Some(LAZY_CONFIG_ID_LIST_MANIFEST_URL.to_string()),
        disable_all_logging: Some(!capture_events),
        event_logging_adapter: event_logging_adapter
            .clone()
            .map(|adapter| adapter as Arc<dyn EventLoggingAdapter>),
        ..StatsigOptions::default()
    });
    let mut statsig = Statsig::new("secret-lazy-config-test", Some(Arc::clone(&options)));
    let mut adapter = StatsigHttpIdListsAdapter::new_with_store(
        "secret-lazy-config-test",
        &options,
        statsig.spec_store.clone(),
    );
    let network: Arc<dyn NetworkProvider> = provider.clone();
    adapter.set_network_provider_for_test(Arc::downgrade(&network));
    let adapter = Arc::new(adapter);
    statsig.id_lists_adapter = IdListsAdapterHousing {
        inner: Some(adapter.clone()),
        as_default_adapter: Some(adapter.clone()),
        as_shared_adapter: None,
    };
    adapter
        .clone()
        .start(&statsig.statsig_runtime, statsig.spec_store.clone())
        .await
        .unwrap();

    let mut specs: Value = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
    specs["condition_map"]["lazy-id-list"] = json!({
        "type": "unit_id",
        "targetValue": "lazy-members",
        "operator": "in_segment_list",
        "idType": "userID"
    });
    specs["condition_map"]["lazy-id-list-exclusion"] = json!({
        "type": "unit_id",
        "targetValue": "lazy-members",
        "operator": "not_in_segment_list",
        "idType": "userID"
    });
    specs["condition_map"]["lazy-nested-gate"] = json!({
        "type": "pass_gate",
        "targetValue": "lazy-list-gate",
        "operator": null,
        "idType": "userID"
    });
    specs["condition_map"]["lazy-nested-fail-gate"] = json!({
        "type": "fail_gate",
        "targetValue": "lazy-list-gate",
        "operator": null,
        "idType": "userID"
    });
    specs["condition_map"]["lazy-public"] = json!({
        "type": "public",
        "targetValue": null,
        "operator": null,
        "idType": "userID"
    });
    let mut list_gate = specs["feature_gates"]["test_small_pass_gate"].clone();
    list_gate["rules"][0]["passPercentage"] = json!(100);
    list_gate["rules"][0]["salt"] = json!("");
    list_gate["rules"][0]["conditions"] = json!(["lazy-id-list"]);
    specs["feature_gates"]["lazy-list-gate"] = list_gate;
    let mut exclusion_gate = specs["feature_gates"]["test_small_pass_gate"].clone();
    exclusion_gate["rules"][0]["passPercentage"] = json!(100);
    exclusion_gate["rules"][0]["salt"] = json!("");
    exclusion_gate["rules"][0]["conditions"] = json!(["lazy-id-list-exclusion"]);
    specs["feature_gates"]["lazy-exclusion-gate"] = exclusion_gate;
    for (name, condition) in [
        ("lazy-pass-gate-wrapper", "lazy-nested-gate"),
        ("lazy-fail-gate-wrapper", "lazy-nested-fail-gate"),
    ] {
        let mut wrapper = specs["feature_gates"]["test_small_pass_gate"].clone();
        wrapper["rules"] = json!([{
            "name": "nested",
            "passPercentage": 100,
            "conditions": [condition],
            "returnValue": true,
            "id": "nested",
            "salt": "",
            "idType": "userID"
        }, {
            "name": "later",
            "passPercentage": 100,
            "conditions": ["lazy-public"],
            "returnValue": true,
            "id": "later",
            "salt": "",
            "idType": "userID"
        }]);
        specs["feature_gates"][name] = wrapper;
    }
    for (name, condition) in [
        ("lazy-inclusion-config", "lazy-id-list"),
        ("lazy-exclusion-config", "lazy-id-list-exclusion"),
    ] {
        specs["dynamic_configs"][name] = json!({
            "type": "dynamic_config",
            "salt": name,
            "enabled": true,
            "defaultValue": {"selected": "default"},
            "rules": [{
                "name": "id-list",
                "passPercentage": 100,
                "conditions": [condition],
                "returnValue": {"selected": "id-list"},
                "id": "id-list",
                "salt": "",
                "idType": "userID"
            }, {
                "name": "later",
                "passPercentage": 100,
                "conditions": ["lazy-public"],
                "returnValue": {"selected": "later"},
                "id": "later",
                "salt": "",
                "idType": "userID"
            }],
            "idType": "userID",
            "entity": "dynamic_config",
            "version": 1
        });
    }
    specs["dynamic_configs"]["lazy-config"] = json!({
        "type": "dynamic_config",
        "salt": "lazy-config",
        "enabled": true,
        "defaultValue": {"loaded": false},
        "rules": [{
            "name": "lazy-rule",
            "passPercentage": 100,
            "conditions": ["lazy-nested-gate"],
            "returnValue": {"loaded": true},
            "id": "lazy-rule",
            "salt": "",
            "idType": "userID"
        }],
        "idType": "userID",
        "entity": "dynamic_config",
        "version": 1
    });
    specs["dynamic_configs"]["lazy-experiment"] = json!({
        "type": "dynamic_config",
        "salt": "lazy-experiment",
        "enabled": true,
        "defaultValue": {"group": "default"},
        "rules": [{
            "name": "member",
            "groupName": "Member",
            "passPercentage": 100,
            "conditions": ["lazy-id-list"],
            "returnValue": {"group": "member"},
            "id": "member",
            "salt": "",
            "idType": "userID",
            "isExperimentGroup": true
        }],
        "idType": "userID",
        "entity": "experiment",
        "isActive": true,
        "version": 1
    });
    specs["layer_configs"]["lazy-layer"] = json!({
        "type": "dynamic_config",
        "salt": "lazy-layer",
        "enabled": true,
        "defaultValue": {"loaded": false},
        "rules": [{
            "name": "member",
            "passPercentage": 100,
            "conditions": ["lazy-id-list"],
            "returnValue": {"loaded": true},
            "id": "member",
            "salt": "",
            "idType": "userID"
        }],
        "idType": "userID",
        "entity": "layer",
        "version": 1
    });
    statsig
        .spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
            source: SpecsSource::Network,
            received_at: 2_000,
            source_api: Some("lazy-config-test".to_string()),
            has_updates: None,
        })
        .unwrap();
    (statsig, provider, event_logging_adapter)
}

#[tokio::test]
async fn get_dynamic_config_downloads_reachable_id_lists_without_an_async_api() {
    let (statsig, adapter) = setup_lazy_config_test(Duration::ZERO).await;
    let config =
        statsig.get_dynamic_config(&StatsigUser::with_user_id("lazy-member"), "lazy-config");

    assert_eq!(config.get_opt::<bool>("loaded"), Some(true));
    assert_eq!(adapter.downloads.load(Ordering::SeqCst), 1);

    let cached =
        statsig.get_dynamic_config(&StatsigUser::with_user_id("lazy-member"), "lazy-config");
    assert_eq!(cached.get_opt::<bool>("loaded"), Some(true));
    assert_eq!(adapter.downloads.load(Ordering::SeqCst), 1);
}

#[tokio::test]
async fn direct_gate_experiment_and_layer_apis_lazy_load_id_lists() {
    let user = StatsigUser::with_user_id("lazy-member");

    let (gate_statsig, gate_provider, gate_events) =
        setup_lazy_config_test_with_logging(Duration::ZERO, true).await;
    let gate = gate_statsig.get_feature_gate(&user, "lazy-list-gate");
    assert!(gate.value);
    assert_eq!(gate_provider.downloads.load(Ordering::SeqCst), 1);
    gate_statsig.flush_events().await;
    let gate_events = gate_events.unwrap();
    {
        let payloads = gate_events.payloads.lock();
        let exposure = payloads
            .iter()
            .flat_map(|payload| payload.events.as_array().into_iter().flatten())
            .find(|event| event["eventName"] == "statsig::gate_exposure")
            .expect("direct gate evaluation should log its exposure");
        assert_eq!(exposure["metadata"]["gate"], "lazy-list-gate");
        assert_eq!(exposure["metadata"]["gateValue"], "true");
    }

    let (experiment_statsig, experiment_provider) = setup_lazy_config_test(Duration::ZERO).await;
    let experiment = experiment_statsig.get_experiment(&user, "lazy-experiment");
    assert_eq!(
        experiment.get_opt::<String>("group").as_deref(),
        Some("member")
    );
    assert_eq!(experiment_provider.downloads.load(Ordering::SeqCst), 1);

    let (layer_statsig, layer_provider) = setup_lazy_config_test(Duration::ZERO).await;
    let layer = layer_statsig.get_layer(&user, "lazy-layer");
    assert_eq!(layer.get_opt::<bool>("loaded"), Some(true));
    assert_eq!(layer_provider.downloads.load(Ordering::SeqCst), 1);
}

#[tokio::test]
async fn lazy_load_timeout_partially_evaluates_logs_reason_and_reports_ops_stats() {
    let (statsig, adapter, event_logging_adapter) =
        setup_lazy_config_test_with_logging(Duration::from_millis(200), true).await;
    let event_logging_adapter = event_logging_adapter.unwrap();
    let mut ops_stats = statsig.ops_stats.subscribe_for_test();
    let started = Instant::now();
    let timed_out =
        statsig.get_dynamic_config(&StatsigUser::with_user_id("lazy-member"), "lazy-config");

    assert!(started.elapsed() < Duration::from_millis(150));
    assert_eq!(timed_out.get_opt::<bool>("loaded"), None);
    assert!(
        timed_out
            .details
            .reason
            .ends_with(":PartialEvaluation:IdListLoadTimeout")
    );
    assert!(timed_out.details.reason.contains(":Unsupported"));
    let metric = loop {
        match ops_stats.try_recv() {
            Ok(crate::observability::ops_stats::OpsStatsEvent::Observability(event))
                if event.metric_name == "lazy_id_list_load.count" =>
            {
                break event;
            }
            Ok(_) => continue,
            Err(error) => panic!("missing lazy-load OpsStats metric: {error}"),
        }
    };
    let tags = metric.tags.unwrap();
    assert_eq!(tags.get("outcome").map(String::as_str), Some("timeout"));
    assert_eq!(
        tags.get("spec_type").map(String::as_str),
        Some("dynamic_config")
    );

    statsig.flush_events().await;
    {
        let payloads = event_logging_adapter.payloads.lock();
        let exposure = payloads
            .iter()
            .flat_map(|payload| payload.events.as_array().into_iter().flatten())
            .find(|event| event["eventName"] == "statsig::config_exposure")
            .expect("partial evaluation should still log a config exposure");
        assert_eq!(
            exposure["metadata"]["reason"],
            timed_out.details.reason.as_str()
        );
    }

    tokio::time::sleep(Duration::from_millis(250)).await;
    let loaded =
        statsig.get_dynamic_config(&StatsigUser::with_user_id("lazy-member"), "lazy-config");
    assert_eq!(loaded.get_opt::<bool>("loaded"), Some(true));
    assert_eq!(adapter.downloads.load(Ordering::SeqCst), 1);
}

#[tokio::test]
async fn unavailable_id_list_is_unsupported_and_stops_later_rules() {
    let (statsig, _) = setup_lazy_config_test(Duration::from_millis(200)).await;
    let user = StatsigUser::with_user_id("not-a-member");

    for name in ["lazy-inclusion-config", "lazy-exclusion-config"] {
        let config = statsig.get_dynamic_config(&user, name);
        assert_ne!(
            config.get_opt::<String>("selected").as_deref(),
            Some("later"),
            "{name} must not select the later public rule"
        );
        assert_ne!(config.rule_id, "later");
        assert!(config.details.reason.contains(":Unsupported"));
        assert!(
            config
                .details
                .reason
                .ends_with(":PartialEvaluation:IdListLoadTimeout")
        );
    }
}

#[tokio::test]
async fn unavailable_id_list_propagates_through_pass_and_fail_gate() {
    let (statsig, _) = setup_lazy_config_test(Duration::from_millis(200)).await;
    let user = StatsigUser::with_user_id("not-a-member");

    for name in ["lazy-pass-gate-wrapper", "lazy-fail-gate-wrapper"] {
        let gate = statsig.get_feature_gate(&user, name);
        assert!(!gate.value, "{name} must preserve the unresolved result");
        assert_ne!(gate.rule_id, "later", "{name} must not select a later rule");
        assert!(gate.details.reason.contains(":Unsupported"));
        assert!(
            gate.details
                .reason
                .ends_with(":PartialEvaluation:IdListLoadTimeout")
        );
    }
}

#[tokio::test]
async fn unset_and_disabled_lazy_loading_remain_eager() {
    let user = StatsigUser::with_user_id("lazy-member");

    for lazy_load_id_lists in [None, Some(false)] {
        let (statsig, provider, _) =
            setup_lazy_config_test_with_option(Duration::ZERO, false, lazy_load_id_lists).await;
        let eager_downloads = provider.downloads.load(Ordering::SeqCst);
        assert_eq!(eager_downloads, 2);

        let config = statsig.get_dynamic_config(&user, "lazy-config");
        assert_eq!(config.get_opt::<bool>("loaded"), Some(true));
        assert!(!config.details.reason.contains("PartialEvaluation"));
        assert_eq!(provider.downloads.load(Ordering::SeqCst), eager_downloads);
    }
}

#[tokio::test]
async fn spec_update_during_load_revalidates_and_evaluates_one_snapshot() {
    let (statsig, provider) = setup_lazy_config_test(Duration::ZERO).await;
    let first_body_gate = Arc::new(tokio::sync::Semaphore::new(0));
    *provider.first_body_gate.lock() = Some(Arc::clone(&first_body_gate));
    let updated_specs = json!({
        "feature_gates": {
            "lazy-list-gate": {
                "type": "feature_gate",
                "salt": "lazy-list-gate",
                "enabled": true,
                "defaultValue": false,
                "rules": [{
                    "name": "member",
                    "passPercentage": 100,
                    "conditions": ["lazy-id-list"],
                    "returnValue": true,
                    "id": "member",
                    "salt": "",
                    "idType": "userID"
                }],
                "idType": "userID",
                "entity": "feature_gate",
                "version": 2
            }
        },
        "dynamic_configs": {
            "lazy-config": {
                "type": "dynamic_config",
                "salt": "lazy-config",
                "enabled": true,
                "defaultValue": {"loaded": false},
                "rules": [{
                    "name": "lazy-rule",
                    "passPercentage": 100,
                    "conditions": ["lazy-nested-gate"],
                    "returnValue": {"loaded": true},
                    "id": "lazy-rule",
                    "salt": "",
                    "idType": "userID"
                }],
                "idType": "userID",
                "entity": "dynamic_config",
                "version": 2
            }
        },
        "layer_configs": {},
        "experiment_to_layer": {},
        "param_stores": {},
        "condition_map": {
            "lazy-id-list": {
                "type": "unit_id",
                "targetValue": "replacement-members",
                "operator": "in_segment_list",
                "idType": "userID"
            },
            "lazy-nested-gate": {
                "type": "pass_gate",
                "targetValue": "lazy-list-gate",
                "operator": null,
                "idType": "userID"
            }
        },
        "time": 1767981029385_u64,
        "checksum": "lazy-replacement-generation",
        "has_updates": true
    });

    let statsig = Arc::new(statsig);
    let updater = {
        let statsig = Arc::clone(&statsig);
        let provider = Arc::clone(&provider);
        let first_body_gate = Arc::clone(&first_body_gate);
        std::thread::spawn(move || {
            while provider.downloads.load(Ordering::SeqCst) == 0 {
                std::thread::yield_now();
            }
            statsig
                .spec_store
                .set_values(SpecsUpdate {
                    data: ResponseData::from_bytes(serde_json::to_vec(&updated_specs).unwrap()),
                    source: SpecsSource::Network,
                    received_at: 2_001,
                    source_api: Some("lazy-config-race-test".to_string()),
                    has_updates: None,
                })
                .unwrap();
            first_body_gate.add_permits(1);
        })
    };

    let config =
        statsig.get_dynamic_config(&StatsigUser::with_user_id("lazy-member"), "lazy-config");
    updater.join().unwrap();

    assert_eq!(
        config.get_opt::<bool>("loaded"),
        Some(true),
        "reason={}, downloads={}",
        config.details.reason,
        provider.downloads.load(Ordering::SeqCst)
    );
    assert!(!config.details.reason.contains("PartialEvaluation"));
    assert_eq!(provider.downloads.load(Ordering::SeqCst), 2);
}

rusty_fork_test! {
    #[test]
    fn experiment_group_lookups_do_not_materialize_mmap_specs() {
        assert!(!InternedStore::has_preloaded_mmap_v2());
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-group-lookup.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_multi_for_test(&[("secret-key", &path)]).unwrap();
        assert!(InternedStore::has_preloaded_mmap_v2());

        let statsig = Statsig::new("secret-key", None);
        statsig
            .spec_store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(EVAL_PROJ_JSON.to_vec()),
                source: SpecsSource::Network,
                received_at: 2_000,
                source_api: Some("mmap-group-test".to_string()),
                has_updates: None,
            })
            .unwrap();

        let experiment_name = "test_experiment_no_targeting";
        let group_name = "Control";
        let group_id = "54QJztEPRLXK7ZCvXeY9q4";
        assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);

        let by_name = statsig.get_experiment_by_group_name(experiment_name, group_name);
        let by_id = statsig.get_experiment_by_group_id_advanced(experiment_name, group_id);
        assert_eq!(by_name.rule_id, group_id);
        assert_eq!(by_id.group_name.as_deref(), Some(group_name));

        #[cfg(feature = "ffi-support")]
        {
            for raw in [
                statsig.get_raw_experiment_by_group_name(experiment_name, group_name),
                statsig.get_raw_experiment_by_group_id_advanced(experiment_name, group_id),
            ] {
                let raw: Value = serde_json::from_str(&raw).unwrap();
                assert_eq!(raw["ruleID"], group_id);
                assert_eq!(raw["groupName"], group_name);
                assert_eq!(raw["value"]["value"], "control");
            }
        }

        assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);
    }
}
