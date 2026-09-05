use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use serde::Serialize;

use crate::evaluation::dynamic_value::DynamicValue;
use crate::evaluation::evaluation_types::{AnyConfigEvaluation, GateEvaluation, LayerEvaluation};
use crate::evaluation::evaluator::{Evaluator, Recognition, SpecType};
use crate::evaluation::evaluator_context::{EvaluatorContext, IdListResolution};
use crate::evaluation::evaluator_result::{
    result_to_dynamic_config_eval, result_to_experiment_eval, result_to_gate_eval,
    result_to_layer_eval,
};
use crate::gcir::gcir_formatter::{GCIRFormatter, GCIRHashable};
use crate::hashing::{self, HashAlgorithm, HashUtil};
use crate::interned_string::InternedString;
use crate::spec_store::{SpecStoreData, build_live_overlay_target_app_index};
use crate::specs_response::spec_types::SpecsResponseFull;
use crate::user::StatsigUserInternal;
use crate::{
    ClientInitResponseOptions, DynamicReturnable, InitializeResponse, OverrideAdapter, Statsig,
    StatsigErr, StatsigUser,
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum SnapshotConfigKind {
    DynamicConfig,
    Experiment,
}

/// A snapshot-pinned gate evaluation plus the metadata needed for exposure shaping.
#[doc(hidden)]
pub struct SnapshotGateEvaluation {
    pub evaluation: Option<GateEvaluation>,
    /// Preserves the optional rule ID before typed conversion applies an empty fallback.
    pub rule_id: Option<InternedString>,
    pub is_holdout: bool,
    pub group_name: Option<InternedString>,
}

/// A snapshot-pinned config evaluation.
#[doc(hidden)]
pub struct SnapshotConfigEvaluation {
    pub evaluation: Option<AnyConfigEvaluation>,
    /// Whether the evaluator produced a value before typed conversion applies an empty fallback.
    pub has_evaluated_value: bool,
    pub group_name: Option<InternedString>,
}

/// The entity filters needed to build a live overlay response.
#[doc(hidden)]
#[derive(Default)]
pub struct SnapshotLiveEntityFilters {
    pub feature_gates: HashSet<String>,
    pub dynamic_configs: HashSet<String>,
    pub experiments: HashSet<String>,
    pub layer_configs: HashSet<String>,
}

/// Selects the normal client initialize response or the explicit live-only overlay.
#[doc(hidden)]
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SnapshotInitializeMode {
    Full,
    LiveOverlay,
}

/// The deterministic, response-hashed names of live entities included in an initialize response.
#[doc(hidden)]
#[derive(Default, Serialize)]
pub struct SnapshotLiveEntityNames {
    pub feature_gates: Vec<InternedString>,
    pub dynamic_configs: Vec<InternedString>,
    pub experiments: Vec<InternedString>,
    pub layer_configs: Vec<InternedString>,
}

impl SnapshotLiveEntityNames {
    pub fn is_empty(&self) -> bool {
        self.feature_gates.is_empty()
            && self.dynamic_configs.is_empty()
            && self.experiments.is_empty()
            && self.layer_configs.is_empty()
    }
}

/// A complete snapshot-pinned client initialization plus its SDK-owned live-overlay metadata.
#[doc(hidden)]
pub struct SnapshotInitializeResult {
    pub response: InitializeResponse,
    pub live_entity_names: SnapshotLiveEntityNames,
    pub live_seed_checksum: Option<u64>,
    pub live_overlay_checksum: Option<String>,
}

/// Pins one parsed SDK snapshot for all work in a request.
///
/// This intentionally exposes typed evaluation and metadata operations rather than the
/// underlying parsed specs or GCIR plan.
#[doc(hidden)]
pub struct SnapshotEvaluationSession<'statsig> {
    data: Arc<SpecStoreData>,
    hashing: HashUtil,
    plan_hashing: &'statsig HashUtil,
    should_use_third_party_parser: bool,
    statsig: Option<&'statsig Statsig>,
    override_adapter: Option<&'statsig Arc<dyn OverrideAdapter>>,
}

impl<'statsig> SnapshotEvaluationSession<'statsig> {
    #[cfg(test)]
    pub(crate) fn new(
        data: Arc<SpecStoreData>,
        hashing: &'statsig HashUtil,
        should_use_third_party_parser: bool,
    ) -> Self {
        Self::new_with_statsig(data, hashing, should_use_third_party_parser, None, None)
    }

    pub(crate) fn new_with_statsig(
        data: Arc<SpecStoreData>,
        hashing: &'statsig HashUtil,
        should_use_third_party_parser: bool,
        statsig: Option<&'statsig Statsig>,
        override_adapter: Option<&'statsig Arc<dyn OverrideAdapter>>,
    ) -> Self {
        Self {
            data,
            hashing: HashUtil::new(),
            plan_hashing: hashing,
            should_use_third_party_parser,
            statsig,
            override_adapter,
        }
    }

    /// Returns the sync cursor for the pinned snapshot. Cursor-only updates may make this newer
    /// than the semantic payload time without changing the pinned snapshot.
    #[cfg(test)]
    pub fn lcut(&self) -> u64 {
        self.data.lcut()
    }

