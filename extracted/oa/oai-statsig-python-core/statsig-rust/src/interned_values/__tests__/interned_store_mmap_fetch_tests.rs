use crate::{
    evaluation::rkyv_value::{ArchivedRkyvNumber, ArchivedRkyvValue},
    hashing,
    interned_values::{
        interned_store::{mmap_path_for_sdk_key, ArchivedMmapDataV1, MmapDataV1},
        InternedStore,
    },
    StatsigErr,
};
use memmap2::Mmap;
use rusty_fork::rusty_fork_test;
#[cfg(unix)]
use std::os::unix::fs::PermissionsExt;
#[cfg(target_os = "linux")]
use std::os::unix::{fs::MetadataExt, process::CommandExt};
use std::{fs, fs::File, io::Read};
use wiremock::{
    matchers::{method, path},
    Mock, MockServer, ResponseTemplate,
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
const EVAL_PROJ_JSON: &str = include_str!("../../../tests/data/eval_proj_dcs.json");
const EVAL_PROJ_PROTO: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.pb.br");
const BIG_NUMBER_JSON: &str = include_str!("../../../tests/data/big_number_dcs.json");
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

    let file = File::open(&path).unwrap();
    let mmap = unsafe { Mmap::map(&file).unwrap() };
    let archived = rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&mmap).unwrap();
    assert_eq!(archived.format_version(), MmapDataV1::FORMAT_VERSION);

    #[cfg(unix)]
    assert_eq!(
        fs::metadata(&path).unwrap().permissions().mode() & 0o777,
        0o644
    );
}

rusty_fork_test! {
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
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, b"previous artifact").unwrap();
    let mut previous_artifact = File::open(&path).unwrap();

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

    let published = fs::read(&path).unwrap();
    assert_ne!(published, b"previous artifact");
    rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&published).unwrap();
    assert_eq!(
        fs::metadata(path).unwrap().permissions().mode() & 0o777,
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

    assert!(run_as("reader", 10001).success());
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
