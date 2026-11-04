use super::tests::TestIdListsUpdateListener;
#[cfg(not(feature = "custom_network_provider"))]
use super::tests::with_local_cdn;
use super::*;
#[cfg(not(feature = "custom_network_provider"))]
use mockito::Server;

#[cfg(not(feature = "custom_network_provider"))]
const CDN_FILE: &str = "https://statsigcdn.openai.com/v1/download_id_list_file/company%2Fids?private=true&range=0-&token=a%2Bb&Range=10-";
#[cfg(not(feature = "custom_network_provider"))]
// The server sees the encoded path and token, with both legacy range parameters removed.
const PATH: &str = "/v1/download_id_list_file/company%2Fids?private=true&token=a%2Bb";

fn normalize_response(
    status: u16,
    range: Option<&str>,
    start: u64,
    size: u64,
    bytes: impl Into<Vec<u8>>,
    pending: PartialIdListRecord,
) -> Result<IdListDownload, StatsigErr> {
    let headers = range.map(|value| HashMap::from([("content-range".into(), value.into())]));
    let response = Response {
        status_code: Some(status),
        data: Some(ResponseData::from_bytes_with_headers(bytes.into(), headers)),
        error: None,
    };
    normalize_id_list_download(response, "/file", start, size, pending)
}

#[test]
fn id_list_range_rejects_invalid_responses() {
    for (status, range, start, size, body) in [
        (206, None, 3, 6, "+b\n"),
        (206, Some("invalid"), 3, 6, "+b\n"),
        (206, Some("bytes 0-2/6"), 3, 6, "+b\n"),
        (206, Some("bytes 3-5/6"), 3, 6, "+b"),
        (206, Some("bytes 3-5/5"), 3, 6, "+b\n"),
        (206, Some("bytes 3-5/*"), 3, 6, "+b\n"),
        (206, Some("bytes 3-2/3"), 3, 6, ""),
        (206, Some("bytes 3-18446744073709551615/6"), 3, 6, "+b\n"),
        (200, Some("invalid"), 3, 6, "+a\n+b\n"),
        (200, Some("bytes 0-5/6"), 3, 6, "+a\n+b\n"),
        (200, Some("bytes 3-8/9"), 3, 9, "+b\n"),
        (200, None, 2, 4, "+é\n"),
        (204, None, 0, 0, ""),
    ] {
        assert!(
            matches!(
                normalize_response(status, range, start, size, body, Default::default()),
                Err(StatsigErr::CustomError(_))
            ),
            "expected a terminal range error for {status} {range:?} at {start} for size {size}"
        );
    }
}

#[test]
fn id_list_range_distinguishes_stale_full_body_responses() {
    for (start, size, body) in [(3, 6, "+a\n"), (0, 3, ""), (9, 6, "+a\n+b\n")] {
        assert!(matches!(
            normalize_response(200, None, start, size, body, Default::default()),
            Err(StatsigErr::NetworkError(NetworkError::RequestFailed(
                _,
                Some(200),
                _
            )))
        ));
    }
}

#[test]
fn id_list_range_handles_empty_files_and_sizes_different_from_manifest() {
    for (status, header, start, size, body, expected, end) in [
        (200, None, 0, 0, "", "", 0),
        (200, None, 3, 9, "+a\n+b\n", "+b\n", 6),
        (200, Some("bytes 3-5/6"), 3, 9, "+b\n", "+b\n", 6),
        (206, Some("bytes 3-5/6"), 3, 9, "+b\n", "+b\n", 6),
        (200, None, 0, 3, "+a\n+b\n", "+a\n+b\n", 6),
        (200, None, 3, 6, "+a\n+b\n+c\n", "+b\n+c\n", 9),
        (200, Some("bytes 3-8/9"), 3, 6, "+b\n+c\n", "+b\n+c\n", 9),
        (206, Some("bytes 3-8/9"), 3, 6, "+b\n+c\n", "+b\n+c\n", 9),
    ] {
        assert_eq!(
            normalize_response(status, header, start, size, body, Default::default()).unwrap(),
            IdListDownload::Complete(expected.into(), start..end)
        );
    }
}