    pub fn has_live_overlay_entities_for_target_app(&self, target_app_id: Option<&str>) -> bool {
        let index = self
            .data
            .live_overlay_target_app_index
            .get_or_init(|| build_live_overlay_target_app_index(self.data.snapshot.as_ref()));
        target_app_id.map_or(index.has_live_entities, |app_id| {
            index.target_app_ids.contains(app_id)
        })
    }

    pub fn has_config(&self, config_name: &str, target_app_id: Option<&str>) -> bool {
        let snapshot = self.data.snapshot.as_ref();
        let spec_name = InternedString::from_str_ref(config_name);
        if let Some(spec) = snapshot.dynamic_configs.get(&spec_name) {
            let spec = spec.as_spec_ref();
            return !is_target_app_ineligible_str(spec.target_app_ids.as_deref(), target_app_id)
                && matches!(
                    spec.entity.as_str(),
                    "dynamic_config" | "experiment" | "autotune" | "autotune_experiment"
                );
        }

        snapshot
            .cmab_configs
            .as_ref()
            .and_then(|configs| configs.get(config_name))
            .is_some_and(|config| {
                !is_target_app_ineligible_str(config.target_app_ids.as_deref(), target_app_id)
            })
    }

    pub fn has_layer(&self, layer_name: &str, target_app_id: Option<&str>) -> bool {
        let spec_name = InternedString::from_str_ref(layer_name);
        self.data
            .snapshot
            .layer_configs
            .get(&spec_name)
            .is_some_and(|spec| {
                !is_target_app_ineligible_str(
                    spec.as_spec_ref().target_app_ids.as_deref(),
                    target_app_id,
                )
            })
    }

    pub fn evaluate_gate(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        gate_name: &str,
    ) -> Result<SnapshotGateEvaluation, StatsigErr> {
        self.with_evaluator(user, target_app_id, |evaluator| {
            evaluator.evaluate_gate(gate_name)
        })
    }

    pub fn evaluate_segment(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        segment_name: &str,
    ) -> Result<SnapshotGateEvaluation, StatsigErr> {
        self.with_evaluator(user, target_app_id, |evaluator| {
            evaluator.evaluate_segment(segment_name)
        })
    }

    pub fn evaluate_gates_borrowed<Name: AsRef<str>>(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        gate_names: impl IntoIterator<Item = Name>,
        mut consume: impl FnMut(Name, &SnapshotGateEvaluation) -> Result<(), StatsigErr>,
    ) -> Result<(), StatsigErr> {
        self.with_evaluator(user, target_app_id, |evaluator| {
            for gate_name in gate_names {
                let mut evaluation = evaluator.evaluate_gate(gate_name.as_ref())?;
                consume(gate_name, &evaluation)?;
                if let Some(gate) = evaluation.evaluation.take() {
                    evaluator.context.result.secondary_exposures = gate.base.secondary_exposures;
                }
            }
            Ok(())
        })
    }

    pub fn evaluate_config(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        config_name: &str,
    ) -> Result<SnapshotConfigEvaluation, StatsigErr> {
        let name = InternedString::from_str_ref(config_name);
        let Some((kind, spec_type, spec_entity)) =
            select_config_spec(self.data.snapshot.as_ref(), &name, target_app_id)
        else {
            return Ok(SnapshotConfigEvaluation {
                evaluation: None,
                has_evaluated_value: false,
                group_name: None,
            });
        };

        self.with_evaluator(user, target_app_id, |evaluator| {
            evaluator.evaluate_selected_config(&name, kind, &spec_type, spec_entity)
        })
    }

    pub fn evaluate_layer(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        layer_name: &str,
    ) -> Result<Option<LayerEvaluation>, StatsigErr> {
        let name = InternedString::from_str_ref(layer_name);
        let Some(spec) = self.data.snapshot.layer_configs.get(&name) else {
            return Ok(None);
        };
        if is_target_app_ineligible_str(spec.as_spec_ref().target_app_ids.as_deref(), target_app_id)
        {
            return Ok(None);
        }

        self.with_evaluator(user, target_app_id, |evaluator| {
            evaluator.evaluate_selected_layer(&name)
        })
    }

    pub fn generate_client_init_response(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        options: &ClientInitResponseOptions,
    ) -> Result<InitializeResponse, StatsigErr> {
        self.with_evaluator(user, target_app_id, |evaluator| {
            evaluator.generate_client_init_response(options)
        })
    }

    /// Builds one complete client response without exposing live-evaluation orchestration.
    pub fn generate_client_initialize_response(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        options: &ClientInitResponseOptions,
        mode: SnapshotInitializeMode,
    ) -> Result<SnapshotInitializeResult, StatsigErr> {
        if mode == SnapshotInitializeMode::LiveOverlay {
            let live_options = self.live_initialize_options(options, false);
            let response =
                self.generate_client_init_response(user, target_app_id, &live_options)?;
            let live_entity_names = build_live_entity_names(&response);
            let live_overlay_checksum =
                Some(build_live_overlay_checksum(&response, &live_entity_names));

            return Ok(SnapshotInitializeResult {
                response,
                live_entity_names,
                live_seed_checksum: None,
                live_overlay_checksum,
            });
        }

        let mut response = self.generate_client_init_response(user, target_app_id, options)?;
        if !response.has_updates {
            return Ok(SnapshotInitializeResult {
                response,
                live_entity_names: SnapshotLiveEntityNames::default(),
                live_seed_checksum: None,
                live_overlay_checksum: None,
            });
        }
        if !self.has_live_overlay_entities_for_target_app(target_app_id) {
            return Ok(SnapshotInitializeResult {
                response,
                live_entity_names: SnapshotLiveEntityNames::default(),
                live_seed_checksum: None,
                live_overlay_checksum: None,
            });
        }

        let live_options = self.live_initialize_options(options, true);
        let live_response =
            self.generate_client_init_response(user, target_app_id, &live_options)?;
        let live_entity_names = build_live_entity_names(&live_response);
        let live_seed_checksum =
            build_live_seed_checksum(live_response.full_checksum.as_deref(), &live_entity_names)?;

        response.feature_gates.extend(live_response.feature_gates);
        response
            .dynamic_configs
            .extend(live_response.dynamic_configs);
        response.layer_configs.extend(live_response.layer_configs);

        Ok(SnapshotInitializeResult {
            response,
            live_entity_names,
            live_seed_checksum,
            live_overlay_checksum: None,
        })
    }

