// ZMQ video recording sink.
//
// Muxes H.264 frames into fMP4 fragments and sends raw (unencrypted) bytes
// to Python via a ZMQ PAIR socket. Python's RecordingReader applies AES-GCM
// and uploads to krouter.
//
// One ZmqVideoSink per session. Call finalize() at session end — the socket
// close signals end-of-recording to Python.

use guacr_handlers::EncodedFrame;
use guacr_recording::zmq_transport::ZmqRecordingSender;
use guacr_recording::RecordingError;

use crate::mp4::Fmp4Writer;

/// Raw fMP4 video recording sink over ZMQ PAIR.
pub struct ZmqVideoSink {
    writer: Fmp4Writer,
    sender: ZmqRecordingSender,
}

impl ZmqVideoSink {
    /// Create a new sink connecting to `addr` (Python's ZMQProxy frontend).
    pub async fn new(
        addr: &str,
        width: u32,
        height: u32,
        allow_unrecorded: bool,
    ) -> Result<Self, RecordingError> {
        let writer = Fmp4Writer::new(width, height);
        let sender = ZmqRecordingSender::connect(addr, allow_unrecorded)?;
        Ok(Self { writer, sender })
    }

    /// Write an encoded H.264 frame. On the first IDR, sends the fMP4 init segment first.
    pub async fn write_video_frame(&mut self, frame: &EncodedFrame) -> Result<(), RecordingError> {
        let annex_b = frame.data.as_ref();
        let pts_90khz = frame.pts; // already in 90kHz clock units

        // On first IDR, send init segment (ftyp + moov).
        if frame.is_keyframe && !self.writer.is_initialized() {
            if let Some(init) = self.writer.init_segment(annex_b) {
                self.send_bytes(&init)?;
            }
        }

        // Prepare and send the video fragment.
        if let Some(mp4_frame) = self
            .writer
            .prepare_frame(annex_b, pts_90khz, frame.is_keyframe)
        {
            let fragment = self.writer.write_video_fragment(&mp4_frame);
            self.send_bytes(&fragment)?;
        }

        Ok(())
    }

    /// Write a Guacamole input instruction to the fMP4 data track.
    pub async fn write_input_event(
        &mut self,
        instruction: &str,
        timestamp_ms: u64,
    ) -> Result<(), RecordingError> {
        let events = vec![(timestamp_ms, instruction.to_string())];
        let fragment = self.writer.write_data_fragment(&events);
        self.send_bytes(&fragment)
    }

    /// Finalize the recording: close the ZMQ socket (signals end-of-recording to Python).
    pub async fn finalize(self) -> Result<(), RecordingError> {
        self.sender.close();
        Ok(())
    }

    fn send_bytes(&self, bytes: &[u8]) -> Result<(), RecordingError> {
        self.sender.send(bytes)
    }
}
