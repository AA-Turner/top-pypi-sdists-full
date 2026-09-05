use super::*;
use crate::interned_values::{
    InternedStore,
    interned_store::{MmapProjectId, preload_mmap_v2_multi_for_test, write_mmap_v2_for_test},
};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::specs_response::{
    proto_specs::{
        ProtobufHydrationContext, ProtobufUpdate, deserialize_protobuf,
        deserialize_protobuf_for_store_with_hydration,
    },
    proto_stream_reader::ProtoStreamReader,
    spec_types::SpecsResponseFull,
    statsig_config_specs::{self as pb, return_value},
};
use prost::Message;
use rusty_fork::rusty_fork_test;
use serde_json::Value;
use serial_test::serial;
use std::io::{Cursor, Read, Seek, SeekFrom, Write};
use std::sync::atomic::{AtomicUsize, Ordering};
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

#[tokio::test]
async fn response_hydration_budget_is_atomic_and_cancellation_safe() {
    let budget = Arc::new(ResponseHydrationBudget::new(12));
    let first = budget.reserve(8).await.unwrap();
    assert_eq!(budget.bytes.available_permits(), 4);

    let waiting_budget = Arc::clone(&budget);
    let waiting = tokio::spawn(async move { waiting_budget.reserve(8).await });
    tokio::task::yield_now().await;

    assert!(!waiting.is_finished());
    waiting.abort();
    assert!(waiting.await.unwrap_err().is_cancelled());
    assert_eq!(budget.bytes.available_permits(), 4);

    drop(first);
    assert_eq!(budget.bytes.available_permits(), 12);
    let complete = budget.reserve(12).await.unwrap();
    assert_eq!(budget.bytes.available_permits(), 0);
    drop(complete);
    assert_eq!(budget.bytes.available_permits(), 12);

    let saturated = budget.reserve(u64::MAX).await.unwrap();
    assert_eq!(saturated.num_permits(), 12);
    assert_eq!(budget.bytes.available_permits(), 0);
    drop(saturated);
    assert_eq!(budget.bytes.available_permits(), 12);
}

#[tokio::test]
async fn streaming_protobuf_charges_discovered_bytes_and_preserves_concurrent_mmap_reuse() {
    let budget = Arc::new(ResponseHydrationBudget::new(MAX_IN_FLIGHT_HYDRATION_BYTES));
    let mut hydrator = test_hydrator("streaming-response-budget");
    hydrator.response_budget = Arc::clone(&budget);
    let source_url = "https://statsigcdn.openai.com/v2/download_config_specs/key.json";

    let make_spec = |body: &[u8]| {
        let sha = lowercase_hex(&Sha256::digest(body));
        let spec = pb::Spec {
            default_value: Some(raw_return_value(
                serde_json::to_vec(&format!("{DOWNLOAD_PATH_PREFIX}{sha}")).unwrap(),
            )),
            remote_config_metadata: Some(protobuf_metadata(sha.clone(), body.len())),
            ..Default::default()
        };
        (spec, sha, Arc::new(body.to_vec()))
    };
    let (first_spec, first_sha, first_value) = make_spec(br#"{"value":"first"}"#);
    let (second_spec, second_sha, second_value) = make_spec(br#"{"value":"second"}"#);
    let first_bytes = first_value.len();
    let second_bytes = second_value.len();

    let mut first = hydrator.begin_protobuf_hydration(source_url);
    first.register_spec_references(&first_spec).unwrap();
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );
    assert!(first.seed_verified_values(HashMap::from([(
        first_sha.clone(),
        Arc::clone(&first_value),
    )])));
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES - first_bytes
    );

    let mut concurrent_scopes = Vec::new();
    for _ in 0..7 {
        let mut session = hydrator.begin_protobuf_hydration(source_url);
        session.register_spec_references(&first_spec).unwrap();
        assert!(session.seed_verified_values(HashMap::from([(
            first_sha.clone(),
            Arc::clone(&first_value),
        )])));
        concurrent_scopes.push(session);
    }
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES - first_bytes * 8,
        "small responses must not each reserve the entire response limit"
    );
    assert_eq!(
        budget.expansion.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );

    first.register_spec_references(&second_spec).unwrap();
    assert!(first.seed_verified_values(HashMap::from([(second_sha, second_value)])));
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES - first_bytes * 8 - second_bytes,
        "available base capacity should absorb small response growth"
    );
    assert_eq!(
        budget.expansion.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );

    first.finish(true);
    for session in concurrent_scopes {
        session.finish(true);
    }
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );
}

#[test]
fn validates_canonical_download_path() {
    let sha = "a".repeat(64);
    let result = resolve_and_validate_download_url(
        &format!("{DOWNLOAD_PATH_PREFIX}{sha}"),
        &sha,
        "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
    );
    assert_eq!(
        result.unwrap().as_str(),
        format!("https://statsigcdn.openai.com{DOWNLOAD_PATH_PREFIX}{sha}")
    );
}

#[test]
fn rejects_untrusted_download_origin() {
    let sha = "a".repeat(64);
    let result = resolve_and_validate_download_url(
        &format!("https://example.com{DOWNLOAD_PATH_PREFIX}{sha}"),
        &sha,
        "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
    );
    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with(
                "Dynamic config hydration failure: untrusted_download_origin:"
            )
    ));
}

#[test]
fn verifies_remote_value_body() {
    let body = br#"{"large":"value"}"#;
    let metadata = valid_metadata(lowercase_hex(&Sha256::digest(body)), body.len() as u64);
    verify_body(body, &metadata, "application/json; charset=utf-8").unwrap();
}

#[test]
fn bounded_body_read_stops_after_declared_length() {
    let bytes_read = Arc::new(AtomicUsize::new(0));
    let stream = CountingCursor {
        cursor: Cursor::new(vec![b'x'; 64]),
        bytes_read: bytes_read.clone(),
    };
    let mut data = ResponseData::from_stream(Box::new(stream));
    let metadata = valid_metadata("a".repeat(64), 4);

    let result = read_body_with_limit(&mut data, &metadata);

    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with(
                "Dynamic config hydration failure: byte_length_mismatch:"
            )
    ));
    assert_eq!(bytes_read.load(Ordering::SeqCst), 5);
}

#[tokio::test]
async fn rejects_oversized_remote_values_before_downloading() {
    let server = MockServer::start().await;
    let byte_length = MAX_REMOTE_VALUE_BYTES + 1;
    let sha = "a".repeat(64);
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    Mock::given(method("GET"))
        .respond_with(ResponseTemplate::new(200))
        .expect(0)
        .mount(&server)
        .await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "oversized": {
                "defaultValue": {"value": download_path},
                "remoteConfigMetadata": valid_json_metadata(&sha, byte_length),
                "rules": []
            }
        }
    });
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&payload).unwrap());
    let hydrator = test_hydrator("declared-byte-preflight");

    let result = hydrate_from_mock_source(&hydrator, &mut data, &server).await;

    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with(
                "Dynamic config hydration failure: total_bytes_exceeded:"
            )
    ));
    assert!(server.received_requests().await.unwrap().is_empty());
    server.verify().await;
}

#[test]
fn accepts_snapshot_values_larger_than_the_in_flight_hydration_budget() {
    let sha = "a".repeat(64);
    let metadata = valid_metadata(sha.clone(), MAX_REMOTE_VALUE_BYTES as u64);
    let occurrences = MAX_IN_FLIGHT_HYDRATION_BYTES / MAX_REMOTE_VALUE_BYTES + 1;
    let reference = RemoteValueReference {
        download_url: Url::parse(&format!(
            "https://statsigcdn.openai.com{DOWNLOAD_PATH_PREFIX}{sha}"
        ))
        .unwrap(),
        metadata,
        occurrences,
    };

    let (reference_count, total_bytes) =
        validate_reference_limits(std::iter::once(&reference)).unwrap();

    assert_eq!(reference_count, occurrences);
    assert_eq!(total_bytes, (MAX_REMOTE_VALUE_BYTES * occurrences) as u64);
    assert!(total_bytes > MAX_IN_FLIGHT_HYDRATION_BYTES as u64);
}

#[tokio::test]
#[serial]
async fn hydrates_many_bounded_references_across_dynamic_configs() {
    let server = MockServer::start().await;
    let rule_body = br#"{"value":"shared variant"}"#;
    let default_body = br#"{"value":"additional default"}"#;
    let rule_sha = lowercase_hex(&Sha256::digest(rule_body));
    let default_sha = lowercase_hex(&Sha256::digest(default_body));
    let rule_path = format!("{DOWNLOAD_PATH_PREFIX}{rule_sha}");
    let default_path = format!("{DOWNLOAD_PATH_PREFIX}{default_sha}");
    mount_json_blob(&server, &rule_path, rule_body, 1).await;
    mount_json_blob(&server, &default_path, default_body, 1).await;

    let mut configs = serde_json::Map::new();
    for config_index in 0..65 {
        let rules = (0..16)
            .map(|index| {
                serde_json::json!({
                    "id": format!("rule-{}:variant-{}", index / 4, index % 4),
                    "returnValue": {"value": rule_path},
                    "remoteConfigMetadata": valid_json_metadata(&rule_sha, rule_body.len())
                })
            })
            .collect::<Vec<_>>();
        configs.insert(
            format!("config-{config_index}"),
            serde_json::json!({"defaultValue": {}, "rules": rules}),
        );
    }
    configs.insert(
        "additional-config".to_string(),
        serde_json::json!({
            "defaultValue": {"value": default_path},
            "remoteConfigMetadata": valid_json_metadata(&default_sha, default_body.len()),
            "rules": []
        }),
    );

    let payload = serde_json::json!({"dynamic_configs": configs});
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&payload).unwrap());
    let hydrator = test_hydrator("many-bounded-config-values");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .expect("valid references across separately bounded configs should hydrate");

    let hydrated = data.deserialize_into::<Value>().unwrap();
    for config_index in 0..65 {
        let rules = hydrated["dynamic_configs"][format!("config-{config_index}")]["rules"]
            .as_array()
            .unwrap();
        assert_eq!(rules.len(), 16);
        for rule in rules {
            assert_eq!(
                rule["returnValue"],
                serde_json::json!({"value": "shared variant"})
            );
        }
    }
    assert_eq!(
        hydrated["dynamic_configs"]["additional-config"]["defaultValue"],
        serde_json::json!({"value": "additional default"})
    );
    assert_eq!(server.received_requests().await.unwrap().len(), 2);
}

#[test]
fn rejects_duplicate_occurrences_before_downloading() {
    let body = br#"{"large":"value"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_url = Url::parse(&format!(
        "https://statsigcdn.openai.com{DOWNLOAD_PATH_PREFIX}{sha}"
    ))
    .unwrap();
    let metadata = valid_metadata(sha, body.len() as u64);
    let metadata_bytes_per_occurrence = std::mem::size_of::<RemoteValueReference>()
        + download_url.as_str().len()
        + metadata.sha256.as_str().len()
        + metadata.content_type.as_str().len();
    let mut reference = RemoteValueReference {
        download_url,
        metadata,
        occurrences: MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC / metadata_bytes_per_occurrence,
    };

    assert!(validate_reference_limits(std::iter::once(&reference)).is_ok());
    reference.occurrences += 1;
    let result = validate_reference_limits(std::iter::once(&reference));

    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: too_many_values:")
    ));

    reference.occurrences = usize::MAX;
    let result = validate_reference_limits(std::iter::once(&reference));
    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: too_many_values:")
    ));
}

#[tokio::test]
async fn rejects_oversized_response_at_network_boundary() {
    let server = MockServer::start().await;
    let sha = "a".repeat(64);
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, b"too large", 1).await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": {"value": download_path},
                "remoteConfigMetadata": {
                    "sha256": sha,
                    "byteLength": 2,
                    "contentType": "application/json",
                    "compression": "none"
                },
                "rules": []
            }
        }
    });
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&payload).unwrap());
    let hydrator = test_hydrator("oversized-network-response");

    let result = hydrate_from_mock_source(&hydrator, &mut data, &server).await;

    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: download_failed:")
                && message.contains("Response exceeded maximum allowed bytes")
    ));
}

