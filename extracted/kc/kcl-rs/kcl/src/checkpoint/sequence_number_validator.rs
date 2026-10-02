//! Port of `software.amazon.kinesis.checkpoint.SequenceNumberValidator`.

use num_bigint::BigInt;
use num_bigint::Sign;

/// Supports extracting the `shardId` from a sequence number.
///
/// # Warning
///
/// **Sequence numbers are an opaque value used by Kinesis, and may be changed
/// at any time. Should validation stop working you may need to update your
/// version of the KCL.**
///
/// This is a stateless, pure value type (Java has no fields either — the
/// reader list is a `static final` singleton). It is constructed with
/// [`SequenceNumberValidator::new`].
#[derive(Debug, Default, Clone, Copy)]
pub struct SequenceNumberValidator;

/// The decoded `(version, shardId)` components of a sequence number.
///
/// Port of the private `SequenceNumberComponents` `@Data` class.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct SequenceNumberComponents {
    version: i32,
    shard_id: i32,
}

// --- V2 sequence-number reader constants (Kinesis wire format). ---

const V2_VERSION: i32 = 2;
const V2_EXPECTED_BIT_LENGTH: u64 = 186;
const V2_VERSION_OFFSET: u64 = 184;
const V2_VERSION_MASK: u64 = (1 << 4) - 1;
const V2_SHARD_ID_OFFSET: u64 = 4;
const V2_SHARD_ID_MASK: u64 = (1u64 << 32) - 1;

/// Read the v2 sequence-number format: parse the decimal string as a
/// [`BigInt`], require an exact bit length of 186, read the 4-bit version at
/// bit offset 184 (must equal 2), then read the 32-bit shardId at bit offset 4.
///
/// Returns `None` for any sequence number that does not parse as a v2 value
/// (wrong length, non-numeric, or version mismatch) — treated the same as an
/// unknown/unsupported sequence number.
fn read_v2(sequence_number_string: &str) -> Option<SequenceNumberComponents> {
    // Java `new BigInteger(sequenceNumberString, 10)` throws NumberFormatException
    // on non-numeric input. In the caller this would propagate; the tests only
    // feed numeric strings. `parse` returns None for non-numeric, which is a
    // superset of the tested behavior (empty Optional = unknown), so we treat a
    // parse failure as "unknown sequence number".
    let sequence_number: BigInt = sequence_number_string.parse().ok()?;

    //
    // If the bit length of the sequence number isn't 186 it's impossible for the
    // version numbers to be where we expect them. We treat this the same as an
    // unknown version of the sequence number.
    //
    if bit_length(&sequence_number) != V2_EXPECTED_BIT_LENGTH {
        return None;
    }

    //
    // Read the 4 most significant bits of the sequence number, the 2 most
    // significant bits are implicitly 0 (2 == 0b0010). If the version number
    // doesn't match we give up and say we can't parse the sequence number.
    //
    let version = read_offset(&sequence_number, V2_VERSION_OFFSET, V2_VERSION_MASK);
    if version != V2_VERSION {
        return None;
    }

    //
    // If we get here the sequence number is big enough, and the version matches
    // so the shardId should be valid.
    //
    let shard_id = read_offset(&sequence_number, V2_SHARD_ID_OFFSET, V2_SHARD_ID_MASK);
    Some(SequenceNumberComponents { version, shard_id })
}

/// Java `sequenceNumber.shiftRight(offset).longValue() & mask`, truncated to an
/// `int`.
fn read_offset(sequence_number: &BigInt, offset: u64, mask: u64) -> i32 {
    // shiftRight by `offset`, then take the low 64 bits (Java `longValue()`),
    // then mask. All extracted fields (version/shardId) fit in 32 bits.
    let shifted = sequence_number >> offset;
    let value = big_int_low_u64(&shifted) & mask;
    // Java casts `(int) value`; the masked value here always fits in an i32.
    value as i32
}

/// Java `BigInteger.bitLength()`: the number of bits in the minimal two's-complement
/// representation excluding the sign bit. For the non-negative values here this is
/// the position of the highest set bit.
fn bit_length(value: &BigInt) -> u64 {
    match value.sign() {
        Sign::NoSign => 0,
        _ => value.bits(),
    }
}

/// The low 64 bits of a non-negative [`BigInt`] (Java `BigInteger.longValue()`
/// keeps the low-order 64 bits). Sufficient here because every masked field is
/// at a low bit offset.
fn big_int_low_u64(value: &BigInt) -> u64 {
    // `to_u64_digits` returns little-endian u64 limbs; the first limb is the low
    // 64 bits. An all-zero value yields an empty vec.
    let (_sign, digits) = value.to_u64_digits();
    digits.first().copied().unwrap_or(0)
}

