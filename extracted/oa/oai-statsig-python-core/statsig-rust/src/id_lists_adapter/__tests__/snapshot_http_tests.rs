use super::*;
use crate::SpecStore;
use crate::id_lists_adapter::shared_id_list_format::{digest, hex};
use crate::portable_id_list_ef::{MEDIA_TYPE, encode_prefix_v1};
use crate::sdk_event_emitter::SdkEventEmitter;
use mockito::{Matcher, Mock, Server};
use serde_json::json;

const KEY: &str = "test-id-list-snapshot-key";
const GEN: &str = "g1.regional.east";
const RAW: &str = "/v1/download_id_list_file/company%2Fg1.regional.east?private=true";
const RECORD: &str = "+AAAAAAAA\n";

fn client(server: &Server) -> (StatsigHttpIdListsAdapter, Arc<SpecStore>) {
    configured_client(server, Some(true), server.url())
}

fn configured_client(
    server: &Server,
    private_ef: Option<bool>,
    endpoint: String,
) -> (StatsigHttpIdListsAdapter, Arc<SpecStore>) {
    let options = StatsigOptions {
        id_lists_url: Some(format!("{}/manifest", server.url())),
        download_id_list_file_api: Some(endpoint),
        enable_id_list_elias_fano: private_ef,
        ..Default::default()
    };
    store_client(options)
}

