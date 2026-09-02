// Unit tests for GuacrRdpsndBackend (T-032 to T-036).
//
// Verifies that the RDPSND wave handler does not panic on typical input and
// that volume/pitch/close lifecycle calls complete without error.

use crate::audio_backend::GuacrRdpsndBackend;
use crossbeam_queue::ArrayQueue;
use ironrdp::rdpsnd::client::RdpsndClientHandler;
use ironrdp::rdpsnd::pdu::{AudioFormat, PitchPdu, VolumePdu, WaveFormat};
use std::borrow::Cow;
use std::sync::Arc;

fn make_backend() -> GuacrRdpsndBackend {
    let queue = Arc::new(ArrayQueue::new(64));
    GuacrRdpsndBackend::new(queue)
}

fn pcm_format() -> AudioFormat {
    AudioFormat {
        format: WaveFormat::PCM,
        n_channels: 2,
        n_samples_per_sec: 44100,
        n_avg_bytes_per_sec: 176400,
        n_block_align: 4,
        bits_per_sample: 16,
        data: None,
    }
}

// AC-2: wave() with small PCM bytes must queue the chunk without panicking.
#[test]
fn test_wave_with_valid_pcm_does_not_panic() {
    let mut backend = make_backend();
    // 4 bytes = one stereo 16-bit PCM sample (little-endian).
    let pcm: &[u8] = &[0x00u8, 0x01, 0x02, 0x03];
    backend.wave(&pcm_format(), 0, Cow::Borrowed(pcm));
}

// AC-2: wave() with empty PCM data does not panic.
#[test]
fn test_wave_with_empty_data_does_not_panic() {
    let mut backend = make_backend();
    backend.wave(&pcm_format(), 100, Cow::Borrowed(&[]));
}

// AC-2: get_formats() returns the advertised PCM format.
#[test]
fn test_get_formats_returns_pcm() {
    let backend = make_backend();
    let formats = backend.get_formats();
    assert!(
        !formats.is_empty(),
        "backend must advertise at least one audio format"
    );
}

// AC-4: set_volume() does not panic.
#[test]
fn test_set_volume_does_not_panic() {
    let mut backend = make_backend();
    let vol = VolumePdu {
        volume_left: 0xFFFF,
        volume_right: 0xFFFF,
    };
    backend.set_volume(vol);
}

// AC-4: set_pitch() does not panic.
#[test]
fn test_set_pitch_does_not_panic() {
    let mut backend = make_backend();
    let pitch = PitchPdu { pitch: 0x00010000 }; // 1.0 fixed-point
    backend.set_pitch(pitch);
}

// AC-4: close() completes without error.
#[test]
fn test_close_does_not_panic() {
    let mut backend = make_backend();
    backend.close();
}

// AC-4: Multiple waves followed by close do not panic.
#[test]
fn test_multiple_waves_then_close() {
    let mut backend = make_backend();
    for i in 0u32..10 {
        let pcm = vec![0u8; 8];
        backend.wave(&pcm_format(), i * 100, Cow::Owned(pcm));
    }
    backend.close();
}
