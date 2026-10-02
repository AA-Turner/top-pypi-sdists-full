//! Test-only helpers for building a mock `aws_sdk_kinesis::Client` backed by
//! [`aws_smithy_mocks`], used by the retrieval polling/fanout behavioral tests.
//!
//! The Java tests mock `KinesisAsyncClient` (Mockito). In Rust we inject canned
//! responses/errors into a *real* `aws_sdk_kinesis::Client` via the smithy mock
//! interceptor, then assert on the fetcher/publisher behavior.

use aws_sdk_kinesis::Client;
use aws_smithy_mocks::{mock_client, Rule, RuleMode};

/// Build a mock Kinesis client that replays the given rules in order
/// ([`RuleMode::Sequential`], mirroring Mockito's chained `thenReturn`).
pub fn mock_kinesis_client(rules: &[&Rule]) -> Client {
    mock_client!(aws_sdk_kinesis, RuleMode::Sequential, rules)
}

/// Build a mock Kinesis client that matches **any** applicable rule regardless
/// of order.
pub fn mock_kinesis_client_match_any(rules: &[&Rule]) -> Client {
    mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, rules)
}

/// A Kinesis client whose HTTP connector never completes: every request stays
/// pending (sleeping on the tokio timer). Under a paused test clock this lets a
/// caller's own `tokio::time::timeout` fire deterministically, exercising the
/// request-timeout / `TimeoutException`-is-retryable path (the Rust async
/// deviation of the Java `resolveOrCancelFuture` timeout).
pub fn hanging_kinesis_client() -> Client {
    use aws_smithy_runtime_api::client::http::{
        HttpClient, HttpConnector, HttpConnectorFuture, HttpConnectorSettings, SharedHttpConnector,
    };
    use aws_smithy_runtime_api::client::orchestrator::HttpRequest;
    use aws_smithy_runtime_api::client::runtime_components::RuntimeComponents;

    #[derive(Debug, Clone)]
    struct HangingConnector;

    impl HttpConnector for HangingConnector {
        fn call(&self, _request: HttpRequest) -> HttpConnectorFuture {
            HttpConnectorFuture::new(async {
                // Sleep effectively forever; under paused time this future never
                // resolves until the runtime is dropped, so the caller's timeout wins.
                tokio::time::sleep(std::time::Duration::from_secs(3600)).await;
                unreachable!("hanging connector should never resolve in a test")
            })
        }
    }

    #[derive(Debug, Clone)]
    struct HangingHttpClient;

    impl HttpClient for HangingHttpClient {
        fn http_connector(
            &self,
            _settings: &HttpConnectorSettings,
            _components: &RuntimeComponents,
        ) -> SharedHttpConnector {
            SharedHttpConnector::new(HangingConnector)
        }
    }

    Client::from_conf(
        aws_sdk_kinesis::Config::builder()
            .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
            .region(aws_sdk_kinesis::config::Region::new("us-east-1"))
            .credentials_provider(aws_sdk_kinesis::config::Credentials::new(
                "test", "test", None, None, "test",
            ))
            .retry_config(aws_sdk_kinesis::config::retry::RetryConfig::disabled())
            .timeout_config(aws_sdk_kinesis::config::timeout::TimeoutConfig::disabled())
            .http_client(HangingHttpClient)
            .build(),
    )
}
