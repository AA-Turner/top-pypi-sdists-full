use super::*;
use rusty_fork::rusty_fork_test;

const INIT_BLOB_METRIC: &str = "statsig.sdk.initialization.config_spec_not_ready_due_to_blob";
const REPORT_BLOB_FAILURE: &str = "STATSIG_REPORT_BLOB_INIT_FAILURE";

#[tokio::test]
async fn inline_values_that_look_like_blob_links_do_not_fetch() {
    for codec in CODECS {
        let server = MockServer::start().await;
        let path = format!("/v1/dynamic_config_value/{}", "a".repeat(64));
        let placeholder = json!({"value": path});
        let application = json!({
            "url": format!("{}{path}", server.uri()), "nested": {"url": path},
            "remoteConfigMetadata": {"description": "ordinary application data"},
        });
        let payload = full_payload(
            json!({
                "placeholder": inline_config(placeholder.clone()),
                "application": inline_config(application.clone()),
            }),
            1,
        );
        let (sdk, _, observer, _) = initialize(&server, codec, "inline-paths", &payload).await;
        assert!(sdk.is_config_spec_ready());
        assert_eq!(evaluate(&sdk, "user", "placeholder"), placeholder);
        assert_eq!(evaluate(&sdk, "user", "application"), application);
        assert_eq!(unavailable_blob_count(&observer), 0.0);
        sdk.shutdown().await.unwrap();
        assert!(
            server
                .received_requests()
                .await
                .unwrap()
                .iter()
                .all(|request| !request.url.path().starts_with("/v1/dynamic_config_value/"))
        );
    }
}

#[tokio::test]
async fn malformed_specs_or_metadata_reject_the_snapshot() {
    for codec in CODECS {
        let failed = RemoteValue::new("corrupt-body");
        let configs = json!({
            "failed_blob": remote_config(&failed),
            "healthy_inline": inline_config(json!({"marker": "must-not-publish"})),
        });
        let mut top_level = full_payload(configs.clone(), 1);
        top_level["experiment_to_layer"] = json!(42);
        let mut metadata = configs.clone();
        let mut invalid = remote_config(&RemoteValue::new("unsupported-compression"));
        invalid["remoteConfigMetadata"]["compression"] = json!("snappy");
        metadata["invalid_reference"] = invalid;
        let mut cases = vec![
            ("top-level", top_level),
            ("compression", full_payload(metadata, 1)),
        ];
        if matches!(codec, Codec::Json) {
            let mut missing_type = configs;
            missing_type["failed_blob"]
                .as_object_mut()
                .unwrap()
                .remove("type");
            cases.push(("missing-type", full_payload(missing_type, 1)));
        }

        for (case, payload) in cases {
            let server = MockServer::start().await;
            mount_blob(&server, &failed, true).await;
            mount_specs(&server, codec, &payload)
                .await
                .replace(codec.response(&payload));
            let observer = Arc::new(MockObservabilityClient::new());
            let sdk = Statsig::new(
                &format!("secret-malformed-{}-{case}", codec.name()),
                Some(Arc::new(sdk_options(&server.uri(), &observer))),
            );
            let error = sdk.initialize().await.unwrap_err();
            if case == "compression" {
                assert!(error.to_string().contains("invalid_compression"), "{error}");
            }
            assert_partial_cursor(&sdk);
            assert!(sdk.specs_snapshot().dynamic_configs.0.is_empty());
            assert_eq!(unavailable_blob_count(&observer), 0.0);
            sdk.shutdown().await.unwrap();
        }
    }
}

rusty_fork_test! {
    #[test]
    fn failed_blobs_warn_once_per_sha_even_after_retry() {
        std::env::set_var(REPORT_BLOB_FAILURE, "true");
        // The SDK logger is process-wide.
        tokio::runtime::Builder::new_current_thread().enable_all().build().unwrap()
            .block_on(check_blob_warnings());
    }

    #[test]
    fn blob_metric_uses_the_final_init_result() {
        std::env::remove_var("STATSIG_ENABLE_PARTIAL_BLOB_PUBLICATION");
        tokio::runtime::Builder::new_current_thread().enable_all().build().unwrap()
            .block_on(check_init_fallback_metric());
    }
}

