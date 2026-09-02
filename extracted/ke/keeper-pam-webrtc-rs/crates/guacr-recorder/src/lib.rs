// guacr-recorder: fMP4 muxing + ZMQ PAIR streaming to Python gateway.
//
// Architecture: Rust produces raw unencrypted fMP4 fragments and streams them
// to Python via a ZMQ PAIR socket. Python's RecordingReader applies AES-GCM
// encryption and uploads to krouter. Rust stays out of crypto entirely.
//
// One ZmqVideoSink per video session (RDP/VNC/RBI). For terminal sessions
// (SSH/Telnet/DB), ZmqRecordingSender from guacr-recording handles asciicast.

pub mod mp4;
pub mod zmq_video_sink;

pub use mp4::Fmp4Writer;
pub use zmq_video_sink::ZmqVideoSink;

#[cfg(test)]
mod tests;