#[tokio::test]
async fn returns_on_first_download_failure_without_waiting_for_siblings() {
    let server = MockServer::start().await;
    let expected_failed_body = b"null";
    let failed_body = b"true";
    let slow_body = b"true";
    let failed_sha = lowercase_hex(&Sha256::digest(expected_failed_body));
    let slow_sha = lowercase_hex(&Sha256::digest(slow_body));
    let failed_path = format!("{DOWNLOAD_PATH_PREFIX}{failed_sha}");
    let slow_path = format!("{DOWNLOAD_PATH_PREFIX}{slow_sha}");

    Mock::given(method("GET"))
        .and(path(failed_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(failed_body),
        )
        .mount(&server)
        .await;
    Mock::given(method("GET"))
        .and(path(slow_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_delay(Duration::from_secs(5))
                .set_body_bytes(slow_body),
        )
        .mount(&server)
        .await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "failed": {
                "defaultValue": {"value": failed_path},
                "remoteConfigMetadata": valid_json_metadata(&failed_sha, expected_failed_body.len()),
                "rules": []
            },
            "slow": {
                "defaultValue": {"value": slow_path},
                "remoteConfigMetadata": valid_json_metadata(&slow_sha, slow_body.len()),
                "rules": []
            }
        }
    });
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&payload).unwrap());
    let hydrator = test_hydrator("fail-fast-downloads");

    let result = timeout(
        Duration::from_millis(1_500),
        hydrate_from_mock_source(&hydrator, &mut data, &server),
    )
    .await
    .expect("terminal download failure should cancel slow sibling downloads");

    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: checksum_mismatch:")
    ));
}

#[tokio::test]
async fn leaves_inline_json_stream_unchanged() {
    let original =
        br#"{"dynamic_configs":{"inline":{"defaultValue":{"large":"value"},"rules":[]}}}"#.to_vec();
    let bytes_read = Arc::new(AtomicUsize::new(0));
    let stream = CountingCursor {
        cursor: Cursor::new(original.clone()),
        bytes_read: bytes_read.clone(),
    };
    let mut data = ResponseData::from_stream(Box::new(stream));
    let hydrator = test_hydrator("inline-json");

    hydrator
        .hydrate_response(
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
        )
        .await
        .unwrap();

    let bytes_read_during_hydration = bytes_read.load(Ordering::SeqCst);
    assert_eq!(data.read_to_bytes().unwrap(), original);
    assert!(bytes_read.load(Ordering::SeqCst) > bytes_read_during_hydration);
}

#[tokio::test]
async fn no_metadata_json_does_not_log_hydration_outcome() {
    let ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut events = ops_stats.subscribe_for_test();
    let mut hydrator = RemoteConfigValueHydrator::new_with_ops_stats(
        Arc::new(NetworkClient::new("secret-key", None, None)),
        ops_stats,
    );
    let budget = Arc::new(ResponseHydrationBudget::new(1));
    let exhausted = budget.reserve(1).await.unwrap();
    hydrator.response_budget = Arc::clone(&budget);
    let mut data = ResponseData::from_bytes(br#"{"dynamic_configs":{}}"#.to_vec());

    hydrator
        .hydrate_response(
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
        )
        .await
        .unwrap();

    assert!(events.try_recv().is_err());
    assert!(hydrator.in_flight.get().is_none());
    assert_eq!(budget.bytes.available_permits(), 0);
    drop(exhausted);
}

#[tokio::test]
async fn leaves_non_object_json_marker_stream_unchanged() {
    let original = br#""remoteConfigMetadata""#.to_vec();
    let mut data = ResponseData::from_bytes(original.clone());
    let hydrator = test_hydrator("non-object-json-marker");

    hydrator
        .hydrate_response(
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
        )
        .await
        .unwrap();

    assert_eq!(data.read_to_bytes().unwrap(), original);
}

#[test]
fn finds_literal_json_metadata_key_across_scan_chunk_boundary() {
    let mut bytes = br#"{"padding":""#.to_vec();
    let key_prefix = br#"",""#;
    bytes.extend(std::iter::repeat_n(
        b'x',
        8 * 1024 - 5 - bytes.len() - key_prefix.len(),
    ));
    bytes.extend_from_slice(key_prefix);
    bytes.extend_from_slice(br#"remoteConfigMetadata":{}}"#);
    let mut data = ResponseData::from_bytes(bytes.clone());

    assert!(response_may_contain_remote_metadata(&mut data).unwrap());
    assert_eq!(data.read_to_bytes().unwrap(), bytes);
}

#[test]
fn finds_escaped_json_metadata_key_across_scan_chunk_boundary() {
    let mut bytes = br#"{"padding":""#.to_vec();
    let key_prefix = br#"",""#;
    bytes.extend(std::iter::repeat_n(
        b'x',
        8 * 1024 - 1 - bytes.len() - key_prefix.len(),
    ));
    bytes.extend_from_slice(key_prefix);
    bytes.extend_from_slice(br#"\u0072emoteConfigMetadata":{}}"#);
    let mut data = ResponseData::from_bytes(bytes.clone());

    assert!(response_may_contain_remote_metadata(&mut data).unwrap());
    assert_eq!(data.read_to_bytes().unwrap(), bytes);
}

#[tokio::test]
async fn unrelated_unicode_escape_stays_on_no_metadata_fast_path() {
    let mut original = br#"{"note":"\u0000","padding":""#.to_vec();
    original.extend(std::iter::repeat_n(b'x', 1024 * 1024));
    original.extend_from_slice(br#""}"#);
    let bytes_read = Arc::new(AtomicUsize::new(0));
    let stream = CountingCursor {
        cursor: Cursor::new(original.clone()),
        bytes_read: bytes_read.clone(),
    };
    let mut data = ResponseData::from_stream(Box::new(stream));
    let hydrator = test_hydrator("unrelated-unicode-fast-path");

    hydrator
        .hydrate_response(
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
        )
        .await
        .unwrap();

    assert_eq!(bytes_read.load(Ordering::SeqCst), original.len());
    assert_eq!(data.read_to_bytes().unwrap(), original);
}

#[test]
fn protobuf_metadata_probe_detects_default_metadata() {
    let spec = pb::Spec {
        remote_config_metadata: Some(pb::RemoteConfigValueMetadata::default()),
        ..Default::default()
    };

    assert!(protobuf_spec_has_remote_metadata(&spec.encode_to_vec()).unwrap());
}

#[test]
fn protobuf_metadata_probe_detects_rule_metadata() {
    let spec = pb::Spec {
        rules: vec![pb::Rule {
            remote_config_metadata: Some(pb::RemoteConfigValueMetadata::default()),
            ..Default::default()
        }],
        ..Default::default()
    };

    assert!(protobuf_spec_has_remote_metadata(&spec.encode_to_vec()).unwrap());
}

#[test]
fn protobuf_metadata_probe_ignores_tag_like_raw_value_bytes() {
    let spec = pb::Spec {
        default_value: Some(raw_return_value(vec![0x82, 0x01, 0x00])),
        ..Default::default()
    };

    assert!(!protobuf_spec_has_remote_metadata(&spec.encode_to_vec()).unwrap());
}

#[tokio::test]
async fn rejects_markerless_remote_metadata_without_downloading() {
    let server = MockServer::start().await;
    let body = br#"{"large":"proto"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 0).await;

    let metadata = protobuf_metadata(sha.clone(), body.len());
    let placeholder = serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap();
    let bytes = serialize_protobuf_envelopes(&[
        protobuf_top_level_envelope(None),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "remote_config".to_string(),
            data: Some(
                pb::Spec {
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(raw_return_value(placeholder)),
                    remote_config_metadata: Some(metadata),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        },
        protobuf_done_envelope(),
    ])
    .unwrap();
    let mut data = protobuf_response_data(bytes);
    let hydrator = test_hydrator("markerless-remote-metadata");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    assert!(data.get_prepared_protobuf_stream().is_none());
    assert_eq!(protobuf_top_level_marker(&mut data), None);

    let current_specs = crate::specs_response::spec_types::SpecsResponseFull::default();
    let mut next_specs = crate::specs_response::spec_types::SpecsResponseFull::default();
    let result = deserialize_protobuf_for_store_with_hydration(
        OPS_STATS
            .get_for_instance("markerless-remote-metadata-decode")
            .as_ref(),
        &current_specs,
        Default::default(),
        &mut next_specs,
        &mut data,
        ProtobufHydrationContext {
            hydrator: &hydrator,
            source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
            mmap_project_id: MmapProjectId::for_sdk_key("markerless-remote-metadata"),
            capture_hydrated_data_store_bytes: false,
            preserve_session_update_mode: false,
        },
    )
    .await;

    assert!(matches!(
        result,
        Err(StatsigErr::ProtobufParseError(tag, message))
            if tag == "proto::RemoteConfigMetadata"
                && message.contains("before hydration")
    ));
    assert!(next_specs.dynamic_configs.is_empty());
}

#[tokio::test]
async fn skips_markerless_delta_protobuf_without_scanning() {
    let original = serialize_protobuf_envelopes(&[
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..Default::default()
        },
        protobuf_top_level_envelope(None),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "malformed".to_string(),
            data: Some(vec![0xff]),
            ..Default::default()
        },
        protobuf_done_envelope(),
    ])
    .unwrap();
    let mut data = protobuf_response_data(original.clone());
    let hydrator = test_hydrator("markerless-delta");

    hydrator
        .hydrate_response(
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
        )
        .await
        .unwrap();

    assert_eq!(data.read_to_bytes().unwrap(), original);
    assert!(data.get_prepared_protobuf_stream().is_none());
}

#[tokio::test]
async fn skips_protobuf_scan_when_top_level_marker_is_false() {
    let original = serialize_protobuf_envelopes(&[
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..Default::default()
        },
        protobuf_top_level_envelope(Some(false)),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "invalid_if_scanned".to_string(),
            data: Some(vec![0xff]),
            ..Default::default()
        },
        protobuf_done_envelope(),
    ])
    .unwrap();
    let mut data = protobuf_response_data(original.clone());
    let hydrator = test_hydrator("protobuf-top-level-no-remote");

    hydrator
        .hydrate_response(
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
        )
        .await
        .unwrap();

    assert_eq!(data.read_to_bytes().unwrap(), original);
    assert!(data.get_prepared_protobuf_stream().is_none());
}

#[tokio::test]
async fn rejects_true_protobuf_marker_without_remote_metadata() {
    let hydrator = test_hydrator("protobuf-marker-without-metadata");

    for is_delta in [false, true] {
        let mut data = protobuf_response_data(protobuf_with_true_marker_without_metadata(is_delta));
        let result = hydrator
            .hydrate_response(
                &mut data,
                "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
            )
            .await;

        assert!(matches!(
            result,
            Err(StatsigErr::ProtobufParseError(tag, message))
                if tag == "proto::RemoteConfigMetadata"
                    && message.contains("marker was true")
        ));
        assert!(data.get_prepared_protobuf_stream().is_none());
    }
}

#[tokio::test]
async fn leaves_inline_protobuf_stream_unchanged() {
    let inline_spec = pb::Spec {
        default_value: Some(raw_return_value(br#"{"inline":true}"#.to_vec())),
        ..Default::default()
    };
    let original = serialize_protobuf_envelopes(&[
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "inline_config".to_string(),
            data: Some(inline_spec.encode_to_vec()),
            ..Default::default()
        },
        protobuf_done_envelope(),
    ])
    .unwrap();
    let (mut data, bytes_read) = counting_protobuf_response_data(original.clone());
    let hydrator = test_hydrator("inline-protobuf");

    hydrator
        .hydrate_response(
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
        )
        .await
        .unwrap();

    let bytes_read_during_hydration = bytes_read.load(Ordering::SeqCst);
    assert_eq!(data.read_to_bytes().unwrap(), original);
    assert!(data.get_prepared_protobuf_stream().is_none());
    assert!(bytes_read.load(Ordering::SeqCst) > bytes_read_during_hydration);
}

#[test]
fn json_hydration_removes_metadata_and_replaces_url() {
    let body = br#"{"large":"value"}"#.to_vec();
    let sha = lowercase_hex(&Sha256::digest(&body));
    let payload = format!(
        r#"{{"dynamic_configs":{{"large_config":{{"defaultValue":"https://statsigcdn.openai.com{DOWNLOAD_PATH_PREFIX}{sha}","remoteConfigMetadata":{{"sha256":"{sha}","byteLength":{byte_length},"contentType":"application/json","compression":"none"}},"rules":[]}}}}}}"#,
        byte_length = body.len(),
    );
    let hydrated = HashMap::from([(sha.clone(), Arc::new(body))]);

    let mut payload: RawJsonObject = serde_json::from_slice(payload.as_bytes()).unwrap();
    apply_json_hydration(&mut payload, &hydrated).unwrap();
    let payload: Value = serde_json::from_slice(&serde_json::to_vec(&payload).unwrap()).unwrap();

    assert_eq!(
        payload["dynamic_configs"]["large_config"]["defaultValue"],
        serde_json::json!({"large": "value"})
    );
    assert!(
        payload["dynamic_configs"]["large_config"]
            .get("remoteConfigMetadata")
            .is_none()
    );
}

#[tokio::test]
async fn json_hydration_preserves_number_lexemes() {
    let server = MockServer::start().await;
    // Negative zero catches a Value round-trip even when the test build
    // unifies serde_json's arbitrary_precision dev feature.
    let body =
        br#"{"remoteExponent":1e140,"remoteDecimal":0.123456789012345678901,"remoteNegativeZero":-0}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let placeholder_url = format!("{}{download_path}", server.uri());
    let payload = format!(
        r#"{{"dynamic_configs":{{"inline_config":{{"defaultValue":{{"inlineExponent":1e140,"inlineNegativeZero":-0}},"rules":[]}},"large_config":{{"defaultValue":"{placeholder_url}","lastModifiedTime":1e140,"negativeZero":-0,"remoteConfigMetadata":{{"sha256":"{sha}","byteLength":{byte_length},"contentType":"application/json","compression":"none"}},"rules":[]}}}}}}"#,
        byte_length = body.len(),
    );
    let mut data = ResponseData::from_bytes(payload.into_bytes());
    let hydrator = test_hydrator("json-number-lexemes");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    let hydrated = String::from_utf8(data.read_to_bytes().unwrap()).unwrap();
    assert!(hydrated.contains(r#""inlineExponent":1e140"#));
    assert!(hydrated.contains(r#""inlineNegativeZero":-0"#));
    assert!(hydrated.contains(r#""lastModifiedTime":1e140"#));
    assert!(hydrated.contains(r#""negativeZero":-0"#));
    assert!(hydrated.contains(r#""remoteExponent":1e140"#));
    assert!(hydrated.contains(r#""remoteDecimal":0.123456789012345678901"#));
    assert!(hydrated.contains(r#""remoteNegativeZero":-0"#));
}

#[tokio::test]
async fn hydrates_json_default_and_duplicate_rule_with_one_download() {
    let server = MockServer::start().await;
    let body = br#"{"large":"value"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let metadata = valid_json_metadata(&sha, body.len());
    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": format!("{}{download_path}", server.uri()),
                "remoteConfigMetadata": metadata,
                "rules": [{
                    "id": "rule",
                    "returnValue": {"value": download_path},
                    "remoteConfigMetadata": metadata
                }]
            }
        }
    });
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&payload).unwrap());
    let hydrator = test_hydrator("json-success");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    let hydrated: Value = data.deserialize_into().unwrap();
    assert_eq!(
        hydrated["dynamic_configs"]["large_config"]["defaultValue"],
        serde_json::json!({"large": "value"})
    );
    assert_eq!(
        hydrated["dynamic_configs"]["large_config"]["rules"][0]["returnValue"],
        serde_json::json!({"large": "value"})
    );
    assert!(
        hydrated["dynamic_configs"]["large_config"]
            .get("remoteConfigMetadata")
            .is_none()
    );
    assert!(
        hydrated["dynamic_configs"]["large_config"]["rules"][0]
            .get("remoteConfigMetadata")
            .is_none()
    );
}

#[tokio::test]
async fn hydrates_json_responses_larger_than_the_in_flight_budget() {
    let server = MockServer::start().await;
    let body = br#"{"large":"shared value"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let metadata = valid_json_metadata(&sha, body.len());
    let payload = serde_json::json!({
        "dynamic_configs": {
            "first": {
                "defaultValue": format!("{}{download_path}", server.uri()),
                "remoteConfigMetadata": metadata,
                "rules": [{
                    "id": "rule",
                    "returnValue": {"value": download_path},
                    "remoteConfigMetadata": metadata
                }]
            },
            "second": {
                "defaultValue": {"value": download_path},
                "remoteConfigMetadata": metadata,
                "rules": []
            }
        }
    });
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&payload).unwrap());
    let capacity = body.len() * 2;
    let budget = Arc::new(ResponseHydrationBudget::new(capacity));
    let mut hydrator = test_hydrator("json-saturated-response-budget");
    hydrator.response_budget = Arc::clone(&budget);

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    let hydrated: Value = data.deserialize_into().unwrap();
    let expected = serde_json::json!({"large": "shared value"});
    assert_eq!(
        hydrated["dynamic_configs"]["first"]["defaultValue"],
        expected
    );
    assert_eq!(
        hydrated["dynamic_configs"]["first"]["rules"][0]["returnValue"],
        expected
    );
    assert_eq!(
        hydrated["dynamic_configs"]["second"]["defaultValue"],
        expected
    );
    assert_eq!(budget.bytes.available_permits(), capacity);
    assert!(hydrator.in_flight_downloads().is_empty());
    server.verify().await;
}

#[tokio::test]
async fn hydrates_escaped_json_metadata_keys() {
    let server = MockServer::start().await;
    let body = br#"{"large":"value"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let metadata = valid_json_metadata(&sha, body.len());
    let payload = serde_json::to_string(&serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": format!("{}{download_path}", server.uri()),
                "remoteConfigMetadata": metadata,
                "rules": [{
                    "id": "rule",
                    "returnValue": {"value": download_path},
                    "remoteConfigMetadata": metadata
                }]
            }
        }
    }))
    .unwrap()
    .replace(
        r#""remoteConfigMetadata""#,
        r#""\u0072emoteConfigMetadata""#,
    );
    let mut data = ResponseData::from_bytes(payload.into_bytes());
    let hydrator = test_hydrator("escaped-json-metadata");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    let hydrated: Value = data.deserialize_into().unwrap();
    assert_eq!(
        hydrated["dynamic_configs"]["large_config"]["defaultValue"],
        serde_json::json!({"large": "value"})
    );
    assert_eq!(
        hydrated["dynamic_configs"]["large_config"]["rules"][0]["returnValue"],
        serde_json::json!({"large": "value"})
    );
    assert!(
        hydrated["dynamic_configs"]["large_config"]
            .get("remoteConfigMetadata")
            .is_none()
    );
    assert!(
        hydrated["dynamic_configs"]["large_config"]["rules"][0]
            .get("remoteConfigMetadata")
            .is_none()
    );
    server.verify().await;
}

#[tokio::test]
async fn coalesces_concurrent_remote_value_downloads_without_retaining_results() {
    let server = MockServer::start().await;
    let body = br#"{"large":"shared"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    Mock::given(method("GET"))
        .and(path(download_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_delay(Duration::from_millis(40))
                .set_body_bytes(body.to_vec()),
        )
        .expect(1)
        .mount(&server)
        .await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": format!("{}{download_path}", server.uri()),
                "remoteConfigMetadata": valid_json_metadata(&sha, body.len()),
                "rules": []
            }
        }
    });
    let bytes = serde_json::to_vec(&payload).unwrap();
    let mut first = ResponseData::from_bytes(bytes.clone());
    let mut second = ResponseData::from_bytes(bytes);
    let budget = Arc::new(ResponseHydrationBudget::new(body.len() * 2));
    let mut hydrator = test_hydrator("shared-concurrent-download");
    hydrator.response_budget = Arc::clone(&budget);

    let (first_result, second_result) = tokio::join!(
        hydrate_from_mock_source(&hydrator, &mut first, &server),
        hydrate_from_mock_source(&hydrator, &mut second, &server)
    );

    first_result.unwrap();
    second_result.unwrap();
    assert!(hydrator.in_flight_downloads().is_empty());
    assert_eq!(budget.bytes.available_permits(), body.len() * 2);
    server.verify().await;
}

#[tokio::test]
async fn json_hydration_waits_for_its_complete_response_byte_reservation() {
    let server = MockServer::start().await;
    let body = br#"{"large":"bounded"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": format!("{}{download_path}", server.uri()),
                "remoteConfigMetadata": valid_json_metadata(&sha, body.len()),
                "rules": []
            }
        }
    });
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&payload).unwrap());
    let budget = Arc::new(ResponseHydrationBudget::new(body.len()));
    let occupied = budget.reserve(body.len() as u64).await.unwrap();
    let mut hydrator = test_hydrator("json-response-budget");
    hydrator.response_budget = Arc::clone(&budget);
    let mut hydration = Box::pin(hydrate_from_mock_source(&hydrator, &mut data, &server));

    assert!(
        timeout(Duration::from_millis(25), hydration.as_mut())
            .await
            .is_err()
    );
    assert!(server.received_requests().await.unwrap().is_empty());

    drop(occupied);
    hydration.await.unwrap();
    assert_eq!(budget.bytes.available_permits(), body.len());
    assert!(hydrator.in_flight_downloads().is_empty());
    server.verify().await;
}

