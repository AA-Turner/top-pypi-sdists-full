use super::*;

fn distributions(
    events: &mut tokio::sync::broadcast::Receiver<OpsStatsEvent>,
    metric: &str,
) -> Vec<crate::observability::observability_client_adapter::ObservabilityEvent> {
    let mut result = Vec::new();
    while let Ok(event) = events.try_recv() {
        if let OpsStatsEvent::Observability(event) = event {
            if event.metric_name == metric {
                assert!(matches!(event.metric_type, MetricType::Dist));
                result.push(event);
            }
        }
    }
    result
}

#[test]
fn timeout_steps_preserve_failure_classification_and_report_elapsed_ms() {
    let (hydrator, mut events) = observed_hydrator();
    for (step, label) in [
        (HydrationTimeoutStep::Response, "response"),
        (HydrationTimeoutStep::PermitPrecheck, "permit_precheck"),
        (HydrationTimeoutStep::PermitWait, "permit_wait"),
        (HydrationTimeoutStep::DownloadPrecheck, "download_precheck"),
        (HydrationTimeoutStep::DownloadWait, "download_wait"),
    ] {
        let error = hydrator.total_timeout_error(Instant::now() - HYDRATION_TIMEOUT, step);
        assert_eq!(
            HydrationFailureReason::from_error(&error),
            Some(HydrationFailureReason::TotalTimeout)
        );
        assert!(
            matches!(error, StatsigErr::CustomError(message) if message == format!(
                "Dynamic config hydration failure: total_timeout: hydration exceeded {} seconds at {label}",
                HYDRATION_TIMEOUT.as_secs_f64()
            ))
        );
        let samples = distributions(&mut events, "remote_config_hydration.timeout");
        assert_eq!(samples.len(), 1);
        assert!(samples[0].value >= HYDRATION_TIMEOUT.as_secs_f64() * 1000.0);
        assert_eq!(
            samples[0].tags.as_ref().unwrap(),
            &HashMap::from([("step".into(), label.into())])
        );
    }
}

#[tokio::test]
async fn permit_distribution_measures_waiting_before_acquisition() {
    let (mut hydrator, mut events) = observed_hydrator();
    hydrator.response_budget = Arc::new(ResponseHydrationBudget::new(1));
    let held = hydrator.response_budget.reserve(1).await.unwrap();
    let release = async {
        tokio::time::sleep(Duration::from_millis(20)).await;
        drop(held);
    };
    let (permit, ()) = tokio::join!(hydrator.reserve_response_bytes(1), release);
    drop(permit.unwrap());
    let samples = distributions(&mut events, "remote_config_hydration.phase_latency");
    assert_eq!(samples.len(), 1);
    assert_eq!(
        samples[0].tags.as_ref().unwrap()["phase"],
        "response_permit"
    );
    assert!(samples[0].value >= 20.0);
}

#[tokio::test]
async fn json_hydration_emits_boundary_distributions_including_verification_failure() {
    let server = MockServer::start().await;
    let body = br#"{"enabled":true}"#;
    let sha = lowercase_hex(&Sha256::digest(body));
    let path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_json_blob(&server, &path, body, 2).await;
    for valid in [true, false] {
        let (hydrator, mut events) = observed_hydrator();
        let mut metadata = valid_json_metadata(&sha, body.len());
        if !valid {
            metadata["byteLength"] = Value::from(body.len() + 1);
        }
        let mut data = ResponseData::from_bytes(
            serde_json::to_vec(&serde_json::json!({
                "dynamic_configs": {"config": {
                    "defaultValue": path,
                    "remoteConfigMetadata": metadata,
                    "rules": []
                }}
            }))
            .unwrap(),
        );
        let result = hydrate_from_mock_source(&hydrator, &mut data, &server).await;
        assert_eq!(result.is_ok(), valid);
        let samples = distributions(&mut events, "remote_config_hydration.phase_latency");
        let phases: Vec<_> = samples
            .iter()
            .map(|sample| {
                assert!(sample.value >= 0.0);
                sample.tags.as_ref().unwrap()["phase"].as_str()
            })
            .collect();
        for expected in [
            "json_parse",
            "response_permit",
            "download_slot_permit",
            "download_bytes_permit",
            "verify",
            "download_wait",
        ] {
            assert_eq!(
                phases.iter().filter(|phase| **phase == expected).count(),
                1,
                "{phases:?}"
            );
        }
        assert_eq!(phases.contains(&"json_apply"), valid);
    }
}

#[tokio::test]
async fn integrated_protobuf_records_response_duration_on_error() {
    let (hydrator, mut events) = observed_hydrator();
    let mut data = ResponseData::from_bytes(vec![255]);
    assert!(
        hydrate_protobuf_for_store(
            &hydrator,
            &mut data,
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json"
        )
        .await
        .is_err()
    );
    let samples = distributions(&mut events, "remote_config_hydration.phase_latency");
    assert_eq!(samples.len(), 1);
    assert_eq!(
        samples[0].tags.as_ref().unwrap()["phase"],
        "protobuf_response"
    );
}

#[tokio::test]
async fn large_protobuf_parse_emits_one_sample_without_flooding_ops_stats() {
    let (hydrator, mut events) = observed_hydrator();
    let mut envelopes = vec![protobuf_top_level_envelope(Some(false))];
    for index in 0..1200 {
        envelopes.push(pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: format!("inline_{index}"),
            checksum: format!("checksum_{index}"),
            data: Some(
                pb::Spec {
                    salt: "salt".into(),
                    enabled: true,
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(raw_return_value(br#"{"inline":true}"#.to_vec())),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        });
    }
    envelopes.push(protobuf_done_envelope());
    let mut data = protobuf_response_data(serialize_protobuf_envelopes(&envelopes).unwrap());
    hydrate_protobuf_for_store(
        &hydrator,
        &mut data,
        "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
    )
    .await
    .unwrap();
    let samples = distributions(&mut events, "remote_config_hydration.phase_latency");
    assert_eq!(samples.len(), 1);
    assert_eq!(
        samples[0].tags.as_ref().unwrap()["phase"],
        "protobuf_response"
    );
}
