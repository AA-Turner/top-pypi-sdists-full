use super::{evaluation_plan::PlannedEvaluation, target_app_id_utils::should_filter_spec_for_app};
use crate::{
    evaluation::{
        evaluator::{Evaluator, SpecType},
        evaluator_context::EvaluatorContext,
        evaluator_result::EvaluatorResult,
        secondary_exposure_key::SecondaryExposureKey,
    },
    gcir::gcir_formatter::GCIRHashable,
    hashing::{self, HashUtil},
    interned_string::InternedString,
    specs_response::{spec_types::Spec, specs_hash_map::SpecsHashMap},
    ClientInitResponseOptions, HashAlgorithm, SecondaryExposure, StatsigErr,
};
use std::collections::{HashMap, HashSet};

pub(crate) fn gcir_process_iter<T: GCIRHashable>(
    context: &mut EvaluatorContext,
    options: &ClientInitResponseOptions,
    sec_expo_hash_memo: &mut HashMap<InternedString, InternedString>,
    specs_map: &SpecsHashMap,
    get_spec_type: impl Fn(&Spec) -> SpecType,
    mut evaluation_factory: impl FnMut(&str, &str, &mut EvaluatorContext) -> T,
) -> Result<HashMap<String, T>, StatsigErr> {
    let mut results = HashMap::with_capacity(specs_map.len());
    let mut hashes = Vec::with_capacity(if options.previous_response_hash.is_some() {
        specs_map.len()
    } else {
        0
    });
    let pipeline_override_names = get_pipeline_override_names(context);
    let mut keys = specs_map.keys().cloned().collect::<Vec<_>>();
    if options.previous_response_hash.is_some() {
        keys.sort_by(|a, b| a.as_str().cmp(b.as_str()));
    }
    for name in keys {
        let spec_ptr = match specs_map.get(&name) {
            Some(s) => s,
            None => continue,
        };
        let spec = spec_ptr.as_spec_ref();
        if spec.entity == "segment" || spec.entity == "holdout" {
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

        if options.remove_default_value_gates.unwrap_or(false)
            && spec.entity == "feature_gate"
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

        let eval = evaluation_factory(&spec.entity, &hashed_name, context);

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
    specs_map: &SpecsHashMap,
    plan: &[PlannedEvaluation],
    mut evaluation_factory: impl FnMut(&str, &InternedString, &mut EvaluatorContext) -> T,
) -> Result<HashMap<InternedString, T>, StatsigErr> {
    let mut results = HashMap::with_capacity(plan.len());
    let mut hashes = Vec::with_capacity(if options.previous_response_hash.is_some() {
        plan.len()
    } else {
        0
    });
    let hash_algorithm = options.get_hash_algorithm();
    for planned in plan {
        let spec_ptr = match gcir_time!("plan.spec_lookup", specs_map.get(&planned.name)) {
            Some(s) => s,
            None => continue,
        };
        let spec = spec_ptr.as_spec_ref();

        if gcir_time!("plan.filtering", {
            should_filter_entity(spec, planned.name.as_str(), options)
                || should_filter_experiment_in_layer(context, spec, planned.name.as_str(), options)
                || should_filter_spec_for_app(spec, &context.app_id, &options.client_sdk_key)
        }) {
            continue;
        }

        context.reset_result();

        gcir_time!("plan.evaluate", {
            Evaluator::evaluate(context, planned.name.as_str(), &planned.spec_type)
        })?;

        if gcir_time!("plan.post_eval_filters", {
            options.remove_default_value_gates.unwrap_or(false)
                && spec.entity == "feature_gate"
                && context.result.rule_id.as_deref() == Some("default")
                && !context.result.bool_value
                && context.result.secondary_exposures.is_empty()
        }) {
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

        if options.previous_response_hash.is_some() {
            let hash = gcir_time!("plan.create_hash", eval.create_hash(&planned.name));
            hashes.push(hash);
        }
        gcir_time!("plan.result_insert", {
            results.insert(hashed_name.clone(), eval)
        });
    }

    if options.previous_response_hash.is_some() {
        gcir_time!("plan.section_hash_aggregate", {
            context.gcir_hashes.push(hashing::hash_one(hashes))
        });
    }

    Ok(results)
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

fn should_filter_entity(spec: &Spec, name: &str, options: &ClientInitResponseOptions) -> bool {
    match spec.entity.as_str() {
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
    spec: &Spec,
    name: &str,
    options: &ClientInitResponseOptions,
) -> bool {
    if spec.entity != "experiment" || !options.remove_experiments_in_layers.unwrap_or(false) {
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

pub fn hash_secondary_exposures(
    result: &mut EvaluatorResult,
    hashing: &HashUtil,
    hash_algorithm: &HashAlgorithm,
    memo: &mut HashMap<InternedString, InternedString>,
) {
    fn loop_filter_n_hash(
        exposures: &mut Vec<SecondaryExposure>,
        hashing: &HashUtil,
        hash_algorithm: &HashAlgorithm,
        memo: &mut HashMap<InternedString, InternedString>,
    ) {
        let mut seen = HashSet::<SecondaryExposureKey>::with_capacity(exposures.len());
        exposures.retain_mut(|expo| {
            let expo_key = SecondaryExposureKey::from(&*expo);
            if seen.contains(&expo_key) {
                return false;
            }
            seen.insert(expo_key);

            match memo.get(&expo.gate) {
                Some(hash) => {
                    expo.gate = hash.clone();
                }
                None => {
                    let hash = hashing.hash(&expo.gate, hash_algorithm);
                    let interned_hash = InternedString::from_string(hash);
                    let old = std::mem::replace(&mut expo.gate, interned_hash.clone());
                    memo.insert(old, interned_hash);
                }
            }
            true
        });
    }

    if !result.secondary_exposures.is_empty() {
        loop_filter_n_hash(
            &mut result.secondary_exposures,
            hashing,
            hash_algorithm,
            memo,
        );
    }

    if let Some(undelegated_secondary_exposures) = result.undelegated_secondary_exposures.as_mut() {
        loop_filter_n_hash(
            undelegated_secondary_exposures,
            hashing,
            hash_algorithm,
            memo,
        );
    }
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
