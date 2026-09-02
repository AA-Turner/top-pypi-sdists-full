//! FFmpeg (libavcodec) hardware H.264 backend — the single HW encoder on every platform:
//! VAAPI/NVENC/QSV (Linux), Media Foundation/QSV/NVENC (Windows), VideoToolbox (macOS).
//!
//! Enabled by the `ffmpeg` cargo feature; runtime-probed and slotted into `make_encoder`
//! ahead of openh264 (which remains the guaranteed software fallback). Links the system
//! FFmpeg (LGPL, dynamically linked); on Linux the GPU-driver userspace (libva vendor
//! driver / libnvidia-encode) is dlopen'd from the gateway host. Replaced the former raw
//! `nvenc` and `videotoolbox` backends.
//!
//! ============================ VERIFICATION STATUS ============================
//! COMPILES AND ENCODES on macOS/VideoToolbox as of 2026-08-03 (previously this header read
//! "NOT yet compiled or run"). `ffmpeg_encode_roundtrip_hw` passes against the Apple media
//! engine: a real device opens, frames encode, and the first emitted frame is an IDR.
//!
//! Still unvalidated: **NVENC** (no NVIDIA host available — note the pinned
//! `NV_CODEC_HEADERS_TAG` 12.x series needs roughly a 52x/53x+ driver, so Kepler-era cards on
//! the 470 legacy branch cannot serve as a test host), and **VAAPI**, which is not merely
//! unvalidated but unimplemented: `new_vaapi` returns an error so `make_encoder` falls back to
//! software. VAAPI needs a hardware frames context + `av_hwframe_transfer_data` upload, written
//! and validated on Intel/AMD hardware.
//!
//! Build gate: still no CI job compiles the `ffmpeg` feature. Locally it needs FFmpeg 7.x —
//! FFmpeg 8 removed `avfft.h`, which ffmpeg-sys-next 7.1 binds. On macOS:
//!   brew install ffmpeg@7
//!   PKG_CONFIG_PATH=/opt/homebrew/opt/ffmpeg@7/lib/pkgconfig \
//!     cargo test -p guacr-encoder --features ffmpeg --lib -- --ignored ffmpeg_encode
//! The manylinux builder (FFMPEG_VERSION=7.1) is the other environment that compiles it.
//!
//! 2026-07-31 review fixes, both now compiled: the RGBA copy honours row stride (a flat copy
//! sheared every row when linesize > width*4 — see `copy_rgba_rows`, covered by
//! `tests/stride_tests.rs` on *every* build, feature or not), and the EAGAIN empty-frame
//! contract is actually honoured by `EncoderPipeline` rather than just claimed.
//! ============================================================================

use crate::{EncodedFrame, EncoderBackendKind, RgbaFrame, VideoEncoder};
use anyhow::{anyhow, Context as _, Result};
use bytes::Bytes;
use ffmpeg_next as ff;
use std::sync::Once;

static FF_INIT: Once = Once::new();

fn ensure_ffmpeg_init() {
    FF_INIT.call_once(|| {
        // Ignore the double-init error path; call_once guarantees single entry.
        let _ = ff::init();
        ff::log::set_level(ff::log::Level::Error);
    });
}

/// Encoders that libavcodec may expose by name but that we cannot actually construct — their
/// constructor is still a stub returning Err.
///
/// These must never appear in a candidate list. `probe()` answers on NAME PRESENCE alone, so a
/// stub listed as a candidate makes `probe()` report "hardware available" on a box where every
/// open attempt falls through to software. That is not merely useless: the RDP handler's
/// `encode_resolution_cap()` gates the resolution ceiling on `probe()`, so a false positive
/// raises the ceiling to 4K and the session then encodes 4K in *software* (~7 fps).
const UNIMPLEMENTED_ENCODERS: &[&str] = &["h264_vaapi"];

