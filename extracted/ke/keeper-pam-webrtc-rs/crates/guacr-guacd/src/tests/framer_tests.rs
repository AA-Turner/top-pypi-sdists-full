// Tests for InstructionFramer — the byte-stream → instruction boundary layer.
//
// The framing this replaced scanned for the first `;` byte and decoded each
// `fill_buf` chunk as UTF-8 independently. Both are wrong: `;` is legal inside an
// element value, and a multi-byte character can straddle a chunk boundary. These
// tests pin instruction and character boundaries at exact byte offsets, which is
// why they drive an `AsyncBufRead` mock rather than a real socket.

use std::collections::VecDeque;
use std::io;
use std::pin::Pin;
use std::task::{Context, Poll};

use tokio::io::{AsyncBufRead, AsyncRead, ReadBuf};

use crate::server::{InstructionFramer, MAX_INSTRUCTION_SIZE};

/// Yields pre-set chunks one `fill_buf` at a time, so a test can place a chunk
/// boundary in the middle of a UTF-8 sequence or an instruction. An exhausted
/// reader returns an empty slice, which the framer treats as EOF.
struct ChunkedBufRead {
    chunks: VecDeque<Vec<u8>>,
    current: Vec<u8>,
    pos: usize,
}

impl ChunkedBufRead {
    fn new<I: IntoIterator<Item = Vec<u8>>>(chunks: I) -> Self {
        Self {
            chunks: chunks.into_iter().collect(),
            current: Vec::new(),
            pos: 0,
        }
    }
}

impl AsyncBufRead for ChunkedBufRead {
    fn poll_fill_buf(self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<io::Result<&[u8]>> {
        let this = self.get_mut();
        if this.pos >= this.current.len() {
            this.current = this.chunks.pop_front().unwrap_or_default();
            this.pos = 0;
        }
        Poll::Ready(Ok(&this.current[this.pos..]))
    }

    fn consume(self: Pin<&mut Self>, amt: usize) {
        self.get_mut().pos += amt;
    }
}

impl AsyncRead for ChunkedBufRead {
    fn poll_read(
        mut self: Pin<&mut Self>,
        cx: &mut Context<'_>,
        buf: &mut ReadBuf<'_>,
    ) -> Poll<io::Result<()>> {
        let available = match self.as_mut().poll_fill_buf(cx) {
            Poll::Ready(Ok(slice)) => slice.to_vec(),
            Poll::Ready(Err(e)) => return Poll::Ready(Err(e)),
            Poll::Pending => return Poll::Pending,
        };
        let n = available.len().min(buf.remaining());
        buf.put_slice(&available[..n]);
        self.consume(n);
        Poll::Ready(Ok(()))
    }
}

fn chunks<I: IntoIterator<Item = &'static str>>(parts: I) -> ChunkedBufRead {
    ChunkedBufRead::new(parts.into_iter().map(|s| s.as_bytes().to_vec()))
}

async fn frame_all(framer: &mut InstructionFramer, reader: &mut ChunkedBufRead) -> Vec<String> {
    let mut out = Vec::new();
    while let Ok(instruction) = framer.next(reader).await {
        out.push(String::from_utf8(instruction.to_vec()).expect("framed bytes are valid UTF-8"));
    }
    out
}

#[tokio::test]
async fn frames_simple_instruction() {
    let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
    let mut reader = chunks(["3.key,5.65507,1.1;"]);

    assert_eq!(
        frame_all(&mut framer, &mut reader).await,
        vec!["3.key,5.65507,1.1;"]
    );
}

/// Regression: `;` inside an element value is data, not a terminator. Scanning for
/// the first `;` cut this instruction in half.
#[tokio::test]
async fn semicolon_inside_value_does_not_end_the_frame() {
    let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
    let mut reader = chunks(["9.clipboard,9.abc;defgh;4.sync,1.1;"]);

    assert_eq!(
        frame_all(&mut framer, &mut reader).await,
        vec!["9.clipboard,9.abc;defgh;", "4.sync,1.1;"]
    );
}

/// Regression: a multi-byte character split across two `fill_buf` chunks. The old
/// code ran `from_utf8` on each chunk independently — the handshake path turned
/// this into an "Invalid UTF-8" error, and the interactive path silently dropped
/// the chunk while still consuming it, corrupting the instruction.
#[tokio::test]
async fn multibyte_character_split_across_chunks() {
    let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
    // "café" is 4 chars / 5 bytes; split inside the 2-byte 'é'.
    let full = "4.name,4.café;".as_bytes();
    let split_at = full.len() - 2; // mid-'é'
    let mut reader = ChunkedBufRead::new([full[..split_at].to_vec(), full[split_at..].to_vec()]);

    assert_eq!(
        frame_all(&mut framer, &mut reader).await,
        vec!["4.name,4.café;"]
    );
}

