//! Port of `software.amazon.kinesis.retrieval.fanout.FanOutConfig`.

use std::sync::Arc;

use crate::retrieval::consumer_registration::ConsumerRegistration;
use crate::retrieval::fanout::fan_out_consumer_registration::FanOutConsumerRegistration;
use crate::retrieval::fanout::fan_out_retrieval_factory::{
    ConsumerArnCreator, FanOutRetrievalFactory,
};
use crate::retrieval::retrieval_factory::RetrievalFactory;
use crate::retrieval::retrieval_specific_config::RetrievalSpecificConfig;

/// A factory that builds a [`ConsumerRegistration`] for a stream (test seam for
/// Java's overridable `createConsumerRegistration`).
pub type ConsumerRegistrationFactory =
    Arc<dyn Fn(&str, &str) -> Arc<dyn ConsumerRegistration> + Send + Sync>;

/// User-facing EFO configuration.
///
/// Port of the Java `@Data @Accessors(fluent=true)` class implementing
/// [`RetrievalSpecificConfig`]. `consumerName ?? applicationName` precedence is
/// preserved; consumer-registration validation is deferred (only enforced at
/// registration time).
pub struct FanOutConfig {
    kinesis_client: aws_sdk_kinesis::Client,
    consumer_arn: Option<String>,
    stream_name: Option<String>,
    consumer_name: Option<String>,
    application_name: Option<String>,
    max_describe_stream_summary_retries: i32,
    max_describe_stream_consumer_retries: i32,
    register_stream_consumer_retries: i32,
    retry_backoff_millis: u64,
    /// Overridable registration factory (Java `createConsumerRegistration`).
    consumer_registration_factory: Option<ConsumerRegistrationFactory>,
}

impl FanOutConfig {
    /// Construct from a Kinesis client (Java `FanOutConfig(KinesisAsyncClient)`).
    pub fn new(kinesis_client: aws_sdk_kinesis::Client) -> Self {
        Self {
            kinesis_client,
            consumer_arn: None,
            stream_name: None,
            consumer_name: None,
            application_name: None,
            max_describe_stream_summary_retries: 10,
            max_describe_stream_consumer_retries: 10,
            register_stream_consumer_retries: 10,
            retry_backoff_millis: 1000,
            consumer_registration_factory: None,
        }
    }

    /// The consumer ARN, if set.
    pub fn consumer_arn(&self) -> Option<&str> {
        self.consumer_arn.as_deref()
    }
    /// Set the consumer ARN (skips automatic consumer creation).
    pub fn set_consumer_arn(mut self, arn: impl Into<String>) -> Self {
        self.consumer_arn = Some(arn.into());
        self
    }
    /// The stream name, if set.
    pub fn stream_name(&self) -> Option<&str> {
        self.stream_name.as_deref()
    }
    /// Set the stream name.
    pub fn set_stream_name(mut self, name: impl Into<String>) -> Self {
        self.stream_name = Some(name.into());
        self
    }
    /// The consumer name, if set.
    pub fn consumer_name(&self) -> Option<&str> {
        self.consumer_name.as_deref()
    }
    /// Set the consumer name.
    pub fn set_consumer_name(mut self, name: impl Into<String>) -> Self {
        self.consumer_name = Some(name.into());
        self
    }
    /// The application name, if set.
    pub fn application_name(&self) -> Option<&str> {
        self.application_name.as_deref()
    }
    /// Set the application name.
    pub fn set_application_name(mut self, name: impl Into<String>) -> Self {
        self.application_name = Some(name.into());
        self
    }

    /// Inject a registration factory (test seam for `createConsumerRegistration`).
    pub fn set_consumer_registration_factory(
        mut self,
        factory: ConsumerRegistrationFactory,
    ) -> Self {
        self.consumer_registration_factory = Some(factory);
        self
    }

    /// `consumerName ?? applicationName` (Java `ObjectUtils.firstNonNull`).
    fn consumer_to_create(&self) -> Option<String> {
        self.consumer_name
            .clone()
            .or_else(|| self.application_name.clone())
    }

    /// Build a [`ConsumerRegistration`] for the given stream (Java
    /// `createConsumerRegistration`). Panics (Java `Preconditions.checkNotNull`)
    /// if the stream name or a consumer/application name is missing.
    fn create_consumer_registration(&self, stream_name: &str) -> Arc<dyn ConsumerRegistration> {
        let consumer = self
            .consumer_to_create()
            .expect("applicationName or consumerName must be set for consumer creation");
        if let Some(factory) = &self.consumer_registration_factory {
            return factory(stream_name, &consumer);
        }
        Arc::new(FanOutConsumerRegistration::new(
            self.kinesis_client.clone(),
            stream_name,
            consumer,
            self.max_describe_stream_summary_retries,
            self.max_describe_stream_consumer_retries,
            self.register_stream_consumer_retries,
            self.retry_backoff_millis,
        ))
    }

