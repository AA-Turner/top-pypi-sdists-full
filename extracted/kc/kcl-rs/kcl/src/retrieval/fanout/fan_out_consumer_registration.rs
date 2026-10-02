//! Port of `software.amazon.kinesis.retrieval.fanout.FanOutConsumerRegistration`.
//!
//! Idempotently discovers or creates (registers) an EFO stream consumer and polls
//! until it is `ACTIVE`, with retry/backoff on throttling.
//!
//! # Async deviation
//!
//! Java blocks each async SDK call via `CompletableFuture.get()`. The Rust port
//! `.await`s and uses `tokio::time::sleep` for backoff, preserving the retry
//! counts + backoff durations + jitter (`retryBackoffMillis + rand(0..100)`) and
//! the error taxonomy (`LimitExceededException` → retry;
//! `ResourceNotFoundException` → create; `ResourceInUseException` → re-describe;
//! others → `DependencyException`).

use std::sync::Mutex;
use std::time::Duration;

use async_trait::async_trait;

use crate::leases::exceptions::LeasingError;
use crate::retrieval::consumer_registration::ConsumerRegistration;

/// The three Kinesis error classes the state machine reacts to.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ConsumerErrorKind {
    LimitExceeded,
    ResourceInUse,
    ResourceNotFound,
    Other,
}

fn classify<E: std::error::Error + 'static>(err: &E) -> ConsumerErrorKind {
    let mut cur: Option<&(dyn std::error::Error + 'static)> = Some(err);
    while let Some(e) = cur {
        let name = std::any::type_name_of_val(e);
        let msg = e.to_string();
        if name.contains("LimitExceeded") || msg.contains("LimitExceeded") {
            return ConsumerErrorKind::LimitExceeded;
        }
        if name.contains("ResourceInUse") || msg.contains("ResourceInUse") {
            return ConsumerErrorKind::ResourceInUse;
        }
        if name.contains("ResourceNotFound") || msg.contains("ResourceNotFound") {
            return ConsumerErrorKind::ResourceNotFound;
        }
        cur = e.source();
    }
    ConsumerErrorKind::Other
}

/// EFO consumer registration/discovery over the async Kinesis client.
///
/// Port of the Java `@RequiredArgsConstructor` class.
pub struct FanOutConsumerRegistration {
    kinesis_client: aws_sdk_kinesis::Client,
    stream_name: String,
    stream_consumer_name: String,
    max_describe_stream_summary_retries: i32,
    max_describe_stream_consumer_retries: i32,
    register_stream_consumer_retries: i32,
    retry_backoff: Duration,

    // Memoized state (Java fields).
    stream_arn: Mutex<Option<String>>,
    stream_consumer_arn: Mutex<Option<String>>,
}

impl FanOutConsumerRegistration {
    /// Construct.
    pub fn new(
        kinesis_client: aws_sdk_kinesis::Client,
        stream_name: impl Into<String>,
        stream_consumer_name: impl Into<String>,
        max_describe_stream_summary_retries: i32,
        max_describe_stream_consumer_retries: i32,
        register_stream_consumer_retries: i32,
        retry_backoff_millis: u64,
    ) -> Self {
        Self {
            kinesis_client,
            stream_name: stream_name.into(),
            stream_consumer_name: stream_consumer_name.into(),
            max_describe_stream_summary_retries,
            max_describe_stream_consumer_retries,
            register_stream_consumer_retries,
            retry_backoff: Duration::from_millis(retry_backoff_millis),
            stream_arn: Mutex::new(None),
            stream_consumer_arn: Mutex::new(None),
        }
    }

    fn cached_arn(&self) -> Option<String> {
        self.stream_consumer_arn.lock().unwrap().clone()
    }

    fn set_arn(&self, arn: String) {
        *self.stream_consumer_arn.lock().unwrap() = Some(arn);
    }

