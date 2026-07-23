#[cfg(any(unix, windows))]
use crate::interned_values::interned_store::open_committed_mmap_v2_for_test;
use crate::{
    evaluation::rkyv_value::{ArchivedRkyvNumber, ArchivedRkyvValue},
    hashing,
    interned_values::{
        interned_store::{
            acquire_mmap_write_lock_for_test, legacy_mmap_v1_path_for_sdk_key,
            mmap_lock_path_for_sdk_key, mmap_manifest_path_for_sdk_key, mmap_v2_path_for_sdk_key,
            validate_mmap_v2_for_test, write_mmap_manifest_for_test, write_mmap_v2_for_test,
            write_mmap_v2_only_manifest_for_test, LEGACY_MMAP_FORMAT_VERSION,
        },
        mmap_data_v2::{ArchivedMmapDataV2, MmapDataV2},
        InternedStore, MmapArtifactState, MmapPreloadOptions, MmapSyncCursor, MmapWriteOutcome,
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
const LEGACY_V1_TEST_BYTES: &[u8] = b"legacy v1 artifact";

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

#[tokio::test]
async fn fetch_and_write_mmap_uses_authoritative_sdk_key_path() {
    let server = MockServer::start().await;
    let v1_path = legacy_mmap_v1_path_for_sdk_key(MMAP_FETCH_SDK_KEY);
    let _ = fs::remove_file(&v1_path);
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

    let v2_path = mmap_v2_path_for_sdk_key(MMAP_FETCH_SDK_KEY);
    let manifest_path = mmap_manifest_path_for_sdk_key(MMAP_FETCH_SDK_KEY);
    let expected_v2_filename = format!(
        "{}_v2_interned_store.mmap",
        hashing::djb2(MMAP_FETCH_SDK_KEY)
    );
    assert!(!v1_path.exists());
    assert_eq!(
        v2_path.file_name().and_then(|name| name.to_str()),
        Some(expected_v2_filename.as_str())
    );

    let v2_file = File::open(&v2_path).unwrap();
    let v2_mmap = unsafe { Mmap::map(&v2_file).unwrap() };
    let v2_archived = rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&v2_mmap).unwrap();
    assert_eq!(
        v2_archived.format_version.to_native(),
        MmapDataV2::FORMAT_VERSION
    );

    #[cfg(unix)]
    assert_eq!(
        fs::metadata(&v2_path).unwrap().permissions().mode() & 0o777,
        0o644
    );
    assert!(manifest_path.exists());
    let manifest =
        serde_json::from_slice::<serde_json::Value>(&fs::read(&manifest_path).unwrap()).unwrap();
    assert!(manifest.get("v1").is_none());
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

    let artifact_path = mmap_v2_path_for_sdk_key(MMAP_NO_UPDATE_SDK_KEY);
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
    let artifact_path = mmap_v2_path_for_sdk_key(MMAP_GENERATION_SDK_KEY);
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
    let artifact_path = mmap_v2_path_for_sdk_key(MMAP_STALE_SDK_KEY);
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

    let artifact_path = mmap_v2_path_for_sdk_key(MMAP_SAME_LCUT_REPAIR_SDK_KEY);
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

    let artifact_path = mmap_v2_path_for_sdk_key(MMAP_EMPTY_CHECKSUM_CONFLICT_SDK_KEY);
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

            let file = File::open(mmap_v2_path_for_sdk_key(MMAP_NUMERIC_SDK_KEY)).unwrap();
            let mmap = unsafe { Mmap::map(&file).unwrap() };
            let archived =
                rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&mmap).unwrap();

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

            let file = File::open(mmap_v2_path_for_sdk_key(MMAP_PROTO_NUMERIC_SDK_KEY)).unwrap();
            let mmap = unsafe { Mmap::map(&file).unwrap() };
            let archived =
                rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&mmap).unwrap();

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
async fn fetch_and_write_mmap_replaces_v2_and_leaves_v1_untouched() {
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

    let v1_path = legacy_mmap_v1_path_for_sdk_key(MMAP_REPLACE_SDK_KEY);
    let v2_path = mmap_v2_path_for_sdk_key(MMAP_REPLACE_SDK_KEY);
    fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
    fs::write(&v1_path, b"previous v1 artifact").unwrap();
    fs::write(&v2_path, b"previous v2 artifact").unwrap();
    let mut previous_v1_artifact = File::open(&v1_path).unwrap();
    let mut previous_v2_artifact = File::open(&v2_path).unwrap();

    InternedStore::fetch_and_write_mmap_with_specs_url(
        MMAP_REPLACE_SDK_KEY,
        &format!("{}/v2/download_config_specs", server.uri()),
    )
    .await
    .unwrap();

    let mut previous_v1_contents = Vec::new();
    previous_v1_artifact
        .read_to_end(&mut previous_v1_contents)
        .unwrap();
    assert_eq!(previous_v1_contents, b"previous v1 artifact");
    let mut previous_v2_contents = Vec::new();
    previous_v2_artifact
        .read_to_end(&mut previous_v2_contents)
        .unwrap();
    assert_eq!(previous_v2_contents, b"previous v2 artifact");

    assert_eq!(fs::read(&v1_path).unwrap(), b"previous v1 artifact");
    let published_v2 = fs::read(&v2_path).unwrap();
    assert_ne!(published_v2, b"previous v2 artifact");
    rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&published_v2).unwrap();
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

    let v1_artifact_path = shared_mount
        .path()
        .join("statsig-interned-store")
        .join(format!(
            "{}_v1_interned_store.mmap",
            hashing::djb2(MMAP_CROSS_UID_SDK_KEY)
        ));
    assert!(!v1_artifact_path.exists());
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
        legacy_mmap_v1_path_for_sdk_key(MMAP_FETCH_SDK_KEY),
        legacy_mmap_v1_path_for_sdk_key(OTHER_MMAP_FETCH_SDK_KEY)
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
fn inspect_mmap_artifact_reports_missing_and_legacy_v1() {
    let sdk_key = "interned-store-inspect-legacy-v1";
    remove_mmap_artifacts(sdk_key);

    let missing = InternedStore::inspect_mmap_artifact(sdk_key).unwrap();
    assert_eq!(missing.state, MmapArtifactState::Missing);
    assert_eq!(missing.state.as_str(), "missing");
    assert_eq!(missing.format_version, None);
    assert_eq!(missing.v1_bytes, None);
    assert_eq!(missing.v2_bytes, None);
    assert_eq!(missing.manifest_bytes, None);
    assert_eq!(missing.total_linked_bytes, 0);
    assert_eq!(missing.linked_file_count, 0);

    let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
    fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
    fs::write(&v1_path, LEGACY_V1_TEST_BYTES).unwrap();

    let legacy = InternedStore::inspect_mmap_artifact(sdk_key).unwrap();
    assert_eq!(legacy.state, MmapArtifactState::LegacyV1);
    assert_eq!(legacy.state.as_str(), "legacy_v1");
    assert_eq!(legacy.format_version, Some(LEGACY_MMAP_FORMAT_VERSION));
    assert_eq!(legacy.v1_bytes, Some(LEGACY_V1_TEST_BYTES.len() as u64));
    assert_eq!(legacy.v2_bytes, None);
    assert_eq!(legacy.manifest_bytes, None);
    assert_eq!(legacy.total_linked_bytes, LEGACY_V1_TEST_BYTES.len() as u64);
    assert_eq!(legacy.linked_file_count, 1);
    assert!(legacy.newest_linked_modified_unix_seconds.is_some());
}