    pub fn live_entity_filters(&self) -> SnapshotLiveEntityFilters {
        let snapshot = self.data.snapshot.as_ref();
        let dynamic_configs = collect_live_entity_filter(&snapshot.dynamic_configs);

        SnapshotLiveEntityFilters {
            feature_gates: collect_live_entity_filter(&snapshot.feature_gates),
            experiments: dynamic_configs.clone(),
            dynamic_configs,
            layer_configs: collect_live_entity_filter(&snapshot.layer_configs),
        }
    }

    fn live_initialize_options(
        &self,
        options: &ClientInitResponseOptions,
        include_seed_checksum: bool,
    ) -> ClientInitResponseOptions {
        let live_filters = self.live_entity_filters();

        ClientInitResponseOptions {
            hash_algorithm: options.hash_algorithm.as_ref().map(copy_hash_algorithm),
            client_sdk_key: options.client_sdk_key.clone(),
            include_local_overrides: options.include_local_overrides,
            feature_gate_filter: Some(live_filters.feature_gates),
            experiment_filter: Some(live_filters.experiments),
            dynamic_config_filter: Some(live_filters.dynamic_configs),
            layer_filter: Some(live_filters.layer_configs),
            param_store_filter: Some(HashSet::new()),
            remove_default_value_gates: Some(false),
            previous_response_hash: include_seed_checksum.then(String::new),
            remove_experiments_in_layers: Some(false),
            ..ClientInitResponseOptions::default()
        }
    }

    pub fn references_any_condition_field(&self, fields: &HashSet<String>) -> bool {
        if fields.is_empty() {
            return false;
        }

        let snapshot = self.data.snapshot.as_ref();
        [
            &snapshot.feature_gates,
            &snapshot.dynamic_configs,
            &snapshot.layer_configs,
        ]
        .into_iter()
        .any(|specs| {
            specs.iter().any(|(_, spec)| {
                spec.as_spec_ref()
                    .rules
                    .iter()
                    .any(|rule| rule_references_any_condition_field(snapshot, rule, fields))
            })
        }) || snapshot
            .override_rules
            .as_ref()
            .is_some_and(|override_rules| {
                override_rules
                    .values()
                    .any(|rule| rule_references_any_condition_field(snapshot, rule, fields))
            })
    }

    /// Creates a request-local evaluator that stays pinned to this session's snapshot.
    pub fn with_evaluator<T>(
        &self,
        user: &StatsigUser,
        target_app_id: Option<&str>,
        evaluate: impl FnOnce(&mut SnapshotEvaluator<'_>) -> T,
    ) -> T {
        let app_id = target_app_id.map(DynamicValue::from);
        self.with_evaluator_app_id(user, app_id.as_ref(), evaluate)
    }

    fn with_evaluator_app_id<T>(
        &self,
        user: &StatsigUser,
        app_id: Option<&DynamicValue>,
        evaluate: impl FnOnce(&mut SnapshotEvaluator<'_>) -> T,
    ) -> T {
        let user_internal = StatsigUserInternal::new(user, self.statsig);
        let mut context = EvaluatorContext::new(
            &user_internal,
            self.data.snapshot.as_ref(),
            IdListResolution::MapLookup(self.data.id_lists.as_ref()),
            &self.hashing,
            app_id,
            self.override_adapter,
            self.should_use_third_party_parser,
            false,
        );
        let mut evaluator = SnapshotEvaluator {
            context: &mut context,
            data: self.data.as_ref(),
            hashing: self.plan_hashing,
        };

        evaluate(&mut evaluator)
    }
}

/// Performs typed evaluations against one pinned session.
#[doc(hidden)]
pub struct SnapshotEvaluator<'a> {
    context: &'a mut EvaluatorContext<'a>,
    data: &'a SpecStoreData,
    hashing: &'a HashUtil,
}

impl SnapshotEvaluator<'_> {
    pub fn evaluate_gate(&mut self, gate_name: &str) -> Result<SnapshotGateEvaluation, StatsigErr> {
        self.evaluate_gate_with_target_app_filter(gate_name, true)
    }

    pub fn evaluate_segment(
        &mut self,
        segment_name: &str,
    ) -> Result<SnapshotGateEvaluation, StatsigErr> {
        self.evaluate_gate_with_target_app_filter(segment_name, false)
    }

