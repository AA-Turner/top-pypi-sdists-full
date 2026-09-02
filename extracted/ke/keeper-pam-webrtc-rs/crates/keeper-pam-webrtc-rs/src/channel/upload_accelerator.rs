// Upload accelerator for RBI file uploads via guacd.
//
// Buffers parallel blob instructions from the client and serializes delivery
// to guacd one blob at a time, forwarding real acks back to the client as
// progress updates. Backpressure naturally limits how far ahead the client
// can get.

use crate::models::ConnectionMessage;
use bytes::{Buf, Bytes, BytesMut};
use dashmap::DashSet;
use guacr_protocol::{GuacdParser, PeekError};
use log::warn;
use std::collections::{HashMap, VecDeque};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use tokio::sync::mpsc;

const MAX_BUFFERED_BLOBS_PER_STREAM: usize = 32;

struct UploadStream {
    pending: VecDeque<Bytes>,
    waiting_for_ack: bool,
    /// Set to true once the "end" instruction has been pushed to `pending`.
    ended: bool,
}

pub(crate) struct UploadAcceleratorHandle {
    /// Outbound task sends the stream_idx here when guacd acks an upload stream.
    pub(crate) ack_tx: mpsc::UnboundedSender<u32>,
    /// Fast-path gate (~1ns check) — true while any upload stream is active.
    pub(crate) has_active_uploads: Arc<AtomicBool>,
    /// Which stream indices are currently being accelerated.
    pub(crate) active_stream_ids: Arc<DashSet<u32>>,
}

pub(crate) struct UploadAccelerator {
    inbound_rx: mpsc::UnboundedReceiver<ConnectionMessage>,
    outbound_tx: mpsc::UnboundedSender<ConnectionMessage>,
    ack_rx: mpsc::UnboundedReceiver<u32>,
    has_active_uploads: Arc<AtomicBool>,
    active_stream_ids: Arc<DashSet<u32>>,
    streams: HashMap<u32, UploadStream>,
    /// Accumulates partial instructions across WebRTC messages.
    parse_buf: BytesMut,
    channel_id: String,
    conn_no: u32,
}

impl UploadAccelerator {
    pub(crate) fn new(
        inbound_rx: mpsc::UnboundedReceiver<ConnectionMessage>,
        outbound_tx: mpsc::UnboundedSender<ConnectionMessage>,
        channel_id: String,
        conn_no: u32,
    ) -> (Self, UploadAcceleratorHandle) {
        let (ack_tx, ack_rx) = mpsc::unbounded_channel();
        let has_active_uploads = Arc::new(AtomicBool::new(false));
        let active_stream_ids = Arc::new(DashSet::new());

        let accel = Self {
            inbound_rx,
            outbound_tx,
            ack_rx,
            has_active_uploads: has_active_uploads.clone(),
            active_stream_ids: active_stream_ids.clone(),
            streams: HashMap::new(),
            parse_buf: BytesMut::new(),
            channel_id,
            conn_no,
        };

        let handle = UploadAcceleratorHandle {
            ack_tx,
            has_active_uploads,
            active_stream_ids,
        };

        (accel, handle)
    }

    pub(crate) async fn run(mut self) {
        loop {
            // Backpressure gate: pause reading inbound if any stream has too many
            // buffered blobs, backing up the WebRTC data channel naturally.
            let backpressure = self
                .streams
                .values()
                .any(|s| s.pending.len() >= MAX_BUFFERED_BLOBS_PER_STREAM);

            tokio::select! {
                biased;

                result = self.ack_rx.recv() => {
                    match result {
                        Some(stream_idx) => self.handle_ack(stream_idx),
                        // ack channel closed means the outbound task is done; exit.
                        None => break,
                    }
                }

                msg = self.inbound_rx.recv(), if !backpressure => {
                    match msg {
                        Some(msg) => self.process_inbound_msg(msg),
                        None => {
                            let _ = self.outbound_tx.send(ConnectionMessage::Eof);
                            break;
                        }
                    }
                }
            }
        }
    }