#[tokio::test]
async fn streaming_protobuf_keeps_its_response_reservation_after_download_completion() {
    let server = MockServer::start().await;
    let body = br#"{"large":"retained"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let budget = Arc::new(ResponseHydrationBudget::new(MAX_IN_FLIGHT_HYDRATION_BYTES));
    let occupied = budget
        .reserve(MAX_IN_FLIGHT_HYDRATION_BYTES as u64)
        .await
        .unwrap();
    let mut hydrator = test_hydrator("streaming-retained-response-budget");
    hydrator.response_budget = Arc::clone(&budget);
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
        ..Default::default()
    };
    let mut session = hydrator.begin_protobuf_hydration(&source_url);
    session.register_spec_references(&spec).unwrap();
    let mut hydration = Box::pin(session.download_registered_references());

    assert!(
        timeout(Duration::from_millis(25), hydration.as_mut())
            .await
            .is_err()
    );
    assert!(server.received_requests().await.unwrap().is_empty());

    drop(occupied);
    hydration.await.unwrap();
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES - body.len(),
        "a completed download must not release the budget while its body is retained"
    );
    assert_eq!(
        budget.expansion.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );

    session.finish(true);
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );
    assert!(hydrator.in_flight_downloads().is_empty());
    server.verify().await;
}

#[tokio::test]
async fn streaming_protobuf_grows_beyond_its_in_flight_hydration_budget() {
    let server = MockServer::start().await;
    let body = br#"{"large":"shared streaming value"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let capacity = body.len() * 2;
    let budget = Arc::new(ResponseHydrationBudget::new(capacity));
    let mut hydrator = test_hydrator("streaming-saturated-response-budget");
    hydrator.response_budget = Arc::clone(&budget);
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
        ..Default::default()
    };
    let mut session = hydrator.begin_protobuf_hydration(&source_url);

    session.register_spec_references(&spec).unwrap();
    session.download_registered_references().await.unwrap();
    assert_eq!(budget.bytes.available_permits(), capacity - body.len());

    session.register_spec_references(&spec).unwrap();
    session.download_registered_references().await.unwrap();
    assert_eq!(budget.bytes.available_permits(), 0);

    session.register_spec_references(&spec).unwrap();
    session.download_registered_references().await.unwrap();
    assert_eq!(budget.bytes.available_permits(), 0);

    let mut hydrated = spec.clone();
    session.apply_registered_spec(&mut hydrated).unwrap();
    assert_eq!(raw_return_value_bytes(&hydrated.default_value), body);
    assert_eq!(server.received_requests().await.unwrap().len(), 1);

    session.finish(true);
    assert_eq!(budget.bytes.available_permits(), capacity);
    assert!(hydrator.in_flight_downloads().is_empty());
    server.verify().await;
}