    fn evaluate_gate_with_target_app_filter(
        &mut self,
        gate_name: &str,
        filter_target_app: bool,
    ) -> Result<SnapshotGateEvaluation, StatsigErr> {
        self.context.reset_result();
        let spec_name = InternedString::from_str_ref(gate_name);
        let Some(spec) = self
            .context
            .specs_data
            .feature_gates
            .get(&spec_name)
            .map(|spec| spec.as_spec_ref())
        else {
            return Ok(SnapshotGateEvaluation {
                evaluation: None,
                rule_id: None,
                is_holdout: false,
                group_name: None,
            });
        };

        let is_holdout = spec.entity.as_str() == "holdout";
        if filter_target_app
            && is_target_app_ineligible(spec.target_app_ids.as_deref(), self.context.app_id)
        {
            return Ok(SnapshotGateEvaluation {
                evaluation: None,
                rule_id: None,
                is_holdout,
                group_name: None,
            });
        }

        if Evaluator::evaluate(self.context, gate_name, &SpecType::Gate)?
            == Recognition::Unrecognized
        {
            return Ok(SnapshotGateEvaluation {
                evaluation: None,
                rule_id: None,
                is_holdout,
                group_name: None,
            });
        }

        let rule_id = self.context.result.rule_id.clone();
        let group_name = self.context.result.group_name.clone();
        Ok(SnapshotGateEvaluation {
            evaluation: Some(result_to_gate_eval(gate_name, &mut self.context.result)),
            rule_id,
            is_holdout,
            group_name,
        })
    }

    fn evaluate_selected_config(
        &mut self,
        name: &InternedString,
        kind: SnapshotConfigKind,
        spec_type: &SpecType,
        spec_entity: Option<&str>,
    ) -> Result<SnapshotConfigEvaluation, StatsigErr> {
        let config_name = name.as_str();
        self.context.reset_result();
        if Evaluator::evaluate_with_name(self.context, name, spec_type)?
            == Recognition::Unrecognized
        {
            return Ok(SnapshotConfigEvaluation {
                evaluation: None,
                has_evaluated_value: false,
                group_name: None,
            });
        }

        let has_evaluated_value = self.context.result.json_value.is_some();
        let group_name = self.context.result.group_name.clone();
        let evaluation = match kind {
            SnapshotConfigKind::DynamicConfig => AnyConfigEvaluation::DynamicConfig(
                result_to_dynamic_config_eval(config_name, &mut self.context.result),
            ),
            SnapshotConfigKind::Experiment => AnyConfigEvaluation::Experiment(
                result_to_experiment_eval(config_name, spec_entity, &mut self.context.result),
            ),
        };
        if has_evaluated_value {
            if let AnyConfigEvaluation::DynamicConfig(evaluation) = &evaluation {
                validate_dynamic_config_value(&evaluation.value)?;
            }
        }

        Ok(SnapshotConfigEvaluation {
            evaluation: Some(evaluation),
            has_evaluated_value,
            group_name,
        })
    }

    fn evaluate_selected_layer(
        &mut self,
        name: &InternedString,
    ) -> Result<Option<LayerEvaluation>, StatsigErr> {
        let layer_name = name.as_str();
        self.context.reset_result();
        if Evaluator::evaluate_with_name(self.context, name, &SpecType::Layer)?
            == Recognition::Unrecognized
        {
            return Ok(None);
        }

        Ok(Some(result_to_layer_eval(
            layer_name,
            &mut self.context.result,
        )))
    }

    /// Generates a response using the pinned snapshot's default GCIR policy.
    ///
    /// Leaving remove_default_value_gates unset applies the snapshot policy. An explicit value is
    /// reserved for response-specific overrides, such as keeping default gates in a live overlay.
    pub fn generate_client_init_response(
        &mut self,
        options: &ClientInitResponseOptions,
    ) -> Result<InitializeResponse, StatsigErr> {
        self.context.gcir_hashes.clear();
        let plan = self.data.gcir_evaluation_plan(self.hashing);
        let override_adapter = self.context.override_adapter;
        if options.include_local_overrides != Some(true) {
            self.context.override_adapter = None;
        }
        let response = GCIRFormatter::generate_v1_format_with_plan(self.context, options, plan);
        self.context.override_adapter = override_adapter;
        let mut response = response?;
        if response.has_updates {
            response.time = self.data.lcut();
        }
        Ok(response)
    }
}

fn validate_dynamic_config_value(value: &DynamicReturnable) -> Result<(), StatsigErr> {
    let object_len = value
        .get_json_pointer_ref()
        .map(|value| value.len())
        .or_else(|| value.get_json_archived_ref().map(|value| value.len()));
    if object_len.is_none()
        || (object_len == Some(0) && value.get_hash() != crate::hashing::hash_one(b"{}"))
    {
        return Err(StatsigErr::SerializationError(
            "Dynamic config value must be a JSON object".to_string(),
        ));
    }
    Ok(())
}

fn rule_references_any_condition_field(
    snapshot: &SpecsResponseFull,
    rule: &crate::specs_response::spec_types::Rule,
    fields: &HashSet<String>,
) -> bool {
    rule.conditions.iter().any(|condition_id| {
        snapshot
            .condition_map
            .get(condition_id)
            .and_then(|condition| condition.field.as_ref())
            .is_some_and(|field| fields.contains(field.lowercased_value.as_str()))
    })
}

