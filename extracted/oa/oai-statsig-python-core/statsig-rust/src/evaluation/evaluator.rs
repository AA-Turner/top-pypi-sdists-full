use std::collections::HashMap;

use chrono::Utc;
use lazy_static::lazy_static;
use serde_json::Value;

use crate::evaluation::cmab_evaluator::evaluate_cmab;
use crate::evaluation::comparisons::{
    compare_arrays, compare_numbers, compare_str_with_regex, compare_strings_in_array,
    compare_time, compare_versions,
};
use crate::evaluation::dynamic_returnable::DynamicReturnable;
use crate::evaluation::dynamic_string::DynamicString;
use crate::evaluation::dynamic_value::DynamicValue;
use crate::evaluation::evaluation_data::{InternedStrRef, RuleRef, SpecAccess, SpecView};
use crate::evaluation::evaluation_types::SecondaryExposure;
use crate::evaluation::evaluator_context::{EvaluatorContext, IdListResolution};
use crate::evaluation::evaluator_value::{EvaluatorValue, EvaluatorValueRef};
use crate::evaluation::get_unit_id::get_unit_id;
use crate::evaluation::user_agent_parsing::UserAgentParser;
use crate::interned_string::InternedString;
use crate::specs_response::explicit_params::ExplicitParameters;
use crate::specs_response::spec_types::{Condition, ConditionOperator, ConditionType};
use crate::user::user_value::UserValueRef;
use crate::{dyn_value, log_w, unwrap_or_return, ExperimentEvaluationOptions, StatsigErr};

use super::country_lookup::CountryLookup;

const TAG: &str = "Evaluator";

pub struct Evaluator;

lazy_static! {
    static ref EMPTY_STR: String = String::new();
    static ref EMPTY_DYNAMIC_VALUE: DynamicValue = DynamicValue::new();
    static ref DISABLED_RULE: InternedString = InternedString::from_str_ref("disabled");
    static ref SALT: InternedString = InternedString::from_str_ref("salt");
}

#[derive(Clone, Debug)]
pub enum SpecType {
    Gate,
    DynamicConfig,
    Experiment,
    Layer,
    ParameterStore,
}

#[derive(PartialEq, Eq, Debug)]
pub enum Recognition {
    Unrecognized,
    Recognized,
}

impl Evaluator {
    pub fn evaluate(
        ctx: &mut EvaluatorContext,
        spec_name: &str,
        spec_type: &SpecType,
    ) -> Result<Recognition, StatsigErr> {
        let spec_name_intern = InternedString::from_str_ref(spec_name);
        Self::evaluate_with_name(ctx, &spec_name_intern, spec_type)
    }

