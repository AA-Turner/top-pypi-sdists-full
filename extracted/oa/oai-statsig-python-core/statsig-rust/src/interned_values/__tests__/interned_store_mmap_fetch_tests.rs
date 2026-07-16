#[cfg(any(unix, windows))]
use crate::interned_values::interned_store::open_committed_mmap_v2_for_test;
use crate::{
    evaluation::rkyv_value::{ArchivedRkyvNumber, ArchivedRkyvValue},
    hashing,
    interned_values::{
        interned_store::{
            acquire_mmap_write_lock_for_test, mmap_lock_path_for_sdk_key,
            mmap_manifest_path_for_sdk_key, mmap_path_for_sdk_key, mmap_v2_path_for_sdk_key,
            validate_mmap_v2_for_test, write_mmap_manifest_for_test, write_mmap_v2_for_test,
            write_mmap_v2_only_manifest_for_test, ArchivedMmapDataV1, MmapDataV1,
        },
        mmap_data_v2::{ArchivedMmapDataV2, MmapDataV2},
        InternedStore, MmapSyncCursor, MmapWriteOutcome,
    },
    specs_response::spec_types::SpecsResponseFull,
    StatsigErr,
};
use memmap2::Mmap;
use rusty_fork::rusty_fork_test;
#[cfg(unix)]
use std::os::unix::fs::{MetadataExt, PermissionsExt};
#[cfg(target_os = "linux")]
use std::os::unix::process::CommandExt;
use std::{
    collections::HashMap,
    fs,
    fs::File,
    io::Read,
    sync::{
        atomic::{AtomicUsize, Ordering},
        Arc,
    },
    time::Duration,
};
use wiremock::{
    matchers::{method, path},
    Mock, MockServer, Request, ResponseTemplate,
};

const MMAP_FETCH_SDK_KEY: &str = "interned-store-fetch-mmap";
const MMAP_REPLACE_SDK_KEY: &str = "interned-store-replace-mmap";
#[cfg(target_os = "linux")]
const MMAP_CROSS_UID_SDK_KEY: &str = "interned-store-cross-uid-mmap";
#[cfg(target_os = "linux")]
const CROSS_UID_TEST_NAME: &str = "interned_values::__tests__::interned_store_mmap_fetch_tests::uid_10001_can_preload_artifact_written_by_uid_1000";
const OTHER_MMAP_FETCH_SDK_KEY: &str = "interned-store-fetch-mmap-other";
const MMAP_NUMERIC_SDK_KEY: &str = "interned-store-numeric-mmap";
const MMAP_PROTO_NUMERIC_SDK_KEY: &str = "interned-store-proto-numeric-mmap";
const MMAP_PROTO_GENERATION_SDK_KEY: &str = "interned-store-conditional-proto-mmap";
const MMAP_NO_UPDATE_SDK_KEY: &str = "interned-store-conditional-no-update-mmap";
const MMAP_GENERATION_SDK_KEY: &str = "interned-store-conditional-generation-mmap";
const MMAP_STALE_SDK_KEY: &str = "interned-store-conditional-stale-mmap";
const MMAP_NO_CHECKSUM_SDK_KEY: &str = "interned-store-conditional-no-checksum-mmap";
const MMAP_SAME_LCUT_REPAIR_SDK_KEY: &str = "interned-store-same-lcut-repair-mmap";
const MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY: &str = "interned-store-empty-checksum-conflict";
const MMAP_V2_PUBLIC_SDK_KEY: &str = "interned-store-v2-public-mmap";
const MMAP_CONCURRENT_A_SDK_KEY: &str = "interned-store-concurrent-a";
const MMAP_CONCURRENT_B_SDK_KEY: &str = "interned-store-concurrent-b";
const MMAP_CONCURRENT_SAME_KEY: &str = "interned-store-concurrent-same-key";
const EVAL_PROJ_JSON: &str = include_str!("../../../tests/data/eval_proj_dcs.json");
const EVAL_PROJ_PROTO: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.pb.br");
const BIG_NUMBER_JSON: &str = include_str!("../../../tests/data/big_number_dcs.json");
const V1_COMPATIBILITY_FIXTURE: &[u8] = include_bytes!("fixtures/interned_store_v1.mmap");

fn config_json_with_cursor(lcut: u64, checksum: Option<&str>) -> String {
    let mut config = serde_json::from_str::<serde_json::Value>(EVAL_PROJ_JSON).unwrap();
    config["time"] = serde_json::json!(lcut);
    config["checksum"] = checksum.map_or(serde_json::Value::Null, |checksum| {
        serde_json::Value::String(checksum.to_string())
    });
    serde_json::to_string(&config).unwrap()
}

fn config_json_with_marker(lcut: u64, checksum: &str, marker: &str) -> String {
    let mut config =
        serde_json::from_str::<serde_json::Value>(&config_json_with_cursor(lcut, Some(checksum)))
            .unwrap();
    let marker_spec = config["feature_gates"]["segment:best_engineers"].clone();
    config["feature_gates"][marker] = marker_spec;
    serde_json::to_string(&config).unwrap()
}

fn config_response(body: String, lcut: u64, checksum: Option<&str>) -> ResponseTemplate {
    let mut response = ResponseTemplate::new(200)
        .insert_header("content-type", "application/json")
        .insert_header("x-since-time", lcut.to_string())
        .set_body_string(body);
    if let Some(checksum) = checksum {
        response = response.insert_header("x-checksum", checksum);
    }
    response
}