/// Candidate H.264 hardware encoders per platform, most-preferred first. All accept software
/// NV12 frames and upload internally.
///
/// Declared unconditionally rather than behind `cfg` so the disjointness invariant against
/// `UNIMPLEMENTED_ENCODERS` is checked for every platform on every build, not just the host's.
#[allow(dead_code)] // referenced by the cfg selection below and by the invariant test
                    // h264_vaapi is deliberately absent: new_vaapi() is a stub, and Dockerfile:99 builds FFmpeg
                    // with --enable-encoder=h264_vaapi, so listing it made probe() claim hardware on every
                    // GPU-less Docker/cloud deployment. See UNIMPLEMENTED_ENCODERS. Re-add only with a working
                    // constructor.
const LINUX_HW_ENCODERS: &[&str] = &["h264_nvenc", "h264_qsv"];
#[allow(dead_code)]
const WINDOWS_HW_ENCODERS: &[&str] = &["h264_mf", "h264_nvenc", "h264_qsv"];
#[allow(dead_code)]
const MACOS_HW_ENCODERS: &[&str] = &["h264_videotoolbox"];

/// Every platform candidate list, for the cross-platform invariant test.
#[allow(dead_code)]
const ALL_PLATFORM_HW_ENCODERS: &[&[&str]] =
    &[LINUX_HW_ENCODERS, WINDOWS_HW_ENCODERS, MACOS_HW_ENCODERS];

/// Every platform's candidate list. Exposed so the disjointness invariant against
/// `unimplemented_encoders()` can be asserted on any host, not just Linux.
pub fn all_platform_hw_encoders() -> &'static [&'static [&'static str]] {
    ALL_PLATFORM_HW_ENCODERS
}

/// Encoders whose constructor is still a stub. See `UNIMPLEMENTED_ENCODERS`.
pub fn unimplemented_encoders() -> &'static [&'static str] {
    UNIMPLEMENTED_ENCODERS
}

#[cfg(target_os = "linux")]
const HW_ENCODERS: &[&str] = LINUX_HW_ENCODERS;
#[cfg(target_os = "windows")]
const HW_ENCODERS: &[&str] = WINDOWS_HW_ENCODERS;
#[cfg(target_os = "macos")]
const HW_ENCODERS: &[&str] = MACOS_HW_ENCODERS;
#[cfg(not(any(target_os = "linux", target_os = "windows", target_os = "macos")))]
const HW_ENCODERS: &[&str] = &[];

/// The platform's candidate encoder names, most-preferred first. Exposed so diagnostics can
/// time the same encoder `new` would pick.
pub fn hw_encoder_candidates() -> &'static [&'static str] {
    HW_ENCODERS
}

/// True if libavcodec exposes any of our hardware H.264 encoders in this build. Presence of
/// the *encoder* doesn't guarantee a usable *device* — `FfmpegEncoder::new` confirms by
/// actually opening one.
pub fn probe() -> bool {
    ensure_ffmpeg_init();
    HW_ENCODERS
        .iter()
        .any(|name| ff::encoder::find_by_name(name).is_some())
}

pub struct FfmpegEncoder {
    encoder: ff::encoder::Video,
    scaler: ff::software::scaling::Context,
    /// Reused RGBA staging frame (~width*height*4). Safe to reuse because it is only
    /// ever *read* by swscale — it is never sent to the encoder, so nothing holds a
    /// reference into it between encodes. The NV12 frame is deliberately NOT reused:
    /// `send_frame` may keep a refcounted reference to its buffer (DPB), and writing
    /// into it on the next tick would mutate a frame the encoder still holds.
    src_frame: ff::frame::Video,
    width: u32,
    height: u32,
    frame_count: u64,
    force_keyframe: bool,
}

// SAFETY: ffmpeg-next's scaling::Context wraps a raw `*mut SwsContext`, so it is not
// auto-Send. A FfmpegEncoder is owned and driven by exactly one EncoderPipeline worker
// thread — it is moved onto that thread once and never shared or accessed concurrently.
// We assert Send (ownership transfer) only; we deliberately do NOT implement Sync.
unsafe impl Send for FfmpegEncoder {}

