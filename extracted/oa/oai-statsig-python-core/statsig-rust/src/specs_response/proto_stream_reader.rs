use std::{io::Read, sync::Arc};

use crate::specs_response::statsig_config_specs as pb;
use crate::{
    StatsigErr,
    networking::{ResponseData, ResponseDataStream},
    specs_response::proto_compression::ProtoCompression,
};
use brotli::Decompressor;
use bytes::BytesMut;
use prost::Message;

// Configuration responses expand to several megabytes. Keeping the decoder's
// input and output buffers at 32 KiB avoids resuming it for every 4 KiB.
pub const BUFFER_SIZE: usize = 32 * 1024;

#[derive(Clone, PartialEq, prost::Message)]
pub(crate) struct ProtobufSnapshotCursor {
    #[prost(uint64, tag = "2")]
    pub(crate) lcut: u64,
    #[prost(string, tag = "5")]
    pub(crate) checksum: String,
}

#[derive(Clone, PartialEq, prost::Message)]
struct SnapshotEnvelope {
    #[prost(int32, tag = "1")]
    kind: i32,
    #[prost(bytes = "bytes", optional, tag = "4")]
    data: Option<bytes::Bytes>,
}

pub(crate) fn read_snapshot_cursor(mut reader: impl Read) -> Option<ProtobufSnapshotCursor> {
    let mut delimiter = [0_u8; 10];
    let mut delimiter_len = 0;
    loop {
        reader
            .read_exact(&mut delimiter[delimiter_len..delimiter_len + 1])
            .ok()?;
        delimiter_len += 1;
        if delimiter[delimiter_len - 1] & 0x80 == 0 {
            break;
        }
        if delimiter_len == delimiter.len() {
            return None;
        }
    }

    let envelope_len = prost::decode_length_delimiter(&delimiter[..delimiter_len]).ok()?;
    let mut encoded_envelope = Vec::new();
    reader
        .take(u64::try_from(envelope_len).ok()?)
        .read_to_end(&mut encoded_envelope)
        .ok()?;
    if encoded_envelope.len() != envelope_len {
        return None;
    }

    let envelope = SnapshotEnvelope::decode(bytes::Bytes::from(encoded_envelope)).ok()?;
    if pb::SpecsEnvelopeKind::try_from(envelope.kind).ok()? != pb::SpecsEnvelopeKind::TopLevel {
        return None;
    }
    let cursor = ProtobufSnapshotCursor::decode(envelope.data?).ok()?;
    (cursor.lcut > 0).then_some(cursor)
}

pub struct ProtoStreamReader<'a, R: Read = std::io::Empty> {
    source: ProtoStreamSource<'a, R>,
    scratch: [u8; BUFFER_SIZE],
    buf: BytesMut,
}

impl<'a> ProtoStreamReader<'a> {
    pub fn new(data: &'a mut ResponseData) -> Self {
        if let Some(bytes) = data.get_prepared_protobuf_stream() {
            return Self::from_prepared_stream(bytes);
        }

        Self::new_compressed(data)
    }

    pub(crate) fn new_for_response(data: &'a mut ResponseData) -> Result<Self, StatsigErr> {
        if let Some(bytes) = data.get_prepared_protobuf_stream() {
            return Ok(Self::from_prepared_stream(bytes));
        }

        match ProtoCompression::from_response(data) {
            Some(ProtoCompression::Brotli) => Ok(Self::new_compressed(data)),
            Some(ProtoCompression::Zstd) => Self::new_zstd_compressed(data),
            // Direct decoder callers and datastore hydration historically pass
            // headerless statsig-br bytes. Network response classification rejects
            // unsupported encodings before this point.
            None => Ok(Self::new_compressed(data)),
        }
    }

    /// Always reads the original statsig-br stream, ignoring any prepared
    /// protobuf stream attached by hydration. Hydration uses this constructor
    /// while producing the prepared stream itself.
    pub(crate) fn new_compressed(data: &'a mut ResponseData) -> Self {
        let stream_borrower = StreamBorrower::new(data);
        let brotli_decompressor = Decompressor::new(stream_borrower, BUFFER_SIZE);

        Self {
            source: ProtoStreamSource::Brotli(Box::new(brotli_decompressor)),
            scratch: [0u8; BUFFER_SIZE],
            buf: BytesMut::new(),
        }
    }

    fn new_zstd_compressed(data: &'a mut ResponseData) -> Result<Self, StatsigErr> {
        let stream_borrower = StreamBorrower::new(data);
        let zstd_decompressor = zstd::stream::read::Decoder::new(stream_borrower).map_err(|e| {
            StatsigErr::ProtobufParseError("ZstdDecompressorInit".to_string(), e.to_string())
        })?;

        Ok(Self {
            source: ProtoStreamSource::Zstd(Box::new(zstd_decompressor)),
            scratch: [0u8; BUFFER_SIZE],
            buf: BytesMut::new(),
        })
    }