fn query_params(request: &Request) -> HashMap<String, String> {
    request
        .url
        .query_pairs()
        .map(|(key, value)| (key.into_owned(), value.into_owned()))
        .collect()
}

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
    let v2_path = mmap_v2_path_for_sdk_key(MMAP_FETCH_SDK_KEY);
    let manifest_path = mmap_manifest_path_for_sdk_key(MMAP_FETCH_SDK_KEY);
    let expected_filename = format!(
        "{}_v1_interned_store.mmap",
        hashing::djb2(MMAP_FETCH_SDK_KEY)
    );
    let expected_v2_filename = format!(
        "{}_v2_interned_store.mmap",
        hashing::djb2(MMAP_FETCH_SDK_KEY)
    );
    assert!(path.exists());
    assert_eq!(
        path.file_name().and_then(|name| name.to_str()),
        Some(expected_filename.as_str())
    );
    assert_eq!(
        v2_path.file_name().and_then(|name| name.to_str()),
        Some(expected_v2_filename.as_str())
    );

    let file = File::open(&path).unwrap();
    let mmap = unsafe { Mmap::map(&file).unwrap() };
    let archived = rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&mmap).unwrap();
    assert_eq!(archived.format_version(), MmapDataV1::FORMAT_VERSION);
    let v2_file = File::open(&v2_path).unwrap();
    let v2_mmap = unsafe { Mmap::map(&v2_file).unwrap() };
    let v2_archived = rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&v2_mmap).unwrap();
    assert_eq!(
        v2_archived.format_version.to_native(),
        MmapDataV2::FORMAT_VERSION
    );

    #[cfg(unix)]
    assert_eq!(
        fs::metadata(&path).unwrap().permissions().mode() & 0o777,
        0o644
    );
    #[cfg(unix)]
    assert_eq!(
        fs::metadata(&v2_path).unwrap().permissions().mode() & 0o777,
        0o644
    );
    assert!(manifest_path.exists());
    #[cfg(unix)]
    assert_eq!(
        fs::metadata(&manifest_path).unwrap().permissions().mode() & 0o777,
        0o644
    );
}

#[tokio::test]
async fn conditional_fetch_sends_cursor_and_preserves_artifact_on_no_update() {
    let server = MockServer::start().await;
    let initial_body = config_json_with_cursor(100, Some("checksum100"));
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_NO_UPDATE_SDK_KEY}.json"
        )))
        .respond_with(move |request: &Request| {
            if query_params(request).contains_key("sinceTime") {
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .insert_header("x-cache-hit", "true")
                    .insert_header("x-since-time", "100")
                    .set_body_string(r#"{"has_updates":false}"#)
            } else {
                config_response(initial_body.clone(), 100, Some("checksum100"))
            }
        })
        .mount(&server)
        .await;

    let specs_url = format!("{}/v2/download_config_specs", server.uri());
    let first = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_NO_UPDATE_SDK_KEY,
        &specs_url,
        None,
    )
    .await
    .unwrap();
    let cursor = MmapSyncCursor {
        lcut: 100,
        checksum: Some("checksum100".to_string()),
    };
    assert_eq!(first, MmapWriteOutcome::Published(cursor.clone()));

    let artifact_path = mmap_path_for_sdk_key(MMAP_NO_UPDATE_SDK_KEY);
    let before_bytes = fs::read(&artifact_path).unwrap();
    let before_metadata = fs::metadata(&artifact_path).unwrap();

    let second = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_NO_UPDATE_SDK_KEY,
        &specs_url,
        Some(&cursor),
    )
    .await
    .unwrap();
    assert_eq!(second, MmapWriteOutcome::NoUpdate);

    let after_metadata = fs::metadata(&artifact_path).unwrap();
    assert_eq!(fs::read(&artifact_path).unwrap(), before_bytes);
    assert_eq!(after_metadata.len(), before_metadata.len());
    assert_eq!(
        after_metadata.modified().unwrap(),
        before_metadata.modified().unwrap()
    );
    #[cfg(unix)]
    assert_eq!(after_metadata.ino(), before_metadata.ino());

    let requests = server.received_requests().await.unwrap();
    assert_eq!(requests.len(), 2);
    let first_query = query_params(&requests[0]);
    assert!(!first_query.contains_key("sinceTime"));
    assert!(!first_query.contains_key("checksum"));
    let second_query = query_params(&requests[1]);
    assert_eq!(
        second_query.get("sinceTime").map(String::as_str),
        Some("100")
    );
    assert_eq!(
        second_query.get("checksum").map(String::as_str),
        Some("checksum100")
    );
}

#[tokio::test]
async fn conditional_fetch_publishes_higher_lcut_and_same_lcut_checksum_repair() {
    let server = MockServer::start().await;
    let initial_body = config_json_with_cursor(100, Some("checksum100"));
    let higher_body = config_json_with_cursor(101, Some("checksum101"));
    let repair_body = config_json_with_cursor(101, Some("checksum102"));
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_GENERATION_SDK_KEY}.json"
        )))
        .respond_with(move |request: &Request| {
            let query = query_params(request);
            match query.get("checksum").map(String::as_str) {
                None => config_response(initial_body.clone(), 100, Some("checksum100")),
                Some("checksum100") => {
                    config_response(higher_body.clone(), 101, Some("checksum101"))
                }
                Some("checksum101") => {
                    config_response(repair_body.clone(), 101, Some("checksum102"))
                }
                checksum => panic!("unexpected checksum query {checksum:?}"),
            }
        })
        .mount(&server)
        .await;

    let specs_url = format!("{}/v2/download_config_specs", server.uri());
    let first = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_GENERATION_SDK_KEY,
        &specs_url,
        None,
    )
    .await
    .unwrap();
    let MmapWriteOutcome::Published(first_cursor) = first else {
        panic!("first fetch did not publish");
    };
    let artifact_path = mmap_path_for_sdk_key(MMAP_GENERATION_SDK_KEY);
    #[cfg(unix)]
    let first_inode = fs::metadata(&artifact_path).unwrap().ino();

    let second = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_GENERATION_SDK_KEY,
        &specs_url,
        Some(&first_cursor),
    )
    .await
    .unwrap();
    let second_cursor = MmapSyncCursor {
        lcut: 101,
        checksum: Some("checksum101".to_string()),
    };
    assert_eq!(second, MmapWriteOutcome::Published(second_cursor.clone()));
    #[cfg(unix)]
    let second_inode = fs::metadata(&artifact_path).unwrap().ino();
    #[cfg(unix)]
    assert_ne!(second_inode, first_inode);

    let third = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_GENERATION_SDK_KEY,
        &specs_url,
        Some(&second_cursor),
    )
    .await
    .unwrap();
    assert_eq!(
        third,
        MmapWriteOutcome::Published(MmapSyncCursor {
            lcut: 101,
            checksum: Some("checksum102".to_string()),
        })
    );
    #[cfg(unix)]
    assert_ne!(fs::metadata(&artifact_path).unwrap().ino(), second_inode);
}

