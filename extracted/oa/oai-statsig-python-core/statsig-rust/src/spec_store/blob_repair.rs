use super::*;
use crate::evaluation::evaluation_data::{InternedStrRef, SpecView};
use crate::specs_adapter::remote_config_value_hydrator::{
    VerifiedRemoteValues, limit_pending_proofs,
};
use crate::specs_response::spec_types::Condition;

/// Only the retained config's own rules may resolve these removed condition IDs.
pub(crate) type RetainedConditions = HashMap<InternedString, ConditionMap>;
pub(crate) type ConditionMap = ahash::HashMap<InternedString, Condition>;

pub(crate) fn resolve_condition<'a>(
    id: InternedStrRef<'_>,
    live: &'a ConditionMap,
    retained: Option<&'a ConditionMap>,
) -> Option<&'a Condition> {
    id.get_from(live)
        .or_else(|| retained.and_then(|conditions| id.get_from(conditions)))
}

/// Aggregated metadata can inspect all conditions without making one entity's
/// retained definition visible to another entity during evaluation.
pub(super) fn effective_conditions<'a>(
    specs: &'a SpecsResponseFull,
    retained: Option<&'a RetainedConditions>,
) -> impl Iterator<Item = &'a Condition> {
    specs
        .condition_map
        .values()
        .chain(retained.into_iter().flat_map(|by_config| {
            by_config
                .values()
                .flat_map(|conditions| conditions.values())
        }))
}

#[derive(Clone)]
pub(super) enum BlobRepair {
    Full(Arc<PartialHydration>),
    Delta(Arc<PartialBlobSnapshot>),
}

impl BlobRepair {
    fn failed_blobs(&self) -> Box<dyn Iterator<Item = (&String, &HydrationFailureReason)> + '_> {
        match self {
            Self::Full(repair) => Box::new(repair.failed_blobs.iter()),
            Self::Delta(repair) => Box::new(
                repair
                    .incomplete
                    .pending
                    .values()
                    .flat_map(|config| &config.failed_blobs),
            ),
        }
    }

    pub(super) fn retained_conditions(&self) -> Option<&RetainedConditions> {
        match self {
            Self::Full(repair) => repair
                .overlay
                .as_ref()
                .map(|s| &s.serving.retained_conditions),
            Self::Delta(repair) => Some(&repair.overlay.serving.retained_conditions),
        }
    }

    pub(super) fn log_new_failures(
        &self,
        hydrator: &RemoteConfigValueHydrator,
        previous: &SpecStoreData,
        format: &str,
    ) {
        let previous = previous.blob_repair.iter().flat_map(Self::failed_blobs);
        hydrator.log_unavailable_blobs(self.failed_blobs(), previous, format);
    }
}

// Only the failed entities differ between the serving snapshot and the wire base for CopyPrev.
pub(super) struct PartialBlobSnapshot {
    pub(super) incomplete: Box<IncompleteBlobConfigs>,
    overlay: Arc<ProducerOverlay>,
}

#[derive(Default)]
struct ProducerOverlay {
    producer_configs: HashMap<InternedString, SpecPointer>,
    // Newly added configs can serve healthy slots on a later full refresh.
    withheld_existing: HashSet<InternedString>,
    serving: ServingOverlay,
}

#[derive(Default)]
struct ServingOverlay {
    unavailable: UnavailableValues,
    retained_conditions: RetainedConditions,
}

#[derive(Default)]
pub(crate) struct FullBlobOverlay {
    serving: ServingOverlay,
    // Verified incoming blobs are reusable while readers still see the old entity.
    pub(super) pending_proofs: VerifiedRemoteConfigValues,
}

impl PartialBlobSnapshot {
    pub(super) fn producer_configs(&self) -> &HashMap<InternedString, SpecPointer> {
        &self.overlay.producer_configs
    }
}

impl SpecStoreData {
    pub(super) fn partial_blobs(&self) -> Option<&Arc<PartialBlobSnapshot>> {
        match self.blob_repair.as_ref()? {
            BlobRepair::Delta(p) => Some(p),
            _ => None,
        }
    }

    pub(super) fn partial_hydration(&self) -> Option<&Arc<PartialHydration>> {
        match self.blob_repair.as_ref()? {
            BlobRepair::Full(p) => Some(p),
            _ => None,
        }
    }

