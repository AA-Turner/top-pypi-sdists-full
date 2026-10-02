//! Port of `software.amazon.kinesis.coordinator.streamInfo.StreamInfoDAO`.

use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;
use aws_sdk_kinesis::Client as KinesisClient;
use rand::RngExt;

use crate::common::StreamIdentifier;
use crate::coordinator::coordinator_state::CoordinatorState;
use crate::coordinator::coordinator_state_dao::CoordinatorStateAccess;
use crate::coordinator::stream_info::StreamInfo;
use crate::leases::exceptions::LeasingError;
use crate::leases::CoordinatorStateType;

const INITIAL_BACKOFF_MILLIS: u64 = 500;
const MAX_BACKOFF_MILLIS: u64 = 5000;
const MAX_RETRIES: i32 = 5;
const JITTER_RANGE: u64 = 100;

/// Higher-level store for `StreamInfo` entities on top of a
/// [`CoordinatorStateAccess`]. Java `StreamInfoDAO` is a concrete class;
/// [`StreamInfoStore`] is the trait its consumers ([`StreamIdCacheManager`],
/// [`StreamInfoManager`]) depend on so they can be unit-tested against a mock
/// (the Java tests mock `StreamInfoDAO`).
#[cfg_attr(test, mockall::automock)]
#[async_trait]
pub trait StreamInfoStore: Send + Sync {
    async fn create_stream_info(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<bool, LeasingError>;

    async fn delete_stream_info(&self, key: &str) -> Result<bool, LeasingError>;

    async fn list_stream_info(&self) -> Result<Vec<StreamInfo>, LeasingError>;

    async fn get_stream_info(&self, key: &str) -> Result<Option<StreamInfo>, LeasingError>;
}

/// DAO built on top of [`CoordinatorStateAccess`] specifically for `StreamInfo`
/// entities; also resolves the Kinesis-service-assigned `streamId` for a
/// [`StreamIdentifier`] via `DescribeStreamSummary` (with retry/backoff on
/// throttling). Java `StreamInfoDAO`.
pub struct StreamInfoDAO {
    coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
    kinesis_async_client: KinesisClient,
}

impl StreamInfoDAO {
    /// Java `StreamInfoDAO(CoordinatorStateDAO, KinesisAsyncClient)`.
    pub fn new(
        coordinator_state_dao: Arc<dyn CoordinatorStateAccess>,
        kinesis_async_client: KinesisClient,
    ) -> Self {
        Self {
            coordinator_state_dao,
            kinesis_async_client,
        }
    }

    /// Java private `getStreamId(StreamIdentifier)`: `DescribeStreamSummary`
    /// with exponential backoff + jitter, retrying only on
    /// `LimitExceededException`. Any other error aborts immediately as
    /// [`LeasingError::Dependency`]. Returns `None` if all retries exhaust.
    async fn get_stream_id(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<Option<String>, LeasingError> {
        let mut builder = self
            .kinesis_async_client
            .describe_stream_summary()
            .stream_name(stream_identifier.stream_name());
        if let Some(arn) = stream_identifier.stream_arn_optional() {
            builder = builder.stream_arn(arn.to_string());
        }

        let mut retry_count = 0;
        let mut backoff_time = INITIAL_BACKOFF_MILLIS;

        while retry_count < MAX_RETRIES {
            match builder.clone().send().await {
                Ok(response) => {
                    return Ok(response
                        .stream_description_summary()
                        .and_then(|s| s.stream_id())
                        .map(str::to_string));
                }
                Err(sdk_err) => {
                    let e = sdk_err.into_service_error();
                    if e.is_limit_exceeded_exception() {
                        if retry_count == MAX_RETRIES - 1 {
                            return Err(LeasingError::dependency_caused_by(
                                "Max retries exceeded while describing stream",
                                Box::new(e),
                            ));
                        }
                        tokio::time::sleep(Duration::from_millis(backoff_time)).await;
                        // Exponential backoff with jitter.
                        let jitter = rand::rng().random_range(0..JITTER_RANGE);
                        backoff_time = (backoff_time * 2).min(MAX_BACKOFF_MILLIS) + jitter;
                        retry_count += 1;
                    } else {
                        return Err(LeasingError::dependency_caused_by(
                            "Error describing stream",
                            Box::new(e),
                        ));
                    }
                }
            }
        }
        tracing::error!(stream = %stream_identifier, "Max retries exceeded while describing stream");
        Ok(None)
    }
}

#[async_trait]
impl StreamInfoStore for StreamInfoDAO {
    /// Java `createStreamInfo(StreamIdentifier)`.
    async fn create_stream_info(
        &self,
        stream_identifier: &StreamIdentifier,
    ) -> Result<bool, LeasingError> {
        let stream_id = self.get_stream_id(stream_identifier).await?;
        tracing::info!(?stream_id, stream = %stream_identifier, "StreamId response from describeStreamSummary");
        let stream_id = match stream_id {
            Some(s) if !s.is_empty() && s != "null" => s,
            _ => {
                return Err(LeasingError::invalid_state(format!(
                    "Failed to create stream metadata because StreamId response from \
                     describeStreamSummary call is null or empty for streamIdentifier {stream_identifier}"
                )));
            }
        };
        let stream_info = StreamInfo::new(stream_identifier.to_string(), stream_id);
        self.coordinator_state_dao
            .create_coordinator_state_if_not_exists(&CoordinatorState::StreamInfo(stream_info))
            .await
    }