#[tokio::test]
async fn conditional_fetch_ignores_stale_response_and_rejects_malformed_identity() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_STALE_SDK_KEY}.json"
        )))
        .respond_with(config_response(
            config_json_with_cursor(100, Some("checksum100")),
            100,
            Some("checksum100"),
        ))
        .mount(&server)
        .await;
    let specs_url = format!("{}/v2/download_config_specs", server.uri());
    let first = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_STALE_SDK_KEY,
        &specs_url,
        None,
    )
    .await
    .unwrap();
    let MmapWriteOutcome::Published(cursor) = first else {
        panic!("first fetch did not publish");
    };
    let artifact_path = mmap_path_for_sdk_key(MMAP_STALE_SDK_KEY);
    let before_bytes = fs::read(&artifact_path).unwrap();
    #[cfg(unix)]
    let before_inode = fs::metadata(&artifact_path).unwrap().ino();

    server.reset().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_STALE_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .insert_header("x-since-time", "99")
                .insert_header("x-checksum", "stalechecksum")
                .set_body_string("this stale body must not be parsed"),
        )
        .mount(&server)
        .await;
    let stale = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_STALE_SDK_KEY,
        &specs_url,
        Some(&cursor),
    )
    .await
    .unwrap();
    assert_eq!(stale, MmapWriteOutcome::NoUpdate);
    assert_eq!(fs::read(&artifact_path).unwrap(), before_bytes);

    server.reset().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_STALE_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_string(r#"{"has_updates":false}"#),
        )
        .mount(&server)
        .await;
    let explicit_no_update = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_STALE_SDK_KEY,
        &specs_url,
        Some(&cursor),
    )
    .await
    .unwrap();
    assert_eq!(explicit_no_update, MmapWriteOutcome::NoUpdate);
    assert_eq!(fs::read(&artifact_path).unwrap(), before_bytes);

    server.reset().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_STALE_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .insert_header("x-checksum", "checksum101")
                .set_body_string(r#"{"has_updates":false}"#),
        )
        .mount(&server)
        .await;
    let malformed = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_STALE_SDK_KEY,
        &specs_url,
        Some(&cursor),
    )
    .await;
    assert!(matches!(malformed, Err(StatsigErr::InvalidOperation(_))));
    assert_eq!(fs::read(&artifact_path).unwrap(), before_bytes);
    #[cfg(unix)]
    assert_eq!(fs::metadata(&artifact_path).unwrap().ino(), before_inode);
}

#[tokio::test]
async fn conditional_fetch_supports_an_empty_optional_checksum() {
    let server = MockServer::start().await;
    let initial_body = config_json_with_cursor(200, None);
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_NO_CHECKSUM_SDK_KEY}.json"
        )))
        .respond_with(move |request: &Request| {
            if query_params(request).contains_key("sinceTime") {
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .insert_header("x-since-time", "200")
                    .insert_header("x-checksum", "")
                    .set_body_string("an exact response must not be parsed")
            } else {
                config_response(initial_body.clone(), 200, Some(""))
            }
        })
        .mount(&server)
        .await;

    let specs_url = format!("{}/v2/download_config_specs", server.uri());
    let first = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_NO_CHECKSUM_SDK_KEY,
        &specs_url,
        None,
    )
    .await
    .unwrap();
    let cursor = MmapSyncCursor {
        lcut: 200,
        checksum: None,
    };
    assert_eq!(first, MmapWriteOutcome::Published(cursor.clone()));

    let second = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_NO_CHECKSUM_SDK_KEY,
        &specs_url,
        Some(&cursor),
    )
    .await
    .unwrap();
    assert_eq!(second, MmapWriteOutcome::NoUpdate);

    let requests = server.received_requests().await.unwrap();
    assert_eq!(requests.len(), 2);
    let second_query = query_params(&requests[1]);
    assert_eq!(
        second_query.get("sinceTime").map(String::as_str),
        Some("200")
    );
    assert!(!second_query.contains_key("checksum"));
}