fn select_config_spec(
    specs: &SpecsResponseFull,
    config_name: &InternedString,
    target_app_id: Option<&str>,
) -> Option<(SnapshotConfigKind, SpecType, Option<&'static str>)> {
    if let Some(spec) = specs.dynamic_configs.get(config_name) {
        let spec = spec.as_spec_ref();
        if is_target_app_ineligible_str(spec.target_app_ids.as_deref(), target_app_id) {
            return None;
        }

        let entity = match spec.entity.as_str() {
            "dynamic_config" => {
                return Some((
                    SnapshotConfigKind::DynamicConfig,
                    SpecType::DynamicConfig,
                    None,
                ));
            }
            "experiment" => "experiment",
            "autotune" => "autotune",
            "autotune_experiment" => "autotune_experiment",
            _ => return None,
        };

        return Some((
            SnapshotConfigKind::Experiment,
            SpecType::Experiment,
            Some(entity),
        ));
    }

    let cmab = specs.cmab_configs.as_ref()?.get(config_name.as_str())?;
    if is_target_app_ineligible_str(cmab.target_app_ids.as_deref(), target_app_id) {
        return None;
    }

    Some((SnapshotConfigKind::Experiment, SpecType::Experiment, None))
}

fn is_target_app_ineligible(
    target_app_ids: Option<&[InternedString]>,
    app_id: Option<&DynamicValue>,
) -> bool {
    is_target_app_ineligible_str(target_app_ids, dynamic_value_string(app_id))
}

fn is_target_app_ineligible_str(
    target_app_ids: Option<&[InternedString]>,
    app_id: Option<&str>,
) -> bool {
    let Some(app_id) = app_id else {
        return false;
    };

    target_app_ids.is_none_or(|target_app_ids| {
        !target_app_ids
            .iter()
            .any(|candidate| candidate.as_str() == app_id)
    })
}

fn dynamic_value_string(value: Option<&DynamicValue>) -> Option<&str> {
    value
        .and_then(|value| value.string_value.as_ref())
        .map(|value| value.value.as_str())
}

fn collect_live_entity_filter(
    specs: &crate::specs_response::specs_hash_map::SpecsHashMap,
) -> HashSet<String> {
    specs
        .iter()
        .filter(|(_, spec)| spec.session_update_mode() == Some("live"))
        .map(|(name, _)| name.as_str().to_string())
        .collect()
}

fn copy_hash_algorithm(algorithm: &HashAlgorithm) -> HashAlgorithm {
    match algorithm {
        HashAlgorithm::Djb2 => HashAlgorithm::Djb2,
        HashAlgorithm::None => HashAlgorithm::None,
        HashAlgorithm::Sha256 => HashAlgorithm::Sha256,
    }
}

fn build_live_entity_names(response: &InitializeResponse) -> SnapshotLiveEntityNames {
    let mut names = SnapshotLiveEntityNames {
        feature_gates: response.feature_gates.keys().cloned().collect(),
        dynamic_configs: Vec::new(),
        experiments: Vec::new(),
        layer_configs: response.layer_configs.keys().cloned().collect(),
    };
    for (name, evaluation) in &response.dynamic_configs {
        match evaluation {
            AnyConfigEvaluation::DynamicConfig(_) => names.dynamic_configs.push(name.clone()),
            AnyConfigEvaluation::Experiment(_) => names.experiments.push(name.clone()),
        }
    }

    for category in [
        &mut names.feature_gates,
        &mut names.dynamic_configs,
        &mut names.experiments,
        &mut names.layer_configs,
    ] {
        category.sort_unstable_by(|left, right| left.as_str().cmp(right.as_str()));
    }

    names
}

fn build_live_overlay_checksum(
    response: &InitializeResponse,
    live_entity_names: &SnapshotLiveEntityNames,
) -> String {
    hashing::hash_one((
        "live_overlay",
        response.hash_used.as_str(),
        hash_live_evaluations(&response.feature_gates),
        hash_live_evaluations(&response.dynamic_configs),
        hash_live_evaluations(&response.layer_configs),
        hash_live_names(&live_entity_names.feature_gates),
        hash_live_names(&live_entity_names.dynamic_configs),
        hash_live_names(&live_entity_names.experiments),
        hash_live_names(&live_entity_names.layer_configs),
    ))
    .to_string()
}

fn hash_live_evaluations<T: GCIRHashable>(values: &HashMap<InternedString, T>) -> u64 {
    hashing::hash_unordered(
        values
            .iter()
            .map(|(name, evaluation)| evaluation.create_hash(name))
            .collect(),
    )
}

fn hash_live_names(names: &[InternedString]) -> u64 {
    hashing::hash_unordered(names.iter().map(|name| name.hash).collect())
}

