// Binary protocol message reassembly (T-077, T-078, T-079)
//
// Reassembles fragmented binary protocol messages (FLAG_FRAGMENTED set) back into
// the original complete message. Supports in-order (AC-1) and out-of-order (T-078 AC-2)
// fragments, with per-message reassembly isolation (T-079 AC-4) and a timeout
// mechanism for missing fragments (T-079 AC-3).
//
// Fragment header layout (from binary.rs):
//   byte[0]: opcode
//   byte[1]: flags (FLAG_FRAGMENTED = 0x04)
//   byte[2]: seq_num (0-indexed fragment sequence number)
//   byte[3]: total_count (total number of fragments)
//   bytes[4..8]: payload_len (little-endian u32)
//   bytes[8..]: fragment payload
//
// A message is identified by its (opcode, total_count) pair. Multiple concurrent
// in-flight fragmented messages of different types are tracked separately.

use std::collections::HashMap;
use std::time::{Duration, Instant};

use bytes::{BufMut, Bytes, BytesMut};
use log::{error, warn};

use crate::binary::FLAG_FRAGMENTED;

/// Default timeout for a partially received fragmented message.
pub const REASSEMBLY_TIMEOUT: Duration = Duration::from_secs(5);

/// The 8-byte binary protocol message header.
const HEADER_SIZE: usize = 8;

/// State for one in-flight fragmented message.
struct InFlightMessage {
    /// Received fragment payloads, indexed by seq_num.
    /// `None` at index i means fragment i not yet received.
    fragments: Vec<Option<Bytes>>,
    /// Total number of fragments expected.
    total: usize,
    /// How many fragments have arrived.
    received: usize,
    /// When the first fragment arrived (for timeout detection).
    first_arrived: Instant,
    /// Opcode of this message.
    opcode: u8,
}

impl InFlightMessage {
    fn new(opcode: u8, total: usize) -> Self {
        Self {
            fragments: vec![None; total],
            total,
            received: 0,
            first_arrived: Instant::now(),
            opcode,
        }
    }

    fn insert(&mut self, seq: usize, payload: Bytes) -> bool {
        if seq >= self.total {
            return false;
        }
        if self.fragments[seq].is_none() {
            self.fragments[seq] = Some(payload);
            self.received += 1;
        }
        self.received == self.total
    }

    fn is_timed_out(&self) -> bool {
        self.first_arrived.elapsed() > REASSEMBLY_TIMEOUT
    }

    fn reassemble(self) -> Bytes {
        let total_len: usize = self
            .fragments
            .iter()
            .filter_map(|f| f.as_ref())
            .map(|f| f.len())
            .sum();
        let mut buf = BytesMut::with_capacity(HEADER_SIZE + total_len);

        // Re-encode as a single non-fragmented message header.
        buf.put_u8(self.opcode);
        buf.put_u8(0); // flags: no FLAG_FRAGMENTED
        buf.put_u16_le(0); // reserved: 0
        buf.put_u32_le(total_len as u32);

        for fragment in self.fragments.into_iter().flatten() {
            buf.extend_from_slice(&fragment);
        }

        buf.freeze()
    }
}

/// Binary protocol message reassembler.
///
/// Tracks per-message reassembly state keyed by `(opcode_u8, total_count)`.
/// Each unique key corresponds to one in-flight fragmented message.
///
/// Architectural constraint: only one fragmented message of a given (opcode,
/// total_count) pair may be in flight at a time per connection. The current
/// architecture enforces this — each protocol handler owns one reassembler and
/// sends fragments of one message to completion before starting the next.
///
/// Sender restart detection: if seq=0 arrives for an existing key the stale
/// partial is evicted and the new message starts cleanly. This handles connection
/// reset without corrupting the new message's payload.
///
/// Stale entry eviction: timed-out partials are evicted inside `feed()`. No
/// background sweep runs — if data stops arriving entirely, stale entries remain
/// until the next `feed()` call. This is acceptable for the per-connection use case.
///
/// Usage:
/// ```ignore
/// let mut reasm = MessageReassembler::new();
/// for raw_frame in incoming_frames {
///     match reasm.feed(raw_frame) {
///         Some(complete_msg) => { /* deliver to application */ }
///         None => { /* fragment buffered, waiting for more */ }
///     }
/// }
/// ```
pub struct MessageReassembler {
    /// Keyed by (opcode, total_count) — supports multi-message isolation (T-079 AC-4).
    in_flight: HashMap<(u8, u8), InFlightMessage>,
}

impl MessageReassembler {
    pub fn new() -> Self {
        Self {
            in_flight: HashMap::new(),
        }
    }

