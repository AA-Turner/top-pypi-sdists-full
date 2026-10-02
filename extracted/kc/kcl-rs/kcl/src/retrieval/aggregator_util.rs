//! Port of `software.amazon.kinesis.retrieval.AggregatorUtil`.
//!
//! De-aggregates KPL (Kinesis Producer Library) aggregated records into
//! individual [`KinesisClientRecord`] user records, filtering by hash-key range.
//!
//! An aggregated record's payload is: a 4-byte magic prefix
//! [`AGGREGATED_RECORD_MAGIC`], a protobuf [`AggregatedRecord`] body, and a
//! trailing 16-byte MD5 digest over the protobuf body. The wire format is a
//! cross-language (Java KCL / C++ KPL / this Rust port) compatibility concern, so
//! the magic bytes, MD5 usage, and 128-bit hash-key arithmetic are reproduced
//! exactly.

use bytes::Bytes;
use md5::{Digest, Md5};
use num_bigint::BigInt;
use num_bigint::Sign;

use crate::retrieval::kinesis_client_record::KinesisClientRecord;
use crate::retrieval::kpl::messages::AggregatedRecord;

/// The 4-byte magic prefix marking a KPL aggregated record.
///
/// Port of the Java `byte[] {-13, -119, -102, -62}` (signed bytes), i.e. the
/// unsigned bytes `0xF3 0x89 0x9A 0xC2`.
pub const AGGREGATED_RECORD_MAGIC: [u8; 4] = [0xF3, 0x89, 0x9A, 0xC2];

/// Size of the trailing MD5 digest.
const DIGEST_SIZE: usize = 16;

/// KPL record de-aggregator.
///
/// Port of the Java `AggregatorUtil` class. Stateless; kept as a unit struct so
/// callers can hold/share an instance exactly as Java does (and so the
/// `calculateTailCheck`/`effectiveHashKey` seams remain associated methods).
#[derive(Debug, Default, Clone, Copy)]
pub struct AggregatorUtil;

impl AggregatorUtil {
    /// Create a new de-aggregator.
    pub fn new() -> Self {
        Self
    }

    /// Starting hash key of the full 128-bit space (`0`).
    fn starting_hash_key() -> BigInt {
        BigInt::from(0)
    }

    /// Ending hash key of the full 128-bit space (`2^128 - 1`).
    fn ending_hash_key() -> BigInt {
        // 2^128 - 1
        (BigInt::from(1) << 128u32) - 1
    }

    /// De-aggregate over the full hash-key range `[0, 2^128 - 1]`.
    ///
    /// Port of `deaggregate(List<KinesisClientRecord>)`.
    pub fn deaggregate(&self, records: Vec<KinesisClientRecord>) -> Vec<KinesisClientRecord> {
        self.deaggregate_with_range(
            records,
            &Self::starting_hash_key(),
            &Self::ending_hash_key(),
        )
    }

    /// De-aggregate with `String`-typed hash-key bounds (parsed as decimal
    /// `BigInt`s). Port of `deaggregate(List, String, String)`.
    pub fn deaggregate_str(
        &self,
        records: Vec<KinesisClientRecord>,
        starting_hash_key: &str,
        ending_hash_key: &str,
    ) -> Vec<KinesisClientRecord> {
        let start: BigInt = starting_hash_key
            .parse()
            .expect("starting hash key must be a decimal integer");
        let end: BigInt = ending_hash_key
            .parse()
            .expect("ending hash key must be a decimal integer");
        self.deaggregate_with_range(records, &start, &end)
    }