#[test]
fn streaming_protobuf_accepts_snapshots_larger_than_the_process_hydration_window() {
    let body = Arc::new(format!(r#"{{"large":"{}"}}"#, "x".repeat(1024 * 1024 - 12)).into_bytes());
    assert_eq!(body.len(), 1024 * 1024);
    let sha = lowercase_hex(&Sha256::digest(body.as_slice()));
    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{DOWNLOAD_PATH_PREFIX}{sha}")).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha.clone(), body.len())),
        ..Default::default()
    };
    let budget = Arc::new(ResponseHydrationBudget::new(MAX_IN_FLIGHT_HYDRATION_BYTES));
    let mut hydrator = test_hydrator("streaming-above-process-hydration-window");
    hydrator.response_budget = Arc::clone(&budget);
    let mut session = hydrator.begin_protobuf_hydration(
        "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
    );

    for _ in 0..65 {
        session.register_spec_references(&spec).unwrap();
    }
    assert!(body.len() * 65 > MAX_IN_FLIGHT_HYDRATION_BYTES);
    assert!(session.seed_verified_values(HashMap::from([(sha, Arc::clone(&body))])));
    assert_eq!(budget.bytes.available_permits(), 0);

    let mut hydrated = spec.clone();
    session.apply_registered_spec(&mut hydrated).unwrap();
    assert_eq!(
        raw_return_value_bytes(&hydrated.default_value),
        body.as_slice()
    );

    session.finish(true);
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );
    assert!(hydrator.in_flight_downloads().is_empty());
}

#[tokio::test]
async fn streaming_protobuf_scopes_share_downloads_under_separate_response_reservations() {
    let server = MockServer::start().await;
    let body = br#"{"large":"shared-streaming"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    Mock::given(method("GET"))
        .and(path(download_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_delay(Duration::from_millis(40))
                .set_body_bytes(body.to_vec()),
        )
        .expect(1)
        .mount(&server)
        .await;

    let scope_count = 4;
    let budget = Arc::new(ResponseHydrationBudget::new(body.len() * scope_count));
    let mut hydrator = test_hydrator("streaming-shared-response-budget");
    hydrator.response_budget = Arc::clone(&budget);
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
        ..Default::default()
    };
    let mut first = hydrator.begin_protobuf_hydration(&source_url);
    first.register_spec_references(&spec).unwrap();
    let mut second = hydrator.begin_protobuf_hydration(&source_url);
    second.register_spec_references(&spec).unwrap();
    let mut third = hydrator.begin_protobuf_hydration(&source_url);
    third.register_spec_references(&spec).unwrap();
    let mut fourth = hydrator.begin_protobuf_hydration(&source_url);
    fourth.register_spec_references(&spec).unwrap();

    let (first_result, second_result, third_result, fourth_result) = tokio::join!(
        first.download_registered_references(),
        second.download_registered_references(),
        third.download_registered_references(),
        fourth.download_registered_references()
    );
    first_result.unwrap();
    second_result.unwrap();
    third_result.unwrap();
    fourth_result.unwrap();
    assert_eq!(budget.bytes.available_permits(), 0);
    assert_eq!(
        budget.expansion.available_permits(),
        body.len() * scope_count
    );
    assert!(hydrator.in_flight_downloads().is_empty());

    first.finish(true);
    assert_eq!(budget.bytes.available_permits(), body.len());
    second.finish(true);
    third.finish(true);
    fourth.finish(true);
    assert_eq!(budget.bytes.available_permits(), body.len() * scope_count);
    server.verify().await;
}

#[tokio::test]
async fn streaming_protobuf_growth_uses_cancellation_safe_deadlock_free_expansion() {
    let server = MockServer::start().await;
    let first_body = br#"{"value":"first"}"#;
    let second_body = br#"{"value":"second-and-larger"}"#;
    let first_sha = lowercase_hex(&Sha256::digest(first_body));
    let second_sha = lowercase_hex(&Sha256::digest(second_body));
    let second_path = format!("{DOWNLOAD_PATH_PREFIX}{second_sha}");
    mount_json_blob(&server, &second_path, second_body, 1).await;

    let make_spec = |sha: &str, body: &[u8]| pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{}{DOWNLOAD_PATH_PREFIX}{sha}", server.uri())).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha.to_string(), body.len())),
        ..Default::default()
    };
    let first_spec = make_spec(&first_sha, first_body);
    let second_spec = make_spec(&second_sha, second_body);
    let budget = Arc::new(ResponseHydrationBudget::new(MAX_IN_FLIGHT_HYDRATION_BYTES));
    let mut hydrator = test_hydrator("streaming-growth-response-budget");
    hydrator.response_budget = Arc::clone(&budget);
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());

    let mut first = hydrator.begin_protobuf_hydration(&source_url);
    first.register_spec_references(&first_spec).unwrap();
    assert!(first.seed_verified_values(HashMap::from([(
        first_sha.clone(),
        Arc::new(first_body.to_vec()),
    )])));
    let mut second = hydrator.begin_protobuf_hydration(&source_url);
    second.register_spec_references(&first_spec).unwrap();
    assert!(
        second.seed_verified_values(HashMap::from([(first_sha, Arc::new(first_body.to_vec()),)]))
    );

    let occupied = budget
        .reserve((MAX_IN_FLIGHT_HYDRATION_BYTES - first_body.len() * 2) as u64)
        .await
        .unwrap();
    assert_eq!(budget.bytes.available_permits(), 0);

    first.register_spec_references(&second_spec).unwrap();
    assert!(first.seed_verified_values(HashMap::from([(
        second_sha.clone(),
        Arc::new(second_body.to_vec()),
    )])));
    assert_eq!(budget.expansion.available_permits(), first_body.len());

    second.register_spec_references(&second_spec).unwrap();
    assert!(!second.seed_verified_values(HashMap::from([(
        second_sha,
        Arc::new(second_body.to_vec()),
    )])));
    let mut waiting = Box::pin(second.download_registered_references());
    assert!(futures::poll!(waiting.as_mut()).is_pending());
    assert!(server.received_requests().await.unwrap().is_empty());
    drop(waiting);
    assert_eq!(
        budget.expansion.available_permits(),
        first_body.len(),
        "cancelling an expansion waiter must return its partially assigned permits"
    );

    let mut waiting = Box::pin(second.download_registered_references());
    assert!(futures::poll!(waiting.as_mut()).is_pending());
    first.finish(true);
    waiting.await.unwrap();
    assert_eq!(budget.bytes.available_permits(), first_body.len());
    assert_eq!(budget.expansion.available_permits(), first_body.len());

    second.finish(true);
    drop(occupied);
    assert_eq!(
        budget.bytes.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );
    assert_eq!(
        budget.expansion.available_permits(),
        MAX_IN_FLIGHT_HYDRATION_BYTES
    );
    assert!(hydrator.in_flight_downloads().is_empty());
    server.verify().await;
}

#[tokio::test]
async fn protobuf_compatibility_hydration_reserves_only_its_declared_response_bytes() {
    let server = MockServer::start().await;
    let body = br#"{"large":"compatibility"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
        ..Default::default()
    };
    let envelopes = [
        protobuf_top_level_envelope(Some(true)),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "bounded_config".to_string(),
            checksum: "bounded-checksum".to_string(),
            data: Some(spec.encode_to_vec()),
        },
        protobuf_done_envelope(),
    ];
    let mut data = protobuf_response_data(serialize_protobuf_envelopes(&envelopes).unwrap());
    let budget = Arc::new(ResponseHydrationBudget::new(body.len()));
    let occupied = budget.reserve(body.len() as u64).await.unwrap();
    let mut hydrator = test_hydrator("protobuf-compatibility-response-budget");
    hydrator.response_budget = Arc::clone(&budget);
    let mut hydration = Box::pin(hydrate_from_mock_source(&hydrator, &mut data, &server));

    assert!(
        timeout(Duration::from_millis(25), hydration.as_mut())
            .await
            .is_err()
    );
    assert!(server.received_requests().await.unwrap().is_empty());

    drop(occupied);
    hydration.await.unwrap();
    assert_eq!(budget.bytes.available_permits(), body.len());
    assert!(hydrator.in_flight_downloads().is_empty());
    assert!(data.get_prepared_protobuf_stream().is_some());
    server.verify().await;
}

#[tokio::test]
async fn protobuf_compatibility_hydrates_responses_larger_than_the_in_flight_budget() {
    let server = MockServer::start().await;
    let body = br#"{"large":"shared compatibility value"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
        ..Default::default()
    };
    let mut envelopes = vec![protobuf_top_level_envelope(Some(true))];
    for index in 0..3 {
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: format!("config-{index}"),
            checksum: format!("checksum-{index}"),
            data: Some(spec.encode_to_vec()),
        });
    }
    envelopes.push(protobuf_done_envelope());

    let mut data = protobuf_response_data(serialize_protobuf_envelopes(&envelopes).unwrap());
    let capacity = body.len() * 2;
    let budget = Arc::new(ResponseHydrationBudget::new(capacity));
    let mut hydrator = test_hydrator("protobuf-compatibility-saturated-response-budget");
    hydrator.response_budget = Arc::clone(&budget);

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    assert_eq!(budget.bytes.available_permits(), capacity);
    assert!(hydrator.in_flight_downloads().is_empty());
    assert!(data.get_prepared_protobuf_stream().is_some());
    server.verify().await;
}

#[tokio::test]
async fn does_not_share_remote_value_downloads_across_trusted_origins() {
    let first_server = MockServer::start().await;
    let second_server = MockServer::start().await;
    let body = br#"{"large":"origin-bound"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    for server in [&first_server, &second_server] {
        Mock::given(method("GET"))
            .and(path(download_path.clone()))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_delay(Duration::from_millis(40))
                    .set_body_bytes(body.to_vec()),
            )
            .expect(1)
            .mount(server)
            .await;
    }

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": {"value": download_path},
                "remoteConfigMetadata": valid_json_metadata(&sha, body.len()),
                "rules": []
            }
        }
    });
    let bytes = serde_json::to_vec(&payload).unwrap();
    let mut first = ResponseData::from_bytes(bytes.clone());
    let mut second = ResponseData::from_bytes(bytes);
    let hydrator = test_hydrator("origin-isolated-download");

    let (first_result, second_result) = tokio::join!(
        hydrate_from_mock_source(&hydrator, &mut first, &first_server),
        hydrate_from_mock_source(&hydrator, &mut second, &second_server)
    );

    first_result.unwrap();
    second_result.unwrap();
    assert!(hydrator.in_flight_downloads().is_empty());
    first_server.verify().await;
    second_server.verify().await;
}

#[tokio::test]
async fn retries_after_a_shared_remote_value_download_fails() {
    let server = MockServer::start().await;
    let expected_body = b"null";
    let invalid_body = b"true";
    let sha = lowercase_hex(&Sha256::digest(expected_body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    Mock::given(method("GET"))
        .and(path(download_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_delay(Duration::from_millis(40))
                .set_body_bytes(invalid_body.to_vec()),
        )
        .expect(1)
        .mount(&server)
        .await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": {"value": download_path},
                "remoteConfigMetadata": valid_json_metadata(&sha, expected_body.len()),
                "rules": []
            }
        }
    });
    let bytes = serde_json::to_vec(&payload).unwrap();
    let mut first = ResponseData::from_bytes(bytes.clone());
    let mut second = ResponseData::from_bytes(bytes.clone());
    let budget = Arc::new(ResponseHydrationBudget::new(expected_body.len() * 2));
    let mut hydrator = test_hydrator("failed-shared-download");
    hydrator.response_budget = Arc::clone(&budget);

    let (first_result, second_result) = tokio::join!(
        hydrate_from_mock_source(&hydrator, &mut first, &server),
        hydrate_from_mock_source(&hydrator, &mut second, &server)
    );

    assert!(matches!(
        first_result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: checksum_mismatch:")
    ));
    assert!(matches!(
        second_result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: checksum_mismatch:")
    ));
    assert!(hydrator.in_flight_downloads().is_empty());
    assert_eq!(budget.bytes.available_permits(), expected_body.len() * 2);
    server.verify().await;
    server.reset().await;
    mount_json_blob(&server, &download_path, expected_body, 1).await;

    let mut retried = ResponseData::from_bytes(bytes);
    hydrate_from_mock_source(&hydrator, &mut retried, &server)
        .await
        .unwrap();

    assert!(hydrator.in_flight_downloads().is_empty());
    assert_eq!(budget.bytes.available_permits(), expected_body.len() * 2);
    server.verify().await;
}

