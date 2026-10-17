#![cfg(feature = "ffi-support")]

mod utils;

use serde_json::Value;
use statsig_rust::evaluation::evaluator_result::EvaluatorResult;
use statsig_rust::specs_response::spec_types::Spec;
use statsig_rust::user::statsig_user_internal::StatsigUserInternal;
use statsig_rust::{
    DynamicConfigEvaluationOptions, OverrideAdapter, Statsig, StatsigOptions, StatsigUser,
};
use std::collections::HashMap;
use std::sync::{Arc, Mutex, mpsc};
use std::time::Duration;
use utils::mock_specs_adapter::MockSpecsAdapter;

// Evaluation calls this adapter only after acquiring its immutable specs snapshot.
// Block that point without adding a production hook or blocking the SDK runtime.
struct PausedOverride {
    entered: Mutex<Option<mpsc::SyncSender<()>>>,
    resume: Mutex<mpsc::Receiver<()>>,
}

impl OverrideAdapter for PausedOverride {
    fn get_dynamic_config_override(
        &self,
        _: &StatsigUser,
        name: &str,
        _: &mut EvaluatorResult,
    ) -> bool {
        if name != "test_max_dynamic_config_size_again" {
            return false;
        }
        let Some(entered) = self.entered.lock().unwrap().take() else {
            return false;
        };
        entered.send(()).unwrap();
        self.resume
            .lock()
            .unwrap()
            .recv_timeout(Duration::from_secs(5))
            .unwrap();
        false
    }

    fn get_gate_override(&self, _: &StatsigUser, _: &str, _: &mut EvaluatorResult) -> bool {
        false
    }
    fn get_experiment_override(
        &self,
        _: &StatsigUser,
        _: &str,
        _: &mut EvaluatorResult,
        _: Option<&Spec>,
    ) -> bool {
        false
    }
    fn get_layer_override(&self, _: &StatsigUser, _: &str, _: &mut EvaluatorResult) -> bool {
        false
    }
    fn get_parameter_store_override(
        &self,
        _: &StatsigUser,
        _: &str,
        _: &mut EvaluatorResult,
    ) -> bool {
        false
    }
    fn override_gate(&self, _: &str, _: bool, _: Option<&str>) {}
    fn override_dynamic_config(&self, _: &str, _: HashMap<String, Value>, _: Option<&str>) {}
    fn override_experiment(&self, _: &str, _: HashMap<String, Value>, _: Option<&str>) {}
    fn override_experiment_by_group_name(&self, _: &str, _: &str, _: Option<&str>) {}
    fn override_layer(&self, _: &str, _: HashMap<String, Value>, _: Option<&str>) {}
    fn override_parameter_store(&self, _: &str, _: HashMap<String, Value>, _: Option<&str>) {}
    fn remove_gate_override(&self, _: &str, _: Option<&str>) {}
    fn remove_dynamic_config_override(&self, _: &str, _: Option<&str>) {}
    fn remove_experiment_override(&self, _: &str, _: Option<&str>) {}
    fn remove_layer_override(&self, _: &str, _: Option<&str>) {}
    fn remove_parameter_store_override(&self, _: &str, _: Option<&str>) {}
    fn remove_all_overrides(&self) {}
}

#[tokio::test]
async fn packaged_eligibility_uses_pinned_specs_across_initialization() {
    let (entered, on_entered) = mpsc::sync_channel(1);
    let (resume, on_resume) = mpsc::sync_channel(1);
    let sdk = Arc::new(Statsig::new(
        "secret-initialization-race",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(Arc::new(MockSpecsAdapter::with_data(
                "tests/data/eval_proj_dcs.json",
            ))),
            override_adapter: Some(Arc::new(PausedOverride {
                entered: Mutex::new(Some(entered)),
                resume: Mutex::new(on_resume),
            })),
            disable_all_logging: Some(true),
            disable_network: Some(true),
            disable_country_lookup: Some(true),
            enable_id_lists: Some(false),
            ..StatsigOptions::new()
        })),
    ));
    let reading_sdk = sdk.clone();
    let reading = std::thread::spawn(move || {
        let user = StatsigUser::with_user_id("startup-user");
        reading_sdk.use_typed_config_with_packaged_fallback(
            &StatsigUserInternal::new(&user, Some(&reading_sdk)),
            "test_max_dynamic_config_size_again",
            DynamicConfigEvaluationOptions {
                disable_exposure_logging: true,
            },
            true,
            |raw, _, _, eligible, _| (raw.details.reason.clone(), eligible),
        )
    });
    on_entered.recv_timeout(Duration::from_secs(5)).unwrap();
    let initialized = sdk.initialize().await;
    // Always release the reading thread before asserting the initialization result.
    resume.send(()).unwrap();
    let (reason, eligible) = reading.join().unwrap();
    initialized.unwrap();
    assert!(sdk.is_config_spec_ready());
    assert_eq!(reason, "Uninitialized");
    assert!(
        eligible,
        "this read pinned empty specs before initialization published remote specs"
    );
    let user = StatsigUser::with_user_id("startup-user");
    assert!(!sdk.use_typed_config_with_packaged_fallback(
        &StatsigUserInternal::new(&user, Some(&sdk)),
        "test_max_dynamic_config_size_again",
        DynamicConfigEvaluationOptions::default(),
        true,
        |_, _, _, eligible, _| eligible,
    ));
    sdk.shutdown().await.unwrap();
}