fn build_live_seed_checksum(
    response_checksum: Option<&str>,
    names: &SnapshotLiveEntityNames,
) -> Result<Option<u64>, StatsigErr> {
    if names.is_empty() {
        return Ok(None);
    }

    let response_checksum = response_checksum.ok_or_else(|| {
        StatsigErr::ChecksumFailure("live overlay seed checksum is missing".to_string())
    })?;
    Ok(Some(hashing::hash_one((
        "live_overlay_seed",
        response_checksum,
        &names.feature_gates,
        &names.dynamic_configs,
        &names.experiments,
        &names.layer_configs,
    ))))
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::sync::Arc;

    use serde_json::json;

    use super::{
        SnapshotEvaluationSession, SnapshotInitializeMode, SnapshotLiveEntityNames,
        build_live_overlay_checksum, build_live_seed_checksum, validate_dynamic_config_value,
    };
    use crate::{
        ClientInitResponseOptions, DynamicReturnable, HashAlgorithm, InitializeResponse,
        SpecsSource, SpecsUpdate, StatsigErr, StatsigUser,
        evaluation::evaluation_types::AnyConfigEvaluation, hashing::HashUtil,
        interned_string::InternedString, networking::ResponseData,
        scoped_snapshot_registry::EvaluationEngine,
    };

    fn engine_with_target_app_specs() -> Arc<EvaluationEngine> {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] = json!(["allowed-app"]);
        specs["layer_configs"]["layer_with_many_params"]["targetAppIDs"] = json!(["allowed-app"]);

        engine_with_specs(specs)
    }

    fn engine_with_specs(specs: serde_json::Value) -> Arc<EvaluationEngine> {
        EvaluationEngine::from_fixture(
            serde_json::to_string(&specs).expect("fixture should serialize"),
            None,
        )
        .expect("fixture evaluation engine should initialize")
    }

    fn snapshot_session(engine: &EvaluationEngine) -> SnapshotEvaluationSession<'_> {
        engine.snapshot_evaluation_session(engine.snapshot_evaluation_data())
    }

    #[test]
    fn snapshot_sessions_do_not_share_request_hashing() {
        let engine = engine_with_target_app_specs();
        let first = snapshot_session(&engine);
        let second = snapshot_session(&engine);

        assert!(
            !std::ptr::eq::<HashUtil>(&first.hashing, &second.hashing),
            "concurrent snapshot sessions must not serialize evaluation hashing"
        );
    }

    #[test]
    fn direct_evaluation_keeps_target_app_filtering_inside_the_sdk() {
        let engine = engine_with_target_app_specs();
        let session = snapshot_session(&engine);
        let user = StatsigUser::with_user_id("direct-target-app-user");

        assert!(session.has_config("test_custom_config", Some("allowed-app")));
        assert!(!session.has_config("test_custom_config", Some("other-app")));
        assert!(session.has_layer("layer_with_many_params", Some("allowed-app")));
        assert!(!session.has_layer("layer_with_many_params", Some("other-app")));

        let allowed_config = session
            .evaluate_config(&user, Some("allowed-app"), "test_custom_config")
            .unwrap();
        let allowed_layer = session
            .evaluate_layer(&user, Some("allowed-app"), "layer_with_many_params")
            .unwrap();
        assert!(allowed_config.evaluation.is_some());
        assert!(allowed_layer.is_some());

        let denied_config = session
            .evaluate_config(&user, Some("other-app"), "test_custom_config")
            .unwrap();
        let denied_layer = session
            .evaluate_layer(&user, Some("other-app"), "layer_with_many_params")
            .unwrap();
        assert!(denied_config.evaluation.is_none());
        assert!(denied_layer.is_none());
    }

    #[test]
    fn live_overlay_presence_filters_each_entity_type_by_target_app() {
        for (collection, entity_name) in [
            ("feature_gates", "test_small_pass_gate"),
            ("dynamic_configs", "test_custom_config"),
            ("layer_configs", "layer_with_many_params"),
        ] {
            let mut specs: serde_json::Value =
                serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
            specs[collection][entity_name]["sessionUpdateMode"] = json!("live");
            specs[collection][entity_name]["targetAppIDs"] = json!(["allowed-app"]);

            let engine = engine_with_specs(specs);
            let session = snapshot_session(&engine);

            assert!(
                session.has_live_overlay_entities_for_target_app(Some("allowed-app")),
                "matching {collection} should be eligible"
            );
            assert!(
                !session.has_live_overlay_entities_for_target_app(Some("other-app")),
                "nonmatching {collection} should be ineligible"
            );
            assert!(session.has_live_overlay_entities_for_target_app(None));
        }
    }

    #[test]
    fn scoped_live_overlay_requires_explicit_matching_target_app() {
        for target_apps in [None, Some(json!([]))] {
            let mut specs: serde_json::Value =
                serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
            let spec = specs["feature_gates"]["test_small_pass_gate"]
                .as_object_mut()
                .unwrap();
            spec.insert("sessionUpdateMode".to_string(), json!("live"));
            if let Some(target_apps) = target_apps {
                spec.insert("targetAppIDs".to_string(), target_apps);
            } else {
                spec.remove("targetAppIDs");
            }

            let engine = engine_with_specs(specs);
            let session = snapshot_session(&engine);

            assert!(!session.has_live_overlay_entities_for_target_app(Some("allowed-app")));
            assert!(session.has_live_overlay_entities_for_target_app(None));
        }
    }

    #[test]
    fn live_overlay_presence_ignores_non_live_entities() {
        let engine = engine_with_target_app_specs();
        let session = snapshot_session(&engine);

        assert!(!session.has_live_overlay_entities_for_target_app(Some("allowed-app")));
        assert!(!session.has_live_overlay_entities_for_target_app(None));
    }

    #[test]
    fn full_initialize_owns_scoped_live_seed_merge_and_checksum() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        for (collection, name) in [
            ("feature_gates", "test_small_pass_gate"),
            ("dynamic_configs", "test_custom_config"),
            ("dynamic_configs", "test_experiment_no_targeting"),
            ("layer_configs", "layer_with_many_params"),
        ] {
            specs[collection][name]["sessionUpdateMode"] = json!("live");
            specs[collection][name]["targetAppIDs"] = json!(["allowed-app"]);
        }

        let engine = engine_with_specs(specs);
        let session = snapshot_session(&engine);
        let user = StatsigUser::with_user_id("live-initialize-user");
        let options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            client_sdk_key: Some("client-live-test".to_string()),
            previous_response_hash: Some(String::new()),
            remove_default_value_gates: Some(true),
            remove_experiments_in_layers: Some(true),
            ..ClientInitResponseOptions::default()
        };

        let result = session
            .generate_client_initialize_response(
                &user,
                Some("allowed-app"),
                &options,
                SnapshotInitializeMode::Full,
            )
            .unwrap();

        assert!(
            result
                .live_entity_names
                .feature_gates
                .iter()
                .any(|name| name.as_str() == "test_small_pass_gate")
        );
        assert!(
            result
                .live_entity_names
                .dynamic_configs
                .iter()
                .any(|name| name.as_str() == "test_custom_config")
        );
        assert!(
            result
                .live_entity_names
                .experiments
                .iter()
                .any(|name| name.as_str() == "test_experiment_no_targeting")
        );
        assert!(
            result
                .live_entity_names
                .layer_configs
                .iter()
                .any(|name| name.as_str() == "layer_with_many_params")
        );
        assert!(result.live_seed_checksum.is_some());
        assert!(result.response.full_checksum.is_some());

        for name in &result.live_entity_names.feature_gates {
            assert!(result.response.feature_gates.contains_key(name));
        }
        for name in result
            .live_entity_names
            .dynamic_configs
            .iter()
            .chain(&result.live_entity_names.experiments)
        {
            assert!(result.response.dynamic_configs.contains_key(name));
        }
        for name in &result.live_entity_names.layer_configs {
            assert!(result.response.layer_configs.contains_key(name));
        }
    }

    #[test]
    fn full_initialize_skips_live_seed_for_nonmatching_target_app() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = json!("live");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] = json!(["allowed-app"]);

        let engine = engine_with_specs(specs);
        let session = snapshot_session(&engine);
        let user = StatsigUser::with_user_id("live-initialize-other-app-user");
        let options = ClientInitResponseOptions {
            previous_response_hash: Some(String::new()),
            ..ClientInitResponseOptions::default()
        };

        let result = session
            .generate_client_initialize_response(
                &user,
                Some("other-app"),
                &options,
                SnapshotInitializeMode::Full,
            )
            .unwrap();

        assert!(result.live_entity_names.is_empty());
        assert!(result.live_seed_checksum.is_none());
    }

    #[test]
    fn full_initialize_preserves_blank_response_when_checksum_matches_with_live_entities() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = json!("live");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] = json!(["allowed-app"]);

        let engine = engine_with_specs(specs);
        let session = snapshot_session(&engine);
        let user = StatsigUser::with_user_id("live-initialize-matching-checksum-user");
        let initial_options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            previous_response_hash: Some(String::new()),
            ..ClientInitResponseOptions::default()
        };
        let checksum = session
            .generate_client_init_response(&user, Some("allowed-app"), &initial_options)
            .unwrap()
            .full_checksum
            .unwrap();
        let matching_options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            previous_response_hash: Some(checksum),
            ..ClientInitResponseOptions::default()
        };

        let result = session
            .generate_client_initialize_response(
                &user,
                Some("allowed-app"),
                &matching_options,
                SnapshotInitializeMode::Full,
            )
            .unwrap();

        assert!(!result.response.has_updates);
        assert!(result.response.feature_gates.is_empty());
        assert!(result.response.dynamic_configs.is_empty());
        assert!(result.response.layer_configs.is_empty());
        assert!(result.live_entity_names.is_empty());
        assert!(result.live_seed_checksum.is_none());
    }

    #[test]
    fn explicit_live_initialize_keeps_only_live_entities_without_seed_checksum() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["dynamic_configs"]["test_custom_config"]["sessionUpdateMode"] = json!("live");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] = json!(["allowed-app"]);
        specs["dynamic_configs"]["test_experiment_no_targeting"]["targetAppIDs"] =
            json!(["allowed-app"]);

        let engine = engine_with_specs(specs);
        let session = snapshot_session(&engine);
        let user = StatsigUser::with_user_id("live-initialize-explicit-user");
        let options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            client_sdk_key: Some("client-live-test".to_string()),
            include_local_overrides: Some(true),
            previous_response_hash: Some("should-not-affect-live-overlay".to_string()),
            ..ClientInitResponseOptions::default()
        };
        assert_eq!(
            session
                .live_initialize_options(&options, false)
                .include_local_overrides,
            Some(true)
        );

        let result = session
            .generate_client_initialize_response(
                &user,
                Some("allowed-app"),
                &options,
                SnapshotInitializeMode::LiveOverlay,
            )
            .unwrap();

        assert_eq!(
            result
                .live_entity_names
                .dynamic_configs
                .iter()
                .map(InternedString::as_str)
                .collect::<Vec<_>>(),
            ["test_custom_config"]
        );
        assert!(result.live_entity_names.experiments.is_empty());
        assert!(result.live_seed_checksum.is_none());
        assert!(result.live_overlay_checksum.is_some());
        assert!(result.response.full_checksum.is_none());
        assert_eq!(result.response.dynamic_configs.len(), 1);
        assert!(result.response.param_stores.is_empty());
    }

    #[test]
    fn explicit_live_overlay_checksum_includes_the_entity_manifest() {
        let mut response = InitializeResponse::blank_without_user();
        response.hash_used = "djb2".to_string();
        let first = build_live_overlay_checksum(
            &response,
            &SnapshotLiveEntityNames {
                feature_gates: vec![InternedString::from_str_ref("a")],
                ..Default::default()
            },
        );
        let second = build_live_overlay_checksum(
            &response,
            &SnapshotLiveEntityNames {
                feature_gates: vec![InternedString::from_str_ref("b")],
                ..Default::default()
            },
        );

        assert_ne!(first, second);
    }

    #[test]
    fn live_seed_checksum_preserves_empty_and_missing_checksum_contracts() {
        let empty = SnapshotLiveEntityNames::default();
        assert!(build_live_seed_checksum(None, &empty).unwrap().is_none());

        let names = SnapshotLiveEntityNames {
            feature_gates: vec![InternedString::from_str_ref("live_gate")],
            ..SnapshotLiveEntityNames::default()
        };
        assert!(matches!(
            build_live_seed_checksum(None, &names),
            Err(StatsigErr::ChecksumFailure(message))
                if message == "live overlay seed checksum is missing"
        ));
    }

    #[test]
    fn live_overlay_target_app_index_stays_pinned_to_its_semantic_snapshot() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json")).unwrap();
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = json!("live");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] = json!(["first-app"]);
        let engine = engine_with_specs(specs.clone());
        let first = snapshot_session(&engine);
        assert!(first.has_live_overlay_entities_for_target_app(Some("first-app")));
        assert!(!first.has_live_overlay_entities_for_target_app(Some("second-app")));

        specs["time"] = json!(first.lcut() + 1);
        specs["checksum"] = json!("updated-live-overlay-snapshot");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] = json!(["second-app"]);
        engine
            .update_fixture_for_test(SpecsUpdate {
                data: ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap()),
                source: SpecsSource::Network,
                received_at: 2,
                source_api: Some("live-overlay-semantic-refresh".to_string()),
                has_updates: None,
            })
            .unwrap();

        let refreshed = snapshot_session(&engine);
        assert!(first.has_live_overlay_entities_for_target_app(Some("first-app")));
        assert!(!first.has_live_overlay_entities_for_target_app(Some("second-app")));
        assert!(!refreshed.has_live_overlay_entities_for_target_app(Some("first-app")));
        assert!(refreshed.has_live_overlay_entities_for_target_app(Some("second-app")));
    }

    #[test]
    fn direct_config_evaluation_preserves_experiment_and_autotune_metadata() {
        let engine = engine_with_target_app_specs();
        let session = snapshot_session(&engine);
        let user = StatsigUser::with_user_id("direct-experiment-entity-user");

        let experiment = session
            .evaluate_config(&user, None, "test_experiment_no_targeting")
            .unwrap()
            .evaluation
            .expect("experiment should evaluate");
        let autotune = session
            .evaluate_config(&user, None, "test_autotune")
            .unwrap()
            .evaluation
            .expect("autotune should evaluate");

        let AnyConfigEvaluation::Experiment(experiment) = experiment else {
            panic!("experiment should retain its typed evaluation");
        };
        let AnyConfigEvaluation::Experiment(autotune) = autotune else {
            panic!("autotune should retain its typed evaluation");
        };

        assert!(experiment.is_experiment_active.is_some());
        assert!(experiment.is_user_in_experiment.is_some());
        assert!(autotune.is_experiment_active.is_none());
        assert!(autotune.is_user_in_experiment.is_none());
    }

    #[test]
    fn direct_gate_segment_and_initialize_evaluation_use_sdk_context() {
        let engine = engine_with_target_app_specs();
        let session = snapshot_session(&engine);
        let user = StatsigUser::with_user_id("direct-evaluation-context-user");

        assert!(
            session
                .evaluate_gate(&user, None, "missing-gate")
                .unwrap()
                .evaluation
                .is_none()
        );
        assert!(
            session
                .evaluate_segment(&user, None, "segment:missing")
                .unwrap()
                .evaluation
                .is_none()
        );

        let response = session
            .generate_client_init_response(
                &user,
                None,
                &crate::ClientInitResponseOptions::default(),
            )
            .unwrap();

        assert_eq!(response.time, session.lcut());
    }

    #[test]
    fn dynamic_config_validation_accepts_object_values() {
        let empty = DynamicReturnable::from_map(HashMap::new());
        let populated = DynamicReturnable::from_map(HashMap::from([(
            "enabled".to_string(),
            serde_json::Value::Bool(true),
        )]));

        assert!(validate_dynamic_config_value(&empty).is_ok());
        assert!(validate_dynamic_config_value(&populated).is_ok());
    }

    #[test]
    fn dynamic_config_validation_rejects_scalar_values() {
        let value = DynamicReturnable::from_bool(true);

        assert!(matches!(
            validate_dynamic_config_value(&value),
            Err(StatsigErr::SerializationError(message))
                if message == "Dynamic config value must be a JSON object"
        ));
    }
}
