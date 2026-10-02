//! Port of `software.amazon.kinesis.common.HashKeyRangeForLease`.

use num_bigint::BigInt;

use aws_sdk_kinesis::types::HashKeyRange;

/// Lease POJO holding the starting and ending hash-key range of a Kinesis shard.
///
/// Java is a Lombok `@Value @Accessors(fluent = true)` — an immutable value type
/// with no-prefix fluent getters. The starting hash key must be strictly less
/// than the ending hash key; construction validates this (Java
/// `Validate.isTrue`, which throws `IllegalArgumentException` → `panic!` here).
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct HashKeyRangeForLease {
    starting_hash_key: BigInt,
    ending_hash_key: BigInt,
}

impl HashKeyRangeForLease {
    /// Construct a hash-key range.
    ///
    /// # Panics
    /// Panics (Java `IllegalArgumentException`) if `starting_hash_key` is not
    /// strictly less than `ending_hash_key`.
    pub fn new(starting_hash_key: BigInt, ending_hash_key: BigInt) -> Self {
        if starting_hash_key >= ending_hash_key {
            panic!(
                "StartingHashKey {} must be less than EndingHashKey {} ",
                starting_hash_key, ending_hash_key
            );
        }
        Self {
            starting_hash_key,
            ending_hash_key,
        }
    }

    /// The starting hash key.
    pub fn starting_hash_key(&self) -> &BigInt {
        &self.starting_hash_key
    }

    /// The ending hash key.
    pub fn ending_hash_key(&self) -> &BigInt {
        &self.ending_hash_key
    }

    /// Serialize the starting hash key for persisting in external storage.
    pub fn serialized_starting_hash_key(&self) -> String {
        self.starting_hash_key.to_string()
    }

    /// Serialize the ending hash key for persisting in external storage.
    pub fn serialized_ending_hash_key(&self) -> String {
        self.ending_hash_key.to_string()
    }

    /// Deserialize from serialized hash-key-range strings from external storage.
    ///
    /// # Panics
    /// Panics if either string is not a valid integer (Java `new BigInteger`
    /// throws `NumberFormatException`), or if the starting key is not strictly
    /// less than the ending key.
    pub fn deserialize(starting_hash_key_str: &str, ending_hash_key_str: &str) -> Self {
        let starting_hash_key: BigInt = starting_hash_key_str
            .parse()
            .expect("startingHashKey must be a valid integer");
        let ending_hash_key: BigInt = ending_hash_key_str
            .parse()
            .expect("endingHashKey must be a valid integer");
        if starting_hash_key >= ending_hash_key {
            panic!(
                "StartingHashKey {} must be less than EndingHashKey {} ",
                starting_hash_key_str, ending_hash_key_str
            );
        }
        Self {
            starting_hash_key,
            ending_hash_key,
        }
    }

    /// Construct from a Kinesis SDK `HashKeyRange`.
    pub fn from_hash_key_range(hash_key_range: &HashKeyRange) -> Self {
        Self::deserialize(
            hash_key_range.starting_hash_key(),
            hash_key_range.ending_hash_key(),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_and_accessors() {
        let r = HashKeyRangeForLease::new(BigInt::from(0), BigInt::from(100));
        assert_eq!(r.starting_hash_key(), &BigInt::from(0));
        assert_eq!(r.ending_hash_key(), &BigInt::from(100));
    }

    #[test]
    #[should_panic(expected = "must be less than EndingHashKey")]
    fn new_rejects_equal() {
        HashKeyRangeForLease::new(BigInt::from(5), BigInt::from(5));
    }

    #[test]
    #[should_panic(expected = "must be less than EndingHashKey")]
    fn new_rejects_reversed() {
        HashKeyRangeForLease::new(BigInt::from(10), BigInt::from(5));
    }

    #[test]
    fn serialize_round_trip() {
        // A full 128-bit range value to exercise BigInt beyond u64.
        let start = "0";
        let end = "340282366920938463463374607431768211455"; // 2^128 - 1
        let r = HashKeyRangeForLease::deserialize(start, end);
        assert_eq!(r.serialized_starting_hash_key(), start);
        assert_eq!(r.serialized_ending_hash_key(), end);
    }

    #[test]
    #[should_panic(expected = "must be less than EndingHashKey")]
    fn deserialize_validates_ordering() {
        HashKeyRangeForLease::deserialize("100", "50");
    }

    #[test]
    fn equality_over_both_fields() {
        let a = HashKeyRangeForLease::new(BigInt::from(0), BigInt::from(100));
        let b = HashKeyRangeForLease::deserialize("0", "100");
        assert_eq!(a, b);
        let c = HashKeyRangeForLease::new(BigInt::from(0), BigInt::from(200));
        assert_ne!(a, c);
    }
}
