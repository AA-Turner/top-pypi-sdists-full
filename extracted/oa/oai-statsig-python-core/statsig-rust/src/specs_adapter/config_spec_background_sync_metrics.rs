use std::collections::HashMap;
use std::sync::Arc;

use chrono::Utc;

use crate::networking::api_from_url;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::OpsStatsForInstance;

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
mod tests {
    use super::*;
    use crate::observability::ops_stats::{OpsStatsEvent, OpsStatsForInstance};

    #[test]
    fn delta_fallback_reason_round_trips_sfp_headers() {
        let cases = [
            ("deltas_disabled", DeltaFallbackReason::DeltasDisabled),
            (
                "deltas_store_unavailable",
                DeltaFallbackReason::DeltasStoreUnavailable,
            ),
            (
                "sdk_key_not_registered",
                DeltaFallbackReason::SdkKeyNotRegistered,
            ),
            ("no_cached", DeltaFallbackReason::NoCached),
            (
                "before_earliest_lcut",
                DeltaFallbackReason::BeforeEarliestLcut,
            ),
            (
                "first_baseline_checksum_mismatch",
                DeltaFallbackReason::FirstBaselineChecksumMismatch,
            ),
            (
                "same_lcut_baseline_missing",
                DeltaFallbackReason::SameLcutBaselineMissing,
            ),
            (
                "first_selected_base_mismatch",
                DeltaFallbackReason::FirstSelectedBaseMismatch,
            ),
            (
                "missing_caller_checksum",
                DeltaFallbackReason::MissingCallerChecksum,
            ),
            (
                "adjacent_checksum_chain_gap",
                DeltaFallbackReason::AdjacentChecksumChainGap,
            ),
            (
                "supports_proto_required",
                DeltaFallbackReason::SupportsProtoRequired,
            ),
            (
                "serialization_failed",
                DeltaFallbackReason::SerializationFailed,
            ),
            ("unsupported_path", DeltaFallbackReason::UnsupportedPath),
            ("unclassified", DeltaFallbackReason::Unclassified),
        ];

        for (header, expected) in cases {
            assert_eq!(DeltaFallbackReason::from_header(Some(header)), expected);
            assert_eq!(expected.as_str(), header);
        }
    }

    #[test]
    fn delta_fallback_reason_preserves_header_sentinels() {
        assert_eq!(
            DeltaFallbackReason::from_header(None),
            DeltaFallbackReason::MissingHeader
        );
        assert_eq!(
            DeltaFallbackReason::MissingHeader.as_str(),
            "missing_header"
        );
        for header in ["", "BEFORE_EARLIEST_LCUT", "free_form_reason"] {
            assert_eq!(
                DeltaFallbackReason::from_header(Some(header)),
                DeltaFallbackReason::InvalidHeader
            );
        }
        assert_eq!(
            DeltaFallbackReason::InvalidHeader.as_str(),
            "invalid_header"
        );
    }

    #[test]
    fn delta_fallback_source_round_trips_sfp_headers() {
        let cases = [
            ("local_compute", DeltaFallbackSource::LocalCompute),
            ("legacy_store", DeltaFallbackSource::LegacyStore),
            ("no_store", DeltaFallbackSource::NoStore),
            ("unclassified", DeltaFallbackSource::Unclassified),
        ];

        for (header, expected) in cases {
            assert_eq!(DeltaFallbackSource::from_header(Some(header)), expected);
            assert_eq!(expected.as_str(), header);
        }
    }

    #[test]
    fn delta_fallback_source_preserves_header_sentinels() {
        assert_eq!(
            DeltaFallbackSource::from_header(None),
            DeltaFallbackSource::MissingHeader
        );
        assert_eq!(
            DeltaFallbackSource::MissingHeader.as_str(),
            "missing_header"
        );
        for header in ["", "LOCAL_COMPUTE", "raw-unbounded-source"] {
            assert_eq!(
                DeltaFallbackSource::from_header(Some(header)),
                DeltaFallbackSource::InvalidHeader
            );
        }
        assert_eq!(
            DeltaFallbackSource::InvalidHeader.as_str(),
            "invalid_header"
        );
    }

    #[tokio::test]
    async fn full_fallback_counter_emits_for_requested_delta_full() {
        let ops_stats = Arc::new(OpsStatsForInstance::new());
        let mut receiver = ops_stats.subscribe_for_test();

        log_config_sync_full_fallback_count(
            &ops_stats,
            "datastore",
            true,
            "full",
            DeltaFallbackReason::BeforeEarliestLcut,
            DeltaFallbackSource::LocalCompute,
            "incremental",
        );

        let event = receiver.recv().await.unwrap();
        let OpsStatsEvent::Observability(event) = event else {
            panic!("expected observability event");
        };

        assert_eq!(event.metric_name, CONFIG_SYNC_FULL_FALLBACK_COUNT_METRIC);
        assert_eq!(event.value, 1.0);
        let tags = event.tags.unwrap();
        assert_eq!(
            tags.get(CONFIG_SYNC_OVERALL_SOURCE_API_TAG),
            Some(&"datastore".to_string())
        );
        assert_eq!(
            tags.get(CONFIG_SYNC_FULL_FALLBACK_REASON_TAG),
            Some(&"before_earliest_lcut".to_string())
        );
        assert_eq!(
            tags.get(CONFIG_SYNC_FULL_FALLBACK_SOURCE_TAG),
            Some(&"local_compute".to_string())
        );
        assert_eq!(
            tags.get(CONFIG_SYNC_FULL_FALLBACK_CURSOR_STATE_TAG),
            Some(&"incremental".to_string())
        );
    }

    #[test]
    fn full_fallback_counter_skips_other_sync_outcomes() {
        let ops_stats = Arc::new(OpsStatsForInstance::new());
        let mut receiver = ops_stats.subscribe_for_test();

        log_config_sync_full_fallback_count(
            &ops_stats,
            "datastore",
            false,
            "full",
            DeltaFallbackReason::MissingHeader,
            DeltaFallbackSource::MissingHeader,
            "initial",
        );
        log_config_sync_full_fallback_count(
            &ops_stats,
            "datastore",
            true,
            "delta",
            DeltaFallbackReason::MissingHeader,
            DeltaFallbackSource::MissingHeader,
            "initial",
        );
        log_config_sync_full_fallback_count(
            &ops_stats,
            "datastore",
            true,
            "no_update",
            DeltaFallbackReason::MissingHeader,
            DeltaFallbackSource::MissingHeader,
            "initial",
        );

        assert!(receiver.try_recv().is_err());
    }
}
