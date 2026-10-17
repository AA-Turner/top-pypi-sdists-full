#![cfg(feature = "ffi-support")]

mod utils;

use async_trait::async_trait;
use serde_json::{Value, json};
use statsig_rust::networking::ResponseData;
use statsig_rust::user::statsig_user_internal::StatsigUserInternal;
use statsig_rust::{
    DynamicConfigEvaluationOptions, SpecsAdapter, SpecsSource, SpecsUpdate, SpecsUpdateListener,
    Statsig, StatsigErr, StatsigLocalOverrideAdapter, StatsigOptions, StatsigRuntime, StatsigUser,
};
use std::sync::{Arc, Mutex};
use std::time::Duration;
use tokio::sync::Notify;
use utils::mock_event_logging_adapter::MockEventLoggingAdapter;

#[derive(Default)]
struct FailingStartup {
    listener: Mutex<Option<Arc<dyn SpecsUpdateListener>>>,
    block_start: bool,
    fail_schedule: bool,
    schedule_entered: Notify,
    started: Notify,
}

impl FailingStartup {
    fn publish(&self, data: Value) -> Result<(), StatsigErr> {
        self.listener
            .lock()
            .unwrap()
            .as_ref()
            .unwrap()
            .did_receive_specs_update(SpecsUpdate {
                data: ResponseData::from_bytes(serde_json::to_vec(&data).unwrap()),
                source: SpecsSource::Network,
                received_at: 123,
                source_api: None,
                has_updates: None,
            })
    }
}

#[async_trait]
impl SpecsAdapter for FailingStartup {
    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>) {
        *self.listener.lock().unwrap() = Some(listener);
    }

    async fn start(self: Arc<Self>, _: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        self.started.notify_one();
        if self.block_start {
            std::future::pending::<()>().await;
        }
        Err(StatsigErr::CustomError("initial fetch failed".into()))
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        _: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.schedule_entered.notify_one();
        if self.fail_schedule {
            return Err(StatsigErr::CustomError("cannot start polling".into()));
        }
        Ok(())
    }

    async fn shutdown(&self, _: Duration, _: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        Ok(())
    }

    fn get_type_name(&self) -> String {
        "FailingStartup".into()
    }
}

fn setup(
    adapter: Arc<FailingStartup>,
    timeout: Option<u64>,
) -> (Arc<Statsig>, Arc<MockEventLoggingAdapter>) {
    let events = Arc::new(MockEventLoggingAdapter::new_with_background_flush(false));
    let sdk = Arc::new(Statsig::new(
        "secret-packaged-test",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(adapter),
            event_logging_adapter: Some(events.clone()),
            override_adapter: Some(Arc::new(StatsigLocalOverrideAdapter::new())),
            environment: Some("production".into()),
            disable_country_lookup: Some(true),
            init_timeout_ms: timeout,
            ..StatsigOptions::new()
        })),
    ));
    (sdk, events)
}

fn eligible(sdk: &Statsig, name: &str, allow: bool) -> bool {
    let user = StatsigUser::with_user_id("test-user");
    sdk.use_typed_config_with_packaged_fallback(
        &StatsigUserInternal::new(&user, Some(sdk)),
        name,
        DynamicConfigEvaluationOptions::default(),
        allow,
        |_, _, _, eligible, _| eligible,
    )
}

fn empty_snapshot() -> Value {
    json!({"time": 0, "has_updates": true, "feature_gates": {}, "dynamic_configs": {},
        "layer_configs": {}, "condition_map": {}, "experiment_to_layer": {}, "response_format": "dcs-v2"})
}

fn snapshot_with_config(value: Value, time: u64) -> Value {
    let mut snapshot = empty_snapshot();
    snapshot["time"] = json!(time);
    snapshot["dynamic_configs"]["config"] = json!({
        "type": "dynamic_config", "salt": "config", "enabled": true,
        "defaultValue": value, "idType": "userID", "version": time,
        "entity": "dynamic_config", "rules": []
    });
    snapshot
}

#[tokio::test]
async fn packaged_eligibility_respects_opt_in_overrides_and_snapshot_availability() {
    let adapter = Arc::new(FailingStartup::default());
    let (sdk, _) = setup(adapter.clone(), None);
    assert!(eligible(&sdk, "config", true));
    assert!(!eligible(&sdk, "config", false));
    assert!(sdk.initialize().await.is_err());
    assert!(eligible(&sdk, "config", true));
    assert!(!eligible(&sdk, "config", false));

    sdk.override_dynamic_config("config", [("number".into(), json!(12))].into(), None);
    assert!(!eligible(&sdk, "config", true));
    assert!(eligible(&sdk, "other-config", true));

    // A successfully loaded empty snapshot forbids fallback even with a zero LCUT.
    adapter.publish(empty_snapshot()).unwrap();
    assert!(!eligible(&sdk, "other-config", true));
    assert!(!sdk.is_config_spec_ready());
    assert!(
        adapter
            .publish(json!({"dynamic_configs": 5, "time": 2}))
            .is_err()
    );
    assert!(!eligible(&sdk, "other-config", true));
    sdk.remove_all_overrides();
    for (index, value) in [json!({"number": 12}), json!({}), Value::Null]
        .into_iter()
        .enumerate()
    {
        adapter
            .publish(snapshot_with_config(value, index as u64 + 1))
            .unwrap();
        assert!(!eligible(&sdk, "config", true));
    }
    let mut unsupported = snapshot_with_config(json!({}), 4);
    unsupported["condition_map"]["unknown"] = json!({"type": "unsupported_condition", "operator": "any", "targetValue": null, "idType": "userID"});
    unsupported["dynamic_configs"]["config"]["rules"] = json!([{
        "id": "unsupported", "name": "unsupported", "salt": "config", "conditions": ["unknown"],
        "passPercentage": 100, "returnValue": {}, "idType": "userID"
    }]);
    adapter.publish(unsupported).unwrap();
    assert!(!eligible(&sdk, "config", true));

    let mut deleted = empty_snapshot();
    deleted["time"] = json!(5);
    adapter.publish(deleted).unwrap();
    assert!(!eligible(&sdk, "config", true));
    assert!(!eligible(&sdk, "config", false));
    let user = StatsigUser::with_user_id("untyped-user");
    assert_eq!(
        sdk.get_dynamic_config(&user, "config").details.reason,
        "Network:Unrecognized"
    );
    sdk.shutdown().await.unwrap();
    assert!(!eligible(&sdk, "config", true));
}

