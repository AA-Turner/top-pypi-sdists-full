use std::collections::HashMap;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};

use chrono::Utc;

use super::response_format::{SpecsResponseFormat, get_specs_response_format};
use crate::networking::{ResponseData, api_from_url, config_specs_url};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::specs_response::spec_types::SpecsResponseNoUpdates;

const CONFIG_SYNC_OVERALL_LATENCY_METRIC: &str = "config_sync_overall.latency";
const CONFIG_SYNC_OVERALL_FORMAT_TAG: &str = "format";
const CONFIG_SYNC_OVERALL_SOURCE_API_TAG: &str = "source_api";
const CONFIG_SYNC_OVERALL_ERROR_TAG: &str = "error";
const CONFIG_SYNC_OVERALL_NETWORK_SUCCESS_TAG: &str = "network_success";
const CONFIG_SYNC_OVERALL_PROCESS_SUCCESS_TAG: &str = "process_success";
const CONFIG_SYNC_OVERALL_DELTAS_USED_TAG: &str = "deltas_used";
const CONFIG_SYNC_OVERALL_RESPONSE_TYPE_TAG: &str = "response_type";
const CONFIG_SYNC_FULL_FALLBACK_COUNT_METRIC: &str = "config_sync_full_fallback.count";
const CONFIG_SYNC_FULL_FALLBACK_REASON_TAG: &str = "fallback_reason";
const CONFIG_SYNC_FULL_FALLBACK_SOURCE_TAG: &str = "fallback_source";
const CONFIG_SYNC_FULL_FALLBACK_CURSOR_STATE_TAG: &str = "cursor_state";

const DELTA_FALLBACK_REASON_HEADER: &str = "x-statsig-delta-fallback-reason";
const DELTA_FALLBACK_SOURCE_HEADER: &str = "x-statsig-delta-fallback-source";

pub(super) enum ConfigSyncResponseType {
    Delta,
    Full,
    NoUpdate,
    NetworkError,
    JsonBody(Arc<AtomicBool>),
}

impl ConfigSyncResponseType {
    pub(super) fn from_headers(data: &ResponseData) -> Option<Self> {
        if is_true_header(data, "x-cache-hit") {
            return Some(Self::NoUpdate);
        }
        data.get_header_ref("x-deltas-used").map(|_| Self::Delta)
    }

    pub(super) fn from_response_data(data: &mut ResponseData) -> Self {
        if let Some(response_type) = Self::from_headers(data) {
            return response_type;
        }

        let response_type = match data.deserialize_into::<SpecsResponseNoUpdates>() {
            Ok(response) if !response.has_updates => Self::NoUpdate,
            _ => Self::Full,
        };
        let _ = data.rewind();
        response_type
    }

    pub(super) fn as_str(&self) -> &'static str {
        match self {
            Self::Delta => "delta",
            Self::Full => "full",
            Self::NoUpdate => "no_update",
            Self::NetworkError => "network_error",
            Self::JsonBody(has_updates) => {
                if has_updates.load(Ordering::Relaxed) {
                    "full"
                } else {
                    "no_update"
                }
            }
        }
    }
}

pub(super) struct ConfigSyncMetrics {
    pub(super) source_api: String,
    pub(super) response_format: SpecsResponseFormat,
    pub(super) network_success: bool,
    pub(super) deltas_used: bool,
    pub(super) delta_fallback_reason: DeltaFallbackReason,
    pub(super) delta_fallback_source: DeltaFallbackSource,
    pub(super) response_type: ConfigSyncResponseType,
}

impl ConfigSyncMetrics {
    pub(super) fn from_response_headers(
        data: &ResponseData,
        source_api: &str,
        requested_deltas: bool,
    ) -> Self {
        let response_type =
            ConfigSyncResponseType::from_headers(data).unwrap_or(ConfigSyncResponseType::Full);
        Self {
            source_api: source_api.to_owned(),
            response_format: get_specs_response_format(data),
            network_success: true,
            deltas_used: requested_deltas,
            delta_fallback_reason: get_delta_fallback_reason(data),
            delta_fallback_source: get_delta_fallback_source(data),
            response_type,
        }
    }