    pub(super) fn had_complete_config(&self, name: &InternedString) -> bool {
        match self
            .unavailable_values()
            .and_then(|missing| missing.get(name))
        {
            None => self.snapshot.dynamic_configs.get(name).is_some(),
            Some(slots) => {
                slots.is_empty()
                    && self
                        .partial_blobs()
                        .is_none_or(|delta| delta.overlay.withheld_existing.contains(name))
            }
        }
    }

    pub(crate) fn retained_conditions(&self) -> Option<&RetainedConditions> {
        self.blob_repair.as_ref()?.retained_conditions()
    }

    pub(crate) fn unavailable_values(&self) -> Option<&UnavailableValues> {
        match self.blob_repair.as_ref()? {
            BlobRepair::Full(repair) => Some(
                repair
                    .overlay
                    .as_ref()
                    .map_or(&repair.unavailable, |s| &s.serving.unavailable),
            ),
            BlobRepair::Delta(repair) => Some(&repair.overlay.serving.unavailable),
        }
    }
}

fn conflicts_with_pending_mapping(
    installed: &SpecStoreData,
    candidate: &SpecsResponseFull,
    incomplete: &IncompleteBlobConfigs,
) -> bool {
    let old = installed.snapshot.overrides.as_ref();
    let new = candidate.overrides.as_ref();
    if [old, new].into_iter().flatten().any(|overrides| {
        overrides
            .values()
            .flatten()
            .any(|mapping| incomplete.pending.contains_key(&mapping.new_config_name))
    }) {
        // A working alias could start reading a missing value, or a formerly hidden value
        // could be exposed by name when its mapping disappears.
        return true;
    }
    incomplete.pending.keys().any(|name| {
        let next = new
            .and_then(|m| m.get(name.as_str()))
            .map(Vec::as_slice)
            .unwrap_or_default();
        if let Some(prev) = old.and_then(|m| m.get(name.as_str())) {
            // An already withheld root can stay withheld while its destinations stay private.
            return !installed
                .partial_blobs()
                .is_some_and(|p| p.overlay.serving.unavailable.contains_key(name))
                || prev
                    .iter()
                    .map(|m| &m.new_config_name)
                    .collect::<HashSet<_>>()
                    != next
                        .iter()
                        .map(|m| &m.new_config_name)
                        .collect::<HashSet<_>>();
        }
        // A new, withheld root may route to new private specs, without hiding installed names.
        next.iter().any(|m| {
            let dest = &m.new_config_name;
            [
                &installed.snapshot.dynamic_configs,
                &installed.snapshot.feature_gates,
                &installed.snapshot.layer_configs,
            ]
            .iter()
            .any(|specs| specs.get(dest).is_some())
        })
    })
}

// The retained spec's fieldsUsed describes the old rules. A nested gate with
// no rules or mapping can still change its default without reading user fields.
fn has_live_field_dependency(condition: &Condition, candidate: &SpecsResponseFull) -> bool {
    match condition.compiled_condition_type {
        ConditionType::PassGate | ConditionType::FailGate => {
            let Some(gate) = condition
                .target_value
                .as_ref()
                .and_then(|value| value.as_value_ref().interned_string_value())
            else {
                return true;
            };
            candidate
                .overrides
                .as_ref()
                .is_some_and(|mappings| mappings.contains_key(gate.as_str()))
                || gate
                    .get_from(&candidate.feature_gates.0)
                    .is_some_and(|gate| gate.view().rules_len() != 0)
        }
        ConditionType::ExperimentGroup => true,
        _ => false,
    }
}

/// Copy only the old rule conditions the producer removed. A newly bound or
/// redefined ID makes reuse unsafe for the entire config.
fn retain_rule_conditions(
    spec: SpecView<'_>,
    installed: &SpecStoreData,
    name: &InternedString,
    candidate: &SpecsResponseFull,
) -> Option<ConditionMap> {
    if candidate
        .cmab_configs
        .as_ref()
        .is_some_and(|configs| configs.contains_key(name.as_str()))
    {
        return None;
    }
    let previous = installed
        .retained_conditions()
        .and_then(|by_name| by_name.get(name));
    let mut removed = ConditionMap::default();
    for index in 0..spec.rules_len() {
        let rule = spec.rule(index);
        if rule.config_delegate().is_some() {
            return None;
        }
        for offset in 0..rule.conditions_len() {
            let id = rule.condition_id(offset);
            let old = resolve_condition(id, &installed.snapshot.condition_map, previous);
            if old.is_some_and(|condition| has_live_field_dependency(condition, candidate)) {
                return None;
            }
            match (old, id.get_from(&candidate.condition_map)) {
                (None, Some(_)) => return None,
                (Some(old), Some(new)) if !old.has_same_targeting(new) => return None,
                (Some(old), None) => {
                    removed
                        .entry(id.to_interned())
                        .or_insert_with(|| old.clone());
                }
                _ => {}
            }
        }
    }
    Some(removed)
}