    fn from_prepared_stream(bytes: Arc<Vec<u8>>) -> Self {
        Self {
            source: ProtoStreamSource::Prepared(PreparedStreamReader { bytes, position: 0 }),
            scratch: [0u8; BUFFER_SIZE],
            buf: BytesMut::new(),
        }
    }
}

impl<'a, R: Read> ProtoStreamReader<'a, R> {
    pub(crate) fn from_reader(reader: R) -> Self {
        Self {
            source: ProtoStreamSource::Reader(reader),
            scratch: [0u8; BUFFER_SIZE],
            buf: BytesMut::new(),
        }
    }

    pub fn read_next_delimited_proto(&mut self) -> Result<BytesMut, StatsigErr> {
        let required_len = self.read_length_delimiter()?;

        while self.buf.len() < required_len {
            let read_error_label = self.source.read_error_label();
            match self.source.read(&mut self.scratch) {
                Ok(0) => {
                    return Err(StatsigErr::ProtobufParseError(
                        read_error_label.to_string(),
                        "unexpected EOF while reading protobuf frame".to_string(),
                    ));
                }
                Ok(n) => {
                    self.buf.extend_from_slice(&self.scratch[..n]);
                }
                Err(e) => {
                    return Err(StatsigErr::ProtobufParseError(
                        read_error_label.to_string(),
                        e.to_string(),
                    ));
                }
            }
        }

        Ok(self.buf.split_to(required_len))
    }

    pub fn sample_current_buf(&self) -> String {
        let len = std::cmp::min(self.buf.len(), 100);
        let slice = &self.buf.as_ref()[..len];
        String::from_utf8(slice.to_vec()).unwrap_or_default()
    }

    fn read_length_delimiter(&mut self) -> Result<usize, StatsigErr> {
        loop {
            match prost::decode_length_delimiter(self.buf.as_ref()) {
                Ok(data_len) => {
                    return prost::length_delimiter_len(data_len)
                        .checked_add(data_len)
                        .ok_or_else(|| {
                            StatsigErr::ProtobufParseError(
                                "DecodeLengthDelimiter".to_string(),
                                "protobuf frame length overflow".to_string(),
                            )
                        });
                }
                Err(e) if self.buf.len() >= 10 => {
                    return Err(StatsigErr::ProtobufParseError(
                        "DecodeLengthDelimiter".to_string(),
                        e.to_string(),
                    ));
                }
                Err(_) => {
                    let read_len = self.source.read(&mut self.scratch).map_err(|e| {
                        StatsigErr::ProtobufParseError(
                            "ReadLengthDelimiter".to_string(),
                            e.to_string(),
                        )
                    })?;

                    if read_len == 0 {
                        return Err(StatsigErr::ProtobufParseError(
                            "ReadLengthDelimiter".to_string(),
                            "unexpected EOF while reading length delimiter".to_string(),
                        ));
                    }

                    self.buf.extend_from_slice(&self.scratch[..read_len]);
                }
            }
        }
    }
}

enum ProtoStreamSource<'a, R: Read> {
    Reader(R),
    Brotli(Box<Decompressor<StreamBorrower<'a>>>),
    Zstd(Box<zstd::stream::read::Decoder<'static, std::io::BufReader<StreamBorrower<'a>>>>),
    Prepared(PreparedStreamReader),
}

impl<R: Read> ProtoStreamSource<'_, R> {
    const fn read_error_label(&self) -> &'static str {
        match self {
            Self::Reader(_) => "ProtobufReaderRead",
            Self::Brotli(_) => "BrotliDecompressorRead",
            Self::Zstd(_) => "ZstdDecompressorRead",
            // Preserve the pre-zstd error label for the existing prepared path.
            Self::Prepared(_) => "BrotliDecompressorRead",
        }
    }
}

impl<R: Read> Read for ProtoStreamSource<'_, R> {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        loop {
            let result = match self {
                Self::Reader(reader) => reader.read(buf),
                Self::Brotli(reader) => reader.read(buf),
                Self::Zstd(reader) => reader.read(buf),
                Self::Prepared(reader) => reader.read(buf),
            };
            match result {
                Err(error) if error.kind() == std::io::ErrorKind::Interrupted => continue,
                result => return result,
            }
        }
    }
}

struct PreparedStreamReader {
    bytes: Arc<Vec<u8>>,
    position: usize,
}

impl Read for PreparedStreamReader {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        let remaining = &self.bytes[self.position..];
        let read_len = remaining.len().min(buf.len());
        buf[..read_len].copy_from_slice(&remaining[..read_len]);
        self.position += read_len;
        Ok(read_len)
    }
}

struct StreamBorrower<'a> {
    stream: &'a mut dyn ResponseDataStream,
}

impl<'a> StreamBorrower<'a> {
    pub fn new(data: &'a mut ResponseData) -> Self {
        Self {
            stream: data.get_stream_mut(),
        }
    }
}

impl<'a> std::io::Read for StreamBorrower<'a> {
    fn read(&mut self, buf: &mut [u8]) -> std::io::Result<usize> {
        self.stream.read(buf)
    }
}
