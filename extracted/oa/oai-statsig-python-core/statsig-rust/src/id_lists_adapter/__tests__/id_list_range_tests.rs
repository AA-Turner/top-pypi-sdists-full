#[cfg(not(feature = "custom_network_provider"))]
use super::tests::{TestIdListsUpdateListener, with_local_cdn};
use super::*;
#[cfg(not(feature = "custom_network_provider"))]
use mockito::Server;

#[cfg(not(feature = "custom_network_provider"))]
const CDN_FILE: &str = "https://statsigcdn.openai.com/v1/download_id_list_file/company%2Fids?private=true&range=0-&token=a%2Bb&Range=10-";
#[cfg(not(feature = "custom_network_provider"))]
// The server sees the encoded path and token, with both legacy range parameters removed.
const PATH: &str = "/v1/download_id_list_file/company%2Fids?private=true&token=a%2Bb";

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
            normalize_id_list_download(Some(status), range, start, size, body.into()).is_err(),
            "accepted {status} {range:?} at {start} for size {size}"
        );
    }
}

#[test]
fn id_list_range_distinguishes_stale_full_body_responses() {
    for (start, size, body) in [(3, 6, "+a\n"), (0, 3, ""), (9, 6, "+a\n+b\n")] {
        assert_eq!(
            normalize_id_list_download(Some(200), None, start, size, body.into()),
            Ok(None)
        );
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
        let (delta, range) =
            normalize_id_list_download(Some(status), header, start, size, body.into())
                .unwrap()
                .unwrap();
        assert_eq!(delta, expected);
        assert_eq!(range, start..end);
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
            let retryable = status == 416 || (status == 200 && header.is_none());
            let mut invalid = destination
                .mock("GET", PATH)
                .match_header("range", "bytes=3-")
                .with_status(status)
                .with_body(body)
                .expect(if retryable && !use_fallback { 2 } else { 1 });
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

#[tokio::test]
#[cfg(not(feature = "custom_network_provider"))]
async fn id_list_range_retries_stale_full_body_in_the_same_refresh() {
    use std::sync::atomic::{AtomicBool, Ordering};

    let mut server = Server::new_async().await;
    let metadata = IdListMetadata {
        name: "list".into(),
        url: format!("{}/file", server.url()),
        size: 6,
        file_id: Some("file-1".into()),
        creation_time: 1,
    };
    let mut list = crate::id_lists_adapter::IdList::new(metadata.clone());
    list.apply_update(IdListUpdate {
        raw_changeset: Some("+a\n".into()),
        new_metadata: metadata.clone(),
    });
    let listener = Arc::new(TestIdListsUpdateListener {
        id_lists: RwLock::new(HashMap::from([("list".into(), list)])),
    });
    let manifest = server
        .mock("POST", "/lists")
        .with_body(serde_json::to_string(&HashMap::from([("list", metadata)])).unwrap())
        .expect(1)
        .create_async()
        .await;
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
    let adapter = StatsigHttpIdListsAdapter::new(
        "secret-key",
        &StatsigOptions {
            id_lists_url: Some(format!("{}/lists", server.url())),
            ..Default::default()
        },
    );
    adapter.set_listener(listener.clone());

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
