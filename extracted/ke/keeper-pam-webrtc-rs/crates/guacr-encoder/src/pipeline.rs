//! Dedicated-thread encoder pipeline with latest-frame-wins drop semantics.

use crate::{EncodedFrame, EncoderBackendKind, RgbaFrame, VideoEncoder};
use crossbeam_queue::ArrayQueue;
use std::sync::{
    atomic::{AtomicBool, AtomicU32, AtomicU8, Ordering},
    Arc, Condvar, Mutex,
};

fn kind_to_u8(kind: EncoderBackendKind) -> u8 {
    match kind {
        EncoderBackendKind::Software => 0,
        EncoderBackendKind::Hardware => 1,
    }
}

fn u8_to_kind(v: u8) -> EncoderBackendKind {
    match v {
        1 => EncoderBackendKind::Hardware,
        _ => EncoderBackendKind::Software,
    }
}

/// Builds a replacement encoder when the submitted frame dimensions change — i.e.
/// when a BWE resolution step asks for a different encode geometry mid-session.
/// Runs on the worker thread, so a slow hardware-encoder open (~640 ms NVENC)
/// never blocks the session's select loop.
pub type EncoderFactory = Box<dyn Fn(u32, u32) -> anyhow::Result<Box<dyn VideoEncoder>> + Send>;

struct PipelineFrame {
    frame: RgbaFrame,
    force_keyframe: bool,
}

struct FrameSlot {
    queue: ArrayQueue<PipelineFrame>,
    ready: Mutex<bool>,
    cvar: Condvar,
    shutdown: AtomicBool,
}

impl FrameSlot {
    fn new() -> Arc<Self> {
        Arc::new(Self {
            queue: ArrayQueue::new(1),
            ready: Mutex::new(false),
            cvar: Condvar::new(),
            shutdown: AtomicBool::new(false),
        })
    }

    /// Returns the evicted frame, if latest-frame-wins displaced one, so its
    /// buffer can be recycled instead of dropped.
    fn submit(&self, frame: PipelineFrame) -> Option<PipelineFrame> {
        let evicted = self.queue.pop();
        let _ = self.queue.push(frame);
        *self.ready.lock().unwrap() = true;
        self.cvar.notify_one();
        evicted
    }

    fn wait_take(&self) -> Option<PipelineFrame> {
        let mut ready = self
            .cvar
            .wait_while(self.ready.lock().unwrap(), |r| {
                !*r && !self.shutdown.load(Ordering::Acquire)
            })
            .unwrap();
        *ready = false;
        self.queue.pop()
    }

    fn shutdown(&self) {
        self.shutdown.store(true, Ordering::Release);
        *self.ready.lock().unwrap() = true;
        self.cvar.notify_all();
    }

    fn is_shutdown(&self) -> bool {
        self.shutdown.load(Ordering::Acquire)
    }
}

/// A dedicated-thread H.264 encoder pipeline with latest-frame-wins eviction.
///
/// The receiver is wrapped in a Mutex so that EncoderPipeline is Sync, which is
/// required when IronRdpSession (which stores this pipeline) is held across .await
/// points in a Send future on a multi-threaded Tokio runtime.
pub struct EncoderPipeline {
    slot: Arc<FrameSlot>,
    pending_bitrate: Arc<AtomicU32>,
    encoded_rx: Mutex<std::sync::mpsc::Receiver<EncodedFrame>>,
    /// Recycled frame buffers. Framebuffer-sized RGBA copies (~8.3 MB at the 1080p
    /// clamp) were previously allocated fresh on every submit — a per-tick allocation
    /// on the session's select loop, violating the no-alloc-in-hot-path rule. The
    /// worker returns each buffer here after encode, and eviction reclaims displaced
    /// ones, so a steady session reaches zero per-frame allocations after warm-up.
    /// Lock-free (ArrayQueue); at most 2 buffers circulate (one encoding, one queued),
    /// capacity 4 gives slack without hoarding.
    buffer_pool: Arc<ArrayQueue<Vec<u8>>>,
    /// Published by the worker after construction and after every rebuild, so a handler
    /// can learn which backend is actually live (see `EncoderBackendKind`) without
    /// crossing onto the worker thread itself.
    backend_kind: Arc<AtomicU8>,
    worker: Option<std::thread::JoinHandle<()>>,
}

impl EncoderPipeline {
    /// Standard construction: dimension changes rebuild the encoder through
    /// `make_encoder`, so a BWE step re-runs the hardware-probe cascade.
    pub fn new(encoder: Box<dyn VideoEncoder>) -> Self {
        Self::with_factory(encoder, Box::new(crate::make_encoder))
    }

