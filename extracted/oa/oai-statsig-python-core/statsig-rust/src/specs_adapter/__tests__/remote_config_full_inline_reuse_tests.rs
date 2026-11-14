use super::*;
use crate::interned_string::InternedString;
use crate::specs_response::proto_specs::{
    ProtobufStoreParseBase, VerifiedRemoteConfigValues, prepare_protobuf_store_update,
};
use crate::specs_response::{
    parse_options::SpecsResponseParseOptions, proto_specs::deserialize_protobuf_with_options,
    spec_types::Spec, specs_hash_map::SpecDecodeStats,
};

#[path = "remote_config_inline_probe_edge_tests.rs"]
mod remote_config_inline_probe_edge_tests;

fn inline_config(name: &str, checksum: &str, value: Value) -> pb::SpecsEnvelope {
    config_envelope(
        name,
        checksum,
        pb::Spec {
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            default_value: Some(raw_return_value(serde_json::to_vec(&value).unwrap())),
            ..Default::default()
        },
    )
}

fn config_envelope(name: &str, checksum: &str, spec: pb::Spec) -> pb::SpecsEnvelope {
    pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
        name: name.to_string(),
        checksum: checksum.to_string(),
        data: Some(spec.encode_to_vec()),
    }
}

fn remote_config(name: &str, checksum: &str, body: &[u8]) -> pb::SpecsEnvelope {
    let sha = lowercase_hex(&Sha256::digest(body));
    config_envelope(
        name,
        checksum,
        pb::Spec {
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            default_value: Some(raw_return_value(
                serde_json::to_vec(&serde_json::json!({
                    "value": format!("{DOWNLOAD_PATH_PREFIX}{sha}")
                }))
                .unwrap(),
            )),
            remote_config_metadata: Some(protobuf_metadata(sha, body.len())),
            ..Default::default()
        },
    )
}

fn full_response(marker: bool, configs: &[pb::SpecsEnvelope]) -> Vec<u8> {
    let mut envelopes = vec![protobuf_top_level_envelope(Some(marker))];
    envelopes.extend_from_slice(configs);
    envelopes.push(protobuf_done_envelope());
    serialize_protobuf_envelopes(&envelopes).unwrap()
}

fn current_inline_configs(
    configs: &[pb::SpecsEnvelope],
    preserve_session_update_mode: bool,
) -> SpecsResponseFull {
    let mut specs = SpecsResponseFull::default();
    deserialize_protobuf_with_options(
        OPS_STATS
            .get_for_instance("inline-full-reuse-current")
            .as_ref(),
        &SpecsResponseFull::default(),
        &mut specs,
        &mut protobuf_response_data(full_response(false, configs)),
        if preserve_session_update_mode {
            SpecsResponseParseOptions::preserving_session_update_mode()
        } else {
            SpecsResponseParseOptions::default()
        },
    )
    .unwrap();
    specs
}

async fn parse_hydrated_update(
    server: &MockServer,
    current: &SpecsResponseFull,
    bytes: Vec<u8>,
    capture_sidecar: bool,
    preserve_session_update_mode: bool,
) -> Result<(SpecsResponseFull, Option<Vec<u8>>, bool), StatsigErr> {
    let ops_stats = OPS_STATS.get_for_instance("inline-full-reuse-update");
    let hydrator = test_hydrator("inline-full-reuse-update");
    let mut next = SpecsResponseFull::default();
    let decode_stats = [
        &current.feature_gates,
        &current.dynamic_configs,
        &current.layer_configs,
    ]
    .into_iter()
    .fold(SpecDecodeStats::default(), |mut stats, specs| {
        stats.total += specs.len();
        stats.mmap += specs.0.values().filter(|spec| spec.is_mmap()).count();
        stats
    });
    let hydrated = deserialize_protobuf_for_store_with_hydration(
        ops_stats.as_ref(),
        current,
        decode_stats,
        &mut next,
        &mut protobuf_response_data(bytes),
        &hydrator,
        StoreHydrationOptions::new(
            &format!("{}/v2/download_config_specs/key.json", server.uri()),
            MmapProjectId::for_sdk_key("inline-full-reuse-update"),
        )
        .with_session_update_mode(preserve_session_update_mode)
        .with_data_store_capture(capture_sidecar),
    )
    .await?;
    let ProtobufUpdate::Materialized { is_delta, .. } = hydrated.update else {
        panic!("a config update must materialize the response");
    };
    Ok((next, hydrated.hydrated_data_store_bytes, is_delta))
}

