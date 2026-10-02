//! Port of `software.amazon.kinesis.retrieval.RetrievalConfig`.

use std::sync::Arc;

use crate::common::deprecation_utils::{convert, Either, StreamTrackerKind};
use crate::common::{
    Arn, DefaultKinesisStreamArnConstructor, InitialPositionInStream,
    InitialPositionInStreamExtended, StreamArnConstructor, StreamConfig, StreamIdentifier,
};
use crate::processor::{SingleStreamTracker, StreamTracker};
use crate::retrieval::retrieval_factory::RetrievalFactory;
use crate::retrieval::retrieval_specific_config::RetrievalSpecificConfig;

/// Top-level user-facing configuration for the retrieval subsystem: which
/// Kinesis client / [`StreamTracker`] to use, ListShards retry/backoff tuning,
/// ARN construction strategy, and which
/// [`RetrievalSpecificConfig`]/[`RetrievalFactory`] to use (defaulting to
/// fan-out).
///
/// Port of the Java `@Getter @Setter @Accessors(fluent = true)` class.
///
/// # Deviations
///
/// * **Glue Schema Registry**: the `glueSchemaRegistryDeserializer` field is
///   omitted (the schema-registry integration is deferred; see PORTING.md).
/// * **`appStreamTracker`**: the deprecated `Either<MultiStreamTracker,
///   StreamConfig>` back-compat field is **kept** (the `RetrievalConfigTest`
///   exercises it), holding `Either<Arc<dyn StreamTracker>, StreamConfig>`.
///   Classification (Java `instanceof MultiStreamTracker`/`SingleStreamTracker`)
///   is derived from [`StreamTracker::is_multi_stream`] since `dyn StreamTracker`
///   cannot be downcast — a multi-stream tracker maps to `Left(tracker)`, a
///   single-stream one to `Right(streamConfigList[0])`.
/// * **`retrieval_factory()` default (fan-out) construction** builds a default
///   [`FanOutConfig`](crate::retrieval::fanout::FanOutConfig) when no
///   retrieval-specific config is set (matching Java).
pub struct RetrievalConfig {
    kinesis_client: aws_sdk_kinesis::Client,
    application_name: String,
    stream_tracker: Arc<dyn StreamTracker + Send + Sync>,
    app_stream_tracker: Either<Arc<dyn StreamTracker + Send + Sync>, StreamConfig>,
    list_shards_backoff_time_in_millis: i64,
    max_list_shards_retry_attempts: i32,
    stream_arn_constructor: Box<dyn StreamArnConstructor + Send + Sync>,
    initial_position_in_stream_extended: InitialPositionInStreamExtended,
    retrieval_specific_config: Option<Box<dyn RetrievalSpecificConfig>>,
    retrieval_factory: Option<Box<dyn RetrievalFactory>>,
}

impl RetrievalConfig {
    /// User-agent name identifying the KCL library
    /// (`KINESIS_CLIENT_LIB_USER_AGENT`).
    pub const KINESIS_CLIENT_LIB_USER_AGENT: &'static str =
        crate::retrieval::KINESIS_CLIENT_LIB_USER_AGENT;
    /// User-agent version (`KINESIS_CLIENT_LIB_USER_AGENT_VERSION`).
    pub const KINESIS_CLIENT_LIB_USER_AGENT_VERSION: &'static str =
        crate::retrieval::KINESIS_CLIENT_LIB_USER_AGENT_VERSION;

    /// Default `listShardsBackoffTimeInMillis` (1500).
    pub const DEFAULT_LIST_SHARDS_BACKOFF_TIME_IN_MILLIS: i64 = 1500;
    /// Default `maxListShardsRetryAttempts` (50).
    pub const DEFAULT_MAX_LIST_SHARDS_RETRY_ATTEMPTS: i32 = 50;

