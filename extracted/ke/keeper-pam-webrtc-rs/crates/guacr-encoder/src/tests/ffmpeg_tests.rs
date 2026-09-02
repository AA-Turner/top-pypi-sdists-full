//! Tests for the FFmpeg hardware H.264 backend.
//!
//! `probe`/selection tests run anywhere the `ffmpeg` feature is built (they just assert no
//! panic and correct fallback). The actual encode roundtrip is `#[ignore]` — it needs a real
//! GPU (VAAPI device or NVENC), so it runs only on target hardware:
//!   cargo test -p guacr-encoder --features ffmpeg -- --ignored ffmpeg_encode
//!
//! VERIFIED on macOS/VideoToolbox 2026-08-03 — the roundtrip passes against the Apple media
//! engine (`brew install ffmpeg@7`, then `PKG_CONFIG_PATH=/opt/homebrew/opt/ffmpeg@7/lib/pkgconfig`).
//! Still unverified for NVENC (implemented, never run by our code) and VAAPI (`new_vaapi` is
//! an `Err` stub, so nothing to verify until it is written).
//!
//! CAUTION: `ffmpeg_encode_roundtrip_hw` uses 1280x720, where `stride == row_bytes`, so it
//! does NOT exercise the aligned-row copy path — that is why the stride shear survived it.
//! `tests/stride_tests.rs` covers the padded case on every build instead.

use crate::ffmpeg_backend;
use crate::{make_encoder, RgbaFrame, VideoEncoder};

/// probe() must never panic and returns whether any FFmpeg H.264 HW encoder is compiled in.
#[test]
fn ffmpeg_probe_does_not_panic() {
    let _ = ffmpeg_backend::probe();
}

/// Per-phase construction timings. Originally written to chase an alarming ~194 s
/// `open_as_with`, which turned out to be a **cargo-test harness artifact on macOS**: the
/// identical code takes ~742 ms on the process main thread via
/// `examples/open_timing.rs`. Keep this for attribution when construction looks slow, but
/// measure real numbers with the example — timings taken under `cargo test` are misleading
/// for VideoToolbox. Run with:
///   PKG_CONFIG_PATH=/opt/homebrew/opt/ffmpeg@7/lib/pkgconfig \
///     cargo test -p guacr-encoder --features ffmpeg --lib -- --ignored --nocapture ffmpeg_open_phase
#[test]
#[ignore = "diagnostic: prints per-phase timings for FfmpegEncoder construction"]
fn ffmpeg_open_phase_timings() {
    use ffmpeg_next as ff;
    use std::time::Instant;

    macro_rules! phase {
        ($label:expr, $body:expr) => {{
            let t = Instant::now();
            let out = $body;
            println!("  {:<34} {:>8.2?}", $label, t.elapsed());
            out
        }};
    }

    let (w, h) = (1280u32, 720u32);
    phase!("ff::init()", {
        let _ = ff::init();
    });
    let name = ffmpeg_backend::hw_encoder_candidates()
        .first()
        .copied()
        .unwrap_or("h264_videotoolbox");
    println!("  candidate: {name}");

    let codec = phase!("find_by_name", ff::encoder::find_by_name(name));
    let Some(codec) = codec else {
        println!("  encoder not compiled in; nothing to time");
        return;
    };

    let ctx = phase!("Context::new_with_codec", {
        ff::codec::context::Context::new_with_codec(codec)
    });
    let mut enc = phase!(
        "ctx.encoder().video()",
        ctx.encoder().video().expect("video")
    );

    phase!("setters", {
        enc.set_width(w);
        enc.set_height(h);
        enc.set_format(ff::format::Pixel::NV12);
        enc.set_time_base((1, 90_000));
        enc.set_frame_rate(Some((30, 1)));
        let bps = crate::initial_bitrate_bps(w, h, 30) as usize;
        enc.set_bit_rate(bps);
        enc.set_max_bit_rate(bps * 2);
        enc.set_gop(120);
        enc.set_max_b_frames(0);
        enc.set_flags(ff::codec::Flags::LOW_DELAY);
    });

    let opened = phase!("open_as_with  <-- suspect", {
        enc.open_as_with(codec, ff::Dictionary::new())
    });
    assert!(opened.is_ok(), "open failed: {:?}", opened.err());

    phase!("make_scaler (sws_getContext)", {
        ff::software::scaling::Context::get(
            ff::format::Pixel::RGBA,
            w,
            h,
            ff::format::Pixel::NV12,
            w,
            h,
            ff::software::scaling::Flags::BILINEAR,
        )
        .expect("scaler")
    });
}

/// make_encoder must always yield *some* encoder — FFmpeg HW when a device is present,
/// otherwise the software (openh264) fallback. Never an error on a supported build.
#[test]
fn make_encoder_always_succeeds_with_fallback() {
    let enc = make_encoder(1280, 720);
    assert!(
        enc.is_ok(),
        "make_encoder must fall back to software, got {:?}",
        enc.err()
    );
}

/// On-hardware encode roundtrip: a solid-color RGBA frame must produce H.264 output, and the
/// first frame must be a keyframe (IDR). Ignored in CI — requires a GPU.
#[test]
#[ignore = "requires a VAAPI or NVENC capable GPU"]
fn ffmpeg_encode_roundtrip_hw() {
    if !ffmpeg_backend::probe() {
        eprintln!("no FFmpeg HW encoder compiled in; skipping");
        return;
    }
    let (w, h) = (1280u32, 720u32);
    let mut enc = match ffmpeg_backend::FfmpegEncoder::new(w, h) {
        Ok(e) => e,
        Err(e) => {
            eprintln!("no usable HW device ({e}); skipping");
            return;
        }
    };
    let frame = RgbaFrame {
        data: vec![0x40u8; (w * h * 4) as usize],
        width: w,
        height: h,
        timestamp_us: 0,
    };
    enc.request_keyframe();
    // Low-latency encoders may need a couple of feeds before the first packet drains.
    let mut got = None;
    for _ in 0..5 {
        let out = enc.encode(&frame).expect("encode");
        if !out.data.is_empty() {
            got = Some(out);
            break;
        }
    }
    let out = got.expect("HW encoder produced no H.264 output after 5 frames");
    assert!(!out.data.is_empty(), "expected H.264 bytes");
    assert!(out.is_keyframe, "first emitted frame should be a keyframe");
}

/// No platform may advertise an encoder whose constructor is a stub.
///
/// `probe()` answers on name presence alone, and `encode_resolution_cap()` (guacr-rdp) gates the
/// 4K-vs-1080p resolution ceiling on `probe()`. So listing an unimplemented encoder makes an
/// Intel/AMD Linux box claim hardware, take the 4K ceiling, then fall through to *software* at
/// 4K (~7 fps) — strictly worse than never claiming hardware at all.
///
/// Checked across every platform list, not just the host's, so a regression is caught on any
/// build rather than only on Linux CI.
#[test]
fn no_platform_advertises_an_unimplemented_encoder() {
    for candidates in ffmpeg_backend::all_platform_hw_encoders() {
        for name in *candidates {
            assert!(
                !ffmpeg_backend::unimplemented_encoders().contains(name),
                "{name} is listed as a hardware candidate but its constructor is a stub; \
                 probe() would report hardware that can never open, and the RDP resolution \
                 ceiling would rise to 4K while encoding actually falls back to software"
            );
        }
    }
}
