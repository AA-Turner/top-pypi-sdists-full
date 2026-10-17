use super::*;
use crate::observability::ops_stats::{OpsStatsEvent, OpsStatsForInstance};

#[test]
fn test_config_sync_response_type_delta() {
    let mut headers = HashMap::new();
    headers.insert("x-deltas-used".to_string(), "true".to_string());
    let mut data =
        ResponseData::from_bytes_with_headers(b"{\"has_updates\": false}".to_vec(), Some(headers));

    let response_type = ConfigSyncResponseType::from_response_data(&mut data);

    assert_eq!(response_type.as_str(), "delta");
}

#[test]
fn test_config_sync_response_type_no_update() {
    let mut data = ResponseData::from_bytes(b"{\"has_updates\": false}".to_vec());

    let response_type = ConfigSyncResponseType::from_response_data(&mut data);

    assert_eq!(response_type.as_str(), "no_update");
    let response = data.deserialize_into::<SpecsResponseNoUpdates>().unwrap();
    assert!(!response.has_updates);
}

#[test]
fn test_config_sync_response_type_no_update_with_delta_header() {
    let mut headers = HashMap::new();
    headers.insert("x-cache-hit".to_string(), "true".to_string());
    headers.insert("x-deltas-used".to_string(), "true".to_string());
    let mut data =
        ResponseData::from_bytes_with_headers(b"{\"has_updates\": false}".to_vec(), Some(headers));

    let response_type = ConfigSyncResponseType::from_response_data(&mut data);

    assert_eq!(response_type.as_str(), "no_update");
}

#[test]
fn test_config_sync_response_type_full() {
    let mut data = ResponseData::from_bytes(b"{\"has_updates\": true}".to_vec());

    let response_type = ConfigSyncResponseType::from_response_data(&mut data);

    assert_eq!(response_type.as_str(), "full");
}

#[test]
fn test_config_sync_response_type_full_for_non_json_payload() {
    let mut data = ResponseData::from_bytes(vec![0, 1, 2]);

    let response_type = ConfigSyncResponseType::from_response_data(&mut data);

    assert_eq!(response_type.as_str(), "full");
    let mut first_byte = [1];
    data.get_stream_mut().read_exact(&mut first_byte).unwrap();
    assert_eq!(first_byte, [0]);
}

#[test]
fn test_delta_fallback_headers_parse_to_typed_values() {
    let data = ResponseData::from_bytes_with_headers(
        vec![],
        Some(HashMap::from([
            (
                DELTA_FALLBACK_REASON_HEADER.to_string(),
                "before_earliest_lcut".to_string(),
            ),
            (
                DELTA_FALLBACK_SOURCE_HEADER.to_string(),
                "local_compute".to_string(),
            ),
        ])),
    );

    assert_eq!(
        get_delta_fallback_reason(&data),
        DeltaFallbackReason::BeforeEarliestLcut
    );
    assert_eq!(
        get_delta_fallback_source(&data),
        DeltaFallbackSource::LocalCompute
    );
}

#[test]
fn test_delta_fallback_headers_preserve_missing_and_invalid() {
    let missing = ResponseData::from_bytes(vec![]);
    assert_eq!(
        get_delta_fallback_reason(&missing),
        DeltaFallbackReason::MissingHeader
    );
    assert_eq!(
        get_delta_fallback_source(&missing),
        DeltaFallbackSource::MissingHeader
    );

    let invalid = ResponseData::from_bytes_with_headers(
        vec![],
        Some(HashMap::from([
            (
                DELTA_FALLBACK_REASON_HEADER.to_string(),
                "free_form_reason".to_string(),
            ),
            (
                DELTA_FALLBACK_SOURCE_HEADER.to_string(),
                "raw-unbounded-source".to_string(),
            ),
        ])),
    );
    assert_eq!(
        get_delta_fallback_reason(&invalid),
        DeltaFallbackReason::InvalidHeader
    );
    assert_eq!(
        get_delta_fallback_source(&invalid),
        DeltaFallbackSource::InvalidHeader
    );
}

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