    fn handle_ack(&mut self, stream_idx: u32) {
        let stream = match self.streams.get_mut(&stream_idx) {
            Some(s) => s,
            None => return, // untracked stream, ignore
        };

        stream.waiting_for_ack = false;

        if let Some(next) = stream.pending.pop_front() {
            // If this was the last pending item and the stream already received "end",
            // then what we just popped is the "end" instruction — clean up after sending.
            let is_end = stream.ended && stream.pending.is_empty();
            let _ = self.outbound_tx.send(ConnectionMessage::Data(next));
            if is_end {
                self.streams.remove(&stream_idx);
                self.active_stream_ids.remove(&stream_idx);
                if self.streams.is_empty() {
                    self.has_active_uploads.store(false, Ordering::Release);
                }
            } else if let Some(s) = self.streams.get_mut(&stream_idx) {
                s.waiting_for_ack = true;
            }
        }
        // else: queue empty — wait for more blobs or the "end" instruction
    }

    fn process_inbound_msg(&mut self, msg: ConnectionMessage) {
        match msg {
            ConnectionMessage::Data(payload) => self.process_inbound(payload),
            ConnectionMessage::Eof => {
                let _ = self.outbound_tx.send(ConnectionMessage::Eof);
            }
        }
    }

    fn process_inbound(&mut self, payload: Bytes) {
        self.parse_buf.extend_from_slice(&payload);

        let mut offset = 0;
        loop {
            let current_slice = &self.parse_buf[offset..];
            if current_slice.is_empty() {
                break;
            }

            let peeked = match GuacdParser::peek_instruction(current_slice) {
                Ok(p) => p,
                Err(PeekError::Incomplete) => break,
                Err(e) => {
                    warn!(
                        "UploadAccelerator: parse error, forwarding remainder raw \
                         (channel_id: {}, conn_no: {}): {:?}",
                        self.channel_id, self.conn_no, e
                    );
                    let remainder = Bytes::copy_from_slice(&self.parse_buf[offset..]);
                    let _ = self.outbound_tx.send(ConnectionMessage::Data(remainder));
                    offset = self.parse_buf.len();
                    break;
                }
            };

            let instr_len = peeked.total_length_in_buffer;
            // One small String alloc per instruction only for routing; dropped immediately.
            let opcode = peeked.opcode.to_string();
            let stream_idx = peeked.args.first().and_then(|s| s.parse::<u32>().ok());
            drop(peeked); // drop borrow before mutating self

            let instr_bytes = Bytes::copy_from_slice(&self.parse_buf[offset..offset + instr_len]);

            match opcode.as_str() {
                "file" => {
                    // Forward immediately; start tracking this upload stream.
                    let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                    if let Some(idx) = stream_idx {
                        self.streams.insert(
                            idx,
                            UploadStream {
                                pending: VecDeque::new(),
                                waiting_for_ack: false,
                                ended: false,
                            },
                        );
                        self.active_stream_ids.insert(idx);
                        self.has_active_uploads.store(true, Ordering::Release);
                    }
                }

                "blob" => {
                    if let Some(idx) = stream_idx {
                        if let Some(stream) = self.streams.get_mut(&idx) {
                            if !stream.waiting_for_ack {
                                // No in-flight blob: send directly.
                                let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                                stream.waiting_for_ack = true;
                            } else {
                                // A blob is already in-flight: buffer this one.
                                stream.pending.push_back(instr_bytes);
                            }
                        } else {
                            // Not a tracked upload stream (e.g. clipboard blob): pass through.
                            let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                        }
                    } else {
                        // Unparseable stream index: pass through unchanged.
                        let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                    }
                }

                "end" => {
                    if let Some(idx) = stream_idx {
                        if let Some(stream) = self.streams.get_mut(&idx) {
                            stream.ended = true;
                            if !stream.waiting_for_ack && stream.pending.is_empty() {
                                // All blobs already delivered: send "end" now and remove stream.
                                let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                                self.streams.remove(&idx);
                                self.active_stream_ids.remove(&idx);
                                if self.streams.is_empty() {
                                    self.has_active_uploads.store(false, Ordering::Release);
                                }
                            } else {
                                // Queue "end" after the remaining blobs.
                                stream.pending.push_back(instr_bytes);
                            }
                        } else {
                            // Untracked stream: pass through.
                            let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                        }
                    } else {
                        let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                    }
                }

                _ => {
                    // All other instructions (mouse, key, clipboard, etc.) pass through.
                    let _ = self.outbound_tx.send(ConnectionMessage::Data(instr_bytes));
                }
            }

            offset += instr_len;
        }

        self.parse_buf.advance(offset);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::Ordering;

    // Build a Guacamole instruction as raw wire bytes.
    // Format: `<char_count>.<value>` for opcode and each arg, separated by commas, terminated by `;`.
    fn guac(opcode: &str, args: &[&str]) -> Bytes {
        let mut s = format!("{}.{}", opcode.chars().count(), opcode);
        for arg in args {
            s.push_str(&format!(",{}.{}", arg.chars().count(), arg));
        }
        s.push(';');
        Bytes::from(s.into_bytes())
    }

    // Construct an accelerator wired to test channels.
    fn make_accel() -> (
        UploadAccelerator,
        mpsc::UnboundedSender<ConnectionMessage>,
        mpsc::UnboundedReceiver<ConnectionMessage>,
        UploadAcceleratorHandle,
    ) {
        let (inbound_tx, inbound_rx) = mpsc::unbounded_channel();
        let (outbound_tx, outbound_rx) = mpsc::unbounded_channel();
        let (accel, handle) =
            UploadAccelerator::new(inbound_rx, outbound_tx, "test-channel".into(), 1);
        (accel, inbound_tx, outbound_rx, handle)
    }

    // Drain all Data payloads currently sitting in the channel without blocking.
    fn drain_bytes(rx: &mut mpsc::UnboundedReceiver<ConnectionMessage>) -> Vec<Bytes> {
        let mut out = Vec::new();
        while let Ok(ConnectionMessage::Data(b)) = rx.try_recv() {
            out.push(b);
        }
        out
    }

    // Return true if at least one Eof message is sitting in the channel.
    fn has_eof(rx: &mut mpsc::UnboundedReceiver<ConnectionMessage>) -> bool {
        let mut found = false;
        while let Ok(msg) = rx.try_recv() {
            if matches!(msg, ConnectionMessage::Eof) {
                found = true;
            }
        }
        found
    }

    // -------------------------------------------------------------------------
    // Routing / process_inbound
    // -------------------------------------------------------------------------

    #[test]
    fn file_forwarded_and_stream_tracked() {
        let (mut accel, _, mut out, handle) = make_accel();
        let file = guac("file", &["0", "text/html", "test.txt"]);
        accel.process_inbound(file.clone());
        let sent = drain_bytes(&mut out);
        assert_eq!(sent, vec![file]);
        assert!(handle.has_active_uploads.load(Ordering::Acquire));
        assert!(handle.active_stream_ids.contains(&0));
    }

    #[test]
    fn first_blob_sent_immediately() {
        let (mut accel, _, mut out, _handle) = make_accel();
        accel.process_inbound(guac("file", &["0", "text/html", "f"]));
        drain_bytes(&mut out);
        let blob = guac("blob", &["0", "aGVsbG8="]);
        accel.process_inbound(blob.clone());
        let sent = drain_bytes(&mut out);
        assert_eq!(sent, vec![blob]);
        assert!(accel.streams[&0].waiting_for_ack);
    }

    #[test]
    fn second_blob_buffered_while_first_in_flight() {
        let (mut accel, _, mut out, _) = make_accel();
        accel.process_inbound(guac("file", &["0", "text/html", "f"]));
        accel.process_inbound(guac("blob", &["0", "first"]));
        drain_bytes(&mut out);
        let second = guac("blob", &["0", "second"]);
        accel.process_inbound(second.clone());
        let sent = drain_bytes(&mut out);
        assert!(
            sent.is_empty(),
            "second blob must not be forwarded while first is in flight"
        );
        assert_eq!(accel.streams[&0].pending.len(), 1);
        assert_eq!(accel.streams[&0].pending[0], second);
    }

    #[test]
    fn blob_for_untracked_stream_passes_through() {
        let (mut accel, _, mut out, handle) = make_accel();
        let clipboard_blob = guac("blob", &["99", "clipboard-data"]);
        accel.process_inbound(clipboard_blob.clone());
        let sent = drain_bytes(&mut out);
        assert_eq!(sent, vec![clipboard_blob]);
        assert!(!handle.has_active_uploads.load(Ordering::Acquire));
    }

    #[test]
    fn non_upload_instructions_pass_through() {
        let (mut accel, _, mut out, _) = make_accel();
        let key = guac("key", &["0", "65534"]);
        let mouse = guac("mouse", &["100", "200", "0"]);
        accel.process_inbound(key.clone());
        accel.process_inbound(mouse.clone());
        let sent = drain_bytes(&mut out);
        assert_eq!(sent, vec![key, mouse]);
    }

    #[test]
    fn end_sent_immediately_when_idle_after_ack() {
        let (mut accel, _, mut out, handle) = make_accel();
        accel.process_inbound(guac("file", &["0", "text/html", "f"]));
        accel.process_inbound(guac("blob", &["0", "data"]));
        drain_bytes(&mut out);
        // Ack the only blob so the stream is idle.
        accel.handle_ack(0);
        drain_bytes(&mut out); // nothing pending
        let end = guac("end", &["0"]);
        accel.process_inbound(end.clone());
        let sent = drain_bytes(&mut out);
        assert_eq!(sent, vec![end]);
        assert!(
            !accel.streams.contains_key(&0),
            "stream should be removed after end"
        );
        assert!(!handle.has_active_uploads.load(Ordering::Acquire));
        assert!(!handle.active_stream_ids.contains(&0));
    }

    #[test]
    fn end_queued_when_blob_in_flight() {
        let (mut accel, _, mut out, _) = make_accel();
        accel.process_inbound(guac("file", &["0", "text/html", "f"]));
        accel.process_inbound(guac("blob", &["0", "data"]));
        drain_bytes(&mut out);
        accel.process_inbound(guac("end", &["0"]));
        let sent = drain_bytes(&mut out);
        assert!(
            sent.is_empty(),
            "end must not be forwarded while a blob is in flight"
        );
        assert!(accel.streams[&0].ended);
        assert_eq!(accel.streams[&0].pending.len(), 1);
    }

    #[test]
    fn multiple_instructions_in_one_payload() {
        let (mut accel, _, mut out, _) = make_accel();
        let file = guac("file", &["0", "text/html", "f"]);
        let blob = guac("blob", &["0", "data"]);
        let mut combined = BytesMut::new();
        combined.extend_from_slice(&file);
        combined.extend_from_slice(&blob);
        accel.process_inbound(combined.freeze());
        let sent = drain_bytes(&mut out);
        assert_eq!(sent.len(), 2);
        assert_eq!(sent[0], file);
        assert_eq!(sent[1], blob);
    }

    // -------------------------------------------------------------------------
    // handle_ack
    // -------------------------------------------------------------------------

    #[test]
    fn ack_for_untracked_stream_is_noop() {
        let (mut accel, _, mut out, _) = make_accel();
        accel.handle_ack(42); // no stream 42
        assert!(drain_bytes(&mut out).is_empty());
    }

    #[test]
    fn ack_dequeues_next_pending_blob() {
        let (mut accel, _, mut out, _) = make_accel();
        accel.process_inbound(guac("file", &["0", "text/html", "f"]));
        accel.process_inbound(guac("blob", &["0", "first"]));
        accel.process_inbound(guac("blob", &["0", "second"]));
        drain_bytes(&mut out); // file + first blob already sent
        accel.handle_ack(0);
        let sent = drain_bytes(&mut out);
        assert_eq!(sent.len(), 1);
        assert_eq!(sent[0], guac("blob", &["0", "second"]));
        assert!(accel.streams[&0].waiting_for_ack);
    }

    #[test]
    fn ack_delivers_end_and_removes_stream() {
        let (mut accel, _, mut out, handle) = make_accel();
        let end = guac("end", &["0"]);
        accel.process_inbound(guac("file", &["0", "text/html", "f"]));
        accel.process_inbound(guac("blob", &["0", "data"]));
        accel.process_inbound(end.clone());
        drain_bytes(&mut out);
        accel.handle_ack(0);
        let sent = drain_bytes(&mut out);
        assert_eq!(sent, vec![end]);
        assert!(!accel.streams.contains_key(&0));
        assert!(!handle.has_active_uploads.load(Ordering::Acquire));
    }

    #[test]
    fn has_active_uploads_cleared_only_when_all_streams_done() {
        let (mut accel, _, mut out, handle) = make_accel();
        accel.process_inbound(guac("file", &["0", "text/html", "a"]));
        accel.process_inbound(guac("file", &["1", "text/html", "b"]));
        drain_bytes(&mut out);
        // End stream 0 (no blobs in flight, so end goes immediately).
        accel.process_inbound(guac("end", &["0"]));
        drain_bytes(&mut out);
        assert!(
            handle.has_active_uploads.load(Ordering::Acquire),
            "stream 1 is still active"
        );
        // End stream 1.
        accel.process_inbound(guac("end", &["1"]));
        drain_bytes(&mut out);
        assert!(!handle.has_active_uploads.load(Ordering::Acquire));
    }

    #[test]
    fn two_concurrent_streams_are_independent() {
        let (mut accel, _, mut out, _) = make_accel();
        accel.process_inbound(guac("file", &["0", "text/html", "a"]));
        accel.process_inbound(guac("file", &["1", "text/html", "b"]));
        accel.process_inbound(guac("blob", &["0", "data0"]));
        accel.process_inbound(guac("blob", &["1", "data1"]));
        drain_bytes(&mut out); // 2 file + 2 blob instructions
                               // Ack stream 1; stream 0 must be unaffected.
        accel.handle_ack(1);
        // Both streams had empty pending queues, so nothing new is forwarded.
        assert!(drain_bytes(&mut out).is_empty());
        assert!(
            accel.streams[&0].waiting_for_ack,
            "stream 0 must still be in-flight"
        );
    }

    // -------------------------------------------------------------------------
    // Parse-buffer continuity
    // -------------------------------------------------------------------------

    #[test]
    fn instruction_split_across_two_payloads() {
        let (mut accel, _, mut out, _) = make_accel();
        let full = guac("key", &["0", "65534"]);
        let mid = full.len() / 2;
        accel.process_inbound(full.slice(..mid));
        assert!(
            drain_bytes(&mut out).is_empty(),
            "partial instruction must not be forwarded"
        );
        accel.process_inbound(full.slice(mid..));
        let sent = drain_bytes(&mut out);
        assert_eq!(sent, vec![full]);
    }

    #[test]
    fn eof_forwarded_to_outbound() {
        let (mut accel, _, mut out, _) = make_accel();
        accel.process_inbound_msg(ConnectionMessage::Eof);
        assert!(has_eof(&mut out));
    }

    // -------------------------------------------------------------------------
    // Async integration — exercises run()
    // -------------------------------------------------------------------------

    #[tokio::test]
    async fn run_full_single_blob_upload() {
        let (inbound_tx, inbound_rx) = mpsc::unbounded_channel();
        let (outbound_tx, mut outbound_rx) = mpsc::unbounded_channel();
        let (accel, handle) = UploadAccelerator::new(inbound_rx, outbound_tx, "ch".into(), 1);
        tokio::spawn(accel.run());

        inbound_tx
            .send(ConnectionMessage::Data(guac(
                "file",
                &["0", "text/html", "f"],
            )))
            .unwrap();
        inbound_tx
            .send(ConnectionMessage::Data(guac("blob", &["0", "payload"])))
            .unwrap();

        // file arrives
        assert!(matches!(
            outbound_rx.recv().await.unwrap(),
            ConnectionMessage::Data(_)
        ));
        // blob 0 arrives
        assert!(matches!(
            outbound_rx.recv().await.unwrap(),
            ConnectionMessage::Data(_)
        ));

        // guacd acks blob 0
        handle.ack_tx.send(0).unwrap();

        inbound_tx
            .send(ConnectionMessage::Data(guac("end", &["0"])))
            .unwrap();

        // end arrives
        assert!(matches!(
            outbound_rx.recv().await.unwrap(),
            ConnectionMessage::Data(_)
        ));
        assert!(!handle.has_active_uploads.load(Ordering::Acquire));
    }

    #[tokio::test]
    async fn run_parallel_blobs_serialized() {
        let (inbound_tx, inbound_rx) = mpsc::unbounded_channel();
        let (outbound_tx, mut outbound_rx) = mpsc::unbounded_channel();
        let (accel, handle) = UploadAccelerator::new(inbound_rx, outbound_tx, "ch".into(), 1);
        tokio::spawn(accel.run());

        // file + 3 blobs all sent at once (parallel client)
        inbound_tx
            .send(ConnectionMessage::Data(guac(
                "file",
                &["0", "text/html", "f"],
            )))
            .unwrap();
        inbound_tx
            .send(ConnectionMessage::Data(guac("blob", &["0", "b0"])))
            .unwrap();
        inbound_tx
            .send(ConnectionMessage::Data(guac("blob", &["0", "b1"])))
            .unwrap();
        inbound_tx
            .send(ConnectionMessage::Data(guac("blob", &["0", "b2"])))
            .unwrap();

        // file
        outbound_rx.recv().await.unwrap();
        // blob 0 only
        outbound_rx.recv().await.unwrap();

        // blobs 1 and 2 must be held
        tokio::task::yield_now().await;
        assert!(
            outbound_rx.try_recv().is_err(),
            "blobs 1 and 2 must be held until blob 0 is acked"
        );

        handle.ack_tx.send(0).unwrap();
        outbound_rx.recv().await.unwrap(); // blob 1

        tokio::task::yield_now().await;
        assert!(outbound_rx.try_recv().is_err());

        handle.ack_tx.send(0).unwrap();
        outbound_rx.recv().await.unwrap(); // blob 2
    }

    #[tokio::test]
    async fn run_non_upload_instructions_not_delayed_by_upload() {
        let (inbound_tx, inbound_rx) = mpsc::unbounded_channel();
        let (outbound_tx, mut outbound_rx) = mpsc::unbounded_channel();
        let (accel, _handle) = UploadAccelerator::new(inbound_rx, outbound_tx, "ch".into(), 1);
        tokio::spawn(accel.run());

        inbound_tx
            .send(ConnectionMessage::Data(guac(
                "file",
                &["0", "text/html", "f"],
            )))
            .unwrap();
        inbound_tx
            .send(ConnectionMessage::Data(guac("blob", &["0", "data"])))
            .unwrap();
        inbound_tx
            .send(ConnectionMessage::Data(guac("key", &["0", "65534"])))
            .unwrap();

        let mut received = Vec::new();
        for _ in 0..3 {
            if let Some(ConnectionMessage::Data(b)) = outbound_rx.recv().await {
                received.push(b);
            }
        }

        // key must arrive even though no ack was sent for the blob
        let has_key = received.iter().any(|b| b.starts_with(b"3.key"));
        assert!(
            has_key,
            "key instruction must pass through without waiting for blob ack"
        );
    }

    #[tokio::test]
    async fn run_inbound_close_sends_eof() {
        let (inbound_tx, inbound_rx) = mpsc::unbounded_channel::<ConnectionMessage>();
        let (outbound_tx, mut outbound_rx) = mpsc::unbounded_channel();
        let (accel, _handle) = UploadAccelerator::new(inbound_rx, outbound_tx, "ch".into(), 1);
        let task = tokio::spawn(accel.run());

        drop(inbound_tx);
        task.await.unwrap();

        let msg = outbound_rx.recv().await.unwrap();
        assert!(matches!(msg, ConnectionMessage::Eof));
    }

    #[tokio::test]
    async fn run_exits_when_ack_channel_closes() {
        let (inbound_tx, inbound_rx) = mpsc::unbounded_channel::<ConnectionMessage>();
        let (outbound_tx, _outbound_rx) = mpsc::unbounded_channel();
        let (accel, handle) = UploadAccelerator::new(inbound_rx, outbound_tx, "ch".into(), 1);
        let task = tokio::spawn(accel.run());

        drop(handle); // drops ack_tx — run() should exit
        let _ = inbound_tx; // keep inbound alive so inbound EOF is not the trigger

        tokio::time::timeout(std::time::Duration::from_millis(200), task)
            .await
            .expect("run() should exit within 200ms when ack channel closes")
            .unwrap();
    }
}