    /// Java `deleteStreamInfo(String key)`.
    async fn delete_stream_info(&self, key: &str) -> Result<bool, LeasingError> {
        self.coordinator_state_dao
            .delete_coordinator_state(key)
            .await
    }

    /// Java `listStreamInfo()` — lists STREAM_INFO coordinator states, keeping
    /// only the `StreamInfo` instances.
    async fn list_stream_info(&self) -> Result<Vec<StreamInfo>, LeasingError> {
        let states = self
            .coordinator_state_dao
            .list_coordinator_state_by_entity_type(CoordinatorStateType::StreamInfo)
            .await?;
        Ok(states
            .into_iter()
            .filter_map(|s| match s {
                CoordinatorState::StreamInfo(info) => Some(info),
                _ => None,
            })
            .collect())
    }

    /// Java `getStreamInfo(String key)` — returns `None` (with a WARN) if the
    /// coordinator state isn't a `StreamInfo` instance.
    async fn get_stream_info(&self, key: &str) -> Result<Option<StreamInfo>, LeasingError> {
        match self
            .coordinator_state_dao
            .get_coordinator_state(key)
            .await?
        {
            Some(CoordinatorState::StreamInfo(info)) => Ok(Some(info)),
            _ => {
                tracing::warn!(key, "Could not find StreamInfo for key");
                Ok(None)
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::coordinator::coordinator_state_dao::MockCoordinatorStateAccess;
    use aws_sdk_kinesis::operation::describe_stream_summary::DescribeStreamSummaryOutput;
    use aws_sdk_kinesis::types::error::{LimitExceededException, ResourceNotFoundException};
    use aws_sdk_kinesis::types::StreamDescriptionSummary;
    use aws_smithy_mocks::{mock, mock_client, RuleMode};
    use mockall::predicate::eq;

    const STREAM_ID: &str = "streamId-123-ghi";
    const STREAM_ARN: &str = "arn:aws:kinesis:us-west-2:123456789012:stream/test-stream";

    fn stream_identifier() -> StreamIdentifier {
        StreamIdentifier::single_stream_instance("test-stream")
    }

    fn describe_response() -> DescribeStreamSummaryOutput {
        DescribeStreamSummaryOutput::builder()
            .stream_description_summary(
                StreamDescriptionSummary::builder()
                    .stream_arn(STREAM_ARN)
                    .stream_name("test-stream")
                    .stream_id(STREAM_ID)
                    .stream_status(aws_sdk_kinesis::types::StreamStatus::Active)
                    .retention_period_hours(24)
                    .stream_creation_timestamp(aws_smithy_types::DateTime::from_secs(0))
                    .encryption_type(aws_sdk_kinesis::types::EncryptionType::None)
                    .open_shard_count(1)
                    .set_enhanced_monitoring(Some(vec![]))
                    .build()
                    .unwrap(),
            )
            .build()
    }

    #[tokio::test]
    async fn create_stream_info_when_valid_returns_true() {
        let rule = mock!(KinesisClient::describe_stream_summary).then_output(describe_response);
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[&rule]);

        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_create_coordinator_state_if_not_exists()
            .returning(|_| Ok(true));

        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        assert!(dao.create_stream_info(&stream_identifier()).await.unwrap());
    }

    #[tokio::test]
    async fn create_stream_info_when_dao_create_fails_returns_false() {
        let rule = mock!(KinesisClient::describe_stream_summary).then_output(describe_response);
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[&rule]);

        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_create_coordinator_state_if_not_exists()
            .returning(|_| Ok(false));

        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        assert!(!dao.create_stream_info(&stream_identifier()).await.unwrap());
    }

    #[tokio::test]
    async fn create_stream_info_with_null_stream_id_returns_invalid_state() {
        let rule = mock!(KinesisClient::describe_stream_summary).then_output(|| {
            DescribeStreamSummaryOutput::builder()
                .stream_description_summary(
                    StreamDescriptionSummary::builder()
                        .stream_arn(STREAM_ARN)
                        .stream_name("test-stream")
                        // stream_id intentionally omitted — this is the null-stream-id case.
                        .stream_status(aws_sdk_kinesis::types::StreamStatus::Active)
                        .retention_period_hours(24)
                        .stream_creation_timestamp(aws_smithy_types::DateTime::from_secs(0))
                        .encryption_type(aws_sdk_kinesis::types::EncryptionType::None)
                        .open_shard_count(1)
                        .set_enhanced_monitoring(Some(vec![]))
                        .build()
                        .unwrap(),
                )
                .build()
        });
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[&rule]);
        let coord = MockCoordinatorStateAccess::new();
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        let err = dao
            .create_stream_info(&stream_identifier())
            .await
            .unwrap_err();
        assert!(matches!(err, LeasingError::InvalidState { .. }));
    }