#[tokio::test]
async fn cancelled_shared_remote_download_allows_another_waiter_to_retry() {
    let server = MockServer::start().await;
    let body = br#"{"large":"survives-cancellation"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    Mock::given(method("GET"))
        .and(path(download_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_delay(Duration::from_millis(120))
                .set_body_bytes(body.to_vec()),
        )
        .expect(2)
        .mount(&server)
        .await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": {"value": download_path},
                "remoteConfigMetadata": valid_json_metadata(&sha, body.len()),
                "rules": []
            }
        }
    });
    let bytes = serde_json::to_vec(&payload).unwrap();
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let budget = Arc::new(ResponseHydrationBudget::new(body.len() * 2));
    let mut hydrator = test_hydrator("cancelled-shared-download");
    hydrator.response_budget = Arc::clone(&budget);
    let hydrator = Arc::new(hydrator);
    let first_hydrator = Arc::clone(&hydrator);
    let first_source = source_url.clone();
    let first_bytes = bytes.clone();
    let first = tokio::spawn(async move {
        let mut data = ResponseData::from_bytes(first_bytes);
        first_hydrator
            .hydrate_response(&mut data, &first_source)
            .await
    });

    timeout(Duration::from_secs(2), async {
        loop {
            if server
                .received_requests()
                .await
                .is_some_and(|requests| !requests.is_empty())
            {
                break;
            }
            tokio::task::yield_now().await;
        }
    })
    .await
    .expect("the first shared download should reach its origin");

    let second_hydrator = Arc::clone(&hydrator);
    let second = tokio::spawn(async move {
        let mut data = ResponseData::from_bytes(bytes);
        second_hydrator
            .hydrate_response(&mut data, &source_url)
            .await
    });
    timeout(Duration::from_secs(2), async {
        loop {
            if hydrator
                .in_flight_downloads()
                .iter()
                .any(|entry| entry.waiters.load(Ordering::Acquire) == 2)
            {
                break;
            }
            tokio::task::yield_now().await;
        }
    })
    .await
    .expect("the second scope should join the active download");
    assert_eq!(budget.bytes.available_permits(), 0);

    first.abort();
    assert!(first.await.unwrap_err().is_cancelled());
    second.await.unwrap().unwrap();

    assert!(hydrator.in_flight_downloads().is_empty());
    assert_eq!(budget.bytes.available_permits(), body.len() * 2);
    server.verify().await;
}

#[tokio::test]
async fn does_not_retain_remote_values_across_responses() {
    let server = MockServer::start().await;
    let body = br#"{"large":"value"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 2).await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": format!("{}{download_path}", server.uri()),
                "remoteConfigMetadata": valid_json_metadata(&sha, body.len()),
                "rules": []
            }
        }
    });
    let bytes = serde_json::to_vec(&payload).unwrap();
    let hydrator = test_hydrator("json-no-persistent-cache");

    for _ in 0..2 {
        let mut data = ResponseData::from_bytes(bytes.clone());
        hydrate_from_mock_source(&hydrator, &mut data, &server)
            .await
            .unwrap();
    }
}

#[tokio::test]
async fn failed_json_hydration_does_not_modify_candidate() {
    let server = MockServer::start().await;
    let body = br#"{"large":"value"}"#;
    let sha = "a".repeat(64);
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let payload = serde_json::json!({
        "dynamic_configs": {
            "large_config": {
                "defaultValue": format!("{}{download_path}", server.uri()),
                "remoteConfigMetadata": valid_json_metadata(&sha, body.len()),
                "rules": []
            }
        }
    });
    let original = serde_json::to_vec(&payload).unwrap();
    let mut data = ResponseData::from_bytes(original.clone());
    let hydrator = test_hydrator("json-failure");

    let result = hydrate_from_mock_source(&hydrator, &mut data, &server).await;

    assert!(matches!(
        result,
        Err(StatsigErr::CustomError(message))
            if message.starts_with("Dynamic config hydration failure: checksum_mismatch:")
    ));
    assert_eq!(data.read_to_bytes().unwrap(), original);
}

#[tokio::test]
async fn hydrates_protobuf_default_and_rule_values() {
    let server = MockServer::start().await;
    let body = br#"{"large":"proto"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let metadata = protobuf_metadata(sha.clone(), body.len());
    let placeholder = serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap();
    let spec = pb::Spec {
        default_value: Some(raw_return_value(placeholder.clone())),
        remote_config_metadata: Some(metadata.clone()),
        rules: vec![pb::Rule {
            return_value: Some(raw_return_value(placeholder)),
            remote_config_metadata: Some(metadata),
            ..Default::default()
        }],
        ..Default::default()
    };
    let envelopes = vec![
        protobuf_top_level_envelope(Some(true)),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "large_config".to_string(),
            checksum: "checksum".to_string(),
            data: Some(spec.encode_to_vec()),
        },
        protobuf_done_envelope(),
    ];
    let bytes = serialize_protobuf_envelopes(&envelopes).unwrap();
    let original_bytes = bytes.clone();
    let (mut data, bytes_read) = counting_protobuf_response_data(bytes);
    let hydrator = test_hydrator("proto-success");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    assert_eq!(data.read_to_bytes().unwrap(), original_bytes);
    assert!(data.get_prepared_protobuf_stream().is_some());
    let original_stream_reads = bytes_read.load(Ordering::SeqCst);
    assert_eq!(protobuf_top_level_marker(&mut data), Some(false));
    let hydrated_envelopes = parse_protobuf_envelopes(&mut data).unwrap();
    let hydrated_dynamic_config = hydrated_envelopes
        .iter()
        .find(|envelope| {
            pb::SpecsEnvelopeKind::try_from(envelope.kind).ok()
                == Some(pb::SpecsEnvelopeKind::DynamicConfig)
        })
        .unwrap();
    let hydrated_spec = pb::Spec::decode(hydrated_dynamic_config.data.as_deref().unwrap()).unwrap();
    assert!(hydrated_spec.remote_config_metadata.is_none());
    assert!(hydrated_spec.rules[0].remote_config_metadata.is_none());
    assert_eq!(
        raw_return_value_bytes(&hydrated_spec.default_value),
        body.as_slice()
    );
    assert_eq!(
        raw_return_value_bytes(&hydrated_spec.rules[0].return_value),
        body.as_slice()
    );
    assert_eq!(bytes_read.load(Ordering::SeqCst), original_stream_reads);
}