    /// Resolve the stream ARN via `describeStreamSummary` (memoized, with throttle
    /// retry). Java `streamArn()` / `getStreamARNAndStreamId()`.
    async fn stream_arn(&self) -> Result<String, LeasingError> {
        if let Some(arn) = self.stream_arn.lock().unwrap().clone() {
            return Ok(arn);
        }
        let mut retries = self.max_describe_stream_summary_retries;
        loop {
            let result = self
                .kinesis_client
                .describe_stream_summary()
                .stream_name(&self.stream_name)
                .send()
                .await;
            match result {
                Ok(resp) => {
                    let arn = resp
                        .stream_description_summary()
                        .map(|s| s.stream_arn().to_string())
                        .unwrap_or_default();
                    *self.stream_arn.lock().unwrap() = Some(arn.clone());
                    return Ok(arn);
                }
                Err(e) => {
                    if classify(&e) == ConsumerErrorKind::LimitExceeded && retries > 1 {
                        self.backoff_with_jitter().await;
                        retries -= 1;
                        continue;
                    }
                    if classify(&e) == ConsumerErrorKind::LimitExceeded {
                        return Err(LeasingError::provisioned_throughput(
                            "DescribeStreamSummary throttled after all retries",
                        ));
                    }
                    return Err(LeasingError::dependency(format!(
                        "DescribeStreamSummary failed: {e}"
                    )));
                }
            }
        }
    }

    async fn backoff_with_jitter(&self) {
        use rand::RngExt;
        let jitter = rand::rng().random_range(0..100);
        tokio::time::sleep(self.retry_backoff + Duration::from_millis(jitter)).await;
    }

    /// `describeStreamConsumer` with throttle retry. Returns
    /// `Ok(Some((arn, is_active)))` on success, `Ok(None)` if not found,
    /// `Err` on dependency failure.
    async fn describe_stream_consumer(&self) -> Result<Option<(String, bool)>, LeasingError> {
        let mut retries = self.max_describe_stream_consumer_retries;
        loop {
            let arn = self.cached_arn();
            let mut builder = self.kinesis_client.describe_stream_consumer();
            builder = if let Some(arn) = &arn {
                builder.consumer_arn(arn)
            } else {
                let stream_arn = self.stream_arn().await?;
                builder
                    .stream_arn(stream_arn)
                    .consumer_name(&self.stream_consumer_name)
            };
            match builder.send().await {
                Ok(resp) => {
                    let desc = resp.consumer_description();
                    let arn = desc
                        .map(|d| d.consumer_arn().to_string())
                        .unwrap_or_default();
                    let is_active = desc
                        .map(|d| {
                            *d.consumer_status() == aws_sdk_kinesis::types::ConsumerStatus::Active
                        })
                        .unwrap_or(false);
                    return Ok(Some((arn, is_active)));
                }
                Err(e) => match classify(&e) {
                    ConsumerErrorKind::ResourceNotFound => return Ok(None),
                    ConsumerErrorKind::LimitExceeded if retries > 1 => {
                        self.backoff_with_jitter().await;
                        retries -= 1;
                        continue;
                    }
                    ConsumerErrorKind::LimitExceeded => {
                        return Err(LeasingError::provisioned_throughput(
                            "DescribeStreamConsumer throttled after all retries",
                        ));
                    }
                    _ => {
                        return Err(LeasingError::dependency(format!(
                            "DescribeStreamConsumer failed: {e}"
                        )))
                    }
                },
            }
        }
    }