#[test]
fn inspect_mmap_artifact_reports_committed_and_incomplete_v2() {
    let sdk_key = "interned-store-inspect-committed-v2";
    remove_mmap_artifacts(sdk_key);
    let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(v2_path.parent().unwrap()).unwrap();
    write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
    write_mmap_v2_only_manifest_for_test(&manifest_path, &v2_path).unwrap();

    let committed = InternedStore::inspect_mmap_artifact(sdk_key).unwrap();
    let v2_bytes = fs::metadata(&v2_path).unwrap().len();
    let manifest_bytes = fs::metadata(&manifest_path).unwrap().len();
    assert_eq!(committed.state, MmapArtifactState::CommittedV2);
    assert_eq!(committed.state.as_str(), "committed_v2");
    assert_eq!(committed.format_version, Some(MmapDataV2::FORMAT_VERSION));
    assert_eq!(committed.v1_bytes, None);
    assert_eq!(committed.v2_bytes, Some(v2_bytes));
    assert_eq!(committed.manifest_bytes, Some(manifest_bytes));
    assert_eq!(committed.total_linked_bytes, v2_bytes + manifest_bytes);
    assert_eq!(committed.linked_file_count, 2);
    assert!(committed.newest_linked_modified_unix_seconds.is_some());
    #[cfg(any(unix, windows))]
    {
        let capacity = committed.filesystem_capacity_bytes.unwrap();
        let available = committed.filesystem_available_bytes.unwrap();
        assert!(capacity > 0);
        assert!(available <= capacity);
    }

    let replacement = tempfile::NamedTempFile::new_in(v2_path.parent().unwrap()).unwrap();
    fs::write(replacement.path(), b"next uncommitted v2 generation").unwrap();
    replacement.persist(&v2_path).unwrap();

    let incomplete = InternedStore::inspect_mmap_artifact(sdk_key).unwrap();
    assert_eq!(incomplete.state, MmapArtifactState::IncompleteV2);
    assert_eq!(incomplete.state.as_str(), "incomplete_v2");
    assert_eq!(incomplete.format_version, None);
    assert_eq!(
        incomplete.v2_bytes,
        Some(b"next uncommitted v2 generation".len() as u64)
    );
    assert_eq!(incomplete.manifest_bytes, Some(manifest_bytes));
    assert_eq!(incomplete.linked_file_count, 2);
}

