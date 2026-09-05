use std::collections::{HashMap, HashSet};
use std::sync::Arc;

use serde_json::Value;

#[cfg(test)]
use crate::Statsig;
use crate::evaluation::evaluation_data::{RuleRef, SpecView};
use crate::evaluation::evaluation_types::LayerEvaluation;
use crate::hashing::HashUtil;
use crate::id_lists_adapter::{IdList, IdListMetadata};
use crate::interned_string::InternedString;
use crate::scoped_id_list_membership_service::ScopedIdListMembershipService;
use crate::scoped_snapshot_registry::EvaluationEngine;
use crate::snapshot_evaluation_session::{
    SnapshotConfigEvaluation, SnapshotEvaluationSession, SnapshotGateEvaluation,
    SnapshotInitializeMode, SnapshotInitializeResult, SnapshotLiveEntityNames,
};
use crate::spec_store::SpecStoreData;
use crate::specs_response::spec_types::{ConditionOperator, ConditionType};
use crate::user::StatsigUserInternal;
use crate::{ClientInitResponseOptions, StatsigErr, StatsigUser};

#[doc(hidden)]
pub type GateEvaluationResult = SnapshotGateEvaluation;
#[doc(hidden)]
pub type ConfigEvaluationResult = SnapshotConfigEvaluation;
#[doc(hidden)]
pub type InitializeEvaluationResult = SnapshotInitializeResult;
#[doc(hidden)]
pub type LiveEntityNames = SnapshotLiveEntityNames;

