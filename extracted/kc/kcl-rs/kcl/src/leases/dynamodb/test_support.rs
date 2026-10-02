//! Test-only helpers for building a mock `aws_sdk_dynamodb::Client` backed by
//! [`aws_smithy_mocks`], used by the `leases::dynamodb` behavioral tests.
//!
//! The Java tests mock `DynamoDbAsyncClient` (via Mockito) or run an embedded
//! DynamoDB. In Rust we inject canned responses/errors into a *real*
//! `aws_sdk_dynamodb::Client` via the smithy mock interceptor, then assert on the
//! `LeaseRefresher`/DAO behavior.

use aws_sdk_dynamodb::Client;
use aws_smithy_mocks::{mock_client, Rule, RuleMode};

/// Build a mock DynamoDB client that replays the given rules in order.
///
/// Uses [`RuleMode::Sequential`]: rules are consumed in sequence as matching
/// requests arrive (mirroring Mockito's chained `thenReturn` semantics).
pub fn mock_ddb_client(rules: &[&Rule]) -> Client {
    mock_client!(aws_sdk_dynamodb, RuleMode::Sequential, rules)
}

/// Build a mock DynamoDB client that matches **any** applicable rule (regardless
/// of order), consuming each rule only once it is exhausted. Use this when a rule
/// must satisfy an unbounded number of calls of one operation (e.g. per-segment
/// parallel scans) — pair with `.sequence()...repeatedly()` rules.
pub fn mock_ddb_client_match_any(rules: &[&Rule]) -> Client {
    mock_client!(aws_sdk_dynamodb, RuleMode::MatchAny, rules)
}
