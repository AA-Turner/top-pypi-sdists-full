use std::sync::Arc;

use serde_json::json;
use sha2::{Digest, Sha256};
use statsig_rust::{
    Statsig, StatsigOptions, StatsigUser, interned_string::InternedString,
    interned_values::InternedStore, specs_response::spec_types::SpecsResponseFull,
};
use wiremock::matchers::{header, method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

#[tokio::test]
async fn raw_preload_keeps_ordinary_specs_and_sdk_hydrates_remote_config() {
    let sdk_key = "secret-remote-config-preload";
    let server = MockServer::start().await;
    let remote_value = br#"{"large":"hydrated after preload"}"#;
    let sha = format!("{:x}", Sha256::digest(remote_value));
    let blob_path = format!("/v1/dynamic_config_value/{sha}");
    let dcs = json!({
        "dynamic_configs": {
            "local_config": {
                "type": "dynamic_config",
                "salt": "salt",
                "enabled": true,
                "defaultValue": {"small": "shared"},
                "rules": [],
                "idType": "userID",
                "entity": "dynamic_config",
                "checksum": "local-checksum",
                "version": 1
            },
            "large_config": {
                "type": "dynamic_config",
                "salt": "salt",
                "enabled": true,
                "defaultValue": {"value": format!("{}{blob_path}", server.uri())},
                "remoteConfigMetadata": {
                    "sha256": sha,
                    "byteLength": remote_value.len(),
                    "contentType": "application/json",
                    "compression": "none"
                },
                "rules": [],
                "idType": "userID",
                "entity": "dynamic_config",
                "checksum": "remote-checksum",
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
    });

    // The preloader receives the original bytes, before the SDK's network
    // adapter has had a chance to download and hydrate the remote value.
    let raw_dcs = serde_json::to_vec(&dcs).unwrap();
    InternedStore::preload(&raw_dcs).unwrap();
    assert!(
        InternedStore::try_get_preloaded_dynamic_config(&InternedString::from_str_ref(
            "local_config"
        ))
        .is_some()
    );
    assert!(
        InternedStore::try_get_preloaded_dynamic_config(&InternedString::from_str_ref(
            "large_config"
        ))
        .is_none()
    );
    assert!(
        serde_json::from_slice::<SpecsResponseFull>(&raw_dcs)
            .unwrap_err()
            .to_string()
            .contains("before hydration")
    );

    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .and(header("statsig-api-key", sdk_key))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(raw_dcs),
        )
        .expect(1)
        .mount(&server)
        .await;
    Mock::given(method("GET"))
        .and(path(blob_path))
        .and(header("statsig-api-key", sdk_key))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_bytes(remote_value.to_vec()),
        )
        .expect(1)
        .mount(&server)
        .await;

    let options = StatsigOptions {
        specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
        disable_all_logging: Some(true),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(sdk_key, Some(Arc::new(options)));
    statsig.initialize().await.unwrap();

    let user = StatsigUser::with_user_id("a-user");
    assert_eq!(
        statsig
            .get_dynamic_config(&user, "local_config")
            .value
            .get("small"),
        Some(&json!("shared"))
    );
    assert_eq!(
        statsig
            .get_dynamic_config(&user, "large_config")
            .value
            .get("large"),
        Some(&json!("hydrated after preload"))
    );

    statsig.shutdown().await.unwrap();
    server.verify().await;
}
