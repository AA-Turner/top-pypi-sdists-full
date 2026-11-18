use super::{RequestArgs, ReqwestTransport};
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

#[tokio::test]
async fn invalid_custom_ca_falls_back_without_caching_or_enabling_redirects() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/redirect"))
        .respond_with(ResponseTemplate::new(302).insert_header("location", "/target"))
        .expect(1)
        .mount(&server)
        .await;
    Mock::given(path("/target"))
        .respond_with(ResponseTemplate::new(200))
        .expect(0)
        .mount(&server)
        .await;
    let args = RequestArgs {
        ca_cert_pem: Some(b"-----BEGIN CERTIFICATE-----\nAAAA\n-----END CERTIFICATE-----".to_vec()),
        ..RequestArgs::new()
    };
    let (client, cacheable) = ReqwestTransport::build_client_with_cache_status(&args, true);
    assert!(!cacheable);
    let response = client
        .get(format!("{}/redirect", server.uri()))
        .send()
        .await
        .unwrap();
    assert_eq!(response.status(), 302);
    server.verify().await;
}
