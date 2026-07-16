use std::collections::{HashMap, HashSet};

use crate::{
    evaluation::{evaluation_data::SpecView, evaluator::SpecType},
    hashing::{HashAlgorithm, HashUtil},
    interned_string::InternedString,
    specs_response::{
        cmab_types::CMABConfig, spec_types::SpecsResponseFull, specs_hash_map::SpecsHashMap,
    },
};

#[derive(Debug)]
pub struct GcirEvaluationPlan {
    pub(crate) feature_gates: Vec<PlannedEvaluation>,
    pub(crate) dynamic_configs: Vec<PlannedEvaluation>,
    pub(crate) cmab_configs: Vec<PlannedCmabEvaluation>,
    pub(crate) layer_configs: Vec<PlannedEvaluation>,
}

#[derive(Debug)]
pub(crate) struct PlannedEvaluation {
    pub(crate) name: InternedString,
    pub(crate) entity: InternedString,
    pub(crate) spec_type: SpecType,
    pub(crate) target_app_ids: Option<Vec<InternedString>>,
    pub(crate) is_experiment_in_layer: bool,
    hashed_djb2: InternedString,
    hashed_sha256: InternedString,
}

#[derive(Debug)]
pub(crate) struct PlannedCmabEvaluation {
    pub(crate) name: InternedString,
    hashed_djb2: InternedString,
    hashed_sha256: InternedString,
}

impl GcirEvaluationPlan {
    #[must_use]
    pub fn new(specs: &SpecsResponseFull, hashing: &HashUtil) -> Self {
        let pipeline_override_names = get_pipeline_override_names(specs);
        Self {
            feature_gates: build_spec_plan(
                &specs.feature_gates,
                &pipeline_override_names,
                &specs.experiment_to_layer,
                hashing,
                |_| SpecType::Gate,
            ),
            dynamic_configs: build_spec_plan(
                &specs.dynamic_configs,
                &pipeline_override_names,
                &specs.experiment_to_layer,
                hashing,
                dynamic_config_type,
            ),
            cmab_configs: build_cmab_plan(specs.cmab_configs.as_ref(), hashing),
            layer_configs: build_spec_plan(
                &specs.layer_configs,
                &pipeline_override_names,
                &specs.experiment_to_layer,
                hashing,
                |_| SpecType::Layer,
            ),
        }
    }

    pub(crate) fn total_evaluation_count(&self) -> usize {
        self.feature_gates.len()
            + self.dynamic_configs.len()
            + self.cmab_configs.len()
            + self.layer_configs.len()
    }
}

impl PlannedEvaluation {
    pub(crate) fn hashed_name(&self, hash_algorithm: &HashAlgorithm) -> &InternedString {
        match hash_algorithm {
            HashAlgorithm::Djb2 => &self.hashed_djb2,
            HashAlgorithm::None => &self.name,
            HashAlgorithm::Sha256 => &self.hashed_sha256,
        }
    }
}

impl PlannedCmabEvaluation {
    pub(crate) fn hashed_name(&self, hash_algorithm: &HashAlgorithm) -> &InternedString {
        match hash_algorithm {
            HashAlgorithm::Djb2 => &self.hashed_djb2,
            HashAlgorithm::None => &self.name,
            HashAlgorithm::Sha256 => &self.hashed_sha256,
        }
    }
}

