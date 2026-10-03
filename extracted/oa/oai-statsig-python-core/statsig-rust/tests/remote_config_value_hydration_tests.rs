mod utils;

use std::collections::{HashMap, HashSet};
use std::io::{Read, Write};
use std::sync::Arc;

use crate::utils::mock_data_store::MockDataStore;
use brotli::enc::BrotliEncoderParams;
use flate2::{Compression, write::GzEncoder};
use prost::Message;
use serde_json::json;
use sha2::{Digest, Sha256};
use statsig_rust::{
    SpecAdapterConfig, SpecsAdapterType, SpecsSource, SpecsUpdate, Statsig, StatsigErr,
    StatsigOptions, StatsigUser,
    networking::ResponseData,
    specs_response::{
        proto_stream_reader::BUFFER_SIZE,
        statsig_config_specs::{self as pb, return_value},
    },
};
use wiremock::matchers::{header, method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

const SDK_KEY: &str = "secret-remote-config-hydration";
const DOWNLOAD_PATH_PREFIX: &str = "/v1/dynamic_config_value/";

#[tokio::test]
async fn initialize_hydrates_remote_dynamic_config_before_evaluation() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"value","nested":{"enabled":true}}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_remote_value(&server, &download_path, remote_value).await;
    mount_dcs(
        &server,
        remote_dcs(&server, &download_path, &sha, remote_value.len()),
    )
    .await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("value")));
    assert_eq!(config.value.get("nested"), Some(&json!({"enabled": true})));

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn initialize_hydrates_gzip_remote_dynamic_config_before_evaluation() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"gzip","nested":{"enabled":true}}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_gzip_remote_value(&server, &download_path, remote_value).await;
    let mut dcs = remote_dcs(&server, &download_path, &sha, remote_value.len());
    dcs["dynamic_configs"]["large_config"]["remoteConfigMetadata"]["compression"] = json!("gzip");
    mount_dcs(&server, dcs).await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("gzip")));
    assert_eq!(config.value.get("nested"), Some(&json!({"enabled": true})));

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_hydrates_gzip_remote_dynamic_config_with_identity_http_body() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"storage-was-gzipped"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_remote_value(&server, &download_path, remote_value).await;
    let mut dcs = remote_dcs(&server, &download_path, &sha, remote_value.len());
    dcs["dynamic_configs"]["large_config"]["remoteConfigMetadata"]["compression"] = json!("gzip");
    mount_dcs(&server, dcs).await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(
        config.value.get("large"),
        Some(&json!("storage-was-gzipped"))
    );

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_hydrates_zstd_remote_dynamic_config_before_evaluation() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"zstd","nested":{"enabled":true}}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_zstd_remote_value(&server, &download_path, remote_value).await;
    let mut dcs = remote_dcs(&server, &download_path, &sha, remote_value.len());
    dcs["dynamic_configs"]["large_config"]["remoteConfigMetadata"]["compression"] = json!("zstd");
    mount_dcs(&server, dcs).await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("zstd")));
    assert_eq!(config.value.get("nested"), Some(&json!({"enabled": true})));

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_hydrates_zstd_remote_dynamic_config_with_identity_http_body() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"storage-was-zstd-compressed"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_remote_value(&server, &download_path, remote_value).await;
    let mut dcs = remote_dcs(&server, &download_path, &sha, remote_value.len());
    dcs["dynamic_configs"]["large_config"]["remoteConfigMetadata"]["compression"] = json!("zstd");
    mount_dcs(&server, dcs).await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(
        config.value.get("large"),
        Some(&json!("storage-was-zstd-compressed"))
    );

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_rejects_zstd_remote_value_that_exceeds_declared_length() {
    let server = MockServer::start().await;
    let declared_value = br#"{"large":"short"}"#;
    let expanded_value = format!(r#"{{"large":"{}"}}"#, "x".repeat(64 * 1024));
    let sha = lowercase_hex(&Sha256::digest(declared_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_zstd_remote_value(&server, &download_path, expanded_value.as_bytes()).await;
    let mut dcs = remote_dcs(&server, &download_path, &sha, declared_value.len());
    dcs["dynamic_configs"]["large_config"]["remoteConfigMetadata"]["compression"] = json!("zstd");
    mount_dcs(&server, dcs).await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    let error = statsig.initialize().await.unwrap_err();

    assert!(matches!(
        error,
        StatsigErr::CustomError(message)
            if message.starts_with("Dynamic config hydration failure: download_failed:")
                && message.contains("Response exceeded maximum allowed bytes")
    ));

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_rejects_unsupported_remote_value_compression_before_download() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"unsupported"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    let mut dcs = remote_dcs(&server, &download_path, &sha, remote_value.len());
    dcs["dynamic_configs"]["large_config"]["remoteConfigMetadata"]["compression"] = json!("snappy");
    mount_dcs(&server, dcs).await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    let error = statsig.initialize().await.unwrap_err();

    assert!(matches!(
        error,
        StatsigErr::CustomError(message)
            if message.starts_with("Dynamic config hydration failure: invalid_compression:")
    ));

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn initialize_rejects_conflicting_remote_value_compression_before_download() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"conflicting"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    let mut dcs = remote_dcs(&server, &download_path, &sha, remote_value.len());
    dcs["dynamic_configs"]["gzip_config"] = dcs["dynamic_configs"]["large_config"].clone();
    dcs["dynamic_configs"]["gzip_config"]["remoteConfigMetadata"]["compression"] = json!("gzip");
    mount_dcs(&server, dcs).await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    let error = statsig.initialize().await.unwrap_err();

    assert!(matches!(
        error,
        StatsigErr::CustomError(message)
            if message.starts_with("Dynamic config hydration failure: metadata_conflict:")
    ));

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn initialize_uses_configured_source_for_relative_remote_value_paths() {
    let dcs_server = MockServer::start().await;
    let blob_server = MockServer::start().await;
    let remote_value = br#"{"large":"from-separate-origin"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_remote_value(&blob_server, &download_path, remote_value).await;
    mount_dcs(
        &dcs_server,
        remote_dcs_with_placeholder(&download_path, &sha, remote_value.len()),
    )
    .await;

    let options = StatsigOptions {
        specs_url: Some(format!("{}/v2/download_config_specs", dcs_server.uri())),
        remote_config_value_source_url: Some(blob_server.uri()),
        disable_all_logging: Some(true),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(SDK_KEY, Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(
        config.value.get("large"),
        Some(&json!("from-separate-origin"))
    );

    statsig.shutdown().await.unwrap();
    dcs_server.verify().await;
    blob_server.verify().await;
}

#[tokio::test]
async fn initialize_fails_when_remote_value_integrity_check_fails() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"value"}"#;
    let incorrect_sha = "a".repeat(64);
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{incorrect_sha}");

    mount_remote_value(&server, &download_path, remote_value).await;
    mount_dcs(
        &server,
        remote_dcs(&server, &download_path, &incorrect_sha, remote_value.len()),
    )
    .await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    let error = statsig.initialize().await.unwrap_err();

    assert!(matches!(
        error,
        StatsigErr::CustomError(message)
            if message.starts_with("Dynamic config hydration failure: checksum_mismatch:")
    ));

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn initialize_hydrates_remote_protobuf_dynamic_config_before_evaluation() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"protobuf","nested":{"enabled":true}}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_remote_value(&server, &download_path, remote_value).await;
    mount_protobuf_dcs(
        &server,
        remote_protobuf_dcs(&server, &download_path, &sha, remote_value.len()),
    )
    .await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("protobuf")));
    assert_eq!(config.value.get("nested"), Some(&json!({"enabled": true})));

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn initialize_hydrates_gzip_remote_protobuf_dynamic_config_before_evaluation() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"gzip-protobuf","nested":{"enabled":true}}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_gzip_remote_value(&server, &download_path, remote_value).await;
    mount_protobuf_dcs(
        &server,
        remote_protobuf_dcs_with_compression(
            &server,
            &download_path,
            &sha,
            remote_value.len(),
            "gzip",
        ),
    )
    .await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("gzip-protobuf")));
    assert_eq!(config.value.get("nested"), Some(&json!({"enabled": true})));

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_hydrates_zstd_remote_protobuf_dynamic_config_before_evaluation() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"zstd-protobuf","nested":{"enabled":true}}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_zstd_remote_value(&server, &download_path, remote_value).await;
    mount_protobuf_dcs(
        &server,
        remote_protobuf_dcs_with_compression(
            &server,
            &download_path,
            &sha,
            remote_value.len(),
            "zstd",
        ),
    )
    .await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("zstd-protobuf")));
    assert_eq!(config.value.get("nested"), Some(&json!({"enabled": true})));

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_hydrates_zstd_remote_value_from_zstd_protobuf_snapshot() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"zstd-snapshot","nested":{"enabled":true}}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");

    mount_zstd_remote_value(&server, &download_path, remote_value).await;
    let brotli_snapshot = remote_protobuf_dcs_with_compression(
        &server,
        &download_path,
        &sha,
        remote_value.len(),
        "zstd",
    );
    let mut uncompressed_snapshot = Vec::new();
    brotli::Decompressor::new(brotli_snapshot.as_slice(), 4096)
        .read_to_end(&mut uncompressed_snapshot)
        .unwrap();
    let zstd_snapshot = zstd::stream::encode_all(uncompressed_snapshot.as_slice(), 3).unwrap();
    mount_protobuf_dcs_with_encoding(&server, zstd_snapshot, "statsig-zstd").await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    statsig.initialize().await.unwrap();

    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("zstd-snapshot")));
    assert_eq!(config.value.get("nested"), Some(&json!({"enabled": true})));

    statsig.shutdown().await.unwrap();
    server.verify().await;
}

