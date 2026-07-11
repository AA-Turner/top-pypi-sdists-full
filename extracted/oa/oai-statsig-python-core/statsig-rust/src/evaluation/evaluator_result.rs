use std::collections::HashMap;

use ahash::AHashMap;

use super::dynamic_returnable::DynamicReturnable;
use super::evaluation_types::ExtraExposureInfo;
use super::evaluation_types_v2::{
    BaseEvaluationV2, DynamicConfigEvaluationV2, ExperimentEvaluationV2, GateEvaluationV2,
    LayerEvaluationV2,
};
use crate::evaluation::evaluation_types::{
    BaseEvaluation, DynamicConfigEvaluation, ExperimentEvaluation, GateEvaluation, LayerEvaluation,
    SecondaryExposure,
};
use crate::evaluation::evaluation_types_initialize_v2::{
    BaseEvaluationInitV2, DynamicConfigEvaluationInitV2, ExperimentEvaluationInitV2,
    GateEvaluationInitV2, LayerEvaluationInitV2,
};
use crate::evaluation::secondary_exposure_key::SecondaryExposureKey;
use crate::hashing::{HashAlgorithm, HashUtil};
use crate::interned_string::InternedString;
use crate::specs_response::explicit_params::ExplicitParameters;
use crate::specs_response::spec_types::Rule;
use crate::specs_response::specs_hash_map::SpecPointer;
use crate::statsig_types_raw::{
    DynamicConfigRaw, ExperimentRaw, FeatureGateRaw, LayerRaw, SuffixedRuleId,
};
use crate::user::StatsigUserInternal;
use crate::{EvaluationDetails, LayerEvaluationOptions};

const LAUNCHED_GROUP_RULE_ID: &str = "launchedGroup";

#[derive(Default, Debug)]
pub struct EvaluatorResult {
    pub name: Option<InternedString>,
    pub bool_value: bool,
    pub unsupported: bool,
    pub is_experiment_group: bool,
    pub is_experiment_active: bool,
    pub is_in_layer: bool,
    pub id_type: Option<InternedString>,
    pub json_value: Option<DynamicReturnable>,
    pub rule_id: Option<InternedString>,
    pub rule_id_suffix: Option<&'static str>,
    pub group_name: Option<InternedString>,
    pub explicit_parameters: Option<ExplicitParameters>,
    pub config_delegate: Option<InternedString>,
    pub secondary_exposures: Vec<SecondaryExposure>,
    pub undelegated_secondary_exposures: Option<Vec<SecondaryExposure>>,
    pub override_reason: Option<&'static str>,
    pub version: Option<u32>,
    pub sampling_rate: Option<u64>,
    pub forward_all_exposures: Option<bool>,
    pub override_config_name: Option<InternedString>,
    pub has_seen_analytical_gates: Option<bool>,
    pub parameter_rule_ids: Option<HashMap<InternedString, InternedString>>,
}

impl EvaluatorResult {
    pub fn clear_for_reuse(&mut self) {
        self.name = None;
        self.bool_value = false;
        self.unsupported = false;
        self.is_experiment_group = false;
        self.is_experiment_active = false;
        self.is_in_layer = false;
        self.id_type = None;
        self.json_value = None;
        self.rule_id = None;
        self.rule_id_suffix = None;
        self.group_name = None;
        self.explicit_parameters = None;
        self.config_delegate = None;
        self.secondary_exposures.clear();
        self.undelegated_secondary_exposures = None;
        self.override_reason = None;
        self.version = None;
        self.sampling_rate = None;
        self.forward_all_exposures = None;
        self.override_config_name = None;
        self.has_seen_analytical_gates = None;
        self.parameter_rule_ids = None;
    }
}

fn get_is_user_in_experiment(result: &EvaluatorResult) -> bool {
    result.is_experiment_group
        && result
            .rule_id
            .as_ref()
            .is_none_or(|rule_id| rule_id.as_str() != LAUNCHED_GROUP_RULE_ID)
}