fn store_client(options: StatsigOptions) -> (StatsigHttpIdListsAdapter, Arc<SpecStore>) {
    let store = Arc::new(SpecStore::new(
        KEY,
        "snapshot".into(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    ));
    let adapter = StatsigHttpIdListsAdapter::new_with_store(KEY, &options, Arc::clone(&store));
    (adapter, store)
}

fn manifest(server: &mut Server, generation: &str, size: usize) -> Mock {
    let path = RAW.replace(GEN, generation);
    server.mock("POST", "/manifest").with_body(json!({
        "users": {"name":"users", "url":format!("https://fixture{path}"), "fileID":generation,
                  "creationTime":1,"size":size}
    }).to_string()).create()
}

fn offer(server: &mut Server, path: &str) -> Mock {
    server
        .mock("GET", path)
        .match_header("statsig-api-key", KEY)
        .match_header("accept", MEDIA_TYPE)
        .match_header("range", "bytes=0-")
        .match_header("accept-encoding", "identity")
}

fn raw_request(server: &mut Server, path: &str, start: usize) -> Mock {
    server
        .mock("GET", path)
        .match_header("range", format!("bytes={start}-").as_str())
        .match_header(
            "accept",
            Matcher::AnyOf(vec![Matcher::Missing, Matcher::Exact("*/*".into())]),
        )
}

fn image_headers(request: Mock, bytes: &[u8], end: usize) -> Mock {
    request
        .with_header("content-type", MEDIA_TYPE)
        .with_header("x-statsig-id-list-file-id", GEN)
        .with_header("x-statsig-id-list-raw-end", end.to_string().as_str())
        .with_header("x-statsig-id-list-sha256", hex(&digest(bytes)).as_str())
}

#[tokio::test]
async fn id_list_snapshot_publishes_800_then_requests_raw_tail_on_next_poll() {
    for lazy in [false, true] {
        let mut server = Server::new_async().await;
        let (adapter, store) = store_client(StatsigOptions {
            id_lists_url: Some(format!("{}/manifest", server.url())),
            download_id_list_file_api: Some(server.url()),
            enable_id_list_elias_fano: Some(true),
            lazy_load_id_lists: Some(lazy),
            id_list_init_build_concurrency: Some(2),
            experimental_flags: Some(["parallel_lazy_id_list_builds".into()].into()),
            ..Default::default()
        });
        let adapter = Arc::new(adapter);
        let prefix = RECORD.repeat(79) + "+CCCCCCCC\n";
        let (end, bytes) = encode_prefix_v1(prefix.as_bytes(), 0).unwrap().unwrap();
        assert_eq!(end, 800);
        let row = manifest(&mut server, GEN, 1000);
        let image = image_headers(offer(&mut server, RAW), &bytes, end)
            .with_body(bytes)
            .expect(1)
            .create();
        let unexpected = raw_request(&mut server, RAW, 800).expect(0).create();
        adapter.sync_id_lists().await.unwrap();
        if lazy {
            assert!(store.load_data().id_lists.is_empty());
            adapter.process_id_list("users").await.unwrap();
            adapter.process_id_list("users").await.unwrap();
        }
        let first = store.load_data();
        let list = &first.id_lists["users"];
        assert_eq!(list.metadata.size, 800);
        assert!(list.ids.has_compact_base());
        assert!(list.ids.contains("AAAAAAAA") && list.ids.contains("CCCCCCCC"));
        assert!(!list.ids.contains("BBBBBBBB"));
        unexpected.assert();
        unexpected.remove();
        let tail = raw_request(&mut server, RAW, 800)
            .with_status(206)
            .with_header("content-range", "bytes 800-999/1000")
            .with_body("-AAAAAAAA\n".to_string() + &"+BBBBBBBB\n".repeat(19))
            .expect(1)
            .create();
        adapter.sync_id_lists().await.unwrap();
        tail.assert();
        image.assert();
        let final_data = store.load_data();
        let list = &final_data.id_lists["users"];
        assert_eq!(list.metadata.size, 1000);
        assert!(list.ids.contains("BBBBBBBB") && list.ids.contains("CCCCCCCC"));
        assert!(!list.ids.contains("AAAAAAAA"));
        assert!(first.id_lists["users"].ids.contains("AAAAAAAA"));
        row.remove();
        let replacement = "g2.regional.west";
        let _row = manifest(&mut server, replacement, 1000);
        let new_file = offer(&mut server, &RAW.replace(GEN, replacement))
            .with_body("+DDDDDDDD\n".repeat(100))
            .create();
        adapter.sync_id_lists().await.unwrap();
        new_file.assert();
        let data = store.load_data();
        assert!(data.id_lists["users"].ids.contains("DDDDDDDD"));
        assert!(!data.id_lists["users"].ids.contains("CCCCCCCC"));
        assert_eq!(data.id_lists["users"].metadata.size, 1000);
    }
}

#[tokio::test]
async fn id_list_snapshot_accepts_legacy_raw_200_and_206_on_the_first_request() {
    for status in [200, 206] {
        let mut server = Server::new_async().await;
        let (adapter, store) = client(&server);
        let _row = manifest(&mut server, GEN, 20);
        let first = offer(&mut server, RAW).with_status(status);
        let first = if status == 206 {
            first.with_header("content-range", "bytes 0-9/20")
        } else {
            first
        };
        let first = first.with_body(RECORD).expect(1).create();
        adapter.sync_id_lists().await.unwrap();
        assert_eq!(store.load_data().id_lists["users"].metadata.size, 10);
        let next = raw_request(&mut server, RAW, 10)
            .with_status(206)
            .with_header("content-range", "bytes 10-19/20")
            .with_body("+BBBBBBBB\n")
            .expect(1)
            .create();
        adapter.sync_id_lists().await.unwrap();
        first.assert();
        next.assert();
        assert_eq!(store.load_data().id_lists["users"].metadata.size, 20);
        assert!(store.load_data().id_lists["users"].ids.contains("BBBBBBBB"));
    }
}

#[test]
fn transport_recognizes_supported_snapshot_in_accept_list() {
    let unsupported = "application/vnd.statsig.id-list-ef;version=2";
    assert!(snapshot_http::accepts_snapshot(&format!(
        "{unsupported}, {MEDIA_TYPE}"
    )));
    assert!(!snapshot_http::accepts_snapshot(unsupported));
}

#[test]
fn content_type_alone_identifies_an_unsupported_snapshot_version() {
    let mut body = ResponseData::from_bytes(Vec::new());
    body.append_header(
        "content-type".into(),
        "Application/Vnd.Statsig.Id-List-Ef;version=2".into(),
    );
    assert!(snapshot_http::is_snapshot_response(&body));
}

#[tokio::test]
async fn id_list_snapshot_invalid_representation_retries_only_authorized_raw() {
    let (_, valid) = encode_prefix_v1(RECORD.as_bytes(), 0).unwrap().unwrap();
    for defect in [
        "generation",
        "zero",
        "unaligned",
        "overshoot",
        "signed",
        "digest",
        "uppercase",
        "codec",
        "range",
        "encoding",
        "gzip",
        "partial",
        "missing",
        "duplicate-digest",
        "duplicate-content-type",
        "version",
    ] {
        let mut server = Server::new_async().await;
        let (adapter, store) = client(&server);
        let _row = manifest(&mut server, GEN, 20);
        let bytes = if defect == "codec" {
            vec![0; valid.len()]
        } else {
            valid.clone()
        };
        let hash = hex(&digest(&bytes));
        let bytes = if defect == "gzip" {
            use std::io::Write;
            let mut encoder =
                flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::default());
            encoder.write_all(&bytes).unwrap();
            encoder.finish().unwrap()
        } else {
            bytes
        };
        let response = offer(&mut server, RAW)
            .with_status(if defect == "partial" { 206 } else { 200 })
            .with_header(
                "content-type",
                if defect == "version" {
                    "application/vnd.statsig.id-list-ef;version=2"
                } else {
                    MEDIA_TYPE
                },
            )
            .with_header(
                "x-statsig-id-list-file-id",
                if defect == "generation" {
                    "g2.regional.east"
                } else {
                    GEN
                },
            )
            .with_header(
                "x-statsig-id-list-raw-end",
                match defect {
                    "zero" => "0",
                    "unaligned" => "11",
                    "overshoot" => "30",
                    "signed" => "+10",
                    _ => "10",
                },
            );
        let response = match defect {
            "missing" => response,
            "digest" => response.with_header("x-statsig-id-list-sha256", &"0".repeat(64)),
            "uppercase" => response.with_header("x-statsig-id-list-sha256", &hash.to_uppercase()),
            _ => response.with_header("x-statsig-id-list-sha256", &hash),
        };
        let response = match defect {
            "range" => response.with_header("content-range", "bytes 0-9/20"),
            "duplicate-digest" => response.with_header("x-statsig-id-list-sha256", &hash),
            "duplicate-content-type" => response.with_header("content-type", MEDIA_TYPE),
            "encoding" => response.with_header("content-encoding", "identity"),
            "gzip" => response.with_header("content-encoding", "gzip"),
            _ => response,
        }
        .with_body(bytes)
        .expect(1)
        .create();
        let retry = raw_request(&mut server, RAW, 0)
            .with_body("+BBBBBBBB\n".repeat(2))
            .expect(1)
            .create();
        adapter.sync_id_lists().await.unwrap();
        response.assert();
        retry.assert();
        let data = store.load_data();
        assert!(data.id_lists["users"].ids.contains("BBBBBBBB"), "{defect}");
        assert!(!data.id_lists["users"].ids.contains("AAAAAAAA"));
    }
}