#[tokio::test]
async fn initialize_rejects_remote_protobuf_value_when_hydration_fails() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"protobuf"}"#;
    let incorrect_sha = "a".repeat(64);
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{incorrect_sha}");

    mount_remote_value(&server, &download_path, remote_value).await;
    mount_protobuf_dcs(
        &server,
        remote_protobuf_dcs(&server, &download_path, &incorrect_sha, remote_value.len()),
    )
    .await;

    let statsig = Statsig::new(SDK_KEY, Some(options_for(&server)));
    let error = statsig.initialize().await.unwrap_err();

    assert!(matches!(
        error,
        StatsigErr::CustomError(message)
            if message.starts_with("Dynamic config hydration failure: checksum_mismatch:")
    ));

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn initialize_hydrates_cached_data_store_remote_value_before_evaluation() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"from-data-store"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    let cached_dcs = remote_dcs(&server, &download_path, &sha, remote_value.len()).to_string();
    let data_store = Arc::new(MockDataStore::with_json_cache(&cached_dcs));

    mount_remote_value(&server, &download_path, remote_value).await;

    let options = StatsigOptions {
        data_store: Some(data_store),
        specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
        spec_adapters_config: Some(vec![data_store_adapter_config()]),
        disable_all_logging: Some(true),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(SDK_KEY, Some(Arc::new(options)));

    let details = statsig.initialize_with_details().await.unwrap();

    assert!(details.init_success);
    assert_eq!(
        details.source,
        SpecsSource::Adapter("DataStore".to_string())
    );
    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!("from-data-store")));

    statsig.shutdown().await.unwrap();
}

#[tokio::test]
async fn initialize_hydrates_cached_data_store_remote_protobuf_value_before_evaluation() {
    assert_cached_remote_protobuf_hydration(false).await;
}