    /// De-aggregate, discarding user records whose effective hash key falls
    /// outside `[starting_hash_key, ending_hash_key]`.
    ///
    /// Port of `deaggregate(List, BigInteger, BigInteger)`, preserving:
    /// * the magic + MD5-digest detection,
    /// * the rollback-current-aggregate-and-break on an out-of-range sub-record,
    /// * the sub-sequence-number increment only for retained records,
    /// * the pass-through (data start-of-buffer) of non-aggregated / malformed
    ///   records.
    pub fn deaggregate_with_range(
        &self,
        records: Vec<KinesisClientRecord>,
        starting_hash_key: &BigInt,
        ending_hash_key: &BigInt,
    ) -> Vec<KinesisClientRecord> {
        let mut result: Vec<KinesisClientRecord> = Vec::new();

        for r in records {
            // Java reads from a ByteBuffer with a moving position; here the data
            // is a `Bytes`, always read from offset 0 (the "rewind on
            // non-aggregated" semantic is implicit — the original `Bytes` is
            // pushed through unchanged).
            let data: &[u8] = r.data().map(|b| b.as_ref()).unwrap_or(&[]);
            let total = data.len();

            let mut is_aggregated = true;

            // Magic check: need at least 4 bytes for the magic, and the magic
            // must match, and there must be more than DIGEST_SIZE bytes after it.
            if total < AGGREGATED_RECORD_MAGIC.len() {
                is_aggregated = false;
            } else {
                let magic = &data[..AGGREGATED_RECORD_MAGIC.len()];
                let remaining_after_magic = total - AGGREGATED_RECORD_MAGIC.len();
                if magic != AGGREGATED_RECORD_MAGIC || remaining_after_magic <= DIGEST_SIZE {
                    is_aggregated = false;
                }
            }

            if is_aggregated {
                let magic_len = AGGREGATED_RECORD_MAGIC.len();
                let message_data = &data[magic_len..total - DIGEST_SIZE];
                let digest = &data[total - DIGEST_SIZE..];
                let calculated_digest = self.calculate_tail_check(message_data);

                if digest != calculated_digest.as_slice() {
                    is_aggregated = false;
                } else {
                    match AggregatedRecord::decode(message_data) {
                        Ok(ar) => {
                            let pks = &ar.partition_key_table;
                            let ehks = &ar.explicit_hash_key_table;
                            let mut sub_seq_num: i64 = 0;
                            // Tracks how many sub-records of THIS aggregate have
                            // been emitted, so an out-of-range record can roll
                            // exactly them back — a load-bearing count, not a
                            // pure loop index (clippy's suggestion would lose it).
                            let mut records_in_curr_record: usize = 0;

                            // Resolve a sub-record's keys, failing (instead of
                            // panicking) on a corrupt index table or explicit
                            // hash key — aggregate contents are producer-
                            // controlled input.
                            let resolve = |mr: &crate::retrieval::kpl::messages::Record| -> Result<(String, Option<String>, BigInt), String> {
                                let partition_key = pks
                                    .get(mr.partition_key_index as usize)
                                    .ok_or_else(|| {
                                        format!(
                                            "partition key index {} out of range ({} entries)",
                                            mr.partition_key_index,
                                            pks.len()
                                        )
                                    })?
                                    .clone();
                                let explicit_hash_key: Option<String> = mr
                                    .explicit_hash_key_index
                                    .map(|idx| {
                                        ehks.get(idx as usize).cloned().ok_or_else(|| {
                                            format!(
                                                "explicit hash key index {idx} out of range ({} entries)",
                                                ehks.len()
                                            )
                                        })
                                    })
                                    .transpose()?;
                                let effective_hash_key = self.effective_hash_key(
                                    &partition_key,
                                    explicit_hash_key.as_deref(),
                                )?;
                                Ok((partition_key, explicit_hash_key, effective_hash_key))
                            };

                            #[allow(clippy::explicit_counter_loop)]
                            for mr in &ar.records {
                                // Port of Java's inner `catch (Exception e)`
                                // around this loop: on a corrupt sub-record,
                                // log the aggregate dump and stop processing
                                // this aggregate, KEEPING the sub-records
                                // already emitted (no rollback, no
                                // pass-through of the raw aggregate).
                                let (partition_key, explicit_hash_key, effective_hash_key) =
                                    match resolve(mr) {
                                        Ok(v) => v,
                                        Err(cause) => {
                                            Self::log_deaggregation_error(
                                                &cause,
                                                &ar,
                                                message_data,
                                                r.sequence_number(),
                                            );
                                            break;
                                        }
                                    };

                                if &effective_hash_key < starting_hash_key
                                    || &effective_hash_key > ending_hash_key
                                {
                                    // Roll back the records added for THIS
                                    // aggregate record, then stop processing it.
                                    for _ in 0..records_in_curr_record {
                                        result.pop();
                                    }
                                    break;
                                }

                                records_in_curr_record += 1;

                                // Java builds `r.toBuilder().data(..).partitionKey(..)
                                // .explicitHashKey(..).build()` then passes it to
                                // convertRecordToKinesisClientRecord, which copies
                                // r's timestamp/encryptionType/sequenceNumber and the
                                // overridden data/partitionKey. We build the final
                                // record directly with the same net field set.
                                result.push(self.build_sub_record(
                                    &r,
                                    Bytes::copy_from_slice(&mr.data),
                                    &partition_key,
                                    sub_seq_num,
                                    explicit_hash_key.as_deref(),
                                ));
                                sub_seq_num += 1;
                            }
                        }
                        Err(_) => {
                            // Java: InvalidProtocolBufferException -> treat as
                            // non-aggregated (pass through unchanged).
                            is_aggregated = false;
                        }
                    }
                }
            }

            if !is_aggregated {
                result.push(r);
            }
        }

        result
    }