impl SequenceNumberValidator {
    /// Construct a validator.
    pub fn new() -> Self {
        Self
    }

    /// Find the components of a sequence number by trying each supported reader
    /// and returning the first that succeeds. (Only the v2 reader is supported;
    /// v1 sequence numbers are no longer used or available.)
    fn retrieve_components_for(&self, sequence_number: &str) -> Option<SequenceNumberComponents> {
        read_v2(sequence_number)
    }

    /// Attempts to retrieve the version for a sequence number.
    ///
    /// Returns `None` if the version cannot be extracted — either because Kinesis
    /// has started using a new sequence-number version or because the provided
    /// value is not a valid Kinesis sequence number.
    pub fn version_for(&self, sequence_number: &str) -> Option<i32> {
        self.retrieve_components_for(sequence_number)
            .map(|c| c.version)
    }

    /// Attempts to retrieve the `shardId` from a sequence number, formatted as
    /// `shardId-%012d`.
    ///
    /// Returns `None` if the sequence number version is unsupported. This should
    /// always return a value if [`version_for`](Self::version_for) does.
    pub fn shard_id_for(&self, sequence_number: &str) -> Option<String> {
        self.retrieve_components_for(sequence_number)
            .map(|c| format!("shardId-{:012}", c.shard_id))
    }

    /// Validates that the sequence number contains the given `shard_id`.
    ///
    /// * `Some(true)` — the sequence number parsed and its shardId matches.
    /// * `Some(false)` — the sequence number parsed but the shardId doesn't match.
    /// * `None` — the sequence number could not be parsed (validity unknown).
    ///
    /// The comparison is case-insensitive (Java `StringUtils.equalsIgnoreCase`).
    pub fn validate_sequence_number_for_shard(
        &self,
        sequence_number: &str,
        shard_id: &str,
    ) -> Option<bool> {
        self.shard_id_for(sequence_number)
            .map(|s| s.eq_ignore_ascii_case(shard_id))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn validator() -> SequenceNumberValidator {
        SequenceNumberValidator::new()
    }

    #[test]
    fn matching_sequence_number() {
        let sequence_number = "49587497311274533994574834252742144236107130636007899138";
        let expected_shard_id = "shardId-000000000000";

        assert_eq!(validator().version_for(sequence_number), Some(2));
        assert_eq!(
            validator().shard_id_for(sequence_number),
            Some(expected_shard_id.to_string())
        );
        assert_eq!(
            validator().validate_sequence_number_for_shard(sequence_number, expected_shard_id),
            Some(true)
        );
    }

    #[test]
    fn shard_mismatch() {
        let sequence_number = "49585389983312162443796657944872008114154899568972529698";
        let invalid_shard_id = "shardId-000000000001";

        assert_eq!(validator().version_for(sequence_number), Some(2));
        assert_ne!(
            validator().shard_id_for(sequence_number),
            Some(invalid_shard_id.to_string())
        );
        assert_eq!(
            validator().validate_sequence_number_for_shard(sequence_number, invalid_shard_id),
            Some(false)
        );
    }

    #[test]
    fn version_mismatch() {
        let sequence_number = "74107425965128755728308386687147091174006956590945533954";
        let expected_shard_id = "shardId-000000000000";

        assert_eq!(validator().version_for(sequence_number), None);
        assert_eq!(validator().shard_id_for(sequence_number), None);
        assert_eq!(
            validator().validate_sequence_number_for_shard(sequence_number, expected_shard_id),
            None
        );
    }

    #[test]
    fn sequence_number_too_short() {
        let sequence_number = "4958538998331216244379665794487200811415489956897252969";
        let expected_shard_id = "shardId-000000000000";

        assert_eq!(validator().version_for(sequence_number), None);
        assert_eq!(validator().shard_id_for(sequence_number), None);
        assert_eq!(
            validator().validate_sequence_number_for_shard(sequence_number, expected_shard_id),
            None
        );
    }

    #[test]
    fn sequence_number_too_long() {
        let sequence_number = "495874973112745339945748342527421442361071306360078991381";
        let expected_shard_id = "shardId-000000000000";

        assert_eq!(validator().version_for(sequence_number), None);
        assert_eq!(validator().shard_id_for(sequence_number), None);
        assert_eq!(
            validator().validate_sequence_number_for_shard(sequence_number, expected_shard_id),
            None
        );
    }
}
