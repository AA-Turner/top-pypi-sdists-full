use super::*;

fn append_message_field(output: &mut Vec<u8>, tag: u32, message: &[u8]) {
    prost::encoding::encode_key(tag, prost::encoding::WireType::LengthDelimited, output);
    prost::encoding::encode_varint(message.len() as u64, output);
    output.extend_from_slice(message);
}

fn marked_update(configs: &[pb::SpecsEnvelope], is_delta: bool) -> Vec<u8> {
    if !is_delta {
        return full_response(true, configs);
    }
    let mut envelopes = vec![
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..Default::default()
        },
        protobuf_top_level_envelope(Some(true)),
    ];
    envelopes.extend_from_slice(configs);
    envelopes.push(pb::SpecsEnvelope {
        kind: pb::SpecsEnvelopeKind::Checksums as i32,
        data: Some(
            pb::RulesetsChecksums {
                field_checksums: HashMap::from([
                    ("condition_map".to_string(), 0),
                    ("dynamic_configs".to_string(), 30),
                    ("feature_gates".to_string(), 0),
                    ("layer_configs".to_string(), 0),
                    ("param_stores".to_string(), 0),
                ]),
            }
            .encode_to_vec(),
        ),
        ..Default::default()
    });
    envelopes.push(protobuf_done_envelope());
    serialize_protobuf_envelopes(&envelopes).unwrap()
}

#[tokio::test]
async fn inline_probe_edges_malformed_projection_preserves_full_skip_and_delta_error() {
    let server = MockServer::start().await;
    let body = br#"{"healthy":"remote"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let corruptions: &[(&str, Option<&[u8]>)] = &[
        (
            "default metadata wrong wire type",
            Some(&[0x80, 0x01, 0x00]),
        ),
        ("rules wrong wire type", Some(&[0x38, 0x00])),
        (
            "rule metadata wrong wire type",
            Some(&[0x3a, 0x02, 0x70, 0x00]),
        ),
        (
            "truncated default metadata",
            Some(&[0x82, 0x01, 0x02, 0x00]),
        ),
        ("truncated rules", Some(&[0x3a, 0x02, 0x00])),
        (
            "truncated rule metadata",
            Some(&[0x3a, 0x03, 0x72, 0x02, 0x00]),
        ),
        ("truncated field key", Some(&[0x80])),
        // The byte projection sees presence; full decoding must still reject
        // metadata whose nested SHA field uses the wrong wire type.
        (
            "malformed metadata message",
            Some(&[0x82, 0x01, 0x02, 0x08, 0x01]),
        ),
        ("missing envelope data", None),
    ];
    mount_json_blob(
        &server,
        &format!("{DOWNLOAD_PATH_PREFIX}{sha}"),
        body,
        u64::try_from(corruptions.len()).unwrap(),
    )
    .await;
    let original = inline_config("config", "10", serde_json::json!({"old": true}));
    let healthy = inline_config("healthy", "20", serde_json::json!({"old": "healthy"}));
    let current = current_inline_configs(&[original.clone(), healthy], false);
    let before = serde_json::to_value(&current).unwrap();
    let pointer = config_pointer(&current, "config");

    for (case, corruption) in corruptions {
        let mut malformed = original.clone();
        malformed.data = corruption.map(|suffix| {
            let mut data = original.data.clone().unwrap();
            data.extend_from_slice(suffix);
            data
        });
        for is_delta in [false, true] {
            let result = parse_hydrated_update(
                &server,
                &current,
                marked_update(
                    &[malformed.clone(), remote_config("healthy", "20", body)],
                    is_delta,
                ),
                false,
                false,
            )
            .await;
            if is_delta {
                let expected_tag = if corruption.is_none() {
                    "SpecsEnvelope"
                } else {
                    "proto::DynamicConfig"
                };
                assert!(
                    matches!(&result, Err(StatsigErr::ProtobufParseError(tag, _)) if tag == expected_tag),
                    "{case}: delta must reject the malformed config before reusing its pointer: {:?}",
                    result.as_ref().err()
                );
            } else {
                let (next, _, parsed_delta) =
                    result.unwrap_or_else(|error| panic!("{case}: {error}"));
                assert!(!parsed_delta);
                assert!(
                    next.dynamic_configs
                        .get(&InternedString::from_str_ref("config"))
                        .is_none(),
                    "{case}: FULL must skip the malformed config instead of keeping its old pointer"
                );
                assert_eq!(
                    config_value(&next, "healthy"),
                    serde_json::json!({"healthy": "remote"})
                );
            }
            assert_eq!(serde_json::to_value(&current).unwrap(), before, "{case}");
            assert!(Arc::ptr_eq(&pointer, &config_pointer(&current, "config")));
        }
    }
    assert_blob_requests(&server, corruptions.len()).await;
}