    pub(crate) fn evaluate_with_name(
        ctx: &mut EvaluatorContext,
        spec_name_intern: &InternedString,
        spec_type: &SpecType,
    ) -> Result<Recognition, StatsigErr> {
        let spec_name = spec_name_intern.as_str();

        let opt_spec = match spec_type {
            SpecType::Gate => ctx.specs_data.feature_gates.get(spec_name_intern),
            SpecType::DynamicConfig => ctx.specs_data.dynamic_configs.get(spec_name_intern),
            SpecType::Experiment => ctx.specs_data.dynamic_configs.get(spec_name_intern),
            SpecType::Layer => ctx.specs_data.layer_configs.get(spec_name_intern),
            SpecType::ParameterStore => {
                return evaluate_param_store_reason(ctx, spec_name.to_string());
            }
        }
        .map(|spec| spec.view());

        if try_apply_override(ctx, spec_name, spec_type, opt_spec) {
            return Ok(Recognition::Recognized);
        }

        if try_apply_config_mapping(ctx, spec_name, spec_type, opt_spec) {
            return Ok(Recognition::Recognized);
        }

        if evaluate_cmab(ctx, spec_name, spec_type) {
            return Ok(Recognition::Recognized);
        }

        let spec = unwrap_or_return!(opt_spec, Ok(Recognition::Unrecognized));

        if ctx.result.name.is_none() {
            ctx.result.name = Some(spec_name_intern.clone());
        }

        if ctx.result.id_type.is_none() {
            ctx.result.id_type = Some(spec.id_type().to_interned());
        }

        if ctx.result.version.is_none() {
            if let Some(version) = spec.version() {
                ctx.result.version = Some(version);
            }
        }

        if let Some(is_active) = spec.is_active() {
            ctx.result.is_experiment_active = is_active;
        }

        if let Some(has_shared_params) = spec.has_shared_params() {
            ctx.result.is_in_layer = has_shared_params;
        }

        if let Some(explicit_params) = spec.explicit_parameters() {
            ctx.result.explicit_parameters = Some(explicit_params);
        }

        if spec.uses_new_layer_eval() && matches!(spec_type, SpecType::Layer) {
            return new_layer_eval(ctx, spec);
        }

        for index in 0..spec.rules_len() {
            let rule = spec.rule(index);
            evaluate_rule(ctx, rule)?;

            if ctx.result.unsupported {
                return Ok(Recognition::Recognized);
            }

            if !ctx.result.bool_value {
                continue;
            }

            if evaluate_config_delegate(ctx, rule)? {
                ctx.finalize_evaluation_values(rule.sampling_rate(), spec.forward_all_exposures());
                return Ok(Recognition::Recognized);
            }

            let did_pass = evaluate_pass_percentage(ctx, rule, spec.salt());

            let return_value = if did_pass {
                rule.return_value()
            } else {
                spec.default_value()
            };
            ctx.result.bool_value = if did_pass {
                return_value.bool_value() != Some(false)
            } else {
                return_value.bool_value() == Some(true)
            };
            ctx.result.json_value = Some(return_value.to_owned());

            ctx.result.rule_id = Some(rule.id().to_interned());
            ctx.result.group_name = rule.group_name().map(InternedStrRef::to_interned);
            ctx.result.is_experiment_group = rule.is_experiment_group();
            ctx.result.is_experiment_active = spec.is_active().unwrap_or(false);
            ctx.finalize_evaluation_values(rule.sampling_rate(), spec.forward_all_exposures());
            return Ok(Recognition::Recognized);
        }

        let default_value = spec.default_value();
        ctx.result.bool_value = default_value.bool_value() == Some(true);
        ctx.result.json_value = Some(default_value.to_owned());
        ctx.result.rule_id = match spec.enabled() {
            true => Some(InternedString::default_rule_id()),
            false => Some(DISABLED_RULE.clone()),
        };
        ctx.finalize_evaluation_values(None, spec.forward_all_exposures());

        Ok(Recognition::Recognized)
    }
}

