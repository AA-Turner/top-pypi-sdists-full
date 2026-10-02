//! Port of `software.amazon.kinesis.lifecycle.ShutdownNotification`.

/// A shutdown request to the `ShardConsumer`.
///
/// Signals two distinct points in a graceful (worker-initiated) shutdown: when
/// the record processor has been notified and given a chance to checkpoint, and
/// when it has fully completed shutdown.
///
/// The concrete production implementation (`ShardConsumerShutdownNotification`,
/// coordinating `CountDownLatch`es with the `LeaseCoordinator`) is part of
/// sub-wave 7b; only the trait is ported here (it is what
/// [`ShutdownNotificationTask`](crate::lifecycle::ShutdownNotificationTask)
/// consumes).
pub trait ShutdownNotification: Send + Sync {
    /// Indicates the record processor has been notified of a requested shutdown
    /// and given the chance to checkpoint.
    fn shutdown_notification_complete(&self);

    /// Indicates the record processor has completed its `shutdown` call.
    fn shutdown_complete(&self);
}
