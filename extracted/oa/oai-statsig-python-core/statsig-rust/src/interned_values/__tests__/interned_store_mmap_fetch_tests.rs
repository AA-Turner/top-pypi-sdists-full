use crate::{
    interned_values::{interned_store::mmap_path_for_sdk_key, InternedStore},
    statsig_metadata::SDK_VERSION,
};
use wiremock::{
    matchers::{method, path},
    Mock, MockServer, ResponseTemplate,
};

const MMAP_FETCH_SDK_KEY: &str = "interned-store-fetch-mmap";
const EVAL_PROJ_JSON: &str = include_str!("../../../tests/data/eval_proj_dcs.json");

#[tokio::test]
async fn fetch_and_write_mmap_uses_sdk_key_path() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_FETCH_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_string(EVAL_PROJ_JSON),
        )
        .mount(&server)
        .await;

    InternedStore::fetch_and_write_mmap_with_specs_url(
        MMAP_FETCH_SDK_KEY,
        &format!("{}/v2/download_config_specs", server.uri()),
    )
    .await
    .unwrap();

    let path = mmap_path_for_sdk_key(MMAP_FETCH_SDK_KEY);
    assert!(path.exists());
    assert!(path
        .file_name()
        .and_then(|name| name.to_str())
        .is_some_and(|name| name.contains(SDK_VERSION)));
}