fn new_layer_eval<'a>(
    ctx: &mut EvaluatorContext<'a>,
    spec: SpecView<'a>,
) -> Result<Recognition, StatsigErr> {
    let mut has_passed_rule = false;
    let mut passed = false;
    let mut rule_id = Some(InternedString::default_rule_id());
    let mut delegate_name: Option<InternedString> = None;
    let mut rule_ids: HashMap<InternedString, InternedString> = HashMap::new();
    let mut value: HashMap<String, Value> = HashMap::new();
    let mut group_name: Option<InternedString> = None;
    let mut is_experiment_group = false;
    let mut is_experiment_active = false;
    let mut explicit_parameters: Option<ExplicitParameters> = None;
    let mut secondary_exposures: Vec<SecondaryExposure> = Vec::new();
    let mut undelegated_secondary_exposures: Vec<SecondaryExposure> = Vec::new();

    for index in 0..spec.rules_len() {
        let rule = spec.rule(index);
        evaluate_rule(ctx, rule)?;
        let rule_secondary_exposures = std::mem::take(&mut ctx.result.secondary_exposures);
        secondary_exposures.extend(rule_secondary_exposures.iter().cloned());
        undelegated_secondary_exposures.extend(rule_secondary_exposures);

        if ctx.result.unsupported {
            return Ok(Recognition::Recognized);
        }

        if !ctx.result.bool_value {
            continue;
        }

        let did_pass = evaluate_pass_percentage(ctx, rule, spec.salt());
        if !did_pass {
            continue;
        }

        if evaluate_config_delegate(ctx, rule)? {
            if has_passed_rule {
                continue;
            }
            let delegate_value = match &ctx.result.json_value {
                Some(val) => val.get_json(),
                None => continue,
            };
            let mut has_reused_parameter = false;
            if let Some(json_map) = &delegate_value {
                for k in json_map.keys() {
                    if value.contains_key(k) {
                        has_reused_parameter = true;
                        break;
                    }
                }
            }

            if has_reused_parameter {
                continue;
            }

            let delegate_rule_id = ctx
                .result
                .rule_id
                .clone()
                .unwrap_or_else(InternedString::default_rule_id);
            update_parameter_values(
                &mut value,
                &mut rule_ids,
                delegate_value,
                (&delegate_rule_id).into(),
            );

            secondary_exposures.append(&mut ctx.result.secondary_exposures);
            ctx.result.secondary_exposures.clear();
            passed = ctx.result.bool_value;
            delegate_name = ctx.result.config_delegate.clone();
            group_name = ctx.result.group_name.clone();
            rule_id = Some(delegate_rule_id);
            is_experiment_group = ctx.result.is_experiment_group;
            is_experiment_active = ctx.result.is_experiment_active;
            explicit_parameters = ctx.result.explicit_parameters.clone();
        } else {
            passed = ctx.result.bool_value;
            update_parameter_values(
                &mut value,
                &mut rule_ids,
                rule.return_value().json_value(),
                rule.id(),
            );
        }
        has_passed_rule = true;
    }
    update_parameter_values(
        &mut value,
        &mut rule_ids,
        spec.default_value().json_value(),
        InternedString::default_rule_id_ref().into(),
    );
    ctx.result.bool_value = passed;
    ctx.result.config_delegate = delegate_name;
    ctx.result.group_name = group_name;
    ctx.result.rule_id = rule_id;
    ctx.result.json_value = Some(DynamicReturnable::from_map(value));
    ctx.result.is_experiment_group = is_experiment_group;
    ctx.result.is_experiment_active = is_experiment_active;
    ctx.result.explicit_parameters = explicit_parameters;
    ctx.result.secondary_exposures = secondary_exposures;
    ctx.result.undelegated_secondary_exposures = Some(undelegated_secondary_exposures);
    ctx.result.parameter_rule_ids = Some(rule_ids);
    ctx.finalize_evaluation_values(None, spec.forward_all_exposures());
    Ok(Recognition::Recognized)
}

fn update_parameter_values(
    value: &mut HashMap<String, Value>,
    rule_ids: &mut HashMap<InternedString, InternedString>,
    values_to_apply: Option<HashMap<String, Value>>,
    rule_id: InternedStrRef<'_>,
) {
    let json_map = match values_to_apply {
        Some(map) => map,
        None => return,
    };
    for (k, v) in json_map {
        let parameter_name = InternedString::from_string_uninterned(k.clone());
        if let std::collections::hash_map::Entry::Vacant(e) = value.entry(k) {
            e.insert(v);
            rule_ids.insert(parameter_name.clone(), rule_id.to_interned());
        }
    }
}

fn try_apply_config_mapping(
    ctx: &mut EvaluatorContext,
    spec_name: &str,
    spec_type: &SpecType,
    opt_spec: Option<SpecView<'_>>,
) -> bool {
    let overrides = match &ctx.specs_data.overrides {
        Some(overrides) => overrides,
        None => return false,
    };

    let override_rules = match &ctx.specs_data.override_rules {
        Some(override_rules) => override_rules,
        None => return false,
    };

    let mapping_list = match overrides.get(spec_name) {
        Some(mapping_list) => mapping_list,
        None => return false,
    };

    let spec_salt = match opt_spec {
        Some(spec) => spec.salt(),
        None => InternedString::empty_ref().into(),
    };

    for mapping in mapping_list {
        for override_rule in &mapping.rules {
            let start_time = override_rule.start_time.unwrap_or_default();

            if start_time > Utc::now().timestamp_millis() {
                continue;
            }

            let rule = match override_rules.get(&override_rule.rule_name) {
                Some(rule) => rule,
                None => continue,
            };
            let rule = RuleRef::from(rule);
            match evaluate_rule(ctx, rule) {
                Ok(_) => {}
                Err(_) => {
                    ctx.reset_result();
                    continue;
                }
            }

            if !ctx.result.bool_value || ctx.result.unsupported {
                ctx.reset_result();
                continue;
            }
            ctx.reset_result();
            let pass = evaluate_pass_percentage(ctx, rule, spec_salt);
            if pass {
                ctx.result.override_config_name = Some(mapping.new_config_name.clone());
                match Evaluator::evaluate_with_name(ctx, &mapping.new_config_name, spec_type) {
                    Ok(Recognition::Recognized) => {
                        return true;
                    }
                    _ => {
                        ctx.reset_result();
                        break;
                    }
                }
            }
        }
    }

    false
}