#[tokio::test]
#[serial]
async fn store_parser_hydrates_protobuf_once_and_reuses_values_within_update() {
    let server = MockServer::start().await;
    let body = br#"{"large":"single-pass"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let metadata = protobuf_metadata(sha.clone(), body.len());
    let placeholder = serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap();
    let top_level = pb::SpecsTopLevel {
        has_updates: true,
        time: 1,
        company_id: "company".to_string(),
        response_format: "dcs-v2".to_string(),
        checksum: "response-checksum".to_string(),
        rest: br#"{"experiment_to_layer":{},"condition_map":{}}"#.to_vec(),
        may_have_remote_config_metadata: Some(true),
    };
    let bytes = serialize_protobuf_envelopes(&[
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(top_level.encode_to_vec()),
            ..Default::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "large_config".to_string(),
            checksum: "config-checksum".to_string(),
            data: Some(
                pb::Spec {
                    salt: "salt".to_string(),
                    enabled: true,
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(raw_return_value(placeholder.clone())),
                    remote_config_metadata: Some(metadata.clone()),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "second_config".to_string(),
            checksum: "second-config-checksum".to_string(),
            data: Some(
                pb::Spec {
                    salt: "second-salt".to_string(),
                    enabled: true,
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(raw_return_value(placeholder)),
                    remote_config_metadata: Some(metadata),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        },
        protobuf_done_envelope(),
    ])
    .unwrap();
    let compressed_len = bytes.len();
    let (mut data, bytes_read) = counting_protobuf_response_data(bytes);
    let hydrator = test_hydrator("single-pass-store-parser");
    let current_specs = SpecsResponseFull::default();
    let mut next_specs = SpecsResponseFull::default();

    let (update, _, _) = deserialize_protobuf_for_store_with_hydration(
        OPS_STATS
            .get_for_instance("single-pass-store-parser-decode")
            .as_ref(),
        &current_specs,
        Default::default(),
        &mut next_specs,
        &mut data,
        ProtobufHydrationContext {
            hydrator: &hydrator,
            source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
            mmap_project_id: MmapProjectId::for_sdk_key("single-pass-store-parser"),
            capture_hydrated_data_store_bytes: false,
            preserve_session_update_mode: false,
        },
    )
    .await
    .unwrap();

    assert_eq!(update, ProtobufUpdate::Materialized { is_delta: false });
    assert!(data.get_prepared_protobuf_stream().is_none());
    assert!(
        bytes_read.load(Ordering::SeqCst) <= compressed_len,
        "protobuf source was read more than once"
    );
    let next_json = serde_json::to_value(&next_specs).unwrap();
    assert_eq!(
        next_json["dynamic_configs"]["large_config"]["defaultValue"]["large"],
        serde_json::json!("single-pass")
    );
    assert_eq!(
        next_json["dynamic_configs"]["second_config"]["defaultValue"]["large"],
        serde_json::json!("single-pass")
    );
}

#[tokio::test]
async fn store_parser_reuses_non_remote_dynamic_configs_with_or_without_sidecar_capture() {
    let response = |marker| {
        serialize_protobuf_envelopes(&[
            protobuf_top_level_envelope(marker),
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
                name: "reused_config".to_string(),
                checksum: "reused-checksum".to_string(),
                data: Some(
                    pb::Spec {
                        salt: "salt".to_string(),
                        enabled: true,
                        entity: pb::EntityType::EntityDynamicConfig as i32,
                        ..Default::default()
                    }
                    .encode_to_vec(),
                ),
            },
            protobuf_done_envelope(),
        ])
        .unwrap()
    };
    let ops_stats = OPS_STATS.get_for_instance("reused-config-decode-stats");
    let mut current_data = protobuf_response_data(response(Some(false)));
    let mut current_specs = SpecsResponseFull::default();
    deserialize_protobuf(
        ops_stats.as_ref(),
        &SpecsResponseFull::default(),
        &mut current_specs,
        &mut current_data,
    )
    .unwrap();
    let hydrator = test_hydrator("reused-config-decode-stats");

    for capture_sidecar in [false, true] {
        let mut data = protobuf_response_data(response(Some(false)));
        let mut next_specs = SpecsResponseFull::default();

        let (update, stats, hydrated_data_store_bytes) =
            deserialize_protobuf_for_store_with_hydration(
                ops_stats.as_ref(),
                &current_specs,
                Default::default(),
                &mut next_specs,
                &mut data,
                ProtobufHydrationContext {
                    hydrator: &hydrator,
                    source_url: "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
                    mmap_project_id: MmapProjectId::for_sdk_key("reused-config-decode-stats"),
                    capture_hydrated_data_store_bytes: capture_sidecar,
                    preserve_session_update_mode: false,
                },
            )
            .await
            .unwrap();

        assert_eq!(update, ProtobufUpdate::Materialized { is_delta: false });
        assert_eq!(stats.total, 1);
        assert_eq!(stats.mmap, 0);
        assert!(hydrated_data_store_bytes.is_none());
    }
}

#[tokio::test]
async fn store_parser_rejects_true_marker_without_remote_metadata() {
    let hydrator = test_hydrator("store-marker-without-metadata");
    let current_specs = SpecsResponseFull::default();

    for (is_delta, capture_sidecar) in [(false, false), (true, true)] {
        let bytes = protobuf_with_true_marker_without_metadata(is_delta);
        let compressed_len = bytes.len();
        let (mut data, bytes_read) = counting_protobuf_response_data(bytes);
        let mut next_specs = SpecsResponseFull::default();

        let result = deserialize_protobuf_for_store_with_hydration(
            OPS_STATS
                .get_for_instance("store-marker-without-metadata-decode")
                .as_ref(),
            &current_specs,
            Default::default(),
            &mut next_specs,
            &mut data,
            ProtobufHydrationContext {
                hydrator: &hydrator,
                source_url: "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
                mmap_project_id: MmapProjectId::for_sdk_key("store-marker-without-metadata"),
                capture_hydrated_data_store_bytes: capture_sidecar,
                preserve_session_update_mode: false,
            },
        )
        .await;

        assert!(matches!(
            result,
            Err(StatsigErr::ProtobufParseError(tag, message))
                if tag == "proto::RemoteConfigMetadata"
                    && message.contains("marker was true")
        ));
        assert!(data.get_prepared_protobuf_stream().is_none());
        assert!(
            bytes_read.load(Ordering::SeqCst) <= compressed_len,
            "protobuf source was read more than once"
        );
    }
}

#[tokio::test]
async fn store_parser_reuses_verified_hydrated_current_values_without_downloading() {
    let server = MockServer::start().await;
    let default_body = br#"{"default":"hydrated"}"#;
    let rule_body = br#"{"rule":"hydrated"}"#;
    let default_sha = lowercase_hex(&Sha256::digest(default_body));
    let rule_sha = lowercase_hex(&Sha256::digest(rule_body));
    let default_path = format!("{DOWNLOAD_PATH_PREFIX}{default_sha}");
    let rule_path = format!("{DOWNLOAD_PATH_PREFIX}{rule_sha}");
    mount_json_blob(&server, &default_path, default_body, 0).await;
    mount_json_blob(&server, &rule_path, rule_body, 0).await;

    let response = |remote: bool| {
        serialize_protobuf_envelopes(&[
            protobuf_top_level_envelope(Some(remote)),
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
                name: "large_config".to_string(),
                checksum: "same-checksum".to_string(),
                data: Some(
                    pb::Spec {
                        enabled: true,
                        entity: pb::EntityType::EntityDynamicConfig as i32,
                        default_value: Some(raw_return_value(if remote {
                            serde_json::to_vec(&serde_json::json!({"value": default_path})).unwrap()
                        } else {
                            default_body.to_vec()
                        })),
                        remote_config_metadata: remote
                            .then(|| protobuf_metadata(&default_sha, default_body.len())),
                        rules: vec![pb::Rule {
                            id: "rule-id".to_string(),
                            return_value: Some(raw_return_value(if remote {
                                serde_json::to_vec(&serde_json::json!({"value": rule_path}))
                                    .unwrap()
                            } else {
                                rule_body.to_vec()
                            })),
                            remote_config_metadata: remote
                                .then(|| protobuf_metadata(&rule_sha, rule_body.len())),
                            ..Default::default()
                        }],
                        ..Default::default()
                    }
                    .encode_to_vec(),
                ),
            },
            protobuf_done_envelope(),
        ])
        .unwrap()
    };
    let ops_stats = OPS_STATS.get_for_instance("verified-current-reuse");
    let mut current_data = protobuf_response_data(response(false));
    let mut current_specs = SpecsResponseFull::default();
    deserialize_protobuf(
        ops_stats.as_ref(),
        &SpecsResponseFull::default(),
        &mut current_specs,
        &mut current_data,
    )
    .unwrap();
    let current_pointer = current_specs
        .dynamic_configs
        .0
        .values()
        .next()
        .unwrap()
        .clone()
        .into_pointer()
        .unwrap();
    let hydrator = test_hydrator("verified-current-reuse");

    for capture_sidecar in [false, true] {
        let mut data = protobuf_response_data(response(true));
        let mut next_specs = SpecsResponseFull::default();
        let (_, _, sidecar) = deserialize_protobuf_for_store_with_hydration(
            ops_stats.as_ref(),
            &current_specs,
            Default::default(),
            &mut next_specs,
            &mut data,
            ProtobufHydrationContext {
                hydrator: &hydrator,
                source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
                mmap_project_id: MmapProjectId::for_sdk_key("verified-current-reuse"),
                capture_hydrated_data_store_bytes: capture_sidecar,
                preserve_session_update_mode: false,
            },
        )
        .await
        .unwrap();

        let next_pointer = next_specs
            .dynamic_configs
            .0
            .values()
            .next()
            .unwrap()
            .clone()
            .into_pointer()
            .unwrap();
        assert!(Arc::ptr_eq(&current_pointer, &next_pointer));
        assert_eq!(sidecar.is_some(), capture_sidecar);
        if let Some(sidecar) = sidecar {
            let mut sidecar_data = protobuf_response_data(sidecar);
            assert_eq!(protobuf_top_level_marker(&mut sidecar_data), Some(false));
            let sidecar_spec = parse_protobuf_envelopes(&mut sidecar_data)
                .unwrap()
                .into_iter()
                .find(|envelope| envelope.name == "large_config")
                .and_then(|envelope| envelope.data)
                .map(|bytes| pb::Spec::decode(bytes.as_slice()).unwrap())
                .unwrap();
            assert!(sidecar_spec.remote_config_metadata.is_none());
            assert!(sidecar_spec.rules[0].remote_config_metadata.is_none());
            assert_eq!(
                raw_return_value_bytes(&sidecar_spec.default_value),
                default_body.as_slice()
            );
            assert_eq!(
                raw_return_value_bytes(&sidecar_spec.rules[0].return_value),
                rule_body.as_slice()
            );
        }
    }

    server.verify().await;
}

#[tokio::test]
async fn store_parser_downloads_when_hydrated_value_cannot_reconstruct_wire_bytes() {
    let server = MockServer::start().await;
    // Parsing an archived/current returnable discards this insignificant
    // whitespace, so its serialization cannot satisfy the producer's exact
    // authenticated bytes.
    let body = br#"{ "large": "hydrated" }"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let response = |remote: bool| {
        serialize_protobuf_envelopes(&[
            protobuf_top_level_envelope(Some(remote)),
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
                name: "large_config".to_string(),
                checksum: "same-checksum".to_string(),
                data: Some(
                    pb::Spec {
                        enabled: true,
                        entity: pb::EntityType::EntityDynamicConfig as i32,
                        default_value: Some(raw_return_value(if remote {
                            serde_json::to_vec(&serde_json::json!({"value": download_path}))
                                .unwrap()
                        } else {
                            body.to_vec()
                        })),
                        remote_config_metadata: remote.then(|| protobuf_metadata(&sha, body.len())),
                        ..Default::default()
                    }
                    .encode_to_vec(),
                ),
            },
            protobuf_done_envelope(),
        ])
        .unwrap()
    };
    let ops_stats = OPS_STATS.get_for_instance("unreconstructable-current-value");
    let mut current_data = protobuf_response_data(response(false));
    let mut current_specs = SpecsResponseFull::default();
    deserialize_protobuf(
        ops_stats.as_ref(),
        &SpecsResponseFull::default(),
        &mut current_specs,
        &mut current_data,
    )
    .unwrap();
    let mut data = protobuf_response_data(response(true));
    let mut next_specs = SpecsResponseFull::default();
    let hydrator = test_hydrator("unreconstructable-current-value");

    deserialize_protobuf_for_store_with_hydration(
        ops_stats.as_ref(),
        &current_specs,
        Default::default(),
        &mut next_specs,
        &mut data,
        ProtobufHydrationContext {
            hydrator: &hydrator,
            source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
            mmap_project_id: MmapProjectId::for_sdk_key("unreconstructable-current-value"),
            capture_hydrated_data_store_bytes: false,
            preserve_session_update_mode: false,
        },
    )
    .await
    .unwrap();

    let next_json = serde_json::to_value(&next_specs).unwrap();
    assert_eq!(
        next_json["dynamic_configs"]["large_config"]["defaultValue"],
        serde_json::json!({"large": "hydrated"})
    );
    server.verify().await;
}

#[tokio::test]
async fn store_parser_does_not_reuse_matching_placeholder_config() {
    let server = MockServer::start().await;
    let body = br#"{"large":"hydrated"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;
    let placeholder = serde_json::to_vec(&serde_json::json!({
        "value": download_path,
    }))
    .unwrap();
    let response = |metadata: Option<pb::RemoteConfigValueMetadata>| {
        let has_remote_metadata = metadata.is_some();
        serialize_protobuf_envelopes(&[
            protobuf_top_level_envelope(Some(has_remote_metadata)),
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
                name: "large_config".to_string(),
                checksum: "same-checksum".to_string(),
                data: Some(
                    pb::Spec {
                        enabled: true,
                        entity: pb::EntityType::EntityDynamicConfig as i32,
                        default_value: Some(raw_return_value(placeholder.clone())),
                        remote_config_metadata: metadata,
                        ..Default::default()
                    }
                    .encode_to_vec(),
                ),
            },
            protobuf_done_envelope(),
        ])
        .unwrap()
    };
    let ops_stats = OPS_STATS.get_for_instance("placeholder-reuse");
    let mut current_data = protobuf_response_data(response(None));
    let mut current_specs = SpecsResponseFull::default();
    deserialize_protobuf(
        ops_stats.as_ref(),
        &SpecsResponseFull::default(),
        &mut current_specs,
        &mut current_data,
    )
    .unwrap();
    let mut data = protobuf_response_data(response(Some(protobuf_metadata(sha, body.len()))));
    let mut next_specs = SpecsResponseFull::default();
    let hydrator = test_hydrator("placeholder-reuse");

    deserialize_protobuf_for_store_with_hydration(
        ops_stats.as_ref(),
        &current_specs,
        Default::default(),
        &mut next_specs,
        &mut data,
        ProtobufHydrationContext {
            hydrator: &hydrator,
            source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
            mmap_project_id: MmapProjectId::for_sdk_key("placeholder-reuse"),
            capture_hydrated_data_store_bytes: false,
            preserve_session_update_mode: false,
        },
    )
    .await
    .unwrap();

    let next_json = serde_json::to_value(&next_specs).unwrap();
    assert_eq!(
        next_json["dynamic_configs"]["large_config"]["defaultValue"],
        serde_json::json!({"large": "hydrated"})
    );
    server.verify().await;
}