    /// Build the lazy consumer-ARN creator closure (Java `this::getOrCreateConsumerArn`).
    ///
    /// The creator drives the (async) registration to completion synchronously via
    /// the current tokio runtime (Java blocks the calling thread here). It must be
    /// invoked from within a tokio runtime.
    fn consumer_arn_creator(self: &Arc<Self>) -> ConsumerArnCreator {
        let this = Arc::clone(self);
        Arc::new(move |stream_name: &str| {
            let registration = this.create_consumer_registration(stream_name);
            // Java wraps DependencyException as an unchecked RuntimeException; we
            // panic (the KCL treats consumer-creation failure as fatal). The
            // flavor-aware bridge avoids a `block_in_place` panic on a
            // current-thread runtime.
            let handle = tokio::runtime::Handle::current();
            crate::utils::sync_bridge::run_sync_on(handle, async {
                registration
                    .get_or_create_stream_consumer_arn()
                    .await
                    .unwrap_or_else(|e| panic!("consumer registration failed: {e}"))
            })
        })
    }

    /// Build the [`RetrievalFactory`], boxing an `Arc<Self>` so the ARN-creator
    /// closure can drive registration lazily. This differs from the trait's
    /// `&self` signature only in requiring an `Arc`; see
    /// [`retrieval_factory_arc`](Self::retrieval_factory_arc).
    pub fn retrieval_factory_arc(self: &Arc<Self>) -> Box<dyn RetrievalFactory> {
        Box::new(FanOutRetrievalFactory::new(
            self.kinesis_client.clone(),
            self.stream_name.clone(),
            self.consumer_arn.clone(),
            self.consumer_arn_creator(),
        ))
    }
}

impl RetrievalSpecificConfig for FanOutConfig {
    fn retrieval_factory(&self) -> Box<dyn RetrievalFactory> {
        // The ARN creator needs an `Arc<Self>`; clone the config's fields into a
        // fresh `Arc` (the config is cheaply cloneable in spirit — only plain data
        // + the SDK client, which is `Clone`).
        let arc = Arc::new(FanOutConfig {
            kinesis_client: self.kinesis_client.clone(),
            consumer_arn: self.consumer_arn.clone(),
            stream_name: self.stream_name.clone(),
            consumer_name: self.consumer_name.clone(),
            application_name: self.application_name.clone(),
            max_describe_stream_summary_retries: self.max_describe_stream_summary_retries,
            max_describe_stream_consumer_retries: self.max_describe_stream_consumer_retries,
            register_stream_consumer_retries: self.register_stream_consumer_retries,
            retry_backoff_millis: self.retry_backoff_millis,
            consumer_registration_factory: self.consumer_registration_factory.clone(),
        });
        arc.retrieval_factory_arc()
    }

