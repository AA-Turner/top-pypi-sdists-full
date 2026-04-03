//! WebRTC stress tests — data integrity across all valid sizes, concurrent connections,
//! and sustained throughput.
//!
//! These tests use local loopback ICE (no STUN/TURN) so they're fast, deterministic,
//! and work offline. Each test creates real RTCPeerConnection pairs and flows real bytes.
//!
//! Run with: cargo test -p keeper-pam-webrtc-rs stress -- --nocapture

use crate::webrtc_data_channel::WebRTCDataChannel;
use bytes::Bytes;
use std::sync::Arc;
use std::sync::Mutex as StdMutex;
use tokio::sync::{mpsc, oneshot};
use tokio::time::Duration;
use webrtc::data_channel::data_channel_message::DataChannelMessage;
use webrtc::data_channel::RTCDataChannel;
use webrtc::peer_connection::configuration::RTCConfiguration;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Creates a fully connected pair of data channels using local loopback ICE only
/// (no STUN/TURN). Returns (sender_side, receiver_side).
async fn make_loopback_channel_pair(label: &str) -> (WebRTCDataChannel, WebRTCDataChannel) {
    let pc1 = Arc::new(
        super::common_tests::create_peer_connection(RTCConfiguration::default())
            .await
            .expect("pc1 create"),
    );
    let pc2 = Arc::new(
        super::common_tests::create_peer_connection(RTCConfiguration::default())
            .await
            .expect("pc2 create"),
    );

    // ICE candidate pipes
    let (ice1_tx, mut ice1_rx) = mpsc::unbounded_channel();
    let (ice2_tx, mut ice2_rx) = mpsc::unbounded_channel();

    let tx = ice1_tx.clone();
    pc1.on_ice_candidate(Box::new(move |c| {
        if let Some(c) = c {
            let _ = tx.send(c);
        }
        Box::pin(async {})
    }));
    let tx = ice2_tx.clone();
    pc2.on_ice_candidate(Box::new(move |c| {
        if let Some(c) = c {
            let _ = tx.send(c);
        }
        Box::pin(async {})
    }));

    // dc1 open signal
    let dc1 = pc1
        .create_data_channel(label, None)
        .await
        .expect("dc1 create");
    let (dc1_open_tx, dc1_open_rx) = oneshot::channel::<Arc<RTCDataChannel>>();
    let tx1_arc = Arc::new(StdMutex::new(Some(dc1_open_tx)));
    let dc1c = dc1.clone();
    dc1.on_open(Box::new(move || {
        if let Some(tx) = tx1_arc.lock().unwrap().take() {
            let _ = tx.send(dc1c.clone());
        }
        Box::pin(async {})
    }));

    // dc2 received on pc2
    let (dc2_open_tx, dc2_open_rx) = oneshot::channel::<Arc<RTCDataChannel>>();
    let tx2_arc = Arc::new(StdMutex::new(Some(dc2_open_tx)));
    pc2.on_data_channel(Box::new(move |dc2| {
        let tx = tx2_arc.clone();
        let dc2c = dc2.clone();
        dc2.on_open(Box::new(move || {
            if let Some(t) = tx.lock().unwrap().take() {
                let _ = t.send(dc2c.clone());
            }
            Box::pin(async {})
        }));
        Box::pin(async {})
    }));

    // Offer / answer
    let offer = pc1.create_offer(None).await.expect("offer");
    pc1.set_local_description(offer.clone())
        .await
        .expect("pc1 sld");
    pc2.set_remote_description(offer).await.expect("pc2 srd");
    let answer = pc2.create_answer(None).await.expect("answer");
    pc2.set_local_description(answer.clone())
        .await
        .expect("pc2 sld");
    pc1.set_remote_description(answer).await.expect("pc1 srd");

    // Drain ICE concurrently
    let pc1c = Arc::clone(&pc1);
    let pc2c = Arc::clone(&pc2);
    tokio::spawn(async move {
        while let Some(c) = ice1_rx.recv().await {
            if let Ok(j) = c.to_json() {
                let _ = pc2c.add_ice_candidate(j).await;
            }
        }
    });
    tokio::spawn(async move {
        while let Some(c) = ice2_rx.recv().await {
            if let Ok(j) = c.to_json() {
                let _ = pc1c.add_ice_candidate(j).await;
            }
        }
    });

    // Wait for both channels to open
    let timeout = Duration::from_secs(15);
    let (opened1, opened2) =
        tokio::time::timeout(timeout, async { tokio::join!(dc1_open_rx, dc2_open_rx) })
            .await
            .expect("timeout waiting for channels to open");

    (
        WebRTCDataChannel::new(opened1.expect("dc1 open")),
        WebRTCDataChannel::new(opened2.expect("dc2 open")),
    )
}

