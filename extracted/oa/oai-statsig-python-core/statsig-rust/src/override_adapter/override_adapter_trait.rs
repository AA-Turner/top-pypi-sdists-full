use crate::evaluation::evaluator_result::EvaluatorResult;
use crate::specs_response::spec_types::Spec;
use crate::StatsigUser;
use serde_json::Value;
use std::collections::HashMap;

pub trait OverrideAdapter: Send + Sync {
    fn has_any_overrides_for_gate(&self, _gate_name: &str) -> bool {
        true
    }

    fn has_any_overrides_for_dynamic_config(&self, _dynamic_config_name: &str) -> bool {
        true
    }

    fn has_any_overrides_for_experiment(&self, _experiment_name: &str) -> bool {
        true
    }

    fn has_any_overrides_for_layer(&self, _layer_name: &str) -> bool {
        true
    }

    fn has_any_overrides_for_parameter_store(&self, _parameter_store_name: &str) -> bool {
        true
    }

    fn get_gate_override(
        &self,
        user: &StatsigUser,
        gate_name: &str,
        result: &mut EvaluatorResult,
    ) -> bool;

    fn get_dynamic_config_override(
        &self,
        user: &StatsigUser,
        dynamic_config_name: &str,
        result: &mut EvaluatorResult,
    ) -> bool;

    fn get_experiment_override(
        &self,
        user: &StatsigUser,
        experiment_name: &str,
        result: &mut EvaluatorResult,
        opt_spec: Option<&Spec>,
    ) -> bool;

    fn get_layer_override(
        &self,
        user: &StatsigUser,
        layer_name: &str,
        result: &mut EvaluatorResult,
    ) -> bool;

    fn get_parameter_store_override(
        &self,
        user: &StatsigUser,
        parameter_store_name: &str,
        result: &mut EvaluatorResult,
    ) -> bool;

    fn override_gate(&self, key: &str, value: bool, id: Option<&str>);
    fn override_dynamic_config(&self, key: &str, value: HashMap<String, Value>, id: Option<&str>);
    fn override_experiment(&self, key: &str, value: HashMap<String, Value>, id: Option<&str>);
    fn override_experiment_by_group_name(&self, key: &str, group_name: &str, id: Option<&str>);
    fn override_layer(&self, key: &str, value: HashMap<String, Value>, id: Option<&str>);
    fn override_parameter_store(&self, key: &str, value: HashMap<String, Value>, id: Option<&str>);

    fn remove_gate_override(&self, key: &str, id: Option<&str>);
    fn remove_dynamic_config_override(&self, key: &str, id: Option<&str>);
    fn remove_experiment_override(&self, key: &str, id: Option<&str>);
    fn remove_layer_override(&self, key: &str, id: Option<&str>);
    fn remove_parameter_store_override(&self, key: &str, id: Option<&str>);
    fn remove_all_overrides(&self);
}