    /// Construct from a stream name (Java `(KinesisAsyncClient, String, String)`).
    pub fn from_stream_name(
        kinesis_async_client: aws_sdk_kinesis::Client,
        stream_name: &str,
        application_name: impl Into<String>,
    ) -> Self {
        Self::new(
            kinesis_async_client,
            Arc::new(SingleStreamTracker::from_stream_name(stream_name)),
            application_name,
        )
    }

    /// Construct from a stream ARN (Java `(KinesisAsyncClient, Arn, String)`).
    pub fn from_stream_arn(
        kinesis_async_client: aws_sdk_kinesis::Client,
        stream_arn: Arn,
        application_name: impl Into<String>,
    ) -> Self {
        Self::new(
            kinesis_async_client,
            Arc::new(SingleStreamTracker::from_arn(stream_arn)),
            application_name,
        )
    }

    /// Construct from a [`StreamTracker`] (Java `(KinesisAsyncClient,
    /// StreamTracker, String)`), the delegate constructor.
    pub fn new(
        kinesis_async_client: aws_sdk_kinesis::Client,
        stream_tracker: Arc<dyn StreamTracker + Send + Sync>,
        application_name: impl Into<String>,
    ) -> Self {
        let app_stream_tracker = Self::compute_app_stream_tracker(&stream_tracker);
        Self {
            kinesis_client: kinesis_async_client,
            application_name: application_name.into(),
            stream_tracker,
            app_stream_tracker,
            list_shards_backoff_time_in_millis: Self::DEFAULT_LIST_SHARDS_BACKOFF_TIME_IN_MILLIS,
            max_list_shards_retry_attempts: Self::DEFAULT_MAX_LIST_SHARDS_RETRY_ATTEMPTS,
            stream_arn_constructor: Box::new(DefaultKinesisStreamArnConstructor),
            initial_position_in_stream_extended:
                InitialPositionInStreamExtended::new_initial_position(
                    InitialPositionInStream::Latest,
                ),
            retrieval_specific_config: None,
            retrieval_factory: None,
        }
    }

    /// Build the deprecated `appStreamTracker` `Either` from the modern tracker.
    ///
    /// Port of `DeprecationUtils.convert(streamTracker, single ->
    /// single.streamConfigList().get(0))`. A multi-stream tracker → `Left(tracker)`;
    /// a single-stream tracker → `Right(streamConfig)`.
    fn compute_app_stream_tracker(
        stream_tracker: &Arc<dyn StreamTracker + Send + Sync>,
    ) -> Either<Arc<dyn StreamTracker + Send + Sync>, StreamConfig> {
        let kind = if stream_tracker.is_multi_stream() {
            StreamTrackerKind::Multi
        } else {
            StreamTrackerKind::Single
        };
        // The `single -> streamConfigList().get(0)` converter runs only for the
        // single-stream (Right) case, so it is evaluated lazily inside the
        // closure — a multi-stream tracker (Left) never touches the config list.
        convert(
            kind,
            Arc::clone(stream_tracker),
            Arc::clone(stream_tracker),
            |single_tracker: Arc<dyn StreamTracker + Send + Sync>| {
                single_tracker
                    .stream_config_list()
                    .into_iter()
                    .next()
                    .expect("single-stream tracker must have at least one stream config")
            },
        )
    }

    /// The Kinesis client used for record retrieval.
    pub fn kinesis_client(&self) -> &aws_sdk_kinesis::Client {
        &self.kinesis_client
    }

    /// The application name.
    pub fn application_name(&self) -> &str {
        &self.application_name
    }

    /// The stream(s) to be consumed by this KCL application.
    pub fn stream_tracker(&self) -> &Arc<dyn StreamTracker + Send + Sync> {
        &self.stream_tracker
    }

    /// The deprecated `appStreamTracker` dual representation.
    pub fn app_stream_tracker(
        &self,
    ) -> &Either<Arc<dyn StreamTracker + Send + Sync>, StreamConfig> {
        &self.app_stream_tracker
    }

    /// Backoff (millis) between consecutive ListShards calls (default 1500).
    pub fn list_shards_backoff_time_in_millis(&self) -> i64 {
        self.list_shards_backoff_time_in_millis
    }