#[tokio::test]
async fn id_list_snapshot_denials_and_redirects_do_not_forward_credentials() {
    for status in [401, 403, 307] {
        let mut server = Server::new_async().await;
        let mut foreign = Server::new_async().await;
        let (adapter, store) = client(&server);
        let _row = manifest(&mut server, GEN, 10);
        let leak = foreign.mock("GET", "/private").expect(0).create();
        let location = format!("{}/private", foreign.url());
        let denied = offer(&mut server, RAW)
            .with_status(status)
            .with_header("location", &location)
            .expect(1)
            .create();
        let raw = raw_request(&mut server, RAW, 0)
            .with_status(status)
            .with_header("location", &location)
            .expect(usize::from(status == 307))
            .create();
        assert!(adapter.sync_id_lists().await.is_err());
        denied.assert();
        raw.assert();
        leak.assert();
        assert!(store.load_data().id_lists.is_empty());
    }
}

#[tokio::test]
async fn id_list_snapshot_opt_out_uses_legacy_raw_request() {
    for enabled in [Some(false), None] {
        let mut server = Server::new_async().await;
        let (adapter, store) = configured_client(&server, enabled, server.url());
        let _row = manifest(&mut server, GEN, 10);
        let raw = raw_request(&mut server, RAW, 0)
            .with_body(RECORD)
            .expect(1)
            .create();
        adapter.sync_id_lists().await.unwrap();
        raw.assert();
        assert!(store.load_data().id_lists["users"].ids.contains("AAAAAAAA"));
    }
}

#[test]
fn id_list_snapshot_requires_private_ef_and_an_explicit_file_endpoint() {
    for (ef, endpoint, enabled) in [
        (None, Some("https://files.test"), false),
        (Some(false), Some("https://files.test"), false),
        (Some(true), None, false),
        (Some(true), Some(""), false),
        (Some(true), Some("relative/path"), false),
        (Some(true), Some("ftp://files.test"), false),
        (Some(true), Some("https://user@files.test"), false),
        (Some(true), Some("https://files.test?key=other"), false),
        (Some(true), Some("https://files.test#fragment"), false),
        (Some(true), Some("https://files.test/sfp"), true),
    ] {
        let options = StatsigOptions {
            enable_id_list_elias_fano: ef,
            download_id_list_file_api: endpoint.map(str::to_owned),
            ..Default::default()
        };
        assert_eq!(
            StatsigHttpIdListsAdapter::new(KEY, &options).snapshot_enabled,
            enabled
        );
    }
}