#[tokio::test]
#[cfg(not(feature = "custom_network_provider"))]
async fn id_list_range_preserves_membership_and_offsets_across_growth_and_replacement() {
    for (use_proxy, use_fallback) in [(false, false), (true, false), (true, true)] {
        for (status, partial) in [(200, false), (200, true), (206, true)] {
            let mut manifest = Server::new_async().await;
            let mut proxy = Server::new_async().await;
            let mut origin = Server::new_async().await;
            let adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    id_lists_url: Some(format!("{}/lists", manifest.url())),
                    download_id_list_file_api: use_proxy.then(|| proxy.url()),
                    fallback_to_statsig_api: Some(use_fallback),
                    ..StatsigOptions::default()
                },
            );
            let (adapter, _provider) = with_local_cdn(adapter, &origin);
            let listener = Arc::new(TestIdListsUpdateListener {
                id_lists: RwLock::new(HashMap::new()),
            });
            adapter.set_listener(listener.clone());

            // SFP can lag the manifest: apply each useful prefix and poll again
            // from the actual cursor. Also preserve overdelivery and replacement.
            for (generation, manifest_size, start, body, expected) in [
                (1, 18, 0, "+a\n+b\n", vec!["a", "b"]),
                (1, 18, 6, "+a\n+b\n-a\n+c\n", vec!["b", "c"]),
                (1, 18, 12, "+a\n+b\n-a\n+c\n-b\n+d\n", vec!["c", "d"]),
                (
                    1,
                    21,
                    18,
                    "+a\n+b\n-a\n+c\n-b\n+d\n-c\n+e\n",
                    vec!["d", "e"],
                ),
                (2, 13, 0, "+replacement\n", vec!["replacement"]),
            ] {
                let size = body.len();
                let manifest_request = manifest
                    .mock("POST", "/lists")
                    .with_body(
                        serde_json::json!({"list": {
                            "name": "list", "size": manifest_size, "url": CDN_FILE,
                            "creationTime": generation, "fileID": format!("file-{generation}")
                        }})
                        .to_string(),
                    )
                    .expect(1)
                    .create_async()
                    .await;
                let proxy_request = proxy
                    .mock("GET", PATH)
                    .match_header("range", format!("bytes={start}-").as_str())
                    .with_status(503)
                    .expect(2 * usize::from(use_fallback))
                    .create_async()
                    .await;
                let destination = if use_proxy && !use_fallback {
                    &mut proxy
                } else {
                    &mut origin
                };
                let mut fallback = destination
                    .mock("GET", PATH)
                    .match_header("range", format!("bytes={start}-").as_str())
                    .match_header(
                        "statsig-id-list-file-size",
                        manifest_size.to_string().as_str(),
                    )
                    .match_header("statsig-api-key", "secret-key")
                    .match_header("accept-encoding", "identity")
                    .with_status(status)
                    .with_body(if partial { &body[start..] } else { body })
                    .expect(1);
                if partial {
                    fallback = fallback.with_header(
                        "content-range",
                        &format!("bytes {start}-{}/{size}", size - 1),
                    );
                }
                let fallback = fallback.create_async().await;
                adapter.sync_id_lists().await.unwrap();
                manifest_request.assert_async().await;
                proxy_request.assert_async().await;
                fallback.assert_async().await;
                let lists = listener.id_lists.read();
                let list = &lists["list"];
                assert_eq!(list.metadata.size, size as u64);
                assert_eq!(
                    *list.ids,
                    expected
                        .into_iter()
                        .map(str::to_string)
                        .collect::<crate::id_lists_adapter::IdListIds>()
                );
            }
        }
    }
}