/// One fully SDK-owned evaluation operation against one authenticated request scope.
#[doc(hidden)]
pub enum EvaluationOperation<'operation> {
    Gate(&'operation str),
    Segment(&'operation str),
    GateBatchStreaming {
        names: Vec<String>,
        consume: &'operation mut (dyn FnMut(String, &GateEvaluationResult) + Send),
    },
    Config {
        name: &'operation str,
    },
    Layer(&'operation str),
    Initialize {
        options: &'operation ClientInitResponseOptions,
        live_overlay: bool,
    },
}

/// Typed endpoint results without exposing SDK snapshots, sessions, leases, or prepared entities.
#[doc(hidden)]
pub enum EvaluationResult {
    Gate(GateEvaluationResult),
    Segment(GateEvaluationResult),
    GateBatchComplete,
    ConfigMissing,
    Config(ConfigEvaluationResult),
    LayerMissing,
    Layer(Option<LayerEvaluation>),
    Initialize {
        response: Box<InitializeEvaluationResult>,
        metadata: EvaluationMetadata,
    },
}

enum EvaluationSnapshotOwner {
    Engine(Arc<EvaluationEngine>),
    #[cfg(test)]
    Statsig(Arc<Statsig>),
}

struct PinnedScopedEvaluation {
    owner: EvaluationSnapshotOwner,
    data: Arc<SpecStoreData>,
    id_lists_initialized: bool,
    allow_id_lists: bool,
}

impl PinnedScopedEvaluation {
    #[cfg(test)]
    fn from_statsig(statsig: Arc<Statsig>) -> Self {
        let data = statsig.snapshot_evaluation_data();
        Self {
            owner: EvaluationSnapshotOwner::Statsig(statsig),
            data,
            id_lists_initialized: true,
            allow_id_lists: true,
        }
    }

    fn from_engine(engine: Arc<EvaluationEngine>, allow_id_lists: bool) -> Self {
        let id_lists_initialized = !allow_id_lists || engine.id_lists_initialized();
        let mut data = engine.snapshot_evaluation_data();
        if !allow_id_lists && !data.id_lists.is_empty() {
            let mut restricted = data.as_ref().clone();
            restricted.id_lists = Arc::default();
            data = Arc::new(restricted);
        }
        Self {
            owner: EvaluationSnapshotOwner::Engine(engine),
            data,
            id_lists_initialized,
            allow_id_lists,
        }
    }

    fn with_session<T>(&self, callback: impl FnOnce(&SnapshotEvaluationSession<'_>) -> T) -> T {
        let session = match &self.owner {
            EvaluationSnapshotOwner::Engine(engine) => {
                engine.snapshot_evaluation_session(Arc::clone(&self.data))
            }
            #[cfg(test)]
            EvaluationSnapshotOwner::Statsig(statsig) => {
                statsig.snapshot_evaluation_session_with_data(Arc::clone(&self.data))
            }
        };
        callback(&session)
    }
}

/// Response metadata for the single SDK snapshot pinned to an evaluation request.
#[doc(hidden)]
pub struct EvaluationMetadata {
    pub lcut: u64,
    pub auto_capture_settings_hash: u64,
    pub auto_capture_settings_value: Option<Arc<Value>>,
}

/// An authenticated request pinned to one immutable configuration snapshot.
///
/// Hosts can inspect generic snapshot metadata before applying their own request policy without
/// exposing SDK instance, configuration, or cache lifecycle.
pub struct EvaluationRequest {
    request: ScopedEvaluationRequest,
    tenant_key: Arc<str>,
    id_list_membership_service: Option<Arc<ScopedIdListMembershipService>>,
}

impl EvaluationRequest {
    pub(crate) fn new(request: ScopedEvaluationRequest, tenant_key: Arc<str>) -> Self {
        Self {
            request,
            tenant_key,
            id_list_membership_service: None,
        }
    }

    pub(crate) fn with_id_list_membership_service(
        mut self,
        service: Option<Arc<ScopedIdListMembershipService>>,
    ) -> Self {
        self.id_list_membership_service = service;
        self
    }

    pub fn metadata(&self) -> EvaluationMetadata {
        self.request.metadata()
    }

    /// Reports whether the pinned snapshot contains a config eligible for this request's app.
    pub fn has_config(&self, config_name: &str) -> bool {
        self.request.has_config(config_name)
    }

    /// Reports whether an operation can reach ID-list conditions in the pinned snapshot.
    pub fn requires_id_lists(&self, operation: &EvaluationOperation<'_>) -> bool {
        self.request.operation_references_id_lists(operation)
    }

    pub fn references_any_condition_field(&self, fields: &HashSet<String>) -> bool {
        self.request.references_any_condition_field(fields)
    }

    pub async fn evaluate(
        mut self,
        operation: EvaluationOperation<'_>,
    ) -> Result<EvaluationResult, StatsigErr> {
        let requires_id_lists = self.request.operation_references_id_lists(&operation);
        if !self.request.pinned.allow_id_lists && requires_id_lists {
            return Err(StatsigErr::InvalidOperation(
                "ID-list access is not authorized for this evaluation".to_string(),
            ));
        }
        if self.request.pinned.allow_id_lists && requires_id_lists {
            if let Some(service) = self.id_list_membership_service.as_ref() {
                self.request
                    .initialize_id_list_memberships(service, self.tenant_key.as_ref())
                    .await;
            } else if !self.request.pinned.id_lists_initialized {
                self.request.initialize_id_lists().await?;
            }
        }
        self.request.evaluate_operation(operation)
    }
}

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
enum EvaluationSpecKind {
    Gate,
    DynamicConfig,
    Layer,
}

/// Owns one evaluation engine, one pinned snapshot, and one authenticated request user.
///
/// Snapshot selection, target-app filtering, entity preparation, and evaluation remain inside
/// the SDK. Keeping this value across request admission and evaluation preserves snapshot identity.
#[doc(hidden)]
pub(crate) struct ScopedEvaluationRequest {
    pinned: PinnedScopedEvaluation,
    user: StatsigUser,
    target_app_id: Option<String>,
}

impl ScopedEvaluationRequest {
    /// Preserves ordinary SDK-context parity coverage without exposing a second production path.
    #[cfg(test)]
    pub(crate) fn from_statsig(
        statsig: Arc<Statsig>,
        user: StatsigUser,
        target_app_id: Option<String>,
    ) -> Self {
        Self {
            pinned: PinnedScopedEvaluation::from_statsig(statsig),
            user,
            target_app_id,
        }
    }

    /// Starts a request from a lightweight, configuration-only evaluation engine.
    pub(crate) fn from_engine(
        engine: Arc<EvaluationEngine>,
        user: StatsigUser,
        target_app_id: Option<String>,
    ) -> Self {
        Self::from_engine_with_id_list_access(engine, user, target_app_id, true)
    }

    pub(crate) fn from_engine_with_id_list_access(
        engine: Arc<EvaluationEngine>,
        user: StatsigUser,
        target_app_id: Option<String>,
        allow_id_lists: bool,
    ) -> Self {
        Self {
            pinned: PinnedScopedEvaluation::from_engine(engine, allow_id_lists),
            user,
            target_app_id,
        }
    }

    fn metadata(&self) -> EvaluationMetadata {
        EvaluationMetadata {
            lcut: self.pinned.data.lcut(),
            auto_capture_settings_hash: self.pinned.data.auto_capture_settings_hash,
            auto_capture_settings_value: self.pinned.data.auto_capture_settings_value.clone(),
        }
    }

    fn references_any_condition_field(&self, fields: &HashSet<String>) -> bool {
        self.pinned
            .with_session(|session| session.references_any_condition_field(fields))
    }

    async fn initialize_id_list_memberships(
        &mut self,
        service: &Arc<ScopedIdListMembershipService>,
        tenant_key: &str,
    ) {
        let user = StatsigUserInternal::new(&self.user, None);
        let hashing = HashUtil::new();
        let mapping = self
            .pinned
            .data
            .id_list_lookup_conditions()
            .iter()
            .filter_map(|condition| {
                let unit = user
                    .get_unit_id(&condition.id_type)
                    .and_then(|value| value.string_value())?;
                let lookup = hashing.sha256(unit).chars().take(8).collect::<String>();
                Some((condition.name.clone(), lookup))
            })
            .collect::<HashMap<_, _>>();
        let memberships = service.resolve(tenant_key, mapping).await;
        let id_lists = materialize_id_list_memberships(memberships.as_ref());
        let mut pinned = self.pinned.data.as_ref().clone();
        pinned.id_lists = Arc::new(id_lists);
        self.pinned.data = Arc::new(pinned);
        self.pinned.id_lists_initialized = true;
    }

    async fn initialize_id_lists(&mut self) -> Result<(), StatsigErr> {
        if !self.pinned.allow_id_lists {
            return Err(StatsigErr::InvalidOperation(
                "ID-list access is not authorized for this evaluation".to_string(),
            ));
        }
        #[cfg(not(test))]
        let EvaluationSnapshotOwner::Engine(engine) = &self.pinned.owner;
        #[cfg(test)]
        let engine = match &self.pinned.owner {
            EvaluationSnapshotOwner::Engine(engine) => engine,
            EvaluationSnapshotOwner::Statsig(_) => return Ok(()),
        };
        engine.initialize_id_lists().await?;
        if !self.pinned.id_lists_initialized {
            let mut pinned = self.pinned.data.as_ref().clone();
            pinned.id_lists = Arc::clone(&engine.snapshot_evaluation_data().id_lists);
            self.pinned.data = Arc::new(pinned);
            self.pinned.id_lists_initialized = true;
        }
        Ok(())
    }

    fn operation_references_id_lists(&self, operation: &EvaluationOperation<'_>) -> bool {
        if !self.pinned.data.has_id_list_conditions {
            return false;
        }

        let mut visited = HashSet::new();
        match operation {
            EvaluationOperation::Gate(name) => {
                self.spec_references_id_lists(EvaluationSpecKind::Gate, name, &mut visited, false)
            }
            EvaluationOperation::Segment(name) => {
                self.spec_references_id_lists(EvaluationSpecKind::Gate, name, &mut visited, true)
            }
            EvaluationOperation::GateBatchStreaming { names, .. } => names.iter().any(|name| {
                self.spec_references_id_lists(EvaluationSpecKind::Gate, name, &mut visited, false)
            }),
            EvaluationOperation::Config { name } => self.spec_references_id_lists(
                EvaluationSpecKind::DynamicConfig,
                name,
                &mut visited,
                false,
            ),
            EvaluationOperation::Layer(name) => {
                self.spec_references_id_lists(EvaluationSpecKind::Layer, name, &mut visited, false)
            }
            EvaluationOperation::Initialize {
                options,
                live_overlay: true,
            } => self.live_overlay_references_id_lists(options, &mut visited),
            EvaluationOperation::Initialize { .. } => true,
        }
    }

    fn live_overlay_references_id_lists(
        &self,
        options: &ClientInitResponseOptions,
        visited: &mut HashSet<(EvaluationSpecKind, String)>,
    ) -> bool {
        let snapshot = self.pinned.data.snapshot.as_ref();
        if snapshot
            .session_replay_info
            .as_ref()
            .and_then(|info| info.targeting_gate.as_deref())
            .is_some_and(|name| {
                self.spec_references_id_lists(EvaluationSpecKind::Gate, name, visited, true)
            })
        {
            return true;
        }

        if !self
            .pinned
            .with_session(|session| session.has_live_overlay_entities_for_target_app(None))
        {
            return false;
        }

        if self.target_app_id.is_some() && options.client_sdk_key.is_none() {
            return true;
        }

        [
            (EvaluationSpecKind::Gate, &snapshot.feature_gates),
            (EvaluationSpecKind::DynamicConfig, &snapshot.dynamic_configs),
            (EvaluationSpecKind::Layer, &snapshot.layer_configs),
        ]
        .into_iter()
        .any(|(kind, specs)| {
            specs.iter().any(|(name, spec)| {
                spec.session_update_mode() == Some("live")
                    && ((kind == EvaluationSpecKind::DynamicConfig
                        && self.live_cmab_references_id_lists(name.as_str(), visited))
                        || (!matches!(spec.view().entity().as_str(), "segment" | "holdout")
                            && self.spec_references_id_lists(kind, name.as_str(), visited, false)))
            })
        })
    }

    fn live_cmab_references_id_lists(
        &self,
        name: &str,
        visited: &mut HashSet<(EvaluationSpecKind, String)>,
    ) -> bool {
        let snapshot = self.pinned.data.snapshot.as_ref();
        let Some(cmab) = snapshot
            .cmab_configs
            .as_ref()
            .and_then(|configs| configs.get(name))
        else {
            return false;
        };

        if self.target_app_id.as_ref().is_some_and(|target_app| {
            cmab.target_app_ids.as_ref().is_none_or(|target_apps| {
                target_apps
                    .iter()
                    .all(|candidate| candidate.as_str() != target_app)
            })
        }) {
            return false;
        }

        cmab.targeting_gate_name.as_ref().is_some_and(|target| {
            self.spec_references_id_lists(EvaluationSpecKind::Gate, target.as_str(), visited, true)
        }) || self.override_mappings_reference_id_lists(
            EvaluationSpecKind::DynamicConfig,
            name,
            visited,
        )
    }

    fn spec_references_id_lists(
        &self,
        kind: EvaluationSpecKind,
        name: &str,
        visited: &mut HashSet<(EvaluationSpecKind, String)>,
        nested: bool,
    ) -> bool {
        let key = (kind, name.to_string());
        if !visited.insert(key.clone()) {
            return true;
        }
        let requires_id_lists = self.spec_references_id_lists_inner(kind, name, visited, nested);
        visited.remove(&key);
        requires_id_lists
    }

    fn spec_references_id_lists_inner(
        &self,
        kind: EvaluationSpecKind,
        name: &str,
        visited: &mut HashSet<(EvaluationSpecKind, String)>,
        nested: bool,
    ) -> bool {
        let snapshot = self.pinned.data.snapshot.as_ref();
        let interned_name = InternedString::from_str_ref(name);
        let pointer = match kind {
            EvaluationSpecKind::Gate => snapshot.feature_gates.get(&interned_name),
            EvaluationSpecKind::DynamicConfig => snapshot.dynamic_configs.get(&interned_name),
            EvaluationSpecKind::Layer => snapshot.layer_configs.get(&interned_name),
        };

        let Some(spec) = pointer.map(|pointer| pointer.view()) else {
            if kind == EvaluationSpecKind::DynamicConfig {
                if let Some(cmab) = snapshot
                    .cmab_configs
                    .as_ref()
                    .and_then(|configs| configs.get(name))
                {
                    if !nested
                        && self.target_app_id.as_ref().is_some_and(|target_app| {
                            cmab.target_app_ids.as_ref().is_none_or(|target_apps| {
                                target_apps
                                    .iter()
                                    .all(|candidate| candidate.as_str() != target_app)
                            })
                        })
                    {
                        return false;
                    }
                    let targeting_gate_requires_lists =
                        cmab.targeting_gate_name.as_ref().is_some_and(|target| {
                            self.spec_references_id_lists(
                                EvaluationSpecKind::Gate,
                                target.as_str(),
                                visited,
                                true,
                            )
                        });
                    return targeting_gate_requires_lists
                        || self.override_mappings_reference_id_lists(kind, name, visited);
                }
            }
            return nested;
        };

        if !nested
            && self
                .target_app_id
                .as_ref()
                .is_some_and(|target_app| spec.target_app_ids_contains(target_app) != Some(true))
        {
            return false;
        }

        if self.spec_rules_reference_id_lists(spec, visited) {
            return true;
        }

        if kind == EvaluationSpecKind::DynamicConfig
            && snapshot
                .cmab_configs
                .as_ref()
                .and_then(|configs| configs.get(name))
                .and_then(|cmab| cmab.targeting_gate_name.as_ref())
                .is_some_and(|target| {
                    self.spec_references_id_lists(
                        EvaluationSpecKind::Gate,
                        target.as_str(),
                        visited,
                        true,
                    )
                })
        {
            return true;
        }

        self.override_mappings_reference_id_lists(kind, name, visited)
    }

    fn override_mappings_reference_id_lists(
        &self,
        kind: EvaluationSpecKind,
        name: &str,
        visited: &mut HashSet<(EvaluationSpecKind, String)>,
    ) -> bool {
        let snapshot = self.pinned.data.snapshot.as_ref();
        let Some(mappings) = snapshot
            .overrides
            .as_ref()
            .and_then(|overrides| overrides.get(name))
        else {
            return false;
        };
        let Some(override_rules) = snapshot.override_rules.as_ref() else {
            return true;
        };
        mappings.iter().any(|mapping| {
            mapping.rules.iter().any(|override_rule| {
                override_rules
                    .get(&override_rule.rule_name)
                    .is_none_or(|rule| self.rule_references_id_lists(RuleRef::from(rule), visited))
            }) || self.spec_references_id_lists(
                kind,
                mapping.new_config_name.as_str(),
                visited,
                true,
            )
        })
    }

    fn spec_rules_reference_id_lists(
        &self,
        spec: SpecView<'_>,
        visited: &mut HashSet<(EvaluationSpecKind, String)>,
    ) -> bool {
        (0..spec.rules_len()).any(|index| self.rule_references_id_lists(spec.rule(index), visited))
    }

    fn rule_references_id_lists(
        &self,
        rule: RuleRef<'_>,
        visited: &mut HashSet<(EvaluationSpecKind, String)>,
    ) -> bool {
        let snapshot = self.pinned.data.snapshot.as_ref();
        for index in 0..rule.conditions_len() {
            let Some(condition) = rule.condition_id(index).get_from(&snapshot.condition_map) else {
                return true;
            };
            if matches!(
                condition.compiled_operator,
                ConditionOperator::InSegmentList | ConditionOperator::NotInSegmentList
            ) {
                return true;
            }
            let dependency = match condition.compiled_condition_type {
                ConditionType::PassGate | ConditionType::FailGate => condition
                    .target_value
                    .as_ref()
                    .and_then(|value| value.as_value_ref().string_value())
                    .map(|name| (EvaluationSpecKind::Gate, name)),
                ConditionType::ExperimentGroup => condition
                    .field
                    .as_ref()
                    .map(|field| (EvaluationSpecKind::DynamicConfig, field.value.as_str())),
                _ => continue,
            };
            let Some((kind, name)) = dependency else {
                return true;
            };
            if self.spec_references_id_lists(kind, name, visited, true) {
                return true;
            }
        }

        rule.config_delegate().is_some_and(|delegate| {
            self.spec_references_id_lists(
                EvaluationSpecKind::DynamicConfig,
                delegate.as_str(),
                visited,
                true,
            )
        })
    }

    fn has_config(&self, config_name: &str) -> bool {
        self.pinned
            .with_session(|session| session.has_config(config_name, self.target_app_id.as_deref()))
    }

    fn has_layer(&self, layer_name: &str) -> bool {
        self.pinned
            .with_session(|session| session.has_layer(layer_name, self.target_app_id.as_deref()))
    }

    fn evaluate_gate(&self, gate_name: &str) -> Result<SnapshotGateEvaluation, StatsigErr> {
        self.pinned.with_session(|session| {
            session.evaluate_gate(&self.user, self.target_app_id.as_deref(), gate_name)
        })
    }

    fn evaluate_segment(&self, segment_name: &str) -> Result<SnapshotGateEvaluation, StatsigErr> {
        self.pinned.with_session(|session| {
            session.evaluate_segment(&self.user, self.target_app_id.as_deref(), segment_name)
        })
    }

    fn evaluate_gates_borrowed<Name: AsRef<str>>(
        &self,
        gate_names: impl IntoIterator<Item = Name>,
        consume: impl FnMut(Name, &SnapshotGateEvaluation) -> Result<(), StatsigErr>,
    ) -> Result<(), StatsigErr> {
        self.pinned.with_session(|session| {
            session.evaluate_gates_borrowed(
                &self.user,
                self.target_app_id.as_deref(),
                gate_names,
                consume,
            )
        })
    }

    fn evaluate_config(&self, config_name: &str) -> Result<SnapshotConfigEvaluation, StatsigErr> {
        self.pinned.with_session(|session| {
            session.evaluate_config(&self.user, self.target_app_id.as_deref(), config_name)
        })
    }

    fn evaluate_layer(&self, layer_name: &str) -> Result<Option<LayerEvaluation>, StatsigErr> {
        self.pinned.with_session(|session| {
            session.evaluate_layer(&self.user, self.target_app_id.as_deref(), layer_name)
        })
    }

    fn generate_client_initialize_response(
        &self,
        options: &ClientInitResponseOptions,
        mode: SnapshotInitializeMode,
    ) -> Result<SnapshotInitializeResult, StatsigErr> {
        self.pinned.with_session(|session| {
            session.generate_client_initialize_response(
                &self.user,
                self.target_app_id.as_deref(),
                options,
                mode,
            )
        })
    }

    pub(crate) fn evaluate_operation(
        self,
        operation: EvaluationOperation<'_>,
    ) -> Result<EvaluationResult, StatsigErr> {
        match &operation {
            EvaluationOperation::Config { name } => {
                if !self.has_config(name) {
                    return Ok(EvaluationResult::ConfigMissing);
                }
            }
            EvaluationOperation::Layer(name) if !self.has_layer(name) => {
                return Ok(EvaluationResult::LayerMissing);
            }
            _ => {}
        }

        match operation {
            EvaluationOperation::Gate(name) => self.evaluate_gate(name).map(EvaluationResult::Gate),
            EvaluationOperation::Segment(name) => {
                self.evaluate_segment(name).map(EvaluationResult::Segment)
            }
            EvaluationOperation::GateBatchStreaming { names, consume } => {
                self.evaluate_gates_borrowed(names, |name, result| {
                    consume(name, result);
                    Ok(())
                })?;
                Ok(EvaluationResult::GateBatchComplete)
            }
            EvaluationOperation::Config { name } => {
                self.evaluate_config(name).map(EvaluationResult::Config)
            }
            EvaluationOperation::Layer(name) => {
                self.evaluate_layer(name).map(EvaluationResult::Layer)
            }
            EvaluationOperation::Initialize {
                options,
                live_overlay,
            } => {
                let mode = if live_overlay {
                    SnapshotInitializeMode::LiveOverlay
                } else {
                    SnapshotInitializeMode::Full
                };
                let response = self.generate_client_initialize_response(options, mode)?;

                Ok(EvaluationResult::Initialize {
                    response: Box::new(response),
                    metadata: self.metadata(),
                })
            }
        }
    }
}

fn materialize_id_list_memberships(memberships: &HashSet<String>) -> HashMap<String, IdList> {
    let mut lookup_ids: HashMap<&str, Arc<HashSet<String>>> = HashMap::new();

    memberships
        .iter()
        .filter_map(|membership| {
            let (name, lookup) = membership.rsplit_once('|')?;
            let ids = Arc::clone(
                lookup_ids
                    .entry(lookup)
                    .or_insert_with(|| Arc::new(HashSet::from([lookup.to_string()]))),
            );
            let name = name.to_string();

            Some((
                name.clone(),
                IdList {
                    metadata: IdListMetadata {
                        name,
                        url: String::new(),
                        file_id: None,
                        size: 0,
                        creation_time: 0,
                    },
                    ids,
                },
            ))
        })
        .collect()
}

/// Evaluates a complete operation through an already-created SDK instance.
#[cfg(test)]
pub(crate) async fn evaluate_static_operation(
    statsig: Arc<Statsig>,
    user: StatsigUser,
    target_app_id: Option<String>,
    operation: EvaluationOperation<'_>,
) -> Result<EvaluationResult, StatsigErr> {
    ScopedEvaluationRequest::from_statsig(statsig, user, target_app_id)
        .evaluate_operation(operation)
}

#[cfg(test)]
mod tests {
    use serde_json::json;
    use std::collections::{HashMap, HashSet};
    use std::sync::Arc;

    use super::{
        EvaluationOperation, EvaluationRequest, EvaluationResult, ScopedEvaluationRequest,
        evaluate_static_operation, materialize_id_list_memberships,
    };
    use crate::{
        ClientInitResponseOptions, HashAlgorithm, SpecsSource, SpecsUpdate, Statsig, StatsigErr,
        StatsigOptions, StatsigUser, networking::ResponseData,
        scoped_snapshot_registry::EvaluationEngine,
    };

    fn load_snapshot(statsig: &Statsig, specs: &serde_json::Value, received_at: u64) {
        statsig
            .get_context()
            .spec_store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(
                    serde_json::to_vec(specs).expect("fixture should serialize"),
                ),
                source: SpecsSource::Network,
                received_at,
                source_api: Some("scoped-request-transaction-test".to_string()),
                has_updates: None,
            })
            .expect("fixture should load");
    }

    fn fixture_engine(specs: &serde_json::Value) -> Arc<EvaluationEngine> {
        EvaluationEngine::from_fixture(
            serde_json::to_string(specs).expect("fixture should serialize"),
            None,
        )
        .expect("fixture evaluation engine should initialize")
    }

    fn refresh_fixture(engine: &EvaluationEngine, specs: &serde_json::Value, received_at: u64) {
        engine
            .update_fixture_for_test(SpecsUpdate {
                data: ResponseData::from_bytes(
                    serde_json::to_vec(specs).expect("fixture should serialize"),
                ),
                source: SpecsSource::Network,
                received_at,
                source_api: Some("scoped-request-transaction-test".to_string()),
                has_updates: None,
            })
            .expect("fixture snapshot should refresh");
    }

    async fn evaluate_fixture_operation(
        engine: Arc<EvaluationEngine>,
        user: StatsigUser,
        target_app_id: Option<String>,
        operation: EvaluationOperation<'_>,
    ) -> Result<EvaluationResult, StatsigErr> {
        ScopedEvaluationRequest::from_engine(engine, user, target_app_id)
            .evaluate_operation(operation)
    }

    fn experiment_group_specs() -> serde_json::Value {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        let experiment_name = "experiment_group_source";
        let mut experiment = specs["dynamic_configs"]["test_experiment_no_targeting"].clone();
        experiment["salt"] = json!("experiment-group-source-salt");
        experiment["rules"] = json!([{
            "name": "experiment-group-source-treatment",
            "groupName": "Treatment",
            "passPercentage": 100,
            "conditions": ["1828919350"],
            "returnValue": {"variant": "treatment"},
            "id": "experiment-group-source-treatment",
            "salt": "experiment-group-source-treatment",
            "idType": "userID",
            "isExperimentGroup": true
        }]);
        specs["dynamic_configs"][experiment_name] = experiment;

        let mut gate = specs["feature_gates"]["test_public"].clone();
        gate["salt"] = json!("experiment-group-gate-salt");
        gate["rules"][0]["name"] = json!("experiment-group-targeted-rule");
        gate["rules"][0]["id"] = json!("experiment-group-targeted-rule");
        gate["rules"][0]["salt"] = json!("experiment-group-targeted-rule");
        gate["rules"][0]["conditions"] = json!(["experiment_group_condition"]);
        specs["feature_gates"]["gate_targeted_by_experiment_group"] = gate;
        specs["condition_map"]["experiment_group_condition"] = json!({
            "type": "experiment_group",
            "targetValue": ["Treatment"],
            "operator": "any",
            "field": experiment_name,
            "additionalValues": {"experiment_name": experiment_name},
            "idType": "userID"
        });
        specs
    }

    #[test]
    fn scoped_request_can_cross_asynchronous_worker_threads() {
        fn assert_send_sync<T: Send + Sync>() {}

        assert_send_sync::<ScopedEvaluationRequest>();
        assert_send_sync::<EvaluationRequest>();
    }

    #[test]
    fn materialized_memberships_share_identical_lookups_without_mixing_units() {
        let memberships = HashSet::from([
            "employees|abcdefgh".to_string(),
            "testers|abcdefgh".to_string(),
            "nested|list|abcdefgh".to_string(),
            "accounts|12345678".to_string(),
            "malformed-membership".to_string(),
        ]);

        let id_lists = materialize_id_list_memberships(&memberships);

        assert_eq!(id_lists.len(), 4);
        assert!(Arc::ptr_eq(
            &id_lists["employees"].ids,
            &id_lists["testers"].ids
        ));
        assert!(Arc::ptr_eq(
            &id_lists["employees"].ids,
            &id_lists["nested|list"].ids
        ));
        assert!(!Arc::ptr_eq(
            &id_lists["employees"].ids,
            &id_lists["accounts"].ids
        ));
        assert!(id_lists["employees"].ids.contains("abcdefgh"));
        assert!(!id_lists["employees"].ids.contains("12345678"));
        assert!(id_lists["accounts"].ids.contains("12345678"));
        assert!(!id_lists["accounts"].ids.contains("abcdefgh"));
    }

    #[tokio::test]
    async fn ordinary_sdk_operations_preserve_experiment_group_evaluation() {
        let statsig = Arc::new(Statsig::new(
            "secret-ordinary-experiment-context",
            Some(Arc::new(StatsigOptions {
                disable_all_logging: Some(true),
                disable_network: Some(true),
                ..StatsigOptions::default()
            })),
        ));
        load_snapshot(statsig.as_ref(), &experiment_group_specs(), 1);
        let user = StatsigUser::with_user_id("9");

        let gate = evaluate_static_operation(
            Arc::clone(&statsig),
            user.clone(),
            None,
            EvaluationOperation::Gate("gate_targeted_by_experiment_group"),
        )
        .await
        .expect("ordinary SDK gate should evaluate");
        let EvaluationResult::Gate(gate) = gate else {
            panic!("gate operation should return a gate evaluation");
        };
        assert!(gate.evaluation.expect("gate should exist").value);
        assert_eq!(
            gate.rule_id.expect("gate should return its rule").as_str(),
            "experiment-group-targeted-rule"
        );

        let options = ClientInitResponseOptions {
            hash_algorithm: Some(HashAlgorithm::None),
            client_sdk_key: Some("client-test-key".to_string()),
            ..Default::default()
        };
        let response = evaluate_static_operation(
            statsig,
            user,
            None,
            EvaluationOperation::Initialize {
                options: &options,
                live_overlay: false,
            },
        )
        .await
        .expect("ordinary SDK initialize should evaluate");
        let EvaluationResult::Initialize { response, .. } = response else {
            panic!("initialize operation should return a full response");
        };
        assert!(
            response.response.feature_gates[&crate::interned_string::InternedString::from_str_ref(
                "gate_targeted_by_experiment_group"
            )]
                .value
        );
    }

    #[tokio::test]
    async fn ordinary_sdk_operations_preserve_environment_and_local_override_policy() {
        let specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/check_gate_perf_dcs.json"))
                .expect("environment fixture should parse");
        let statsig = Arc::new(Statsig::new(
            "secret-ordinary-environment-context",
            Some(Arc::new(StatsigOptions {
                environment: Some("development".to_string()),
                disable_all_logging: Some(true),
                disable_network: Some(true),
                ..StatsigOptions::default()
            })),
        ));
        load_snapshot(statsig.as_ref(), &specs, 1);
        let user = StatsigUser::with_user_id("9");

        let initial = evaluate_static_operation(
            Arc::clone(&statsig),
            user.clone(),
            None,
            EvaluationOperation::Gate("public_dev_only"),
        )
        .await
        .expect("ordinary environment gate should evaluate");
        assert!(matches!(
            initial,
            EvaluationResult::Gate(gate)
                if gate.evaluation.as_ref().is_some_and(|evaluation| evaluation.value)
        ));

        statsig.override_gate("public_dev_only", false, None);
        for include_local_overrides in [None, Some(false), Some(true)] {
            let options = ClientInitResponseOptions {
                hash_algorithm: Some(HashAlgorithm::None),
                include_local_overrides,
                remove_default_value_gates: Some(false),
                ..Default::default()
            };
            let expected = statsig.get_client_init_response_with_options(&user, &options);
            let response = statsig
                .snapshot_evaluation_session()
                .generate_client_init_response(&user, None, &options)
                .expect("ordinary SDK initialize should evaluate");
            let name = crate::interned_string::InternedString::from_str_ref("public_dev_only");
            assert_eq!(
                response.feature_gates[&name].value,
                expected.feature_gates[&name].value
            );
        }

        let overridden = evaluate_static_operation(
            statsig,
            user,
            None,
            EvaluationOperation::Gate("public_dev_only"),
        )
        .await
        .expect("ordinary overridden gate should evaluate");
        assert!(matches!(
            overridden,
            EvaluationResult::Gate(gate)
                if gate.evaluation.as_ref().is_some_and(|evaluation| !evaluation.value)
        ));
    }

    #[tokio::test]
    async fn scoped_request_keeps_one_snapshot_across_asynchronous_transport_and_refresh() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] = json!(["first-app"]);
        specs["layer_configs"]["layer_with_many_params"]["targetAppIDs"] = json!(["first-app"]);

        let engine = fixture_engine(&specs);
        let request = ScopedEvaluationRequest::from_engine(
            Arc::clone(&engine),
            StatsigUser::with_user_id("scoped-request-user"),
            Some("first-app".to_string()),
        );
        let initial_lcut = request.metadata().lcut;
        assert!(request.has_config("test_custom_config"));
        assert!(request.has_layer("layer_with_many_params"));

        specs["time"] = json!(initial_lcut + 1);
        specs["checksum"] = json!("updated-scoped-request-snapshot");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] = json!(["second-app"]);
        specs["layer_configs"]["layer_with_many_params"]["targetAppIDs"] = json!(["second-app"]);
        refresh_fixture(&engine, &specs, 2);
        tokio::task::yield_now().await;

        assert_eq!(request.metadata().lcut, initial_lcut);
        assert!(request.has_config("test_custom_config"));
        assert!(request.has_layer("layer_with_many_params"));
        assert!(
            request
                .evaluate_config("test_custom_config")
                .expect("pinned config should evaluate")
                .evaluation
                .is_some()
        );
        assert!(
            request
                .evaluate_layer("layer_with_many_params")
                .expect("pinned layer should evaluate")
                .is_some()
        );

        let refreshed = ScopedEvaluationRequest::from_engine(
            engine,
            StatsigUser::with_user_id("scoped-request-user"),
            Some("first-app".to_string()),
        );
        assert_eq!(refreshed.metadata().lcut, initial_lcut + 1);
        assert!(!refreshed.has_config("test_custom_config"));
        assert!(!refreshed.has_layer("layer_with_many_params"));
    }

    #[tokio::test]
    async fn missing_configs_return_missing_results() {
        let specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        let engine = fixture_engine(&specs);

        let result = evaluate_fixture_operation(
            engine,
            StatsigUser::with_user_id("missing-config-user"),
            None,
            EvaluationOperation::Config {
                name: "missing-config",
            },
        )
        .await
        .expect("missing config is a successful operation outcome");

        assert!(matches!(result, EvaluationResult::ConfigMissing));
    }

    #[tokio::test]
    async fn config_presence_uses_the_pinned_snapshot_and_target_app() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] = json!(["first-app"]);
        let engine = fixture_engine(&specs);
        let request = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine(
                Arc::clone(&engine),
                StatsigUser::with_user_id("recognized-config-user"),
                Some("first-app".to_string()),
            ),
            Arc::from("config-presence-tenant"),
        );
        assert!(request.has_config("test_custom_config"));
        assert!(!request.has_config("missing-config"));

        specs["time"] = json!(request.metadata().lcut + 1);
        specs["checksum"] = json!("updated-config-presence-snapshot");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] = json!(["second-app"]);
        refresh_fixture(engine.as_ref(), &specs, 2);

        assert!(request.has_config("test_custom_config"));
        let refreshed = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine(
                engine,
                StatsigUser::with_user_id("recognized-config-user"),
                Some("first-app".to_string()),
            ),
            Arc::from("config-presence-tenant"),
        );
        assert!(!refreshed.has_config("test_custom_config"));
    }

    #[test]
    fn id_list_requirements_remain_visible_after_initialization() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["condition_map"]["capability-id-list"] = json!({
            "type": "unit_id",
            "targetValue": "authorized_members",
            "operator": "in_segment_list",
            "idType": "userID"
        });
        let mut list_gate = specs["feature_gates"]["test_small_pass_gate"].clone();
        list_gate["rules"][0]["conditions"] = json!(["capability-id-list"]);
        list_gate["targetAppIDs"] = json!(["authorized-app"]);
        specs["feature_gates"]["list_backed_gate"] = list_gate.clone();
        list_gate["rules"] = json!([]);
        specs["feature_gates"]["unrelated_gate"] = list_gate;

        let engine = fixture_engine(&specs);
        let empty_snapshot = engine.snapshot_evaluation_data();
        let unmaterialized = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                Arc::clone(&engine),
                StatsigUser::with_user_id("unauthorized-member"),
                Some("authorized-app".to_string()),
                false,
            ),
            Arc::from("capability-tenant"),
        );
        assert!(Arc::ptr_eq(
            &unmaterialized.request.pinned.data,
            &empty_snapshot
        ));
        assert!(!unmaterialized.request.pinned.allow_id_lists);
        assert!(unmaterialized.requires_id_lists(&EvaluationOperation::Gate("list_backed_gate")));

        engine.seed_id_lists_for_test(&HashMap::from([(
            "authorized_members".to_string(),
            HashSet::from(["authorized-member".to_string()]),
        )]));
        let prepared = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine(
                Arc::clone(&engine),
                StatsigUser::with_user_id("authorized-member"),
                Some("authorized-app".to_string()),
            ),
            Arc::from("capability-tenant"),
        );
        assert!(prepared.request.pinned.id_lists_initialized);
        assert!(
            prepared
                .request
                .pinned
                .data
                .id_lists
                .contains_key("authorized_members")
        );
        assert!(prepared.requires_id_lists(&EvaluationOperation::Gate("list_backed_gate")));
        assert!(!prepared.requires_id_lists(&EvaluationOperation::Gate("unrelated_gate")));
        assert!(!prepared.requires_id_lists(&EvaluationOperation::Gate("missing_gate")));

        let restricted = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                Arc::clone(&engine),
                StatsigUser::with_user_id("unauthorized-member"),
                Some("authorized-app".to_string()),
                false,
            ),
            Arc::from("capability-tenant"),
        );
        assert!(!restricted.request.pinned.allow_id_lists);
        assert!(restricted.request.pinned.id_lists_initialized);
        assert!(restricted.request.pinned.data.id_lists.is_empty());
        assert!(restricted.requires_id_lists(&EvaluationOperation::Gate("list_backed_gate")));
        assert!(!restricted.requires_id_lists(&EvaluationOperation::Gate("unrelated_gate")));

        let wrong_app = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine(
                engine,
                StatsigUser::with_user_id("authorized-member"),
                Some("another-app".to_string()),
            ),
            Arc::from("capability-tenant"),
        );
        assert!(!wrong_app.requires_id_lists(&EvaluationOperation::Gate("list_backed_gate")));
    }

    #[tokio::test]
    #[serial_test::serial]
    async fn list_free_live_overlay_does_not_require_unrelated_id_list_credentials() {
        let specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        let engine = fixture_engine(&specs);
        let options = ClientInitResponseOptions {
            client_sdk_key: Some("client-live-overlay".to_string()),
            ..ClientInitResponseOptions::default()
        };
        let request = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                Arc::clone(&engine),
                StatsigUser::with_user_id("live-overlay-user"),
                None,
                false,
            ),
            Arc::from("live-overlay-tenant"),
        );
        let operation = EvaluationOperation::Initialize {
            options: &options,
            live_overlay: true,
        };

        assert!(!request.requires_id_lists(&operation));
        let response = request
            .evaluate(operation)
            .await
            .expect("a live overlay without live entities must not require list credentials");
        let EvaluationResult::Initialize { response, .. } = response else {
            panic!("live overlay should return an initialize response");
        };
        assert!(response.response.feature_gates.is_empty());
        assert!(response.response.dynamic_configs.is_empty());
        assert!(response.response.layer_configs.is_empty());
        assert!(response.live_entity_names.is_empty());

        let full_request = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                engine,
                StatsigUser::with_user_id("live-overlay-user"),
                None,
                false,
            ),
            Arc::from("live-overlay-tenant"),
        );
        let full_operation = EvaluationOperation::Initialize {
            options: &options,
            live_overlay: false,
        };
        assert!(full_request.requires_id_lists(&full_operation));
        assert!(matches!(
            full_request.evaluate(full_operation).await,
            Err(StatsigErr::InvalidOperation(_))
        ));
    }

    #[tokio::test]
    #[serial_test::serial]
    async fn session_replay_targeting_requires_id_lists_without_live_entities() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["session_replay_info"]["targeting_gate"] = json!("segment:company_id_list");
        specs["session_replay_info"]["recording_blocked"] = json!(true);
        specs["feature_gates"]["segment:company_id_list"]["targetAppIDs"] =
            json!(["different-app"]);
        let options = ClientInitResponseOptions {
            client_sdk_key: Some("client-live-overlay".to_string()),
            ..ClientInitResponseOptions::default()
        };
        let request = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                fixture_engine(&specs),
                StatsigUser::with_user_id("live-overlay-user"),
                Some("replay-app".to_string()),
                false,
            ),
            Arc::from("live-overlay-tenant"),
        );
        let operation = EvaluationOperation::Initialize {
            options: &options,
            live_overlay: true,
        };

        assert!(request.requires_id_lists(&operation));
        assert!(matches!(
            request.evaluate(operation).await,
            Err(StatsigErr::InvalidOperation(_))
        ));
    }

    #[test]
    #[serial_test::serial]
    fn live_overlay_id_list_reachability_filters_live_roots_and_target_apps() {
        let options = ClientInitResponseOptions {
            client_sdk_key: Some("client-live-overlay".to_string()),
            ..ClientInitResponseOptions::default()
        };

        for (collection, name) in [
            ("feature_gates", "test_small_pass_gate"),
            ("dynamic_configs", "test_custom_config"),
            ("layer_configs", "layer_with_many_params"),
        ] {
            let mut specs: serde_json::Value =
                serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                    .expect("fixture should parse");
            specs[collection][name]["sessionUpdateMode"] = json!("live");
            specs[collection][name]["targetAppIDs"] = json!(["allowed-app"]);
            specs[collection][name]["rules"][0]["conditions"] = json!(["3614985732"]);
            let engine = fixture_engine(&specs);

            for (target_app, requires_lists) in [("allowed-app", true), ("other-app", false)] {
                let request = EvaluationRequest::new(
                    ScopedEvaluationRequest::from_engine_with_id_list_access(
                        Arc::clone(&engine),
                        StatsigUser::with_user_id("live-overlay-user"),
                        Some(target_app.to_string()),
                        false,
                    ),
                    Arc::from("live-overlay-tenant"),
                );
                assert_eq!(
                    request.requires_id_lists(&EvaluationOperation::Initialize {
                        options: &options,
                        live_overlay: true,
                    }),
                    requires_lists,
                    "{collection} live-root ID-list access should follow its target app",
                );
            }
        }

        for excluded_entity in ["segment", "holdout"] {
            let mut specs: serde_json::Value =
                serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                    .expect("fixture should parse");
            let spec = &mut specs["feature_gates"]["segment:company_id_list"];
            spec["entity"] = json!(excluded_entity);
            spec["sessionUpdateMode"] = json!("live");
            spec["targetAppIDs"] = json!(["allowed-app"]);

            let request = EvaluationRequest::new(
                ScopedEvaluationRequest::from_engine_with_id_list_access(
                    fixture_engine(&specs),
                    StatsigUser::with_user_id("live-overlay-user"),
                    Some("allowed-app".to_string()),
                    false,
                ),
                Arc::from("live-overlay-tenant"),
            );
            assert!(
                !request.requires_id_lists(&EvaluationOperation::Initialize {
                    options: &options,
                    live_overlay: true,
                }),
                "a {excluded_entity} cannot be emitted as a top-level live entity",
            );
        }
    }

    #[tokio::test]
    #[serial_test::serial]
    async fn live_overlay_id_list_reachability_preserves_nested_segments_and_cmab_scopes() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["condition_map"]["live-nested-list"] = json!({
            "type": "pass_gate",
            "targetValue": "segment:company_id_list",
            "operator": null,
            "idType": "userID"
        });
        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] = json!("live");
        specs["feature_gates"]["test_small_pass_gate"]["targetAppIDs"] = json!(["allowed-app"]);
        specs["feature_gates"]["test_small_pass_gate"]["rules"][0]["conditions"] =
            json!(["live-nested-list"]);
        specs["feature_gates"]["segment:company_id_list"]["targetAppIDs"] =
            json!(["nested-only-app"]);

        let options = ClientInitResponseOptions {
            client_sdk_key: Some("client-live-overlay".to_string()),
            ..ClientInitResponseOptions::default()
        };
        let nested_request = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                fixture_engine(&specs),
                StatsigUser::with_user_id("live-overlay-user"),
                Some("allowed-app".to_string()),
                false,
            ),
            Arc::from("live-overlay-tenant"),
        );
        let nested_operation = EvaluationOperation::Initialize {
            options: &options,
            live_overlay: true,
        };
        assert!(nested_request.requires_id_lists(&nested_operation));
        assert!(matches!(
            nested_request.evaluate(nested_operation).await,
            Err(StatsigErr::InvalidOperation(_))
        ));

        let no_client_key_options = ClientInitResponseOptions::default();
        let no_client_key_request = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                fixture_engine(&specs),
                StatsigUser::with_user_id("live-overlay-user"),
                Some("different-app".to_string()),
                false,
            ),
            Arc::from("live-overlay-tenant"),
        );
        let no_client_key_operation = EvaluationOperation::Initialize {
            options: &no_client_key_options,
            live_overlay: true,
        };
        assert!(no_client_key_request.requires_id_lists(&no_client_key_operation));
        assert!(matches!(
            no_client_key_request
                .evaluate(no_client_key_operation)
                .await,
            Err(StatsigErr::InvalidOperation(_))
        ));

        specs["feature_gates"]["test_small_pass_gate"]["sessionUpdateMode"] =
            serde_json::Value::Null;
        specs["dynamic_configs"]["test_custom_config"]["sessionUpdateMode"] = json!("live");
        specs["dynamic_configs"]["test_custom_config"]["targetAppIDs"] = json!(["dynamic-app"]);
        specs["dynamic_configs"]["test_custom_config"]["rules"] = json!([]);
        specs["cmab_configs"] = json!({
            "test_custom_config": {
                "salt": "live-overlay-cmab",
                "defaultValue": {},
                "idType": "userID",
                "enabled": true,
                "version": 1,
                "sampleRate": 1.0,
                "higherIsBetter": true,
                "groups": [],
                "targetAppIDs": ["cmab-app"],
                "targetingGateName": "segment:company_id_list"
            }
        });
        let engine = fixture_engine(&specs);

        for (target_app, requires_lists) in [("cmab-app", true), ("other-app", false)] {
            let request = EvaluationRequest::new(
                ScopedEvaluationRequest::from_engine_with_id_list_access(
                    Arc::clone(&engine),
                    StatsigUser::with_user_id("live-overlay-user"),
                    Some(target_app.to_string()),
                    false,
                ),
                Arc::from("live-overlay-tenant"),
            );
            let operation = EvaluationOperation::Initialize {
                options: &options,
                live_overlay: true,
            };
            assert_eq!(
                request.requires_id_lists(&operation),
                requires_lists,
                "same-name live CMAB access must use its own target-app eligibility",
            );
            if requires_lists {
                assert!(matches!(
                    request.evaluate(operation).await,
                    Err(StatsigErr::InvalidOperation(_))
                ));
            }
        }

        for suppressed_entity in ["segment", "holdout"] {
            specs["dynamic_configs"]["test_custom_config"]["entity"] = json!(suppressed_entity);
            let cmab_request = EvaluationRequest::new(
                ScopedEvaluationRequest::from_engine_with_id_list_access(
                    fixture_engine(&specs),
                    StatsigUser::with_user_id("live-overlay-user"),
                    Some("cmab-app".to_string()),
                    false,
                ),
                Arc::from("live-overlay-tenant"),
            );
            assert!(
                cmab_request.requires_id_lists(&EvaluationOperation::Initialize {
                    options: &options,
                    live_overlay: true,
                }),
                "a separately evaluated CMAB remains reachable for a {suppressed_entity} spec",
            );
        }
        specs["dynamic_configs"]["test_custom_config"]["entity"] = json!("dynamic_config");

        specs["cmab_configs"]["test_custom_config"]["targetingGateName"] = serde_json::Value::Null;
        let list_override_rule =
            specs["feature_gates"]["segment:company_id_list"]["rules"][0].clone();
        specs["override_rules"] = json!({"live-cmab-id-list": list_override_rule});
        specs["overrides"] = json!({
            "test_custom_config": [{
                "new_config_name": "mapped_live_cmab",
                "rules": [{"rule_name": "live-cmab-id-list", "start_time": 0}]
            }]
        });
        let mapped_request = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine_with_id_list_access(
                fixture_engine(&specs),
                StatsigUser::with_user_id("live-overlay-user"),
                Some("cmab-app".to_string()),
                false,
            ),
            Arc::from("live-overlay-tenant"),
        );
        let mapped_operation = EvaluationOperation::Initialize {
            options: &options,
            live_overlay: true,
        };
        assert!(mapped_request.requires_id_lists(&mapped_operation));
        assert!(matches!(
            mapped_request.evaluate(mapped_operation).await,
            Err(StatsigErr::InvalidOperation(_))
        ));
    }

    #[test]
    #[serial_test::serial]
    fn id_list_reachability_follows_nested_delegated_and_cmab_override_dependencies() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["condition_map"]["reachable-id-list"] = json!({
            "type": "unit_id",
            "targetValue": "reachable_members",
            "operator": "not_in_segment_list",
            "idType": "userID"
        });
        specs["condition_map"]["nested-reachable-gate"] = json!({
            "type": "pass_gate",
            "targetValue": "list_backed_gate",
            "operator": null,
            "idType": "userID"
        });
        specs["condition_map"]["shared-unrelated-gate"] = json!({
            "type": "pass_gate",
            "targetValue": "unrelated_gate",
            "operator": null,
            "idType": "userID"
        });
        specs["condition_map"]["cyclic-reachable-gate"] = json!({
            "type": "pass_gate",
            "targetValue": "cyclic_gate",
            "operator": null,
            "idType": "userID"
        });

        let template_gate = specs["feature_gates"]["test_small_pass_gate"].clone();
        let mut list_gate = template_gate.clone();
        list_gate["rules"][0]["conditions"] = json!(["reachable-id-list"]);
        specs["feature_gates"]["list_backed_gate"] = list_gate;
        let mut nested_gate = template_gate.clone();
        nested_gate["rules"][0]["conditions"] = json!(["nested-reachable-gate"]);
        specs["feature_gates"]["nested_list_gate"] = nested_gate;
        let mut unrelated_gate = template_gate;
        unrelated_gate["rules"] = json!([]);
        specs["feature_gates"]["unrelated_gate"] = unrelated_gate;
        let mut shared_parent = specs["feature_gates"]["test_small_pass_gate"].clone();
        shared_parent["rules"][0]["conditions"] = json!(["shared-unrelated-gate"]);
        specs["feature_gates"]["left_shared_gate"] = shared_parent.clone();
        specs["feature_gates"]["right_shared_gate"] = shared_parent;
        let mut cyclic_gate = specs["feature_gates"]["test_small_pass_gate"].clone();
        cyclic_gate["rules"][0]["conditions"] = json!(["cyclic-reachable-gate"]);
        specs["feature_gates"]["cyclic_gate"] = cyclic_gate;

        let mut delegated_config = specs["dynamic_configs"]["test_custom_config"].clone();
        delegated_config["rules"][0]["conditions"] = json!(["reachable-id-list"]);
        specs["dynamic_configs"]["list_backed_config"] = delegated_config;
        let mut overlapping_config = specs["dynamic_configs"]["test_custom_config"].clone();
        overlapping_config["rules"] = json!([]);
        specs["dynamic_configs"]["overlapping_cmab"] = overlapping_config;
        let mut delegated_layer = specs["layer_configs"]["layer_with_many_params"].clone();
        delegated_layer["rules"][0]["conditions"] = json!([]);
        delegated_layer["rules"][0]["configDelegate"] = json!("list_backed_config");
        specs["layer_configs"]["delegated_list_layer"] = delegated_layer;

        specs["cmab_configs"] = json!({
            "mapped_cmab": {
                "salt": "mapped-cmab",
                "defaultValue": {},
                "idType": "userID",
                "enabled": true,
                "version": 1,
                "sampleRate": 1.0,
                "higherIsBetter": true,
                "groups": []
            },
            "overlapping_cmab": {
                "salt": "overlapping-cmab",
                "defaultValue": {},
                "idType": "userID",
                "enabled": true,
                "version": 1,
                "sampleRate": 1.0,
                "higherIsBetter": true,
                "groups": [],
                "targetingGateName": "list_backed_gate"
            }
        });
        let override_rule = specs["feature_gates"]["list_backed_gate"]["rules"][0].clone();
        specs["override_rules"] = json!({"reachable-override": override_rule});
        specs["overrides"] = json!({
            "mapped_cmab": [{
                "new_config_name": "list_backed_config",
                "rules": [{"rule_name": "reachable-override", "start_time": 0}]
            }]
        });

        let request = ScopedEvaluationRequest::from_engine(
            fixture_engine(&specs),
            StatsigUser::with_user_id("reachable-user"),
            None,
        );
        assert!(
            !request.operation_references_id_lists(&EvaluationOperation::Gate("unrelated_gate"))
        );
        let mut consume = |_name: String, _evaluation: &super::GateEvaluationResult| {};
        assert!(
            !request.operation_references_id_lists(&EvaluationOperation::GateBatchStreaming {
                names: vec!["unrelated_gate".to_string(), "unrelated_gate".to_string()],
                consume: &mut consume,
            })
        );
        assert!(
            !request.operation_references_id_lists(&EvaluationOperation::GateBatchStreaming {
                names: vec![
                    "left_shared_gate".to_string(),
                    "right_shared_gate".to_string()
                ],
                consume: &mut consume,
            })
        );
        assert!(request.operation_references_id_lists(&EvaluationOperation::Gate("cyclic_gate")));
        assert!(
            request.operation_references_id_lists(&EvaluationOperation::Gate("nested_list_gate"))
        );
        assert!(
            request
                .operation_references_id_lists(&EvaluationOperation::Layer("delegated_list_layer"))
        );
        assert!(
            request.operation_references_id_lists(&EvaluationOperation::Config {
                name: "mapped_cmab",
            })
        );
        assert!(
            request.operation_references_id_lists(&EvaluationOperation::Config {
                name: "overlapping_cmab",
            })
        );
    }

    #[tokio::test]
    async fn gate_batch_preserves_order_and_nested_secondary_exposures() {
        let specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        let engine = fixture_engine(&specs);
        let names = vec![
            "test_nested_gate_condition".to_string(),
            "missing-gate".to_string(),
            "test_nested_gate_condition".to_string(),
        ];
        let original_name_allocation = names[0].as_ptr() as usize;

        let mut streamed_names = Vec::new();
        let mut transferred_name_allocation = None;
        let mut first_exposure_allocation = None;
        let mut consume = |name: String, evaluation: &super::GateEvaluationResult| {
            if streamed_names.is_empty() {
                transferred_name_allocation = Some(name.as_ptr() as usize);
            }
            if name == "missing-gate" {
                assert!(evaluation.evaluation.is_none());
            } else {
                let gate = evaluation
                    .evaluation
                    .as_ref()
                    .expect("nested gate should be recognized");
                assert!(!gate.base.secondary_exposures.is_empty());
                let allocation = gate.base.secondary_exposures.as_ptr() as usize;
                if let Some(previous) = first_exposure_allocation {
                    assert_eq!(allocation, previous);
                } else {
                    first_exposure_allocation = Some(allocation);
                }
            }
            streamed_names.push(name);
        };
        let streamed = evaluate_fixture_operation(
            engine,
            StatsigUser::with_user_id("gate-batch-user"),
            None,
            EvaluationOperation::GateBatchStreaming {
                names,
                consume: &mut consume,
            },
        )
        .await
        .expect("streaming gate batch should evaluate");

        assert!(matches!(streamed, EvaluationResult::GateBatchComplete));
        assert_eq!(
            streamed_names,
            [
                "test_nested_gate_condition",
                "missing-gate",
                "test_nested_gate_condition",
            ]
        );
        assert_eq!(transferred_name_allocation, Some(original_name_allocation));
        assert!(first_exposure_allocation.is_some());
    }

    #[tokio::test]
    async fn prepared_evaluation_pins_metadata_and_id_lists() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["time"] = json!(123);
        specs["condition_map"]["prepared-id-list"] = json!({
            "type": "unit_id",
            "targetValue": "prepared_users",
            "operator": "in_segment_list",
            "idType": "userID"
        });
        let engine = fixture_engine(&specs);
        let prepared = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine(
                Arc::clone(&engine),
                StatsigUser::with_user_id("prepared-initialize-user"),
                None,
            ),
            Arc::from("test-company"),
        );

        assert_eq!(prepared.metadata().lcut, 123);
        assert!(
            prepared.references_any_condition_field(&HashSet::from(["browser_name".to_string()]))
        );

        specs["time"] = json!(124);
        specs["checksum"] = json!("prepared-initialize-refreshed");
        refresh_fixture(&engine, &specs, 2);
        tokio::task::yield_now().await;

        assert_eq!(prepared.metadata().lcut, 123);
        let options = ClientInitResponseOptions::default();
        let result = prepared
            .evaluate(EvaluationOperation::Initialize {
                options: &options,
                live_overlay: false,
            })
            .await
            .expect("prepared initialize should evaluate its pinned snapshot");
        let EvaluationResult::Initialize { response, metadata } = result else {
            panic!("initialize operation should return its evaluated snapshot");
        };
        assert_eq!(metadata.lcut, 123);
        assert_eq!(response.response.time, 123);
    }

    #[tokio::test]
    async fn live_overlay_returns_canonical_checksum_and_pinned_cursor() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["time"] = json!(123);
        let engine = fixture_engine(&specs);
        let user = StatsigUser::with_user_id("live-overlay-user");
        let options = ClientInitResponseOptions {
            client_sdk_key: Some("client-test-key".to_string()),
            ..Default::default()
        };

        let initial = evaluate_fixture_operation(
            Arc::clone(&engine),
            user.clone(),
            None,
            EvaluationOperation::Initialize {
                options: &options,
                live_overlay: true,
            },
        )
        .await
        .expect("initial live overlay should evaluate");
        let EvaluationResult::Initialize { response, metadata } = initial else {
            panic!("initial live overlay must return its evaluated response");
        };
        let checksum = response
            .live_overlay_checksum
            .expect("SDK must produce the canonical live-overlay checksum");
        assert_eq!(metadata.lcut, 123);

        let repeated = evaluate_fixture_operation(
            engine,
            user,
            None,
            EvaluationOperation::Initialize {
                options: &options,
                live_overlay: true,
            },
        )
        .await
        .expect("live overlay should always return its evaluated body");
        let EvaluationResult::Initialize { response, metadata } = repeated else {
            panic!("live overlay must not apply host no-content policy");
        };
        assert_eq!(
            response.live_overlay_checksum.as_deref(),
            Some(checksum.as_str())
        );
        assert_eq!(metadata.lcut, 123);
    }

    #[tokio::test]
    async fn prepared_request_exposes_relevant_snapshot_condition_fields() {
        let mut specs: serde_json::Value =
            serde_json::from_slice(include_bytes!("../tests/data/eval_proj_dcs.json"))
                .expect("fixture should parse");
        specs["time"] = json!(123);
        let engine = fixture_engine(&specs);

        let prepared = EvaluationRequest::new(
            ScopedEvaluationRequest::from_engine(
                engine,
                StatsigUser::with_user_id("derived-initialize-user"),
                None,
            ),
            Arc::from("test-company"),
        );
        assert_eq!(prepared.metadata().lcut, 123);
        assert!(
            prepared.references_any_condition_field(&HashSet::from(["browser_name".to_string()]))
        );
        assert!(!prepared.references_any_condition_field(&HashSet::from([
            "unreferenced-host-field".to_string()
        ])));

        let options = ClientInitResponseOptions::default();
        let result = prepared
            .evaluate(EvaluationOperation::Initialize {
                options: &options,
                live_overlay: false,
            })
            .await
            .expect("generic initialize must return its evaluated snapshot");

        assert!(matches!(result, EvaluationResult::Initialize { .. }));
    }
}