#[tokio::test]
async fn initialize_hydrates_read_only_data_store_remote_protobuf_value_before_evaluation() {
    assert_cached_remote_protobuf_hydration(true).await;
}

async fn assert_cached_remote_protobuf_hydration(read_only: bool) {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"proto-from-data-store"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    let cached_dcs = remote_protobuf_dcs(&server, &download_path, &sha, remote_value.len());
    let data_store =
        Arc::new(MockDataStore::with_proto_cache(&cached_dcs).with_read_only(read_only));

    mount_remote_value(&server, &download_path, remote_value).await;

    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
        spec_adapters_config: Some(vec![data_store_adapter_config()]),
        disable_all_logging: Some(true),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(SDK_KEY, Some(Arc::new(options)));

    let details = statsig.initialize_with_details().await.unwrap();

    assert!(details.init_success);
    assert_eq!(
        details.source,
        SpecsSource::Adapter("DataStore".to_string())
    );
    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(
        config.value.get("large"),
        Some(&json!("proto-from-data-store"))
    );

    statsig.shutdown().await.unwrap();
    assert!(data_store.num_get_bytes_calls() > 0);
    assert_eq!(data_store.num_set_bytes_calls(), 0);
    assert_eq!(data_store.num_set_calls(), 0);
}

#[tokio::test]
async fn network_hydration_writes_offline_ready_protobuf_to_data_store() {
    assert_network_hydration_data_store_behavior("statsig-br", ReadOnlyBehavior::Never).await;
}

#[tokio::test]
async fn network_hydration_writes_offline_ready_zstd_protobuf_to_data_store() {
    assert_network_hydration_data_store_behavior("statsig-zstd", ReadOnlyBehavior::Never).await;
}

#[tokio::test]
async fn network_hydration_skips_read_only_protobuf_data_store() {
    assert_network_hydration_data_store_behavior("statsig-br", ReadOnlyBehavior::Always).await;
}

#[tokio::test]
async fn network_hydration_skips_read_only_zstd_protobuf_data_store() {
    assert_network_hydration_data_store_behavior("statsig-zstd", ReadOnlyBehavior::Always).await;
}

#[tokio::test]
async fn network_hydration_skips_protobuf_cache_after_transient_read_only_result() {
    assert_network_hydration_data_store_behavior("statsig-br", ReadOnlyBehavior::FirstCheck).await;
}

#[tokio::test]
async fn network_hydration_skips_zstd_cache_after_transient_read_only_result() {
    assert_network_hydration_data_store_behavior("statsig-zstd", ReadOnlyBehavior::FirstCheck)
        .await;
}

#[tokio::test]
async fn network_hydration_skips_cache_when_data_store_becomes_read_only() {
    assert_network_hydration_data_store_behavior("statsig-br", ReadOnlyBehavior::AfterFirstCheck)
        .await;
}

#[tokio::test]
async fn write_once_store_publishes_one_snapshot_across_full_fallbacks() {
    for (encoding, warm_start) in [
        ("statsig-br", false),
        ("statsig-zstd", false),
        ("statsig-br", true),
    ] {
        assert_data_store_full_fallbacks(encoding, warm_start, true).await;
    }
}

#[tokio::test]
async fn default_store_publishes_each_full_fallback() {
    assert_data_store_full_fallbacks("statsig-br", false, false).await;
}

async fn assert_data_store_full_fallbacks(
    encoding: &'static str,
    warm_start: bool,
    write_once: bool,
) {
    let server = MockServer::start().await;
    let initial_value = br#"{"large":"initial"}"#;
    let initial_sha = lowercase_hex(&Sha256::digest(initial_value));
    let initial_path = format!("{DOWNLOAD_PATH_PREFIX}{initial_sha}");
    let initial_bytes =
        remote_protobuf_dcs(&server, &initial_path, &initial_sha, initial_value.len());
    mount_remote_value(&server, &initial_path, initial_value).await;
    let mut data_store = if warm_start {
        MockDataStore::with_proto_cache(&initial_bytes)
    } else {
        MockDataStore::new_with_byte_cache(false)
    };
    if write_once {
        data_store = data_store.with_write_once();
    }
    let data_store = Arc::new(data_store);
    let initial_bytes = if encoding == "statsig-zstd" {
        let mut decoded = Vec::new();
        brotli::Decompressor::new(initial_bytes.as_slice(), 4096)
            .read_to_end(&mut decoded)
            .unwrap();
        zstd::stream::encode_all(decoded.as_slice(), 3).unwrap()
    } else {
        initial_bytes
    };
    mount_protobuf_dcs_with_encoding(&server, initial_bytes, encoding).await;
    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
        specs_sync_interval_ms: Some(1000),
        enable_dcs_deltas: Some(true),
        disable_all_logging: Some(true),
        disable_country_lookup: Some(true),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(SDK_KEY, Some(Arc::new(options)));
    statsig.initialize().await.unwrap();
    let expected_writes = usize::from(!warm_start);
    assert_eventually!(|| data_store.num_set_bytes_calls() == expected_writes);
    assert_eventually!(|| if encoding == "statsig-zstd" {
        data_store.stored_zstd_proto_bytes().is_some()
    } else {
        data_store.stored_proto_bytes().is_some()
    });
    let mut published_bytes = (!warm_start).then(|| {
        (
            data_store.stored_proto_bytes(),
            data_store.stored_zstd_proto_bytes(),
        )
    });

    for (version, value) in [(2, "updated"), (3, "latest")] {
        server.reset().await;
        let updated_value = serde_json::to_vec(&json!({"large": value})).unwrap();
        let updated_sha = lowercase_hex(&Sha256::digest(&updated_value));
        let updated_path = format!("{DOWNLOAD_PATH_PREFIX}{updated_sha}");
        mount_remote_value(&server, &updated_path, &updated_value).await;
        let mut envelopes = decode_protobuf_envelopes(&remote_protobuf_dcs(
            &server,
            &updated_path,
            &updated_sha,
            updated_value.len(),
        ));
        let mut top = pb::SpecsTopLevel::decode(envelopes[0].data.as_deref().unwrap()).unwrap();
        top.time = version;
        top.checksum = format!("response-{version}");
        envelopes[0].data = Some(top.encode_to_vec());
        envelopes[1].checksum = format!("config-{version}");
        let mut decoded = Vec::new();
        for envelope in envelopes {
            envelope.encode_length_delimited(&mut decoded).unwrap();
        }
        let updated_bytes = if encoding == "statsig-zstd" {
            zstd::stream::encode_all(decoded.as_slice(), 3).unwrap()
        } else {
            let mut writer = brotli::CompressorWriter::new(Vec::new(), 4096, 1, 22);
            writer.write_all(&decoded).unwrap();
            writer.into_inner()
        };
        // No delta header: the upstream falls back to a full response.
        mount_protobuf_dcs_with_encoding(&server, updated_bytes, encoding).await;
        let user = StatsigUser::with_user_id("a-user");
        assert_eventually!(|| statsig
            .get_dynamic_config(&user, "large_config")
            .value
            .get("large")
            == Some(&json!(value)));
        let expected_writes = if write_once { 1 } else { version as usize };
        assert_eventually!(|| data_store.num_set_bytes_calls() == expected_writes);
        if let Some((brotli, zstd)) = &published_bytes {
            if write_once {
                assert_eq!(&data_store.stored_proto_bytes(), brotli);
                assert_eq!(&data_store.stored_zstd_proto_bytes(), zstd);
            }
        } else {
            assert_eventually!(|| data_store
                .stored_proto_bytes()
                .as_ref()
                .is_some_and(|bytes| {
                    let envelopes = decode_protobuf_envelopes(bytes);
                    let top =
                        pb::SpecsTopLevel::decode(envelopes[0].data.as_deref().unwrap()).unwrap();
                    top.time == version
                }));
            published_bytes = Some((
                data_store.stored_proto_bytes(),
                data_store.stored_zstd_proto_bytes(),
            ));
        }
    }
    statsig.shutdown().await.unwrap();
    assert_eq!(
        data_store.num_set_bytes_calls(),
        if write_once { 1 } else { 3 }
    );
    assert_eq!(data_store.num_set_calls(), 0);
}