#[tokio::test]
#[cfg(not(feature = "custom_network_provider"))]
async fn id_list_range_rejects_invalid_or_exhausted_stale_data_without_publishing_or_advancing() {
    for (use_proxy, use_fallback) in [(false, false), (true, false), (true, true)] {
        for (status, header, body) in [
            (200, None, "+a\n"),
            (200, Some("invalid"), "+a\n+b\n"),
            (200, Some("bytes 0-5/6"), "+a\n+b\n"),
            (200, Some("bytes 3-8/9"), "+b\n"),
            (206, Some("bytes 0-2/6"), "+b\n"),
            (206, Some("bytes 3-5/6"), "+b"),
            (206, Some("bytes 3-3/6"), "+"),
            (416, None, ""),
        ] {
            let mut manifest = Server::new_async().await;
            let mut proxy = Server::new_async().await;
            let mut origin = Server::new_async().await;
            let metadata = IdListMetadata {
                name: "list".into(),
                url: CDN_FILE.into(),
                size: 6,
                file_id: Some("file-1".into()),
                creation_time: 1,
            };
            let mut list = crate::id_lists_adapter::IdList::new(metadata.clone());
            list.apply_update(IdListUpdate {
                raw_changeset: Some("+a\n".into()),
                new_metadata: metadata,
            });
            let listener = Arc::new(TestIdListsUpdateListener {
                id_lists: RwLock::new(HashMap::from([("list".into(), list)])),
            });
            let manifest_request = manifest
                .mock("POST", "/lists")
                .with_body(
                    serde_json::json!({"list": {
                        "name": "list", "size": 6, "url": CDN_FILE,
                        "creationTime": 1, "fileID": "file-1"
                    }})
                    .to_string(),
                )
                .expect(2)
                .create_async()
                .await;
            let proxy_request = proxy
                .mock("GET", PATH)
                .match_header("range", "bytes=3-")
                .with_status(503)
                .expect(if use_fallback { 4 } else { 0 })
                .create_async()
                .await;
            let destination = if use_proxy && !use_fallback {
                &mut proxy
            } else {
                &mut origin
            };
            let changes_etag = header == Some("bytes 3-3/6");
            let retryable = changes_etag || status == 416 || (status == 200 && header.is_none());
            let attempts = if retryable && !use_fallback { 2 } else { 1 };
            let continuation = destination
                .mock("GET", PATH)
                .match_header("range", "bytes=4-")
                .match_header("if-range", "\"v1\"")
                .with_status(206)
                .with_header("etag", "W/\"v2\"")
                .with_header("content-range", "bytes 4-5/6")
                .with_body("b\n")
                .expect(if changes_etag { attempts } else { 0 })
                .create_async()
                .await;
            let mut invalid = destination
                .mock("GET", PATH)
                .match_header("range", "bytes=3-")
                .with_status(status)
                .with_body(body)
                .with_header("etag", "\"v1\"")
                .expect(attempts);
            if let Some(header) = header {
                invalid = invalid.with_header("content-range", header);
            }
            let invalid = invalid.create_async().await;
            let adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    id_lists_url: Some(format!("{}/lists", manifest.url())),
                    download_id_list_file_api: use_proxy.then(|| proxy.url()),
                    fallback_to_statsig_api: Some(use_fallback),
                    ..StatsigOptions::default()
                },
            );
            let (adapter, _provider) = with_local_cdn(adapter, &origin);
            adapter.set_listener(listener.clone());
            let error = adapter.sync_id_lists().await.unwrap_err();
            if retryable {
                assert!(matches!(error, StatsigErr::NetworkError(_)));
            } else {
                assert!(matches!(error, StatsigErr::CustomError(_)));
            }
            invalid.assert_async().await;
            continuation.assert_async().await;
            assert_eq!(listener.id_lists.read()["list"].metadata.size, 3);
            assert_eq!(
                *listener.id_lists.read()["list"].ids,
                crate::id_lists_adapter::IdListIds::from([String::from("a")])
            );
            invalid.remove_async().await;
            let destination = if use_proxy && !use_fallback {
                &mut proxy
            } else {
                &mut origin
            };
            let recovered = destination
                .mock("GET", PATH)
                .match_header("range", "bytes=3-")
                .with_status(200)
                .with_body("+a\n+b\n")
                .expect(1)
                .create_async()
                .await;
            adapter.sync_id_lists().await.unwrap();
            assert_eq!(listener.id_lists.read()["list"].metadata.size, 6);
            assert!(listener.id_lists.read()["list"].ids.contains("b"));
            recovered.assert_async().await;
            proxy_request.assert_async().await;
            manifest_request.assert_async().await;
        }
    }
}

#[cfg(not(feature = "custom_network_provider"))]
async fn local_range_list(
    server: &mut Server,
    manifest_size: u64,
    initial_changes: Option<&str>,
    polls: usize,
) -> (
    StatsigHttpIdListsAdapter,
    Arc<TestIdListsUpdateListener>,
    mockito::Mock,
) {
    let metadata = IdListMetadata {
        name: "list".into(),
        url: format!("{}/file", server.url()),
        size: manifest_size,
        file_id: Some("file-1".into()),
        creation_time: 1,
    };
    let manifest = server
        .mock("POST", "/lists")
        .with_body(serde_json::to_string(&HashMap::from([("list", &metadata)])).unwrap())
        .expect(polls)
        .create_async()
        .await;
    let mut lists = HashMap::new();
    if let Some(changes) = initial_changes {
        let mut list = crate::id_lists_adapter::IdList::new(metadata.clone());
        list.apply_update(IdListUpdate {
            raw_changeset: Some(changes.into()),
            new_metadata: metadata,
        });
        lists.insert("list".into(), list);
    }
    let listener = Arc::new(TestIdListsUpdateListener {
        id_lists: RwLock::new(lists),
    });
    let adapter = StatsigHttpIdListsAdapter::new(
        "secret-key",
        &StatsigOptions {
            id_lists_url: Some(format!("{}/lists", server.url())),
            ..Default::default()
        },
    );
    adapter.set_listener(listener.clone());
    (adapter, listener, manifest)
}