fn try_apply_override(
    ctx: &mut EvaluatorContext,
    spec_name: &str,
    spec_type: &SpecType,
    opt_spec: Option<SpecView<'_>>,
) -> bool {
    let adapter = match &ctx.override_adapter {
        Some(adapter) => adapter,
        None => return false,
    };

    let has_any_override_for_spec = match spec_type {
        SpecType::Gate => adapter.has_any_overrides_for_gate(spec_name),
        SpecType::DynamicConfig => adapter.has_any_overrides_for_dynamic_config(spec_name),
        SpecType::Experiment => adapter.has_any_overrides_for_experiment(spec_name),
        SpecType::Layer => adapter.has_any_overrides_for_layer(spec_name),
        SpecType::ParameterStore => adapter.has_any_overrides_for_parameter_store(spec_name),
    };

    if !has_any_override_for_spec {
        return false;
    }

    ctx.user.with_public_user(|user| match spec_type {
        SpecType::Gate => adapter.get_gate_override(user, spec_name, &mut ctx.result),

        SpecType::DynamicConfig => {
            adapter.get_dynamic_config_override(user, spec_name, &mut ctx.result)
        }

        SpecType::Experiment => {
            let override_spec = opt_spec.map(SpecView::materialize);
            adapter.get_experiment_override(
                user,
                spec_name,
                &mut ctx.result,
                override_spec.as_ref().map(SpecAccess::as_ref),
            )
        }

        SpecType::Layer => adapter.get_layer_override(user, spec_name, &mut ctx.result),

        SpecType::ParameterStore => {
            adapter.get_parameter_store_override(user, spec_name, &mut ctx.result)
        }
    })
}

fn evaluate_rule<'a>(ctx: &mut EvaluatorContext<'a>, rule: RuleRef<'a>) -> Result<(), StatsigErr> {
    let mut all_conditions_pass = true;
    // println!("--- Eval Rule {} ---", rule.id);
    for index in 0..rule.conditions_len() {
        let condition_hash = rule.condition_id(index);
        // println!("Condition Hash {}", condition_hash);
        let opt_condition = condition_hash.get_from(&ctx.specs_data.condition_map);
        let condition = if let Some(c) = opt_condition {
            c
        } else {
            log_w!(
                TAG,
                "Unsupported - Condition not found: {}",
                condition_hash.as_str()
            );
            ctx.result.unsupported = true;
            return Ok(());
        };

        evaluate_condition(ctx, condition)?;

        if !ctx.result.bool_value {
            all_conditions_pass = false;
        }
    }

    ctx.result.bool_value = all_conditions_pass;

    Ok(())
}