    /// `registerStreamConsumer` (no backoff between attempts — Java asymmetry).
    /// Returns `Ok(Some(arn))` on success, `Ok(None)` if it already exists
    /// (`ResourceInUse`), `Err` if throttled through all retries.
    async fn register_stream_consumer(&self) -> Result<Option<String>, LeasingError> {
        let mut retries = self.register_stream_consumer_retries;
        // Tracks whether the most recent failure was a throttle (Java's
        // `finalException`), read after the retry budget is exhausted.
        let mut throttled = false;
        while retries > 0 {
            let stream_arn = self.stream_arn().await?;
            let result = self
                .kinesis_client
                .register_stream_consumer()
                .stream_arn(stream_arn)
                .consumer_name(&self.stream_consumer_name)
                .send()
                .await;
            match result {
                Ok(resp) => {
                    let arn = resp
                        .consumer()
                        .map(|c| c.consumer_arn().to_string())
                        .unwrap_or_default();
                    return Ok(Some(arn));
                }
                Err(e) => match classify(&e) {
                    ConsumerErrorKind::LimitExceeded => {
                        // No sleep between register attempts (Java asymmetry).
                        throttled = true;
                    }
                    ConsumerErrorKind::ResourceInUse => {
                        // Consumer now exists (race) — caller re-describes.
                        return Ok(None);
                    }
                    _ => {
                        return Err(LeasingError::dependency(format!(
                            "RegisterStreamConsumer failed: {e}"
                        )))
                    }
                },
            }
            retries -= 1;
        }
        if throttled {
            return Err(LeasingError::dependency(
                "RegisterStreamConsumer throttled after all retries",
            ));
        }
        Ok(None)
    }

    /// Poll `describeStreamConsumer` until `ACTIVE` (Java `waitForActive`).
    async fn wait_for_active(&self) -> Result<(), LeasingError> {
        let mut retries = self.max_describe_stream_consumer_retries;
        let mut active = false;
        while retries > 0 && !active {
            if let Some((arn, is_active)) = self.describe_stream_consumer().await? {
                self.set_arn(arn);
                if is_active {
                    active = true;
                    break;
                }
            }
            retries -= 1;
            tokio::time::sleep(self.retry_backoff).await;
        }
        if !active {
            return Err(LeasingError::invalid_state(format!(
                "Status of StreamConsumer {} was not ACTIVE after all retries.",
                self.stream_consumer_name
            )));
        }
        Ok(())
    }
}

