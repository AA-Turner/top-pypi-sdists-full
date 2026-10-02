//! KPL (Kinesis Producer Library) protobuf messages.
//!
//! Port of the Java `software.amazon.kinesis.retrieval.kpl.Messages` generated
//! protobuf class. The wire schema lives in `kcl/proto/messages.proto` (a subset
//! of the KPL `messages.proto`, kept as the schema reference).
//!
//! The proto2 wire format is implemented by hand here instead of via
//! `prost`/`protoc`: the schema is three small messages that only ever need
//! decoding at runtime (KCL de-aggregates; it never produces), and dropping the
//! codegen removed the `protoc` toolchain requirement from every build. The
//! decoder reproduces the prost behavior this crate previously shipped:
//! unknown fields (including groups) are skipped, duplicated scalar fields are
//! last-wins, string fields must be valid UTF-8, a wrong wire type on a known
//! field is an error, and — matching prost's proto2 handling — a missing
//! `required` field is *not* an error (the default value remains).
//!
//! The wire format (magic prefix + this protobuf payload + MD5 digest trailer)
//! is a cross-language compatibility concern, so the field numbers and
//! semantics must match the KPL exactly; the tests below pin the encoding
//! byte-for-byte against vectors generated with prost.

use std::fmt;

/// Error decoding a KPL protobuf payload.
///
/// Carries a static description of the first malformation encountered. Callers
/// treat any decode failure as "not an aggregated record".
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DecodeError(&'static str);

impl fmt::Display for DecodeError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "failed to decode KPL protobuf: {}", self.0)
    }
}

impl std::error::Error for DecodeError {}

/// `message Tag { required string key = 1; optional string value = 2; }`
#[derive(Debug, Clone, PartialEq, Default)]
pub struct Tag {
    pub key: String,
    pub value: Option<String>,
}

/// ```proto
/// message Record {
///   required uint64 partition_key_index = 1;
///   optional uint64 explicit_hash_key_index = 2;
///   required bytes data = 3;
///   repeated Tag tags = 4;
/// }
/// ```
#[derive(Debug, Clone, PartialEq, Default)]
pub struct Record {
    pub partition_key_index: u64,
    pub explicit_hash_key_index: Option<u64>,
    pub data: Vec<u8>,
    pub tags: Vec<Tag>,
}

/// ```proto
/// message AggregatedRecord {
///   repeated string partition_key_table = 1;
///   repeated string explicit_hash_key_table = 2;
///   repeated Record records = 3;
/// }
/// ```
#[derive(Debug, Clone, PartialEq, Default)]
pub struct AggregatedRecord {
    pub partition_key_table: Vec<String>,
    pub explicit_hash_key_table: Vec<String>,
    pub records: Vec<Record>,
}

// ---------------------------------------------------------------------------
// Wire-format primitives
// ---------------------------------------------------------------------------

const WT_VARINT: u64 = 0;
const WT_FIXED64: u64 = 1;
const WT_LEN: u64 = 2;
const WT_START_GROUP: u64 = 3;
const WT_END_GROUP: u64 = 4;
const WT_FIXED32: u64 = 5;

struct Reader<'a> {
    buf: &'a [u8],
    pos: usize,
}

impl<'a> Reader<'a> {
    fn new(buf: &'a [u8]) -> Self {
        Reader { buf, pos: 0 }
    }

    fn at_end(&self) -> bool {
        self.pos >= self.buf.len()
    }

    /// LEB128 varint, at most 10 bytes (bits beyond 64 are discarded, matching
    /// prost's wrapping behavior on over-wide but well-terminated varints).
    fn read_varint(&mut self) -> Result<u64, DecodeError> {
        let mut value: u64 = 0;
        for i in 0..10 {
            let byte = *self
                .buf
                .get(self.pos)
                .ok_or(DecodeError("truncated varint"))?;
            self.pos += 1;
            // Shift amount peaks at 63 (i == 9); value bits beyond u64 are
            // discarded, matching prost.
            value |= u64::from(byte & 0x7f) << (7 * i);
            if byte & 0x80 == 0 {
                return Ok(value);
            }
        }
        Err(DecodeError("varint exceeds 10 bytes"))
    }