pub fn result_to_gate_raw<'a>(
    gate_name: &'a str,
    eval_details: &'a EvaluationDetails,
    result: Option<&'a EvaluatorResult>,
) -> FeatureGateRaw<'a> {
    match result {
        Some(result) => FeatureGateRaw {
            name: gate_name,
            details: eval_details,
            rule_id: create_raw_suffixed_rule_id(result),
            id_type: result.id_type.as_ref(),
            value: result.bool_value,
        },
        None => FeatureGateRaw::empty(gate_name, eval_details),
    }
}

pub fn result_to_gate_eval(gate_name: &str, result: &mut EvaluatorResult) -> GateEvaluation {
    let name = get_exposure_name_if_not_hashed(gate_name, &result.name);
    result_to_gate_eval_with_name(name, result)
}

pub fn result_to_gate_eval_with_name(
    gate_name: InternedString,
    result: &mut EvaluatorResult,
) -> GateEvaluation {
    GateEvaluation {
        base: result_to_base_eval_with_name(gate_name, result),
        id_type: result.id_type.take(),
        value: result.bool_value,
    }
}

pub fn result_to_gate_eval_v2(
    gate_name: &str,
    result: &mut EvaluatorResult,
    hashing: &HashUtil,
) -> GateEvaluationV2 {
    GateEvaluationV2 {
        base: result_to_base_eval_v2(gate_name, result, hashing),
        id_type: result.id_type.take(),
        value: result.bool_value,
    }
}

pub fn result_to_gate_eval_init_v2(
    result: &mut EvaluatorResult,
    expo_id_to_exposure_map: &mut HashMap<InternedString, SecondaryExposure>,
    expo_key_to_expo_id_map: &mut AHashMap<SecondaryExposureKey, InternedString>,
) -> GateEvaluationInitV2 {
    let value: Option<bool> = match result.bool_value {
        true => Some(true),
        _ => None,
    };
    GateEvaluationInitV2 {
        base: result_to_base_eval_init_v2(result, expo_id_to_exposure_map, expo_key_to_expo_id_map),
        id_type: result.id_type.take(),
        value,
    }
}

pub fn rule_to_experiment_raw<'a>(
    experiment_name: &'a str,
    spec_pointer: Option<&'a SpecPointer>,
    rule: Option<&'a Rule>,
    eval_details: &'a EvaluationDetails,
) -> ExperimentRaw<'a> {
    match (spec_pointer, rule) {
        (Some(spec_pointer), Some(rule)) => ExperimentRaw {
            name: experiment_name,
            value: Some(&rule.return_value),
            details: eval_details,
            rule_id: SuffixedRuleId {
                rule_id: &rule.id,
                rule_id_suffix: None,
            },
            id_type: Some(&rule.id_type.value),
            group_name: rule.group_name.as_ref(),
            is_experiment_active: Some(spec_pointer.as_spec_ref().is_active.unwrap_or(false)),
            secondary_exposures: None,
        },
        _ => ExperimentRaw::empty(experiment_name, eval_details),
    }
}

pub fn result_to_experiment_raw<'a>(
    experiment_name: &'a str,
    eval_details: &'a EvaluationDetails,
    result: Option<&'a EvaluatorResult>,
) -> ExperimentRaw<'a> {
    match result {
        Some(result) => ExperimentRaw {
            name: experiment_name,
            value: result.json_value.as_ref(),
            details: eval_details,
            rule_id: create_raw_suffixed_rule_id(result),
            id_type: result.id_type.as_ref(),
            group_name: result.group_name.as_ref(),
            is_experiment_active: Some(result.is_experiment_active),
            secondary_exposures: Some(&result.secondary_exposures),
        },
        None => ExperimentRaw::empty(experiment_name, eval_details),
    }
}