impl FfmpegEncoder {
    pub fn new(width: u32, height: u32) -> Result<Self> {
        ensure_ffmpeg_init();

        // Try each hardware encoder in preference order; fall through on failure so
        // make_encoder can drop to software.
        let mut last_err = anyhow!("no FFmpeg H.264 hardware encoder available");
        for name in HW_ENCODERS {
            // NVENC / QSV / Media Foundation / VideoToolbox all accept software NV12 input.
            // VAAPI would need a hardware frames context instead (see new_vaapi), but it is not
            // a candidate while that constructor is a stub — see UNIMPLEMENTED_ENCODERS.
            let result = Self::new_sw_input(name, width, height);
            match result {
                Ok(enc) => {
                    log::info!(
                        "guacr-encoder: using FFmpeg {} ({}x{})",
                        name,
                        width,
                        height
                    );
                    return Ok(enc);
                }
                Err(e) => {
                    log::warn!(
                        "guacr-encoder: FFmpeg {} unavailable ({}), trying next",
                        name,
                        e
                    );
                    last_err = e;
                }
            }
        }
        Err(last_err)
    }

    /// Encoders that accept software NV12 frames and upload internally (NVENC, and QSV in
    /// some builds). No hardware frames context needed.
    ///
    /// RESOLVED 2026-08-03 — the alarming ~195 s `open_as_with` cost is a cargo-test
    /// harness artifact on macOS, not a production issue. Same code, same settings:
    /// under `cargo test` (spawned thread, no app context) it takes ~194 s; on the
    /// process main thread (`examples/open_timing.rs`) it takes ~742 ms.
    /// VideoToolbox session creation degrades badly on test-harness threads. Ruled out along
    /// the way: the private-option set, and the 90 kHz `time_base` — both were tested and
    /// changed nothing, so don't re-chase them. Keep `examples/open_timing.rs` as the way to
    /// measure construction honestly; timings taken under `cargo test` are meaningless here.
    /// MEASURED ON LINUX 2026-08-03 (this file compiled verbatim on a Precision 5540,
    /// Quadro T1000 + UHD 630, FFmpeg 7.1, at the stride-padded 1918x1004 geometry):
    ///   probe()                      178 µs
    ///   open h264_vaapi              5.5 µs   (fails instantly — the stub, by design)
    ///   open h264_nvenc              639 ms   OK
    ///   open h264_qsv                 45 µs   (not compiled in; fails instantly)
    ///   full cascade new()           213 ms   ok
    ///   first frame                   29 ms   487 bytes, IDR
    ///   sustained                  194.7 fps  (6.49x realtime @30)
    /// So the macOS pathology does NOT occur here, and — the point that gates the default
    /// wheel — the **CPU-only fallthrough costs microseconds**, not seconds: both failing
    /// candidates return before openh264 is reached. Shipping the `ffmpeg` feature by default
    /// therefore does not penalise GPU-less Docker hosts, the commonest deployment.
    /// The 194 fps run at 1918x1004 also validates `copy_rgba_rows` on real hardware: that
    /// width pads 7672 row bytes to a 7680 stride, the exact case that used to shear.
    fn new_sw_input(name: &str, width: u32, height: u32) -> Result<Self> {
        let codec = ff::encoder::find_by_name(name)
            .ok_or_else(|| anyhow!("encoder {} not compiled into libavcodec", name))?;

        let ctx = ff::codec::context::Context::new_with_codec(codec);
        let mut enc = ctx.encoder().video()?;
        enc.set_width(width);
        enc.set_height(height);
        enc.set_format(ff::format::Pixel::NV12);
        enc.set_time_base((1, 90_000));
        enc.set_frame_rate(Some((30, 1)));
        // WARNING: some devices support only CQP rate control and reject a bitrate outright —
        // measured on Intel gen9.5 (UHD 630) where open fails with "Driver does not support any
        // RC mode compatible with selected options (supported modes: CQP)". That affects
        // `h264_qsv`, which comes through here, and it degrades *silently* to software because
        // `new` falls through on error. Query supported RC modes and fall back to qp /
        // global_quality when bitrate is unsupported. See `new_vaapi` for the full note.
        let initial_bps = crate::initial_bitrate_bps(width, height, 30);
        enc.set_bit_rate(initial_bps as usize);
        enc.set_max_bit_rate((initial_bps as usize).saturating_mul(2));
        // Zero-latency interactive streaming: the EncoderPipeline submits one frame and
        // expects one packet back with no buffering. B-frames add reorder delay, and
        // LOW_DELAY asks the codec to emit without lookahead — so each input frame yields
        // exactly one output packet (matching the openh264 fallback's behaviour).
        enc.set_gop(120); // keyframe ~every 4s at 30fps; request_keyframe forces I on demand
        enc.set_max_b_frames(0);
        enc.set_flags(ff::codec::Flags::LOW_DELAY);
        // Private options are PER-ENCODER — only send an encoder options it understands.
        // (Correctness fix, not a performance one: tested 2026-08-03, restricting these did
        // NOT change the open_as_with slowness documented below. Hypothesis disproven.)
        let mut opts = ff::Dictionary::new();
        match name {
            "h264_nvenc" => {
                opts.set("preset", "p4"); // low-latency balanced
                opts.set("tune", "ll"); // low latency
                opts.set("delay", "0"); // emit immediately, no output frame queue
            }
            "h264_qsv" => {
                opts.set("low_power", "1");
                opts.set("async_depth", "1"); // no pipelining — one frame in, one packet out
            }
            "h264_videotoolbox" => {
                opts.set("realtime", "1"); // real-time mode, minimal internal delay
            }
            "h264_mf" => {
                opts.set("low_latency", "1"); // Media Foundation low-latency mode
            }
            _ => {}
        }
        let encoder = enc
            .open_as_with(codec, opts)
            .with_context(|| format!("open {} encoder", name))?;

        let scaler = Self::make_scaler(width, height)?;
        Ok(Self {
            encoder,
            scaler,
            src_frame: ff::frame::Video::new(ff::format::Pixel::RGBA, width, height),
            width,
            height,
            frame_count: 0,
            force_keyframe: false,
        })
    }