    fn read_slice(&mut self, len: usize) -> Result<&'a [u8], DecodeError> {
        let end = self
            .pos
            .checked_add(len)
            .filter(|&end| end <= self.buf.len())
            .ok_or(DecodeError("length-delimited field overruns buffer"))?;
        let slice = &self.buf[self.pos..end];
        self.pos = end;
        Ok(slice)
    }

    /// Read a field key, returning `(field_number, wire_type)`.
    fn read_key(&mut self) -> Result<(u64, u64), DecodeError> {
        let key = self.read_varint()?;
        Ok((key >> 3, key & 7))
    }

    fn read_len_delimited(&mut self) -> Result<&'a [u8], DecodeError> {
        let len = self.read_varint()?;
        let len = usize::try_from(len).map_err(|_| DecodeError("length does not fit usize"))?;
        self.read_slice(len)
    }

    fn read_string(&mut self) -> Result<String, DecodeError> {
        String::from_utf8(self.read_len_delimited()?.to_vec())
            .map_err(|_| DecodeError("string field is not valid UTF-8"))
    }

    /// Skip an unknown field of the given wire type (groups included, as prost
    /// does).
    fn skip_field(&mut self, wire_type: u64) -> Result<(), DecodeError> {
        match wire_type {
            WT_VARINT => {
                self.read_varint()?;
            }
            WT_FIXED64 => {
                self.read_slice(8)?;
            }
            WT_LEN => {
                self.read_len_delimited()?;
            }
            WT_START_GROUP => loop {
                let (_, wt) = self.read_key()?;
                if wt == WT_END_GROUP {
                    break;
                }
                self.skip_field(wt)?;
            },
            WT_END_GROUP => return Err(DecodeError("unexpected end-group tag")),
            WT_FIXED32 => {
                self.read_slice(4)?;
            }
            _ => return Err(DecodeError("invalid wire type")),
        }
        Ok(())
    }
}

fn write_varint(buf: &mut Vec<u8>, mut value: u64) {
    loop {
        let byte = (value & 0x7f) as u8;
        value >>= 7;
        if value == 0 {
            buf.push(byte);
            return;
        }
        buf.push(byte | 0x80);
    }
}

fn write_key(buf: &mut Vec<u8>, field_number: u64, wire_type: u64) {
    write_varint(buf, (field_number << 3) | wire_type);
}

fn write_len_delimited(buf: &mut Vec<u8>, field_number: u64, bytes: &[u8]) {
    write_key(buf, field_number, WT_LEN);
    write_varint(buf, bytes.len() as u64);
    buf.extend_from_slice(bytes);
}

// ---------------------------------------------------------------------------
// Message decode / encode
// ---------------------------------------------------------------------------

impl Tag {
    fn merge(reader: &mut Reader<'_>) -> Result<Tag, DecodeError> {
        let mut tag = Tag::default();
        while !reader.at_end() {
            match reader.read_key()? {
                (1, WT_LEN) => tag.key = reader.read_string()?,
                (2, WT_LEN) => tag.value = Some(reader.read_string()?),
                (1..=2, _) => return Err(DecodeError("wrong wire type for Tag field")),
                (_, wt) => reader.skip_field(wt)?,
            }
        }
        Ok(tag)
    }

    fn encode(&self, buf: &mut Vec<u8>) {
        write_len_delimited(buf, 1, self.key.as_bytes());
        if let Some(value) = &self.value {
            write_len_delimited(buf, 2, value.as_bytes());
        }
    }
}

impl Record {
    fn merge(reader: &mut Reader<'_>) -> Result<Record, DecodeError> {
        let mut record = Record::default();
        while !reader.at_end() {
            match reader.read_key()? {
                (1, WT_VARINT) => record.partition_key_index = reader.read_varint()?,
                (2, WT_VARINT) => record.explicit_hash_key_index = Some(reader.read_varint()?),
                (3, WT_LEN) => record.data = reader.read_len_delimited()?.to_vec(),
                (4, WT_LEN) => record
                    .tags
                    .push(Tag::merge(&mut Reader::new(reader.read_len_delimited()?))?),
                (1..=4, _) => return Err(DecodeError("wrong wire type for Record field")),
                (_, wt) => reader.skip_field(wt)?,
            }
        }
        Ok(record)
    }

