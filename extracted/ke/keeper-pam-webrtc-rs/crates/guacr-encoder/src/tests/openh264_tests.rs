use crate::{openh264_backend::OpenH264Encoder, RgbaFrame, VideoEncoder};

fn solid_frame(width: u32, height: u32, ts: u64) -> RgbaFrame {
    RgbaFrame {
        data: vec![0x80u8; (width * height * 4) as usize],
        width,
        height,
        timestamp_us: ts,
    }
}

#[test]
fn encoder_constructs() {
    OpenH264Encoder::new(320, 240).unwrap();
}

#[test]
fn encode_returns_non_empty_bytes() {
    let mut enc = OpenH264Encoder::new(320, 240).unwrap();
    assert!(!enc
        .encode(&solid_frame(320, 240, 0))
        .unwrap()
        .data
        .is_empty());
}

#[test]
fn first_frame_is_keyframe() {
    let mut enc = OpenH264Encoder::new(320, 240).unwrap();
    assert!(enc.encode(&solid_frame(320, 240, 0)).unwrap().is_keyframe);
}

#[test]
fn request_keyframe_forces_idr() {
    let mut enc = OpenH264Encoder::new(320, 240).unwrap();
    enc.encode(&solid_frame(320, 240, 0)).unwrap();
    enc.encode(&solid_frame(320, 240, 1)).unwrap();
    enc.request_keyframe();
    assert!(enc.encode(&solid_frame(320, 240, 2)).unwrap().is_keyframe);
}

#[test]
fn frame_count_increments() {
    let mut enc = OpenH264Encoder::new(320, 240).unwrap();
    assert_eq!(enc.frame_count(), 0);
    enc.encode(&solid_frame(320, 240, 0)).unwrap();
    assert_eq!(enc.frame_count(), 1);
}

#[test]
fn pts_advances_by_3000_per_frame() {
    let mut enc = OpenH264Encoder::new(320, 240).unwrap();
    let f0 = enc.encode(&solid_frame(320, 240, 0)).unwrap();
    let f1 = enc.encode(&solid_frame(320, 240, 1)).unwrap();
    assert_eq!(f0.pts, 0);
    assert_eq!(f1.pts, 3000);
}

#[test]
fn set_target_bitrate_does_not_panic() {
    let mut enc = OpenH264Encoder::new(320, 240).unwrap();
    enc.set_target_bitrate(500_000);
    enc.set_target_bitrate(8_000_000);
    enc.encode(&solid_frame(320, 240, 0)).unwrap();
}

#[test]
fn wrong_size_frame_returns_error() {
    let mut enc = OpenH264Encoder::new(320, 240).unwrap();
    let bad = RgbaFrame {
        data: vec![0u8; 100],
        width: 320,
        height: 240,
        timestamp_us: 0,
    };
    assert!(enc.encode(&bad).is_err());
}

/// A gradient (not a solid color) exercises every distinct byte value the alpha-strip loop
/// copies, so a transposed R/G/B channel or an off-by-one chunk offset would show up as a
/// gross color-plane error rather than being masked by uniform input.
#[test]
fn encode_gradient_frame_succeeds() {
    let (width, height) = (64u32, 64u32);
    let mut data = vec![0u8; (width * height * 4) as usize];
    for (i, px) in data.chunks_exact_mut(4).enumerate() {
        px[0] = (i % 256) as u8; // R
        px[1] = ((i / 2) % 256) as u8; // G
        px[2] = ((i / 3) % 256) as u8; // B
        px[3] = 255; // A — must be ignored by the strip step, not encoded
    }
    let frame = RgbaFrame {
        data,
        width,
        height,
        timestamp_us: 0,
    };
    let mut enc = OpenH264Encoder::new(width, height).unwrap();
    assert!(!enc.encode(&frame).unwrap().data.is_empty());
}