pub fn result_to_experiment_eval(
    experiment_name: &str,
    spec_entity: Option<&str>,
    result: &mut EvaluatorResult,
) -> ExperimentEvaluation {
    let name = get_exposure_name_if_not_hashed(experiment_name, &result.name);
    result_to_experiment_eval_with_name(name, spec_entity, result)
}

pub fn result_to_experiment_eval_with_name(
    experiment_name: InternedString,
    spec_entity: Option<&str>,
    result: &mut EvaluatorResult,
) -> ExperimentEvaluation {
    let (id_type, is_device_based) = get_id_type_info(result.id_type.as_ref());

    let mut is_experiment_active = None;
    let mut is_user_in_experiment = None;

    if spec_entity.is_none_or(|s| s == "experiment") {
        is_experiment_active = Some(result.is_experiment_active);
        is_user_in_experiment = Some(get_is_user_in_experiment(result));
    }

    ExperimentEvaluation {
        base: result_to_base_eval_with_name(experiment_name, result),
        id_type: Some(id_type),
        is_device_based,
        value: get_json_value(result),
        is_in_layer: result.is_in_layer,
        group_name: result.group_name.take(),
        explicit_parameters: result.explicit_parameters.clone(),
        is_experiment_active,
        is_user_in_experiment,
        undelegated_secondary_exposures: std::mem::take(
            &mut result.undelegated_secondary_exposures,
        ),
    }
}

pub fn result_to_experiment_eval_v2(
    experiment_name: &str,
    spec_entity: Option<&str>,
    result: &mut EvaluatorResult,
    hashing: &HashUtil,
) -> ExperimentEvaluationV2 {
    let (id_type, is_device_based) = get_id_type_info(result.id_type.as_ref());

    let mut is_experiment_active = None;
    let mut is_user_in_experiment = None;

    if let Some(spec_entity) = spec_entity {
        if spec_entity == "experiment" {
            is_experiment_active = Some(result.is_experiment_active);
            is_user_in_experiment = Some(get_is_user_in_experiment(result));
        }
    }

    ExperimentEvaluationV2 {
        base: result_to_base_eval_v2(experiment_name, result, hashing),
        id_type: Some(id_type),
        is_device_based,
        value: get_json_value(result),
        is_in_layer: result.is_in_layer,
        group_name: result.group_name.take(),
        explicit_parameters: result.explicit_parameters.clone(),
        is_experiment_active,
        is_user_in_experiment,
        undelegated_secondary_exposures: result.undelegated_secondary_exposures.clone(),
    }
}

pub fn result_to_experiment_eval_init_v2(
    spec_entity: Option<&str>,
    result: &mut EvaluatorResult,
    expo_id_to_exposure_map: &mut HashMap<InternedString, SecondaryExposure>,
    expo_key_to_expo_id_map: &mut AHashMap<SecondaryExposureKey, InternedString>,
    value_id_to_value_map: &mut HashMap<InternedString, DynamicReturnable>,
    value_key_to_value_id: &mut AHashMap<u64, InternedString>,
) -> ExperimentEvaluationInitV2 {
    let value: Option<DynamicReturnable> = result.json_value.take();

    let id_type = result.id_type.take();

    let mut is_experiment_active = None;
    let mut is_user_in_experiment = None;

    if let Some(spec_entity) = spec_entity {
        if spec_entity == "experiment" {
            is_experiment_active = Some(result.is_experiment_active);
            is_user_in_experiment = Some(get_is_user_in_experiment(result));
        }
    }

    let mapped_value = self::get_mapped_value(value, value_id_to_value_map, value_key_to_value_id);

    ExperimentEvaluationInitV2 {
        base: result_to_base_eval_init_v2(result, expo_id_to_exposure_map, expo_key_to_expo_id_map),
        id_type,
        value: mapped_value,
        group_name: result.group_name.take(),
        is_experiment_active,
        is_user_in_experiment,
    }
}