/// An emoji is 4 bytes; split it at every interior offset to be sure no boundary
/// is mishandled.
#[tokio::test]
async fn multibyte_split_at_every_interior_offset() {
    let full = "9.clipboard,4.hi 👋;".as_bytes().to_vec();
    for split_at in 1..full.len() {
        let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
        let mut reader =
            ChunkedBufRead::new([full[..split_at].to_vec(), full[split_at..].to_vec()]);

        assert_eq!(
            frame_all(&mut framer, &mut reader).await,
            vec!["9.clipboard,4.hi 👋;"],
            "failed when split at byte {split_at}"
        );
    }
}

/// Several instructions arriving in one chunk must all be framed — none may be
/// lost to over-read.
#[tokio::test]
async fn multiple_instructions_in_one_chunk() {
    let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
    let mut reader = chunks(["4.sync,1.1;3.key,5.65507,1.1;5.mouse,1.0,2.10;"]);

    assert_eq!(
        frame_all(&mut framer, &mut reader).await,
        vec!["4.sync,1.1;", "3.key,5.65507,1.1;", "5.mouse,1.0,2.10;"]
    );
}

/// One instruction arriving one byte at a time still frames exactly once.
#[tokio::test]
async fn instruction_dribbled_one_byte_per_chunk() {
    let full = "9.clipboard,9.abc;defgh;";
    let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
    let mut reader = ChunkedBufRead::new(full.bytes().map(|b| vec![b]));

    assert_eq!(frame_all(&mut framer, &mut reader).await, vec![full]);
}

/// Bytes read past the handshake's last instruction are handed to the interactive
/// framer rather than dropped — the `into_parts` contract.
#[tokio::test]
async fn seeded_buffer_is_framed_before_reading_more() {
    let mut framer =
        InstructionFramer::with_buffered(MAX_INSTRUCTION_SIZE, b"4.sync,1.1;3.key".to_vec());
    let mut reader = chunks([",5.65507,1.1;"]);

    assert_eq!(
        frame_all(&mut framer, &mut reader).await,
        vec!["4.sync,1.1;", "3.key,5.65507,1.1;"]
    );
}

/// A seeded buffer that already holds everything needs no further reads, even from
/// an immediately-EOF stream.
#[tokio::test]
async fn seeded_buffer_alone_is_sufficient() {
    let mut framer =
        InstructionFramer::with_buffered(MAX_INSTRUCTION_SIZE, b"4.sync,1.1;".to_vec());
    let mut reader = ChunkedBufRead::new(Vec::<Vec<u8>>::new());

    assert_eq!(
        frame_all(&mut framer, &mut reader).await,
        vec!["4.sync,1.1;"]
    );
}

/// The size cap bounds buffering on the interactive path, which previously had no
/// limit at all: a client that never sent `;` grew the buffer without bound.
#[tokio::test]
async fn oversized_instruction_is_rejected() {
    let max = 256;
    let mut framer = InstructionFramer::new(max);
    // A declared length far beyond the cap, with no terminator ever arriving.
    let filler = "x".repeat(max * 2);
    let wire = format!("4.name,{}.{}", max * 2, filler);
    let mut reader = ChunkedBufRead::new([wire.into_bytes()]);

    let err = framer.next(&mut reader).await.expect_err("should reject");
    assert!(
        err.to_string().contains("maximum size"),
        "unexpected error: {err}"
    );
}

/// Malformed input is rejected rather than framed: the declared length is
/// satisfied, but the byte that follows is neither `,` nor `;`.
#[tokio::test]
async fn malformed_instruction_is_rejected() {
    let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
    let mut reader = chunks(["4.name,3.abcX;"]);

    let err = framer.next(&mut reader).await.expect_err("should reject");
    assert!(
        matches!(err, crate::HandshakeError::Parse(_)),
        "unexpected error: {err}"
    );
}

/// A stream that closes mid-instruction reports closure, not a bogus frame.
#[tokio::test]
async fn truncated_stream_reports_connection_closed() {
    let mut framer = InstructionFramer::new(MAX_INSTRUCTION_SIZE);
    let mut reader = chunks(["4.name,9.abc;"]);

    let err = framer
        .next(&mut reader)
        .await
        .expect_err("should not frame");
    assert!(
        matches!(err, crate::HandshakeError::ConnectionClosed),
        "unexpected error: {err}"
    );
}
