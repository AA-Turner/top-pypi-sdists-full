use std::collections::{HashMap, HashSet};

use crate::{
    evaluation::evaluator::SpecType,
    hashing::{HashAlgorithm, HashUtil},
    interned_string::InternedString,
    specs_response::{
        cmab_types::CMABConfig,
        spec_types::{Spec, SpecsResponseFull},
        specs_hash_map::SpecsHashMap,
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
    get_spec_type: impl Fn(&Spec) -> SpecType,
) -> Vec<PlannedEvaluation> {
    let mut keys = specs_map.keys().cloned().collect::<Vec<_>>();
    keys.sort_by(|a, b| a.as_str().cmp(b.as_str()));

    keys.into_iter()
        .filter_map(|name| {
            let spec = specs_map.get(&name)?.as_spec_ref();
            if spec.entity == "segment"
                || spec.entity == "holdout"
                || pipeline_override_names.contains(&name)
            {
                return None;
            }

            let is_experiment_in_layer =
                spec.entity == "experiment" && experiment_to_layer.contains_key(name.as_str());

            Some(PlannedEvaluation {
                hashed_djb2: InternedString::from_string(
                    hashing.hash(name.as_str(), &HashAlgorithm::Djb2),
                ),
                hashed_sha256: InternedString::from_string(
                    hashing.hash(name.as_str(), &HashAlgorithm::Sha256),
                ),
                name,
                entity: InternedString::from_str_ref(spec.entity.as_str()),
                spec_type: get_spec_type(spec),
                target_app_ids: spec.target_app_ids.clone(),
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
    keys.sort();

    keys.into_iter()
        .map(|name| PlannedCmabEvaluation {
            hashed_djb2: InternedString::from_string(
                hashing.hash(name.as_str(), &HashAlgorithm::Djb2),
            ),
            hashed_sha256: InternedString::from_string(
                hashing.hash(name.as_str(), &HashAlgorithm::Sha256),
            ),
            name: InternedString::from_string(name),
        })
        .collect()
}

fn dynamic_config_type(spec: &Spec) -> SpecType {
    if spec.entity == "dynamic_config" {
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
