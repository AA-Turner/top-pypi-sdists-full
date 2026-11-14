use std::{collections::HashMap, sync::Arc};

use prost::Message;

use crate::{
    StatsigErr,
    interned_string::InternedString,
    interned_values::InternedStore,
    specs_adapter::remote_config_value_hydrator::{
        IncompleteBlobConfigs, PartialBlobRefresh, ProtobufHydrationSession,
        RemoteConfigValueHydrator, StoreHydrationOptions,
    },
    specs_response::{specs_hash_map::SpecPointer, statsig_config_specs as pb},
};

use super::{VerifiedRemoteConfigValues, map_decode_err, spec_with_remote_values};

#[derive(Default)]
pub(crate) struct RepairedBlobConfigs {
    pub(crate) configs: HashMap<InternedString, SpecPointer>,
    pub(crate) verified: VerifiedRemoteConfigValues,
    pub(crate) incomplete: Option<Box<IncompleteBlobConfigs>>,
}

pub(crate) async fn repair_pending_blob_configs(
    hydrator: &RemoteConfigValueHydrator,
    options: StoreHydrationOptions<'_>,
    previous: &IncompleteBlobConfigs,
    verified: &VerifiedRemoteConfigValues,
) -> Result<RepairedBlobConfigs, StatsigErr> {
    let refresh = PartialBlobRefresh::new(Some(previous));
    let mut hydration =
        hydrator.begin_protobuf_hydration_with_trigger(options.source_url, options.sync_trigger);
    hydration.set_response_type(true);
    hydration.retain_previous_configs(&refresh);
    let result = repair_carried_configs(&mut hydration, options, &refresh, verified).await;
    hydration.finish(result.as_ref().map(|_| ()));
    let mut repaired = result?;
    repaired.incomplete = refresh.take_incomplete();
    Ok(repaired)
}

// Retry only definitions that survived the current delta. Registration uses each definition's
// original DCS origin, but every download shares one concurrency window and one deadline.
pub(super) async fn repair_carried_configs(
    hydration: &mut ProtobufHydrationSession<'_>,
    options: StoreHydrationOptions<'_>,
    refresh: &PartialBlobRefresh<'_>,
    verified: &VerifiedRemoteConfigValues,
) -> Result<RepairedBlobConfigs, StatsigErr> {
    let mut result = RepairedBlobConfigs::default();
    let pending = refresh.carried_configs();
    if pending.is_empty() {
        return Ok(result);
    }
    hydration.set_previous_values(
        verified
            .values()
            .flat_map(|values| {
                values
                    .iter()
                    .map(|(sha, value)| (sha.clone(), Arc::clone(value)))
            })
            .collect(),
    );
    hydration.set_previous_mmap_values(InternedStore::mmap_verified_remote_values(
        options.mmap_project_id,
    ));
    for (name, config) in &pending {
        let definition = &config.definition;
        let spec = pb::Spec::decode(definition.data.as_slice())
            .map_err(|error| map_decode_err("DynamicConfig", error))?;
        hydration.register_config_references(name, &spec, Some(&definition.source_url))?;
    }
    hydration.download_registered_references().await?;
    for (name, config) in pending {
        let definition = &config.definition;
        let resolved: Result<_, StatsigErr> =
            InternedStore::with_mmap_project(options.mmap_project_id, || {
                let mut spec = pb::Spec::decode(definition.data.as_slice())
                    .map_err(|error| map_decode_err("DynamicConfig", error))?;
                let values = hydration.take_resolved_spec_values(&mut spec)?;
                if !values.unavailable_slots.is_empty() {
                    refresh.defer(&name, Arc::clone(definition), values);
                    return Ok(None);
                }
                let spec =
                    spec_with_remote_values(definition.checksum.clone(), spec, Some(&values))?;
                Ok(Some((
                    SpecPointer::from_spec(spec),
                    Arc::new(values.provenance),
                )))
            });
        if let Some((spec, values)) = resolved? {
            refresh.clear_config(&name);
            result.configs.insert(name.clone(), spec);
            result.verified.insert(name, values);
        }
    }
    Ok(result)
}