#[tokio::test]
async fn write_once_store_publishes_after_failed_or_timed_out_init() {
    for timed_out in [false, true] {
        let server = MockServer::start().await;
        Mock::given(method("GET"))
            .respond_with(if timed_out {
                ResponseTemplate::new(503).set_delay(std::time::Duration::from_secs(1))
            } else {
                ResponseTemplate::new(503)
            })
            .mount(&server)
            .await;
        let data_store = Arc::new(MockDataStore::new_with_byte_cache(false).with_write_once());
        let options = StatsigOptions {
            data_store: Some(data_store.clone()),
            specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
            specs_sync_interval_ms: Some(1000),
            init_timeout_ms: timed_out.then_some(20),
            fallback_to_statsig_api: Some(false),
            disable_all_logging: Some(true),
            disable_country_lookup: Some(true),
            ..StatsigOptions::new()
        };
        let statsig = Statsig::new(SDK_KEY, Some(Arc::new(options)));
        let details = statsig.initialize_with_details().await.unwrap();
        assert!(details.failure_details.is_some());
        server.reset().await;
        let remote_value = br#"{"large":"recovered"}"#;
        let sha = lowercase_hex(&Sha256::digest(remote_value));
        let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
        mount_remote_value(&server, &download_path, remote_value).await;
        mount_protobuf_dcs(
            &server,
            remote_protobuf_dcs(&server, &download_path, &sha, remote_value.len()),
        )
        .await;
        let user = StatsigUser::with_user_id("a-user");
        assert_eventually!(|| statsig
            .get_dynamic_config(&user, "large_config")
            .value
            .get("large")
            == Some(&json!("recovered")));
        assert_eventually!(|| data_store.stored_proto_bytes().is_some());
        statsig.shutdown().await.unwrap();
        assert_eq!(data_store.num_set_bytes_calls(), 1);
        assert_eq!(data_store.num_set_calls(), 0);
        assert_offline_follower_bootstrap(&server, &data_store, "recovered").await;
    }
}