/// Structured high-frequency content (fine checkerboard + a moving band) — unlike
/// `solid_frame` this needs real bits to encode, but unlike literal per-pixel-independent
/// noise it has the spatial/temporal correlation H.264's block-based prediction can
/// actually exploit. Per-pixel-independent noise was tried first and rejected: it defeats
/// rate control at any QP (there's a bit-cost floor per macroblock even at max QP=51), so
/// it doesn't distinguish "rate control works" from "content is information-theoretically
/// incompressible" — a real screen-content proxy is needed to test the former honestly.
fn checkerboard_frame(width: u32, height: u32, frame_idx: u64) -> RgbaFrame {
    let (w, h) = (width as usize, height as usize);
    let mut data = vec![0u8; w * h * 4];
    let band = (frame_idx % 32) as i64;
    for y in 0..h {
        for x in 0..w {
            let i = (y * w + x) * 4;
            let checker = (((x / 6) + (y / 6)) % 2) as u8;
            let base = if checker == 0 { 30u8 } else { 210u8 };
            let diag = ((x as i64 + y as i64) % 64 - band).unsigned_abs();
            data[i] = if diag < 10 { 255 } else { base };
            data[i + 1] = base;
            data[i + 2] = if checker == 0 { 200 } else { 40 };
            data[i + 3] = 255;
        }
    }
    RgbaFrame {
        data,
        width,
        height,
        timestamp_us: frame_idx,
    }
}

/// `set_target_bitrate` must actually constrain output size. Two independent bugs
/// combined to make it decorative before this, both measured live on a Precision 5540
/// (2026-08-04) and reproduced locally:
/// (1) OpenH264 itself warns that bitrate control does not function in
///     `RC_QUALITY_MODE`/`RC_BITRATE_MODE`/`RC_TIMESTAMP_MODE` without `skip_frames`
///     enabled — the crate's previous defaults (`RateControlMode::Quality`,
///     `skip_frames(false)`) overshot target bitrate by 3.5-5x regardless of resolution
///     or content.
/// (2) Independently, calling `set_target_bitrate` (raw `ENCODER_OPTION_BITRATE`) before
///     the encoder's first `encode()` call is silently ineffective — measured: identical
///     config, calling it before vs. after a warm-up encode took a 100kbps target from
///     ~3-4x overshoot (untracked) to within ~17% (tracked). This is why the warm-up
///     encode below is not incidental — it reproduces how `EncoderPipeline` now always
///     calls it (see `pipeline.rs`'s `encoder_is_warm` guard, which defers a pending
///     bitrate change by one frame after construction/rebuild rather than dropping it).
#[test]
fn set_target_bitrate_actually_constrains_output_size() {
    let (width, height) = (128u32, 128u32);
    let mut enc = OpenH264Encoder::new(width, height).unwrap();
    enc.encode(&checkerboard_frame(width, height, 999)).unwrap();
    let target_bps: u32 = 100_000;
    enc.set_target_bitrate(target_bps);

    let fps = 30u64;
    let frames = 30u64;
    let mut total_bytes = 0u64;
    for i in 0..frames {
        let f = enc.encode(&checkerboard_frame(width, height, i)).unwrap();
        total_bytes += f.data.len() as u64;
    }
    let achieved_bps = total_bytes * 8 * fps / frames;
    assert!(
        achieved_bps < u64::from(target_bps) * 2,
        "target bitrate not honoured: wanted ~{target_bps}bps, got {achieved_bps}bps"
    );
}

/// The alpha-strip step must reuse its RGB8 scratch buffer, not allocate one per frame —
/// same discipline as the pooled input/output buffers elsewhere in the pipeline. A stable
/// pointer across repeated `encode()` calls is direct proof the buffer never reallocates.
#[test]
fn rgb_scratch_buffer_is_never_reallocated_across_frames() {
    let mut enc = OpenH264Encoder::new(64, 64).unwrap();
    let ptr0 = enc.rgb_scratch_ptr();
    for i in 0..5 {
        enc.encode(&solid_frame(64, 64, i)).unwrap();
        assert_eq!(
            enc.rgb_scratch_ptr(),
            ptr0,
            "rgb_scratch reallocated on frame {i}"
        );
    }
}