#[tokio::test]
async fn conditional_fetch_publishes_same_lcut_checksum_without_header() {
    let server = MockServer::start().await;
    let initial_body = config_json_with_cursor(300, None);
    let repaired_body = config_json_with_cursor(300, Some("repairchecksum"));
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_SAME_LCUT_REPAIR_SDK_KEY}.json"
        )))
        .respond_with(move |request: &Request| {
            if query_params(request).contains_key("sinceTime") {
                config_response(repaired_body.clone(), 300, None)
            } else {
                config_response(initial_body.clone(), 300, None)
            }
        })
        .mount(&server)
        .await;

    let specs_url = format!("{}/v2/download_config_specs", server.uri());
    let first = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_SAME_LCUT_REPAIR_SDK_KEY,
        &specs_url,
        None,
    )
    .await
    .unwrap();
    let initial_cursor = MmapSyncCursor {
        lcut: 300,
        checksum: None,
    };
    assert_eq!(first, MmapWriteOutcome::Published(initial_cursor.clone()));

    let artifact_path = mmap_path_for_sdk_key(MMAP_SAME_LCUT_REPAIR_SDK_KEY);
    #[cfg(unix)]
    let initial_inode = fs::metadata(&artifact_path).unwrap().ino();

    let second = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_SAME_LCUT_REPAIR_SDK_KEY,
        &specs_url,
        Some(&initial_cursor),
    )
    .await
    .unwrap();
    let repaired_cursor = MmapSyncCursor {
        lcut: 300,
        checksum: Some("repairchecksum".to_string()),
    };
    assert_eq!(second, MmapWriteOutcome::Published(repaired_cursor.clone()));
    #[cfg(unix)]
    let repaired_inode = fs::metadata(&artifact_path).unwrap().ino();
    #[cfg(unix)]
    assert_ne!(repaired_inode, initial_inode);

    let third = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_SAME_LCUT_REPAIR_SDK_KEY,
        &specs_url,
        Some(&repaired_cursor),
    )
    .await
    .unwrap();
    assert_eq!(third, MmapWriteOutcome::NoUpdate);
    #[cfg(unix)]
    assert_eq!(fs::metadata(&artifact_path).unwrap().ino(), repaired_inode);

    let requests = server.received_requests().await.unwrap();
    assert_eq!(requests.len(), 3);
    let second_query = query_params(&requests[1]);
    assert_eq!(
        second_query.get("sinceTime").map(String::as_str),
        Some("300")
    );
    assert!(!second_query.contains_key("checksum"));
    let third_query = query_params(&requests[2]);
    assert_eq!(
        third_query.get("checksum").map(String::as_str),
        Some("repairchecksum")
    );
}

#[tokio::test]
async fn conditional_fetch_rejects_explicit_empty_checksum_conflicts() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY}.json"
        )))
        .respond_with(config_response(
            config_json_with_cursor(400, Some("checksum400")),
            400,
            Some("checksum400"),
        ))
        .mount(&server)
        .await;

    let specs_url = format!("{}/v2/download_config_specs", server.uri());
    let first = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY,
        &specs_url,
        None,
    )
    .await
    .unwrap();
    let cursor = MmapSyncCursor {
        lcut: 400,
        checksum: Some("checksum400".to_string()),
    };
    assert_eq!(first, MmapWriteOutcome::Published(cursor.clone()));

    let artifact_path = mmap_path_for_sdk_key(MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY);
    let artifact_bytes = fs::read(&artifact_path).unwrap();
    #[cfg(unix)]
    let artifact_inode = fs::metadata(&artifact_path).unwrap().ino();

    server.reset().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY}.json"
        )))
        .respond_with(config_response(
            config_json_with_cursor(401, Some("checksum401")),
            401,
            Some(""),
        ))
        .mount(&server)
        .await;
    let full_mismatch = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY,
        &specs_url,
        Some(&cursor),
    )
    .await;
    assert!(matches!(
        full_mismatch,
        Err(StatsigErr::InvalidOperation(_))
    ));

    server.reset().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .insert_header("x-cache-hit", "true")
                .insert_header("x-since-time", "400")
                .insert_header("x-checksum", "")
                .set_body_string(r#"{"has_updates":false}"#),
        )
        .mount(&server)
        .await;
    let no_update_mismatch = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY,
        &specs_url,
        Some(&cursor),
    )
    .await;
    assert!(matches!(
        no_update_mismatch,
        Err(StatsigErr::InvalidOperation(_))
    ));

    assert_eq!(fs::read(&artifact_path).unwrap(), artifact_bytes);
    #[cfg(unix)]
    assert_eq!(fs::metadata(&artifact_path).unwrap().ino(), artifact_inode);
}

#[tokio::test]
async fn conditional_fetch_accepts_protobuf_generation_without_checksum_header() {
    const PROTO_LCUT: u64 = 1_767_981_029_384;

    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_PROTO_GENERATION_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/octet-stream")
                .insert_header("content-encoding", "statsig-br")
                .insert_header("x-since-time", PROTO_LCUT.to_string())
                .set_body_bytes(EVAL_PROJ_PROTO),
        )
        .mount(&server)
        .await;

    let previous = MmapSyncCursor {
        lcut: PROTO_LCUT - 1,
        checksum: Some("previouschecksum".to_string()),
    };
    let specs_url = format!("{}/v2/download_config_specs", server.uri());
    let outcome = InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
        MMAP_PROTO_GENERATION_SDK_KEY,
        &specs_url,
        Some(&previous),
    )
    .await
    .unwrap();

    let MmapWriteOutcome::Published(cursor) = outcome else {
        panic!("higher-LCUT protobuf response did not publish");
    };
    assert_eq!(cursor.lcut, PROTO_LCUT);
    assert!(cursor.checksum.is_some());

    let requests = server.received_requests().await.unwrap();
    assert_eq!(requests.len(), 1);
    let query = query_params(&requests[0]);
    assert_eq!(query["sinceTime"], (PROTO_LCUT - 1).to_string());
    assert_eq!(
        query.get("checksum").map(String::as_str),
        Some("previouschecksum")
    );
}