    /// Set [`list_shards_backoff_time_in_millis`](Self::list_shards_backoff_time_in_millis).
    pub fn set_list_shards_backoff_time_in_millis(mut self, value: i64) -> Self {
        self.list_shards_backoff_time_in_millis = value;
        self
    }

    /// Max ListShards retries when throttled (default 50).
    pub fn max_list_shards_retry_attempts(&self) -> i32 {
        self.max_list_shards_retry_attempts
    }

    /// Set [`max_list_shards_retry_attempts`](Self::max_list_shards_retry_attempts).
    pub fn set_max_list_shards_retry_attempts(mut self, value: i32) -> Self {
        self.max_list_shards_retry_attempts = value;
        self
    }

    /// The stream-ARN constructor (default [`DefaultKinesisStreamArnConstructor`]).
    pub fn stream_arn_constructor(&self) -> &(dyn StreamArnConstructor + Send + Sync) {
        self.stream_arn_constructor.as_ref()
    }

    /// Set [`stream_arn_constructor`](Self::stream_arn_constructor).
    pub fn set_stream_arn_constructor(
        mut self,
        value: Box<dyn StreamArnConstructor + Send + Sync>,
    ) -> Self {
        self.stream_arn_constructor = value;
        self
    }

    /// The deprecated flat `initialPositionInStreamExtended` (default `LATEST`).
    pub fn initial_position_in_stream_extended(&self) -> &InitialPositionInStreamExtended {
        &self.initial_position_in_stream_extended
    }

    /// Reconfigure the embedded [`StreamTracker`]'s initial position, but only
    /// when **not** in multi-stream mode.
    ///
    /// Port of the deprecated fluent
    /// `initialPositionInStreamExtended(InitialPositionInStreamExtended)`. Panics
    /// (Java `IllegalArgumentException`) if the tracker is multi-stream.
    pub fn set_initial_position_in_stream_extended(
        &mut self,
        initial_position_in_stream_extended: InitialPositionInStreamExtended,
    ) -> &mut Self {
        if self.stream_tracker.is_multi_stream() {
            panic!("Cannot set initialPositionInStreamExtended when multiStreamTracker is set");
        }
        let stream_identifier = self.single_stream_identifier();
        let updated_config = StreamConfig::new(
            stream_identifier.clone(),
            initial_position_in_stream_extended,
        );
        self.stream_tracker = Arc::new(SingleStreamTracker::new(
            stream_identifier,
            updated_config.clone(),
        ));
        self.app_stream_tracker = Either::Right(updated_config);
        self.initial_position_in_stream_extended = initial_position_in_stream_extended;
        self
    }

    /// Set the retrieval-specific config, validating it against the multi-stream
    /// mode first. If validation panics, the previous value is **not** replaced
    /// (the panic propagates before the assignment) — matching Java's
    /// fail-before-mutate behavior (`validateState` throws before the field is
    /// set).
    ///
    /// Port of the `retrievalSpecificConfig(RetrievalSpecificConfig)` setter.
    pub fn set_retrieval_specific_config(
        &mut self,
        retrieval_specific_config: Box<dyn RetrievalSpecificConfig>,
    ) -> &mut Self {
        retrieval_specific_config.validate_state(self.stream_tracker.is_multi_stream());
        self.retrieval_specific_config = Some(retrieval_specific_config);
        self
    }

    /// The retrieval-specific config, if set.
    pub fn retrieval_specific_config(&self) -> Option<&dyn RetrievalSpecificConfig> {
        self.retrieval_specific_config.as_deref()
    }