#[tokio::test]
async fn write_once_store_retries_failed_publication_without_an_upstream_change() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"retry-payload"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    let response = remote_protobuf_dcs(&server, &download_path, &sha, remote_value.len());
    mount_remote_value(&server, &download_path, remote_value).await;
    mount_protobuf_dcs(&server, response.clone()).await;
    let data_store = Arc::new(
        MockDataStore::new_with_byte_cache(false)
            .with_write_once()
            .with_set_bytes_failures(1)
            .with_blocked_set_bytes(),
    );
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            data_store: Some(data_store.clone()),
            ..(*options_for(&server)).clone()
        })),
    );
    statsig.initialize().await.unwrap();
    data_store.wait_for_set_bytes_call().await;

    // This full fallback has the same LCUT/checksum and is skipped. Publication
    // must retry independently: no subsequent upstream request is needed.
    statsig
        .get_context()
        .spec_store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes_with_headers(
                response,
                Some(HashMap::from([
                    (
                        "content-type".to_string(),
                        "application/octet-stream".to_string(),
                    ),
                    ("content-encoding".to_string(), "statsig-br".to_string()),
                ])),
            ),
            source: SpecsSource::Network,
            received_at: 2,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
    assert!(data_store.stored_proto_bytes().is_none());
    data_store.release_set_bytes_calls(1);
    data_store.wait_for_set_bytes_call().await;
    assert!(data_store.stored_proto_bytes().is_none());
    let attempts = data_store.set_bytes_payloads();
    assert_eq!(attempts.len(), 2);
    assert_eq!(
        attempts[0], attempts[1],
        "retry must reuse the prepared snapshot"
    );
    data_store.release_set_bytes_calls(1);
    await_data_store_writes(&statsig).await;
    assert!(data_store.stored_proto_bytes().is_some());
    apply_full_response(&statsig, 2);
    await_data_store_writes(&statsig).await;
    statsig.shutdown().await.unwrap();
    assert_eq!(data_store.num_set_bytes_calls(), 2);
    assert_eq!(data_store.num_set_calls(), 0);
    assert_eq!(server.received_requests().await.unwrap().len(), 2);
    assert_offline_follower_bootstrap(&server, &data_store, "retry-payload").await;
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn write_once_store_has_only_one_in_flight_publication() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"first-publication"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    mount_remote_value(&server, &download_path, remote_value).await;
    mount_protobuf_dcs(
        &server,
        remote_protobuf_dcs(&server, &download_path, &sha, remote_value.len()),
    )
    .await;
    let data_store = Arc::new(
        MockDataStore::new_with_byte_cache(false)
            .with_write_once()
            .with_blocked_set_bytes(),
    );
    let statsig = Arc::new(Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            data_store: Some(data_store.clone()),
            ..(*options_for(&server)).clone()
        })),
    ));
    statsig.initialize().await.unwrap();
    data_store.wait_for_set_bytes_call().await;
    let mut updates = Vec::new();
    for version in 2..10 {
        let statsig = statsig.clone();
        updates.push(tokio::task::spawn_blocking(move || {
            apply_full_response(&statsig, version)
        }));
    }
    for update in updates {
        update.await.unwrap();
    }
    // Let any incorrectly scheduled duplicate writes complete so shutdown and
    // the final attempt count detect them without relying on a scheduling sleep.
    data_store.release_set_bytes_calls(10);
    await_data_store_writes(&statsig).await;
    assert!(data_store.stored_proto_bytes().is_some());
    statsig.shutdown().await.unwrap();
    assert_eq!(data_store.num_set_bytes_calls(), 1);
    assert_eq!(data_store.num_set_calls(), 0);
    assert_offline_follower_bootstrap(&server, &data_store, "first-publication").await;
}

#[tokio::test]
async fn write_once_store_cancels_blocked_publication_on_shutdown() {
    let server = MockServer::start().await;
    mount_dcs(
        &server,
        json!({
            "has_updates": true,
            "time": 1,
            "experiment_to_layer": {},
            "condition_map": {},
            "feature_gates": {},
            "dynamic_configs": {},
            "layer_configs": {}
        }),
    )
    .await;
    let data_store = Arc::new(
        MockDataStore::new_with_byte_cache(false)
            .with_write_once()
            .with_blocked_set_bytes(),
    );
    let statsig = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            data_store: Some(data_store.clone()),
            ..(*options_for(&server)).clone()
        })),
    );
    statsig.initialize().await.unwrap();
    data_store.wait_for_set_bytes_call().await;
    statsig
        .shutdown_with_timeout(std::time::Duration::from_secs(1))
        .await
        .unwrap();
    assert_eq!(data_store.num_set_bytes_calls(), 1);
    assert!(data_store.stored_json_bytes().is_none());
    assert_eq!(statsig.statsig_runtime.get_num_active_tasks(), 0);
}

async fn await_data_store_writes(statsig: &Statsig) {
    tokio::time::timeout(
        std::time::Duration::from_secs(5),
        statsig
            .statsig_runtime
            .await_tasks_with_tag("spec_store_update_data_store"),
    )
    .await
    .expect("datastore publications should complete");
}

fn apply_full_response(statsig: &Statsig, version: u64) {
    let store = &statsig.get_context().spec_store;
    let mut values = store.get_current_values().unwrap();
    values.time = version;
    values.checksum = Some(format!("full-response-{version}"));
    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(serde_json::to_vec(&values).unwrap()),
            source: SpecsSource::Network,
            received_at: version,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
}