    fn encode(&self, buf: &mut Vec<u8>) {
        // `required` fields are written unconditionally, like prost/protoc.
        write_key(buf, 1, WT_VARINT);
        write_varint(buf, self.partition_key_index);
        if let Some(index) = self.explicit_hash_key_index {
            write_key(buf, 2, WT_VARINT);
            write_varint(buf, index);
        }
        write_len_delimited(buf, 3, &self.data);
        for tag in &self.tags {
            let mut nested = Vec::new();
            tag.encode(&mut nested);
            write_len_delimited(buf, 4, &nested);
        }
    }
}

impl AggregatedRecord {
    /// Decode an `AggregatedRecord` from its protobuf wire encoding (the bytes
    /// between the KPL magic prefix and the MD5 digest trailer).
    pub fn decode(buf: &[u8]) -> Result<AggregatedRecord, DecodeError> {
        let reader = &mut Reader::new(buf);
        let mut ar = AggregatedRecord::default();
        while !reader.at_end() {
            match reader.read_key()? {
                (1, WT_LEN) => ar.partition_key_table.push(reader.read_string()?),
                (2, WT_LEN) => ar.explicit_hash_key_table.push(reader.read_string()?),
                (3, WT_LEN) => ar.records.push(Record::merge(&mut Reader::new(
                    reader.read_len_delimited()?,
                ))?),
                (1..=3, _) => {
                    return Err(DecodeError("wrong wire type for AggregatedRecord field"))
                }
                (_, wt) => reader.skip_field(wt)?,
            }
        }
        Ok(ar)
    }