pub fn eval_result_to_experiment_eval(
    experiment_name: &str,
    result: &mut EvaluatorResult,
) -> ExperimentEvaluation {
    let (id_type, is_device_based) = get_id_type_info(result.id_type.as_ref());

    ExperimentEvaluation {
        base: result_to_base_eval(experiment_name, result),
        id_type: Some(id_type),
        is_device_based,
        value: get_json_value(result),
        is_in_layer: result.is_in_layer,
        group_name: result.group_name.take(),
        explicit_parameters: result.explicit_parameters.clone(),
        is_experiment_active: Some(result.is_experiment_active),
        is_user_in_experiment: Some(result.is_experiment_group),
        undelegated_secondary_exposures: std::mem::take(
            &mut result.undelegated_secondary_exposures,
        ),
    }
}

pub fn result_to_layer_raw<'a>(
    user: &'a StatsigUserInternal,
    layer_name: &'a str,
    options: LayerEvaluationOptions,
    eval_details: &'a EvaluationDetails,
    result: Option<&'a EvaluatorResult>,
) -> LayerRaw<'a> {
    match result {
        Some(result) => LayerRaw {
            name: layer_name,
            details: eval_details,
            rule_id: create_raw_suffixed_rule_id(result),
            id_type: result.id_type.as_ref(),
            group_name: result.group_name.as_ref(),
            is_experiment_active: Some(result.is_experiment_active),
            value: result.json_value.as_ref(),
            allocated_experiment_name: result.config_delegate.as_ref(),
            disable_exposure: options.disable_exposure_logging,
            user: user.to_loggable(),
            secondary_exposures: Some(&result.secondary_exposures),
            undelegated_secondary_exposures: result.undelegated_secondary_exposures.as_ref(),
            explicit_parameters: result.explicit_parameters.clone(),
            parameter_rule_ids: result.parameter_rule_ids.as_ref(),
            exposure_info: Some(result_to_extra_exposure_info(result)),
        },
        None => LayerRaw::empty(layer_name, eval_details),
    }
}

pub fn result_to_layer_eval(layer_name: &str, result: &mut EvaluatorResult) -> LayerEvaluation {
    let name = get_exposure_name_if_not_hashed(layer_name, &result.name);
    result_to_layer_eval_with_name(name, result)
}

pub fn result_to_layer_eval_with_name(
    layer_name: InternedString,
    result: &mut EvaluatorResult,
) -> LayerEvaluation {
    let mut allocated_experiment_name = None;
    let mut is_experiment_active = None;
    let mut is_user_in_experiment = None;

    if let Some(config_delegate) = result.config_delegate.take() {
        if !config_delegate.is_empty() {
            allocated_experiment_name = Some(config_delegate.clone());
            is_experiment_active = Some(result.is_experiment_active);
            is_user_in_experiment = Some(get_is_user_in_experiment(result));
        }
    }

    let (id_type, is_device_based) = get_id_type_info(result.id_type.as_ref());
    let undelegated_sec_expos = std::mem::take(&mut result.undelegated_secondary_exposures);

    LayerEvaluation {
        base: result_to_base_eval_with_name(layer_name, result),
        value: get_json_value(result),
        is_device_based,
        group_name: result.group_name.take(),
        is_experiment_active,
        is_user_in_experiment,
        allocated_experiment_name,
        explicit_parameters: result.explicit_parameters.clone().unwrap_or_default(),
        undelegated_secondary_exposures: Some(undelegated_sec_expos.unwrap_or_default()),
        id_type: Some(id_type),
        parameter_rule_ids: result.parameter_rule_ids.clone(),
    }
}