async fn assert_offline_follower_bootstrap(
    server: &MockServer,
    data_store: &MockDataStore,
    expected_value: &str,
) {
    server.verify().await;
    server.reset().await;
    Mock::given(method("GET"))
        .respond_with(ResponseTemplate::new(500))
        .expect(0)
        .mount(server)
        .await;
    let follower_store = Arc::new(
        MockDataStore::with_proto_cache(&data_store.stored_proto_bytes().unwrap())
            .with_read_only(true)
            .with_write_once(),
    );
    let follower = Statsig::new(
        SDK_KEY,
        Some(Arc::new(StatsigOptions {
            data_store: Some(follower_store.clone()),
            spec_adapters_config: Some(vec![data_store_adapter_config()]),
            ..(*options_for(server)).clone()
        })),
    );
    let details = follower.initialize_with_details().await.unwrap();
    assert!(details.init_success);
    assert_eq!(
        details.source,
        SpecsSource::Adapter("DataStore".to_string())
    );
    let config =
        follower.get_dynamic_config(&StatsigUser::with_user_id("follower"), "large_config");
    assert_eq!(config.value.get("large"), Some(&json!(expected_value)));
    follower.shutdown().await.unwrap();
    assert_eq!(follower_store.num_set_bytes_calls(), 0);
    assert_eq!(follower_store.num_set_calls(), 0);
    server.verify().await;
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum ReadOnlyBehavior {
    Never,
    Always,
    FirstCheck,
    AfterFirstCheck,
}

async fn assert_network_hydration_data_store_behavior(
    content_encoding: &'static str,
    read_only: ReadOnlyBehavior,
) {
    let server = MockServer::start().await;
    // Exercise writer buffering and decoder refills with several ordered frames,
    // including both rewritten remote values and an untouched inline value.
    let remote_json = json!({
        "large": "offline-from-data-store",
        "padding": "remote-value-".repeat(BUFFER_SIZE / 4),
    });
    let remote_value = serde_json::to_vec(&remote_json).unwrap();
    let inline_json = json!({"inline": "inline-value-".repeat(BUFFER_SIZE / 4)});
    let sha = lowercase_hex(&Sha256::digest(&remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    let data_store = Arc::new(match read_only {
        ReadOnlyBehavior::Never => MockDataStore::new_with_byte_cache(false),
        ReadOnlyBehavior::Always => MockDataStore::new_with_byte_cache(false).with_read_only(true),
        ReadOnlyBehavior::FirstCheck => {
            MockDataStore::new_with_byte_cache(false).with_read_only_once()
        }
        ReadOnlyBehavior::AfterFirstCheck => {
            MockDataStore::new_with_byte_cache(false).with_read_only_after_first_check()
        }
    });

    let mut input_envelopes = decode_protobuf_envelopes(&remote_protobuf_dcs(
        &server,
        &download_path,
        &sha,
        remote_value.len(),
    ));
    let mut inline_envelope = input_envelopes[1].clone();
    inline_envelope.name = "inline_config".to_string();
    inline_envelope.checksum = "inline-checksum".to_string();
    let mut inline_spec = pb::Spec::decode(inline_envelope.data.as_deref().unwrap()).unwrap();
    inline_spec.remote_config_metadata = None;
    inline_spec.default_value = Some(pb::ReturnValue {
        value: Some(return_value::Value::RawValue(
            serde_json::to_vec(&inline_json).unwrap(),
        )),
    });
    inline_envelope.data = Some(inline_spec.encode_to_vec());
    input_envelopes.insert(2, inline_envelope);
    let mut second_remote = input_envelopes[1].clone();
    second_remote.name = "second_remote_config".to_string();
    second_remote.checksum = "second-config-checksum".to_string();
    input_envelopes.insert(3, second_remote);

    let mut input_bytes = Vec::new();
    for envelope in &input_envelopes {
        envelope.encode_length_delimited(&mut input_bytes).unwrap();
    }
    assert!(input_bytes.len() > BUFFER_SIZE * 2);
    let compressed = match content_encoding {
        "statsig-zstd" => zstd::stream::encode_all(input_bytes.as_slice(), 3).unwrap(),
        "statsig-br" => {
            let mut writer = brotli::CompressorWriter::new(Vec::new(), 4096, 1, 22);
            writer.write_all(&input_bytes).unwrap();
            writer.into_inner()
        }
        _ => unreachable!(),
    };
    mount_remote_value(&server, &download_path, &remote_value).await;
    mount_protobuf_dcs_with_encoding(&server, compressed, content_encoding).await;

    let leader_options = StatsigOptions {
        data_store: Some(data_store.clone()),
        specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
        spec_adapters_config: Some(vec![
            data_store_adapter_config(),
            network_http_adapter_config(format!("{}/v2/download_config_specs", server.uri())),
        ]),
        disable_all_logging: Some(true),
        experimental_flags: Some(HashSet::from(["enable_dcs_zstd_datastore".to_string()])),
        ..StatsigOptions::new()
    };
    let leader = Statsig::new(SDK_KEY, Some(Arc::new(leader_options)));

    let leader_details = leader.initialize_with_details().await.unwrap();
    assert!(leader_details.init_success);
    assert_eq!(leader_details.source, SpecsSource::Network);
    for (name, expected) in [
        ("large_config", &remote_json),
        ("inline_config", &inline_json),
        ("second_remote_config", &remote_json),
    ] {
        let config = leader.get_dynamic_config(&StatsigUser::with_user_id("a-user"), name);
        assert_eq!(serde_json::to_value(&config.value).unwrap(), *expected);
    }
    assert!(data_store.num_get_bytes_calls() > 0);
    if read_only != ReadOnlyBehavior::Never {
        if read_only == ReadOnlyBehavior::FirstCheck {
            assert_eq!(
                data_store.num_read_only_calls(),
                1,
                "a later capability check must not permit writing uncaptured protobuf bytes",
            );
        } else if read_only == ReadOnlyBehavior::AfterFirstCheck {
            assert_eq!(data_store.num_read_only_calls(), 2);
        }
        leader.shutdown().await.unwrap();
        assert_eq!(data_store.num_set_bytes_calls(), 0);
        assert_eq!(data_store.num_set_calls(), 0);
        assert!(data_store.stored_proto_bytes().is_none());
        assert!(data_store.stored_zstd_proto_bytes().is_none());
        server.verify().await;
        return;
    }
    let stored_bytes = || match content_encoding {
        "statsig-zstd" => data_store.stored_zstd_proto_bytes(),
        "statsig-br" => data_store.stored_proto_bytes(),
        _ => unreachable!(),
    };
    assert_eventually!(|| stored_bytes().is_some());
    let stored_bytes = stored_bytes().expect("leader should write bytes using the response codec");
    let stored_envelopes = if content_encoding == "statsig-zstd" {
        assert!(data_store.stored_proto_bytes().is_none());
        let decompressed = zstd::stream::decode_all(stored_bytes.as_slice()).unwrap();
        decode_uncompressed_protobuf_envelopes(&decompressed)
    } else {
        assert!(data_store.stored_zstd_proto_bytes().is_none());
        decode_protobuf_envelopes(&stored_bytes)
    };
    assert_eq!(stored_envelopes.len(), input_envelopes.len());
    for (stored, input) in stored_envelopes.iter().zip(&input_envelopes) {
        assert_eq!(stored.kind, input.kind);
        assert_eq!(stored.name, input.name);
        assert_eq!(stored.checksum, input.checksum);
    }
    let stored_top_level = stored_envelopes
        .iter()
        .find(|envelope| {
            pb::SpecsEnvelopeKind::try_from(envelope.kind).ok()
                == Some(pb::SpecsEnvelopeKind::TopLevel)
        })
        .and_then(|envelope| envelope.data.as_deref())
        .map(pb::SpecsTopLevel::decode)
        .unwrap()
        .unwrap();
    assert_eq!(
        stored_top_level.may_have_remote_config_metadata,
        Some(false)
    );
    let mut expected_top_level =
        pb::SpecsTopLevel::decode(input_envelopes[0].data.as_deref().unwrap()).unwrap();
    expected_top_level.may_have_remote_config_metadata = Some(false);
    assert_eq!(stored_top_level, expected_top_level);
    assert_eq!(stored_envelopes[2], input_envelopes[2]);
    assert_eq!(stored_envelopes[4], input_envelopes[4]);
    for index in [1, 3] {
        let stored_spec =
            pb::Spec::decode(stored_envelopes[index].data.as_deref().unwrap()).unwrap();
        let mut expected_spec =
            pb::Spec::decode(input_envelopes[index].data.as_deref().unwrap()).unwrap();
        expected_spec.remote_config_metadata = None;
        expected_spec.default_value = Some(pb::ReturnValue {
            value: Some(return_value::Value::RawValue(remote_value.clone())),
        });
        assert_eq!(stored_spec, expected_spec);
    }
    leader.shutdown().await.unwrap();

    server.verify().await;
    server.reset().await;
    Mock::given(method("GET"))
        .respond_with(ResponseTemplate::new(500))
        .expect(0)
        .mount(&server)
        .await;

    for _ in 0..2 {
        let follower_options = StatsigOptions {
            data_store: Some(data_store.clone()),
            specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
            spec_adapters_config: Some(vec![data_store_adapter_config()]),
            disable_all_logging: Some(true),
            experimental_flags: Some(HashSet::from(["enable_dcs_zstd_datastore".to_string()])),
            ..StatsigOptions::new()
        };
        let follower = Statsig::new(SDK_KEY, Some(Arc::new(follower_options)));

        let follower_details = follower.initialize_with_details().await.unwrap();
        assert!(follower_details.init_success);
        assert_eq!(
            follower_details.source,
            SpecsSource::Adapter("DataStore".to_string())
        );
        for (name, expected) in [
            ("large_config", &remote_json),
            ("inline_config", &inline_json),
            ("second_remote_config", &remote_json),
        ] {
            let config = follower.get_dynamic_config(&StatsigUser::with_user_id("a-user"), name);
            assert_eq!(serde_json::to_value(&config.value).unwrap(), *expected);
        }

        follower.shutdown().await.unwrap();
    }

    server.verify().await;
}

#[tokio::test]
async fn data_store_hydration_uses_configured_http_adapter_source() {
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"from-custom-sfp-data-store"}"#;
    let sha = lowercase_hex(&Sha256::digest(remote_value));
    let download_path = format!("{DOWNLOAD_PATH_PREFIX}{sha}");
    let cached_dcs = remote_dcs(&server, &download_path, &sha, remote_value.len()).to_string();
    let data_store = Arc::new(MockDataStore::with_json_cache(&cached_dcs));

    mount_remote_value(&server, &download_path, remote_value).await;

    let options = StatsigOptions {
        data_store: Some(data_store),
        spec_adapters_config: Some(vec![
            data_store_adapter_config(),
            network_http_adapter_config(format!("{}/v2/download_config_specs", server.uri())),
        ]),
        disable_all_logging: Some(true),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(SDK_KEY, Some(Arc::new(options)));

    let details = statsig.initialize_with_details().await.unwrap();

    assert!(details.init_success);
    assert_eq!(
        details.source,
        SpecsSource::Adapter("DataStore".to_string())
    );
    let config = statsig.get_dynamic_config(&StatsigUser::with_user_id("a-user"), "large_config");
    assert_eq!(
        config.value.get("large"),
        Some(&json!("from-custom-sfp-data-store"))
    );

    statsig.shutdown().await.unwrap();
}

fn options_for(server: &MockServer) -> Arc<StatsigOptions> {
    Arc::new(StatsigOptions {
        specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
        disable_all_logging: Some(true),
        ..StatsigOptions::new()
    })
}

fn data_store_adapter_config() -> SpecAdapterConfig {
    SpecAdapterConfig {
        adapter_type: SpecsAdapterType::DataStore,
        init_timeout_ms: 3_000,
        specs_url: None,
        authentication_mode: None,
        ca_cert_path: None,
        client_cert_path: None,
        client_key_path: None,
        domain_name: None,
    }
}

fn network_http_adapter_config(specs_url: String) -> SpecAdapterConfig {
    SpecAdapterConfig {
        adapter_type: SpecsAdapterType::NetworkHttp,
        init_timeout_ms: 3_000,
        specs_url: Some(specs_url),
        authentication_mode: None,
        ca_cert_path: None,
        client_cert_path: None,
        client_key_path: None,
        domain_name: None,
    }
}

fn remote_dcs(
    server: &MockServer,
    download_path: &str,
    sha: &str,
    byte_length: usize,
) -> serde_json::Value {
    remote_dcs_with_placeholder(
        &format!("{}{download_path}", server.uri()),
        sha,
        byte_length,
    )
}

fn remote_dcs_with_placeholder(
    placeholder: &str,
    sha: &str,
    byte_length: usize,
) -> serde_json::Value {
    json!({
        "dynamic_configs": {
            "large_config": {
                "type": "dynamic_config",
                "salt": "salt",
                "enabled": true,
                "defaultValue": {"value": placeholder},
                "remoteConfigMetadata": {
                    "sha256": sha,
                    "byteLength": byte_length,
                    "contentType": "application/json",
                    "compression": "none"
                },
                "rules": [],
                "idType": "userID",
                "entity": "dynamic_config",
                "version": 1
            }
        },
        "feature_gates": {},
        "experiment_to_layer": {},
        "layer_configs": {},
        "has_updates": true,
        "time": 1,
        "company_id": "company",
        "condition_map": {},
        "response_format": "dcs-v2"
    })
}

async fn mount_dcs(server: &MockServer, dcs: serde_json::Value) {
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .and(header("statsig-api-key", SDK_KEY))
        .respond_with(ResponseTemplate::new(200).set_body_json(dcs))
        .mount(server)
        .await;
}

async fn mount_protobuf_dcs(server: &MockServer, dcs: Vec<u8>) {
    mount_protobuf_dcs_with_encoding(server, dcs, "statsig-br").await;
}

async fn mount_protobuf_dcs_with_encoding(
    server: &MockServer,
    dcs: Vec<u8>,
    content_encoding: &'static str,
) {
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .and(header("statsig-api-key", SDK_KEY))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/octet-stream")
                .insert_header("content-encoding", content_encoding)
                .set_body_bytes(dcs),
        )
        .mount(server)
        .await;
}

fn remote_protobuf_dcs(
    server: &MockServer,
    download_path: &str,
    sha: &str,
    byte_length: usize,
) -> Vec<u8> {
    remote_protobuf_dcs_with_compression(server, download_path, sha, byte_length, "none")
}

fn remote_protobuf_dcs_with_compression(
    server: &MockServer,
    download_path: &str,
    sha: &str,
    byte_length: usize,
    compression: &str,
) -> Vec<u8> {
    let placeholder = serde_json::to_vec(&format!("{}{download_path}", server.uri())).unwrap();
    let metadata = pb::RemoteConfigValueMetadata {
        sha256: sha.to_string(),
        byte_length: byte_length as u64,
        content_type: "application/json".to_string(),
        compression: compression.to_string(),
    };
    let top_level = pb::SpecsTopLevel {
        has_updates: true,
        time: 1,
        company_id: "company".to_string(),
        response_format: "dcs-v2".to_string(),
        checksum: "response-checksum".to_string(),
        rest: br#"{"experiment_to_layer":{},"condition_map":{}}"#.to_vec(),
        may_have_remote_config_metadata: Some(true),
    };
    let spec = pb::Spec {
        salt: "salt".to_string(),
        enabled: true,
        entity: pb::EntityType::EntityDynamicConfig as i32,
        default_value: Some(pb::ReturnValue {
            value: Some(return_value::Value::RawValue(placeholder)),
        }),
        remote_config_metadata: Some(metadata),
        ..Default::default()
    };
    let envelopes = [
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(top_level.encode_to_vec()),
            ..Default::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::DynamicConfig as i32,
            name: "large_config".to_string(),
            checksum: "config-checksum".to_string(),
            data: Some(spec.encode_to_vec()),
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Done as i32,
            ..Default::default()
        },
    ];
    let mut uncompressed = Vec::new();
    for envelope in envelopes {
        envelope.encode_length_delimited(&mut uncompressed).unwrap();
    }

    let mut compressed = Vec::new();
    {
        let mut writer = brotli::CompressorWriter::with_params(
            &mut compressed,
            4096,
            &BrotliEncoderParams::default(),
        );
        writer.write_all(&uncompressed).unwrap();
        writer.flush().unwrap();
    }
    compressed
}

fn decode_protobuf_envelopes(bytes: &[u8]) -> Vec<pb::SpecsEnvelope> {
    let mut decompressed = Vec::new();
    brotli::Decompressor::new(std::io::Cursor::new(bytes), 4096)
        .read_to_end(&mut decompressed)
        .unwrap();

    decode_uncompressed_protobuf_envelopes(&decompressed)
}

fn decode_uncompressed_protobuf_envelopes(mut remaining: &[u8]) -> Vec<pb::SpecsEnvelope> {
    let mut envelopes = Vec::new();
    while !remaining.is_empty() {
        envelopes.push(pb::SpecsEnvelope::decode_length_delimited(&mut remaining).unwrap());
    }
    envelopes
}

async fn mount_remote_value(server: &MockServer, download_path: &str, body: &[u8]) {
    Mock::given(method("GET"))
        .and(path(download_path.to_string()))
        .and(header("statsig-api-key", SDK_KEY))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(body.to_vec()),
        )
        .expect(1)
        .mount(server)
        .await;
}

async fn mount_gzip_remote_value(server: &MockServer, download_path: &str, body: &[u8]) {
    let mut encoder = GzEncoder::new(Vec::new(), Compression::default());
    encoder.write_all(body).unwrap();
    let compressed = encoder.finish().unwrap();

    Mock::given(method("GET"))
        .and(path(download_path.to_string()))
        .and(header("statsig-api-key", SDK_KEY))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .insert_header("content-encoding", "gzip")
                .set_body_bytes(compressed),
        )
        .expect(1)
        .mount(server)
        .await;
}

async fn mount_zstd_remote_value(server: &MockServer, download_path: &str, body: &[u8]) {
    let compressed = zstd::stream::encode_all(body, 3).unwrap();

    Mock::given(method("GET"))
        .and(path(download_path.to_string()))
        .and(header("statsig-api-key", SDK_KEY))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .insert_header("content-encoding", "zstd")
                .set_body_bytes(compressed),
        )
        .expect(1)
        .mount(server)
        .await;
}

fn lowercase_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let mut result = String::with_capacity(bytes.len() * 2);
    for byte in bytes {
        result.push(HEX[(byte >> 4) as usize] as char);
        result.push(HEX[(byte & 0x0f) as usize] as char);
    }
    result
}