rusty_fork_test! {
    #[test]
    fn same_key_refresh_lock_prevents_delayed_response_rollback() {
        const STALE_MARKER: &str = "mmap-generation-101";
        const NEWEST_MARKER: &str = "mmap-generation-102";

        tokio::runtime::Builder::new_multi_thread()
            .worker_threads(2)
            .enable_all()
            .build()
            .unwrap()
            .block_on(async {
                let server = MockServer::start().await;
                let response_index = Arc::new(AtomicUsize::new(0));
                let first_body = config_json_with_marker(101, "checksum101", STALE_MARKER);
                let second_body = config_json_with_marker(102, "checksum102", NEWEST_MARKER);
                Mock::given(method("GET"))
                    .and(path(format!(
                        "/v2/download_config_specs/{MMAP_CONCURRENT_SAME_KEY}.json"
                    )))
                    .respond_with(move |_request: &Request| {
                        match response_index.fetch_add(1, Ordering::SeqCst) {
                            0 => config_response(first_body.clone(), 101, Some("checksum101"))
                                .set_delay(Duration::from_millis(250)),
                            1 => config_response(second_body.clone(), 102, Some("checksum102")),
                            index => panic!("unexpected request index {index}"),
                        }
                    })
                    .mount(&server)
                    .await;

                let previous = MmapSyncCursor {
                    lcut: 100,
                    checksum: Some("checksum100".to_string()),
                };
                let specs_url = format!("{}/v2/download_config_specs", server.uri());
                let first_url = specs_url.clone();
                let first_previous = previous.clone();
                let first = tokio::spawn(async move {
                    InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
                        MMAP_CONCURRENT_SAME_KEY,
                        &first_url,
                        Some(&first_previous),
                    )
                    .await
                });
                let second = tokio::spawn(async move {
                    InternedStore::fetch_and_write_mmap_with_specs_url_if_changed(
                        MMAP_CONCURRENT_SAME_KEY,
                        &specs_url,
                        Some(&previous),
                    )
                    .await
                });

                let mut published_lcuts = [first.await.unwrap().unwrap(), second.await.unwrap().unwrap()]
                    .map(|outcome| match outcome {
                        MmapWriteOutcome::Published(cursor) => cursor.lcut,
                        MmapWriteOutcome::NoUpdate => panic!("concurrent refresh did not publish"),
                    });
                published_lcuts.sort_unstable();
                assert_eq!(published_lcuts, [101, 102]);

                let v2_path = mmap_v2_path_for_sdk_key(MMAP_CONCURRENT_SAME_KEY);
                let v2_file = File::open(v2_path).unwrap();
                let v2_mmap = unsafe { Mmap::map(&v2_file).unwrap() };
                let archived =
                    rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&v2_mmap).unwrap();
                let newest_hash = rkyv::primitive::ArchivedU64::from_native(hashing::hash_one(
                    NEWEST_MARKER.as_bytes(),
                ));
                let stale_hash = rkyv::primitive::ArchivedU64::from_native(hashing::hash_one(
                    STALE_MARKER.as_bytes(),
                ));
                assert!(archived.feature_gates.get(&newest_hash).is_some());
                assert!(archived.feature_gates.get(&stale_hash).is_none());
            });
    }

    #[test]
    fn concurrent_fetches_publish_two_valid_v2_artifacts() {
        tokio::runtime::Builder::new_multi_thread()
            .worker_threads(2)
            .enable_all()
            .build()
            .unwrap()
            .block_on(async {
                let server = MockServer::start().await;
                for sdk_key in [MMAP_CONCURRENT_A_SDK_KEY, MMAP_CONCURRENT_B_SDK_KEY] {
                    Mock::given(method("GET"))
                        .and(path(format!("/v2/download_config_specs/{sdk_key}.json")))
                        .respond_with(
                            ResponseTemplate::new(200)
                                .insert_header("content-type", "application/json")
                                .set_body_string(EVAL_PROJ_JSON),
                        )
                        .mount(&server)
                        .await;
                }

                let specs_url = format!("{}/v2/download_config_specs", server.uri());
                let first_url = specs_url.clone();
                let first = tokio::spawn(async move {
                    InternedStore::fetch_and_write_mmap_with_specs_url(
                        MMAP_CONCURRENT_A_SDK_KEY,
                        &first_url,
                    )
                    .await
                });
                let second = tokio::spawn(async move {
                    InternedStore::fetch_and_write_mmap_with_specs_url(
                        MMAP_CONCURRENT_B_SDK_KEY,
                        &specs_url,
                    )
                    .await
                });
                first.await.unwrap().unwrap();
                second.await.unwrap().unwrap();

                validate_mmap_v2_for_test(&mmap_v2_path_for_sdk_key(
                    MMAP_CONCURRENT_A_SDK_KEY,
                ))
                .unwrap();
                validate_mmap_v2_for_test(&mmap_v2_path_for_sdk_key(
                    MMAP_CONCURRENT_B_SDK_KEY,
                ))
                .unwrap();
            });
    }

    #[test]
    fn public_fetch_and_preload_uses_full_v2_graph() {
        tokio::runtime::Runtime::new().unwrap().block_on(async {
            let server = MockServer::start().await;
            Mock::given(method("GET"))
                .and(path(format!(
                    "/v2/download_config_specs/{MMAP_V2_PUBLIC_SDK_KEY}.json"
                )))
                .respond_with(
                    ResponseTemplate::new(200)
                        .insert_header("content-type", "application/json")
                        .set_body_string(EVAL_PROJ_JSON),
                )
                .mount(&server)
                .await;

            InternedStore::fetch_and_write_mmap_with_specs_url(
                MMAP_V2_PUBLIC_SDK_KEY,
                &format!("{}/v2/download_config_specs", server.uri()),
            )
            .await
            .unwrap();
            InternedStore::preload_mmap(MMAP_V2_PUBLIC_SDK_KEY).unwrap();

            let specs: SpecsResponseFull = serde_json::from_str(EVAL_PROJ_JSON).unwrap();
            assert!(specs.feature_gates.0.values().all(|spec| spec.is_mmap()));
            assert!(specs.dynamic_configs.0.values().all(|spec| spec.is_mmap()));
            assert!(specs.layer_configs.0.values().all(|spec| spec.is_mmap()));
        });
    }

    #[test]
    fn fetch_and_write_mmap_decodes_json_numeric_returnables_with_arbitrary_precision() {
        tokio::runtime::Runtime::new().unwrap().block_on(async {
            let server = MockServer::start().await;
            Mock::given(method("GET"))
                .and(path(format!(
                    "/v2/download_config_specs/{MMAP_NUMERIC_SDK_KEY}.json"
                )))
                .respond_with(
                    ResponseTemplate::new(200)
                        .insert_header("content-type", "application/json")
                        .set_body_string(BIG_NUMBER_JSON),
                )
                .mount(&server)
                .await;

            InternedStore::fetch_and_write_mmap_with_specs_url(
                MMAP_NUMERIC_SDK_KEY,
                &format!("{}/v2/download_config_specs", server.uri()),
            )
            .await
            .unwrap();

            let file = File::open(mmap_path_for_sdk_key(MMAP_NUMERIC_SDK_KEY)).unwrap();
            let mmap = unsafe { Mmap::map(&file).unwrap() };
            let archived =
                rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&mmap).unwrap();

            assert!(matches!(
                archived.find_returnable_value_for_test("f64"),
                Some(ArchivedRkyvValue::Number(ArchivedRkyvNumber::Float(value)))
                    if value.to_native() == 0.999_999_999_999_999_1
            ));
        });
    }

    #[test]
    fn fetch_and_write_mmap_decodes_protobuf_numeric_returnables_with_arbitrary_precision() {
        tokio::runtime::Runtime::new().unwrap().block_on(async {
            let server = MockServer::start().await;
            Mock::given(method("GET"))
                .and(path(format!(
                    "/v2/download_config_specs/{MMAP_PROTO_NUMERIC_SDK_KEY}.json"
                )))
                .respond_with(
                    ResponseTemplate::new(200)
                        .insert_header("content-type", "application/octet-stream")
                        .insert_header("content-encoding", "statsig-br")
                        .set_body_bytes(EVAL_PROJ_PROTO),
                )
                .mount(&server)
                .await;

            InternedStore::fetch_and_write_mmap_with_specs_url(
                MMAP_PROTO_NUMERIC_SDK_KEY,
                &format!("{}/v2/download_config_specs", server.uri()),
            )
            .await
            .unwrap();

            let file = File::open(mmap_path_for_sdk_key(MMAP_PROTO_NUMERIC_SDK_KEY)).unwrap();
            let mmap = unsafe { Mmap::map(&file).unwrap() };
            let archived =
                rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&mmap).unwrap();

            assert!(matches!(
                archived.find_returnable_value_for_test("bbb"),
                Some(ArchivedRkyvValue::Number(ArchivedRkyvNumber::Float(value)))
                    if value.to_native() == 1e55
            ));
        });
    }
}