fn spec_with_metadata_fields(
    metadata_fields: &[Vec<u8>],
    default_remote: bool,
    rule_remote: bool,
    body: &[u8],
) -> pb::SpecsEnvelope {
    let sha = lowercase_hex(&Sha256::digest(body));
    let placeholder = raw_return_value(
        serde_json::to_vec(&serde_json::json!({"value": format!("{DOWNLOAD_PATH_PREFIX}{sha}")}))
            .unwrap(),
    );
    let mut spec = pb::Spec {
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        default_value: Some(if default_remote {
            placeholder.clone()
        } else {
            raw_return_value(br#"{"default":"inline"}"#.to_vec())
        }),
        ..Default::default()
    }
    .encode_to_vec();
    if default_remote {
        for metadata in metadata_fields {
            append_message_field(&mut spec, 16, metadata);
        }
    }
    let mut rule = pb::Rule {
        id: "rule".to_string(),
        return_value: Some(if rule_remote {
            placeholder
        } else {
            raw_return_value(br#"{"rule":"inline"}"#.to_vec())
        }),
        ..Default::default()
    }
    .encode_to_vec();
    if rule_remote {
        for metadata in metadata_fields {
            append_message_field(&mut rule, 14, metadata);
        }
    }
    append_message_field(&mut spec, 7, &rule);
    pb::SpecsEnvelope {
        data: Some(spec),
        ..inline_config("config", "10", serde_json::json!({"old": true}))
    }
}

#[tokio::test]
async fn inline_probe_edges_duplicate_metadata_with_last_empty_hydrates_default_and_rules() {
    let server = MockServer::start().await;
    let body = br#"{"hydrated":true}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let metadata = protobuf_metadata(&sha, body.len()).encode_to_vec();
    mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 6).await;
    let stable = inline_config("stable", "20", serde_json::json!({"stable": true}));
    let current = current_inline_configs(
        &[
            inline_config("config", "10", serde_json::json!({"old": true})),
            stable.clone(),
        ],
        false,
    );
    let before = serde_json::to_value(&current).unwrap();
    let pointer = config_pointer(&current, "config");

    for (default_remote, rule_remote) in [(true, false), (false, true), (true, true)] {
        let envelope = spec_with_metadata_fields(
            &[metadata.clone(), metadata.clone(), Vec::new()],
            default_remote,
            rule_remote,
            body,
        );
        // Protobuf merges duplicate message fields; an empty final occurrence
        // must preserve the earlier SHA even though the projection retains [].
        let decoded = pb::Spec::decode(envelope.data.as_deref().unwrap()).unwrap();
        if default_remote {
            assert_eq!(decoded.remote_config_metadata.as_ref().unwrap().sha256, sha);
        }
        if rule_remote {
            assert_eq!(
                decoded.rules[0]
                    .remote_config_metadata
                    .as_ref()
                    .unwrap()
                    .sha256,
                sha
            );
        }
        for is_delta in [false, true] {
            let (next, _, parsed_delta) = parse_hydrated_update(
                &server,
                &current,
                marked_update(&[envelope.clone(), stable.clone()], is_delta),
                false,
                false,
            )
            .await
            .unwrap();
            assert_eq!(parsed_delta, is_delta);
            assert!(!Arc::ptr_eq(&pointer, &config_pointer(&next, "config")));
            assert_eq!(
                config_value(&next, "config"),
                if default_remote {
                    serde_json::json!({"hydrated": true})
                } else {
                    serde_json::json!({"default": "inline"})
                }
            );
            assert_eq!(
                serde_json::to_value(&next).unwrap()["dynamic_configs"]["config"]["rules"][0]["returnValue"],
                if rule_remote {
                    serde_json::json!({"hydrated": true})
                } else {
                    serde_json::json!({"rule": "inline"})
                }
            );
            assert_eq!(serde_json::to_value(&current).unwrap(), before);
        }
    }
    // Identical default/rule references share one GET per update.
    assert_blob_requests(&server, 6).await;
}

#[tokio::test]
async fn inline_probe_edges_empty_or_invalid_duplicate_metadata_cannot_reuse() {
    let server = MockServer::start().await;
    let body = br#"{"remote":true}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let metadata = protobuf_metadata(&sha, body.len()).encode_to_vec();
    let invalid_sha = pb::RemoteConfigValueMetadata {
        sha256: "invalid".to_string(),
        ..Default::default()
    }
    .encode_to_vec();
    let stable = inline_config("stable", "20", serde_json::json!({"stable": true}));
    let current = current_inline_configs(
        &[
            inline_config("config", "10", serde_json::json!({"old": true})),
            stable.clone(),
        ],
        false,
    );
    let before = serde_json::to_value(&current).unwrap();
    for (case, fields) in [
        ("empty metadata", vec![Vec::new()]),
        ("invalid final duplicate SHA", vec![metadata, invalid_sha]),
    ] {
        for (default_remote, rule_remote) in [(true, false), (false, true)] {
            let envelope = spec_with_metadata_fields(&fields, default_remote, rule_remote, body);
            for is_delta in [false, true] {
                let result = parse_hydrated_update(
                    &server,
                    &current,
                    marked_update(&[envelope.clone(), stable.clone()], is_delta),
                    false,
                    false,
                )
                .await;
                assert!(
                    matches!(result, Err(ref error) if HydrationFailureReason::from_error(error) == Some(HydrationFailureReason::InvalidSha256)),
                    "{case}, default={default_remote}, delta={is_delta}: metadata must reach SHA validation"
                );
                assert_eq!(serde_json::to_value(&current).unwrap(), before);
            }
        }
    }
    assert_blob_requests(&server, 0).await;
}

#[tokio::test]
async fn inline_probe_edges_skipped_values_keep_existing_checksum_authority() {
    let server = MockServer::start().await;
    let body = br#"{"healthy":"remote"}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    mount_json_blob(&server, &format!("{DOWNLOAD_PATH_PREFIX}{sha}"), body, 2).await;
    let original = inline_config("config", "10", serde_json::json!({"old": true}));
    let current = current_inline_configs(std::slice::from_ref(&original), false);
    let before = serde_json::to_value(&current).unwrap();
    let pointer = config_pointer(&current, "config");
    let tag_like_values = config_envelope(
        "config",
        "10",
        pb::Spec {
            default_value: Some(raw_return_value(vec![0x82, 0x01, 0x00])),
            rules: vec![pb::Rule {
                return_value: Some(raw_return_value(vec![0x72, 0x00])),
                ..Default::default()
            }],
            ..Default::default()
        },
    );
    let mut malformed_return_value = original.clone();
    append_message_field(malformed_return_value.data.as_mut().unwrap(), 3, &[0x00]);
    assert!(pb::Spec::decode(malformed_return_value.data.as_deref().unwrap()).is_err());
    for envelope in [tag_like_values, malformed_return_value] {
        // Matching producer checksum is authoritative for inline values on the
        // existing marker=false path, including invalid skipped value contents.
        let (plain, _, _) = parse_hydrated_update(
            &server,
            &current,
            full_response(false, std::slice::from_ref(&envelope)),
            false,
            false,
        )
        .await
        .unwrap();
        let (mixed, _, _) = parse_hydrated_update(
            &server,
            &current,
            full_response(true, &[envelope, remote_config("healthy", "20", body)]),
            false,
            false,
        )
        .await
        .unwrap();
        assert!(Arc::ptr_eq(&pointer, &config_pointer(&plain, "config")));
        assert!(Arc::ptr_eq(&pointer, &config_pointer(&mixed, "config")));
        assert_eq!(
            config_value(&mixed, "config"),
            config_value(&plain, "config")
        );
        assert_eq!(
            config_value(&mixed, "healthy"),
            serde_json::json!({"healthy": "remote"})
        );
        assert_eq!(serde_json::to_value(&current).unwrap(), before);
    }
    assert_blob_requests(&server, 2).await;
}