    /// Lazily build (memoized) and return the [`RetrievalFactory`].
    ///
    /// Port of the lazy `retrievalFactory()`: when no `retrievalSpecificConfig`
    /// is set, builds a default [`FanOutConfig`](crate::retrieval::fanout::FanOutConfig)
    /// (applying the application name, and the single-stream name when not
    /// multi-stream), stores it, and caches its factory. First call wins.
    pub fn retrieval_factory(&mut self) -> &dyn RetrievalFactory {
        if self.retrieval_factory.is_none() {
            if self.retrieval_specific_config.is_none() {
                // Build the default FanOutConfig (Java `new FanOutConfig(kinesisClient)`).
                let mut fan_out =
                    crate::retrieval::fanout::FanOutConfig::new(self.kinesis_client.clone())
                        .set_application_name(self.application_name.clone());
                if !self.stream_tracker.is_multi_stream() {
                    fan_out =
                        fan_out.set_stream_name(self.single_stream_identifier().stream_name());
                }
                self.set_retrieval_specific_config(Box::new(fan_out));
            }
            let specific = self
                .retrieval_specific_config
                .as_ref()
                .expect("retrieval-specific config set above");
            self.retrieval_factory = Some(specific.retrieval_factory());
        }
        self.retrieval_factory.as_deref().unwrap()
    }

