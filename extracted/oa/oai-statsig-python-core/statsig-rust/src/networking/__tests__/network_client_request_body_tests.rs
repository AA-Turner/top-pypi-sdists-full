use super::NetworkClient;
use crate::StatsigOptions;
use crate::networking::{HttpMethod, NetworkProvider, RequestArgs, Response, ResponseData};
use async_trait::async_trait;
use std::collections::HashMap;
use std::sync::{
    Arc,
    atomic::{AtomicI64, AtomicUsize, Ordering},
};

struct BodyCheckingProvider {
    original_body_address: usize,
    expected_body: Vec<u8>,
    failures: u32,
    attempts: AtomicUsize,
    last_timestamp: AtomicI64,
}

#[async_trait]
impl NetworkProvider for BodyCheckingProvider {
    async fn send(&self, method: &HttpMethod, args: &RequestArgs) -> Response {
        assert!(*method == HttpMethod::POST);
        assert_eq!(args.url, "https://events.statsigapi.net/v1/log_event");
        assert_eq!(args.retries, self.failures);
        let body = args.body.as_ref().unwrap();
        assert_eq!(
            body.as_ptr() as usize,
            self.original_body_address,
            "the client must borrow the original payload on every attempt"
        );
        assert_eq!(body, &self.expected_body);

        let headers = args.headers.as_ref().unwrap();
        assert_eq!(headers["X-Request"], "request-value");
        assert_eq!(headers["X-Shared"], "client-value");
        let timestamp = headers["STATSIG-CLIENT-TIME"].parse::<i64>().unwrap();
        assert!(timestamp > 0);
        let previous_timestamp = self.last_timestamp.swap(timestamp, Ordering::SeqCst);
        if previous_timestamp != 0 {
            assert_eq!(timestamp, previous_timestamp);
        }

        let attempt = self.attempts.fetch_add(1, Ordering::SeqCst);
        Response {
            status_code: Some(if attempt < self.failures as usize {
                503
            } else {
                200
            }),
            data: Some(ResponseData::from_bytes(b"{}".to_vec())),
            error: None,
        }
    }
}

async fn check_post_body(failures: u32) {
    let body: Vec<u8> = (0..65536).map(|index| (index % 251) as u8).collect();
    let provider = Arc::new(BodyCheckingProvider {
        original_body_address: body.as_ptr() as usize,
        expected_body: body.clone(),
        failures,
        attempts: AtomicUsize::new(0),
        last_timestamp: AtomicI64::new(0),
    });
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    let mut client = NetworkClient::new(
        "secret-test",
        Some(HashMap::from([("X-Shared".into(), "client-value".into())])),
        Some(&StatsigOptions {
            state_read_primary_attempts: Some(1),
            ..Default::default()
        }),
    );
    client.set_network_provider_for_test(Arc::downgrade(&network_provider));
    let response = client
        .post(
            RequestArgs {
                url: "https://events.statsigapi.net/v1/log_event".into(),
                retries: failures,
                headers: Some(HashMap::from([
                    ("X-Request".into(), "request-value".into()),
                    ("X-Shared".into(), "overridden-value".into()),
                    ("STATSIG-CLIENT-TIME".into(), "0".into()),
                ])),
                ..RequestArgs::new()
            },
            Some(body),
        )
        .await
        .unwrap();
    assert_eq!(response.status_code, Some(200));
    assert_eq!(
        provider.attempts.load(Ordering::SeqCst),
        failures as usize + 1
    );
}

#[tokio::test]
async fn post_reuses_body_buffer_on_first_attempt() {
    check_post_body(0).await;
}

#[tokio::test]
async fn post_reuses_body_buffer_across_retries() {
    check_post_body(2).await;
}