#[test]
fn inspect_mmap_artifact_reports_v1_fallback_after_identity_failure() {
    let sdk_key = "interned-store-inspect-v1-fallback";
    remove_mmap_artifacts(sdk_key);
    let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
    let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
    fs::write(&v1_path, LEGACY_V1_TEST_BYTES).unwrap();
    write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
    write_mmap_manifest_for_test(&manifest_path, &v1_path, &v2_path).unwrap();

    let replacement = tempfile::NamedTempFile::new_in(v2_path.parent().unwrap()).unwrap();
    fs::write(replacement.path(), b"replacement v2 generation").unwrap();
    replacement.persist(&v2_path).unwrap();

    let fallback = InternedStore::inspect_mmap_artifact(sdk_key).unwrap();
    assert_eq!(fallback.state, MmapArtifactState::FallbackV1);
    assert_eq!(fallback.state.as_str(), "fallback_v1");
    assert_eq!(fallback.format_version, Some(LEGACY_MMAP_FORMAT_VERSION));
    assert_eq!(fallback.v1_bytes, Some(LEGACY_V1_TEST_BYTES.len() as u64));
    assert_eq!(
        fallback.v2_bytes,
        Some(b"replacement v2 generation".len() as u64)
    );
    assert!(fallback.manifest_bytes.is_some());
    assert_eq!(fallback.linked_file_count, 3);

    fs::remove_file(v1_path).unwrap();
    let invalid = InternedStore::inspect_mmap_artifact(sdk_key).unwrap();
    assert_eq!(invalid.state, MmapArtifactState::Invalid);
    assert_eq!(invalid.state.as_str(), "invalid");
    assert_eq!(invalid.format_version, None);
    assert_eq!(invalid.v1_bytes, None);
    assert_eq!(invalid.linked_file_count, 2);
}

