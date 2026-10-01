use super::NetworkClient;
#[cfg(not(feature = "custom_network_provider"))]
use super::{STATUS_CODE_TAG, latency_tests::take_network_latencies};
use crate::StatsigOptions;
#[cfg(not(feature = "custom_network_provider"))]
use crate::networking::__tests__::http2_test_helpers::isolated_http2_test;
#[cfg(not(feature = "custom_network_provider"))]
use crate::networking::NetworkError;
use crate::networking::proxy_config::ProxyConfig;
use crate::networking::{
    HttpMethod, NetworkProvider, RequestArgs, Response, ResponseData, ResponseLimitOutcome,
};
#[cfg(not(feature = "custom_network_provider"))]
use crate::observability::ops_stats::OpsStatsForInstance;
use async_trait::async_trait;
use std::sync::{
    Arc,
    atomic::{AtomicUsize, Ordering},
};

struct RoutingProvider {
    normal_calls: AtomicUsize,
    http2_calls: AtomicUsize,
    http2_policies: std::sync::Mutex<Vec<(Option<u64>, bool)>>,
}

struct DefaultOnlyProvider {
    normal_calls: AtomicUsize,
}

fn success_response() -> Response {
    Response {
        status_code: Some(200),
        data: Some(ResponseData::from_bytes(b"{}".to_vec())),
        error: None,
    }
}

#[async_trait]
impl NetworkProvider for RoutingProvider {
    async fn send(&self, _method: &HttpMethod, _args: &RequestArgs) -> Response {
        self.normal_calls.fetch_add(1, Ordering::SeqCst);
        success_response()
    }

    async fn send_http2_preferred(
        &self,
        _method: &HttpMethod,
        _args: &RequestArgs,
        max_response_bytes: Option<u64>,
        disable_redirects: bool,
    ) -> ResponseLimitOutcome {
        self.http2_calls.fetch_add(1, Ordering::SeqCst);
        self.http2_policies
            .lock()
            .unwrap()
            .push((max_response_bytes, disable_redirects));
        ResponseLimitOutcome::Response(success_response())
    }
}

#[async_trait]
impl NetworkProvider for DefaultOnlyProvider {
    async fn send(&self, _method: &HttpMethod, _args: &RequestArgs) -> Response {
        self.normal_calls.fetch_add(1, Ordering::SeqCst);
        success_response()
    }
}

fn http2_options(enabled: bool) -> StatsigOptions {
    StatsigOptions {
        prefer_http2: Some(enabled),
        ..StatsigOptions::default()
    }
}

#[tokio::test]
async fn http2_is_default_on_and_scoped_per_client() {
    let provider = Arc::new(RoutingProvider {
        normal_calls: AtomicUsize::new(0),
        http2_calls: AtomicUsize::new(0),
        http2_policies: Default::default(),
    });
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    for options in [
        None,
        Some(StatsigOptions::default()),
        Some(http2_options(false)),
        Some(http2_options(true)),
        Some(http2_options(false)),
        None,
    ] {
        let mut client = NetworkClient::new("secret-test", None, options.as_ref());
        client.net_provider = Arc::downgrade(&network_provider);
        client
            .get(RequestArgs {
                url: "http://regular:8080/v2/download_config_specs".to_string(),
                ..RequestArgs::new()
            })
            .await
            .unwrap();
    }
    assert_eq!(provider.normal_calls.load(Ordering::SeqCst), 2);
    assert_eq!(provider.http2_calls.load(Ordering::SeqCst), 4);
}

#[tokio::test]
async fn http2_selects_all_request_kinds_origins_and_schemes() {
    let provider = Arc::new(RoutingProvider {
        normal_calls: AtomicUsize::new(0),
        http2_calls: AtomicUsize::new(0),
        http2_policies: Default::default(),
    });
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    let mut client = NetworkClient::new("secret-test", None, Some(&http2_options(true)));
    client.net_provider = Arc::downgrade(&network_provider);
    for url in [
        "https://cdn/another/path?token=opaque",
        "http://cdn/v2/download_config_specs",
        "http://regular:8080/v1/log_event",
        "http://regular:8080/v1/dynamic_config_value/blob",
    ] {
        client
            .get(RequestArgs {
                url: url.to_string(),
                ..RequestArgs::new()
            })
            .await
            .unwrap();
    }
    client
        .get(RequestArgs {
            url: "http://regular:8080/v2/download_config_specs".to_string(),
            ..RequestArgs::new()
        })
        .await
        .unwrap();
    client
        .post(
            RequestArgs {
                url: "http://regular:8080/v1/log_event".to_string(),
                ..RequestArgs::new()
            },
            None,
        )
        .await
        .unwrap();
    client
        .post(
            RequestArgs {
                url: "http://regular:8080/v1/get_id_lists".to_string(),
                ..RequestArgs::new()
            },
            None,
        )
        .await
        .unwrap();
    client
        .get(RequestArgs {
            url: "http://regular:8080/v1/download_id_list_file/file?token=opaque".to_string(),
            ..RequestArgs::new()
        })
        .await
        .unwrap();
    client
        .get_with_response_limit(
            RequestArgs {
                url: "https://blob-receiver/value".to_string(),
                ..RequestArgs::new()
            },
            32,
        )
        .await
        .unwrap();
    client
        .get_without_redirects(RequestArgs {
            url: "https://fallback-receiver/list".to_string(),
            ..RequestArgs::new()
        })
        .await
        .unwrap();
    assert_eq!(provider.normal_calls.load(Ordering::SeqCst), 0);
    assert_eq!(provider.http2_calls.load(Ordering::SeqCst), 10);
    let policies = provider.http2_policies.lock().unwrap();
    assert_eq!(policies[8], (Some(32), false));
    assert_eq!(policies[9], (None, true));
}