    /// The single-stream tracker's [`StreamIdentifier`] (Java
    /// `getSingleStreamIdentifier`).
    fn single_stream_identifier(&self) -> StreamIdentifier {
        self.stream_tracker
            .stream_config_list()
            .into_iter()
            .next()
            .expect("single-stream tracker must have at least one stream config")
            .stream_identifier()
            .clone()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::common::{InitialPositionInStream, InitialPositionInStreamExtended};
    use crate::processor::former_streams_leases_deletion_strategy::{
        FormerStreamsLeasesDeletionStrategy, NoLeaseDeletionStrategy,
    };
    use crate::processor::multi_stream_tracker::MultiStreamTracker;

    const APPLICATION_NAME: &str = "RetrievalConfigTest";

    fn kinesis_client() -> aws_sdk_kinesis::Client {
        aws_sdk_kinesis::Client::from_conf(
            aws_sdk_kinesis::Config::builder()
                .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
                .region(aws_sdk_kinesis::config::Region::new("us-east-1"))
                .build(),
        )
    }

    fn create_config_from_name(stream_name: &str) -> RetrievalConfig {
        RetrievalConfig::from_stream_name(kinesis_client(), stream_name, APPLICATION_NAME)
    }

    fn create_config_from_tracker(
        tracker: Arc<dyn StreamTracker + Send + Sync>,
    ) -> RetrievalConfig {
        RetrievalConfig::new(kinesis_client(), tracker, APPLICATION_NAME)
    }

    fn create_arn(stream_name: &str) -> Arn {
        Arn::new(
            "aws",
            "kinesis",
            Some("us-east-1".to_string()),
            Some("123456789012".to_string()),
            format!("stream/{stream_name}"),
        )
    }

    /// A minimal multi-stream tracker for the multi-stream tests.
    struct TestMultiStreamTracker;
    impl StreamTracker for TestMultiStreamTracker {
        fn stream_config_list(&self) -> Vec<StreamConfig> {
            vec![]
        }
        fn former_streams_leases_deletion_strategy(
            &self,
        ) -> Box<dyn FormerStreamsLeasesDeletionStrategy + Send + Sync> {
            Box::new(NoLeaseDeletionStrategy)
        }
        fn is_multi_stream(&self) -> bool {
            true
        }
    }
    impl MultiStreamTracker for TestMultiStreamTracker {}

    // Port of RetrievalConfigTest.testSingleStreamTrackerConstruction.
    #[test]
    fn single_stream_tracker_construction() {
        let stream_name = "single-stream";
        let arn = create_arn(stream_name);
        let configs = vec![
            create_config_from_name(stream_name),
            create_config_from_tracker(Arc::new(SingleStreamTracker::from_stream_name(
                stream_name,
            ))),
            create_config_from_tracker(Arc::new(SingleStreamTracker::from_arn(arn.clone()))),
            create_config_from_tracker(Arc::new(SingleStreamTracker::from_arn(arn))),
        ];
        for rc in &configs {
            // appStreamTracker.left() is empty (it's a Right for single stream).
            assert!(matches!(rc.app_stream_tracker(), Either::Right(_)));
            let list = rc.stream_tracker().stream_config_list();
            assert_eq!(list.len(), 1);
            assert_eq!(list[0].stream_identifier().stream_name(), stream_name);
            assert!(!rc.stream_tracker().is_multi_stream());
        }
    }

    // Port of RetrievalConfigTest.testMultiStreamTrackerConstruction.
    #[test]
    fn multi_stream_tracker_construction() {
        let tracker: Arc<dyn StreamTracker + Send + Sync> = Arc::new(TestMultiStreamTracker);
        let config = create_config_from_tracker(Arc::clone(&tracker));
        // appStreamTracker.right() is empty (it's a Left for multi stream).
        match config.app_stream_tracker() {
            Either::Left(t) => assert!(Arc::ptr_eq(t, &tracker)),
            Either::Right(_) => panic!("expected Left for multi-stream tracker"),
        }
        assert!(Arc::ptr_eq(config.stream_tracker(), &tracker));
    }

    // Port of RetrievalConfigTest.testUpdateInitialPositionInSingleStream.
    #[test]
    fn update_initial_position_in_single_stream() {
        let mut config =
            create_config_from_tracker(Arc::new(SingleStreamTracker::from_stream_name("foo")));
        for sc in config.stream_tracker().stream_config_list() {
            assert_eq!(
                sc.initial_position_in_stream_extended()
                    .initial_position_in_stream(),
                InitialPositionInStream::Latest
            );
        }
        config.set_initial_position_in_stream_extended(
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        );
        for sc in config.stream_tracker().stream_config_list() {
            assert_eq!(
                sc.initial_position_in_stream_extended()
                    .initial_position_in_stream(),
                InitialPositionInStream::TrimHorizon
            );
        }
    }

    // Port of RetrievalConfigTest.testUpdateInitialPositionInMultiStream.
    #[test]
    #[should_panic(
        expected = "Cannot set initialPositionInStreamExtended when multiStreamTracker is set"
    )]
    fn update_initial_position_in_multi_stream_panics() {
        let mut config = create_config_from_tracker(Arc::new(TestMultiStreamTracker));
        config.set_initial_position_in_stream_extended(
            InitialPositionInStreamExtended::new_initial_position(
                InitialPositionInStream::TrimHorizon,
            ),
        );
    }

    /// A [`RetrievalSpecificConfig`] whose `validate_state` optionally panics,
    /// standing in for the Java mock with `doThrow(...).validateState(true)`. It
    /// tags itself with an id so the test can assert which config survives.
    struct TestRetrievalSpecificConfig {
        should_panic: bool,
    }
    impl RetrievalSpecificConfig for TestRetrievalSpecificConfig {
        fn retrieval_factory(&self) -> Box<dyn RetrievalFactory> {
            unimplemented!("not needed for this test")
        }
        fn validate_state(&self, _is_multi_stream: bool) {
            if self.should_panic {
                panic!("womp womp");
            }
        }
    }

    // Port of RetrievalConfigTest.testInvalidRetrievalSpecificConfig: an invalid
    // config does not overwrite a valid one.
    #[test]
    fn invalid_retrieval_specific_config_does_not_overwrite() {
        let mut config = create_config_from_tracker(Arc::new(TestMultiStreamTracker));
        assert!(config.retrieval_specific_config().is_none());

        config.set_retrieval_specific_config(Box::new(TestRetrievalSpecificConfig {
            should_panic: false,
        }));
        assert!(config.retrieval_specific_config().is_some());

        // set_retrieval_specific_config panics inside validate_state before the
        // field is replaced; catch it and assert the valid config remains.
        let result = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            config.set_retrieval_specific_config(Box::new(TestRetrievalSpecificConfig {
                should_panic: true,
            }));
        }));
        assert!(result.is_err());
        // The valid config (id 1) is still present; the invalid one never replaced it.
        assert!(config.retrieval_specific_config().is_some());
    }
}
