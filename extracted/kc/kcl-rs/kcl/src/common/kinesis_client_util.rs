//! Port of `software.amazon.kinesis.common.KinesisClientUtil`.
//!
//! Utility to configure a Kinesis async client with KCL's recommended HTTP
//! tuning for the long-lived `SubscribeToShard` HTTP/2 streaming RPC.
//!
//! # Deviation from Java — HTTP-client config does not map 1:1 to the Rust SDK
//!
//! The Java version wires an AWS-SDK-for-Java-v2 / Netty
//! (`NettyNioAsyncHttpClient`) HTTP client with:
//! - `maxConcurrency = Integer.MAX_VALUE`,
//! - HTTP/2 with `initialWindowSize = 512 KB` ([`INITIAL_WINDOW_SIZE_BYTES`]),
//! - `healthCheckPingPeriod = 60 s` ([`HEALTH_CHECK_PING_PERIOD_MILLIS`]),
//! - forced `Protocol.HTTP2`.
//!
//! The Rust AWS SDK uses a different HTTP stack (`aws-smithy-runtime` over
//! `hyper`). As of the pinned SDK versions, its default HTTP connector
//! **does not expose** equivalent knobs for the HTTP/2 initial window size,
//! per-connection health-check ping period, or a forced-HTTP/2 protocol
//! selector, and there is no `maxConcurrency` cap analogous to Netty's. These
//! three tuning constants are therefore preserved here **as documented
//! constants** (so the intent and exact values are not lost) but are **not
//! applied** to a Rust client builder — this is a known gap flagged for the
//! retrieval / fan-out wave, where the SubscribeToShard streaming path may need
//! a custom `hyper`-based connector to restore adequate flow-control window
//! sizing.
//!
//! [`create_kinesis_async_client`] is consequently a pass-through that documents
//! the intended tuning rather than transliterating the Netty wiring.

use aws_sdk_kinesis::config::Builder as KinesisConfigBuilder;

/// HTTP/2 initial window size KCL configures on the Kinesis client (512 KB).
///
/// Load-bearing for SubscribeToShard streaming throughput/backpressure. See the
/// module-level deviation note: not applied to the Rust HTTP stack yet.
pub const INITIAL_WINDOW_SIZE_BYTES: i32 = 512 * 1024;

/// HTTP/2 health-check ping period KCL configures on the Kinesis client (60 s,
/// in milliseconds).
///
/// See the module-level deviation note: not applied to the Rust HTTP stack yet.
pub const HEALTH_CHECK_PING_PERIOD_MILLIS: i64 = 60 * 1000;

/// Adjust a Kinesis `config::Builder` with KCL's recommended HTTP tuning.
///
/// Java sets a Netty HTTP/2 client with the tuning above. The Rust SDK exposes
/// no equivalent knobs (see the module deviation note), so this returns the
/// builder unchanged. Kept for API fidelity and as the single documented place
/// where the HTTP tuning would be applied if/when the Rust SDK gains the knobs.
pub fn adjust_kinesis_client_builder(builder: KinesisConfigBuilder) -> KinesisConfigBuilder {
    // TODO(port): apply INITIAL_WINDOW_SIZE_BYTES / HEALTH_CHECK_PING_PERIOD_MILLIS /
    // forced HTTP/2 / unbounded max-concurrency once the Rust SDK / hyper connector
    // exposes equivalent settings (retrieval/fan-out wave).
    builder
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tuning_constants_match_java() {
        assert_eq!(INITIAL_WINDOW_SIZE_BYTES, 524_288);
        assert_eq!(HEALTH_CHECK_PING_PERIOD_MILLIS, 60_000);
    }

    #[test]
    fn adjust_is_a_passthrough() {
        // Should compile and not panic; returns a usable builder.
        let _b = adjust_kinesis_client_builder(KinesisConfigBuilder::default());
    }
}