    fn validate_state(&self, is_multi_stream: bool) {
        if is_multi_stream && (self.stream_name.is_some() || self.consumer_arn.is_some()) {
            panic!(
                "FanOutConfig must not have streamName/consumerArn configured in multi-stream mode"
            );
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{
        InitialPositionInStream, InitialPositionInStreamExtended, StreamConfig, StreamIdentifier,
    };
    use crate::leases::exceptions::LeasingError;
    use crate::leases::ShardInfo;
    use crate::metrics::NullMetricsFactory;
    use std::sync::atomic::{AtomicUsize, Ordering};

    const TEST_CONSUMER_ARN: &str = "TestConsumerArn";
    const TEST_APPLICATION_NAME: &str = "TestApplication";
    const TEST_STREAM_NAME: &str = "TestStream";
    const TEST_CONSUMER_NAME: &str = "TestConsumerName";

    fn client() -> aws_sdk_kinesis::Client {
        aws_sdk_kinesis::Client::from_conf(
            aws_sdk_kinesis::Config::builder()
                .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
                .region(aws_sdk_kinesis::config::Region::new("us-east-1"))
                .build(),
        )
    }

    /// Test double for [`ConsumerRegistration`] (Mockito-mocked
    /// `FanOutConsumerRegistration` in Java). Counts invocations of
    /// `get_or_create_stream_consumer_arn` and can be primed to fail.
    struct StubConsumerRegistration {
        calls: Arc<AtomicUsize>,
        fail: bool,
    }

    #[async_trait::async_trait]
    impl ConsumerRegistration for StubConsumerRegistration {
        async fn get_or_create_stream_consumer_arn(&self) -> Result<String, LeasingError> {
            self.calls.fetch_add(1, Ordering::SeqCst);
            if self.fail {
                Err(LeasingError::dependency("Bad"))
            } else {
                Ok("created-consumer-arn".to_string())
            }
        }
    }

    /// Build a config wired with a counting/failing registration factory (the
    /// Rust analog of Mockito's `doReturn(consumerRegistration).when(config)
    /// .createConsumerRegistration(...)`).
    fn config_with_stub(calls: &Arc<AtomicUsize>, fail: bool) -> FanOutConfig {
        let calls = Arc::clone(calls);
        let factory: ConsumerRegistrationFactory =
            Arc::new(move |_stream: &str, _consumer: &str| {
                Arc::new(StubConsumerRegistration {
                    calls: Arc::clone(&calls),
                    fail,
                }) as Arc<dyn ConsumerRegistration>
            });
        FanOutConfig::new(client())
            .set_application_name(TEST_APPLICATION_NAME)
            .set_stream_name(TEST_STREAM_NAME)
            .set_consumer_registration_factory(factory)
    }

    fn stream_config(consumer_arn: Option<&str>) -> StreamConfig {
        let cfg = StreamConfig::new(
            StreamIdentifier::single_stream_instance(TEST_STREAM_NAME),
            InitialPositionInStreamExtended::new_initial_position(InitialPositionInStream::Latest),
        );
        match consumer_arn {
            Some(arn) => cfg.set_consumer_arn(arn),
            None => cfg,
        }
    }

    /// Rust analog of the Java `getRecordsCache(streamIdentifier)` helper: build
    /// the retrieval factory from the config, then create a records cache for a
    /// shard whose `streamIdentifierSerOpt` is `stream_identifier_ser`. Driving
    /// `create_get_records_cache` triggers the lazy consumer-ARN creation.
    fn get_records_cache(
        config: &FanOutConfig,
        stream_identifier_ser: Option<&str>,
        stream_cfg_consumer_arn: Option<&str>,
    ) {
        let shard_info = ShardInfo::new(
            "shardId-0",
            None,
            Vec::<String>::new(),
            None,
            stream_identifier_ser.map(str::to_string),
        );
        let factory = config.retrieval_factory();
        let _publisher = factory.create_get_records_cache(
            &shard_info,
            &stream_config(stream_cfg_consumer_arn),
            Arc::new(NullMetricsFactory),
            None,
        );
    }

    // Port of FanOutConfigTest.testValidState.
    #[test]
    fn valid_state() {
        let config = FanOutConfig::new(client()).set_stream_name(TEST_STREAM_NAME);
        assert!(config.consumer_arn().is_none());
        assert!(config.stream_name().is_some());
        config.validate_state(false);
        let config = config.set_consumer_arn(TEST_CONSUMER_ARN);
        config.validate_state(false);
    }

    // Port of FanOutConfigTest.testInvalidStateMultiWithStreamName.
    #[test]
    #[should_panic(
        expected = "must not have streamName/consumerArn configured in multi-stream mode"
    )]
    fn invalid_state_multi_with_stream_name() {
        FanOutConfig::new(client())
            .set_stream_name(TEST_STREAM_NAME)
            .validate_state(true);
    }