async fn check_blob_warnings() {
    for codec in CODECS {
        let server = MockServer::start().await;
        let healthy = RemoteValue::new("healthy");
        let shared = RemoteValue::new("shared-failure");
        let rule_only = RemoteValue::new("rule-only-failure");
        let short = RemoteValue::new("length-failure");
        mount_blob(&server, &healthy, false).await;
        mount_blob(&server, &shared, true).await;
        mount_blob(&server, &rule_only, true).await;
        Mock::given(method("GET"))
            .and(path(short.path()))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(b"{}"),
            )
            .mount(&server)
            .await;
        let mut configs = mixed_configs(&healthy, &shared);
        configs["rule_only"] = config_with_remote_rule(inline_config(json!({})), &rule_only);
        configs["short"] = remote_config(&short);
        let payload = full_payload(configs, 1);
        let dcs = mount_specs(&server, codec, &payload).await;
        let logger = Arc::new(MockLogProvider::new());
        let (sdk, _, observer) = new_sdk(
            &server.uri(),
            codec,
            "warning",
            false,
            Some(logger.clone()),
            None,
        );
        sdk.initialize().await.unwrap();

        dcs.replace(codec.response(&payload));
        wait_for_requests(&server, &rule_only.path(), 2).await;
        let warnings: Vec<_> = logger
            .logs
            .lock()
            .iter()
            .filter_map(|log| match log {
                RecordedLog::Warn(_, message) if message.starts_with("Blob hydration failed:") => {
                    Some(message.clone())
                }
                _ => None,
            })
            .collect();
        assert_eq!(warnings.len(), 3);
        assert_init_blob_metric(&observer, 1).await;
        for (blob, reason) in [
            (&shared, "checksum_mismatch"),
            (&rule_only, "checksum_mismatch"),
            (&short, "byte_length_mismatch"),
        ] {
            assert!(warnings.iter().any(|msg| msg.contains(&blob.sha)
                && msg.contains(&format!("format={}", codec.name()))
                && msg.contains(&format!("failure_reason={reason}"))));
        }
        let counts: Vec<_> = observer
            .increment_calls
            .lock()
            .unwrap()
            .iter()
            .filter(|(name, _, _)| name == UNAVAILABLE_BLOB_METRIC)
            .map(|(_, count, tags)| {
                let tags = tags.as_ref().unwrap();
                assert_eq!(tags["format"], codec.name());
                (tags["failure_reason"].clone(), *count)
            })
            .collect();
        assert_eq!(counts.len(), 2);
        assert!(counts.contains(&("checksum_mismatch".to_string(), 2.0)));
        assert!(counts.contains(&("byte_length_mismatch".to_string(), 1.0)));
        sdk.shutdown().await.unwrap();
    }
}

async fn assert_init_blob_metric(observer: &MockObservabilityClient, expected_count: usize) {
    // Initialization is queued after the counter, so zero is safe to assert once it arrives.
    assert_eventually!(|| {
        let calls = observer.dist_calls.lock().unwrap();
        calls
            .iter()
            .any(|(name, ..)| name == "statsig.sdk.initialization")
    });
    let calls = observer.increment_calls.lock().unwrap();
    let values: Vec<_> = calls
        .iter()
        .filter_map(|(name, value, _)| (name == INIT_BLOB_METRIC).then_some(*value))
        .collect();
    assert_eq!(values, vec![1.0; expected_count]);
}

async fn check_init_fallback_metric() {
    let codec = Codec::Json;
    let blob = RemoteValue::new("corrupt");
    let slow_blob = blob.response(false).set_delay(Duration::from_secs(3));
    let cached_specs = full_payload(json!({"config": remote_config(&blob)}), 1);
    let blob_failure = codec.response(&cached_specs);
    let ready = codec.response(&full_payload(json!({}), 2));
    let unrelated_failure = ResponseTemplate::new(200).set_body_string("malformed specs");
    for (setting, fallback, timeout, expected_ready, expected_count) in [
        (None, blob_failure.clone(), None, false, 0),
        (Some("false"), blob_failure.clone(), None, false, 0),
        (Some("invalid"), blob_failure.clone(), None, false, 0),
        (Some("1"), blob_failure.clone(), None, false, 1),
        (Some("true"), ready, None, true, 0),
        (Some("true"), unrelated_failure, None, false, 0),
        (Some("true"), blob_failure, Some(750), false, 0),
    ] {
        match setting {
            Some(value) => std::env::set_var(REPORT_BLOB_FAILURE, value),
            None => std::env::remove_var(REPORT_BLOB_FAILURE),
        }
        let server = MockServer::start().await;
        let origin = mount_blob(&server, &blob, true).await;
        if timeout.is_some() {
            // Cached specs get a corrupt response. The fallback download is still pending at the deadline.
            origin.once(blob.response(true), slow_blob.clone());
        }
        mount_specs(&server, codec, &cached_specs)
            .await
            .replace(fallback);
        let (sdk, store, observer) = new_sdk(&server.uri(), codec, "metric", false, None, timeout);
        store.mock_json_bytes(&cached_specs.to_string());
        let details = sdk.initialize_with_details().await.unwrap();
        let blob_reads = get_count(&server, &blob.path()).await;
        assert!(blob_reads > 0);
        if timeout.is_some() {
            assert!(blob_reads >= 2);
            let failure = details.failure_details.unwrap();
            assert_eq!(failure.reason, "Initialization timed out");
        }
        assert!(get_count(&server, DCS_PATH).await > 0);
        assert_eq!(details.is_config_spec_ready, expected_ready);
        assert_init_blob_metric(&observer, expected_count).await;
        sdk.shutdown().await.unwrap();
    }
}