#[cfg(unix)]
#[tokio::test]
async fn fetch_and_write_mmap_atomically_replaces_existing_artifact() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_REPLACE_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_string(EVAL_PROJ_JSON),
        )
        .mount(&server)
        .await;

    let path = mmap_path_for_sdk_key(MMAP_REPLACE_SDK_KEY);
    let v2_path = mmap_v2_path_for_sdk_key(MMAP_REPLACE_SDK_KEY);
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, b"previous artifact").unwrap();
    fs::write(&v2_path, b"previous v2 artifact").unwrap();
    let mut previous_artifact = File::open(&path).unwrap();
    let mut previous_v2_artifact = File::open(&v2_path).unwrap();

    InternedStore::fetch_and_write_mmap_with_specs_url(
        MMAP_REPLACE_SDK_KEY,
        &format!("{}/v2/download_config_specs", server.uri()),
    )
    .await
    .unwrap();

    let mut previous_contents = Vec::new();
    previous_artifact
        .read_to_end(&mut previous_contents)
        .unwrap();
    assert_eq!(previous_contents, b"previous artifact");
    let mut previous_v2_contents = Vec::new();
    previous_v2_artifact
        .read_to_end(&mut previous_v2_contents)
        .unwrap();
    assert_eq!(previous_v2_contents, b"previous v2 artifact");

    let published = fs::read(&path).unwrap();
    assert_ne!(published, b"previous artifact");
    rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&published).unwrap();
    let published_v2 = fs::read(&v2_path).unwrap();
    assert_ne!(published_v2, b"previous v2 artifact");
    rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&published_v2).unwrap();
    assert_eq!(
        fs::metadata(path).unwrap().permissions().mode() & 0o777,
        0o644
    );
    assert_eq!(
        fs::metadata(v2_path).unwrap().permissions().mode() & 0o777,
        0o644
    );
}