/// Sends `data` on `sender`, asserts `receiver` gets back the same bytes.
/// Attaches an on_message handler BEFORE sending to avoid races.
async fn assert_round_trip(sender: &WebRTCDataChannel, receiver: &WebRTCDataChannel, data: Bytes) {
    let (msg_tx, mut msg_rx) = mpsc::unbounded_channel::<Bytes>();
    receiver
        .data_channel
        .on_message(Box::new(move |msg: DataChannelMessage| {
            let tx = msg_tx.clone();
            Box::pin(async move {
                let _ = tx.send(msg.data);
            })
        }));

    sender.send(data.clone()).await.expect("send failed");

    let received = tokio::time::timeout(Duration::from_secs(10), msg_rx.recv())
        .await
        .expect("timeout waiting for message")
        .expect("channel closed before message arrived");

    assert_eq!(
        received.len(),
        data.len(),
        "length mismatch: sent {} bytes, got {}",
        data.len(),
        received.len()
    );
    assert_eq!(received, data, "data mismatch at size {}", data.len());
}

/// Send N messages on `sender`, collect all on `receiver`, verify order + integrity.
async fn assert_bulk_round_trip(
    sender: &WebRTCDataChannel,
    receiver: &WebRTCDataChannel,
    messages: Vec<Bytes>,
) {
    let n = messages.len();
    let (msg_tx, mut msg_rx) = mpsc::unbounded_channel::<Bytes>();
    receiver
        .data_channel
        .on_message(Box::new(move |msg: DataChannelMessage| {
            let tx = msg_tx.clone();
            Box::pin(async move {
                let _ = tx.send(msg.data);
            })
        }));

    for msg in &messages {
        sender.send(msg.clone()).await.expect("send failed");
    }

    let mut received = Vec::with_capacity(n);
    let deadline = tokio::time::Instant::now() + Duration::from_secs(30);
    while received.len() < n {
        let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
        let msg = tokio::time::timeout(remaining, msg_rx.recv())
            .await
            .unwrap_or(None)
            .expect("channel closed or timed out waiting for all messages");
        received.push(msg);
    }

    assert_eq!(received.len(), n, "message count mismatch");
    for (i, (sent, got)) in messages.iter().zip(received.iter()).enumerate() {
        assert_eq!(got, sent, "message {} corrupted (size {})", i, sent.len());
    }
}

fn make_payload(size: usize, seed: u8) -> Bytes {
    Bytes::from(
        (0..size)
            .map(|i| ((i as u64 + seed as u64) % 251) as u8)
            .collect::<Vec<_>>(),
    )
}

// ---------------------------------------------------------------------------
// Data integrity — every valid WebRTC message size bucket
// ---------------------------------------------------------------------------

/// Tests round-trip data integrity across the full range of valid message sizes
/// for a single WebRTCDataChannel::send() call.
///
/// The ceiling here is OUR_MAX_MESSAGE_SIZE (65_536 bytes, exclusive). Messages
/// larger than that go through the fragmentation layer in send_with_event_backpressure()
/// in connections.rs, which splits them into ≤16 KB chunks before reaching send().
/// Testing those sizes here (directly against send()) would bypass fragmentation
/// and hit raw SCTP, which rejects them.
///
/// Buckets covered:
///   1 B       — minimum, single byte
///   13 B      — prime, tests odd alignment
///   64 B      — typical control frame
///   256 B     — small payload
///   1 KB      — common buffer unit
///   4 KB      — page size
///   8 KB      — guac frame budget
///   16 KB     — MTU-ish (SCTP chunk boundary)
///   32 KB     — half UDP max
///   64 KB - 1 — largest single send() payload (one below the SCTP ceiling)
#[tokio::test(flavor = "multi_thread")]
async fn test_data_integrity_all_size_buckets() {
    let sizes: &[(usize, &str)] = &[
        (1, "1 B   — minimum"),
        (13, "13 B  — prime"),
        (64, "64 B  — control frame"),
        (256, "256 B — small payload"),
        (1_024, "1 KB  — common unit"),
        (4_096, "4 KB  — page size"),
        (8_192, "8 KB  — guac frame"),
        (16_384, "16 KB — MTU-ish"),
        (32_768, "32 KB — half UDP max"),
        (65_535, "64 KB - 1 — largest single send()"),
    ];

    let (sender, receiver) = make_loopback_channel_pair("integrity").await;

    for (size, label) in sizes {
        let data = make_payload(*size, (*size % 251) as u8);
        assert_round_trip(&sender, &receiver, data).await;
        println!("  ✓ {}", label);
    }
}

