//! Times `FfmpegEncoder::new` on the process's **main thread**, outside the cargo-test harness.
//!
//! Diagnostic for the ~195 s `avcodec_open2` cost measured on macOS/h264_videotoolbox
//! (2026-08-03). Under `cargo test` the open takes ~195 s regardless of private options or
//! time_base (both hypotheses tested and disproven), while ffmpeg's own CLI performs an
//! equivalent open in under a second. The remaining difference is process context: test
//! functions run on spawned threads with no macOS app context, and VideoToolbox session
//! creation may degrade there. If this example is fast, the slowness is a test-harness
//! artifact rather than a production problem — which matters because production ships the
//! Linux wheel, where VideoToolbox does not exist.
//!
//! Run:
//!   PKG_CONFIG_PATH=/opt/homebrew/opt/ffmpeg@7/lib/pkgconfig \
//!     cargo run -p guacr-encoder --features ffmpeg --example open_timing

fn main() {
    #[cfg(not(feature = "ffmpeg"))]
    {
        eprintln!("build with --features ffmpeg");
    }

    #[cfg(feature = "ffmpeg")]
    {
        use std::time::Instant;

        let (w, h) = (1280u32, 720u32);
        println!(
            "candidates: {:?}",
            guacr_encoder::ffmpeg_backend::hw_encoder_candidates()
        );

        let t = Instant::now();
        let probed = guacr_encoder::ffmpeg_backend::probe();
        println!(
            "probe()                {:>10.2?}  (compiled in: {probed})",
            t.elapsed()
        );

        let t = Instant::now();
        let enc = guacr_encoder::ffmpeg_backend::FfmpegEncoder::new(w, h);
        println!(
            "FfmpegEncoder::new     {:>10.2?}  (ok: {})",
            t.elapsed(),
            enc.is_ok()
        );
        if let Err(e) = &enc {
            println!("  error: {e}");
        }

        let t = Instant::now();
        let _any = guacr_encoder::make_encoder(w, h).expect("make_encoder must always succeed");
        println!("make_encoder()         {:>10.2?}", t.elapsed());
    }
}