    /// Feed a raw message frame (with 8-byte header) into the reassembler.
    ///
    /// - Non-fragmented messages (FLAG_FRAGMENTED not set) are returned immediately.
    /// - Fragmented messages are buffered until all fragments arrive.
    /// - Returns the complete reassembled message when ready, or `None` if more fragments needed.
    /// - Returns `None` and logs an error for malformed frames.
    pub fn feed(&mut self, frame: Bytes) -> Option<Bytes> {
        if frame.len() < HEADER_SIZE {
            warn!("Reassembler: frame too short ({} bytes)", frame.len());
            return None;
        }

        let flags = frame[1];

        // Non-fragmented: return immediately (AC-1, backward-compat).
        if flags & FLAG_FRAGMENTED == 0 {
            return Some(frame);
        }

        // Fragmented message.
        let opcode = frame[0];
        let seq = frame[2]; // reserved[0] = seq_num
        let total = frame[3]; // reserved[1] = total_count
        let payload_len = u32::from_le_bytes([frame[4], frame[5], frame[6], frame[7]]) as usize;

        if frame.len() < HEADER_SIZE + payload_len {
            warn!(
                "Reassembler: fragment truncated (expected {} payload, got {})",
                payload_len,
                frame.len() - HEADER_SIZE
            );
            return None;
        }

        if total == 0 {
            warn!("Reassembler: fragment total_count=0 is invalid");
            return None;
        }

        let payload = frame.slice(HEADER_SIZE..HEADER_SIZE + payload_len);
        let key = (opcode, total);

        // Evict timed-out messages before inserting (T-079 AC-3).
        self.evict_timed_out();

        // seq=0 with an existing entry that already has seq=0 means the sender
        // restarted (duplicate seq=0 is not possible within one message). Evict the
        // stale partial so the new message starts clean.
        //
        // seq=0 arriving when the entry doesn't yet have seq=0 is normal out-of-order
        // delivery — don't evict in that case.
        if seq == 0 {
            let stale = self
                .in_flight
                .get(&key)
                .is_some_and(|m| m.fragments[0].is_some());
            if stale && self.in_flight.remove(&key).is_some() {
                warn!(
                    "Reassembler: duplicate seq=0 for (opcode=0x{:02X}, total={}); \
                     evicting stale partial (sender restart).",
                    opcode, total
                );
            }
        }

        let msg = self
            .in_flight
            .entry(key)
            .or_insert_with(|| InFlightMessage::new(opcode, total as usize));

        // AC-2 (T-078): out-of-order fragments — indexed by seq, order doesn't matter.
        let complete = msg.insert(seq as usize, payload);

        if complete {
            // All fragments received — reassemble.
            let complete_msg = self.in_flight.remove(&key).unwrap().reassemble();
            Some(complete_msg)
        } else {
            None
        }
    }

    /// Evict partial messages that have exceeded the timeout (T-079 AC-3).
    ///
    /// Discards the partial message and logs an error.
    fn evict_timed_out(&mut self) {
        self.in_flight.retain(|key, msg| {
            if msg.is_timed_out() {
                error!(
                    "Reassembler: timed out partial message (opcode=0x{:02X}, total={}, \
                     received={}/{}). Discarding.",
                    key.0, key.1, msg.received, msg.total
                );
                false // remove
            } else {
                true // keep
            }
        });
    }
}

impl Default for MessageReassembler {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::binary::{BinaryEncoder, Opcode, FLAG_FRAGMENTED, FRAGMENT_PAYLOAD_SIZE};

    // AC-1: In-order fragments reassembled with byte-exact fidelity.
    #[test]
    fn test_in_order_reassembly() {
        let mut enc = BinaryEncoder::new();
        let payload = vec![0xAAu8; FRAGMENT_PAYLOAD_SIZE + 100]; // 2 fragments
        let frames = enc.fragment_message(Opcode::Image, 0, &payload);
        assert_eq!(frames.len(), 2);

        let mut reasm = MessageReassembler::new();

        // Feed fragment 0 — not complete yet.
        assert!(reasm.feed(frames[0].clone()).is_none());
        // Feed fragment 1 — complete.
        let complete = reasm.feed(frames[1].clone()).expect("should reassemble");

        // Verify byte-exact fidelity (AC-1).
        let reassembled_payload = &complete[HEADER_SIZE..];
        assert_eq!(
            reassembled_payload,
            payload.as_slice(),
            "payload must be byte-exact"
        );
        // FLAG_FRAGMENTED must not be set in the reassembled message.
        assert_eq!(
            complete[1] & FLAG_FRAGMENTED,
            0,
            "reassembled message must not be flagged"
        );
    }

