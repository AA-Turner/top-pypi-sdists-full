use super::{
    evaluation_plan::PlannedEvaluation,
    secondary_exposure_hashing::hash_secondary_exposures,
    target_app_id_utils::{should_filter_config_for_app, should_filter_spec_for_app},
};
use crate::{
    ClientInitResponseOptions, StatsigErr,
    evaluation::{
        evaluation_data::SpecView,
        evaluator::{Evaluator, SpecType},
        evaluator_context::EvaluatorContext,
    },
    gcir::gcir_formatter::GCIRHashable,
    hashing,
    interned_string::InternedString,
    specs_response::specs_hash_map::SpecsHashMap,
};
use std::collections::{HashMap, HashSet};

pub(crate) fn gcir_process_iter<T: GCIRHashable>(
    context: &mut EvaluatorContext,
    options: &ClientInitResponseOptions,
    sec_expo_hash_memo: &mut HashMap<InternedString, InternedString>,
    specs_map: &SpecsHashMap,
    get_spec_type: impl Fn(SpecView<'_>) -> SpecType,
    mut evaluation_factory: impl FnMut(&str, &str, &mut EvaluatorContext) -> T,
) -> Result<HashMap<String, T>, StatsigErr> {
    let mut results = HashMap::with_capacity(specs_map.len());
    let mut hashes = Vec::with_capacity(if options.previous_response_hash.is_some() {
        specs_map.len()
    } else {
        0
    });
    let pipeline_override_names = get_pipeline_override_names(context);
    let remove_default_value_gates = should_remove_default_value_gates(context, options);
    let mut keys = specs_map.keys().cloned().collect::<Vec<_>>();
    if options.previous_response_hash.is_some() {
        keys.sort_by(|a, b| a.as_str().cmp(b.as_str()));
    }
    for name in keys {
        let spec_ptr = match specs_map.get(&name) {
            Some(s) => s,
            None => continue,
        };
        let spec = spec_ptr.view();
        let entity = spec.entity();
        if entity.as_str() == "segment" || entity.as_str() == "holdout" {
            continue;
        }

        if pipeline_override_names.contains(&name) {
            continue;
        }

        if should_filter_entity(spec, name.as_str(), options)
            || should_filter_experiment_in_layer(context, spec, name.as_str(), options)
        {
            continue;
        }

        if should_filter_spec_for_app(spec, &context.app_id, &options.client_sdk_key) {
            continue;
        }

        context.reset_result();

        let spec_type = get_spec_type(spec);
        Evaluator::evaluate(context, name.as_str(), &spec_type)?;

        if remove_default_value_gates
            && entity.as_str() == "feature_gate"
            && context.result.rule_id.as_deref() == Some("default")
            && !context.result.bool_value
            && context.result.secondary_exposures.is_empty()
        {
            continue;
        }

        let hashed_name = context
            .hashing
            .hash(name.as_str(), options.get_hash_algorithm());
        hash_secondary_exposures(
            &mut context.result,
            context.hashing,
            options.get_hash_algorithm(),
            sec_expo_hash_memo,
        );

        let eval = evaluation_factory(entity.as_str(), &hashed_name, context);

        if options.previous_response_hash.is_some() {
            hashes.push(eval.create_hash(&name));
        }
        results.insert(hashed_name, eval);
    }

    if options.previous_response_hash.is_some() {
        context.gcir_hashes.push(hashing::hash_one(hashes));
    }

    Ok(results)
}

pub(crate) fn gcir_process_plan<T: GCIRHashable>(
    context: &mut EvaluatorContext,
    options: &ClientInitResponseOptions,
    sec_expo_hash_memo: &mut HashMap<InternedString, InternedString>,
    plan: &[PlannedEvaluation],
    evaluation_factory: impl FnMut(&str, &InternedString, &mut EvaluatorContext) -> T,
) -> Result<HashMap<InternedString, T>, StatsigErr> {
    let plan_options = PlanProcessOptions::new(context, options);

    // Dispatch once per response so option checks are compiled out of the per-config hot loop.
    match (plan_options.has_checksum, plan_options.has_extra_filters()) {
        (false, false) => gcir_process_plan_impl::<T, false, false>(
            context,
            options,
            sec_expo_hash_memo,
            plan,
            plan_options,
            evaluation_factory,
        ),
        (false, true) => gcir_process_plan_impl::<T, false, true>(
            context,
            options,
            sec_expo_hash_memo,
            plan,
            plan_options,
            evaluation_factory,
        ),
        (true, false) => gcir_process_plan_impl::<T, true, false>(
            context,
            options,
            sec_expo_hash_memo,
            plan,
            plan_options,
            evaluation_factory,
        ),
        (true, true) => gcir_process_plan_impl::<T, true, true>(
            context,
            options,
            sec_expo_hash_memo,
            plan,
            plan_options,
            evaluation_factory,
        ),
    }
}

#[derive(Clone, Copy)]
struct PlanProcessOptions {
    has_checksum: bool,
    has_entity_filters: bool,
    remove_experiments_in_layers: bool,
    should_filter_for_app: bool,
    remove_default_value_gates: bool,
}

impl PlanProcessOptions {
    fn new(context: &EvaluatorContext, options: &ClientInitResponseOptions) -> Self {
        Self {
            has_checksum: options.previous_response_hash.is_some(),
            has_entity_filters: options.feature_gate_filter.is_some()
                || options.experiment_filter.is_some()
                || options.dynamic_config_filter.is_some()
                || options.layer_filter.is_some(),
            remove_experiments_in_layers: options.remove_experiments_in_layers.unwrap_or(false),
            should_filter_for_app: options.client_sdk_key.is_some()
                && context
                    .app_id
                    .as_ref()
                    .is_some_and(|app_id| app_id.string_value.is_some()),
            remove_default_value_gates: should_remove_default_value_gates(context, options),
        }
    }

    fn has_extra_filters(self) -> bool {
        self.has_pre_eval_filters() || self.remove_default_value_gates
    }

    fn has_pre_eval_filters(self) -> bool {
        self.has_entity_filters || self.remove_experiments_in_layers || self.should_filter_for_app
    }
}

fn should_remove_default_value_gates(
    context: &EvaluatorContext,
    options: &ClientInitResponseOptions,
) -> bool {
    options.remove_default_value_gates.unwrap_or_else(|| {
        context
            .specs_data
            .gcir_config
            .as_ref()
            .is_some_and(|config| config.remove_default_value_gates)
    })
}

fn gcir_process_plan_impl<T: GCIRHashable, const WITH_CHECKSUM: bool, const WITH_FILTERS: bool>(
    context: &mut EvaluatorContext,
    options: &ClientInitResponseOptions,
    sec_expo_hash_memo: &mut HashMap<InternedString, InternedString>,
    plan: &[PlannedEvaluation],
    plan_options: PlanProcessOptions,
    mut evaluation_factory: impl FnMut(&str, &InternedString, &mut EvaluatorContext) -> T,
) -> Result<HashMap<InternedString, T>, StatsigErr> {
    let mut results = HashMap::with_capacity(plan.len());
    let mut hashes = Vec::with_capacity(if WITH_CHECKSUM { plan.len() } else { 0 });
    let hash_algorithm = options.get_hash_algorithm();
    for planned in plan {
        if WITH_FILTERS && should_filter_planned_evaluation(context, options, plan_options, planned)
        {
            continue;
        }

        context.reset_result();

        gcir_time!("plan.evaluate", {
            Evaluator::evaluate_with_name(context, &planned.name, &planned.spec_type)
        })?;

        if WITH_FILTERS && should_filter_default_gate(context, plan_options, planned) {
            continue;
        }

        let hashed_name = planned.hashed_name(hash_algorithm);
        gcir_time!("plan.hash_secondary_exposures", {
            hash_secondary_exposures(
                &mut context.result,
                context.hashing,
                hash_algorithm,
                sec_expo_hash_memo,
            )
        });

        let eval = gcir_time!("plan.result_factory", {
            evaluation_factory(planned.entity.as_str(), hashed_name, context)
        });

        if WITH_CHECKSUM {
            let hash = gcir_time!("plan.create_hash", eval.create_hash(&planned.name));
            hashes.push(hash);
        }

        gcir_time!("plan.result_insert", {
            results.insert(hashed_name.clone(), eval)
        });
    }

    if WITH_CHECKSUM {
        gcir_time!("plan.section_hash_aggregate", {
            context.gcir_hashes.push(hashing::hash_one(hashes))
        });
    }

    Ok(results)
}

fn should_filter_planned_evaluation(
    context: &EvaluatorContext,
    options: &ClientInitResponseOptions,
    plan_options: PlanProcessOptions,
    planned: &PlannedEvaluation,
) -> bool {
    if !plan_options.has_pre_eval_filters() {
        return false;
    }

    gcir_time!("plan.filtering", {
        (plan_options.has_entity_filters && should_filter_planned_entity(planned, options))
            || (plan_options.remove_experiments_in_layers
                && should_filter_planned_experiment_in_layer(planned, options))
            || (plan_options.should_filter_for_app
                && should_filter_config_for_app(
                    planned.target_app_ids.as_ref(),
                    &context.app_id,
                    &options.client_sdk_key,
                ))
    })
}

fn should_filter_default_gate(
    context: &EvaluatorContext,
    plan_options: PlanProcessOptions,
    planned: &PlannedEvaluation,
) -> bool {
    if !plan_options.remove_default_value_gates {
        return false;
    }

    gcir_time!("plan.post_eval_filters", {
        matches!(&planned.spec_type, SpecType::Gate)
            && context.result.rule_id.as_deref() == Some("default")
            && !context.result.bool_value
            && context.result.secondary_exposures.is_empty()
    })
}

fn should_filter_planned_entity(
    planned: &PlannedEvaluation,
    options: &ClientInitResponseOptions,
) -> bool {
    match &planned.spec_type {
        SpecType::Gate => options
            .feature_gate_filter
            .as_ref()
            .is_some_and(|f| !f.contains(planned.name.as_str())),
        SpecType::Experiment => options
            .experiment_filter
            .as_ref()
            .is_some_and(|f| !f.contains(planned.name.as_str())),
        SpecType::DynamicConfig => options
            .dynamic_config_filter
            .as_ref()
            .is_some_and(|f| !f.contains(planned.name.as_str())),
        SpecType::Layer => options
            .layer_filter
            .as_ref()
            .is_some_and(|f| !f.contains(planned.name.as_str())),
        SpecType::ParameterStore => false,
    }
}

fn should_filter_planned_experiment_in_layer(
    planned: &PlannedEvaluation,
    options: &ClientInitResponseOptions,
) -> bool {
    if !planned.is_experiment_in_layer {
        return false;
    }

    !is_experiment_in_layer_allowlisted(planned.name.as_str(), options)
}

fn get_pipeline_override_names(context: &EvaluatorContext) -> HashSet<InternedString> {
    context
        .specs_data
        .overrides
        .as_ref()
        .map(get_pipeline_override_names_from_mappings)
        .unwrap_or_default()
}

fn get_pipeline_override_names_from_mappings(
    overrides: &HashMap<String, Vec<crate::specs_response::spec_types::ConfigMapping>>,
) -> HashSet<InternedString> {
    overrides
        .values()
        .flat_map(|mappings| {
            mappings
                .iter()
                .map(|mapping| mapping.new_config_name.clone())
        })
        .collect()
}

fn should_filter_entity(
    spec: SpecView<'_>,
    name: &str,
    options: &ClientInitResponseOptions,
) -> bool {
    match spec.entity().as_str() {
        "feature_gate" => options
            .feature_gate_filter
            .as_ref()
            .is_some_and(|f| !f.contains(name)),
        "experiment" => options
            .experiment_filter
            .as_ref()
            .is_some_and(|f| !f.contains(name)),
        "dynamic_config" => options
            .dynamic_config_filter
            .as_ref()
            .is_some_and(|f| !f.contains(name)),
        "layer" => options
            .layer_filter
            .as_ref()
            .is_some_and(|f| !f.contains(name)),
        _ => false,
    }
}

fn should_filter_experiment_in_layer(
    context: &EvaluatorContext,
    spec: SpecView<'_>,
    name: &str,
    options: &ClientInitResponseOptions,
) -> bool {
    if spec.entity().as_str() != "experiment"
        || !options.remove_experiments_in_layers.unwrap_or(false)
    {
        return false;
    }

    if is_experiment_in_layer_allowlisted(name, options) {
        return false;
    }

    context.specs_data.experiment_to_layer.contains_key(name)
}

fn is_experiment_in_layer_allowlisted(name: &str, options: &ClientInitResponseOptions) -> bool {
    options
        .experiments_in_layers_allowlist
        .as_ref()
        .is_some_and(|allowlist| allowlist.contains(name))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::specs_response::spec_types::{ConfigMapping, OverrideRule};

    #[test]
    fn filters_only_names_from_pipeline_override_mappings() {
        let override_names = get_pipeline_override_names_from_mappings(&HashMap::from([(
            "base_config".to_string(),
            vec![ConfigMapping {
                new_config_name: InternedString::from_str_ref("base_config::trigger_id"),
                rules: vec![OverrideRule {
                    rule_name: "phase_rule".to_string(),
                    start_time: Some(0),
                }],
            }],
        )]));

        assert!(override_names.contains(&InternedString::from_str_ref("base_config::trigger_id")));
        assert!(!override_names.contains(&InternedString::from_str_ref(
            "manual_config::not_a_pipeline_override"
        )));
    }
}
