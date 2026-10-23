use super::*;
use crate::interned_string::InternedString;
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
    let (update, _, sidecar) = deserialize_protobuf_for_store_with_hydration(
        ops_stats.as_ref(),
        current,
        decode_stats,
        &mut next,
        &mut protobuf_response_data(bytes),
        ProtobufHydrationContext {
            hydrator: &hydrator,
            source_url: &format!("{}/v2/download_config_specs/key.json", server.uri()),
            sync_trigger: None,
            mmap_project_id: MmapProjectId::for_sdk_key("inline-full-reuse-update"),
            capture_hydrated_data_store_bytes: capture_sidecar,
            preserve_session_update_mode,
        },
    )
    .await?;
    let ProtobufUpdate::Materialized { is_delta, .. } = update else {
        panic!("a config update must materialize the response");
    };
    Ok((next, sidecar, is_delta))
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