#[test]
fn inspect_mmap_artifact_rejects_an_oversized_manifest() {
    let sdk_key = "interned-store-inspect-oversized-manifest";
    remove_mmap_artifacts(sdk_key);
    let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(v2_path.parent().unwrap()).unwrap();
    write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
    fs::write(&manifest_path, vec![b' '; 64 * 1024 + 1]).unwrap();

    let snapshot = InternedStore::inspect_mmap_artifact(sdk_key).unwrap();
    assert_eq!(snapshot.state, MmapArtifactState::Invalid);
    assert_eq!(
        snapshot.v2_bytes,
        Some(fs::metadata(v2_path).unwrap().len())
    );
    assert_eq!(snapshot.manifest_bytes, Some(64 * 1024 + 1));
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

fn remove_mmap_artifacts(sdk_key: &str) {
    for path in [
        legacy_mmap_v1_path_for_sdk_key(sdk_key),
        mmap_v2_path_for_sdk_key(sdk_key),
        mmap_manifest_path_for_sdk_key(sdk_key),
        mmap_lock_path_for_sdk_key(sdk_key),
    ] {
        let _ = fs::remove_file(path);
    }
}

#[cfg(any(unix, windows))]
#[test]
fn committed_v2_validation_keeps_the_validated_file_handle() {
    let sdk_key = "interned-store-open-handle";
    let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
    let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
    fs::write(&v1_path, b"paired v1 generation").unwrap();
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
        let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
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
        let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v2_path.parent().unwrap()).unwrap();
        let _ = fs::remove_file(v1_path);
        write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
        write_mmap_v2_only_manifest_for_test(&manifest_path, &v2_path).unwrap();

        let report = InternedStore::preload_mmap_with_options(
            sdk_key,
            &MmapPreloadOptions::default(),
        )
        .unwrap();
        assert_eq!(report.format_version, MmapDataV2::FORMAT_VERSION);
        assert_eq!(report.loaded, 1);
        let specs: SpecsResponseFull = serde_json::from_str(EVAL_PROJ_JSON).unwrap();
        assert!(specs.feature_gates.0.values().all(|spec| spec.is_mmap()));
        assert!(specs.dynamic_configs.0.values().all(|spec| spec.is_mmap()));
        assert!(specs.layer_configs.0.values().all(|spec| spec.is_mmap()));
    }

    #[test]
    fn preload_mmap_retries_during_v2_only_refresh() {
        let sdk_key = "interned-store-v2-only-refresh";
        let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
        fs::write(&v1_path, b"stale v1 generation").unwrap();
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
    fn preload_mmap_rejects_v2_when_paired_v1_was_replaced() {
        let sdk_key = "interned-store-v1-only-refresh";
        let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v1_path.parent().unwrap()).unwrap();
        fs::write(&v1_path, b"old v1 generation").unwrap();
        write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
        write_mmap_manifest_for_test(&manifest_path, &v1_path, &v2_path).unwrap();

        fs::write(&v1_path, b"replacement v1 generation").unwrap();

        assert!(matches!(
            InternedStore::preload_mmap(sdk_key),
            Err(StatsigErr::InvalidOperation(message))
                if message == "No committed interned mmap V2 artifact was found"
        ));
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn mmap_reader_memory_snapshot_tracks_deleted_loaded_generation() {
        let sdk_key = "interned-store-reader-memory";
        remove_mmap_artifacts(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v2_path.parent().unwrap()).unwrap();
        write_mmap_v2_for_test(EVAL_PROJ_JSON.as_bytes(), &v2_path).unwrap();
        write_mmap_v2_only_manifest_for_test(&manifest_path, &v2_path).unwrap();
        let expected_mapped_bytes = fs::metadata(&v2_path).unwrap().len();

        InternedStore::preload_mmap(sdk_key).unwrap();
        let loaded = InternedStore::mmap_reader_memory_snapshot()
            .unwrap()
            .unwrap();
        assert_eq!(loaded.format_version, MmapDataV2::FORMAT_VERSION);
        assert_eq!(loaded.mapped_bytes, expected_mapped_bytes);
        assert_eq!(loaded.loaded_generation_count, 1);
        assert!(loaded.resident_bytes.is_some());
        assert!(loaded.proportional_set_bytes.is_some());
        assert!(loaded.private_dirty_bytes.is_some());
        assert_eq!(loaded.deleted_mapped_bytes, Some(0));
        assert!(loaded.vma_segment_count.is_some_and(|count| count >= 1));

        let replacement = tempfile::NamedTempFile::new_in(v2_path.parent().unwrap()).unwrap();
        fs::write(replacement.path(), b"next generation").unwrap();
        replacement.persist(&v2_path).unwrap();

        let deleted = InternedStore::mmap_reader_memory_snapshot()
            .unwrap()
            .unwrap();
        assert_eq!(deleted.mapped_bytes, expected_mapped_bytes);
        assert_eq!(deleted.deleted_mapped_bytes, Some(expected_mapped_bytes));
        assert_eq!(deleted.loaded_generation_count, 1);
    }

    #[test]
    fn preload_mmap_rejects_committed_malformed_v2() {
        let sdk_key = "interned-store-malformed-v2";
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
        fs::create_dir_all(v2_path.parent().unwrap()).unwrap();
        fs::write(&v2_path, b"malformed v2").unwrap();
        write_mmap_v2_only_manifest_for_test(&manifest_path, &v2_path).unwrap();

        assert!(matches!(
            InternedStore::preload_mmap(sdk_key),
            Err(StatsigErr::SerializationError(_))
        ));
    }
}

#[test]
fn preload_mmap_rejects_malformed_archive() {
    let sdk_key = "interned-store-malformed-mmap";
    let path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, b"not an rkyv archive").unwrap();
    write_mmap_v2_only_manifest_for_test(&manifest_path, &path).unwrap();

    assert!(matches!(
        InternedStore::preload_mmap(sdk_key),
        Err(StatsigErr::SerializationError(_))
    ));
}

#[test]
fn preload_mmap_rejects_unsupported_format_version() {
    let sdk_key = "interned-store-unsupported-version-mmap";
    let path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(path.parent().unwrap()).unwrap();

    let mmap_data = MmapDataV2 {
        format_version: 3,
        ..MmapDataV2::default()
    };
    let archived = rkyv::to_bytes::<rkyv::rancor::Error>(&mmap_data).unwrap();
    fs::write(&path, archived).unwrap();
    write_mmap_v2_only_manifest_for_test(&manifest_path, &path).unwrap();

    assert!(matches!(
        InternedStore::preload_mmap(sdk_key),
        Err(StatsigErr::SerializationError(message))
            if message == "Unsupported interned mmap format version 3; expected 2"
    ));
}

#[test]
fn preload_mmap_rejects_uncommitted_v2() {
    let sdk_key = "interned-store-uncommitted-v2";
    let path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, b"uncommitted v2").unwrap();
    let _ = fs::remove_file(manifest_path);

    assert!(matches!(
        InternedStore::preload_mmap(sdk_key),
        Err(StatsigErr::InvalidOperation(message))
            if message == "Interned mmap V2 publication is incomplete; retry preload"
    ));
}