pub fn result_to_layer_eval_v2(
    layer_name: &str,
    result: &mut EvaluatorResult,
    hashing: &HashUtil,
) -> LayerEvaluationV2 {
    let mut undelegated_secondary_exposures = Vec::new();

    if let Some(u) = &result.undelegated_secondary_exposures {
        for exposure in u {
            let key = format!(
                "{}:{}:{}",
                exposure.gate,
                exposure.gate_value,
                exposure.rule_id.as_str()
            );
            let hash = hashing.hash(&key, &HashAlgorithm::Djb2);
            undelegated_secondary_exposures.push(InternedString::from_string(hash));
        }
    }

    let mut allocated_experiment_name = None;
    let mut is_experiment_active = None;
    let mut is_user_in_experiment = None;

    if let Some(config_delegate) = result.config_delegate.take() {
        if !config_delegate.is_empty() {
            allocated_experiment_name = Some(config_delegate.clone());
            is_experiment_active = Some(result.is_experiment_active);
            is_user_in_experiment = Some(get_is_user_in_experiment(result));
        }
    }

    let (id_type, is_device_based) = get_id_type_info(result.id_type.as_ref());

    LayerEvaluationV2 {
        base: result_to_base_eval_v2(layer_name, result, hashing),
        value: get_json_value(result),
        is_device_based,
        group_name: result.group_name.take(),
        is_experiment_active,
        is_user_in_experiment,
        allocated_experiment_name,
        explicit_parameters: result.explicit_parameters.clone().unwrap_or_default(),
        undelegated_secondary_exposures: Some(undelegated_secondary_exposures),
        id_type: Some(id_type),
    }
}

pub fn result_to_layer_eval_init_v2(
    result: &mut EvaluatorResult,
    expo_id_to_exposure_map: &mut HashMap<InternedString, SecondaryExposure>,
    expo_key_to_expo_id_map: &mut AHashMap<SecondaryExposureKey, InternedString>,
    value_id_to_value_map: &mut HashMap<InternedString, DynamicReturnable>,
    value_key_to_value_id: &mut AHashMap<u64, InternedString>,
) -> LayerEvaluationInitV2 {
    let value: Option<DynamicReturnable> = result.json_value.take();

    let mut allocated_experiment_name = None;
    let mut is_experiment_active = None;
    let mut is_user_in_experiment = None;

    if let Some(config_delegate) = result.config_delegate.take() {
        if !config_delegate.is_empty() {
            allocated_experiment_name = Some(config_delegate.clone());
            is_experiment_active = Some(result.is_experiment_active);
            is_user_in_experiment = Some(get_is_user_in_experiment(result));
        }
    }

    let id_type = result.id_type.take();

    let mapped_exposures: Option<Vec<InternedString>> = match result
        .undelegated_secondary_exposures
        .as_mut()
    {
        Some(undelegated_secondary_exposures) if !&undelegated_secondary_exposures.is_empty() => {
            Some(self::map_exposures(
                undelegated_secondary_exposures,
                expo_id_to_exposure_map,
                expo_key_to_expo_id_map,
            ))
        }
        _ => None,
    };

    let mapped_value = self::get_mapped_value(value, value_id_to_value_map, value_key_to_value_id);

    LayerEvaluationInitV2 {
        base: result_to_base_eval_init_v2(result, expo_id_to_exposure_map, expo_key_to_expo_id_map),
        id_type,
        value: mapped_value,
        group_name: result.group_name.take(),
        is_experiment_active,
        is_user_in_experiment,
        allocated_experiment_name,
        explicit_parameters: result.explicit_parameters.clone(),
        undelegated_secondary_exposures: mapped_exposures,
    }
}

pub fn result_to_dynamic_config_raw<'a>(
    dynamic_config_name: &'a str,
    eval_details: &'a EvaluationDetails,
    result: Option<&'a EvaluatorResult>,
) -> DynamicConfigRaw<'a> {
    match result {
        Some(result) => DynamicConfigRaw {
            name: dynamic_config_name,
            value: result.json_value.as_ref(),
            details: eval_details,
            rule_id: create_raw_suffixed_rule_id(result),
            id_type: result.id_type.as_ref(),
        },
        None => DynamicConfigRaw::empty(dynamic_config_name, eval_details),
    }
}