    pub(super) fn from_network_error(source_url: &str, requested_deltas: bool) -> Self {
        Self {
            source_api: api_from_url(&config_specs_url(source_url)),
            response_format: SpecsResponseFormat::Unknown,
            network_success: false,
            deltas_used: requested_deltas,
            delta_fallback_reason: DeltaFallbackReason::MissingHeader,
            delta_fallback_source: DeltaFallbackSource::MissingHeader,
            response_type: ConfigSyncResponseType::NetworkError,
        }
    }
}

fn is_true_header(data: &ResponseData, key: &str) -> bool {
    data.get_header_ref(key)
        .is_some_and(|value| value.eq_ignore_ascii_case("true"))
}

fn get_delta_fallback_reason(data: &ResponseData) -> DeltaFallbackReason {
    DeltaFallbackReason::from_header(
        data.get_header_ref(DELTA_FALLBACK_REASON_HEADER)
            .map(String::as_str),
    )
}

fn get_delta_fallback_source(data: &ResponseData) -> DeltaFallbackSource {
    DeltaFallbackSource::from_header(
        data.get_header_ref(DELTA_FALLBACK_SOURCE_HEADER)
            .map(String::as_str),
    )
}

// This is a bounded response contract with Statsig Forward Proxy. Keep the
// header parsing exact so arbitrary response values cannot become metric tags.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(super) enum DeltaFallbackReason {
    DeltasDisabled,
    DeltasStoreUnavailable,
    SdkKeyNotRegistered,
    NoCached,
    BeforeEarliestLcut,
    FirstBaselineChecksumMismatch,
    SameLcutBaselineMissing,
    FirstSelectedBaseMismatch,
    MissingCallerChecksum,
    AdjacentChecksumChainGap,
    SupportsProtoRequired,
    SerializationFailed,
    UnsupportedPath,
    Unclassified,
    MissingHeader,
    InvalidHeader,
}

impl DeltaFallbackReason {
    pub(super) fn from_header(value: Option<&str>) -> Self {
        match value {
            Some("deltas_disabled") => Self::DeltasDisabled,
            Some("deltas_store_unavailable") => Self::DeltasStoreUnavailable,
            Some("sdk_key_not_registered") => Self::SdkKeyNotRegistered,
            Some("no_cached") => Self::NoCached,
            Some("before_earliest_lcut") => Self::BeforeEarliestLcut,
            Some("first_baseline_checksum_mismatch") => Self::FirstBaselineChecksumMismatch,
            Some("same_lcut_baseline_missing") => Self::SameLcutBaselineMissing,
            Some("first_selected_base_mismatch") => Self::FirstSelectedBaseMismatch,
            Some("missing_caller_checksum") => Self::MissingCallerChecksum,
            Some("adjacent_checksum_chain_gap") => Self::AdjacentChecksumChainGap,
            Some("supports_proto_required") => Self::SupportsProtoRequired,
            Some("serialization_failed") => Self::SerializationFailed,
            Some("unsupported_path") => Self::UnsupportedPath,
            Some("unclassified") => Self::Unclassified,
            Some(_) => Self::InvalidHeader,
            None => Self::MissingHeader,
        }
    }