#[tokio::test]
#[cfg(not(feature = "custom_network_provider"))]
async fn id_list_range_retries_stale_full_body_in_the_same_refresh() {
    use std::sync::atomic::{AtomicBool, Ordering};

    let mut server = Server::new_async().await;
    let (adapter, listener, manifest) = local_range_list(&mut server, 6, Some("+a\n"), 1).await;
    let stale = AtomicBool::new(true);
    let file = server
        .mock("GET", "/file")
        .match_header("range", "bytes=3-")
        .match_header("statsig-id-list-file-size", "6")
        .with_body_from_request(move |_| {
            if stale.swap(false, Ordering::SeqCst) {
                b"+a\n".to_vec()
            } else {
                b"+a\n+b\n".to_vec()
            }
        })
        .expect(2)
        .create_async()
        .await;

    adapter.sync_id_lists().await.unwrap();

    manifest.assert_async().await;
    file.assert_async().await;
    let lists = listener.id_lists.read();
    assert_eq!(lists["list"].metadata.size, 6);
    assert_eq!(
        *lists["list"].ids,
        crate::id_lists_adapter::IdListIds::from([String::from("a"), String::from("b")])
    );
}

#[tokio::test]
#[cfg(not(feature = "custom_network_provider"))]
async fn id_list_range_applies_only_complete_records_across_partial_responses() {
    const FILE: &[u8] = "+victim01\n-victim01\n+néw+d01\n+marker01".as_bytes();

    for (status, polls) in [
        (206, vec![vec![(0, FILE.len())]]),
        (
            206,
            vec![
                vec![(0, 15)],
                vec![(10, 12), (12, 15), (15, 25)],
                vec![(20, 25), (25, 28), (28, FILE.len())],
            ],
        ),
        (
            200,
            [0..10, 10..20, 20..30, 30..FILE.len()]
                .into_iter()
                .map(|poll| poll.map(|i| (i, i + 1)).collect())
                .collect(),
        ),
    ] {
        let mut server = Server::new_async().await;
        // A published object may be shorter than the latest manifest.
        let (adapter, listener, manifest) =
            local_range_list(&mut server, FILE.len() as u64 + 10, None, polls.len()).await;

        for responses in polls {
            let mut mocks = Vec::new();
            let end = responses.last().unwrap().1;
            for (start, end) in responses {
                mocks.push(
                    server
                        .mock("GET", "/file")
                        .match_header("range", format!("bytes={start}-").as_str())
                        .with_status(status)
                        .with_header(
                            "content-range",
                            &format!("bytes {start}-{}/{}", end - 1, FILE.len()),
                        )
                        .with_body(&FILE[start..end])
                        .expect(1)
                        .create_async()
                        .await,
                );
            }
            adapter.sync_id_lists().await.unwrap();
            let (cursor, members): (usize, &[&str]) = match end {
                10 | 15 => (10, &["victim01"]),
                20 | 25 => (20, &[]),
                30 => (30, &["néw+d01"]),
                _ => (FILE.len(), &["néw+d01", "marker01"]),
            };
            {
                let lists = listener.id_lists.read();
                assert_eq!(lists["list"].metadata.size, cursor as u64);
                assert_eq!(
                    *lists["list"].ids,
                    members.iter().copied().map(str::to_owned).collect()
                );
            }
            for response in mocks {
                response.assert_async().await;
            }
        }
        manifest.assert_async().await;
    }
}

#[test]
fn id_list_range_handles_representation_changes_during_a_record() {
    let pending = || PartialIdListRecord {
        bytes: b"+old".to_vec(),
        total: 16,
        etag: None,
    };
    // A body that shrank mid-record can no longer substantiate its saved prefix.
    assert!(matches!(
        normalize_response(206, Some("bytes 7-9/10"), 3, 16, "id\n", pending()),
        Err(StatsigErr::NetworkError(NetworkError::RequestFailed(
            _,
            Some(206),
            _
        )))
    ));

    // A server ignoring Range supplies the prefix again, including the in-flight bytes.
    assert_eq!(
        normalize_response(200, None, 3, 16, "+x\n+n", pending()).unwrap(),
        IdListDownload::Complete("+n".into(), 3..5)
    );
}

