use ahash::AHashMap;
use fancy_regex::Regex as FancyRegex;
use lazy_static::lazy_static;
use parking_lot::Mutex;

use crate::{
    DynamicReturnable,
    evaluation::{
        dynamic_string::DynamicString,
        evaluator_value::{EvaluatorValueType, MemoizedEvaluatorValue},
    },
    hashing,
    interned_string::InternedString,
    interned_values::mmap_data_v2::{
        ArchivedMmapDynamicString, ArchivedMmapEvaluatorValue, ArchivedMmapEvaluatorValueType,
        ArchivedMmapReturnable, ArchivedMmapRule, ArchivedMmapSpec,
    },
    specs_response::{
        explicit_params::ExplicitParameters,
        spec_types::{Rule, Spec},
    },
};

use super::{MMAP_DATA, get_returnable, get_string};
use crate::interned_values::interned_store::InternedStore;

lazy_static! {
    static ref MMAP_EVALUATOR_MATERIALIZATIONS: Mutex<AHashMap<u64, &'static MemoizedEvaluatorValue>> =
        Mutex::new(AHashMap::new());
    static ref MMAP_SPEC_MATERIALIZATIONS: Mutex<AHashMap<usize, &'static Spec>> =
        Mutex::new(AHashMap::new());
    static ref MMAP_LIVE_SPEC_MATERIALIZATIONS: Mutex<AHashMap<usize, &'static Spec>> =
        Mutex::new(AHashMap::new());
}

impl InternedStore {
    pub(crate) fn materialize_mmap_evaluator_value(
        hash: u64,
        value: &'static ArchivedMmapEvaluatorValue,
        regex: Option<&'static FancyRegex>,
    ) -> &'static MemoizedEvaluatorValue {
        let mut materialized = MMAP_EVALUATOR_MATERIALIZATIONS.lock();
        if let Some(value) = materialized.get(&hash) {
            return value;
        }

        let value = Box::leak(Box::new(materialize_evaluator_value(value, regex)));
        materialized.insert(hash, value);
        value
    }

    pub(crate) fn materialize_mmap_evaluator_value_owned(
        value: &ArchivedMmapEvaluatorValue,
        regex: Option<&FancyRegex>,
    ) -> MemoizedEvaluatorValue {
        materialize_evaluator_value(value, regex)
    }

    pub(crate) fn get_mmap_returnable(value: &ArchivedMmapReturnable) -> DynamicReturnable {
        match value {
            ArchivedMmapReturnable::Null => DynamicReturnable::empty(),
            ArchivedMmapReturnable::Bool(value) => DynamicReturnable::from_bool(*value),
            ArchivedMmapReturnable::Json(hash) => DynamicReturnable::from_archived(
                hash.to_native(),
                get_returnable(hash.to_native())
                    .expect("validated mmap returnable reference must exist"),
            ),
        }
    }

    pub(crate) fn get_mmap_explicit_parameters(
        values: &rkyv::vec::ArchivedVec<rkyv::primitive::ArchivedU64>,
    ) -> ExplicitParameters {
        let key = values as *const _ as usize;
        mmap_explicit_parameters()
            .get(&key)
            .expect("preloaded mmap explicit parameters must exist")
            .clone()
    }

    pub(crate) fn materialize_mmap_spec(spec: &ArchivedMmapSpec) -> &'static Spec {
        let key = spec as *const _ as usize;
        let mut cached = MMAP_SPEC_MATERIALIZATIONS.lock();
        if let Some(spec) = cached.get(&key) {
            return spec;
        }

        let spec = Box::leak(Box::new(materialize_spec(spec, None)));
        cached.insert(key, spec);
        spec
    }

    pub(crate) fn materialize_mmap_live_spec(spec: &ArchivedMmapSpec) -> &'static Spec {
        let key = spec as *const _ as usize;
        let mut cached = MMAP_LIVE_SPEC_MATERIALIZATIONS.lock();
        if let Some(spec) = cached.get(&key) {
            return spec;
        }

        let spec = Box::leak(Box::new(materialize_spec(
            spec,
            Some(InternedString::from_str_ref("live")),
        )));
        cached.insert(key, spec);
        spec
    }

    #[cfg(test)]
    pub(crate) fn get_mmap_spec_materialization_len() -> usize {
        MMAP_SPEC_MATERIALIZATIONS.lock().len()
    }
}

pub(super) fn initialize_explicit_parameters() {
    let _ = mmap_explicit_parameters();
}

fn mmap_explicit_parameters() -> &'static AHashMap<usize, ExplicitParameters> {
    let registry = MMAP_DATA
        .get()
        .expect("mmap data must be installed before explicit parameters are initialized");

    registry.explicit_parameters.get_or_init(|| {
        let mut parameters = AHashMap::new();
        for project in registry.projects.iter() {
            let archive = project.archive.borrow_archived();
            for specs in [
                &archive.feature_gates,
                &archive.dynamic_configs,
                &archive.layer_configs,
            ] {
                for (_, spec) in specs.iter() {
                    let Some(values) = spec.explicit_parameters.as_ref() else {
                        continue;
                    };
                    let key = values as *const _ as usize;
                    let value = ExplicitParameters::from_interned(
                        values
                            .iter()
                            .map(|hash| mmap_interned_string(hash.to_native()))
                            .collect(),
                    );
                    parameters.insert(key, value);
                }
            }
        }
        parameters
    })
}