pub fn result_to_dynamic_config_eval(
    dynamic_config_name: &str,
    result: &mut EvaluatorResult,
) -> DynamicConfigEvaluation {
    let name = get_exposure_name_if_not_hashed(dynamic_config_name, &result.name);
    result_to_dynamic_config_eval_with_name(name, result)
}

pub fn result_to_dynamic_config_eval_with_name(
    dynamic_config_name: InternedString,
    result: &mut EvaluatorResult,
) -> DynamicConfigEvaluation {
    let (id_type, is_device_based) = get_id_type_info(result.id_type.as_ref());

    DynamicConfigEvaluation {
        base: result_to_base_eval_with_name(dynamic_config_name, result),
        id_type: Some(id_type),
        is_device_based,
        value: get_json_value(result),
        passed: result.bool_value,
    }
}

pub fn result_to_dynamic_config_eval_v2(
    dynamic_config_name: &str,
    result: &mut EvaluatorResult,
    hashing: &HashUtil,
) -> DynamicConfigEvaluationV2 {
    let (id_type, is_device_based) = get_id_type_info(result.id_type.as_ref());

    DynamicConfigEvaluationV2 {
        base: result_to_base_eval_v2(dynamic_config_name, result, hashing),
        id_type: Some(id_type),
        is_device_based,
        value: get_json_value(result),
        passed: result.bool_value,
    }
}

pub fn result_to_dynamic_config_eval_init_v2(
    result: &mut EvaluatorResult,
    expo_id_to_exposure_map: &mut HashMap<InternedString, SecondaryExposure>,
    expo_key_to_expo_id_map: &mut AHashMap<SecondaryExposureKey, InternedString>,
    value_id_to_value_map: &mut HashMap<InternedString, DynamicReturnable>,
    value_key_to_value_id: &mut AHashMap<u64, InternedString>,
) -> DynamicConfigEvaluationInitV2 {
    let value: Option<DynamicReturnable> = result.json_value.take();

    let id_type = result.id_type.take();

    let mapped_value = self::get_mapped_value(value, value_id_to_value_map, value_key_to_value_id);

    DynamicConfigEvaluationInitV2 {
        base: result_to_base_eval_init_v2(result, expo_id_to_exposure_map, expo_key_to_expo_id_map),
        id_type,
        value: mapped_value,
        passed: result.bool_value,
    }
}

fn get_mapped_value(
    value: Option<DynamicReturnable>,
    value_id_to_value_map: &mut HashMap<InternedString, DynamicReturnable>,
    value_key_to_value_id: &mut AHashMap<u64, InternedString>,
) -> InternedString {
    let val = match &value {
        Some(v) => v,
        None => &DynamicReturnable::empty(),
    };
    let hash = val.get_hash();
    match value_key_to_value_id.get(&hash) {
        Some(mapped_key) => mapped_key.clone(),
        None => {
            let value_id = InternedString::from_string(value_id_to_value_map.len().to_string());
            value_id_to_value_map.insert(value_id.clone(), val.clone());
            value_key_to_value_id.insert(hash, value_id.clone());
            value_id
        }
    }
}

fn get_id_type_info(id_type: Option<&InternedString>) -> (InternedString, bool) {
    let id_type = id_type.cloned().unwrap_or_default();
    let is_device_based = id_type == "stableID" || id_type == "stableid";
    (id_type, is_device_based)
}

fn get_json_value(result: &mut EvaluatorResult) -> DynamicReturnable {
    result
        .json_value
        .take()
        .unwrap_or_else(DynamicReturnable::empty)
}

// todo: remove when 'QueuedExposure' does not use `BaseEvaluation`
fn get_exposure_name_if_not_hashed(
    possibly_hashed_name: &str,
    exposure_name: &Option<InternedString>,
) -> InternedString {
    let exposure_name = exposure_name
        .as_ref()
        .unwrap_or(InternedString::empty_ref());

    if possibly_hashed_name == exposure_name.as_str() {
        exposure_name.clone()
    } else {
        InternedString::from_str_ref(possibly_hashed_name)
    }
}