pub(super) fn restore_pending_configs(
    installed: &SpecStoreData,
    candidate: &mut SpecsResponseFull,
    proofs: &mut VerifiedRemoteConfigValues,
    incomplete: Box<IncompleteBlobConfigs>,
) -> Result<PartialBlobSnapshot, StatsigErr> {
    if conflicts_with_pending_mapping(installed, candidate, &incomplete) {
        return Err(StatsigErr::InvalidOperation(
            "Incomplete delta would change routing for a mapped config".into(),
        ));
    }
    let mut overlay = ProducerOverlay::default();
    restore_complete_entities(
        installed,
        candidate,
        proofs,
        incomplete.pending.keys(),
        &mut overlay.serving,
        HashSet::new(),
        |name, pending, _| {
            overlay.producer_configs.insert(name.clone(), pending);
        },
    )?;
    overlay.withheld_existing = overlay
        .serving
        .unavailable
        .keys()
        .filter(|name| installed.had_complete_config(name))
        .cloned()
        .collect();
    Ok(PartialBlobSnapshot {
        incomplete,
        overlay: Arc::new(overlay),
    })
}

pub(super) fn restore_full_configs(
    installed: &SpecStoreData,
    candidate: &mut SpecsResponseFull,
    proofs: &mut VerifiedRemoteConfigValues,
    hydration: &mut PartialHydration,
) -> Result<(), StatsigErr> {
    let mut names = hydration
        .unavailable
        .keys()
        .filter(|name| installed.had_complete_config(name))
        .peekable();
    if names.peek().is_none() {
        return Ok(());
    }
    let mut mapped = HashSet::new();
    for overrides in installed
        .snapshot
        .overrides
        .iter()
        .chain(&candidate.overrides)
    {
        for entry in overrides.values().flatten() {
            if hydration.unavailable.contains_key(&entry.new_config_name) {
                mapped.insert(entry.new_config_name.clone());
            }
        }
    }
    let mut verified_bytes = 0;
    let mut overlay = FullBlobOverlay::default();
    let restored_names = restore_complete_entities(
        installed,
        candidate,
        proofs,
        names,
        &mut overlay.serving,
        mapped,
        |name, _, values| {
            if let Some(mut values) = values {
                limit_pending_proofs(Arc::make_mut(&mut values), &mut verified_bytes);
                if !values.is_empty() {
                    overlay.pending_proofs.insert(name.clone(), values);
                }
            }
        },
    )?;
    for (name, slots) in &hydration.unavailable {
        if !restored_names.contains(name.as_str()) {
            overlay
                .serving
                .unavailable
                .insert(name.clone(), slots.clone());
        }
    }
    hydration.overlay = Some(Box::new(overlay));
    Ok(())
}