#[tokio::test]
async fn http2_forwards_proxy_and_ca_to_provider() {
    let provider = Arc::new(RoutingProvider {
        normal_calls: AtomicUsize::new(0),
        http2_calls: AtomicUsize::new(0),
        http2_policies: Default::default(),
    });
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    for use_proxy in [false, true] {
        let mut options = http2_options(true);
        if use_proxy {
            options.proxy_config = Some(ProxyConfig {
                proxy_host: Some("127.0.0.1".to_string()),
                proxy_port: Some(8081),
                proxy_auth: None,
                proxy_protocol: Some("http".to_string()),
                ca_cert_path: None,
            });
        }
        let mut client = NetworkClient::new("secret-test", None, Some(&options));
        client.net_provider = Arc::downgrade(&network_provider);
        let result = client
            .get(RequestArgs {
                url: "http://regular:8080/v2/download_config_specs".to_string(),
                ca_cert_pem: (!use_proxy).then(Vec::new),
                retries: 3,
                ..RequestArgs::new()
            })
            .await;
        assert!(result.is_ok());
    }
    assert_eq!(provider.normal_calls.load(Ordering::SeqCst), 0);
    assert_eq!(provider.http2_calls.load(Ordering::SeqCst), 2);
}

#[tokio::test]
async fn http2_custom_provider_may_use_existing_transport_without_bypassing_safety() {
    let provider = Arc::new(DefaultOnlyProvider {
        normal_calls: AtomicUsize::new(0),
    });
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    let mut client = NetworkClient::new("secret-test", None, Some(&http2_options(true)));
    client.net_provider = Arc::downgrade(&network_provider);
    let result = client
        .get(RequestArgs {
            url: "http://regular:8080/v2/download_config_specs".to_string(),
            ..RequestArgs::new()
        })
        .await;
    assert!(result.is_ok());
    assert_eq!(provider.normal_calls.load(Ordering::SeqCst), 1);
    assert!(
        client
            .get_with_response_limit(
                RequestArgs {
                    url: "http://regular/blob".into(),
                    ..RequestArgs::new()
                },
                4
            )
            .await
            .is_err()
    );
    assert!(
        client
            .get_without_redirects(RequestArgs {
                url: "http://regular/fallback".into(),
                ..RequestArgs::new()
            })
            .await
            .is_err()
    );
    assert_eq!(provider.normal_calls.load(Ordering::SeqCst), 1);
}

#[cfg(not(feature = "custom_network_provider"))]
isolated_http2_test! {
async fn response_limited_blob_urls_retry_oversized_errors() {
    use crate::networking::providers::net_provider_reqwest::NetworkProviderReqwest;
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    for enabled in [false, true] {
        let server = MockServer::start().await;
        Mock::given(method("GET"))
            .and(path("/v1/dynamic_config_value/retry"))
            .respond_with(
                ResponseTemplate::new(500).set_body_bytes(b"temporary upstream failure"),
            )
            .up_to_n_times(1)
            .with_priority(1)
            .expect(1)
            .mount(&server)
            .await;
        Mock::given(method("GET"))
            .and(path("/v1/dynamic_config_value/retry"))
            .respond_with(ResponseTemplate::new(200).set_body_bytes(b"retry"))
            .with_priority(2)
            .expect(1)
            .mount(&server)
            .await;
        let network_provider: Arc<dyn NetworkProvider> =
            Arc::new(NetworkProviderReqwest::new());
        let mut client = NetworkClient::new("secret-test", None, Some(&http2_options(enabled)));
        client.net_provider = Arc::downgrade(&network_provider);
        client.ops_stats = Arc::new(OpsStatsForInstance::new());
        let mut metrics = client.ops_stats.subscribe_for_test();

        let retry_response = client
            .get_with_response_limit(
                RequestArgs {
                    url: format!("{}/v1/dynamic_config_value/retry", server.uri()),
                    retries: 1,
                    ..RequestArgs::new()
                },
                5,
            )
            .await
            .expect("retrying blob request should succeed");
        assert_eq!(retry_response.status_code, Some(200));

        Mock::given(method("GET"))
            .and(path("/v1/dynamic_config_value/oversized-success"))
            .respond_with(ResponseTemplate::new(200).set_body_bytes(b"too-large"))
            .expect(1)
            .mount(&server)
            .await;

        let oversized_success = client
            .get_with_response_limit(
                RequestArgs {
                    url: format!("{}/v1/dynamic_config_value/oversized-success", server.uri()),
                    retries: 1,
                    ..RequestArgs::new()
                },
                5,
            )
            .await;
        assert!(matches!(
            oversized_success,
            Err(NetworkError::RequestNotRetryable(_, Some(200), _))
        ));

        server.verify().await;
        let latencies = take_network_latencies(&mut metrics);
        assert_eq!(latencies.len(), 3);
        for (event, (status, success)) in
            latencies
                .iter()
                .zip([("500", "false"), ("200", "true"), ("200", "false")])
        {
            let tags = event.tags.as_ref().unwrap();
            assert_eq!(tags[STATUS_CODE_TAG], status);
            assert_eq!(tags[super::IS_SUCCESS_TAG], success);
            assert_eq!(tags[super::SOURCE_SERVICE_TAG], server.uri());
        }
    }
}
}