    /// Construction with an explicit rebuild factory — used by tests to observe
    /// reconfiguration without touching real encoders.
    pub fn with_factory(mut encoder: Box<dyn VideoEncoder>, factory: EncoderFactory) -> Self {
        let slot = FrameSlot::new();
        let slot2 = slot.clone();
        let pending_bitrate = Arc::new(AtomicU32::new(0));
        let bitrate2 = pending_bitrate.clone();
        let (encoded_tx, encoded_rx) = std::sync::mpsc::channel();
        let buffer_pool = Arc::new(ArrayQueue::new(4));
        let pool2 = Arc::clone(&buffer_pool);
        let backend_kind = Arc::new(AtomicU8::new(kind_to_u8(encoder.backend_kind())));
        let kind2 = Arc::clone(&backend_kind);

        let worker = std::thread::Builder::new()
            .name("guacr-encoder".to_owned())
            .spawn(move || {
                // True once `encoder` has completed at least one `encode()` call. Runtime
                // bitrate changes (`set_target_bitrate` -> openh264's raw ENCODER_OPTION_BITRATE)
                // are silently ineffective if applied before the encoder's first encode —
                // measured directly: identical config, calling set_target_bitrate before vs.
                // after a warm-up encode took a 100kbps target from ~3.5x overshoot (untracked)
                // to within ~17% (tracked). A freshly (re)built encoder starts unwarmed, so a
                // bitrate estimate already pending when the first frame after construction or
                // a resolution-step rebuild arrives must wait one frame, not be dropped.
                let mut encoder_is_warm = false;
                loop {
                    let pf = match slot2.wait_take() {
                        Some(f) => f,
                        None => {
                            if slot2.is_shutdown() {
                                break;
                            }
                            continue;
                        }
                    };
                    // BWE resolution step: the handler submitted a different geometry, so
                    // rebuild the encoder to match. The fresh encoder opens with an IDR,
                    // which is exactly what a resolution change needs on the wire. On
                    // rebuild failure, drop this frame (recycling its buffer) and keep the
                    // old encoder — the next same-geometry frame will encode again.
                    let dims = (pf.frame.width, pf.frame.height);
                    if dims != encoder.dimensions() {
                        match factory(dims.0, dims.1) {
                            Ok(rebuilt) => {
                                log::info!(
                                    "guacr-encoder: rebuilt encoder {}x{} -> {}x{} (resolution step)",
                                    encoder.dimensions().0,
                                    encoder.dimensions().1,
                                    dims.0,
                                    dims.1
                                );
                                encoder = rebuilt;
                                kind2.store(kind_to_u8(encoder.backend_kind()), Ordering::Release);
                                encoder_is_warm = false;
                            }
                            Err(e) => {
                                log::warn!(
                                    "guacr-encoder: encoder rebuild to {}x{} failed ({e}); frame dropped",
                                    dims.0,
                                    dims.1
                                );
                                let _ = pool2.push(pf.frame.data);
                                continue;
                            }
                        }
                    }
                    if encoder_is_warm {
                        let bps = bitrate2.swap(0, Ordering::Relaxed);
                        if bps > 0 {
                            encoder.set_target_bitrate(bps);
                        }
                    }
                    if pf.force_keyframe {
                        encoder.request_keyframe();
                    }
                    let result = encoder.encode(&pf.frame);
                    encoder_is_warm = true;
                    // Recycle the frame's buffer BEFORE forwarding the encoded output:
                    // once a consumer observes the encoded frame via drain(), the buffer
                    // is guaranteed back in the pool for the next acquire.
                    let _ = pool2.push(pf.frame.data);
                    match result {
                        // Zero-length output means the encoder is holding the frame back
                        // (e.g. FFmpeg EAGAIN) — never forward it; an empty sample must
                        // not reach the WebRTC video track.
                        Ok(ef) if ef.data.is_empty() => {
                            log::debug!("guacr-encoder: encode produced empty output (frame held back)");
                        }
                        Ok(ef) => {
                            log::debug!(
                                "guacr-encoder: encoded frame ({} bytes, keyframe={})",
                                ef.data.len(),
                                ef.is_keyframe
                            );
                            let _ = encoded_tx.send(ef);
                        }
                        Err(e) => log::warn!("guacr-encoder: {e}"),
                    }
                }
            })
            .expect("failed to spawn guacr-encoder thread");

        Self {
            slot,
            pending_bitrate,
            encoded_rx: Mutex::new(encoded_rx),
            buffer_pool,
            backend_kind,
            worker: Some(worker),
        }
    }

    /// Which backend the live encoder is — updated after every rebuild (BWE resolution
    /// step). A handler can consult this once after first construction to raise its
    /// resolution ceiling when hardware encode is actually running.
    pub fn backend_kind(&self) -> EncoderBackendKind {
        u8_to_kind(self.backend_kind.load(Ordering::Acquire))
    }

    /// Get a cleared buffer for the next frame — recycled after warm-up, freshly
    /// allocated only on a cold start or pool miss. Fill it (e.g. with
    /// `extend_from_slice`) and hand it back via `submit`.
    pub fn acquire_frame_buffer(&self) -> Vec<u8> {
        match self.buffer_pool.pop() {
            Some(mut buf) => {
                buf.clear();
                buf
            }
            None => Vec::new(),
        }
    }

    pub fn submit(&self, frame: RgbaFrame, force_keyframe: bool) {
        if let Some(evicted) = self.slot.submit(PipelineFrame {
            frame,
            force_keyframe,
        }) {
            // Latest-frame-wins displaced a queued frame; recycle its buffer.
            let _ = self.buffer_pool.push(evicted.frame.data);
        }
    }

    /// Number of buffers currently resting in the pool. Test-only observability.
    #[cfg(test)]
    pub fn pooled_buffer_count(&self) -> usize {
        self.buffer_pool.len()
    }

    pub fn set_target_bitrate(&self, bps: u32) {
        self.pending_bitrate.store(bps, Ordering::Relaxed);
    }

    pub fn drain(&self) -> Vec<EncodedFrame> {
        self.encoded_rx.lock().unwrap().try_iter().collect()
    }
}

impl Drop for EncoderPipeline {
    fn drop(&mut self) {
        self.slot.shutdown();
        if let Some(w) = self.worker.take() {
            let _ = w.join();
        }
    }
}