fn restore_complete_entities<'a>(
    installed: &SpecStoreData,
    candidate: &mut SpecsResponseFull,
    proofs: &mut VerifiedRemoteConfigValues,
    names: impl Iterator<Item = &'a InternedString> + Clone,
    overlay: &mut ServingOverlay,
    mut indirect: HashSet<InternedString>,
    mut save_pending: impl FnMut(&InternedString, SpecPointer, Option<Arc<VerifiedRemoteValues>>),
) -> Result<HashSet<&'a str>, StatsigErr> {
    let pending_names: HashSet<_> = names.clone().map(|n| n.as_str()).collect();
    for (_, layer) in installed
        .snapshot
        .layer_configs
        .iter()
        .chain(candidate.layer_configs.iter())
    {
        let layer = layer.view();
        for index in 0..layer.rules_len() {
            if let Some(delegate) = layer
                .rule(index)
                .config_delegate()
                .filter(|delegate| pending_names.contains(delegate.as_str()))
            {
                indirect.insert(delegate.to_interned());
            }
        }
    }
    let target_apps = |spec: SpecView<'_>| spec.target_app_ids().map(HashSet::<_>::from_iter);
    let same_app_routing = installed.snapshot.company_id == candidate.company_id
        && installed.snapshot.default_environment == candidate.default_environment
        && installed.snapshot.app_id == candidate.app_id
        && installed.snapshot.sdk_keys_to_app_ids == candidate.sdk_keys_to_app_ids
        && installed.snapshot.hashed_sdk_keys_to_app_ids == candidate.hashed_sdk_keys_to_app_ids;
    for name in names {
        let pending = candidate.dynamic_configs.remove(name).ok_or_else(|| {
            StatsigErr::InvalidOperation("Pending blob config missing from parsed update".into())
        })?;
        let old = installed.snapshot.dynamic_configs.get(name).filter(|old| {
            same_app_routing
                && !indirect.contains(name)
                && old.view().entity().as_str() == pending.view().entity().as_str()
                && target_apps(old.view()) == target_apps(pending.view())
                && !installed
                    .snapshot
                    .overrides
                    .iter()
                    .chain(&candidate.overrides)
                    .any(|m| m.contains_key(name.as_str()))
        });
        save_pending(name, pending, proofs.remove(name));
        let retained = old.and_then(|old| {
            retain_rule_conditions(old.view(), installed, name, candidate)
                .map(|conditions| (old, conditions))
        });
        if let Some((old, conditions)) = retained {
            if !conditions.is_empty() {
                overlay.retained_conditions.insert(name.clone(), conditions);
            }
            candidate.dynamic_configs.insert(name.clone(), old.clone());
            if let Some(values) = installed.verified_remote_values.get(name) {
                proofs.insert(name.clone(), Arc::clone(values));
            }
        } else {
            overlay.unavailable.insert(name.clone(), HashSet::new());
        }
    }
    Ok(pending_names)
}

impl SpecStore {
    pub(super) async fn retry_pending_configs(
        &self,
        base: &SpecStoreData,
        pending: &PartialBlobSnapshot,
        hydration: &SpecsUpdateHydration,
    ) -> Result<(), StatsigErr> {
        let options = StoreHydrationOptions::new(&hydration.source_url, self.mmap_project_id)
            .with_sync_trigger(hydration.sync_trigger)
            .with_session_update_mode(self.preserve_session_update_mode);
        let repaired = repair_pending_blob_configs(
            &hydration.hydrator,
            options,
            &pending.incomplete,
            &base.verified_remote_values,
        )
        .await?;
        // Building protocol maps may be expensive. Only successful repairs need a new evaluation snapshot.
        let candidate = if repaired.configs.is_empty() {
            None
        } else {
            let mut candidate = base
                .snapshot
                .with_cursor(base.lcut(), base.sync_cursor.checksum.clone())
                .map_err(|e| StatsigErr::SerializationError(e.to_string()))?;
            candidate.restore_producer_configs(pending.producer_configs());
            Some(candidate)
        };
        let guard = self
            .try_lock_for_update("retry_pending_configs")
            .ok_or_else(|| StatsigErr::LockFailure("Could not publish blob retry".into()))?;
        let current = self.load_data();
        if !same_parse_base(base, &current) {
            // A newer delta may have replaced or deleted this target during the GET.
            return Ok(());
        }
        if let Some(mut candidate) = candidate {
            let mut proofs = (*base.verified_remote_values).clone();
            for name in pending.incomplete.pending.keys() {
                proofs.remove(name);
            }
            proofs.extend(repaired.verified);
            candidate.dynamic_configs.0.extend(repaired.configs);
            let applied = self.specs_update_apply(
                Box::new(candidate),
                base.field_checksums,
                (&current.source, &current.source_api),
                true,
                base.spec_decode_stats,
                RemoteValueState {
                    verified: proofs,
                    pending_delta: repaired.incomplete,
                    ..Default::default()
                },
            )?;
            drop(guard);
            if let Some(repair) = &applied.blob_repair {
                repair.log_new_failures(&hydration.hydrator, base, "protobuf");
            }
            self.specs_update_notify(
                SpecsFormat::Protobuf,
                ConfigResponseType::Delta,
                None,
                applied,
                false,
            )?;
        } else if let Some(incomplete) = repaired.incomplete {
            // Some slots may have downloaded even if no whole config is ready yet.
            let mut next = current.as_ref().clone();
            let repair = BlobRepair::Delta(Arc::new(PartialBlobSnapshot {
                incomplete,
                overlay: Arc::clone(&pending.overlay),
            }));
            next.blob_repair = Some(repair.clone());
            self.data.store(Arc::new(next));
            drop(guard);
            repair.log_new_failures(&hydration.hydrator, base, "protobuf");
        }
        Ok(())
    }
}