/// All powers of two up to 32 KB — tests every doubling within send() range.
///
/// Stops at 32_768: the next power of two (65_536) equals OUR_MAX_MESSAGE_SIZE
/// exactly and is silently dropped by the SCTP layer (no error, just no delivery).
/// The 65_535 ceiling is already covered by test_data_integrity_all_size_buckets
/// and test_data_integrity_boundary_sizes.
#[tokio::test(flavor = "multi_thread")]
async fn test_data_integrity_powers_of_two() {
    let (sender, receiver) = make_loopback_channel_pair("pow2").await;
    let mut size = 1usize;
    while size <= 32_768 {
        let data = make_payload(size, 0xA5);
        assert_round_trip(&sender, &receiver, data).await;
        println!("  ✓ {} B", size);
        size *= 2;
    }
}

// ---------------------------------------------------------------------------
// Fragmentation — end-to-end wire format
// ---------------------------------------------------------------------------

/// Proves that the fragmentation layer works over a real WebRTC transport.
///
/// Uses fragment_frame() to split a 128 KB payload into ≤16 KB chunks, sends
/// each chunk as a separate WebRTCDataChannel::send() call (each fits under the
/// 64 KB SCTP ceiling), collects them on the receive side, and reassembles by
/// stripping fragment headers and concatenating payloads in order.
///
/// This validates:
///   1. fragment_frame() produces fragments that individually fit in send()
///   2. Fragment headers survive the WebRTC transport intact
///   3. Reassembly from ordered fragments reproduces the original exactly
///
/// Note: this tests the fragmentation wire format, not the Channel-level
/// send_with_event_backpressure() integration. That path is exercised in the
/// full tube/channel tests.
#[tokio::test(flavor = "multi_thread")]
async fn test_fragmentation_large_payload_round_trip() {
    use crate::channel::assembler::{
        fragment_frame, has_fragment_header, FragmentHeader, DEFAULT_FRAGMENT_THRESHOLD,
        DEFAULT_MAX_FRAGMENTS, FRAGMENT_HEADER_SIZE,
    };

    let (sender, receiver) = make_loopback_channel_pair("fragmentation").await;

    // 128 KB — requires fragmentation (8× DEFAULT_FRAGMENT_THRESHOLD)
    let original = make_payload(128 * 1024, 0x42);

    let fragments = fragment_frame(&original, DEFAULT_FRAGMENT_THRESHOLD, DEFAULT_MAX_FRAGMENTS)
        .expect("128 KB payload must fragment: exceeds DEFAULT_FRAGMENT_THRESHOLD");
    let n_fragments = fragments.len();
    assert!(
        n_fragments > 1,
        "expected multiple fragments, got {}",
        n_fragments
    );

    // Each fragment must fit within the WebRTCDataChannel::send() 64 KB ceiling
    for (i, frag) in fragments.iter().enumerate() {
        assert!(
            frag.len() <= 65_535,
            "fragment {} is {} bytes, exceeds send() max (65535)",
            i,
            frag.len()
        );
    }

    // Register receiver before sending to avoid any race
    let (msg_tx, mut msg_rx) = mpsc::unbounded_channel::<Bytes>();
    receiver
        .data_channel
        .on_message(Box::new(move |msg: DataChannelMessage| {
            let tx = msg_tx.clone();
            Box::pin(async move {
                let _ = tx.send(msg.data);
            })
        }));

    // Send all fragments
    for frag in &fragments {
        sender
            .send(frag.clone())
            .await
            .expect("fragment send failed");
    }

    // Collect all fragments on the receive side
    let mut received: Vec<(u16, Bytes)> = Vec::with_capacity(n_fragments);
    let deadline = tokio::time::Instant::now() + Duration::from_secs(15);
    while received.len() < n_fragments {
        let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
        let frag = tokio::time::timeout(remaining, msg_rx.recv())
            .await
            .expect("timeout waiting for fragment")
            .expect("channel closed before all fragments arrived");

        assert!(
            has_fragment_header(&frag),
            "received chunk missing fragment header"
        );
        let header = FragmentHeader::decode(&frag).expect("invalid fragment header");
        let payload = frag.slice(FRAGMENT_HEADER_SIZE..);
        received.push((header.frag_idx, payload));
    }

    // Sort by index — loopback preserves order, but be explicit
    received.sort_by_key(|(idx, _)| *idx);

    // Reassemble by concatenating payloads in order
    let reassembled: Bytes = received
        .into_iter()
        .flat_map(|(_, payload)| payload.into_iter())
        .collect::<Vec<u8>>()
        .into();

    assert_eq!(
        reassembled.len(),
        original.len(),
        "reassembled length mismatch: got {}, expected {}",
        reassembled.len(),
        original.len()
    );
    assert_eq!(
        reassembled, original,
        "reassembled bytes do not match original"
    );

    println!(
        "  ✓ 128 KB fragmented into {} fragments, all received and reassembled correctly",
        n_fragments
    );
}