#[tokio::test]
async fn id_list_snapshot_mixed_batch_rejects_concurrent_raw_cursors_and_catalog_changes() {
    // "other" needs a raw append. "retired" will be removed by this manifest.
    fn update(name: &str, size: u64, raw: Option<&str>) -> IdListUpdate {
        IdListUpdate {
            new_metadata: IdListMetadata {
                name: name.into(),
                url: format!("https://fixture/{name}"),
                file_id: Some(name.into()),
                size,
                creation_time: 1,
            },
            raw_changeset: raw.map(str::to_owned),
        }
    }
    for race in [
        "append",
        "remove",
        "add",
        "failed download",
        "partial refresh",
    ] {
        let partial = race == "partial refresh";
        let download_failed = partial || race == "failed download";
        let mut server = Server::new_async().await;
        let (mut adapter, store) = client(&server);
        adapter.partial_refresh = partial;
        store.did_receive_id_list_updates(HashMap::from([
            ("other".into(), update("other", 10, Some(RECORD))),
            ("retired".into(), update("retired", 10, Some(RECORD))),
        ]));
        let (_, bytes) = encode_prefix_v1(RECORD.repeat(1000).as_bytes(), 0)
            .unwrap()
            .unwrap();
        let _row = server.mock("POST", "/manifest").with_body(json!({
            "users": {"name":"users","url":format!("https://fixture{RAW}"),"fileID":GEN,
                      "size":10000,"creationTime":1},
            "other": {"name":"other","url":"https://fixture/other","fileID":"other","size":20,"creationTime":1}
        }).to_string()).create();
        let concurrent = Arc::clone(&store);
        let image = image_headers(offer(&mut server, RAW), &bytes, 10000)
            .with_body_from_request(move |_| {
                let mut rows = HashMap::from([
                    ("other".into(), update("other", 10, None)),
                    ("retired".into(), update("retired", 10, None)),
                ]);
                match race {
                    "append" => {
                        rows.insert("other".into(), update("other", 20, Some("+BBBBBBBB\n")));
                    }
                    "remove" => {
                        rows.remove("retired");
                    }
                    "add" => {
                        rows.insert("new".into(), update("new", 10, Some(RECORD)));
                    }
                    _ => return bytes.clone(),
                }
                concurrent.did_receive_id_list_updates(rows);
                bytes.clone()
            })
            .create();
        let raw = server
            .mock("GET", "/other")
            .match_header("range", "bytes=10-")
            .with_status(if download_failed { 403 } else { 206 })
            .with_header("content-range", "bytes 10-19/20")
            .with_body("+CCCCCCCC\n")
            .create();
        let err = adapter.sync_id_lists().await.unwrap_err();
        if !download_failed {
            assert!(err.to_string().contains("cursor changed"), "{race}: {err}");
        }
        image.assert();
        raw.assert();
        let published = store.load_data();
        assert_eq!(published.id_lists.contains_key("users"), partial, "{race}");
        if partial {
            let users = &published.id_lists["users"];
            assert_eq!(users.metadata.size, 10000);
            assert!(users.ids.contains("AAAAAAAA"));
        }
        assert_eq!(
            published.id_lists.contains_key("retired"),
            !partial && race != "remove"
        );
        assert_eq!(published.id_lists.contains_key("new"), race == "add");
        let other = &published.id_lists["other"];
        assert_eq!(other.metadata.size, if race == "append" { 20 } else { 10 });
        assert_eq!(other.ids.contains("BBBBBBBB"), race == "append");
        assert!(!other.ids.contains("CCCCCCCC"));
    }
}