fn result_to_base_eval(spec_name: &str, result: &mut EvaluatorResult) -> BaseEvaluation {
    let name = get_exposure_name_if_not_hashed(spec_name, &result.name);
    result_to_base_eval_with_name(name, result)
}

fn result_to_base_eval_with_name(
    name: InternedString,
    result: &mut EvaluatorResult,
) -> BaseEvaluation {
    let rule_id = create_suffixed_rule_id(result.rule_id.as_ref(), result.rule_id_suffix);

    let exposure_info = result_to_extra_exposure_info(result);

    BaseEvaluation {
        name,
        rule_id,
        secondary_exposures: std::mem::take(&mut result.secondary_exposures),
        version: result.version,
        exposure_info: Some(exposure_info),
    }
}

pub fn result_to_extra_exposure_info(result: &EvaluatorResult) -> ExtraExposureInfo {
    ExtraExposureInfo {
        sampling_rate: result.sampling_rate,
        forward_all_exposures: result.forward_all_exposures,
        has_seen_analytical_gates: result.has_seen_analytical_gates,
        override_config_name: result.override_config_name.clone(),
        version: result.version,
    }
}

fn result_to_base_eval_v2(
    spec_name: &str,
    result: &mut EvaluatorResult,
    hashing: &HashUtil,
) -> BaseEvaluationV2 {
    let mut exposures = Vec::new();

    for exposure in &result.secondary_exposures {
        let key = format!(
            "{}:{}:{}",
            exposure.gate,
            exposure.gate_value,
            exposure.rule_id.as_str()
        );
        let hash = hashing.hash(&key, &HashAlgorithm::Djb2);
        exposures.push(hash.clone());
    }

    let rule_id = create_suffixed_rule_id(result.rule_id.as_ref(), result.rule_id_suffix);

    BaseEvaluationV2 {
        name: spec_name.to_string(),
        rule_id,
        secondary_exposures: exposures,
        version: result.version,
    }
}

fn result_to_base_eval_init_v2(
    result: &mut EvaluatorResult,
    expo_id_to_exposure_map: &mut HashMap<InternedString, SecondaryExposure>,
    expo_key_to_expo_id_map: &mut AHashMap<SecondaryExposureKey, InternedString>,
) -> BaseEvaluationInitV2 {
    let rule_id = create_suffixed_rule_id(result.rule_id.as_ref(), result.rule_id_suffix);
    let opt_rule_id = match rule_id.as_str() {
        "default" => None,
        _ => Some(rule_id),
    };

    if result.secondary_exposures.is_empty() {
        return BaseEvaluationInitV2 {
            rule_id: opt_rule_id,
            secondary_exposures: None,
        };
    }

    BaseEvaluationInitV2 {
        rule_id: opt_rule_id,
        secondary_exposures: Some(self::map_exposures(
            &mut result.secondary_exposures,
            expo_id_to_exposure_map,
            expo_key_to_expo_id_map,
        )),
    }
}

fn map_exposures(
    input_exposures: &mut Vec<SecondaryExposure>,
    expo_id_to_exposure_map: &mut HashMap<InternedString, SecondaryExposure>,
    expo_key_to_expo_id_map: &mut AHashMap<SecondaryExposureKey, InternedString>,
) -> Vec<InternedString> {
    let my_exposures = std::mem::take(input_exposures);
    my_exposures
        .into_iter()
        .map(|exposure| {
            let expo_key = SecondaryExposureKey::from(&exposure);

            match expo_key_to_expo_id_map.get(&expo_key) {
                Some(expo_id) => expo_id.clone(),
                None => {
                    let expo_id =
                        InternedString::from_string(expo_id_to_exposure_map.len().to_string());

                    expo_id_to_exposure_map.insert(expo_id.clone(), exposure);
                    expo_key_to_expo_id_map.insert(expo_key, expo_id.clone());

                    expo_id
                }
            }
        })
        .collect()
}