fn materialize_evaluator_value(
    value: &ArchivedMmapEvaluatorValue,
    regex: Option<&FancyRegex>,
) -> MemoizedEvaluatorValue {
    let string_for_hash = |hash: u64| get_string(hash).unwrap_or_default();

    let object_value = value.object_value.as_ref().map(|object| {
        object
            .iter()
            .map(|(key, value)| {
                (
                    InternedString::from_str_ref(string_for_hash(key.to_native())),
                    DynamicString::from(string_for_hash(value.to_native()).to_string()),
                )
            })
            .collect()
    });

    let array_value = value.array_value.as_ref().map(|array| {
        array
            .iter()
            .map(|(lowercase, entry)| {
                (
                    InternedString::from_str_ref(string_for_hash(lowercase.to_native())),
                    (
                        entry.0.to_native() as usize,
                        InternedString::from_str_ref(string_for_hash(entry.1.to_native())),
                    ),
                )
            })
            .collect()
    });

    MemoizedEvaluatorValue {
        value_type: match value.value_type {
            ArchivedMmapEvaluatorValueType::Null => EvaluatorValueType::Null,
            ArchivedMmapEvaluatorValueType::Bool => EvaluatorValueType::Bool,
            ArchivedMmapEvaluatorValueType::Number => EvaluatorValueType::Number,
            ArchivedMmapEvaluatorValueType::String => EvaluatorValueType::String,
            ArchivedMmapEvaluatorValueType::Array => EvaluatorValueType::Array,
            ArchivedMmapEvaluatorValueType::Object => EvaluatorValueType::Object,
        },
        bool_value: value.bool_value.as_ref().copied(),
        float_value: value.float_value.as_ref().map(|value| value.to_native()),
        string_value: value
            .string_value
            .as_ref()
            .map(|hash| DynamicString::from(string_for_hash(hash.to_native()).to_string())),
        regex_value: regex.cloned(),
        timestamp_value: value
            .timestamp_value
            .as_ref()
            .map(|value| value.to_native()),
        object_value,
        array_value,
    }
}

fn mmap_interned_string(hash: u64) -> InternedString {
    InternedString::from_static(
        hash,
        get_string(hash).expect("validated mmap string reference must exist"),
    )
}

fn mmap_dynamic_string(value: &ArchivedMmapDynamicString) -> DynamicString {
    let raw = get_string(value.value.to_native()).unwrap_or_default();
    DynamicString {
        value: mmap_interned_string(value.value.to_native()),
        lowercased_value: mmap_interned_string(value.lowercased_value.to_native()),
        hash_value: hashing::ahash_str(raw),
    }
}

fn materialize_rule(rule: &ArchivedMmapRule) -> Rule {
    Rule {
        name: mmap_interned_string(rule.name.to_native()),
        pass_percentage: rule.pass_percentage.to_native(),
        return_value: InternedStore::get_mmap_returnable(&rule.return_value),
        id: mmap_interned_string(rule.id.to_native()),
        salt: rule
            .salt
            .as_ref()
            .map(|value| mmap_interned_string(value.to_native())),
        conditions: rule
            .conditions
            .iter()
            .map(|value| mmap_interned_string(value.to_native()))
            .collect(),
        id_type: mmap_dynamic_string(&rule.id_type),
        group_name: rule
            .group_name
            .as_ref()
            .map(|value| mmap_interned_string(value.to_native())),
        config_delegate: rule
            .config_delegate
            .as_ref()
            .map(|value| mmap_interned_string(value.to_native())),
        is_experiment_group: rule.is_experiment_group.as_ref().copied(),
        sampling_rate: rule.sampling_rate.as_ref().map(|value| value.to_native()),
    }
}

fn materialize_spec(spec: &ArchivedMmapSpec, session_update_mode: Option<InternedString>) -> Spec {
    Spec {
        checksum: spec
            .checksum
            .as_ref()
            .map(|value| mmap_interned_string(value.to_native())),
        _type: mmap_interned_string(spec.spec_type.to_native()),
        salt: mmap_interned_string(spec.salt.to_native()),
        default_value: InternedStore::get_mmap_returnable(&spec.default_value),
        enabled: spec.enabled,
        rules: spec.rules.iter().map(materialize_rule).collect(),
        id_type: mmap_interned_string(spec.id_type.to_native()),
        explicit_parameters: spec
            .explicit_parameters
            .as_ref()
            .map(InternedStore::get_mmap_explicit_parameters),
        entity: mmap_interned_string(spec.entity.to_native()),
        has_shared_params: spec.has_shared_params.as_ref().copied(),
        is_active: spec.is_active.as_ref().copied(),
        version: spec.version.as_ref().map(|value| value.to_native()),
        target_app_ids: spec.target_app_ids.as_ref().map(|values| {
            values
                .iter()
                .map(|value| mmap_interned_string(value.to_native()))
                .collect()
        }),
        forward_all_exposures: spec.forward_all_exposures.as_ref().copied(),
        fields_used: spec.fields_used.as_ref().map(|values| {
            values
                .iter()
                .map(|value| mmap_interned_string(value.to_native()))
                .collect()
        }),
        use_new_layer_eval: spec.use_new_layer_eval.as_ref().copied(),
        session_update_mode,
    }
}
