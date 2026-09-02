use crate::{
    make_encoder, pipeline::EncoderPipeline, EncodedFrame, EncoderBackendKind, RgbaFrame,
    VideoEncoder,
};
use bytes::Bytes;
use std::sync::{Arc, Mutex};
use std::time::Duration;

fn tiny_frame(ts: u64) -> RgbaFrame {
    RgbaFrame {
        data: vec![0x40u8; 32 * 32 * 4],
        width: 32,
        height: 32,
        timestamp_us: ts,
    }
}

#[test]
fn submit_and_drain_produces_frame() {
    let pipeline = EncoderPipeline::new(make_encoder(32, 32).unwrap());
    pipeline.submit(tiny_frame(0), false);
    std::thread::sleep(Duration::from_millis(300));
    assert!(!pipeline.drain().is_empty());
}

#[test]
fn first_drained_frame_is_keyframe() {
    let pipeline = EncoderPipeline::new(make_encoder(32, 32).unwrap());
    pipeline.submit(tiny_frame(0), false);
    std::thread::sleep(Duration::from_millis(300));
    assert!(pipeline.drain().into_iter().next().unwrap().is_keyframe);
}

#[test]
fn forced_keyframe_flag_is_honoured() {
    let pipeline = EncoderPipeline::new(make_encoder(32, 32).unwrap());
    pipeline.submit(tiny_frame(0), false);
    std::thread::sleep(Duration::from_millis(300));
    let _ = pipeline.drain();
    pipeline.submit(tiny_frame(1), false);
    std::thread::sleep(Duration::from_millis(300));
    let _ = pipeline.drain();
    pipeline.submit(tiny_frame(2), true);
    std::thread::sleep(Duration::from_millis(300));
    assert!(pipeline.drain().into_iter().next().unwrap().is_keyframe);
}

#[test]
fn drop_does_not_hang() {
    let pipeline = EncoderPipeline::new(make_encoder(32, 32).unwrap());
    pipeline.submit(tiny_frame(0), false);
    drop(pipeline);
}

/// Encoder that emits a zero-length frame first (an encoder holding back output,
/// e.g. FFmpeg EAGAIN), then real frames. Used to prove the pipeline never
/// forwards empty frames to the video track.
struct EagainThenDataEncoder {
    calls: u64,
}

impl VideoEncoder for EagainThenDataEncoder {
    fn encode(&mut self, _frame: &RgbaFrame) -> anyhow::Result<EncodedFrame> {
        self.calls += 1;
        if self.calls == 1 {
            Ok(EncodedFrame {
                data: Bytes::new(),
                is_keyframe: false,
                pts: 0,
            })
        } else {
            Ok(EncodedFrame {
                data: Bytes::from_static(&[0, 0, 0, 1, 0x65]),
                is_keyframe: true,
                pts: self.calls * 3000,
            })
        }
    }
    fn request_keyframe(&mut self) {}
    fn set_target_bitrate(&mut self, _bps: u32) {}
    fn frame_count(&self) -> u64 {
        self.calls
    }
    fn dimensions(&self) -> (u32, u32) {
        (32, 32)
    }
    fn backend_kind(&self) -> EncoderBackendKind {
        EncoderBackendKind::Software
    }
}

/// Records the order of `encode`/`set_target_bitrate` calls it receives, so a test can
/// prove a pending bitrate is never applied before the encoder's first `encode()` — which
/// silently no-ops on real openh264 (measured 2026-08-04: a 100kbps target went untracked,
/// ~3-4x overshoot, if set before any encode, vs. tracked within ~17% if set after).
struct EventLogEncoder {
    log: Arc<Mutex<Vec<String>>>,
    calls: u64,
}