    pub(super) const fn as_str(self) -> &'static str {
        match self {
            Self::DeltasDisabled => "deltas_disabled",
            Self::DeltasStoreUnavailable => "deltas_store_unavailable",
            Self::SdkKeyNotRegistered => "sdk_key_not_registered",
            Self::NoCached => "no_cached",
            Self::BeforeEarliestLcut => "before_earliest_lcut",
            Self::FirstBaselineChecksumMismatch => "first_baseline_checksum_mismatch",
            Self::SameLcutBaselineMissing => "same_lcut_baseline_missing",
            Self::FirstSelectedBaseMismatch => "first_selected_base_mismatch",
            Self::MissingCallerChecksum => "missing_caller_checksum",
            Self::AdjacentChecksumChainGap => "adjacent_checksum_chain_gap",
            Self::SupportsProtoRequired => "supports_proto_required",
            Self::SerializationFailed => "serialization_failed",
            Self::UnsupportedPath => "unsupported_path",
            Self::Unclassified => "unclassified",
            Self::MissingHeader => "missing_header",
            Self::InvalidHeader => "invalid_header",
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(super) enum DeltaFallbackSource {
    LocalCompute,
    LegacyStore,
    NoStore,
    Unclassified,
    MissingHeader,
    InvalidHeader,
}

impl DeltaFallbackSource {
    pub(super) fn from_header(value: Option<&str>) -> Self {
        match value {
            Some("local_compute") => Self::LocalCompute,
            Some("legacy_store") => Self::LegacyStore,
            Some("no_store") => Self::NoStore,
            Some("unclassified") => Self::Unclassified,
            Some(_) => Self::InvalidHeader,
            None => Self::MissingHeader,
        }
    }

    pub(super) const fn as_str(self) -> &'static str {
        match self {
            Self::LocalCompute => "local_compute",
            Self::LegacyStore => "legacy_store",
            Self::NoStore => "no_store",
            Self::Unclassified => "unclassified",
            Self::MissingHeader => "missing_header",
            Self::InvalidHeader => "invalid_header",
        }
    }
}

#[allow(clippy::too_many_arguments)]
pub fn log_config_sync_overall_latency(
    ops_stats: &Arc<OpsStatsForInstance>,
    sync_start_ms: u64,
    source_api: &str,
    response_format: &str,
    network_success: bool,
    process_success: bool,
    error: String,
    deltas_used: bool,
    response_type: &str,
) {
    let latency_ms = (Utc::now().timestamp_millis() as u64).saturating_sub(sync_start_ms) as f64;
    ops_stats.log(ObservabilityEvent::new_event(
        MetricType::Dist,
        CONFIG_SYNC_OVERALL_LATENCY_METRIC.to_string(),
        latency_ms,
        Some(HashMap::from([
            (
                CONFIG_SYNC_OVERALL_SOURCE_API_TAG.to_string(),
                if source_api == "datastore" {
                    source_api.to_string()
                } else {
                    api_from_url(source_api)
                },
            ),
            (
                CONFIG_SYNC_OVERALL_FORMAT_TAG.to_string(),
                response_format.to_string(),
            ),
            (CONFIG_SYNC_OVERALL_ERROR_TAG.to_string(), error),
            (
                CONFIG_SYNC_OVERALL_NETWORK_SUCCESS_TAG.to_string(),
                network_success.to_string(),
            ),
            (
                CONFIG_SYNC_OVERALL_PROCESS_SUCCESS_TAG.to_string(),
                process_success.to_string(),
            ),
            (
                CONFIG_SYNC_OVERALL_DELTAS_USED_TAG.to_string(),
                deltas_used.to_string(),
            ),
            (
                CONFIG_SYNC_OVERALL_RESPONSE_TYPE_TAG.to_string(),
                response_type.to_string(),
            ),
        ])),
    ));
}

pub fn log_config_sync_full_fallback_count(
    ops_stats: &Arc<OpsStatsForInstance>,
    source_api: &str,
    deltas_used: bool,
    response_type: &str,
    fallback_reason: DeltaFallbackReason,
    fallback_source: DeltaFallbackSource,
    cursor_state: &str,
) {
    if !deltas_used || response_type != "full" {
        return;
    }

    ops_stats.log(ObservabilityEvent::new_event(
        MetricType::Increment,
        CONFIG_SYNC_FULL_FALLBACK_COUNT_METRIC.to_string(),
        1.0,
        Some(HashMap::from([
            (
                CONFIG_SYNC_OVERALL_SOURCE_API_TAG.to_string(),
                if source_api == "datastore" {
                    source_api.to_string()
                } else {
                    api_from_url(source_api)
                },
            ),
            (
                CONFIG_SYNC_FULL_FALLBACK_REASON_TAG.to_string(),
                fallback_reason.as_str().to_string(),
            ),
            (
                CONFIG_SYNC_FULL_FALLBACK_SOURCE_TAG.to_string(),
                fallback_source.as_str().to_string(),
            ),
            (
                CONFIG_SYNC_FULL_FALLBACK_CURSOR_STATE_TAG.to_string(),
                cursor_state.to_string(),
            ),
        ])),
    ));
}

#[cfg(test)]
#[path = "__tests__/config_spec_background_sync_metrics_tests.rs"]
mod tests;
