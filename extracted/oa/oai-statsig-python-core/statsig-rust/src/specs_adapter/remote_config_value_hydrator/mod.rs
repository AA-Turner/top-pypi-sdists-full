use std::sync::{Arc, OnceLock};
use std::time::{Duration, Instant};

use dashmap::DashMap;
use tokio::time::timeout;

use crate::StatsigErr;
use crate::networking::{NetworkClient, ResponseData};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::specs_adapter::response_format::{
    SpecsResponseFormat, get_specs_response_format, is_legacy_json_no_update_under_protobuf_headers,
};

mod download;
mod errors;
mod json;
mod metadata;
mod protobuf;
mod telemetry;

use download::{
    GLOBAL_RESPONSE_HYDRATION_BUDGET, MAX_ACTIVE_RESPONSE_RESERVATION_BYTES,
    ResponseHydrationBudget, SharedDownload, SharedDownloadKey,
};
use errors::HydrationTimeoutStep;
use telemetry::{HydrationOutcome, HydrationResult};

pub(crate) use download::DOWNLOAD_CONCURRENCY;
pub(crate) use protobuf::{
    ProtobufHydrationSession, VerifiedRemoteValues,
    protobuf_top_level_has_hydrated_sidecar_provenance,
    remote_metadata_marker_without_metadata_error, rewrite_decoded_dynamic_config_envelope,
    rewrite_top_level_envelope,
};
pub(crate) use telemetry::HydrationPhase;

const TAG: &str = "RemoteConfigValueHydrator";
const HYDRATION_TIMEOUT: Duration = Duration::from_secs(30);

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

    pub(crate) fn begin_protobuf_hydration<'a>(
        &'a self,
        source_url: &'a str,
    ) -> ProtobufHydrationSession<'a> {
        protobuf::begin_session(self, source_url)
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
        // Some legacy DCS responses keep statsig-br headers around a JSON
        // no-update body. Preserve those bytes instead of probing protobuf.
        if is_legacy_json_no_update_under_protobuf_headers(data)? {
            return Ok(());
        }

        let started_at = Instant::now();
        let mut hydration_result = HydrationResult::new(self);
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
                self.log_hydration_outcome(started_at, HydrationOutcome::Success);
                Ok(())
            }
            Err(error) => {
                self.log_hydration_outcome(started_at, HydrationOutcome::Failure);
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
