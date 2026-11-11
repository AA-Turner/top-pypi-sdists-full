use super::*;

#[tokio::test]
async fn json_rejects_blob_metadata_outside_dynamic_configs() {
    let server = MockServer::start().await;
    let hydrator = test_hydrator("inline-only-json");
    let rule = serde_json::json!({"remoteConfigMetadata": {}});
    for collection in [
        "feature_gates",
        "layer_configs",
        "param_stores",
        "condition_map",
        "override_rules",
    ] {
        for spec in [rule.clone(), serde_json::json!({"rules": [null, rule]})] {
            let wire = serde_json::json!({collection: {"bad": spec}});
            let mut data = ResponseData::from_bytes(serde_json::to_vec(&wire).unwrap());
            let error = hydrate_from_mock_source(&hydrator, &mut data, &server)
                .await
                .unwrap_err();
            assert!(
                error.to_string().contains("unsupported_entity"),
                "{error:?}"
            );
        }
    }
    assert!(server.received_requests().await.unwrap().is_empty());
}

#[tokio::test]
async fn protobuf_rejects_blob_metadata_outside_dynamic_configs() {
    let server = MockServer::start().await;
    let (hydrator, mut events) = observed_hydrator();
    let sha = "a".repeat(64);
    let spec = pb::Spec {
        default_value: Some(raw_return_value(
            serde_json::to_vec(&format!("{DOWNLOAD_PATH_PREFIX}{sha}")).unwrap(),
        )),
        remote_config_metadata: Some(protobuf_metadata(&sha, 3)),
        ..Default::default()
    };
    for kind in [
        pb::SpecsEnvelopeKind::FeatureGate,
        pb::SpecsEnvelopeKind::LayerConfig,
    ] {
        let encoded = serialize_protobuf_envelopes(&[
            protobuf_top_level_envelope(Some(true)),
            pb::SpecsEnvelope {
                kind: kind as i32,
                name: "bad".into(),
                data: Some(spec.encode_to_vec()),
                ..Default::default()
            },
            protobuf_done_envelope(),
        ])
        .unwrap();
        let error = hydrate_from_mock_source(
            &hydrator,
            &mut protobuf_response_data(encoded.clone()),
            &server,
        )
        .await
        .unwrap_err();
        assert!(
            error.to_string().contains("unsupported_entity"),
            "{error:?}"
        );
        let error = hydrate_protobuf_for_store(
            &hydrator,
            &mut protobuf_response_data(encoded),
            &server.uri(),
        )
        .await
        .unwrap_err();
        assert!(
            error.to_string().contains("unsupported_entity"),
            "{error:?}"
        );
        assert_hydration_results(&mut events, &[("failure", "unsupported_entity"); 2]);
    }
    assert!(server.received_requests().await.unwrap().is_empty());
}