#[tokio::test]
async fn id_list_snapshot_raw_only_append_after_adoption_rejects_a_changed_cursor() {
    let mut server = Server::new_async().await;
    let (adapter, store) = client(&server);
    let (_, bytes) = encode_prefix_v1(RECORD.repeat(1000).as_bytes(), 0)
        .unwrap()
        .unwrap();
    let row = manifest(&mut server, GEN, 10000);
    let image = image_headers(offer(&mut server, RAW), &bytes, 10000)
        .with_body(bytes)
        .expect(1)
        .create();
    adapter.sync_id_lists().await.unwrap();
    row.remove();
    let _next = manifest(&mut server, GEN, 10010);
    let other = Arc::clone(&store);
    let raw = server
        .mock("GET", RAW)
        .match_header("range", "bytes=10000-")
        .with_status(206)
        .with_header("content-range", "bytes 10000-10009/10010")
        .with_body_from_request(move |_| {
            let mut metadata = other
                .get_current_id_list_metadata()
                .remove("users")
                .unwrap();
            metadata.size = 10010;
            other.did_receive_id_list_updates(HashMap::from([(
                "users".into(),
                IdListUpdate {
                    new_metadata: metadata,
                    raw_changeset: Some("+BBBBBBBB\n".into()),
                },
            )]));
            b"+CCCCCCCC\n".to_vec()
        })
        .create();
    assert!(
        adapter
            .sync_id_lists()
            .await
            .unwrap_err()
            .to_string()
            .contains("cursor changed")
    );
    image.assert();
    raw.assert();
    let data = store.load_data();
    assert_eq!(data.id_lists["users"].metadata.size, 10010);
    assert!(data.id_lists["users"].ids.contains("BBBBBBBB"));
    assert!(!data.id_lists["users"].ids.contains("CCCCCCCC"));
}

fn raw_update(name: &str, member: &str) -> IdListUpdate {
    let raw = format!("+{member}\n");
    IdListUpdate {
        new_metadata: IdListMetadata {
            name: name.into(),
            creation_time: 1,
            size: raw.len() as u64,
            file_id: Some(GEN.into()),
            url: format!("https://fixture{RAW}"),
        },
        raw_changeset: Some(raw),
    }
}

#[tokio::test]
async fn id_list_snapshot_empty_and_removal_only_replacements_check_concurrent_catalog() {
    for initially_empty in [true, false] {
        let server = Server::new_async().await;
        let (adapter, store) = client(&server);
        if !initially_empty {
            store.did_receive_id_list_updates(HashMap::from([(
                "retired".into(),
                raw_update("retired", "AAAAAAAA"),
            )]));
        }
        let staged = adapter
            .fetch_id_list_updates(
                store.as_ref(),
                FetchReason::Refresh(RefreshTrigger::PrivateInitialize),
                &store.get_current_id_list_metadata(),
                HashMap::new(),
                &mut 0,
            )
            .await
            .unwrap();
        store.did_receive_partial_id_list_updates_with_propagation(
            HashMap::from([("winner".into(), raw_update("winner", "BBBBBBBB"))]),
            HashMap::new(),
        );
        assert!(
            adapter
                .publish_id_list_updates(store.clone(), staged, None, None, None)
                .await
                .unwrap_err()
                .to_string()
                .contains("cursor changed")
        );
        let catalog = &store.load_data().id_lists;
        assert!(catalog["winner"].ids.contains("BBBBBBBB"));
        assert_eq!(catalog.contains_key("retired"), !initially_empty);
    }
}

#[tokio::test]
async fn id_list_snapshot_rejected_lazy_refresh_preserves_manifest_for_next_cold_load() {
    let mut server = Server::new_async().await;
    let (mut adapter, store) = client(&server);
    adapter.lazy_id_lists = Some(LazyIdLists {
        manifest: Default::default(),
        build_permits: None,
        before_build: None,
    });
    let adapter = Arc::new(adapter);
    let rows = |size, cold_path| {
        json!({
        "users":{"name":"users","url":format!("https://fixture{RAW}"),"fileID":GEN,"size":size,"creationTime":1},
        "cold":{"name":"cold","url":format!("https://fixture/{cold_path}"),"fileID":cold_path,"size":10,"creationTime":1},
    }).to_string()
    };
    let before = server
        .mock("POST", "/manifest")
        .with_body(rows(10, "old"))
        .create();
    adapter.sync_id_lists().await.unwrap();
    let _initial = server
        .mock("GET", RAW)
        .match_header("range", "bytes=0-")
        .with_body("+AAAAAAAA\n")
        .create();
    adapter.process_id_list("users").await.unwrap();
    before.remove();
    let _after = server
        .mock("POST", "/manifest")
        .with_body(rows(20, "rejected"))
        .create();
    let other = store.clone();
    let _append = server
        .mock("GET", RAW)
        .match_header("range", "bytes=10-")
        .with_status(206)
        .with_header("content-range", "bytes 10-19/20")
        .with_body_from_request(move |_| {
            other.did_receive_partial_id_list_updates_with_propagation(
                HashMap::from([("winner".into(), raw_update("winner", "BBBBBBBB"))]),
                HashMap::new(),
            );
            b"+CCCCCCCC\n".to_vec()
        })
        .create();
    assert!(
        adapter
            .sync_id_lists()
            .await
            .unwrap_err()
            .to_string()
            .contains("cursor changed")
    );
    let old = server.mock("GET", "/old").with_body("+DDDDDDDD\n").create();
    let rejected = server.mock("GET", "/rejected").expect(0).create();
    adapter.process_id_list("cold").await.unwrap();
    old.assert();
    rejected.assert();
    let data = store.load_data();
    assert!(data.id_lists["cold"].ids.contains("DDDDDDDD"));
    assert!(data.id_lists["winner"].ids.contains("BBBBBBBB"));
    assert_eq!(data.id_lists["users"].metadata.size, 10);
    assert!(!data.id_lists["users"].ids.contains("CCCCCCCC"));
}