    /// Encode to protobuf wire bytes. Only exercised by tests (KCL never
    /// aggregates), kept for fixture-building symmetry with the Java tests.
    pub fn encode_to_vec(&self) -> Vec<u8> {
        let mut buf = Vec::new();
        for key in &self.partition_key_table {
            write_len_delimited(&mut buf, 1, key.as_bytes());
        }
        for key in &self.explicit_hash_key_table {
            write_len_delimited(&mut buf, 2, key.as_bytes());
        }
        for record in &self.records {
            let mut nested = Vec::new();
            record.encode(&mut nested);
            write_len_delimited(&mut buf, 3, &nested);
        }
        buf
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn hex(bytes: &[u8]) -> String {
        bytes.iter().map(|b| format!("{b:02x}")).collect()
    }

    fn unhex(s: &str) -> Vec<u8> {
        (0..s.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap())
            .collect()
    }

    fn full_record() -> AggregatedRecord {
        AggregatedRecord {
            partition_key_table: vec!["a".into(), "bb".into()],
            explicit_hash_key_table: vec!["123".into()],
            records: vec![
                Record {
                    partition_key_index: 0,
                    explicit_hash_key_index: Some(0),
                    data: b"hello".to_vec(),
                    tags: vec![Tag {
                        key: "k".into(),
                        value: Some("v".into()),
                    }],
                },
                Record {
                    partition_key_index: 1,
                    explicit_hash_key_index: None,
                    data: vec![],
                    tags: vec![],
                },
            ],
        }
    }

    // Golden vectors generated with prost 0.14 from proto/messages.proto
    // before the codegen was replaced — pin byte-for-byte compatibility.
    const GOLDEN_FULL: &str =
        "0a01610a02626212033132331a13080010001a0568656c6c6f22060a016b1201761a0408011a00";
    const GOLDEN_VARINT_MULTIBYTE: &str =
        "0a01701a1708ac0210f0a2041a02ff00220a0a086f6e6c792d6b6579";

    #[test]
    fn encode_matches_prost_golden_vectors() {
        assert_eq!(hex(&AggregatedRecord::default().encode_to_vec()), "");
        assert_eq!(hex(&full_record().encode_to_vec()), GOLDEN_FULL);
        let multibyte = AggregatedRecord {
            partition_key_table: vec!["p".into()],
            explicit_hash_key_table: vec![],
            records: vec![Record {
                partition_key_index: 300,
                explicit_hash_key_index: Some(70000),
                data: vec![0xff, 0x00],
                tags: vec![Tag {
                    key: "only-key".into(),
                    value: None,
                }],
            }],
        };
        assert_eq!(hex(&multibyte.encode_to_vec()), GOLDEN_VARINT_MULTIBYTE);
    }

    #[test]
    fn decode_matches_prost_golden_vectors() {
        assert_eq!(
            AggregatedRecord::decode(&[]).unwrap(),
            AggregatedRecord::default()
        );
        assert_eq!(
            AggregatedRecord::decode(&unhex(GOLDEN_FULL)).unwrap(),
            full_record()
        );
        let multibyte = AggregatedRecord::decode(&unhex(GOLDEN_VARINT_MULTIBYTE)).unwrap();
        assert_eq!(multibyte.records[0].partition_key_index, 300);
        assert_eq!(multibyte.records[0].explicit_hash_key_index, Some(70000));
        assert_eq!(multibyte.records[0].tags[0].key, "only-key");
        assert_eq!(multibyte.records[0].tags[0].value, None);
    }

    #[test]
    fn round_trips() {
        let ar = full_record();
        assert_eq!(AggregatedRecord::decode(&ar.encode_to_vec()).unwrap(), ar);
    }

    #[test]
    fn unknown_fields_are_skipped() {
        // field 15 varint, field 14 fixed64, field 13 fixed32, field 12 LEN —
        // all unknown to AggregatedRecord — followed by a real pk-table entry.
        let mut buf = Vec::new();
        write_key(&mut buf, 15, WT_VARINT);
        write_varint(&mut buf, 12345);
        write_key(&mut buf, 14, WT_FIXED64);
        buf.extend_from_slice(&[0; 8]);
        write_key(&mut buf, 13, WT_FIXED32);
        buf.extend_from_slice(&[0; 4]);
        write_len_delimited(&mut buf, 12, b"ignored");
        write_len_delimited(&mut buf, 1, b"pk");
        let ar = AggregatedRecord::decode(&buf).unwrap();
        assert_eq!(ar.partition_key_table, vec!["pk".to_string()]);
    }

    #[test]
    fn unknown_groups_are_skipped() {
        let mut buf = Vec::new();
        write_key(&mut buf, 9, WT_START_GROUP);
        write_key(&mut buf, 1, WT_VARINT); // field inside the group
        write_varint(&mut buf, 7);
        write_key(&mut buf, 9, WT_END_GROUP);
        write_len_delimited(&mut buf, 1, b"pk");
        let ar = AggregatedRecord::decode(&buf).unwrap();
        assert_eq!(ar.partition_key_table, vec!["pk".to_string()]);
    }

    #[test]
    fn malformed_input_errors() {
        // Truncated varint.
        assert!(AggregatedRecord::decode(&[0x80]).is_err());
        // Length overrunning the buffer.
        assert!(AggregatedRecord::decode(&[0x0a, 0x05, b'x']).is_err());
        // Wrong wire type for a known field (pk table as varint).
        assert!(AggregatedRecord::decode(&[0x08, 0x01]).is_err());
        // Invalid UTF-8 in a string field.
        assert!(AggregatedRecord::decode(&[0x0a, 0x01, 0xff]).is_err());
        // Bare end-group tag.
        assert!(AggregatedRecord::decode(&[0x4c]).is_err());
    }

    #[test]
    fn duplicated_scalar_fields_are_last_wins() {
        // Two partition_key_index values in one Record: prost keeps the last.
        let mut record = Vec::new();
        write_key(&mut record, 1, WT_VARINT);
        write_varint(&mut record, 1);
        write_key(&mut record, 1, WT_VARINT);
        write_varint(&mut record, 2);
        let mut buf = Vec::new();
        write_len_delimited(&mut buf, 3, &record);
        let ar = AggregatedRecord::decode(&buf).unwrap();
        assert_eq!(ar.records[0].partition_key_index, 2);
    }

    #[test]
    fn missing_required_fields_default_like_prost_proto2() {
        // An empty Record body: prost leaves required fields at their default.
        let mut buf = Vec::new();
        write_len_delimited(&mut buf, 3, &[]);
        let ar = AggregatedRecord::decode(&buf).unwrap();
        assert_eq!(ar.records[0], Record::default());
    }
}