fn create_raw_suffixed_rule_id<'a>(result: &'a EvaluatorResult) -> SuffixedRuleId<'a> {
    SuffixedRuleId {
        rule_id: result
            .rule_id
            .as_ref()
            .unwrap_or(InternedString::empty_ref()),
        rule_id_suffix: result.rule_id_suffix,
    }
}

fn create_suffixed_rule_id(
    rule_id: Option<&InternedString>,
    suffix: Option<&str>,
) -> InternedString {
    let rule_id_str = match rule_id {
        Some(rule_id) => rule_id.as_str(),
        None => "",
    };

    match &suffix {
        Some(suffix) => InternedString::from_str_parts(&[rule_id_str, ":", suffix]),
        None => rule_id.cloned().unwrap_or_default(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn clear_for_reuse_resets_fields_and_keeps_secondary_exposure_capacity() {
        let mut result = EvaluatorResult {
            name: Some(InternedString::from_str_ref("a_gate")),
            bool_value: true,
            unsupported: true,
            is_experiment_group: true,
            is_experiment_active: true,
            is_in_layer: true,
            id_type: Some(InternedString::from_str_ref("stableID")),
            json_value: Some(DynamicReturnable::from_bool(true)),
            rule_id: Some(InternedString::from_str_ref("rule")),
            rule_id_suffix: Some("suffix"),
            group_name: Some(InternedString::from_str_ref("group")),
            explicit_parameters: Some(ExplicitParameters::from_vec(vec!["param".to_string()])),
            config_delegate: Some(InternedString::from_str_ref("delegate")),
            secondary_exposures: Vec::with_capacity(8),
            undelegated_secondary_exposures: Some(vec![SecondaryExposure {
                gate: InternedString::from_str_ref("undelegated_gate"),
                gate_value: InternedString::from_bool(true),
                rule_id: InternedString::from_str_ref("undelegated_rule"),
            }]),
            override_reason: Some("override"),
            version: Some(1),
            sampling_rate: Some(10),
            forward_all_exposures: Some(true),
            override_config_name: Some(InternedString::from_str_ref("override_config")),
            has_seen_analytical_gates: Some(true),
            parameter_rule_ids: Some(HashMap::from([(
                InternedString::from_str_ref("param"),
                InternedString::from_str_ref("rule"),
            )])),
        };

        result.secondary_exposures.push(SecondaryExposure {
            gate: InternedString::from_str_ref("gate"),
            gate_value: InternedString::from_bool(false),
            rule_id: InternedString::from_str_ref("rule"),
        });
        let secondary_exposure_capacity = result.secondary_exposures.capacity();

        result.clear_for_reuse();

        assert!(result.name.is_none());
        assert!(!result.bool_value);
        assert!(!result.unsupported);
        assert!(!result.is_experiment_group);
        assert!(!result.is_experiment_active);
        assert!(!result.is_in_layer);
        assert!(result.id_type.is_none());
        assert!(result.json_value.is_none());
        assert!(result.rule_id.is_none());
        assert!(result.rule_id_suffix.is_none());
        assert!(result.group_name.is_none());
        assert!(result.explicit_parameters.is_none());
        assert!(result.config_delegate.is_none());
        assert!(result.secondary_exposures.is_empty());
        assert_eq!(
            result.secondary_exposures.capacity(),
            secondary_exposure_capacity
        );
        assert!(result.undelegated_secondary_exposures.is_none());
        assert!(result.override_reason.is_none());
        assert!(result.version.is_none());
        assert!(result.sampling_rate.is_none());
        assert!(result.forward_all_exposures.is_none());
        assert!(result.override_config_name.is_none());
        assert!(result.has_seen_analytical_gates.is_none());
        assert!(result.parameter_rule_ids.is_none());
    }
}