#[tokio::test]
async fn id_list_snapshot_gateway_allows_legacy_encoded_percent_and_rejects_encoded_traversal() {
    let mut server = Server::new_async().await;
    let (adapter, store) =
        configured_client(&server, Some(false), format!("{}/gateway", server.url()));
    let _row = server.mock("POST","/manifest").with_body(json!({"users":{"name":"users","url":"https://fixture/discount%25","fileID":"discount%","size":10,"creationTime":1}}).to_string()).create();
    let raw = server
        .mock("GET", "/gateway/discount%25")
        .with_body("+AAAAAAAA\n")
        .create();
    adapter.sync_id_lists().await.unwrap();
    raw.assert();
    assert!(store.load_data().id_lists["users"].ids.contains("AAAAAAAA"));
    for path in ["/x%2f..%2fv1", "/x%252f%252e%252e%252fv1"] {
        assert!(adapter.get_override_id_list_download_url(path).is_err());
    }
}

#[tokio::test]
async fn id_list_snapshot_same_file_id_at_another_source_restarts_membership() {
    let other_private = RAW.replace("company", "another");
    for (path, size) in [
        (other_private.as_str(), 10),
        ("/raw-only", 10),
        ("/raw-only", 20),
    ] {
        let mut server = Server::new_async().await;
        let (adapter, store) = client(&server);
        let (_, image) = encode_prefix_v1(RECORD.as_bytes(), 0).unwrap().unwrap();
        let first = manifest(&mut server, GEN, 10);
        let _image = image_headers(offer(&mut server, RAW), &image, 10)
            .with_body(image)
            .create();
        adapter.sync_id_lists().await.unwrap();
        first.remove();
        let old = store.load_data().id_lists["users"].metadata.clone();
        let target = IdListMetadata {
            url: format!("https://fixture{path}"),
            size: size as u64,
            ..old.clone()
        };
        assert!(!adapter.lazy_list_ready(store.as_ref(), Some(&old), &target));
        let _new = server
            .mock("POST", "/manifest")
            .with_body(json!({"users": target}).to_string())
            .create();
        if path == "/raw-only" && size == 20 {
            let mut foreign = Server::new_async().await;
            let leak = foreign.mock("GET", "/escaped").expect(0).create();
            let redirect = raw_request(&mut server, path, 0)
                .with_status(307)
                .with_header("location", &format!("{}/escaped", foreign.url()))
                .create();
            assert!(adapter.sync_id_lists().await.is_err());
            leak.assert();
            redirect.remove();
        }
        let request = if path == other_private {
            offer(&mut server, path)
        } else {
            raw_request(&mut server, path, 0)
        };
        let raw = request
            .with_body("+BBBBBBBB\n".repeat(size / 10))
            .expect(1)
            .create();
        adapter.sync_id_lists().await.unwrap();
        raw.assert();
        let data = store.load_data();
        let list = &data.id_lists["users"];
        assert_eq!(list.metadata.size, size as u64);
        assert!(list.ids.contains("BBBBBBBB"));
        assert!(!list.ids.contains("AAAAAAAA"));
    }
}