impl VideoEncoder for EventLogEncoder {
    fn encode(&mut self, _frame: &RgbaFrame) -> anyhow::Result<EncodedFrame> {
        self.calls += 1;
        self.log.lock().unwrap().push("encode".to_string());
        Ok(EncodedFrame {
            data: Bytes::from_static(&[0, 0, 0, 1, 0x65]),
            is_keyframe: true,
            pts: self.calls * 3000,
        })
    }
    fn request_keyframe(&mut self) {}
    fn set_target_bitrate(&mut self, bps: u32) {
        self.log
            .lock()
            .unwrap()
            .push(format!("set_target_bitrate({bps})"));
    }
    fn frame_count(&self) -> u64 {
        self.calls
    }
    fn dimensions(&self) -> (u32, u32) {
        (8, 8)
    }
    fn backend_kind(&self) -> EncoderBackendKind {
        EncoderBackendKind::Software
    }
}

/// A bitrate estimate arriving before the very first frame is ever submitted must wait
/// for that first `encode()` to complete, not be silently dropped — see `EventLogEncoder`.
#[test]
fn pending_bitrate_before_first_frame_is_deferred_not_dropped() {
    let log = Arc::new(Mutex::new(Vec::new()));
    let pipeline = EncoderPipeline::new(Box::new(EventLogEncoder {
        log: log.clone(),
        calls: 0,
    }));

    // Set before any frame has ever been submitted.
    pipeline.set_target_bitrate(555_000);

    let mk = |ts: u64| RgbaFrame {
        data: vec![0u8; 8 * 8 * 4],
        width: 8,
        height: 8,
        timestamp_us: ts,
    };
    pipeline.submit(mk(0), false);
    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    while pipeline.drain().is_empty() && std::time::Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(5));
    }
    assert_eq!(
        log.lock().unwrap().first().cloned(),
        Some("encode".to_string()),
        "first encoder call must be encode, not the pending set_target_bitrate"
    );

    // A second frame gives the deferred bitrate its chance to apply — it must not have
    // been dropped by skipping it on the first frame.
    pipeline.submit(mk(1), false);
    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    let mut got = 0;
    while got < 1 && std::time::Instant::now() < deadline {
        got += pipeline.drain().len();
        std::thread::sleep(Duration::from_millis(5));
    }
    assert!(
        log.lock()
            .unwrap()
            .contains(&"set_target_bitrate(555000)".to_string()),
        "pending bitrate must be applied on a later frame, not dropped: {:?}",
        log.lock().unwrap()
    );
}

/// Mock encoder pinned to explicit dimensions, for reconfiguration tests.
struct FixedDimsEncoder {
    w: u32,
    h: u32,
    calls: u64,
    kind: EncoderBackendKind,
}

impl FixedDimsEncoder {
    fn new(w: u32, h: u32) -> Self {
        Self {
            w,
            h,
            calls: 0,
            kind: EncoderBackendKind::Software,
        }
    }
}

impl VideoEncoder for FixedDimsEncoder {
    fn encode(&mut self, _frame: &RgbaFrame) -> anyhow::Result<EncodedFrame> {
        self.calls += 1;
        Ok(EncodedFrame {
            data: Bytes::from_static(&[0, 0, 0, 1, 0x65]),
            is_keyframe: true,
            pts: self.calls * 3000,
        })
    }
    fn request_keyframe(&mut self) {}
    fn set_target_bitrate(&mut self, _bps: u32) {}
    fn frame_count(&self) -> u64 {
        self.calls
    }
    fn dimensions(&self) -> (u32, u32) {
        (self.w, self.h)
    }
    fn backend_kind(&self) -> EncoderBackendKind {
        self.kind
    }
}