#[cfg(target_os = "linux")]
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
#[ignore = "requires root to run writer and reader subprocesses with distinct UIDs"]
async fn uid_10001_can_preload_artifact_written_by_uid_1000() {
    match std::env::var("STATSIG_CROSS_UID_ROLE").as_deref() {
        Ok("writer") => {
            InternedStore::fetch_and_write_mmap_with_specs_url(
                MMAP_CROSS_UID_SDK_KEY,
                &std::env::var("STATSIG_CROSS_UID_SPECS_URL").unwrap(),
            )
            .await
            .unwrap();
            return;
        }
        Ok("reader") => {
            InternedStore::preload_mmap(MMAP_CROSS_UID_SDK_KEY).unwrap();
            return;
        }
        Ok(role) => panic!("unexpected cross-UID test role {role}"),
        Err(_) => {}
    }

    assert_eq!(
        unsafe { libc::geteuid() },
        0,
        "cross-UID integration test must run as root"
    );

    let shared_mount = tempfile::tempdir().unwrap();
    fs::set_permissions(shared_mount.path(), fs::Permissions::from_mode(0o755)).unwrap();
    let mount_path_bytes = std::os::unix::ffi::OsStrExt::as_bytes(shared_mount.path().as_os_str());
    let mount_path_c_string = std::ffi::CString::new(mount_path_bytes).unwrap();
    assert_eq!(
        unsafe { libc::chown(mount_path_c_string.as_ptr(), 1000, 1000) },
        0
    );

    let cross_uid_test_binary = shared_mount.path().join("cross_uid_test");
    fs::copy(std::env::current_exe().unwrap(), &cross_uid_test_binary).unwrap();
    fs::set_permissions(&cross_uid_test_binary, fs::Permissions::from_mode(0o755)).unwrap();

    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path(format!(
            "/v2/download_config_specs/{MMAP_CROSS_UID_SDK_KEY}.json"
        )))
        .respond_with(
            ResponseTemplate::new(200)
                .insert_header("content-type", "application/json")
                .set_body_string(EVAL_PROJ_JSON),
        )
        .mount(&server)
        .await;

    let run_as = |role: &str, uid: u32| {
        std::process::Command::new(&cross_uid_test_binary)
            .arg("--ignored")
            .arg("--exact")
            .arg(CROSS_UID_TEST_NAME)
            .arg("--nocapture")
            .env("STATSIG_CROSS_UID_ROLE", role)
            .env(
                "STATSIG_CROSS_UID_SPECS_URL",
                format!("{}/v2/download_config_specs", server.uri()),
            )
            .env("TMPDIR", shared_mount.path())
            .uid(uid)
            .gid(uid)
            .status()
            .unwrap()
    };

    assert!(run_as("writer", 1000).success());

    let artifact_path = shared_mount
        .path()
        .join("statsig-interned-store")
        .join(format!(
            "{}_v1_interned_store.mmap",
            hashing::djb2(MMAP_CROSS_UID_SDK_KEY)
        ));
    let metadata = fs::metadata(&artifact_path).unwrap();
    assert_eq!(metadata.uid(), 1000);
    assert_eq!(metadata.permissions().mode() & 0o777, 0o644);
    let v2_artifact_path = shared_mount
        .path()
        .join("statsig-interned-store")
        .join(format!(
            "{}_v2_interned_store.mmap",
            hashing::djb2(MMAP_CROSS_UID_SDK_KEY)
        ));
    let v2_metadata = fs::metadata(&v2_artifact_path).unwrap();
    assert_eq!(v2_metadata.uid(), 1000);
    assert_eq!(v2_metadata.permissions().mode() & 0o777, 0o644);
    let manifest_path = shared_mount
        .path()
        .join("statsig-interned-store")
        .join(format!(
            "{}_interned_store_manifest.json",
            hashing::djb2(MMAP_CROSS_UID_SDK_KEY)
        ));
    let manifest_metadata = fs::metadata(&manifest_path).unwrap();
    assert_eq!(manifest_metadata.uid(), 1000);
    assert_eq!(manifest_metadata.permissions().mode() & 0o777, 0o644);

    assert!(run_as("reader", 10001).success());
}

#[test]
fn mmap_paths_are_scoped_by_sdk_key() {
    assert_ne!(
        mmap_path_for_sdk_key(MMAP_FETCH_SDK_KEY),
        mmap_path_for_sdk_key(OTHER_MMAP_FETCH_SDK_KEY)
    );
    assert_ne!(
        mmap_v2_path_for_sdk_key(MMAP_FETCH_SDK_KEY),
        mmap_v2_path_for_sdk_key(OTHER_MMAP_FETCH_SDK_KEY)
    );
    assert_ne!(
        mmap_manifest_path_for_sdk_key(MMAP_FETCH_SDK_KEY),
        mmap_manifest_path_for_sdk_key(OTHER_MMAP_FETCH_SDK_KEY)
    );
    assert_ne!(
        mmap_lock_path_for_sdk_key(MMAP_FETCH_SDK_KEY),
        mmap_lock_path_for_sdk_key(OTHER_MMAP_FETCH_SDK_KEY)
    );
}

#[test]
fn sdk_key_write_lock_rejects_a_second_file_handle() {
    let path = mmap_lock_path_for_sdk_key("interned-store-file-lock");
    let first = acquire_mmap_write_lock_for_test(&path).unwrap();
    let second = fs::OpenOptions::new()
        .read(true)
        .write(true)
        .open(path)
        .unwrap();
    assert!(fs4::FileExt::try_lock(&second).is_err());
    drop((first, second));
}

#[cfg(any(unix, windows))]
#[test]
fn committed_v2_validation_keeps_the_validated_file_handle() {
    let sdk_key = "interned-store-open-handle";
    let v1_path = mmap_path_for_sdk_key(sdk_key);
    let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
    fs::write(&v1_path, V1_COMPATIBILITY_FIXTURE).unwrap();
    write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
    write_mmap_manifest_for_test(&manifest_path, &v1_path, &v2_path).unwrap();

    let validated = open_committed_mmap_v2_for_test(&manifest_path, &v1_path, &v2_path)
        .unwrap()
        .unwrap();
    let replacement = tempfile::NamedTempFile::new_in(v2_path.parent().unwrap()).unwrap();
    fs::write(replacement.path(), b"replacement is malformed").unwrap();
    replacement.persist(&v2_path).unwrap();

    let mmap = unsafe { Mmap::map(&validated).unwrap() };
    rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&mmap).unwrap();
    assert_eq!(fs::read(v2_path).unwrap(), b"replacement is malformed");
}