rusty_fork_test! {
    #[test]
    fn store_parser_reuses_verified_hydrated_mmap_without_downloading() {
        tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .unwrap()
            .block_on(async {
                const SDK_KEY: &str = "verified-hydrated-mmap-reuse";
                assert!(!InternedStore::has_preloaded_mmap_v2());

                let server = MockServer::start().await;
                let body = br#"{"large":"hydrated"}"#;
                let sha = lowercase_hex(&Sha256::digest(body));
                let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
                mount_json_blob(&server, &download_path, body, 0).await;

                let baseline = serde_json::to_vec(&serde_json::json!({
                    "experiment_to_layer": {},
                    "condition_map": {},
                    "dynamic_configs": {
                        "large_config": {
                            "checksum": "same-checksum",
                            "type": "dynamic_config",
                            "salt": "",
                            "defaultValue": {"large": "hydrated"},
                            "enabled": true,
                            "rules": [],
                            "idType": "userID",
                            "entity": "dynamic_config"
                        }
                    },
                    "feature_gates": {},
                    "layer_configs": {},
                    "has_updates": true,
                    "time": 1
                }))
                .unwrap();
                let directory = tempfile::tempdir().unwrap();
                let path = directory.path().join("already-hydrated.mmap");
                write_mmap_v2_for_test(&baseline, &path).unwrap();
                preload_mmap_v2_multi_for_test(&[(SDK_KEY, &path)]).unwrap();

                let live_response = serialize_protobuf_envelopes(&[
                    protobuf_top_level_envelope(Some(true)),
                    pb::SpecsEnvelope {
                        kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
                        name: "large_config".to_string(),
                        checksum: "same-checksum".to_string(),
                        data: Some(
                            pb::Spec {
                                enabled: true,
                                entity: pb::EntityType::EntityDynamicConfig as i32,
                                default_value: Some(raw_return_value(
                                    serde_json::to_vec(&serde_json::json!({
                                        "value": download_path,
                                    }))
                                    .unwrap(),
                                )),
                                remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
                                ..Default::default()
                            }
                            .encode_to_vec(),
                        ),
                    },
                    protobuf_done_envelope(),
                ])
                .unwrap();
                let mut data = protobuf_response_data(live_response);
                let mut next_specs = SpecsResponseFull::default();
                let hydrator = test_hydrator(SDK_KEY);

                deserialize_protobuf_for_store_with_hydration(
                    OPS_STATS.get_for_instance(SDK_KEY).as_ref(),
                    &SpecsResponseFull::default(),
                    Default::default(),
                    &mut next_specs,
                    &mut data,
                    ProtobufHydrationContext {
                        hydrator: &hydrator,
                        source_url: &format!(
                            "{}/v2/download_config_specs/key.json",
                            server.uri()
                        ),
                        mmap_project_id: MmapProjectId::for_sdk_key(SDK_KEY),
                        capture_hydrated_data_store_bytes: false,
                        preserve_session_update_mode: false,
                    },
                )
                .await
                .unwrap();

                let config = next_specs
                    .dynamic_configs
                    .0
                    .values()
                    .next()
                    .expect("hydrated mmap config should be reused");
                assert!(config.is_mmap(), "verified config must remain mmap-backed");
                let next_json = serde_json::to_value(&next_specs).unwrap();
                assert_eq!(
                    next_json["dynamic_configs"]["large_config"]["defaultValue"],
                    serde_json::json!({"large": "hydrated"})
                );
                server.verify().await;
            });
    }

    #[test]
    fn store_parser_replays_hydrated_sidecar_over_same_checksum_mmap_placeholder() {
        tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .unwrap()
            .block_on(async {
                const SDK_KEY: &str = "hydrated-sidecar-stale-mmap";
                assert!(!InternedStore::has_preloaded_mmap_v2());

                let server = MockServer::start().await;
                let body = br#"{"large":"hydrated"}"#;
                let sha = lowercase_hex(&Sha256::digest(body));
                let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
                mount_json_blob(&server, &download_path, body, 1).await;
                let placeholder = serde_json::json!({"value": download_path});
                let live_response = serialize_protobuf_envelopes(&[
                    protobuf_top_level_envelope(Some(true)),
                    pb::SpecsEnvelope {
                        kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
                        name: "large_config".to_string(),
                        checksum: "same-checksum".to_string(),
                        data: Some(
                            pb::Spec {
                                enabled: true,
                                entity: pb::EntityType::EntityDynamicConfig as i32,
                                default_value: Some(raw_return_value(
                                    serde_json::to_vec(&placeholder).unwrap(),
                                )),
                                remote_config_metadata: Some(protobuf_metadata(
                                    sha,
                                    body.len(),
                                )),
                                ..Default::default()
                            }
                            .encode_to_vec(),
                        ),
                    },
                    protobuf_done_envelope(),
                ])
                .unwrap();
                let hydrator = test_hydrator(SDK_KEY);
                let ops_stats = OPS_STATS.get_for_instance(SDK_KEY);
                let mut leader_data = protobuf_response_data(live_response);
                let mut leader_specs = SpecsResponseFull::default();
                let (_, _, sidecar) = deserialize_protobuf_for_store_with_hydration(
                    ops_stats.as_ref(),
                    &SpecsResponseFull::default(),
                    Default::default(),
                    &mut leader_specs,
                    &mut leader_data,
                    ProtobufHydrationContext {
                        hydrator: &hydrator,
                        source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
                        mmap_project_id: MmapProjectId::for_sdk_key(SDK_KEY),
                        capture_hydrated_data_store_bytes: true,
                        preserve_session_update_mode: false,
                    },
                )
                .await
                .unwrap();
                let sidecar = sidecar.expect("remote metadata should produce a sidecar");

                let baseline = serde_json::to_vec(&serde_json::json!({
                    "experiment_to_layer": {},
                    "condition_map": {},
                    "dynamic_configs": {
                        "large_config": {
                            "checksum": "same-checksum",
                            "type": "dynamic_config",
                            "salt": "",
                            "defaultValue": placeholder,
                            "enabled": true,
                            "rules": [],
                            "idType": "userID",
                            "entity": "dynamic_config"
                        }
                    },
                    "feature_gates": {},
                    "layer_configs": {},
                    "has_updates": true,
                    "time": 1
                }))
                .unwrap();
                let directory = tempfile::tempdir().unwrap();
                let path = directory.path().join("stale-placeholder.mmap");
                write_mmap_v2_for_test(&baseline, &path).unwrap();
                preload_mmap_v2_multi_for_test(&[(SDK_KEY, &path)]).unwrap();
                assert!(InternedStore::has_preloaded_mmap_v2());

                let mut follower_data = protobuf_response_data(sidecar);
                let mut follower_specs = SpecsResponseFull::default();
                deserialize_protobuf_for_store_with_hydration(
                    ops_stats.as_ref(),
                    &SpecsResponseFull::default(),
                    Default::default(),
                    &mut follower_specs,
                    &mut follower_data,
                    ProtobufHydrationContext {
                        hydrator: &hydrator,
                        source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
                        mmap_project_id: MmapProjectId::for_sdk_key(SDK_KEY),
                        capture_hydrated_data_store_bytes: false,
                        preserve_session_update_mode: false,
                    },
                )
                .await
                .unwrap();

                let config = follower_specs
                    .dynamic_configs
                    .0
                    .values()
                    .next()
                    .expect("sidecar should publish the dynamic config");
                assert!(!config.is_mmap());
                let follower_json = serde_json::to_value(&follower_specs).unwrap();
                assert_eq!(
                    follower_json["dynamic_configs"]["large_config"]["defaultValue"],
                    serde_json::json!({"large": "hydrated"})
                );
                server.verify().await;
            });
    }
}

