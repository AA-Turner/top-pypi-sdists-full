use crate::{
    evaluation::rkyv_value::ArchivedRkyvValue,
    hashing,
    interned_values::{
        interned_store::{mmap_path_for_sdk_key, ArchivedMmapDataV1, MmapDataV1},
        InternedStore,
    },
    StatsigErr,
};
use memmap2::Mmap;
use std::{fs, fs::File};
use wiremock::{
    matchers::{method, path},
    Mock, MockServer, ResponseTemplate,
};

const MMAP_FETCH_SDK_KEY: &str = "interned-store-fetch-mmap";
const OTHER_MMAP_FETCH_SDK_KEY: &str = "interned-store-fetch-mmap-other";
const EVAL_PROJ_JSON: &str = include_str!("../../../tests/data/eval_proj_dcs.json");
const V1_COMPATIBILITY_FIXTURE: &[u8] = include_bytes!("fixtures/interned_store_v1.mmap");

#[test]
fn v1_compatibility_fixture_remains_readable() {
    let mut fixture = rkyv::util::AlignedVec::<8>::new();
    fixture.extend_from_slice(V1_COMPATIBILITY_FIXTURE);
    let archived = rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&fixture).unwrap();

    assert_eq!(archived.format_version(), MmapDataV1::FORMAT_VERSION);
    assert_eq!(archived.string_for_test(7), Some("v1-string"));
    assert!(matches!(
        archived.returnable_for_test(11, "enabled"),
        Some(ArchivedRkyvValue::Bool(true))
    ));
}

#[tokio::test]
async fn fetch_and_write_mmap_uses_authoritative_sdk_key_path() {
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
    let expected_filename = format!(
        "{}_v1_interned_store.mmap",
        hashing::djb2(MMAP_FETCH_SDK_KEY)
    );
    assert!(path.exists());
    assert_eq!(
        path.file_name().and_then(|name| name.to_str()),
        Some(expected_filename.as_str())
    );

    let file = File::open(path).unwrap();
    let mmap = unsafe { Mmap::map(&file).unwrap() };
    let archived = rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&mmap).unwrap();
    assert_eq!(archived.format_version(), MmapDataV1::FORMAT_VERSION);
}

#[test]
fn mmap_paths_are_scoped_by_sdk_key() {
    assert_ne!(
        mmap_path_for_sdk_key(MMAP_FETCH_SDK_KEY),
        mmap_path_for_sdk_key(OTHER_MMAP_FETCH_SDK_KEY)
    );
}

#[test]
fn preload_mmap_rejects_malformed_archive() {
    let sdk_key = "interned-store-malformed-mmap";
    let path = mmap_path_for_sdk_key(sdk_key);
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, b"not an rkyv archive").unwrap();

    assert!(matches!(
        InternedStore::preload_mmap(sdk_key),
        Err(StatsigErr::SerializationError(_))
    ));
}

#[test]
fn preload_mmap_rejects_unsupported_format_version() {
    let sdk_key = "interned-store-unsupported-version-mmap";
    let path = mmap_path_for_sdk_key(sdk_key);
    fs::create_dir_all(path.parent().unwrap()).unwrap();

    let mmap_data = MmapDataV1::empty_with_format_version(2);
    let archived = rkyv::to_bytes::<rkyv::rancor::Error>(&mmap_data).unwrap();
    fs::write(&path, archived).unwrap();

    assert!(matches!(
        InternedStore::preload_mmap(sdk_key),
        Err(StatsigErr::SerializationError(message))
            if message == "Unsupported interned mmap format version 2; expected 1"
    ));
}