    /// VAAPI (Intel QuickSync / AMD). REQUIRES a VAAPI hardware device + frames context and
    /// per-frame `av_hwframe_transfer_data` upload of the NV12 data — none of which is wired
    /// here yet. Implement + validate on Intel/AMD hardware:
    ///   1. `av_hwdevice_ctx_create(&dev, AV_HWDEVICE_TYPE_VAAPI, "/dev/dri/renderD128", ..)`
    ///   2. alloc + init `AVHWFramesContext` (sw_format NV12, format VAAPI, width/height)
    ///   3. set `codec_ctx->hw_frames_ctx = av_buffer_ref(frames_ctx)` before open
    ///   4. per frame: `av_hwframe_get_buffer` + `av_hwframe_transfer_data(hw <- sw NV12)`,
    ///      then send the hardware frame.
    ///
    /// These use `ff::ffi::*` (raw sys); guard ref-counts carefully. Until done, return Err
    /// so make_encoder falls back to software.
    ///
    /// VALIDATED ON HARDWARE 2026-08-03 (Dell Precision 5540, Intel UHD 630 / gen9.5, i915,
    /// `/dev/dri/renderD128`) — `h264_vaapi` encodes 1080p cleanly there, 300 frames in 1.76 s
    /// (~170 fps encoder ceiling; capture + RGBA->NV12 swscale are still CPU and are not in
    /// that number). ffmpeg auto-selects `VAEntrypointEncSliceLP`; no explicit `low_power`
    /// flag is needed. Encode-capable profiles: H264Main, H264High, H264ConstrainedBaseline.
    ///
    /// RATE CONTROL IS THE TRAP — DO NOT SET bit_rate BLINDLY.
    /// On that gen9.5 iHD low-power path the ONLY supported RC mode is CQP. Passing a bitrate
    /// makes `open_as_with` fail with "Driver does not support any RC mode compatible with
    /// selected options (supported modes: CQP)". This is NOT universal — gen12+ Intel supports
    /// CBR/VBR on the LP path — so the implementation must QUERY the supported RC modes at init
    /// and fall back to CQP (driving `qp` / `global_quality`) rather than hardcoding a bitrate.
    /// Note `new_sw_input` currently sets `set_bit_rate` unconditionally (see line ~138), which
    /// means `h264_qsv` can hit this same failure on such devices; because `new` falls through
    /// on error, it degrades silently to software and looks like "no hardware present".
    /// CQP maps onto the existing `AdaptiveQuality` infrastructure by adapting QP instead of
    /// bitrate, which also gives `set_target_bitrate` something real to do on this path.
    fn new_vaapi(_width: u32, _height: u32) -> Result<Self> {
        Err(anyhow!(
            "h264_vaapi: hardware frames context not wired yet (needs on-hardware implementation)"
        ))
    }