fn config_pointer(specs: &SpecsResponseFull, name: &str) -> Arc<Spec> {
    specs
        .dynamic_configs
        .get(&InternedString::from_str_ref(name))
        .unwrap()
        .clone()
        .into_pointer()
        .unwrap()
}

fn config_value(specs: &SpecsResponseFull, name: &str) -> Value {
    serde_json::to_value(specs).unwrap()["dynamic_configs"][name]["defaultValue"].clone()
}

async fn assert_blob_requests(server: &MockServer, expected: usize) {
    server.verify().await;
    let requests = server.received_requests().await.unwrap();
    assert_eq!(requests.len(), expected, "unexpected blob request count");
    assert!(requests.iter().all(|request| request.method == "GET"));
}

#[tokio::test]
async fn protobuf_rejects_remote_metadata_inside_json_envelopes() {
    let server = MockServer::start().await;
    let hydrator = test_hydrator("forbidden-proto-json");
    // The param store has a matching prior checksum: its incoming bytes must still be checked.
    let current = SpecsResponseFull {
        param_stores: serde_json::from_value(serde_json::json!({
            "store": {"parameters": {}, "checksum": "7"}
        }))
        .unwrap(),
        ..Default::default()
    };
    let param_store = pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::ParamStore as i32,
        name: "store".into(),
        checksum: "7".into(),
        data: Some(br#"{"parameters":{},"remoteConfigMetadata":{}}"#.to_vec()),
    };
    let rest = serde_json::json!({
        "experiment_to_layer": {},
        "override_rules": {"public": {
            "name": "public", "id": "public", "idType": "userID", "passPercentage": 100,
            "conditions": [], "returnValue": true, "remoteConfigMetadata": {}
        }}
    });
    for hint in [Some(true), Some(false), None] {
        for bad_override in [true, false] {
            let mut top = protobuf_top_level_envelope(hint);
            let mut frames = if bad_override {
                let mut data = pb::SpecsTopLevel::decode(top.data.as_deref().unwrap()).unwrap();
                data.rest = serde_json::to_vec(&rest).unwrap();
                top.data = Some(data.encode_to_vec());
                vec![top]
            } else {
                vec![top, param_store.clone()]
            };
            if hint == Some(true) {
                frames.push(remote_config("allowed", "8", b"{}"));
            }
            frames.push(protobuf_done_envelope());
            let wire = serialize_protobuf_envelopes(&frames).unwrap();
            if hint == Some(true) {
                let error = hydrate_from_mock_source(
                    &hydrator,
                    &mut protobuf_response_data(wire.clone()),
                    &server,
                )
                .await
                .unwrap_err();
                assert!(
                    error.to_string().contains("unsupported_entity"),
                    "{error:?}"
                );
            }
            let error = parse_hydrated_update(&server, &current, wire, false, false)
                .await
                .expect_err("must reject JSON metadata before reuse");
            assert!(
                error.to_string().contains("unsupported_entity"),
                "{error:?}"
            );
        }
    }
    assert!(server.received_requests().await.unwrap().is_empty());
}