#[async_trait]
impl ConsumerRegistration for FanOutConsumerRegistration {
    async fn get_or_create_stream_consumer_arn(&self) -> Result<String, LeasingError> {
        if let Some(arn) = self.cached_arn() {
            return Ok(arn);
        }

        // 1. Check if the consumer exists.
        let mut describe = self.describe_stream_consumer().await?;

        // 2. If not, register it (retry only on throttle; ResourceInUse → re-describe).
        if describe.is_none() {
            match self.register_stream_consumer().await? {
                Some(arn) => self.set_arn(arn),
                None => {
                    // ResourceInUse or throttle-exhausted-but-no-error: re-describe.
                    describe = self.describe_stream_consumer().await?;
                }
            }
        }

        // 3. If a describe response exists, cache it; ACTIVE → return early.
        if let Some((arn, is_active)) = describe {
            self.set_arn(arn.clone());
            if is_active {
                return Ok(arn);
            }
        }

        // 4. Otherwise poll until ACTIVE.
        self.wait_for_active().await?;
        Ok(self.cached_arn().unwrap_or_default())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::retrieval::polling::test_support::{
        mock_kinesis_client, mock_kinesis_client_match_any,
    };
    use aws_sdk_kinesis::operation::describe_stream_consumer::{
        DescribeStreamConsumerError, DescribeStreamConsumerOutput,
    };
    use aws_sdk_kinesis::operation::describe_stream_summary::DescribeStreamSummaryOutput;
    use aws_sdk_kinesis::operation::register_stream_consumer::{
        RegisterStreamConsumerError, RegisterStreamConsumerOutput,
    };
    use aws_sdk_kinesis::types::error::{LimitExceededException, ResourceNotFoundException};
    use aws_sdk_kinesis::types::{
        Consumer, ConsumerDescription, ConsumerStatus, StreamDescriptionSummary,
    };
    use aws_smithy_mocks::mock;

    const STREAM_NAME: &str = "TestStream";
    const CONSUMER_NAME: &str = "TestConsumer";
    const STREAM_ARN: &str = "arn:aws:kinesis:us-east-1:123456789012:stream/TestStream";
    const CONSUMER_ARN: &str = "TestConsumerArn";
    const BACKOFF_MILLIS: u64 = 5;

    fn dss_active() -> aws_smithy_mocks::Rule {
        mock!(aws_sdk_kinesis::Client::describe_stream_summary).then_output(|| {
            DescribeStreamSummaryOutput::builder()
                .stream_description_summary(
                    StreamDescriptionSummary::builder()
                        .stream_name(STREAM_NAME)
                        .stream_arn(STREAM_ARN)
                        .stream_status(aws_sdk_kinesis::types::StreamStatus::Active)
                        .retention_period_hours(24)
                        .stream_creation_timestamp(aws_smithy_types::DateTime::from_secs(0))
                        .set_enhanced_monitoring(Some(vec![]))
                        .open_shard_count(1)
                        .build()
                        .unwrap(),
                )
                .build()
        })
    }

    fn dsc_status(status: ConsumerStatus) -> DescribeStreamConsumerOutput {
        DescribeStreamConsumerOutput::builder()
            .consumer_description(
                ConsumerDescription::builder()
                    .consumer_name(CONSUMER_NAME)
                    .consumer_arn(CONSUMER_ARN)
                    .consumer_status(status)
                    .consumer_creation_timestamp(aws_smithy_types::DateTime::from_secs(0))
                    .stream_arn(STREAM_ARN)
                    .build()
                    .unwrap(),
            )
            .build()
    }

    fn registration(client: aws_sdk_kinesis::Client) -> FanOutConsumerRegistration {
        FanOutConsumerRegistration::new(client, STREAM_NAME, CONSUMER_NAME, 5, 5, 5, BACKOFF_MILLIS)
    }

    // Port of FanOutConsumerRegistrationTest.testConsumerAlreadyExists.
    #[tokio::test]
    async fn consumer_already_exists() {
        let dss = dss_active();
        let dsc = mock!(aws_sdk_kinesis::Client::describe_stream_consumer)
            .then_output(|| dsc_status(ConsumerStatus::Active));
        let register = mock!(aws_sdk_kinesis::Client::register_stream_consumer)
            .then_output(|| RegisterStreamConsumerOutput::builder().build());
        let client = mock_kinesis_client_match_any(&[&dss, &dsc, &register]);
        let reg = registration(client);
        let arn = reg.get_or_create_stream_consumer_arn().await.unwrap();
        assert_eq!(arn, CONSUMER_ARN);
    }

    // Port of FanOutConsumerRegistrationTest.testConsumerAlreadyExistsMultipleCalls
    // (caching): the second call returns the cached ARN without more SDK calls.
    #[tokio::test]
    async fn consumer_already_exists_caches() {
        let dss = dss_active();
        let dsc = mock!(aws_sdk_kinesis::Client::describe_stream_consumer)
            .then_output(|| dsc_status(ConsumerStatus::Active));
        let client = mock_kinesis_client_match_any(&[&dss, &dsc]);
        let reg = registration(client);
        assert_eq!(
            reg.get_or_create_stream_consumer_arn().await.unwrap(),
            CONSUMER_ARN
        );
        assert_eq!(
            reg.get_or_create_stream_consumer_arn().await.unwrap(),
            CONSUMER_ARN
        );
    }

    // Port of FanOutConsumerRegistrationTest.testNewRegisterStreamConsumer:
    // not-found → register (CREATING) → poll until ACTIVE.
    #[tokio::test]
    async fn new_register_then_active() {
        let dss = dss_active();
        // describeStreamConsumer: RNFE, then CREATING, then ACTIVE.
        let dsc = mock!(aws_sdk_kinesis::Client::describe_stream_consumer)
            .sequence()
            .error(|| {
                DescribeStreamConsumerError::ResourceNotFoundException(
                    ResourceNotFoundException::builder().message("nope").build(),
                )
            })
            .output(|| dsc_status(ConsumerStatus::Creating))
            .output(|| dsc_status(ConsumerStatus::Active))
            .build();
        let register = mock!(aws_sdk_kinesis::Client::register_stream_consumer).then_output(|| {
            RegisterStreamConsumerOutput::builder()
                .consumer(
                    Consumer::builder()
                        .consumer_name(CONSUMER_NAME)
                        .consumer_arn(CONSUMER_ARN)
                        .consumer_status(ConsumerStatus::Creating)
                        .consumer_creation_timestamp(aws_smithy_types::DateTime::from_secs(0))
                        .build()
                        .unwrap(),
                )
                .build()
        });
        let client = mock_kinesis_client_match_any(&[&dss, &dsc, &register]);
        let reg = registration(client);
        let arn = reg.get_or_create_stream_consumer_arn().await.unwrap();
        assert_eq!(arn, CONSUMER_ARN);
    }

    // Port of FanOutConsumerRegistrationTest.testStreamConsumerStuckInCreating:
    // never ACTIVE → IllegalStateException (InvalidState).
    #[tokio::test]
    async fn stuck_in_creating_errors() {
        let dss = dss_active();
        let dsc = mock!(aws_sdk_kinesis::Client::describe_stream_consumer)
            .then_output(|| dsc_status(ConsumerStatus::Creating));
        let client = mock_kinesis_client_match_any(&[&dss, &dsc]);
        let reg = registration(client);
        let err = reg.get_or_create_stream_consumer_arn().await.unwrap_err();
        assert!(
            matches!(err, LeasingError::InvalidState { .. }),
            "got {err:?}"
        );
    }

    // Port of FanOutConsumerRegistrationTest.testDescribeStreamConsumerThrottled:
    // repeated LimitExceededException → provisioned-throughput error after retries.
    #[tokio::test]
    async fn describe_throttled_exhausts_retries() {
        let dss = dss_active();
        let dsc = mock!(aws_sdk_kinesis::Client::describe_stream_consumer).then_error(|| {
            DescribeStreamConsumerError::LimitExceededException(
                LimitExceededException::builder()
                    .message("throttled")
                    .build(),
            )
        });
        // MatchAny so the throttle rule can be consumed repeatedly.
        let client = mock_kinesis_client_match_any(&[&dss, &dsc]);
        let reg = registration(client);
        let err = reg.get_or_create_stream_consumer_arn().await.unwrap_err();
        assert!(
            matches!(
                err,
                LeasingError::ProvisionedThroughput { .. } | LeasingError::Dependency { .. }
            ),
            "got {err:?}"
        );
    }

    // Port of FanOutConsumerRegistrationTest.testRegisterStreamConsumerThrottled:
    // not-found + register throttled through all retries → DependencyException.
    #[tokio::test]
    async fn register_throttled_exhausts_retries() {
        let dss = dss_active();
        let dsc = mock!(aws_sdk_kinesis::Client::describe_stream_consumer).then_error(|| {
            DescribeStreamConsumerError::ResourceNotFoundException(
                ResourceNotFoundException::builder().message("nope").build(),
            )
        });
        let register = mock!(aws_sdk_kinesis::Client::register_stream_consumer).then_error(|| {
            RegisterStreamConsumerError::LimitExceededException(
                LimitExceededException::builder()
                    .message("throttled")
                    .build(),
            )
        });
        let client = mock_kinesis_client_match_any(&[&dss, &dsc, &register]);
        let reg = registration(client);
        let err = reg.get_or_create_stream_consumer_arn().await.unwrap_err();
        assert!(
            matches!(err, LeasingError::Dependency { .. }),
            "got {err:?}"
        );
    }

    // Keep `mock_kinesis_client` referenced (Sequential mode helper).
    #[allow(dead_code)]
    fn _uses_sequential(rules: &[&aws_smithy_mocks::Rule]) -> aws_sdk_kinesis::Client {
        mock_kinesis_client(rules)
    }
}