/// A BWE resolution step submits frames at a new geometry; the worker must rebuild
/// the encoder via the factory (off the session loop) and keep encoding. This is
/// what makes `resolution_scale_pct` consumable without any handler-side encoder
/// management.
#[test]
fn dimension_change_rebuilds_the_encoder_via_factory() {
    use std::sync::atomic::AtomicU32;
    let rebuilt_to = Arc::new(AtomicU32::new(0));
    let observer = rebuilt_to.clone();

    let pipeline = EncoderPipeline::with_factory(
        Box::new(FixedDimsEncoder::new(8, 8)),
        Box::new(move |w, h| {
            observer.store(w * 10_000 + h, std::sync::atomic::Ordering::Relaxed);
            Ok(Box::new(FixedDimsEncoder::new(w, h)))
        }),
    );

    let mk = |w: u32, h: u32| RgbaFrame {
        data: vec![0u8; (w * h * 4) as usize],
        width: w,
        height: h,
        timestamp_us: 0,
    };

    // Same geometry as the encoder: no rebuild.
    pipeline.submit(mk(8, 8), false);
    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    let mut got = 0;
    while got < 1 && std::time::Instant::now() < deadline {
        got += pipeline.drain().len();
        std::thread::sleep(Duration::from_millis(5));
    }
    assert_eq!(got, 1, "same-geometry frame must encode");
    assert_eq!(
        rebuilt_to.load(std::sync::atomic::Ordering::Relaxed),
        0,
        "factory must not run without a dimension change"
    );

    // New geometry (a 50% step of 8x8): rebuild, then the frame still encodes.
    pipeline.submit(mk(4, 4), false);
    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    while got < 2 && std::time::Instant::now() < deadline {
        got += pipeline.drain().len();
        std::thread::sleep(Duration::from_millis(5));
    }
    assert_eq!(
        got, 2,
        "frame at the new geometry must encode after rebuild"
    );
    assert_eq!(
        rebuilt_to.load(std::sync::atomic::Ordering::Relaxed),
        4 * 10_000 + 4,
        "factory must be called with the new geometry"
    );
}

/// `EncoderPipeline::backend_kind()` must reflect the live encoder: the constructor's
/// initial value, and whatever the factory produces on a rebuild — this is what lets a
/// handler raise its resolution ceiling once hardware encode is confirmed running.
#[test]
fn backend_kind_reflects_construction_and_rebuild() {
    let pipeline = EncoderPipeline::with_factory(
        Box::new(FixedDimsEncoder::new(8, 8)),
        Box::new(|w, h| {
            let mut enc = FixedDimsEncoder::new(w, h);
            enc.kind = EncoderBackendKind::Hardware;
            Ok(Box::new(enc))
        }),
    );
    assert_eq!(pipeline.backend_kind(), EncoderBackendKind::Software);

    let mk = |w: u32, h: u32| RgbaFrame {
        data: vec![0u8; (w * h * 4) as usize],
        width: w,
        height: h,
        timestamp_us: 0,
    };
    pipeline.submit(mk(4, 4), false);
    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    while pipeline.drain().is_empty() && std::time::Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(5));
    }
    assert_eq!(
        pipeline.backend_kind(),
        EncoderBackendKind::Hardware,
        "backend_kind must reflect the rebuilt encoder"
    );
}

/// After the worker encodes a frame, its buffer must be back in the pool — and the
/// ordering guarantee is that recycling happens BEFORE the encoded frame is
/// observable via drain(), so this test is deterministic, not timing-dependent.
#[test]
fn frame_buffers_are_recycled_after_encode() {
    let pipeline = EncoderPipeline::new(make_encoder(32, 32).unwrap());

    // Cold start: pool is empty, acquire hands out a fresh buffer.
    assert_eq!(pipeline.pooled_buffer_count(), 0);
    let mut buf = pipeline.acquire_frame_buffer();
    assert!(buf.is_empty());
    buf.extend_from_slice(&vec![0x40u8; 32 * 32 * 4]);
    let cap = buf.capacity();
    pipeline.submit(
        RgbaFrame {
            data: buf,
            width: 32,
            height: 32,
            timestamp_us: 0,
        },
        false,
    );

    // Wait until the encoded frame is observable — at that point the buffer is
    // guaranteed recycled (worker pushes to the pool before sending the frame).
    let deadline = std::time::Instant::now() + Duration::from_secs(10);
    let mut drained = Vec::new();
    while drained.is_empty() && std::time::Instant::now() < deadline {
        drained = pipeline.drain();
        std::thread::sleep(Duration::from_millis(10));
    }
    assert!(!drained.is_empty(), "encoder produced no frame in 10s");
    assert_eq!(pipeline.pooled_buffer_count(), 1, "buffer must be recycled");

    // Warm acquire: the recycled buffer comes back cleared with its capacity intact —
    // no fresh allocation.
    let warm = pipeline.acquire_frame_buffer();
    assert!(warm.is_empty(), "recycled buffer must be cleared");
    assert_eq!(warm.capacity(), cap, "recycled, not reallocated");
    assert_eq!(pipeline.pooled_buffer_count(), 0);
}

