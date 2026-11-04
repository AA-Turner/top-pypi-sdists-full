use std::{io::Write, sync::Arc, time::Duration};

use prost::Message;
use serde_json::json;
use sha2::{Digest, Sha256};
use statsig_rust::interned_values::{InternedStore, MmapArtifactState};
use statsig_rust::specs_response::statsig_config_specs::{self as pb, return_value};
use statsig_rust::{DynamicConfigEvaluationOptions, Statsig, StatsigOptions, StatsigUser};
use tokio::{
    io::{AsyncReadExt, AsyncWriteExt},
    net::TcpListener,
    sync::Notify,
    time::timeout,
};
use wiremock::{
    Mock, MockServer, ResponseTemplate,
    matchers::{method, path},
};

fn sha256(body: &[u8]) -> String {
    Sha256::digest(body)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn protobuf_specs(config_name: &str, body: &[u8]) -> Vec<u8> {
    let sha = sha256(body);
    let envelopes = [
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(
                pb::SpecsTopLevel {
                    has_updates: true,
                    time: 100,
                    checksum: config_name.to_owned(),
                    rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                    may_have_remote_config_metadata: Some(true),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: config_name.to_owned(),
            checksum: config_name.to_owned(),
            data: Some(
                pb::Spec {
                    enabled: true,
                    salt: "writer-sdk-concurrency".to_owned(),
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(pb::ReturnValue {
                        value: Some(return_value::Value::RawValue(
                            serde_json::to_vec(&format!("/v1/dynamic_config_value/{sha}")).unwrap(),
                        )),
                    }),
                    remote_config_metadata: Some(pb::RemoteConfigValueMetadata {
                        sha256: sha,
                        byte_length: body.len() as u64,
                        content_type: "application/json".to_owned(),
                        compression: "none".to_owned(),
                    }),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Done as i32,
            ..Default::default()
        },
    ];
    let frames: Vec<_> = envelopes
        .iter()
        .flat_map(Message::encode_length_delimited_to_vec)
        .collect();
    let mut compressed = Vec::new();
    {
        let mut writer = brotli::CompressorWriter::new(&mut compressed, 4096, 5, 22);
        writer.write_all(&frames).unwrap();
    }
    compressed
}

fn sdk(key: &str, server: &MockServer, specs_path: &str) -> Statsig {
    Statsig::new(
        key,
        Some(Arc::new(StatsigOptions {
            specs_url: Some(format!("{}{specs_path}", server.uri())),
            log_event_url: Some(format!("{}/log_event", server.uri())),
            init_timeout_ms: Some(1000),
            enable_id_lists: Some(false),
            disable_all_logging: Some(true),
            disable_country_lookup: Some(true),
            use_third_party_ua_parser: Some(false),
            wait_for_country_lookup_init: Some(false),
            wait_for_user_agent_init: Some(false),
            fallback_to_statsig_api: Some(false),
            disable_disk_access: Some(true),
            specs_sync_interval_ms: Some(3_600_000),
            ..StatsigOptions::new()
        })),
    )
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn tiny_protobuf_writer_does_not_block_unrelated_sdk_blob_downloads() {
    let writer_body = br#"{"marker":"writer"}"#;
    let json_body = br#"{"marker":"json-sdk"}"#;
    let protobuf_body = br#"{"marker":"protobuf-sdk"}"#;
    let json_path = format!("/v1/dynamic_config_value/{}", sha256(json_body));
    let protobuf_path = format!("/v1/dynamic_config_value/{}", sha256(protobuf_body));
    let server = MockServer::start().await;

    for (blob_path, body) in [
        (&json_path, json_body.as_slice()),
        (&protobuf_path, protobuf_body.as_slice()),
    ] {
        Mock::given(method("GET"))
            .and(path(blob_path))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(body.to_vec()),
            )
            .expect(1)
            .mount(&server)
            .await;
    }
    Mock::given(path("/json_specs"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "dynamic_configs": {"json_config": {
                "type": "dynamic_config", "entity": "dynamic_config", "enabled": true,
                "salt": "writer-sdk-concurrency", "idType": "userID", "rules": [],
                "defaultValue": {"value": json_path},
                "remoteConfigMetadata": {
                    "sha256": sha256(json_body), "byteLength": json_body.len(),
                    "contentType": "application/json", "compression": "none"
                }
            }},
            "feature_gates": {}, "layer_configs": {}, "experiment_to_layer": {},
            "condition_map": {}, "has_updates": true, "time": 100,
            "checksum": "json-sdk", "company_id": "writer-sdk-concurrency",
            "response_format": "dcs-v2"
        })))
        .mount(&server)
        .await;
    Mock::given(path("/protobuf_specs"))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/octet-stream")
                .insert_header("content-encoding", "statsig-br")
                .set_body_bytes(protobuf_specs("protobuf_config", protobuf_body)),
        )
        .mount(&server)
        .await;
    Mock::given(method("POST"))
        .and(path("/log_event"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({"success": true})))
        .mount(&server)
        .await;

    let writer_started = Arc::new(Notify::new());
    let release_writer = Arc::new(Notify::new());
    let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
    let writer_origin = format!("http://{}", listener.local_addr().unwrap());
    let writer_server = tokio::spawn({
        let writer_started = Arc::clone(&writer_started);
        let release_writer = Arc::clone(&release_writer);
        async move {
            // Each response closes its connection: one specs GET and one blob GET.
            for expected_path in [
                "/writer_specs".to_owned(),
                format!("/v1/dynamic_config_value/{}", sha256(writer_body)),
            ] {
                let (mut socket, _) = listener.accept().await.unwrap();
                let mut request = Vec::new();
                let mut buffer = [0; 2048];
                while !request.windows(4).any(|bytes| bytes == b"\r\n\r\n") {
                    let count = socket.read(&mut buffer).await.unwrap();
                    assert_ne!(count, 0);
                    request.extend_from_slice(&buffer[..count]);
                    assert!(request.len() < 16_384);
                }
                let request = String::from_utf8_lossy(&request);
                assert_eq!(request.split_whitespace().next(), Some("GET"));
                assert!(
                    request
                        .split_whitespace()
                        .nth(1)
                        .unwrap()
                        .starts_with(&expected_path)
                );
                let (content_type, content_encoding, body) = if expected_path == "/writer_specs" {
                    (
                        "application/octet-stream",
                        "Content-Encoding: statsig-br\r\n",
                        protobuf_specs("writer_config", writer_body),
                    )
                } else {
                    writer_started.notify_one();
                    release_writer.notified().await;
                    ("application/json", "", writer_body.to_vec())
                };
                let headers = format!(
                    "HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n{content_encoding}Content-Length: {}\r\nConnection: close\r\n\r\n",
                    body.len()
                );
                socket.write_all(headers.as_bytes()).await.unwrap();
                socket.write_all(&body).await.unwrap();
            }
        }
    });
    let suffix = uuid::Uuid::new_v4();
    let writer_key = format!("mmap-writer-sdk-concurrency-{suffix}");
    let writer = tokio::spawn({
        let writer_key = writer_key.clone();
        async move {
            InternedStore::fetch_and_write_mmap_with_specs_url(
                &writer_key,
                &format!("{writer_origin}/writer_specs"),
            )
            .await
        }
    });
    timeout(Duration::from_secs(10), writer_started.notified())
        .await
        .expect("writer must hold admission while its blob response is blocked");

    let json_sdk = sdk(&format!("json-sdk-{suffix}"), &server, "/json_specs");
    let protobuf_sdk = sdk(
        &format!("protobuf-sdk-{suffix}"),
        &server,
        "/protobuf_specs",
    );
    let initialized = timeout(Duration::from_secs(2), async {
        tokio::join!(
            json_sdk.initialize_with_details(),
            protobuf_sdk.initialize_with_details()
        )
    })
    .await;
    let writer_was_blocked = !writer.is_finished();
    let requests = server.received_requests().await.unwrap();
    let blob_gets_before_release = [&json_path, &protobuf_path].map(|blob_path| {
        requests
            .iter()
            .filter(|request| request.url.path() == blob_path)
            .count()
    });
    let user = StatsigUser::with_user_id("concurrent-sdk-user");
    let json_value = json_sdk
        .get_dynamic_config_with_options(
            &user,
            "json_config",
            DynamicConfigEvaluationOptions {
                disable_exposure_logging: true,
            },
        )
        .value;
    let protobuf_value = protobuf_sdk
        .get_dynamic_config_with_options(
            &user,
            "protobuf_config",
            DynamicConfigEvaluationOptions {
                disable_exposure_logging: true,
            },
        )
        .value;

    // Unblock and join all work before asserting the regression, including on failure.
    release_writer.notify_one();
    timeout(Duration::from_secs(10), writer)
        .await
        .unwrap()
        .unwrap()
        .unwrap();
    timeout(Duration::from_secs(10), writer_server)
        .await
        .unwrap()
        .unwrap();
    timeout(Duration::from_secs(5), async {
        tokio::try_join!(json_sdk.shutdown(), protobuf_sdk.shutdown())
    })
    .await
    .unwrap()
    .unwrap();

    let (json_details, protobuf_details) =
        initialized.expect("SDK initialization must remain bounded");
    let json_details = json_details.unwrap();
    let protobuf_details = protobuf_details.unwrap();
    println!(
        "Concurrent SDK initialization: JSON={} ms (success={}), Protobuf={} ms (success={}), blob GETs before writer release={blob_gets_before_release:?}",
        json_details.duration_ms,
        json_details.init_success,
        protobuf_details.duration_ms,
        protobuf_details.init_success,
    );
    assert!(
        json_details.init_success,
        "JSON SDK must initialize before writer release"
    );
    assert!(
        protobuf_details.init_success,
        "Protobuf SDK must initialize before writer release"
    );
    assert!(writer_was_blocked);
    assert_eq!(blob_gets_before_release, [1, 1]);
    assert_eq!(json_value.get("marker"), Some(&json!("json-sdk")));
    assert_eq!(protobuf_value.get("marker"), Some(&json!("protobuf-sdk")));
    assert_eq!(
        InternedStore::inspect_mmap_artifact(&writer_key)
            .unwrap()
            .state,
        MmapArtifactState::CommittedV2
    );
}
