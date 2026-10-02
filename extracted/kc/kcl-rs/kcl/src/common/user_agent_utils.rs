//! Port of `software.amazon.kinesis.common.UserAgentUtils`.

use base64::Engine;
use sha2::{Digest, Sha256};

/// Prefix for the generated consumer id.
const CONSUMER_ID_PREFIX: &str = "KCL-ConsumerId-";

/// Derive a short, stable, hashed "consumer id" string from a DynamoDB table ARN.
///
/// Used to tag requests (e.g. via [`KinesisRequestsBuilder`]'s consumer-id
/// overloads) so that traffic from a given KCL deployment / lease table can be
/// distinguished in Kinesis-side telemetry.
///
/// Algorithm (must match the Java implementation byte-for-byte for
/// cross-implementation consistency):
/// 1. If `table_arn` is empty, return `None` (Java returns `null` and logs a
///    warning).
/// 2. Compute the SHA-256 digest of the UTF-8 bytes of `table_arn`.
/// 3. Base64-encode the digest (standard alphabet, **with** padding).
/// 4. Take the first `min(16, len)` characters of the Base64 string. Since a
///    Base64-of-SHA-256 is always 44 characters, this is always 16 characters.
/// 5. Prefix with `"KCL-ConsumerId-"`.
///
/// The Java `NoSuchAlgorithmException` branch is dead code here (`sha2` has no
/// fallible algorithm lookup), so it is not reproduced.
///
/// [`KinesisRequestsBuilder`]: crate::common::KinesisRequestsBuilder
pub fn generate_consumer_id(table_arn: &str) -> Option<String> {
    if table_arn.is_empty() {
        // Java logs a warning ("Table ARN is empty, cannot generate consumer ID")
        // and returns null.
        tracing::warn!("Table ARN is empty, cannot generate consumer ID");
        return None;
    }

    let mut hasher = Sha256::new();
    hasher.update(table_arn.as_bytes());
    let hash_bytes = hasher.finalize();
    let hash = base64::engine::general_purpose::STANDARD.encode(hash_bytes);
    // Use only a portion of the hash to keep the UserAgent header reasonably
    // sized. Base64 output is ASCII so byte-slicing is character-equivalent,
    // but mirror Java's Math.min guard for safety.
    let short_hash = &hash[..hash.len().min(16)];
    Some(format!("{}{}", CONSUMER_ID_PREFIX, short_hash))
}

/// Alias for [`generate_consumer_id`] (Java `getConsumerId`).
pub fn get_consumer_id(table_arn: &str) -> Option<String> {
    generate_consumer_id(table_arn)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_arn_returns_none() {
        assert_eq!(generate_consumer_id(""), None);
        assert_eq!(get_consumer_id(""), None);
    }

    #[test]
    fn deterministic_prefix_and_length() {
        let id =
            generate_consumer_id("arn:aws:dynamodb:us-east-1:123456789012:table/my-app").unwrap();
        assert!(id.starts_with("KCL-ConsumerId-"));
        // Prefix (15) + 16 chars of base64 hash = 31 chars total.
        assert_eq!(id.len(), CONSUMER_ID_PREFIX.len() + 16);
    }

    #[test]
    fn known_test_vector() {
        // SHA-256 of "test" = 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
        // Base64(standard, padded) of those 32 bytes = "n4bQgYhMfWWaL+qgxVrQFaO/TxsrC4Is0V1sFbDwCgg="
        // First 16 chars = "n4bQgYhMfWWaL+qg"
        let id = generate_consumer_id("test").unwrap();
        assert_eq!(id, "KCL-ConsumerId-n4bQgYhMfWWaL+qg");
    }

    #[test]
    fn get_consumer_id_delegates() {
        assert_eq!(
            get_consumer_id("arn:aws:dynamodb:us-east-1:123456789012:table/x"),
            generate_consumer_id("arn:aws:dynamodb:us-east-1:123456789012:table/x")
        );
    }
}