    /// Compute the trailing MD5 digest over the protobuf body (the "tail check").
    ///
    /// Port of `calculateTailCheck`; a protected seam in Java (overridden in the
    /// test to build a valid aggregate record).
    pub fn calculate_tail_check(&self, data: &[u8]) -> Vec<u8> {
        Self::md5(data)
    }

    /// Compute a sub-record's effective hash key: the explicit hash key if
    /// present (parsed as a decimal `BigInt`), else the unsigned `BigInt` of the
    /// MD5 of the partition key's UTF-8 bytes.
    ///
    /// Port of `effectiveHashKey`. A non-numeric explicit hash key is an `Err`
    /// (Java: `NumberFormatException`, caught by the de-aggregation loop's
    /// `catch (Exception)`), not a panic — it arrives from the producer.
    fn effective_hash_key(
        &self,
        partition_key: &str,
        explicit_hash_key: Option<&str>,
    ) -> Result<BigInt, String> {
        match explicit_hash_key {
            None => {
                // Java: new BigInteger(1, md5(partitionKey)) — a *positive*
                // (unsigned) big integer over the 16 MD5 bytes, big-endian.
                let digest = Self::md5(partition_key.as_bytes());
                Ok(BigInt::from_bytes_be(Sign::Plus, &digest))
            }
            Some(ehk) => ehk
                .parse()
                .map_err(|_| format!("explicit hash key {ehk:?} is not a decimal integer")),
        }
    }

    /// Log a corrupt sub-record inside an otherwise digest-valid aggregate.
    ///
    /// Port of the record dump Java builds in the de-aggregation loop's
    /// `catch (Exception e)` block (`log.error(sb.toString(), e)`).
    fn log_deaggregation_error(
        cause: &str,
        ar: &AggregatedRecord,
        message_data: &[u8],
        sequence_number: Option<&str>,
    ) {
        use base64::Engine;
        use std::fmt::Write;

        let mut sb = String::from("Unexpected exception during deaggregation, record was:\n");
        sb.push_str("PKS:\n");
        for s in &ar.partition_key_table {
            let _ = writeln!(sb, "{s}");
        }
        sb.push_str("EHKS: \n");
        for s in &ar.explicit_hash_key_table {
            let _ = writeln!(sb, "{s}");
        }
        for mr in &ar.records {
            let _ = writeln!(
                sb,
                "Record: [hasEhk={}, ehkIdx={}, pkIdx={}, dataLen={}]",
                mr.explicit_hash_key_index.is_some(),
                mr.explicit_hash_key_index.unwrap_or_default(),
                mr.partition_key_index,
                mr.data.len()
            );
        }
        let _ = writeln!(sb, "Sequence number: {}", sequence_number.unwrap_or(""));
        let _ = writeln!(
            sb,
            "Raw data: {}",
            base64::engine::general_purpose::STANDARD.encode(message_data)
        );
        tracing::error!(target: "kcl::retrieval", "{sb}{cause}");
    }

    fn md5(data: &[u8]) -> Vec<u8> {
        let mut hasher = Md5::new();
        hasher.update(data);
        hasher.finalize().to_vec()
    }

    /// Build a de-aggregated [`KinesisClientRecord`] from a per-record source,
    /// stamping the aggregation flag, sub-sequence number, and explicit hash key.
    ///
    /// Port of `convertRecordToKinesisClientRecord`: copies `record`'s data,
    /// partition key, approximate arrival timestamp, encryption type, and
    /// sequence number, then overrides the aggregation fields.
    pub fn convert_record_to_kinesis_client_record(
        &self,
        record: &KinesisClientRecord,
        aggregated: bool,
        sub_sequence_number: i64,
        explicit_hash_key: Option<&str>,
    ) -> KinesisClientRecord {
        KinesisClientRecord::builder()
            .maybe_data(record.data().cloned())
            .maybe_partition_key(record.partition_key().map(str::to_string))
            .maybe_approximate_arrival_timestamp(record.approximate_arrival_timestamp())
            .maybe_encryption_type(record.encryption_type().cloned())
            .maybe_sequence_number(record.sequence_number().map(str::to_string))
            .aggregated(aggregated)
            .sub_sequence_number(sub_sequence_number)
            .maybe_explicit_hash_key(explicit_hash_key.map(str::to_string))
            .build()
    }