#[tokio::test]
#[serial]
async fn store_parser_downloads_remote_values_across_envelopes_concurrently() {
    let server = MockServer::start().await;
    let first_body = br#"{"large":"first"}"#;
    let second_body = br#"{"large":"second"}"#;
    let first_sha = lowercase_hex(&Sha256::digest(first_body));
    let second_sha = lowercase_hex(&Sha256::digest(second_body));
    let first_path = format!("{DOWNLOAD_PATH_PREFIX}{first_sha}");
    let second_path = format!("{DOWNLOAD_PATH_PREFIX}{second_sha}");
    let response_delay = Duration::from_millis(750);

    Mock::given(method("GET"))
        .and(path(first_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(first_body)
                .set_delay(response_delay),
        )
        .expect(1)
        .mount(&server)
        .await;
    Mock::given(method("GET"))
        .and(path(second_path.clone()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(second_body)
                .set_delay(response_delay),
        )
        .expect(1)
        .mount(&server)
        .await;

    let remote_config =
        |name: &str, body: &[u8], sha: &str, download_path: &str| pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: name.to_string(),
            checksum: format!("{name}-checksum"),
            data: Some(
                pb::Spec {
                    salt: format!("{name}-salt"),
                    enabled: true,
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(raw_return_value(
                        serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap(),
                    )),
                    remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        };
    let mut envelopes = vec![
        protobuf_top_level_envelope(Some(true)),
        remote_config("first_config", first_body, &first_sha, &first_path),
    ];
    envelopes.extend((0..7).map(|index| {
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::FeatureGate as i32,
            name: format!("interleaved_gate_{index}"),
            checksum: format!("gate-{index}-checksum"),
            data: Some(
                pb::Spec {
                    salt: format!("gate-{index}-salt"),
                    enabled: true,
                    entity: pb::EntityType::EntityFeatureGate as i32,
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        }
    }));
    envelopes.push(remote_config(
        "second_config",
        second_body,
        &second_sha,
        &second_path,
    ));
    envelopes.push(protobuf_done_envelope());
    let bytes = serialize_protobuf_envelopes(&envelopes).unwrap();
    let mut data = protobuf_response_data(bytes);
    let hydrator = test_hydrator("concurrent-store-parser");
    let current_specs = SpecsResponseFull::default();
    let mut next_specs = SpecsResponseFull::default();

    let (update, _, hydrated_data_store_bytes) = tokio::time::timeout(
        Duration::from_millis(1_300),
        deserialize_protobuf_for_store_with_hydration(
            OPS_STATS
                .get_for_instance("concurrent-store-parser-decode")
                .as_ref(),
            &current_specs,
            Default::default(),
            &mut next_specs,
            &mut data,
            ProtobufHydrationContext {
                hydrator: &hydrator,
                source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
                mmap_project_id: MmapProjectId::for_sdk_key("concurrent-store-parser"),
                capture_hydrated_data_store_bytes: true,
                preserve_session_update_mode: false,
            },
        ),
    )
    .await
    .expect("distinct config downloads should share the bounded fanout")
    .unwrap();

    assert_eq!(update, ProtobufUpdate::Materialized { is_delta: false });
    let next_json = serde_json::to_value(&next_specs).unwrap();
    assert_eq!(
        next_json["dynamic_configs"]["first_config"]["defaultValue"]["large"],
        serde_json::json!("first")
    );
    assert_eq!(
        next_json["dynamic_configs"]["second_config"]["defaultValue"]["large"],
        serde_json::json!("second")
    );

    let mut sidecar_data = protobuf_response_data(
        hydrated_data_store_bytes.expect("remote metadata should produce a hydrated sidecar"),
    );
    let sidecar_envelopes = parse_protobuf_envelopes(&mut sidecar_data).unwrap();
    assert_eq!(
        sidecar_envelopes
            .iter()
            .filter_map(|envelope| (!envelope.name.is_empty()).then_some(envelope.name.as_str()))
            .collect::<Vec<_>>(),
        vec![
            "first_config",
            "interleaved_gate_0",
            "interleaved_gate_1",
            "interleaved_gate_2",
            "interleaved_gate_3",
            "interleaved_gate_4",
            "interleaved_gate_5",
            "interleaved_gate_6",
            "second_config",
        ]
    );
    for config_name in ["first_config", "second_config"] {
        let hydrated_spec = sidecar_envelopes
            .iter()
            .find(|envelope| envelope.name == config_name)
            .and_then(|envelope| envelope.data.as_deref())
            .map(pb::Spec::decode)
            .transpose()
            .unwrap()
            .expect("sidecar should retain the dynamic config envelope");
        assert!(hydrated_spec.remote_config_metadata.is_none());
    }
}

#[tokio::test]
#[serial]
async fn store_parser_keeps_download_window_full_behind_slow_blob() {
    let server = MockServer::start().await;
    let slow_delay = Duration::from_millis(750);
    let mut envelopes = vec![protobuf_top_level_envelope(Some(true))];
    let mut final_download_path = String::new();

    for index in 0..=DOWNLOAD_CONCURRENCY {
        let body = format!(r#"{{"large":"value-{index}"}}"#).into_bytes();
        let body_len = body.len();
        let sha = lowercase_hex(&Sha256::digest(&body));
        let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
        let response = ResponseTemplate::new(200)
            .insert_header("content-type", "application/json")
            .set_body_bytes(body);
        let response = if index == 0 || index == DOWNLOAD_CONCURRENCY {
            response.set_delay(slow_delay)
        } else {
            response
        };
        Mock::given(method("GET"))
            .and(path(download_path.clone()))
            .respond_with(response)
            .expect(1)
            .mount(&server)
            .await;

        if index == DOWNLOAD_CONCURRENCY {
            final_download_path = download_path.clone();
        }
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: format!("window_config_{index}"),
            checksum: format!("window-config-{index}-checksum"),
            data: Some(
                pb::Spec {
                    salt: format!("window-config-{index}-salt"),
                    enabled: true,
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(raw_return_value(
                        serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap(),
                    )),
                    remote_config_metadata: Some(protobuf_metadata(sha, body_len)),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        });
    }
    envelopes.push(protobuf_done_envelope());

    let mut data = protobuf_response_data(serialize_protobuf_envelopes(&envelopes).unwrap());
    let hydrator = test_hydrator("sliding-window-store-parser");
    let ops_stats = OPS_STATS.get_for_instance("sliding-window-store-parser-decode");
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let current_specs = SpecsResponseFull::default();
    let mut next_specs = SpecsResponseFull::default();
    let parse = deserialize_protobuf_for_store_with_hydration(
        ops_stats.as_ref(),
        &current_specs,
        Default::default(),
        &mut next_specs,
        &mut data,
        ProtobufHydrationContext {
            hydrator: &hydrator,
            source_url: &source_url,
            mmap_project_id: MmapProjectId::for_sdk_key("sliding-window-store-parser"),
            capture_hydrated_data_store_bytes: false,
            preserve_session_update_mode: false,
        },
    );
    let final_request_started = async {
        tokio::time::timeout(Duration::from_millis(500), async {
            loop {
                if server
                    .received_requests()
                    .await
                    .unwrap()
                    .iter()
                    .any(|request| request.url.path() == final_download_path)
                {
                    return;
                }
                tokio::time::sleep(Duration::from_millis(10)).await;
            }
        })
        .await
        .expect("the ninth download should start before the first slow blob finishes");
    };

    let (result, ()) = tokio::join!(parse, final_request_started);
    let (update, _, _) = result.unwrap();
    assert_eq!(update, ProtobufUpdate::Materialized { is_delta: false });
    let next_json = serde_json::to_value(&next_specs).unwrap();
    assert_eq!(
        next_json["dynamic_configs"][format!("window_config_{DOWNLOAD_CONCURRENCY}")]["defaultValue"]
            ["large"],
        serde_json::json!(format!("value-{DOWNLOAD_CONCURRENCY}"))
    );
    server.verify().await;
}

#[tokio::test]
async fn preserves_unknown_fields_in_touched_and_untouched_protobuf_specs() {
    let server = MockServer::start().await;
    let body = br#"{"large":"proto"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let metadata = protobuf_metadata(sha.clone(), body.len());
    let placeholder = serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap();
    let mut touched_spec_bytes = pb::Spec {
        default_value: Some(raw_return_value(placeholder)),
        remote_config_metadata: Some(metadata),
        ..Default::default()
    }
    .encode_to_vec();
    append_length_delimited_field(&mut touched_spec_bytes, 100, b"future-touched");

    let mut untouched_spec_bytes = pb::Spec {
        default_value: Some(raw_return_value(br#"{"inline":true}"#.to_vec())),
        ..Default::default()
    }
    .encode_to_vec();
    append_length_delimited_field(&mut untouched_spec_bytes, 101, b"future-untouched");

    let bytes = serialize_protobuf_envelopes(&[
        protobuf_top_level_envelope(Some(true)),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "touched".to_string(),
            checksum: "touched-checksum".to_string(),
            data: Some(touched_spec_bytes),
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "untouched".to_string(),
            checksum: "untouched-checksum".to_string(),
            data: Some(untouched_spec_bytes.clone()),
        },
        protobuf_done_envelope(),
    ])
    .unwrap();
    let mut data = protobuf_response_data(bytes);
    let hydrator = test_hydrator("proto-preserve-unknown-spec-fields");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    let hydrated_envelopes = parse_protobuf_envelopes(&mut data).unwrap();
    let touched_data = hydrated_envelopes
        .iter()
        .find(|envelope| envelope.name == "touched")
        .and_then(|envelope| envelope.data.as_deref())
        .unwrap();
    assert!(has_raw_length_delimited_field(
        touched_data,
        100,
        b"future-touched"
    ));
    let touched_spec = pb::Spec::decode(touched_data).unwrap();
    assert!(touched_spec.remote_config_metadata.is_none());
    assert_eq!(
        raw_return_value_bytes(&touched_spec.default_value),
        body.as_slice()
    );

    let untouched_data = hydrated_envelopes
        .iter()
        .find(|envelope| envelope.name == "untouched")
        .and_then(|envelope| envelope.data.as_deref())
        .unwrap();
    assert_eq!(untouched_data, untouched_spec_bytes.as_slice());
    assert!(has_raw_length_delimited_field(
        untouched_data,
        101,
        b"future-untouched"
    ));
}

#[tokio::test]
async fn preserves_unrelated_protobuf_envelope_wire_bytes_during_hydration() {
    let server = MockServer::start().await;
    let body = br#"{"large":"proto"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;

    let metadata = protobuf_metadata(sha.clone(), body.len());
    let placeholder = serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap();
    let touched = pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
        name: "touched".to_string(),
        checksum: "touched-checksum".to_string(),
        data: Some(
            pb::Spec {
                default_value: Some(raw_return_value(placeholder)),
                remote_config_metadata: Some(metadata),
                ..Default::default()
            }
            .encode_to_vec(),
        ),
    };
    let unrelated = pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::FeatureGate as i32,
        name: "unrelated".to_string(),
        checksum: "unrelated-checksum".to_string(),
        data: Some(pb::Spec::default().encode_to_vec()),
    };
    let mut unrelated_bytes = unrelated.encode_to_vec();
    append_length_delimited_field(&mut unrelated_bytes, 102, b"future-envelope");
    let unrelated_frame = encode_delimited_message(&unrelated_bytes).unwrap();
    let frames = vec![
        encode_envelope_frame(&protobuf_top_level_envelope(Some(true))),
        encode_envelope_frame(&touched),
        unrelated_frame.clone(),
        encode_envelope_frame(&protobuf_done_envelope()),
    ];
    let mut data = protobuf_response_data(serialize_raw_protobuf_frames(&frames));
    let hydrator = test_hydrator("proto-preserve-unknown-envelope-fields");

    hydrate_from_mock_source(&hydrator, &mut data, &server)
        .await
        .unwrap();

    let hydrated_frames = read_raw_protobuf_frames(&mut data);
    let hydrated_unrelated_frame = hydrated_frames
        .iter()
        .find(|frame| decode_protobuf_envelope(frame).unwrap().name == "unrelated")
        .unwrap();
    assert_eq!(hydrated_unrelated_frame, &unrelated_frame);
}

fn test_hydrator(instance_id: &str) -> RemoteConfigValueHydrator {
    RemoteConfigValueHydrator::new_with_ops_stats(
        Arc::new(NetworkClient::new("secret-key", None, None)),
        OPS_STATS.get_for_instance(instance_id),
    )
}

async fn hydrate_from_mock_source(
    hydrator: &RemoteConfigValueHydrator,
    data: &mut ResponseData,
    server: &MockServer,
) -> Result<(), StatsigErr> {
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    hydrator.hydrate_response(data, &source_url).await
}

async fn mount_json_blob(
    server: &MockServer,
    download_path: &str,
    body: &[u8],
    expected_requests: u64,
) {
    Mock::given(method("GET"))
        .and(path(download_path.to_string()))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(body.to_vec()),
        )
        .expect(expected_requests)
        .mount(server)
        .await;
}

fn valid_json_metadata(sha256: &str, byte_length: usize) -> Value {
    serde_json::json!({
        "sha256": sha256,
        "byteLength": byte_length,
        "contentType": "application/json",
        "compression": "none"
    })
}

fn valid_metadata(sha256: String, byte_length: u64) -> RemoteConfigValueMetadata {
    RemoteConfigValueMetadataWire {
        sha256,
        byte_length,
        content_type: "application/json".to_string(),
        compression: "none".to_string(),
    }
    .try_into()
    .unwrap()
}

fn protobuf_metadata(
    sha256: impl Into<String>,
    byte_length: usize,
) -> pb::RemoteConfigValueMetadata {
    pb::RemoteConfigValueMetadata {
        sha256: sha256.into(),
        byte_length: byte_length as u64,
        content_type: "application/json".to_string(),
        compression: "none".to_string(),
    }
}

fn counting_protobuf_response_data(bytes: Vec<u8>) -> (ResponseData, Arc<AtomicUsize>) {
    let bytes_read = Arc::new(AtomicUsize::new(0));
    let stream = CountingCursor {
        cursor: Cursor::new(bytes),
        bytes_read: bytes_read.clone(),
    };
    (
        ResponseData::from_stream_with_headers(Box::new(stream), Some(protobuf_headers())),
        bytes_read,
    )
}

#[derive(Debug)]
struct CountingCursor {
    cursor: Cursor<Vec<u8>>,
    bytes_read: Arc<AtomicUsize>,
}

impl Read for CountingCursor {
    fn read(&mut self, buffer: &mut [u8]) -> std::io::Result<usize> {
        let bytes_read = self.cursor.read(buffer)?;
        self.bytes_read.fetch_add(bytes_read, Ordering::SeqCst);
        Ok(bytes_read)
    }
}

impl Seek for CountingCursor {
    fn seek(&mut self, position: SeekFrom) -> std::io::Result<u64> {
        self.cursor.seek(position)
    }
}

fn raw_return_value(bytes: Vec<u8>) -> pb::ReturnValue {
    pb::ReturnValue {
        value: Some(return_value::Value::RawValue(bytes)),
    }
}

fn protobuf_top_level_envelope(may_have_remote_config_metadata: Option<bool>) -> pb::SpecsEnvelope {
    let data = pb::SpecsTopLevel {
        rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
        may_have_remote_config_metadata,
        ..Default::default()
    }
    .encode_to_vec();

    pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::TopLevel as i32,
        data: Some(data),
        ..Default::default()
    }
}

fn protobuf_with_true_marker_without_metadata(is_delta: bool) -> Vec<u8> {
    if is_delta {
        return serialize_protobuf_envelopes(&[
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
                ..Default::default()
            },
            protobuf_top_level_envelope(Some(true)),
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Checksums as i32,
                data: Some(
                    pb::RulesetsChecksums {
                        field_checksums: HashMap::from([
                            ("condition_map".to_string(), 0),
                            ("dynamic_configs".to_string(), 0),
                            ("feature_gates".to_string(), 0),
                            ("layer_configs".to_string(), 0),
                            ("param_stores".to_string(), 0),
                        ]),
                    }
                    .encode_to_vec(),
                ),
                ..Default::default()
            },
            protobuf_done_envelope(),
        ])
        .unwrap();
    }

    serialize_protobuf_envelopes(&[
        protobuf_top_level_envelope(Some(true)),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "inline_config".to_string(),
            checksum: "inline-checksum".to_string(),
            data: Some(
                pb::Spec {
                    salt: "salt".to_string(),
                    enabled: true,
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(raw_return_value(br#"{"inline":true}"#.to_vec())),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        },
        protobuf_done_envelope(),
    ])
    .unwrap()
}

fn protobuf_done_envelope() -> pb::SpecsEnvelope {
    pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::Done as i32,
        ..Default::default()
    }
}

fn protobuf_top_level_marker(data: &mut ResponseData) -> Option<bool> {
    let top_level = parse_protobuf_envelopes(data)
        .unwrap()
        .into_iter()
        .find(|envelope| {
            pb::SpecsEnvelopeKind::try_from(envelope.kind).ok()
                == Some(pb::SpecsEnvelopeKind::TopLevel)
        })
        .expect("response should contain a top-level envelope");
    pb::SpecsTopLevel::decode(top_level.data.as_deref().unwrap())
        .unwrap()
        .may_have_remote_config_metadata
}

fn raw_return_value_bytes(value: &Option<pb::ReturnValue>) -> &[u8] {
    match value.as_ref().and_then(|value| value.value.as_ref()) {
        Some(return_value::Value::RawValue(bytes)) => bytes,
        _ => panic!("expected raw protobuf return value"),
    }
}

fn protobuf_response_data(bytes: Vec<u8>) -> ResponseData {
    ResponseData::from_bytes_with_headers(bytes, Some(protobuf_headers()))
}

fn protobuf_headers() -> HashMap<String, String> {
    HashMap::from([
        (
            "content-type".to_string(),
            "application/octet-stream".to_string(),
        ),
        ("content-encoding".to_string(), "statsig-br".to_string()),
    ])
}

fn has_raw_length_delimited_field(data: &[u8], tag: u32, value: &[u8]) -> bool {
    parse_raw_protobuf_fields(data)
        .unwrap()
        .iter()
        .any(|field| field.tag == tag && field.length_delimited_value == Some(value))
}

fn encode_envelope_frame(envelope: &pb::SpecsEnvelope) -> Vec<u8> {
    encode_delimited_message(&envelope.encode_to_vec()).unwrap()
}

fn serialize_raw_protobuf_frames(frames: &[Vec<u8>]) -> Vec<u8> {
    let mut compressed = Vec::new();
    {
        let mut writer = brotli::CompressorWriter::new(&mut compressed, 4096, 5, 22);
        for frame in frames {
            writer.write_all(frame).unwrap();
        }
    }
    compressed
}

fn read_raw_protobuf_frames(data: &mut ResponseData) -> Vec<Vec<u8>> {
    data.rewind().unwrap();
    let mut reader = ProtoStreamReader::new(data);
    let mut frames = Vec::new();
    loop {
        let frame = reader.read_next_delimited_proto().unwrap();
        let is_done =
            pb::SpecsEnvelopeKind::try_from(decode_protobuf_envelope(frame.as_ref()).unwrap().kind)
                .ok()
                == Some(pb::SpecsEnvelopeKind::Done);
        frames.push(frame.to_vec());
        if is_done {
            return frames;
        }
    }
}