    // Port of FanOutConfigTest.testInvalidStateMultiWithConsumerArn.
    #[test]
    #[should_panic(
        expected = "must not have streamName/consumerArn configured in multi-stream mode"
    )]
    fn invalid_state_multi_with_consumer_arn() {
        FanOutConfig::new(client())
            .set_consumer_arn(TEST_CONSUMER_ARN)
            .validate_state(true);
    }

    // Port of FanOutConfigTest.testCreationWithBothConsumerApplication: consumerName
    // takes precedence over applicationName.
    #[test]
    fn consumer_name_precedence() {
        let config = FanOutConfig::new(client())
            .set_stream_name(TEST_STREAM_NAME)
            .set_application_name(TEST_APPLICATION_NAME)
            .set_consumer_name(TEST_CONSUMER_NAME);
        assert_eq!(
            config.consumer_to_create().as_deref(),
            Some(TEST_CONSUMER_NAME)
        );
    }

    #[test]
    fn application_name_fallback() {
        let config = FanOutConfig::new(client())
            .set_stream_name(TEST_STREAM_NAME)
            .set_application_name(TEST_APPLICATION_NAME);
        assert_eq!(
            config.consumer_to_create().as_deref(),
            Some(TEST_APPLICATION_NAME)
        );
    }

    // Port of FanOutConfigTest.testNoRegisterIfConsumerArnSet: a set consumerArn
    // yields a factory without touching the registration (the factory uses the ARN
    // directly). We assert the factory builds and does not require a registration.
    #[test]
    fn no_register_if_consumer_arn_set() {
        let config = FanOutConfig::new(client()).set_consumer_arn(TEST_CONSUMER_ARN);
        // Building the factory must not panic (no registration invoked here; the
        // ARN is used directly at cache-creation time).
        let _factory = config.retrieval_factory();
    }

    // Port of FanOutConfigTest.testRegisterCalledWhenConsumerArnUnset:
    // single-stream, consumerArn unset -> registration IS driven.
    #[tokio::test(flavor = "multi_thread")]
    async fn register_called_when_consumer_arn_unset() {
        let calls = Arc::new(AtomicUsize::new(0));
        let config = config_with_stub(&calls, false);
        get_records_cache(&config, None, None);
        assert_eq!(calls.load(Ordering::SeqCst), 1);
    }

    // Port of FanOutConfigTest.testRegisterNotCalledWhenConsumerArnSetInMultiStreamMode:
    // multi-stream shard + streamConfig.consumerArn set -> registration NOT driven
    // (the explicit ARN is used directly).
    #[tokio::test(flavor = "multi_thread")]
    async fn register_not_called_when_consumer_arn_set_in_multi_stream_mode() {
        let calls = Arc::new(AtomicUsize::new(0));
        let config = config_with_stub(&calls, false);
        get_records_cache(
            &config,
            Some("123456789012:stream:12345"),
            Some("consumerArn"),
        );
        assert_eq!(calls.load(Ordering::SeqCst), 0);
    }

    // Port of FanOutConfigTest.testRegisterCalledWhenConsumerArnNotSetInMultiStreamMode:
    // multi-stream shard, no per-stream consumerArn -> registration IS driven.
    #[tokio::test(flavor = "multi_thread")]
    async fn register_called_when_consumer_arn_not_set_in_multi_stream_mode() {
        let calls = Arc::new(AtomicUsize::new(0));
        let config = config_with_stub(&calls, false);
        get_records_cache(&config, Some("123456789012:stream:12345"), None);
        assert_eq!(calls.load(Ordering::SeqCst), 1);
    }

    // Port of FanOutConfigTest.testDependencyExceptionInConsumerCreation: a failing
    // registration surfaces as a panic (Java wraps DependencyException as an
    // unchecked RuntimeException). The registration is still invoked exactly once.
    #[tokio::test(flavor = "multi_thread")]
    #[should_panic(expected = "consumer registration failed")]
    async fn dependency_exception_in_consumer_creation() {
        let calls = Arc::new(AtomicUsize::new(0));
        let config = config_with_stub(&calls, true);
        get_records_cache(&config, None, None);
    }

    // Port of FanOutConfigTest.testCreationWithApplicationName: streamName and
    // applicationName are preserved after building the records cache.
    #[tokio::test(flavor = "multi_thread")]
    async fn creation_with_application_name() {
        let calls = Arc::new(AtomicUsize::new(0));
        let config = config_with_stub(&calls, false);
        get_records_cache(&config, None, None);
        assert_eq!(config.stream_name(), Some(TEST_STREAM_NAME));
        assert_eq!(config.application_name(), Some(TEST_APPLICATION_NAME));
    }

    // Port of FanOutConfigTest.testCreationWithConsumerName: consumerName (with
    // applicationName unset) is preserved after building the records cache.
    #[tokio::test(flavor = "multi_thread")]
    async fn creation_with_consumer_name() {
        let calls = Arc::new(AtomicUsize::new(0));
        let calls2 = Arc::clone(&calls);
        let factory: ConsumerRegistrationFactory =
            Arc::new(move |_stream: &str, _consumer: &str| {
                Arc::new(StubConsumerRegistration {
                    calls: Arc::clone(&calls2),
                    fail: false,
                }) as Arc<dyn ConsumerRegistration>
            });
        let config = FanOutConfig::new(client())
            .set_stream_name(TEST_STREAM_NAME)
            .set_consumer_name(TEST_CONSUMER_NAME)
            .set_consumer_registration_factory(factory);
        get_records_cache(&config, None, None);
        assert_eq!(config.stream_name(), Some(TEST_STREAM_NAME));
        assert_eq!(config.consumer_name(), Some(TEST_CONSUMER_NAME));
    }

    // Port of FanOutConfigTest.testInvalidStateMultiWithStreamNameAndConsumerArn:
    // validateState(true) with BOTH streamName and consumerArn set panics.
    #[test]
    #[should_panic(
        expected = "must not have streamName/consumerArn configured in multi-stream mode"
    )]
    fn invalid_state_multi_with_stream_name_and_consumer_arn() {
        FanOutConfig::new(client())
            .set_stream_name(TEST_STREAM_NAME)
            .set_consumer_arn(TEST_CONSUMER_ARN)
            .validate_state(true);
    }
}