#[test]
fn id_list_snapshot_accepts_only_the_manifest_private_generation() {
    let metadata = |path: &str| IdListMetadata {
        name: "users".into(),
        size: 10,
        creation_time: 1,
        file_id: Some(GEN.into()),
        url: format!("https://fixture{path}"),
    };
    assert!(snapshot_http::private_generation(&metadata(RAW)));
    for path in [
        RAW.replace("g1.", "g2."),
        RAW.replace("%2F", "/"),
        RAW.replace("company", "company.regional.other"),
        format!("{RAW}&private=false"),
        format!("{RAW}&k={KEY}"),
        format!("{RAW}#fragment"),
    ] {
        assert!(
            !snapshot_http::private_generation(&metadata(&path)),
            "{path}"
        );
    }
}

struct FixedLimitProvider(
    crate::networking::providers::net_provider_reqwest::NetworkProviderReqwest,
);

#[async_trait]
impl crate::networking::NetworkProvider for FixedLimitProvider {
    async fn send(&self, method: &HttpMethod, args: &RequestArgs) -> Response {
        self.0.send(method, args).await
    }
    async fn send_with_response_limit(
        &self,
        method: &HttpMethod,
        args: &RequestArgs,
        limit: u64,
    ) -> crate::networking::ResponseLimitOutcome {
        self.0.send_with_response_limit(method, args, limit).await
    }
}

#[tokio::test]
async fn id_list_snapshot_decoder_limits_only_the_encoded_response() {
    use crate::networking::NetworkProvider;
    use crate::portable_id_list_ef::MAX_IMAGE_BYTES;

    let records = MAX_IMAGE_BYTES / RECORD.len() + 1;
    let size = records * RECORD.len();
    for fixed_limit_only in [false, true] {
        let mut server = Server::new_async().await;
        let (mut adapter, store) = store_client(StatsigOptions {
            id_lists_url: Some(format!("{}/manifest", server.url())),
            download_id_list_file_api: Some(server.url()),
            enable_id_list_elias_fano: Some(true),
            state_read_primary_attempts: Some(1),
            ..Default::default()
        });
        let _row = manifest(&mut server, GEN, size);
        let provider: Arc<dyn NetworkProvider> = Arc::new(FixedLimitProvider(Default::default()));
        let raw = if fixed_limit_only {
            adapter
                .network
                .set_network_provider_for_test(Arc::downgrade(&provider));
            raw_request(&mut server, RAW, 0)
        } else {
            let encoded = image_headers(offer(&mut server, RAW), b"", size)
                .with_body(vec![0; MAX_IMAGE_BYTES + 1])
                .expect(1)
                .create();
            let error = adapter.sync_id_lists().await.unwrap_err();
            assert!(
                error
                    .to_string()
                    .contains("snapshot exceeds maximum image size"),
                "{error}"
            );
            assert!(store.load_data().id_lists.is_empty());
            encoded.assert();
            encoded.remove();
            offer(&mut server, RAW)
        };
        let raw = raw.with_body(RECORD.repeat(records)).expect(1).create();
        adapter.sync_id_lists().await.unwrap();
        raw.assert();
        let data = store.load_data();
        assert_eq!(data.id_lists["users"].metadata.size, size as u64);
        assert!(data.id_lists["users"].ids.contains("AAAAAAAA"));
    }
}

