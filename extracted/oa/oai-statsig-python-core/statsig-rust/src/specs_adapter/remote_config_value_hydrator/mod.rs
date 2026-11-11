use std::sync::{Arc, OnceLock, atomic::AtomicBool};
use std::time::{Duration, Instant};

use dashmap::DashMap;
use tokio::time::timeout;

use crate::StatsigErr;
use crate::interned_values::interned_store::MmapProjectId;
use crate::networking::{NetworkClient, ResponseData};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::specs_adapter::SpecsSyncTrigger;
use crate::specs_adapter::response_format::{
    SpecsResponseFormat, get_specs_response_format, is_legacy_json_no_update_under_protobuf_headers,
};
use crate::specs_response::proto_specs::VerifiedRemoteConfigValues;

mod download;
mod errors;
mod json;
mod metadata;
mod protobuf;
mod telemetry;
mod verified_values;

use download::{
    GLOBAL_RESPONSE_HYDRATION_BUDGET, MAX_ACTIVE_RESPONSE_RESERVATION_BYTES,
    ResponseHydrationBudget, SharedDownload, SharedDownloadKey,
};
use errors::HydrationTimeoutStep;
use telemetry::{HydrationOutcome, HydrationResult};

pub(crate) use download::DOWNLOAD_CONCURRENCY;
pub(crate) use errors::unsupported_entity_error;
pub(crate) use json::HydratedJsonStoreUpdate;
pub(crate) use protobuf::{
    ProtobufHydrationSession, declares_unsupported_remote_metadata,
    protobuf_spec_has_remote_metadata as protobuf_spec_bytes_have_remote_metadata,
    protobuf_top_level_has_hydrated_sidecar_provenance,
    remote_metadata_marker_without_metadata_error, rewrite_decoded_dynamic_config_envelope,
    rewrite_top_level_envelope,
};
pub(crate) use telemetry::HydrationPhase;
pub(crate) use verified_values::{MmapRemoteValueProof, VerifiedRemoteValue, VerifiedRemoteValues};

const TAG: &str = "RemoteConfigValueHydrator";
const HYDRATION_TIMEOUT: Duration = Duration::from_secs(30);

/// Shared settings for hydrating a store update. Source URL and project scope
/// are required; telemetry tagging and additional output are opt-in.
#[derive(Clone, Copy)]
pub(crate) struct StoreHydrationOptions<'a> {
    pub(crate) source_url: &'a str,
    pub(crate) mmap_project_id: MmapProjectId,
    pub(crate) sync_trigger: Option<SpecsSyncTrigger>,
    pub(crate) preserve_session_update_mode: bool,
    pub(crate) capture_data_store_bytes: bool,
}

impl<'a> StoreHydrationOptions<'a> {
    pub(crate) fn new(source_url: &'a str, mmap_project_id: MmapProjectId) -> Self {
        Self {
            source_url,
            mmap_project_id,
            sync_trigger: None,
            preserve_session_update_mode: false,
            capture_data_store_bytes: false,
        }
    }

    pub(crate) fn with_sync_trigger(mut self, sync_trigger: Option<SpecsSyncTrigger>) -> Self {
        self.sync_trigger = sync_trigger;
        self
    }

    pub(crate) fn with_session_update_mode(mut self, preserve: bool) -> Self {
        self.preserve_session_update_mode = preserve;
        self
    }

    pub(crate) fn with_data_store_capture(mut self, capture: bool) -> Self {
        self.capture_data_store_bytes = capture;
        self
    }
}

/// Hydrates blob-backed dynamic config values in a DCS response before the
/// response is parsed or published.
pub(crate) struct RemoteConfigValueHydrator {
    network: Arc<NetworkClient>,
    ops_stats: Arc<OpsStatsForInstance>,
    in_flight: OnceLock<DashMap<SharedDownloadKey, Arc<SharedDownload>>>,
    response_budget: Arc<ResponseHydrationBudget>,
}

impl RemoteConfigValueHydrator {
    pub(crate) fn new_with_ops_stats(
        network: Arc<NetworkClient>,
        ops_stats: Arc<OpsStatsForInstance>,
    ) -> Self {
        Self {
            network,
            ops_stats,
            in_flight: OnceLock::new(),
            response_budget: Arc::clone(GLOBAL_RESPONSE_HYDRATION_BUDGET.get_or_init(|| {
                Arc::new(ResponseHydrationBudget::new(
                    MAX_ACTIVE_RESPONSE_RESERVATION_BYTES / 2,
                ))
            })),
        }
    }