rusty_fork_test! {
    #[test]
    fn preload_mmap_prefers_v2_when_both_artifacts_exist() {
        let sdk_key = "interned-store-prefer-v2";
        let v1_path = mmap_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
        fs::write(&v1_path, b"malformed v1 that must not be read").unwrap();
        write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
        write_mmap_manifest_for_test(&manifest_path, &v1_path, &v2_path).unwrap();

        InternedStore::preload_mmap(sdk_key).unwrap();
        let specs: SpecsResponseFull = serde_json::from_str(EVAL_PROJ_JSON).unwrap();
        assert!(specs.feature_gates.0.values().all(|spec| spec.is_mmap()));
        assert!(specs.dynamic_configs.0.values().all(|spec| spec.is_mmap()));
        assert!(specs.layer_configs.0.values().all(|spec| spec.is_mmap()));
    }

    #[test]
    fn preload_mmap_accepts_v2_only_manifest_without_v1() {
        let sdk_key = "interned-store-v2-only-manifest";
        let v1_path = mmap_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v2_path.parent().unwrap()).unwrap();
        let _ = fs::remove_file(v1_path);
        write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
        write_mmap_v2_only_manifest_for_test(&manifest_path, &v2_path).unwrap();

        InternedStore::preload_mmap(sdk_key).unwrap();
        let specs: SpecsResponseFull = serde_json::from_str(EVAL_PROJ_JSON).unwrap();
        assert!(specs.feature_gates.0.values().all(|spec| spec.is_mmap()));
        assert!(specs.dynamic_configs.0.values().all(|spec| spec.is_mmap()));
        assert!(specs.layer_configs.0.values().all(|spec| spec.is_mmap()));
    }

    #[test]
    fn preload_mmap_retries_instead_of_latching_v1_during_v2_only_refresh() {
        let sdk_key = "interned-store-v2-only-refresh";
        let v1_path = mmap_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
        fs::write(&v1_path, V1_COMPATIBILITY_FIXTURE).unwrap();
        write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
        write_mmap_v2_only_manifest_for_test(&manifest_path, &v2_path).unwrap();

        let replacement = tempfile::NamedTempFile::new_in(v2_path.parent().unwrap()).unwrap();
        fs::write(replacement.path(), b"next v2 generation").unwrap();
        replacement.persist(&v2_path).unwrap();

        assert!(matches!(
            InternedStore::preload_mmap(sdk_key),
            Err(StatsigErr::InvalidOperation(message))
                if message == "Interned mmap V2 publication is incomplete; retry preload"
        ));
    }

    #[test]
    fn preload_mmap_falls_back_to_v1_only_when_v2_is_absent() {
        let sdk_key = "interned-store-v1-fallback";
        let v1_path = mmap_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
        let _ = fs::remove_file(v2_path);
        let _ = fs::remove_file(manifest_path);
        fs::write(v1_path, V1_COMPATIBILITY_FIXTURE).unwrap();

        InternedStore::preload_mmap(sdk_key).unwrap();
    }

    #[test]
    fn preload_mmap_falls_back_after_v1_only_refresh() {
        let sdk_key = "interned-store-v1-only-refresh";
        let v1_path = mmap_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
        fs::write(&v1_path, b"old v1 generation").unwrap();
        write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
        write_mmap_manifest_for_test(&manifest_path, &v1_path, &v2_path).unwrap();

        // Simulate a rollback to a V1-only writer or a partial next publication.
        fs::write(&v1_path, V1_COMPATIBILITY_FIXTURE).unwrap();

        InternedStore::preload_mmap(sdk_key).unwrap();
        let specs: SpecsResponseFull = serde_json::from_str(EVAL_PROJ_JSON).unwrap();
        assert!(specs.feature_gates.0.values().all(|spec| !spec.is_mmap()));
        assert!(specs.dynamic_configs.0.values().all(|spec| !spec.is_mmap()));
        assert!(specs.layer_configs.0.values().all(|spec| !spec.is_mmap()));
    }

    #[test]
    fn preload_mmap_rejects_committed_malformed_v2() {
        let sdk_key = "interned-store-malformed-v2";
        let v1_path = mmap_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
        fs::write(v1_path, V1_COMPATIBILITY_FIXTURE).unwrap();
        fs::write(&v2_path, b"malformed v2").unwrap();
        write_mmap_manifest_for_test(&manifest_path, &mmap_path_for_sdk_key(sdk_key), &v2_path)
            .unwrap();

        assert!(matches!(
            InternedStore::preload_mmap(sdk_key),
            Err(StatsigErr::SerializationError(_))
        ));
    }
}

#[test]
fn preload_mmap_rejects_malformed_archive() {
    let sdk_key = "interned-store-malformed-mmap";
    let path = mmap_path_for_sdk_key(sdk_key);
    let _ = fs::remove_file(mmap_v2_path_for_sdk_key(sdk_key));
    let _ = fs::remove_file(mmap_manifest_path_for_sdk_key(sdk_key));
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
    let _ = fs::remove_file(mmap_v2_path_for_sdk_key(sdk_key));
    let _ = fs::remove_file(mmap_manifest_path_for_sdk_key(sdk_key));
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