#[tokio::test]
async fn inline_full_reuse_mixed_full_keeps_inline_rules_and_hydrates_remote_values() {
    let server = MockServer::start().await;
    let default_body = br#"{"remote":"default"}"#;
    let rule_body = br#"{"remote":"rule"}"#;
    let default_sha = lowercase_hex(&Sha256::digest(default_body));
    let rule_sha = lowercase_hex(&Sha256::digest(rule_body));
    let default_path = format!("{DOWNLOAD_PATH_PREFIX}{default_sha}");
    let rule_path = format!("{DOWNLOAD_PATH_PREFIX}{rule_sha}");
    mount_json_blob(&server, &default_path, default_body, 1).await;
    mount_json_blob(&server, &rule_path, rule_body, 1).await;

    let inline = config_envelope(
        "inline_config",
        "10",
        pb::Spec {
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            default_value: Some(raw_return_value(br#"{"inline":"default"}"#.to_vec())),
            rules: vec![pb::Rule {
                id: "inline-rule".to_string(),
                return_value: Some(raw_return_value(br#"{"inline":"rule"}"#.to_vec())),
                ..Default::default()
            }],
            ..Default::default()
        },
    );
    let current = current_inline_configs(
        &[
            inline.clone(),
            inline_config("obsolete", "20", serde_json::json!({"old": true})),
        ],
        false,
    );
    let pointer = config_pointer(&current, "inline_config");
    let remote = config_envelope(
        "remote_config",
        "30",
        pb::Spec {
            enabled: true,
            entity: pb::EntityType::EntityDynamicConfig as i32,
            default_value: Some(raw_return_value(
                serde_json::to_vec(&serde_json::json!({"value": default_path})).unwrap(),
            )),
            remote_config_metadata: Some(protobuf_metadata(default_sha, default_body.len())),
            rules: vec![pb::Rule {
                id: "remote-rule".to_string(),
                return_value: Some(raw_return_value(
                    serde_json::to_vec(&serde_json::json!({"value": rule_path})).unwrap(),
                )),
                remote_config_metadata: Some(protobuf_metadata(rule_sha, rule_body.len())),
                ..Default::default()
            }],
            ..Default::default()
        },
    );

    let (next, sidecar, is_delta) = parse_hydrated_update(
        &server,
        &current,
        full_response(true, &[inline, remote]),
        false,
        false,
    )
    .await
    .unwrap();
    assert!(!is_delta);
    assert!(sidecar.is_none());
    assert!(Arc::ptr_eq(
        &pointer,
        &config_pointer(&next, "inline_config")
    ));
    let next_json = serde_json::to_value(&next).unwrap();
    assert_eq!(
        next_json["dynamic_configs"]["inline_config"],
        serde_json::to_value(&current).unwrap()["dynamic_configs"]["inline_config"]
    );
    assert_eq!(
        config_value(&next, "remote_config"),
        serde_json::json!({"remote": "default"})
    );
    assert_eq!(
        next_json["dynamic_configs"]["remote_config"]["rules"][0]["returnValue"],
        serde_json::json!({"remote": "rule"})
    );
    assert!(
        next.dynamic_configs
            .get(&InternedString::from_str_ref("obsolete"))
            .is_none()
    );
    assert_eq!(
        config_value(&current, "obsolete"),
        serde_json::json!({"old": true})
    );
    assert_blob_requests(&server, 2).await;
}

#[tokio::test]
async fn inline_full_reuse_inline_to_remote_same_checksum_fetches_changed_value() {
    let server = MockServer::start().await;
    let body = br#"{"value":"remote"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 1).await;
    let current = current_inline_configs(
        &[inline_config(
            "config",
            "10",
            serde_json::json!({"value": "inline"}),
        )],
        false,
    );
    let pointer = config_pointer(&current, "config");

    let (next, _, _) = parse_hydrated_update(
        &server,
        &current,
        full_response(true, &[remote_config("config", "10", body)]),
        false,
        false,
    )
    .await
    .unwrap();
    assert_eq!(
        config_value(&next, "config"),
        serde_json::json!({"value": "remote"})
    );
    assert_eq!(
        config_value(&current, "config"),
        serde_json::json!({"value": "inline"})
    );
    assert!(!Arc::ptr_eq(&pointer, &config_pointer(&next, "config")));
    assert_blob_requests(&server, 1).await;
}

#[tokio::test]
async fn inline_full_reuse_rule_only_remote_metadata_keeps_validation_and_hydration() {
    let server = MockServer::start().await;
    let body = br#"{"rule":"remote"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;
    let mut spec = pb::Spec {
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        default_value: Some(raw_return_value(br#"{"default":"inline"}"#.to_vec())),
        rules: vec![pb::Rule {
            id: "rule".to_string(),
            return_value: Some(raw_return_value(br#"{"rule":"inline"}"#.to_vec())),
            ..Default::default()
        }],
        ..Default::default()
    };
    let current = current_inline_configs(&[config_envelope("config", "10", spec.clone())], false);
    let pointer = config_pointer(&current, "config");
    spec.rules[0].return_value = Some(raw_return_value(
        serde_json::to_vec(&serde_json::json!({"value": download_path})).unwrap(),
    ));
    spec.rules[0].remote_config_metadata = Some(protobuf_metadata(sha, body.len()));

    let (next, _, _) = parse_hydrated_update(
        &server,
        &current,
        full_response(true, &[config_envelope("config", "10", spec)]),
        false,
        false,
    )
    .await
    .unwrap();
    assert_eq!(
        config_value(&next, "config"),
        serde_json::json!({"default": "inline"})
    );
    assert_eq!(
        serde_json::to_value(&next).unwrap()["dynamic_configs"]["config"]["rules"][0]["returnValue"],
        serde_json::json!({"rule": "remote"})
    );
    assert_eq!(
        serde_json::to_value(&current).unwrap()["dynamic_configs"]["config"]["rules"][0]["returnValue"],
        serde_json::json!({"rule": "inline"})
    );
    assert!(!Arc::ptr_eq(&pointer, &config_pointer(&next, "config")));
    assert_blob_requests(&server, 1).await;
}

#[tokio::test]
async fn inline_full_reuse_changed_sha_same_checksum_does_not_keep_old_remote_value() {
    let server = MockServer::start().await;
    let first_body = br#"{"revision":"first"}"#;
    let next_body = br#"{"revision":"next"}"#;
    for body in [first_body.as_slice(), next_body.as_slice()] {
        let sha = lowercase_hex(&Sha256::digest(body));
        mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 1).await;
    }
    let (current, _, _) = parse_hydrated_update(
        &server,
        &SpecsResponseFull::default(),
        full_response(true, &[remote_config("config", "10", first_body)]),
        false,
        false,
    )
    .await
    .unwrap();
    let pointer = config_pointer(&current, "config");
    let (next, _, _) = parse_hydrated_update(
        &server,
        &current,
        full_response(true, &[remote_config("config", "10", next_body)]),
        false,
        false,
    )
    .await
    .unwrap();
    assert_eq!(
        config_value(&next, "config"),
        serde_json::json!({"revision": "next"})
    );
    assert_eq!(
        config_value(&current, "config"),
        serde_json::json!({"revision": "first"})
    );
    assert!(!Arc::ptr_eq(&pointer, &config_pointer(&next, "config")));
    assert_blob_requests(&server, 2).await;
}

#[tokio::test]
async fn inline_full_reuse_malformed_metadata_cannot_hide_behind_matching_checksum() {
    let server = MockServer::start().await;
    let body = br#"{"value":"remote"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 0).await;
    let current = current_inline_configs(
        &[inline_config(
            "config",
            "10",
            serde_json::json!({"value": "inline"}),
        )],
        false,
    );
    let before = serde_json::to_value(&current).unwrap();
    let mut invalid_metadata = Vec::new();
    invalid_metadata.push(("bad SHA", protobuf_metadata("bad-sha", body.len())));
    let mut unsupported_compression = protobuf_metadata(&sha, body.len());
    unsupported_compression.compression = "brotli".to_string();
    invalid_metadata.push(("unsupported codec", unsupported_compression));
    let mut invalid_size = protobuf_metadata(&sha, body.len());
    invalid_size.byte_length = MAX_REMOTE_VALUE_BYTES as u64 + 1;
    invalid_metadata.push(("oversized body", invalid_size));

    for (case, metadata) in invalid_metadata {
        let mut envelope = remote_config("config", "10", body);
        let mut spec = pb::Spec::decode(envelope.data.as_deref().unwrap()).unwrap();
        spec.remote_config_metadata = Some(metadata);
        envelope.data = Some(spec.encode_to_vec());
        let result = parse_hydrated_update(
            &server,
            &current,
            full_response(true, &[envelope]),
            false,
            false,
        )
        .await;
        assert!(
            result.is_err(),
            "{case}: invalid metadata must fail even for an unchanged producer checksum"
        );
        assert_eq!(serde_json::to_value(&current).unwrap(), before);
    }
    assert_blob_requests(&server, 0).await;
}

#[tokio::test]
async fn inline_full_reuse_changed_session_mode_is_preserved_in_mixed_full() {
    let server = MockServer::start().await;
    let body = br#"{"remote":true}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 3).await;
    let mut spec = pb::Spec {
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        default_value: Some(raw_return_value(br#"{"inline":true}"#.to_vec())),
        session_update_mode: Some("sticky".to_string()),
        ..Default::default()
    };
    let current = current_inline_configs(&[config_envelope("inline", "10", spec.clone())], true);
    let pointer = config_pointer(&current, "inline");
    for mode in [Some("sticky"), Some("live"), None] {
        spec.session_update_mode = mode.map(str::to_string);
        let (next, _, _) = parse_hydrated_update(
            &server,
            &current,
            full_response(
                true,
                &[
                    config_envelope("inline", "10", spec.clone()),
                    remote_config("remote", "20", body),
                ],
            ),
            false,
            true,
        )
        .await
        .unwrap();
        let next_pointer = config_pointer(&next, "inline");
        assert_eq!(next_pointer.session_update_mode.as_deref(), mode);
        assert_eq!(Arc::ptr_eq(&pointer, &next_pointer), mode == Some("sticky"));
        assert_eq!(
            config_value(&next, "inline"),
            serde_json::json!({"inline": true})
        );
        assert_eq!(
            config_value(&next, "remote"),
            serde_json::json!({"remote": true})
        );
    }
    assert_eq!(pointer.session_update_mode.as_deref(), Some("sticky"));
    assert_blob_requests(&server, 3).await;
}

#[tokio::test]
async fn inline_full_reuse_hydrated_sidecar_does_not_reuse_same_checksum_placeholder() {
    let server = MockServer::start().await;
    let body = br#"{"hydrated":true}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &download_path, body, 1).await;
    let (_, sidecar, _) = parse_hydrated_update(
        &server,
        &SpecsResponseFull::default(),
        full_response(true, &[remote_config("config", "10", body)]),
        true,
        false,
    )
    .await
    .unwrap();
    let sidecar = sidecar.unwrap();
    assert_eq!(
        protobuf_top_level_marker(&mut protobuf_response_data(sidecar.clone())),
        Some(false)
    );
    let current = current_inline_configs(
        &[inline_config(
            "config",
            "10",
            serde_json::json!({"value": download_path}),
        )],
        false,
    );
    let pointer = config_pointer(&current, "config");
    let (next, replay_sidecar, _) = parse_hydrated_update(&server, &current, sidecar, false, false)
        .await
        .unwrap();
    assert_eq!(
        config_value(&next, "config"),
        serde_json::json!({"hydrated": true})
    );
    assert_eq!(
        config_value(&current, "config"),
        serde_json::json!({"value": download_path})
    );
    assert!(!Arc::ptr_eq(&pointer, &config_pointer(&next, "config")));
    assert!(replay_sidecar.is_none());
    assert_blob_requests(&server, 1).await;
}

#[tokio::test]
async fn inline_full_reuse_mixed_delta_keeps_inline_pointer_and_applies_removal() {
    let server = MockServer::start().await;
    let body = br#"{"remote":"delta"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 1).await;
    let inline = inline_config("inline", "10", serde_json::json!({"inline": true}));
    let current = current_inline_configs(
        &[
            inline.clone(),
            inline_config("obsolete", "20", serde_json::json!({"old": true})),
        ],
        false,
    );
    let pointer = config_pointer(&current, "inline");
    let response = serialize_protobuf_envelopes(&[
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..Default::default()
        },
        protobuf_top_level_envelope(Some(true)),
        inline,
        remote_config("remote", "30", body),
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Deletions as i32,
            data: Some(
                pb::RulesetsResponseDeletions {
                    dynamic_configs: vec!["obsolete".to_string()],
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Checksums as i32,
            data: Some(
                pb::RulesetsChecksums {
                    field_checksums: HashMap::from([
                        ("condition_map".to_string(), 0),
                        ("dynamic_configs".to_string(), 40),
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
    let (next, _, is_delta) = parse_hydrated_update(&server, &current, response, false, false)
        .await
        .unwrap();
    assert!(is_delta);
    assert!(Arc::ptr_eq(&pointer, &config_pointer(&next, "inline")));
    assert_eq!(
        config_value(&next, "inline"),
        serde_json::json!({"inline": true})
    );
    assert_eq!(
        config_value(&next, "remote"),
        serde_json::json!({"remote": "delta"})
    );
    assert_eq!(next.dynamic_configs.0.len(), 2);
    assert!(
        next.dynamic_configs
            .get(&InternedString::from_str_ref("obsolete"))
            .is_none()
    );
    assert_eq!(
        config_value(&current, "obsolete"),
        serde_json::json!({"old": true})
    );
    assert_blob_requests(&server, 1).await;
}

fn remote_rule(id: &str, spec: pb::Spec) -> pb::Rule {
    pb::Rule {
        id: id.to_owned(),
        return_value: spec.default_value,
        remote_config_metadata: spec.remote_config_metadata,
        ..Default::default()
    }
}

#[tokio::test]
async fn partial_protobuf_retries_only_unverified_slots_and_skips_the_sidecar() {
    let server = MockServer::start().await;
    let hydrator = test_hydrator("partial-protobuf");
    let (mut config, checksum_mismatch) = remote_spec(b"{}");
    let (valid_rule, healthy) = remote_spec(br#"{"healthy":true}"#);
    let (invalid_rule, invalid_json) = remote_spec(b"{");
    for (sha, body, gets) in [
        (&checksum_mismatch, &b"[]"[..], 2),
        (&invalid_json, &b"{"[..], 2),
        (&healthy, &br#"{"healthy":true}"#[..], 1),
    ] {
        mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, gets).await;
    }
    config.rules = vec![
        remote_rule("valid", valid_rule),
        remote_rule("invalid", invalid_rule),
    ];
    let envelope = config_envelope("mixed", "11", config);
    let wire = full_response(true, &[envelope]);
    let name = InternedString::from_str_ref("mixed");
    let mut current = SpecsResponseFull::default();
    let mut proofs = VerifiedRemoteConfigValues::new();
    let mut unavailable = None;
    for _ in 0..2 {
        let mut next = SpecsResponseFull::default();
        let checksums = SpecsFieldChecksums::from_specs(&current);
        let mut base =
            ProtobufStoreParseBase::new(&current, Default::default(), &checksums, &proofs);
        base.unavailable = unavailable.as_ref();
        let update = prepare_protobuf_store_update(
            OPS_STATS.get_for_instance("partial-protobuf").as_ref(),
            base,
            &mut next,
            &mut protobuf_response_data(wire.clone()),
            &hydrator,
            StoreHydrationOptions::new(
                &server.uri(),
                MmapProjectId::for_sdk_key("partial-protobuf"),
            )
            .with_data_store_capture(true)
            .with_partial_full_response(true),
        )
        .await
        .unwrap();

        let configs = serde_json::to_value(&next.dynamic_configs).unwrap();
        assert_eq!(
            configs["mixed"]["rules"][0]["returnValue"],
            serde_json::json!({"healthy":true})
        );
        let partial = update.partial_hydration.unwrap();
        assert_eq!(
            partial.unavailable[&name],
            std::collections::HashSet::from([None, Some(1)])
        );
        assert_eq!(
            partial.failed_blobs[&invalid_json],
            HydrationFailureReason::InvalidJson
        );
        assert_eq!(
            partial.failed_blobs[&checksum_mismatch],
            HydrationFailureReason::ChecksumMismatch
        );
        assert!(update.hydrated_data_store_bytes.is_none());
        unavailable = Some(partial.unavailable);
        current = next;
        proofs = update.verified_remote_values;
        assert_eq!(proofs[&name].len(), 1);
        assert!(proofs[&name].contains_key(&healthy));
    }
    server.verify().await;
}

#[tokio::test]
async fn superseded_blob_failure_only_retries_a_discarded_sidecar() {
    let server = MockServer::start().await;
    let wire = full_response(
        true,
        &[
            remote_config("config", "1", b"{}"),
            inline_config("config", "2", serde_json::json!({"latest":true})),
        ],
    );
    let hydrator = test_hydrator("overwritten-failure");
    for capture in [false, true] {
        let mut next = SpecsResponseFull::default();
        let update = deserialize_protobuf_for_store_with_hydration(
            OPS_STATS.get_for_instance("overwritten-failure").as_ref(),
            &SpecsResponseFull::default(),
            Default::default(),
            &mut next,
            &mut protobuf_response_data(wire.clone()),
            &hydrator,
            StoreHydrationOptions::new(
                &server.uri(),
                MmapProjectId::for_sdk_key("overwritten-failure"),
            )
            .with_data_store_capture(capture)
            .with_partial_full_response(true),
        )
        .await
        .unwrap();
        assert_eq!(
            serde_json::to_value(next.dynamic_configs).unwrap()["config"]["defaultValue"],
            serde_json::json!({"latest": true})
        );
        assert!(update.hydrated_data_store_bytes.is_none());
        assert_eq!(update.partial_hydration.is_some(), capture);
        if let Some(repair) = update.partial_hydration {
            assert!(repair.failed_blobs.is_empty() && repair.unavailable.is_empty());
        }
    }
}