/// Encoder that blocks until its gate is dropped/fed — lets a test hold the worker
/// mid-encode so latest-frame-wins eviction can be exercised deterministically.
struct GatedEncoder {
    gate: std::sync::mpsc::Receiver<()>,
    calls: u64,
}

impl VideoEncoder for GatedEncoder {
    fn encode(&mut self, _frame: &RgbaFrame) -> anyhow::Result<EncodedFrame> {
        // Blocks until the test sends a token or drops the sender.
        let _ = self.gate.recv();
        self.calls += 1;
        Ok(EncodedFrame {
            data: Bytes::from_static(&[0, 0, 0, 1, 0x65]),
            is_keyframe: true,
            pts: self.calls * 3000,
        })
    }
    fn request_keyframe(&mut self) {}
    fn set_target_bitrate(&mut self, _bps: u32) {}
    fn frame_count(&self) -> u64 {
        self.calls
    }
    fn dimensions(&self) -> (u32, u32) {
        (4, 4)
    }
    fn backend_kind(&self) -> EncoderBackendKind {
        EncoderBackendKind::Software
    }
}

/// While the worker is busy encoding, a newer submit displaces the queued frame
/// (latest-frame-wins). The displaced frame's buffer must be reclaimed into the
/// pool, not dropped — otherwise every eviction under load leaks an allocation's
/// worth of warm-up.
#[test]
fn evicted_frames_return_their_buffers_to_the_pool() {
    let (gate_tx, gate_rx) = std::sync::mpsc::channel();
    let pipeline = EncoderPipeline::new(Box::new(GatedEncoder {
        gate: gate_rx,
        calls: 0,
    }));

    let mk = |ts: u64| RgbaFrame {
        data: vec![0u8; 64],
        width: 4,
        height: 4,
        timestamp_us: ts,
    };

    // Three submits against a blocked worker: whichever interleaving occurs (worker
    // already took the first frame or not), exactly one queued frame is displaced
    // by the third submit and must land in the pool synchronously, producer-side.
    pipeline.submit(mk(0), false);
    std::thread::sleep(Duration::from_millis(50));
    pipeline.submit(mk(1), false);
    pipeline.submit(mk(2), false);
    assert!(
        pipeline.pooled_buffer_count() >= 1,
        "displaced frame's buffer must be reclaimed"
    );

    // Unblock the worker so Drop can join it.
    drop(gate_tx);
}

#[test]
fn empty_frames_are_never_forwarded() {
    let pipeline = EncoderPipeline::new(Box::new(EagainThenDataEncoder { calls: 0 }));
    pipeline.submit(tiny_frame(0), false);
    std::thread::sleep(Duration::from_millis(200));
    pipeline.submit(tiny_frame(1), false);
    std::thread::sleep(Duration::from_millis(200));
    let drained = pipeline.drain();
    assert!(
        !drained.is_empty(),
        "real frame must still come through the pipeline"
    );
    assert!(
        drained.iter().all(|f| !f.data.is_empty()),
        "zero-length frames must be dropped by the pipeline, not sent to write_sample"
    );
}
