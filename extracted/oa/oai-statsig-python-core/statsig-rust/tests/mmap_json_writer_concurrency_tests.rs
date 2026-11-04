use std::{io::Write, sync::Arc, time::Duration};

use prost::Message;
use serde_json::json;
use sha2::{Digest, Sha256};
use statsig_rust::interned_values::{InternedStore, MmapArtifactState};
use statsig_rust::specs_response::statsig_config_specs::{self as pb, return_value};
use tokio::{
    io::{AsyncReadExt, AsyncWriteExt},
    net::TcpListener,
    sync::{Notify, oneshot},
    task::{AbortHandle, JoinHandle},
    time::timeout,
};
use wiremock::{Mock, MockServer, ResponseTemplate, matchers::path};

const BODY: &[u8] = br#"{"marker":"verified-blob"}"#;
const DEADLINE: Duration = Duration::from_secs(10);

fn sha() -> String {
    Sha256::digest(BODY)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn specs_body(protobuf: bool, remote: bool) -> Vec<u8> {
    let inline = json!({"marker": "inline"});
    let blob_path = format!("/v1/dynamic_config_value/{}", sha());
    if !protobuf {
        let mut config = json!({
            "type": "dynamic_config", "entity": "dynamic_config", "enabled": true,
            "salt": "concurrent-writer", "idType": "userID", "rules": [],
            "defaultValue": if remote { json!({"value": blob_path}) } else { inline },
        });
        if remote {
            config["remoteConfigMetadata"] = json!({
                "sha256": sha(), "byteLength": BODY.len(),
                "contentType": "application/json", "compression": "none",
            });
        }
        return serde_json::to_vec(&json!({
            "dynamic_configs": {"test": config},
            "feature_gates": {}, "layer_configs": {}, "experiment_to_layer": {},
            "condition_map": {}, "has_updates": true, "time": 100,
            "checksum": "concurrent-writer", "company_id": "concurrent-writer",
            "response_format": "dcs-v2",
        }))
        .unwrap();
    }
    let envelopes = [
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(
                pb::SpecsTopLevel {
                    has_updates: true,
                    time: 100,
                    checksum: "concurrent-writer".to_owned(),
                    rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                    may_have_remote_config_metadata: Some(remote),
                    ..Default::default()
                }
                .encode_to_vec(),
            ),
            ..Default::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "test".to_owned(),
            checksum: "concurrent-writer".to_owned(),
            data: Some(
                pb::Spec {
                    salt: "concurrent-writer".to_owned(),
                    enabled: true,
                    entity: pb::EntityType::EntityDynamicConfig as i32,
                    default_value: Some(pb::ReturnValue {
                        value: Some(return_value::Value::RawValue(if remote {
                            serde_json::to_vec(&blob_path).unwrap()
                        } else {
                            serde_json::to_vec(&inline).unwrap()
                        })),
                    }),
                    remote_config_metadata: remote.then_some(pb::RemoteConfigValueMetadata {
                        sha256: sha(),
                        byte_length: BODY.len() as u64,
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

fn specs(protobuf: bool, remote: bool) -> ResponseTemplate {
    let response = ResponseTemplate::new(200).set_body_bytes(specs_body(protobuf, remote));
    if protobuf {
        response
            .insert_header("content-type", "application/octet-stream")
            .insert_header("content-encoding", "statsig-br")
    } else {
        response.insert_header("content-type", "application/json")
    }
}

struct AbortOnDrop(AbortHandle);

impl Drop for AbortOnDrop {
    fn drop(&mut self) {
        self.0.abort();
    }
}

fn write(key: String, url: String) -> JoinHandle<Result<(), statsig_rust::StatsigErr>> {
    tokio::spawn(
        async move { InternedStore::fetch_and_write_mmap_with_specs_url(&key, &url).await },
    )
}

fn assert_published(key: &str) {
    assert_eq!(
        InternedStore::inspect_mmap_artifact(key).unwrap().state,
        MmapArtifactState::CommittedV2
    );
}

async fn wait_for_request(server: &MockServer, request_path: &str) {
    timeout(DEADLINE, async {
        loop {
            if server
                .received_requests()
                .await
                .unwrap()
                .iter()
                .any(|request| request.url.path() == request_path)
            {
                break;
            }
            tokio::time::sleep(Duration::from_millis(5)).await;
        }
    })
    .await
    .expect("writer must reach the requested stage");
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn mixed_format_writers_serialize_blob_loading_through_publication() {
    for slow_protobuf in [false, true] {
        let server = MockServer::start().await;
        Mock::given(path("/fast_specs"))
            .respond_with(specs(!slow_protobuf, false))
            .expect(1)
            .mount(&server)
            .await;
        let blob_path = format!("/v1/dynamic_config_value/{}", sha());
        let blob_started = Arc::new(Notify::new());
        let (release_blob, mut wait_for_release) = oneshot::channel();
        let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
        let slow_origin = format!("http://{}", listener.local_addr().unwrap());
        let blob_server = tokio::spawn({
            let blob_started = Arc::clone(&blob_started);
            async move {
                // Specs and their relative blob URL must share an origin.
                for (expected_path, is_blob) in [("/slow_specs", false), (blob_path.as_str(), true)]
                {
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
                    let mut fields = request.split_whitespace();
                    assert_eq!(fields.next(), Some("GET"));
                    assert_eq!(
                        fields.next().unwrap().split('?').next(),
                        Some(expected_path)
                    );
                    let body = if is_blob {
                        blob_started.notify_one();
                        (&mut wait_for_release)
                            .await
                            .expect("test must release blob");
                        BODY.to_vec()
                    } else {
                        specs_body(slow_protobuf, true)
                    };
                    let (content_type, encoding) = if slow_protobuf && !is_blob {
                        (
                            "application/octet-stream",
                            "Content-Encoding: statsig-br\r\n",
                        )
                    } else {
                        ("application/json", "")
                    };
                    let headers = format!(
                        "HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n{encoding}Content-Length: {}\r\nConnection: close\r\n\r\n",
                        body.len()
                    );
                    socket.write_all(headers.as_bytes()).await.unwrap();
                    socket.write_all(&body).await.unwrap();
                }
            }
        });
        let _server_abort = AbortOnDrop(blob_server.abort_handle());
        let suffix = uuid::Uuid::new_v4();
        let slow_key = format!("mmap-slow-{suffix}");
        let fast_key = format!("mmap-fast-{suffix}");
        let slow = write(slow_key.clone(), format!("{slow_origin}/slow_specs"));
        let _slow_abort = AbortOnDrop(slow.abort_handle());
        timeout(DEADLINE, blob_started.notified())
            .await
            .expect("slow writer must reach the blocked blob response");
        let mut fast = write(fast_key.clone(), format!("{}/fast_specs", server.uri()));
        let _fast_abort = AbortOnDrop(fast.abort_handle());
        wait_for_request(&server, "/fast_specs").await;
        // The blob gate stays closed throughout this observation, even if the
        // runner pauses. Unlike a fixed response delay, it cannot expire first.
        let early_result = timeout(Duration::from_millis(100), &mut fast).await;
        let still_queued = early_result.is_err();
        release_blob.send(()).expect("blob server must be waiting");
        timeout(DEADLINE, async {
            slow.await.unwrap().unwrap();
            match early_result {
                Ok(result) => result.unwrap().unwrap(),
                Err(_) => fast.await.unwrap().unwrap(),
            }
        })
        .await
        .expect("both writer formats must make progress after the blob completes");
        timeout(DEADLINE, blob_server).await.unwrap().unwrap();
        assert!(
            still_queued,
            "another key must wait for the first writer to publish"
        );
        assert_published(&slow_key);
        assert_published(&fast_key);
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn cancelling_blob_loading_releases_both_writer_locks() {
    for slow_protobuf in [false, true] {
        let server = MockServer::start().await;
        Mock::given(path("/slow_specs"))
            .respond_with(specs(slow_protobuf, true))
            .mount(&server)
            .await;
        Mock::given(path("/fast_specs"))
            .respond_with(specs(!slow_protobuf, false))
            .mount(&server)
            .await;
        let blob_path = format!("/v1/dynamic_config_value/{}", sha());
        Mock::given(path(&blob_path))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(BODY.to_vec())
                    .set_delay(Duration::from_secs(5)),
            )
            .mount(&server)
            .await;
        let key = format!("mmap-cancelled-{}", uuid::Uuid::new_v4());
        let slow = write(key.clone(), format!("{}/slow_specs", server.uri()));
        wait_for_request(&server, &blob_path).await;
        // Same-key recovery needs the file lock as well as the intern graph lock.
        let recovery = write(key.clone(), format!("{}/fast_specs", server.uri()));
        slow.abort();
        assert!(slow.await.unwrap_err().is_cancelled());
        timeout(DEADLINE, recovery)
            .await
            .expect("cancellation must release writer locks")
            .unwrap()
            .unwrap();
        assert_published(&key);
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn invalid_blob_releases_writer_locks_and_allows_next_publication() {
    for protobuf in [false, true] {
        let server = MockServer::start().await;
        Mock::given(path("/invalid_specs"))
            .respond_with(specs(protobuf, true))
            .mount(&server)
            .await;
        Mock::given(path("/valid_specs"))
            .respond_with(specs(protobuf, false))
            .mount(&server)
            .await;
        Mock::given(path(format!("/v1/dynamic_config_value/{}", sha())))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(vec![b'x'; BODY.len()]),
            )
            .expect(1)
            .mount(&server)
            .await;
        let key = format!("mmap-invalid-{}", uuid::Uuid::new_v4());
        let invalid = timeout(
            DEADLINE,
            InternedStore::fetch_and_write_mmap_with_specs_url(
                &key,
                &format!("{}/invalid_specs", server.uri()),
            ),
        )
        .await
        .unwrap();
        assert!(invalid.is_err(), "an invalid blob must not be published");
        timeout(
            DEADLINE,
            InternedStore::fetch_and_write_mmap_with_specs_url(
                &key,
                &format!("{}/valid_specs", server.uri()),
            ),
        )
        .await
        .expect("failure must release writer locks")
        .unwrap();
        assert_published(&key);
    }
}