    #[cfg(test)]
    pub(crate) fn begin_protobuf_hydration<'a>(
        &'a self,
        source_url: &'a str,
    ) -> ProtobufHydrationSession<'a> {
        self.begin_protobuf_hydration_with_trigger(source_url, None)
    }

    pub(crate) fn begin_protobuf_hydration_with_trigger<'a>(
        &'a self,
        source_url: &'a str,
        sync_trigger: Option<SpecsSyncTrigger>,
    ) -> ProtobufHydrationSession<'a> {
        protobuf::begin_session(self, source_url, sync_trigger)
    }

    /// Build a candidate JSON snapshot using provenance from the same immutable
    /// store base. The store must reject publication if that base has changed.
    /// `None` means hydration was not needed; the caller should parse normally.
    pub(crate) async fn prepare_json_store_update(
        &self,
        data: &mut ResponseData,
        options: StoreHydrationOptions<'_>,
        current_verified_values: &VerifiedRemoteConfigValues,
        response_has_updates: Option<&AtomicBool>,
    ) -> Result<Option<HydratedJsonStoreUpdate>, StatsigErr> {
        let started_at = Instant::now();
        let mut hydration_result = HydrationResult::new_with_trigger(self, options.sync_trigger);
        let result = json::hydrate_response_for_store(
            self,
            data,
            options,
            current_verified_values,
            response_has_updates,
            &mut hydration_result,
        )
        .await;
        hydration_result.finish(result.as_ref().map(|_| ()));
        match &result {
            Ok(Some(_)) => {
                hydration_result.log_hydration_outcome(started_at, HydrationOutcome::Success)
            }
            Ok(None) => {}
            Err(_) => hydration_result.log_hydration_outcome(started_at, HydrationOutcome::Failure),
        }
        result
    }

    /// Rewrites any remote-backed values in data to their verified JSON
    /// values. Callers must preserve DCS response headers so protobuf payloads
    /// can be detected, and source_url must be the trusted DCS origin used
    /// to resolve relative remote-value paths.
    pub(crate) async fn hydrate_response(
        &self,
        data: &mut ResponseData,
        source_url: &str,
    ) -> Result<(), StatsigErr> {
        self.hydrate_response_with_trigger(data, source_url, None)
            .await
    }

    pub(crate) async fn hydrate_response_with_trigger(
        &self,
        data: &mut ResponseData,
        source_url: &str,
        sync_trigger: Option<SpecsSyncTrigger>,
    ) -> Result<(), StatsigErr> {
        // Some legacy DCS responses keep statsig-br headers around a JSON
        // no-update body. Preserve those bytes instead of probing protobuf.
        if is_legacy_json_no_update_under_protobuf_headers(data)? {
            return Ok(());
        }

        let started_at = Instant::now();
        let mut hydration_result = HydrationResult::new_with_trigger(self, sync_trigger);
        let result = timeout(
            HYDRATION_TIMEOUT,
            self.hydrate_response_within_timeout(data, source_url, &mut hydration_result),
        )
        .await
        .map_err(|_| self.total_timeout_error(started_at, HydrationTimeoutStep::Response))
        .and_then(|result| result);

        hydration_result.finish(result.as_ref().map(|_| ()));

        match result {
            Ok(false) => Ok(()),
            Ok(true) => {
                hydration_result.log_hydration_outcome(started_at, HydrationOutcome::Success);
                Ok(())
            }
            Err(error) => {
                hydration_result.log_hydration_outcome(started_at, HydrationOutcome::Failure);
                Err(error)
            }
        }
    }

    async fn hydrate_response_within_timeout(
        &self,
        data: &mut ResponseData,
        source_url: &str,
        hydration_result: &mut HydrationResult<'_>,
    ) -> Result<bool, StatsigErr> {
        if get_specs_response_format(data) == SpecsResponseFormat::Protobuf {
            protobuf::hydrate_response(self, data, source_url, hydration_result).await
        } else {
            json::hydrate_response(self, data, source_url, hydration_result).await
        }
    }
}

#[cfg(test)]
use json::{RawJsonObject, apply_json_hydration, response_may_contain_remote_metadata};
#[cfg(test)]
use protobuf::{
    append_length_delimited_field, decode_protobuf_envelope, encode_delimited_message,
    parse_protobuf_envelopes, parse_raw_protobuf_fields, protobuf_spec_has_remote_metadata,
    serialize_protobuf_envelopes,
};

#[cfg(test)]
#[path = "../__tests__/remote_config_value_hydrator_tests.rs"]
mod tests;

#[cfg(test)]
#[path = "__tests__/mmap_writer_hydration_order_tests.rs"]
mod mmap_writer_hydration_order_tests;
