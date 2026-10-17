use super::NetworkProviderReqwest;
use crate::networking::{HttpMethod, NetworkProvider, RequestArgs, ResponseLimitOutcome};
use flate2::{Compression, write::GzEncoder};
use serde::Deserialize;
use serde_json::value::RawValue;
use std::io::Write;
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

const BODY: &[u8] = br#"{ "number": -0.0, "raw": {"n":1.2300e+09,"n":18446744073709551616} }"#;

#[derive(Debug, Deserialize)]
struct Payload {
    number: f64,
    raw: Box<RawValue>,
}

async fn serve(body: Vec<u8>, gzip: bool) -> MockServer {
    let server = MockServer::start().await;
    let mut response = ResponseTemplate::new(200)
        .insert_header("x-response-marker", "shared-body-test")
        .set_body_bytes(body);
    if gzip {
        response = response.insert_header("content-encoding", "gzip");
    }
    Mock::given(method("GET"))
        .and(path("/body"))
        .respond_with(response)
        .mount(&server)
        .await;
    server
}

fn args(server: &MockServer, disable_file_streaming: Option<bool>) -> RequestArgs {
    RequestArgs {
        url: format!("{}/body", server.uri()),
        disable_file_streaming,
        ..RequestArgs::new()
    }
}

#[tokio::test]
async fn unlimited_memory_shares_bytes_for_both_selection_paths() {
    let server = serve(BODY.to_vec(), false).await;
    for (file_access, disable_streaming) in [(true, Some(true)), (false, None)] {
        let mut provider = NetworkProviderReqwest::new();
        provider.has_file_write_access = file_access;
        let response = provider
            .send(&HttpMethod::GET, &args(&server, disable_streaming))
            .await;
        assert_eq!(response.status_code, Some(200));
        assert!(response.error.is_none(), "{:?}", response.error);
        let mut data = response.data.unwrap();
        assert_eq!(data.shared_bytes(), Some(BODY));
        assert_eq!(
            data.get_header_ref("x-response-marker").map(String::as_str),
            Some("shared-body-test")
        );
        for _ in 0..2 {
            let mut payload = data.deserialize_into::<Payload>().unwrap();
            assert_eq!(payload.number.to_bits(), (-0.0_f64).to_bits());
            assert_eq!(
                payload.raw.get(),
                r#"{"n":1.2300e+09,"n":18446744073709551616}"#
            );
            payload.number = 1.0;
            data.deserialize_in_place(&mut payload).unwrap();
            assert_eq!(payload.number.to_bits(), (-0.0_f64).to_bits());
            assert_eq!(
                payload.raw.get(),
                r#"{"n":1.2300e+09,"n":18446744073709551616}"#
            );
            assert_eq!(data.read_to_bytes().unwrap(), BODY);
            assert_eq!(data.read_to_string().unwrap().as_bytes(), BODY);
        }
    }
}

#[tokio::test]
async fn unlimited_memory_shares_decoded_gzip_body() {
    let mut encoder = GzEncoder::new(Vec::new(), Compression::default());
    encoder.write_all(BODY).unwrap();
    let server = serve(encoder.finish().unwrap(), true).await;
    let response = NetworkProviderReqwest::new()
        .send(&HttpMethod::GET, &args(&server, Some(true)))
        .await;
    assert!(response.error.is_none(), "{:?}", response.error);
    let mut data = response.data.unwrap();
    assert_eq!(data.shared_bytes(), Some(BODY));
    assert_eq!(data.read_to_bytes().unwrap(), BODY);
}

#[tokio::test]
async fn spooled_responses_remain_non_shared_before_and_after_rollover() {
    for size in [BODY.len(), 2 * 1024 * 1024 + 1] {
        let body = vec![b'a'; size];
        let server = serve(body.clone(), false).await;
        let mut provider = NetworkProviderReqwest::new();
        provider.has_file_write_access = true;
        let response = provider.send(&HttpMethod::GET, &args(&server, None)).await;
        assert!(response.error.is_none(), "{:?}", response.error);
        let mut data = response.data.unwrap();
        assert!(data.shared_bytes().is_none());
        assert_eq!(data.read_to_bytes().unwrap(), body);
    }
}

#[tokio::test]
async fn bounded_responses_keep_non_shared_storage() {
    let server = serve(BODY.to_vec(), false).await;
    for disable_streaming in [None, Some(true)] {
        let mut provider = NetworkProviderReqwest::new();
        provider.has_file_write_access = true;
        let result = provider
            .send_with_response_limit(
                &HttpMethod::GET,
                &args(&server, disable_streaming),
                BODY.len() as u64,
            )
            .await;
        let ResponseLimitOutcome::Response(response) = result else {
            panic!("body at the limit should be accepted");
        };
        assert!(response.error.is_none(), "{:?}", response.error);
        let mut data = response.data.unwrap();
        assert!(data.shared_bytes().is_none());
        assert_eq!(data.read_to_bytes().unwrap(), BODY);
    }
}