#[tokio::test]
async fn id_list_snapshot_stripped_headers_never_publish_binary_as_raw() {
    let (_, single) = encode_prefix_v1(RECORD.as_bytes(), 0).unwrap().unwrap();
    assert_eq!(single.len(), 35);
    assert!(std::str::from_utf8(&single).is_ok());
    let ten_records = (0..10)
        .map(|i| format!("+AAAAAAA{i}\n"))
        .collect::<String>();
    let (_, ten) = encode_prefix_v1(ten_records.as_bytes(), 0)
        .unwrap()
        .unwrap();
    assert_eq!(ten[0], b'\n'); // A split inside the count can look like a complete raw line.
    for (image, split, raw_retry) in [
        (&single, None, true),
        (&single, None, false),
        (&single, Some(16), true),
        (&single, Some(1), true),
        (&ten, Some(1), true),
    ] {
        let total = image.len();
        let mut server = Server::new_async().await;
        let (adapter, store) = client(&server);
        let _row = manifest(&mut server, GEN, RECORD.len());
        let mut first =
            offer(&mut server, RAW).with_header("content-type", "application/octet-stream");
        let mut suffix = None;
        if let Some(split) = split {
            first = first
                .with_status(206)
                .with_header("content-range", &format!("bytes 0-{}/{total}", split - 1))
                .with_body(&image[..split]);
            suffix = Some(
                raw_request(&mut server, RAW, split)
                    .with_status(206)
                    .with_header("content-type", "application/octet-stream")
                    .with_header(
                        "content-range",
                        &format!("bytes {split}-{}/{total}", total - 1),
                    )
                    .with_body(&image[split..])
                    .expect(usize::from(split < 8))
                    .create(),
            );
        } else {
            first = first.with_body(image);
        }
        let first = first.expect(1).create();
        let retry = raw_request(&mut server, RAW, 0)
            .match_header("statsig-api-key", KEY)
            .with_header("content-type", "application/octet-stream")
            .with_body(if raw_retry { RECORD.as_bytes() } else { image })
            .expect(1)
            .create();
        let result = adapter.sync_id_lists().await;
        let data = store.load_data();
        if raw_retry {
            result.unwrap();
            assert_eq!(
                data.id_lists["users"].metadata.size,
                RECORD.len() as u64,
                "split {split:?}"
            );
            assert!(data.id_lists["users"].ids.contains("AAAAAAAA"));
        } else {
            assert!(result.is_err());
            assert!(data.id_lists.is_empty());
        }
        first.assert();
        retry.assert();
        if let Some(suffix) = suffix {
            suffix.assert();
        }
    }
}

#[tokio::test]
async fn id_list_snapshot_accepts_short_raw_lines_on_a_partial_response() {
    let mut server = Server::new_async().await;
    let (adapter, store) = client(&server);
    let _row = manifest(&mut server, GEN, 3);
    let first = offer(&mut server, RAW)
        .with_status(206)
        .with_header("content-range", "bytes 0-2/35")
        .with_body("+a\n")
        .expect(1)
        .create();
    adapter.sync_id_lists().await.unwrap();
    first.assert();
    let data = store.load_data();
    assert_eq!(data.id_lists["users"].metadata.size, 3);
    assert!(data.id_lists["users"].ids.contains("a"));
}

#[tokio::test]
async fn id_list_snapshot_stale_source_switch_skips_downloads() {
    let mut server = Server::new_async().await;
    let (adapter, store) = client(&server);
    let first = manifest(&mut server, GEN, 10);
    let initial = offer(&mut server, RAW).with_body(RECORD).expect(1).create();
    adapter.sync_id_lists().await.unwrap();
    first.remove();
    let installed = store.load_data().id_lists["users"].metadata.clone();
    let path = RAW.replace("company", "another");
    let stale = IdListMetadata {
        url: format!("https://fixture{path}"),
        creation_time: installed.creation_time - 1,
        ..installed.clone()
    };
    let _next = server
        .mock("POST", "/manifest")
        .with_body(json!({"users": stale}).to_string())
        .create();
    let skipped = server
        .mock("GET", path.as_str())
        .with_body("+BBBBBBBB\n")
        .expect(0)
        .create();
    for _ in 0..2 {
        adapter.sync_id_lists().await.unwrap();
        let data = store.load_data();
        let list = &data.id_lists["users"];
        assert_eq!(list.metadata.url, installed.url);
        assert_eq!(list.metadata.creation_time, installed.creation_time);
        assert!(list.ids.contains("AAAAAAAA"));
        assert!(!list.ids.contains("BBBBBBBB"));
    }
    initial.assert();
    skipped.assert();
    assert!(adapter.lazy_list_ready(store.as_ref(), Some(&installed), &stale));
}

#[tokio::test]
async fn id_list_snapshot_query_gateway_preserves_raw_routing() {
    let mut server = Server::new_async().await;
    let (adapter, store) = configured_client(
        &server,
        Some(false),
        format!("{}/download?path=", server.url()),
    );
    let _row = server.mock("POST", "/manifest").with_body(json!({"users":{
        "name":"users", "url":"https://origin/tenant/list", "fileID":"list", "size":10, "creationTime":1
    }}).to_string()).create();
    let raw = raw_request(&mut server, "/download?path=/tenant/list", 0)
        .with_body(RECORD)
        .expect(1)
        .create();
    adapter.sync_id_lists().await.unwrap();
    raw.assert();
    assert!(store.load_data().id_lists["users"].ids.contains("AAAAAAAA"));
}