fn build_spec_plan(
    specs_map: &SpecsHashMap,
    pipeline_override_names: &HashSet<InternedString>,
    experiment_to_layer: &HashMap<String, String>,
    hashing: &HashUtil,
    get_spec_type: impl Fn(SpecView<'_>) -> SpecType,
) -> Vec<PlannedEvaluation> {
    let mut keys = specs_map.keys().cloned().collect::<Vec<_>>();
    keys.sort_unstable_by(|a, b| a.as_str().cmp(b.as_str()));

    keys.into_iter()
        .filter_map(|name| {
            let spec = specs_map.get(&name)?.view();
            let entity = spec.entity();
            if entity.as_str() == "segment"
                || entity.as_str() == "holdout"
                || pipeline_override_names.contains(&name)
            {
                return None;
            }

            let is_experiment_in_layer =
                entity.as_str() == "experiment" && experiment_to_layer.contains_key(name.as_str());

            Some(PlannedEvaluation {
                hashed_djb2: InternedString::from_string_uninterned(
                    hashing.hash(name.as_str(), &HashAlgorithm::Djb2),
                ),
                hashed_sha256: InternedString::from_string_uninterned(
                    hashing.hash(name.as_str(), &HashAlgorithm::Sha256),
                ),
                name,
                entity: entity.to_interned(),
                spec_type: get_spec_type(spec),
                target_app_ids: spec.target_app_ids(),
                is_experiment_in_layer,
            })
        })
        .collect()
}

fn build_cmab_plan(
    cmab_configs: Option<&std::collections::HashMap<String, CMABConfig>>,
    hashing: &HashUtil,
) -> Vec<PlannedCmabEvaluation> {
    let Some(cmab_configs) = cmab_configs else {
        return Vec::new();
    };

    let mut keys = cmab_configs.keys().cloned().collect::<Vec<_>>();
    keys.sort_unstable();

    keys.into_iter()
        .map(|name| PlannedCmabEvaluation {
            hashed_djb2: InternedString::from_string_uninterned(
                hashing.hash(name.as_str(), &HashAlgorithm::Djb2),
            ),
            hashed_sha256: InternedString::from_string_uninterned(
                hashing.hash(name.as_str(), &HashAlgorithm::Sha256),
            ),
            name: InternedString::from_string_uninterned(name),
        })
        .collect()
}

fn dynamic_config_type(spec: SpecView<'_>) -> SpecType {
    if spec.entity().as_str() == "dynamic_config" {
        SpecType::DynamicConfig
    } else {
        SpecType::Experiment
    }
}

fn get_pipeline_override_names(specs: &SpecsResponseFull) -> HashSet<InternedString> {
    specs
        .overrides
        .as_ref()
        .map(|overrides| {
            overrides
                .values()
                .flat_map(|mappings| {
                    mappings
                        .iter()
                        .map(|mapping| mapping.new_config_name.clone())
                })
                .collect()
        })
        .unwrap_or_default()
}

#[cfg(test)]
mod tests {
    use super::GcirEvaluationPlan;
    use crate::{
        dcs_str::DCS_STR, hashing::HashUtil, interned_string::InternedStringValue,
        specs_response::spec_types::SpecsResponseFull,
    };

    #[test]
    fn generated_response_names_do_not_use_the_global_interner() {
        let specs: SpecsResponseFull = serde_json::from_str(DCS_STR).unwrap();
        let plan = GcirEvaluationPlan::new(&specs, &HashUtil::new());

        for (planned, source) in [
            (&plan.feature_gates, &specs.feature_gates),
            (&plan.dynamic_configs, &specs.dynamic_configs),
            (&plan.layer_configs, &specs.layer_configs),
        ] {
            for evaluation in planned {
                let original = source
                    .keys()
                    .find(|name| name.as_str() == evaluation.name.as_str())
                    .unwrap();
                match (&evaluation.name.value, &original.value) {
                    (InternedStringValue::Pointer(left), InternedStringValue::Pointer(right))
                    | (
                        InternedStringValue::Uninterned(left),
                        InternedStringValue::Uninterned(right),
                    ) => {
                        assert!(std::sync::Arc::ptr_eq(left, right));
                    }
                    (InternedStringValue::Static(left), InternedStringValue::Static(right)) => {
                        assert!(std::ptr::eq(*left, *right));
                    }
                    (left, right) => {
                        panic!("planned name changed representation: {left:?} vs {right:?}")
                    }
                }
            }
        }

        for planned in plan
            .feature_gates
            .iter()
            .chain(&plan.dynamic_configs)
            .chain(&plan.layer_configs)
        {
            assert!(matches!(
                planned.hashed_djb2.value,
                InternedStringValue::Uninterned(_)
            ));
            assert!(matches!(
                planned.hashed_sha256.value,
                InternedStringValue::Uninterned(_)
            ));
        }

        for planned in &plan.cmab_configs {
            assert!(matches!(
                planned.name.value,
                InternedStringValue::Uninterned(_)
            ));
            assert!(matches!(
                planned.hashed_djb2.value,
                InternedStringValue::Uninterned(_)
            ));
            assert!(matches!(
                planned.hashed_sha256.value,
                InternedStringValue::Uninterned(_)
            ));
        }
    }
}