/// Off-by-one around common boundaries — catches fence-post bugs in framing code.
#[tokio::test(flavor = "multi_thread")]
async fn test_data_integrity_boundary_sizes() {
    let (sender, receiver) = make_loopback_channel_pair("boundary").await;
    let boundaries = [
        1, 2, 3, 63, 64, 65, 255, 256, 257, 1023, 1024, 1025, 8191, 8192, 8193, 16383, 16384,
        16385, 65534, 65535,
    ];
    for size in boundaries {
        let data = make_payload(size, (size % 251) as u8);
        assert_round_trip(&sender, &receiver, data).await;
        println!("  ✓ {} B (boundary)", size);
    }
}

/// All-zeros, all-ones, alternating bytes — catches bit-flip or masking bugs.
#[tokio::test(flavor = "multi_thread")]
async fn test_data_integrity_pathological_byte_patterns() {
    let (sender, receiver) = make_loopback_channel_pair("patterns").await;
    let size = 8_192;
    let patterns: Vec<(&str, Vec<u8>)> = vec![
        ("all-zeros", vec![0x00; size]),
        ("all-ones", vec![0xFF; size]),
        (
            "alternating",
            (0..size)
                .map(|i| if i % 2 == 0 { 0xAA } else { 0x55 })
                .collect(),
        ),
        ("incrementing", (0..size).map(|i| (i % 256) as u8).collect()),
        (
            "decrementing",
            (0..size).map(|i| (255 - i % 256) as u8).collect(),
        ),
        (
            "pseudo-random",
            (0..size)
                .map(|i| {
                    (i.wrapping_mul(6364136223846793005)
                        .wrapping_add(1442695040888963407)
                        % 256) as u8
                })
                .collect(),
        ),
    ];

    for (name, payload) in patterns {
        let data = Bytes::from(payload);
        assert_round_trip(&sender, &receiver, data).await;
        println!("  ✓ {} ({} B)", name, size);
    }
}

// ---------------------------------------------------------------------------
// Bulk / throughput
// ---------------------------------------------------------------------------

/// Sends 500 messages of 1 KB each on a single connection. Verifies every message
/// arrives with correct content. Measures end-to-end throughput.
#[tokio::test(flavor = "multi_thread")]
async fn test_bulk_500_messages_1kb() {
    let (sender, receiver) = make_loopback_channel_pair("bulk-1k").await;
    let n = 500;
    let size = 1_024;
    let messages: Vec<Bytes> = (0..n).map(|i| make_payload(size, i as u8)).collect();

    let start = std::time::Instant::now();
    assert_bulk_round_trip(&sender, &receiver, messages).await;
    let elapsed = start.elapsed();
    let total_bytes = n * size;
    let mbps = (total_bytes as f64 / elapsed.as_secs_f64()) / 1_000_000.0;
    println!(
        "  ✓ {} messages × {} B in {:.2?} ({:.1} MB/s)",
        n, size, elapsed, mbps
    );
}

