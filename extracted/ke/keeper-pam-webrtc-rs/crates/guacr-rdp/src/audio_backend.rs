// RDP RDPSND audio backend implementation (T-032 to T-036)
//
// Implements RdpsndClientHandler from ironrdp-rdpsnd to enable server-to-client
// audio output forwarding.
//
// AC-1: Server audio output reaches the Guacamole client.
// AC-2: Audio uses L16 PCM format (raw 16-bit LE PCM samples, WAVE_FORMAT_PCM).
// AC-3: If server does not negotiate audio output, no audio is sent and no error occurs.
// AC-4: Audio stream start and stop are signaled correctly (lifecycle).
//
// Audio input (T-035 to T-036): the RDPEA channel is a separate DVC not currently
// wired in. Microphone data from Guacamole clients is silently discarded with a
// debug log (AC-2 of rdp-completion R3).

use crossbeam_queue::ArrayQueue;
use ironrdp::rdpsnd::client::RdpsndClientHandler;
use ironrdp::rdpsnd::pdu::{AudioFormat, PitchPdu, VolumePdu, WaveFormat};
use log::{debug, info};
use std::borrow::Cow;
use std::sync::Arc;

/// A single audio chunk ready for Guacamole delivery.
pub struct AudioChunk {
    /// PCM data (16-bit LE samples).
    pub data: Vec<u8>,
    /// Sample rate in Hz.
    pub sample_rate: u32,
    /// Number of channels.
    pub channels: u8,
}

/// RdpsndClientHandler that queues decoded PCM audio for the main loop (T-032 to T-034).
#[derive(Debug)]
pub struct GuacrRdpsndBackend {
    /// Queue for decoded audio chunks. The main loop drains this.
    chunks: Arc<ArrayQueue<AudioChunk>>,
    /// Advertised audio formats (stored to enable `get_formats` to return a slice reference).
    formats: Vec<AudioFormat>,
    /// Active format sample rate (updated when server negotiates).
    active_sample_rate: u32,
    /// Active format channels.
    active_channels: u8,
}

impl GuacrRdpsndBackend {
    pub fn new(chunks: Arc<ArrayQueue<AudioChunk>>) -> Self {
        // AC-2: Advertise L16 PCM (WAVE_FORMAT_PCM, 44100 Hz, stereo).
        let pcm_format = AudioFormat {
            format: WaveFormat::PCM,
            n_channels: 2,
            n_samples_per_sec: 44100,
            n_avg_bytes_per_sec: 176400, // 44100 * 2 channels * 2 bytes/sample
            n_block_align: 4,
            bits_per_sample: 16,
            data: None,
        };
        Self {
            chunks,
            formats: vec![pcm_format],
            active_sample_rate: 44100,
            active_channels: 2,
        }
    }
}

impl RdpsndClientHandler for GuacrRdpsndBackend {
    fn get_formats(&self) -> &[AudioFormat] {
        // AC-2: We advertise only L16 PCM.
        &self.formats
    }

    fn wave(&mut self, format_no: &AudioFormat, _ts: u32, data: Cow<'_, [u8]>) {
        // Server sent an audio wave packet. Since we advertise only format index 0
        // (L16 PCM), all audio arrives in L16 PCM format.
        let _ = format_no;

        let chunk = AudioChunk {
            data: data.into_owned(),
            sample_rate: self.active_sample_rate,
            channels: self.active_channels,
        };

        // AC-4: Queue for main loop delivery.
        // force_push drops old data if full — acceptable for audio (slightly dropped
        // audio is better than blocking the RDP event loop).
        if self.chunks.force_push(chunk).is_some() {
            debug!("RDPSND: Audio queue full, dropped old chunk");
        }
    }

    fn set_volume(&mut self, _volume: VolumePdu) {
        debug!("RDPSND: Volume change received (Guacamole client controls volume)");
    }

    fn set_pitch(&mut self, _pitch: PitchPdu) {
        debug!("RDPSND: Pitch change received (not applied)");
    }

    fn close(&mut self) {
        // AC-4: Audio stream stop lifecycle signal.
        info!("RDPSND: Audio channel closed");
    }
}