    /// Build a single de-aggregated sub-record, inheriting the source record's
    /// timestamp / encryption type / sequence number while overriding the data,
    /// partition key, and explicit hash key.
    ///
    /// Mirrors Java's `r.toBuilder().data(..).partitionKey(..).explicitHashKey(..)
    /// .build()` followed by `convertRecordToKinesisClientRecord(record, true, ..)`.
    fn build_sub_record(
        &self,
        source: &KinesisClientRecord,
        data: Bytes,
        partition_key: &str,
        sub_sequence_number: i64,
        explicit_hash_key: Option<&str>,
    ) -> KinesisClientRecord {
        KinesisClientRecord::builder()
            .data(data)
            .partition_key(partition_key.to_string())
            .maybe_approximate_arrival_timestamp(source.approximate_arrival_timestamp())
            .maybe_encryption_type(source.encryption_type().cloned())
            .maybe_sequence_number(source.sequence_number().map(str::to_string))
            .aggregated(true)
            .sub_sequence_number(sub_sequence_number)
            .maybe_explicit_hash_key(explicit_hash_key.map(str::to_string))
            .build()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::retrieval::kpl::messages::Record as KplRecord;

    const AGGREGATOR: AggregatorUtil = AggregatorUtil;

    /// Wrap a KPL `AggregatedRecord` in the magic + protobuf + MD5 envelope,
    /// producing the payload bytes a real aggregated Kinesis record carries.
    fn envelope(ar: &AggregatedRecord) -> Bytes {
        let body = ar.encode_to_vec();
        let digest = AGGREGATOR.calculate_tail_check(&body);
        let mut buf = Vec::with_capacity(AGGREGATED_RECORD_MAGIC.len() + body.len() + digest.len());
        buf.extend_from_slice(&AGGREGATED_RECORD_MAGIC);
        buf.extend_from_slice(&body);
        buf.extend_from_slice(&digest);
        Bytes::from(buf)
    }

    fn aggregated_client_record(data: Bytes) -> KinesisClientRecord {
        KinesisClientRecord::builder()
            .data(data)
            .partition_key("agg-pk")
            .sequence_number("555")
            .build()
    }

    // Port of AggregatorUtilTest's `constructKplAggregatedRecord` shape: a
    // magic + arbitrary body + valid MD5 digest. Because the body is not a valid
    // protobuf `AggregatedRecord`, decode fails and the record is passed through.
    #[test]
    fn valid_envelope_but_invalid_protobuf_passes_through() {
        let message_data = b"test message";
        let digest = AGGREGATOR.calculate_tail_check(message_data);
        let mut buf = Vec::new();
        buf.extend_from_slice(&AGGREGATED_RECORD_MAGIC);
        buf.extend_from_slice(message_data);
        buf.extend_from_slice(&digest);
        let record = aggregated_client_record(Bytes::from(buf));
        let original = record.clone();

        let out = AGGREGATOR.deaggregate(vec![record]);
        assert_eq!(out.len(), 1);
        // Unchanged pass-through (decode failed -> not aggregated).
        assert_eq!(out[0], original);
    }

    #[test]
    fn non_aggregated_record_passes_through_unchanged() {
        let record = KinesisClientRecord::builder()
            .data(Bytes::from_static(b"just some data"))
            .partition_key("pk")
            .sequence_number("1")
            .build();
        let original = record.clone();
        let out = AGGREGATOR.deaggregate(vec![record]);
        assert_eq!(out, vec![original]);
    }

    #[test]
    fn short_record_passes_through_unchanged() {
        // Fewer than 4 bytes: cannot be aggregated.
        let record = KinesisClientRecord::builder()
            .data(Bytes::from_static(b"ab"))
            .partition_key("pk")
            .sequence_number("1")
            .build();
        let out = AGGREGATOR.deaggregate(vec![record]);
        assert_eq!(out.len(), 1);
        assert_eq!(out[0].data().unwrap().as_ref(), b"ab");
    }

    #[test]
    fn bad_digest_passes_through_unchanged() {
        let ar = AggregatedRecord {
            partition_key_table: vec!["pk0".to_string()],
            explicit_hash_key_table: vec![],
            records: vec![KplRecord {
                partition_key_index: 0,
                explicit_hash_key_index: None,
                data: b"payload".to_vec(),
                tags: vec![],
            }],
        };
        let body = ar.encode_to_vec();
        let mut buf = Vec::new();
        buf.extend_from_slice(&AGGREGATED_RECORD_MAGIC);
        buf.extend_from_slice(&body);
        // Corrupt/incorrect 16-byte digest.
        buf.extend_from_slice(&[0u8; 16]);
        let record = aggregated_client_record(Bytes::from(buf));
        let original = record.clone();
        let out = AGGREGATOR.deaggregate(vec![record]);
        assert_eq!(out, vec![original]);
    }

    // High-value de-aggregation round-trip: two user records inside one
    // aggregate, both using partition-key-derived hash keys (no explicit hash
    // keys), full hash-key range -> both retained with incrementing subseq.
    #[test]
    fn deaggregate_round_trip_two_user_records() {
        let ar = AggregatedRecord {
            partition_key_table: vec!["pk-a".to_string(), "pk-b".to_string()],
            explicit_hash_key_table: vec![],
            records: vec![
                KplRecord {
                    partition_key_index: 0,
                    explicit_hash_key_index: None,
                    data: b"user-record-1".to_vec(),
                    tags: vec![],
                },
                KplRecord {
                    partition_key_index: 1,
                    explicit_hash_key_index: None,
                    data: b"user-record-2".to_vec(),
                    tags: vec![],
                },
            ],
        };
        let record = aggregated_client_record(envelope(&ar));
        let out = AGGREGATOR.deaggregate(vec![record]);

        assert_eq!(out.len(), 2);
        assert_eq!(out[0].data().unwrap().as_ref(), b"user-record-1");
        assert_eq!(out[0].partition_key(), Some("pk-a"));
        assert!(out[0].aggregated());
        assert_eq!(out[0].sub_sequence_number(), 0);
        assert_eq!(out[0].sequence_number(), Some("555"));

        assert_eq!(out[1].data().unwrap().as_ref(), b"user-record-2");
        assert_eq!(out[1].partition_key(), Some("pk-b"));
        assert!(out[1].aggregated());
        assert_eq!(out[1].sub_sequence_number(), 1);
    }

    // Explicit hash keys drive the range filter: an out-of-range sub-record
    // rolls back all sub-records already emitted for the CURRENT aggregate and
    // stops processing it (subsequent aggregates would still be processed).
    #[test]
    fn out_of_range_explicit_hash_key_rolls_back_current_aggregate() {
        // Two records: first in-range (hash key "5"), second out-of-range
        // (hash key "9999") with range [0, 100]. The break rolls back the first.
        let ar = AggregatedRecord {
            partition_key_table: vec!["pk".to_string()],
            explicit_hash_key_table: vec!["5".to_string(), "9999".to_string()],
            records: vec![
                KplRecord {
                    partition_key_index: 0,
                    explicit_hash_key_index: Some(0),
                    data: b"keep-then-rollback".to_vec(),
                    tags: vec![],
                },
                KplRecord {
                    partition_key_index: 0,
                    explicit_hash_key_index: Some(1),
                    data: b"out-of-range".to_vec(),
                    tags: vec![],
                },
            ],
        };
        let record = aggregated_client_record(envelope(&ar));
        let out =
            AGGREGATOR.deaggregate_with_range(vec![record], &BigInt::from(0), &BigInt::from(100));
        // Both rolled back: the first was emitted, then removed when the second
        // fell out of range.
        assert!(out.is_empty());
    }

    #[test]
    fn explicit_hash_key_in_range_is_retained() {
        let ar = AggregatedRecord {
            partition_key_table: vec!["pk".to_string()],
            explicit_hash_key_table: vec!["42".to_string()],
            records: vec![KplRecord {
                partition_key_index: 0,
                explicit_hash_key_index: Some(0),
                data: b"in-range".to_vec(),
                tags: vec![],
            }],
        };
        let record = aggregated_client_record(envelope(&ar));
        let out =
            AGGREGATOR.deaggregate_with_range(vec![record], &BigInt::from(0), &BigInt::from(100));
        assert_eq!(out.len(), 1);
        assert_eq!(out[0].data().unwrap().as_ref(), b"in-range");
        assert_eq!(out[0].explicit_hash_key(), Some("42"));
    }

    // Port of Java's inner `catch (Exception e)` semantics: a digest-valid
    // aggregate whose protobuf decodes but whose index tables are corrupt must
    // not panic — already-emitted sub-records are kept, the remainder of THAT
    // aggregate is skipped, and the raw aggregate is NOT passed through.
    #[test]
    fn out_of_range_partition_key_index_skips_rest_of_aggregate() {
        let ar = AggregatedRecord {
            partition_key_table: vec!["pk0".to_string()],
            explicit_hash_key_table: vec![],
            records: vec![
                KplRecord {
                    partition_key_index: 0,
                    explicit_hash_key_index: None,
                    data: b"good".to_vec(),
                    tags: vec![],
                },
                KplRecord {
                    // Index 7 is out of range for the 1-entry table: Java throws
                    // IndexOutOfBoundsException -> caught, logged, loop exits.
                    partition_key_index: 7,
                    explicit_hash_key_index: None,
                    data: b"corrupt".to_vec(),
                    tags: vec![],
                },
                KplRecord {
                    partition_key_index: 0,
                    explicit_hash_key_index: None,
                    data: b"never-reached".to_vec(),
                    tags: vec![],
                },
            ],
        };
        let record = aggregated_client_record(envelope(&ar));
        let out = AGGREGATOR.deaggregate(vec![record]);
        // The first sub-record survives; the corrupt one and everything after
        // it are dropped; the raw aggregate is not passed through.
        assert_eq!(out.len(), 1);
        assert_eq!(out[0].data().unwrap().as_ref(), b"good");
        assert!(out[0].aggregated());
    }

    #[test]
    fn out_of_range_explicit_hash_key_index_skips_rest_of_aggregate() {
        let ar = AggregatedRecord {
            partition_key_table: vec!["pk0".to_string()],
            explicit_hash_key_table: vec![],
            records: vec![KplRecord {
                partition_key_index: 0,
                // No entries in the EHK table at all.
                explicit_hash_key_index: Some(3),
                data: b"corrupt".to_vec(),
                tags: vec![],
            }],
        };
        let record = aggregated_client_record(envelope(&ar));
        let out = AGGREGATOR.deaggregate(vec![record]);
        assert!(out.is_empty());
    }

    #[test]
    fn non_numeric_explicit_hash_key_skips_rest_of_aggregate() {
        let ar = AggregatedRecord {
            partition_key_table: vec!["pk0".to_string()],
            explicit_hash_key_table: vec!["not-a-number".to_string()],
            records: vec![KplRecord {
                partition_key_index: 0,
                explicit_hash_key_index: Some(0),
                data: b"corrupt".to_vec(),
                tags: vec![],
            }],
        };
        let record = aggregated_client_record(envelope(&ar));
        // Java: NumberFormatException from effectiveHashKey -> caught, logged.
        let out = AGGREGATOR.deaggregate(vec![record]);
        assert!(out.is_empty());
    }

    // A corrupt aggregate must not poison the batch: records after it in the
    // same deaggregate() call are still processed normally.
    #[test]
    fn corrupt_aggregate_does_not_affect_subsequent_records() {
        let corrupt = AggregatedRecord {
            partition_key_table: vec![],
            explicit_hash_key_table: vec![],
            records: vec![KplRecord {
                partition_key_index: 0,
                explicit_hash_key_index: None,
                data: b"corrupt".to_vec(),
                tags: vec![],
            }],
        };
        let good = AggregatedRecord {
            partition_key_table: vec!["pk0".to_string()],
            explicit_hash_key_table: vec![],
            records: vec![KplRecord {
                partition_key_index: 0,
                explicit_hash_key_index: None,
                data: b"good".to_vec(),
                tags: vec![],
            }],
        };
        let out = AGGREGATOR.deaggregate(vec![
            aggregated_client_record(envelope(&corrupt)),
            aggregated_client_record(envelope(&good)),
        ]);
        assert_eq!(out.len(), 1);
        assert_eq!(out[0].data().unwrap().as_ref(), b"good");
    }

    #[test]
    fn magic_bytes_match_java_signed_values() {
        // Java: byte[] {-13, -119, -102, -62}
        assert_eq!(
            AGGREGATED_RECORD_MAGIC,
            [(-13i8) as u8, (-119i8) as u8, (-102i8) as u8, (-62i8) as u8,]
        );
        assert_eq!(AGGREGATED_RECORD_MAGIC, [0xF3, 0x89, 0x9A, 0xC2]);
    }

    #[test]
    fn ending_hash_key_is_2_pow_128_minus_1() {
        let expected: BigInt = "340282366920938463463374607431768211455".parse().unwrap();
        assert_eq!(AggregatorUtil::ending_hash_key(), expected);
    }
}
