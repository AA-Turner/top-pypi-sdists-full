use super::dynamic_returnable::DynamicReturnable;
use crate::gcir::gcir_formatter::GCIRHashable;
use crate::hashing::opt_bool_to_hashable;
use crate::interned_string::InternedString;
use crate::{
    evaluation::evaluation_types::is_false, specs_response::explicit_params::ExplicitParameters,
};
use crate::{hashing, SecondaryExposure};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone)]
pub struct BaseEvaluationV2 {
    pub name: String,
    pub rule_id: InternedString,
    pub secondary_exposures: Vec<String>,
    pub version: Option<u32>,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct GateEvaluationV2 {
    #[serde(flatten)]
    pub base: BaseEvaluationV2,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub id_type: Option<InternedString>,
    pub value: bool,
}

impl GCIRHashable for GateEvaluationV2 {
    fn create_hash(&self, name: &InternedString) -> u64 {
        let version_hashes = optional_version_hash_values(&self.base.version);
        let hash_array = [
            name.hash,
            self.value as u64,
            self.base.rule_id.hash,
            hash_secondary_exposures(&self.base.secondary_exposures),
            version_hashes[0],
            version_hashes[1],
        ];
        hashing::hash_u64_slice(&hash_array)
    }
}

#[derive(Serialize, Deserialize, Clone)]
pub struct DynamicConfigEvaluationV2 {
    #[serde(flatten)]
    pub base: BaseEvaluationV2,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub id_type: Option<InternedString>,
    pub value: DynamicReturnable,

    pub is_device_based: bool,

    pub passed: bool,
}

impl GCIRHashable for DynamicConfigEvaluationV2 {
    fn create_hash(&self, name: &InternedString) -> u64 {
        let version_hashes = optional_version_hash_values(&self.base.version);
        let hash_array = [
            name.hash,
            self.value.get_hash(),
            self.base.rule_id.hash,
            hash_secondary_exposures(&self.base.secondary_exposures),
            self.passed as u64,
            version_hashes[0],
            version_hashes[1],
        ];
        hashing::hash_u64_slice(&hash_array)
    }
}

#[derive(Serialize, Deserialize, Clone)]
pub struct ExperimentEvaluationV2 {
    #[serde(flatten)]
    pub base: BaseEvaluationV2,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub id_type: Option<InternedString>,
    pub value: DynamicReturnable,

    pub is_device_based: bool,

    #[serde(skip_serializing_if = "is_false")]
    pub is_in_layer: bool,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub explicit_parameters: Option<ExplicitParameters>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub group_name: Option<InternedString>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_experiment_active: Option<bool>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_user_in_experiment: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub undelegated_secondary_exposures: Option<Vec<SecondaryExposure>>,
}

impl GCIRHashable for ExperimentEvaluationV2 {
    fn create_hash(&self, name: &InternedString) -> u64 {
        let version_hashes = optional_version_hash_values(&self.base.version);
        let hash_array = [
            name.hash,
            self.value.get_hash(),
            self.base.rule_id.hash,
            hash_secondary_exposures(&self.base.secondary_exposures),
            self.is_in_layer as u64,
            version_hashes[0],
            version_hashes[1],
            hash_explicit_parameters(self.explicit_parameters.as_ref()),
            self.group_name.as_ref().map_or(0, |g| g.hash),
            opt_bool_to_hashable(&self.is_experiment_active),
            opt_bool_to_hashable(&self.is_user_in_experiment),
        ];

        hashing::hash_u64_slice(&hash_array)
    }
}

#[derive(Serialize, Deserialize, Clone)]
#[serde(untagged)]
pub enum AnyConfigEvaluationV2 {
    DynamicConfig(DynamicConfigEvaluationV2),
    Experiment(ExperimentEvaluationV2),
}

impl GCIRHashable for AnyConfigEvaluationV2 {
    fn create_hash(&self, name: &InternedString) -> u64 {
        match self {
            AnyConfigEvaluationV2::DynamicConfig(eval) => eval.create_hash(name),
            AnyConfigEvaluationV2::Experiment(eval) => eval.create_hash(name),
        }
    }
}

#[derive(Serialize, Deserialize, Clone)]
pub struct LayerEvaluationV2 {
    #[serde(flatten)]
    pub base: BaseEvaluationV2,

    pub value: DynamicReturnable,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub id_type: Option<InternedString>,

    pub is_device_based: bool,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub group_name: Option<InternedString>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_experiment_active: Option<bool>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub is_user_in_experiment: Option<bool>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub allocated_experiment_name: Option<InternedString>,
    pub explicit_parameters: ExplicitParameters,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub undelegated_secondary_exposures: Option<Vec<InternedString>>,
}

impl GCIRHashable for LayerEvaluationV2 {
    fn create_hash(&self, name: &InternedString) -> u64 {
        let version_hashes = optional_version_hash_values(&self.base.version);
        let hash_array = [
            name.hash,
            self.value.get_hash(),
            self.base.rule_id.hash,
            hash_secondary_exposures(&self.base.secondary_exposures),
            self.group_name.as_ref().map_or(0, |g| g.hash),
            opt_bool_to_hashable(&self.is_experiment_active),
            opt_bool_to_hashable(&self.is_user_in_experiment),
            self.allocated_experiment_name
                .as_ref()
                .map_or(0, |n| n.hash),
            version_hashes[0],
            version_hashes[1],
            hash_explicit_parameters(Some(&self.explicit_parameters)),
            hash_optional_interned_string_exposures(self.undelegated_secondary_exposures.as_ref()),
        ];

        hashing::hash_u64_slice(&hash_array)
    }
}

fn hash_secondary_exposures(exposures: &[String]) -> u64 {
    let mut secondary_exposure_hashes = hashing::U64HashBuilder::with_capacity(exposures.len());
    for exposure in exposures {
        secondary_exposure_hashes.push(hashing::ahash_str(exposure));
    }
    secondary_exposure_hashes.finish()
}

fn hash_optional_interned_string_exposures(exposures: Option<&Vec<InternedString>>) -> u64 {
    let Some(exposures) = exposures else {
        return hashing::hash_u64_slice(&[]);
    };

    let mut exposure_hashes = hashing::U64HashBuilder::with_capacity(exposures.len());
    for exposure in exposures {
        exposure_hashes.push(exposure.hash);
    }
    exposure_hashes.finish()
}

fn hash_explicit_parameters(explicit_parameters: Option<&ExplicitParameters>) -> u64 {
    let Some(explicit_parameters) = explicit_parameters else {
        return hashing::hash_u64_slice(&[]);
    };

    let mut explicit_params_hashes =
        hashing::U64HashBuilder::with_capacity(explicit_parameters.as_slice().len());
    for value in explicit_parameters.as_slice() {
        explicit_params_hashes.push(value.hash);
    }
    explicit_params_hashes.finish()
}

fn optional_version_hash_values(version: &Option<u32>) -> [u64; 2] {
    [version.is_some() as u64, version.map_or(0, u64::from)]
}