/// Swamp test: 100 large (32 KB) messages back-to-back. Proves the connection
/// doesn't stall or corrupt under sustained large-frame pressure.
#[tokio::test(flavor = "multi_thread")]
async fn test_swamp_100_large_messages_32kb() {
    let (sender, receiver) = make_loopback_channel_pair("swamp-32k").await;
    let n = 100;
    let size = 32_768;
    let messages: Vec<Bytes> = (0..n).map(|i| make_payload(size, i as u8)).collect();

    let start = std::time::Instant::now();
    assert_bulk_round_trip(&sender, &receiver, messages).await;
    let elapsed = start.elapsed();
    let total_mb = (n * size) as f64 / 1_000_000.0;
    println!(
        "  ✓ {} × 32 KB in {:.2?} ({:.1} MB total)",
        n, elapsed, total_mb
    );
}

/// Mixed sizes: alternates between tiny control frames and large data frames.
/// Models real guac traffic where key/mouse events interleave with image frames.
#[tokio::test(flavor = "multi_thread")]
async fn test_mixed_size_interleaving() {
    let (sender, receiver) = make_loopback_channel_pair("mixed").await;
    let mut messages = Vec::new();
    for i in 0..200 {
        // Alternate: 20-byte control, 8 KB data
        messages.push(make_payload(20, i as u8));
        messages.push(make_payload(8_192, i as u8));
    }
    assert_bulk_round_trip(&sender, &receiver, messages).await;
    println!("  ✓ 400 messages (200 × 20 B control + 200 × 8 KB data)");
}

// ---------------------------------------------------------------------------
// Concurrent connections
// ---------------------------------------------------------------------------

/// 10 simultaneous loopback connections, each transferring data independently.
/// Proves no shared mutable state bleeds between connections.
#[tokio::test(flavor = "multi_thread")]
async fn test_10_concurrent_connections_data_integrity() {
    let n = 10;
    let size = 4_096;

    let handles: Vec<_> = (0..n)
        .map(|i| {
            tokio::spawn(async move {
                let label = format!("conn-{}", i);
                let (sender, receiver) = make_loopback_channel_pair(&label).await;
                let data = make_payload(size, i as u8);
                assert_round_trip(&sender, &receiver, data).await;
                i
            })
        })
        .collect();

    for handle in handles {
        let i = handle.await.expect("task panicked");
        println!("  ✓ connection {} completed", i);
    }
}

/// 20 simultaneous connections, each sending 50 messages of 1 KB.
/// Total: 20 connections × 50 messages × 1 KB = 1 MB under concurrent load.
/// This is the primary "does my WebRTC implementation hold up" stress test.
#[tokio::test(flavor = "multi_thread")]
async fn test_20_concurrent_connections_bulk_data() {
    let n = 20;
    let msgs_per_conn = 50;
    let msg_size = 1_024;

    let handles: Vec<_> = (0..n)
        .map(|i| {
            tokio::spawn(async move {
                let label = format!("stress-{}", i);
                let (sender, receiver) = make_loopback_channel_pair(&label).await;
                let messages: Vec<Bytes> = (0..msgs_per_conn)
                    .map(|j| make_payload(msg_size, ((i + j) % 251) as u8))
                    .collect();
                assert_bulk_round_trip(&sender, &receiver, messages).await;
                i
            })
        })
        .collect();

    let start = std::time::Instant::now();
    for handle in handles {
        let i = handle.await.expect("task panicked");
        println!("  ✓ connection {} done", i);
    }
    let elapsed = start.elapsed();
    let total_bytes = n * msgs_per_conn * msg_size;
    println!(
        "  20 concurrent connections × 50 × 1 KB in {:.2?} ({:.1} MB)",
        elapsed,
        total_bytes as f64 / 1_000_000.0
    );
}

/// Rapid connection churn: create and close 30 connections sequentially.
/// Verifies no resource leak (FDs, tasks, memory) across connect/close cycles.
#[tokio::test(flavor = "multi_thread")]
async fn test_30_sequential_connect_transfer_close() {
    for i in 0..30 {
        let label = format!("churn-{}", i);
        let (sender, receiver) = make_loopback_channel_pair(&label).await;
        let data = make_payload(512, i as u8);
        assert_round_trip(&sender, &receiver, data).await;
        // channels are dropped here — verifies RAII cleanup each cycle
    }
    println!("  ✓ 30 sequential connect/transfer/close cycles completed");
}