fn evaluate_condition<'a>(
    ctx: &mut EvaluatorContext<'a>,
    condition: &'a Condition,
) -> Result<(), StatsigErr> {
    let temp_value: Option<DynamicValue>;
    let target_value = condition
        .target_value
        .as_ref()
        .map(EvaluatorValue::as_value_ref)
        .unwrap_or_else(|| EvaluatorValue::empty().as_value_ref());
    let condition_type = condition.condition_type.as_str();

    let value: UserValueRef<'_> = match condition.compiled_condition_type {
        ConditionType::Public => {
            ctx.result.bool_value = true;
            return Ok(());
        }
        ConditionType::FailGate => {
            evaluate_nested_gate(ctx, target_value, true)?;
            return Ok(());
        }
        ConditionType::PassGate => {
            evaluate_nested_gate(ctx, target_value, false)?;
            return Ok(());
        }
        ConditionType::ExperimentGroup => {
            let group_name = evaluate_experiment_group(ctx, &condition.field);
            match group_name {
                Some(name) => {
                    temp_value = Some(DynamicValue::from(name));
                    temp_value.as_ref().map(UserValueRef::Dynamic)
                }
                None => None,
            }
        }
        ConditionType::UaBased => match ctx.user.get_user_value(&condition.field) {
            Some(value) => Some(value),
            None => {
                temp_value = UserAgentParser::get_value_from_user_agent(
                    ctx.user,
                    &condition.field,
                    &mut ctx.result.override_reason,
                    ctx.should_user_third_party_parser,
                );
                temp_value.as_ref().map(UserValueRef::Dynamic)
            }
        },
        ConditionType::IpBased => match ctx.user.get_user_value(&condition.field) {
            Some(value) => Some(value),
            None => {
                temp_value = CountryLookup::get_value_from_ip(ctx.user, &condition.field, ctx);
                temp_value.as_ref().map(UserValueRef::Dynamic)
            }
        },
        ConditionType::UserField => ctx.user.get_user_value(&condition.field),
        ConditionType::EnvironmentField => {
            temp_value = ctx.user.get_value_from_environment(&condition.field);
            temp_value.as_ref().map(UserValueRef::Dynamic)
        }
        ConditionType::CurrentTime => {
            temp_value = Some(DynamicValue::for_timestamp_evaluation(
                Utc::now().timestamp_millis(),
            ));
            temp_value.as_ref().map(UserValueRef::Dynamic)
        }
        ConditionType::UserBucket => {
            temp_value = Some(get_hash_for_user_bucket(ctx, condition));
            temp_value.as_ref().map(UserValueRef::Dynamic)
        }
        ConditionType::TargetApp => ctx.app_id.map(UserValueRef::Dynamic),
        ConditionType::UnitId => ctx.user.get_unit_id(&condition.id_type),
        ConditionType::Unknown => {
            log_w!(
                TAG,
                "Unsupported - Unknown condition type: {}",
                condition_type
            );
            ctx.result.unsupported = true;
            return Ok(());
        }
    }
    .unwrap_or(UserValueRef::Dynamic(&EMPTY_DYNAMIC_VALUE));

    // println!("Eval Condition {}, {:?}", condition_type, value);

    ctx.result.bool_value = match condition.compiled_operator {
        ConditionOperator::Missing => {
            log_w!(TAG, "Unsupported - Operator is None",);
            ctx.result.unsupported = true;
            return Ok(());
        }

        // numerical comparisons
        op @ (ConditionOperator::Gt
        | ConditionOperator::Gte
        | ConditionOperator::Lt
        | ConditionOperator::Lte) => compare_numbers(value, target_value, op),

        // version comparisons
        op @ (ConditionOperator::VersionGt
        | ConditionOperator::VersionGte
        | ConditionOperator::VersionLt
        | ConditionOperator::VersionLte
        | ConditionOperator::VersionEq
        | ConditionOperator::VersionNeq) => compare_versions(value, target_value, op),

        // string/array comparisons
        op @ (ConditionOperator::Any
        | ConditionOperator::NoneOf
        | ConditionOperator::StrStartsWithAny
        | ConditionOperator::StrEndsWithAny
        | ConditionOperator::StrContainsAny
        | ConditionOperator::StrContainsNone
        | ConditionOperator::AnyCaseSensitive
        | ConditionOperator::NoneCaseSensitive) => {
            compare_strings_in_array(value, target_value, op)
        }
        ConditionOperator::StrMatches => compare_str_with_regex(value, target_value),

        // time comparisons
        op @ (ConditionOperator::Before | ConditionOperator::After | ConditionOperator::On) => {
            compare_time(value, target_value, op)
        }

        // strict equals
        ConditionOperator::Eq => target_value.is_equal_to_user_value(value),
        ConditionOperator::Neq => !target_value.is_equal_to_user_value(value),

        // id_lists
        op @ (ConditionOperator::InSegmentList | ConditionOperator::NotInSegmentList) => {
            evaluate_id_list(ctx, op, target_value, value)
        }

        op @ (ConditionOperator::ArrayContainsAny
        | ConditionOperator::ArrayContainsNone
        | ConditionOperator::ArrayContainsAll
        | ConditionOperator::NotArrayContainsAll) => compare_arrays(value, target_value, op),

        ConditionOperator::Unknown => {
            log_w!(
                TAG,
                "Unsupported - Unknown operator: {}",
                condition.operator.as_deref().unwrap_or_default()
            );
            ctx.result.unsupported = true;
            return Ok(());
        }
    };

    Ok(())
}

