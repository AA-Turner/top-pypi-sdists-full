//! Port of `software.amazon.kinesis.retrieval.ConsumerRegistration`.

use async_trait::async_trait;

use crate::leases::exceptions::LeasingError;

/// Abstraction for obtaining or creating an EFO (enhanced fan-out) stream
/// consumer ARN.
///
/// Port of the Java interface. The sole implementation is
/// `fanout.FanOutConsumerRegistration` (fan-out wave). Async because it makes
/// `DescribeStreamConsumer` / `RegisterStreamConsumer` calls; the Java
/// `throws DependencyException` maps to
/// `Result<_, LeasingError>` (`DependencyException` is a `LeasingException`
/// subclass → [`LeasingError::Dependency`]).
///
/// [`LeasingError::Dependency`]: crate::leases::exceptions::LeasingError::Dependency
#[async_trait]
pub trait ConsumerRegistration: Send + Sync {
    /// Get or create the `StreamConsumer` in Kinesis, returning its ARN.
    ///
    /// Port of `getOrCreateStreamConsumerArn()`.
    async fn get_or_create_stream_consumer_arn(&self) -> Result<String, LeasingError>;
}
