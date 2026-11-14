use super::*;
use rusty_fork::rusty_fork_test;

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
        // The SDK logger is process-wide.
        tokio::runtime::Builder::new_current_thread().enable_all().build().unwrap()
            .block_on(check_blob_warnings());
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