fn evaluate_id_list(
    ctx: &mut EvaluatorContext<'_>,
    op: ConditionOperator,
    target_value: EvaluatorValueRef<'_>,
    value: UserValueRef<'_>,
) -> bool {
    let is_in_list = is_in_id_list(ctx, target_value, value);

    if matches!(op, ConditionOperator::NotInSegmentList) {
        return !is_in_list;
    }

    is_in_list
}

fn is_in_id_list(
    ctx: &mut EvaluatorContext<'_>,
    target_value: EvaluatorValueRef<'_>,
    value: UserValueRef<'_>,
) -> bool {
    let list_name = unwrap_or_return!(target_value.string_value(), false);
    let dyn_str = unwrap_or_return!(value.string_value(), false);
    let hashed = ctx.hashing.sha256(dyn_str);
    let lookup_id: String = hashed.chars().take(8).collect();

    match ctx.id_list_resolver {
        IdListResolution::MapLookup(id_lists) => {
            let list = unwrap_or_return!(id_lists.get(list_name), false);

            list.ids.contains(&lookup_id)
        }
        IdListResolution::Callback(callback) => callback(list_name, lookup_id.as_str()),
    }
}

fn evaluate_experiment_group<'a>(
    ctx: &mut EvaluatorContext<'a>,
    experiment_name: &Option<DynamicString>,
) -> Option<String> {
    let exp_name = match experiment_name {
        Some(name) => &name.value,
        None => {
            return None;
        }
    };
    let statsig = match &ctx.statsig {
        Some(s) => s,
        None => {
            ctx.result.unsupported = true;
            return None;
        }
    };
    let res = ctx.user.with_public_user(|user| {
        statsig.get_experiment_with_options(
            user,
            exp_name.as_str(),
            ExperimentEvaluationOptions {
                disable_exposure_logging: ctx.disable_exposure_logging,
                user_persisted_values: None,
            },
        )
    });
    res.group_name
}

fn evaluate_nested_gate<'a>(
    ctx: &mut EvaluatorContext<'a>,
    target_value: EvaluatorValueRef<'a>,
    is_fail_gate: bool,
) -> Result<(), StatsigErr> {
    let gate_name = match target_value.interned_string_value() {
        Some(name) => name,
        None => InternedString::empty_ref().into(),
    };

    match gate_name.get_from(&ctx.nested_gate_memo) {
        Some((previous_bool, previous_rule_id, previous_secondary_exposures)) => {
            ctx.result.bool_value = *previous_bool;
            ctx.result.rule_id = previous_rule_id.clone();
            ctx.result
                .secondary_exposures
                .extend_from_slice(previous_secondary_exposures);
        }
        None => {
            let parent_nested_count = ctx.nested_count;
            if let Err(error) = ctx.prep_for_nested_evaluation() {
                ctx.nested_count = parent_nested_count;
                return Err(error);
            }

            let parent_exposures = std::mem::take(&mut ctx.result.secondary_exposures);

            let gate_name_owned = gate_name.to_interned();
            let recognition = Evaluator::evaluate_with_name(ctx, &gate_name_owned, &SpecType::Gate);
            ctx.nested_count = parent_nested_count;

            let recognition = match recognition {
                Ok(recognition) => recognition,
                Err(error) => {
                    ctx.result.secondary_exposures = parent_exposures;
                    return Err(error);
                }
            };

            let mut nested_exposures = std::mem::take(&mut ctx.result.secondary_exposures);

            if recognition == Recognition::Unrecognized {
                ctx.result.bool_value = false;
                ctx.result.rule_id = None;
            }

            if ctx.result.unsupported {
                ctx.result.secondary_exposures = parent_exposures;
                return Ok(());
            }

            if !gate_name.as_str().is_empty() {
                ctx.nested_gate_memo.insert(
                    gate_name.to_interned(),
                    (
                        ctx.result.bool_value,
                        ctx.result.rule_id.clone(),
                        nested_exposures.clone(),
                    ),
                );
            }

            ctx.result.secondary_exposures = parent_exposures;
            ctx.result.secondary_exposures.append(&mut nested_exposures);
        }
    }

    let is_empty_rule_id = match &ctx.result.rule_id {
        Some(id) => id.as_str().is_empty(),
        None => true,
    };

    if !gate_name.as_str().starts_with("segment:") && !is_empty_rule_id {
        let res = &ctx.result;
        let expo = SecondaryExposure {
            gate: gate_name.to_interned(),
            gate_value: InternedString::from_bool(res.bool_value),
            rule_id: res.rule_id.clone().unwrap_or_default(),
        };

        if res.sampling_rate.is_none() {
            ctx.result.has_seen_analytical_gates = Option::from(true);
        }

        ctx.result.secondary_exposures.push(expo);
    }

    if is_fail_gate {
        ctx.result.bool_value = !ctx.result.bool_value;
    }
    Ok(())
}