#[tokio::test]
async fn packaged_eligibility_is_pinned_and_never_logs_a_remote_exposure() {
    let adapter = Arc::new(FailingStartup::default());
    let (sdk, events) = setup(adapter.clone(), None);
    assert!(sdk.initialize().await.is_err());
    let user = StatsigUser::with_user_id("test-user");
    sdk.use_typed_config_with_packaged_fallback(
        &StatsigUserInternal::new(&user, Some(&sdk)),
        "config",
        DynamicConfigEvaluationOptions::default(),
        true,
        |_, _, _, eligible, _| {
            assert!(eligible);
            // A remote publication during the read cannot change this result's
            // exposure decision or make the next read use the package.
            adapter
                .publish(snapshot_with_config(json!({"number": 12}), 1))
                .unwrap();
        },
    );
    sdk.flush_events().await;
    {
        let payloads = events.logged_payloads.lock().unwrap();
        assert!(!payloads.iter().any(|p| {
            p.events
                .as_array()
                .unwrap()
                .iter()
                .any(|e| e["eventName"] == "statsig::config_exposure")
        }));
    }
    assert!(!eligible(&sdk, "config", true));
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
async fn packaged_eligibility_does_not_require_initialization_or_background_setup() {
    let adapter = Arc::new(FailingStartup {
        block_start: true,
        fail_schedule: true,
        ..Default::default()
    });
    let (sdk, _) = setup(adapter.clone(), Some(30));
    let init_sdk = sdk.clone();
    let init = tokio::spawn(async move { init_sdk.initialize().await });
    adapter.started.notified().await;
    assert!(eligible(&sdk, "config", true));
    assert!(
        tokio::time::timeout(Duration::from_secs(1), init)
            .await
            .unwrap()
            .unwrap()
            .is_err()
    );
    adapter.schedule_entered.notified().await;
    assert!(eligible(&sdk, "config", true));
    sdk.shutdown().await.unwrap();
    assert!(eligible(&sdk, "config", true));

    let (sdk, _) = setup(
        Arc::new(FailingStartup {
            fail_schedule: true,
            ..Default::default()
        }),
        None,
    );
    assert!(!sdk.initialize_with_details().await.unwrap().init_success);
    assert!(eligible(&sdk, "config", true));
    sdk.shutdown().await.unwrap();
}

#[tokio::test]
async fn packaged_tier_matches_remote_environment_rules() {
    let adapter = Arc::new(FailingStartup::default());
    let (sdk, _) = setup(adapter.clone(), None);
    assert!(sdk.initialize().await.is_err());
    let plain_user = StatsigUser::with_user_id("plain");
    let mut staging_user = StatsigUser::with_user_id("staging");
    staging_user.set_statsig_environment(Some([("tier", "staging")].into()));
    let mut tiers = Vec::new();
    for (user, expected) in [(&plain_user, "production"), (&staging_user, "staging")] {
        let tier = sdk.use_typed_config_with_packaged_fallback(
            &StatsigUserInternal::new(user, Some(&sdk)),
            "config",
            DynamicConfigEvaluationOptions::default(),
            true,
            |_, _, _, eligible, tier| {
                assert!(eligible);
                tier.unwrap()
            },
        );
        assert_eq!(tier, expected);
        tiers.push(tier);
    }
    let mut snapshot = snapshot_with_config(json!({"tier": "production"}), 1);
    snapshot["condition_map"]["staging"] = json!({
        "type": "environment_field", "field": "tier", "operator": "any",
        "targetValue": ["staging"], "idType": "userID"
    });
    snapshot["dynamic_configs"]["config"]["rules"] = json!([{
        "id": "staging", "name": "staging", "salt": "config", "conditions": ["staging"],
        "passPercentage": 100, "returnValue": {"tier": "staging"}, "idType": "userID"
    }]);
    adapter.publish(snapshot).unwrap();
    for (user, tier) in [&plain_user, &staging_user].into_iter().zip(tiers) {
        assert_eq!(
            sdk.get_dynamic_config(user, "config")
                .get("tier", String::new()),
            tier
        );
    }
    sdk.shutdown().await.unwrap();
}
