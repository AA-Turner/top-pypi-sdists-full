use super::{HTTP2_CAPABILITY_TTL, NetworkProviderReqwest};
use crate::StatsigOptions;
use crate::networking::__tests__::http2_test_helpers::isolated_http2_test;
use crate::networking::proxy_config::ProxyConfig;
use crate::networking::{HttpMethod, NetworkClient, NetworkError, NetworkProvider, RequestArgs};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::{Duration, Instant};
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

isolated_http2_test! {
async fn http2_body_deadline_preserves_terminal_status_and_retry_classification() {
    use std::sync::atomic::{AtomicUsize, Ordering};
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    use tokio::net::TcpListener;
    use tokio::task::JoinSet;

    let mut outcomes = Vec::new();
    for (limited, retries) in [(false, 0), (false, 1), (true, 1)] {
        let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
        let url = format!("http://{}/stalled-body", listener.local_addr().unwrap());
        let requests = Arc::new(AtomicUsize::new(0));
        let received = requests.clone();
        let receiver = tokio::spawn(async move {
            let (mut probe, _) = listener.accept().await.unwrap();
            let mut discovery = [0; 33];
            probe.read_exact(&mut discovery).await.unwrap();
            assert_eq!(&discovery[..24], b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n");
            // Let the SDK's bounded discovery expire. The payload's own timeout
            // now ends later than the shared attempt deadline, without a test sleep.
            assert_eq!(probe.read(&mut [0; 1]).await.unwrap(), 0);
            let mut handlers = JoinSet::new();
            loop {
                tokio::select! {
                    accepted = listener.accept() => {
                        let (mut socket, _) = accepted.unwrap();
                        let received = received.clone();
                        handlers.spawn(async move {
                            let mut headers = Vec::new();
                            while !headers.ends_with(b"\r\n\r\n") {
                                headers.push(socket.read_u8().await.unwrap());
                            }
                            let expected = if limited { b"GET ".as_slice() } else { b"POST " };
                            assert!(headers.starts_with(expected));
                            if !limited {
                                let mut body = [0; 6];
                                socket.read_exact(&mut body).await.unwrap();
                                assert_eq!(&body, b"events");
                            }
                            received.fetch_add(1, Ordering::SeqCst);
                            socket.write_all(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 8\r\n\r\n")
                                .await.unwrap();
                            // Keep the declared response body incomplete until cancellation.
                            let _ = socket.read(&mut [0; 1]).await;
                        });
                    }
                    completed = handlers.join_next(), if !handlers.is_empty() => {
                        completed.unwrap().unwrap();
                    }
                }
            }
        });
        let provider: Arc<dyn NetworkProvider> = Arc::new(NetworkProviderReqwest::new());
        let mut client = NetworkClient::new("secret-test", None, None).mute_network_error_log();
        client.set_network_provider_for_test(Arc::downgrade(&provider));
        let args = RequestArgs {
            url,
            retries,
            timeout_ms: 200,
            disable_file_streaming: Some(true),
            ..RequestArgs::new()
        };
        let result = tokio::time::timeout(Duration::from_secs(2), async {
            if limited {
                client.get_with_response_limit(args, 16).await
            } else {
                client.post(args, Some(b"events".to_vec())).await
            }
        }).await.expect("request must remain bounded");
        let error = match result {
            Err(error) => error,
            Ok(_) => panic!("terminal 400 must fail"),
        };
        outcomes.push((limited, retries, requests.load(Ordering::SeqCst), error));
        receiver.abort();
        assert!(receiver.await.unwrap_err().is_cancelled());
    }
    assert!(outcomes.iter().all(|(_, _, requests, error)| {
        *requests == 1 && matches!(error, NetworkError::RequestNotRetryable(_, Some(400), message)
            if message == "HTTP request timed out")
    }), "(limited, retries, request count, error): {outcomes:?}");
}
}

isolated_http2_test! {
async fn http2_limited_body_deadline_retains_received_status() {
    let mut server = mockito::Server::new_async().await;
    let mock = server.mock("GET", "/stalled-body")
        .with_status(400)
        .with_chunked_body(|writer| {
            writer.write_all(b"x")?;
            std::thread::sleep(Duration::from_millis(500));
            writer.write_all(b"end")
        })
        .expect(1)
        .create_async().await;
    let provider = NetworkProviderReqwest::new();
    let (response, exceeded, unsupported) = provider.send_http2_preferred(
        &HttpMethod::GET,
        &RequestArgs {
            url: format!("{}/stalled-body", server.url()),
            timeout_ms: 200,
            log_event_connection_reuse: true,
            disable_file_streaming: Some(true),
            ..RequestArgs::new()
        },
        Some(16),
        false,
    ).await.into_parts();
    assert_eq!(response.status_code, Some(400), "{:?}", response.error);
    assert!(response.error.is_some());
    assert!(response.data.is_none());
    assert!(!exceeded && !unsupported);
    assert_eq!(provider.http2_clients.lock().entries.len(), 1);
    mock.assert_async().await;
}
}

isolated_http2_test! {
async fn http2_default_uses_prior_knowledge_and_reuses_connection() {
    use std::sync::atomic::{AtomicUsize, Ordering};
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    use tokio::net::{TcpListener, TcpStream};
    use tokio::task::JoinSet;

    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .respond_with(ResponseTemplate::new(200).set_body_bytes(b"{}"))
        .expect(5)
        .mount(&server)
        .await;

    // Observe the wire preface, then relay to the existing H1/H2 test server.
    let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
    let origin = format!("http://{}", listener.local_addr().unwrap());
    let upstream_addr = *server.address();
    let connections = Arc::new(AtomicUsize::new(0));
    let relay_connections = connections.clone();
    let relay = tokio::spawn(async move {
        let (mut probe, _) = listener.accept().await.unwrap();
        let mut discovery = [0; 33];
        probe.read_exact(&mut discovery).await.unwrap();
        assert_eq!(&discovery[..24], b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n");
        probe.write_all(b"\0\0\0\x04\0\0\0\0\0").await.unwrap();
        drop(probe);
        let mut relays = JoinSet::new();
        loop {
            let (mut downstream, _) = listener.accept().await.unwrap();
            let connections = relay_connections.clone();
            relays.spawn(async move {
                let mut preface = [0_u8; 24];
                downstream.read_exact(&mut preface).await.unwrap();
                assert_eq!(&preface, b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n");
                connections.fetch_add(1, Ordering::SeqCst);
                let mut upstream = TcpStream::connect(upstream_addr).await.unwrap();
                upstream.write_all(&preface).await.unwrap();
                let _ = tokio::io::copy_bidirectional(&mut downstream, &mut upstream).await;
            });
        }
    });
    let provider = Arc::new(NetworkProviderReqwest::new());
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    let args = RequestArgs {
        url: format!("{origin}/v2/download_config_specs"),
        timeout_ms: 2000,
        disable_file_streaming: Some(true),
        ..RequestArgs::new()
    };
    for (reuse, expected_connections) in [
        (None, 1),
        (Some(false), 2),
        (Some(false), 3),
        (Some(true), 3),
        (None, 3),
    ] {
        let options = reuse.map(|enabled| StatsigOptions {
            log_event_connection_reuse: Some(enabled),
            ..Default::default()
        });
        let mut client = NetworkClient::new("secret-test", None, options.as_ref());
        client.set_network_provider_for_test(Arc::downgrade(&network_provider));
        let mut response = client.get(args.clone()).await.unwrap();
        assert_eq!(response.status_code, Some(200));
        assert!(response.error.is_none());
        assert_eq!(
            response.data.as_mut().unwrap().read_to_string().unwrap(),
            "{}"
        );
        assert_eq!(connections.load(Ordering::SeqCst), expected_connections);
    }
    assert_eq!(provider.http2_clients.lock().entries.len(), 1);
    server.verify().await;
    relay.abort();
    assert!(relay.await.unwrap_err().is_cancelled());
}
}

#[test]
fn http2_client_cache_respects_connection_reuse_for_all_routes() {
    for route in [
        "/v1/log_event",
        "/v2/download_config_specs/secret-test.json",
        "/v1/get_id_lists/secret-test.json",
        "/v1/download_id_list_file/file",
        "/v1/sdk_exception",
        "/custom/log_event",
        "/custom/id-list-file",
        "/custom/blob",
    ] {
        let provider = NetworkProviderReqwest::new();
        let mut args = RequestArgs {
            url: format!("http://localhost{route}"),
            log_event_connection_reuse: false,
            ..RequestArgs::new()
        };
        provider.get_http2_client(&args, true).unwrap();
        assert!(provider.http2_clients.lock().entries.is_empty(), "{route}");
        args.log_event_connection_reuse = true;
        provider.get_http2_client(&args, true).unwrap();
        assert_eq!(provider.http2_clients.lock().entries.len(), 1, "{route}");
    }
}

isolated_http2_test! {
async fn http2_default_falls_back_before_post_and_explicit_opt_out_uses_http1() {
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    use tokio::net::TcpListener;

    for http2 in [false, true] {
        let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
        let origin = format!("http://{}", listener.local_addr().unwrap());
        let receiver = tokio::spawn(async move {
            if http2 {
                let (mut probe, _) = listener.accept().await.unwrap();
                let mut discovery = [0; 33];
                probe.read_exact(&mut discovery).await.unwrap();
                assert_eq!(&discovery[..24], b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n");
                probe
                    .write_all(b"HTTP/1.1 400 Bad Request\r\nContent-Length:0\r\n\r\n")
                    .await
                    .unwrap();
            }
            let (mut socket, _) = listener.accept().await.unwrap();
            let mut bytes = [0_u8; 24];
            socket.read_exact(&mut bytes).await.unwrap();
            let mut headers = bytes.to_vec();
            while !headers.ends_with(b"\r\n\r\n") {
                headers.push(socket.read_u8().await.unwrap());
            }
            assert!(headers.starts_with(b"POST /v1/log_event HTTP/1.1\r\n"));
            let mut body = [0; 6];
            socket.read_exact(&mut body).await.unwrap();
            assert_eq!(&body, b"events");
            socket
                .write_all(
                    b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\n{}",
                )
                .await
                .unwrap();
            drop(socket);
            if http2 {
                assert!(
                    tokio::time::timeout(Duration::from_millis(200), listener.accept())
                        .await
                        .is_err()
                );
            }
            bytes
        });
        let provider = Arc::new(NetworkProviderReqwest::new());
        let network_provider: Arc<dyn NetworkProvider> = provider.clone();
        let options = (!http2).then(|| StatsigOptions {
            prefer_http2: Some(false),
            ..Default::default()
        });
        let mut client = NetworkClient::new("secret-test", None, options.as_ref());
        client.set_network_provider_for_test(Arc::downgrade(&network_provider));
        let args = RequestArgs {
            url: format!("{origin}/v1/log_event"),
            timeout_ms: 2000,
            disable_file_streaming: Some(true),
            ..RequestArgs::new()
        };
        let response = client.post(args, Some(b"events".to_vec())).await.unwrap();
        let preface = receiver.await.unwrap();
        assert!(preface.starts_with(b"POST /v1/log_event"));
        assert_eq!(response.status_code, Some(200));
        assert!(response.error.is_none());
        assert!(provider.http2_clients.lock().entries.is_empty());
    }
}
}

isolated_http2_test! {
async fn http2_respects_shutdown_and_does_not_replay_a_timed_out_post() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/v1/log_event"))
        .respond_with(ResponseTemplate::new(200))
        .expect(1)
        .mount(&server)
        .await;
    Mock::given(method("POST"))
        .and(path("/v1/log_event"))
        .and(wiremock::matchers::body_bytes(b"events"))
        .respond_with(ResponseTemplate::new(200).set_delay(Duration::from_secs(1)))
        .expect(1)
        .mount(&server)
        .await;
    let provider = NetworkProviderReqwest::new();
    let origin = server.uri();
    let mut args = RequestArgs {
        url: format!("{origin}/v1/log_event"),
        body: Some(b"events".to_vec()),
        timeout_ms: 250,
        disable_file_streaming: Some(true),
        log_event_connection_reuse: true,
        is_shutdown: Some(std::sync::Arc::new(std::sync::atomic::AtomicBool::new(
            true,
        ))),
        ..RequestArgs::new()
    };
    let cancelled = provider
        .send_http2_preferred(&HttpMethod::POST, &args, None, false)
        .await
        .into_parts()
        .0;
    assert_eq!(cancelled.error.as_deref(), Some("Request was shutdown"));
    assert!(provider.http2_clients.lock().entries.is_empty());
    assert!(server.received_requests().await.unwrap().is_empty());

    // Exclude cold discovery and connection setup from the POST timeout check.
    let ready = provider
        .send_http2_preferred(
            &HttpMethod::GET,
            &RequestArgs {
                body: None,
                timeout_ms: 2000,
                is_shutdown: None,
                ..args.clone()
            },
            None,
            false,
        )
        .await
        .into_parts()
        .0;
    assert_eq!(ready.status_code, Some(200));
    assert!(ready.error.is_none());
    assert_eq!(provider.http2_clients.lock().entries.len(), 1);

    args.is_shutdown = None;
    let timed_out = provider
        .send_http2_preferred(&HttpMethod::POST, &args, None, false)
        .await
        .into_parts()
        .0;
    assert!(timed_out.error.is_some());
    assert_eq!(timed_out.status_code, None);
    assert_eq!(provider.http2_clients.lock().entries.len(), 1);
    server.verify().await;
}
}

isolated_http2_test! {
async fn http2_preserves_redirect_policy_in_separate_client_pools() {
    let source = MockServer::start().await;
    let target = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/v2/download_config_specs"))
        .respond_with(
            ResponseTemplate::new(302)
                .insert_header("location", format!("{}/escaped", target.uri())),
        )
        .expect(2)
        .mount(&source)
        .await;
    Mock::given(method("GET"))
        .and(path("/escaped"))
        .respond_with(ResponseTemplate::new(200))
        .expect(1)
        .mount(&target)
        .await;

    let provider = NetworkProviderReqwest::new();
    let origin = source.uri();
    for disable_redirects in [true, false] {
        let response = provider
            .send_http2_preferred(
                &HttpMethod::GET,
                &RequestArgs {
                    url: format!("{origin}/v2/download_config_specs"),
                    disable_file_streaming: Some(true),
                    log_event_connection_reuse: true,
                    ..RequestArgs::new()
                },
                None,
                disable_redirects,
            )
            .await
            .into_parts()
            .0;

        assert_eq!(
            response.status_code,
            Some(if disable_redirects { 302 } else { 200 })
        );
    }
    assert_eq!(provider.http2_clients.lock().entries.len(), 1);
    source.verify().await;
    target.verify().await;
}
}

#[tokio::test]
async fn http2_invalid_ca_fails_without_default_client_fallback() {
    let provider = NetworkProviderReqwest::new();
    let result = provider.get_http2_client(
        &RequestArgs {
            url: "https://receiver.invalid/any-path".into(),
            ca_cert_pem: Some(b"invalid certificate".to_vec()),
            ..RequestArgs::new()
        },
        true,
    );
    assert!(result.is_err());
    assert!(provider.http2_clients.lock().entries.is_empty());
}

isolated_http2_test! {
async fn http2_redirect_to_http1_preserves_post_rules_and_strips_cross_origin_auth() {
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    for status in [302, 307] {
        let target = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let destination = format!("http://{}/next?token=opaque", target.local_addr().unwrap());
        let receiver = tokio::spawn(async move {
            let (mut socket, _) = target.accept().await.unwrap();
            let mut headers = Vec::new();
            while !headers.ends_with(b"\r\n\r\n") {
                headers.push(socket.read_u8().await.unwrap());
            }
            let headers = String::from_utf8(headers).unwrap().to_ascii_lowercase();
            assert!(!headers.contains("authorization:"));
            assert!(!headers.contains("cookie:"));
            assert!(headers.contains("statsig-api-key: secret-test"));
            if status == 302 {
                assert!(headers.starts_with("get /next?token=opaque http/1.1\r\n"));
                assert!(!headers.contains("content-type:"));
                assert!(!headers.contains("content-length:"));
            } else {
                assert!(headers.starts_with("post /next?token=opaque http/1.1\r\n"));
                assert!(headers.contains("content-type: application/json"));
                let mut body = [0; 6];
                socket.read_exact(&mut body).await.unwrap();
                assert_eq!(&body, b"events");
            }
            socket
                .write_all(b"HTTP/1.1 200 OK\r\nContent-Length:2\r\nConnection:close\r\n\r\n{}")
                .await
                .unwrap();
        });
        let source = MockServer::start().await;
        Mock::given(method("POST"))
            .and(path("/event"))
            .and(wiremock::matchers::body_bytes(b"events"))
            .respond_with(ResponseTemplate::new(status).insert_header("location", destination))
            .expect(1)
            .mount(&source)
            .await;
        let provider = NetworkProviderReqwest::new();
        let response = provider
            .send_http2_preferred(
                &HttpMethod::POST,
                &RequestArgs {
                    url: format!("{}/event", source.uri()),
                    body: Some(b"events".to_vec()),
                    headers: Some(HashMap::from([
                        ("authorization".into(), "Bearer test".into()),
                        ("cookie".into(), "session=test".into()),
                        ("statsig-api-key".into(), "secret-test".into()),
                        ("content-type".into(), "application/json".into()),
                    ])),
                    timeout_ms: 1000,
                    log_event_connection_reuse: true,
                    ..RequestArgs::new()
                },
                None,
                false,
            )
            .await
            .into_parts()
            .0;
        assert_eq!(response.status_code, Some(200), "{:?}", response.error);
        assert_eq!(provider.http2_clients.lock().entries.len(), 1);
        receiver.await.unwrap();
        source.verify().await;
    }
}
}

isolated_http2_test! {
async fn plaintext_discovery_is_coalesced_cached_and_expires() {
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    assert_eq!(
        super::plaintext_probe_host(&url::Url::parse("http://[::1]:8000/path").unwrap()),
        Some("::1")
    );
    let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
    let origin = format!("http://{}", listener.local_addr().unwrap());
    let receiver = tokio::spawn(async move {
        let (mut socket, _) = listener.accept().await.unwrap();
        let mut discovery = [0; 33];
        socket.read_exact(&mut discovery).await.unwrap();
        assert_eq!(&discovery[..24], b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n");
        socket.write_all(b"\0\0\0\x04\0\0\0\0\0").await.unwrap();
    });
    let provider = NetworkProviderReqwest::new();
    let args = RequestArgs {
        url: format!("{origin}/unused"),
        ..RequestArgs::new()
    };
    let results = futures::future::join_all(
        (0..16).map(|_| provider.plaintext_http2_available(&args, Duration::from_secs(1))),
    )
    .await;
    assert!(results.into_iter().all(|supports| supports));
    receiver.await.unwrap();
    assert!(
        provider
            .plaintext_http2_available(&args, Duration::from_secs(1))
            .await
    );
    provider.http2_origins.lock().get_mut(&origin).unwrap().0 =
        Instant::now() - HTTP2_CAPABILITY_TTL;
    assert!(
        !provider
            .plaintext_http2_available(&args, Duration::from_secs(1))
            .await
    );
    assert_eq!(provider.http2_origins.lock().len(), 1);
}
}

isolated_http2_test! {
async fn http2_all_receivers_and_request_types_preserve_headers_and_bodies() {
    let provider = NetworkProviderReqwest::new();
    for _ in 0..2 {
        let server = MockServer::start().await;
        for (verb, route) in [
            (HttpMethod::GET, "/v2/download_config_specs"),
            (HttpMethod::POST, "/v1/get_id_lists"),
            (HttpMethod::GET, "/v1/download_id_list_file/file"),
            (HttpMethod::POST, "/v1/log_event"),
            (HttpMethod::POST, "/v1/sdk_exception"),
            (HttpMethod::GET, "/custom/blob"),
        ] {
            let method_name = if verb == HttpMethod::GET {
                "GET"
            } else {
                "POST"
            };
            Mock::given(method(method_name))
                .and(path(route))
                .and(wiremock::matchers::query_param("token", "opaque"))
                .and(wiremock::matchers::header("statsig-api-key", "secret-test"))
                .and(wiremock::matchers::header("range", "bytes=3-"))
                .and(wiremock::matchers::body_bytes(
                    if verb == HttpMethod::POST {
                        b"test-payload".as_slice()
                    } else {
                        b""
                    },
                ))
                .respond_with(ResponseTemplate::new(200).set_body_bytes(b"ok"))
                .expect(1)
                .mount(&server)
                .await;
            let response = provider
                .send_http2_preferred(
                    &verb,
                    &RequestArgs {
                        url: format!("{}{route}?token=opaque", server.uri()),
                        headers: Some(HashMap::from([
                            ("statsig-api-key".into(), "secret-test".into()),
                            ("range".into(), "bytes=3-".into()),
                        ])),
                        body: Some(b"test-payload".to_vec()),
                        timeout_ms: 1000,
                        disable_file_streaming: Some(true),
                        ..RequestArgs::new()
                    },
                    None,
                    false,
                )
                .await
                .into_parts()
                .0;
            assert_eq!(
                response.status_code,
                Some(200),
                "{route}: {:?}",
                response.error
            );
        }
        server.verify().await;
    }
}
}

isolated_http2_test! {
async fn http2_limited_requests_enforce_byte_caps_and_do_not_follow_redirects() {
    let server = MockServer::start().await;
    Mock::given(path("/large"))
        .respond_with(ResponseTemplate::new(200).set_body_bytes(b"12345"))
        .expect(2)
        .mount(&server)
        .await;
    Mock::given(path("/small"))
        .respond_with(ResponseTemplate::new(200).set_body_bytes(b"1234"))
        .expect(2)
        .mount(&server)
        .await;
    Mock::given(path("/redirect"))
        .respond_with(
            ResponseTemplate::new(302)
                .insert_header("location", format!("{}/escaped", server.uri())),
        )
        .expect(2)
        .mount(&server)
        .await;
    Mock::given(path("/escaped"))
        .respond_with(ResponseTemplate::new(200))
        .expect(0)
        .mount(&server)
        .await;
    let provider = NetworkProviderReqwest::new();
    for disable_file_streaming in [false, true] {
        for route in ["/large", "/small", "/redirect"] {
            let result = provider
                .send_http2_preferred(
                    &HttpMethod::GET,
                    &RequestArgs {
                        url: format!("{}{route}", server.uri()),
                        timeout_ms: 1000,
                        disable_file_streaming: Some(disable_file_streaming),
                        ..RequestArgs::new()
                    },
                    Some(4),
                    false,
                )
                .await;
            let (response, exceeded, unsupported) = result.into_parts();
            assert!(!unsupported);
            assert_eq!(exceeded, route == "/large");
            assert_eq!(
                response.status_code,
                Some(if route == "/redirect" { 302 } else { 200 })
            );
            if exceeded {
                assert!(response.data.is_none());
            } else {
                assert!(response.error.is_none());
            }
        }
    }
    server.verify().await;
}
}

isolated_http2_test! {
async fn http2_honors_explicit_proxy_without_origin_allowlist() {
    let proxy = MockServer::start().await;
    Mock::given(method("POST"))
        .and(path("/v1/log_event"))
        .and(wiremock::matchers::body_bytes(b"events"))
        .respond_with(ResponseTemplate::new(200))
        .expect(1)
        .mount(&proxy)
        .await;
    let provider = NetworkProviderReqwest::new();
    let result = provider
        .send_http2_preferred(
            &HttpMethod::POST,
            &RequestArgs {
                url: "http://receiver.invalid/v1/log_event".into(),
                proxy_config: Some(ProxyConfig {
                    proxy_host: Some("127.0.0.1".into()),
                    proxy_port: Some(proxy.address().port()),
                    proxy_protocol: Some("http".into()),
                    proxy_auth: None,
                    ca_cert_path: None,
                }),
                body: Some(b"events".to_vec()),
                timeout_ms: 1000,
                ..RequestArgs::new()
            },
            None,
            false,
        )
        .await
        .into_parts()
        .0;
    assert_eq!(result.status_code, Some(200), "{:?}", result.error);
    proxy.verify().await;
}
}