#[tokio::test(start_paused = true)]
async fn id_list_range_retries_changed_etag_with_mixed_case_headers() {
    use crate::networking::NetworkProvider;
    use parking_lot::Mutex;

    #[derive(Default)]
    struct Provider {
        ranges: Mutex<Vec<String>>,
    }

    #[async_trait]
    impl NetworkProvider for Provider {
        async fn send(&self, method: &HttpMethod, args: &RequestArgs) -> Response {
            if *method == HttpMethod::POST {
                let manifest = br#"{"list": {
                    "name":"list", "url":"https://files.test/file",
                    "size":5, "fileID":"file-1", "creationTime":1
                }}"#;
                return Response {
                    status_code: Some(200),
                    data: Some(ResponseData::from_bytes(manifest.to_vec())),
                    error: None,
                };
            }
            let headers = args.headers.as_ref().unwrap();
            let range = &headers["Range"];
            self.ranges.lock().push(range.clone());
            let (content_range, etag, body) = match range.as_str() {
                "bytes=0-" => {
                    assert!(!headers.contains_key("If-Range"));
                    ("bytes 0-2/5", "\"v1\"", "+ab")
                }
                "bytes=3-" => {
                    assert_eq!(headers["If-Range"], "\"v1\"");
                    ("bytes 3-4/5", "\"V1\"", "z\n")
                }
                _ => panic!("unexpected range {range}"),
            };
            let headers = HashMap::from([
                ("Content-Range".into(), content_range.into()),
                ("ETag".into(), etag.into()),
            ]);
            Response {
                status_code: Some(206),
                data: Some(ResponseData::from_bytes_with_headers(
                    body.into(),
                    Some(headers),
                )),
                error: None,
            }
        }
    }

    let provider = Arc::new(Provider::default());
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    let mut adapter = StatsigHttpIdListsAdapter::new(
        "secret-range-test",
        &StatsigOptions {
            id_lists_url: Some("https://manifest.test/lists".into()),
            state_read_primary_attempts: Some(2),
            ..Default::default()
        },
    );
    adapter
        .network
        .set_network_provider_for_test(Arc::downgrade(&network_provider));
    let listener = Arc::new(TestIdListsUpdateListener {
        id_lists: RwLock::new(HashMap::new()),
    });
    adapter.set_listener(listener.clone());

    let error = adapter.sync_id_lists().await.unwrap_err();
    assert!(retryable_state_error(&error));
    assert_eq!(
        *provider.ranges.lock(),
        ["bytes=0-", "bytes=3-", "bytes=0-", "bytes=3-"]
    );
    assert!(listener.id_lists.read().is_empty());
}

#[tokio::test]
#[cfg(not(feature = "custom_network_provider"))]
async fn id_list_range_limits_continuations_without_publishing() {
    use std::sync::atomic::{AtomicU64, Ordering};

    let mut server = Server::new_async().await;
    let (adapter, listener, manifest) = local_range_list(&mut server, 100, Some("+a\n"), 1).await;

    // Return successive one-byte intervals. Going past the cap would eventually reach EOF.
    let next = AtomicU64::new(3);
    let file = server
        .mock("GET", "/file")
        .match_header("if-range", mockito::Matcher::Missing)
        .with_status(206)
        .with_header("etag", "W/\"v1\"")
        .with_header_from_request("content-range", move |_| {
            let start = next.fetch_add(1, Ordering::Relaxed);
            format!("bytes {start}-{start}/100")
        })
        .with_body("+")
        .expect(65)
        .create_async()
        .await;
    let result = adapter.sync_id_lists().await;
    assert!(
        matches!(result, Err(StatsigErr::CustomError(msg)) if msg.contains("Too many partial responses"))
    );
    manifest.assert_async().await;
    file.assert_async().await;
    let lists = listener.id_lists.read();
    assert_eq!(lists["list"].metadata.size, 3);
    assert_eq!(
        *lists["list"].ids,
        crate::id_lists_adapter::IdListIds::from(["a".to_owned()])
    );
}

#[test]
fn id_list_range_limits_unfinished_record_bytes() {
    let IdListDownload::Incomplete(record) = normalize_response(
        206,
        Some("bytes 0-65535/70000"),
        0,
        70000,
        vec![b'+'; 65536],
        Default::default(),
    )
    .unwrap() else {
        panic!("64 KiB should fit")
    };
    assert_eq!(record.bytes.len(), 65536);
    let next = normalize_response(
        206,
        Some("bytes 65536-65536/70000"),
        0,
        70000,
        vec![b'+'],
        record,
    );
    assert!(matches!(next, Err(StatsigErr::CustomError(msg)) if msg.contains("too large")));
}