fn evaluate_config_delegate<'a>(
    ctx: &mut EvaluatorContext<'a>,
    rule: RuleRef<'a>,
) -> Result<bool, StatsigErr> {
    let delegate = unwrap_or_return!(rule.config_delegate(), Ok(false));
    let delegate_spec = unwrap_or_return!(
        delegate.get_from(&ctx.specs_data.dynamic_configs.0),
        Ok(false)
    );
    let delegate_owned = delegate.to_interned();

    ctx.result.undelegated_secondary_exposures = Some(ctx.result.secondary_exposures.clone());

    ctx.prep_for_nested_evaluation()?;
    let recognition = Evaluator::evaluate_with_name(ctx, &delegate_owned, &SpecType::Experiment)?;
    if recognition == Recognition::Unrecognized {
        ctx.result.undelegated_secondary_exposures = None;
        return Ok(false);
    }

    ctx.result.explicit_parameters = delegate_spec.view().explicit_parameters();
    ctx.result.config_delegate = Some(delegate_owned);

    Ok(true)
}

fn evaluate_pass_percentage(
    ctx: &mut EvaluatorContext,
    rule: RuleRef<'_>,
    spec_salt: InternedStrRef<'_>,
) -> bool {
    let pass_percentage = rule.pass_percentage();
    if pass_percentage == 100f64 {
        return true;
    }

    if pass_percentage == 0f64 {
        return false;
    }

    let rule_salt = rule.salt().unwrap_or_else(|| rule.id()).as_str();
    let unit_id = get_unit_id(ctx, rule.id_type());
    let input = format!("{}.{rule_salt}.{unit_id}", spec_salt.as_str());
    match ctx.hashing.evaluation_hash(&input) {
        Some(hash) => ((hash % 10000) as f64) < pass_percentage * 100.0,
        None => false,
    }
}

fn get_hash_for_user_bucket(ctx: &mut EvaluatorContext, condition: &Condition) -> DynamicValue {
    let unit_id = get_unit_id(ctx, (&condition.id_type).into());

    let mut salt = InternedString::empty_ref();

    if let Some(add_values) = &condition.additional_values {
        if let Some(v) = add_values.get(&SALT) {
            salt = v;
        }
    }

    let input = format!("{salt}.{unit_id}");
    let hash = ctx.hashing.evaluation_hash(&input).unwrap_or(1);
    dyn_value!(hash % 1000)
}

fn evaluate_param_store_reason(
    ctx: &mut EvaluatorContext,
    spec_name: String,
) -> Result<Recognition, StatsigErr> {
    let spec_name_intern = InternedString::from_str_ref(&spec_name);
    let has_param_store = ctx
        .specs_data
        .param_stores
        .as_ref()
        .and_then(|stores| stores.get(&spec_name_intern))
        .is_some();
    Ok(if has_param_store {
        Recognition::Recognized
    } else {
        Recognition::Unrecognized
    })
}