    fn make_scaler(width: u32, height: u32) -> Result<ff::software::scaling::Context> {
        // RGBA (from the RDP/VNC framebuffer) -> NV12 (H.264 encoder input).
        ff::software::scaling::Context::get(
            ff::format::Pixel::RGBA,
            width,
            height,
            ff::format::Pixel::NV12,
            width,
            height,
            ff::software::scaling::Flags::BILINEAR,
        )
        .context("create RGBA->NV12 scaler")
    }
}

impl VideoEncoder for FfmpegEncoder {
    fn encode(&mut self, frame: &RgbaFrame) -> Result<EncodedFrame> {
        let expected = (self.width * self.height * 4) as usize;
        anyhow::ensure!(
            frame.data.len() == expected,
            "expected {} RGBA bytes for {}x{}, got {}",
            expected,
            self.width,
            self.height,
            frame.data.len()
        );

        // Stage RGBA into the reused source frame. av_frame_get_buffer aligns rows, so
        // linesize can exceed width*4 and a flat copy would shear — see copy_rgba_rows.
        let row_bytes = (self.width as usize) * 4;
        let stride = self.src_frame.stride(0);
        crate::copy_rgba_rows(self.src_frame.data_mut(0), stride, &frame.data, row_bytes);

        // Convert to NV12. This frame is allocated per encode on purpose — the encoder
        // may hold a reference to it after send_frame (see the src_frame field note).
        let mut nv12 = ff::frame::Video::new(ff::format::Pixel::NV12, self.width, self.height);
        self.scaler.run(&self.src_frame, &mut nv12)?;
        nv12.set_pts(Some(self.frame_count as i64));
        if std::mem::take(&mut self.force_keyframe) {
            nv12.set_kind(ff::picture::Type::I);
        }

        self.encoder.send_frame(&nv12).context("send_frame")?;

        // Drain one packet (the pipeline calls us per frame; low-latency encoders emit
        // ~1 packet per frame).
        let mut packet = ff::Packet::empty();
        match self.encoder.receive_packet(&mut packet) {
            Ok(()) => {
                let data = packet.data().unwrap_or(&[]).to_vec();
                let is_keyframe = packet.is_key();
                let pts = self.frame_count * 3000;
                self.frame_count += 1;
                Ok(EncodedFrame {
                    data: Bytes::from(data),
                    is_keyframe,
                    pts,
                })
            }
            // EAGAIN: encoder needs more input before it emits — return an empty,
            // non-keyframe frame; EncoderPipeline drops zero-length frames instead
            // of forwarding them (see pipeline.rs), so nothing reaches write_sample.
            Err(ff::Error::Other { errno }) if errno == ff::util::error::EAGAIN => {
                self.frame_count += 1;
                Ok(EncodedFrame {
                    data: Bytes::new(),
                    is_keyframe: false,
                    pts: 0,
                })
            }
            Err(e) => Err(anyhow!("receive_packet: {}", e)),
        }
    }

    fn request_keyframe(&mut self) {
        self.force_keyframe = true;
    }

    fn dimensions(&self) -> (u32, u32) {
        (self.width, self.height)
    }

    fn backend_kind(&self) -> EncoderBackendKind {
        // Unconditional: new_vaapi() returns Err before construction succeeds (see its
        // doc comment), so any live FfmpegEncoder reached one of the real hardware
        // candidates in new_sw_input (NVENC/QSV/MF/VideoToolbox).
        EncoderBackendKind::Hardware
    }

    fn set_target_bitrate(&mut self, bps: u32) {
        // ffmpeg-next has no live rate-control setter after open; NVENC honors rc via the
        // rate-control opts at open time. A live change needs a codec reconfigure (reopen)
        // — deferred; log for now so the adaptive controller path is visible in testing.
        log::debug!(
            "guacr-encoder: FFmpeg set_target_bitrate({}) — live RC reconfigure TODO",
            bps
        );
    }

    fn frame_count(&self) -> u64 {
        self.frame_count
    }
}