    // AC-2 (T-078): Out-of-order fragments reassembled correctly.
    #[test]
    fn test_out_of_order_reassembly() {
        let mut enc = BinaryEncoder::new();
        let payload: Vec<u8> = (0u8..=255)
            .cycle()
            .take(FRAGMENT_PAYLOAD_SIZE + 50)
            .collect();
        let frames = enc.fragment_message(Opcode::Audio, 0, &payload);
        assert_eq!(frames.len(), 2);

        let mut reasm = MessageReassembler::new();

        // Feed out of order: fragment 1 first.
        assert!(reasm.feed(frames[1].clone()).is_none());
        let complete = reasm.feed(frames[0].clone()).expect("should reassemble");
        let reassembled_payload = &complete[HEADER_SIZE..];
        assert_eq!(
            reassembled_payload,
            payload.as_slice(),
            "out-of-order payload must match"
        );
    }

    // AC-5 (backward compat): Non-fragmented message returned immediately.
    #[test]
    fn test_non_fragmented_passthrough() {
        let mut enc = BinaryEncoder::new();
        let payload = vec![0xBBu8; 10];
        let frames = enc.fragment_message(Opcode::Key, 0, &payload);
        assert_eq!(frames.len(), 1, "small payload must produce single frame");

        let mut reasm = MessageReassembler::new();
        let result = reasm
            .feed(frames[0].clone())
            .expect("non-fragmented must pass through");
        assert_eq!(result[0], Opcode::Key as u8);
        assert_eq!(result[1] & FLAG_FRAGMENTED, 0);
    }

    // Sender restart: seq=0 for an existing key evicts the stale partial and
    // the new message completes correctly with the new payload.
    #[test]
    fn test_sender_restart_evicts_stale_partial() {
        let mut enc = BinaryEncoder::new();
        let payload_a = vec![0xAAu8; FRAGMENT_PAYLOAD_SIZE + 10];
        let payload_b = vec![0xBBu8; FRAGMENT_PAYLOAD_SIZE + 10];

        // Both messages fragment into 2 pieces with the same opcode — same key.
        let frames_a = enc.fragment_message(Opcode::Image, 0, &payload_a);
        let frames_b = enc.fragment_message(Opcode::Image, 0, &payload_b);
        assert_eq!(frames_a.len(), 2);
        assert_eq!(frames_b.len(), 2);

        let mut reasm = MessageReassembler::new();

        // Feed only fragment 0 of message A (leaves a stale partial).
        assert!(reasm.feed(frames_a[0].clone()).is_none());

        // Sender restarts — message B's seq=0 must evict the stale A partial.
        assert!(
            reasm.feed(frames_b[0].clone()).is_none(),
            "seq=0 evicts stale, returns None"
        );

        // Message B completes with its own payload, not A's.
        let complete = reasm
            .feed(frames_b[1].clone())
            .expect("message B must complete");
        assert_eq!(
            &complete[HEADER_SIZE..],
            payload_b.as_slice(),
            "reassembled payload must be B's, not A's corrupted data"
        );
    }

    // AC-4 (T-079): Multi-message reassembly isolation.
    #[test]
    fn test_multi_message_isolation() {
        let mut enc = BinaryEncoder::new();
        let payload_a = vec![0xAAu8; FRAGMENT_PAYLOAD_SIZE + 1];
        let payload_b = vec![0xBBu8; FRAGMENT_PAYLOAD_SIZE + 1];

        let frames_a = enc.fragment_message(Opcode::Image, 0, &payload_a);
        let frames_b = enc.fragment_message(Opcode::Audio, 0, &payload_b);

        let mut reasm = MessageReassembler::new();

        // Interleave fragments.
        assert!(reasm.feed(frames_a[0].clone()).is_none());
        assert!(reasm.feed(frames_b[0].clone()).is_none());

        let complete_a = reasm
            .feed(frames_a[1].clone())
            .expect("message A must complete");
        let complete_b = reasm
            .feed(frames_b[1].clone())
            .expect("message B must complete");

        assert_eq!(
            complete_a[0],
            Opcode::Image as u8,
            "message A opcode must be Image"
        );
        assert_eq!(
            complete_b[0],
            Opcode::Audio as u8,
            "message B opcode must be Audio"
        );
        assert_eq!(&complete_a[HEADER_SIZE..], payload_a.as_slice());
        assert_eq!(&complete_b[HEADER_SIZE..], payload_b.as_slice());
    }
}