    #[tokio::test]
    async fn create_stream_info_retries_on_limit_exceeded_then_succeeds() {
        let fail = mock!(KinesisClient::describe_stream_summary).then_error(|| {
            DescribeStreamSummaryError::LimitExceededException(
                LimitExceededException::builder().build(),
            )
        });
        let ok = mock!(KinesisClient::describe_stream_summary).then_output(describe_response);
        // Sequential: first call fails, second succeeds.
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::Sequential, &[&fail, &ok]);

        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_create_coordinator_state_if_not_exists()
            .returning(|_| Ok(true));

        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        assert!(dao.create_stream_info(&stream_identifier()).await.unwrap());
    }

    #[tokio::test]
    async fn create_stream_info_with_non_retryable_error_returns_dependency() {
        // Any DescribeStreamSummary error other than LimitExceededException aborts
        // immediately as LeasingError::Dependency (ResourceNotFound stands in for
        // the Java test's generic non-retryable Kinesis error).
        let rule = mock!(KinesisClient::describe_stream_summary).then_error(|| {
            DescribeStreamSummaryError::ResourceNotFoundException(
                ResourceNotFoundException::builder()
                    .message("missing")
                    .build(),
            )
        });
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[&rule]);
        let coord = MockCoordinatorStateAccess::new();
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        let err = dao
            .create_stream_info(&stream_identifier())
            .await
            .unwrap_err();
        assert!(matches!(err, LeasingError::Dependency { .. }));
    }

    #[tokio::test]
    async fn get_stream_info_when_exists_returns_it() {
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[]);
        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_get_coordinator_state()
            .with(eq("test-stream"))
            .returning(|_| {
                Ok(Some(CoordinatorState::StreamInfo(StreamInfo::new(
                    "test-stream",
                    STREAM_ID,
                ))))
            });
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        let result = dao.get_stream_info("test-stream").await.unwrap().unwrap();
        assert_eq!(result.key(), "test-stream");
        assert_eq!(result.stream_id(), STREAM_ID);
    }

    #[tokio::test]
    async fn get_stream_info_when_not_found_returns_none() {
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[]);
        let mut coord = MockCoordinatorStateAccess::new();
        coord.expect_get_coordinator_state().returning(|_| Ok(None));
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        assert!(dao.get_stream_info("non-existent").await.unwrap().is_none());
    }

    #[tokio::test]
    async fn get_stream_info_propagates_provisioned_throughput() {
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[]);
        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_get_coordinator_state()
            .returning(|_| Err(LeasingError::provisioned_throughput("Throughput exceeded")));
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        let err = dao.get_stream_info("test-key").await.unwrap_err();
        assert!(matches!(err, LeasingError::ProvisionedThroughput { .. }));
    }

    #[tokio::test]
    async fn list_stream_info_returns_stream_list() {
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[]);
        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_list_coordinator_state_by_entity_type()
            .returning(|_| {
                Ok(vec![
                    CoordinatorState::StreamInfo(StreamInfo::new("stream-id-key1", "stream1")),
                    CoordinatorState::StreamInfo(StreamInfo::new("stream-id-key2", "stream2")),
                ])
            });
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        let result = dao.list_stream_info().await.unwrap();
        assert_eq!(result.len(), 2);
        assert_eq!(result[0].key(), "stream-id-key1");
        assert_eq!(result[1].key(), "stream-id-key2");
    }

    #[tokio::test]
    async fn list_stream_info_propagates_provisioned_throughput() {
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[]);
        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_list_coordinator_state_by_entity_type()
            .returning(|_| Err(LeasingError::provisioned_throughput("Throughput exceeded")));
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        assert!(matches!(
            dao.list_stream_info().await.unwrap_err(),
            LeasingError::ProvisionedThroughput { .. }
        ));
    }

    #[tokio::test]
    async fn delete_stream_info_returns_dao_result() {
        let kinesis = mock_client!(aws_sdk_kinesis, RuleMode::MatchAny, &[]);
        let mut coord = MockCoordinatorStateAccess::new();
        coord
            .expect_delete_coordinator_state()
            .with(eq("test-stream"))
            .returning(|_| Ok(true));
        let dao = StreamInfoDAO::new(Arc::new(coord), kinesis);
        assert!(dao.delete_stream_info("test-stream").await.unwrap());
    }

    use aws_sdk_kinesis::operation::describe_stream_summary::DescribeStreamSummaryError;
}
